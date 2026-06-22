"""SQLite row mapping helpers for Workspace Runtime records."""

from __future__ import annotations

import sqlite3

from isomer_labs.runtime.models import (
    AgentInstanceRecord,
    AgentTeamInstanceRecord,
    AgentWorkspaceRecord,
    AdapterCommandRunRecord,
    AdapterInspectionSnapshotRecord,
    AdapterLaunchAttemptRecord,
    AdapterManifestRefRecord,
    AdapterMaterializationRecord,
    AdapterPayloadRefRecord,
    AdapterReconciliationRecord,
    AdapterStopOutcomeRecord,
    HandoffRecord,
    PathPlanRecord,
    RuntimeLifecycleRecord,
    TopicEnvironmentReadinessRecord,
)
from isomer_labs.runtime.serialization import (
    _loads_dict,
    _loads_json_list,
    _loads_list,
    _loads_object_dict,
)


def _row_to_path_plan(row: sqlite3.Row) -> PathPlanRecord:
    return PathPlanRecord(
        id=row["id"],
        topic_workspace_id=row["topic_workspace_id"],
        surface=row["surface"],
        path=row["path"],
        source=row["source"],
        source_detail=row["source_detail"],
        created_at=row["created_at"],
    )


def _row_to_lifecycle_record(row: sqlite3.Row) -> RuntimeLifecycleRecord:
    return RuntimeLifecycleRecord(
        id=row["id"],
        record_kind=row["record_kind"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        status=row["status"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        lifecycle_refs=_loads_dict(row["lifecycle_refs_json"]),
        transition_metadata=_loads_object_dict(row["transition_metadata_json"]),
        content_path=row["content_path"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_readiness(row: sqlite3.Row) -> TopicEnvironmentReadinessRecord:
    return TopicEnvironmentReadinessRecord(
        id=row["id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        status=row["status"],
        project_pixi_environment_refs=_loads_list(row["project_pixi_environment_refs_json"]),
        standalone_pixi_manifest_refs=_loads_list(row["standalone_pixi_manifest_refs_json"]),
        diagnostics=_loads_json_list(row["diagnostics_json"]),
        checked_at=row["checked_at"],
        actor_ref=row["actor_ref"],
        repair_service_request_hint=row["repair_service_request_hint"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_agent_team_instance(row: sqlite3.Row) -> AgentTeamInstanceRecord:
    return AgentTeamInstanceRecord(
        id=row["id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        topic_agent_team_profile_id=row["topic_agent_team_profile_id"],
        domain_agent_team_template_id=row["domain_agent_team_template_id"],
        status=row["status"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        agent_instance_ids=_loads_list(row["agent_instance_ids_json"]),
        agent_workspace_ids=_loads_list(row["agent_workspace_ids_json"]),
        run_ids=_loads_list(row["run_ids_json"]),
        workflow_stage_cursor_ids=_loads_list(row["workflow_stage_cursor_ids_json"]),
        blocker_refs=_loads_list(row["blocker_refs_json"]),
        handoff_ids=_loads_list(row["handoff_ids_json"]),
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_agent_instance(row: sqlite3.Row) -> AgentInstanceRecord:
    return AgentInstanceRecord(
        id=row["id"],
        agent_team_instance_id=row["agent_team_instance_id"],
        agent_role_id=row["agent_role_id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        agent_profile_ref=row["agent_profile_ref"],
        status=row["status"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_agent_workspace(row: sqlite3.Row) -> AgentWorkspaceRecord:
    return AgentWorkspaceRecord(
        id=row["id"],
        agent_instance_id=row["agent_instance_id"],
        topic_workspace_id=row["topic_workspace_id"],
        path_plan_id=row["path_plan_id"],
        status=row["status"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_handoff(row: sqlite3.Row) -> HandoffRecord:
    return HandoffRecord(
        id=row["id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        source_actor_ref=row["source_actor_ref"],
        target_actor_ref=row["target_actor_ref"],
        status=row["status"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        research_task_id=row["research_task_id"],
        run_id=row["run_id"],
        agent_team_instance_id=row["agent_team_instance_id"],
        completion_watcher_contract_refs=_loads_list(row["completion_watcher_contract_refs_json"]),
        expected_output_refs=_loads_list(row["expected_output_refs_json"]),
        stale_after=row["stale_after"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_adapter_manifest_ref(row: sqlite3.Row) -> AdapterManifestRefRecord:
    return AdapterManifestRefRecord(
        id=row["id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        agent_team_instance_id=row["agent_team_instance_id"],
        adapter_id=row["adapter_id"],
        manifest_kind=row["manifest_kind"],
        manifest_path=row["manifest_path"],
        manifest_digest=row["manifest_digest"],
        source=row["source"],
        path_plan_id=row["path_plan_id"],
        agent_instance_ids=_loads_list(row["agent_instance_ids_json"]),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_adapter_reconciliation_record(row: sqlite3.Row) -> AdapterReconciliationRecord:
    return AdapterReconciliationRecord(
        id=row["id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        agent_team_instance_id=row["agent_team_instance_id"],
        adapter_id=row["adapter_id"],
        state=row["state"],
        mapping_confidence=row["mapping_confidence"],
        manifest_refs=_loads_list(row["manifest_refs_json"]),
        manifest_digest_summary=_loads_object_dict(row["manifest_digest_summary_json"]),
        live_observation_summary=_loads_object_dict(row["live_observation_summary_json"]),
        diagnostics=_loads_json_list(row["diagnostics_json"]),
        actor_ref=row["actor_ref"],
        created_at=row["created_at"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_adapter_payload_ref(row: sqlite3.Row) -> AdapterPayloadRefRecord:
    return AdapterPayloadRefRecord(
        id=row["id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        agent_team_instance_id=row["agent_team_instance_id"],
        agent_instance_id=row["agent_instance_id"],
        adapter_id=row["adapter_id"],
        payload_kind=row["payload_kind"],
        payload_path=row["payload_path"],
        payload_digest=row["payload_digest"],
        source=row["source"],
        command_run_id=row["command_run_id"],
        path_plan_id=row["path_plan_id"],
        created_at=row["created_at"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_adapter_command_run(row: sqlite3.Row) -> AdapterCommandRunRecord:
    return AdapterCommandRunRecord(
        id=row["id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        agent_team_instance_id=row["agent_team_instance_id"],
        agent_instance_id=row["agent_instance_id"],
        adapter_id=row["adapter_id"],
        operation_kind=row["operation_kind"],
        argv=_loads_list(row["argv_json"]),
        cwd=row["cwd"],
        env_hints=_loads_dict(row["env_hints_json"]),
        status=row["status"],
        returncode=row["returncode"],
        started_at=row["started_at"],
        finished_at=row["finished_at"],
        duration_seconds=float(row["duration_seconds"]),
        payload_ref_ids=_loads_list(row["payload_ref_ids_json"]),
        diagnostics=_loads_json_list(row["diagnostics_json"]),
        actor_ref=row["actor_ref"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_adapter_materialization(row: sqlite3.Row) -> AdapterMaterializationRecord:
    return AdapterMaterializationRecord(
        id=row["id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        agent_team_instance_id=row["agent_team_instance_id"],
        adapter_id=row["adapter_id"],
        status=row["status"],
        material_ref_ids=_loads_list(row["material_ref_ids_json"]),
        manifest_ref_ids=_loads_list(row["manifest_ref_ids_json"]),
        path_plan_ids=_loads_list(row["path_plan_ids_json"]),
        diagnostics=_loads_json_list(row["diagnostics_json"]),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        actor_ref=row["actor_ref"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_adapter_launch_attempt(row: sqlite3.Row) -> AdapterLaunchAttemptRecord:
    return AdapterLaunchAttemptRecord(
        id=row["id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        agent_team_instance_id=row["agent_team_instance_id"],
        adapter_id=row["adapter_id"],
        status=row["status"],
        agent_instance_ids=_loads_list(row["agent_instance_ids_json"]),
        command_run_ids=_loads_list(row["command_run_ids_json"]),
        manifest_ref_ids=_loads_list(row["manifest_ref_ids_json"]),
        payload_ref_ids=_loads_list(row["payload_ref_ids_json"]),
        adapter_refs=_loads_json_list(row["adapter_refs_json"]),
        diagnostics=_loads_json_list(row["diagnostics_json"]),
        started_at=row["started_at"],
        updated_at=row["updated_at"],
        finished_at=row["finished_at"],
        actor_ref=row["actor_ref"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_adapter_inspection_snapshot(row: sqlite3.Row) -> AdapterInspectionSnapshotRecord:
    return AdapterInspectionSnapshotRecord(
        id=row["id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        agent_team_instance_id=row["agent_team_instance_id"],
        adapter_id=row["adapter_id"],
        status=row["status"],
        command_run_ids=_loads_list(row["command_run_ids_json"]),
        manifest_ref_ids=_loads_list(row["manifest_ref_ids_json"]),
        snapshot_payload_ref_id=row["snapshot_payload_ref_id"],
        live_observation_summary=_loads_object_dict(row["live_observation_summary_json"]),
        diagnostics=_loads_json_list(row["diagnostics_json"]),
        inspected_at=row["inspected_at"],
        actor_ref=row["actor_ref"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_adapter_stop_outcome(row: sqlite3.Row) -> AdapterStopOutcomeRecord:
    return AdapterStopOutcomeRecord(
        id=row["id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        agent_team_instance_id=row["agent_team_instance_id"],
        adapter_id=row["adapter_id"],
        status=row["status"],
        target_agent_instance_ids=_loads_list(row["target_agent_instance_ids_json"]),
        command_run_ids=_loads_list(row["command_run_ids_json"]),
        payload_ref_ids=_loads_list(row["payload_ref_ids_json"]),
        remaining_live_refs=_loads_json_list(row["remaining_live_refs_json"]),
        diagnostics=_loads_json_list(row["diagnostics_json"]),
        stopped_at=row["stopped_at"],
        actor_ref=row["actor_ref"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )
