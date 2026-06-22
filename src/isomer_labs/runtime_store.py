"""SQLite-backed Workspace Runtime store."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json
import re
import sqlite3
from typing import Any, Callable, Mapping

from isomer_labs.diagnostics import Diagnostic, has_errors
from isomer_labs.doctor import DoctorCheck, find_project_pixi_manifest, inspect_topic_pixi
from isomer_labs.models import (
    DomainAgentTeamTemplate,
    EffectiveTopicContext,
    TopicAgentTeamProfile,
)
from isomer_labs.paths import preview_paths
from isomer_labs.runtime_models import (
    ADAPTER_MANIFEST_KINDS,
    ADAPTER_COMMAND_RUN_STATUSES,
    ADAPTER_INSPECTION_STATUSES,
    ADAPTER_LAUNCH_ATTEMPT_STATUSES,
    ADAPTER_MATERIALIZATION_STATUSES,
    ADAPTER_RECONCILIATION_STATES,
    ADAPTER_STOP_OUTCOME_STATUSES,
    HANDOFF_STATUSES,
    LIFECYCLE_RECORD_KINDS,
    READINESS_STATUSES,
    RUNTIME_DIRECTORIES,
    RUNTIME_PATH_SURFACES,
    WORKSPACE_RUNTIME_SCHEMA_VERSION,
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
    ValidationIssueRecord,
    WorkspaceRuntimeMetadata,
    utc_timestamp,
)


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


@dataclass(frozen=True)
class RuntimeInitializationResult:
    runtime_path: Path
    metadata: WorkspaceRuntimeMetadata
    created: bool
    directories: list[Path]
    path_plans: list[PathPlanRecord]

    def to_json(self) -> dict[str, object]:
        return {
            "runtime_path": str(self.runtime_path),
            "metadata": self.metadata.to_json(),
            "created": self.created,
            "directories": [str(path) for path in self.directories],
            "path_plans": [record.to_json() for record in self.path_plans],
        }


@dataclass(frozen=True)
class ReadinessPreparationResult:
    readiness: TopicEnvironmentReadinessRecord | None
    checks: list[DoctorCheck]
    topic_payload: dict[str, object] | None

    def to_json(self) -> dict[str, object]:
        return {
            "readiness": self.readiness.to_json() if self.readiness is not None else None,
            "preparation_status": self.readiness.status if self.readiness is not None else "blocked",
            "checks": [check.to_json() for check in self.checks],
            "topic": self.topic_payload,
        }


@dataclass(frozen=True)
class AgentTeamInstanceCreationResult:
    agent_team_instance: AgentTeamInstanceRecord
    agent_instances: list[AgentInstanceRecord]
    agent_workspaces: list[AgentWorkspaceRecord]
    path_plans: list[PathPlanRecord]
    workflow_stage_cursors: list[RuntimeLifecycleRecord]

    def to_json(self) -> dict[str, object]:
        return {
            "agent_team_instance": self.agent_team_instance.to_json(),
            "agent_instances": [record.to_json() for record in self.agent_instances],
            "agent_workspaces": [record.to_json() for record in self.agent_workspaces],
            "path_plans": [record.to_json() for record in self.path_plans],
            "workflow_stage_cursors": [record.to_json() for record in self.workflow_stage_cursors],
        }


@dataclass(frozen=True)
class AgentTeamInstanceSummary:
    agent_team_instance: AgentTeamInstanceRecord
    agent_instances: list[AgentInstanceRecord]
    agent_workspaces: list[AgentWorkspaceRecord]
    path_plans: list[PathPlanRecord]
    workflow_stage_cursors: list[RuntimeLifecycleRecord]
    handoffs: list[HandoffRecord]
    adapter_manifest_refs: list[AdapterManifestRefRecord] = field(default_factory=list)
    reconciliation_records: list[AdapterReconciliationRecord] = field(default_factory=list)
    adapter_payload_refs: list[AdapterPayloadRefRecord] = field(default_factory=list)
    adapter_command_runs: list[AdapterCommandRunRecord] = field(default_factory=list)
    adapter_materializations: list[AdapterMaterializationRecord] = field(default_factory=list)
    adapter_launch_attempts: list[AdapterLaunchAttemptRecord] = field(default_factory=list)
    adapter_inspection_snapshots: list[AdapterInspectionSnapshotRecord] = field(default_factory=list)
    adapter_stop_outcomes: list[AdapterStopOutcomeRecord] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        return {
            "agent_team_instance": self.agent_team_instance.to_json(),
            "agent_instances": [record.to_json() for record in self.agent_instances],
            "agent_workspaces": [record.to_json() for record in self.agent_workspaces],
            "path_plans": [record.to_json() for record in self.path_plans],
            "workflow_stage_cursors": [record.to_json() for record in self.workflow_stage_cursors],
            "handoffs": [record.to_json() for record in self.handoffs],
            "adapter_manifest_refs": [record.to_json() for record in self.adapter_manifest_refs],
            "reconciliation_records": [record.to_json() for record in self.reconciliation_records],
            "adapter_payload_refs": [record.to_json() for record in self.adapter_payload_refs],
            "adapter_command_runs": [record.to_json() for record in self.adapter_command_runs],
            "adapter_materializations": [record.to_json() for record in self.adapter_materializations],
            "adapter_launch_attempts": [record.to_json() for record in self.adapter_launch_attempts],
            "adapter_inspection_snapshots": [record.to_json() for record in self.adapter_inspection_snapshots],
            "adapter_stop_outcomes": [record.to_json() for record in self.adapter_stop_outcomes],
        }


class WorkspaceRuntimeStore:
    """Small typed wrapper around the Workspace Runtime SQLite database."""

    def __init__(self, db_path: Path, connection: sqlite3.Connection) -> None:
        self.db_path = db_path
        self.connection = connection
        self.connection.row_factory = sqlite3.Row

    def close(self) -> None:
        self.connection.close()

    def metadata(self) -> WorkspaceRuntimeMetadata:
        values = {
            row["key"]: row["value"]
            for row in self.connection.execute("SELECT key, value FROM runtime_metadata ORDER BY key")
        }
        return WorkspaceRuntimeMetadata(
            schema_version=values["schema_version"],
            project_root=values["project_root"],
            project_manifest_path=values["project_manifest_path"],
            research_topic_id=values["research_topic_id"],
            topic_workspace_id=values["topic_workspace_id"],
            topic_workspace_path=values["topic_workspace_path"],
            created_at=values["created_at"],
            updated_at=values["updated_at"],
            provenance_refs=_loads_list(values.get("provenance_refs", "[]")),
        )

    def record_path_plan(
        self,
        *,
        topic_workspace_id: str,
        surface: str,
        path: Path,
        source: str,
        source_detail: str | None,
        created_at: str | None = None,
    ) -> PathPlanRecord:
        timestamp = created_at or utc_timestamp()
        record = PathPlanRecord(
            id=_path_plan_id(topic_workspace_id, surface),
            topic_workspace_id=topic_workspace_id,
            surface=surface,
            path=str(path.resolve(strict=False)),
            source=source,
            source_detail=source_detail,
            created_at=timestamp,
        )
        self.connection.execute(
            """
            INSERT OR IGNORE INTO path_plans
                (id, topic_workspace_id, surface, path, source, source_detail, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.id,
                record.topic_workspace_id,
                record.surface,
                record.path,
                record.source,
                record.source_detail,
                record.created_at,
            ),
        )
        return self.get_path_plan(topic_workspace_id, surface) or record

    def get_path_plan(self, topic_workspace_id: str, surface: str) -> PathPlanRecord | None:
        row = self.connection.execute(
            "SELECT * FROM path_plans WHERE topic_workspace_id = ? AND surface = ?",
            (topic_workspace_id, surface),
        ).fetchone()
        return _row_to_path_plan(row) if row is not None else None

    def list_path_plans(self) -> list[PathPlanRecord]:
        return [
            _row_to_path_plan(row)
            for row in self.connection.execute("SELECT * FROM path_plans ORDER BY topic_workspace_id, surface")
        ]

    def upsert_lifecycle_record(self, record: RuntimeLifecycleRecord) -> None:
        self.connection.execute(
            """
            INSERT INTO lifecycle_records
                (
                    id, record_kind, research_topic_id, topic_workspace_id, status,
                    created_at, updated_at, lifecycle_refs_json, transition_metadata_json,
                    content_path, provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                status = excluded.status,
                updated_at = excluded.updated_at,
                lifecycle_refs_json = excluded.lifecycle_refs_json,
                transition_metadata_json = excluded.transition_metadata_json,
                content_path = excluded.content_path,
                provenance_refs_json = excluded.provenance_refs_json
            """,
            (
                record.id,
                record.record_kind,
                record.research_topic_id,
                record.topic_workspace_id,
                record.status,
                record.created_at,
                record.updated_at,
                _dumps(record.lifecycle_refs),
                _dumps(record.transition_metadata),
                record.content_path,
                _dumps(record.provenance_refs),
            ),
        )

    def list_lifecycle_records(self) -> list[RuntimeLifecycleRecord]:
        return [
            _row_to_lifecycle_record(row)
            for row in self.connection.execute("SELECT * FROM lifecycle_records ORDER BY record_kind, id")
        ]

    def record_lifecycle_transition(
        self,
        *,
        transition_id: str,
        record_kind: str,
        record_id: str,
        previous_status: str | None,
        next_status: str | None,
        actor_ref: str | None,
        rationale: str | None,
        created_at: str | None = None,
    ) -> None:
        self.connection.execute(
            """
            INSERT OR REPLACE INTO lifecycle_transitions
                (
                    id, record_kind, record_id, previous_status, next_status,
                    actor_ref, rationale, created_at
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                transition_id,
                record_kind,
                record_id,
                previous_status,
                next_status,
                actor_ref,
                rationale,
                created_at or utc_timestamp(),
            ),
        )

    def list_lifecycle_transitions(self) -> list[sqlite3.Row]:
        return list(self.connection.execute("SELECT * FROM lifecycle_transitions ORDER BY id"))

    def record_readiness(self, record: TopicEnvironmentReadinessRecord) -> None:
        self.connection.execute(
            """
            INSERT INTO readiness_records
                (
                    id, research_topic_id, topic_workspace_id, status,
                    project_pixi_environment_refs_json, standalone_pixi_manifest_refs_json,
                    diagnostics_json, checked_at, actor_ref, repair_service_request_hint,
                    provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.status,
                _dumps(record.project_pixi_environment_refs),
                _dumps(record.standalone_pixi_manifest_refs),
                _dumps(record.diagnostics),
                record.checked_at,
                record.actor_ref,
                record.repair_service_request_hint,
                _dumps(record.provenance_refs),
            ),
        )

    def list_readiness_records(self) -> list[TopicEnvironmentReadinessRecord]:
        return [
            _row_to_readiness(row)
            for row in self.connection.execute("SELECT * FROM readiness_records ORDER BY sequence, id")
        ]

    def latest_readiness(self) -> TopicEnvironmentReadinessRecord | None:
        row = self.connection.execute(
            "SELECT * FROM readiness_records ORDER BY sequence DESC LIMIT 1"
        ).fetchone()
        return _row_to_readiness(row) if row is not None else None

    def create_agent_team_instance(
        self,
        context: EffectiveTopicContext,
        profile: TopicAgentTeamProfile,
        template: DomainAgentTeamTemplate,
        *,
        requested_id: str | None,
    ) -> tuple[AgentTeamInstanceCreationResult | None, list[Diagnostic]]:
        diagnostics: list[Diagnostic] = []
        readiness = self.latest_readiness()
        if readiness is None or readiness.status != "ready":
            diagnostics.append(
                Diagnostic(
                    code="ISO043",
                    severity="error",
                    concept="Topic Environment Readiness",
                    field="readiness",
                    message=(
                        "Agent Team Instance creation requires a current ready Topic Environment "
                        "Readiness record. Run runtime prepare or dispatch a Service Request for repair."
                    ),
                )
            )
            return None, diagnostics

        team_id = requested_id or self.next_agent_team_instance_id(profile.id)
        if self.get_agent_team_instance(team_id) is not None:
            diagnostics.append(
                Diagnostic(
                    code="ISO046",
                    severity="error",
                    concept="Agent Team Instance",
                    field="id",
                    message=f"Agent Team Instance id already exists in this Workspace Runtime: {team_id}.",
                )
            )
            return None, diagnostics

        active_bindings = [binding for binding in profile.role_bindings if binding.active]
        if not active_bindings:
            diagnostics.append(
                Diagnostic(
                    code="ISO020",
                    severity="error",
                    concept="Topic Agent Team Profile",
                    field="role_bindings",
                    message="Agent Team Instance creation requires at least one active Agent Role binding.",
                )
            )
            return None, diagnostics

        now = utc_timestamp()
        agent_instances: list[AgentInstanceRecord] = []
        agent_workspaces: list[AgentWorkspaceRecord] = []
        path_plans: list[PathPlanRecord] = []
        workflow_stage_cursors: list[RuntimeLifecycleRecord] = []
        agent_instance_ids: list[str] = []
        agent_workspace_ids: list[str] = []

        try:
            with self.connection:
                for binding in active_bindings:
                    agent_id = f"{team_id}-{_slug(binding.role_id)}"
                    workspace_id = f"agent-workspace-{agent_id}"
                    surface = f"agent_workspace:{agent_id}"
                    workspace_path = context.topic_workspace_path / "agents" / agent_id
                    path_plan = self.record_path_plan(
                        topic_workspace_id=context.topic_workspace_id,
                        surface=surface,
                        path=workspace_path,
                        source="default",
                        source_detail=None,
                        created_at=now,
                    )
                    workspace_path.mkdir(parents=True, exist_ok=True)
                    agent_record = AgentInstanceRecord(
                        id=agent_id,
                        agent_team_instance_id=team_id,
                        agent_role_id=binding.role_id,
                        research_topic_id=context.research_topic.id,
                        topic_workspace_id=context.topic_workspace_id,
                        agent_profile_ref=binding.agent_profile_ref,
                        status="planned",
                        created_at=now,
                        updated_at=now,
                        provenance_refs=[_provenance_ref("agent-instance", agent_id)],
                    )
                    workspace_record = AgentWorkspaceRecord(
                        id=workspace_id,
                        agent_instance_id=agent_id,
                        topic_workspace_id=context.topic_workspace_id,
                        path_plan_id=path_plan.id,
                        status="ready",
                        created_at=now,
                        updated_at=now,
                        provenance_refs=[_provenance_ref("agent-workspace", workspace_id)],
                    )
                    self._insert_agent_instance(agent_record)
                    self._insert_agent_workspace(workspace_record)
                    agent_instances.append(agent_record)
                    agent_workspaces.append(workspace_record)
                    path_plans.append(path_plan)
                    agent_instance_ids.append(agent_id)
                    agent_workspace_ids.append(workspace_id)

                for route in template.workflow_stage_routes:
                    cursor_id = f"{team_id}-stage-{_slug(route.workflow_stage)}"
                    cursor = RuntimeLifecycleRecord(
                        id=cursor_id,
                        record_kind="workflow_stage_cursor",
                        research_topic_id=context.research_topic.id,
                        topic_workspace_id=context.topic_workspace_id,
                        status="planned",
                        created_at=now,
                        updated_at=now,
                        lifecycle_refs={
                            "agent_team_instance_id": team_id,
                            "workflow_stage": route.workflow_stage,
                            "owner_role": route.owner_role,
                        },
                        provenance_refs=[_provenance_ref("workflow-stage-cursor", cursor_id)],
                    )
                    self.upsert_lifecycle_record(cursor)
                    workflow_stage_cursors.append(cursor)

                team_record = AgentTeamInstanceRecord(
                    id=team_id,
                    research_topic_id=context.research_topic.id,
                    topic_workspace_id=context.topic_workspace_id,
                    topic_agent_team_profile_id=profile.id,
                    domain_agent_team_template_id=template.id,
                    status="planned",
                    created_at=now,
                    updated_at=now,
                    agent_instance_ids=agent_instance_ids,
                    agent_workspace_ids=agent_workspace_ids,
                    workflow_stage_cursor_ids=[record.id for record in workflow_stage_cursors],
                    provenance_refs=[_provenance_ref("agent-team-instance", team_id)],
                )
                self._insert_agent_team_instance(team_record)
        except sqlite3.Error as exc:
            diagnostics.append(
                Diagnostic(
                    code="ISO040",
                    severity="error",
                    concept="Workspace Runtime",
                    message=f"Agent Team Instance transaction failed: {exc}.",
                )
            )
            return None, diagnostics

        return (
            AgentTeamInstanceCreationResult(
                agent_team_instance=team_record,
                agent_instances=agent_instances,
                agent_workspaces=agent_workspaces,
                path_plans=path_plans,
                workflow_stage_cursors=workflow_stage_cursors,
            ),
            diagnostics,
        )

    def next_agent_team_instance_id(self, profile_id: str) -> str:
        prefix = f"ati-{_slug(profile_id)}"
        count = self.connection.execute(
            "SELECT COUNT(*) AS count FROM agent_team_instances WHERE id LIKE ?",
            (f"{prefix}-%",),
        ).fetchone()["count"]
        return f"{prefix}-{int(count) + 1:03d}"

    def get_agent_team_instance(self, team_id: str) -> AgentTeamInstanceRecord | None:
        row = self.connection.execute(
            "SELECT * FROM agent_team_instances WHERE id = ?",
            (team_id,),
        ).fetchone()
        return _row_to_agent_team_instance(row) if row is not None else None

    def list_agent_team_instances(self) -> list[AgentTeamInstanceRecord]:
        return [
            _row_to_agent_team_instance(row)
            for row in self.connection.execute("SELECT * FROM agent_team_instances ORDER BY id")
        ]

    def get_agent_team_instance_summary(self, team_id: str) -> AgentTeamInstanceSummary | None:
        team = self.get_agent_team_instance(team_id)
        if team is None:
            return None
        agent_instances = [
            _row_to_agent_instance(row)
            for row in self.connection.execute(
                "SELECT * FROM agent_instances WHERE agent_team_instance_id = ? ORDER BY id",
                (team_id,),
            )
        ]
        agent_instance_ids = [record.id for record in agent_instances]
        agent_workspaces = [
            _row_to_agent_workspace(row)
            for row in self.connection.execute(
                """
                SELECT aw.*
                FROM agent_workspaces aw
                JOIN agent_instances ai ON ai.id = aw.agent_instance_id
                WHERE ai.agent_team_instance_id = ?
                ORDER BY aw.id
                """,
                (team_id,),
            )
        ]
        path_plan_ids = [workspace.path_plan_id for workspace in agent_workspaces]
        path_plans = self._path_plans_by_ids(path_plan_ids)
        workflow_stage_cursors = [
            record
            for record in self.list_lifecycle_records()
            if record.record_kind == "workflow_stage_cursor"
            and record.lifecycle_refs.get("agent_team_instance_id") == team_id
        ]
        handoffs = [
            _row_to_handoff(row)
            for row in self.connection.execute(
                "SELECT * FROM handoff_records WHERE agent_team_instance_id = ? ORDER BY id",
                (team_id,),
            )
        ]
        adapter_manifest_refs = self.list_adapter_manifest_refs(agent_team_instance_id=team_id)
        reconciliation_records = self.list_adapter_reconciliation_records(agent_team_instance_id=team_id)
        adapter_payload_refs = self.list_adapter_payload_refs(agent_team_instance_id=team_id)
        adapter_command_runs = self.list_adapter_command_runs(agent_team_instance_id=team_id)
        adapter_materializations = self.list_adapter_materializations(agent_team_instance_id=team_id)
        adapter_launch_attempts = self.list_adapter_launch_attempts(agent_team_instance_id=team_id)
        adapter_inspection_snapshots = self.list_adapter_inspection_snapshots(agent_team_instance_id=team_id)
        adapter_stop_outcomes = self.list_adapter_stop_outcomes(agent_team_instance_id=team_id)
        return AgentTeamInstanceSummary(
            agent_team_instance=team,
            agent_instances=[
                record for record in agent_instances if record.id in set(agent_instance_ids)
            ],
            agent_workspaces=agent_workspaces,
            path_plans=path_plans,
            workflow_stage_cursors=workflow_stage_cursors,
            handoffs=handoffs,
            adapter_manifest_refs=adapter_manifest_refs,
            reconciliation_records=reconciliation_records,
            adapter_payload_refs=adapter_payload_refs,
            adapter_command_runs=adapter_command_runs,
            adapter_materializations=adapter_materializations,
            adapter_launch_attempts=adapter_launch_attempts,
            adapter_inspection_snapshots=adapter_inspection_snapshots,
            adapter_stop_outcomes=adapter_stop_outcomes,
        )

    def list_agent_instances(self) -> list[AgentInstanceRecord]:
        return [
            _row_to_agent_instance(row)
            for row in self.connection.execute("SELECT * FROM agent_instances ORDER BY id")
        ]

    def list_agent_workspaces(self) -> list[AgentWorkspaceRecord]:
        return [
            _row_to_agent_workspace(row)
            for row in self.connection.execute("SELECT * FROM agent_workspaces ORDER BY id")
        ]

    def record_handoff(self, record: HandoffRecord) -> None:
        if record.status not in HANDOFF_STATUSES:
            raise ValueError(f"Unsupported handoff status: {record.status}")
        self.connection.execute(
            """
            INSERT OR REPLACE INTO handoff_records
                (
                    id, research_topic_id, topic_workspace_id, source_actor_ref,
                    target_actor_ref, research_task_id, run_id, agent_team_instance_id,
                    status, completion_watcher_contract_refs_json,
                    expected_output_refs_json, created_at, updated_at, stale_after,
                    provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.source_actor_ref,
                record.target_actor_ref,
                record.research_task_id,
                record.run_id,
                record.agent_team_instance_id,
                record.status,
                _dumps(record.completion_watcher_contract_refs),
                _dumps(record.expected_output_refs),
                record.created_at,
                record.updated_at,
                record.stale_after,
                _dumps(record.provenance_refs),
            ),
        )

    def list_handoffs(self) -> list[HandoffRecord]:
        return [
            _row_to_handoff(row)
            for row in self.connection.execute("SELECT * FROM handoff_records ORDER BY id")
        ]

    def record_validation_issue(self, issue: ValidationIssueRecord) -> None:
        self.connection.execute(
            """
            INSERT OR REPLACE INTO validation_issues
                (
                    id, research_topic_id, topic_workspace_id, severity, code,
                    concept, message, record_ref, created_at, provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                issue.id,
                issue.research_topic_id,
                issue.topic_workspace_id,
                issue.severity,
                issue.code,
                issue.concept,
                issue.message,
                issue.record_ref,
                issue.created_at,
                _dumps(issue.provenance_refs),
            ),
        )

    def record_adapter_manifest_ref(self, record: AdapterManifestRefRecord) -> None:
        if record.manifest_kind not in ADAPTER_MANIFEST_KINDS:
            raise ValueError(f"Unsupported adapter manifest kind: {record.manifest_kind}")
        self.connection.execute(
            """
            INSERT INTO adapter_manifest_refs
                (
                    id, research_topic_id, topic_workspace_id, agent_team_instance_id,
                    adapter_id, manifest_kind, manifest_path, manifest_digest, source,
                    path_plan_id, agent_instance_ids_json, created_at, updated_at,
                    provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                manifest_path = excluded.manifest_path,
                manifest_digest = excluded.manifest_digest,
                source = excluded.source,
                path_plan_id = excluded.path_plan_id,
                agent_instance_ids_json = excluded.agent_instance_ids_json,
                updated_at = excluded.updated_at,
                provenance_refs_json = excluded.provenance_refs_json
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.agent_team_instance_id,
                record.adapter_id,
                record.manifest_kind,
                record.manifest_path,
                record.manifest_digest,
                record.source,
                record.path_plan_id,
                _dumps(record.agent_instance_ids),
                record.created_at,
                record.updated_at,
                _dumps(record.provenance_refs),
            ),
        )

    def list_adapter_manifest_refs(
        self,
        *,
        agent_team_instance_id: str | None = None,
    ) -> list[AdapterManifestRefRecord]:
        if not _table_exists(self.connection, "adapter_manifest_refs"):
            return []
        if agent_team_instance_id is None:
            rows = self.connection.execute(
                "SELECT * FROM adapter_manifest_refs ORDER BY agent_team_instance_id, manifest_kind, id"
            )
        else:
            rows = self.connection.execute(
                "SELECT * FROM adapter_manifest_refs WHERE agent_team_instance_id = ? ORDER BY manifest_kind, id",
                (agent_team_instance_id,),
            )
        return [_row_to_adapter_manifest_ref(row) for row in rows]

    def get_adapter_manifest_ref(
        self,
        *,
        agent_team_instance_id: str,
        manifest_kind: str,
    ) -> AdapterManifestRefRecord | None:
        if not _table_exists(self.connection, "adapter_manifest_refs"):
            return None
        row = self.connection.execute(
            """
            SELECT * FROM adapter_manifest_refs
            WHERE agent_team_instance_id = ? AND manifest_kind = ?
            ORDER BY updated_at DESC, id DESC
            LIMIT 1
            """,
            (agent_team_instance_id, manifest_kind),
        ).fetchone()
        return _row_to_adapter_manifest_ref(row) if row is not None else None

    def record_adapter_reconciliation(self, record: AdapterReconciliationRecord) -> None:
        if record.state not in ADAPTER_RECONCILIATION_STATES:
            raise ValueError(f"Unsupported adapter reconciliation state: {record.state}")
        self.connection.execute(
            """
            INSERT OR REPLACE INTO adapter_reconciliation_records
                (
                    id, research_topic_id, topic_workspace_id, agent_team_instance_id,
                    adapter_id, state, mapping_confidence, manifest_refs_json,
                    manifest_digest_summary_json, live_observation_summary_json,
                    diagnostics_json, actor_ref, created_at, provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.agent_team_instance_id,
                record.adapter_id,
                record.state,
                record.mapping_confidence,
                _dumps(record.manifest_refs),
                _dumps(record.manifest_digest_summary),
                _dumps(record.live_observation_summary),
                _dumps(record.diagnostics),
                record.actor_ref,
                record.created_at,
                _dumps(record.provenance_refs),
            ),
        )

    def list_adapter_reconciliation_records(
        self,
        *,
        agent_team_instance_id: str | None = None,
    ) -> list[AdapterReconciliationRecord]:
        if not _table_exists(self.connection, "adapter_reconciliation_records"):
            return []
        if agent_team_instance_id is None:
            rows = self.connection.execute(
                "SELECT * FROM adapter_reconciliation_records ORDER BY created_at, id"
            )
        else:
            rows = self.connection.execute(
                """
                SELECT * FROM adapter_reconciliation_records
                WHERE agent_team_instance_id = ?
                ORDER BY created_at, id
                """,
                (agent_team_instance_id,),
            )
        return [_row_to_adapter_reconciliation_record(row) for row in rows]

    def latest_adapter_reconciliation_record(
        self,
        *,
        agent_team_instance_id: str,
    ) -> AdapterReconciliationRecord | None:
        if not _table_exists(self.connection, "adapter_reconciliation_records"):
            return None
        row = self.connection.execute(
            """
            SELECT * FROM adapter_reconciliation_records
            WHERE agent_team_instance_id = ?
            ORDER BY created_at DESC, id DESC
            LIMIT 1
            """,
            (agent_team_instance_id,),
        ).fetchone()
        return _row_to_adapter_reconciliation_record(row) if row is not None else None

    def record_adapter_payload_ref(self, record: AdapterPayloadRefRecord) -> None:
        self.connection.execute(
            """
            INSERT OR REPLACE INTO adapter_payload_refs
                (
                    id, research_topic_id, topic_workspace_id, agent_team_instance_id,
                    agent_instance_id, adapter_id, payload_kind, payload_path,
                    payload_digest, source, command_run_id, path_plan_id, created_at,
                    provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.agent_team_instance_id,
                record.agent_instance_id,
                record.adapter_id,
                record.payload_kind,
                record.payload_path,
                record.payload_digest,
                record.source,
                record.command_run_id,
                record.path_plan_id,
                record.created_at,
                _dumps(record.provenance_refs),
            ),
        )

    def list_adapter_payload_refs(
        self,
        *,
        agent_team_instance_id: str | None = None,
    ) -> list[AdapterPayloadRefRecord]:
        if not _table_exists(self.connection, "adapter_payload_refs"):
            return []
        if agent_team_instance_id is None:
            rows = self.connection.execute("SELECT * FROM adapter_payload_refs ORDER BY created_at, id")
        else:
            rows = self.connection.execute(
                """
                SELECT * FROM adapter_payload_refs
                WHERE agent_team_instance_id = ?
                ORDER BY created_at, id
                """,
                (agent_team_instance_id,),
            )
        return [_row_to_adapter_payload_ref(row) for row in rows]

    def record_adapter_command_run(self, record: AdapterCommandRunRecord) -> None:
        if record.status not in ADAPTER_COMMAND_RUN_STATUSES:
            raise ValueError(f"Unsupported adapter command run status: {record.status}")
        self.connection.execute(
            """
            INSERT OR REPLACE INTO adapter_command_runs
                (
                    id, research_topic_id, topic_workspace_id, agent_team_instance_id,
                    agent_instance_id, adapter_id, operation_kind, argv_json, cwd,
                    env_hints_json, status, returncode, started_at, finished_at,
                    duration_seconds, payload_ref_ids_json, diagnostics_json,
                    actor_ref, provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.agent_team_instance_id,
                record.agent_instance_id,
                record.adapter_id,
                record.operation_kind,
                _dumps(record.argv),
                record.cwd,
                _dumps(record.env_hints),
                record.status,
                record.returncode,
                record.started_at,
                record.finished_at,
                record.duration_seconds,
                _dumps(record.payload_ref_ids),
                _dumps(record.diagnostics),
                record.actor_ref,
                _dumps(record.provenance_refs),
            ),
        )

    def list_adapter_command_runs(
        self,
        *,
        agent_team_instance_id: str | None = None,
    ) -> list[AdapterCommandRunRecord]:
        if not _table_exists(self.connection, "adapter_command_runs"):
            return []
        if agent_team_instance_id is None:
            rows = self.connection.execute("SELECT * FROM adapter_command_runs ORDER BY started_at, id")
        else:
            rows = self.connection.execute(
                """
                SELECT * FROM adapter_command_runs
                WHERE agent_team_instance_id = ?
                ORDER BY started_at, id
                """,
                (agent_team_instance_id,),
            )
        return [_row_to_adapter_command_run(row) for row in rows]

    def record_adapter_materialization(self, record: AdapterMaterializationRecord) -> None:
        if record.status not in ADAPTER_MATERIALIZATION_STATUSES:
            raise ValueError(f"Unsupported adapter materialization status: {record.status}")
        self.connection.execute(
            """
            INSERT OR REPLACE INTO adapter_materialization_records
                (
                    id, research_topic_id, topic_workspace_id, agent_team_instance_id,
                    adapter_id, status, material_ref_ids_json, manifest_ref_ids_json,
                    path_plan_ids_json, diagnostics_json, created_at, updated_at,
                    actor_ref, provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.agent_team_instance_id,
                record.adapter_id,
                record.status,
                _dumps(record.material_ref_ids),
                _dumps(record.manifest_ref_ids),
                _dumps(record.path_plan_ids),
                _dumps(record.diagnostics),
                record.created_at,
                record.updated_at,
                record.actor_ref,
                _dumps(record.provenance_refs),
            ),
        )

    def list_adapter_materializations(
        self,
        *,
        agent_team_instance_id: str | None = None,
    ) -> list[AdapterMaterializationRecord]:
        if not _table_exists(self.connection, "adapter_materialization_records"):
            return []
        if agent_team_instance_id is None:
            rows = self.connection.execute("SELECT * FROM adapter_materialization_records ORDER BY created_at, id")
        else:
            rows = self.connection.execute(
                """
                SELECT * FROM adapter_materialization_records
                WHERE agent_team_instance_id = ?
                ORDER BY created_at, id
                """,
                (agent_team_instance_id,),
            )
        return [_row_to_adapter_materialization(row) for row in rows]

    def record_adapter_launch_attempt(self, record: AdapterLaunchAttemptRecord) -> None:
        if record.status not in ADAPTER_LAUNCH_ATTEMPT_STATUSES:
            raise ValueError(f"Unsupported adapter launch attempt status: {record.status}")
        self.connection.execute(
            """
            INSERT OR REPLACE INTO adapter_launch_attempts
                (
                    id, research_topic_id, topic_workspace_id, agent_team_instance_id,
                    adapter_id, status, agent_instance_ids_json, command_run_ids_json,
                    manifest_ref_ids_json, payload_ref_ids_json, adapter_refs_json,
                    diagnostics_json, started_at, updated_at, finished_at, actor_ref,
                    provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.agent_team_instance_id,
                record.adapter_id,
                record.status,
                _dumps(record.agent_instance_ids),
                _dumps(record.command_run_ids),
                _dumps(record.manifest_ref_ids),
                _dumps(record.payload_ref_ids),
                _dumps(record.adapter_refs),
                _dumps(record.diagnostics),
                record.started_at,
                record.updated_at,
                record.finished_at,
                record.actor_ref,
                _dumps(record.provenance_refs),
            ),
        )

    def list_adapter_launch_attempts(
        self,
        *,
        agent_team_instance_id: str | None = None,
    ) -> list[AdapterLaunchAttemptRecord]:
        if not _table_exists(self.connection, "adapter_launch_attempts"):
            return []
        if agent_team_instance_id is None:
            rows = self.connection.execute("SELECT * FROM adapter_launch_attempts ORDER BY started_at, id")
        else:
            rows = self.connection.execute(
                """
                SELECT * FROM adapter_launch_attempts
                WHERE agent_team_instance_id = ?
                ORDER BY started_at, id
                """,
                (agent_team_instance_id,),
            )
        return [_row_to_adapter_launch_attempt(row) for row in rows]

    def latest_adapter_launch_attempt(
        self,
        *,
        agent_team_instance_id: str,
    ) -> AdapterLaunchAttemptRecord | None:
        if not _table_exists(self.connection, "adapter_launch_attempts"):
            return None
        row = self.connection.execute(
            """
            SELECT * FROM adapter_launch_attempts
            WHERE agent_team_instance_id = ?
            ORDER BY started_at DESC, id DESC
            LIMIT 1
            """,
            (agent_team_instance_id,),
        ).fetchone()
        return _row_to_adapter_launch_attempt(row) if row is not None else None

    def record_adapter_inspection_snapshot(self, record: AdapterInspectionSnapshotRecord) -> None:
        if record.status not in ADAPTER_INSPECTION_STATUSES:
            raise ValueError(f"Unsupported adapter inspection status: {record.status}")
        self.connection.execute(
            """
            INSERT OR REPLACE INTO adapter_inspection_snapshots
                (
                    id, research_topic_id, topic_workspace_id, agent_team_instance_id,
                    adapter_id, status, command_run_ids_json, manifest_ref_ids_json,
                    snapshot_payload_ref_id, live_observation_summary_json,
                    diagnostics_json, inspected_at, actor_ref, provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.agent_team_instance_id,
                record.adapter_id,
                record.status,
                _dumps(record.command_run_ids),
                _dumps(record.manifest_ref_ids),
                record.snapshot_payload_ref_id,
                _dumps(record.live_observation_summary),
                _dumps(record.diagnostics),
                record.inspected_at,
                record.actor_ref,
                _dumps(record.provenance_refs),
            ),
        )

    def list_adapter_inspection_snapshots(
        self,
        *,
        agent_team_instance_id: str | None = None,
    ) -> list[AdapterInspectionSnapshotRecord]:
        if not _table_exists(self.connection, "adapter_inspection_snapshots"):
            return []
        if agent_team_instance_id is None:
            rows = self.connection.execute("SELECT * FROM adapter_inspection_snapshots ORDER BY inspected_at, id")
        else:
            rows = self.connection.execute(
                """
                SELECT * FROM adapter_inspection_snapshots
                WHERE agent_team_instance_id = ?
                ORDER BY inspected_at, id
                """,
                (agent_team_instance_id,),
            )
        return [_row_to_adapter_inspection_snapshot(row) for row in rows]

    def record_adapter_stop_outcome(self, record: AdapterStopOutcomeRecord) -> None:
        if record.status not in ADAPTER_STOP_OUTCOME_STATUSES:
            raise ValueError(f"Unsupported adapter stop outcome status: {record.status}")
        self.connection.execute(
            """
            INSERT OR REPLACE INTO adapter_stop_outcomes
                (
                    id, research_topic_id, topic_workspace_id, agent_team_instance_id,
                    adapter_id, status, target_agent_instance_ids_json,
                    command_run_ids_json, payload_ref_ids_json, remaining_live_refs_json,
                    diagnostics_json, stopped_at, actor_ref, provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.agent_team_instance_id,
                record.adapter_id,
                record.status,
                _dumps(record.target_agent_instance_ids),
                _dumps(record.command_run_ids),
                _dumps(record.payload_ref_ids),
                _dumps(record.remaining_live_refs),
                _dumps(record.diagnostics),
                record.stopped_at,
                record.actor_ref,
                _dumps(record.provenance_refs),
            ),
        )

    def list_adapter_stop_outcomes(
        self,
        *,
        agent_team_instance_id: str | None = None,
    ) -> list[AdapterStopOutcomeRecord]:
        if not _table_exists(self.connection, "adapter_stop_outcomes"):
            return []
        if agent_team_instance_id is None:
            rows = self.connection.execute("SELECT * FROM adapter_stop_outcomes ORDER BY stopped_at, id")
        else:
            rows = self.connection.execute(
                """
                SELECT * FROM adapter_stop_outcomes
                WHERE agent_team_instance_id = ?
                ORDER BY stopped_at, id
                """,
                (agent_team_instance_id,),
            )
        return [_row_to_adapter_stop_outcome(row) for row in rows]

    def count_records(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        table_names = _table_names(self.connection)
        for table in RUNTIME_SCHEMA_TABLES:
            if table not in table_names:
                counts[table] = 0
            else:
                counts[table] = int(
                    self.connection.execute(f"SELECT COUNT(*) AS count FROM {table}").fetchone()["count"]
                )
        return counts

    def _insert_agent_team_instance(self, record: AgentTeamInstanceRecord) -> None:
        self.connection.execute(
            """
            INSERT INTO agent_team_instances
                (
                    id, research_topic_id, topic_workspace_id,
                    topic_agent_team_profile_id, domain_agent_team_template_id,
                    status, created_at, updated_at, agent_instance_ids_json,
                    agent_workspace_ids_json, run_ids_json,
                    workflow_stage_cursor_ids_json, blocker_refs_json,
                    handoff_ids_json, provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.topic_agent_team_profile_id,
                record.domain_agent_team_template_id,
                record.status,
                record.created_at,
                record.updated_at,
                _dumps(record.agent_instance_ids),
                _dumps(record.agent_workspace_ids),
                _dumps(record.run_ids),
                _dumps(record.workflow_stage_cursor_ids),
                _dumps(record.blocker_refs),
                _dumps(record.handoff_ids),
                _dumps(record.provenance_refs),
            ),
        )

    def _insert_agent_instance(self, record: AgentInstanceRecord) -> None:
        self.connection.execute(
            """
            INSERT INTO agent_instances
                (
                    id, agent_team_instance_id, agent_role_id, research_topic_id,
                    topic_workspace_id, agent_profile_ref, status, created_at,
                    updated_at, provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.id,
                record.agent_team_instance_id,
                record.agent_role_id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.agent_profile_ref,
                record.status,
                record.created_at,
                record.updated_at,
                _dumps(record.provenance_refs),
            ),
        )

    def _insert_agent_workspace(self, record: AgentWorkspaceRecord) -> None:
        self.connection.execute(
            """
            INSERT INTO agent_workspaces
                (
                    id, agent_instance_id, topic_workspace_id, path_plan_id, status,
                    created_at, updated_at, provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.id,
                record.agent_instance_id,
                record.topic_workspace_id,
                record.path_plan_id,
                record.status,
                record.created_at,
                record.updated_at,
                _dumps(record.provenance_refs),
            ),
        )

    def _path_plans_by_ids(self, path_plan_ids: list[str]) -> list[PathPlanRecord]:
        if not path_plan_ids:
            return []
        placeholders = ", ".join("?" for _ in path_plan_ids)
        rows = self.connection.execute(
            f"SELECT * FROM path_plans WHERE id IN ({placeholders}) ORDER BY id",
            tuple(path_plan_ids),
        )
        return [_row_to_path_plan(row) for row in rows]


def initialize_workspace_runtime(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
) -> tuple[RuntimeInitializationResult | None, list[Diagnostic]]:
    entries, diagnostics = preview_paths(context, env=env)
    if has_errors(diagnostics):
        return None, diagnostics
    entry_by_surface = {entry.surface: entry for entry in entries}
    db_path = entry_by_surface["workspace_runtime_db"].path
    existed = db_path.exists()

    if existed:
        store, open_diagnostics = open_workspace_runtime(context, env=env, read_only=False)
        diagnostics.extend(open_diagnostics)
        if store is None:
            return None, diagnostics
        directories = _ensure_runtime_directories(context, entry_by_surface)
        path_plans = store.list_path_plans()
        result = RuntimeInitializationResult(
            runtime_path=db_path,
            metadata=store.metadata(),
            created=False,
            directories=directories,
            path_plans=path_plans,
        )
        store.close()
        return result, diagnostics

    directories = _ensure_runtime_directories(context, entry_by_surface)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    store = WorkspaceRuntimeStore(db_path, connection)
    now = utc_timestamp()
    metadata = WorkspaceRuntimeMetadata(
        schema_version=WORKSPACE_RUNTIME_SCHEMA_VERSION,
        project_root=str(context.project.root),
        project_manifest_path=str(context.project.manifest_path),
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        topic_workspace_path=str(context.topic_workspace_path),
        created_at=now,
        updated_at=now,
        provenance_refs=[_provenance_ref("workspace-runtime", context.topic_workspace_id)],
    )
    try:
        with connection:
            _create_schema(connection)
            _write_metadata(connection, metadata)
            _write_initial_lifecycle_records(store, context, now)
            for surface in RUNTIME_PATH_SURFACES:
                entry = entry_by_surface[surface]
                store.record_path_plan(
                    topic_workspace_id=context.topic_workspace_id,
                    surface=surface,
                    path=entry.path,
                    source=entry.source,
                    source_detail=entry.source_detail,
                    created_at=now,
                )
    except sqlite3.Error as exc:
        store.close()
        diagnostics.append(
            Diagnostic(
                code="ISO040",
                severity="error",
                concept="Workspace Runtime",
                path=db_path,
                message=f"Workspace Runtime initialization failed: {exc}.",
            )
        )
        return None, diagnostics

    path_plans = store.list_path_plans()
    result = RuntimeInitializationResult(
        runtime_path=db_path,
        metadata=store.metadata(),
        created=True,
        directories=directories,
        path_plans=path_plans,
    )
    store.close()
    return result, diagnostics


def open_workspace_runtime(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    read_only: bool,
) -> tuple[WorkspaceRuntimeStore | None, list[Diagnostic]]:
    entries, diagnostics = preview_paths(context, env=env)
    if has_errors(diagnostics):
        return None, diagnostics
    db_path = next(entry.path for entry in entries if entry.surface == "workspace_runtime_db")
    if not db_path.exists():
        diagnostics.append(
            Diagnostic(
                code="ISO040",
                severity="error",
                concept="Workspace Runtime",
                path=db_path,
                message="Workspace Runtime has not been initialized for the selected Topic Workspace.",
            )
        )
        return None, diagnostics

    try:
        if read_only:
            uri = f"file:{db_path}?mode=ro"
            connection = sqlite3.connect(uri, uri=True)
        else:
            connection = sqlite3.connect(db_path)
    except sqlite3.Error as exc:
        diagnostics.append(
            Diagnostic(
                code="ISO040",
                severity="error",
                concept="Workspace Runtime",
                path=db_path,
                message=f"Workspace Runtime could not be opened: {exc}.",
            )
        )
        return None, diagnostics

    store = WorkspaceRuntimeStore(db_path, connection)
    schema_diagnostics = _validate_open_schema(store, context)
    diagnostics.extend(schema_diagnostics)
    if schema_diagnostics:
        store.close()
        return None, diagnostics
    if not read_only:
        with store.connection:
            _create_schema(store.connection)
    return store, diagnostics


def prepare_topic_environment_readiness(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    actor_ref: str | None = None,
) -> tuple[ReadinessPreparationResult | None, list[Diagnostic]]:
    store, diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    if store is None:
        return None, diagnostics

    project_pixi_info, pixi_diagnostics = find_project_pixi_manifest(context.project.root)
    diagnostics.extend(pixi_diagnostics)
    topic_payload, checks, topic_diagnostics = inspect_topic_pixi(context, project_pixi_info)
    diagnostics.extend(topic_diagnostics)
    failed_checks = [check for check in checks if check.status == "fail"]
    readiness_diagnostics = [_readiness_diagnostic(check, context) for check in failed_checks]
    diagnostics.extend(readiness_diagnostics)

    project_bindings = context.project.manifest.active_topic_pixi_environment_bindings(
        context.research_topic.id
    )
    standalone_bindings = context.project.manifest.active_topic_standalone_pixi_bindings(
        context.research_topic.id
    )
    if any(check.id == "topic.pixi.binding.present" for check in failed_checks):
        status = "blocked"
    elif failed_checks or pixi_diagnostics or topic_diagnostics:
        status = "failed"
    else:
        status = "ready"
    checked_at = utc_timestamp()
    record = TopicEnvironmentReadinessRecord(
        id=f"readiness-{_slug(context.research_topic.id)}-{checked_at.replace(':', '').replace('-', '')}",
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        status=status,
        project_pixi_environment_refs=[
            binding.pixi_environment for binding in project_bindings
        ],
        standalone_pixi_manifest_refs=[
            binding.manifest_path_input for binding in standalone_bindings
        ],
        diagnostics=[diagnostic.to_json() for diagnostic in readiness_diagnostics],
        checked_at=checked_at,
        actor_ref=actor_ref,
        repair_service_request_hint=(
            "Create a Service Request for environment setup or compatibility repair before launch-facing work."
            if status in {"failed", "blocked"}
            else None
        ),
        provenance_refs=[_provenance_ref("topic-environment-readiness", context.research_topic.id)],
    )
    if record.status not in READINESS_STATUSES:
        diagnostics.append(
            Diagnostic(
                code="ISO043",
                severity="error",
                concept="Topic Environment Readiness",
                message=f"Unsupported readiness status: {record.status}.",
            )
        )
        store.close()
        return None, diagnostics

    with store.connection:
        store.record_readiness(record)
    store.close()
    return ReadinessPreparationResult(record, checks, topic_payload), diagnostics


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
            provenance_refs_json TEXT NOT NULL
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


def _write_metadata(connection: sqlite3.Connection, metadata: WorkspaceRuntimeMetadata) -> None:
    values = metadata.to_json()
    values["provenance_refs"] = _dumps(metadata.provenance_refs)
    for key, value in values.items():
        connection.execute(
            "INSERT OR REPLACE INTO runtime_metadata (key, value) VALUES (?, ?)",
            (key, str(value)),
        )


def _write_initial_lifecycle_records(
    store: WorkspaceRuntimeStore,
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
    store: WorkspaceRuntimeStore,
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


def _readiness_diagnostic(check: DoctorCheck, context: EffectiveTopicContext) -> Diagnostic:
    return Diagnostic(
        code="ISO043",
        severity="error",
        concept=check.concept,
        path=context.project.manifest_path,
        field=check.id,
        message=f"{check.summary} Use a Service Request for environment setup or compatibility repair.",
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


def _path_plan_id(topic_workspace_id: str, surface: str) -> str:
    return f"path-plan-{_slug(topic_workspace_id)}-{_slug(surface)}"


def _provenance_ref(record_kind: str, record_id: str) -> str:
    return f"provenance:{record_kind}:{record_id}"


def _slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "-", value).strip("-") or "record"


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
    store: WorkspaceRuntimeStore,
    callback: Callable[[WorkspaceRuntimeStore], None],
) -> None:
    """Run a caller-supplied mutation inside the store transaction boundary."""

    with store.connection:
        callback(store)
