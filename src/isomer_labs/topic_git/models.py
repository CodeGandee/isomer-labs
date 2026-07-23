"""Typed state and schema-validated support files for Topic Git."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from importlib.resources import files
import json
from pathlib import Path
import re
from typing import Mapping
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

from isomer_labs.core.path_utils import canonicalize, is_within


TOPIC_GIT_SUPPORT_DIRECTORY = "topic-git"
TOPIC_GIT_COPY_SUPPORT_DIRECTORY = ".isomer/topic-git"
TOPIC_GIT_SCHEMA_VERSION = "isomer-topic-git.v1"
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_GIT_SHA_RE = re.compile(r"^[0-9a-f]{7,64}$")
_FORBIDDEN_FIELD_NAMES = {
    "api_key",
    "credential",
    "credentials",
    "password",
    "private_diff",
    "private_key",
    "raw_private_diff",
    "secret",
    "secret_value",
    "sensitive_excerpt",
    "source_git_config",
    "token",
}


class LocalTrackingState(StrEnum):
    DISABLED = "disabled"
    ENABLED = "enabled"
    INVALID = "invalid"


class PublicationState(StrEnum):
    DISABLED = "disabled"
    PREPARED = "prepared"
    SYNCHRONIZED = "synchronized"
    STALE = "stale"
    COPY_MISSING = "copy-missing"
    BLOCKED = "blocked"


class PrivacyDisposition(StrEnum):
    TRACK = "track"
    TEMPLATE = "template"
    EXCLUDE = "exclude"
    COMPONENT = "component"
    BLOCK = "block"


class RemoteVisibility(StrEnum):
    PRIVATE = "private"
    RESTRICTED = "restricted"
    PUBLIC = "public"
    UNKNOWN = "unknown"


class ComponentKind(StrEnum):
    TOPIC_MAIN = "topic-main"
    TOPIC_ACTOR = "topic-actor"
    AGENT = "agent"


class ComponentSelection(StrEnum):
    SELECTED = "selected"
    EXCLUDED = "excluded"
    UNAVAILABLE = "unavailable"
    BLOCKED = "blocked"


class BranchOutcomeStatus(StrEnum):
    PENDING = "pending"
    FETCHED = "fetched"
    PUSHED = "pushed"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"


class SupportFileKind(StrEnum):
    LOCAL_STATE = "local-state"
    LOCAL_PLAN = "local-plan"
    PUBLICATION_BINDING = "publication-binding"
    PUBLICATION_PLAN = "publication-plan"
    PROJECTION_MANIFEST = "projection-manifest"
    PUBLICATION_OUTCOMES = "publication-outcomes"


@dataclass(frozen=True)
class ComponentBinding:
    component_id: str
    kind: ComponentKind
    name: str
    relative_path: str
    branch: str
    selection: ComponentSelection
    commit_sha: str | None = None
    reason: str | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "component_id": self.component_id,
            "kind": self.kind.value,
            "name": self.name,
            "relative_path": self.relative_path,
            "branch": self.branch,
            "selection": self.selection.value,
        }
        if self.commit_sha is not None:
            data["commit_sha"] = self.commit_sha
        if self.reason is not None:
            data["reason"] = self.reason
        return data


@dataclass(frozen=True)
class PublicationConflict:
    relative_path: str
    reason: str
    source_fingerprint: str | None = None
    prior_output_fingerprint: str | None = None
    current_output_fingerprint: str | None = None
    resolution: str | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "relative_path": self.relative_path,
            "reason": self.reason,
        }
        for key, value in (
            ("source_fingerprint", self.source_fingerprint),
            ("prior_output_fingerprint", self.prior_output_fingerprint),
            ("current_output_fingerprint", self.current_output_fingerprint),
            ("resolution", self.resolution),
        ):
            if value is not None:
                data[key] = value
        return data


@dataclass(frozen=True)
class BranchOutcome:
    branch: str
    status: BranchOutcomeStatus
    observed_remote_commit: str | None = None
    replacement_commit: str | None = None
    pushed_commit: str | None = None
    diagnostic: str | None = None
    safe_resume: bool = True

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "branch": self.branch,
            "status": self.status.value,
            "safe_resume": self.safe_resume,
        }
        for key, value in (
            ("observed_remote_commit", self.observed_remote_commit),
            ("replacement_commit", self.replacement_commit),
            ("pushed_commit", self.pushed_commit),
            ("diagnostic", self.diagnostic),
        ):
            if value is not None:
                data[key] = value
        return data


@dataclass(frozen=True)
class PublicationBinding:
    binding_id: str
    research_topic_id: str
    topic_workspace_id: str
    copy_path: str
    remote_name: str
    remote_url: str
    visibility: RemoteVisibility
    created_at: str

    def to_json(self) -> dict[str, object]:
        return {
            "schema_version": "isomer-topic-git-publication-binding.v1",
            "binding_id": self.binding_id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "copy_path": self.copy_path,
            "remote_name": self.remote_name,
            "remote_url": self.remote_url,
            "visibility": self.visibility.value,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class TopicGitStatus:
    local: LocalTrackingState
    publication: PublicationState
    local_blockers: tuple[str, ...] = ()
    publication_blockers: tuple[str, ...] = ()
    local_next_actions: tuple[str, ...] = ()
    publication_next_actions: tuple[str, ...] = ()

    def to_json(self) -> dict[str, object]:
        return {
            "local": {
                "state": self.local.value,
                "blockers": list(self.local_blockers),
                "next_actions": list(self.local_next_actions),
            },
            "publication": {
                "state": self.publication.value,
                "blockers": list(self.publication_blockers),
                "next_actions": list(self.publication_next_actions),
            },
        }


def runtime_support_root(topic_runtime: Path) -> Path:
    """Return the namespaced Topic Git support root below a validated runtime."""

    return canonicalize(topic_runtime) / TOPIC_GIT_SUPPORT_DIRECTORY


def copy_support_root(publication_copy: Path) -> Path:
    """Return the ignored pre-runtime support root inside a publication copy."""

    return canonicalize(publication_copy) / Path(TOPIC_GIT_COPY_SUPPORT_DIRECTORY)


def validate_support_payload(kind: SupportFileKind, payload: Mapping[str, object]) -> tuple[str, ...]:
    """Validate a support payload and reject credential or private-content fields."""

    schema = _load_schema(kind)
    diagnostics = [
        f"{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(Draft202012Validator(schema).iter_errors(dict(payload)), key=str)
    ]
    diagnostics.extend(_sensitive_payload_diagnostics(payload))
    return tuple(diagnostics)


def write_support_file(
    path: Path,
    *,
    support_root: Path,
    kind: SupportFileKind,
    payload: Mapping[str, object],
) -> Path:
    """Validate and atomically write one support file inside its approved root."""

    resolved_root = canonicalize(support_root)
    resolved_path = canonicalize(path)
    if not is_within(resolved_path, resolved_root):
        raise ValueError("Topic Git support file must stay inside the approved support root.")
    if resolved_path.name == "state.sqlite":
        raise ValueError("Topic Git never writes Workspace Runtime state.sqlite.")
    diagnostics = validate_support_payload(kind, payload)
    if diagnostics:
        raise ValueError("Invalid Topic Git support payload: " + "; ".join(diagnostics))
    resolved_root.mkdir(parents=True, exist_ok=True)
    resolved_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = resolved_path.with_name(f".{resolved_path.name}.tmp")
    temporary_path.write_text(
        json.dumps(dict(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary_path.replace(resolved_path)
    return resolved_path


def load_support_file(path: Path, *, kind: SupportFileKind) -> dict[str, object]:
    """Load and validate a Topic Git support file."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Topic Git support file root must be an object.")
    diagnostics = validate_support_payload(kind, payload)
    if diagnostics:
        raise ValueError("Invalid Topic Git support payload: " + "; ".join(diagnostics))
    return payload


