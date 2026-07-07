"""SQLite persistence helpers for Workspace Runtime."""

from __future__ import annotations

from pathlib import Path
import json
import re
import sqlite3
from typing import Any, Callable

from isomer_labs.core.diagnostics import Diagnostic
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.runtime.records import (
    LIFECYCLE_RECORD_KINDS,
    RUNTIME_DIRECTORIES,
    WORKSPACE_RUNTIME_SCHEMA_VERSION,
    AgentInstanceRecord,
    AgentTeamInstanceRecord,
    AgentWorkspaceRecord,
    ArtifactFormatRegistrationRecord,
    AdapterCommandRunRecord,
    AdapterHandoffDispatchRecord,
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
    ResearchIdea,
    ResearchIdeaGenerationGroup,
    ResearchIdeaLineageEdge,
    ResearchIdeaRealization,
    ResearchRecordGenerationGroup,
    ResearchRecordLineageEdge,
    ResetCheckpointRecord,
    ResetOutcomeRecord,
    ResetPlanActionRecord,
    ResetPlanRecord,
    RuntimeLifecycleRecord,
    SignalObservationRecord,
    StructuredResearchPayloadRecord,
    TopicEnvironmentReadinessRecord,
    WorkspaceRuntimeMetadata,
    _provenance_ref,
)

