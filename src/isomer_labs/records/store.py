"""Extension-backed research record CRUD over Workspace Runtime."""

from __future__ import annotations

from dataclasses import dataclass, replace
import json
from pathlib import Path
import re
import shutil
from typing import Any, Mapping, TypedDict
import uuid

from isomer_labs.artifact_formats import (
    ArtifactFormatResolver,
    ArtifactFormatRegistry,
    WorkspaceRuntimeArtifactFormatProvider,
    digest_bytes,
    digest_json,
    register_custom_artifact_format,
    register_builtin_artifact_format_providers,
    render_artifact,
    validate_payload,
)
from isomer_labs.artifact_formats.processing import load_payload_file
from isomer_labs.deepsci_ext.record_formats import is_unsupported_deepsci_v1_ref
from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.workspace.path_resolution import resolve_semantic_path
from isomer_labs.runtime.records import _provenance_ref, _slug
from isomer_labs.runtime.records import (
    LIFECYCLE_RECORD_KINDS,
    LIFECYCLE_STATUSES,
    RESEARCH_RECORD_LINEAGE_KINDS,
    RESEARCH_IDEA_LINEAGE_KINDS,
    ResearchRecordGenerationGroup,
    ResearchRecordLineageEdge,
    ResearchIdea,
    ResearchIdeaGenerationGroup,
    ResearchIdeaLineageEdge,
    ResearchIdeaRealization,
    RuntimeLifecycleRecord,
    StructuredResearchPayloadRecord,
    utc_timestamp,
)
from isomer_labs.runtime.store import WorkspaceRuntimeStore, open_workspace_runtime
from isomer_labs.records.index import refresh_query_index_for_record
from isomer_labs.records.idea_sources import (
    SOURCE_STATUS_EXACT,
    IdeaEntryFragment,
    load_structured_payload,
    profile_idea_entry_fragments,
    resolve_structured_source_fragment,
)


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
    semantic_id: str | None = None
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
    relationships: list[dict[str, object]] | None = None
    parents: list[dict[str, object]] | None = None
    lineage_kind: str | None = None
    generation_id: str | None = None
    generation_purpose: str | None = None
    decision_record_id: str | None = None
    lineage_rationale: str | None = None
    file_attachments: list[dict[str, object]] | None = None
    index_hints: dict[str, object] | None = None
    realizes_idea_id: str | None = None
    idea_realizations: list[dict[str, object]] | None = None
    idea_parents: list[dict[str, object]] | None = None
    primary_idea: dict[str, object] | None = None


class LineageParentSpec(TypedDict):
    record_id: str
    lineage_kind: str
    parent_role: str | None
    decision_record_id: str | None
    rationale: str | None
    status: str
    metadata: dict[str, object]


