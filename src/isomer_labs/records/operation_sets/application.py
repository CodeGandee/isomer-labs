"""Receipt-backed apply, resume, and independent verification."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any, Mapping, Sequence
import os
import shutil
import tempfile

from isomer_labs.core.diagnostics import Diagnostic
from isomer_labs.core.path_utils import is_within
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.records.index import refresh_query_index_for_record
from isomer_labs.records.store import ResearchRecordError, create_record, revise_record
from isomer_labs.runtime.records import (
    OperationSetAcceptanceItemRecord,
    OperationSetAcceptanceRecord,
    _provenance_ref,
    utc_timestamp,
)
from isomer_labs.runtime.store import WorkspaceRuntimeStore, open_workspace_runtime

from .inventory import _reconcile_manifest, inventory_operation_set
from .models import (
    OperationSetAcceptanceError,
    OperationSetAcceptanceManifest,
    OperationSetInventoryEntry,
    OperationSetOutput,
    OperationSetRecordIntent,
    ResolvedOperationSet,
    _context_failure_payload,
    _has_item_errors,
    _item_diagnostic,
    _manifest_error,
    _optional_string,
    _output_summary,
    file_digest,
    load_operation_set_manifest,
)
from .planning import (
    _acceptance_item_id,
    _expanded_parents,
    _expected_record_id,
    _ordered_intents,
    _request_for_intent,
    plan_operation_set_acceptance,
)

def apply_operation_set_acceptance(
    context: EffectiveTopicContext,
    manifest_path: Path,
    *,
    env: Mapping[str, str],
    cwd: Path,
    agent_name: str | None = None,
    topic_actor_name: str | None = None,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    preview, diagnostics = plan_operation_set_acceptance(
        context,
        manifest_path,
        env=env,
        cwd=cwd,
        agent_name=agent_name,
        topic_actor_name=topic_actor_name,
    )
    if preview.get("ok") is not True:
        return {**preview, "mode": "apply", "mutated": False}, diagnostics
    selected_manifest_path = Path(str(preview["manifest_path"]))
    manifest = load_operation_set_manifest(selected_manifest_path)
    resolved_payload = preview["resolved"]
    assert isinstance(resolved_payload, Mapping)
    resolved = ResolvedOperationSet(
        root=Path(str(resolved_payload["canonical_root"])),
        output_root=Path(str(resolved_payload["worker_output_root"])),
        worker_kind=str(resolved_payload["worker_kind"]),
        worker_name=str(resolved_payload["worker_name"]),
        worker_scope_ref=str(resolved_payload["worker_scope_ref"]),
        relative_path=str(resolved_payload["relative_path"]),
        operation_set_id=str(resolved_payload["operation_set_id"]),
    )
    actions_by_key = {str(item["intent_key"]): item for item in preview["actions"] if isinstance(item, Mapping)}
    receipt_id = str(preview["acceptance_id"])
    store, runtime_diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    diagnostics.extend(runtime_diagnostics)
    if store is None:
        return _context_failure_payload("operation-sets.accept", diagnostics), diagnostics
    now = utc_timestamp()
    try:
        existing = store.get_operation_set_acceptance(receipt_id)
        receipt = OperationSetAcceptanceRecord(
            id=receipt_id,
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            operation_set_id=manifest.operation_set_id,
            revision=manifest.revision,
            supersedes_receipt_id=manifest.supersedes_receipt_id,
            worker_kind=resolved.worker_kind,
            worker_name=resolved.worker_name,
            canonical_root=str(resolved.root),
            manifest_path=str(selected_manifest_path),
            manifest_digest=manifest.digest,
            manifest=manifest.to_json(),
            status=existing.status if existing is not None and existing.status == "complete" else "applying",
            output_summary=_output_summary(manifest),
            diagnostics=[],
            created_at=existing.created_at if existing is not None else now,
            updated_at=now,
            provenance_refs=existing.provenance_refs if existing is not None else [_provenance_ref("operation-set-acceptance", receipt_id)],
        )
        with store.connection:
            store.upsert_operation_set_acceptance(receipt)
            existing_items = {item.intent_key: item for item in store.list_operation_set_acceptance_items(receipt_id)}
            for intent in manifest.record_intents:
                action = actions_by_key[intent.key]
                prior_item = existing_items.get(intent.key)
                item = OperationSetAcceptanceItemRecord(
                    id=_acceptance_item_id(receipt_id, intent.key),
                    acceptance_id=receipt_id,
                    intent_key=intent.key,
                    intent_digest=str(action["intent_digest"]),
                    action=intent.action,
                    status=prior_item.status if prior_item is not None else "pending",
                    record_id=prior_item.record_id if prior_item is not None else None,
                    managed_files=prior_item.managed_files if prior_item is not None else [],
                    lineage_refs=prior_item.lineage_refs if prior_item is not None else [],
                    idea_effect_refs=prior_item.idea_effect_refs if prior_item is not None else [],
                    diagnostics=prior_item.diagnostics if prior_item is not None else [],
                    created_at=prior_item.created_at if prior_item is not None else now,
                    updated_at=now,
                )
                store.upsert_operation_set_acceptance_item(item)

        applied_items: list[dict[str, object]] = []
        for intent in _ordered_intents(manifest)[0]:
            action = actions_by_key[intent.key]
            item = next(item for item in store.list_operation_set_acceptance_items(receipt_id) if item.intent_key == intent.key)
            if item.status == "complete":
                replay_diagnostics = _verify_completed_item(store, item)
                if not _has_item_errors(replay_diagnostics):
                    applied_items.append({**item.to_json(), "replayed": True})
                    continue
            applying_item = replace(item, status="applying", diagnostics=[], updated_at=utc_timestamp())
            with store.connection:
                store.upsert_operation_set_acceptance_item(applying_item)
            try:
                record_id = str(action["record_id"])
                intent_outputs = tuple(
                    item_value
                    for item_value in manifest.outputs
                    if item_value.record_key == intent.key
                )
                _verify_output_sources(resolved.root, intent_outputs)
                managed_files = [dict(item_value) for item_value in action["managed_files"] if isinstance(item_value, Mapping)]
                existing_record = store.get_lifecycle_record(record_id)
                result: dict[str, Any]
                if intent.action == "reference":
                    result = {"record": existing_record.to_json() if existing_record is not None else {"id": record_id}, "idea_writes": {}}
                elif existing_record is not None:
                    metadata = existing_record.transition_metadata
                    if metadata.get("operation_set_acceptance_id") != receipt_id or metadata.get("operation_set_intent_digest") != str(action["intent_digest"]):
                        raise _manifest_error("operation_set_record_id_conflict", f"Record id was claimed by another operation: {record_id}")
                    result = {"record": existing_record.to_json(), "idea_writes": _idea_writes_for_record(store, record_id)}
                else:
                    target_record = (
                        store.get_lifecycle_record(intent.target_record_id)
                        if intent.target_record_id is not None
                        else None
                    )
                    request = _request_for_intent(
                        context,
                        resolved,
                        manifest,
                        intent,
                        intent_outputs,
                        record_id=record_id,
                        receipt_id=receipt_id,
                        intent_digest=str(action["intent_digest"]),
                        parents=tuple(dict(item_value) for item_value in action["parents"] if isinstance(item_value, Mapping)),
                        managed_files=managed_files,
                        record_kind=intent.record_kind or (target_record.record_kind if target_record is not None else None),
                    )
                    if intent.action == "revise":
                        assert intent.target_record_id is not None
                        result, record_diagnostics = revise_record(context, intent.target_record_id, request, env=env, cwd=cwd)
                    else:
                        result, record_diagnostics = create_record(context, request, env=env, cwd=cwd)
                    diagnostics.extend(record_diagnostics)
                    if result.get("ok") is not True:
                        raise OperationSetAcceptanceError(
                            f"Record intent failed: {intent.key}",
                            code="operation_set_record_action_failed",
                            payload={"intent_key": intent.key, "record_result": result},
                        )
                _copy_managed_files(resolved.root, managed_files)
                refresh_query_index_for_record(context, store, record_id)
                lineage_refs = _lineage_refs_for_record(store, record_id)
                idea_refs = _idea_effect_refs(result.get("idea_writes"))
                complete_item = replace(
                    applying_item,
                    status="complete",
                    record_id=record_id,
                    managed_files=managed_files,
                    lineage_refs=lineage_refs,
                    idea_effect_refs=idea_refs,
                    diagnostics=[],
                    updated_at=utc_timestamp(),
                )
                with store.connection:
                    store.upsert_operation_set_acceptance_item(complete_item)
                applied_items.append({**complete_item.to_json(), "replayed": existing_record is not None})
            except Exception as exc:
                failure_payload = exc.to_payload() if isinstance(exc, ResearchRecordError) else {"error": {"code": "operation_set_item_failed", "message": str(exc)}}
                failed_item = replace(
                    applying_item,
                    status="failed",
                    diagnostics=[_item_diagnostic(str(failure_payload.get("error", {}).get("code", "operation_set_item_failed")), str(failure_payload.get("error", {}).get("message", exc)))],
                    updated_at=utc_timestamp(),
                )
                partial_receipt = replace(
                    receipt,
                    status="partial",
                    diagnostics=failed_item.diagnostics,
                    updated_at=utc_timestamp(),
                )
                with store.connection:
                    store.upsert_operation_set_acceptance_item(failed_item)
                    store.upsert_operation_set_acceptance(partial_receipt)
                return {
                    "ok": False,
                    "mutated": True,
                    "operation": "operation-sets.accept",
                    "mode": "apply",
                    "acceptance": partial_receipt.to_json(include_manifest=False),
                    "items": [item.to_json() for item in store.list_operation_set_acceptance_items(receipt_id)],
                    "failed_intent_key": intent.key,
                    "diagnostics": failed_item.diagnostics,
                    "recovery_actions": [f"Retry accept --apply with the unchanged manifest {selected_manifest_path}."],
                }, diagnostics

        completed = replace(receipt, status="complete", diagnostics=[], updated_at=utc_timestamp())
        with store.connection:
            store.upsert_operation_set_acceptance(completed)
            if manifest.supersedes_receipt_id is not None:
                prior = store.get_operation_set_acceptance(manifest.supersedes_receipt_id)
                if prior is not None:
                    store.upsert_operation_set_acceptance(replace(prior, status="superseded", updated_at=utc_timestamp()))
    finally:
        store.close()

    verification, verify_diagnostics = verify_operation_set_acceptance(context, receipt_id, env=env)
    diagnostics.extend(verify_diagnostics)
    if verification.get("ok") is not True:
        repair_store, repair_diagnostics = open_workspace_runtime(context, env=env, read_only=False)
        diagnostics.extend(repair_diagnostics)
        if repair_store is not None:
            try:
                current = repair_store.get_operation_set_acceptance(receipt_id)
                if current is not None:
                    with repair_store.connection:
                        repair_store.upsert_operation_set_acceptance(
                            replace(current, status="partial", diagnostics=[dict(item) for item in verification.get("diagnostics", []) if isinstance(item, Mapping)], updated_at=utc_timestamp())
                        )
            finally:
                repair_store.close()
        return {
            "ok": False,
            "mutated": True,
            "operation": "operation-sets.accept",
            "mode": "apply",
            "acceptance_id": receipt_id,
            "verification": verification,
            "diagnostics": verification.get("diagnostics", []),
        }, diagnostics
    return {
        "ok": True,
        "mutated": True,
        "operation": "operation-sets.accept",
        "mode": "apply",
        "acceptance": verification["acceptance"],
        "items": verification["items"],
        "verification": verification,
        "replayed": all(bool(item.get("replayed")) for item in applied_items) if applied_items else True,
        "diagnostics": [],
    }, diagnostics


def verify_operation_set_acceptance(
    context: EffectiveTopicContext,
    receipt_or_operation_set_id: str,
    *,
    env: Mapping[str, str],
) -> tuple[dict[str, Any], list[Diagnostic]]:
    store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if store is None:
        return _context_failure_payload("operation-sets.verify", diagnostics), diagnostics
    try:
        receipt = store.get_operation_set_acceptance(receipt_or_operation_set_id)
        if receipt is None:
            candidates = store.list_operation_set_acceptances(
                topic_workspace_id=context.topic_workspace_id,
                operation_set_id=receipt_or_operation_set_id,
            )
            receipt = candidates[0] if candidates else None
        if receipt is None:
            raise OperationSetAcceptanceError(
                f"Operation-set acceptance receipt not found: {receipt_or_operation_set_id}",
                code="operation_set_acceptance_not_found",
            )
        if (
            receipt.research_topic_id != context.research_topic.id
            or receipt.topic_workspace_id != context.topic_workspace_id
        ):
            raise OperationSetAcceptanceError(
                "Operation-set acceptance receipt is outside the selected Topic Workspace.",
                code="operation_set_acceptance_scope_mismatch",
            )
        manifest = OperationSetAcceptanceManifest.from_json(receipt.manifest)
        verification_diagnostics: list[dict[str, object]] = []
        if manifest.digest != receipt.manifest_digest:
            verification_diagnostics.append(
                _item_diagnostic(
                    "operation_set_receipt_manifest_digest_mismatch",
                    "Acceptance receipt manifest no longer matches its recorded digest.",
                    expected_digest=receipt.manifest_digest,
                    observed_digest=manifest.digest,
                )
            )
        if receipt.status != "complete":
            verification_diagnostics.append(_item_diagnostic("operation_set_acceptance_incomplete", "Acceptance receipt is not complete.", status=receipt.status))
        root = Path(receipt.canonical_root)
        if not root.exists() or not root.is_dir():
            verification_diagnostics.append(_item_diagnostic("operation_set_root_missing", "Accepted operation-set root is unavailable for staged-file verification.", path=root))
            inventory: list[OperationSetInventoryEntry] = []
        else:
            inventory, inventory_diagnostics = inventory_operation_set(root)
            verification_diagnostics.extend(inventory_diagnostics)
            verification_diagnostics.extend(_reconcile_manifest(inventory, manifest, require_dispositions=True))
        items = store.list_operation_set_acceptance_items(receipt.id)
        item_by_key = {item.intent_key: item for item in items}
        expected_ids = {intent.key: _expected_record_id(manifest, intent) for intent in manifest.record_intents}
        for intent in manifest.record_intents:
            item = item_by_key.get(intent.key)
            if item is None:
                verification_diagnostics.append(_item_diagnostic("operation_set_acceptance_item_missing", "Acceptance receipt lacks an intent item.", intent_key=intent.key))
                continue
            if item.status != "complete":
                verification_diagnostics.append(_item_diagnostic("operation_set_acceptance_item_incomplete", "Acceptance item is not complete.", intent_key=intent.key, status=item.status))
                continue
            verification_diagnostics.extend(_verify_completed_item(store, item))
            record_id = item.record_id or expected_ids[intent.key]
            if store.connection.execute("SELECT 1 FROM research_record_index WHERE record_id = ?", (record_id,)).fetchone() is None:
                verification_diagnostics.append(_item_diagnostic("operation_set_record_not_queryable", "Accepted record is absent from the query index.", intent_key=intent.key, record_id=record_id))
            parents, parent_diagnostics = _expanded_parents(intent, expected_ids, store)
            verification_diagnostics.extend(parent_diagnostics)
            edges = store.list_research_record_lineage_edges(topic_workspace_id=context.topic_workspace_id, child_record_id=record_id)
            edge_keys = {(edge.parent_record_id, edge.lineage_kind, edge.parent_role) for edge in edges}
            for parent in parents:
                expected = (str(parent["record_id"]), str(parent.get("lineage_kind") or intent.lineage_kind or "derived_from"), _optional_string(parent.get("parent_role") or parent.get("role")))
                if expected not in edge_keys:
                    verification_diagnostics.append(_item_diagnostic("operation_set_record_lineage_missing", "Promised canonical record parent edge is missing.", intent_key=intent.key, parent_record_id=expected[0], lineage_kind=expected[1]))
            accepted_record = store.get_lifecycle_record(record_id)
            effective_intent = replace(intent, record_kind=accepted_record.record_kind) if accepted_record is not None else intent
            verification_diagnostics.extend(_verify_idea_effects(store, effective_intent, record_id))
        ok = not _has_item_errors(verification_diagnostics)
        return {
            "ok": ok,
            "mutated": False,
            "operation": "operation-sets.verify",
            "acceptance": receipt.to_json(include_manifest=False),
            "items": [item.to_json() for item in items],
            "verified": ok,
            "diagnostics": verification_diagnostics,
        }, diagnostics
    finally:
        store.close()


def _copy_managed_files(operation_root: Path, managed_files: Sequence[Mapping[str, object]]) -> None:
    for item in managed_files:
        source = Path(str(item["source_path"])).resolve(strict=False)
        target = Path(str(item["path"])).resolve(strict=False)
        expected_digest = str(item["digest"])
        size_value = item["size_bytes"]
        if isinstance(size_value, bool) or not isinstance(size_value, int):
            raise _manifest_error("operation_set_attachment_size_invalid", f"Managed attachment size is invalid: {source}")
        expected_size = size_value
        if not is_within(source, operation_root) or not source.exists() or not source.is_file():
            raise _manifest_error("operation_set_attachment_source_invalid", f"Managed attachment source is unavailable or outside the operation set: {source}")
        if file_digest(source) != expected_digest or source.stat().st_size != expected_size:
            raise _manifest_error("operation_set_attachment_source_drift", f"Managed attachment source changed before copy: {source}")
        if target.exists():
            if target.is_file() and file_digest(target) == expected_digest:
                continue
            raise _manifest_error("operation_set_attachment_destination_conflict", f"Managed attachment destination already contains different content: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        descriptor, staged_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".staged", dir=target.parent)
        os.close(descriptor)
        staged = Path(staged_name)
        try:
            shutil.copyfile(source, staged)
            if file_digest(staged) != expected_digest:
                raise _manifest_error("operation_set_attachment_copy_mismatch", f"Managed attachment copy digest mismatch: {target}")
            os.replace(staged, target)
        finally:
            staged.unlink(missing_ok=True)


def _verify_output_sources(operation_root: Path, outputs: Sequence[OperationSetOutput]) -> None:
    for output in outputs:
        if output.disposition not in {"record_payload", "record_attachment"}:
            continue
        source = (operation_root / output.path).resolve(strict=False)
        if not is_within(source, operation_root) or not source.exists() or not source.is_file():
            raise _manifest_error(
                "operation_set_output_source_invalid",
                f"Durable operation-set source is unavailable or outside the operation set: {source}",
            )
        if source.stat().st_size != output.size_bytes or file_digest(source) != output.digest:
            raise _manifest_error(
                "operation_set_output_drift",
                f"Operation-set output changed after preflight: {output.path}",
            )


def _verify_completed_item(
    store: WorkspaceRuntimeStore,
    item: OperationSetAcceptanceItemRecord,
) -> list[dict[str, object]]:
    diagnostics: list[dict[str, object]] = []
    if item.record_id is None or store.get_lifecycle_record(item.record_id) is None:
        diagnostics.append(_item_diagnostic("operation_set_accepted_record_missing", "Acceptance item record is missing.", intent_key=item.intent_key, record_id=item.record_id))
    for managed in item.managed_files:
        path = Path(str(managed.get("path", "")))
        expected_digest = _optional_string(managed.get("digest"))
        if not path.exists() or not path.is_file():
            diagnostics.append(_item_diagnostic("operation_set_managed_file_missing", "Managed attachment is missing.", intent_key=item.intent_key, path=path))
        elif expected_digest is not None and file_digest(path) != expected_digest:
            diagnostics.append(_item_diagnostic("operation_set_managed_file_drift", "Managed attachment digest differs from the receipt.", intent_key=item.intent_key, path=path))
    topic_workspace_id = store.metadata().topic_workspace_id
    lineage_edge_ids = {
        edge.id
        for edge in store.list_research_record_lineage_edges(
            topic_workspace_id=topic_workspace_id,
            child_record_id=item.record_id,
        )
    }
    idea_edge_ids = {
        edge.id
        for edge in store.list_research_idea_lineage_edges(topic_workspace_id=topic_workspace_id)
    }
    for ref in item.lineage_refs:
        kind, separator, identifier = ref.partition(":")
        exists = bool(separator and identifier)
        if kind == "research-record-lineage":
            exists = identifier in lineage_edge_ids
        elif kind == "research-record-generation-group":
            exists = store.get_research_record_generation_group(identifier) is not None
        if not exists:
            diagnostics.append(
                _item_diagnostic(
                    "operation_set_lineage_ref_missing",
                    "Acceptance item lineage ref is no longer queryable.",
                    intent_key=item.intent_key,
                    ref=ref,
                )
            )
    for ref in item.idea_effect_refs:
        kind, separator, identifier = ref.partition(":")
        exists = bool(separator and identifier)
        if kind == "research-idea":
            exists = store.get_research_idea(identifier, topic_workspace_id=topic_workspace_id) is not None
        elif kind == "research-idea-realization":
            exists = store.get_research_idea_realization(identifier) is not None
        elif kind == "research-idea-generation-group":
            exists = store.get_research_idea_generation_group(identifier) is not None
        elif kind == "research-idea-lineage-edge":
            exists = identifier in idea_edge_ids
        elif kind == "research-idea-decision-option":
            exists = store.get_research_idea_decision_option(identifier) is not None
        elif kind == "research-idea-state-transition":
            exists = store.get_research_idea_state_transition(identifier) is not None
        elif kind == "research-idea-operation":
            exists = store.get_research_idea_operation(identifier, topic_workspace_id=topic_workspace_id) is not None
        if not exists:
            diagnostics.append(
                _item_diagnostic(
                    "operation_set_idea_effect_ref_missing",
                    "Acceptance item Research Idea effect ref is no longer queryable.",
                    intent_key=item.intent_key,
                    ref=ref,
                )
            )
    return diagnostics


def _idea_effect_refs(value: object) -> list[str]:
    if not isinstance(value, Mapping):
        return []
    refs: set[str] = set()
    operation = value.get("operation")
    if isinstance(operation, Mapping) and _optional_string(operation.get("operation_id")) is not None:
        refs.add(f"research-idea-operation:{operation['operation_id']}")
    for field_name, prefix, id_field in (
        ("ideas", "research-idea", "idea_id"),
        ("realizations", "research-idea-realization", "id"),
        ("generation_groups", "research-idea-generation-group", "id"),
        ("edges", "research-idea-lineage-edge", "id"),
        ("decision_options", "research-idea-decision-option", "id"),
        ("transitions", "research-idea-state-transition", "id"),
    ):
        rows = value.get(field_name)
        if not isinstance(rows, list):
            continue
        for row in rows:
            if isinstance(row, Mapping) and (identifier := _optional_string(row.get(id_field))) is not None:
                refs.add(f"{prefix}:{identifier}")
    return sorted(refs)


def _lineage_refs_for_record(store: WorkspaceRuntimeStore, record_id: str) -> list[str]:
    refs: set[str] = set()
    for edge in store.list_research_record_lineage_edges(
        topic_workspace_id=store.metadata().topic_workspace_id,
        child_record_id=record_id,
    ):
        refs.add(f"research-record-lineage:{edge.id}")
        if edge.generation_id is not None:
            refs.add(f"research-record-generation-group:{edge.generation_id}")
    return sorted(refs)


def _idea_writes_for_record(store: WorkspaceRuntimeStore, record_id: str) -> dict[str, object]:
    realizations = [item for item in store.list_research_idea_realizations(topic_workspace_id=store.metadata().topic_workspace_id) if item.record_id == record_id]
    ideas = [store.get_research_idea(item.idea_id, topic_workspace_id=item.topic_workspace_id) for item in realizations]
    return {
        "ideas": [item.to_json() for item in ideas if item is not None],
        "realizations": [item.to_json() for item in realizations],
    }


def _verify_idea_effects(
    store: WorkspaceRuntimeStore,
    intent: OperationSetRecordIntent,
    record_id: str,
) -> list[dict[str, object]]:
    if intent.idea_effects is None:
        return []
    diagnostics: list[dict[str, object]] = []
    effects = intent.idea_effects
    idea_values = effects.get("ideas")
    if not isinstance(idea_values, list):
        idea_values = []
    for item in idea_values:
        if not isinstance(item, Mapping):
            continue
        idea_id = _optional_string(item.get("idea_id"))
        if idea_id is None:
            continue
        current_idea = store.get_research_idea(idea_id, topic_workspace_id=store.metadata().topic_workspace_id)
        if current_idea is None:
            diagnostics.append(_item_diagnostic("operation_set_research_idea_missing", "Promised Research Idea is missing.", idea_id=idea_id, record_id=record_id))
        else:
            for field_name in (
                "title",
                "summary",
                "exploration_state",
                "decision_state",
                "evidence_state",
                "archive_state",
                "visibility",
                "closure_reason",
            ):
                expected_value = item.get(field_name)
                if expected_value is not None and getattr(current_idea, field_name) != expected_value:
                    diagnostics.append(
                        _item_diagnostic(
                            "operation_set_research_idea_state_mismatch",
                            "Canonical Research Idea differs from the authored acceptance effect.",
                            idea_id=idea_id,
                            field=field_name,
                            expected=expected_value,
                            observed=getattr(current_idea, field_name),
                        )
                    )
        realizations = store.list_research_idea_realizations(topic_workspace_id=store.metadata().topic_workspace_id, idea_id=idea_id)
        source_path = _optional_string(item.get("source_json_path"))
        if not any(realization.record_id == record_id and realization.source_json_path == source_path for realization in realizations):
            diagnostics.append(_item_diagnostic("operation_set_idea_realization_missing", "Promised Research Idea realization is missing.", idea_id=idea_id, record_id=record_id, source_json_path=source_path))
    edges = store.list_research_idea_lineage_edges(topic_workspace_id=store.metadata().topic_workspace_id)
    edge_keys = {
        (
            item.parent_idea_id,
            item.child_idea_id,
            item.lineage_kind,
            item.parent_role,
            item.generation_id,
        )
        for item in edges
    }
    edge_values = effects.get("lineage_edges")
    if not isinstance(edge_values, list):
        edge_values = []
    for item in edge_values:
        if not isinstance(item, Mapping):
            continue
        expected_edge = (
            _optional_string(item.get("parent_idea_id")),
            _optional_string(item.get("child_idea_id")),
            _optional_string(item.get("lineage_kind")),
            _optional_string(item.get("parent_role")),
            _optional_string(item.get("generation_id")),
        )
        if expected_edge not in edge_keys:
            diagnostics.append(_item_diagnostic("operation_set_idea_lineage_missing", "Promised Idea Lineage Edge is missing.", parent_idea_id=expected_edge[0], child_idea_id=expected_edge[1], lineage_kind=expected_edge[2]))
    generation_values = effects.get("generation_groups")
    if not isinstance(generation_values, list):
        generation_values = []
    for item in generation_values:
        if not isinstance(item, Mapping):
            continue
        generation_id = _optional_string(item.get("generation_id"))
        group = store.get_research_idea_generation_group(generation_id or "")
        expected_members = _sorted_string_values(item.get("member_idea_ids"))
        expected_parents = _sorted_string_values(item.get("parent_idea_ids"))
        if (
            group is None
            or _sorted_string_values(group.metadata.get("member_idea_ids")) != expected_members
            or _sorted_string_values(group.metadata.get("parent_idea_ids")) != expected_parents
        ):
            diagnostics.append(
                _item_diagnostic(
                    "operation_set_idea_generation_group_missing",
                    "Promised Research Idea generation membership is missing or differs.",
                    generation_id=generation_id,
                )
            )
    options = store.list_research_idea_decision_options(topic_workspace_id=store.metadata().topic_workspace_id)
    option_keys = {(item.decision_record_id, item.idea_id, item.outcome) for item in options}
    option_values = effects.get("decision_options")
    if not isinstance(option_values, list):
        option_values = []
    for item in option_values:
        if not isinstance(item, Mapping):
            continue
        decision_id = _optional_string(item.get("decision_record_id")) or (record_id if intent.record_kind == "decision_record" else intent.decision_record_id)
        expected_option = (decision_id, _optional_string(item.get("idea_id")), _optional_string(item.get("outcome")))
        if expected_option not in option_keys:
            diagnostics.append(_item_diagnostic("operation_set_idea_decision_option_missing", "Promised Research Idea decision option is missing.", decision_record_id=expected_option[0], idea_id=expected_option[1], outcome=expected_option[2]))
    transitions = store.list_research_idea_state_transitions(topic_workspace_id=store.metadata().topic_workspace_id)
    transition_keys = {
        (
            item.idea_id,
            item.facet,
            item.previous_value,
            item.next_value,
            item.decision_record_id,
        )
        for item in transitions
    }
    transition_values = effects.get("transitions")
    if not isinstance(transition_values, list):
        transition_values = []
    for item in transition_values:
        if not isinstance(item, Mapping):
            continue
        expected_transition = (
            _optional_string(item.get("idea_id")),
            _optional_string(item.get("facet")),
            _optional_string(item.get("previous_value")),
            _optional_string(item.get("next_value")),
            _optional_string(item.get("decision_record_id")) or (record_id if intent.record_kind == "decision_record" else intent.decision_record_id),
        )
        if expected_transition not in transition_keys:
            diagnostics.append(
                _item_diagnostic(
                    "operation_set_idea_transition_missing",
                    "Promised Research Idea state transition is missing.",
                    idea_id=expected_transition[0],
                    facet=expected_transition[1],
                    previous_value=expected_transition[2],
                    next_value=expected_transition[3],
                )
            )
    return diagnostics


def _sorted_string_values(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return sorted(str(item) for item in value if isinstance(item, str))
