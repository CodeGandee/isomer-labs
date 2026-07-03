"""Topic Workspace reset checkpoint, plan, and apply APIs."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import re
import shutil
from typing import Any, Mapping
import uuid

from isomer_labs.artifact_formats import (
    ArtifactFormatRegistry,
    WorkspaceRuntimeArtifactFormatProvider,
    digest_bytes,
    digest_json,
    render_artifact,
    validate_payload,
)
from isomer_labs.deepsci_ext.record_formats import register_deepsci_record_format_provider
from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.core.path_utils import canonicalize, is_within
from isomer_labs.workspace.paths import preview_paths, resolve_semantic_path
from isomer_labs.runtime.identifiers import _provenance_ref, _slug
from isomer_labs.runtime.models import (
    ArtifactFormatRegistrationRecord,
    ResetCheckpointRecord,
    ResetOutcomeRecord,
    ResetPlanActionRecord,
    ResetPlanRecord,
    RuntimeLifecycleRecord,
    StructuredResearchPayloadRecord,
    TopicEnvironmentReadinessRecord,
    utc_timestamp,
)
from isomer_labs.runtime.store import WorkspaceRuntimeStore, open_workspace_runtime


CHECKPOINT_PROFILE_REF = "isomer:deepsci/record-format/profile/control/topic-reset-checkpoint/v1"
PLAN_PROFILE_REF = "isomer:deepsci/record-format/profile/control/topic-reset-plan/v1"
OUTCOME_PROFILE_REF = "isomer:deepsci/record-format/profile/report/topic-reset-outcome/v1"
RESET_RECORD_LABEL = "topic.records.views"
RESET_RECORD_DIRNAME = "topic-reset"
RESET_ACTIONS = ("preserve", "delete_record", "delete_file", "delete_generated_view", "regenerate", "skip", "blocked")
MANAGED_WORKSPACE_LABELS = {"topic.actors.workspace", "agent.workspace"}
SECRET_NAME_FRAGMENTS = (".env", "secret", "token", "credential", "private-key", "private_key")
OPEN_HANDOFF_STATUSES = {"draft", "sent", "observing", "candidate", "blocked", "repair", "follow_up", "stale"}
LIVE_ADAPTER_STATUSES = {"running", "launched", "partial"}


def create_reset_checkpoint(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    actor_ref: str | None = None,
    checkpoint_id: str | None = None,
    render_markdown: bool = True,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """Create a topic-scoped reset checkpoint from current initialization state."""

    store, diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    if store is None:
        return _runtime_missing_payload("checkpoint", diagnostics), diagnostics
    try:
        timestamp = utc_timestamp()
        selected_checkpoint_id = checkpoint_id or f"topic-reset-checkpoint-{_slug(context.topic_workspace_id)}-{uuid.uuid4().hex[:12]}"
        semantic_inventory, inventory_diagnostics = _semantic_path_inventory(context, env)
        diagnostics.extend(inventory_diagnostics)
        if has_errors(diagnostics):
            return _diagnostic_payload("checkpoint", diagnostics), diagnostics
        payload = _checkpoint_payload(
            context,
            store,
            checkpoint_id=selected_checkpoint_id,
            actor_ref=actor_ref,
            created_at=timestamp,
            semantic_inventory=semantic_inventory,
        )
        payload_diagnostics = _forbidden_git_payload_diagnostics(payload, concept="Topic Reset Checkpoint", record_id=selected_checkpoint_id)
        diagnostics.extend(payload_diagnostics)
        render_path, render_digest, render_diagnostics = _render_reset_markdown(
            context,
            store,
            payload,
            profile_ref=CHECKPOINT_PROFILE_REF,
            content_name=f"{selected_checkpoint_id}.md",
            env=env,
            enabled=render_markdown,
        )
        diagnostics.extend(render_diagnostics)
        if has_errors(diagnostics):
            return _diagnostic_payload("checkpoint", diagnostics), diagnostics
        checkpoint_digest = digest_json(payload)
        checkpoint = ResetCheckpointRecord(
            id=selected_checkpoint_id,
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            status="ready",
            payload_json=payload,
            payload_digest=digest_json(payload),
            checkpoint_digest=checkpoint_digest,
            actor_ref=actor_ref,
            source_record_id=selected_checkpoint_id,
            rendered_markdown_path=str(render_path) if render_path is not None else None,
            rendered_markdown_digest=render_digest,
            diagnostics=[],
            created_at=timestamp,
            updated_at=timestamp,
            provenance_refs=[_provenance_ref("topic-reset-checkpoint", selected_checkpoint_id)],
        )
        with store.connection:
            _write_reset_structured_record(
                context,
                store,
                record_id=selected_checkpoint_id,
                record_kind="decision_record",
                status="ready",
                profile_ref=CHECKPOINT_PROFILE_REF,
                payload=payload,
                rendered_markdown_path=render_path,
                rendered_markdown_digest=render_digest,
                created_at=timestamp,
                updated_at=timestamp,
                actor_ref=actor_ref,
                reset_kind="checkpoint",
            )
            store.upsert_reset_checkpoint(checkpoint)
        stored = store.get_reset_checkpoint(selected_checkpoint_id) or checkpoint
        return {
            "ok": True,
            "mutated": True,
            "operation": "checkpoint",
            "research_topic_id": context.research_topic.id,
            "topic_workspace_id": context.topic_workspace_id,
            "checkpoint_id": stored.id,
            "checkpoint": stored.to_json(),
            "rendered_markdown_path": stored.rendered_markdown_path,
            "diagnostics": [],
        }, diagnostics
    finally:
        store.close()


def update_reset_checkpoint(
    context: EffectiveTopicContext,
    checkpoint_id: str,
    *,
    env: Mapping[str, str],
    actor_ref: str | None = None,
    preserve_record_ids: list[str] | None = None,
    preserve_structured_payload_ids: list[str] | None = None,
    preserve_generated_view_paths: list[str] | None = None,
    preserve_semantic_labels: list[str] | None = None,
    preserve_support_paths: list[str] | None = None,
    provenance_refs: list[str] | None = None,
    source_label: str | None = None,
    render_markdown: bool = True,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """Extend a checkpoint with later setup that should survive reset."""

    store, diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    if store is None:
        return _runtime_missing_payload("update-checkpoint", diagnostics), diagnostics
    try:
        checkpoint = store.get_reset_checkpoint(checkpoint_id)
        if checkpoint is None or not _checkpoint_belongs_to_context(checkpoint, context):
            diagnostics.append(_missing_checkpoint_diagnostic(checkpoint_id))
            return _diagnostic_payload("update-checkpoint", diagnostics), diagnostics
        timestamp = utc_timestamp()
        payload = dict(checkpoint.payload_json)
        _merge_payload_list(payload, "preserved_record_ids", preserve_record_ids or [])
        _merge_payload_list(payload, "preserved_structured_payload_ids", preserve_structured_payload_ids or [])
        _merge_payload_list(payload, "preserved_generated_view_paths", preserve_generated_view_paths or [])
        _merge_payload_list(payload, "preserved_semantic_labels", preserve_semantic_labels or [])
        _merge_payload_list(payload, "preserved_support_paths", preserve_support_paths or [])
        _merge_payload_list(payload, "provenance_refs", provenance_refs or [])
        extensions = payload.get("extensions")
        if not isinstance(extensions, list):
            extensions = []
        extensions.append(
            {
                "updated_at": timestamp,
                "actor_ref": actor_ref,
                "source_label": source_label or "checkpoint-update",
                "preserved_record_ids": list(preserve_record_ids or []),
                "preserved_structured_payload_ids": list(preserve_structured_payload_ids or []),
                "preserved_generated_view_paths": list(preserve_generated_view_paths or []),
                "preserved_semantic_labels": list(preserve_semantic_labels or []),
                "preserved_support_paths": list(preserve_support_paths or []),
                "provenance_refs": list(provenance_refs or []),
            }
        )
        payload["extensions"] = extensions
        payload["updated_at"] = timestamp
        diagnostics.extend(_forbidden_git_payload_diagnostics(payload, concept="Topic Reset Checkpoint", record_id=checkpoint_id))
        render_path, render_digest, render_diagnostics = _render_reset_markdown(
            context,
            store,
            payload,
            profile_ref=CHECKPOINT_PROFILE_REF,
            content_name=f"{checkpoint_id}.md",
            env=env,
            enabled=render_markdown,
        )
        diagnostics.extend(render_diagnostics)
        if has_errors(diagnostics):
            return _diagnostic_payload("update-checkpoint", diagnostics), diagnostics
        updated = replace(
            checkpoint,
            payload_json=payload,
            payload_digest=digest_json(payload),
            checkpoint_digest=digest_json(payload),
            actor_ref=actor_ref or checkpoint.actor_ref,
            rendered_markdown_path=str(render_path) if render_path is not None else checkpoint.rendered_markdown_path,
            rendered_markdown_digest=render_digest or checkpoint.rendered_markdown_digest,
            updated_at=timestamp,
            provenance_refs=list(dict.fromkeys([*checkpoint.provenance_refs, *(provenance_refs or [])])),
        )
        with store.connection:
            _write_reset_structured_record(
                context,
                store,
                record_id=checkpoint_id,
                record_kind="decision_record",
                status="ready",
                profile_ref=CHECKPOINT_PROFILE_REF,
                payload=payload,
                rendered_markdown_path=render_path or (Path(checkpoint.rendered_markdown_path) if checkpoint.rendered_markdown_path else None),
                rendered_markdown_digest=updated.rendered_markdown_digest,
                created_at=checkpoint.created_at,
                updated_at=timestamp,
                actor_ref=actor_ref,
                reset_kind="checkpoint",
            )
            store.upsert_reset_checkpoint(updated)
        stored = store.get_reset_checkpoint(checkpoint_id) or updated
        return {
            "ok": True,
            "mutated": True,
            "operation": "update-checkpoint",
            "research_topic_id": context.research_topic.id,
            "topic_workspace_id": context.topic_workspace_id,
            "checkpoint_id": checkpoint_id,
            "checkpoint": stored.to_json(),
            "rendered_markdown_path": stored.rendered_markdown_path,
        }, diagnostics
    finally:
        store.close()


def list_reset_checkpoints(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    include_payload: bool = False,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if store is None:
        return _runtime_missing_payload("list", diagnostics), diagnostics
    try:
        records = store.list_reset_checkpoints(topic_workspace_id=context.topic_workspace_id)
        return {
            "ok": True,
            "mutated": False,
            "operation": "list",
            "research_topic_id": context.research_topic.id,
            "topic_workspace_id": context.topic_workspace_id,
            "count": len(records),
            "checkpoints": [
                record.to_json(include_payload=include_payload, include_diagnostics=include_payload)
                for record in records
            ],
        }, diagnostics
    finally:
        store.close()


def show_reset_checkpoint(
    context: EffectiveTopicContext,
    checkpoint_id: str,
    *,
    env: Mapping[str, str],
    include_payload: bool = False,
    include_rendered_body: bool = False,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if store is None:
        return _runtime_missing_payload("show", diagnostics), diagnostics
    try:
        checkpoint = store.get_reset_checkpoint(checkpoint_id)
        if checkpoint is None or not _checkpoint_belongs_to_context(checkpoint, context):
            diagnostics.append(_missing_checkpoint_diagnostic(checkpoint_id))
            return _diagnostic_payload("show", diagnostics), diagnostics
        payload: dict[str, Any] = {
            "ok": True,
            "mutated": False,
            "operation": "show",
            "research_topic_id": context.research_topic.id,
            "topic_workspace_id": context.topic_workspace_id,
            "checkpoint_id": checkpoint.id,
            "checkpoint": checkpoint.to_json(include_payload=include_payload, include_diagnostics=include_payload),
        }
        if include_rendered_body:
            payload["rendered_body"] = _read_text_path(checkpoint.rendered_markdown_path)
        return payload, diagnostics
    finally:
        store.close()


def plan_topic_reset(
    context: EffectiveTopicContext,
    checkpoint_id: str,
    *,
    env: Mapping[str, str],
    actor_ref: str | None = None,
    plan_id: str | None = None,
    render_markdown: bool = True,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """Generate and store a read-only destructive reset plan."""

    store, diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    if store is None:
        return _runtime_missing_payload("plan", diagnostics), diagnostics
    try:
        checkpoint = store.get_reset_checkpoint(checkpoint_id)
        if checkpoint is None or not _checkpoint_belongs_to_context(checkpoint, context):
            diagnostics.append(_missing_checkpoint_diagnostic(checkpoint_id))
            return _diagnostic_payload("plan", diagnostics), diagnostics
        timestamp = utc_timestamp()
        selected_plan_id = plan_id or f"topic-reset-plan-{_slug(checkpoint_id)}-{uuid.uuid4().hex[:12]}"
        precondition_payload = _runtime_precondition_payload(store, context)
        precondition_digest = digest_json(precondition_payload)
        actions, action_diagnostics = _build_reset_actions(context, store, checkpoint, plan_id=selected_plan_id)
        diagnostics.extend(action_diagnostics)
        blocker_actions = [action for action in actions if action.action == "blocked"]
        status = "blocked" if blocker_actions or has_errors(diagnostics) else "ready"
        payload = {
            "title": "Topic Reset Plan",
            "summary": "Read-only destructive reset plan for returning a Topic Workspace to its selected checkpoint.",
            "status": status,
            "research_topic_id": context.research_topic.id,
            "topic_workspace_id": context.topic_workspace_id,
            "checkpoint_id": checkpoint.id,
            "plan_id": selected_plan_id,
            "checkpoint_digest": checkpoint.checkpoint_digest,
            "precondition_digest": precondition_digest,
            "preconditions": precondition_payload,
            "actions": [action.to_json() for action in actions],
            "blockers": [action.to_json() for action in blocker_actions],
            "no_git_operations": True,
            "created_at": timestamp,
            "actor_ref": actor_ref,
        }
        diagnostics.extend(_forbidden_git_payload_diagnostics(payload, concept="Topic Reset Plan", record_id=selected_plan_id))
        render_path, render_digest, render_diagnostics = _render_reset_markdown(
            context,
            store,
            payload,
            profile_ref=PLAN_PROFILE_REF,
            content_name=f"{selected_plan_id}.md",
            env=env,
            enabled=render_markdown,
        )
        diagnostics.extend(render_diagnostics)
        if has_errors(diagnostics):
            status = "blocked"
        plan = ResetPlanRecord(
            id=selected_plan_id,
            checkpoint_id=checkpoint.id,
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            status=status,
            payload_json=payload,
            payload_digest=digest_json(payload),
            checkpoint_digest=checkpoint.checkpoint_digest,
            precondition_digest=precondition_digest,
            actor_ref=actor_ref,
            rendered_markdown_path=str(render_path) if render_path is not None else None,
            rendered_markdown_digest=render_digest,
            diagnostics=[diagnostic.to_json() for diagnostic in diagnostics],
            created_at=timestamp,
            updated_at=timestamp,
            provenance_refs=[_provenance_ref("topic-reset-plan", selected_plan_id)],
        )
        with store.connection:
            _write_reset_structured_record(
                context,
                store,
                record_id=selected_plan_id,
                record_kind="decision_record",
                status="blocked" if status == "blocked" else "ready",
                profile_ref=PLAN_PROFILE_REF,
                payload=payload,
                rendered_markdown_path=render_path,
                rendered_markdown_digest=render_digest,
                created_at=timestamp,
                updated_at=timestamp,
                actor_ref=actor_ref,
                reset_kind="plan",
            )
            store.upsert_reset_plan(plan, actions=actions)
        stored = store.get_reset_plan(selected_plan_id) or plan
        return {
            "ok": status == "ready" and not has_errors(diagnostics),
            "mutated": True,
            "operation": "plan",
            "research_topic_id": context.research_topic.id,
            "topic_workspace_id": context.topic_workspace_id,
            "checkpoint_id": checkpoint.id,
            "plan_id": stored.id,
            "plan": stored.to_json(),
            "actions": [action.to_json() for action in actions],
            "blockers": [action.to_json() for action in blocker_actions],
            "rendered_markdown_path": stored.rendered_markdown_path,
        }, diagnostics
    finally:
        store.close()


def show_reset_plan(
    context: EffectiveTopicContext,
    plan_id: str,
    *,
    env: Mapping[str, str],
    include_payload: bool = False,
    include_rendered_body: bool = False,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if store is None:
        return _runtime_missing_payload("show-plan", diagnostics), diagnostics
    try:
        plan = store.get_reset_plan(plan_id)
        if plan is None or not _plan_belongs_to_context(plan, context):
            diagnostics.append(_missing_plan_diagnostic(plan_id))
            return _diagnostic_payload("show-plan", diagnostics), diagnostics
        actions = store.list_reset_plan_actions(plan_id=plan_id)
        payload: dict[str, Any] = {
            "ok": True,
            "mutated": False,
            "operation": "show-plan",
            "research_topic_id": context.research_topic.id,
            "topic_workspace_id": context.topic_workspace_id,
            "checkpoint_id": plan.checkpoint_id,
            "plan_id": plan.id,
            "plan": plan.to_json(include_payload=include_payload, include_diagnostics=include_payload),
            "actions": [action.to_json() for action in actions],
            "blockers": [action.to_json() for action in actions if action.action == "blocked"],
        }
        if include_rendered_body:
            payload["rendered_body"] = _read_text_path(plan.rendered_markdown_path)
        return payload, diagnostics
    finally:
        store.close()


def apply_topic_reset(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    checkpoint_id: str,
    plan_id: str,
    actor_ref: str | None = None,
    yes: bool = False,
    render_markdown: bool = True,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """Apply an approved destructive reset plan."""

    store, diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    if store is None:
        return _runtime_missing_payload("apply", diagnostics), diagnostics
    try:
        started_at = utc_timestamp()
        if not yes:
            diagnostics.append(
                Diagnostic(
                    code="ISO224",
                    severity="error",
                    concept="Topic Reset Apply",
                    field="yes",
                    message="Reset apply requires explicit --yes confirmation.",
                )
            )
            return _diagnostic_payload("apply", diagnostics), diagnostics
        checkpoint = store.get_reset_checkpoint(checkpoint_id)
        plan = store.get_reset_plan(plan_id)
        if checkpoint is None or not _checkpoint_belongs_to_context(checkpoint, context):
            diagnostics.append(_missing_checkpoint_diagnostic(checkpoint_id))
        if plan is None or not _plan_belongs_to_context(plan, context):
            diagnostics.append(_missing_plan_diagnostic(plan_id))
        if checkpoint is None or plan is None or has_errors(diagnostics):
            return _diagnostic_payload("apply", diagnostics), diagnostics
        if plan.checkpoint_id != checkpoint.id:
            diagnostics.append(
                Diagnostic(
                    code="ISO224",
                    severity="error",
                    concept="Topic Reset Apply",
                    field="plan_id",
                    message="Selected reset plan does not belong to the selected checkpoint.",
                )
            )
        current_precondition_digest = digest_json(_runtime_precondition_payload(store, context))
        if checkpoint.checkpoint_digest != plan.checkpoint_digest or current_precondition_digest != plan.precondition_digest:
            diagnostics.append(
                Diagnostic(
                    code="ISO224",
                    severity="error",
                    concept="Topic Reset Apply",
                    field="plan_id",
                    message="Reset plan is stale; generate a new plan before applying.",
                )
            )
        actions = store.list_reset_plan_actions(plan_id=plan.id)
        if any(action.action == "blocked" for action in actions):
            diagnostics.append(
                Diagnostic(
                    code="ISO224",
                    severity="error",
                    concept="Topic Reset Apply",
                    field="plan_id",
                    message="Reset plan has blockers and cannot be applied.",
                )
            )
        diagnostics.extend(_forbidden_git_payload_diagnostics(plan.payload_json, concept="Topic Reset Plan", record_id=plan.id))
        if has_errors(diagnostics):
            return _diagnostic_payload("apply", diagnostics), diagnostics

        applied_actions: list[dict[str, object]] = []
        skipped_actions: list[dict[str, object]] = []
        failed_actions: list[dict[str, object]] = []
        for action in _apply_order(actions):
            if action.action in {"preserve", "skip", "regenerate"}:
                skipped_actions.append(action.to_json())
                continue
            action_diagnostics = _apply_one_action(context, store, action)
            if has_errors(action_diagnostics):
                diagnostics.extend(action_diagnostics)
                failed_actions.append({**action.to_json(), "diagnostics": [diagnostic.to_json() for diagnostic in action_diagnostics]})
            else:
                applied_actions.append(action.to_json())

        finished_at = utc_timestamp()
        status = "succeeded"
        if failed_actions and applied_actions:
            status = "partial"
        elif failed_actions:
            status = "failed"
        outcome_id = f"topic-reset-outcome-{_slug(plan.id)}-{uuid.uuid4().hex[:12]}"
        outcome_payload: dict[str, object] = {
            "title": "Topic Reset Outcome",
            "summary": "Outcome record for a destructive Topic Workspace reset.",
            "status": status,
            "research_topic_id": context.research_topic.id,
            "topic_workspace_id": context.topic_workspace_id,
            "checkpoint_id": checkpoint.id,
            "plan_id": plan.id,
            "outcome_id": outcome_id,
            "applied_actions": applied_actions,
            "skipped_actions": skipped_actions,
            "failed_actions": failed_actions,
            "diagnostics": [diagnostic.to_json() for diagnostic in diagnostics],
            "started_at": started_at,
            "finished_at": finished_at,
            "actor_ref": actor_ref,
            "no_git_operations": True,
        }
        render_path, render_digest, render_diagnostics = _render_reset_markdown(
            context,
            store,
            outcome_payload,
            profile_ref=OUTCOME_PROFILE_REF,
            content_name=f"{outcome_id}.md",
            env=env,
            enabled=render_markdown,
        )
        diagnostics.extend(render_diagnostics)
        outcome = ResetOutcomeRecord(
            id=outcome_id,
            checkpoint_id=checkpoint.id,
            plan_id=plan.id,
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            status=status,
            payload_json=outcome_payload,
            payload_digest=digest_json(outcome_payload),
            applied_actions=applied_actions,
            skipped_actions=skipped_actions,
            failed_actions=failed_actions,
            diagnostics=[diagnostic.to_json() for diagnostic in diagnostics],
            actor_ref=actor_ref,
            started_at=started_at,
            finished_at=finished_at,
            rendered_markdown_path=str(render_path) if render_path is not None else None,
            rendered_markdown_digest=render_digest,
            provenance_refs=[_provenance_ref("topic-reset-outcome", outcome_id)],
        )
        with store.connection:
            store.upsert_reset_outcome(outcome)
            _write_reset_structured_record(
                context,
                store,
                record_id=outcome_id,
                record_kind="provenance_record",
                status="ready" if status == "succeeded" else "failed",
                profile_ref=OUTCOME_PROFILE_REF,
                payload=outcome_payload,
                rendered_markdown_path=render_path,
                rendered_markdown_digest=render_digest,
                created_at=started_at,
                updated_at=finished_at,
                actor_ref=actor_ref,
                reset_kind="outcome",
            )
            store.upsert_reset_plan(replace(plan, status="applied" if status == "succeeded" else "failed", updated_at=finished_at))
        return {
            "ok": status == "succeeded" and not has_errors(diagnostics),
            "mutated": True,
            "operation": "apply",
            "research_topic_id": context.research_topic.id,
            "topic_workspace_id": context.topic_workspace_id,
            "checkpoint_id": checkpoint.id,
            "plan_id": plan.id,
            "outcome_id": outcome.id,
            "outcome": outcome.to_json(),
            "rendered_markdown_path": outcome.rendered_markdown_path,
        }, diagnostics
    finally:
        store.close()


def _checkpoint_payload(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    *,
    checkpoint_id: str,
    actor_ref: str | None,
    created_at: str,
    semantic_inventory: list[dict[str, object]],
) -> dict[str, object]:
    lifecycle_records = [
        record for record in store.list_lifecycle_records() if _record_belongs_to_context(record, context)
    ]
    structured_payloads = [
        payload for payload in store.list_structured_payloads(topic_workspace_id=context.topic_workspace_id)
        if payload.research_topic_id == context.research_topic.id
    ]
    artifact_registrations = [
        record for record in store.list_artifact_format_registrations(topic_workspace_id=context.topic_workspace_id)
        if record.research_topic_id == context.research_topic.id
    ]
    readiness_records = [
        record for record in store.list_readiness_records()
        if record.research_topic_id == context.research_topic.id and record.topic_workspace_id == context.topic_workspace_id
    ]
    summary_paths = [
        str(item["path"])
        for item in semantic_inventory
        if item.get("semantic_label") == "topic.workspace.summary" and item.get("path") is not None
    ]
    preserved_record_ids = sorted({record.id for record in lifecycle_records} | {checkpoint_id})
    preserved_structured_ids = sorted({payload.record_id for payload in structured_payloads} | {checkpoint_id})
    preserved_view_paths = sorted(
        {
            path
            for path in (payload.rendered_markdown_path for payload in structured_payloads)
            if path is not None
        }
    )
    return {
        "title": "Topic Reset Checkpoint",
        "summary": "Post-initialization/pre-research Topic Workspace reset checkpoint.",
        "status": "ready",
        "research_topic_id": context.research_topic.id,
        "topic_workspace_id": context.topic_workspace_id,
        "checkpoint_id": checkpoint_id,
        "actor_ref": actor_ref,
        "created_at": created_at,
        "workspace_runtime_schema_version": store.metadata().schema_version,
        "source_readiness_evidence": _latest_readiness_json(store),
        "topic_workspace_summary_ref": summary_paths[0] if summary_paths else None,
        "summary_paths": summary_paths,
        "semantic_path_inventory": semantic_inventory,
        "preserved_record_ids": preserved_record_ids,
        "preserved_structured_payload_ids": preserved_structured_ids,
        "preserved_generated_view_paths": preserved_view_paths,
        "preserved_artifact_format_registration_ids": sorted(record.id for record in artifact_registrations),
        "preserved_readiness_record_ids": sorted(record.id for record in readiness_records),
        "preserved_semantic_labels": sorted({str(item.get("semantic_label")) for item in semantic_inventory if item.get("semantic_label")}),
        "runtime_high_watermarks": _runtime_high_watermarks(
            lifecycle_records=lifecycle_records,
            structured_payloads=structured_payloads,
            artifact_registrations=artifact_registrations,
            readiness_records=readiness_records,
        ),
        "blockers": [],
        "extensions": [],
        "no_git_operations": True,
    }


def _semantic_path_inventory(context: EffectiveTopicContext, env: Mapping[str, str]) -> tuple[list[dict[str, object]], list[Diagnostic]]:
    entries, diagnostics = preview_paths(context, env=env)
    required_labels = {"topic.runtime.db", "topic.records.artifacts", "topic.records.views", "topic.workspace.summary"}
    inventory = []
    observed_labels = set()
    for entry in entries:
        payload = entry.to_json()
        inventory.append(payload)
        label = payload.get("semantic_label")
        if isinstance(label, str):
            observed_labels.add(label)
    for label in sorted(required_labels - observed_labels):
        result, label_diagnostics = resolve_semantic_path(context, label, env=env, cwd=context.topic_workspace_path)
        diagnostics.extend(label_diagnostics)
        if result is not None:
            inventory.append(result.to_json())
            observed_labels.add(label)
    for label in sorted(required_labels - observed_labels):
        diagnostics.append(
            Diagnostic(
                code="ISO220",
                severity="error",
                concept="Topic Reset Checkpoint",
                field=label,
                message="Checkpoint creation requires this semantic label to resolve for the selected Topic Workspace.",
            )
        )
    return inventory, diagnostics


def _runtime_high_watermarks(
    *,
    lifecycle_records: list[RuntimeLifecycleRecord],
    structured_payloads: list[StructuredResearchPayloadRecord],
    artifact_registrations: list[ArtifactFormatRegistrationRecord],
    readiness_records: list[TopicEnvironmentReadinessRecord],
) -> dict[str, object]:
    return {
        "lifecycle_records": _max_timestamp(record.updated_at for record in lifecycle_records),
        "structured_research_payloads": _max_timestamp(record.updated_at for record in structured_payloads),
        "artifact_format_registrations": _max_timestamp(record.updated_at for record in artifact_registrations),
        "readiness_records": _max_timestamp(record.checked_at for record in readiness_records),
    }


def _max_timestamp(values: Any) -> str | None:
    selected = sorted(str(value) for value in values if value is not None)
    return selected[-1] if selected else None


def _latest_readiness_json(store: WorkspaceRuntimeStore) -> dict[str, object] | None:
    readiness = store.latest_readiness()
    return readiness.to_json() if readiness is not None else None


def _build_reset_actions(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    checkpoint: ResetCheckpointRecord,
    *,
    plan_id: str,
) -> tuple[list[ResetPlanActionRecord], list[Diagnostic]]:
    now = utc_timestamp()
    diagnostics: list[Diagnostic] = []
    actions: list[ResetPlanActionRecord] = []
    preserved_record_ids = set(_payload_string_list(checkpoint.payload_json, "preserved_record_ids"))
    preserved_structured_ids = set(_payload_string_list(checkpoint.payload_json, "preserved_structured_payload_ids"))
    preserved_view_paths = {canonicalize(Path(path)) for path in _payload_string_list(checkpoint.payload_json, "preserved_generated_view_paths")}
    preserved_support_paths = {canonicalize(Path(path)) for path in _payload_string_list(checkpoint.payload_json, "preserved_support_paths")}
    preserved_artifact_ids = set(_payload_string_list(checkpoint.payload_json, "preserved_artifact_format_registration_ids"))
    preserved_readiness_ids = set(_payload_string_list(checkpoint.payload_json, "preserved_readiness_record_ids"))

    for record in store.list_lifecycle_records():
        if not _record_belongs_to_context(record, context):
            actions.append(_blocked_action(plan_id, now, "cross_topic_record", record.id, "Cross-topic lifecycle record encountered."))
            continue
        if _is_reset_lifecycle_record(record) or record.id in preserved_record_ids:
            actions.append(_preserve_action(plan_id, now, "lifecycle_record", record.id))
            continue
        actions.append(
            _record_action(
                plan_id,
                now,
                action="delete_record",
                target_kind="lifecycle_record",
                target_ref=record.id,
                details={"record_kind": record.record_kind, "created_at": record.created_at},
            )
        )
        if record.content_path is not None:
            _append_path_delete_action(
                actions,
                plan_id,
                now,
                context,
                Path(record.content_path),
                action="delete_file",
                target_kind="record_content_path",
                target_ref=record.id,
                semantic_label=str(record.transition_metadata.get("semantic_label") or record.transition_metadata.get("content_semantic_label") or ""),
                preserved_paths=preserved_view_paths | preserved_support_paths,
            )

    for payload in store.list_structured_payloads(topic_workspace_id=context.topic_workspace_id):
        if payload.record_id in preserved_structured_ids or payload.record_id in preserved_record_ids:
            actions.append(_preserve_action(plan_id, now, "structured_payload", payload.record_id))
            continue
        if payload.rendered_markdown_path is not None:
            _append_path_delete_action(
                actions,
                plan_id,
                now,
                context,
                Path(payload.rendered_markdown_path),
                action="delete_generated_view",
                target_kind="generated_markdown_view",
                target_ref=payload.record_id,
                semantic_label="topic.records.views",
                preserved_paths=preserved_view_paths | preserved_support_paths,
            )
        actions.append(
            _record_action(
                plan_id,
                now,
                action="delete_record",
                target_kind="structured_payload",
                target_ref=payload.record_id,
                details={"created_at": payload.created_at, "format_profile_ref": payload.format_profile_ref},
            )
        )

    for registration in store.list_artifact_format_registrations(topic_workspace_id=context.topic_workspace_id):
        if registration.id in preserved_artifact_ids:
            actions.append(_preserve_action(plan_id, now, "artifact_format_registration", registration.id))
        else:
            actions.append(
                _record_action(
                    plan_id,
                    now,
                    action="delete_record",
                    target_kind="artifact_format_registration",
                    target_ref=registration.id,
                    details={"format_profile_ref": registration.format_profile_ref, "created_at": registration.created_at},
                )
            )

    for readiness in store.list_readiness_records():
        if readiness.research_topic_id != context.research_topic.id or readiness.topic_workspace_id != context.topic_workspace_id:
            actions.append(_blocked_action(plan_id, now, "cross_topic_readiness", readiness.id, "Cross-topic readiness record encountered."))
        elif readiness.id in preserved_readiness_ids:
            actions.append(_preserve_action(plan_id, now, "readiness_record", readiness.id))
        else:
            actions.append(
                _record_action(
                    plan_id,
                    now,
                    action="delete_record",
                    target_kind="readiness_record",
                    target_ref=readiness.id,
                    details={"checked_at": readiness.checked_at, "status": readiness.status},
                )
            )

    actions.extend(_managed_workspace_delete_actions(context, store, plan_id=plan_id, created_at=now, preserved_paths=preserved_support_paths | preserved_view_paths))
    actions.extend(_preflight_blocker_actions(context, store, plan_id=plan_id, created_at=now))
    diagnostics.extend(_forbidden_git_payload_diagnostics([action.to_json() for action in actions], concept="Topic Reset Plan", record_id=plan_id))
    return _dedupe_actions(actions), diagnostics


def _record_action(
    plan_id: str,
    created_at: str,
    *,
    action: str,
    target_kind: str,
    target_ref: str | None = None,
    target_path: Path | None = None,
    semantic_label: str | None = None,
    source_kind: str | None = None,
    details: dict[str, object] | None = None,
) -> ResetPlanActionRecord:
    target = target_ref or str(target_path) if target_path is not None else target_kind
    return ResetPlanActionRecord(
        id=f"{plan_id}-{action}-{target_kind}-{_slug(str(target))}",
        plan_id=plan_id,
        action=action,
        target_kind=target_kind,
        target_ref=target_ref,
        target_path=str(target_path) if target_path is not None else None,
        semantic_label=semantic_label or None,
        source_kind=source_kind,
        status="planned",
        details=details or {},
        created_at=created_at,
    )


def _preserve_action(plan_id: str, created_at: str, target_kind: str, target_ref: str) -> ResetPlanActionRecord:
    return _record_action(plan_id, created_at, action="preserve", target_kind=target_kind, target_ref=target_ref)


def _blocked_action(plan_id: str, created_at: str, target_kind: str, target_ref: str, message: str) -> ResetPlanActionRecord:
    return _record_action(
        plan_id,
        created_at,
        action="blocked",
        target_kind=target_kind,
        target_ref=target_ref,
        details={"message": message},
    )


def _append_path_delete_action(
    actions: list[ResetPlanActionRecord],
    plan_id: str,
    created_at: str,
    context: EffectiveTopicContext,
    path: Path,
    *,
    action: str,
    target_kind: str,
    target_ref: str,
    semantic_label: str,
    preserved_paths: set[Path],
) -> None:
    candidate = canonicalize(path)
    if candidate in preserved_paths:
        actions.append(_record_action(plan_id, created_at, action="preserve", target_kind=target_kind, target_ref=target_ref, target_path=candidate, semantic_label=semantic_label))
        return
    if not _path_is_safe_for_topic(context, candidate):
        actions.append(_blocked_action(plan_id, created_at, "unsafe_path", str(candidate), "Reset action path is outside the selected Topic Workspace."))
        return
    if not candidate.exists():
        actions.append(_record_action(plan_id, created_at, action="skip", target_kind=target_kind, target_ref=target_ref, target_path=candidate, semantic_label=semantic_label, details={"reason": "path_missing"}))
        return
    actions.append(
        _record_action(
            plan_id,
            created_at,
            action=action,
            target_kind=target_kind,
            target_ref=target_ref,
            target_path=candidate,
            semantic_label=semantic_label,
            source_kind="semantic_label",
        )
    )


def _managed_workspace_delete_actions(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    *,
    plan_id: str,
    created_at: str,
    preserved_paths: set[Path],
) -> list[ResetPlanActionRecord]:
    actions: list[ResetPlanActionRecord] = []
    roots = [
        plan
        for plan in store.list_path_plans()
        if plan.topic_workspace_id == context.topic_workspace_id and plan.semantic_label in MANAGED_WORKSPACE_LABELS
    ]
    for root_plan in roots:
        root = canonicalize(Path(root_plan.path))
        if not root.exists():
            actions.append(_record_action(plan_id, created_at, action="skip", target_kind="managed_workspace_root", target_path=root, semantic_label=root_plan.semantic_label, details={"reason": "root_missing"}))
            continue
        if not _path_is_safe_for_topic(context, root):
            actions.append(_blocked_action(plan_id, created_at, "managed_workspace_root", str(root), "Managed actor or agent workspace root is outside the selected Topic Workspace."))
            continue
        for child in sorted(root.rglob("*"), key=lambda item: len(item.parts), reverse=True):
            candidate = canonicalize(child)
            if candidate in preserved_paths or candidate == root:
                continue
            if child.is_symlink():
                actions.append(_blocked_action(plan_id, created_at, "managed_root_traversal_hazard", str(candidate), "Managed workspace contains a symlink; reset refuses traversal hazards."))
                continue
            if _looks_secret_like(candidate):
                actions.append(_blocked_action(plan_id, created_at, "possible_secret_material", str(candidate), "Managed workspace contains possible secret material."))
                continue
            actions.append(
                _record_action(
                    plan_id,
                    created_at,
                    action="delete_file",
                    target_kind="managed_workspace_path",
                    target_path=candidate,
                    semantic_label=root_plan.semantic_label,
                    source_kind="managed_workspace_root",
                    details={"root": str(root), "path_plan_id": root_plan.id},
                )
            )
    return actions


def _preflight_blocker_actions(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    *,
    plan_id: str,
    created_at: str,
) -> list[ResetPlanActionRecord]:
    actions: list[ResetPlanActionRecord] = []
    for team in store.list_agent_team_instances():
        if team.research_topic_id == context.research_topic.id and team.topic_workspace_id == context.topic_workspace_id and team.status in {"running", "ready", "blocked"}:
            actions.append(_blocked_action(plan_id, created_at, "agent_team_instance", team.id, "Agent Team Instance must be stopped or cleared before reset apply."))
    for handoff in store.list_handoffs():
        if handoff.research_topic_id == context.research_topic.id and handoff.topic_workspace_id == context.topic_workspace_id and handoff.status in OPEN_HANDOFF_STATUSES:
            actions.append(_blocked_action(plan_id, created_at, "handoff", handoff.id, "Open handoff blocks reset apply."))
    for attempt in store.list_adapter_launch_attempts():
        if attempt.research_topic_id == context.research_topic.id and attempt.topic_workspace_id == context.topic_workspace_id and attempt.status in LIVE_ADAPTER_STATUSES:
            actions.append(_blocked_action(plan_id, created_at, "adapter_launch_attempt", attempt.id, "Live adapter launch state blocks reset apply."))
    return actions


def _dedupe_actions(actions: list[ResetPlanActionRecord]) -> list[ResetPlanActionRecord]:
    by_key: dict[tuple[str, str, str | None, str | None], ResetPlanActionRecord] = {}
    for action in actions:
        key = (action.action, action.target_kind, action.target_ref, action.target_path)
        if key not in by_key:
            by_key[key] = action
    return list(by_key.values())


def _runtime_precondition_payload(store: WorkspaceRuntimeStore, context: EffectiveTopicContext) -> dict[str, object]:
    lifecycle_records = [
        record.to_json()
        for record in store.list_lifecycle_records()
        if _record_belongs_to_context(record, context) and not _is_reset_lifecycle_record(record)
    ]
    structured_payloads = [
        payload.to_summary_json()
        for payload in store.list_structured_payloads(topic_workspace_id=context.topic_workspace_id)
        if payload.research_topic_id == context.research_topic.id and not _is_reset_record_id(payload.record_id)
    ]
    return {
        "metadata": store.metadata().to_json(),
        "path_plans": [record.to_json() for record in store.list_path_plans() if record.topic_workspace_id == context.topic_workspace_id],
        "lifecycle_records": lifecycle_records,
        "structured_payloads": structured_payloads,
        "artifact_format_registrations": [
            record.to_json()
            for record in store.list_artifact_format_registrations(topic_workspace_id=context.topic_workspace_id)
            if record.research_topic_id == context.research_topic.id
        ],
        "readiness_records": [
            record.to_json()
            for record in store.list_readiness_records()
            if record.research_topic_id == context.research_topic.id and record.topic_workspace_id == context.topic_workspace_id
        ],
        "agent_team_instances": [
            record.to_json()
            for record in store.list_agent_team_instances()
            if record.research_topic_id == context.research_topic.id and record.topic_workspace_id == context.topic_workspace_id
        ],
        "agent_instances": [
            record.to_json()
            for record in store.list_agent_instances()
            if record.research_topic_id == context.research_topic.id and record.topic_workspace_id == context.topic_workspace_id
        ],
        "agent_workspaces": [
            record.to_json()
            for record in store.list_agent_workspaces()
            if record.topic_workspace_id == context.topic_workspace_id
        ],
        "handoffs": [
            record.to_json()
            for record in store.list_handoffs()
            if record.research_topic_id == context.research_topic.id and record.topic_workspace_id == context.topic_workspace_id
        ],
    }


def _apply_order(actions: list[ResetPlanActionRecord]) -> list[ResetPlanActionRecord]:
    priority = {
        "delete_generated_view": 0,
        "delete_file": 1,
        "delete_record:structured_payload": 2,
        "delete_record:lifecycle_record": 3,
        "delete_record": 4,
    }

    def sort_key(action: ResetPlanActionRecord) -> tuple[int, int, str]:
        key = f"{action.action}:{action.target_kind}"
        return (priority.get(key, priority.get(action.action, 99)), -(len(Path(action.target_path).parts) if action.target_path else 0), action.id)

    return sorted(actions, key=sort_key)


def _apply_one_action(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    action: ResetPlanActionRecord,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if action.action in {"delete_file", "delete_generated_view"}:
        if action.target_path is None:
            return [
                Diagnostic(
                    code="ISO225",
                    severity="error",
                    concept="Topic Reset Apply",
                    field=action.id,
                    message="Delete file action has no target path.",
                )
            ]
        diagnostics.extend(_delete_path(context, Path(action.target_path), action_id=action.id))
        return diagnostics
    if action.action != "delete_record":
        return diagnostics
    try:
        if action.target_kind == "structured_payload" and action.target_ref is not None:
            store.delete_structured_payload(action.target_ref)
        elif action.target_kind == "lifecycle_record" and action.target_ref is not None:
            store.delete_lifecycle_record(action.target_ref)
        elif action.target_kind == "artifact_format_registration" and action.target_ref is not None:
            store.delete_artifact_format_registration(action.target_ref)
        elif action.target_kind == "readiness_record" and action.target_ref is not None:
            store.delete_readiness_record(action.target_ref)
        else:
            diagnostics.append(
                Diagnostic(
                    code="ISO225",
                    severity="error",
                    concept="Topic Reset Apply",
                    field=action.id,
                    message=f"Unsupported reset record deletion target: {action.target_kind}.",
                )
            )
    except OSError as exc:
        diagnostics.append(
            Diagnostic(
                code="ISO225",
                severity="error",
                concept="Topic Reset Apply",
                field=action.id,
                message=f"Reset record deletion failed: {exc}.",
            )
        )
    return diagnostics


def _delete_path(context: EffectiveTopicContext, path: Path, *, action_id: str) -> list[Diagnostic]:
    candidate = canonicalize(path)
    if not _path_is_safe_for_topic(context, candidate):
        return [
            Diagnostic(
                code="ISO225",
                severity="error",
                concept="Topic Reset Apply",
                path=candidate,
                field=action_id,
                message="Reset apply refuses to delete a path outside the selected Topic Workspace.",
            )
        ]
    if not candidate.exists():
        return []
    try:
        if candidate.is_symlink():
            return [
                Diagnostic(
                    code="ISO225",
                    severity="error",
                    concept="Topic Reset Apply",
                    path=candidate,
                    field=action_id,
                    message="Reset apply refuses to delete symlink traversal hazards.",
                )
            ]
        if candidate.is_dir():
            shutil.rmtree(candidate)
        else:
            candidate.unlink()
    except OSError as exc:
        return [
            Diagnostic(
                code="ISO225",
                severity="error",
                concept="Topic Reset Apply",
                path=candidate,
                field=action_id,
                message=f"Reset file deletion failed: {exc}.",
            )
        ]
    return []


def _write_reset_structured_record(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    *,
    record_id: str,
    record_kind: str,
    status: str,
    profile_ref: str,
    payload: dict[str, object],
    rendered_markdown_path: Path | None,
    rendered_markdown_digest: str | None,
    created_at: str,
    updated_at: str,
    actor_ref: str | None,
    reset_kind: str,
) -> None:
    registry = _artifact_format_registry(context, store)
    validation = validate_payload(payload, registry=registry, format_profile_ref=profile_ref)
    render_status = "rendered" if rendered_markdown_path is not None else "not_requested"
    lifecycle_record = RuntimeLifecycleRecord(
        id=record_id,
        record_kind=record_kind,
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        status=status,
        created_at=created_at,
        updated_at=updated_at,
        lifecycle_refs={"reset_record_id": record_id, "reset_kind": reset_kind},
        transition_metadata={
            "reset_kind": reset_kind,
            "format_profile_ref": profile_ref,
            "payload_digest": validation.payload_digest,
            "render_status": render_status,
            "actor_ref": actor_ref,
            "created_by": "isomer-cli project topic-reset",
            "semantic_label": RESET_RECORD_LABEL,
        },
        content_path=str(rendered_markdown_path) if rendered_markdown_path is not None else None,
        provenance_refs=[_provenance_ref(f"topic-reset-{reset_kind}", record_id)],
    )
    structured_payload = StructuredResearchPayloadRecord(
        id=f"structured-payload-{_slug(record_id)}",
        record_id=record_id,
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        format_profile_ref=validation.profile_ref or profile_ref,
        schema_ref=str(validation.schema_ref or ""),
        schema_version=validation.schema_version,
        schema_source_kind=str(validation.schema_source_kind or "provider_asset"),
        template_ref=_template_ref_for_profile(profile_ref),
        template_source_kind="provider_asset" if rendered_markdown_path is not None else None,
        payload_json=payload,
        payload_digest=validation.payload_digest,
        validation_status=validation.status,
        validation_diagnostics=[diagnostic.to_json() for diagnostic in validation.diagnostics],
        render_status=render_status,
        render_diagnostics=[],
        rendered_markdown_path=str(rendered_markdown_path) if rendered_markdown_path is not None else None,
        rendered_markdown_digest=rendered_markdown_digest,
        created_at=created_at,
        updated_at=updated_at,
        provenance_refs=[_provenance_ref("structured-payload", record_id)],
    )
    store.upsert_lifecycle_record(lifecycle_record)
    store.upsert_structured_payload(structured_payload)


def _render_reset_markdown(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    payload: dict[str, object],
    *,
    profile_ref: str,
    content_name: str,
    env: Mapping[str, str],
    enabled: bool,
) -> tuple[Path | None, str | None, list[Diagnostic]]:
    if not enabled:
        return None, None, []
    registry = _artifact_format_registry(context, store)
    render = render_artifact(payload, registry=registry, output_format="markdown", format_profile_ref=profile_ref)
    diagnostics = list(render.diagnostics)
    if not render.ok or render.content is None:
        return None, None, diagnostics
    result, path_diagnostics = resolve_semantic_path(context, RESET_RECORD_LABEL, env=env, cwd=context.topic_workspace_path)
    diagnostics.extend(path_diagnostics)
    if result is None:
        return None, None, diagnostics
    target_dir = result.path / RESET_RECORD_DIRNAME
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / content_name
    target.write_text(render.content, encoding="utf-8")
    return target.resolve(strict=False), digest_bytes(target.read_bytes()), diagnostics


def _artifact_format_registry(context: EffectiveTopicContext, store: WorkspaceRuntimeStore) -> ArtifactFormatRegistry:
    registry = ArtifactFormatRegistry()
    register_deepsci_record_format_provider(registry)
    registry.register_provider(WorkspaceRuntimeArtifactFormatProvider(store, topic_workspace_id=context.topic_workspace_id))
    return registry


def _template_ref_for_profile(profile_ref: str) -> str:
    if profile_ref == CHECKPOINT_PROFILE_REF:
        return "isomer:deepsci/record-format/template/markdown/control/topic-reset-checkpoint/v1"
    if profile_ref == PLAN_PROFILE_REF:
        return "isomer:deepsci/record-format/template/markdown/control/topic-reset-plan/v1"
    return "isomer:deepsci/record-format/template/markdown/report/topic-reset-outcome/v1"


def _record_belongs_to_context(record: RuntimeLifecycleRecord, context: EffectiveTopicContext) -> bool:
    return record.research_topic_id == context.research_topic.id and record.topic_workspace_id == context.topic_workspace_id


def _checkpoint_belongs_to_context(record: ResetCheckpointRecord, context: EffectiveTopicContext) -> bool:
    return record.research_topic_id == context.research_topic.id and record.topic_workspace_id == context.topic_workspace_id


def _plan_belongs_to_context(record: ResetPlanRecord, context: EffectiveTopicContext) -> bool:
    return record.research_topic_id == context.research_topic.id and record.topic_workspace_id == context.topic_workspace_id


def _is_reset_lifecycle_record(record: RuntimeLifecycleRecord) -> bool:
    return _is_reset_record_id(record.id) or "reset_kind" in record.transition_metadata


def _is_reset_record_id(record_id: str) -> bool:
    return record_id.startswith("topic-reset-")


def _payload_string_list(payload: dict[str, object], field: str) -> list[str]:
    value = payload.get(field)
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, str)]


def _merge_payload_list(payload: dict[str, object], field: str, values: list[str]) -> None:
    existing = _payload_string_list(payload, field)
    payload[field] = sorted(dict.fromkeys([*existing, *values]))


def _path_is_safe_for_topic(context: EffectiveTopicContext, path: Path) -> bool:
    root = canonicalize(context.topic_workspace_path)
    return canonicalize(path) == root or is_within(canonicalize(path), root)


def _looks_secret_like(path: Path) -> bool:
    name = path.name.lower()
    return any(fragment in name for fragment in SECRET_NAME_FRAGMENTS)


def _read_text_path(path: str | None) -> str | None:
    if path is None:
        return None
    selected = Path(path)
    if not selected.exists() or not selected.is_file():
        return None
    return selected.read_text(encoding="utf-8", errors="replace")


def _runtime_missing_payload(operation: str, diagnostics: list[Diagnostic]) -> dict[str, Any]:
    return {
        "ok": False,
        "mutated": False,
        "operation": operation,
        "error": {
            "code": "workspace_runtime_missing",
            "message": "Workspace Runtime must be initialized before topic reset records can be stored.",
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
            "message": "Topic reset operation failed preflight diagnostics.",
        },
        "diagnostics": [diagnostic.to_json() for diagnostic in diagnostics],
    }


def _missing_checkpoint_diagnostic(checkpoint_id: str) -> Diagnostic:
    return Diagnostic(
        code="ISO220",
        severity="error",
        concept="Topic Reset Checkpoint",
        field="checkpoint_id",
        message=f"Reset checkpoint not found for selected Topic Workspace: {checkpoint_id}.",
    )


def _missing_plan_diagnostic(plan_id: str) -> Diagnostic:
    return Diagnostic(
        code="ISO221",
        severity="error",
        concept="Topic Reset Plan",
        field="plan_id",
        message=f"Reset plan not found for selected Topic Workspace: {plan_id}.",
    )


def _forbidden_git_payload_diagnostics(
    payload: object,
    *,
    concept: str,
    record_id: str,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for field_path, value in _walk_payload(payload):
        key = field_path[-1] if field_path else ""
        key_text = str(key).lower().replace("-", "_")
        value_text = str(value)
        if key_text == "no_git_operations":
            continue
        if key_text in _FORBIDDEN_GIT_FIELDS or any(fragment in key_text for fragment in _FORBIDDEN_GIT_KEY_FRAGMENTS):
            diagnostics.append(
                Diagnostic(
                    code="ISO223",
                    severity="error",
                    concept=concept,
                    field=f"{record_id}.{'.'.join(str(part) for part in field_path)}",
                    message="Reset payload contains forbidden Git operation metadata.",
                )
            )
        elif isinstance(value, str) and _GIT_COMMAND_RE.search(value_text):
            diagnostics.append(
                Diagnostic(
                    code="ISO223",
                    severity="error",
                    concept=concept,
                    field=f"{record_id}.{'.'.join(str(part) for part in field_path)}",
                    message="Reset payload contains a command string that invokes Git.",
                )
            )
    return diagnostics


def _walk_payload(payload: object, prefix: tuple[object, ...] = ()) -> list[tuple[tuple[object, ...], object]]:
    if isinstance(payload, dict):
        items: list[tuple[tuple[object, ...], object]] = []
        for key, value in payload.items():
            items.extend(_walk_payload(value, (*prefix, key)))
        return items
    if isinstance(payload, list):
        items = []
        for index, value in enumerate(payload):
            items.extend(_walk_payload(value, (*prefix, index)))
        return items
    return [(prefix, payload)]


_FORBIDDEN_GIT_FIELDS = {
    "git_stash_id",
    "git_ref",
    "git_branch",
    "git_tag",
    "git_commit",
    "git_command",
    "git_operation",
    "project_root_git_tracking",
}
_FORBIDDEN_GIT_KEY_FRAGMENTS = ("git_stash", "git_ref", "git_branch", "git_commit", "git_command", "git_operation")
_GIT_COMMAND_RE = re.compile(r"(^|[;&|]\s*)git\s+[A-Za-z0-9_-]+")
