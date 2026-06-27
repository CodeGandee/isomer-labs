"""SQLite row mapping helpers for Workspace Runtime records."""

from __future__ import annotations

import sqlite3

from isomer_labs.runtime.models import (
    AgentInstanceRecord,
    AgentTeamInstanceRecord,
    AgentWorkspaceRecord,
    AdapterHandoffDispatchRecord,
    AdapterCommandRunRecord,
    AdapterInspectionSnapshotRecord,
    AdapterLaunchAttemptRecord,
    AdapterManifestRefRecord,
    AdapterMaterializationRecord,
    AdapterPayloadRefRecord,
    AdapterReconciliationRecord,
    AdapterStopOutcomeRecord,
    HandoffNormalizationRecord,
    HandoffRecord,
    PathPlanRecord,
    RuntimeLifecycleRecord,
    SignalObservationRecord,
    TopicEnvironmentReadinessRecord,
)
from isomer_labs.runtime.serialization import (
    _loads_dict,
    _loads_json_list,
    _loads_list,
    _loads_object_dict,
)


def _row_to_path_plan(row: sqlite3.Row) -> PathPlanRecord:
    keys = set(row.keys())
    return PathPlanRecord(
        id=row["id"],
        topic_workspace_id=row["topic_workspace_id"],
        surface=row["surface"],
        path=row["path"],
        source=row["source"],
        source_detail=row["source_detail"],
        created_at=row["created_at"],
        semantic_label=row["semantic_label"] if "semantic_label" in keys else None,
        scope_ref=row["scope_ref"] if "scope_ref" in keys else None,
        compatibility_surface=row["compatibility_surface"] if "compatibility_surface" in keys else None,
        storage_profile=row["storage_profile"] if "storage_profile" in keys else None,
        storage_profile_traits=_loads_object_dict(row["storage_profile_traits_json"]) if "storage_profile_traits_json" in keys else {},
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
    keys = set(row.keys())
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
        topic_agent_team_profile_bundle_ref=(
            row["topic_agent_team_profile_bundle_ref"] if "topic_agent_team_profile_bundle_ref" in keys else None
        ),
        instantiation_packet_ref=row["instantiation_packet_ref"] if "instantiation_packet_ref" in keys else None,
        approval_ref=row["approval_ref"] if "approval_ref" in keys else None,
        project_operator_ref=row["project_operator_ref"] if "project_operator_ref" in keys else None,
        topic_service_agent_refs=_loads_list(row["topic_service_agent_refs_json"]) if "topic_service_agent_refs_json" in keys else [],
        validation_refs=_loads_list(row["validation_refs_json"]) if "validation_refs_json" in keys else [],
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
    keys = set(row.keys())
    return AgentWorkspaceRecord(
        id=row["id"],
        agent_instance_id=row["agent_instance_id"],
        topic_workspace_id=row["topic_workspace_id"],
        path_plan_id=row["path_plan_id"],
        status=row["status"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        agent_name=row["agent_name"] if "agent_name" in keys else None,
        expected_repo_ref=row["expected_repo_ref"] if "expected_repo_ref" in keys else None,
        expected_branch_namespace=row["expected_branch_namespace"] if "expected_branch_namespace" in keys else None,
        current_branch=row["current_branch"] if "current_branch" in keys else None,
        isomer_managed_path_plan_id=row["isomer_managed_path_plan_id"] if "isomer_managed_path_plan_id" in keys else None,
        support_root_path=row["support_root_path"] if "support_root_path" in keys else None,
        boundary_refs=_loads_list(row["boundary_refs_json"]) if "boundary_refs_json" in keys else [],
        generated_link_summary=(
            _loads_object_dict(row["generated_link_summary_json"]) if "generated_link_summary_json" in keys else {}
        ),
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


def _row_to_adapter_handoff_dispatch(row: sqlite3.Row) -> AdapterHandoffDispatchRecord:
    return AdapterHandoffDispatchRecord(
        id=row["id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        handoff_id=row["handoff_id"],
        agent_team_instance_id=row["agent_team_instance_id"],
        source_agent_instance_id=row["source_agent_instance_id"],
        target_agent_instance_id=row["target_agent_instance_id"],
        adapter_id=row["adapter_id"],
        status=row["status"],
        research_task_id=row["research_task_id"],
        run_id=row["run_id"],
        command_run_ids=_loads_list(row["command_run_ids_json"]),
        payload_ref_ids=_loads_list(row["payload_ref_ids_json"]),
        expected_output_refs=_loads_list(row["expected_output_refs_json"]),
        completion_watcher_contract_refs=_loads_list(row["completion_watcher_contract_refs_json"]),
        diagnostics=_loads_json_list(row["diagnostics_json"]),
        actor_ref=row["actor_ref"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_signal_observation(row: sqlite3.Row) -> SignalObservationRecord:
    return SignalObservationRecord(
        id=row["id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        handoff_id=row["handoff_id"],
        run_id=row["run_id"],
        agent_team_instance_id=row["agent_team_instance_id"],
        source_agent_instance_id=row["source_agent_instance_id"],
        target_agent_instance_id=row["target_agent_instance_id"],
        adapter_id=row["adapter_id"],
        observation_kind=row["observation_kind"],
        status=row["status"],
        summary=row["summary"],
        command_run_ids=_loads_list(row["command_run_ids_json"]),
        payload_ref_ids=_loads_list(row["payload_ref_ids_json"]),
        diagnostics=_loads_json_list(row["diagnostics_json"]),
        actor_ref=row["actor_ref"],
        observed_at=row["observed_at"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_handoff_normalization(row: sqlite3.Row) -> HandoffNormalizationRecord:
    return HandoffNormalizationRecord(
        id=row["id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        handoff_id=row["handoff_id"],
        run_id=row["run_id"],
        status=row["status"],
        rationale=row["rationale"],
        signal_observation_ids=_loads_list(row["signal_observation_ids_json"]),
        output_artifact_refs=_loads_list(row["output_artifact_refs_json"]),
        corrective_refs=_loads_list(row["corrective_refs_json"]),
        payload_ref_ids=_loads_list(row["payload_ref_ids_json"]),
        actor_ref=row["actor_ref"],
        created_at=row["created_at"],
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
