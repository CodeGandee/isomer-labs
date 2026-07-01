"""Extension-backed research record CRUD over Workspace Runtime."""

from __future__ import annotations

from dataclasses import dataclass, replace
import json
from pathlib import Path
import shutil
from typing import Any, Mapping
import uuid

from isomer_labs.diagnostics import Diagnostic, has_errors
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.paths import resolve_semantic_path
from isomer_labs.runtime.identifiers import _provenance_ref, _slug
from isomer_labs.runtime.models import LIFECYCLE_RECORD_KINDS, LIFECYCLE_STATUSES, RuntimeLifecycleRecord, utc_timestamp
from isomer_labs.runtime.store import open_workspace_runtime


RESEARCH_RECORD_DEFAULT_LABELS = {
    "run": "topic.records.runs",
    "research_task": "topic.records.tasks",
    "workflow_stage_cursor": "topic.records.views",
    "view_manifest": "topic.records.views",
}
DEFAULT_RECORD_LABEL = "topic.records.artifacts"


class ResearchRecordError(Exception):
    """Deterministic research-record extension error."""

    def __init__(self, message: str, *, code: str = "research_record_error", payload: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.payload = payload or {}

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "ok": False,
            "error": {
                "code": self.code,
                "message": self.message,
            },
        }
        payload.update(self.payload)
        return payload


@dataclass(frozen=True)
class ResearchRecordRequest:
    record_kind: str
    record_id: str | None = None
    status: str = "ready"
    placeholder: str | None = None
    profile: str | None = None
    skill: str | None = None
    producer: str | None = None
    consumer: str | None = None
    semantic_label: str | None = None
    body: str | None = None
    body_file: Path | None = None
    content_name: str | None = None
    metadata: dict[str, object] | None = None
    lifecycle_refs: dict[str, str] | None = None


