"""Focused validation checks for Workspace Runtime records."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Mapping

from isomer_labs.diagnostics import Diagnostic
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.paths import preview_paths
from isomer_labs.runtime.adapter_handoff_validation import validate_adapter_handoff_records
from isomer_labs.runtime.agent_identity import project_agent_instance_id_locations
from isomer_labs.runtime.store import WorkspaceRuntimeStore
from isomer_labs.runtime.validation_utils import (
    missing_ref_diagnostics as _missing_ref_diagnostics,
    owner_diagnostics as _owner_diagnostics,
)
from isomer_labs.workspace_refs import validate_agent_name_value


def _validate_metadata(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    metadata = store.metadata()
    if metadata.research_topic_id != context.research_topic.id:
        diagnostics.append(
            Diagnostic(
                code="ISO041",
                severity="error",
                concept="Workspace Runtime",
                path=store.db_path,
                field="research_topic_id",
                message="Workspace Runtime metadata references another Research Topic.",
            )
        )
    if metadata.topic_workspace_id != context.topic_workspace_id:
        diagnostics.append(
            Diagnostic(
                code="ISO041",
                severity="error",
                concept="Workspace Runtime",
                path=store.db_path,
                field="topic_workspace_id",
                message="Workspace Runtime metadata references another Topic Workspace.",
            )
        )
    return diagnostics


def _validate_path_plans(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    env: Mapping[str, str],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    current_entries, path_diagnostics = preview_paths(context, env=env)
    diagnostics.extend(path_diagnostics)
    current_by_surface = {entry.surface: entry for entry in current_entries}
    for plan in store.list_path_plans():
        if plan.topic_workspace_id != context.topic_workspace_id:
            diagnostics.append(
                Diagnostic(
                    code="ISO042",
                    severity="error",
                    concept="Workspace Runtime path plan",
                    path=store.db_path,
                    field=plan.surface,
                    message="Path plan belongs to another Topic Workspace.",
                )
            )
        current = current_by_surface.get(plan.surface)
        if current is not None and str(current.path) != plan.path:
            diagnostics.append(
                Diagnostic(
                    code="ISO042",
                    severity="warning",
                    concept="Workspace Runtime path plan",
                    path=store.db_path,
                    field=plan.surface,
                    message="Stored path plan differs from current Workspace Path Resolution output.",
                )
            )
        if not Path(plan.path).exists():
            diagnostics.append(
                Diagnostic(
                    code="ISO042",
                    severity="warning",
                    concept="Workspace Runtime path plan",
                    path=Path(plan.path),
                    field=plan.surface,
                    message="Stored path-plan target does not exist.",
                )
            )
    return diagnostics


def _validate_readiness(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    *,
    require_ready: bool,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    readiness_records = store.list_readiness_records()
    for record in readiness_records:
        if record.research_topic_id != context.research_topic.id:
            diagnostics.append(
                Diagnostic(
                    code="ISO043",
                    severity="error",
                    concept="Topic Environment Readiness",
                    path=store.db_path,
                    field=record.id,
                    message="Readiness record references another Research Topic.",
                )
            )
        if record.topic_workspace_id != context.topic_workspace_id:
            diagnostics.append(
                Diagnostic(
                    code="ISO043",
                    severity="error",
                    concept="Topic Environment Readiness",
                    path=store.db_path,
                    field=record.id,
                    message="Readiness record references another Topic Workspace.",
                )
            )
    latest = store.latest_readiness()
    if latest is None:
        diagnostics.append(
            Diagnostic(
                code="ISO043",
                severity="error" if require_ready else "warning",
                concept="Topic Environment Readiness",
                path=store.db_path,
                message="No Topic Environment Readiness record exists for this Workspace Runtime.",
            )
        )
    elif latest.status != "ready":
        diagnostics.append(
            Diagnostic(
                code="ISO043",
                severity="error" if require_ready else "warning",
                concept="Topic Environment Readiness",
                path=store.db_path,
                field=latest.id,
                message=f"Latest Topic Environment Readiness record is {latest.status}, not ready.",
            )
        )
    return diagnostics


def _validate_lifecycle_records(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    record_ids: dict[str, set[str]] = {}
    records = store.list_lifecycle_records()
    for record in records:
        record_ids.setdefault(record.record_kind, set()).add(record.id)
    for record in records:
        diagnostics.extend(_owner_diagnostics(context, store.db_path, record.id, record.research_topic_id, record.topic_workspace_id))
        if record.record_kind == "artifact" and record.content_path is not None and not Path(record.content_path).exists():
            diagnostics.append(
                Diagnostic(
                    code="ISO044",
                    severity="error",
                    concept="Artifact",
                    path=Path(record.content_path),
                    field=record.id,
                    message="Artifact record points to a missing file.",
                )
            )
        if record.record_kind == "gate" and record.status in {"open", "pending", "unresolved", "blocked"}:
            diagnostics.append(
                Diagnostic(
                    code="ISO045",
                    severity="warning",
                    concept="Gate",
                    path=store.db_path,
                    field=record.id,
                    message="Gate remains unresolved in Workspace Runtime.",
                )
            )
        if record.record_kind == "research_claim" and record.status == "supported":
            evidence_refs = [
                value
                for key, value in record.lifecycle_refs.items()
                if key.startswith("evidence_item")
            ]
            evidence_records = record_ids.get("evidence_item", set())
            if not evidence_refs or any(ref not in evidence_records for ref in evidence_refs):
                diagnostics.append(
                    Diagnostic(
                        code="ISO045",
                        severity="error",
                        concept="Research Claim",
                        path=store.db_path,
                        field=record.id,
                        message="Supported Research Claim lacks a valid Evidence Item ref.",
                    )
                )
        if record.record_kind == "provenance_record" and record.status == "stale":
            diagnostics.append(
                Diagnostic(
                    code="ISO045",
                    severity="warning",
                    concept="Provenance Record",
                    path=store.db_path,
                    field=record.id,
                    message="Provenance Record is stale.",
                )
            )
    return diagnostics


def _validate_agent_team_instances(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    manifest_profile_ids = {
        profile.id
        for profile in context.project.manifest.topic_agent_team_profiles
        if profile.research_topic_id == context.research_topic.id
    }
    agent_instances = {record.id: record for record in store.list_agent_instances()}
    agent_workspaces = {record.id: record for record in store.list_agent_workspaces()}
    path_plans = {record.id: record for record in store.list_path_plans()}

    for team in store.list_agent_team_instances():
        diagnostics.extend(_owner_diagnostics(context, store.db_path, team.id, team.research_topic_id, team.topic_workspace_id))
        if team.topic_agent_team_profile_id not in manifest_profile_ids:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Agent Team Instance",
                    path=store.db_path,
                    field=team.id,
                    message="Agent Team Instance references a missing or cross-topic Topic Agent Team Profile.",
                )
            )
        for agent_id in team.agent_instance_ids:
            if agent_id not in agent_instances:
                diagnostics.append(
                    Diagnostic(
                        code="ISO041",
                        severity="error",
                        concept="Agent Instance",
                        path=store.db_path,
                        field=agent_id,
                        message="Agent Team Instance references a missing Agent Instance.",
                    )
                )
        for workspace_id in team.agent_workspace_ids:
            if workspace_id not in agent_workspaces:
                diagnostics.append(
                    Diagnostic(
                        code="ISO041",
                        severity="error",
                        concept="Agent Workspace",
                        path=store.db_path,
                        field=workspace_id,
                        message="Agent Team Instance references a missing Agent Workspace.",
                    )
                )

    for agent in agent_instances.values():
        diagnostics.extend(_owner_diagnostics(context, store.db_path, agent.id, agent.research_topic_id, agent.topic_workspace_id))
        if store.get_agent_team_instance(agent.agent_team_instance_id) is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Agent Instance",
                    path=store.db_path,
                    field=agent.id,
                    message="Agent Instance references a missing Agent Team Instance.",
                )
            )

    for workspace in agent_workspaces.values():
        if workspace.topic_workspace_id != context.topic_workspace_id:
            diagnostics.append(
                Diagnostic(
                    code="ISO044",
                    severity="error",
                    concept="Agent Workspace",
                    path=store.db_path,
                    field=workspace.id,
                    message="Agent Workspace belongs to another Topic Workspace.",
                )
            )
        diagnostics.extend(
            validate_agent_name_value(
                agent_name=workspace.agent_name,
                source_path=store.db_path,
                field=f"{workspace.id}.agent_name",
                concept="Agent Workspace",
            )
        )
        plan = path_plans.get(workspace.path_plan_id)
        if plan is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Agent Workspace",
                    path=store.db_path,
                    field=workspace.id,
                    message="Agent Workspace references a missing path plan.",
                )
            )
        elif not Path(plan.path).exists():
            diagnostics.append(
                Diagnostic(
                    code="ISO044",
                    severity="error",
                    concept="Agent Workspace",
                    path=Path(plan.path),
                    field=workspace.id,
                    message="Agent Workspace directory is missing.",
                )
            )
        elif workspace.agent_name is not None:
            expected_path = context.topic_workspace_path / "agents" / workspace.agent_name
            if Path(plan.path).resolve(strict=False) != expected_path.resolve(strict=False):
                diagnostics.append(
                    Diagnostic(
                        code="ISO044",
                        severity="error",
                        concept="Agent Workspace",
                        path=Path(plan.path),
                        field=workspace.id,
                        message="Agent Workspace path plan does not match its topic-local agent name.",
                    )
                )
    return diagnostics


def _validate_global_agent_instance_id_uniqueness(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    id_locations, scan_issues = project_agent_instance_id_locations(context.project)
    for db_path, message in scan_issues:
        diagnostics.append(
            Diagnostic(
                code="ISO040",
                severity="warning",
                concept="Agent Instance Identity",
                path=db_path,
                message=f"Could not read Agent Instance ids for duplicate scan: {message}.",
            )
        )

    for agent_id, locations in id_locations.items():
        if len(locations) > 1:
            records = ", ".join(location.record_ref() for location in locations)
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Agent Instance Identity",
                    path=store.db_path,
                    field=agent_id,
                    message=(
                        f"Agent Instance id {agent_id} appears in multiple Project runtime records: "
                        f"{records}."
                    ),
                )
            )

    return diagnostics


def _validate_handoffs(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    lifecycle_by_kind: dict[str, set[str]] = {}
    for record in store.list_lifecycle_records():
        lifecycle_by_kind.setdefault(record.record_kind, set()).add(record.id)
    for handoff in store.list_handoffs():
        diagnostics.extend(_owner_diagnostics(context, store.db_path, handoff.id, handoff.research_topic_id, handoff.topic_workspace_id))
        if handoff.agent_team_instance_id is not None and store.get_agent_team_instance(handoff.agent_team_instance_id) is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Handoff",
                    path=store.db_path,
                    field=handoff.id,
                    message="Handoff references a missing Agent Team Instance.",
                )
            )
        if handoff.research_task_id is not None and handoff.research_task_id not in lifecycle_by_kind.get("research_task", set()):
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Handoff",
                    path=store.db_path,
                    field=handoff.id,
                    message="Handoff references a missing Research Task.",
                )
            )
        if handoff.run_id is not None and handoff.run_id not in lifecycle_by_kind.get("run", set()):
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Handoff",
                    path=store.db_path,
                    field=handoff.id,
                    message="Handoff references a missing Run.",
                )
            )
        if handoff.status in {"sent", "observing"} and handoff.stale_after is not None:
            stale_after = _parse_timestamp(handoff.stale_after)
            if stale_after is not None and stale_after < datetime.now(UTC):
                diagnostics.append(
                    Diagnostic(
                        code="ISO045",
                        severity="warning",
                        concept="Handoff",
                        path=store.db_path,
                        field=handoff.id,
                        message=(
                            "Handoff is stale; Signal Observations are not authoritative "
                            "completion until the Operator Agent records normalization."
                        ),
                    )
                )
    return diagnostics


def _validate_adapter_records(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    teams = {record.id for record in store.list_agent_team_instances()}
    agents = {record.id for record in store.list_agent_instances()}
    handoffs = {record.id: record for record in store.list_handoffs()}
    lifecycle_by_kind: dict[str, set[str]] = {}
    for record in store.list_lifecycle_records():
        lifecycle_by_kind.setdefault(record.record_kind, set()).add(record.id)
    path_plans = {record.id: record for record in store.list_path_plans()}
    manifest_refs = {record.id: record for record in store.list_adapter_manifest_refs()}
    payload_refs = {record.id: record for record in store.list_adapter_payload_refs()}
    command_runs = {record.id: record for record in store.list_adapter_command_runs()}
    for manifest_ref in store.list_adapter_manifest_refs():
        diagnostics.extend(
            _owner_diagnostics(
                context,
                store.db_path,
                manifest_ref.id,
                manifest_ref.research_topic_id,
                manifest_ref.topic_workspace_id,
            )
        )
        if manifest_ref.agent_team_instance_id not in teams:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter manifest ref",
                    path=store.db_path,
                    field=manifest_ref.id,
                    message="Adapter manifest ref points to a missing Agent Team Instance.",
                )
            )
        if manifest_ref.path_plan_id is not None and manifest_ref.path_plan_id not in path_plans:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter manifest ref",
                    path=store.db_path,
                    field=manifest_ref.id,
                    message="Adapter manifest ref points to a missing path plan.",
                )
            )
        manifest_path = Path(manifest_ref.manifest_path)
        if not manifest_path.exists():
            diagnostics.append(
                Diagnostic(
                    code="ISO044",
                    severity="warning",
                    concept="Execution Adapter manifest ref",
                    path=manifest_path,
                    field=manifest_ref.id,
                    message="Adapter manifest file is missing.",
                )
            )
    for reconciliation in store.list_adapter_reconciliation_records():
        diagnostics.extend(
            _owner_diagnostics(
                context,
                store.db_path,
                reconciliation.id,
                reconciliation.research_topic_id,
                reconciliation.topic_workspace_id,
            )
        )
        if reconciliation.agent_team_instance_id not in teams:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter reconciliation",
                    path=store.db_path,
                    field=reconciliation.id,
                    message="Reconciliation record points to a missing Agent Team Instance.",
                )
            )
    for payload_ref in store.list_adapter_payload_refs():
        diagnostics.extend(
            _owner_diagnostics(
                context,
                store.db_path,
                payload_ref.id,
                payload_ref.research_topic_id,
                payload_ref.topic_workspace_id,
            )
        )
        if payload_ref.agent_team_instance_id not in teams:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter payload ref",
                    path=store.db_path,
                    field=payload_ref.id,
                    message="Adapter payload ref points to a missing Agent Team Instance.",
                )
            )
        if payload_ref.agent_instance_id is not None and payload_ref.agent_instance_id not in agents:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter payload ref",
                    path=store.db_path,
                    field=payload_ref.id,
                    message="Adapter payload ref points to a missing Agent Instance.",
                )
            )
        if payload_ref.path_plan_id is not None and payload_ref.path_plan_id not in path_plans:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter payload ref",
                    path=store.db_path,
                    field=payload_ref.id,
                    message="Adapter payload ref points to a missing path plan.",
                )
            )
        payload_path = Path(payload_ref.payload_path)
        if not payload_path.exists():
            diagnostics.append(
                Diagnostic(
                    code="ISO044",
                    severity="warning",
                    concept="Execution Adapter payload ref",
                    path=payload_path,
                    field=payload_ref.id,
                    message="Adapter payload file is missing.",
                )
            )
    for command in store.list_adapter_command_runs():
        diagnostics.extend(
            _owner_diagnostics(
                context,
                store.db_path,
                command.id,
                command.research_topic_id,
                command.topic_workspace_id,
            )
        )
        if command.agent_team_instance_id not in teams:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter command run",
                    path=store.db_path,
                    field=command.id,
                    message="Adapter command run points to a missing Agent Team Instance.",
                )
            )
        if command.agent_instance_id is not None and command.agent_instance_id not in agents:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter command run",
                    path=store.db_path,
                    field=command.id,
                    message="Adapter command run points to a missing Agent Instance.",
                )
            )
        for payload_ref_id in command.payload_ref_ids:
            if payload_ref_id not in payload_refs:
                diagnostics.append(
                    Diagnostic(
                        code="ISO041",
                        severity="error",
                        concept="Execution Adapter command run",
                        path=store.db_path,
                        field=command.id,
                        message=f"Adapter command run points to a missing payload ref: {payload_ref_id}.",
                    )
                )
        if command.status in {"timed_out", "invalid_json", "failed"}:
            diagnostics.append(
                Diagnostic(
                    code="ISO075",
                    severity="warning",
                    concept="Execution Adapter command run",
                    path=store.db_path,
                    field=command.id,
                    message=f"Adapter command run is {command.status}; inspect or reconcile before treating the backend state as current.",
                )
            )
    diagnostics.extend(
        validate_adapter_handoff_records(
            context,
            store,
            handoffs=handoffs,
            teams=teams,
            agents=agents,
            command_runs=command_runs,
            payload_refs=payload_refs,
            lifecycle_by_kind=lifecycle_by_kind,
        )
    )
    for materialization in store.list_adapter_materializations():
        diagnostics.extend(_owner_diagnostics(context, store.db_path, materialization.id, materialization.research_topic_id, materialization.topic_workspace_id))
        if materialization.agent_team_instance_id not in teams:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter materialization",
                    path=store.db_path,
                    field=materialization.id,
                    message="Adapter materialization points to a missing Agent Team Instance.",
                )
            )
        diagnostics.extend(_missing_ref_diagnostics(store.db_path, "Execution Adapter materialization", materialization.id, "payload", materialization.material_ref_ids, payload_refs))
        diagnostics.extend(_missing_ref_diagnostics(store.db_path, "Execution Adapter materialization", materialization.id, "manifest", materialization.manifest_ref_ids, manifest_refs))
    for launch_attempt in store.list_adapter_launch_attempts():
        diagnostics.extend(_owner_diagnostics(context, store.db_path, launch_attempt.id, launch_attempt.research_topic_id, launch_attempt.topic_workspace_id))
        if launch_attempt.agent_team_instance_id not in teams:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter launch attempt",
                    path=store.db_path,
                    field=launch_attempt.id,
                    message="Adapter launch attempt points to a missing Agent Team Instance.",
                )
            )
        for agent_id in launch_attempt.agent_instance_ids:
            if agent_id not in agents:
                diagnostics.append(
                    Diagnostic(
                        code="ISO041",
                        severity="error",
                        concept="Execution Adapter launch attempt",
                        path=store.db_path,
                        field=launch_attempt.id,
                        message=f"Adapter launch attempt points to a missing Agent Instance: {agent_id}.",
                    )
                )
        diagnostics.extend(_missing_ref_diagnostics(store.db_path, "Execution Adapter launch attempt", launch_attempt.id, "command", launch_attempt.command_run_ids, command_runs))
        diagnostics.extend(_missing_ref_diagnostics(store.db_path, "Execution Adapter launch attempt", launch_attempt.id, "manifest", launch_attempt.manifest_ref_ids, manifest_refs))
        diagnostics.extend(_missing_ref_diagnostics(store.db_path, "Execution Adapter launch attempt", launch_attempt.id, "payload", launch_attempt.payload_ref_ids, payload_refs))
        if launch_attempt.status in {"partial", "failed"}:
            diagnostics.append(
                Diagnostic(
                    code="ISO075",
                    severity="warning",
                    concept="Execution Adapter launch attempt",
                    path=store.db_path,
                    field=launch_attempt.id,
                    message=f"Adapter launch attempt is {launch_attempt.status}; inspect-live or stop may be needed for recovery.",
                )
            )
    for snapshot in store.list_adapter_inspection_snapshots():
        diagnostics.extend(_owner_diagnostics(context, store.db_path, snapshot.id, snapshot.research_topic_id, snapshot.topic_workspace_id))
        if snapshot.snapshot_payload_ref_id is not None and snapshot.snapshot_payload_ref_id not in payload_refs:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter inspection snapshot",
                    path=store.db_path,
                    field=snapshot.id,
                    message="Adapter inspection snapshot points to a missing payload ref.",
                )
            )
        if snapshot.status in {"failed", "stale"}:
            diagnostics.append(
                Diagnostic(
                    code="ISO075",
                    severity="warning",
                    concept="Execution Adapter inspection snapshot",
                    path=store.db_path,
                    field=snapshot.id,
                    message=f"Adapter inspection snapshot is {snapshot.status}.",
                )
            )
    for stop_outcome in store.list_adapter_stop_outcomes():
        diagnostics.extend(_owner_diagnostics(context, store.db_path, stop_outcome.id, stop_outcome.research_topic_id, stop_outcome.topic_workspace_id))
        diagnostics.extend(_missing_ref_diagnostics(store.db_path, "Execution Adapter stop outcome", stop_outcome.id, "command", stop_outcome.command_run_ids, command_runs))
        diagnostics.extend(_missing_ref_diagnostics(store.db_path, "Execution Adapter stop outcome", stop_outcome.id, "payload", stop_outcome.payload_ref_ids, payload_refs))
        if stop_outcome.status in {"partial", "failed", "stale"}:
            diagnostics.append(
                Diagnostic(
                    code="ISO075",
                    severity="warning",
                    concept="Execution Adapter stop outcome",
                    path=store.db_path,
                    field=stop_outcome.id,
                    message=f"Adapter stop outcome is {stop_outcome.status}; remaining live refs must be inspected before cleanup is complete.",
                )
            )
    return diagnostics


def _validate_lifecycle_transitions(store: WorkspaceRuntimeStore) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for transition in store.list_lifecycle_transitions():
        missing_fields = [
            field
            for field in ("record_kind", "record_id", "previous_status", "next_status", "actor_ref", "rationale", "created_at")
            if transition[field] in (None, "")
        ]
        if missing_fields:
            diagnostics.append(
                Diagnostic(
                    code="ISO045",
                    severity="error",
                    concept="Research Lifecycle State",
                    path=store.db_path,
                    field=transition["id"],
                    message=f"Lifecycle transition is missing required field(s): {', '.join(missing_fields)}.",
                )
            )
    return diagnostics


def _parse_timestamp(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
