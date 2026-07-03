"""Extension-backed research record CRUD over Workspace Runtime."""

from __future__ import annotations

from dataclasses import dataclass, replace
import json
from pathlib import Path
import shutil
from typing import Any, Mapping
import uuid

from isomer_labs.artifact_formats import (
    ArtifactFormatRegistry,
    WorkspaceRuntimeArtifactFormatProvider,
    digest_bytes,
    register_custom_artifact_format,
    render_artifact,
    validate_payload,
)
from isomer_labs.artifact_formats.validation import load_payload_file
from isomer_labs.deepsci_ext.record_formats import register_deepsci_record_format_provider
from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.workspace.paths import resolve_semantic_path
from isomer_labs.runtime.identifiers import _provenance_ref, _slug
from isomer_labs.runtime.models import (
    LIFECYCLE_RECORD_KINDS,
    LIFECYCLE_STATUSES,
    RuntimeLifecycleRecord,
    StructuredResearchPayloadRecord,
    utc_timestamp,
)
from isomer_labs.runtime.store import WorkspaceRuntimeStore, open_workspace_runtime


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
    topic_actor_name: str | None = None
    actor_kind: str | None = None
    runtime_kind: str | None = None
    controller_kind: str | None = None
    adapter_ref: str | None = None
    semantic_label: str | None = None
    body: str | None = None
    body_file: Path | None = None
    content_name: str | None = None
    payload_file: Path | None = None
    format_profile_ref: str | None = None
    schema_ref: str | None = None
    template_ref: str | None = None
    schema_file: Path | None = None
    template_file: Path | None = None
    render_format: str | None = None
    metadata: dict[str, object] | None = None
    lifecycle_refs: dict[str, str] | None = None