def create_record(
    context: EffectiveTopicContext,
    request: ResearchRecordRequest,
    *,
    env: Mapping[str, str],
    cwd: Path,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """Create a generic research record in Workspace Runtime."""

    _validate_record_kind(request.record_kind)
    _validate_status(request.status)
    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    if runtime_store is None:
        return _runtime_missing_payload("create", diagnostics), diagnostics
    try:
        content_path, body_diagnostics = _write_body(context, request, env=env, cwd=cwd)
        diagnostics.extend(body_diagnostics)
        if has_errors(diagnostics):
            return _diagnostic_payload("create", diagnostics), diagnostics
        now = utc_timestamp()
        record_id = request.record_id or _new_record_id(request)
        metadata = _record_metadata(request)
        metadata["created_by"] = "isomer-cli ext research records create"
        if content_path is not None:
            metadata["content_semantic_label"] = _semantic_label_for_request(request)
        lifecycle_refs = _lifecycle_refs(context, request)
        record = RuntimeLifecycleRecord(
            id=record_id,
            record_kind=request.record_kind,
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            status=request.status,
            created_at=now,
            updated_at=now,
            lifecycle_refs=lifecycle_refs,
            transition_metadata=metadata,
            content_path=str(content_path) if content_path is not None else None,
            provenance_refs=[_provenance_ref(request.record_kind, record_id)],
        )
        with runtime_store.connection:
            runtime_store.upsert_lifecycle_record(record)
        stored = runtime_store.get_lifecycle_record(record_id) or record
        return {
            "ok": True,
            "mutated": True,
            "operation": "create",
            "record": stored.to_json(),
            "content_path": str(content_path) if content_path is not None else None,
        }, diagnostics
    finally:
        runtime_store.close()


def show_record(
    context: EffectiveTopicContext,
    record_id: str,
    *,
    env: Mapping[str, str],
    include_body: bool = False,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """Show one research record."""

    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if runtime_store is None:
        return _runtime_missing_payload("show", diagnostics), diagnostics
    try:
        record = runtime_store.get_lifecycle_record(record_id)
        if record is None or not _belongs_to_context(record, context):
            raise ResearchRecordError(f"Research record not found: {record_id}", code="record_not_found")
        payload: dict[str, Any] = {
            "ok": True,
            "mutated": False,
            "operation": "show",
            "record": record.to_json(),
        }
        if include_body:
            payload["body"] = _read_record_body(record)
        return payload, diagnostics
    finally:
        runtime_store.close()


def list_records(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    record_kind: str | None = None,
    status: str | None = None,
    placeholder: str | None = None,
    profile: str | None = None,
    skill: str | None = None,
    producer: str | None = None,
    consumer: str | None = None,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """List research records matching filters."""

    if record_kind is not None:
        _validate_record_kind(record_kind)
    if status is not None:
        _validate_status(status)
    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if runtime_store is None:
        return _runtime_missing_payload("list", diagnostics), diagnostics
    try:
        records = [
            record
            for record in runtime_store.list_lifecycle_records()
            if _belongs_to_context(record, context)
            and _matches_filter(record, "record_kind", record_kind)
            and _matches_filter(record, "status", status)
            and _matches_metadata(record, "placeholder", placeholder)
            and _matches_metadata(record, "profile", profile)
            and _matches_metadata(record, "skill", skill)
            and _matches_metadata(record, "producer", producer)
            and _matches_metadata(record, "consumer", consumer)
        ]
        return {
            "ok": True,
            "mutated": False,
            "operation": "list",
            "count": len(records),
            "records": [record.to_json() for record in records],
        }, diagnostics
    finally:
        runtime_store.close()


def update_record(
    context: EffectiveTopicContext,
    record_id: str,
    request: ResearchRecordRequest,
    *,
    env: Mapping[str, str],
    cwd: Path,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """Update a research record while preserving identity."""

    _validate_record_kind(request.record_kind)
    _validate_status(request.status)
    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    if runtime_store is None:
        return _runtime_missing_payload("update", diagnostics), diagnostics
    try:
        existing = runtime_store.get_lifecycle_record(record_id)
        if existing is None or not _belongs_to_context(existing, context):
            raise ResearchRecordError(f"Research record not found: {record_id}", code="record_not_found")
        if existing.record_kind != request.record_kind:
            raise ResearchRecordError(
                f"Record kind mismatch for {record_id}: existing {existing.record_kind}, requested {request.record_kind}.",
                code="record_kind_mismatch",
            )
        content_path, body_diagnostics = _write_body(context, replace(request, record_id=record_id), env=env, cwd=cwd)
        diagnostics.extend(body_diagnostics)
        if has_errors(diagnostics):
            return _diagnostic_payload("update", diagnostics), diagnostics
        metadata = dict(existing.transition_metadata)
        metadata.update(_record_metadata(request))
        metadata["updated_by"] = "isomer-cli ext research records update"
        metadata["updated_at"] = utc_timestamp()
        next_lifecycle_refs = dict(existing.lifecycle_refs)
        next_lifecycle_refs.update(_lifecycle_refs(context, request))
        updated = RuntimeLifecycleRecord(
            **{
                **existing.__dict__,
                "status": request.status,
                "updated_at": str(metadata["updated_at"]),
                "lifecycle_refs": next_lifecycle_refs,
                "transition_metadata": metadata,
                "content_path": str(content_path) if content_path is not None else existing.content_path,
            }
        )
        with runtime_store.connection:
            runtime_store.upsert_lifecycle_record(updated)
        stored = runtime_store.get_lifecycle_record(record_id) or updated
        return {
            "ok": True,
            "mutated": True,
            "operation": "update",
            "record": stored.to_json(),
            "content_path": stored.content_path,
        }, diagnostics
    finally:
        runtime_store.close()


def archive_record(
    context: EffectiveTopicContext,
    record_id: str,
    *,
    env: Mapping[str, str],
    reason: str | None = None,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """Archive a research record without removing durable body files."""

    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    if runtime_store is None:
        return _runtime_missing_payload("delete", diagnostics), diagnostics
    try:
        existing = runtime_store.get_lifecycle_record(record_id)
        if existing is None or not _belongs_to_context(existing, context):
            raise ResearchRecordError(f"Research record not found: {record_id}", code="record_not_found")
        now = utc_timestamp()
        metadata = dict(existing.transition_metadata)
        metadata.update(
            {
                "archived_by": "isomer-cli ext research records delete",
                "archived_at": now,
                "delete_mode": "archive",
            }
        )
        if reason:
            metadata["archive_reason"] = reason
        archived = RuntimeLifecycleRecord(
            **{
                **existing.__dict__,
                "status": "archived",
                "updated_at": now,
                "transition_metadata": metadata,
            }
        )
        with runtime_store.connection:
            runtime_store.upsert_lifecycle_record(archived)
        stored = runtime_store.get_lifecycle_record(record_id) or archived
        return {
            "ok": True,
            "mutated": True,
            "operation": "delete",
            "delete_mode": "archive",
            "record": stored.to_json(),
        }, diagnostics
    finally:
        runtime_store.close()


def _validate_record_kind(record_kind: str) -> None:
    if record_kind not in LIFECYCLE_RECORD_KINDS:
        raise ResearchRecordError(f"Unsupported research record kind: {record_kind}", code="unsupported_record_kind")


def _validate_status(status: str) -> None:
    if status not in LIFECYCLE_STATUSES:
        raise ResearchRecordError(f"Unsupported research record status: {status}", code="unsupported_record_status")


def _write_body(
    context: EffectiveTopicContext,
    request: ResearchRecordRequest,
    *,
    env: Mapping[str, str],
    cwd: Path,
) -> tuple[Path | None, list[Diagnostic]]:
    if request.body is None and request.body_file is None:
        return None, []
    if request.body is not None and request.body_file is not None:
        raise ResearchRecordError("Use either --body or --body-file, not both.", code="body_source_conflict")
    label = _semantic_label_for_request(request)
    result, diagnostics = resolve_semantic_path(context, label, env=env, cwd=cwd)
    if result is None:
        return None, diagnostics
    target_dir = result.path / "research-records" / request.record_kind
    target_dir.mkdir(parents=True, exist_ok=True)
    source_suffix = ""
    if request.body_file is not None:
        if not request.body_file.exists() or not request.body_file.is_file():
            raise ResearchRecordError(f"Body file does not exist: {request.body_file}", code="body_file_missing")
        source_suffix = request.body_file.suffix
    filename = _content_filename(request, suffix=source_suffix or ".md")
    target = target_dir / filename
    if request.body_file is not None:
        shutil.copyfile(request.body_file, target)
    else:
        target.write_text(request.body or "", encoding="utf-8")
    return target.resolve(strict=False), diagnostics


def _semantic_label_for_request(request: ResearchRecordRequest) -> str:
    return request.semantic_label or RESEARCH_RECORD_DEFAULT_LABELS.get(request.record_kind, DEFAULT_RECORD_LABEL)


def _content_filename(request: ResearchRecordRequest, *, suffix: str) -> str:
    if request.content_name:
        name = request.content_name
        return name if Path(name).suffix else f"{name}{suffix}"
    stem_source = request.placeholder or request.profile or request.record_id or request.record_kind
    record_id = request.record_id or uuid.uuid4().hex[:12]
    return f"{_slug(stem_source)}-{_slug(record_id)}{suffix}"


def _new_record_id(request: ResearchRecordRequest) -> str:
    stem = request.placeholder or request.profile or request.record_kind
    return f"{_slug(request.record_kind)}-{_slug(stem)}-{uuid.uuid4().hex[:12]}"


def _record_metadata(request: ResearchRecordRequest) -> dict[str, object]:
    metadata: dict[str, object] = dict(request.metadata or {})
    for key, value in (
        ("placeholder", request.placeholder),
        ("profile", request.profile),
        ("skill", request.skill),
        ("producer", request.producer),
        ("consumer", request.consumer),
        ("semantic_label", _semantic_label_for_request(request)),
    ):
        if value is not None:
            metadata[key] = value
    return metadata


def _lifecycle_refs(context: EffectiveTopicContext, request: ResearchRecordRequest) -> dict[str, str]:
    refs = dict(context.lifecycle_refs)
    if context.topic_agent_team_profile_id is not None:
        refs.setdefault("topic_agent_team_profile_id", context.topic_agent_team_profile_id)
    for key, value in (request.lifecycle_refs or {}).items():
        refs[str(key)] = str(value)
    return refs


def _belongs_to_context(record: RuntimeLifecycleRecord, context: EffectiveTopicContext) -> bool:
    return record.research_topic_id == context.research_topic.id and record.topic_workspace_id == context.topic_workspace_id


def _matches_filter(record: RuntimeLifecycleRecord, field: str, value: str | None) -> bool:
    return value is None or getattr(record, field) == value


def _matches_metadata(record: RuntimeLifecycleRecord, key: str, value: str | None) -> bool:
    if value is None:
        return True
    return str(record.transition_metadata.get(key) or "") == value


def _read_record_body(record: RuntimeLifecycleRecord) -> str | None:
    if record.content_path is None:
        return None
    path = Path(record.content_path)
    if not path.exists() or not path.is_file():
        return None
    return path.read_text(encoding="utf-8", errors="replace")


def _runtime_missing_payload(operation: str, diagnostics: list[Diagnostic]) -> dict[str, Any]:
    return {
        "ok": False,
        "mutated": False,
        "operation": operation,
        "error": {
            "code": "workspace_runtime_missing",
            "message": "Workspace Runtime must be initialized before research records can be stored.",
        },
        "diagnostics": [diagnostic.to_json() for diagnostic in diagnostics],
    }


def _diagnostic_payload(operation: str, diagnostics: list[Diagnostic]) -> dict[str, Any]:
    return {
        "ok": False,
        "mutated": False,
        "operation": operation,
        "error": {
            "code": "diagnostics_failed",
            "message": "Research record operation failed preflight diagnostics.",
        },
        "diagnostics": [diagnostic.to_json() for diagnostic in diagnostics],
    }


def parse_json_object(raw: str | None, *, field_name: str) -> dict[str, object]:
    if raw is None or not raw.strip():
        return {}
    loaded = json.loads(raw)
    if not isinstance(loaded, dict):
        raise ResearchRecordError(f"{field_name} must be a JSON object.", code="invalid_json_object")
    return {str(key): value for key, value in loaded.items()}


def parse_string_map(raw: str | None, *, field_name: str) -> dict[str, str]:
    return {key: str(value) for key, value in parse_json_object(raw, field_name=field_name).items()}
