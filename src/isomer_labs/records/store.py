"""Extension-backed research record CRUD over Workspace Runtime."""

from __future__ import annotations

from dataclasses import dataclass, replace
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import tempfile
from typing import Any, Mapping, TypedDict, cast
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
from isomer_labs.core.artifact_identity import (
    ArtifactIdentityError,
    extension_id_for_skill,
    packaged_extension_ids,
    parse_artifact_identity,
)
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
    ResearchIdeaArchiveState,
    ResearchIdeaDecisionOptionOutcome,
    ResearchIdeaDecisionOption,
    ResearchIdeaDecisionState,
    ResearchIdeaEvidenceState,
    ResearchIdeaExplorationState,
    ResearchIdeaFacet,
    ResearchIdeaGenerationGroup,
    ResearchIdeaLineageEdge,
    ResearchIdeaOperation,
    ResearchIdeaRealization,
    ResearchIdeaStateTransition,
    RuntimeLifecycleRecord,
    StructuredResearchPayloadRecord,
    project_research_idea_compatibility_status,
    research_idea_facets_from_legacy_status,
    utc_timestamp,
)
from isomer_labs.runtime.store import WorkspaceRuntimeStore, open_workspace_runtime
from isomer_labs.records.index import refresh_query_index_for_record
from isomer_labs.records.idea_sources import (
    SOURCE_STATUS_EXACT,
    IdeaEntryFragment,
    load_structured_payload,
    profile_idea_entry_fragments,
    resolve_payload_source_fragment,
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
    semantic_id: str | None = None
    scope_key: str | None = None
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
    registered_content_path: Path | None = None
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
    idea_effects: dict[str, object] | None = None
    idea_effects_required: bool = False


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
    _validate_write_artifact_identity(request)
    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    if runtime_store is None:
        return _runtime_missing_payload("create", diagnostics), diagnostics
    try:
        now = utc_timestamp()
        record_id = request.record_id or _new_record_id(request)
        request = replace(request, record_id=record_id)
        if runtime_store.get_lifecycle_record(record_id) is not None:
            raise ResearchRecordError(
                f"Research record already exists: {record_id}",
                code="record_already_exists",
                payload={"recovery_actions": ["Choose a new record id.", "Use update or revise for existing state."]},
            )
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
        try:
            request = _request_with_resolved_idea_effects(context, runtime_store, request, structured_payload)
        except ResearchRecordError:
            _cleanup_failed_record_content(request, content_path)
            raise
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
        try:
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
        except ResearchRecordError:
            _cleanup_failed_record_content(request, content_path)
            raise
        except Exception as exc:
            removed = _cleanup_failed_record_content(request, content_path)
            raise ResearchRecordError(
                f"Research record commit failed: {exc}",
                code="record_commit_failed",
                payload={
                    "recovery_actions": [
                        "Retry with the same idempotency key when using the typed Artifact service.",
                        "Inspect the reported cleanup paths before retrying if cleanup was incomplete.",
                    ],
                    "cleanup": removed,
                },
            ) from exc
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
    semantic_id: str | None = None,
    scope_key: str | None = None,
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
        selected_limit = effective_records_list_limit(context, limit, diagnostics)
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
            and _matches_metadata(record, "semantic_id", semantic_id)
            and _matches_metadata(record, "scope_key", scope_key)
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
    _validate_write_artifact_identity(request)
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
        existing_extension_id = extension_id_for_skill(_optional_metadata_string(existing.transition_metadata.get("skill")))
        _validate_semantic_id(existing_semantic_id, expected_extension=existing_extension_id)
        if existing_extension_id is not None and existing_semantic_id is None:
            raise ResearchRecordError(
                f"Extension-owned research record {record_id!r} has no canonical artifact identity.",
                code="artifact_identity_missing",
                payload={"expected_namespace": existing_extension_id.upper()},
            )
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
        request = _request_with_resolved_idea_effects(context, runtime_store, request, structured_payload)
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
    existing_semantic_id = _optional_metadata_string(existing_metadata.get("semantic_id"))
    latest_for = _optional_metadata_string(
        existing_metadata.get("latest_for_semantic_id")
        or existing_semantic_id
        or existing_metadata.get("profile")
        or existing.id
    )
    if latest_for is not None:
        request_metadata.setdefault("latest_for_semantic_id", latest_for)
    next_request = replace(
        request,
        record_kind=request.record_kind or existing.record_kind,
        record_id=request.record_id or _revision_record_id(existing),
        semantic_id=request.semantic_id or existing_semantic_id,
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
    status: str | None = None,
    exploration_state: str | None = None,
    decision_state: str | None = None,
    evidence_state: str | None = None,
    archive_state: str | None = None,
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
        compatibility_diagnostics: list[dict[str, object]] = []
        if status is not None:
            compatibility_diagnostics.append(
                {
                    "severity": "warning",
                    "code": "idea_status_deprecated",
                    "message": "Direct Research Idea status mutation is deprecated; use canonical facet arguments or the transition command.",
                    "status": status,
                }
            )
        if status is not None and all(value is None for value in (exploration_state, decision_state, evidence_state, archive_state)):
            legacy_facets = research_idea_facets_from_legacy_status(status)
            exploration_state, decision_state, evidence_state, archive_state = legacy_facets
        selected_exploration = exploration_state or (existing.exploration_state if existing is not None else "unknown")
        selected_decision = decision_state or (existing.decision_state if existing is not None else "unknown")
        selected_evidence = evidence_state or (existing.evidence_state if existing is not None else "unknown")
        selected_archive = archive_state or (existing.archive_state if existing is not None else "active")
        compatibility_status = project_research_idea_compatibility_status(
            exploration_state=selected_exploration,
            decision_state=selected_decision,
            evidence_state=selected_evidence,
            archive_state=selected_archive,
            preserved_status=status or (existing.status if existing is not None else None),
        )
        if status is not None and status != compatibility_status:
            raise ResearchRecordError(
                "Deprecated status conflicts with the canonical Research Idea facets.",
                code="idea_compatibility_status_conflict",
                payload={"status": status, "projected_status": compatibility_status},
            )
        record = _idea_record(
            context,
            idea_id=idea_id,
            display_key=existing.display_key if existing is not None and existing.display_key is not None else display_key or runtime_store.next_research_idea_display_key(context.topic_workspace_id),
            title=title,
            summary=summary,
            family=family,
            status=compatibility_status,
            exploration_state=selected_exploration,
            decision_state=selected_decision,
            evidence_state=selected_evidence,
            archive_state=selected_archive,
            visibility=visibility,
            aliases=aliases or (existing.aliases if existing is not None else []),
            source_record_id=source_record_id,
            source_json_path=source_json_path,
            metadata={**(metadata or (existing.metadata if existing is not None else {})), "portfolio_state_version": 1},
            created_at=existing.created_at if existing is not None else now,
            updated_at=now,
        )
        validation = runtime_store.validate_research_idea(record)
        if _has_lineage_errors(validation):
            raise ResearchRecordError("Research idea failed validation.", code="idea_validation_failed", payload={"diagnostics": validation})
        with runtime_store.connection:
            runtime_store.upsert_research_idea(record, validate=False)
        return {"ok": True, "mutated": True, "operation": "ideas.upsert", "idea": record.to_json(), "diagnostics": [*validation, *compatibility_diagnostics]}, diagnostics
    finally:
        runtime_store.close()


def transition_research_idea(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    idea_id: str,
    facet: str,
    expected_from: str,
    next_value: str,
    actor_ref: str,
    rationale: str,
    reason_code: str | None = None,
    decision_record_id: str | None = None,
    gate_id: str | None = None,
    evidence_item_refs: list[str] | None = None,
    artifact_refs: list[str] | None = None,
    finding_refs: list[str] | None = None,
    research_task_id: str | None = None,
    run_id: str | None = None,
    provenance_record_refs: list[str] | None = None,
    operation_id: str | None = None,
    idempotency_key: str | None = None,
    metadata: dict[str, object] | None = None,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    if runtime_store is None:
        return _runtime_missing_payload("ideas.transition", diagnostics), diagnostics
    try:
        now = utc_timestamp()
        input_payload = {
            "topic_workspace_id": context.topic_workspace_id,
            "idea_id": idea_id,
            "facet": facet,
            "expected_from": expected_from,
            "next_value": next_value,
            "actor_ref": actor_ref,
            "rationale": rationale,
            "reason_code": reason_code,
            "decision_record_id": decision_record_id,
            "gate_id": gate_id,
            "evidence_item_refs": sorted(evidence_item_refs or []),
            "artifact_refs": sorted(artifact_refs or []),
            "finding_refs": sorted(finding_refs or []),
            "research_task_id": research_task_id,
            "run_id": run_id,
            "provenance_record_refs": sorted(provenance_record_refs or []),
            "metadata": metadata or {},
        }
        input_digest = digest_json(input_payload)
        selected_operation_id = operation_id or f"idea-transition-{input_digest[:16]}"
        selected_idempotency_key = idempotency_key or selected_operation_id
        transition_id = f"idea-state-transition-{digest_json({'operation_id': selected_operation_id, 'idea_id': idea_id, 'facet': facet})[:16]}"
        transition = ResearchIdeaStateTransition(
            id=transition_id,
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            idea_id=idea_id,
            facet=cast(Any, facet),
            previous_value=expected_from,
            next_value=next_value,
            operation_id=selected_operation_id,
            actor_ref=actor_ref,
            reason_code=reason_code,
            rationale=rationale,
            decision_record_id=decision_record_id,
            gate_id=gate_id,
            evidence_item_refs=sorted(set(evidence_item_refs or [])),
            artifact_refs=sorted(set(artifact_refs or [])),
            finding_refs=sorted(set(finding_refs or [])),
            research_task_id=research_task_id,
            run_id=run_id,
            provenance_record_refs=sorted(set(provenance_record_refs or [])),
            metadata=metadata or {},
            transitioned_at=now,
            provenance_refs=[_provenance_ref("research-idea-state-transition", transition_id)],
        )
        operation = ResearchIdeaOperation(
            id=f"idea-operation-{_slug(context.topic_workspace_id)}-{_slug(selected_operation_id)}",
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            operation_id=selected_operation_id,
            idempotency_key=selected_idempotency_key,
            action_kind="ideas.transition",
            input_digest=input_digest,
            status="committed",
            result={"transition_ids": [transition_id], "idea_ids": [idea_id]},
            actor_ref=actor_ref,
            metadata={"facet": facet, **(metadata or {})},
            created_at=now,
            updated_at=now,
            provenance_refs=[_provenance_ref("research-idea-operation", selected_operation_id)],
        )
        try:
            result = runtime_store.apply_research_idea_mutation(transitions=[transition], operation=operation)
        except ValueError as exc:
            validation = runtime_store.validate_research_idea_state_transition(transition)
            raise ResearchRecordError(
                str(exc),
                code="idea_transition_validation_failed",
                payload={"diagnostics": validation},
            ) from exc
        result_payload = dict(result)
        operation_record = result_payload.pop("operation", None)
        return {
            "ok": True,
            "mutated": not bool(result.get("replayed")),
            "operation": "ideas.transition",
            "operation_record": operation_record,
            **result_payload,
        }, diagnostics
    finally:
        runtime_store.close()


def upsert_research_idea_decision_option(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    decision_record_id: str,
    idea_id: str,
    outcome: str,
    actor_ref: str,
    option_role: str | None = None,
    ordinal: int | None = None,
    generation_id: str | None = None,
    rationale: str | None = None,
    consequence: str | None = None,
    supporting_refs: list[str] | None = None,
    operation_id: str | None = None,
    idempotency_key: str | None = None,
    metadata: dict[str, object] | None = None,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    if runtime_store is None:
        return _runtime_missing_payload("ideas.decision-options.upsert", diagnostics), diagnostics
    try:
        now = utc_timestamp()
        input_payload = {
            "topic_workspace_id": context.topic_workspace_id,
            "decision_record_id": decision_record_id,
            "idea_id": idea_id,
            "outcome": outcome,
            "actor_ref": actor_ref,
            "option_role": option_role,
            "ordinal": ordinal,
            "generation_id": generation_id,
            "rationale": rationale,
            "consequence": consequence,
            "supporting_refs": sorted(supporting_refs or []),
            "metadata": metadata or {},
        }
        input_digest = digest_json(input_payload)
        selected_operation_id = operation_id or f"idea-decision-option-{input_digest[:16]}"
        selected_idempotency_key = idempotency_key or selected_operation_id
        option_id = f"idea-decision-option-{digest_json({'topic_workspace_id': context.topic_workspace_id, 'decision_record_id': decision_record_id, 'idea_id': idea_id})[:16]}"
        existing = runtime_store.get_research_idea_decision_option(option_id)
        option = ResearchIdeaDecisionOption(
            id=option_id,
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            decision_record_id=decision_record_id,
            idea_id=idea_id,
            outcome=cast(Any, outcome),
            operation_id=selected_operation_id,
            option_role=option_role,
            ordinal=ordinal,
            generation_id=generation_id,
            rationale=rationale,
            consequence=consequence,
            actor_ref=actor_ref,
            supporting_refs=sorted(set(supporting_refs or [])),
            metadata=metadata or {},
            created_at=existing.created_at if existing is not None else now,
            updated_at=now,
            provenance_refs=[_provenance_ref("research-idea-decision-option", option_id)],
        )
        operation = ResearchIdeaOperation(
            id=f"idea-operation-{_slug(context.topic_workspace_id)}-{_slug(selected_operation_id)}",
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            operation_id=selected_operation_id,
            idempotency_key=selected_idempotency_key,
            action_kind="ideas.decision-options.upsert",
            input_digest=input_digest,
            status="committed",
            result={"decision_option_ids": [option_id], "idea_ids": [idea_id], "decision_record_ids": [decision_record_id]},
            actor_ref=actor_ref,
            metadata=metadata or {},
            created_at=now,
            updated_at=now,
            provenance_refs=[_provenance_ref("research-idea-operation", selected_operation_id)],
        )
        try:
            result = runtime_store.apply_research_idea_mutation(transitions=[], decision_options=[option], operation=operation)
        except ValueError as exc:
            validation = runtime_store.validate_research_idea_decision_option(option)
            raise ResearchRecordError(
                str(exc),
                code="idea_decision_option_validation_failed",
                payload={"diagnostics": validation},
            ) from exc
        result_payload = dict(result)
        operation_record = result_payload.pop("operation", None)
        return {
            "ok": True,
            "mutated": not bool(result.get("replayed")),
            "operation": "ideas.decision-options.upsert",
            "operation_record": operation_record,
            **result_payload,
        }, diagnostics
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
    _validate_semantic_id(semantic_id)
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
    exploration_states: list[str] | None = None,
    decision_states: list[str] | None = None,
    evidence_states: list[str] | None = None,
    archive_states: list[str] | None = None,
    visibilities: list[str] | None = None,
    generation_id: str | None = None,
    decision_record_id: str | None = None,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if runtime_store is None:
        return _runtime_missing_payload("ideas.query", diagnostics), diagnostics
    try:
        selected_visibilities = set(visibilities or ([] if visibility is None else [visibility]))
        include_archive_rows = include_archived or bool(archive_states and "archived" in archive_states)
        ideas = runtime_store.list_research_ideas(topic_workspace_id=context.topic_workspace_id, include_archived=include_archive_rows)
        edges = runtime_store.list_research_idea_lineage_edges(topic_workspace_id=context.topic_workspace_id, include_archived=include_archived)
        options = runtime_store.list_research_idea_decision_options(topic_workspace_id=context.topic_workspace_id)
        eligible_generation_ids: set[str] | None = None
        if generation_id is not None:
            eligible_generation_ids = {
                edge.child_idea_id
                for edge in edges
                if edge.generation_id == generation_id
            }
            eligible_generation_ids.update(option.idea_id for option in options if option.generation_id == generation_id)
        eligible_decision_ids: set[str] | None = None
        if decision_record_id is not None:
            eligible_decision_ids = {option.idea_id for option in options if option.decision_record_id == decision_record_id}
        ideas = [
            idea
            for idea in ideas
            if (not exploration_states or idea.exploration_state in exploration_states)
            and (not decision_states or idea.decision_state in decision_states)
            and (not evidence_states or idea.evidence_state in evidence_states)
            and (not archive_states or idea.archive_state in archive_states)
            and (not selected_visibilities or idea.visibility in selected_visibilities)
            and (eligible_generation_ids is None or idea.idea_id in eligible_generation_ids)
            and (eligible_decision_ids is None or idea.idea_id in eligible_decision_ids)
        ]
        allowed_ids = {idea.idea_id for idea in ideas}
        return {
            "ok": True,
            "mutated": False,
            "operation": "ideas.query",
            "ideas": [idea.to_json() for idea in ideas],
            "realizations": [item.to_json() for item in runtime_store.list_research_idea_realizations(topic_workspace_id=context.topic_workspace_id) if item.idea_id in allowed_ids],
            "edges": [edge.to_json() for edge in edges if edge.parent_idea_id in allowed_ids and edge.child_idea_id in allowed_ids],
            "generation_groups": [group.to_json() for group in runtime_store.list_research_idea_generation_groups(topic_workspace_id=context.topic_workspace_id)],
            "state_transitions": [item.to_json() for item in runtime_store.list_research_idea_state_transitions(topic_workspace_id=context.topic_workspace_id) if item.idea_id in allowed_ids],
            "decision_options": [item.to_json() for item in options if item.idea_id in allowed_ids],
            "applied_filters": {
                "exploration_states": sorted(exploration_states or []),
                "decision_states": sorted(decision_states or []),
                "evidence_states": sorted(evidence_states or []),
                "archive_states": sorted(archive_states or []),
                "visibilities": sorted(selected_visibilities),
                "generation_id": generation_id,
                "decision_record_id": decision_record_id,
            },
            "diagnostics": [],
        }, diagnostics
    finally:
        runtime_store.close()


def query_research_idea_decision_context(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    idea_id: str | None = None,
    decision_record_id: str | None = None,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if runtime_store is None:
        return _runtime_missing_payload("ideas.decision-context", diagnostics), diagnostics
    try:
        options = runtime_store.list_research_idea_decision_options(topic_workspace_id=context.topic_workspace_id)
        all_transitions = runtime_store.list_research_idea_state_transitions(topic_workspace_id=context.topic_workspace_id)
        selected_decision_ids: set[str]
        if decision_record_id is not None:
            selected_decision_ids = {decision_record_id}
        elif idea_id is not None:
            selected_decision_ids = {
                *(option.decision_record_id for option in options if option.idea_id == idea_id),
                *(transition.decision_record_id for transition in all_transitions if transition.idea_id == idea_id and transition.decision_record_id is not None),
            }
        else:
            selected_decision_ids = {option.decision_record_id for option in options}
        selected_options = [option for option in options if option.decision_record_id in selected_decision_ids]
        selected_idea_ids = {option.idea_id for option in selected_options}
        if idea_id is not None:
            selected_idea_ids.add(idea_id)
        idea_records = [
            idea
            for idea in runtime_store.list_research_ideas(topic_workspace_id=context.topic_workspace_id, include_archived=True)
            if idea.idea_id in selected_idea_ids
        ]
        idea_by_id = {idea.idea_id: idea for idea in idea_records}
        ideas = [idea.to_json() for idea in idea_records]
        transitions = [
            transition.to_json()
            for transition in all_transitions
            if transition.decision_record_id in selected_decision_ids
            or (idea_id is not None and transition.idea_id == idea_id and transition.facet == "decision_state")
        ]
        reopen_history = [
            transition.to_json()
            for transition in all_transitions
            if transition.idea_id in selected_idea_ids
            and transition.facet == "decision_state"
            and transition.previous_value in {"deferred", "closed"}
            and transition.next_value in {"open", "shortlisted", "selected"}
        ]
        context_diagnostics: list[dict[str, object]] = []
        decisions: list[dict[str, object]] = []
        for selected_id in sorted(selected_decision_ids):
            decision = runtime_store.get_lifecycle_record(selected_id)
            if decision is None:
                context_diagnostics.append({"severity": "error", "code": "idea_decision_record_missing", "message": f"Research Idea decision context references a missing Decision Record: {selected_id}", "decision_record_id": selected_id})
                continue
            decision_options = [option for option in selected_options if option.decision_record_id == selected_id]
            decision_transitions = [transition for transition in all_transitions if transition.decision_record_id == selected_id]
            option_set_complete = bool(decision_options) and all(option.metadata.get("option_set_complete") is True for option in decision_options)
            rationale = _optional_metadata_string(decision.transition_metadata.get("rationale"))
            if rationale is None:
                rationale = next((option.rationale for option in decision_options if option.rationale), None)
            if rationale is None:
                rationale = next((transition.rationale for transition in decision_transitions if transition.rationale), None)
            missing_fields: list[str] = []
            if not decision_options:
                missing_fields.append("options")
            elif not option_set_complete:
                missing_fields.append("complete_option_set")
            if rationale is None:
                missing_fields.append("rationale")
            if missing_fields:
                context_diagnostics.append(
                    {
                        "severity": "warning",
                        "code": "idea_decision_context_incomplete",
                        "message": f"Decision Record has incomplete Research Idea context: {selected_id}",
                        "decision_record_id": selected_id,
                        "missing_fields": missing_fields,
                    }
                )
            enriched_options: list[dict[str, object]] = []
            for option in decision_options:
                idea = idea_by_id.get(option.idea_id)
                option_transition = next(
                    (
                        transition
                        for transition in reversed(decision_transitions)
                        if transition.idea_id == option.idea_id and transition.facet == "decision_state"
                    ),
                    None,
                )
                enriched_options.append(
                    {
                        **option.to_json(),
                        "idea": idea.to_json() if idea is not None else None,
                        "reason_code": option_transition.reason_code if option_transition is not None else None,
                        "transition_ref": option_transition.id if option_transition is not None else None,
                        "transition_rationale": option_transition.rationale if option_transition is not None else None,
                    }
                )
            decisions.append(
                {
                    **decision.to_json(),
                    "decision_record_id": selected_id,
                    "options": enriched_options,
                    "selected_idea_ids": [option.idea_id for option in decision_options if option.outcome == "selected"],
                    "option_set_complete": option_set_complete,
                    "rationale": rationale,
                    "consequences": [option.consequence for option in decision_options if option.consequence],
                    "actor_refs": sorted({str(value) for value in [*(option.actor_ref for option in decision_options), *(transition.actor_ref for transition in decision_transitions)] if value}),
                    "decided_at": max([decision.updated_at, *(option.updated_at for option in decision_options), *(transition.transitioned_at for transition in decision_transitions)]),
                    "supporting_refs": sorted({ref for option in decision_options for ref in option.supporting_refs}),
                    "transition_refs": [transition.id for transition in decision_transitions],
                    "missing_fields": missing_fields,
                }
            )
        return {
            "ok": not any(item.get("severity") == "error" for item in context_diagnostics),
            "mutated": False,
            "operation": "ideas.decision-context",
            "idea_id": idea_id,
            "decision_record_id": decision_record_id,
            "decisions": decisions,
            "ideas": ideas,
            "transitions": transitions,
            "reopen_history": reopen_history,
            "diagnostics": context_diagnostics,
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


def traverse_research_ideas(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    root_idea_ids: list[str],
    direction: str,
    relation_kinds: list[str] | None = None,
    max_depth: int = 8,
    max_nodes: int = 500,
    max_edges: int = 1000,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if runtime_store is None:
        return _runtime_missing_payload("ideas.traverse", diagnostics), diagnostics
    try:
        traversal_diagnostics: list[dict[str, object]] = []
        if direction not in {"ancestors", "descendants"}:
            return {
                "ok": False,
                "mutated": False,
                "operation": "ideas.traverse",
                "error": {"code": "idea_traversal_direction_unsupported", "message": f"Unsupported traversal direction: {direction}"},
                "diagnostics": [],
            }, diagnostics
        invalid_kinds = sorted(set(relation_kinds or []) - set(RESEARCH_IDEA_LINEAGE_KINDS))
        if invalid_kinds:
            return {
                "ok": False,
                "mutated": False,
                "operation": "ideas.traverse",
                "error": {"code": "idea_traversal_relation_unsupported", "message": f"Unsupported Research Idea lineage kind(s): {', '.join(invalid_kinds)}"},
                "diagnostics": [],
            }, diagnostics
        if max_depth < 0 or max_nodes < 1 or max_edges < 0:
            return {
                "ok": False,
                "mutated": False,
                "operation": "ideas.traverse",
                "error": {"code": "idea_traversal_bound_invalid", "message": "Traversal bounds require max-depth >= 0, max-nodes >= 1, and max-edges >= 0."},
                "diagnostics": [],
            }, diagnostics
        ideas = runtime_store.list_research_ideas(topic_workspace_id=context.topic_workspace_id, include_archived=True)
        idea_by_id = {idea.idea_id: idea for idea in ideas}
        roots = list(dict.fromkeys(root_idea_ids))
        valid_roots = [root for root in roots if root in idea_by_id]
        unresolved_roots = [root for root in roots if root not in idea_by_id]
        for root in unresolved_roots:
            traversal_diagnostics.append({"severity": "warning", "code": "idea_traversal_root_unresolved", "message": f"Research Idea traversal root is unresolved: {root}", "idea_id": root})
        eligible_kinds = set(relation_kinds or RESEARCH_IDEA_LINEAGE_KINDS)
        all_edges = [
            edge
            for edge in runtime_store.list_research_idea_lineage_edges(topic_workspace_id=context.topic_workspace_id)
            if edge.lineage_kind in eligible_kinds
        ]
        adjacency: dict[str, list[str]] = {}
        for edge in all_edges:
            source, target = (
                (edge.parent_idea_id, edge.child_idea_id)
                if direction == "descendants"
                else (edge.child_idea_id, edge.parent_idea_id)
            )
            adjacency.setdefault(source, []).append(target)
        for neighbors in adjacency.values():
            neighbors.sort()

        selected_ids: set[str] = set(valid_roots[:max_nodes])
        depths: dict[str, int] = {root: 0 for root in valid_roots[:max_nodes]}
        queue = list(valid_roots[:max_nodes])
        cursor = 0
        limiting_bounds: set[str] = set()
        if len(valid_roots) > max_nodes:
            limiting_bounds.add("max_nodes")
        while cursor < len(queue):
            current = queue[cursor]
            cursor += 1
            current_depth = depths[current]
            neighbors = adjacency.get(current, [])
            if current_depth >= max_depth:
                if any(neighbor not in selected_ids for neighbor in neighbors):
                    limiting_bounds.add("max_depth")
                continue
            for neighbor in neighbors:
                if neighbor in selected_ids:
                    continue
                if len(selected_ids) >= max_nodes:
                    limiting_bounds.add("max_nodes")
                    continue
                selected_ids.add(neighbor)
                depths[neighbor] = current_depth + 1
                queue.append(neighbor)

        induced_edges = [edge for edge in all_edges if edge.parent_idea_id in selected_ids and edge.child_idea_id in selected_ids]
        induced_edges.sort(key=lambda edge: (edge.parent_idea_id, edge.child_idea_id, edge.lineage_kind, edge.id))
        if len(induced_edges) > max_edges:
            limiting_bounds.add("max_edges")
            induced_edges = induced_edges[:max_edges]
        complete = not limiting_bounds
        returned_ideas = [idea_by_id[idea_id] for idea_id in sorted(selected_ids)]
        return {
            "ok": True,
            "mutated": False,
            "operation": "ideas.traverse",
            "roots": roots,
            "resolved_roots": valid_roots,
            "unresolved_roots": unresolved_roots,
            "direction": direction,
            "relation_kinds": sorted(eligible_kinds),
            "nodes": [idea.to_json() for idea in returned_ideas],
            "edges": [edge.to_json() for edge in induced_edges],
            "topology_complete": complete,
            "limiting_bounds": sorted(limiting_bounds),
            "maximum_observed_depth": max(depths.values(), default=0),
            "counts": {
                "nodes": len(returned_ideas),
                "edges": len(induced_edges),
                "source_nodes": len(ideas),
                "source_edges": len(all_edges),
            },
            "bounds": {"max_depth": max_depth, "max_nodes": max_nodes, "max_edges": max_edges},
            "continuation": None if complete else {"action": "increase_bounds_or_refine_relation_kinds", "limiting_bounds": sorted(limiting_bounds)},
            "diagnostics": traversal_diagnostics,
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
        ideas = runtime_store.list_research_ideas(topic_workspace_id=context.topic_workspace_id, include_archived=True)
        transitions = runtime_store.list_research_idea_state_transitions(topic_workspace_id=context.topic_workspace_id)
        options = runtime_store.list_research_idea_decision_options(topic_workspace_id=context.topic_workspace_id)
        option_keys = {(option.decision_record_id, option.idea_id) for option in options}
        transitions_by_facet: dict[tuple[str, str], list[ResearchIdeaStateTransition]] = {}
        for transition in transitions:
            transitions_by_facet.setdefault((transition.idea_id, transition.facet), []).append(transition)
            if transition.decision_record_id is not None and transition.facet == "decision_state" and (transition.decision_record_id, transition.idea_id) not in option_keys:
                idea_diagnostics.append({"severity": "error", "code": "idea_decision_option_missing", "message": f"Decision-linked Research Idea transition has no option membership: {transition.idea_id} in {transition.decision_record_id}", "idea_id": transition.idea_id, "decision_record_id": transition.decision_record_id, "transition_id": transition.id})
        idea_by_id = {idea.idea_id: idea for idea in ideas}
        for (idea_id, facet), history in transitions_by_facet.items():
            history.sort(key=lambda item: (item.transitioned_at, item.id))
            for previous, current in zip(history, history[1:]):
                if previous.next_value != current.previous_value:
                    idea_diagnostics.append({"severity": "error", "code": "idea_transition_history_gap", "message": f"Research Idea transition history is discontinuous for {idea_id} {facet}.", "idea_id": idea_id, "facet": facet, "previous_transition_id": previous.id, "transition_id": current.id})
            idea = idea_by_id.get(idea_id)
            if idea is not None and str(getattr(idea, facet)) != history[-1].next_value:
                idea_diagnostics.append({"severity": "error", "code": "idea_transition_current_state_stale", "message": f"Research Idea current {facet} does not match its latest transition.", "idea_id": idea_id, "facet": facet, "latest_transition_id": history[-1].id, "current_value": str(getattr(idea, facet)), "transition_value": history[-1].next_value})
        realizations_by_idea: dict[str, list[ResearchIdeaRealization]] = {}
        for realization in runtime_store.list_research_idea_realizations(topic_workspace_id=context.topic_workspace_id):
            realizations_by_idea.setdefault(realization.idea_id, []).append(realization)
        for idea_id, realizations in realizations_by_idea.items():
            latest_count = sum(1 for realization in realizations if realization.latest)
            if latest_count != 1:
                idea_diagnostics.append({"severity": "error" if latest_count > 1 else "warning", "code": "idea_realization_latest_inconsistent", "message": f"Research Idea {idea_id} has {latest_count} latest realizations.", "idea_id": idea_id, "latest_count": latest_count})
        for idea in ideas:
            unknown_facets = [field_name for field_name in ("exploration_state", "decision_state", "evidence_state") if getattr(idea, field_name) == "unknown"]
            if unknown_facets:
                idea_diagnostics.append({"severity": "warning", "code": "idea_needs_classification", "message": f"Research Idea needs classification for: {', '.join(unknown_facets)}.", "idea_id": idea.idea_id, "facets": unknown_facets})
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


def migrate_legacy_kaoju_direction_set(
    context: EffectiveTopicContext,
    record_id: str,
    *,
    env: Mapping[str, str],
    apply: bool = False,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """Preview or apply a conservative canonical projection for one legacy Kaoju Direction Set."""

    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=not apply)
    if runtime_store is None:
        return _runtime_missing_payload("ideas.migrate-kaoju-direction-set", diagnostics), diagnostics
    try:
        structured = runtime_store.get_structured_payload(record_id)
        if structured is None:
            return {"ok": False, "mutated": False, "operation": "ideas.migrate-kaoju-direction-set", "error": {"code": "legacy_direction_set_payload_missing", "message": f"Direction Set has no structured payload: {record_id}"}, "diagnostics": []}, diagnostics
        profile_ref = structured.format_profile_ref or ""
        if "direction-set/v1" not in profile_ref:
            return {"ok": False, "mutated": False, "operation": "ideas.migrate-kaoju-direction-set", "error": {"code": "legacy_direction_set_profile_required", "message": f"Direction Set migration requires the legacy v1 profile, observed: {profile_ref or 'none'}"}, "diagnostics": []}, diagnostics
        lifecycle = runtime_store.get_lifecycle_record(record_id)
        if lifecycle is None or lifecycle.record_kind != "decision_record":
            return {"ok": False, "mutated": False, "operation": "ideas.migrate-kaoju-direction-set", "error": {"code": "legacy_direction_set_record_invalid", "message": f"Legacy Direction Set must resolve to a Decision Record: {record_id}"}, "diagnostics": []}, diagnostics
        payload, payload_diagnostics = load_structured_payload(context, structured)
        if not isinstance(payload, Mapping):
            return {"ok": False, "mutated": False, "operation": "ideas.migrate-kaoju-direction-set", "error": {"code": "legacy_direction_set_payload_invalid", "message": f"Legacy Direction Set payload is not an object: {record_id}"}, "diagnostics": payload_diagnostics}, diagnostics
        plan, plan_diagnostics, plan_metadata = _legacy_kaoju_direction_migration_plan(context, runtime_store, record_id, payload)
        operation_id = f"legacy-kaoju-direction-set-migration-v1-{digest_json({'topic_workspace_id': context.topic_workspace_id, 'record_id': record_id})[:16]}"
        provenance_record_id = f"provenance:{operation_id}"
        error_diagnostics = [item for item in plan_diagnostics if item.get("severity") == "error"]
        preview = {
            "ok": not error_diagnostics,
            "mutated": False,
            "operation": "ideas.migrate-kaoju-direction-set",
            "apply": False,
            "record_id": record_id,
            "operation_id": operation_id,
            "plan": plan,
            "plan_metadata": plan_metadata,
            "affected_count": len(plan),
            "diagnostics": [*payload_diagnostics, *plan_diagnostics],
        }
        if not apply:
            return preview, diagnostics
        existing_operation = runtime_store.get_research_idea_operation(operation_id, topic_workspace_id=context.topic_workspace_id)
        if existing_operation is not None:
            return {
                **preview,
                "ok": True,
                "apply": True,
                "replayed": True,
                "diagnostics": [*payload_diagnostics, *(item for item in plan_diagnostics if item.get("code") != "legacy_direction_idea_collision")],
                "operation_record": existing_operation.to_json(),
                "applied": [],
            }, diagnostics
        if error_diagnostics:
            return {**preview, "apply": True, "error": {"code": "legacy_direction_set_migration_plan_invalid", "message": "Legacy Direction Set migration plan contains blocking diagnostics."}}, diagnostics

        now = utc_timestamp()
        actor_ref = str(plan_metadata["actor_ref"])
        generation_id = str(plan_metadata["generation_id"])
        selected_ids = set(cast(list[str], plan_metadata["selected_idea_ids"]))
        provenance = RuntimeLifecycleRecord(
            id=provenance_record_id,
            record_kind="provenance_record",
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            status="complete",
            created_at=now,
            updated_at=now,
            lifecycle_refs={"operation_id": operation_id, "source_record_id": record_id},
            transition_metadata={"migration": "legacy-kaoju-direction-set-v1", "source_profile_ref": profile_ref},
            provenance_refs=[_provenance_ref("legacy-kaoju-direction-set-migration", operation_id)],
        )
        generation = ResearchIdeaGenerationGroup(
            id=generation_id,
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            purpose="Canonical Research Ideas recovered from one actor-confirmed legacy Kaoju Direction Set proposal slate.",
            parent_set_digest=_idea_parent_set_digest([]),
            producer_skill=lifecycle.lifecycle_refs.get("producer_skill") or "isomer-kaoju-frame",
            decision_record_id=record_id if bool(plan_metadata["confirmation_accepted"]) else None,
            metadata={"parent_idea_ids": [], "member_idea_ids": [str(item["idea_id"]) for item in plan], "source_record_id": record_id, "migration_operation_id": operation_id},
            created_at=now,
            updated_at=now,
            provenance_refs=[_provenance_ref("research-idea-generation-group", generation_id), provenance_record_id],
        )
        ideas: list[ResearchIdea] = []
        realizations: list[ResearchIdeaRealization] = []
        transitions: list[ResearchIdeaStateTransition] = []
        options: list[ResearchIdeaDecisionOption] = []
        first_display_key = runtime_store.next_research_idea_display_key(context.topic_workspace_id)
        first_display_match = re.fullmatch(r"I-(?P<number>[1-9][0-9]*)", first_display_key)
        first_display_number = int(first_display_match.group("number")) if first_display_match else 1
        for index, item in enumerate(plan):
            idea_id = str(item["idea_id"])
            decision_state = "selected" if idea_id in selected_ids else "unknown"
            idea = _idea_record(
                context,
                idea_id=idea_id,
                display_key=f"I-{first_display_number + index}",
                title=str(item["title"]),
                summary=str(item["summary"]),
                family="kaoju-survey-direction",
                status="selected" if decision_state == "selected" else "candidate",
                exploration_state="unknown",
                decision_state=decision_state,
                evidence_state="unknown",
                archive_state="active",
                visibility="primary",
                aliases=[str(item["direction_id"])],
                source_record_id=record_id,
                source_json_path=str(item["source_json_path"]),
                metadata={"migration_operation_id": operation_id, "source_profile_ref": profile_ref, "legacy_direction_id": item["direction_id"], "ambiguous_fields": item["ambiguous_fields"]},
                created_at=now,
                updated_at=now,
            )
            ideas.append(idea)
            realizations.append(
                _idea_realization_record(
                    context,
                    idea_id=idea_id,
                    record_id=record_id,
                    source_json_path=str(item["source_json_path"]),
                    realization_stage="survey-framing",
                    semantic_id="KAOJU:DIRECTION-SET",
                    latest=True,
                    metadata={"migration_operation_id": operation_id, "legacy_direction_id": item["direction_id"]},
                    created_at=now,
                    updated_at=now,
                )
            )
            if bool(plan_metadata["confirmation_accepted"]):
                option_id = f"idea-decision-option-{digest_json({'topic_workspace_id': context.topic_workspace_id, 'decision_record_id': record_id, 'idea_id': idea_id})[:16]}"
                options.append(
                    ResearchIdeaDecisionOption(
                        id=option_id,
                        research_topic_id=context.research_topic.id,
                        topic_workspace_id=context.topic_workspace_id,
                        decision_record_id=record_id,
                        idea_id=idea_id,
                        outcome=cast(ResearchIdeaDecisionOptionOutcome, "selected" if idea_id in selected_ids else "not_selected"),
                        operation_id=operation_id,
                        option_role="legacy_direction_proposal",
                        ordinal=index,
                        generation_id=generation_id,
                        rationale=cast(str | None, item.get("rationale")),
                        actor_ref=actor_ref,
                        supporting_refs=[record_id],
                        metadata={"option_set_complete": True, "migration_operation_id": operation_id, "legacy_direction_id": item["direction_id"]},
                        created_at=now,
                        updated_at=now,
                        provenance_refs=[_provenance_ref("research-idea-decision-option", option_id), provenance_record_id],
                    )
                )
            if idea_id in selected_ids:
                transition_id = f"idea-state-transition-{digest_json({'operation_id': operation_id, 'idea_id': idea_id, 'facet': 'decision_state'})[:16]}"
                transitions.append(
                    ResearchIdeaStateTransition(
                        id=transition_id,
                        research_topic_id=context.research_topic.id,
                        topic_workspace_id=context.topic_workspace_id,
                        idea_id=idea_id,
                        facet="decision_state",
                        previous_value="unknown",
                        next_value="selected",
                        operation_id=operation_id,
                        actor_ref=actor_ref,
                        rationale=cast(str | None, item.get("rationale")) or "Actor-confirmed selection in the legacy Kaoju Direction Set.",
                        decision_record_id=record_id,
                        artifact_refs=[],
                        provenance_record_refs=[provenance_record_id],
                        metadata={"migration_version": 1, "source_record_id": record_id},
                        transitioned_at=now,
                        provenance_refs=[_provenance_ref("research-idea-state-transition", transition_id), provenance_record_id],
                    )
                )
        operation = ResearchIdeaOperation(
            id=f"idea-operation-{_slug(context.topic_workspace_id)}-{_slug(operation_id)}",
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            operation_id=operation_id,
            idempotency_key=operation_id,
            action_kind="ideas.migrate-kaoju-direction-set",
            input_digest=digest_json({"record_id": record_id, "plan": plan, "plan_metadata": plan_metadata}),
            status="committed",
            result={"idea_ids": [idea.idea_id for idea in ideas], "realization_ids": [item.id for item in realizations], "transition_ids": [item.id for item in transitions], "decision_option_ids": [item.id for item in options], "generation_ids": [generation_id]},
            actor_ref=actor_ref,
            metadata={"migration_version": 1, "source_record_id": record_id, "source_profile_ref": profile_ref},
            created_at=now,
            updated_at=now,
            provenance_refs=[_provenance_ref("research-idea-operation", operation_id), provenance_record_id],
        )
        try:
            with runtime_store.connection:
                runtime_store.upsert_lifecycle_record(provenance)
                for idea in ideas:
                    idea_validation = runtime_store.validate_research_idea(idea)
                    if _has_lineage_errors(idea_validation):
                        raise ValueError(f"Migrated Research Idea failed validation: {idea.idea_id}")
                    runtime_store.upsert_research_idea(idea, validate=False)
                runtime_store.upsert_research_idea_generation_group(generation)
                for realization in realizations:
                    realization_validation = runtime_store.validate_research_idea_realization(realization)
                    realization_validation.extend(_validate_realization_source(context, runtime_store, realization, report_missing_payload=True))
                    if _has_lineage_errors(realization_validation):
                        raise ValueError(f"Migrated Research Idea realization failed validation: {realization.id}")
                    runtime_store.upsert_research_idea_realization(realization, validate=False)
                for option in options:
                    option_validation = runtime_store.validate_research_idea_decision_option(option)
                    if _has_lineage_errors(option_validation):
                        raise ValueError(f"Migrated Research Idea decision option failed validation: {option.id}")
                    runtime_store.upsert_research_idea_decision_option(option, validate=False)
                for transition in transitions:
                    transition_validation = runtime_store.validate_research_idea_state_transition(transition, check_current=False)
                    if _has_lineage_errors(transition_validation):
                        raise ValueError(f"Migrated Research Idea transition failed validation: {transition.id}")
                    runtime_store.upsert_research_idea_state_transition(transition, validate=False)
                runtime_store.upsert_research_idea_operation(operation)
        except (ValueError, sqlite3.Error) as exc:
            raise ResearchRecordError(f"Legacy Kaoju Direction Set migration rolled back: {exc}", code="legacy_direction_set_migration_failed", payload={"plan": plan, "diagnostics": plan_diagnostics}) from exc
        refresh_query_index_for_record(context, runtime_store, record_id)
        return {
            **preview,
            "ok": True,
            "mutated": True,
            "apply": True,
            "provenance_record_id": provenance_record_id,
            "operation_record": operation.to_json(),
            "applied": [idea.to_json() for idea in ideas],
            "realizations": [item.to_json() for item in realizations],
            "decision_options": [item.to_json() for item in options],
            "transitions": [item.to_json() for item in transitions],
            "generation_group": generation.to_json(),
        }, diagnostics
    finally:
        runtime_store.close()


def migrate_research_idea_portfolio(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    apply: bool = False,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=not apply)
    if runtime_store is None:
        return _runtime_missing_payload("ideas.migrate-status", diagnostics), diagnostics
    try:
        schema_columns = {
            str(row["name"])
            for row in runtime_store.connection.execute("PRAGMA table_info(research_ideas)")
        }
        has_portfolio_columns = {"exploration_state", "decision_state", "evidence_state", "archive_state"}.issubset(schema_columns)
        operation_id = f"research-idea-portfolio-migration-v1-{_slug(context.topic_workspace_id)}"
        provenance_record_id = f"provenance:{operation_id}"
        plan: list[dict[str, object]] = []
        for idea in runtime_store.list_research_ideas(topic_workspace_id=context.topic_workspace_id, include_archived=True):
            if idea.metadata.get("portfolio_state_version") == 1:
                continue
            legacy_status = idea.status
            mapped_exploration, mapped_decision, mapped_evidence, mapped_archive = research_idea_facets_from_legacy_status(legacy_status)
            current_exploration = idea.exploration_state if has_portfolio_columns else "unknown"
            current_decision = idea.decision_state if has_portfolio_columns else "unknown"
            current_evidence = idea.evidence_state if has_portfolio_columns else "unknown"
            current_archive = idea.archive_state if has_portfolio_columns else "active"
            target_exploration = current_exploration if current_exploration != "unknown" else mapped_exploration
            target_decision = current_decision if current_decision != "unknown" else mapped_decision
            target_evidence = current_evidence if current_evidence != "unknown" else mapped_evidence
            target_archive = "archived" if mapped_archive == "archived" else current_archive
            closure_reason = None
            if legacy_status == "rejected":
                closure_reason = "legacy_rejection"
            elif legacy_status == "superseded":
                closure_reason = "legacy_supersession"
            compatibility_status = project_research_idea_compatibility_status(
                exploration_state=target_exploration,
                decision_state=target_decision,
                evidence_state=target_evidence,
                archive_state=target_archive,
                closure_reason=closure_reason,
                preserved_status=legacy_status,
            )
            item_diagnostics: list[dict[str, object]] = []
            for field_name, value in (
                ("exploration_state", target_exploration),
                ("decision_state", target_decision),
                ("evidence_state", target_evidence),
            ):
                if value == "unknown":
                    item_diagnostics.append({"severity": "warning", "code": "idea_legacy_classification_unknown", "message": f"Legacy status {legacy_status} does not justify {field_name}.", "idea_id": idea.idea_id, "facet": field_name})
            transitions: list[dict[str, object]] = []
            for facet, previous, next_value in (
                ("exploration_state", current_exploration, target_exploration),
                ("decision_state", current_decision, target_decision),
                ("evidence_state", current_evidence, target_evidence),
                ("archive_state", current_archive, target_archive),
            ):
                if previous == next_value:
                    continue
                transition_id = f"idea-state-transition-{digest_json({'operation_id': operation_id, 'idea_id': idea.idea_id, 'facet': facet})[:16]}"
                transitions.append(
                    {
                        "id": transition_id,
                        "facet": facet,
                        "previous_value": previous,
                        "next_value": next_value,
                        "reason_code": closure_reason if facet == "decision_state" and next_value == "closed" else "legacy_status_migration",
                    }
                )
            plan.append(
                {
                    "idea_id": idea.idea_id,
                    "original_status": legacy_status,
                    "facets": {
                        "exploration_state": target_exploration,
                        "decision_state": target_decision,
                        "evidence_state": target_evidence,
                        "archive_state": target_archive,
                        "visibility": idea.visibility,
                    },
                    "compatibility_status": compatibility_status,
                    "closure_reason": closure_reason,
                    "transitions": transitions,
                    "diagnostics": item_diagnostics,
                }
            )
        plan.sort(key=lambda item: str(item["idea_id"]))
        if not apply:
            return {
                "ok": True,
                "mutated": False,
                "operation": "ideas.migrate-status",
                "apply": False,
                "operation_id": operation_id,
                "plan": plan,
                "affected_count": len(plan),
                "diagnostics": [diagnostic for item in plan for diagnostic in cast(list[dict[str, object]], item["diagnostics"])],
            }, diagnostics

        existing_operation = runtime_store.get_research_idea_operation(operation_id, topic_workspace_id=context.topic_workspace_id)
        if existing_operation is not None and not plan:
            return {
                "ok": True,
                "mutated": False,
                "replayed": True,
                "operation": "ideas.migrate-status",
                "apply": True,
                "operation_id": operation_id,
                "operation_record": existing_operation.to_json(),
                "plan": [],
                "applied": [],
                "affected_count": 0,
                "diagnostics": [],
            }, diagnostics
        if existing_operation is not None:
            raise ResearchRecordError(
                "Research Idea portfolio migration has an existing operation but still finds unmigrated rows.",
                code="idea_portfolio_migration_inconsistent",
                payload={"operation": existing_operation.to_json(), "plan": plan},
            )

        now = utc_timestamp()
        provenance = RuntimeLifecycleRecord(
            id=provenance_record_id,
            record_kind="provenance_record",
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            status="complete",
            created_at=now,
            updated_at=now,
            lifecycle_refs={"operation_id": operation_id},
            transition_metadata={"migration": "research-idea-portfolio-v1", "affected_idea_ids": ",".join(str(item["idea_id"]) for item in plan)},
            provenance_refs=[_provenance_ref("research-idea-portfolio-migration", operation_id)],
        )
        operation = ResearchIdeaOperation(
            id=f"idea-operation-{_slug(context.topic_workspace_id)}-{_slug(operation_id)}",
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            operation_id=operation_id,
            idempotency_key=operation_id,
            action_kind="ideas.migrate-status",
            input_digest=digest_json(plan),
            status="committed",
            result={"affected_idea_ids": [str(item["idea_id"]) for item in plan]},
            actor_ref="actor:isomer-migration",
            metadata={"migration_version": 1},
            created_at=now,
            updated_at=now,
            provenance_refs=[_provenance_ref("research-idea-operation", operation_id)],
        )
        applied: list[dict[str, object]] = []
        try:
            with runtime_store.connection:
                runtime_store.upsert_lifecycle_record(provenance)
                for item in plan:
                    current_idea = runtime_store.get_research_idea(str(item["idea_id"]), topic_workspace_id=context.topic_workspace_id)
                    if current_idea is None:
                        raise ValueError(f"Research Idea disappeared during migration: {item['idea_id']}")
                    facets = cast(dict[str, object], item["facets"])
                    updated = replace(
                        current_idea,
                        status=str(item["compatibility_status"]),
                        exploration_state=cast(ResearchIdeaExplorationState, facets["exploration_state"]),
                        decision_state=cast(ResearchIdeaDecisionState, facets["decision_state"]),
                        evidence_state=cast(ResearchIdeaEvidenceState, facets["evidence_state"]),
                        archive_state=cast(ResearchIdeaArchiveState, facets["archive_state"]),
                        metadata={
                            **current_idea.metadata,
                            "portfolio_state_version": 1,
                            "portfolio_migration": {
                                "operation_id": operation_id,
                                "original_status": item["original_status"],
                                "classified_at": now,
                            },
                        },
                        updated_at=now,
                    )
                    idea_validation = runtime_store.validate_research_idea(updated)
                    if _has_lineage_errors(idea_validation):
                        raise ValueError(f"Migrated Research Idea failed validation: {current_idea.idea_id}")
                    runtime_store.upsert_research_idea(updated, validate=False)
                    for transition_payload in cast(list[dict[str, object]], item["transitions"]):
                        transition = ResearchIdeaStateTransition(
                            id=str(transition_payload["id"]),
                            research_topic_id=context.research_topic.id,
                            topic_workspace_id=context.topic_workspace_id,
                            idea_id=current_idea.idea_id,
                            facet=cast(Any, transition_payload["facet"]),
                            previous_value=str(transition_payload["previous_value"]),
                            next_value=str(transition_payload["next_value"]),
                            operation_id=operation_id,
                            actor_ref="actor:isomer-migration",
                            reason_code=str(transition_payload["reason_code"]),
                            rationale=f"Conservative classification from preserved legacy status {item['original_status']}.",
                            provenance_record_refs=[provenance_record_id],
                            metadata={"migration_version": 1, "original_status": item["original_status"]},
                            transitioned_at=now,
                            provenance_refs=[_provenance_ref("research-idea-state-transition", str(transition_payload["id"]))],
                        )
                        transition_validation = runtime_store.validate_research_idea_state_transition(transition, check_current=False)
                        if _has_lineage_errors(transition_validation):
                            raise ValueError(f"Migrated Research Idea transition failed validation: {transition.id}")
                        runtime_store.upsert_research_idea_state_transition(transition, validate=False)
                    applied.append(updated.to_json())
                runtime_store.upsert_research_idea_operation(operation)
        except (ValueError, sqlite3.Error) as exc:
            raise ResearchRecordError(
                f"Research Idea portfolio migration rolled back: {exc}",
                code="idea_portfolio_migration_failed",
                payload={"plan": plan, "diagnostics": [diagnostic for item in plan for diagnostic in cast(list[dict[str, object]], item["diagnostics"])]},
            ) from exc
        return {
            "ok": True,
            "mutated": bool(applied),
            "operation": "ideas.migrate-status",
            "apply": True,
            "operation_id": operation_id,
            "provenance_record_id": provenance_record_id,
            "plan": plan,
            "applied": applied,
            "affected_count": len(applied),
            "diagnostics": [diagnostic for item in plan for diagnostic in cast(list[dict[str, object]], item["diagnostics"])],
        }, diagnostics
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
                semantic_id=_optional_metadata_string(record.transition_metadata.get("semantic_id")),
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


def _validate_semantic_id(semantic_id: str | None, *, expected_extension: str | None = None) -> None:
    if semantic_id is None:
        return
    try:
        parse_artifact_identity(
            semantic_id,
            expected_extension=expected_extension,
            known_extensions=packaged_extension_ids(),
        )
    except ArtifactIdentityError as exc:
        payload: dict[str, Any] = {"artifact_identity": semantic_id}
        if exc.expected_namespace is not None:
            payload["expected_namespace"] = exc.expected_namespace
        raise ResearchRecordError(exc.args[0], code=exc.code, payload=payload) from exc


def _validate_write_artifact_identity(request: ResearchRecordRequest) -> None:
    metadata = request.metadata or {}
    if "placeholder" in metadata or "semantic_id" in metadata:
        raise ResearchRecordError(
            "Artifact identity must be supplied only through the semantic_id field.",
            code="invalid_artifact_identity_metadata",
            payload={"forbidden_fields": sorted(key for key in ("placeholder", "semantic_id") if key in metadata)},
        )
    extension_id = extension_id_for_skill(request.skill)
    if extension_id is not None and request.semantic_id is None:
        raise ResearchRecordError(
            f"Extension-owned writes require an exact uppercase {extension_id.upper()}:WHAT semantic id.",
            code="artifact_identity_missing",
            payload={"expected_namespace": extension_id.upper()},
        )
    _validate_semantic_id(request.semantic_id, expected_extension=extension_id)


def _write_body(
    context: EffectiveTopicContext,
    request: ResearchRecordRequest,
    *,
    env: Mapping[str, str],
    cwd: Path,
) -> tuple[Path | None, list[Diagnostic]]:
    sources = sum(value is not None for value in (request.body, request.body_file, request.registered_content_path))
    if sources == 0:
        return None, []
    if sources > 1:
        raise ResearchRecordError("Use one of body, body-file, or a registered content path.", code="body_source_conflict")
    if request.registered_content_path is not None:
        registered = request.registered_content_path.resolve(strict=False)
        if not registered.exists():
            raise ResearchRecordError(f"Registered content path does not exist: {registered}", code="registered_content_missing")
        return registered, []
    label = _semantic_label_for_request(request)
    result, diagnostics = resolve_semantic_path(context, label, env=env, cwd=cwd)
    if result is None:
        return None, diagnostics
    target_dir = result.path / "research-records" / request.record_kind / _slug(request.record_id or "record")
    target_dir.mkdir(parents=True, exist_ok=True)
    source_suffix = ""
    if request.body_file is not None:
        if not request.body_file.exists() or not request.body_file.is_file():
            raise ResearchRecordError(f"Body file does not exist: {request.body_file}", code="body_file_missing")
        source_suffix = request.body_file.suffix
    filename = _content_filename(request, suffix=source_suffix or ".md")
    target = target_dir / filename
    if request.body_file is not None:
        _atomic_copy(request.body_file, target)
    else:
        _atomic_write_text(target, request.body or "")
    return target.resolve(strict=False), diagnostics


def _request_with_resolved_idea_effects(
    context: EffectiveTopicContext,
    runtime_store: WorkspaceRuntimeStore,
    request: ResearchRecordRequest,
    preparation: StructuredPayloadPreparation | None,
) -> ResearchRecordRequest:
    payload_effects: dict[str, object] | None = None
    if preparation is not None:
        raw_effects = preparation.payload.get("research_idea_effects")
        if raw_effects is not None:
            if not isinstance(raw_effects, Mapping):
                raise ResearchRecordError("research_idea_effects must be an object.", code="invalid_research_idea_effects")
            payload_effects = {str(key): value for key, value in raw_effects.items()}
    if request.idea_effects is not None and payload_effects is not None and request.idea_effects != payload_effects:
        raise ResearchRecordError(
            "CLI and structured-payload Research Idea effects differ.",
            code="research_idea_effects_conflict",
        )
    selected_effects = request.idea_effects or payload_effects
    required = request.idea_effects_required
    profile_effects: Mapping[str, object] = {}
    if request.format_profile_ref is not None:
        registry = _artifact_format_registry(context, runtime_store)
        profile, _resolution, _diagnostics = ArtifactFormatResolver(registry).resolve_profile(request.format_profile_ref)
        if profile is not None:
            raw_profile_effects = profile.metadata.get("idea_effects")
            if isinstance(raw_profile_effects, Mapping):
                profile_effects = raw_profile_effects
                required = required or bool(raw_profile_effects.get("required"))
    if required and selected_effects is None:
        raise ResearchRecordError(
            "The selected record profile promises canonical Research Idea effects, but research_idea_effects is missing.",
            code="research_idea_effects_required",
            payload={"format_profile_ref": request.format_profile_ref},
        )
    if selected_effects is None:
        return replace(request, idea_effects_required=required)
    if selected_effects.get("atomic") is not True:
        raise ResearchRecordError("research_idea_effects must declare atomic=true.", code="research_idea_effects_not_atomic")
    payload_family = _optional_metadata_string(preparation.payload.get("artifact_family")) if preparation is not None else None
    effects_family = _optional_metadata_string(selected_effects.get("artifact_family"))
    required_family = _optional_metadata_string(profile_effects.get("artifact_family"))
    for expected_family in (payload_family, required_family):
        if effects_family is not None and expected_family is not None and effects_family != expected_family:
            raise ResearchRecordError(
                f"Research Idea effects artifact family {effects_family!r} does not match {expected_family!r}.",
                code="research_idea_effects_family_mismatch",
            )
    required_components = _string_list(profile_effects.get("required_components"))
    for component in required_components:
        value = selected_effects.get(component)
        if not isinstance(value, list) or not value:
            raise ResearchRecordError(
                f"The selected profile requires a non-empty research_idea_effects.{component} array.",
                code="research_idea_effects_component_missing",
                payload={"format_profile_ref": request.format_profile_ref, "component": component},
            )
    source_path_prefix = _optional_metadata_string(profile_effects.get("source_path_prefix"))
    if source_path_prefix is not None:
        ideas = selected_effects.get("ideas")
        if not isinstance(ideas, list) or any(
            not isinstance(item, Mapping)
            or not str(item.get("source_json_path") or "").startswith(source_path_prefix)
            for item in ideas
        ):
            raise ResearchRecordError(
                f"The selected profile requires exact idea paths under {source_path_prefix}.",
                code="research_idea_effects_source_path_profile_mismatch",
            )
    return replace(request, idea_effects=selected_effects, idea_effects_required=required)


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
    request_family = request.semantic_id.split(":", 1)[0].lower()
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
    stem = request.record_id or request.semantic_id or request.content_name or "structured-payload"
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
    _atomic_write_text(payload_path, json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
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
    _atomic_write_text(
        manifest_path,
        json.dumps({key: value for key, value in manifest.items() if value is not None}, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
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
    stem_source = request.semantic_id or request.profile or request.record_id or request.record_kind
    record_id = request.record_id or uuid.uuid4().hex[:12]
    return f"{_slug(stem_source)}-{_slug(record_id)}{suffix}"


def _atomic_copy(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, staged_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".staged", dir=target.parent)
    os.close(descriptor)
    staged = Path(staged_name)
    try:
        shutil.copyfile(source, staged)
        os.replace(staged, target)
    finally:
        staged.unlink(missing_ok=True)


def _atomic_write_text(target: Path, content: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, staged_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".staged", dir=target.parent)
    staged = Path(staged_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(staged, target)
    finally:
        staged.unlink(missing_ok=True)


def _cleanup_failed_record_content(request: ResearchRecordRequest, content_path: Path | None) -> dict[str, object]:
    if content_path is None or request.registered_content_path is not None:
        return {"attempted": False, "removed": []}
    removed: list[str] = []
    target = content_path.parent if content_path.name == "payload.json" else content_path.parent
    try:
        if target.exists():
            shutil.rmtree(target)
            removed.append(str(target))
        return {"attempted": True, "removed": removed, "complete": True}
    except OSError as exc:
        return {"attempted": True, "removed": removed, "complete": False, "error": str(exc), "remaining_path": str(target)}


def _new_record_id(request: ResearchRecordRequest) -> str:
    stem = request.semantic_id or request.profile or request.record_kind
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
    if request.idea_effects is not None:
        if any(
            value
            for value in (
                request.primary_idea,
                request.idea_realizations,
                request.idea_parents,
                request.realizes_idea_id,
            )
        ):
            raise ResearchRecordError(
                "research_idea_effects cannot be combined with legacy per-idea write arguments.",
                code="research_idea_effects_legacy_conflict",
            )
        return _store_canonical_idea_effects(
            context,
            runtime_store,
            request,
            record_id=record_id,
            created_at=created_at,
            updated_at=updated_at,
        )
    if request.idea_effects_required:
        raise ResearchRecordError(
            "The selected profile requires canonical Research Idea effects.",
            code="research_idea_effects_required",
        )
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


def _store_canonical_idea_effects(
    context: EffectiveTopicContext,
    runtime_store: WorkspaceRuntimeStore,
    request: ResearchRecordRequest,
    *,
    record_id: str,
    created_at: str,
    updated_at: str,
) -> dict[str, object]:
    effects = request.idea_effects or {}
    idea_inputs = _idea_effect_object_list(effects, "ideas", required=True)
    transition_inputs = _idea_effect_object_list(effects, "transitions")
    generation_inputs = _idea_effect_object_list(effects, "generation_groups")
    lineage_inputs = _idea_effect_object_list(effects, "lineage_edges")
    option_inputs = _idea_effect_object_list(effects, "decision_options")
    structured = runtime_store.get_structured_payload(record_id)
    if structured is None:
        raise ResearchRecordError(
            "Canonical Research Idea effects require a structured source payload.",
            code="research_idea_effects_payload_missing",
        )
    source_payload, source_diagnostics = load_structured_payload(context, structured)
    if not isinstance(source_payload, Mapping):
        raise ResearchRecordError(
            "Canonical Research Idea effects require an object-valued structured source payload.",
            code="research_idea_effects_payload_invalid",
            payload={"diagnostics": source_diagnostics},
        )

    input_digest = digest_json(
        {
            "record_id": record_id,
            "payload_digest": structured.payload_digest,
            "effects": effects,
        }
    )
    operation_id = _optional_metadata_string(effects.get("operation_id")) or f"idea-effects-{input_digest[:16]}"
    idempotency_key = _optional_metadata_string(effects.get("idempotency_key")) or f"record-idea-effects:{record_id}:{input_digest[:16]}"
    existing_operation = runtime_store.get_research_idea_operation_by_idempotency_key(
        idempotency_key,
        topic_workspace_id=context.topic_workspace_id,
    )
    if existing_operation is not None:
        if existing_operation.input_digest != input_digest:
            raise ResearchRecordError(
                f"Research Idea effect idempotency key has different input: {idempotency_key}",
                code="research_idea_effects_idempotency_conflict",
            )
        return {
            "replayed": True,
            "operation": existing_operation.to_json(),
            **existing_operation.result,
            "diagnostics": source_diagnostics,
        }
    operation_collision = runtime_store.get_research_idea_operation(
        operation_id,
        topic_workspace_id=context.topic_workspace_id,
    )
    if operation_collision is not None and operation_collision.input_digest != input_digest:
        raise ResearchRecordError(
            f"Research Idea effect operation id has different input: {operation_id}",
            code="research_idea_effects_operation_conflict",
        )

    actor_ref = _optional_metadata_string(effects.get("actor_ref")) or request.topic_actor_name or request.producer or request.skill
    transition_first_values: dict[tuple[str, str], str] = {}
    for index, item in enumerate(transition_inputs):
        idea_id = _required_idea_effect_string(item, "idea_id", f"transitions[{index}]")
        facet = _required_idea_effect_string(item, "facet", f"transitions[{index}]")
        previous_value = _required_idea_effect_string(item, "previous_value", f"transitions[{index}]")
        transition_first_values.setdefault((idea_id, facet), previous_value)

    diagnostics: list[dict[str, object]] = list(source_diagnostics)
    ideas: list[ResearchIdea] = []
    realizations: list[ResearchIdeaRealization] = []
    desired_state_by_idea: dict[str, dict[str, str]] = {}
    existing_idea_ids: set[str] = set()
    seen_idea_ids: set[str] = set()
    seen_source_paths: set[str] = set()
    for index, item in enumerate(idea_inputs):
        location = f"ideas[{index}]"
        idea_id = _required_idea_effect_string(item, "idea_id", location)
        if idea_id in seen_idea_ids:
            raise ResearchRecordError(f"Duplicate canonical idea id in Research Idea effects: {idea_id}", code="research_idea_effects_duplicate_idea")
        seen_idea_ids.add(idea_id)
        title = _required_idea_effect_string(item, "title", location)
        summary = _required_idea_effect_string(item, "summary", location)
        source_json_path = _required_idea_effect_string(item, "source_json_path", location)
        if source_json_path in seen_source_paths:
            raise ResearchRecordError(
                f"Research Idea effects map more than one idea to {source_json_path}.",
                code="research_idea_effects_duplicate_source_path",
            )
        seen_source_paths.add(source_json_path)
        source_resolution = resolve_payload_source_fragment(
            source_payload,
            source_json_path,
            format_profile_ref=structured.format_profile_ref,
            idea_id=idea_id,
            record_id=record_id,
            severity="error",
        )
        diagnostics.extend(source_resolution.diagnostics)
        if source_resolution.status != SOURCE_STATUS_EXACT or not isinstance(source_resolution.source_json, Mapping):
            raise ResearchRecordError(
                f"Research Idea {idea_id} must resolve to one exact source object.",
                code="research_idea_effects_source_not_exact",
                payload={"idea_id": idea_id, "source_json_path": source_json_path, "diagnostics": source_resolution.diagnostics},
            )
        aliases = sorted(set(_strict_string_list(item.get("aliases"), field=f"{location}.aliases")))
        source_labels = _idea_source_labels(source_resolution.source_json)
        if source_labels and source_labels.isdisjoint({idea_id, *aliases}):
            raise ResearchRecordError(
                f"Research Idea {idea_id} does not match its exact source-object identity.",
                code="research_idea_effects_source_label_mismatch",
                payload={"idea_id": idea_id, "aliases": aliases, "source_labels": sorted(source_labels)},
            )
        desired_state = {
            "exploration_state": _required_idea_effect_string(item, "exploration_state", location),
            "decision_state": _required_idea_effect_string(item, "decision_state", location),
            "evidence_state": _required_idea_effect_string(item, "evidence_state", location),
            "archive_state": _required_idea_effect_string(item, "archive_state", location),
            "visibility": _required_idea_effect_string(item, "visibility", location),
        }
        desired_state_by_idea[idea_id] = desired_state
        existing = runtime_store.get_research_idea(idea_id, topic_workspace_id=context.topic_workspace_id)
        if existing is not None:
            existing_idea_ids.add(idea_id)
        display_key: str | None
        if existing is None:
            initial_state = dict(desired_state)
            for facet in desired_state:
                first_value = transition_first_values.get((idea_id, facet))
                if first_value is not None:
                    initial_state[facet] = first_value
            display_key = _optional_metadata_string(item.get("display_key")) or runtime_store.next_research_idea_display_key(context.topic_workspace_id)
            base_metadata: dict[str, object] = {}
            idea_created_at = created_at
            provenance_refs = [_provenance_ref("research-idea", idea_id)]
        else:
            initial_state = {
                "exploration_state": existing.exploration_state,
                "decision_state": existing.decision_state,
                "evidence_state": existing.evidence_state,
                "archive_state": existing.archive_state,
                "visibility": existing.visibility,
            }
            display_key = _optional_metadata_string(item.get("display_key")) or existing.display_key
            base_metadata = dict(existing.metadata)
            aliases = sorted(set([*existing.aliases, *aliases]))
            idea_created_at = existing.created_at
            provenance_refs = list(existing.provenance_refs)
        closure_reason = _optional_metadata_string(item.get("closure_reason"))
        status = project_research_idea_compatibility_status(
            exploration_state=initial_state["exploration_state"],
            decision_state=initial_state["decision_state"],
            evidence_state=initial_state["evidence_state"],
            archive_state=initial_state["archive_state"],
            closure_reason=closure_reason,
            preserved_status=existing.status if existing is not None else None,
        )
        idea_metadata = {
            **base_metadata,
            **dict(item),
            "portfolio_state_version": 1,
            "idea_effect_operation_id": operation_id,
            "source_artifact_family": _optional_metadata_string(effects.get("artifact_family")) or source_payload.get("artifact_family"),
        }
        idea = _idea_record(
            context,
            idea_id=idea_id,
            display_key=display_key,
            title=title,
            summary=summary,
            family=_optional_metadata_string(item.get("family")) or _optional_metadata_string(effects.get("artifact_family")) or (existing.family if existing is not None else None),
            status=status,
            exploration_state=initial_state["exploration_state"],
            decision_state=initial_state["decision_state"],
            evidence_state=initial_state["evidence_state"],
            archive_state=initial_state["archive_state"],
            visibility=initial_state["visibility"],
            aliases=aliases,
            source_record_id=record_id,
            source_json_path=source_json_path,
            metadata=idea_metadata,
            created_at=idea_created_at,
            updated_at=updated_at,
        )
        idea = replace(idea, provenance_refs=provenance_refs)
        idea_diagnostics = runtime_store.validate_research_idea(idea)
        diagnostics.extend(idea_diagnostics)
        if _has_lineage_errors(idea_diagnostics):
            raise ResearchRecordError("Research Idea effects failed idea validation.", code="research_idea_effects_idea_invalid", payload={"diagnostics": diagnostics})
        runtime_store.upsert_research_idea(idea, validate=False)
        ideas.append(idea)
        realization = _idea_realization_record(
            context,
            idea_id=idea_id,
            record_id=record_id,
            source_json_path=source_json_path,
            realization_stage=_optional_metadata_string(item.get("realization_stage")),
            semantic_id=request.semantic_id,
            latest=bool(item.get("latest", True)),
            metadata={"source": "research_idea_effects", "operation_id": operation_id, **dict(item)},
            created_at=created_at,
            updated_at=updated_at,
        )
        realization_diagnostics = runtime_store.validate_research_idea_realization(realization)
        realization_diagnostics.extend(_validate_realization_source(context, runtime_store, realization, report_missing_payload=True))
        diagnostics.extend(realization_diagnostics)
        if _has_lineage_errors(realization_diagnostics):
            raise ResearchRecordError("Research Idea effects failed realization validation.", code="research_idea_effects_realization_invalid", payload={"diagnostics": diagnostics})
        runtime_store.upsert_research_idea_realization(realization, validate=False)
        realizations.append(realization)

    generation_groups: list[ResearchIdeaGenerationGroup] = []
    for index, item in enumerate(generation_inputs):
        location = f"generation_groups[{index}]"
        generation_id = _required_idea_effect_string(item, "generation_id", location)
        member_ids = _strict_string_list(item.get("member_idea_ids"), field=f"{location}.member_idea_ids", required=True)
        parent_ids = _strict_string_list(item.get("parent_idea_ids"), field=f"{location}.parent_idea_ids")
        if len(member_ids) != len(set(member_ids)) or len(parent_ids) != len(set(parent_ids)):
            raise ResearchRecordError(f"{location} contains duplicate idea ids.", code="research_idea_effects_generation_duplicate")
        for idea_id in [*member_ids, *parent_ids]:
            if runtime_store.get_research_idea(idea_id, topic_workspace_id=context.topic_workspace_id) is None:
                raise ResearchRecordError(f"{location} references a missing Research Idea: {idea_id}", code="research_idea_effects_generation_idea_missing")
        existing_group = runtime_store.get_research_idea_generation_group(generation_id)
        if existing_group is not None and existing_group.topic_workspace_id != context.topic_workspace_id:
            raise ResearchRecordError(f"Generation group is outside this Topic Workspace: {generation_id}", code="research_idea_effects_generation_cross_topic")
        decision_record_id = _optional_metadata_string(item.get("decision_record_id")) or request.decision_record_id
        if decision_record_id is None and request.record_kind == "decision_record":
            decision_record_id = record_id
        group = ResearchIdeaGenerationGroup(
            id=generation_id,
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            purpose=_optional_metadata_string(item.get("purpose")),
            parent_set_digest=_idea_parent_set_digest(parent_ids),
            producer_skill=request.skill,
            decision_record_id=decision_record_id,
            metadata={**dict(item), "member_idea_ids": member_ids, "parent_idea_ids": parent_ids, "operation_id": operation_id},
            created_at=existing_group.created_at if existing_group is not None else created_at,
            updated_at=updated_at,
            provenance_refs=existing_group.provenance_refs if existing_group is not None else [_provenance_ref("research-idea-generation-group", generation_id)],
        )
        runtime_store.upsert_research_idea_generation_group(group)
        generation_groups.append(group)

    edges: list[ResearchIdeaLineageEdge] = []
    for index, item in enumerate(lineage_inputs):
        location = f"lineage_edges[{index}]"
        edge = _idea_lineage_edge(
            context,
            parent_idea_id=_required_idea_effect_string(item, "parent_idea_id", location),
            child_idea_id=_required_idea_effect_string(item, "child_idea_id", location),
            lineage_kind=_required_idea_effect_string(item, "lineage_kind", location),
            parent_role=_optional_metadata_string(item.get("parent_role")),
            generation_id=_optional_metadata_string(item.get("generation_id")),
            decision_record_id=_optional_metadata_string(item.get("decision_record_id")) or request.decision_record_id,
            rationale=_optional_metadata_string(item.get("rationale")),
            status=_optional_metadata_string(item.get("status")) or "ready",
            confidence=_optional_float(item.get("confidence")),
            metadata={**dict(item), "operation_id": operation_id},
            created_at=created_at,
            updated_at=updated_at,
        )
        edge_diagnostics = runtime_store.validate_research_idea_lineage_edge(edge)
        diagnostics.extend(edge_diagnostics)
        if _has_lineage_errors(edge_diagnostics):
            raise ResearchRecordError("Research Idea effects failed lineage validation.", code="research_idea_effects_lineage_invalid", payload={"diagnostics": diagnostics})
        runtime_store.upsert_research_idea_lineage_edge(edge, validate=False)
        edges.append(edge)

    options: list[ResearchIdeaDecisionOption] = []
    option_outcomes: dict[str, set[str]] = {}
    for index, item in enumerate(option_inputs):
        location = f"decision_options[{index}]"
        idea_id = _required_idea_effect_string(item, "idea_id", location)
        outcome = _required_idea_effect_string(item, "outcome", location)
        decision_record_id = _optional_metadata_string(item.get("decision_record_id")) or request.decision_record_id
        if decision_record_id is None and request.record_kind == "decision_record":
            decision_record_id = record_id
        if decision_record_id is None:
            raise ResearchRecordError(f"{location} requires a Decision Record id.", code="research_idea_effects_decision_record_missing")
        option_digest = digest_json({"topic_workspace_id": context.topic_workspace_id, "decision_record_id": decision_record_id, "idea_id": idea_id})[:16]
        option_id = f"idea-decision-option-{option_digest}"
        existing_option = runtime_store.get_research_idea_decision_option(option_id)
        ordinal_value = item.get("ordinal")
        if ordinal_value is not None and (isinstance(ordinal_value, bool) or not isinstance(ordinal_value, int) or ordinal_value < 0):
            raise ResearchRecordError(f"{location}.ordinal must be a non-negative integer.", code="research_idea_effects_option_ordinal_invalid")
        option = ResearchIdeaDecisionOption(
            id=option_id,
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            decision_record_id=decision_record_id,
            idea_id=idea_id,
            outcome=cast(ResearchIdeaDecisionOptionOutcome, outcome),
            operation_id=operation_id,
            created_at=existing_option.created_at if existing_option is not None else created_at,
            updated_at=updated_at,
            option_role=_optional_metadata_string(item.get("option_role")),
            ordinal=cast(int | None, ordinal_value),
            generation_id=_optional_metadata_string(item.get("generation_id")),
            rationale=_optional_metadata_string(item.get("rationale")),
            consequence=_optional_metadata_string(item.get("consequence")),
            actor_ref=_optional_metadata_string(item.get("actor_ref")) or actor_ref,
            supporting_refs=_strict_string_list(item.get("supporting_refs"), field=f"{location}.supporting_refs"),
            metadata={**dict(item), "source_record_id": record_id, "option_set_complete": True},
            provenance_refs=existing_option.provenance_refs if existing_option is not None else [_provenance_ref("research-idea-decision-option", option_id)],
        )
        option_diagnostics = runtime_store.validate_research_idea_decision_option(option)
        diagnostics.extend(option_diagnostics)
        if _has_lineage_errors(option_diagnostics):
            raise ResearchRecordError("Research Idea effects failed decision-option validation.", code="research_idea_effects_decision_option_invalid", payload={"diagnostics": diagnostics})
        runtime_store.upsert_research_idea_decision_option(option, validate=False)
        options.append(option)
        option_outcomes.setdefault(idea_id, set()).add(outcome)

    transitions: list[ResearchIdeaStateTransition] = []
    for index, item in enumerate(transition_inputs):
        location = f"transitions[{index}]"
        idea_id = _required_idea_effect_string(item, "idea_id", location)
        if idea_id not in desired_state_by_idea:
            raise ResearchRecordError(f"{location} must name an idea declared in the same effect set.", code="research_idea_effects_transition_idea_undeclared")
        facet = _required_idea_effect_string(item, "facet", location)
        previous_value = _required_idea_effect_string(item, "previous_value", location)
        next_value = _required_idea_effect_string(item, "next_value", location)
        if previous_value == next_value:
            raise ResearchRecordError(f"{location} is a no-op transition.", code="research_idea_effects_transition_noop")
        current = runtime_store.get_research_idea(idea_id, topic_workspace_id=context.topic_workspace_id)
        if current is None:
            raise ResearchRecordError(f"{location} references a missing Research Idea.", code="research_idea_effects_transition_idea_missing")
        decision_record_id = _optional_metadata_string(item.get("decision_record_id")) or request.decision_record_id
        if decision_record_id is None and request.record_kind == "decision_record":
            decision_record_id = record_id
        transition_digest = digest_json(
            {
                "operation_id": operation_id,
                "ordinal": index,
                "idea_id": idea_id,
                "facet": facet,
                "previous_value": previous_value,
                "next_value": next_value,
            }
        )[:16]
        transition_id = f"idea-transition-{transition_digest}"
        transition = ResearchIdeaStateTransition(
            id=transition_id,
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            idea_id=idea_id,
            facet=cast(ResearchIdeaFacet, facet),
            previous_value=previous_value,
            next_value=next_value,
            operation_id=operation_id,
            actor_ref=_optional_metadata_string(item.get("actor_ref")) or actor_ref or "unknown-actor",
            rationale=_required_idea_effect_string(item, "rationale", location),
            transitioned_at=_optional_metadata_string(item.get("transitioned_at")) or updated_at,
            reason_code=_optional_metadata_string(item.get("reason_code")),
            decision_record_id=decision_record_id,
            gate_id=_optional_metadata_string(item.get("gate_id")),
            evidence_item_refs=_strict_string_list(item.get("evidence_item_refs"), field=f"{location}.evidence_item_refs"),
            artifact_refs=_strict_string_list(item.get("artifact_refs"), field=f"{location}.artifact_refs"),
            finding_refs=_strict_string_list(item.get("finding_refs"), field=f"{location}.finding_refs"),
            research_task_id=_optional_metadata_string(item.get("research_task_id")),
            run_id=_optional_metadata_string(item.get("run_id")),
            provenance_record_refs=_strict_string_list(item.get("provenance_record_refs"), field=f"{location}.provenance_record_refs"),
            metadata={**dict(item), "source_record_id": record_id},
            provenance_refs=[_provenance_ref("research-idea-state-transition", transition_id)],
        )
        transition_diagnostics = runtime_store.validate_research_idea_state_transition(transition)
        diagnostics.extend(transition_diagnostics)
        if _has_lineage_errors(transition_diagnostics):
            raise ResearchRecordError("Research Idea effects failed transition validation.", code="research_idea_effects_transition_invalid", payload={"diagnostics": diagnostics})
        next_state = {
            "exploration_state": current.exploration_state,
            "decision_state": current.decision_state,
            "evidence_state": current.evidence_state,
            "archive_state": current.archive_state,
            "visibility": current.visibility,
        }
        next_state[facet] = next_value
        next_idea = replace(
            current,
            exploration_state=cast(ResearchIdeaExplorationState, next_state["exploration_state"]),
            decision_state=cast(ResearchIdeaDecisionState, next_state["decision_state"]),
            evidence_state=cast(ResearchIdeaEvidenceState, next_state["evidence_state"]),
            archive_state=cast(ResearchIdeaArchiveState, next_state["archive_state"]),
            visibility=next_state["visibility"],
            status=project_research_idea_compatibility_status(
                exploration_state=next_state["exploration_state"],
                decision_state=next_state["decision_state"],
                evidence_state=next_state["evidence_state"],
                archive_state=next_state["archive_state"],
                closure_reason=transition.reason_code,
                preserved_status=current.status,
            ),
            updated_at=transition.transitioned_at,
        )
        next_diagnostics = runtime_store.validate_research_idea(next_idea)
        diagnostics.extend(next_diagnostics)
        if _has_lineage_errors(next_diagnostics):
            raise ResearchRecordError("Research Idea effects produced invalid current state.", code="research_idea_effects_transition_result_invalid", payload={"diagnostics": diagnostics})
        runtime_store.upsert_research_idea(next_idea, validate=False)
        runtime_store.upsert_research_idea_state_transition(transition, validate=False)
        transitions.append(transition)

    current_ideas: list[ResearchIdea] = []
    for idea_id, desired_state in desired_state_by_idea.items():
        current = runtime_store.get_research_idea(idea_id, topic_workspace_id=context.topic_workspace_id)
        if current is None:
            raise ResearchRecordError(f"Research Idea effect disappeared during acceptance: {idea_id}", code="research_idea_effects_idea_missing")
        observed_state = {
            "exploration_state": current.exploration_state,
            "decision_state": current.decision_state,
            "evidence_state": current.evidence_state,
            "archive_state": current.archive_state,
            "visibility": current.visibility,
        }
        if observed_state != desired_state:
            raise ResearchRecordError(
                f"Research Idea effects do not transition {idea_id} to the declared current facets.",
                code="research_idea_effects_partial_state",
                payload={"idea_id": idea_id, "declared": desired_state, "observed": observed_state},
            )
        current_ideas.append(current)

    required_outcomes = {
        "selected": "selected",
        "deferred": "deferred",
        "closed": "closed",
        "shortlisted": "shortlisted",
    }
    transition_targets = {
        (transition.idea_id, transition.facet, transition.next_value)
        for transition in transitions
    }
    for idea_id, desired_state in desired_state_by_idea.items():
        decision_state = desired_state["decision_state"]
        if idea_id not in existing_idea_ids and decision_state in required_outcomes and (idea_id, "decision_state", decision_state) not in transition_targets:
            raise ResearchRecordError(
                f"New Research Idea {idea_id} requires a justified transition to decision state {decision_state}.",
                code="research_idea_effects_initial_decision_transition_missing",
            )
    for transition in transitions:
        if transition.facet != "decision_state":
            continue
        expected_outcome = required_outcomes.get(transition.next_value)
        if transition.next_value == "open" and transition.previous_value in {"closed", "deferred"}:
            expected_outcome = "reopened"
        if expected_outcome is not None and expected_outcome not in option_outcomes.get(transition.idea_id, set()):
            raise ResearchRecordError(
                f"Decision transition for {transition.idea_id} lacks a matching Decision Record option outcome: {expected_outcome}",
                code="research_idea_effects_decision_option_missing",
            )

    result: dict[str, object] = {
        "ideas": [item.to_json() for item in current_ideas],
        "realizations": [item.to_json() for item in realizations],
        "generation_groups": [item.to_json() for item in generation_groups],
        "edges": [item.to_json() for item in edges],
        "decision_options": [item.to_json() for item in options],
        "transitions": [item.to_json() for item in transitions],
    }
    operation = ResearchIdeaOperation(
        id=f"idea-operation-{_slug(context.topic_workspace_id)}-{_slug(operation_id)}",
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        operation_id=operation_id,
        idempotency_key=idempotency_key,
        action_kind="record_acceptance",
        input_digest=input_digest,
        status="committed",
        result=result,
        created_at=created_at,
        updated_at=updated_at,
        actor_ref=actor_ref,
        metadata={"record_id": record_id, "format_profile_ref": request.format_profile_ref},
        provenance_refs=[_provenance_ref("research-idea-operation", operation_id)],
    )
    runtime_store.upsert_research_idea_operation(operation)
    return {"replayed": False, "operation": operation.to_json(), **result, "diagnostics": diagnostics}


def _idea_effect_object_list(
    effects: Mapping[str, object],
    field: str,
    *,
    required: bool = False,
) -> list[dict[str, object]]:
    raw = effects.get(field)
    if raw is None:
        if required:
            raise ResearchRecordError(f"research_idea_effects.{field} is required.", code="research_idea_effects_component_missing")
        return []
    if not isinstance(raw, list) or (required and not raw):
        raise ResearchRecordError(f"research_idea_effects.{field} must be a non-empty array." if required else f"research_idea_effects.{field} must be an array.", code="research_idea_effects_component_invalid")
    items: list[dict[str, object]] = []
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            raise ResearchRecordError(f"research_idea_effects.{field}[{index}] must be an object.", code="research_idea_effects_component_invalid")
        items.append({str(key): value for key, value in item.items()})
    return items


def _required_idea_effect_string(item: Mapping[str, object], field: str, location: str) -> str:
    value = _optional_metadata_string(item.get(field))
    if value is None:
        raise ResearchRecordError(f"research_idea_effects.{location}.{field} is required.", code="research_idea_effects_field_missing")
    return value


def _strict_string_list(value: object, *, field: str, required: bool = False) -> list[str]:
    if value is None:
        if required:
            raise ResearchRecordError(f"research_idea_effects.{field} is required.", code="research_idea_effects_field_missing")
        return []
    if not isinstance(value, list):
        raise ResearchRecordError(f"research_idea_effects.{field} must be an array of strings.", code="research_idea_effects_field_invalid")
    result: list[str] = []
    for item in value:
        selected = _optional_metadata_string(item)
        if selected is None:
            raise ResearchRecordError(f"research_idea_effects.{field} must contain non-empty strings.", code="research_idea_effects_field_invalid")
        result.append(selected)
    if required and not result:
        raise ResearchRecordError(f"research_idea_effects.{field} must not be empty.", code="research_idea_effects_field_invalid")
    return result


def _idea_record(
    context: EffectiveTopicContext,
    *,
    idea_id: str,
    display_key: str | None = None,
    title: str,
    summary: str,
    family: str | None,
    status: str,
    exploration_state: str = "unknown",
    decision_state: str = "unknown",
    evidence_state: str = "unknown",
    archive_state: str = "active",
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
        exploration_state=cast(ResearchIdeaExplorationState, exploration_state),
        decision_state=cast(ResearchIdeaDecisionState, decision_state),
        evidence_state=cast(ResearchIdeaEvidenceState, evidence_state),
        archive_state=cast(ResearchIdeaArchiveState, archive_state),
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
    for key in ("canonical_idea_id", "idea_id", "direction_id", "proposal_id", "id", "label", "candidate_id"):
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


def _legacy_kaoju_direction_migration_plan(
    context: EffectiveTopicContext,
    runtime_store: WorkspaceRuntimeStore,
    record_id: str,
    payload: Mapping[str, object],
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    sections = payload.get("sections") if isinstance(payload.get("sections"), Mapping) else {}
    raw_proposals = sections.get("proposals") if isinstance(sections, Mapping) else None
    proposals = raw_proposals if isinstance(raw_proposals, list) else []
    raw_selections = sections.get("selections") if isinstance(sections, Mapping) else None
    selections = raw_selections if isinstance(raw_selections, list) else []
    confirmation = sections.get("confirmation") if isinstance(sections, Mapping) and isinstance(sections.get("confirmation"), Mapping) else {}
    diagnostics: list[dict[str, object]] = []
    if not proposals:
        diagnostics.append({"severity": "error", "code": "legacy_direction_proposals_missing", "message": "Legacy Kaoju Direction Set contains no durable proposal objects.", "record_id": record_id})
    selected_direction_ids: list[str] = []
    selection_rationales: dict[str, str] = {}
    for index, selection in enumerate(selections):
        if isinstance(selection, str) and selection.strip():
            selected_direction_ids.append(selection.strip())
            continue
        if isinstance(selection, Mapping):
            selection_id = _optional_metadata_string(selection.get("id") or selection.get("direction_id"))
            if selection_id is not None:
                selected_direction_ids.append(selection_id)
                rationale = _optional_metadata_string(selection.get("rationale"))
                if rationale is not None:
                    selection_rationales[selection_id] = rationale
                continue
        diagnostics.append({"severity": "error", "code": "legacy_direction_selection_invalid", "message": f"Legacy Direction Set selection {index} does not identify one proposal.", "record_id": record_id, "selection_index": index})
    confirmation_accepted = bool(isinstance(confirmation, Mapping) and confirmation.get("status") == "accepted")
    confirmation_actor = _optional_metadata_string(confirmation.get("actor_ref")) if isinstance(confirmation, Mapping) else None
    actor_ref = confirmation_actor or "actor:isomer-migration"
    if not confirmation_accepted:
        diagnostics.append({"severity": "warning", "code": "legacy_direction_confirmation_unknown", "message": "Direction Set confirmation is not accepted; migration will leave every decision state unknown and will not create Decision Record option membership.", "record_id": record_id})
    elif confirmation_actor is None:
        diagnostics.append({"severity": "warning", "code": "legacy_direction_actor_unknown", "message": "Accepted Direction Set does not identify the confirming actor; migration provenance will use the Isomer migration actor.", "record_id": record_id})

    plan: list[dict[str, object]] = []
    observed_direction_ids: set[str] = set()
    observed_idea_ids: set[str] = set()
    direction_to_idea: dict[str, str] = {}
    for index, raw_proposal in enumerate(proposals):
        path = f"$.sections.proposals[{index}]"
        if not isinstance(raw_proposal, Mapping):
            diagnostics.append({"severity": "error", "code": "legacy_direction_proposal_invalid", "message": f"Direction proposal {index} is not an object.", "record_id": record_id, "source_json_path": path})
            continue
        direction_id = _optional_metadata_string(raw_proposal.get("id") or raw_proposal.get("direction_id"))
        if direction_id is None:
            diagnostics.append({"severity": "error", "code": "legacy_direction_id_missing", "message": f"Direction proposal {index} has no stable direction id.", "record_id": record_id, "source_json_path": path})
            direction_id = f"missing-{index + 1}"
        elif direction_id in observed_direction_ids:
            diagnostics.append({"severity": "error", "code": "legacy_direction_id_duplicate", "message": f"Direction id is duplicated: {direction_id}", "record_id": record_id, "direction_id": direction_id})
        observed_direction_ids.add(direction_id)
        authored_idea_id = _optional_metadata_string(raw_proposal.get("idea_id"))
        idea_id = authored_idea_id or f"kaoju-direction-{_slug(direction_id)}"
        if idea_id in observed_idea_ids:
            diagnostics.append({"severity": "error", "code": "legacy_direction_idea_id_duplicate", "message": f"Canonical Research Idea id would be duplicated: {idea_id}", "record_id": record_id, "idea_id": idea_id})
        observed_idea_ids.add(idea_id)
        direction_to_idea[direction_id] = idea_id
        title = _optional_metadata_string(raw_proposal.get("title"))
        summary = _optional_metadata_string(raw_proposal.get("summary")) or _optional_metadata_string(raw_proposal.get("research_question"))
        if title is None:
            diagnostics.append({"severity": "error", "code": "legacy_direction_title_missing", "message": f"Direction {direction_id} has no authored title.", "record_id": record_id, "source_json_path": path})
        if summary is None:
            diagnostics.append({"severity": "error", "code": "legacy_direction_summary_missing", "message": f"Direction {direction_id} has no authored summary or research question.", "record_id": record_id, "source_json_path": path})
        existing = runtime_store.get_research_idea(idea_id, topic_workspace_id=context.topic_workspace_id)
        if existing is not None:
            diagnostics.append({"severity": "error", "code": "legacy_direction_idea_collision", "message": f"Direction {direction_id} maps to an existing canonical Research Idea: {idea_id}", "record_id": record_id, "idea_id": idea_id, "existing_source_record_id": existing.source_record_id})
        rationale = _optional_metadata_string(raw_proposal.get("disposition_rationale") or raw_proposal.get("rationale")) or selection_rationales.get(direction_id)
        ambiguous_fields = ["exploration_state", "evidence_state"]
        if direction_id not in selected_direction_ids or not confirmation_accepted:
            ambiguous_fields.append("decision_state")
        if rationale is None:
            diagnostics.append({"severity": "warning", "code": "legacy_direction_rationale_unknown", "message": f"Direction {direction_id} has no authored disposition rationale; migration will preserve that omission.", "record_id": record_id, "idea_id": idea_id})
        for facet in ambiguous_fields:
            diagnostics.append({"severity": "warning", "code": "legacy_direction_classification_unknown", "message": f"Legacy Direction Set does not justify {facet} for {direction_id}.", "record_id": record_id, "idea_id": idea_id, "facet": facet})
        plan.append(
            {
                "direction_id": direction_id,
                "idea_id": idea_id,
                "title": title or direction_id,
                "summary": summary or "Missing authored proposal summary.",
                "source_json_path": path,
                "aliases": [direction_id],
                "facets": {
                    "exploration_state": "unknown",
                    "decision_state": "selected" if confirmation_accepted and direction_id in selected_direction_ids else "unknown",
                    "evidence_state": "unknown",
                    "archive_state": "active",
                    "visibility": "primary",
                },
                "decision_outcome": "selected" if direction_id in selected_direction_ids else "not_selected",
                "rationale": rationale,
                "ambiguous_fields": ambiguous_fields,
                "lineage": [],
            }
        )
    unknown_selections = sorted(set(selected_direction_ids) - observed_direction_ids)
    for direction_id in unknown_selections:
        diagnostics.append({"severity": "error", "code": "legacy_direction_selection_unknown", "message": f"Accepted selection does not resolve to a proposal: {direction_id}", "record_id": record_id, "direction_id": direction_id})
    selected_idea_ids = [direction_to_idea[item] for item in selected_direction_ids if item in direction_to_idea] if confirmation_accepted else []
    generation_id = f"idea-generation-kaoju-legacy-{digest_json({'topic_workspace_id': context.topic_workspace_id, 'record_id': record_id})[:16]}"
    metadata = {
        "generation_id": generation_id,
        "selected_direction_ids": selected_direction_ids if confirmation_accepted else [],
        "selected_idea_ids": selected_idea_ids,
        "confirmation_accepted": confirmation_accepted,
        "actor_ref": actor_ref,
        "lineage_policy": "none_invented",
        "option_set_complete": confirmation_accepted and not unknown_selections and bool(plan),
    }
    return plan, diagnostics, metadata


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
        ("semantic_id", request.semantic_id),
        ("scope_key", request.scope_key),
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


def effective_records_list_limit(
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
