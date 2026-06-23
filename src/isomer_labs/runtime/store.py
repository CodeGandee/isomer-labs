"""SQLite-backed Workspace Runtime store."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from pathlib import Path
import sqlite3
from typing import Callable, Mapping

from isomer_labs.diagnostics import Diagnostic, has_errors
from isomer_labs.doctor import DoctorCheck, find_project_pixi_manifest, inspect_topic_pixi
from isomer_labs.models import (
    DomainAgentTeamTemplate,
    EffectiveTopicContext,
    TopicAgentTeamProfile,
)
from isomer_labs.paths import preview_paths
from isomer_labs.runtime.models import (
    ADAPTER_MANIFEST_KINDS,
    ADAPTER_COMMAND_RUN_STATUSES,
    ADAPTER_INSPECTION_STATUSES,
    ADAPTER_HANDOFF_DISPATCH_STATUSES,
    ADAPTER_LAUNCH_ATTEMPT_STATUSES,
    ADAPTER_MATERIALIZATION_STATUSES,
    ADAPTER_RECONCILIATION_STATES,
    ADAPTER_STOP_OUTCOME_STATUSES,
    HANDOFF_NORMALIZATION_STATUSES,
    HANDOFF_STATUSES,
    READINESS_STATUSES,
    RUNTIME_PATH_SURFACES,
    SIGNAL_OBSERVATION_STATUSES,
    WORKSPACE_RUNTIME_SCHEMA_VERSION,
    AgentInstanceRecord,
    AgentTeamInstanceRecord,
    AgentWorkspaceRecord,
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
    RuntimeLifecycleRecord,
    SignalObservationRecord,
    TopicEnvironmentReadinessRecord,
    ValidationIssueRecord,
    WorkspaceRuntimeMetadata,
    utc_timestamp,
)
from isomer_labs.runtime.identifiers import _agent_instance_id, _path_plan_id, _provenance_ref, _slug
from isomer_labs.runtime.readiness import _readiness_diagnostic
from isomer_labs.runtime.rows import (
    _row_to_adapter_command_run,
    _row_to_adapter_handoff_dispatch,
    _row_to_adapter_inspection_snapshot,
    _row_to_adapter_launch_attempt,
    _row_to_adapter_manifest_ref,
    _row_to_adapter_materialization,
    _row_to_adapter_payload_ref,
    _row_to_adapter_reconciliation_record,
    _row_to_adapter_stop_outcome,
    _row_to_agent_instance,
    _row_to_agent_team_instance,
    _row_to_agent_workspace,
    _row_to_handoff,
    _row_to_handoff_normalization,
    _row_to_lifecycle_record,
    _row_to_path_plan,
    _row_to_readiness,
    _row_to_signal_observation,
)
from isomer_labs.runtime.schema import (
    RUNTIME_SCHEMA_TABLES,
    _create_schema,
    _ensure_runtime_directories,
    _validate_open_schema,
    _write_initial_lifecycle_records,
    _write_metadata,
)
from isomer_labs.runtime.serialization import _dumps, _loads_list
from isomer_labs.runtime.transactions import (
    _table_exists,
    _table_names,
    run_runtime_transaction as _run_runtime_transaction,
)


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
    adapter_handoff_dispatches: list[AdapterHandoffDispatchRecord] = field(default_factory=list)
    signal_observations: list[SignalObservationRecord] = field(default_factory=list)
    handoff_normalizations: list[HandoffNormalizationRecord] = field(default_factory=list)
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
            "adapter_handoff_dispatches": [record.to_json() for record in self.adapter_handoff_dispatches],
            "signal_observations": [record.to_json() for record in self.signal_observations],
            "handoff_normalizations": [record.to_json() for record in self.handoff_normalizations],
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

    def get_lifecycle_record(self, record_id: str) -> RuntimeLifecycleRecord | None:
        row = self.connection.execute(
            "SELECT * FROM lifecycle_records WHERE id = ?",
            (record_id,),
        ).fetchone()
        return _row_to_lifecycle_record(row) if row is not None else None

    def ensure_run_record(
        self,
        *,
        context: EffectiveTopicContext,
        agent_team_instance_id: str,
        run_id: str | None,
        research_task_id: str | None,
        actor_ref: str | None,
    ) -> RuntimeLifecycleRecord:
        timestamp = utc_timestamp()
        selected_run_id = run_id or f"run-{_slug(agent_team_instance_id)}-{_slug(research_task_id or 'manual-handoff')}"
        existing = self.get_lifecycle_record(selected_run_id)
        if existing is not None:
            return existing
        refs = {"agent_team_instance_id": agent_team_instance_id}
        if research_task_id is not None:
            refs["research_task_id"] = research_task_id
        if actor_ref is not None:
            refs["actor_ref"] = actor_ref
        record = RuntimeLifecycleRecord(
            id=selected_run_id,
            record_kind="run",
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            status="running",
            created_at=timestamp,
            updated_at=timestamp,
            lifecycle_refs=refs,
            transition_metadata={"source": "handoff_dispatch"},
            provenance_refs=[_provenance_ref("run", selected_run_id)],
        )
        self.upsert_lifecycle_record(record)
        self.link_agent_team_instance_refs(agent_team_instance_id, run_ids=[selected_run_id])
        return record

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
                    agent_id = _agent_instance_id(team_id, binding.role_id)
                    if self._agent_instance_id_exists(agent_id):
                        diagnostics.append(
                            Diagnostic(
                                code="ISO041",
                                severity="error",
                                concept="Agent Instance Identity",
                                field="id",
                                message=f"Generated Agent Instance id already exists: {agent_id}.",
                            )
                        )
                        return None, diagnostics
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
        adapter_handoff_dispatches = self.list_adapter_handoff_dispatches(agent_team_instance_id=team_id)
        signal_observations = self.list_signal_observations(agent_team_instance_id=team_id)
        handoff_normalizations = self.list_handoff_normalizations(handoff_ids=[record.id for record in handoffs])
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
            adapter_handoff_dispatches=adapter_handoff_dispatches,
            signal_observations=signal_observations,
            handoff_normalizations=handoff_normalizations,
            adapter_manifest_refs=adapter_manifest_refs,
            reconciliation_records=reconciliation_records,
            adapter_payload_refs=adapter_payload_refs,
            adapter_command_runs=adapter_command_runs,
            adapter_materializations=adapter_materializations,
            adapter_launch_attempts=adapter_launch_attempts,
            adapter_inspection_snapshots=adapter_inspection_snapshots,
            adapter_stop_outcomes=adapter_stop_outcomes,
        )

    def _agent_instance_id_exists(self, agent_id: str) -> bool:
        row = self.connection.execute(
            "SELECT 1 FROM agent_instances WHERE id = ?",
            (agent_id,),
        ).fetchone()
        return row is not None

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

    def link_agent_team_instance_refs(
        self,
        team_id: str,
        *,
        run_ids: list[str] | None = None,
        handoff_ids: list[str] | None = None,
        status: str | None = None,
    ) -> AgentTeamInstanceRecord | None:
        team = self.get_agent_team_instance(team_id)
        if team is None:
            return None
        next_run_ids = list(dict.fromkeys([*team.run_ids, *(run_ids or [])]))
        next_handoff_ids = list(dict.fromkeys([*team.handoff_ids, *(handoff_ids or [])]))
        updated = replace(
            team,
            run_ids=next_run_ids,
            handoff_ids=next_handoff_ids,
            status=status or team.status,
            updated_at=utc_timestamp(),
        )
        self._insert_agent_team_instance(updated)
        return updated

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

    def record_adapter_handoff_dispatch(self, record: AdapterHandoffDispatchRecord) -> None:
        if record.status not in ADAPTER_HANDOFF_DISPATCH_STATUSES:
            raise ValueError(f"Unsupported adapter handoff dispatch status: {record.status}")
        self.connection.execute(
            """
            INSERT OR REPLACE INTO adapter_handoff_dispatch_records
                (
                    id, research_topic_id, topic_workspace_id, handoff_id,
                    agent_team_instance_id, source_agent_instance_id,
                    target_agent_instance_id, adapter_id, status, research_task_id,
                    run_id, command_run_ids_json, payload_ref_ids_json,
                    expected_output_refs_json, completion_watcher_contract_refs_json,
                    diagnostics_json, actor_ref, created_at, updated_at,
                    provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.handoff_id,
                record.agent_team_instance_id,
                record.source_agent_instance_id,
                record.target_agent_instance_id,
                record.adapter_id,
                record.status,
                record.research_task_id,
                record.run_id,
                _dumps(record.command_run_ids),
                _dumps(record.payload_ref_ids),
                _dumps(record.expected_output_refs),
                _dumps(record.completion_watcher_contract_refs),
                _dumps(record.diagnostics),
                record.actor_ref,
                record.created_at,
                record.updated_at,
                _dumps(record.provenance_refs),
            ),
        )

    def list_adapter_handoff_dispatches(
        self,
        *,
        agent_team_instance_id: str | None = None,
        handoff_id: str | None = None,
    ) -> list[AdapterHandoffDispatchRecord]:
        if not _table_exists(self.connection, "adapter_handoff_dispatch_records"):
            return []
        clauses: list[str] = []
        values: list[str] = []
        if agent_team_instance_id is not None:
            clauses.append("agent_team_instance_id = ?")
            values.append(agent_team_instance_id)
        if handoff_id is not None:
            clauses.append("handoff_id = ?")
            values.append(handoff_id)
        where = f" WHERE {' AND '.join(clauses)}" if clauses else ""
        rows = self.connection.execute(
            f"SELECT * FROM adapter_handoff_dispatch_records{where} ORDER BY created_at, id",
            tuple(values),
        )
        return [_row_to_adapter_handoff_dispatch(row) for row in rows]

    def record_signal_observation(self, record: SignalObservationRecord) -> None:
        if record.status not in SIGNAL_OBSERVATION_STATUSES:
            raise ValueError(f"Unsupported Signal Observation status: {record.status}")
        self.connection.execute(
            """
            INSERT OR REPLACE INTO signal_observation_records
                (
                    id, research_topic_id, topic_workspace_id, handoff_id, run_id,
                    agent_team_instance_id, source_agent_instance_id,
                    target_agent_instance_id, adapter_id, observation_kind, status,
                    summary, command_run_ids_json, payload_ref_ids_json,
                    diagnostics_json, actor_ref, observed_at, provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.handoff_id,
                record.run_id,
                record.agent_team_instance_id,
                record.source_agent_instance_id,
                record.target_agent_instance_id,
                record.adapter_id,
                record.observation_kind,
                record.status,
                record.summary,
                _dumps(record.command_run_ids),
                _dumps(record.payload_ref_ids),
                _dumps(record.diagnostics),
                record.actor_ref,
                record.observed_at,
                _dumps(record.provenance_refs),
            ),
        )

    def list_signal_observations(
        self,
        *,
        agent_team_instance_id: str | None = None,
        handoff_id: str | None = None,
    ) -> list[SignalObservationRecord]:
        if not _table_exists(self.connection, "signal_observation_records"):
            return []
        clauses: list[str] = []
        values: list[str] = []
        if agent_team_instance_id is not None:
            clauses.append("agent_team_instance_id = ?")
            values.append(agent_team_instance_id)
        if handoff_id is not None:
            clauses.append("handoff_id = ?")
            values.append(handoff_id)
        where = f" WHERE {' AND '.join(clauses)}" if clauses else ""
        rows = self.connection.execute(
            f"SELECT * FROM signal_observation_records{where} ORDER BY observed_at, id",
            tuple(values),
        )
        return [_row_to_signal_observation(row) for row in rows]

    def record_handoff_normalization(self, record: HandoffNormalizationRecord) -> None:
        if record.status not in HANDOFF_NORMALIZATION_STATUSES:
            raise ValueError(f"Unsupported handoff normalization status: {record.status}")
        self.connection.execute(
            """
            INSERT OR REPLACE INTO handoff_normalization_records
                (
                    id, research_topic_id, topic_workspace_id, handoff_id,
                    run_id, status, rationale, signal_observation_ids_json,
                    output_artifact_refs_json, corrective_refs_json,
                    payload_ref_ids_json, actor_ref, created_at,
                    provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.handoff_id,
                record.run_id,
                record.status,
                record.rationale,
                _dumps(record.signal_observation_ids),
                _dumps(record.output_artifact_refs),
                _dumps(record.corrective_refs),
                _dumps(record.payload_ref_ids),
                record.actor_ref,
                record.created_at,
                _dumps(record.provenance_refs),
            ),
        )

    def list_handoff_normalizations(
        self,
        *,
        handoff_id: str | None = None,
        handoff_ids: list[str] | None = None,
    ) -> list[HandoffNormalizationRecord]:
        if not _table_exists(self.connection, "handoff_normalization_records"):
            return []
        if handoff_ids is not None:
            if not handoff_ids:
                return []
            placeholders = ", ".join("?" for _ in handoff_ids)
            rows = self.connection.execute(
                f"SELECT * FROM handoff_normalization_records WHERE handoff_id IN ({placeholders}) ORDER BY created_at, id",
                tuple(handoff_ids),
            )
            return [_row_to_handoff_normalization(row) for row in rows]
        if handoff_id is not None:
            rows = self.connection.execute(
                "SELECT * FROM handoff_normalization_records WHERE handoff_id = ? ORDER BY created_at, id",
                (handoff_id,),
            )
            return [_row_to_handoff_normalization(row) for row in rows]
        return [
            _row_to_handoff_normalization(row)
            for row in self.connection.execute("SELECT * FROM handoff_normalization_records ORDER BY created_at, id")
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
            INSERT OR REPLACE INTO agent_team_instances
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


def run_runtime_transaction(
    store: WorkspaceRuntimeStore,
    callback: Callable[[WorkspaceRuntimeStore], None],
) -> None:
    """Run a caller-supplied mutation inside the store transaction boundary."""

    _run_runtime_transaction(store, callback)