@dataclass(frozen=True)
class StructuredPayloadPreparation:
    payload: dict[str, object]
    validation_status: str
    validation_diagnostics: list[dict[str, object]]
    schema_ref: str
    schema_version: str | None
    schema_source_kind: str
    format_profile_ref: str | None
    template_ref: str | None
    template_source_kind: str | None
    render_status: str
    render_diagnostics: list[dict[str, object]]
    rendered_markdown_path: Path | None
    rendered_markdown_digest: str | None
    payload_digest: str


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
        now = utc_timestamp()
        record_id = request.record_id or _new_record_id(request)
        request = replace(request, record_id=record_id)
        structured_payload = None
        if _structured_request(request):
            structured_payload, content_path, structured_diagnostics = _prepare_structured_payload(
                context,
                runtime_store,
                request,
                env=env,
                cwd=cwd,
                durable=True,
            )
            diagnostics.extend(structured_diagnostics)
        else:
            content_path, body_diagnostics = _write_body(context, request, env=env, cwd=cwd)
            diagnostics.extend(body_diagnostics)
        if has_errors(diagnostics):
            return _diagnostic_payload("create", diagnostics), diagnostics
        metadata = _record_metadata(request)
        metadata["created_by"] = "isomer-cli ext research records create"
        if content_path is not None:
            metadata["content_semantic_label"] = _semantic_label_for_request(request)
        if structured_payload is not None:
            metadata.update(_structured_metadata(structured_payload))
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
            if structured_payload is not None:
                runtime_store.upsert_structured_payload(
                    _structured_payload_record(
                        context,
                        record_id=record_id,
                        preparation=structured_payload,
                        created_at=now,
                        updated_at=now,
                        provenance_refs=[_provenance_ref("structured-payload", record_id)],
                    )
                )
        stored = runtime_store.get_lifecycle_record(record_id) or record
        stored_payload = runtime_store.get_structured_payload(record_id)
        return {
            "ok": True,
            "mutated": True,
            "operation": "create",
            "record": stored.to_json(),
            "structured_payload": stored_payload.to_json() if stored_payload is not None else None,
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
    include_payload: bool = False,
    include_validation_diagnostics: bool = False,
    include_render_diagnostics: bool = False,
    include_rendered_body: bool = False,
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
        structured_payload = runtime_store.get_structured_payload(record_id)
        if structured_payload is not None:
            payload["structured_payload"] = structured_payload.to_json(
                include_payload=include_payload,
                include_diagnostics=include_validation_diagnostics or include_render_diagnostics,
            )
            if not include_validation_diagnostics:
                payload["structured_payload"].pop("validation_diagnostics", None)  # type: ignore[index]
            if not include_render_diagnostics:
                payload["structured_payload"].pop("render_diagnostics", None)  # type: ignore[index]
        if include_body:
            payload["body"] = _read_record_body(record)
        if include_rendered_body and structured_payload is not None:
            payload["rendered_body"] = _read_rendered_body(structured_payload.rendered_markdown_path)
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
    topic_actor_name: str | None = None,
    actor_kind: str | None = None,
    runtime_kind: str | None = None,
    controller_kind: str | None = None,
    adapter_ref: str | None = None,
    format_profile_ref: str | None = None,
    schema_ref: str | None = None,
    template_ref: str | None = None,
    validation_status: str | None = None,
    render_status: str | None = None,
    limit: int | None = None,
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
        selected_limit = _effective_records_list_limit(context, limit, diagnostics)
        structured_by_record_id = {
            payload.record_id: payload
            for payload in runtime_store.list_structured_payloads(
                topic_workspace_id=context.topic_workspace_id,
                format_profile_ref=format_profile_ref,
                schema_ref=schema_ref,
                template_ref=template_ref,
                validation_status=validation_status,
                render_status=render_status,
            )
        }
        structured_filter_requested = any(
            value is not None
            for value in (format_profile_ref, schema_ref, template_ref, validation_status, render_status)
        )
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
            and _matches_metadata(record, "topic_actor_name", topic_actor_name)
            and _matches_metadata(record, "actor_kind", actor_kind)
            and _matches_metadata(record, "runtime_kind", runtime_kind)
            and _matches_metadata(record, "controller_kind", controller_kind)
            and _matches_metadata(record, "adapter_ref", adapter_ref)
            and (not structured_filter_requested or record.id in structured_by_record_id)
        ]
        records = sorted(records, key=lambda item: (item.updated_at, item.created_at, item.id), reverse=True)[:selected_limit]
        return {
            "ok": True,
            "mutated": False,
            "operation": "list",
            "count": len(records),
            "limit": selected_limit,
            "records": [
                _record_with_structured_summary(record, structured_by_record_id.get(record.id))
                for record in records
            ],
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
        request = replace(request, record_id=record_id)
        structured_payload = None
        if _structured_request(request):
            structured_payload, content_path, structured_diagnostics = _prepare_structured_payload(
                context,
                runtime_store,
                request,
                env=env,
                cwd=cwd,
                durable=True,
            )
            diagnostics.extend(structured_diagnostics)
        else:
            content_path, body_diagnostics = _write_body(context, request, env=env, cwd=cwd)
            diagnostics.extend(body_diagnostics)
        if has_errors(diagnostics):
            return _diagnostic_payload("update", diagnostics), diagnostics
        metadata = dict(existing.transition_metadata)
        metadata.update(_record_metadata(request))
        metadata["updated_by"] = "isomer-cli ext research records update"
        metadata["updated_at"] = utc_timestamp()
        if structured_payload is not None:
            metadata.update(_structured_metadata(structured_payload))
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
        existing_payload = runtime_store.get_structured_payload(record_id)
        with runtime_store.connection:
            runtime_store.upsert_lifecycle_record(updated)
            if structured_payload is not None:
                runtime_store.upsert_structured_payload(
                    _structured_payload_record(
                        context,
                        record_id=record_id,
                        preparation=structured_payload,
                        created_at=existing_payload.created_at if existing_payload is not None else existing.created_at,
                        updated_at=str(metadata["updated_at"]),
                        provenance_refs=[
                            *(existing_payload.provenance_refs if existing_payload is not None else []),
                            _provenance_ref("structured-payload-update", record_id),
                        ],
                    )
                )
        stored = runtime_store.get_lifecycle_record(record_id) or updated
        stored_payload = runtime_store.get_structured_payload(record_id)
        return {
            "ok": True,
            "mutated": True,
            "operation": "update",
            "record": stored.to_json(),
            "structured_payload": stored_payload.to_json() if stored_payload is not None else None,
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


def validate_record_payload(
    context: EffectiveTopicContext,
    request: ResearchRecordRequest,
    *,
    env: Mapping[str, str],
    cwd: Path,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """Validate a structured research record payload without mutation."""

    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if runtime_store is None:
        return _runtime_missing_payload("validate", diagnostics), diagnostics
    try:
        preparation, _content_path, structured_diagnostics = _prepare_structured_payload(
            context,
            runtime_store,
            request,
            env=env,
            cwd=cwd,
            durable=False,
        )
        diagnostics.extend(structured_diagnostics)
        if preparation is None or has_errors(diagnostics):
            return _diagnostic_payload("validate", diagnostics), diagnostics
        return {
            "ok": True,
            "mutated": False,
            "operation": "validate",
            "validation": {
                "status": preparation.validation_status,
                "format_profile_ref": preparation.format_profile_ref,
                "schema_ref": preparation.schema_ref,
                "schema_version": preparation.schema_version,
                "schema_source_kind": preparation.schema_source_kind,
                "payload_digest": preparation.payload_digest,
                "diagnostics": preparation.validation_diagnostics,
            },
        }, diagnostics
    finally:
        runtime_store.close()


def render_record(
    context: EffectiveTopicContext,
    record_id: str,
    *,
    env: Mapping[str, str],
    output_file: Path | None = None,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """Render a stored structured research record without mutating its locator."""

    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if runtime_store is None:
        return _runtime_missing_payload("render", diagnostics), diagnostics
    try:
        record = runtime_store.get_lifecycle_record(record_id)
        if record is None or not _belongs_to_context(record, context):
            raise ResearchRecordError(f"Research record not found: {record_id}", code="record_not_found")
        structured_payload = runtime_store.get_structured_payload(record_id)
        if structured_payload is None:
            raise ResearchRecordError(f"Research record is not structured: {record_id}", code="structured_payload_missing")
        registry = _artifact_format_registry(context, runtime_store)
        render = render_artifact(
            structured_payload.payload_json,
            registry=registry,
            output_format="markdown",
            format_profile_ref=structured_payload.format_profile_ref,
            schema_ref=None if structured_payload.format_profile_ref is not None else structured_payload.schema_ref,
            template_ref=None if structured_payload.format_profile_ref is not None else structured_payload.template_ref,
        )
        diagnostics.extend(render.diagnostics)
        if render.ok and output_file is not None and render.content is not None:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(render.content, encoding="utf-8")
        return {
            "ok": render.ok,
            "mutated": False,
            "operation": "render",
            "record": record.to_json(),
            "render": render.to_json(include_content=True),
            "output_file": str(output_file) if output_file is not None else None,
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


def _prepare_structured_payload(
    context: EffectiveTopicContext,
    runtime_store: WorkspaceRuntimeStore,
    request: ResearchRecordRequest,
    *,
    env: Mapping[str, str],
    cwd: Path,
    durable: bool,
) -> tuple[StructuredPayloadPreparation | None, Path | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    if request.body is not None or request.body_file is not None:
        raise ResearchRecordError(
            "Structured research records require --payload-file; do not use --body or --body-file with structured format inputs.",
            code="structured_payload_requires_json",
        )
    if request.payload_file is None:
        diagnostics.append(
            Diagnostic(
                code="ISO210",
                severity="error",
                concept="Structured Research Payload",
                field="payload_file",
                message="Structured research records require a JSON payload file.",
            )
        )
        return None, None, diagnostics
    payload, payload_diagnostics = load_payload_file(request.payload_file)
    diagnostics.extend(payload_diagnostics)
    if not isinstance(payload, dict):
        diagnostics.append(
            Diagnostic(
                code="ISO210",
                severity="error",
                concept="Structured Research Payload",
                path=request.payload_file,
                field="payload_file",
                message="Structured research record payloads must be JSON objects.",
            )
        )
        return None, None, diagnostics

    selected_request = request
    if durable and request.schema_file is not None:
        selected_request, snapshot_diagnostics = _snapshot_plain_format_inputs(context, runtime_store, request)
        diagnostics.extend(snapshot_diagnostics)
        if has_errors(diagnostics):
            return None, None, diagnostics
    registry = _artifact_format_registry(context, runtime_store)
    validation = validate_payload(
        payload,
        registry=registry,
        format_profile_ref=selected_request.format_profile_ref,
        schema_ref=selected_request.schema_ref,
        schema_file=selected_request.schema_file if not durable else None,
    )
    diagnostics.extend(validation.diagnostics)
    if not validation.ok:
        return None, None, diagnostics

    render_result = None
    content_path = None
    rendered_markdown_digest = None
    if selected_request.render_format is not None:
        render_result = render_artifact(
            payload,
            registry=registry,
            output_format=selected_request.render_format,
            format_profile_ref=selected_request.format_profile_ref,
            schema_ref=selected_request.schema_ref,
            template_ref=selected_request.template_ref,
            schema_file=selected_request.schema_file if not durable else None,
            template_file=selected_request.template_file if not durable else None,
        )
        diagnostics.extend(render_result.diagnostics)
        if not render_result.ok or render_result.content is None:
            return None, None, diagnostics
        content_path, write_diagnostics = _write_generated_markdown(
            context,
            selected_request,
            render_result.content,
            validation_payload=validation.to_json(),
            env=env,
            cwd=cwd,
        )
        diagnostics.extend(write_diagnostics)
        if content_path is not None:
            rendered_markdown_digest = digest_bytes(content_path.read_bytes())

    template_ref = render_result.template_ref if render_result is not None else selected_request.template_ref
    template_source_kind = render_result.template_source_kind if render_result is not None else None
    return (
        StructuredPayloadPreparation(
            payload={str(key): value for key, value in payload.items()},
            validation_status=validation.status,
            validation_diagnostics=[diagnostic.to_json() for diagnostic in validation.diagnostics],
            schema_ref=str(validation.schema_ref or selected_request.schema_ref or selected_request.schema_file),
            schema_version=validation.schema_version,
            schema_source_kind=str(validation.schema_source_kind or "plain_file"),
            format_profile_ref=validation.profile_ref or selected_request.format_profile_ref,
            template_ref=template_ref,
            template_source_kind=template_source_kind,
            render_status=render_result.status if render_result is not None else "not_requested",
            render_diagnostics=[diagnostic.to_json() for diagnostic in (render_result.diagnostics if render_result is not None else [])],
            rendered_markdown_path=content_path,
            rendered_markdown_digest=rendered_markdown_digest,
            payload_digest=validation.payload_digest,
        ),
        content_path,
        diagnostics,
    )


def _snapshot_plain_format_inputs(
    context: EffectiveTopicContext,
    runtime_store: WorkspaceRuntimeStore,
    request: ResearchRecordRequest,
) -> tuple[ResearchRecordRequest, list[Diagnostic]]:
    if request.schema_file is None:
        return request, []
    if request.render_format is not None and request.template_file is None:
        return request, [
            Diagnostic(
                code="ISO210",
                severity="error",
                concept="Structured Research Payload",
                field="template_file",
                message="Durable Markdown rendering from a plain schema file also requires --template-file.",
            )
        ]
    stem = request.record_id or request.placeholder or request.content_name or "structured-payload"
    topic_slug = _slug(context.topic_workspace_id)
    format_profile_ref = (
        request.format_profile_ref
        or f"custom:{topic_slug}/record-format/profile/snapshot/{_slug(stem)}/v1"
    )
    registration, diagnostics = register_custom_artifact_format(
        runtime_store,
        context,
        format_profile_ref=format_profile_ref,
        schema_file=request.schema_file,
        template_file=request.template_file,
        output_format=request.render_format or "markdown",
        replace=True,
        source_kind="file_snapshot",
    )
    if registration is None:
        return request, diagnostics
    return (
        replace(
            request,
            format_profile_ref=registration.format_profile_ref,
            schema_ref=None,
            template_ref=None,
            schema_file=None,
            template_file=None,
        ),
        diagnostics,
    )


def _artifact_format_registry(
    context: EffectiveTopicContext,
    runtime_store: WorkspaceRuntimeStore,
) -> ArtifactFormatRegistry:
    registry = ArtifactFormatRegistry()
    register_deepsci_record_format_provider(registry)
    registry.register_provider(
        WorkspaceRuntimeArtifactFormatProvider(runtime_store, topic_workspace_id=context.topic_workspace_id)
    )
    return registry


def _write_generated_markdown(
    context: EffectiveTopicContext,
    request: ResearchRecordRequest,
    content: str,
    *,
    validation_payload: dict[str, object],
    env: Mapping[str, str],
    cwd: Path,
) -> tuple[Path | None, list[Diagnostic]]:
    label = _semantic_label_for_request(request)
    result, diagnostics = resolve_semantic_path(context, label, env=env, cwd=cwd)
    if result is None:
        return None, diagnostics
    target_dir = result.path / "research-records" / request.record_kind
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / _content_filename(request, suffix=".md")
    header = "\n".join(
        [
            "<!-- isomer-structured-research-record",
            f"format_profile_ref: {validation_payload.get('format_profile_ref')}",
            f"schema_ref: {validation_payload.get('schema_ref')}",
            f"payload_digest: {validation_payload.get('payload_digest')}",
            "-->",
            "",
        ]
    )
    target.write_text(f"{header}{content}", encoding="utf-8")
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
        ("format_profile_ref", request.format_profile_ref),
        ("schema_ref", request.schema_ref),
        ("template_ref", request.template_ref),
        ("render_format", request.render_format),
        ("skill", request.skill),
        ("producer", request.producer),
        ("consumer", request.consumer),
        ("topic_actor_name", request.topic_actor_name),
        ("actor_kind", request.actor_kind),
        ("runtime_kind", request.runtime_kind),
        ("controller_kind", request.controller_kind),
        ("adapter_ref", request.adapter_ref),
        ("semantic_label", _semantic_label_for_request(request)),
    ):
        if value is not None:
            metadata[key] = value
    return metadata


def _structured_request(request: ResearchRecordRequest) -> bool:
    return any(
        value is not None
        for value in (
            request.payload_file,
            request.format_profile_ref,
            request.schema_ref,
            request.template_ref,
            request.schema_file,
            request.template_file,
            request.render_format,
        )
    )


def _structured_metadata(preparation: StructuredPayloadPreparation) -> dict[str, object]:
    metadata: dict[str, object] = {
        "structured_payload": True,
        "schema_ref": preparation.schema_ref,
        "schema_source_kind": preparation.schema_source_kind,
        "payload_digest": preparation.payload_digest,
        "validation_status": preparation.validation_status,
        "render_status": preparation.render_status,
    }
    if preparation.format_profile_ref is not None:
        metadata["format_profile_ref"] = preparation.format_profile_ref
    if preparation.template_ref is not None:
        metadata["template_ref"] = preparation.template_ref
    if preparation.template_source_kind is not None:
        metadata["template_source_kind"] = preparation.template_source_kind
    if preparation.rendered_markdown_path is not None:
        metadata["rendered_markdown_path"] = str(preparation.rendered_markdown_path)
    return metadata


def _structured_payload_record(
    context: EffectiveTopicContext,
    *,
    record_id: str,
    preparation: StructuredPayloadPreparation,
    created_at: str,
    updated_at: str,
    provenance_refs: list[str],
) -> StructuredResearchPayloadRecord:
    return StructuredResearchPayloadRecord(
        id=f"structured-payload-{_slug(record_id)}",
        record_id=record_id,
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        format_profile_ref=preparation.format_profile_ref,
        schema_ref=preparation.schema_ref,
        schema_version=preparation.schema_version,
        schema_source_kind=preparation.schema_source_kind,
        template_ref=preparation.template_ref,
        template_source_kind=preparation.template_source_kind,
        payload_json=preparation.payload,
        payload_digest=preparation.payload_digest,
        validation_status=preparation.validation_status,
        validation_diagnostics=preparation.validation_diagnostics,
        render_status=preparation.render_status,
        render_diagnostics=preparation.render_diagnostics,
        rendered_markdown_path=str(preparation.rendered_markdown_path) if preparation.rendered_markdown_path is not None else None,
        rendered_markdown_digest=preparation.rendered_markdown_digest,
        created_at=created_at,
        updated_at=updated_at,
        provenance_refs=provenance_refs,
    )


def _record_with_structured_summary(
    record: RuntimeLifecycleRecord,
    structured_payload: StructuredResearchPayloadRecord | None,
) -> dict[str, object]:
    data = record.to_json()
    if structured_payload is not None:
        data["structured_payload"] = structured_payload.to_summary_json()
    return data


def _read_rendered_body(rendered_markdown_path: str | None) -> str | None:
    if rendered_markdown_path is None:
        return None
    path = Path(rendered_markdown_path)
    if not path.exists() or not path.is_file():
        return None
    return path.read_text(encoding="utf-8", errors="replace")


def _effective_records_list_limit(
    context: EffectiveTopicContext,
    requested_limit: int | None,
    diagnostics: list[Diagnostic],
) -> int:
    if requested_limit is not None:
        if requested_limit <= 0:
            diagnostics.append(
                Diagnostic(
                    code="ISO211",
                    severity="error",
                    concept="Research Record list limit",
                    field="limit",
                    message="Research record list limit must be a positive integer.",
                )
            )
            return 20
        return requested_limit
    ext_defaults = context.project.manifest.defaults.get("ext")
    if isinstance(ext_defaults, dict):
        research_defaults = ext_defaults.get("research")
        if isinstance(research_defaults, dict) and "records_list_limit" in research_defaults:
            value = research_defaults["records_list_limit"]
            if isinstance(value, int) and value > 0:
                return value
            diagnostics.append(
                Diagnostic(
                    code="ISO211",
                    severity="error",
                    concept="Project Manifest",
                    path=context.project.manifest.source_path,
                    field="defaults.ext.research.records_list_limit",
                    message="Project Manifest records_list_limit must be a positive integer.",
                )
            )
    return 20


def _lifecycle_refs(context: EffectiveTopicContext, request: ResearchRecordRequest) -> dict[str, str]:
    refs = dict(context.lifecycle_refs)
    if context.topic_agent_team_profile_id is not None:
        refs.setdefault("topic_agent_team_profile_id", context.topic_agent_team_profile_id)
    if request.topic_actor_name is not None:
        refs.setdefault("topic_actor_name", request.topic_actor_name)
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