@dataclass(frozen=True)
class StructuredPayloadPreparation:
    payload: dict[str, object]
    payload_file_path: Path | None
    payload_manifest_path: Path | None
    payload_source_path: str | None
    payload_media_type: str
    revision_of_record_id: str | None
    supersedes_record_id: str | None
    latest_for_semantic_id: str | None
    legacy_rendered_markdown_path: str | None
    legacy_rendered_markdown_digest: str | None
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
    _validate_semantic_id(request.semantic_id)
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
            lineage_payload = _store_request_lineage(
                context,
                runtime_store,
                request,
                created_at=now,
                updated_at=now,
            )
            idea_payload = _store_request_ideas(
                context,
                runtime_store,
                request,
                record_id=record_id,
                created_at=now,
                updated_at=now,
            )
        index_payload = refresh_query_index_for_record(context, runtime_store, record_id)
        for parent_id in _affected_parent_record_ids(lineage_payload):
            refresh_query_index_for_record(context, runtime_store, parent_id)
        stored = runtime_store.get_lifecycle_record(record_id) or record
        stored_payload = runtime_store.get_structured_payload(record_id)
        return {
            "ok": True,
            "mutated": True,
            "operation": "create",
            "record": stored.to_json(),
            "structured_payload": stored_payload.to_json() if stored_payload is not None else None,
            "content_path": str(content_path) if content_path is not None else None,
            "lineage": lineage_payload,
            "idea_writes": idea_payload,
            "query_index": index_payload,
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
                include_payload=False,
                include_diagnostics=include_validation_diagnostics or include_render_diagnostics,
            )
            if include_payload:
                payload_json, payload_diagnostics = _read_structured_payload_json(structured_payload)
                diagnostics.extend(payload_diagnostics)
                if payload_json is not None:
                    payload["structured_payload"]["payload"] = payload_json  # type: ignore[index]
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
    semantic_id: str | None = None,
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
    _validate_semantic_id(semantic_id)
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
            and _matches_metadata(record, "semantic_id", semantic_id)
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
    _validate_semantic_id(request.semantic_id)
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
        existing_semantic_id = _optional_metadata_string(existing.transition_metadata.get("semantic_id"))
        if request.semantic_id is not None and existing_semantic_id is not None and request.semantic_id != existing_semantic_id:
            raise ResearchRecordError(
                f"Semantic id mismatch for {record_id}: existing {existing_semantic_id}, requested {request.semantic_id}.",
                code="semantic_id_mismatch",
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
            lineage_payload = _store_request_lineage(
                context,
                runtime_store,
                request,
                created_at=existing.created_at,
                updated_at=str(metadata["updated_at"]),
            )
            idea_payload = _store_request_ideas(
                context,
                runtime_store,
                request,
                record_id=record_id,
                created_at=existing.created_at,
                updated_at=str(metadata["updated_at"]),
            )
        index_payload = refresh_query_index_for_record(context, runtime_store, record_id)
        for parent_id in _affected_parent_record_ids(lineage_payload):
            refresh_query_index_for_record(context, runtime_store, parent_id)
        stored = runtime_store.get_lifecycle_record(record_id) or updated
        stored_payload = runtime_store.get_structured_payload(record_id)
        return {
            "ok": True,
            "mutated": True,
            "operation": "update",
            "record": stored.to_json(),
            "structured_payload": stored_payload.to_json() if stored_payload is not None else None,
            "content_path": stored.content_path,
            "lineage": lineage_payload,
            "idea_writes": idea_payload,
            "query_index": index_payload,
        }, diagnostics
    finally:
        runtime_store.close()


def revise_record(
    context: EffectiveTopicContext,
    record_id: str,
    request: ResearchRecordRequest,
    *,
    env: Mapping[str, str],
    cwd: Path,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """Create a new descendant record for a content-changing revision."""

    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if runtime_store is None:
        return _runtime_missing_payload("revise", diagnostics), diagnostics
    try:
        existing = runtime_store.get_lifecycle_record(record_id)
        if existing is None or not _belongs_to_context(existing, context):
            raise ResearchRecordError(f"Research record not found: {record_id}", code="record_not_found")
        existing_payload = runtime_store.get_structured_payload(record_id)
    finally:
        runtime_store.close()

    existing_metadata = existing.transition_metadata
    request_metadata = dict(request.metadata or {})
    request_metadata.setdefault("revision_of_record_id", record_id)
    request_metadata.setdefault("supersedes_record_id", record_id)
    latest_for = _optional_metadata_string(
        existing_metadata.get("latest_for_semantic_id")
        or existing_metadata.get("semantic_id")
        or existing_metadata.get("placeholder")
        or existing_metadata.get("profile")
        or existing.id
    )
    if latest_for is not None:
        request_metadata.setdefault("latest_for_semantic_id", latest_for)
    next_request = replace(
        request,
        record_kind=request.record_kind or existing.record_kind,
        record_id=request.record_id or _revision_record_id(existing),
        placeholder=request.placeholder or _optional_metadata_string(existing_metadata.get("placeholder")),
        semantic_id=request.semantic_id or _optional_metadata_string(existing_metadata.get("semantic_id")),
        profile=request.profile or _optional_metadata_string(existing_metadata.get("profile")),
        skill=request.skill or _optional_metadata_string(existing_metadata.get("skill")),
        producer=request.producer or _optional_metadata_string(existing_metadata.get("producer")),
        consumer=request.consumer or _optional_metadata_string(existing_metadata.get("consumer")),
        format_profile_ref=request.format_profile_ref or (existing_payload.format_profile_ref if existing_payload is not None else None),
        schema_ref=(
            request.schema_ref
            if request.format_profile_ref is None
            else None
        )
        or (
            existing_payload.schema_ref
            if existing_payload is not None
            and existing_payload.format_profile_ref is None
            and request.format_profile_ref is None
            else None
        ),
        template_ref=(
            request.template_ref
            if request.format_profile_ref is None
            else None
        )
        or (
            existing_payload.template_ref
            if existing_payload is not None
            and existing_payload.format_profile_ref is None
            and request.format_profile_ref is None
            else None
        ),
        metadata=request_metadata,
        parents=[{"record_id": record_id, "role": "previous_revision"}],
        lineage_kind="revision_of",
        generation_id=None,
        generation_purpose=None,
        lineage_rationale=request.lineage_rationale or _optional_metadata_string(request_metadata.get("rationale")),
    )
    payload, create_diagnostics = create_record(context, next_request, env=env, cwd=cwd)
    payload["operation"] = "revise"
    payload["revision_of_record_id"] = record_id
    return payload, [*diagnostics, *create_diagnostics]


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
        index_payload = refresh_query_index_for_record(context, runtime_store, record_id)
        stored = runtime_store.get_lifecycle_record(record_id) or archived
        return {
            "ok": True,
            "mutated": True,
            "operation": "delete",
            "delete_mode": "archive",
            "record": stored.to_json(),
            "query_index": index_payload,
        }, diagnostics
    finally:
        runtime_store.close()


def add_lineage_edge(
    context: EffectiveTopicContext,
    *,
    parent_record_id: str,
    child_record_id: str,
    lineage_kind: str,
    env: Mapping[str, str],
    parent_role: str | None = None,
    generation_id: str | None = None,
    generation_purpose: str | None = None,
    decision_record_id: str | None = None,
    rationale: str | None = None,
    metadata: dict[str, object] | None = None,
    status: str = "ready",
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """Add one canonical lineage edge for maintenance or migration."""

    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    if runtime_store is None:
        return _runtime_missing_payload("lineage.add", diagnostics), diagnostics
    try:
        now = utc_timestamp()
        parent_ids = [parent_record_id]
        group = _generation_group_for_request(
            context,
            runtime_store,
            generation_id=generation_id,
            generation_purpose=generation_purpose,
            producer_skill=None,
            decision_record_id=decision_record_id,
            parent_ids=parent_ids,
            created_at=now,
            updated_at=now,
        )
        edge = _lineage_edge(
            context,
            parent_record_id=parent_record_id,
            child_record_id=child_record_id,
            lineage_kind=lineage_kind,
            parent_role=parent_role,
            generation_id=group.id if group is not None else generation_id,
            decision_record_id=decision_record_id,
            rationale=rationale,
            status=status,
            metadata=metadata or {},
            created_at=now,
            updated_at=now,
        )
        validation = runtime_store.validate_research_record_lineage_edge(edge)
        if _has_lineage_errors(validation):
            raise ResearchRecordError("Canonical lineage edge failed validation.", code="lineage_validation_failed", payload={"diagnostics": validation})
        with runtime_store.connection:
            if group is not None:
                runtime_store.upsert_research_record_generation_group(group)
            runtime_store.upsert_research_record_lineage_edge(edge)
        refresh_query_index_for_record(context, runtime_store, parent_record_id)
        refresh_query_index_for_record(context, runtime_store, child_record_id)
        return {
            "ok": True,
            "mutated": True,
            "operation": "lineage.add",
            "generation_group": group.to_json() if group is not None else None,
            "edge": edge.to_json(),
            "diagnostics": validation,
        }, diagnostics
    finally:
        runtime_store.close()


def validate_lineage(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
) -> tuple[dict[str, Any], list[Diagnostic]]:
    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if runtime_store is None:
        return _runtime_missing_payload("lineage.validate", diagnostics), diagnostics
    try:
        lineage_diagnostics = runtime_store.validate_research_record_lineage(topic_workspace_id=context.topic_workspace_id)
        lineage_diagnostics.extend(_missing_expected_lineage_diagnostics(context, runtime_store))
        return {
            "ok": not _has_lineage_errors(lineage_diagnostics),
            "mutated": False,
            "operation": "lineage.validate",
            "diagnostics": lineage_diagnostics,
            "count": len(lineage_diagnostics),
        }, diagnostics
    finally:
        runtime_store.close()


def upsert_research_idea(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    idea_id: str,
    title: str,
    summary: str,
    family: str | None = None,
    status: str = "candidate",
    visibility: str = "primary",
    aliases: list[str] | None = None,
    display_key: str | None = None,
    source_record_id: str | None = None,
    source_json_path: str | None = None,
    metadata: dict[str, object] | None = None,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    if runtime_store is None:
        return _runtime_missing_payload("ideas.upsert", diagnostics), diagnostics
    try:
        now = utc_timestamp()
        existing = runtime_store.get_research_idea(idea_id, topic_workspace_id=context.topic_workspace_id)
        record = _idea_record(
            context,
            idea_id=idea_id,
            display_key=existing.display_key if existing is not None and existing.display_key is not None else display_key or runtime_store.next_research_idea_display_key(context.topic_workspace_id),
            title=title,
            summary=summary,
            family=family,
            status=status,
            visibility=visibility,
            aliases=aliases or (existing.aliases if existing is not None else []),
            source_record_id=source_record_id,
            source_json_path=source_json_path,
            metadata=metadata or (existing.metadata if existing is not None else {}),
            created_at=existing.created_at if existing is not None else now,
            updated_at=now,
        )
        validation = runtime_store.validate_research_idea(record)
        if _has_lineage_errors(validation):
            raise ResearchRecordError("Research idea failed validation.", code="idea_validation_failed", payload={"diagnostics": validation})
        with runtime_store.connection:
            runtime_store.upsert_research_idea(record, validate=False)
        return {"ok": True, "mutated": True, "operation": "ideas.upsert", "idea": record.to_json(), "diagnostics": validation}, diagnostics
    finally:
        runtime_store.close()


def realize_research_idea(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    idea_id: str,
    record_id: str,
    source_json_path: str | None = None,
    realization_stage: str | None = None,
    semantic_id: str | None = None,
    latest: bool = True,
    metadata: dict[str, object] | None = None,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    if runtime_store is None:
        return _runtime_missing_payload("ideas.realize", diagnostics), diagnostics
    try:
        now = utc_timestamp()
        realization = _idea_realization_record(
            context,
            idea_id=idea_id,
            record_id=record_id,
            source_json_path=source_json_path,
            realization_stage=realization_stage,
            semantic_id=semantic_id,
            latest=latest,
            metadata=metadata or {},
            created_at=now,
            updated_at=now,
        )
        validation = runtime_store.validate_research_idea_realization(realization)
        validation.extend(_validate_realization_source(context, runtime_store, realization, report_missing_payload=False))
        if _has_lineage_errors(validation):
            raise ResearchRecordError("Research idea realization failed validation.", code="idea_realization_validation_failed", payload={"diagnostics": validation})
        with runtime_store.connection:
            runtime_store.upsert_research_idea_realization(realization, validate=False)
        refresh_query_index_for_record(context, runtime_store, record_id)
        return {"ok": True, "mutated": True, "operation": "ideas.realize", "realization": realization.to_json(), "diagnostics": validation}, diagnostics
    finally:
        runtime_store.close()


def add_research_idea_lineage_edge(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    parent_idea_id: str,
    child_idea_id: str,
    lineage_kind: str,
    parent_role: str | None = None,
    generation_id: str | None = None,
    decision_record_id: str | None = None,
    rationale: str | None = None,
    status: str = "ready",
    confidence: float | None = None,
    metadata: dict[str, object] | None = None,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    if runtime_store is None:
        return _runtime_missing_payload("ideas.lineage.add", diagnostics), diagnostics
    try:
        now = utc_timestamp()
        edge = _idea_lineage_edge(
            context,
            parent_idea_id=parent_idea_id,
            child_idea_id=child_idea_id,
            lineage_kind=lineage_kind,
            parent_role=parent_role,
            generation_id=generation_id,
            decision_record_id=decision_record_id,
            rationale=rationale,
            status=status,
            confidence=confidence,
            metadata=metadata or {},
            created_at=now,
            updated_at=now,
        )
        validation = runtime_store.validate_research_idea_lineage_edge(edge)
        if _has_lineage_errors(validation):
            raise ResearchRecordError("Research idea lineage edge failed validation.", code="idea_lineage_validation_failed", payload={"diagnostics": validation})
        with runtime_store.connection:
            runtime_store.upsert_research_idea_lineage_edge(edge, validate=False)
        return {"ok": True, "mutated": True, "operation": "ideas.lineage.add", "edge": edge.to_json(), "diagnostics": validation}, diagnostics
    finally:
        runtime_store.close()


def upsert_research_idea_generation_group(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    generation_id: str,
    parent_idea_ids: list[str],
    purpose: str | None = None,
    producer_skill: str | None = None,
    decision_record_id: str | None = None,
    metadata: dict[str, object] | None = None,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    if runtime_store is None:
        return _runtime_missing_payload("ideas.generation.upsert", diagnostics), diagnostics
    try:
        now = utc_timestamp()
        existing = runtime_store.get_research_idea_generation_group(generation_id)
        group = ResearchIdeaGenerationGroup(
            id=generation_id,
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            purpose=purpose or (existing.purpose if existing is not None else None),
            parent_set_digest=_idea_parent_set_digest(parent_idea_ids),
            producer_skill=producer_skill or (existing.producer_skill if existing is not None else None),
            decision_record_id=decision_record_id or (existing.decision_record_id if existing is not None else None),
            metadata=metadata or (existing.metadata if existing is not None else {"parent_idea_ids": sorted(parent_idea_ids)}),
            created_at=existing.created_at if existing is not None else now,
            updated_at=now,
            provenance_refs=existing.provenance_refs if existing is not None else [_provenance_ref("research-idea-generation-group", generation_id)],
        )
        with runtime_store.connection:
            runtime_store.upsert_research_idea_generation_group(group)
        return {"ok": True, "mutated": True, "operation": "ideas.generation.upsert", "generation_group": group.to_json(), "diagnostics": []}, diagnostics
    finally:
        runtime_store.close()


def query_research_ideas(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    visibility: str | None = None,
    include_archived: bool = False,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if runtime_store is None:
        return _runtime_missing_payload("ideas.query", diagnostics), diagnostics
    try:
        ideas = runtime_store.list_research_ideas(topic_workspace_id=context.topic_workspace_id, visibility=visibility, include_archived=include_archived)
        return {
            "ok": True,
            "mutated": False,
            "operation": "ideas.query",
            "ideas": [idea.to_json() for idea in ideas],
            "realizations": [item.to_json() for item in runtime_store.list_research_idea_realizations(topic_workspace_id=context.topic_workspace_id)],
            "edges": [edge.to_json() for edge in runtime_store.list_research_idea_lineage_edges(topic_workspace_id=context.topic_workspace_id, include_archived=include_archived)],
            "generation_groups": [group.to_json() for group in runtime_store.list_research_idea_generation_groups(topic_workspace_id=context.topic_workspace_id)],
            "diagnostics": [],
        }, diagnostics
    finally:
        runtime_store.close()


def graph_research_ideas(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    visibility: str = "primary",
    include_supporting: bool = False,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if runtime_store is None:
        return _runtime_missing_payload("ideas.graph", diagnostics), diagnostics
    try:
        selected_visibility = None if include_supporting else visibility
        ideas = runtime_store.list_research_ideas(topic_workspace_id=context.topic_workspace_id, visibility=selected_visibility)
        allowed = {idea.idea_id for idea in ideas}
        edges = [
            edge
            for edge in runtime_store.list_research_idea_lineage_edges(topic_workspace_id=context.topic_workspace_id)
            if edge.parent_idea_id in allowed and edge.child_idea_id in allowed
        ]
        return {
            "ok": True,
            "mutated": False,
            "operation": "ideas.graph",
            "graph_source": "canonical",
            "nodes": [idea.to_json() for idea in ideas],
            "edges": [edge.to_json() for edge in edges],
            "generation_groups": [group.to_json() for group in runtime_store.list_research_idea_generation_groups(topic_workspace_id=context.topic_workspace_id)],
            "diagnostics": runtime_store.validate_research_idea_lineage(topic_workspace_id=context.topic_workspace_id),
        }, diagnostics
    finally:
        runtime_store.close()


def validate_research_ideas(context: EffectiveTopicContext, *, env: Mapping[str, str]) -> tuple[dict[str, Any], list[Diagnostic]]:
    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if runtime_store is None:
        return _runtime_missing_payload("ideas.validate", diagnostics), diagnostics
    try:
        idea_diagnostics = runtime_store.validate_research_idea_lineage(topic_workspace_id=context.topic_workspace_id)
        for realization in runtime_store.list_research_idea_realizations(topic_workspace_id=context.topic_workspace_id):
            idea_diagnostics.extend(_validate_realization_source(context, runtime_store, realization, report_missing_payload=True))
        return {
            "ok": not _has_lineage_errors(idea_diagnostics),
            "mutated": False,
            "operation": "ideas.validate",
            "diagnostics": idea_diagnostics,
            "count": len(idea_diagnostics),
        }, diagnostics
    finally:
        runtime_store.close()


def import_research_ideas_from_record(
    context: EffectiveTopicContext,
    record_id: str,
    *,
    env: Mapping[str, str],
    apply: bool = False,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=not apply)
    if runtime_store is None:
        return _runtime_missing_payload("ideas.import-from-record", diagnostics), diagnostics
    try:
        payload = runtime_store.get_structured_payload(record_id)
        if payload is None:
            return {"ok": False, "mutated": False, "operation": "ideas.import-from-record", "error": {"code": "record_payload_missing", "message": f"Record has no structured payload: {record_id}"}, "diagnostics": []}, diagnostics
        payload_json, payload_diagnostics = load_structured_payload(context, payload)
        if not isinstance(payload_json, Mapping):
            return {
                "ok": False,
                "mutated": False,
                "operation": "ideas.import-from-record",
                "error": {"code": "record_payload_unavailable", "message": f"Record payload could not be read as an object: {record_id}"},
                "diagnostics": payload_diagnostics,
            }, diagnostics
        fragments, fragment_diagnostics = profile_idea_entry_fragments(payload_json, payload.format_profile_ref, record_id=record_id)
        plan = _idea_import_plan_from_fragments(context, fragments, record_id)
        applied: list[dict[str, object]] = []
        if apply:
            now = utc_timestamp()
            with runtime_store.connection:
                for item in plan:
                    idea = _idea_record(
                        context,
                        idea_id=str(item["idea_id"]),
                        display_key=_optional_metadata_string(item.get("display_key")) or runtime_store.next_research_idea_display_key(context.topic_workspace_id),
                        title=str(item["title"]),
                        summary=str(item["summary"]),
                        family=str(item.get("family") or "legacy-import"),
                        status=str(item.get("status") or "candidate"),
                        visibility=str(item.get("visibility") or "supporting"),
                        aliases=_string_list(item.get("aliases")),
                        source_record_id=record_id,
                        source_json_path=str(item.get("source_json_path") or ""),
                        metadata={"import_source": "legacy-record-facet", "preview": item},
                        created_at=now,
                        updated_at=now,
                    )
                    runtime_store.upsert_research_idea(idea)
                    realization = _idea_realization_record(
                        context,
                        idea_id=str(item["idea_id"]),
                        record_id=record_id,
                        source_json_path=str(item.get("source_json_path") or ""),
                        realization_stage=_optional_metadata_string(item.get("realization_stage")) or "imported",
                        semantic_id=_optional_metadata_string(item.get("semantic_id")),
                        latest=bool(item.get("latest", False)),
                        metadata={"import_source": "profile-aware-record", "preview": item},
                        created_at=now,
                        updated_at=now,
                    )
                    realization_diagnostics = runtime_store.validate_research_idea_realization(realization)
                    realization_diagnostics.extend(_validate_realization_source(context, runtime_store, realization, report_missing_payload=False))
                    if _has_lineage_errors(realization_diagnostics):
                        raise ResearchRecordError("Research idea realization failed validation.", code="idea_realization_validation_failed", payload={"diagnostics": realization_diagnostics})
                    runtime_store.upsert_research_idea_realization(realization, validate=False)
                    applied.append(idea.to_json())
        return {"ok": True, "mutated": apply, "operation": "ideas.import-from-record", "record_id": record_id, "plan": plan, "applied": applied, "diagnostics": [*payload_diagnostics, *fragment_diagnostics]}, diagnostics
    finally:
        runtime_store.close()


def repair_research_ideas(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    apply: bool = False,
    update_payloads: bool = False,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=not apply)
    if runtime_store is None:
        return _runtime_missing_payload("ideas.repair", diagnostics), diagnostics
    try:
        plan = _idea_repair_plan(context, runtime_store)
        applied: list[dict[str, object]] = []
        plan_errors = [
            diagnostic
            for item in plan
            for diagnostic in _dict_list(item.get("diagnostics"))
            if diagnostic.get("severity") == "error"
        ]
        if apply:
            if plan_errors:
                validation_payload, _ = validate_research_ideas(context, env=env)
                return {
                    "ok": False,
                    "mutated": False,
                    "operation": "ideas.repair",
                    "apply": apply,
                    "update_payloads": update_payloads,
                    "error": {"code": "idea_repair_plan_blocked", "message": "Research Idea repair plan has errors and was not applied."},
                    "diagnostics": [*validation_payload.get("diagnostics", []), *plan_errors],
                    "plan": plan,
                    "applied": applied,
                    "note": "Managed payload files are not mutated unless a dedicated payload-update repair path is implemented and explicitly enabled.",
                }, diagnostics
            now = utc_timestamp()
            with runtime_store.connection:
                for item in plan:
                    if item.get("action") != "update_realization_source_path":
                        if item.get("action") in {"assign_display_key", "migrate_display_key"}:
                            idea = runtime_store.get_research_idea(str(item["idea_id"]), topic_workspace_id=context.topic_workspace_id)
                            if idea is None:
                                continue
                            repaired_idea = ResearchIdea(
                                id=idea.id,
                                research_topic_id=idea.research_topic_id,
                                topic_workspace_id=idea.topic_workspace_id,
                                idea_id=idea.idea_id,
                                display_key=str(item["display_key"]),
                                title=idea.title,
                                summary=idea.summary,
                                family=idea.family,
                                status=idea.status,
                                visibility=idea.visibility,
                                aliases=idea.aliases,
                                source_record_id=idea.source_record_id,
                                source_json_path=idea.source_json_path,
                                metadata={**idea.metadata, "display_key_repair_source": "ideas.repair"},
                                created_at=idea.created_at,
                                updated_at=now,
                                provenance_refs=idea.provenance_refs,
                            )
                            runtime_store.upsert_research_idea(repaired_idea)
                            payload: dict[str, object] = {"idea_id": repaired_idea.idea_id, "display_key": repaired_idea.display_key}
                            if item.get("previous_display_key") is not None:
                                payload["previous_display_key"] = str(item["previous_display_key"])
                            applied.append(payload)
                        continue
                    realization = runtime_store.get_research_idea_realization(str(item["realization_id"]))
                    if realization is None:
                        continue
                    repaired = ResearchIdeaRealization(
                        id=realization.id,
                        research_topic_id=realization.research_topic_id,
                        topic_workspace_id=realization.topic_workspace_id,
                        idea_id=realization.idea_id,
                        record_id=realization.record_id,
                        source_json_path=str(item["source_json_path"]),
                        realization_stage=realization.realization_stage,
                        semantic_id=realization.semantic_id,
                        latest=realization.latest,
                        metadata={**realization.metadata, "repair_source": "ideas.repair", "previous_source_json_path": realization.source_json_path},
                        created_at=realization.created_at,
                        updated_at=now,
                        provenance_refs=realization.provenance_refs,
                    )
                    runtime_store.upsert_research_idea_realization(repaired)
                    applied.append({"realization_id": repaired.id, "source_json_path": repaired.source_json_path})
        validation_payload, _ = validate_research_ideas(context, env=env)
        return {
            "ok": validation_payload.get("ok", False),
            "mutated": apply,
            "operation": "ideas.repair",
            "apply": apply,
            "update_payloads": update_payloads,
            "diagnostics": validation_payload.get("diagnostics", []),
            "plan": plan,
            "applied": applied,
            "note": "Managed payload files are not mutated unless a dedicated payload-update repair path is implemented and explicitly enabled.",
        }, diagnostics
    finally:
        runtime_store.close()


def backfill_lineage(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    dry_run: bool = True,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """Backfill canonical lineage from explicit structured refs only."""

    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=dry_run)
    if runtime_store is None:
        return _runtime_missing_payload("lineage.backfill", diagnostics), diagnostics
    try:
        now = utc_timestamp()
        planned_edges: list[ResearchRecordLineageEdge] = []
        for record in runtime_store.list_lifecycle_records():
            if not _belongs_to_context(record, context):
                continue
            metadata = record.transition_metadata
            for parent_id, kind, role, source in _explicit_lineage_refs_for_backfill(record, runtime_store.get_structured_payload(record.id)):
                planned_edges.append(
                    _lineage_edge(
                        context,
                        parent_record_id=parent_id,
                        child_record_id=record.id,
                        lineage_kind=kind,
                        parent_role=role,
                        generation_id=None,
                        decision_record_id=_optional_metadata_string(metadata.get("decision_record_id")),
                        rationale=None,
                        status="ready",
                        metadata={"backfill_source": source},
                        created_at=now,
                        updated_at=now,
                    )
                )
        diagnostics_json: list[dict[str, object]] = []
        accepted: list[ResearchRecordLineageEdge] = []
        for edge in planned_edges:
            edge_diagnostics = runtime_store.validate_research_record_lineage_edge(edge)
            diagnostics_json.extend(edge_diagnostics)
            if not _has_lineage_errors(edge_diagnostics):
                accepted.append(edge)
        if not dry_run:
            with runtime_store.connection:
                for edge in accepted:
                    runtime_store.upsert_research_record_lineage_edge(edge, validate=False)
            for edge in accepted:
                refresh_query_index_for_record(context, runtime_store, edge.parent_record_id)
                refresh_query_index_for_record(context, runtime_store, edge.child_record_id)
        return {
            "ok": not _has_lineage_errors(diagnostics_json),
            "mutated": not dry_run,
            "operation": "lineage.backfill",
            "dry_run": dry_run,
            "planned_count": len(planned_edges),
            "accepted_count": len(accepted),
            "edges": [edge.to_json() for edge in accepted],
            "diagnostics": diagnostics_json,
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

    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=output_file is None)
    if runtime_store is None:
        return _runtime_missing_payload("render", diagnostics), diagnostics
    try:
        record = runtime_store.get_lifecycle_record(record_id)
        if record is None or not _belongs_to_context(record, context):
            raise ResearchRecordError(f"Research record not found: {record_id}", code="record_not_found")
        structured_payload = runtime_store.get_structured_payload(record_id)
        if structured_payload is None:
            raise ResearchRecordError(f"Research record is not structured: {record_id}", code="structured_payload_missing")
        payload_json, payload_diagnostics = _read_structured_payload_json(structured_payload)
        diagnostics.extend(payload_diagnostics)
        if payload_json is None:
            return _diagnostic_payload("render", diagnostics), diagnostics
        registry = _artifact_format_registry(context, runtime_store)
        render = render_artifact(
            payload_json,
            registry=registry,
            output_format="markdown",
            format_profile_ref=structured_payload.format_profile_ref,
            schema_ref=None if structured_payload.format_profile_ref is not None else structured_payload.schema_ref,
            template_ref=None if structured_payload.format_profile_ref is not None else structured_payload.template_ref,
        )
        diagnostics.extend(render.diagnostics)
        output_digest = None
        output_path = None
        index_payload: dict[str, object] | None = None
        response_record = record
        if render.ok and output_file is not None and render.content is not None:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(render.content, encoding="utf-8")
            output_path = output_file.resolve(strict=False)
            output_digest = digest_bytes(output_path.read_bytes())
            export_record = {
                "path": str(output_path),
                "format": "markdown",
                "file_role": "generated_markdown_export",
                "source_record_id": record.id,
                "payload_digest": structured_payload.payload_digest,
                "template_ref": render.template_ref,
                "template_digest": render.template_digest,
                "output_digest": output_digest,
                "exported_at": utc_timestamp(),
                "provenance_refs": [_provenance_ref("structured-record-render-export", record.id)],
            }
            metadata = dict(record.transition_metadata)
            generated_exports = metadata.get("generated_exports")
            exports = [item for item in generated_exports if isinstance(item, dict)] if isinstance(generated_exports, list) else []
            exports.append({key: value for key, value in export_record.items() if value is not None})
            metadata["generated_exports"] = exports
            updated = RuntimeLifecycleRecord(
                **{
                    **record.__dict__,
                    "updated_at": str(export_record["exported_at"]),
                    "transition_metadata": metadata,
                    "provenance_refs": [*record.provenance_refs, _provenance_ref("structured-record-render-export", record.id)],
                }
            )
            with runtime_store.connection:
                runtime_store.upsert_lifecycle_record(updated)
            response_record = runtime_store.get_lifecycle_record(record.id) or updated
            index_payload = refresh_query_index_for_record(context, runtime_store, record.id)
        return {
            "ok": render.ok,
            "mutated": output_file is not None and render.ok,
            "operation": "render",
            "record": response_record.to_json(),
            "render": render.to_json(include_content=True),
            "output_file": str(output_path or output_file) if output_file is not None else None,
            "output_digest": output_digest,
            "query_index": index_payload,
        }, diagnostics
    finally:
        runtime_store.close()


def migrate_structured_payload_files(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    cwd: Path,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """Export legacy SQLite structured payload rows into managed JSON files."""

    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    if runtime_store is None:
        return _runtime_missing_payload("migrate-payload-files", diagnostics), diagnostics
    migrated: list[dict[str, object]] = []
    skipped: list[dict[str, object]] = []
    try:
        for structured_payload in runtime_store.list_structured_payloads(topic_workspace_id=context.topic_workspace_id):
            if structured_payload.payload_file_path is not None and Path(structured_payload.payload_file_path).exists():
                skipped.append({"record_id": structured_payload.record_id, "reason": "payload_file_exists"})
                continue
            record = runtime_store.get_lifecycle_record(structured_payload.record_id)
            if record is None or not _belongs_to_context(record, context):
                skipped.append({"record_id": structured_payload.record_id, "reason": "missing_lifecycle_record"})
                continue
            payload = structured_payload.payload_json
            if not isinstance(payload, dict):
                skipped.append({"record_id": structured_payload.record_id, "reason": "payload_not_object"})
                continue
            request = ResearchRecordRequest(
                record_kind=record.record_kind,
                record_id=record.id,
                status=record.status,
                placeholder=_optional_metadata_string(record.transition_metadata.get("placeholder")),
                profile=_optional_metadata_string(record.transition_metadata.get("profile")),
                semantic_label=_optional_metadata_string(record.transition_metadata.get("semantic_label")),
                format_profile_ref=structured_payload.format_profile_ref,
                schema_ref=structured_payload.schema_ref,
                template_ref=structured_payload.template_ref,
                metadata=dict(record.transition_metadata),
            )
            payload_path, manifest_path, write_diagnostics = _write_payload_snapshot(
                context,
                request,
                payload,
                validation_payload={
                    "payload_digest": structured_payload.payload_digest,
                    "format_profile_ref": structured_payload.format_profile_ref,
                    "schema_ref": structured_payload.schema_ref,
                    "schema_version": structured_payload.schema_version,
                    "status": structured_payload.validation_status,
                },
                env=env,
                cwd=cwd,
            )
            diagnostics.extend(write_diagnostics)
            if payload_path is None:
                skipped.append({"record_id": structured_payload.record_id, "reason": "payload_path_unresolved"})
                continue
            revision_of, supersedes, latest_for = _payload_revision_refs(request)
            migrated_payload = replace(
                structured_payload,
                payload_json={},
                payload_file_path=str(payload_path),
                payload_media_type="application/json",
                payload_manifest_path=str(manifest_path) if manifest_path is not None else None,
                payload_source_path=None,
                revision_of_record_id=structured_payload.revision_of_record_id or revision_of,
                supersedes_record_id=structured_payload.supersedes_record_id or supersedes,
                latest_for_semantic_id=structured_payload.latest_for_semantic_id or latest_for,
                legacy_rendered_markdown_path=structured_payload.legacy_rendered_markdown_path or structured_payload.rendered_markdown_path,
                legacy_rendered_markdown_digest=structured_payload.legacy_rendered_markdown_digest or structured_payload.rendered_markdown_digest,
                rendered_markdown_path=None,
                rendered_markdown_digest=None,
                updated_at=utc_timestamp(),
                provenance_refs=[
                    *structured_payload.provenance_refs,
                    _provenance_ref("structured-payload-file-migration", structured_payload.record_id),
                ],
            )
            metadata = dict(record.transition_metadata)
            metadata.update(
                {
                    "payload_file_path": str(payload_path),
                    "payload_media_type": "application/json",
                    "payload_manifest_path": str(manifest_path) if manifest_path is not None else None,
                    "payload_digest": structured_payload.payload_digest,
                    "legacy_rendered_markdown_path": structured_payload.rendered_markdown_path,
                }
            )
            updated_record = RuntimeLifecycleRecord(
                **{
                    **record.__dict__,
                    "content_path": str(payload_path),
                    "updated_at": migrated_payload.updated_at,
                    "transition_metadata": {key: value for key, value in metadata.items() if value is not None},
                    "provenance_refs": [
                        *record.provenance_refs,
                        _provenance_ref("structured-payload-file-migration", record.id),
                    ],
                }
            )
            with runtime_store.connection:
                runtime_store.upsert_lifecycle_record(updated_record)
                runtime_store.upsert_structured_payload(migrated_payload)
            refresh_payload = refresh_query_index_for_record(context, runtime_store, record.id)
            migrated.append(
                {
                    "record_id": record.id,
                    "payload_file_path": str(payload_path),
                    "payload_manifest_path": str(manifest_path) if manifest_path is not None else None,
                    "query_index": refresh_payload,
                }
            )
        return {
            "ok": not has_errors(diagnostics),
            "mutated": bool(migrated),
            "operation": "migrate-payload-files",
            "migrated_count": len(migrated),
            "skipped_count": len(skipped),
            "migrated": migrated,
            "skipped": skipped,
        }, diagnostics
    finally:
        runtime_store.close()


def _validate_record_kind(record_kind: str) -> None:
    if record_kind not in LIFECYCLE_RECORD_KINDS:
        raise ResearchRecordError(f"Unsupported research record kind: {record_kind}", code="unsupported_record_kind")


def _validate_status(status: str) -> None:
    if status not in LIFECYCLE_STATUSES:
        raise ResearchRecordError(f"Unsupported research record status: {status}", code="unsupported_record_status")


SEMANTIC_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*:[a-z0-9][a-z0-9-]*$")


def _validate_semantic_id(semantic_id: str | None) -> None:
    if semantic_id is not None and SEMANTIC_ID_RE.fullmatch(semantic_id) is None:
        raise ResearchRecordError(
            "Semantic id must use exact <family>:<semantic-id> lowercase slug syntax.",
            code="invalid_semantic_id",
        )


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
    diagnostics.extend(_structured_display_diagnostics(payload, payload_file=request.payload_file))
    diagnostics.extend(_structured_semantic_diagnostics(payload, request, payload_file=request.payload_file))

    selected_request = request
    if durable and request.schema_file is not None:
        selected_request, snapshot_diagnostics = _snapshot_plain_format_inputs(context, runtime_store, request)
        diagnostics.extend(snapshot_diagnostics)
        if has_errors(diagnostics):
            return None, None, diagnostics
    diagnostics.extend(_unsupported_structured_format_diagnostics(selected_request))
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
    if selected_request.format_profile_ref is not None:
        profile, _resolution, profile_diagnostics = ArtifactFormatResolver(registry).resolve_profile(
            selected_request.format_profile_ref
        )
        diagnostics.extend(profile_diagnostics)
        if profile is not None:
            compatible = profile.metadata.get("compatible_record_kinds")
            if isinstance(compatible, list) and selected_request.record_kind not in compatible:
                diagnostics.append(
                    Diagnostic(
                        code="record_kind_profile_mismatch",
                        severity="error",
                        concept="Structured Research Payload",
                        path=request.payload_file,
                        field="record_kind",
                        message=f"Record kind {selected_request.record_kind!r} is incompatible with profile {profile.ref}; expected one of {compatible}.",
                    )
                )
    if not validation.ok:
        return None, None, diagnostics

    render_result = None
    content_path = None
    payload_file_path = None
    payload_manifest_path = None
    payload_source_path = str(request.payload_file.resolve(strict=False)) if request.payload_file is not None else None
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

    if durable:
        payload_file_path, payload_manifest_path, write_diagnostics = _write_payload_snapshot(
            context,
            selected_request,
            {str(key): value for key, value in payload.items()},
            validation_payload=validation.to_json(),
            env=env,
            cwd=cwd,
        )
        diagnostics.extend(write_diagnostics)
        content_path = payload_file_path

    template_ref = render_result.template_ref if render_result is not None else selected_request.template_ref
    template_source_kind = render_result.template_source_kind if render_result is not None else None
    revision_of_record_id, supersedes_record_id, latest_for_semantic_id = _payload_revision_refs(selected_request)
    return (
        StructuredPayloadPreparation(
            payload={str(key): value for key, value in payload.items()},
            payload_file_path=payload_file_path,
            payload_manifest_path=payload_manifest_path,
            payload_source_path=payload_source_path,
            payload_media_type="application/json",
            revision_of_record_id=revision_of_record_id,
            supersedes_record_id=supersedes_record_id,
            latest_for_semantic_id=latest_for_semantic_id,
            legacy_rendered_markdown_path=None,
            legacy_rendered_markdown_digest=None,
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
            rendered_markdown_path=None,
            rendered_markdown_digest=None,
            payload_digest=validation.payload_digest,
        ),
        content_path,
        diagnostics,
    )


def _structured_display_diagnostics(payload: Mapping[str, object], *, payload_file: Path | None) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    title = _optional_metadata_string(payload.get("title"))
    summary = _optional_metadata_string(payload.get("summary"))
    if title is None:
        diagnostics.append(
            Diagnostic(
                code="display_title_missing",
                severity="error",
                concept="Structured Research Payload",
                path=payload_file,
                field="title",
                message="Structured research record payloads require a non-empty title.",
            )
        )
    if summary is None:
        diagnostics.append(
            Diagnostic(
                code="display_summary_missing",
                severity="error",
                concept="Structured Research Payload",
                path=payload_file,
                field="summary",
                message="Structured research record payloads require a non-empty summary.",
            )
        )
    if title is not None and summary is not None and title.strip() == summary.strip():
        diagnostics.append(
            Diagnostic(
                code="display_fields_duplicate",
                severity="warning",
                concept="Structured Research Payload",
                path=payload_file,
                field="summary",
                message="Structured research record payload title and summary are identical.",
            )
        )
    return diagnostics


def _structured_semantic_diagnostics(
    payload: Mapping[str, object],
    request: ResearchRecordRequest,
    *,
    payload_file: Path | None,
) -> list[Diagnostic]:
    if request.semantic_id is None:
        return []
    diagnostics: list[Diagnostic] = []
    payload_semantic_id = _optional_metadata_string(payload.get("semantic_id"))
    if payload_semantic_id is not None and payload_semantic_id != request.semantic_id:
        diagnostics.append(
            Diagnostic(
                code="semantic_id_payload_mismatch",
                severity="error",
                concept="Structured Research Payload",
                path=payload_file,
                field="semantic_id",
                message=f"Payload semantic_id {payload_semantic_id!r} does not match authored semantic id {request.semantic_id!r}.",
            )
        )
    payload_family = _optional_metadata_string(payload.get("artifact_family"))
    request_family = request.semantic_id.split(":", 1)[0]
    if payload_family is not None and payload_family != request_family:
        diagnostics.append(
            Diagnostic(
                code="artifact_family_payload_mismatch",
                severity="error",
                concept="Structured Research Payload",
                path=payload_file,
                field="artifact_family",
                message=f"Payload artifact_family {payload_family!r} does not match semantic-id family {request_family!r}.",
            )
        )
    return diagnostics


def _unsupported_structured_format_diagnostics(request: ResearchRecordRequest) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for field, value in (
        ("format_profile_ref", request.format_profile_ref),
        ("schema_ref", request.schema_ref),
        ("template_ref", request.template_ref),
    ):
        if is_unsupported_deepsci_v1_ref(value):
            diagnostics.append(
                Diagnostic(
                    code="structured_record_v1_unsupported",
                    severity="error",
                    concept="Structured Research Payload",
                    field=field,
                    message="DeepSci structured-record.v1 refs are unsupported for new writes; use the supported v2 profile or schema.",
                    hint="Legacy v1 data may be read only by validation, repair, or migration code.",
                )
            )
    return diagnostics


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
                message="Markdown rendering from a plain schema file requires --template-file.",
            )
        ]
    stem = request.record_id or request.semantic_id or request.placeholder or request.content_name or "structured-payload"
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
    register_builtin_artifact_format_providers(registry)
    registry.register_provider(
        WorkspaceRuntimeArtifactFormatProvider(runtime_store, topic_workspace_id=context.topic_workspace_id)
    )
    return registry


def _write_payload_snapshot(
    context: EffectiveTopicContext,
    request: ResearchRecordRequest,
    payload: dict[str, object],
    *,
    validation_payload: dict[str, object],
    env: Mapping[str, str],
    cwd: Path,
) -> tuple[Path | None, Path | None, list[Diagnostic]]:
    label = _semantic_label_for_request(request)
    result, diagnostics = resolve_semantic_path(context, label, env=env, cwd=cwd)
    if result is None:
        return None, None, diagnostics
    if request.record_id is None:
        raise ResearchRecordError("Structured payload snapshot requires a record id.", code="record_id_missing")
    target_dir = _payload_snapshot_dir(result.path, request)
    target_dir.mkdir(parents=True, exist_ok=True)
    payload_path = target_dir / "payload.json"
    manifest_path = target_dir / "manifest.json"
    payload_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    manifest = {
        "schema_version": "isomer-structured-payload-file.v1",
        "record_id": request.record_id,
        "record_kind": request.record_kind,
        "research_topic_id": context.research_topic.id,
        "topic_workspace_id": context.topic_workspace_id,
        "payload_file": payload_path.name,
        "payload_digest": validation_payload.get("payload_digest"),
        "payload_media_type": "application/json",
        "format_profile_ref": validation_payload.get("format_profile_ref"),
        "semantic_id": request.semantic_id,
        "schema_ref": validation_payload.get("schema_ref"),
        "schema_version_ref": validation_payload.get("schema_version"),
        "validation_status": validation_payload.get("status"),
        "source_payload_file": str(request.payload_file.resolve(strict=False)) if request.payload_file is not None else None,
    }
    manifest_path.write_text(
        json.dumps({key: value for key, value in manifest.items() if value is not None}, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return payload_path.resolve(strict=False), manifest_path.resolve(strict=False), diagnostics


def _payload_snapshot_dir(base_path: Path, request: ResearchRecordRequest) -> Path:
    record_id = request.record_id or "structured-payload"
    candidate = base_path / "research-records" / request.record_kind / _slug(record_id)
    manifest_path = candidate / "manifest.json"
    if not manifest_path.exists():
        return candidate
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return candidate
    if isinstance(manifest, dict) and str(manifest.get("record_id") or "") == record_id:
        return candidate
    return candidate.with_name(f"{candidate.name}-{uuid.uuid4().hex[:8]}")


def _payload_revision_refs(request: ResearchRecordRequest) -> tuple[str | None, str | None, str | None]:
    metadata = request.metadata or {}
    revision_of = _optional_metadata_string(metadata.get("revision_of_record_id") or metadata.get("revision_of"))
    supersedes = _optional_metadata_string(metadata.get("supersedes_record_id") or metadata.get("supersedes"))
    latest_for = _optional_metadata_string(
        metadata.get("latest_for_semantic_id")
        or metadata.get("semantic_id")
        or request.semantic_id
        or request.placeholder
        or request.profile
        or request.content_name
    )
    return revision_of, supersedes, latest_for


def _optional_metadata_string(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _optional_float(value: object) -> float | None:
    if value is None:
        return None
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


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


def _revision_record_id(record: RuntimeLifecycleRecord) -> str:
    return f"{_slug(record.record_kind)}-{_slug(record.id)}-revision-{uuid.uuid4().hex[:8]}"


def _store_request_lineage(
    context: EffectiveTopicContext,
    runtime_store: WorkspaceRuntimeStore,
    request: ResearchRecordRequest,
    *,
    created_at: str,
    updated_at: str,
) -> dict[str, object]:
    parent_specs = _lineage_parent_specs(request)
    if not parent_specs:
        return {
            "ok": True,
            "edges": [],
            "generation_group": None,
            "diagnostics": [],
            "affected_parent_record_ids": [],
        }
    revision_parent_count = sum(1 for spec in parent_specs if spec["lineage_kind"] == "revision_of")
    if request.lineage_kind == "revision_of" and len(parent_specs) != 1:
        raise ResearchRecordError("revision_of lineage requires exactly one parent.", code="invalid_revision_lineage")
    if revision_parent_count > 1:
        raise ResearchRecordError("A child record can have at most one immediate revision_of parent.", code="invalid_revision_lineage")
    parent_ids = [str(spec["record_id"]) for spec in parent_specs]
    group = _generation_group_for_request(
        context,
        runtime_store,
        generation_id=request.generation_id,
        generation_purpose=request.generation_purpose,
        producer_skill=request.skill,
        decision_record_id=request.decision_record_id,
        parent_ids=parent_ids,
        created_at=created_at,
        updated_at=updated_at,
    )
    if group is not None:
        runtime_store.upsert_research_record_generation_group(group)
    edges: list[ResearchRecordLineageEdge] = []
    diagnostics: list[dict[str, object]] = []
    for spec in parent_specs:
        edge = _lineage_edge(
            context,
            parent_record_id=str(spec["record_id"]),
            child_record_id=str(request.record_id),
            lineage_kind=str(spec["lineage_kind"]),
            parent_role=spec["parent_role"],
            generation_id=group.id if group is not None else request.generation_id,
            decision_record_id=spec["decision_record_id"],
            rationale=spec["rationale"],
            status=str(spec["status"]),
            metadata=spec["metadata"],
            created_at=created_at,
            updated_at=updated_at,
        )
        edge_diagnostics = runtime_store.validate_research_record_lineage_edge(edge)
        diagnostics.extend(edge_diagnostics)
        if _has_lineage_errors(edge_diagnostics):
            raise ResearchRecordError(
                "Canonical lineage failed validation.",
                code="lineage_validation_failed",
                payload={"diagnostics": diagnostics},
            )
        runtime_store.upsert_research_record_lineage_edge(edge, validate=False)
        edges.append(edge)
    return {
        "ok": True,
        "edges": [edge.to_json() for edge in edges],
        "generation_group": group.to_json() if group is not None else None,
        "diagnostics": diagnostics,
        "affected_parent_record_ids": sorted({edge.parent_record_id for edge in edges}),
    }


def _lineage_parent_specs(request: ResearchRecordRequest) -> list[LineageParentSpec]:
    specs: list[LineageParentSpec] = []
    for index, item in enumerate(request.parents or []):
        parent_id = _optional_metadata_string(
            item.get("record_id")
            or item.get("parent_record_id")
            or item.get("id")
            or item.get("ref")
        )
        if parent_id is None:
            raise ResearchRecordError(f"parents-json[{index}] must include record_id.", code="invalid_lineage_parent")
        lineage_kind = _optional_metadata_string(item.get("lineage_kind") or item.get("kind") or request.lineage_kind) or "derived_from"
        if lineage_kind not in RESEARCH_RECORD_LINEAGE_KINDS:
            raise ResearchRecordError(f"Unsupported lineage kind: {lineage_kind}", code="unsupported_lineage_kind")
        metadata = dict(item)
        metadata.setdefault("lineage_input_source", "parents-json")
        specs.append(
            LineageParentSpec(
                record_id=parent_id,
                lineage_kind=lineage_kind,
                parent_role=_optional_metadata_string(item.get("parent_role") or item.get("role")),
                decision_record_id=_optional_metadata_string(item.get("decision_record_id") or request.decision_record_id),
                rationale=_optional_metadata_string(item.get("rationale") or request.lineage_rationale),
                status=_optional_metadata_string(item.get("status")) or "ready",
                metadata=metadata,
            )
        )
    return specs


def _generation_group_for_request(
    context: EffectiveTopicContext,
    runtime_store: WorkspaceRuntimeStore,
    *,
    generation_id: str | None,
    generation_purpose: str | None,
    producer_skill: str | None,
    decision_record_id: str | None,
    parent_ids: list[str],
    created_at: str,
    updated_at: str,
) -> ResearchRecordGenerationGroup | None:
    if generation_id is None:
        return None
    existing = runtime_store.get_research_record_generation_group(generation_id)
    return ResearchRecordGenerationGroup(
        id=generation_id,
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        purpose=generation_purpose or (existing.purpose if existing is not None else None),
        parent_set_digest=_parent_set_digest(parent_ids),
        producer_skill=producer_skill or (existing.producer_skill if existing is not None else None),
        decision_record_id=decision_record_id or (existing.decision_record_id if existing is not None else None),
        metadata=existing.metadata if existing is not None else {"parent_record_ids": sorted(parent_ids)},
        created_at=existing.created_at if existing is not None else created_at,
        updated_at=updated_at,
        provenance_refs=existing.provenance_refs if existing is not None else [_provenance_ref("research-record-generation-group", generation_id)],
    )


def _store_request_ideas(
    context: EffectiveTopicContext,
    runtime_store: WorkspaceRuntimeStore,
    request: ResearchRecordRequest,
    *,
    record_id: str,
    created_at: str,
    updated_at: str,
) -> dict[str, object]:
    ideas: list[dict[str, object]] = []
    realizations: list[dict[str, object]] = []
    edges: list[dict[str, object]] = []
    diagnostics: list[dict[str, object]] = []
    if request.primary_idea:
        item = request.primary_idea
        idea_id = _optional_metadata_string(item.get("idea_id") or item.get("id"))
        title = _optional_metadata_string(item.get("title"))
        summary = _optional_metadata_string(item.get("summary"))
        if idea_id is None or title is None or summary is None:
            raise ResearchRecordError("primary-idea-json must include idea_id, title, and summary.", code="invalid_primary_idea")
        existing = runtime_store.get_research_idea(idea_id, topic_workspace_id=context.topic_workspace_id)
        idea = _idea_record(
            context,
            idea_id=idea_id,
            display_key=_optional_metadata_string(item.get("display_key")) or (existing.display_key if existing is not None and existing.display_key is not None else runtime_store.next_research_idea_display_key(context.topic_workspace_id)),
            title=title,
            summary=summary,
            family=_optional_metadata_string(item.get("family")),
            status=_optional_metadata_string(item.get("status")) or "candidate",
            visibility=_optional_metadata_string(item.get("visibility")) or "primary",
            aliases=_string_list(item.get("aliases")),
            source_record_id=record_id,
            source_json_path=_optional_metadata_string(item.get("source_json_path")),
            metadata=dict(item),
            created_at=existing.created_at if existing is not None else created_at,
            updated_at=updated_at,
        )
        idea_diagnostics = runtime_store.validate_research_idea(idea)
        diagnostics.extend(idea_diagnostics)
        if _has_lineage_errors(idea_diagnostics):
            raise ResearchRecordError("Research idea failed validation.", code="idea_validation_failed", payload={"diagnostics": diagnostics})
        runtime_store.upsert_research_idea(idea, validate=False)
        ideas.append(idea.to_json())
    realization_inputs = list(request.idea_realizations or [])
    if request.realizes_idea_id is not None:
        realization_inputs.append({"idea_id": request.realizes_idea_id, "latest": True, "source": "realizes-idea-id"})
    for index, item in enumerate(realization_inputs):
        idea_id = _optional_metadata_string(item.get("idea_id") or item.get("id"))
        if idea_id is None:
            raise ResearchRecordError(f"idea-realizations-json[{index}] must include idea_id.", code="invalid_idea_realization")
        realization = _idea_realization_record(
            context,
            idea_id=idea_id,
            record_id=record_id,
            source_json_path=_optional_metadata_string(item.get("source_json_path")),
            realization_stage=_optional_metadata_string(item.get("realization_stage") or item.get("stage")),
            semantic_id=_optional_metadata_string(item.get("semantic_id")),
            latest=bool(item.get("latest", True)),
            metadata=dict(item),
            created_at=created_at,
            updated_at=updated_at,
        )
        realization_diagnostics = runtime_store.validate_research_idea_realization(realization)
        realization_diagnostics.extend(_validate_realization_source(context, runtime_store, realization, report_missing_payload=False))
        diagnostics.extend(realization_diagnostics)
        if _has_lineage_errors(realization_diagnostics):
            raise ResearchRecordError("Research idea realization failed validation.", code="idea_realization_validation_failed", payload={"diagnostics": diagnostics})
        runtime_store.upsert_research_idea_realization(realization, validate=False)
        realizations.append(realization.to_json())
    child_idea_id = request.realizes_idea_id or _optional_metadata_string((request.primary_idea or {}).get("idea_id"))
    for index, item in enumerate(request.idea_parents or []):
        parent_idea_id = _optional_metadata_string(item.get("idea_id") or item.get("parent_idea_id") or item.get("id"))
        selected_child = _optional_metadata_string(item.get("child_idea_id")) or child_idea_id
        if parent_idea_id is None or selected_child is None:
            raise ResearchRecordError(f"idea-parents-json[{index}] must include parent idea_id and child_idea_id or --realizes-idea-id.", code="invalid_idea_parent")
        lineage_kind = _optional_metadata_string(item.get("lineage_kind") or item.get("kind")) or "derived_from"
        edge = _idea_lineage_edge(
            context,
            parent_idea_id=parent_idea_id,
            child_idea_id=selected_child,
            lineage_kind=lineage_kind,
            parent_role=_optional_metadata_string(item.get("parent_role") or item.get("role")),
            generation_id=_optional_metadata_string(item.get("generation_id") or request.generation_id),
            decision_record_id=_optional_metadata_string(item.get("decision_record_id") or request.decision_record_id),
            rationale=_optional_metadata_string(item.get("rationale") or request.lineage_rationale),
            status=_optional_metadata_string(item.get("status")) or "ready",
            confidence=_optional_float(item.get("confidence")),
            metadata=dict(item),
            created_at=created_at,
            updated_at=updated_at,
        )
        edge_diagnostics = runtime_store.validate_research_idea_lineage_edge(edge)
        diagnostics.extend(edge_diagnostics)
        if _has_lineage_errors(edge_diagnostics):
            raise ResearchRecordError("Research idea lineage failed validation.", code="idea_lineage_validation_failed", payload={"diagnostics": diagnostics})
        runtime_store.upsert_research_idea_lineage_edge(edge, validate=False)
        edges.append(edge.to_json())
    return {"ideas": ideas, "realizations": realizations, "edges": edges, "diagnostics": diagnostics}


def _idea_record(
    context: EffectiveTopicContext,
    *,
    idea_id: str,
    display_key: str | None = None,
    title: str,
    summary: str,
    family: str | None,
    status: str,
    visibility: str,
    aliases: list[str],
    source_record_id: str | None,
    source_json_path: str | None,
    metadata: dict[str, object],
    created_at: str,
    updated_at: str,
) -> ResearchIdea:
    stable_id = f"idea-{_slug(context.topic_workspace_id)}-{_slug(idea_id)}"
    return ResearchIdea(
        id=stable_id,
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        idea_id=idea_id,
        display_key=display_key,
        title=title,
        summary=summary,
        family=family,
        status=status,
        visibility=visibility,
        aliases=sorted(set(aliases)),
        source_record_id=source_record_id,
        source_json_path=source_json_path,
        metadata=metadata,
        created_at=created_at,
        updated_at=updated_at,
        provenance_refs=[_provenance_ref("research-idea", idea_id)],
    )


def _idea_realization_record(
    context: EffectiveTopicContext,
    *,
    idea_id: str,
    record_id: str,
    source_json_path: str | None,
    realization_stage: str | None,
    semantic_id: str | None,
    latest: bool,
    metadata: dict[str, object],
    created_at: str,
    updated_at: str,
) -> ResearchIdeaRealization:
    digest = digest_json({"topic_workspace_id": context.topic_workspace_id, "idea_id": idea_id, "record_id": record_id, "source_json_path": source_json_path})[:16]
    realization_id = f"idea-realization-{digest}"
    return ResearchIdeaRealization(
        id=realization_id,
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        idea_id=idea_id,
        record_id=record_id,
        source_json_path=source_json_path,
        realization_stage=realization_stage,
        semantic_id=semantic_id,
        latest=latest,
        metadata=metadata,
        created_at=created_at,
        updated_at=updated_at,
        provenance_refs=[_provenance_ref("research-idea-realization", realization_id)],
    )


def _idea_lineage_edge(
    context: EffectiveTopicContext,
    *,
    parent_idea_id: str,
    child_idea_id: str,
    lineage_kind: str,
    parent_role: str | None,
    generation_id: str | None,
    decision_record_id: str | None,
    rationale: str | None,
    status: str,
    confidence: float | None,
    metadata: dict[str, object],
    created_at: str,
    updated_at: str,
) -> ResearchIdeaLineageEdge:
    if lineage_kind not in RESEARCH_IDEA_LINEAGE_KINDS and lineage_kind != "revision_of":
        raise ResearchRecordError(f"Unsupported idea lineage kind: {lineage_kind}", code="unsupported_idea_lineage_kind")
    digest = digest_json(
        {
            "topic_workspace_id": context.topic_workspace_id,
            "parent_idea_id": parent_idea_id,
            "child_idea_id": child_idea_id,
            "lineage_kind": lineage_kind,
            "parent_role": parent_role,
            "generation_id": generation_id,
        }
    )[:16]
    edge_id = f"idea-lineage-{_slug(lineage_kind)}-{digest}"
    return ResearchIdeaLineageEdge(
        id=edge_id,
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        parent_idea_id=parent_idea_id,
        child_idea_id=child_idea_id,
        lineage_kind=lineage_kind,
        parent_role=parent_role,
        generation_id=generation_id,
        decision_record_id=decision_record_id,
        rationale=rationale,
        status=status,
        confidence=confidence,
        metadata=metadata,
        created_at=created_at,
        updated_at=updated_at,
        provenance_refs=[_provenance_ref("research-idea-lineage", edge_id)],
    )


def _idea_parent_set_digest(parent_idea_ids: list[str]) -> str:
    return digest_json({"parent_idea_ids": sorted(set(parent_idea_ids))})


def _validate_realization_source(
    context: EffectiveTopicContext,
    runtime_store: WorkspaceRuntimeStore,
    realization: ResearchIdeaRealization,
    *,
    report_missing_payload: bool,
) -> list[dict[str, object]]:
    idea = runtime_store.get_research_idea(realization.idea_id, topic_workspace_id=realization.topic_workspace_id)
    structured = runtime_store.get_structured_payload(realization.record_id)
    if structured is None and not report_missing_payload and not realization.source_json_path:
        return []
    latest_primary = idea is not None and idea.visibility == "primary" and realization.latest
    severity = "error" if latest_primary and structured is not None else "warning"
    resolution = resolve_structured_source_fragment(
        context,
        structured,
        realization.source_json_path,
        idea_id=realization.idea_id,
        record_id=realization.record_id,
        severity=severity,
    )
    diagnostics = list(resolution.diagnostics)
    if resolution.status == SOURCE_STATUS_EXACT and idea is not None and isinstance(resolution.source_json, Mapping):
        labels = _idea_source_labels(resolution.source_json)
        known = {idea.idea_id, *idea.aliases}
        if labels and labels.isdisjoint(known):
            diagnostics.append(
                _source_diag(
                    severity,
                    "idea_source_label_mismatch",
                    "Source fragment label does not match the canonical idea id or aliases.",
                    idea_id=idea.idea_id,
                    record_id=realization.record_id,
                    source_json_path=realization.source_json_path,
                    source_labels=sorted(labels),
                    known_labels=sorted(known),
                )
            )
    return diagnostics


def _idea_source_labels(source_json: Mapping[str, object]) -> set[str]:
    labels: set[str] = set()
    for key in ("canonical_idea_id", "idea_id", "id", "label", "candidate_id"):
        value = source_json.get(key)
        if isinstance(value, str) and value.strip():
            labels.add(value.strip())
    return labels


def _source_diag(severity: str, code: str, message: str, **details: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "severity": severity,
        "code": code,
        "concept": "Research Idea Source JSON",
        "message": message,
    }
    payload.update({key: value for key, value in details.items() if value is not None})
    return payload


def _idea_import_plan_from_fragments(
    context: EffectiveTopicContext,
    fragments: list[IdeaEntryFragment],
    record_id: str,
) -> list[dict[str, object]]:
    plan: list[dict[str, object]] = []
    for fragment in fragments:
        item_map = dict(fragment.source_json)
        title = _optional_metadata_string(item_map.get("title"))
        summary = _optional_metadata_string(item_map.get("summary"))
        if title is None or summary is None:
            continue
        source_id = _optional_metadata_string(item_map.get("idea_id") or item_map.get("id") or item_map.get("label") or item_map.get("candidate_id"))
        idea_id = _optional_metadata_string(item_map.get("canonical_idea_id")) or f"idea-{_slug(source_id or title)}"
        family = _optional_metadata_string(item_map.get("family")) or fragment.source_json_path.rsplit(".", 1)[-1].split("[", 1)[0]
        plan.append(
            {
                "idea_id": idea_id,
                "display_key": _optional_metadata_string(item_map.get("display_key")),
                "title": title,
                "summary": summary,
                "family": family,
                "status": _optional_metadata_string(item_map.get("status")) or ("selected" if "selected" in fragment.source_json_path else "candidate"),
                "visibility": _optional_metadata_string(item_map.get("visibility")) or "primary",
                "aliases": [source_id] if source_id else [],
                "source_record_id": record_id,
                "source_json_path": fragment.source_json_path,
                "latest": bool(item_map.get("latest", False)),
                "metadata": {"source_payload": item_map, "research_topic_id": context.research_topic.id},
            }
        )
    return plan


def _idea_repair_plan(context: EffectiveTopicContext, runtime_store: WorkspaceRuntimeStore) -> list[dict[str, object]]:
    plan: list[dict[str, object]] = []
    next_display_key = runtime_store.next_research_idea_display_key(context.topic_workspace_id)
    next_match = re.fullmatch(r"I-(?P<number>[1-9][0-9]*)", next_display_key)
    next_number = int(next_match.group("number")) if next_match else 1
    ideas = runtime_store.list_research_ideas(topic_workspace_id=context.topic_workspace_id, include_archived=True)
    allocated_keys = _allocated_display_keys(runtime_store, context.topic_workspace_id)
    occupied_targets = {key: idea.idea_id for idea in ideas for key in [idea.display_key] if key}
    planned_targets: dict[str, str] = {}
    for idea in ideas:
        display_key = (idea.display_key or "").strip()
        old_match = re.fullmatch(r"I(?P<number>[1-9][0-9]*)", display_key)
        if old_match:
            target = f"I-{old_match.group('number')}"
            diagnostics: list[dict[str, object]] = []
            collision_idea = occupied_targets.get(target)
            collision_plan = planned_targets.get(target)
            if collision_idea is not None and collision_idea != idea.idea_id:
                diagnostics.append(_display_key_migration_collision(idea.idea_id, display_key, target, "research_ideas", collision_idea))
            if target in allocated_keys and allocated_keys[target] != idea.idea_id:
                diagnostics.append(_display_key_migration_collision(idea.idea_id, display_key, target, "research_idea_display_keys", allocated_keys[target]))
            if collision_plan is not None and collision_plan != idea.idea_id:
                diagnostics.append(_display_key_migration_collision(idea.idea_id, display_key, target, "repair_plan", collision_plan))
            planned_targets[target] = idea.idea_id
            plan.append(
                {
                    "action": "migrate_display_key",
                    "idea_id": idea.idea_id,
                    "previous_display_key": display_key,
                    "display_key": target,
                    "visibility": idea.visibility,
                    "status": idea.status,
                    "diagnostics": diagnostics,
                }
            )
            continue
        if display_key:
            continue
        assigned = f"I-{next_number}"
        next_number += 1
        plan.append(
            {
                "action": "assign_display_key",
                "idea_id": idea.idea_id,
                "display_key": assigned,
                "visibility": idea.visibility,
                "status": idea.status,
            }
        )
    for realization in runtime_store.list_research_idea_realizations(topic_workspace_id=context.topic_workspace_id):
        lineage_idea = runtime_store.get_research_idea(realization.idea_id, topic_workspace_id=context.topic_workspace_id)
        structured = runtime_store.get_structured_payload(realization.record_id)
        if lineage_idea is None or structured is None:
            continue
        resolution = resolve_structured_source_fragment(
            context,
            structured,
            realization.source_json_path,
            idea_id=lineage_idea.idea_id,
            record_id=realization.record_id,
            severity="warning",
        )
        if resolution.status == SOURCE_STATUS_EXACT:
            continue
        payload, payload_diagnostics = load_structured_payload(context, structured)
        if not isinstance(payload, Mapping):
            continue
        fragments, _ = profile_idea_entry_fragments(payload, structured.format_profile_ref, record_id=realization.record_id)
        match = _matching_fragment_for_idea(lineage_idea, fragments)
        if match is None:
            continue
        plan.append(
            {
                "action": "update_realization_source_path",
                "idea_id": lineage_idea.idea_id,
                "realization_id": realization.id,
                "record_id": realization.record_id,
                "previous_source_json_path": realization.source_json_path,
                "source_json_path": match.source_json_path,
                "diagnostics": [*payload_diagnostics, *resolution.diagnostics],
            }
        )
    return plan


def _allocated_display_keys(runtime_store: WorkspaceRuntimeStore, topic_workspace_id: str) -> dict[str, str]:
    if not runtime_store.connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'research_idea_display_keys'"
    ).fetchone():
        return {}
    rows = runtime_store.connection.execute(
        "SELECT display_key, idea_id FROM research_idea_display_keys WHERE topic_workspace_id = ?",
        (topic_workspace_id,),
    )
    return {str(row["display_key"]): str(row["idea_id"]) for row in rows}


def _dict_list(value: object) -> list[dict[str, object]]:
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, Mapping)]


def _display_key_migration_collision(
    idea_id: str,
    previous_display_key: str,
    display_key: str,
    collision_source: str,
    collision_ref: str,
) -> dict[str, object]:
    return {
        "severity": "error",
        "code": "idea_display_key_migration_collision",
        "message": f"Cannot migrate Research Idea display key {previous_display_key} to {display_key}; target is already allocated.",
        "idea_id": idea_id,
        "previous_display_key": previous_display_key,
        "display_key": display_key,
        "collision_source": collision_source,
        "collision_ref": collision_ref,
    }


def _matching_fragment_for_idea(idea: ResearchIdea, fragments: list[IdeaEntryFragment]) -> IdeaEntryFragment | None:
    known = {idea.idea_id, *idea.aliases}
    for fragment in fragments:
        if not _idea_source_labels(fragment.source_json).isdisjoint(known):
            return fragment
    normalized_title = _slug(idea.title)
    for fragment in fragments:
        title = _optional_metadata_string(fragment.source_json.get("title"))
        if title is not None and _slug(title) == normalized_title:
            return fragment
    return None


def _lineage_edge(
    context: EffectiveTopicContext,
    *,
    parent_record_id: str,
    child_record_id: str,
    lineage_kind: str,
    parent_role: str | None,
    generation_id: str | None,
    decision_record_id: str | None,
    rationale: str | None,
    status: str,
    metadata: dict[str, object],
    created_at: str,
    updated_at: str,
) -> ResearchRecordLineageEdge:
    edge_id = _lineage_edge_id(context.topic_workspace_id, parent_record_id, child_record_id, lineage_kind, parent_role, generation_id)
    return ResearchRecordLineageEdge(
        id=edge_id,
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        parent_record_id=parent_record_id,
        child_record_id=child_record_id,
        lineage_kind=lineage_kind,
        parent_role=parent_role,
        generation_id=generation_id,
        decision_record_id=decision_record_id,
        rationale=rationale,
        status=status,
        metadata=metadata,
        created_at=created_at,
        updated_at=updated_at,
        provenance_refs=[_provenance_ref("research-record-lineage", edge_id)],
    )


def _lineage_edge_id(
    topic_workspace_id: str,
    parent_record_id: str,
    child_record_id: str,
    lineage_kind: str,
    parent_role: str | None,
    generation_id: str | None,
) -> str:
    digest = digest_json(
        {
            "topic_workspace_id": topic_workspace_id,
            "parent_record_id": parent_record_id,
            "child_record_id": child_record_id,
            "lineage_kind": lineage_kind,
            "parent_role": parent_role,
            "generation_id": generation_id,
        }
    )[:16]
    return f"lineage-{_slug(lineage_kind)}-{digest}"


def _parent_set_digest(parent_ids: list[str]) -> str:
    return digest_json({"parent_record_ids": sorted(set(parent_ids))})


def _has_lineage_errors(diagnostics: list[dict[str, object]]) -> bool:
    return any(item.get("severity") == "error" for item in diagnostics)


def _missing_expected_lineage_diagnostics(
    context: EffectiveTopicContext,
    runtime_store: WorkspaceRuntimeStore,
) -> list[dict[str, object]]:
    incoming = {
        edge.child_record_id
        for edge in runtime_store.list_research_record_lineage_edges(topic_workspace_id=context.topic_workspace_id)
    }
    diagnostics: list[dict[str, object]] = []
    for record in runtime_store.list_lifecycle_records():
        if not _belongs_to_context(record, context) or record.status == "archived" or record.id in incoming:
            continue
        metadata = record.transition_metadata
        profile_ref = _optional_metadata_string(metadata.get("format_profile_ref") or metadata.get("profile")) or ""
        lineage_required = bool(metadata.get("lineage_required")) or _profile_normally_requires_lineage(profile_ref)
        if lineage_required:
            diagnostics.append(
                {
                    "severity": "warning",
                    "code": "lineage_expected_parent_missing",
                    "message": f"Record normally requires canonical lineage parents but has none: {record.id}",
                    "record_id": record.id,
                    "profile": profile_ref,
                }
            )
    return diagnostics


def _profile_normally_requires_lineage(profile_ref: str) -> bool:
    parent_dependent_tokens = (
        "candidate-idea-frontier",
        "pre-idea-draft",
        "selected-hypothesis",
        "selected-idea-draft",
        "experiment-contract",
        "main-run-record",
        "experiment-result-summary",
        "analysis-slice-record",
        "analysis-campaign-summary",
        "route-decision",
        "paper-contract",
        "draft-section-set",
        "review-report",
        "final-summary",
    )
    return any(token in profile_ref for token in parent_dependent_tokens)


def _affected_parent_record_ids(lineage_payload: Mapping[str, object]) -> list[str]:
    value = lineage_payload.get("affected_parent_record_ids")
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _explicit_lineage_refs_for_backfill(
    record: RuntimeLifecycleRecord,
    payload: StructuredResearchPayloadRecord | None,
) -> list[tuple[str, str, str | None, str]]:
    refs: list[tuple[str, str, str | None, str]] = []
    metadata = record.transition_metadata
    for key in ("revision_of_record_id", "revision_of", "supersedes_record_id", "supersedes"):
        parent = _optional_metadata_string(metadata.get(key))
        if parent is not None:
            refs.append((parent, "revision_of", "previous_revision", f"transition_metadata.{key}"))
    if payload is not None:
        for value, kind, role, source in (
            (payload.revision_of_record_id, "revision_of", "previous_revision", "structured_payload.revision_of_record_id"),
            (payload.supersedes_record_id, "revision_of", "previous_revision", "structured_payload.supersedes_record_id"),
        ):
            parent = _optional_metadata_string(value)
            if parent is not None:
                refs.append((parent, kind, role, source))
    for key in ("parent_record_id", "parent", "source_ref"):
        parent = _optional_metadata_string(metadata.get(key))
        if parent is not None:
            refs.append((parent, "derived_from", None, f"transition_metadata.{key}"))
    for key in ("source_refs", "parent_record_ids"):
        raw = metadata.get(key)
        if isinstance(raw, list):
            for item in raw:
                parent = _optional_metadata_string(item)
                if parent is not None:
                    refs.append((parent, "derived_from", None, f"transition_metadata.{key}"))
    query_index = metadata.get("query_index")
    if isinstance(query_index, dict):
        relationships = query_index.get("relationships")
        if isinstance(relationships, list):
            for item in relationships:
                if not isinstance(item, dict):
                    continue
                relationship_kind = _optional_metadata_string(item.get("lineage_kind") or item.get("relation_kind") or item.get("kind"))
                parent = _optional_metadata_string(item.get("parent_record_id") or item.get("target_record_id") or item.get("record_id") or item.get("ref"))
                if relationship_kind in RESEARCH_RECORD_LINEAGE_KINDS and parent is not None:
                    refs.append((parent, relationship_kind, _optional_metadata_string(item.get("role") or item.get("parent_role")), "transition_metadata.query_index.relationships"))
    return sorted(set(refs), key=lambda item: item[3:])


def _record_metadata(request: ResearchRecordRequest) -> dict[str, object]:
    metadata: dict[str, object] = dict(request.metadata or {})
    for key, value in (
        ("placeholder", request.placeholder),
        ("semantic_id", request.semantic_id),
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
    query_index: dict[str, object] = {}
    if request.relationships:
        query_index["relationships"] = request.relationships
    if request.file_attachments:
        query_index["files"] = request.file_attachments
    if request.index_hints:
        query_index["hints"] = request.index_hints
    if query_index:
        metadata["query_index"] = query_index
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
        "payload_media_type": preparation.payload_media_type,
        "validation_status": preparation.validation_status,
        "render_status": preparation.render_status,
    }
    if preparation.payload_file_path is not None:
        metadata["payload_file_path"] = str(preparation.payload_file_path)
    if preparation.payload_manifest_path is not None:
        metadata["payload_manifest_path"] = str(preparation.payload_manifest_path)
    if preparation.payload_source_path is not None:
        metadata["payload_source_path"] = preparation.payload_source_path
    if preparation.revision_of_record_id is not None:
        metadata["revision_of_record_id"] = preparation.revision_of_record_id
    if preparation.supersedes_record_id is not None:
        metadata["supersedes_record_id"] = preparation.supersedes_record_id
    if preparation.latest_for_semantic_id is not None:
        metadata["latest_for_semantic_id"] = preparation.latest_for_semantic_id
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
        payload_json={} if preparation.payload_file_path is not None else preparation.payload,
        payload_digest=preparation.payload_digest,
        payload_file_path=str(preparation.payload_file_path) if preparation.payload_file_path is not None else None,
        payload_media_type=preparation.payload_media_type,
        payload_manifest_path=str(preparation.payload_manifest_path) if preparation.payload_manifest_path is not None else None,
        payload_source_path=preparation.payload_source_path,
        revision_of_record_id=preparation.revision_of_record_id,
        supersedes_record_id=preparation.supersedes_record_id,
        latest_for_semantic_id=preparation.latest_for_semantic_id,
        legacy_rendered_markdown_path=preparation.legacy_rendered_markdown_path,
        legacy_rendered_markdown_digest=preparation.legacy_rendered_markdown_digest,
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


def _read_structured_payload_json(
    structured_payload: StructuredResearchPayloadRecord,
) -> tuple[dict[str, object] | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    if structured_payload.payload_file_path is None:
        return structured_payload.payload_json, diagnostics
    path = Path(structured_payload.payload_file_path)
    if not path.exists() or not path.is_file():
        diagnostics.append(
            Diagnostic(
                code="ISO208",
                severity="error",
                concept="Structured Research Payload",
                path=path,
                field=structured_payload.record_id,
                message="Structured payload file is missing.",
            )
        )
        return None, diagnostics
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        diagnostics.append(
            Diagnostic(
                code="ISO208",
                severity="error",
                concept="Structured Research Payload",
                path=path,
                field=structured_payload.record_id,
                message=f"Structured payload file is not valid JSON: {exc.msg}.",
            )
        )
        return None, diagnostics
    if not isinstance(loaded, dict):
        diagnostics.append(
            Diagnostic(
                code="ISO208",
                severity="error",
                concept="Structured Research Payload",
                path=path,
                field=structured_payload.record_id,
                message="Structured payload file must contain a JSON object.",
            )
        )
        return None, diagnostics
    payload = {str(key): value for key, value in loaded.items()}
    observed_digest = digest_json(payload)
    if observed_digest != structured_payload.payload_digest:
        diagnostics.append(
            Diagnostic(
                code="ISO208",
                severity="error",
                concept="Structured Research Payload",
                path=path,
                field=structured_payload.record_id,
                message="Structured payload file digest does not match the recorded payload digest.",
            )
        )
        return None, diagnostics
    return payload, diagnostics


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


def parse_json_object_list(raw: str | None, *, field_name: str) -> list[dict[str, object]]:
    if raw is None or not raw.strip():
        return []
    loaded = json.loads(raw)
    if not isinstance(loaded, list):
        raise ResearchRecordError(f"{field_name} must be a JSON array.", code="invalid_json_array")
    result: list[dict[str, object]] = []
    for index, item in enumerate(loaded):
        if not isinstance(item, dict):
            raise ResearchRecordError(f"{field_name}[{index}] must be a JSON object.", code="invalid_json_object")
        result.append({str(key): value for key, value in item.items()})
    return result