def _dumps(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _loads_dict(value: str) -> dict[str, str]:
    loaded = json.loads(value)
    if not isinstance(loaded, dict):
        return {}
    return {str(key): str(item) for key, item in loaded.items() if isinstance(item, str)}


def _loads_object_dict(value: str) -> dict[str, object]:
    loaded = json.loads(value)
    if not isinstance(loaded, dict):
        return {}
    return {str(key): item for key, item in loaded.items()}


def _loads_json_list(value: str) -> list[dict[str, object]]:
    loaded = json.loads(value)
    if not isinstance(loaded, list):
        return []
    return [item for item in loaded if isinstance(item, dict)]


def _loads_list(value: str) -> list[str]:
    loaded = json.loads(value)
    if not isinstance(loaded, list):
        return []
    return [str(item) for item in loaded if isinstance(item, str)]

def _table_names(connection: sqlite3.Connection) -> set[str]:
    return {
        row["name"]
        for row in connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    }


def _table_exists(connection: sqlite3.Connection, table_name: str) -> bool:
    return table_name in _table_names(connection)


def run_runtime_transaction(
    store: Any,
    callback: Callable[[Any], None],
) -> None:
    """Run a caller-supplied mutation inside the store transaction boundary."""

    with store.connection:
        callback(store)

def create_reset_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS topic_reset_checkpoints (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            status TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            payload_digest TEXT NOT NULL,
            checkpoint_digest TEXT NOT NULL,
            actor_ref TEXT,
            source_record_id TEXT,
            rendered_markdown_path TEXT,
            rendered_markdown_digest TEXT,
            diagnostics_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_topic_reset_checkpoints_topic
            ON topic_reset_checkpoints (research_topic_id, topic_workspace_id);
        CREATE INDEX IF NOT EXISTS idx_topic_reset_checkpoints_status
            ON topic_reset_checkpoints (status, updated_at);

        CREATE TABLE IF NOT EXISTS topic_reset_plans (
            id TEXT PRIMARY KEY,
            checkpoint_id TEXT NOT NULL,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            status TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            payload_digest TEXT NOT NULL,
            checkpoint_digest TEXT NOT NULL,
            precondition_digest TEXT NOT NULL,
            actor_ref TEXT,
            rendered_markdown_path TEXT,
            rendered_markdown_digest TEXT,
            diagnostics_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_topic_reset_plans_checkpoint
            ON topic_reset_plans (checkpoint_id, created_at);
        CREATE INDEX IF NOT EXISTS idx_topic_reset_plans_topic
            ON topic_reset_plans (research_topic_id, topic_workspace_id);
        CREATE INDEX IF NOT EXISTS idx_topic_reset_plans_status
            ON topic_reset_plans (status, updated_at);

        CREATE TABLE IF NOT EXISTS topic_reset_plan_actions (
            id TEXT PRIMARY KEY,
            plan_id TEXT NOT NULL,
            action TEXT NOT NULL,
            target_kind TEXT NOT NULL,
            target_ref TEXT,
            target_path TEXT,
            semantic_label TEXT,
            source_kind TEXT,
            status TEXT NOT NULL,
            details_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_topic_reset_plan_actions_plan
            ON topic_reset_plan_actions (plan_id, action, target_kind);
        CREATE INDEX IF NOT EXISTS idx_topic_reset_plan_actions_target
            ON topic_reset_plan_actions (target_kind, target_ref);

        CREATE TABLE IF NOT EXISTS topic_reset_outcomes (
            id TEXT PRIMARY KEY,
            checkpoint_id TEXT NOT NULL,
            plan_id TEXT NOT NULL,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            status TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            payload_digest TEXT NOT NULL,
            applied_actions_json TEXT NOT NULL,
            skipped_actions_json TEXT NOT NULL,
            failed_actions_json TEXT NOT NULL,
            diagnostics_json TEXT NOT NULL,
            actor_ref TEXT,
            started_at TEXT NOT NULL,
            finished_at TEXT NOT NULL,
            rendered_markdown_path TEXT,
            rendered_markdown_digest TEXT,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_topic_reset_outcomes_plan
            ON topic_reset_outcomes (plan_id, finished_at);
        CREATE INDEX IF NOT EXISTS idx_topic_reset_outcomes_topic
            ON topic_reset_outcomes (research_topic_id, topic_workspace_id);
        """
    )

CORE_RUNTIME_SCHEMA_TABLES = (
    "runtime_metadata",
    "path_plans",
    "lifecycle_records",
    "lifecycle_transitions",
    "artifact_format_registrations",
    "structured_research_payloads",
    "research_record_index",
    "research_record_edges",
    "research_record_files",
    "research_record_ideas",
    "research_record_routes",
    "research_record_metrics",
    "research_record_claims",
    "research_record_json_facts",
    "topic_reset_checkpoints",
    "topic_reset_plans",
    "topic_reset_plan_actions",
    "topic_reset_outcomes",
    "readiness_records",
    "agent_team_instances",
    "agent_instances",
    "agent_workspaces",
    "handoff_records",
    "validation_issues",
)
LINEAGE_RUNTIME_SCHEMA_TABLES = (
    "research_record_generation_groups",
    "research_record_lineage_edges",
    "research_ideas",
    "research_idea_realizations",
    "research_idea_generation_groups",
    "research_idea_lineage_edges",
)
ADAPTER_RUNTIME_SCHEMA_TABLES = (
    "adapter_handoff_dispatch_records",
    "signal_observation_records",
    "handoff_normalization_records",
    "adapter_manifest_refs",
    "adapter_reconciliation_records",
    "adapter_payload_refs",
    "adapter_command_runs",
    "adapter_materialization_records",
    "adapter_launch_attempts",
    "adapter_inspection_snapshots",
    "adapter_stop_outcomes",
)
RUNTIME_SCHEMA_TABLES = (*CORE_RUNTIME_SCHEMA_TABLES, *LINEAGE_RUNTIME_SCHEMA_TABLES, *ADAPTER_RUNTIME_SCHEMA_TABLES)


def _create_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS runtime_metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS path_plans (
            id TEXT PRIMARY KEY,
            topic_workspace_id TEXT NOT NULL,
            surface TEXT NOT NULL,
            path TEXT NOT NULL,
            source TEXT NOT NULL,
            source_detail TEXT,
            semantic_label TEXT,
            scope_ref TEXT,
            compatibility_surface TEXT,
            storage_profile TEXT,
            storage_profile_traits_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            UNIQUE(topic_workspace_id, surface)
        );

        CREATE TABLE IF NOT EXISTS lifecycle_records (
            id TEXT PRIMARY KEY,
            record_kind TEXT NOT NULL,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            lifecycle_refs_json TEXT NOT NULL,
            transition_metadata_json TEXT NOT NULL,
            content_path TEXT,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS lifecycle_transitions (
            id TEXT PRIMARY KEY,
            record_kind TEXT NOT NULL,
            record_id TEXT NOT NULL,
            previous_status TEXT,
            next_status TEXT,
            actor_ref TEXT,
            rationale TEXT,
            created_at TEXT
        );

        CREATE TABLE IF NOT EXISTS artifact_format_registrations (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            format_profile_ref TEXT NOT NULL,
            schema_ref TEXT NOT NULL,
            template_ref TEXT,
            output_format TEXT NOT NULL,
            source_kind TEXT NOT NULL,
            profile_json TEXT NOT NULL,
            schema_snapshot_path TEXT,
            template_snapshot_path TEXT,
            original_schema_path TEXT,
            original_template_path TEXT,
            profile_digest TEXT NOT NULL,
            schema_digest TEXT NOT NULL,
            template_digest TEXT,
            diagnostics_json TEXT NOT NULL,
            actor_ref TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            provenance_refs_json TEXT NOT NULL,
            UNIQUE(topic_workspace_id, format_profile_ref)
        );

        CREATE INDEX IF NOT EXISTS idx_artifact_format_registrations_topic
            ON artifact_format_registrations (research_topic_id, topic_workspace_id);
        CREATE INDEX IF NOT EXISTS idx_artifact_format_registrations_schema_ref
            ON artifact_format_registrations (schema_ref);
        CREATE INDEX IF NOT EXISTS idx_artifact_format_registrations_template_ref
            ON artifact_format_registrations (template_ref);

        CREATE TABLE IF NOT EXISTS structured_research_payloads (
            id TEXT PRIMARY KEY,
            record_id TEXT NOT NULL UNIQUE,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            format_profile_ref TEXT,
            schema_ref TEXT NOT NULL,
            schema_version TEXT,
            schema_source_kind TEXT NOT NULL,
            template_ref TEXT,
            template_source_kind TEXT,
            payload_json TEXT NOT NULL,
            payload_digest TEXT NOT NULL,
            payload_file_path TEXT,
            payload_media_type TEXT NOT NULL DEFAULT 'application/json',
            payload_manifest_path TEXT,
            payload_source_path TEXT,
            revision_of_record_id TEXT,
            supersedes_record_id TEXT,
            latest_for_semantic_id TEXT,
            legacy_rendered_markdown_path TEXT,
            legacy_rendered_markdown_digest TEXT,
            validation_status TEXT NOT NULL,
            validation_diagnostics_json TEXT NOT NULL,
            render_status TEXT NOT NULL,
            render_diagnostics_json TEXT NOT NULL,
            rendered_markdown_path TEXT,
            rendered_markdown_digest TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_structured_research_payloads_topic
            ON structured_research_payloads (research_topic_id, topic_workspace_id);
        CREATE INDEX IF NOT EXISTS idx_structured_research_payloads_format_profile
            ON structured_research_payloads (format_profile_ref);
        CREATE INDEX IF NOT EXISTS idx_structured_research_payloads_schema_ref
            ON structured_research_payloads (schema_ref);
        CREATE INDEX IF NOT EXISTS idx_structured_research_payloads_template_ref
            ON structured_research_payloads (template_ref);
        CREATE INDEX IF NOT EXISTS idx_structured_research_payloads_status
            ON structured_research_payloads (validation_status, render_status);

        CREATE TABLE IF NOT EXISTS research_record_index (
            record_id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            record_kind TEXT NOT NULL,
            status TEXT NOT NULL,
            placeholder TEXT,
            profile TEXT,
            skill TEXT,
            producer TEXT,
            consumer TEXT,
            format_profile_ref TEXT,
            profile_family TEXT,
            profile_name TEXT,
            title TEXT,
            summary TEXT,
            content_path TEXT,
            payload_file_path TEXT,
            payload_media_type TEXT,
            payload_manifest_path TEXT,
            latest_for_semantic_id TEXT,
            rendered_markdown_path TEXT,
            validation_status TEXT,
            render_status TEXT,
            payload_digest TEXT,
            source_classification TEXT NOT NULL,
            stale INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            indexed_at TEXT NOT NULL,
            metadata_json TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_research_record_index_topic
            ON research_record_index (research_topic_id, topic_workspace_id);
        CREATE INDEX IF NOT EXISTS idx_research_record_index_kind_status
            ON research_record_index (record_kind, status);
        CREATE INDEX IF NOT EXISTS idx_research_record_index_profile
            ON research_record_index (format_profile_ref, profile_family, profile_name);

        CREATE TABLE IF NOT EXISTS research_record_edges (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            source_record_id TEXT NOT NULL,
            target_record_id TEXT NOT NULL,
            relation_kind TEXT NOT NULL,
            relation_role TEXT,
            source_field TEXT,
            source_classification TEXT NOT NULL,
            confidence REAL,
            status TEXT NOT NULL,
            rationale TEXT,
            metadata_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_research_record_edges_topic
            ON research_record_edges (research_topic_id, topic_workspace_id);
        CREATE INDEX IF NOT EXISTS idx_research_record_edges_source
            ON research_record_edges (source_record_id, relation_kind);
        CREATE INDEX IF NOT EXISTS idx_research_record_edges_target
            ON research_record_edges (target_record_id, relation_kind);

        CREATE TABLE IF NOT EXISTS research_record_generation_groups (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            purpose TEXT,
            parent_set_digest TEXT NOT NULL,
            producer_skill TEXT,
            decision_record_id TEXT,
            metadata_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_research_record_generation_groups_topic
            ON research_record_generation_groups (research_topic_id, topic_workspace_id);
        CREATE INDEX IF NOT EXISTS idx_research_record_generation_groups_parent_set
            ON research_record_generation_groups (topic_workspace_id, parent_set_digest);

        CREATE TABLE IF NOT EXISTS research_record_lineage_edges (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            parent_record_id TEXT NOT NULL,
            child_record_id TEXT NOT NULL,
            lineage_kind TEXT NOT NULL,
            parent_role TEXT,
            generation_id TEXT,
            decision_record_id TEXT,
            rationale TEXT,
            status TEXT NOT NULL,
            metadata_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_research_record_lineage_edges_topic
            ON research_record_lineage_edges (research_topic_id, topic_workspace_id);
        CREATE INDEX IF NOT EXISTS idx_research_record_lineage_edges_parent
            ON research_record_lineage_edges (topic_workspace_id, parent_record_id);
        CREATE INDEX IF NOT EXISTS idx_research_record_lineage_edges_child
            ON research_record_lineage_edges (topic_workspace_id, child_record_id);
        CREATE INDEX IF NOT EXISTS idx_research_record_lineage_edges_kind
            ON research_record_lineage_edges (topic_workspace_id, lineage_kind);
        CREATE INDEX IF NOT EXISTS idx_research_record_lineage_edges_generation
            ON research_record_lineage_edges (topic_workspace_id, generation_id);

        CREATE TABLE IF NOT EXISTS research_ideas (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            idea_id TEXT NOT NULL,
            title TEXT NOT NULL,
            one_liner TEXT,
            family TEXT,
            status TEXT NOT NULL,
            visibility TEXT NOT NULL,
            aliases_json TEXT NOT NULL,
            source_record_id TEXT,
            source_json_path TEXT,
            metadata_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            provenance_refs_json TEXT NOT NULL,
            UNIQUE(topic_workspace_id, idea_id)
        );

        CREATE INDEX IF NOT EXISTS idx_research_ideas_topic
            ON research_ideas (research_topic_id, topic_workspace_id);
        CREATE INDEX IF NOT EXISTS idx_research_ideas_visibility
            ON research_ideas (topic_workspace_id, visibility, status);

        CREATE TABLE IF NOT EXISTS research_idea_realizations (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            idea_id TEXT NOT NULL,
            record_id TEXT NOT NULL,
            source_json_path TEXT,
            realization_stage TEXT,
            semantic_id TEXT,
            latest INTEGER NOT NULL,
            metadata_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_research_idea_realizations_idea
            ON research_idea_realizations (topic_workspace_id, idea_id, latest);
        CREATE INDEX IF NOT EXISTS idx_research_idea_realizations_record
            ON research_idea_realizations (topic_workspace_id, record_id);

        CREATE TABLE IF NOT EXISTS research_idea_generation_groups (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            purpose TEXT,
            parent_set_digest TEXT NOT NULL,
            producer_skill TEXT,
            decision_record_id TEXT,
            metadata_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_research_idea_generation_groups_topic
            ON research_idea_generation_groups (research_topic_id, topic_workspace_id);
        CREATE INDEX IF NOT EXISTS idx_research_idea_generation_groups_parent_set
            ON research_idea_generation_groups (topic_workspace_id, parent_set_digest);

        CREATE TABLE IF NOT EXISTS research_idea_lineage_edges (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            parent_idea_id TEXT NOT NULL,
            child_idea_id TEXT NOT NULL,
            lineage_kind TEXT NOT NULL,
            parent_role TEXT,
            generation_id TEXT,
            decision_record_id TEXT,
            rationale TEXT,
            status TEXT NOT NULL,
            confidence REAL,
            metadata_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_research_idea_lineage_edges_topic
            ON research_idea_lineage_edges (research_topic_id, topic_workspace_id);
        CREATE INDEX IF NOT EXISTS idx_research_idea_lineage_edges_parent
            ON research_idea_lineage_edges (topic_workspace_id, parent_idea_id);
        CREATE INDEX IF NOT EXISTS idx_research_idea_lineage_edges_child
            ON research_idea_lineage_edges (topic_workspace_id, child_idea_id);
        CREATE INDEX IF NOT EXISTS idx_research_idea_lineage_edges_kind
            ON research_idea_lineage_edges (topic_workspace_id, lineage_kind);
        CREATE INDEX IF NOT EXISTS idx_research_idea_lineage_edges_generation
            ON research_idea_lineage_edges (topic_workspace_id, generation_id);

        CREATE TABLE IF NOT EXISTS research_record_files (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            record_id TEXT NOT NULL,
            path TEXT NOT NULL,
            file_role TEXT NOT NULL,
            semantic_label TEXT,
            operation_set_id TEXT,
            digest TEXT,
            size_bytes INTEGER,
            media_type TEXT,
            exists_flag INTEGER NOT NULL,
            status TEXT NOT NULL,
            source_field TEXT,
            source_classification TEXT NOT NULL,
            metadata_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_research_record_files_topic
            ON research_record_files (research_topic_id, topic_workspace_id);
        CREATE INDEX IF NOT EXISTS idx_research_record_files_record
            ON research_record_files (record_id, file_role);
        CREATE INDEX IF NOT EXISTS idx_research_record_files_status
            ON research_record_files (status, exists_flag);

        CREATE TABLE IF NOT EXISTS research_record_ideas (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            record_id TEXT NOT NULL,
            idea_id TEXT,
            family TEXT,
            one_liner TEXT,
            status TEXT,
            selected INTEGER NOT NULL,
            source_json_path TEXT,
            metadata_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_research_record_ideas_record
            ON research_record_ideas (record_id, selected);

        CREATE TABLE IF NOT EXISTS research_record_routes (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            record_id TEXT NOT NULL,
            decision TEXT,
            next_route TEXT,
            reason TEXT,
            selected_hypothesis_id TEXT,
            source_json_path TEXT,
            metadata_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_research_record_routes_record
            ON research_record_routes (record_id);

        CREATE TABLE IF NOT EXISTS research_record_metrics (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            record_id TEXT NOT NULL,
            metric_key TEXT NOT NULL,
            metric_value TEXT,
            unit TEXT,
            comparator TEXT,
            scope TEXT,
            source_json_path TEXT,
            metadata_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_research_record_metrics_record
            ON research_record_metrics (record_id, metric_key);

        CREATE TABLE IF NOT EXISTS research_record_claims (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            record_id TEXT NOT NULL,
            claim TEXT,
            metric_key TEXT,
            observed_value TEXT,
            expected TEXT,
            verdict TEXT,
            caveat TEXT,
            source_json_path TEXT,
            metadata_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_research_record_claims_record
            ON research_record_claims (record_id, verdict);

        CREATE TABLE IF NOT EXISTS research_record_json_facts (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            record_id TEXT NOT NULL,
            json_path TEXT NOT NULL,
            value_type TEXT NOT NULL,
            value_text TEXT,
            source_classification TEXT NOT NULL,
            metadata_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_research_record_json_facts_record
            ON research_record_json_facts (record_id, json_path);

        CREATE TABLE IF NOT EXISTS readiness_records (
            sequence INTEGER PRIMARY KEY AUTOINCREMENT,
            id TEXT NOT NULL UNIQUE,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            status TEXT NOT NULL,
            project_pixi_environment_refs_json TEXT NOT NULL,
            standalone_pixi_manifest_refs_json TEXT NOT NULL,
            diagnostics_json TEXT NOT NULL,
            checked_at TEXT NOT NULL,
            actor_ref TEXT,
            repair_service_request_hint TEXT,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS agent_team_instances (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            topic_agent_team_profile_id TEXT NOT NULL,
            domain_agent_team_template_id TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            agent_instance_ids_json TEXT NOT NULL,
            agent_workspace_ids_json TEXT NOT NULL,
            run_ids_json TEXT NOT NULL,
            workflow_stage_cursor_ids_json TEXT NOT NULL,
            blocker_refs_json TEXT NOT NULL,
            handoff_ids_json TEXT NOT NULL,
            provenance_refs_json TEXT NOT NULL,
            topic_agent_team_profile_bundle_ref TEXT,
            instantiation_packet_ref TEXT,
            approval_ref TEXT,
            project_operator_ref TEXT,
            topic_service_agent_refs_json TEXT NOT NULL DEFAULT '[]',
            validation_refs_json TEXT NOT NULL DEFAULT '[]'
        );

        CREATE TABLE IF NOT EXISTS agent_instances (
            id TEXT PRIMARY KEY,
            agent_team_instance_id TEXT NOT NULL,
            agent_role_id TEXT NOT NULL,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            agent_profile_ref TEXT,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS agent_workspaces (
            id TEXT PRIMARY KEY,
            agent_instance_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            path_plan_id TEXT NOT NULL,
            agent_name TEXT,
            expected_repo_ref TEXT,
            expected_branch_namespace TEXT,
            current_branch TEXT,
            isomer_managed_path_plan_id TEXT,
            support_root_path TEXT,
            boundary_refs_json TEXT NOT NULL DEFAULT '[]',
            generated_link_summary_json TEXT NOT NULL DEFAULT '{}',
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS handoff_records (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            source_actor_ref TEXT NOT NULL,
            target_actor_ref TEXT NOT NULL,
            research_task_id TEXT,
            run_id TEXT,
            agent_team_instance_id TEXT,
            status TEXT NOT NULL,
            completion_watcher_contract_refs_json TEXT NOT NULL,
            expected_output_refs_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            stale_after TEXT,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS adapter_handoff_dispatch_records (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            handoff_id TEXT NOT NULL,
            agent_team_instance_id TEXT NOT NULL,
            source_agent_instance_id TEXT NOT NULL,
            target_agent_instance_id TEXT NOT NULL,
            adapter_id TEXT NOT NULL,
            status TEXT NOT NULL,
            research_task_id TEXT,
            run_id TEXT,
            command_run_ids_json TEXT NOT NULL,
            payload_ref_ids_json TEXT NOT NULL,
            expected_output_refs_json TEXT NOT NULL,
            completion_watcher_contract_refs_json TEXT NOT NULL,
            diagnostics_json TEXT NOT NULL,
            actor_ref TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS signal_observation_records (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            handoff_id TEXT NOT NULL,
            run_id TEXT,
            agent_team_instance_id TEXT NOT NULL,
            source_agent_instance_id TEXT,
            target_agent_instance_id TEXT,
            adapter_id TEXT NOT NULL,
            observation_kind TEXT NOT NULL,
            status TEXT NOT NULL,
            summary TEXT NOT NULL,
            command_run_ids_json TEXT NOT NULL,
            payload_ref_ids_json TEXT NOT NULL,
            diagnostics_json TEXT NOT NULL,
            actor_ref TEXT,
            observed_at TEXT NOT NULL,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS handoff_normalization_records (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            handoff_id TEXT NOT NULL,
            run_id TEXT,
            status TEXT NOT NULL,
            rationale TEXT NOT NULL,
            signal_observation_ids_json TEXT NOT NULL,
            output_artifact_refs_json TEXT NOT NULL,
            corrective_refs_json TEXT NOT NULL,
            payload_ref_ids_json TEXT NOT NULL,
            actor_ref TEXT,
            created_at TEXT NOT NULL,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS validation_issues (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            severity TEXT NOT NULL,
            code TEXT NOT NULL,
            concept TEXT NOT NULL,
            message TEXT NOT NULL,
            record_ref TEXT,
            created_at TEXT NOT NULL,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS adapter_manifest_refs (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            agent_team_instance_id TEXT NOT NULL,
            adapter_id TEXT NOT NULL,
            manifest_kind TEXT NOT NULL,
            manifest_path TEXT NOT NULL,
            manifest_digest TEXT NOT NULL,
            source TEXT NOT NULL,
            path_plan_id TEXT,
            agent_instance_ids_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS adapter_reconciliation_records (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            agent_team_instance_id TEXT NOT NULL,
            adapter_id TEXT NOT NULL,
            state TEXT NOT NULL,
            mapping_confidence TEXT NOT NULL,
            manifest_refs_json TEXT NOT NULL,
            manifest_digest_summary_json TEXT NOT NULL,
            live_observation_summary_json TEXT NOT NULL,
            diagnostics_json TEXT NOT NULL,
            actor_ref TEXT,
            created_at TEXT NOT NULL,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS adapter_payload_refs (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            agent_team_instance_id TEXT NOT NULL,
            agent_instance_id TEXT,
            adapter_id TEXT NOT NULL,
            payload_kind TEXT NOT NULL,
            payload_path TEXT NOT NULL,
            payload_digest TEXT NOT NULL,
            source TEXT NOT NULL,
            command_run_id TEXT,
            path_plan_id TEXT,
            created_at TEXT NOT NULL,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS adapter_command_runs (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            agent_team_instance_id TEXT NOT NULL,
            agent_instance_id TEXT,
            adapter_id TEXT NOT NULL,
            operation_kind TEXT NOT NULL,
            argv_json TEXT NOT NULL,
            cwd TEXT,
            env_hints_json TEXT NOT NULL,
            status TEXT NOT NULL,
            returncode INTEGER,
            started_at TEXT NOT NULL,
            finished_at TEXT NOT NULL,
            duration_seconds REAL NOT NULL,
            payload_ref_ids_json TEXT NOT NULL,
            diagnostics_json TEXT NOT NULL,
            actor_ref TEXT,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS adapter_materialization_records (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            agent_team_instance_id TEXT NOT NULL,
            adapter_id TEXT NOT NULL,
            status TEXT NOT NULL,
            material_ref_ids_json TEXT NOT NULL,
            manifest_ref_ids_json TEXT NOT NULL,
            path_plan_ids_json TEXT NOT NULL,
            diagnostics_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            actor_ref TEXT,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS adapter_launch_attempts (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            agent_team_instance_id TEXT NOT NULL,
            adapter_id TEXT NOT NULL,
            status TEXT NOT NULL,
            agent_instance_ids_json TEXT NOT NULL,
            command_run_ids_json TEXT NOT NULL,
            manifest_ref_ids_json TEXT NOT NULL,
            payload_ref_ids_json TEXT NOT NULL,
            adapter_refs_json TEXT NOT NULL,
            diagnostics_json TEXT NOT NULL,
            started_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            finished_at TEXT,
            actor_ref TEXT,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS adapter_inspection_snapshots (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            agent_team_instance_id TEXT NOT NULL,
            adapter_id TEXT NOT NULL,
            status TEXT NOT NULL,
            command_run_ids_json TEXT NOT NULL,
            manifest_ref_ids_json TEXT NOT NULL,
            snapshot_payload_ref_id TEXT,
            live_observation_summary_json TEXT NOT NULL,
            diagnostics_json TEXT NOT NULL,
            inspected_at TEXT NOT NULL,
            actor_ref TEXT,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS adapter_stop_outcomes (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            agent_team_instance_id TEXT NOT NULL,
            adapter_id TEXT NOT NULL,
            status TEXT NOT NULL,
            target_agent_instance_ids_json TEXT NOT NULL,
            command_run_ids_json TEXT NOT NULL,
            payload_ref_ids_json TEXT NOT NULL,
            remaining_live_refs_json TEXT NOT NULL,
            diagnostics_json TEXT NOT NULL,
            stopped_at TEXT NOT NULL,
            actor_ref TEXT,
            provenance_refs_json TEXT NOT NULL
        );
        """
    )
    create_reset_schema(connection)
    _ensure_path_plan_semantic_columns(connection)
    _ensure_agent_team_instance_provenance_columns(connection)
    _ensure_agent_workspace_metadata_columns(connection)
    _ensure_structured_payload_file_columns(connection)
    _ensure_record_index_payload_file_columns(connection)


def _ensure_path_plan_semantic_columns(connection: sqlite3.Connection) -> None:
    columns = {
        row["name"] if isinstance(row, sqlite3.Row) else row[1]
        for row in connection.execute("PRAGMA table_info(path_plans)")
    }
    additions = {
        "semantic_label": "TEXT",
        "scope_ref": "TEXT",
        "compatibility_surface": "TEXT",
        "storage_profile": "TEXT",
        "storage_profile_traits_json": "TEXT NOT NULL DEFAULT '{}'",
    }
    for column, declaration in additions.items():
        if column not in columns:
            connection.execute(f"ALTER TABLE path_plans ADD COLUMN {column} {declaration}")


def _ensure_agent_team_instance_provenance_columns(connection: sqlite3.Connection) -> None:
    columns = {
        row["name"] if isinstance(row, sqlite3.Row) else row[1]
        for row in connection.execute("PRAGMA table_info(agent_team_instances)")
    }
    additions = {
        "topic_agent_team_profile_bundle_ref": "TEXT",
        "instantiation_packet_ref": "TEXT",
        "approval_ref": "TEXT",
        "project_operator_ref": "TEXT",
        "topic_service_agent_refs_json": "TEXT NOT NULL DEFAULT '[]'",
        "validation_refs_json": "TEXT NOT NULL DEFAULT '[]'",
    }
    for column, declaration in additions.items():
        if column not in columns:
            connection.execute(f"ALTER TABLE agent_team_instances ADD COLUMN {column} {declaration}")


def _ensure_agent_workspace_metadata_columns(connection: sqlite3.Connection) -> None:
    columns = {
        row["name"] if isinstance(row, sqlite3.Row) else row[1]
        for row in connection.execute("PRAGMA table_info(agent_workspaces)")
    }
    additions = {
        "agent_name": "TEXT",
        "expected_repo_ref": "TEXT",
        "expected_branch_namespace": "TEXT",
        "current_branch": "TEXT",
        "isomer_managed_path_plan_id": "TEXT",
        "support_root_path": "TEXT",
        "boundary_refs_json": "TEXT NOT NULL DEFAULT '[]'",
        "generated_link_summary_json": "TEXT NOT NULL DEFAULT '{}'",
    }
    for column, declaration in additions.items():
        if column not in columns:
            connection.execute(f"ALTER TABLE agent_workspaces ADD COLUMN {column} {declaration}")


def _ensure_structured_payload_file_columns(connection: sqlite3.Connection) -> None:
    columns = {
        row["name"] if isinstance(row, sqlite3.Row) else row[1]
        for row in connection.execute("PRAGMA table_info(structured_research_payloads)")
    }
    additions = {
        "payload_file_path": "TEXT",
        "payload_media_type": "TEXT NOT NULL DEFAULT 'application/json'",
        "payload_manifest_path": "TEXT",
        "payload_source_path": "TEXT",
        "revision_of_record_id": "TEXT",
        "supersedes_record_id": "TEXT",
        "latest_for_semantic_id": "TEXT",
        "legacy_rendered_markdown_path": "TEXT",
        "legacy_rendered_markdown_digest": "TEXT",
    }
    for column, declaration in additions.items():
        if column not in columns:
            connection.execute(f"ALTER TABLE structured_research_payloads ADD COLUMN {column} {declaration}")


def _ensure_record_index_payload_file_columns(connection: sqlite3.Connection) -> None:
    columns = {
        row["name"] if isinstance(row, sqlite3.Row) else row[1]
        for row in connection.execute("PRAGMA table_info(research_record_index)")
    }
    additions = {
        "payload_file_path": "TEXT",
        "payload_media_type": "TEXT",
        "payload_manifest_path": "TEXT",
        "latest_for_semantic_id": "TEXT",
    }
    for column, declaration in additions.items():
        if column not in columns:
            connection.execute(f"ALTER TABLE research_record_index ADD COLUMN {column} {declaration}")


def _write_metadata(connection: sqlite3.Connection, metadata: WorkspaceRuntimeMetadata) -> None:
    values = metadata.to_json()
    values["provenance_refs"] = _dumps(metadata.provenance_refs)
    for key, value in values.items():
        connection.execute(
            "INSERT OR REPLACE INTO runtime_metadata (key, value) VALUES (?, ?)",
            (key, str(value)),
        )


def _write_initial_lifecycle_records(
    store: Any,
    context: EffectiveTopicContext,
    created_at: str,
) -> None:
    records = [
        RuntimeLifecycleRecord(
            id=f"research-topic:{context.research_topic.id}",
            record_kind="research_topic",
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            status=context.research_topic.status,
            created_at=created_at,
            updated_at=created_at,
            lifecycle_refs={"research_topic_id": context.research_topic.id},
            provenance_refs=[_provenance_ref("research-topic", context.research_topic.id)],
        ),
        RuntimeLifecycleRecord(
            id=f"topic-workspace:{context.topic_workspace_id}",
            record_kind="topic_workspace",
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            status="active",
            created_at=created_at,
            updated_at=created_at,
            lifecycle_refs={"topic_workspace_id": context.topic_workspace_id},
            provenance_refs=[_provenance_ref("topic-workspace", context.topic_workspace_id)],
        ),
    ]
    if context.topic_agent_team_profile_id is not None:
        records.append(
            RuntimeLifecycleRecord(
                id=f"topic-agent-team-profile:{context.topic_agent_team_profile_id}",
                record_kind="topic_agent_team_profile",
                research_topic_id=context.research_topic.id,
                topic_workspace_id=context.topic_workspace_id,
                status="active",
                created_at=created_at,
                updated_at=created_at,
                lifecycle_refs={"topic_agent_team_profile_id": context.topic_agent_team_profile_id},
                provenance_refs=[
                    _provenance_ref("topic-agent-team-profile", context.topic_agent_team_profile_id)
                ],
            )
        )
    for record in records:
        if record.record_kind not in LIFECYCLE_RECORD_KINDS:
            raise ValueError(f"Unsupported lifecycle record kind: {record.record_kind}")
        store.upsert_lifecycle_record(record)


def _validate_open_schema(
    store: Any,
    context: EffectiveTopicContext,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    table_names = {
        row["name"]
        for row in store.connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
    }
    if "runtime_metadata" not in table_names:
        diagnostics.append(
            Diagnostic(
                code="ISO040",
                severity="error",
                concept="Workspace Runtime",
                path=store.db_path,
                message="Workspace Runtime is missing schema metadata.",
            )
        )
        return diagnostics

    try:
        metadata = store.metadata()
    except (KeyError, sqlite3.Error) as exc:
        diagnostics.append(
            Diagnostic(
                code="ISO040",
                severity="error",
                concept="Workspace Runtime",
                path=store.db_path,
                message=f"Workspace Runtime schema metadata could not be read: {exc}.",
            )
        )
        return diagnostics

    if metadata.schema_version != WORKSPACE_RUNTIME_SCHEMA_VERSION:
        diagnostics.append(_unsupported_schema_diagnostic(store.db_path, metadata.schema_version))
        return diagnostics

    missing_tables = sorted(set(CORE_RUNTIME_SCHEMA_TABLES) - table_names)
    if missing_tables:
        diagnostics.append(
            Diagnostic(
                code="ISO040",
                severity="error",
                concept="Workspace Runtime",
                path=store.db_path,
                message=f"Workspace Runtime is missing schema table(s): {', '.join(missing_tables)}.",
            )
        )
    if metadata.research_topic_id != context.research_topic.id:
        diagnostics.append(
            Diagnostic(
                code="ISO041",
                severity="error",
                concept="Workspace Runtime",
                path=store.db_path,
                field="research_topic_id",
                message="Workspace Runtime owner Research Topic does not match the selected context.",
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
                message="Workspace Runtime owner Topic Workspace does not match the selected context.",
            )
        )
    return diagnostics


def _unsupported_schema_diagnostic(path: Path, version: str) -> Diagnostic:
    relation = _schema_version_relation(version)
    return Diagnostic(
        code="ISO040",
        severity="error",
        concept="Workspace Runtime",
        path=path,
        field="schema_version",
        message=(
            f"Workspace Runtime schema version {version} is unsupported "
            f"({relation}; expected {WORKSPACE_RUNTIME_SCHEMA_VERSION})."
        ),
    )


def _schema_version_relation(version: str) -> str:
    observed = _schema_version_number(version)
    current = _schema_version_number(WORKSPACE_RUNTIME_SCHEMA_VERSION)
    if observed is not None and current is not None:
        if observed < current:
            return "older"
        if observed > current:
            return "newer"
    return "different"


def _schema_version_number(version: str) -> int | None:
    match = re.search(r"\.v(\d+)$", version)
    if match is None:
        return None
    return int(match.group(1))


def _ensure_runtime_directories(
    context: EffectiveTopicContext,
    entry_by_surface: dict[str, Any],
) -> list[Path]:
    directories: list[Path] = []
    context.topic_workspace_path.mkdir(parents=True, exist_ok=True)
    for surface in RUNTIME_DIRECTORIES:
        path = entry_by_surface[surface].path if surface in entry_by_surface else context.topic_workspace_path / surface
        path.mkdir(parents=True, exist_ok=True)
        directories.append(path)
    return directories

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


def _row_to_research_record_generation_group(row: sqlite3.Row) -> ResearchRecordGenerationGroup:
    return ResearchRecordGenerationGroup(
        id=row["id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        purpose=row["purpose"],
        parent_set_digest=row["parent_set_digest"],
        producer_skill=row["producer_skill"],
        decision_record_id=row["decision_record_id"],
        metadata=_loads_object_dict(row["metadata_json"]),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_research_record_lineage_edge(row: sqlite3.Row) -> ResearchRecordLineageEdge:
    return ResearchRecordLineageEdge(
        id=row["id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        parent_record_id=row["parent_record_id"],
        child_record_id=row["child_record_id"],
        lineage_kind=row["lineage_kind"],
        parent_role=row["parent_role"],
        generation_id=row["generation_id"],
        decision_record_id=row["decision_record_id"],
        rationale=row["rationale"],
        status=row["status"],
        metadata=_loads_object_dict(row["metadata_json"]),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_research_idea(row: sqlite3.Row) -> ResearchIdea:
    return ResearchIdea(
        id=row["id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        idea_id=row["idea_id"],
        title=row["title"],
        one_liner=row["one_liner"],
        family=row["family"],
        status=row["status"],
        visibility=row["visibility"],
        aliases=_loads_list(row["aliases_json"]),
        source_record_id=row["source_record_id"],
        source_json_path=row["source_json_path"],
        metadata=_loads_object_dict(row["metadata_json"]),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_research_idea_realization(row: sqlite3.Row) -> ResearchIdeaRealization:
    return ResearchIdeaRealization(
        id=row["id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        idea_id=row["idea_id"],
        record_id=row["record_id"],
        source_json_path=row["source_json_path"],
        realization_stage=row["realization_stage"],
        semantic_id=row["semantic_id"],
        latest=bool(row["latest"]),
        metadata=_loads_object_dict(row["metadata_json"]),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_research_idea_generation_group(row: sqlite3.Row) -> ResearchIdeaGenerationGroup:
    return ResearchIdeaGenerationGroup(
        id=row["id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        purpose=row["purpose"],
        parent_set_digest=row["parent_set_digest"],
        producer_skill=row["producer_skill"],
        decision_record_id=row["decision_record_id"],
        metadata=_loads_object_dict(row["metadata_json"]),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_research_idea_lineage_edge(row: sqlite3.Row) -> ResearchIdeaLineageEdge:
    return ResearchIdeaLineageEdge(
        id=row["id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        parent_idea_id=row["parent_idea_id"],
        child_idea_id=row["child_idea_id"],
        lineage_kind=row["lineage_kind"],
        parent_role=row["parent_role"],
        generation_id=row["generation_id"],
        decision_record_id=row["decision_record_id"],
        rationale=row["rationale"],
        status=row["status"],
        confidence=row["confidence"],
        metadata=_loads_object_dict(row["metadata_json"]),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_artifact_format_registration(row: sqlite3.Row) -> ArtifactFormatRegistrationRecord:
    return ArtifactFormatRegistrationRecord(
        id=row["id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        format_profile_ref=row["format_profile_ref"],
        schema_ref=row["schema_ref"],
        template_ref=row["template_ref"],
        output_format=row["output_format"],
        source_kind=row["source_kind"],
        profile_json=_loads_object_dict(row["profile_json"]),
        schema_snapshot_path=row["schema_snapshot_path"],
        template_snapshot_path=row["template_snapshot_path"],
        original_schema_path=row["original_schema_path"],
        original_template_path=row["original_template_path"],
        profile_digest=row["profile_digest"],
        schema_digest=row["schema_digest"],
        template_digest=row["template_digest"],
        diagnostics=_loads_json_list(row["diagnostics_json"]),
        actor_ref=row["actor_ref"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_structured_payload(row: sqlite3.Row) -> StructuredResearchPayloadRecord:
    keys = set(row.keys())
    return StructuredResearchPayloadRecord(
        id=row["id"],
        record_id=row["record_id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        format_profile_ref=row["format_profile_ref"],
        schema_ref=row["schema_ref"],
        schema_version=row["schema_version"],
        schema_source_kind=row["schema_source_kind"],
        template_ref=row["template_ref"],
        template_source_kind=row["template_source_kind"],
        payload_json=_loads_object_dict(row["payload_json"]),
        payload_digest=row["payload_digest"],
        payload_file_path=row["payload_file_path"] if "payload_file_path" in keys else None,
        payload_media_type=row["payload_media_type"] if "payload_media_type" in keys and row["payload_media_type"] is not None else "application/json",
        payload_manifest_path=row["payload_manifest_path"] if "payload_manifest_path" in keys else None,
        payload_source_path=row["payload_source_path"] if "payload_source_path" in keys else None,
        revision_of_record_id=row["revision_of_record_id"] if "revision_of_record_id" in keys else None,
        supersedes_record_id=row["supersedes_record_id"] if "supersedes_record_id" in keys else None,
        latest_for_semantic_id=row["latest_for_semantic_id"] if "latest_for_semantic_id" in keys else None,
        legacy_rendered_markdown_path=row["legacy_rendered_markdown_path"] if "legacy_rendered_markdown_path" in keys else None,
        legacy_rendered_markdown_digest=row["legacy_rendered_markdown_digest"] if "legacy_rendered_markdown_digest" in keys else None,
        validation_status=row["validation_status"],
        validation_diagnostics=_loads_json_list(row["validation_diagnostics_json"]),
        render_status=row["render_status"],
        render_diagnostics=_loads_json_list(row["render_diagnostics_json"]),
        rendered_markdown_path=row["rendered_markdown_path"],
        rendered_markdown_digest=row["rendered_markdown_digest"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_reset_checkpoint(row: sqlite3.Row) -> ResetCheckpointRecord:
    return ResetCheckpointRecord(
        id=row["id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        status=row["status"],
        payload_json=_loads_object_dict(row["payload_json"]),
        payload_digest=row["payload_digest"],
        checkpoint_digest=row["checkpoint_digest"],
        actor_ref=row["actor_ref"],
        source_record_id=row["source_record_id"],
        rendered_markdown_path=row["rendered_markdown_path"],
        rendered_markdown_digest=row["rendered_markdown_digest"],
        diagnostics=_loads_json_list(row["diagnostics_json"]),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_reset_plan(row: sqlite3.Row) -> ResetPlanRecord:
    return ResetPlanRecord(
        id=row["id"],
        checkpoint_id=row["checkpoint_id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        status=row["status"],
        payload_json=_loads_object_dict(row["payload_json"]),
        payload_digest=row["payload_digest"],
        checkpoint_digest=row["checkpoint_digest"],
        precondition_digest=row["precondition_digest"],
        actor_ref=row["actor_ref"],
        rendered_markdown_path=row["rendered_markdown_path"],
        rendered_markdown_digest=row["rendered_markdown_digest"],
        diagnostics=_loads_json_list(row["diagnostics_json"]),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        provenance_refs=_loads_list(row["provenance_refs_json"]),
    )


def _row_to_reset_plan_action(row: sqlite3.Row) -> ResetPlanActionRecord:
    return ResetPlanActionRecord(
        id=row["id"],
        plan_id=row["plan_id"],
        action=row["action"],
        target_kind=row["target_kind"],
        target_ref=row["target_ref"],
        target_path=row["target_path"],
        semantic_label=row["semantic_label"],
        source_kind=row["source_kind"],
        status=row["status"],
        details=_loads_object_dict(row["details_json"]),
        created_at=row["created_at"],
    )


def _row_to_reset_outcome(row: sqlite3.Row) -> ResetOutcomeRecord:
    return ResetOutcomeRecord(
        id=row["id"],
        checkpoint_id=row["checkpoint_id"],
        plan_id=row["plan_id"],
        research_topic_id=row["research_topic_id"],
        topic_workspace_id=row["topic_workspace_id"],
        status=row["status"],
        payload_json=_loads_object_dict(row["payload_json"]),
        payload_digest=row["payload_digest"],
        applied_actions=_loads_json_list(row["applied_actions_json"]),
        skipped_actions=_loads_json_list(row["skipped_actions_json"]),
        failed_actions=_loads_json_list(row["failed_actions_json"]),
        diagnostics=_loads_json_list(row["diagnostics_json"]),
        actor_ref=row["actor_ref"],
        started_at=row["started_at"],
        finished_at=row["finished_at"],
        rendered_markdown_path=row["rendered_markdown_path"],
        rendered_markdown_digest=row["rendered_markdown_digest"],
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
