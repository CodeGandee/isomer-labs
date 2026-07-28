"""Typed state and schema-validated support files for Topic Git."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import hashlib
from importlib.resources import files
import json
from pathlib import Path
import re
from typing import Mapping
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

from isomer_labs.core.path_utils import canonicalize, is_within
from isomer_labs.topic_git.history_models import PublicationRefUpdateStrategy


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


class ProjectionEntryOrigin(StrEnum):
    SOURCE = "source"
    GENERATED = "generated"


class PublicationContentClass(StrEnum):
    INTENT = "intent"
    ENVIRONMENT = "environment"
    RESEARCH_RECORD = "research-record"
    TOPIC_COMPONENT = "topic-component"
    REFERENCE_REPOSITORY = "reference-repository"
    RAW_MATERIAL = "raw-material"
    RAW_EXPERIMENT_OUTPUT = "raw-experiment-output"
    PRIVATE_RUNTIME = "private-runtime"
    OTHER = "other"


class RemoteVisibility(StrEnum):
    PRIVATE = "private"
    RESTRICTED = "restricted"
    PUBLIC = "public"
    UNKNOWN = "unknown"


class PublicationSnapshotMode(StrEnum):
    EXCLUSIVE_SNAPSHOT = "exclusive_snapshot"


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
    DELETED = "deleted"


class PublicationRefKind(StrEnum):
    BRANCH = "branch"
    TAG = "tag"
    REMOTE_HEAD = "remote-head"


class PublicationRefOperation(StrEnum):
    UPDATE = "update"
    DELETE = "delete"
    OBSERVE = "observe"
    PROVIDER_ACTION = "provider-action"


class SupportFileKind(StrEnum):
    LOCAL_STATE = "local-state"
    LOCAL_PLAN = "local-plan"
    PUBLICATION_BINDING = "publication-binding"
    PUBLICATION_PLAN = "publication-plan"
    PROJECTION_MANIFEST = "projection-manifest"
    PUBLICATION_OUTCOMES = "publication-outcomes"


@dataclass(frozen=True)
class PublicationSelectionSettings:
    include_raw_material_bytes: bool = False
    include_raw_experiment_output_bytes: bool = False

    def to_json(self) -> dict[str, object]:
        return {
            "include_raw_material_bytes": self.include_raw_material_bytes,
            "include_raw_experiment_output_bytes": self.include_raw_experiment_output_bytes,
        }


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
    git_anchor_component_id: str | None = None

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
        if self.git_anchor_component_id is not None:
            data["git_anchor_component_id"] = self.git_anchor_component_id
        return data

    @classmethod
    def from_json(cls, payload: Mapping[str, object]) -> ComponentBinding:
        """Load current or legacy component metadata."""

        return cls(
            component_id=str(payload["component_id"]),
            kind=ComponentKind(str(payload["kind"])),
            name=str(payload["name"]),
            relative_path=str(payload["relative_path"]),
            branch=str(payload["branch"]),
            selection=ComponentSelection(str(payload["selection"])),
            commit_sha=str(payload["commit_sha"]) if payload.get("commit_sha") is not None else None,
            reason=str(payload["reason"]) if payload.get("reason") is not None else None,
            git_anchor_component_id=(
                str(payload["git_anchor_component_id"])
                if payload.get("git_anchor_component_id") is not None
                else None
            ),
        )


@dataclass(frozen=True)
class ReferenceRepositoryBinding:
    reference_id: str
    semantic_label: str
    relative_path: str
    remote_url: str
    commit_sha: str
    visibility: RemoteVisibility
    selection: ComponentSelection = ComponentSelection.SELECTED
    license_status: str | None = None
    access_limitation: str | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "reference_id": self.reference_id,
            "semantic_label": self.semantic_label,
            "relative_path": self.relative_path,
            "remote_url": self.remote_url,
            "commit_sha": self.commit_sha,
            "visibility": self.visibility.value,
            "selection": self.selection.value,
        }
        if self.license_status is not None:
            data["license_status"] = self.license_status
        if self.access_limitation is not None:
            data["access_limitation"] = self.access_limitation
        return data

    @classmethod
    def from_json(cls, payload: Mapping[str, object]) -> ReferenceRepositoryBinding:
        """Load a reference binding from tracked projection metadata."""

        return cls(
            reference_id=str(payload["reference_id"]),
            semantic_label=str(payload["semantic_label"]),
            relative_path=str(payload["relative_path"]),
            remote_url=str(payload["remote_url"]),
            commit_sha=str(payload["commit_sha"]),
            visibility=RemoteVisibility(str(payload["visibility"])),
            selection=ComponentSelection(str(payload.get("selection", ComponentSelection.SELECTED.value))),
            license_status=str(payload["license_status"]) if payload.get("license_status") is not None else None,
            access_limitation=(
                str(payload["access_limitation"])
                if payload.get("access_limitation") is not None
                else None
            ),
        )


@dataclass(frozen=True)
class ResearchRecordIndexEntry:
    record_ref: str
    semantic_id: str
    state: str
    fingerprint: str
    revision: str | None = None
    relationships: tuple[str, ...] = ()

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "record_ref": self.record_ref,
            "semantic_id": self.semantic_id,
            "state": self.state,
            "fingerprint": self.fingerprint,
            "relationships": list(self.relationships),
        }
        if self.revision is not None:
            data["revision"] = self.revision
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
class PublicationRefOutcome:
    ref: str
    kind: PublicationRefKind
    operation: PublicationRefOperation
    status: BranchOutcomeStatus
    observed_commit: str | None = None
    expected_commit: str | None = None
    resulting_commit: str | None = None
    diagnostic: str | None = None
    safe_resume: bool = True
    strategy: PublicationRefUpdateStrategy | None = None
    base_commit: str | None = None
    observed_lease: str | None = None
    fallback_used: bool = False
    verified: bool = False

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "ref": self.ref,
            "kind": self.kind.value,
            "operation": self.operation.value,
            "status": self.status.value,
            "safe_resume": self.safe_resume,
            "fallback_used": self.fallback_used,
            "verified": self.verified,
        }
        for key, value in (
            ("strategy", self.strategy.value if self.strategy is not None else None),
            ("base_commit", self.base_commit),
            ("observed_lease", self.observed_lease),
            ("observed_commit", self.observed_commit),
            ("expected_commit", self.expected_commit),
            ("resulting_commit", self.resulting_commit),
            ("diagnostic", self.diagnostic),
        ):
            if value is not None:
                data[key] = value
        return data

    @classmethod
    def from_json(cls, payload: Mapping[str, object]) -> PublicationRefOutcome:
        strategy = payload.get("strategy")
        return cls(
            ref=str(payload["ref"]),
            kind=PublicationRefKind(str(payload["kind"])),
            operation=PublicationRefOperation(str(payload["operation"])),
            status=BranchOutcomeStatus(str(payload["status"])),
            observed_commit=(
                str(payload["observed_commit"])
                if payload.get("observed_commit") is not None
                else None
            ),
            expected_commit=(
                str(payload["expected_commit"])
                if payload.get("expected_commit") is not None
                else None
            ),
            resulting_commit=(
                str(payload["resulting_commit"])
                if payload.get("resulting_commit") is not None
                else None
            ),
            diagnostic=(
                str(payload["diagnostic"])
                if payload.get("diagnostic") is not None
                else None
            ),
            safe_resume=bool(payload.get("safe_resume", True)),
            strategy=(
                PublicationRefUpdateStrategy(str(strategy))
                if strategy is not None
                else None
            ),
            base_commit=(
                str(payload["base_commit"])
                if payload.get("base_commit") is not None
                else None
            ),
            observed_lease=(
                str(payload["observed_lease"])
                if payload.get("observed_lease") is not None
                else None
            ),
            fallback_used=bool(payload.get("fallback_used", False)),
            verified=bool(payload.get("verified", False)),
        )


@dataclass(frozen=True)
class PublicationSnapshotOutcome:
    binding_id: str
    plan_id: str
    ref_outcomes: tuple[PublicationRefOutcome, ...]
    resume_at: str | None
    updated_at: str
    observed_remote_head: str | None = None
    provider_default_branch_action_required: bool = False

    def to_json(self) -> dict[str, object]:
        return {
            "schema_version": "isomer-topic-git-publication-outcomes.v3",
            "binding_id": self.binding_id,
            "plan_id": self.plan_id,
            "ref_outcomes": [outcome.to_json() for outcome in self.ref_outcomes],
            "resume_at": self.resume_at,
            "observed_remote_head": self.observed_remote_head,
            "provider_default_branch_action_required": self.provider_default_branch_action_required,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_json(cls, payload: Mapping[str, object]) -> PublicationSnapshotOutcome:
        raw_outcomes = payload.get("ref_outcomes")
        return cls(
            binding_id=str(payload["binding_id"]),
            plan_id=str(payload["plan_id"]),
            ref_outcomes=(
                tuple(
                    PublicationRefOutcome.from_json(outcome)
                    for outcome in raw_outcomes
                    if isinstance(outcome, Mapping)
                )
                if isinstance(raw_outcomes, list)
                else ()
            ),
            resume_at=(
                str(payload["resume_at"])
                if payload.get("resume_at") is not None
                else None
            ),
            updated_at=str(payload["updated_at"]),
            observed_remote_head=(
                str(payload["observed_remote_head"])
                if payload.get("observed_remote_head") is not None
                else None
            ),
            provider_default_branch_action_required=bool(
                payload.get("provider_default_branch_action_required", False)
            ),
        )


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
    snapshot_mode: PublicationSnapshotMode | None = None
    canonical_branch: str = "main"

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "schema_version": "isomer-topic-git-publication-binding.v1",
            "binding_id": self.binding_id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "copy_path": self.copy_path,
            "remote_name": self.remote_name,
            "remote_url": self.remote_url,
            "visibility": self.visibility.value,
            "created_at": self.created_at,
            "canonical_branch": self.canonical_branch,
        }
        if self.snapshot_mode is not None:
            data["snapshot_mode"] = self.snapshot_mode.value
            data["authority_fingerprint"] = self.authority_fingerprint()
        return data

    def authority_fingerprint(self) -> str:
        """Bind exclusive authority to remote, topic, workspace, mode, and canonical branch."""

        payload = (
            self.remote_url.strip(),
            self.research_topic_id,
            self.topic_workspace_id,
            self.snapshot_mode.value if self.snapshot_mode is not None else None,
            self.canonical_branch,
        )
        return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()

    @classmethod
    def from_json(cls, payload: Mapping[str, object]) -> PublicationBinding:
        """Load current bindings while accepting pre-snapshot legacy bindings."""

        snapshot_mode = payload.get("snapshot_mode")
        return cls(
            binding_id=str(payload["binding_id"]),
            research_topic_id=str(payload["research_topic_id"]),
            topic_workspace_id=str(payload["topic_workspace_id"]),
            copy_path=str(payload["copy_path"]),
            remote_name=str(payload["remote_name"]),
            remote_url=str(payload["remote_url"]),
            visibility=RemoteVisibility(str(payload["visibility"])),
            created_at=str(payload["created_at"]),
            snapshot_mode=PublicationSnapshotMode(str(snapshot_mode)) if snapshot_mode is not None else None,
            canonical_branch=str(payload.get("canonical_branch", "main")),
        )


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

    schema = _load_schema(kind, payload)
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


def publication_plan_approval_is_stale(payload: Mapping[str, object]) -> bool:
    """Return whether stored approval predates history-aware plan semantics."""

    return payload.get("schema_version") != "isomer-topic-git-publication-plan.v2"


def _schema_filename(
    kind: SupportFileKind,
    payload: Mapping[str, object] | None = None,
) -> str:
    schema_version = str((payload or {}).get("schema_version", ""))
    versioned = {
        (
            SupportFileKind.PUBLICATION_PLAN,
            "isomer-topic-git-publication-plan.v2",
        ): "publication-plan.v2.schema.json",
        (
            SupportFileKind.PROJECTION_MANIFEST,
            "isomer-topic-git-projection-manifest.v3",
        ): "projection-manifest.v3.schema.json",
        (
            SupportFileKind.PUBLICATION_OUTCOMES,
            "isomer-topic-git-publication-outcomes.v3",
        ): "publication-outcomes.v3.schema.json",
    }
    selected = versioned.get((kind, schema_version))
    if selected is not None:
        return selected
    return f"{kind.value}.v1.schema.json"


def _load_schema(
    kind: SupportFileKind,
    payload: Mapping[str, object] | None = None,
) -> dict[str, object]:
    schema_filename = _schema_filename(kind, payload)
    schema_path = files("isomer_labs.topic_git.schemas").joinpath(schema_filename)
    payload = json.loads(schema_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Topic Git schema {schema_filename} is not an object.")
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
