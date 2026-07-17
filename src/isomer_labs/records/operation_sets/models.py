"""Models and strict manifest parsing for operation-set acceptance."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence
import hashlib
import json
import os
import tempfile

from isomer_labs.core.diagnostics import Diagnostic
from isomer_labs.records.store import ResearchRecordError

OPERATION_SET_MANIFEST_SCHEMA_VERSION = "isomer-operation-set-acceptance.v1"
OPERATION_SET_CONTROL_DIR = ".isomer-operation-set"
OPERATION_SET_DEFAULT_MANIFEST = "manifest.json"
OUTPUT_DISPOSITIONS = ("record_payload", "record_attachment", "disposable")
RECORD_ACTIONS = ("create", "revise", "reference")
_BUFFER_SIZE = 1024 * 1024


class OperationSetAcceptanceError(ResearchRecordError):
    """Deterministic operation-set acceptance error."""


@dataclass(frozen=True)
class OperationSetOutput:
    key: str
    path: str
    digest: str
    size_bytes: int
    media_type: str | None = None
    disposition: str | None = None
    record_key: str | None = None
    reason: str | None = None
    metadata: dict[str, object] = field(default_factory=dict)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "key": self.key,
            "path": self.path,
            "digest": self.digest,
            "size_bytes": self.size_bytes,
        }
        for key, value in (
            ("media_type", self.media_type),
            ("disposition", self.disposition),
            ("record_key", self.record_key),
            ("reason", self.reason),
        ):
            if value is not None:
                data[key] = value
        if self.metadata:
            data["metadata"] = self.metadata
        return data


@dataclass(frozen=True)
class OperationSetRecordIntent:
    key: str
    action: str
    record_id: str | None = None
    target_record_id: str | None = None
    record_kind: str | None = None
    status: str = "ready"
    semantic_id: str | None = None
    scope_key: str | None = None
    profile: str | None = None
    skill: str | None = None
    producer: str | None = None
    consumer: str | None = None
    semantic_label: str | None = None
    format_profile_ref: str | None = None
    schema_ref: str | None = None
    template_ref: str | None = None
    render_format: str | None = None
    content_name: str | None = None
    metadata: dict[str, object] = field(default_factory=dict)
    lifecycle_refs: dict[str, str] = field(default_factory=dict)
    relationships: list[dict[str, object]] = field(default_factory=list)
    parents: list[dict[str, object]] = field(default_factory=list)
    lineage_kind: str | None = None
    generation_id: str | None = None
    generation_purpose: str | None = None
    decision_record_id: str | None = None
    lineage_rationale: str | None = None
    index_hints: dict[str, object] = field(default_factory=dict)
    idea_effects: dict[str, object] | None = None
    idea_effects_required: bool = False
    root_reason: str | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {"key": self.key, "action": self.action, "status": self.status}
        for key, value in (
            ("record_id", self.record_id),
            ("target_record_id", self.target_record_id),
            ("record_kind", self.record_kind),
            ("semantic_id", self.semantic_id),
            ("scope_key", self.scope_key),
            ("profile", self.profile),
            ("skill", self.skill),
            ("producer", self.producer),
            ("consumer", self.consumer),
            ("semantic_label", self.semantic_label),
            ("format_profile_ref", self.format_profile_ref),
            ("schema_ref", self.schema_ref),
            ("template_ref", self.template_ref),
            ("render_format", self.render_format),
            ("content_name", self.content_name),
            ("lineage_kind", self.lineage_kind),
            ("generation_id", self.generation_id),
            ("generation_purpose", self.generation_purpose),
            ("decision_record_id", self.decision_record_id),
            ("lineage_rationale", self.lineage_rationale),
            ("root_reason", self.root_reason),
        ):
            if value is not None:
                data[key] = value
        for key, collection_value in (
            ("metadata", self.metadata),
            ("lifecycle_refs", self.lifecycle_refs),
            ("relationships", self.relationships),
            ("parents", self.parents),
            ("index_hints", self.index_hints),
        ):
            if collection_value:
                data[key] = collection_value
        if self.idea_effects is not None:
            data["idea_effects"] = self.idea_effects
        if self.idea_effects_required:
            data["idea_effects_required"] = True
        return data


@dataclass(frozen=True)
class OperationSetAcceptanceManifest:
    operation_set_id: str
    revision: int
    research_topic_id: str
    topic_workspace_id: str
    worker_kind: str
    worker_name: str
    outputs: tuple[OperationSetOutput, ...]
    record_intents: tuple[OperationSetRecordIntent, ...]
    producer_skill: str | None = None
    lifecycle_refs: dict[str, str] = field(default_factory=dict)
    supersedes_receipt_id: str | None = None
    metadata: dict[str, object] = field(default_factory=dict)
    schema_version: str = OPERATION_SET_MANIFEST_SCHEMA_VERSION

    @classmethod
    def from_json(cls, value: Mapping[str, object]) -> OperationSetAcceptanceManifest:
        _reject_unknown_keys(
            value,
            {
                "schema_version",
                "operation_set_id",
                "revision",
                "research_topic_id",
                "topic_workspace_id",
                "worker",
                "producer_skill",
                "lifecycle_refs",
                "supersedes_receipt_id",
                "outputs",
                "record_intents",
                "metadata",
            },
            "manifest",
        )
        schema_version = _required_string(value, "schema_version", "manifest")
        if schema_version != OPERATION_SET_MANIFEST_SCHEMA_VERSION:
            raise _manifest_error(
                "operation_set_manifest_version_unsupported",
                f"Unsupported operation-set manifest version: {schema_version}",
            )
        revision = value.get("revision")
        if isinstance(revision, bool) or not isinstance(revision, int) or revision < 1:
            raise _manifest_error("operation_set_manifest_revision_invalid", "manifest.revision must be a positive integer.")
        worker = _required_object(value, "worker", "manifest")
        _reject_unknown_keys(worker, {"kind", "name"}, "manifest.worker")
        worker_kind = _required_string(worker, "kind", "manifest.worker")
        if worker_kind not in {"agent", "topic_actor"}:
            raise _manifest_error("operation_set_worker_kind_unsupported", f"Unsupported worker kind: {worker_kind}")
        outputs_raw = _required_object_list(value, "outputs", "manifest")
        intents_raw = _required_object_list(value, "record_intents", "manifest")
        outputs = tuple(sorted((_parse_output(item, index) for index, item in enumerate(outputs_raw)), key=lambda item: item.key))
        intents = tuple(sorted((_parse_intent(item, index) for index, item in enumerate(intents_raw)), key=lambda item: item.key))
        _require_unique((item.key for item in outputs), "output key", "operation_set_output_key_duplicate")
        _require_unique((item.path for item in outputs), "output path", "operation_set_output_path_duplicate")
        _require_unique((item.key for item in intents), "record intent key", "operation_set_intent_key_duplicate")
        return cls(
            schema_version=schema_version,
            operation_set_id=_required_string(value, "operation_set_id", "manifest"),
            revision=revision,
            research_topic_id=_required_string(value, "research_topic_id", "manifest"),
            topic_workspace_id=_required_string(value, "topic_workspace_id", "manifest"),
            worker_kind=worker_kind,
            worker_name=_required_string(worker, "name", "manifest.worker"),
            producer_skill=_optional_string_field(value, "producer_skill", "manifest"),
            lifecycle_refs=_string_map(value.get("lifecycle_refs"), "manifest.lifecycle_refs"),
            supersedes_receipt_id=_optional_string_field(value, "supersedes_receipt_id", "manifest"),
            outputs=outputs,
            record_intents=intents,
            metadata=_object(value.get("metadata"), "manifest.metadata"),
        )

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "schema_version": self.schema_version,
            "operation_set_id": self.operation_set_id,
            "revision": self.revision,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "worker": {"kind": self.worker_kind, "name": self.worker_name},
            "outputs": [item.to_json() for item in self.outputs],
            "record_intents": [item.to_json() for item in self.record_intents],
        }
        if self.producer_skill is not None:
            data["producer_skill"] = self.producer_skill
        if self.lifecycle_refs:
            data["lifecycle_refs"] = self.lifecycle_refs
        if self.supersedes_receipt_id is not None:
            data["supersedes_receipt_id"] = self.supersedes_receipt_id
        if self.metadata:
            data["metadata"] = self.metadata
        return data

    @property
    def digest(self) -> str:
        return canonical_json_digest(self.to_json())


@dataclass(frozen=True)
class OperationSetInventoryEntry:
    path: str
    digest: str
    size_bytes: int
    media_type: str | None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {"path": self.path, "digest": self.digest, "size_bytes": self.size_bytes}
        if self.media_type is not None:
            data["media_type"] = self.media_type
        return data


@dataclass(frozen=True)
class ResolvedOperationSet:
    root: Path
    output_root: Path
    worker_kind: str
    worker_name: str
    worker_scope_ref: str
    relative_path: str
    operation_set_id: str

    def to_json(self) -> dict[str, object]:
        return {
            "canonical_root": str(self.root),
            "worker_output_root": str(self.output_root),
            "worker_kind": self.worker_kind,
            "worker_name": self.worker_name,
            "worker_scope_ref": self.worker_scope_ref,
            "relative_path": self.relative_path,
            "operation_set_id": self.operation_set_id,
        }


def canonical_json_digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(_BUFFER_SIZE):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def load_operation_set_manifest(path: Path) -> OperationSetAcceptanceManifest:
    if not path.exists() or not path.is_file():
        raise _manifest_error("operation_set_manifest_missing", f"Operation-set manifest does not exist: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise _manifest_error("operation_set_manifest_invalid_json", f"Operation-set manifest is not valid UTF-8 JSON: {exc}") from exc
    if not isinstance(value, Mapping):
        raise _manifest_error("operation_set_manifest_not_object", "Operation-set manifest must be a JSON object.")
    return OperationSetAcceptanceManifest.from_json(value)


def write_operation_set_manifest(path: Path, manifest: OperationSetAcceptanceManifest) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write_text(path, json.dumps(manifest.to_json(), indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def _parse_output(value: Mapping[str, object], index: int) -> OperationSetOutput:
    location = f"manifest.outputs[{index}]"
    _reject_unknown_keys(value, {"key", "path", "digest", "size_bytes", "media_type", "disposition", "record_key", "reason", "metadata"}, location)
    path = _normalize_relative_path(_required_string(value, "path", location), location)
    size = value.get("size_bytes")
    if isinstance(size, bool) or not isinstance(size, int) or size < 0:
        raise _manifest_error("operation_set_output_size_invalid", f"{location}.size_bytes must be a non-negative integer.")
    digest = _required_string(value, "digest", location)
    if not _valid_sha256_digest(digest):
        raise _manifest_error("operation_set_output_digest_invalid", f"{location}.digest must be a sha256 digest.")
    disposition = _optional_string_field(value, "disposition", location)
    if disposition is not None and disposition not in OUTPUT_DISPOSITIONS:
        raise _manifest_error("operation_set_output_disposition_unsupported", f"Unsupported output disposition: {disposition}")
    return OperationSetOutput(
        key=_required_string(value, "key", location),
        path=path,
        digest=_normalize_digest(digest),
        size_bytes=size,
        media_type=_optional_string_field(value, "media_type", location),
        disposition=disposition,
        record_key=_optional_string_field(value, "record_key", location),
        reason=_optional_string_field(value, "reason", location),
        metadata=_object(value.get("metadata"), f"{location}.metadata"),
    )


def _parse_intent(value: Mapping[str, object], index: int) -> OperationSetRecordIntent:
    location = f"manifest.record_intents[{index}]"
    allowed = {
        "key", "action", "record_id", "target_record_id", "record_kind", "status", "semantic_id", "scope_key",
        "profile", "skill", "producer", "consumer", "semantic_label", "format_profile_ref", "schema_ref", "template_ref",
        "render_format", "content_name", "metadata", "lifecycle_refs", "relationships", "parents", "lineage_kind",
        "generation_id", "generation_purpose", "decision_record_id", "lineage_rationale", "index_hints", "idea_effects",
        "idea_effects_required", "root_reason",
    }
    _reject_unknown_keys(value, allowed, location)
    action = _required_string(value, "action", location)
    if action not in RECORD_ACTIONS:
        raise _manifest_error("operation_set_record_action_unsupported", f"Unsupported record intent action: {action}")
    required_effects = value.get("idea_effects_required", False)
    if not isinstance(required_effects, bool):
        raise _manifest_error("operation_set_idea_effects_required_invalid", f"{location}.idea_effects_required must be a boolean.")
    idea_effects_value = value.get("idea_effects")
    def optional(key: str) -> str | None:
        return _optional_string_field(value, key, location)
    parents = _object_list(value.get("parents"), f"{location}.parents")
    for parent_index, parent in enumerate(parents):
        _reject_unknown_keys(
            parent,
            {
                "record_id",
                "local_record_key",
                "lineage_kind",
                "kind",
                "parent_role",
                "role",
                "decision_record_id",
                "rationale",
                "status",
                "metadata",
            },
            f"{location}.parents[{parent_index}]",
        )
    return OperationSetRecordIntent(
        key=_required_string(value, "key", location),
        action=action,
        record_id=optional("record_id"),
        target_record_id=optional("target_record_id"),
        record_kind=optional("record_kind"),
        status=optional("status") or "ready",
        semantic_id=optional("semantic_id"),
        scope_key=optional("scope_key"),
        profile=optional("profile"),
        skill=optional("skill"),
        producer=optional("producer"),
        consumer=optional("consumer"),
        semantic_label=optional("semantic_label"),
        format_profile_ref=optional("format_profile_ref"),
        schema_ref=optional("schema_ref"),
        template_ref=optional("template_ref"),
        render_format=optional("render_format"),
        content_name=optional("content_name"),
        metadata=_object(value.get("metadata"), f"{location}.metadata"),
        lifecycle_refs=_string_map(value.get("lifecycle_refs"), f"{location}.lifecycle_refs"),
        relationships=_object_list(value.get("relationships"), f"{location}.relationships"),
        parents=parents,
        lineage_kind=optional("lineage_kind"),
        generation_id=optional("generation_id"),
        generation_purpose=optional("generation_purpose"),
        decision_record_id=optional("decision_record_id"),
        lineage_rationale=optional("lineage_rationale"),
        index_hints=_object(value.get("index_hints"), f"{location}.index_hints"),
        idea_effects=_object(idea_effects_value, f"{location}.idea_effects") if idea_effects_value is not None else None,
        idea_effects_required=required_effects,
        root_reason=optional("root_reason"),
    )


def _reject_unknown_keys(value: Mapping[str, object], allowed: set[str], location: str) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise _manifest_error("operation_set_manifest_unknown_field", f"{location} contains unsupported field(s): {', '.join(unknown)}")


def _required_string(value: Mapping[str, object], key: str, location: str) -> str:
    selected = _optional_string(value.get(key))
    if selected is None:
        raise _manifest_error("operation_set_manifest_field_missing", f"{location}.{key} must be a non-empty string.")
    return selected


def _optional_string(value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        return None
    selected = value.strip()
    return selected or None


def _optional_string_field(value: Mapping[str, object], key: str, location: str) -> str | None:
    if key not in value or value[key] is None:
        return None
    selected = value[key]
    if not isinstance(selected, str) or not selected.strip():
        raise _manifest_error(
            "operation_set_manifest_field_invalid",
            f"{location}.{key} must be a non-empty string when provided.",
        )
    return selected.strip()


def _required_object(value: Mapping[str, object], key: str, location: str) -> dict[str, object]:
    selected = value.get(key)
    if not isinstance(selected, Mapping):
        raise _manifest_error("operation_set_manifest_field_invalid", f"{location}.{key} must be an object.")
    return {str(item_key): item_value for item_key, item_value in selected.items()}


def _object(value: object, location: str) -> dict[str, object]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise _manifest_error("operation_set_manifest_field_invalid", f"{location} must be an object.")
    return {str(key): item for key, item in value.items()}


def _required_object_list(value: Mapping[str, object], key: str, location: str) -> list[dict[str, object]]:
    if key not in value:
        raise _manifest_error("operation_set_manifest_field_missing", f"{location}.{key} is required.")
    return _object_list(value.get(key), f"{location}.{key}")


def _object_list(value: object, location: str) -> list[dict[str, object]]:
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(item, Mapping) for item in value):
        raise _manifest_error("operation_set_manifest_field_invalid", f"{location} must be an array of objects.")
    return [{str(key): item_value for key, item_value in item.items()} for item in value]


def _string_map(value: object, location: str) -> dict[str, str]:
    selected = _object(value, location)
    if any(not isinstance(item, str) for item in selected.values()):
        raise _manifest_error("operation_set_manifest_field_invalid", f"{location} must contain only string values.")
    return {key: str(item) for key, item in selected.items()}


def _require_unique(values: Sequence[str] | Any, label: str, code: str) -> None:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    if duplicates:
        raise _manifest_error(code, f"Duplicate {label}(s): {', '.join(sorted(duplicates))}")


def _normalize_relative_path(value: str, location: str) -> str:
    if "\\" in value:
        raise _manifest_error("operation_set_path_invalid", f"{location}.path must use forward slashes.")
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise _manifest_error("operation_set_path_escape", f"{location}.path must be a normalized relative path without traversal.")
    normalized = path.as_posix()
    if normalized == OPERATION_SET_CONTROL_DIR or normalized.startswith(f"{OPERATION_SET_CONTROL_DIR}/"):
        raise _manifest_error("operation_set_control_path_reserved", f"{location}.path points inside the reserved coordinator directory.")
    return normalized


def _valid_sha256_digest(value: str) -> bool:
    normalized = value.removeprefix("sha256:")
    return len(normalized) == 64 and all(character in "0123456789abcdefABCDEF" for character in normalized)


def _normalize_digest(value: str) -> str:
    return f"sha256:{value.removeprefix('sha256:').lower()}"


def _manifest_error(code: str, message: str, **details: object) -> OperationSetAcceptanceError:
    payload: dict[str, object] = {}
    if details:
        payload["details"] = details
    return OperationSetAcceptanceError(message, code=code, payload=payload)


def _diagnostic(code: str, message: str, *, path: Path | None = None) -> Diagnostic:
    return Diagnostic(code=code, severity="error", concept="Operation Set Acceptance", path=path, message=message)


def _item_diagnostic(code: str, message: str, **details: object) -> dict[str, object]:
    return {"severity": "error", "code": code, "message": message, **{key: str(value) if isinstance(value, Path) else value for key, value in details.items()}}


def _has_item_errors(diagnostics: Sequence[Mapping[str, object]]) -> bool:
    return any(item.get("severity") == "error" for item in diagnostics)


def _context_failure_payload(operation: str, diagnostics: Sequence[Diagnostic]) -> dict[str, Any]:
    return {
        "ok": False,
        "mutated": False,
        "operation": operation,
        "error": {"code": "operation_set_context_resolution_failed", "message": "Operation-set worker context could not be resolved."},
        "diagnostics": [item.to_json() for item in diagnostics],
    }


def _atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, staged_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".staged", dir=path.parent)
    staged = Path(staged_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(staged, path)
    finally:
        staged.unlink(missing_ok=True)
def _output_summary(manifest: OperationSetAcceptanceManifest) -> dict[str, object]:
    counts = {disposition: sum(1 for item in manifest.outputs if item.disposition == disposition) for disposition in OUTPUT_DISPOSITIONS}
    return {
        "total": len(manifest.outputs),
        "dispositions": counts,
        "record_intents": len(manifest.record_intents),
        "disposable_reasons": {item.path: item.reason for item in manifest.outputs if item.disposition == "disposable"},
    }