def promote_publication_binding(
    *,
    publication_copy: Path,
    topic_runtime: Path,
    expected_binding_id: str,
    approved_mutation: bool,
) -> Path:
    """Promote a validated copy-local binding during an approved publication mutation."""

    if not approved_mutation:
        raise ValueError("Read-only status cannot promote Topic Git publication state.")
    source_root = copy_support_root(publication_copy)
    payload = load_support_file(
        source_root / "publication-binding.json",
        kind=SupportFileKind.PUBLICATION_BINDING,
    )
    if payload.get("binding_id") != expected_binding_id:
        raise ValueError("Copy-local publication binding identity does not match the approved mutation.")
    destination_root = runtime_support_root(topic_runtime)
    return write_support_file(
        destination_root / "publication-binding.json",
        support_root=destination_root,
        kind=SupportFileKind.PUBLICATION_BINDING,
        payload=payload,
    )


def valid_fingerprint(value: str | None) -> bool:
    return value is None or _SHA256_RE.fullmatch(value) is not None


def valid_git_sha(value: str | None) -> bool:
    return value is None or _GIT_SHA_RE.fullmatch(value) is not None


def _schema_filename(kind: SupportFileKind) -> str:
    return f"{kind.value}.v1.schema.json"


def _load_schema(kind: SupportFileKind) -> dict[str, object]:
    schema_path = files("isomer_labs.topic_git.schemas").joinpath(_schema_filename(kind))
    payload = json.loads(schema_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Topic Git schema {_schema_filename(kind)} is not an object.")
    return payload


def _sensitive_payload_diagnostics(value: object, path: tuple[str, ...] = ()) -> list[str]:
    diagnostics: list[str] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = str(key).lower().replace("-", "_")
            child_path = (*path, str(key))
            if normalized in _FORBIDDEN_FIELD_NAMES or normalized.endswith(("_password", "_secret", "_token")):
                diagnostics.append(f"{'.'.join(child_path)}: sensitive fields are forbidden")
            diagnostics.extend(_sensitive_payload_diagnostics(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            diagnostics.extend(_sensitive_payload_diagnostics(child, (*path, str(index))))
    elif isinstance(value, str):
        parsed = urlsplit(value)
        if parsed.scheme in {"http", "https", "ssh"} and (
            parsed.password is not None or parsed.query or parsed.fragment
        ):
            diagnostics.append(f"{'.'.join(path)}: credential-bearing or signed URLs are forbidden")
    return diagnostics
