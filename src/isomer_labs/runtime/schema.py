"""Schema helpers for Workspace Runtime persistence."""

from __future__ import annotations

from pathlib import Path
import re
import sqlite3
from typing import Any

from isomer_labs.diagnostics import Diagnostic
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.runtime.identifiers import _provenance_ref
from isomer_labs.runtime.models import (
    LIFECYCLE_RECORD_KINDS,
    RUNTIME_DIRECTORIES,
    WORKSPACE_RUNTIME_SCHEMA_VERSION,
    RuntimeLifecycleRecord,
    WorkspaceRuntimeMetadata,
)
from isomer_labs.runtime.serialization import _dumps


CORE_RUNTIME_SCHEMA_TABLES = (
    "runtime_metadata",
    "path_plans",
    "lifecycle_records",
    "lifecycle_transitions",
    "readiness_records",
    "agent_team_instances",
    "agent_instances",
    "agent_workspaces",
    "handoff_records",
    "validation_issues",
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
RUNTIME_SCHEMA_TABLES = (*CORE_RUNTIME_SCHEMA_TABLES, *ADAPTER_RUNTIME_SCHEMA_TABLES)


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
    _ensure_agent_team_instance_provenance_columns(connection)


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
