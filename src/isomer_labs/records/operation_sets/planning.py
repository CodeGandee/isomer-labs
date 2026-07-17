"""Whole-plan preflight and deterministic action planning."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence
import hashlib
import json

from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.records.idea_sources import SOURCE_STATUS_EXACT, resolve_payload_source_fragment
from isomer_labs.records.store import (
    RESEARCH_RECORD_DEFAULT_LABELS,
    ResearchRecordError,
    ResearchRecordRequest,
    _validate_record_kind,
    _validate_status,
    _validate_write_artifact_identity,
    validate_record_payload,
)
from isomer_labs.runtime.records import _slug
from isomer_labs.runtime.store import WorkspaceRuntimeStore, open_workspace_runtime
from isomer_labs.workspace.path_resolution import resolve_semantic_path

from .inventory import (
    _manifest_context_diagnostics,
    _reconcile_manifest,
    _require_manifest_control_path,
    inventory_operation_set,
    resolve_operation_set,
)
from .models import (
    OPERATION_SET_CONTROL_DIR,
    OperationSetAcceptanceManifest,
    OperationSetOutput,
    OperationSetRecordIntent,
    ResolvedOperationSet,
    _context_failure_payload,
    _has_item_errors,
    _item_diagnostic,
    _manifest_error,
    _normalize_digest,
    _optional_string,
    _output_summary,
    _reject_unknown_keys,
    canonical_json_digest,
    file_digest,
    load_operation_set_manifest,
)

@dataclass(frozen=True)
class PlannedRecordIntent:
    intent: OperationSetRecordIntent
    record_id: str
    parents: tuple[dict[str, object], ...]
    outputs: tuple[OperationSetOutput, ...]
    managed_files: tuple[dict[str, object], ...]
    intent_digest: str
    replayed: bool = False

    def to_json(self) -> dict[str, object]:
        return {
            "intent_key": self.intent.key,
            "action": self.intent.action,
            "record_id": self.record_id,
            "intent_digest": self.intent_digest,
            "parents": list(self.parents),
            "outputs": [item.to_json() for item in self.outputs],
            "managed_files": list(self.managed_files),
            "research_idea_effects": self.intent.idea_effects,
            "replayed": self.replayed,
        }


def plan_operation_set_acceptance(
    context: EffectiveTopicContext,
    manifest_path: Path,
    *,
    env: Mapping[str, str],
    cwd: Path,
    agent_name: str | None = None,
    topic_actor_name: str | None = None,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    selected_manifest_path = manifest_path if manifest_path.is_absolute() else cwd / manifest_path
    selected_manifest_path = selected_manifest_path.resolve(strict=False)
    manifest = load_operation_set_manifest(selected_manifest_path)
    if selected_manifest_path.parent.name != OPERATION_SET_CONTROL_DIR:
        raise _manifest_error("operation_set_manifest_path_invalid", f"Manifest must be stored directly under {OPERATION_SET_CONTROL_DIR}.")
    operation_root = selected_manifest_path.parent.parent
    selected_agent = agent_name
    selected_actor = topic_actor_name
    if selected_agent is None and selected_actor is None:
        if manifest.worker_kind == "agent":
            selected_agent = manifest.worker_name
        else:
            selected_actor = manifest.worker_name
    resolved, diagnostics = resolve_operation_set(
        context,
        operation_root,
        env=env,
        cwd=cwd,
        agent_name=selected_agent,
        topic_actor_name=selected_actor,
    )
    if resolved is None:
        return _context_failure_payload("operation-sets.accept", diagnostics), diagnostics
    _require_manifest_control_path(selected_manifest_path, resolved.root)
    inventory, inventory_diagnostics = inventory_operation_set(resolved.root)
    plan_diagnostics: list[dict[str, object]] = [*inventory_diagnostics]
    plan_diagnostics.extend(_manifest_context_diagnostics(context, resolved, manifest))
    plan_diagnostics.extend(_reconcile_manifest(inventory, manifest, require_dispositions=True))
    plan_diagnostics.extend(_validate_acceptance_manifest(manifest))

    store, runtime_diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    diagnostics.extend(runtime_diagnostics)
    if store is None:
        return _context_failure_payload("operation-sets.accept", diagnostics), diagnostics
    try:
        receipt_id = _acceptance_id(manifest)
        existing_receipt = store.get_operation_set_acceptance_revision(
            topic_workspace_id=context.topic_workspace_id,
            operation_set_id=manifest.operation_set_id,
            revision=manifest.revision,
        )
        existing_items = {
            item.intent_key: item
            for item in store.list_operation_set_acceptance_items(existing_receipt.id)
        } if existing_receipt is not None else {}
        if existing_receipt is not None and existing_receipt.manifest_digest != manifest.digest:
            plan_diagnostics.append(
                _item_diagnostic(
                    "operation_set_acceptance_revision_conflict",
                    "This operation-set revision already has a receipt for a different manifest digest.",
                    receipt_id=existing_receipt.id,
                    existing_manifest_digest=existing_receipt.manifest_digest,
                    manifest_digest=manifest.digest,
                )
            )
        if manifest.supersedes_receipt_id is not None:
            prior = store.get_operation_set_acceptance(manifest.supersedes_receipt_id)
            if prior is None:
                plan_diagnostics.append(_item_diagnostic("operation_set_superseded_receipt_missing", "The declared superseded receipt does not exist.", receipt_id=manifest.supersedes_receipt_id))
            elif prior.operation_set_id != manifest.operation_set_id or prior.revision >= manifest.revision:
                plan_diagnostics.append(_item_diagnostic("operation_set_supersession_invalid", "Supersession must name an earlier receipt for the same operation set.", receipt_id=prior.id))
        elif manifest.revision > 1:
            plan_diagnostics.append(_item_diagnostic("operation_set_superseded_receipt_required", "Acceptance revisions after revision 1 must name supersedes_receipt_id."))

        expected_ids = {intent.key: _expected_record_id(manifest, intent) for intent in manifest.record_intents}
        ordered_intents, ordering_diagnostics = _ordered_intents(manifest)
        plan_diagnostics.extend(ordering_diagnostics)
        planned: list[PlannedRecordIntent] = []
        for intent in ordered_intents:
            intent_outputs = tuple(item for item in manifest.outputs if item.record_key == intent.key)
            target_record = (
                store.get_lifecycle_record(intent.target_record_id)
                if intent.target_record_id is not None
                else None
            )
            resolved_record_kind = intent.record_kind or (
                target_record.record_kind if target_record is not None else None
            )
            parents, parent_diagnostics = _expanded_parents(intent, expected_ids, store)
            plan_diagnostics.extend(parent_diagnostics)
            record_id = expected_ids[intent.key]
            managed_files, managed_diagnostics = _planned_managed_files(
                context,
                resolved,
                manifest,
                intent,
                intent_outputs,
                record_id=record_id,
                receipt_id=receipt_id,
                record_kind=resolved_record_kind,
                env=env,
                cwd=cwd,
            )
            plan_diagnostics.extend(managed_diagnostics)
            intent_digest = canonical_json_digest(
                {
                    "intent": intent.to_json(),
                    "record_id": record_id,
                    "parents": parents,
                    "outputs": [item.to_json() for item in intent_outputs],
                    "managed_files": managed_files,
                }
            )
            replayed = False
            current_item = existing_items.get(intent.key)
            existing_record = store.get_lifecycle_record(record_id)
            if current_item is not None and current_item.intent_digest != intent_digest:
                plan_diagnostics.append(_item_diagnostic("operation_set_item_digest_conflict", "Existing acceptance item has different input.", intent_key=intent.key))
            if intent.action in {"create", "revise"}:
                target_id = intent.target_record_id
                if intent.action == "revise" and (target_id is None or store.get_lifecycle_record(target_id) is None):
                    plan_diagnostics.append(_item_diagnostic("operation_set_revision_target_missing", "Revision intent target record does not exist.", intent_key=intent.key, target_record_id=target_id))
                if existing_record is not None:
                    metadata = existing_record.transition_metadata
                    if metadata.get("operation_set_acceptance_id") == receipt_id and metadata.get("operation_set_intent_digest") == intent_digest:
                        replayed = True
                    else:
                        plan_diagnostics.append(_item_diagnostic("operation_set_record_id_conflict", "Planned record id already exists outside this acceptance item.", intent_key=intent.key, record_id=record_id))
            else:
                target_id = intent.target_record_id
                if target_id is None:
                    plan_diagnostics.append(_item_diagnostic("operation_set_reference_target_missing", "Reference intent requires target_record_id.", intent_key=intent.key))
                else:
                    reference_diagnostics = _verify_reference_outputs(store, target_id, intent_outputs, resolved.root)
                    plan_diagnostics.extend(reference_diagnostics)
                    replayed = not _has_item_errors(reference_diagnostics)
            if intent.action in {"create", "revise"} and not replayed:
                request = _request_for_intent(
                    context,
                    resolved,
                    manifest,
                    intent,
                    intent_outputs,
                    record_id=record_id,
                    receipt_id=receipt_id,
                    intent_digest=intent_digest,
                    parents=parents,
                    managed_files=managed_files,
                    record_kind=resolved_record_kind,
                )
                plan_diagnostics.extend(_preflight_record_request(context, store, request, intent_outputs, resolved.root, env=env, cwd=cwd))
            planned.append(
                PlannedRecordIntent(
                    intent=intent,
                    record_id=record_id,
                    parents=tuple(parents),
                    outputs=intent_outputs,
                    managed_files=tuple(managed_files),
                    intent_digest=intent_digest,
                    replayed=replayed,
                )
            )
        output_summary = _output_summary(manifest)
        ok = not _has_item_errors(plan_diagnostics) and not has_errors(diagnostics)
        return {
            "ok": ok,
            "mutated": False,
            "operation": "operation-sets.accept",
            "mode": "preview",
            "manifest_path": str(selected_manifest_path),
            "manifest_digest": manifest.digest,
            "acceptance_id": receipt_id,
            "resolved": resolved.to_json(),
            "output_summary": output_summary,
            "actions": [item.to_json() for item in planned],
            "action_count": len(planned),
            "replay": bool(existing_receipt is not None and existing_receipt.manifest_digest == manifest.digest),
            "diagnostics": plan_diagnostics,
        }, diagnostics
    finally:
        store.close()


def _validate_acceptance_manifest(manifest: OperationSetAcceptanceManifest) -> list[dict[str, object]]:
    diagnostics: list[dict[str, object]] = []
    intent_keys = {intent.key for intent in manifest.record_intents}
    durable_outputs_by_intent = {
        key: [item for item in manifest.outputs if item.record_key == key and item.disposition in {"record_payload", "record_attachment"}]
        for key in intent_keys
    }
    for output in manifest.outputs:
        if output.disposition == "disposable" and output.record_key is not None:
            diagnostics.append(_item_diagnostic("operation_set_disposable_record_key_forbidden", "Disposable output must not name a record intent.", path=output.path))
    for intent in manifest.record_intents:
        if intent.action == "create" and intent.record_kind is None:
            diagnostics.append(_item_diagnostic("operation_set_record_kind_missing", "Create intent requires record_kind.", intent_key=intent.key))
        if intent.action in {"revise", "reference"} and intent.target_record_id is None:
            diagnostics.append(_item_diagnostic("operation_set_target_record_missing", f"{intent.action} intent requires target_record_id.", intent_key=intent.key))
        if intent.action == "create" and not intent.parents and intent.root_reason is None:
            diagnostics.append(_item_diagnostic("operation_set_root_reason_missing", "A root create intent without parents requires root_reason.", intent_key=intent.key))
        payloads = [item for item in durable_outputs_by_intent[intent.key] if item.disposition == "record_payload"]
        if len(payloads) > 1:
            diagnostics.append(_item_diagnostic("operation_set_record_payload_multiple", "A record intent can consume at most one record_payload output.", intent_key=intent.key))
        if not durable_outputs_by_intent[intent.key]:
            diagnostics.append(_item_diagnostic("operation_set_record_intent_unused", "Record intent is not referenced by any durable output.", intent_key=intent.key))
        if intent.idea_effects_required and intent.idea_effects is None:
            diagnostics.append(_item_diagnostic("operation_set_idea_effects_missing", "Intent requires explicit Research Idea effects.", intent_key=intent.key))
        if intent.idea_effects is not None:
            if intent.idea_effects.get("atomic") is not True:
                diagnostics.append(_item_diagnostic("operation_set_idea_effects_not_atomic", "Research Idea effects must declare atomic=true.", intent_key=intent.key))
            ideas = intent.idea_effects.get("ideas")
            if not isinstance(ideas, list) or not ideas:
                diagnostics.append(_item_diagnostic("operation_set_idea_effects_ideas_missing", "Research Idea effects require a non-empty ideas array.", intent_key=intent.key))
    return diagnostics


def _ordered_intents(
    manifest: OperationSetAcceptanceManifest,
) -> tuple[list[OperationSetRecordIntent], list[dict[str, object]]]:
    intent_by_key = {intent.key: intent for intent in manifest.record_intents}
    dependencies: dict[str, set[str]] = {key: set() for key in intent_by_key}
    diagnostics: list[dict[str, object]] = []
    for intent in manifest.record_intents:
        for index, parent in enumerate(intent.parents):
            _reject_unknown_keys(parent, {"record_id", "local_record_key", "lineage_kind", "kind", "parent_role", "role", "decision_record_id", "rationale", "status", "metadata"}, f"manifest.record_intents[{intent.key}].parents[{index}]")
            local_key = _optional_string(parent.get("local_record_key"))
            record_id = _optional_string(parent.get("record_id"))
            if (local_key is None) == (record_id is None):
                diagnostics.append(_item_diagnostic("operation_set_parent_ref_invalid", "Each parent must name exactly one record_id or local_record_key.", intent_key=intent.key, parent_index=index))
            elif local_key is not None:
                if local_key not in intent_by_key:
                    diagnostics.append(_item_diagnostic("operation_set_local_parent_unknown", "Local parent key does not exist.", intent_key=intent.key, local_record_key=local_key))
                elif local_key == intent.key:
                    diagnostics.append(_item_diagnostic("operation_set_local_parent_self", "Record intent cannot be its own parent.", intent_key=intent.key))
                else:
                    dependencies[intent.key].add(local_key)
    ordered: list[OperationSetRecordIntent] = []
    remaining = {key: set(values) for key, values in dependencies.items()}
    while remaining:
        ready = sorted(key for key, values in remaining.items() if not values)
        if not ready:
            diagnostics.append(_item_diagnostic("operation_set_local_dependency_cycle", "Record intent local-parent dependencies contain a cycle.", intent_keys=sorted(remaining)))
            ordered.extend(intent_by_key[key] for key in sorted(remaining))
            break
        for key in ready:
            ordered.append(intent_by_key[key])
            remaining.pop(key)
            for values in remaining.values():
                values.discard(key)
    return ordered, diagnostics


def _expanded_parents(
    intent: OperationSetRecordIntent,
    expected_ids: Mapping[str, str],
    store: WorkspaceRuntimeStore,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    parents: list[dict[str, object]] = []
    diagnostics: list[dict[str, object]] = []
    if intent.action == "revise":
        target_record_id = intent.target_record_id
        if target_record_id is None:
            return [], diagnostics
        if intent.parents:
            if len(intent.parents) != 1:
                diagnostics.append(
                    _item_diagnostic(
                        "operation_set_revision_parent_invalid",
                        "Revision intent can declare only its target as the immediate revision parent.",
                        intent_key=intent.key,
                    )
                )
            else:
                authored_parent = intent.parents[0]
                authored_record_id = _optional_string(authored_parent.get("record_id"))
                authored_local_key = _optional_string(authored_parent.get("local_record_key"))
                authored_kind = _optional_string(authored_parent.get("lineage_kind") or authored_parent.get("kind"))
                if authored_local_key is not None or authored_record_id != target_record_id or authored_kind not in {None, "revision_of"}:
                    diagnostics.append(
                        _item_diagnostic(
                            "operation_set_revision_parent_invalid",
                            "Revision intent parent must be the target record with revision_of lineage.",
                            intent_key=intent.key,
                            target_record_id=target_record_id,
                        )
                    )
        return [
            {
                "record_id": target_record_id,
                "lineage_kind": "revision_of",
                "parent_role": "previous_revision",
            }
        ], diagnostics
    for index, value in enumerate(intent.parents):
        parent = dict(value)
        local_key = _optional_string(parent.pop("local_record_key", None))
        if local_key is not None:
            parent["record_id"] = expected_ids.get(local_key)
        record_id = _optional_string(parent.get("record_id"))
        if record_id is None:
            diagnostics.append(_item_diagnostic("operation_set_parent_record_missing", "Parent record could not be resolved.", intent_key=intent.key, parent_index=index))
            continue
        if store.get_lifecycle_record(record_id) is None and record_id not in expected_ids.values():
            diagnostics.append(_item_diagnostic("operation_set_parent_record_unknown", "Parent record does not exist and is not produced locally.", intent_key=intent.key, parent_record_id=record_id))
        parent["record_id"] = record_id
        if "lineage_kind" not in parent and "kind" not in parent and intent.lineage_kind is not None:
            parent["lineage_kind"] = intent.lineage_kind
        parents.append(parent)
    return parents, diagnostics


def _expected_record_id(manifest: OperationSetAcceptanceManifest, intent: OperationSetRecordIntent) -> str:
    if intent.action == "reference":
        return intent.target_record_id or ""
    if intent.record_id is not None:
        return intent.record_id
    digest = hashlib.sha256(f"{manifest.operation_set_id}:{manifest.revision}:{intent.key}".encode()).hexdigest()[:12]
    return f"{_slug(intent.record_kind or 'record')}-{_slug(intent.key)}-{digest}"


def _acceptance_id(manifest: OperationSetAcceptanceManifest) -> str:
    digest = manifest.digest.removeprefix("sha256:")[:12]
    return f"operation-set-acceptance-{_slug(manifest.operation_set_id)}-r{manifest.revision}-{digest}"


def _acceptance_item_id(receipt_id: str, intent_key: str) -> str:
    digest = hashlib.sha256(f"{receipt_id}:{intent_key}".encode()).hexdigest()[:12]
    return f"operation-set-item-{_slug(intent_key)}-{digest}"


def _planned_managed_files(
    context: EffectiveTopicContext,
    resolved: ResolvedOperationSet,
    manifest: OperationSetAcceptanceManifest,
    intent: OperationSetRecordIntent,
    outputs: Sequence[OperationSetOutput],
    *,
    record_id: str,
    receipt_id: str,
    record_kind: str | None,
    env: Mapping[str, str],
    cwd: Path,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    attachments = [item for item in outputs if item.disposition == "record_attachment"]
    if not attachments:
        return [], []
    selected_record_kind = record_kind or intent.record_kind or "artifact"
    label = intent.semantic_label or RESEARCH_RECORD_DEFAULT_LABELS.get(selected_record_kind, "topic.records.artifacts")
    result, diagnostics = resolve_semantic_path(context, label, env=env, cwd=cwd)
    item_diagnostics = [dict(item.to_json()) for item in diagnostics]
    if result is None:
        return [], item_diagnostics
    target_root = result.path / "research-records" / selected_record_kind / _slug(record_id) / "attachments"
    planned: list[dict[str, object]] = []
    for output in attachments:
        digest_prefix = output.digest.removeprefix("sha256:")[:12]
        target = target_root / f"{digest_prefix}-{_slug(Path(output.path).stem)}{Path(output.path).suffix}"
        if target.exists() and (not target.is_file() or file_digest(target) != output.digest):
            item_diagnostics.append(
                _item_diagnostic(
                    "operation_set_attachment_destination_conflict",
                    "Managed attachment destination already contains different content.",
                    path=target,
                    intent_key=intent.key,
                )
            )
        planned.append(
            {
                "path": str(target.resolve(strict=False)),
                "source_path": str((resolved.root / output.path).resolve(strict=False)),
                "original_relative_path": output.path,
                "file_role": "attachment",
                "semantic_label": label,
                "operation_set_id": manifest.operation_set_id,
                "acceptance_receipt_id": receipt_id,
                "digest": output.digest,
                "size_bytes": output.size_bytes,
                "media_type": output.media_type or "application/octet-stream",
            }
        )
    return planned, item_diagnostics


def _request_for_intent(
    context: EffectiveTopicContext,
    resolved: ResolvedOperationSet,
    manifest: OperationSetAcceptanceManifest,
    intent: OperationSetRecordIntent,
    outputs: Sequence[OperationSetOutput],
    *,
    record_id: str,
    receipt_id: str,
    intent_digest: str,
    parents: Sequence[dict[str, object]],
    managed_files: Sequence[dict[str, object]],
    record_kind: str | None,
) -> ResearchRecordRequest:
    payloads = [item for item in outputs if item.disposition == "record_payload"]
    source = resolved.root / payloads[0].path if payloads else None
    structured = any((intent.format_profile_ref, intent.schema_ref, intent.template_ref, intent.render_format))
    metadata = {
        **intent.metadata,
        "operation_set_id": manifest.operation_set_id,
        "operation_set_revision": manifest.revision,
        "operation_set_manifest_digest": manifest.digest,
        "operation_set_acceptance_id": receipt_id,
        "operation_set_intent_key": intent.key,
        "operation_set_intent_digest": intent_digest,
        "operation_set_worker": {"kind": resolved.worker_kind, "name": resolved.worker_name},
        "operation_set_root_reason": intent.root_reason,
    }
    lifecycle_refs = {**manifest.lifecycle_refs, **intent.lifecycle_refs}
    return ResearchRecordRequest(
        record_kind=record_kind or intent.record_kind or "",
        record_id=record_id,
        status=intent.status,
        semantic_id=intent.semantic_id,
        scope_key=intent.scope_key,
        profile=intent.profile,
        skill=intent.skill or manifest.producer_skill,
        producer=intent.producer or manifest.producer_skill,
        consumer=intent.consumer,
        topic_actor_name=resolved.worker_name if resolved.worker_kind == "topic_actor" else None,
        semantic_label=intent.semantic_label,
        body_file=source if source is not None and not structured else None,
        content_name=intent.content_name or (Path(source).name if source is not None and not structured else None),
        payload_file=source if source is not None and structured else None,
        format_profile_ref=intent.format_profile_ref,
        schema_ref=intent.schema_ref,
        template_ref=intent.template_ref,
        render_format=intent.render_format,
        metadata={key: value for key, value in metadata.items() if value is not None},
        lifecycle_refs=lifecycle_refs,
        relationships=list(intent.relationships),
        parents=[dict(item) for item in parents],
        lineage_kind=intent.lineage_kind,
        generation_id=intent.generation_id,
        generation_purpose=intent.generation_purpose,
        decision_record_id=intent.decision_record_id,
        lineage_rationale=intent.lineage_rationale,
        file_attachments=[dict(item) for item in managed_files],
        index_hints=dict(intent.index_hints),
        idea_effects=dict(intent.idea_effects) if intent.idea_effects is not None else None,
        idea_effects_required=intent.idea_effects_required,
    )


def _preflight_record_request(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    request: ResearchRecordRequest,
    outputs: Sequence[OperationSetOutput],
    operation_root: Path,
    *,
    env: Mapping[str, str],
    cwd: Path,
) -> list[dict[str, object]]:
    diagnostics: list[dict[str, object]] = []
    try:
        _validate_record_kind(request.record_kind)
        _validate_status(request.status)
        _validate_write_artifact_identity(request)
    except ResearchRecordError as exc:
        diagnostics.append(_item_diagnostic(exc.code, exc.message))
    if request.payload_file is not None:
        validation, validation_diagnostics = validate_record_payload(context, request, env=env, cwd=cwd)
        diagnostics.extend(dict(item.to_json()) for item in validation_diagnostics)
        if validation.get("ok") is not True and not validation_diagnostics:
            error = validation.get("error")
            diagnostics.append(_item_diagnostic(str(error.get("code", "operation_set_payload_invalid")) if isinstance(error, Mapping) else "operation_set_payload_invalid", str(error.get("message", "Structured record payload failed validation.")) if isinstance(error, Mapping) else "Structured record payload failed validation."))
    if request.idea_effects is not None:
        payload_output = next((item for item in outputs if item.disposition == "record_payload"), None)
        if payload_output is None:
            diagnostics.append(_item_diagnostic("operation_set_idea_effects_payload_missing", "Research Idea effects require one structured record_payload."))
        else:
            source_path = operation_root / payload_output.path
            try:
                payload = json.loads(source_path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                diagnostics.append(_item_diagnostic("operation_set_idea_effects_payload_invalid", f"Cannot read idea-bearing structured payload: {exc}", path=source_path))
            else:
                if not isinstance(payload, Mapping):
                    diagnostics.append(_item_diagnostic("operation_set_idea_effects_payload_invalid", "Idea-bearing structured payload must be an object.", path=source_path))
                else:
                    diagnostics.extend(_preflight_idea_effects(store, request, payload))
    return diagnostics


def _preflight_idea_effects(
    store: WorkspaceRuntimeStore,
    request: ResearchRecordRequest,
    payload: Mapping[str, object],
) -> list[dict[str, object]]:
    diagnostics: list[dict[str, object]] = []
    effects = request.idea_effects or {}
    ideas = effects.get("ideas")
    if not isinstance(ideas, list):
        return [_item_diagnostic("operation_set_idea_effects_ideas_missing", "Research Idea effects require an ideas array.")]
    declared_ids: set[str] = set()
    for index, item in enumerate(ideas):
        if not isinstance(item, Mapping):
            diagnostics.append(_item_diagnostic("operation_set_idea_effect_invalid", "Research Idea effect entry must be an object.", index=index))
            continue
        idea_id = _optional_string(item.get("idea_id"))
        source_path = _optional_string(item.get("source_json_path"))
        if idea_id is None or source_path is None:
            diagnostics.append(_item_diagnostic("operation_set_idea_effect_invalid", "Research Idea effect requires idea_id and source_json_path.", index=index))
            continue
        declared_ids.add(idea_id)
        resolution = resolve_payload_source_fragment(payload, source_path, format_profile_ref=request.format_profile_ref, idea_id=idea_id, record_id=request.record_id, severity="error")
        diagnostics.extend(resolution.diagnostics)
        if resolution.status != SOURCE_STATUS_EXACT:
            diagnostics.append(_item_diagnostic("operation_set_idea_source_not_exact", "Research Idea source_json_path must resolve to one object.", idea_id=idea_id, source_json_path=source_path))
    for field_name in ("lineage_edges", "generation_groups"):
        values = effects.get(field_name)
        if not isinstance(values, list):
            continue
        for item in values:
            if not isinstance(item, Mapping):
                continue
            ref_fields = ("parent_idea_id", "child_idea_id") if field_name == "lineage_edges" else ("parent_idea_ids",)
            refs: list[str] = []
            for ref_field in ref_fields:
                value = item.get(ref_field)
                if isinstance(value, str):
                    refs.append(value)
                elif isinstance(value, list):
                    refs.extend(str(ref) for ref in value if isinstance(ref, str))
            for idea_id in refs:
                if idea_id not in declared_ids and store.get_research_idea(idea_id) is None:
                    diagnostics.append(_item_diagnostic("operation_set_idea_ref_missing", "Research Idea effect references an unknown idea.", idea_id=idea_id, component=field_name))
    return diagnostics


def _verify_reference_outputs(
    store: WorkspaceRuntimeStore,
    record_id: str,
    outputs: Sequence[OperationSetOutput],
    operation_root: Path,
) -> list[dict[str, object]]:
    record = store.get_lifecycle_record(record_id)
    if record is None:
        return [_item_diagnostic("operation_set_reference_record_missing", "Referenced durable record does not exist.", record_id=record_id)]
    metadata = store.metadata()
    if record.topic_workspace_id != metadata.topic_workspace_id or record.research_topic_id != metadata.research_topic_id:
        return [
            _item_diagnostic(
                "operation_set_reference_scope_mismatch",
                "Referenced durable record is outside the selected Topic Workspace.",
                record_id=record_id,
            )
        ]
    candidate_digests: set[str] = set()
    for path_value in (record.content_path,):
        if path_value is not None:
            path = Path(path_value)
            if path.exists() and path.is_file():
                candidate_digests.add(file_digest(path))
    structured = store.get_structured_payload(record_id)
    if structured is not None and structured.payload_file_path is not None:
        path = Path(structured.payload_file_path)
        if path.exists() and path.is_file():
            candidate_digests.add(file_digest(path))
    if store.connection.execute("SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'research_record_files'").fetchone() is not None:
        for row in store.connection.execute("SELECT path, digest FROM research_record_files WHERE record_id = ?", (record_id,)):
            if row["digest"]:
                candidate_digests.add(_normalize_digest(str(row["digest"])))
            path = Path(str(row["path"]))
            if path.exists() and path.is_file():
                candidate_digests.add(file_digest(path))
    diagnostics: list[dict[str, object]] = []
    for output in outputs:
        if output.disposition not in {"record_payload", "record_attachment"}:
            continue
        if output.digest not in candidate_digests:
            diagnostics.append(_item_diagnostic("operation_set_reference_digest_unverified", "Referenced record has no managed content matching this output digest.", record_id=record_id, path=output.path, digest=output.digest, staged_path=str(operation_root / output.path)))
    return diagnostics
