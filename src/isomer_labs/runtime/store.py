"""SQLite-backed Workspace Runtime store."""

from __future__ import annotations

from contextlib import nullcontext
from dataclasses import dataclass, field, replace
from pathlib import Path
import re
import sqlite3
from typing import Callable, Mapping, cast

from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.core.path_utils import is_within, resolve_project_path
from isomer_labs.project.doctor import DoctorCheck, find_project_pixi_manifest, inspect_topic_pixi
from isomer_labs.models import (
    DomainAgentTeamTemplate,
    EffectiveTopicContext,
    Project,
    TopicAgentTeamProfile,
    TopicWorkspaceRegistration,
)
from isomer_labs.workspace.path_resolution import preview_paths, resolve_semantic_path
from isomer_labs.runtime import records as runtime_records
from isomer_labs.runtime.records import (
    ADAPTER_MANIFEST_KINDS,
    ADAPTER_COMMAND_RUN_STATUSES,
    ADAPTER_INSPECTION_STATUSES,
    ADAPTER_HANDOFF_DISPATCH_STATUSES,
    ADAPTER_LAUNCH_ATTEMPT_STATUSES,
    ADAPTER_MATERIALIZATION_STATUSES,
    ADAPTER_RECONCILIATION_STATES,
    ADAPTER_STOP_OUTCOME_STATUSES,
    ARTIFACT_FORMAT_REGISTRATION_SOURCE_KINDS,
    HANDOFF_NORMALIZATION_STATUSES,
    HANDOFF_STATUSES,
    READINESS_STATUSES,
    RESEARCH_IDEA_ARCHIVE_STATES,
    RESEARCH_IDEA_CLOSURE_REASONS,
    RESEARCH_IDEA_DECISION_OPTION_OUTCOMES,
    RESEARCH_IDEA_DECISION_STATES,
    RESEARCH_IDEA_EVIDENCE_STATES,
    RESEARCH_IDEA_EXPLORATION_STATES,
    RESEARCH_IDEA_FACETS,
    RESEARCH_IDEA_LINEAGE_KINDS,
    RESEARCH_IDEA_LINEAGE_STATUSES,
    RESEARCH_IDEA_OPERATION_STATUSES,
    RESEARCH_IDEA_STATUSES,
    RESEARCH_IDEA_VISIBILITIES,
    RESEARCH_RECORD_LINEAGE_KINDS,
    RESEARCH_RECORD_LINEAGE_STATUSES,
    RESET_CHECKPOINT_STATUSES,
    RESET_OUTCOME_STATUSES,
    RESET_PLAN_ACTIONS,
    RESET_PLAN_ACTION_STATUSES,
    RESET_PLAN_STATUSES,
    RUNTIME_PATH_SURFACES,
    SIGNAL_OBSERVATION_STATUSES,
    WORKSPACE_RUNTIME_SCHEMA_VERSION,
    _path_plan_id,
    _provenance_ref,
    _slug,
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
    ResearchIdeaArchiveState,
    ResearchIdeaDecisionState,
    ResearchIdeaDecisionOption,
    ResearchIdeaEvidenceState,
    ResearchIdeaExplorationState,
    ResearchIdeaGenerationGroup,
    ResearchIdeaLineageEdge,
    ResearchIdeaOperation,
    ResearchIdeaRealization,
    ResearchIdeaStateTransition,
    ResearchRecordGenerationGroup,
    ResearchRecordLineageEdge,
    ResetCheckpointRecord,
    ResetOutcomeRecord,
    ResetPlanActionRecord,
    ResetPlanRecord,
    RuntimeLifecycleRecord,
    SignalObservationRecord,
    STRUCTURED_PAYLOAD_RENDER_STATUSES,
    STRUCTURED_PAYLOAD_VALIDATION_STATUSES,
    StructuredResearchPayloadRecord,
    TopicEnvironmentReadinessRecord,
    ValidationIssueRecord,
    WorkspaceRuntimeMetadata,
    project_research_idea_compatibility_status,
    utc_timestamp,
)
from isomer_labs.runtime.sqlite import (
    RUNTIME_SCHEMA_TABLES,
    _column_names,
    _create_schema,
    _dumps,
    _ensure_runtime_directories,
    _loads_list,
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
    _row_to_artifact_format_registration,
    _row_to_handoff,
    _row_to_handoff_normalization,
    _row_to_lifecycle_record,
    _row_to_path_plan,
    _row_to_readiness,
    _row_to_research_idea,
    _row_to_research_idea_decision_option,
    _row_to_research_idea_generation_group,
    _row_to_research_idea_lineage_edge,
    _row_to_research_idea_operation,
    _row_to_research_idea_realization,
    _row_to_research_idea_state_transition,
    _row_to_research_record_generation_group,
    _row_to_research_record_lineage_edge,
    _row_to_reset_checkpoint,
    _row_to_reset_outcome,
    _row_to_reset_plan,
    _row_to_reset_plan_action,
    _row_to_signal_observation,
    _row_to_structured_payload,
    _table_exists,
    _table_names,
    _validate_open_schema,
    _write_initial_lifecycle_records,
    _write_metadata,
    run_runtime_transaction as _run_runtime_transaction,
)
from isomer_labs.workspace.surfaces import ensure_tmp_surface_ignore_policy
from isomer_labs.workspace.path_resolution import AgentWorkspacePlan, resolve_role_binding_agent_workspace_plan
from isomer_labs.workspace.surfaces import topic_workspace_path as default_topic_workspace_path
from isomer_labs.workspace.manifest import (
    EffectiveAgentContext,
    SemanticPathResult,
    compatibility_surface_for_label,
    catalog,
    resolve_semantic_binding,
    semantic_label_for_surface,
)
from isomer_labs.workspace.surfaces import storage_profile_by_id


def _readiness_diagnostic(check: DoctorCheck, context: EffectiveTopicContext) -> Diagnostic:
    return Diagnostic(
        code="ISO043",
        severity="error",
        concept=check.concept,
        path=context.project.manifest_path,
        field=check.id,
        message=f"{check.summary} Use a Service Request for environment setup or compatibility repair.",
    )


def _lineage_diag(severity: str, code: str, message: str, **details: object) -> dict[str, object]:
    payload: dict[str, object] = {"severity": severity, "code": code, "message": message}
    payload.update(details)
    return payload


@dataclass(frozen=True)
class AgentInstanceIdLocation:
    agent_id: str
    db_path: Path
    agent_team_instance_id: str
    agent_role_id: str
    research_topic_id: str
    topic_workspace_id: str

    def record_ref(self) -> str:
        return (
            f"{self.db_path}:{self.topic_workspace_id}:"
            f"{self.agent_team_instance_id}:{self.agent_role_id}"
        )


def project_agent_instance_id_locations(
    project: Project,
) -> tuple[dict[str, list[AgentInstanceIdLocation]], list[tuple[Path, str]]]:
    locations: dict[str, list[AgentInstanceIdLocation]] = {}
    issues: list[tuple[Path, str]] = []

    for db_path in project_runtime_db_paths(project):
        if not db_path.exists():
            continue
        try:
            connection = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            connection.row_factory = sqlite3.Row
            try:
                rows = connection.execute(
                    """
                    SELECT id, agent_team_instance_id, agent_role_id, research_topic_id, topic_workspace_id
                    FROM agent_instances
                    ORDER BY id, agent_team_instance_id, agent_role_id
                    """
                ).fetchall()
            finally:
                connection.close()
        except sqlite3.Error as exc:
            issues.append((db_path, str(exc)))
            continue
        for row in rows:
            location = AgentInstanceIdLocation(
                agent_id=row["id"],
                db_path=db_path,
                agent_team_instance_id=row["agent_team_instance_id"],
                agent_role_id=row["agent_role_id"],
                research_topic_id=row["research_topic_id"],
                topic_workspace_id=row["topic_workspace_id"],
            )
            locations.setdefault(location.agent_id, []).append(location)

    return locations, issues


def validate_global_agent_instance_id_uniqueness(
    context: EffectiveTopicContext,
    db_path: Path,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    id_locations, scan_issues = project_agent_instance_id_locations(context.project)
    for scan_db_path, message in scan_issues:
        diagnostics.append(
            Diagnostic(
                code="ISO040",
                severity="warning",
                concept="Agent Instance Identity",
                path=scan_db_path,
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
                    path=db_path,
                    field=agent_id,
                    message=(
                        f"Agent Instance id {agent_id} appears in multiple Project runtime records: "
                        f"{records}."
                    ),
                )
            )

    return diagnostics


def project_runtime_db_paths(project: Project) -> list[Path]:
    paths: list[Path] = []
    seen: set[Path] = set()

    for workspace in project.manifest.topic_workspaces:
        workspace_path = _workspace_path(project, workspace)
        if workspace_path is None:
            continue
        db_path = workspace_path / "state.sqlite"
        if db_path not in seen:
            paths.append(db_path)
            seen.add(db_path)

    registered_topic_ids = {
        workspace.research_topic_id
        for workspace in project.manifest.topic_workspaces
        if workspace.research_topic_id is not None
    }
    for topic in project.manifest.research_topics:
        if topic.id in registered_topic_ids:
            continue
        workspace_path = _default_workspace_path(project, topic.id)
        db_path = workspace_path / "state.sqlite"
        if db_path not in seen:
            paths.append(db_path)
            seen.add(db_path)

    return paths


def _workspace_path(project: Project, workspace: TopicWorkspaceRegistration) -> Path | None:
    if workspace.path_input is not None:
        path = resolve_project_path(project.root, workspace.path_input)
    else:
        workspace_id = workspace.research_topic_id or workspace.id
        path = _default_workspace_path(project, workspace_id)
    return path if is_within(path, project.root) else None


def _default_workspace_path(project: Project, workspace_id: str) -> Path:
    return default_topic_workspace_path(project.root, workspace_id, project.manifest.path_defaults)


AGENT_TEAM_INSTANCE_PATH_LABELS = (
    "agent.workspace",
    "agent.isomer_managed",
    "agent.output_root",
    "agent.owned",
    "agent.runtime",
    "agent.private_artifacts",
    "agent.scratch",
    "agent.logs",
    "agent.public_share",
    "agent.inbox",
    "agent.topic_owned",
    "agent.topic_readonly",
    "agent.topic_writable",
    "agent.links",
)


def _agent_path_plan_source_detail(plan: AgentWorkspacePlan, result: SemanticPathResult) -> str:
    parts = [
        plan.source_detail,
        f"branch={plan.branch}",
        f"semantic_label={result.label}",
        f"semantic_source={result.source}",
    ]
    if result.source_detail is not None:
        parts.append(f"semantic_source_detail={result.source_detail}")
    return "; ".join(parts)


def _storage_profile_traits_for_result(result: SemanticPathResult) -> dict[str, object]:
    traits = result.to_json().get("storage_profile_traits", {})
    return traits if isinstance(traits, dict) else {}


def _prepare_runtime_local_tmp_surfaces(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
) -> tuple[list[Path], list[Diagnostic]]:
    directories: list[Path] = []
    diagnostics: list[Diagnostic] = []
    for label in ("topic.tmp", "topic.repos.main.tmp"):
        result, result_diagnostics = resolve_semantic_path(
            context,
            label,
            env=env,
            cwd=context.topic_workspace_path,
            use_path_plan=False,
        )
        diagnostics.extend(result_diagnostics)
        if result is None:
            continue
        result.path.mkdir(parents=True, exist_ok=True)
        directories.append(result.path)
        diagnostics.extend(ensure_tmp_surface_ignore_policy(context, label, result.path, env=env))
    return directories, diagnostics


def _prepare_agent_local_tmp_surface(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    agent_name: str,
    agent_workspace_path: Path,
    tmp_path: Path,
) -> list[Diagnostic]:
    agent_context = EffectiveAgentContext(
        agent_name=agent_name,
        agent_workspace_path=agent_workspace_path,
        source="runtime-agent-workspace-setup",
    )
    diagnostics: list[Diagnostic] = []
    tmp_path.mkdir(parents=True, exist_ok=True)
    diagnostics.extend(ensure_tmp_surface_ignore_policy(context, "agent.tmp", tmp_path, env=env, agent_context=agent_context))
    return diagnostics


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
        semantic_label: str | None = None,
        scope_ref: str | None = None,
        compatibility_surface: str | None = None,
        storage_profile: str | None = None,
        storage_profile_traits: dict[str, object] | None = None,
        created_at: str | None = None,
    ) -> PathPlanRecord:
        timestamp = created_at or utc_timestamp()
        selected_semantic_label = semantic_label or semantic_label_for_surface(surface)
        selected_compatibility_surface = compatibility_surface or surface
        selected_storage_profile = storage_profile
        selected_storage_profile_traits = storage_profile_traits or {}
        if selected_storage_profile is None and selected_semantic_label is not None:
            semantic_surface = catalog().get(selected_semantic_label)
            if semantic_surface is not None:
                selected_storage_profile = semantic_surface.storage_profile
                profile = storage_profile_by_id(semantic_surface.storage_profile)
                selected_storage_profile_traits = profile.to_json() if profile is not None else {}
        selected_scope_ref = scope_ref
        if selected_scope_ref is None and selected_semantic_label is not None:
            selected_scope_ref = f"topic_workspace:{topic_workspace_id}"
            if surface.startswith("agent_") and ":" in surface:
                selected_scope_ref = f"agent_name:{surface.split(':', 1)[1]}"
        record = PathPlanRecord(
            id=_path_plan_id(topic_workspace_id, surface),
            topic_workspace_id=topic_workspace_id,
            surface=surface,
            path=str(path.resolve(strict=False)),
            source=source,
            source_detail=source_detail,
            created_at=timestamp,
            semantic_label=selected_semantic_label,
            scope_ref=selected_scope_ref,
            compatibility_surface=selected_compatibility_surface,
            storage_profile=selected_storage_profile,
            storage_profile_traits=selected_storage_profile_traits,
        )
        self.connection.execute(
            """
            INSERT OR IGNORE INTO path_plans
                (
                    id, topic_workspace_id, surface, path, source, source_detail,
                    semantic_label, scope_ref, compatibility_surface, storage_profile,
                    storage_profile_traits_json, created_at
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.id,
                record.topic_workspace_id,
                record.surface,
                record.path,
                record.source,
                record.source_detail,
                record.semantic_label,
                record.scope_ref,
                record.compatibility_surface,
                record.storage_profile,
                _dumps(record.storage_profile_traits),
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

    def upsert_research_record_generation_group(self, record: ResearchRecordGenerationGroup) -> None:
        self.connection.execute(
            """
            INSERT INTO research_record_generation_groups
                (
                    id, research_topic_id, topic_workspace_id, purpose, parent_set_digest,
                    producer_skill, decision_record_id, metadata_json, created_at, updated_at,
                    provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                purpose = excluded.purpose,
                parent_set_digest = excluded.parent_set_digest,
                producer_skill = excluded.producer_skill,
                decision_record_id = excluded.decision_record_id,
                metadata_json = excluded.metadata_json,
                updated_at = excluded.updated_at,
                provenance_refs_json = excluded.provenance_refs_json
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.purpose,
                record.parent_set_digest,
                record.producer_skill,
                record.decision_record_id,
                _dumps(record.metadata),
                record.created_at,
                record.updated_at,
                _dumps(record.provenance_refs),
            ),
        )

    def get_research_record_generation_group(self, group_id: str) -> ResearchRecordGenerationGroup | None:
        if not _table_exists(self.connection, "research_record_generation_groups"):
            return None
        row = self.connection.execute(
            "SELECT * FROM research_record_generation_groups WHERE id = ?",
            (group_id,),
        ).fetchone()
        return _row_to_research_record_generation_group(row) if row is not None else None

    def list_research_record_generation_groups(
        self,
        *,
        topic_workspace_id: str | None = None,
        parent_set_digest: str | None = None,
    ) -> list[ResearchRecordGenerationGroup]:
        if not _table_exists(self.connection, "research_record_generation_groups"):
            return []
        query = "SELECT * FROM research_record_generation_groups"
        clauses: list[str] = []
        params: list[object] = []
        if topic_workspace_id is not None:
            clauses.append("topic_workspace_id = ?")
            params.append(topic_workspace_id)
        if parent_set_digest is not None:
            clauses.append("parent_set_digest = ?")
            params.append(parent_set_digest)
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY updated_at DESC, id"
        return [_row_to_research_record_generation_group(row) for row in self.connection.execute(query, params)]

    def upsert_research_record_lineage_edge(self, record: ResearchRecordLineageEdge, *, validate: bool = True) -> None:
        diagnostics = self.validate_research_record_lineage_edge(record) if validate else []
        errors = [item for item in diagnostics if item.get("severity") == "error"]
        if errors:
            codes = ", ".join(str(item.get("code") or "lineage_error") for item in errors)
            raise ValueError(f"Invalid research record lineage edge {record.id}: {codes}")
        self.connection.execute(
            """
            INSERT INTO research_record_lineage_edges
                (
                    id, research_topic_id, topic_workspace_id, parent_record_id,
                    child_record_id, lineage_kind, parent_role, generation_id,
                    decision_record_id, rationale, status, metadata_json,
                    created_at, updated_at, provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                parent_record_id = excluded.parent_record_id,
                child_record_id = excluded.child_record_id,
                lineage_kind = excluded.lineage_kind,
                parent_role = excluded.parent_role,
                generation_id = excluded.generation_id,
                decision_record_id = excluded.decision_record_id,
                rationale = excluded.rationale,
                status = excluded.status,
                metadata_json = excluded.metadata_json,
                updated_at = excluded.updated_at,
                provenance_refs_json = excluded.provenance_refs_json
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.parent_record_id,
                record.child_record_id,
                record.lineage_kind,
                record.parent_role,
                record.generation_id,
                record.decision_record_id,
                record.rationale,
                record.status,
                _dumps(record.metadata),
                record.created_at,
                record.updated_at,
                _dumps(record.provenance_refs),
            ),
        )

    def get_research_record_lineage_edge(self, edge_id: str) -> ResearchRecordLineageEdge | None:
        if not _table_exists(self.connection, "research_record_lineage_edges"):
            return None
        row = self.connection.execute(
            "SELECT * FROM research_record_lineage_edges WHERE id = ?",
            (edge_id,),
        ).fetchone()
        return _row_to_research_record_lineage_edge(row) if row is not None else None

    def list_research_record_lineage_edges(
        self,
        *,
        topic_workspace_id: str | None = None,
        parent_record_id: str | None = None,
        child_record_id: str | None = None,
        generation_id: str | None = None,
        lineage_kind: str | None = None,
        include_archived: bool = False,
    ) -> list[ResearchRecordLineageEdge]:
        if not _table_exists(self.connection, "research_record_lineage_edges"):
            return []
        query = "SELECT * FROM research_record_lineage_edges"
        clauses: list[str] = []
        params: list[object] = []
        for column, value in (
            ("topic_workspace_id", topic_workspace_id),
            ("parent_record_id", parent_record_id),
            ("child_record_id", child_record_id),
            ("generation_id", generation_id),
            ("lineage_kind", lineage_kind),
        ):
            if value is not None:
                clauses.append(f"{column} = ?")
                params.append(value)
        if not include_archived:
            clauses.append("status != ?")
            params.append("archived")
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY created_at, parent_record_id, child_record_id, id"
        return [_row_to_research_record_lineage_edge(row) for row in self.connection.execute(query, params)]

    def delete_research_record_lineage_edge(self, edge_id: str) -> None:
        self.connection.execute("DELETE FROM research_record_lineage_edges WHERE id = ?", (edge_id,))

    def validate_research_record_lineage_edge(self, record: ResearchRecordLineageEdge) -> list[dict[str, object]]:
        diagnostics: list[dict[str, object]] = []
        if not _table_exists(self.connection, "research_record_lineage_edges"):
            return [_lineage_diag("error", "lineage_schema_missing", "Workspace Runtime is missing research record lineage tables.", edge_id=record.id)]
        if record.lineage_kind not in RESEARCH_RECORD_LINEAGE_KINDS:
            diagnostics.append(_lineage_diag("error", "lineage_kind_unsupported", f"Unsupported lineage kind: {record.lineage_kind}", edge_id=record.id))
        if record.status not in RESEARCH_RECORD_LINEAGE_STATUSES:
            diagnostics.append(_lineage_diag("error", "lineage_status_unsupported", f"Unsupported lineage status: {record.status}", edge_id=record.id))
        parent = self.get_lifecycle_record(record.parent_record_id)
        child = self.get_lifecycle_record(record.child_record_id)
        if parent is None:
            diagnostics.append(_lineage_diag("error", "lineage_parent_missing", f"Lineage parent record is missing: {record.parent_record_id}", edge_id=record.id, record_id=record.parent_record_id))
        elif parent.research_topic_id != record.research_topic_id or parent.topic_workspace_id != record.topic_workspace_id:
            diagnostics.append(_lineage_diag("error", "lineage_parent_cross_topic", f"Lineage parent is outside the Topic Workspace: {record.parent_record_id}", edge_id=record.id, record_id=record.parent_record_id))
        if child is None:
            diagnostics.append(_lineage_diag("error", "lineage_child_missing", f"Lineage child record is missing: {record.child_record_id}", edge_id=record.id, record_id=record.child_record_id))
        elif child.research_topic_id != record.research_topic_id or child.topic_workspace_id != record.topic_workspace_id:
            diagnostics.append(_lineage_diag("error", "lineage_child_cross_topic", f"Lineage child is outside the Topic Workspace: {record.child_record_id}", edge_id=record.id, record_id=record.child_record_id))
        if record.generation_id is not None:
            group = self.get_research_record_generation_group(record.generation_id)
            if group is None:
                diagnostics.append(_lineage_diag("error", "lineage_generation_group_missing", f"Lineage generation group is missing: {record.generation_id}", edge_id=record.id, generation_id=record.generation_id))
            elif group.research_topic_id != record.research_topic_id or group.topic_workspace_id != record.topic_workspace_id:
                diagnostics.append(_lineage_diag("error", "lineage_generation_group_cross_topic", f"Lineage generation group is outside the Topic Workspace: {record.generation_id}", edge_id=record.id, generation_id=record.generation_id))
        if record.lineage_kind == "revision_of":
            existing_revision = self.connection.execute(
                """
                SELECT id FROM research_record_lineage_edges
                WHERE topic_workspace_id = ? AND child_record_id = ? AND lineage_kind = 'revision_of'
                    AND status != 'archived' AND id != ?
                LIMIT 1
                """,
                (record.topic_workspace_id, record.child_record_id, record.id),
            ).fetchone()
            if existing_revision is not None:
                diagnostics.append(_lineage_diag("error", "lineage_revision_parent_not_unique", f"Revision child already has an immediate revision parent: {record.child_record_id}", edge_id=record.id, record_id=record.child_record_id))
        if record.parent_record_id == record.child_record_id or self._research_record_lineage_creates_cycle(record):
            diagnostics.append(_lineage_diag("error", "lineage_cycle", f"Lineage edge would create a cycle: {record.parent_record_id} -> {record.child_record_id}", edge_id=record.id))
        return diagnostics

    def validate_research_record_lineage(
        self,
        *,
        topic_workspace_id: str | None = None,
    ) -> list[dict[str, object]]:
        if not _table_exists(self.connection, "research_record_lineage_edges"):
            return [_lineage_diag("warning", "lineage_schema_missing", "Workspace Runtime has no canonical research record lineage table yet.")]
        diagnostics: list[dict[str, object]] = []
        for edge in self.list_research_record_lineage_edges(topic_workspace_id=topic_workspace_id, include_archived=True):
            diagnostics.extend(self.validate_research_record_lineage_edge(edge))
        return diagnostics

    def _research_record_lineage_creates_cycle(self, record: ResearchRecordLineageEdge) -> bool:
        if not _table_exists(self.connection, "research_record_lineage_edges"):
            return False
        row = self.connection.execute(
            """
            WITH RECURSIVE descendants(record_id) AS (
                SELECT child_record_id
                FROM research_record_lineage_edges
                WHERE topic_workspace_id = ?
                    AND parent_record_id = ?
                    AND status != 'archived'
                    AND id != ?
                UNION
                SELECT edge.child_record_id
                FROM research_record_lineage_edges edge
                JOIN descendants ON edge.parent_record_id = descendants.record_id
                WHERE edge.topic_workspace_id = ?
                    AND edge.status != 'archived'
                    AND edge.id != ?
            )
            SELECT 1 AS found FROM descendants WHERE record_id = ? LIMIT 1
            """,
            (
                record.topic_workspace_id,
                record.child_record_id,
                record.id,
                record.topic_workspace_id,
                record.id,
                record.parent_record_id,
            ),
        ).fetchone()
        return row is not None

    def upsert_research_idea(self, record: ResearchIdea, *, validate: bool = True) -> None:
        diagnostics = self.validate_research_idea(record) if validate else []
        errors = [item for item in diagnostics if item.get("severity") == "error"]
        if errors:
            codes = ", ".join(str(item.get("code") or "idea_error") for item in errors)
            raise ValueError(f"Invalid research idea {record.idea_id}: {codes}")
        if record.display_key is not None:
            self.reserve_research_idea_display_key(record)
        self.connection.execute(
            """
            INSERT INTO research_ideas
                (
                    id, research_topic_id, topic_workspace_id, idea_id, display_key, title, summary,
                    family, status, exploration_state, decision_state, evidence_state, archive_state,
                    visibility, aliases_json, source_record_id, source_json_path, metadata_json,
                    created_at, updated_at, provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(topic_workspace_id, idea_id) DO UPDATE SET
                display_key = COALESCE(excluded.display_key, research_ideas.display_key),
                title = excluded.title,
                summary = excluded.summary,
                family = excluded.family,
                status = excluded.status,
                exploration_state = excluded.exploration_state,
                decision_state = excluded.decision_state,
                evidence_state = excluded.evidence_state,
                archive_state = excluded.archive_state,
                visibility = excluded.visibility,
                aliases_json = excluded.aliases_json,
                source_record_id = excluded.source_record_id,
                source_json_path = excluded.source_json_path,
                metadata_json = excluded.metadata_json,
                updated_at = excluded.updated_at,
                provenance_refs_json = excluded.provenance_refs_json
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.idea_id,
                record.display_key,
                record.title,
                record.summary,
                record.family,
                record.status,
                record.exploration_state,
                record.decision_state,
                record.evidence_state,
                record.archive_state,
                record.visibility,
                _dumps(record.aliases),
                record.source_record_id,
                record.source_json_path,
                _dumps(record.metadata),
                record.created_at,
                record.updated_at,
                _dumps(record.provenance_refs),
            ),
        )

    def get_research_idea(self, idea_id: str, *, topic_workspace_id: str | None = None) -> ResearchIdea | None:
        if not _table_exists(self.connection, "research_ideas"):
            return None
        if topic_workspace_id is None:
            row = self.connection.execute("SELECT * FROM research_ideas WHERE idea_id = ? OR id = ? LIMIT 1", (idea_id, idea_id)).fetchone()
        else:
            row = self.connection.execute(
                "SELECT * FROM research_ideas WHERE topic_workspace_id = ? AND (idea_id = ? OR id = ?) LIMIT 1",
                (topic_workspace_id, idea_id, idea_id),
            ).fetchone()
        return _row_to_research_idea(row) if row is not None else None

    def list_research_ideas(
        self,
        *,
        topic_workspace_id: str | None = None,
        visibility: str | None = None,
        include_archived: bool = False,
    ) -> list[ResearchIdea]:
        if not _table_exists(self.connection, "research_ideas"):
            return []
        query = "SELECT * FROM research_ideas"
        clauses: list[str] = []
        params: list[object] = []
        if topic_workspace_id is not None:
            clauses.append("topic_workspace_id = ?")
            params.append(topic_workspace_id)
        if visibility is not None:
            clauses.append("visibility = ?")
            params.append(visibility)
        if not include_archived:
            columns = _column_names(self.connection, "research_ideas")
            if "archive_state" in columns:
                clauses.append("archive_state != ?")
                params.append("archived")
            else:
                clauses.append("status != ?")
                params.append("archived")
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY created_at, idea_id"
        return [_row_to_research_idea(row) for row in self.connection.execute(query, params)]

    def next_research_idea_display_key(self, topic_workspace_id: str) -> str:
        keys: list[str] = []
        if _table_exists(self.connection, "research_ideas"):
            keys.extend(
                str(row["display_key"])
                for row in self.connection.execute(
                    "SELECT display_key FROM research_ideas WHERE topic_workspace_id = ? AND display_key IS NOT NULL",
                    (topic_workspace_id,),
                )
            )
        if _table_exists(self.connection, "research_idea_display_keys"):
            keys.extend(
                str(row["display_key"])
                for row in self.connection.execute(
                    "SELECT display_key FROM research_idea_display_keys WHERE topic_workspace_id = ?",
                    (topic_workspace_id,),
                )
            )
        largest = 0
        for key in keys:
            match = re.fullmatch(r"I-?([1-9][0-9]*)", key)
            if match:
                largest = max(largest, int(match.group(1)))
        return f"I-{largest + 1}"

    def reserve_research_idea_display_key(self, record: ResearchIdea) -> None:
        if record.display_key is None:
            return
        if not _table_exists(self.connection, "research_idea_display_keys"):
            return
        existing = self.connection.execute(
            """
            SELECT idea_id FROM research_idea_display_keys
            WHERE topic_workspace_id = ? AND display_key = ?
            LIMIT 1
            """,
            (record.topic_workspace_id, record.display_key),
        ).fetchone()
        if existing is not None and str(existing["idea_id"]) != record.idea_id:
            raise ValueError(f"Display key already allocated in Topic Workspace: {record.display_key}")
        allocation_id = f"idea-display-key-{_slug(record.topic_workspace_id)}-{_slug(record.display_key)}"
        self.connection.execute(
            """
            INSERT INTO research_idea_display_keys
                (id, research_topic_id, topic_workspace_id, idea_id, display_key, status, created_at, updated_at, provenance_refs_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(topic_workspace_id, display_key) DO UPDATE SET
                idea_id = excluded.idea_id,
                status = excluded.status,
                updated_at = excluded.updated_at,
                provenance_refs_json = excluded.provenance_refs_json
            """,
            (
                allocation_id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.idea_id,
                record.display_key,
                "active",
                record.created_at,
                record.updated_at,
                _dumps(record.provenance_refs),
            ),
        )

    def upsert_research_idea_realization(self, record: ResearchIdeaRealization, *, validate: bool = True) -> None:
        diagnostics = self.validate_research_idea_realization(record) if validate else []
        errors = [item for item in diagnostics if item.get("severity") == "error"]
        if errors:
            codes = ", ".join(str(item.get("code") or "idea_realization_error") for item in errors)
            raise ValueError(f"Invalid research idea realization {record.id}: {codes}")
        if record.latest:
            self.connection.execute(
                """
                UPDATE research_idea_realizations
                SET latest = 0, updated_at = ?
                WHERE topic_workspace_id = ? AND idea_id = ? AND id != ?
                """,
                (record.updated_at, record.topic_workspace_id, record.idea_id, record.id),
            )
        self.connection.execute(
            """
            INSERT INTO research_idea_realizations
                (
                    id, research_topic_id, topic_workspace_id, idea_id, record_id,
                    source_json_path, realization_stage, semantic_id, latest, metadata_json,
                    created_at, updated_at, provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                record_id = excluded.record_id,
                source_json_path = excluded.source_json_path,
                realization_stage = excluded.realization_stage,
                semantic_id = excluded.semantic_id,
                latest = excluded.latest,
                metadata_json = excluded.metadata_json,
                updated_at = excluded.updated_at,
                provenance_refs_json = excluded.provenance_refs_json
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.idea_id,
                record.record_id,
                record.source_json_path,
                record.realization_stage,
                record.semantic_id,
                1 if record.latest else 0,
                _dumps(record.metadata),
                record.created_at,
                record.updated_at,
                _dumps(record.provenance_refs),
            ),
        )

    def list_research_idea_realizations(
        self,
        *,
        topic_workspace_id: str | None = None,
        idea_id: str | None = None,
        record_id: str | None = None,
    ) -> list[ResearchIdeaRealization]:
        if not _table_exists(self.connection, "research_idea_realizations"):
            return []
        query = "SELECT * FROM research_idea_realizations"
        clauses: list[str] = []
        params: list[object] = []
        for column, value in (
            ("topic_workspace_id", topic_workspace_id),
            ("idea_id", idea_id),
            ("record_id", record_id),
        ):
            if value is not None:
                clauses.append(f"{column} = ?")
                params.append(value)
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY latest DESC, updated_at DESC, id"
        return [_row_to_research_idea_realization(row) for row in self.connection.execute(query, params)]

    def get_research_idea_realization(self, realization_id: str) -> ResearchIdeaRealization | None:
        if not _table_exists(self.connection, "research_idea_realizations"):
            return None
        row = self.connection.execute("SELECT * FROM research_idea_realizations WHERE id = ? LIMIT 1", (realization_id,)).fetchone()
        return _row_to_research_idea_realization(row) if row is not None else None

    def upsert_research_idea_generation_group(self, record: ResearchIdeaGenerationGroup) -> None:
        self.connection.execute(
            """
            INSERT INTO research_idea_generation_groups
                (
                    id, research_topic_id, topic_workspace_id, purpose, parent_set_digest,
                    producer_skill, decision_record_id, metadata_json, created_at, updated_at,
                    provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                purpose = excluded.purpose,
                parent_set_digest = excluded.parent_set_digest,
                producer_skill = excluded.producer_skill,
                decision_record_id = excluded.decision_record_id,
                metadata_json = excluded.metadata_json,
                updated_at = excluded.updated_at,
                provenance_refs_json = excluded.provenance_refs_json
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.purpose,
                record.parent_set_digest,
                record.producer_skill,
                record.decision_record_id,
                _dumps(record.metadata),
                record.created_at,
                record.updated_at,
                _dumps(record.provenance_refs),
            ),
        )

    def get_research_idea_generation_group(self, group_id: str) -> ResearchIdeaGenerationGroup | None:
        if not _table_exists(self.connection, "research_idea_generation_groups"):
            return None
        row = self.connection.execute("SELECT * FROM research_idea_generation_groups WHERE id = ?", (group_id,)).fetchone()
        return _row_to_research_idea_generation_group(row) if row is not None else None

    def list_research_idea_generation_groups(
        self,
        *,
        topic_workspace_id: str | None = None,
    ) -> list[ResearchIdeaGenerationGroup]:
        if not _table_exists(self.connection, "research_idea_generation_groups"):
            return []
        query = "SELECT * FROM research_idea_generation_groups"
        params: list[object] = []
        if topic_workspace_id is not None:
            query += " WHERE topic_workspace_id = ?"
            params.append(topic_workspace_id)
        query += " ORDER BY updated_at DESC, id"
        return [_row_to_research_idea_generation_group(row) for row in self.connection.execute(query, params)]

    def upsert_research_idea_lineage_edge(self, record: ResearchIdeaLineageEdge, *, validate: bool = True) -> None:
        diagnostics = self.validate_research_idea_lineage_edge(record) if validate else []
        errors = [item for item in diagnostics if item.get("severity") == "error"]
        if errors:
            codes = ", ".join(str(item.get("code") or "idea_lineage_error") for item in errors)
            raise ValueError(f"Invalid research idea lineage edge {record.id}: {codes}")
        self.connection.execute(
            """
            INSERT INTO research_idea_lineage_edges
                (
                    id, research_topic_id, topic_workspace_id, parent_idea_id, child_idea_id,
                    lineage_kind, parent_role, generation_id, decision_record_id, rationale,
                    status, confidence, metadata_json, created_at, updated_at, provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                parent_idea_id = excluded.parent_idea_id,
                child_idea_id = excluded.child_idea_id,
                lineage_kind = excluded.lineage_kind,
                parent_role = excluded.parent_role,
                generation_id = excluded.generation_id,
                decision_record_id = excluded.decision_record_id,
                rationale = excluded.rationale,
                status = excluded.status,
                confidence = excluded.confidence,
                metadata_json = excluded.metadata_json,
                updated_at = excluded.updated_at,
                provenance_refs_json = excluded.provenance_refs_json
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.parent_idea_id,
                record.child_idea_id,
                record.lineage_kind,
                record.parent_role,
                record.generation_id,
                record.decision_record_id,
                record.rationale,
                record.status,
                record.confidence,
                _dumps(record.metadata),
                record.created_at,
                record.updated_at,
                _dumps(record.provenance_refs),
            ),
        )

    def list_research_idea_lineage_edges(
        self,
        *,
        topic_workspace_id: str | None = None,
        parent_idea_id: str | None = None,
        child_idea_id: str | None = None,
        generation_id: str | None = None,
        include_archived: bool = False,
    ) -> list[ResearchIdeaLineageEdge]:
        if not _table_exists(self.connection, "research_idea_lineage_edges"):
            return []
        query = "SELECT * FROM research_idea_lineage_edges"
        clauses: list[str] = []
        params: list[object] = []
        for column, value in (
            ("topic_workspace_id", topic_workspace_id),
            ("parent_idea_id", parent_idea_id),
            ("child_idea_id", child_idea_id),
            ("generation_id", generation_id),
        ):
            if value is not None:
                clauses.append(f"{column} = ?")
                params.append(value)
        if not include_archived:
            clauses.append("status != ?")
            params.append("archived")
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY created_at, parent_idea_id, child_idea_id, id"
        return [_row_to_research_idea_lineage_edge(row) for row in self.connection.execute(query, params)]

    def upsert_research_idea_state_transition(
        self,
        record: ResearchIdeaStateTransition,
        *,
        validate: bool = True,
    ) -> None:
        diagnostics = self.validate_research_idea_state_transition(record) if validate else []
        errors = [item for item in diagnostics if item.get("severity") == "error"]
        if errors:
            codes = ", ".join(str(item.get("code") or "idea_transition_error") for item in errors)
            raise ValueError(f"Invalid Research Idea transition {record.id}: {codes}")
        self.connection.execute(
            """
            INSERT INTO research_idea_state_transitions
                (
                    id, research_topic_id, topic_workspace_id, idea_id, facet,
                    previous_value, next_value, operation_id, actor_ref, reason_code,
                    rationale, decision_record_id, gate_id, evidence_item_refs_json,
                    artifact_refs_json, finding_refs_json, research_task_id, run_id,
                    provenance_record_refs_json, metadata_json, transitioned_at,
                    provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                previous_value = excluded.previous_value,
                next_value = excluded.next_value,
                operation_id = excluded.operation_id,
                actor_ref = excluded.actor_ref,
                reason_code = excluded.reason_code,
                rationale = excluded.rationale,
                decision_record_id = excluded.decision_record_id,
                gate_id = excluded.gate_id,
                evidence_item_refs_json = excluded.evidence_item_refs_json,
                artifact_refs_json = excluded.artifact_refs_json,
                finding_refs_json = excluded.finding_refs_json,
                research_task_id = excluded.research_task_id,
                run_id = excluded.run_id,
                provenance_record_refs_json = excluded.provenance_record_refs_json,
                metadata_json = excluded.metadata_json,
                transitioned_at = excluded.transitioned_at,
                provenance_refs_json = excluded.provenance_refs_json
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.idea_id,
                record.facet,
                record.previous_value,
                record.next_value,
                record.operation_id,
                record.actor_ref,
                record.reason_code,
                record.rationale,
                record.decision_record_id,
                record.gate_id,
                _dumps(record.evidence_item_refs),
                _dumps(record.artifact_refs),
                _dumps(record.finding_refs),
                record.research_task_id,
                record.run_id,
                _dumps(record.provenance_record_refs),
                _dumps(record.metadata),
                record.transitioned_at,
                _dumps(record.provenance_refs),
            ),
        )

    def get_research_idea_state_transition(self, transition_id: str) -> ResearchIdeaStateTransition | None:
        if not _table_exists(self.connection, "research_idea_state_transitions"):
            return None
        row = self.connection.execute(
            "SELECT * FROM research_idea_state_transitions WHERE id = ? LIMIT 1",
            (transition_id,),
        ).fetchone()
        return _row_to_research_idea_state_transition(row) if row is not None else None

    def list_research_idea_state_transitions(
        self,
        *,
        topic_workspace_id: str | None = None,
        idea_id: str | None = None,
        operation_id: str | None = None,
        decision_record_id: str | None = None,
    ) -> list[ResearchIdeaStateTransition]:
        if not _table_exists(self.connection, "research_idea_state_transitions"):
            return []
        query = "SELECT * FROM research_idea_state_transitions"
        clauses: list[str] = []
        params: list[object] = []
        for column, value in (
            ("topic_workspace_id", topic_workspace_id),
            ("idea_id", idea_id),
            ("operation_id", operation_id),
            ("decision_record_id", decision_record_id),
        ):
            if value is not None:
                clauses.append(f"{column} = ?")
                params.append(value)
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY transitioned_at, id"
        return [_row_to_research_idea_state_transition(row) for row in self.connection.execute(query, params)]

    def upsert_research_idea_decision_option(
        self,
        record: ResearchIdeaDecisionOption,
        *,
        validate: bool = True,
    ) -> None:
        diagnostics = self.validate_research_idea_decision_option(record) if validate else []
        errors = [item for item in diagnostics if item.get("severity") == "error"]
        if errors:
            codes = ", ".join(str(item.get("code") or "idea_decision_option_error") for item in errors)
            raise ValueError(f"Invalid Research Idea decision option {record.id}: {codes}")
        self.connection.execute(
            """
            INSERT INTO research_idea_decision_options
                (
                    id, research_topic_id, topic_workspace_id, decision_record_id,
                    idea_id, outcome, option_role, ordinal, generation_id, rationale,
                    consequence, actor_ref, supporting_refs_json, operation_id,
                    metadata_json, created_at, updated_at, provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(topic_workspace_id, decision_record_id, idea_id) DO UPDATE SET
                outcome = excluded.outcome,
                option_role = excluded.option_role,
                ordinal = excluded.ordinal,
                generation_id = excluded.generation_id,
                rationale = excluded.rationale,
                consequence = excluded.consequence,
                actor_ref = excluded.actor_ref,
                supporting_refs_json = excluded.supporting_refs_json,
                operation_id = excluded.operation_id,
                metadata_json = excluded.metadata_json,
                updated_at = excluded.updated_at,
                provenance_refs_json = excluded.provenance_refs_json
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.decision_record_id,
                record.idea_id,
                record.outcome,
                record.option_role,
                record.ordinal,
                record.generation_id,
                record.rationale,
                record.consequence,
                record.actor_ref,
                _dumps(record.supporting_refs),
                record.operation_id,
                _dumps(record.metadata),
                record.created_at,
                record.updated_at,
                _dumps(record.provenance_refs),
            ),
        )

    def get_research_idea_decision_option(self, option_id: str) -> ResearchIdeaDecisionOption | None:
        if not _table_exists(self.connection, "research_idea_decision_options"):
            return None
        row = self.connection.execute(
            "SELECT * FROM research_idea_decision_options WHERE id = ? LIMIT 1",
            (option_id,),
        ).fetchone()
        return _row_to_research_idea_decision_option(row) if row is not None else None

    def list_research_idea_decision_options(
        self,
        *,
        topic_workspace_id: str | None = None,
        decision_record_id: str | None = None,
        idea_id: str | None = None,
        generation_id: str | None = None,
    ) -> list[ResearchIdeaDecisionOption]:
        if not _table_exists(self.connection, "research_idea_decision_options"):
            return []
        query = "SELECT * FROM research_idea_decision_options"
        clauses: list[str] = []
        params: list[object] = []
        for column, value in (
            ("topic_workspace_id", topic_workspace_id),
            ("decision_record_id", decision_record_id),
            ("idea_id", idea_id),
            ("generation_id", generation_id),
        ):
            if value is not None:
                clauses.append(f"{column} = ?")
                params.append(value)
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY created_at, COALESCE(ordinal, 2147483647), id"
        return [_row_to_research_idea_decision_option(row) for row in self.connection.execute(query, params)]

    def upsert_research_idea_operation(self, record: ResearchIdeaOperation) -> None:
        diagnostics = self.validate_research_idea_operation(record)
        errors = [item for item in diagnostics if item.get("severity") == "error"]
        if errors:
            codes = ", ".join(str(item.get("code") or "idea_operation_error") for item in errors)
            raise ValueError(f"Invalid Research Idea operation {record.operation_id}: {codes}")
        existing = self.get_research_idea_operation_by_idempotency_key(
            record.idempotency_key,
            topic_workspace_id=record.topic_workspace_id,
        )
        if existing is not None and existing.input_digest != record.input_digest:
            raise ValueError(f"Research Idea idempotency key has different input: {record.idempotency_key}")
        self.connection.execute(
            """
            INSERT INTO research_idea_operations
                (
                    id, research_topic_id, topic_workspace_id, operation_id,
                    idempotency_key, action_kind, input_digest, status, result_json,
                    actor_ref, metadata_json, created_at, updated_at, provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(topic_workspace_id, operation_id) DO UPDATE SET
                status = excluded.status,
                result_json = excluded.result_json,
                actor_ref = excluded.actor_ref,
                metadata_json = excluded.metadata_json,
                updated_at = excluded.updated_at,
                provenance_refs_json = excluded.provenance_refs_json
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.operation_id,
                record.idempotency_key,
                record.action_kind,
                record.input_digest,
                record.status,
                _dumps(record.result),
                record.actor_ref,
                _dumps(record.metadata),
                record.created_at,
                record.updated_at,
                _dumps(record.provenance_refs),
            ),
        )

    def get_research_idea_operation(self, operation_id: str, *, topic_workspace_id: str | None = None) -> ResearchIdeaOperation | None:
        if not _table_exists(self.connection, "research_idea_operations"):
            return None
        if topic_workspace_id is None:
            row = self.connection.execute(
                "SELECT * FROM research_idea_operations WHERE operation_id = ? LIMIT 1",
                (operation_id,),
            ).fetchone()
        else:
            row = self.connection.execute(
                "SELECT * FROM research_idea_operations WHERE topic_workspace_id = ? AND operation_id = ? LIMIT 1",
                (topic_workspace_id, operation_id),
            ).fetchone()
        return _row_to_research_idea_operation(row) if row is not None else None

    def get_research_idea_operation_by_idempotency_key(
        self,
        idempotency_key: str,
        *,
        topic_workspace_id: str,
    ) -> ResearchIdeaOperation | None:
        if not _table_exists(self.connection, "research_idea_operations"):
            return None
        row = self.connection.execute(
            "SELECT * FROM research_idea_operations WHERE topic_workspace_id = ? AND idempotency_key = ? LIMIT 1",
            (topic_workspace_id, idempotency_key),
        ).fetchone()
        return _row_to_research_idea_operation(row) if row is not None else None

    def list_research_idea_operations(
        self,
        *,
        topic_workspace_id: str | None = None,
        status: str | None = None,
    ) -> list[ResearchIdeaOperation]:
        if not _table_exists(self.connection, "research_idea_operations"):
            return []
        query = "SELECT * FROM research_idea_operations"
        clauses: list[str] = []
        params: list[object] = []
        for column, value in (("topic_workspace_id", topic_workspace_id), ("status", status)):
            if value is not None:
                clauses.append(f"{column} = ?")
                params.append(value)
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY created_at, operation_id"
        return [_row_to_research_idea_operation(row) for row in self.connection.execute(query, params)]

    def validate_research_idea_state_transition(
        self,
        record: ResearchIdeaStateTransition,
        *,
        check_current: bool = True,
    ) -> list[dict[str, object]]:
        diagnostics: list[dict[str, object]] = []
        allowed_values: dict[str, tuple[str, ...]] = {
            "exploration_state": RESEARCH_IDEA_EXPLORATION_STATES,
            "decision_state": RESEARCH_IDEA_DECISION_STATES,
            "evidence_state": RESEARCH_IDEA_EVIDENCE_STATES,
            "archive_state": RESEARCH_IDEA_ARCHIVE_STATES,
            "visibility": RESEARCH_IDEA_VISIBILITIES,
        }
        if record.facet not in RESEARCH_IDEA_FACETS:
            diagnostics.append(_lineage_diag("error", "idea_transition_facet_unsupported", f"Unsupported Research Idea transition facet: {record.facet}", transition_id=record.id))
        else:
            vocabulary = allowed_values[record.facet]
            if record.previous_value not in vocabulary:
                diagnostics.append(_lineage_diag("error", "idea_transition_previous_value_unsupported", f"Unsupported previous value for {record.facet}: {record.previous_value}", transition_id=record.id))
            if record.next_value not in vocabulary:
                diagnostics.append(_lineage_diag("error", "idea_transition_next_value_unsupported", f"Unsupported next value for {record.facet}: {record.next_value}", transition_id=record.id))
        idea = self.get_research_idea(record.idea_id, topic_workspace_id=record.topic_workspace_id)
        if idea is None:
            diagnostics.append(_lineage_diag("error", "idea_transition_idea_missing", f"Research Idea transition references a missing idea: {record.idea_id}", transition_id=record.id, idea_id=record.idea_id))
        elif idea.research_topic_id != record.research_topic_id:
            diagnostics.append(_lineage_diag("error", "idea_transition_idea_cross_topic", f"Research Idea transition references an idea outside the Research Topic: {record.idea_id}", transition_id=record.id, idea_id=record.idea_id))
        elif check_current and record.facet in allowed_values:
            current = str(getattr(idea, record.facet))
            if current != record.previous_value:
                diagnostics.append(_lineage_diag("error", "idea_transition_expected_state_conflict", f"Research Idea {record.idea_id} has {record.facet}={current}, not expected {record.previous_value}.", transition_id=record.id, idea_id=record.idea_id, current_value=current))
        if not record.operation_id.strip():
            diagnostics.append(_lineage_diag("error", "idea_transition_operation_missing", "Research Idea transition requires an operation id.", transition_id=record.id))
        if not record.actor_ref.strip():
            diagnostics.append(_lineage_diag("error", "idea_transition_actor_missing", "Research Idea transition requires an actor ref.", transition_id=record.id))
        if not record.rationale.strip():
            diagnostics.append(_lineage_diag("error", "idea_transition_rationale_missing", "Research Idea transition requires a rationale.", transition_id=record.id))
        if record.facet == "decision_state" and record.next_value == "closed":
            if record.reason_code not in RESEARCH_IDEA_CLOSURE_REASONS:
                diagnostics.append(_lineage_diag("error", "idea_closure_reason_missing", "A closed Research Idea transition requires a supported closure reason.", transition_id=record.id, idea_id=record.idea_id))
            if record.decision_record_id is None and not record.provenance_record_refs:
                diagnostics.append(_lineage_diag("error", "idea_closure_context_missing", "A closed Research Idea transition requires a Decision Record or Provenance Record ref.", transition_id=record.id, idea_id=record.idea_id))
        for ref, kind, field_name in (
            (record.decision_record_id, "decision_record", "decision_record_id"),
            (record.gate_id, "gate", "gate_id"),
            (record.research_task_id, "research_task", "research_task_id"),
            (record.run_id, "run", "run_id"),
        ):
            if ref is not None:
                diagnostics.extend(self._validate_research_idea_lifecycle_ref(ref, record, expected_kind=kind, field_name=field_name))
        for refs, kind, field_name in (
            (record.evidence_item_refs, "evidence_item", "evidence_item_refs"),
            (record.artifact_refs, "artifact", "artifact_refs"),
            (record.finding_refs, "finding", "finding_refs"),
            (record.provenance_record_refs, "provenance_record", "provenance_record_refs"),
        ):
            for ref in refs:
                diagnostics.extend(self._validate_research_idea_lifecycle_ref(ref, record, expected_kind=kind, field_name=field_name))
        return diagnostics

    def validate_research_idea_decision_option(self, record: ResearchIdeaDecisionOption) -> list[dict[str, object]]:
        diagnostics: list[dict[str, object]] = []
        if record.outcome not in RESEARCH_IDEA_DECISION_OPTION_OUTCOMES:
            diagnostics.append(_lineage_diag("error", "idea_decision_option_outcome_unsupported", f"Unsupported Research Idea decision option outcome: {record.outcome}", option_id=record.id))
        if not record.operation_id.strip():
            diagnostics.append(_lineage_diag("error", "idea_decision_option_operation_missing", "Research Idea decision option requires an operation id.", option_id=record.id))
        idea = self.get_research_idea(record.idea_id, topic_workspace_id=record.topic_workspace_id)
        if idea is None:
            diagnostics.append(_lineage_diag("error", "idea_decision_option_idea_missing", f"Decision option references a missing Research Idea: {record.idea_id}", option_id=record.id, idea_id=record.idea_id))
        elif idea.research_topic_id != record.research_topic_id:
            diagnostics.append(_lineage_diag("error", "idea_decision_option_idea_cross_topic", f"Decision option references a Research Idea outside the Research Topic: {record.idea_id}", option_id=record.id, idea_id=record.idea_id))
        diagnostics.extend(self._validate_research_idea_lifecycle_ref(record.decision_record_id, record, expected_kind="decision_record", field_name="decision_record_id"))
        if record.generation_id is not None:
            generation = self.get_research_idea_generation_group(record.generation_id)
            if generation is None:
                diagnostics.append(_lineage_diag("error", "idea_decision_option_generation_missing", f"Decision option generation group is missing: {record.generation_id}", option_id=record.id, generation_id=record.generation_id))
            elif generation.research_topic_id != record.research_topic_id or generation.topic_workspace_id != record.topic_workspace_id:
                diagnostics.append(_lineage_diag("error", "idea_decision_option_generation_cross_topic", f"Decision option generation group is outside the Topic Workspace: {record.generation_id}", option_id=record.id, generation_id=record.generation_id))
        for ref in record.supporting_refs:
            diagnostics.extend(self._validate_research_idea_lifecycle_ref(ref, record, expected_kind=None, field_name="supporting_refs"))
        return diagnostics

    def validate_research_idea_operation(self, record: ResearchIdeaOperation) -> list[dict[str, object]]:
        diagnostics: list[dict[str, object]] = []
        if record.status not in RESEARCH_IDEA_OPERATION_STATUSES:
            diagnostics.append(_lineage_diag("error", "idea_operation_status_unsupported", f"Unsupported Research Idea operation status: {record.status}", operation_id=record.operation_id))
        for field_name, value in (
            ("operation_id", record.operation_id),
            ("idempotency_key", record.idempotency_key),
            ("action_kind", record.action_kind),
            ("input_digest", record.input_digest),
        ):
            if not value.strip():
                diagnostics.append(_lineage_diag("error", f"idea_operation_{field_name}_missing", f"Research Idea operation requires {field_name}.", operation_id=record.operation_id))
        existing = self.get_research_idea_operation_by_idempotency_key(record.idempotency_key, topic_workspace_id=record.topic_workspace_id)
        if existing is not None and existing.operation_id != record.operation_id:
            diagnostics.append(_lineage_diag("error", "idea_operation_idempotency_conflict", f"Research Idea idempotency key is already used by {existing.operation_id}.", operation_id=record.operation_id, existing_operation_id=existing.operation_id))
        return diagnostics

    def apply_research_idea_mutation(
        self,
        *,
        transitions: list[ResearchIdeaStateTransition],
        decision_options: list[ResearchIdeaDecisionOption] | None = None,
        operation: ResearchIdeaOperation | None = None,
        manage_transaction: bool = True,
    ) -> dict[str, object]:
        """Validate and commit one correlated Research Idea mutation atomically."""

        options = decision_options or []
        if operation is not None:
            existing = self.get_research_idea_operation_by_idempotency_key(
                operation.idempotency_key,
                topic_workspace_id=operation.topic_workspace_id,
            )
            if existing is not None:
                if existing.input_digest != operation.input_digest:
                    raise ValueError(f"Research Idea idempotency key has different input: {operation.idempotency_key}")
                return {
                    "replayed": True,
                    "operation": existing.to_json(),
                    "ideas": [],
                    "transitions": [item.to_json() for item in self.list_research_idea_state_transitions(topic_workspace_id=existing.topic_workspace_id, operation_id=existing.operation_id)],
                    "decision_options": [item.to_json() for item in self.list_research_idea_decision_options(topic_workspace_id=existing.topic_workspace_id) if item.operation_id == existing.operation_id],
                }

        diagnostics: list[dict[str, object]] = []
        current_ideas: dict[str, ResearchIdea] = {}
        state_by_idea: dict[str, dict[str, str]] = {}
        closure_reason_by_idea: dict[str, str | None] = {}
        updated_at_by_idea: dict[str, str] = {}
        operation_ids = {item.operation_id for item in transitions} | {item.operation_id for item in options}
        if operation is not None:
            operation_ids.add(operation.operation_id)
        if len(operation_ids) > 1:
            diagnostics.append(_lineage_diag("error", "idea_mutation_operation_mismatch", "All transitions, decision options, and the idempotency record must share one operation id.", operation_ids=sorted(operation_ids)))
        for transition in transitions:
            diagnostics.extend(self.validate_research_idea_state_transition(transition, check_current=False))
            idea = current_ideas.get(transition.idea_id)
            if idea is None:
                idea = self.get_research_idea(transition.idea_id, topic_workspace_id=transition.topic_workspace_id)
                if idea is None:
                    continue
                current_ideas[transition.idea_id] = idea
                state_by_idea[transition.idea_id] = {
                    "exploration_state": idea.exploration_state,
                    "decision_state": idea.decision_state,
                    "evidence_state": idea.evidence_state,
                    "archive_state": idea.archive_state,
                    "visibility": idea.visibility,
                }
            current_value = state_by_idea[transition.idea_id].get(transition.facet)
            if current_value is not None and current_value != transition.previous_value:
                diagnostics.append(_lineage_diag("error", "idea_transition_expected_state_conflict", f"Research Idea {transition.idea_id} has {transition.facet}={current_value}, not expected {transition.previous_value}.", transition_id=transition.id, idea_id=transition.idea_id, current_value=current_value))
                continue
            state_by_idea[transition.idea_id][transition.facet] = transition.next_value
            updated_at_by_idea[transition.idea_id] = max(updated_at_by_idea.get(transition.idea_id, transition.transitioned_at), transition.transitioned_at)
            if transition.facet == "decision_state" and transition.next_value == "closed":
                closure_reason_by_idea[transition.idea_id] = transition.reason_code
        for option in options:
            diagnostics.extend(self.validate_research_idea_decision_option(option))
        if operation is not None:
            diagnostics.extend(self.validate_research_idea_operation(operation))

        updated_ideas: list[ResearchIdea] = []
        for idea_id, idea in current_ideas.items():
            state = state_by_idea[idea_id]
            status = project_research_idea_compatibility_status(
                exploration_state=cast(ResearchIdeaExplorationState, state["exploration_state"]),
                decision_state=cast(ResearchIdeaDecisionState, state["decision_state"]),
                evidence_state=cast(ResearchIdeaEvidenceState, state["evidence_state"]),
                archive_state=cast(ResearchIdeaArchiveState, state["archive_state"]),
                closure_reason=closure_reason_by_idea.get(idea_id),
                preserved_status=idea.status,
            )
            updated = replace(
                idea,
                exploration_state=cast(ResearchIdeaExplorationState, state["exploration_state"]),
                decision_state=cast(ResearchIdeaDecisionState, state["decision_state"]),
                evidence_state=cast(ResearchIdeaEvidenceState, state["evidence_state"]),
                archive_state=cast(ResearchIdeaArchiveState, state["archive_state"]),
                visibility=state["visibility"],
                status=status,
                updated_at=updated_at_by_idea.get(idea_id, idea.updated_at),
            )
            diagnostics.extend(self.validate_research_idea(updated))
            updated_ideas.append(updated)
        errors = [item for item in diagnostics if item.get("severity") == "error"]
        if errors:
            codes = ", ".join(sorted({str(item.get("code") or "idea_mutation_error") for item in errors}))
            raise ValueError(f"Research Idea mutation failed validation: {codes}")

        transaction = self.connection if manage_transaction else nullcontext()
        with transaction:
            for idea in updated_ideas:
                self.upsert_research_idea(idea, validate=False)
            for transition in transitions:
                self.upsert_research_idea_state_transition(transition, validate=False)
            for option in options:
                self.upsert_research_idea_decision_option(option, validate=False)
            if operation is not None:
                self.upsert_research_idea_operation(operation)
        return {
            "replayed": False,
            "operation": operation.to_json() if operation is not None else None,
            "ideas": [item.to_json() for item in updated_ideas],
            "transitions": [item.to_json() for item in transitions],
            "decision_options": [item.to_json() for item in options],
            "diagnostics": diagnostics,
        }

    def _validate_research_idea_lifecycle_ref(
        self,
        ref: str,
        owner: ResearchIdeaStateTransition | ResearchIdeaDecisionOption,
        *,
        expected_kind: str | None,
        field_name: str,
    ) -> list[dict[str, object]]:
        lifecycle = self.get_lifecycle_record(ref)
        owner_id = owner.id
        if lifecycle is None:
            return [_lineage_diag("error", "idea_durable_ref_missing", f"Research Idea {field_name} ref is missing: {ref}", owner_id=owner_id, field=field_name, ref=ref)]
        if lifecycle.research_topic_id != owner.research_topic_id or lifecycle.topic_workspace_id != owner.topic_workspace_id:
            return [_lineage_diag("error", "idea_durable_ref_cross_topic", f"Research Idea {field_name} ref is outside the Topic Workspace: {ref}", owner_id=owner_id, field=field_name, ref=ref)]
        if expected_kind is not None and lifecycle.record_kind != expected_kind:
            return [_lineage_diag("error", "idea_durable_ref_kind_mismatch", f"Research Idea {field_name} ref {ref} is {lifecycle.record_kind}, expected {expected_kind}.", owner_id=owner_id, field=field_name, ref=ref)]
        return []

    def validate_research_idea(self, record: ResearchIdea) -> list[dict[str, object]]:
        diagnostics: list[dict[str, object]] = []
        if record.status not in RESEARCH_IDEA_STATUSES:
            diagnostics.append(_lineage_diag("error", "idea_status_unsupported", f"Unsupported idea status: {record.status}", idea_id=record.idea_id))
        if record.visibility not in RESEARCH_IDEA_VISIBILITIES:
            diagnostics.append(_lineage_diag("error", "idea_visibility_unsupported", f"Unsupported idea visibility: {record.visibility}", idea_id=record.idea_id))
        for field_name, value, vocabulary in (
            ("exploration_state", record.exploration_state, RESEARCH_IDEA_EXPLORATION_STATES),
            ("decision_state", record.decision_state, RESEARCH_IDEA_DECISION_STATES),
            ("evidence_state", record.evidence_state, RESEARCH_IDEA_EVIDENCE_STATES),
            ("archive_state", record.archive_state, RESEARCH_IDEA_ARCHIVE_STATES),
        ):
            if value not in vocabulary:
                diagnostics.append(_lineage_diag("error", f"idea_{field_name}_unsupported", f"Unsupported Research Idea {field_name}: {value}", idea_id=record.idea_id))
        projected_status = project_research_idea_compatibility_status(
            exploration_state=record.exploration_state,
            decision_state=record.decision_state,
            evidence_state=record.evidence_state,
            archive_state=record.archive_state,
            preserved_status=record.status,
        )
        if record.status != projected_status:
            diagnostics.append(_lineage_diag("error", "idea_compatibility_status_conflict", f"Deprecated Research Idea status {record.status} conflicts with canonical facet projection {projected_status}.", idea_id=record.idea_id, projected_status=projected_status))
        if not record.title.strip():
            diagnostics.append(_lineage_diag("error", "idea_title_missing", f"Research Idea has no title: {record.idea_id}", idea_id=record.idea_id))
        if not record.summary.strip():
            diagnostics.append(_lineage_diag("error", "idea_summary_missing", f"Research Idea has no summary: {record.idea_id}", idea_id=record.idea_id))
        if record.title.strip() and record.summary.strip() and record.title.strip() == record.summary.strip():
            diagnostics.append(_lineage_diag("warning", "idea_display_fields_duplicate", f"Research Idea title and summary are identical: {record.idea_id}", idea_id=record.idea_id))
        if record.display_key is None or not record.display_key.strip():
            diagnostics.append(_lineage_diag("warning", "idea_display_key_missing", f"Research Idea has no GUI display key: {record.idea_id}", idea_id=record.idea_id))
        elif re.fullmatch(r"I-[1-9][0-9]*", record.display_key) is None:
            diagnostics.append(_lineage_diag("error", "idea_display_key_invalid", f"Invalid Research Idea display key: {record.display_key}", idea_id=record.idea_id, display_key=record.display_key))
        if record.source_record_id is not None:
            source = self.get_lifecycle_record(record.source_record_id)
            if source is None:
                diagnostics.append(_lineage_diag("warning", "idea_source_record_missing", f"Idea source record is missing: {record.source_record_id}", idea_id=record.idea_id, record_id=record.source_record_id))
            elif source.research_topic_id != record.research_topic_id or source.topic_workspace_id != record.topic_workspace_id:
                diagnostics.append(_lineage_diag("error", "idea_source_record_cross_topic", f"Idea source record is outside the Topic Workspace: {record.source_record_id}", idea_id=record.idea_id, record_id=record.source_record_id))
        existing = self.connection.execute(
            "SELECT id FROM research_ideas WHERE topic_workspace_id = ? AND idea_id = ? AND id != ? LIMIT 1",
            (record.topic_workspace_id, record.idea_id, record.id),
        ).fetchone() if _table_exists(self.connection, "research_ideas") else None
        if existing is not None:
            diagnostics.append(_lineage_diag("error", "idea_id_duplicate", f"Duplicate canonical idea id: {record.idea_id}", idea_id=record.idea_id))
        if record.display_key:
            duplicate_key = self.connection.execute(
                "SELECT id, idea_id FROM research_ideas WHERE topic_workspace_id = ? AND display_key = ? AND id != ? LIMIT 1",
                (record.topic_workspace_id, record.display_key, record.id),
            ).fetchone() if _table_exists(self.connection, "research_ideas") else None
            if duplicate_key is not None:
                diagnostics.append(_lineage_diag("error", "idea_display_key_duplicate", f"Duplicate Research Idea display key: {record.display_key}", idea_id=record.idea_id, display_key=record.display_key))
            reserved_key = self.connection.execute(
                "SELECT idea_id FROM research_idea_display_keys WHERE topic_workspace_id = ? AND display_key = ? LIMIT 1",
                (record.topic_workspace_id, record.display_key),
            ).fetchone() if _table_exists(self.connection, "research_idea_display_keys") else None
            if reserved_key is not None and str(reserved_key["idea_id"]) != record.idea_id:
                diagnostics.append(_lineage_diag("error", "idea_display_key_reserved", f"Research Idea display key is already allocated: {record.display_key}", idea_id=record.idea_id, display_key=record.display_key))
        return diagnostics

    def validate_research_idea_realization(self, record: ResearchIdeaRealization) -> list[dict[str, object]]:
        diagnostics: list[dict[str, object]] = []
        idea = self.get_research_idea(record.idea_id, topic_workspace_id=record.topic_workspace_id)
        if idea is None:
            diagnostics.append(_lineage_diag("error", "idea_realization_idea_missing", f"Idea realization references a missing idea: {record.idea_id}", idea_id=record.idea_id))
        elif idea.research_topic_id != record.research_topic_id:
            diagnostics.append(_lineage_diag("error", "idea_realization_idea_cross_topic", f"Idea realization references an idea outside the Research Topic: {record.idea_id}", idea_id=record.idea_id))
        lifecycle = self.get_lifecycle_record(record.record_id)
        if lifecycle is None:
            diagnostics.append(_lineage_diag("error", "idea_realization_record_missing", f"Idea realization references a missing record: {record.record_id}", idea_id=record.idea_id, record_id=record.record_id))
        elif lifecycle.research_topic_id != record.research_topic_id or lifecycle.topic_workspace_id != record.topic_workspace_id:
            diagnostics.append(_lineage_diag("error", "idea_realization_record_cross_topic", f"Idea realization record is outside the Topic Workspace: {record.record_id}", idea_id=record.idea_id, record_id=record.record_id))
        return diagnostics

    def validate_research_idea_lineage_edge(self, record: ResearchIdeaLineageEdge) -> list[dict[str, object]]:
        diagnostics: list[dict[str, object]] = []
        if record.lineage_kind == "revision_of":
            diagnostics.append(_lineage_diag("error", "idea_revision_edge_rejected", "Idea-level revision_of edges are rejected; update the same idea and add a realization.", edge_id=record.id))
        elif record.lineage_kind not in RESEARCH_IDEA_LINEAGE_KINDS:
            diagnostics.append(_lineage_diag("error", "idea_lineage_kind_unsupported", f"Unsupported idea lineage kind: {record.lineage_kind}", edge_id=record.id))
        if record.status not in RESEARCH_IDEA_LINEAGE_STATUSES:
            diagnostics.append(_lineage_diag("error", "idea_lineage_status_unsupported", f"Unsupported idea lineage status: {record.status}", edge_id=record.id))
        parent = self.get_research_idea(record.parent_idea_id, topic_workspace_id=record.topic_workspace_id)
        child = self.get_research_idea(record.child_idea_id, topic_workspace_id=record.topic_workspace_id)
        if parent is None:
            diagnostics.append(_lineage_diag("error", "idea_lineage_parent_missing", f"Idea lineage parent is missing: {record.parent_idea_id}", edge_id=record.id, idea_id=record.parent_idea_id))
        elif parent.research_topic_id != record.research_topic_id:
            diagnostics.append(_lineage_diag("error", "idea_lineage_parent_cross_topic", f"Idea lineage parent is outside the Research Topic: {record.parent_idea_id}", edge_id=record.id, idea_id=record.parent_idea_id))
        if child is None:
            diagnostics.append(_lineage_diag("error", "idea_lineage_child_missing", f"Idea lineage child is missing: {record.child_idea_id}", edge_id=record.id, idea_id=record.child_idea_id))
        elif child.research_topic_id != record.research_topic_id:
            diagnostics.append(_lineage_diag("error", "idea_lineage_child_cross_topic", f"Idea lineage child is outside the Research Topic: {record.child_idea_id}", edge_id=record.id, idea_id=record.child_idea_id))
        if record.generation_id is not None:
            group = self.get_research_idea_generation_group(record.generation_id)
            if group is None:
                diagnostics.append(_lineage_diag("error", "idea_generation_group_missing", f"Idea generation group is missing: {record.generation_id}", edge_id=record.id, generation_id=record.generation_id))
            elif group.research_topic_id != record.research_topic_id or group.topic_workspace_id != record.topic_workspace_id:
                diagnostics.append(_lineage_diag("error", "idea_generation_group_cross_topic", f"Idea generation group is outside the Topic Workspace: {record.generation_id}", edge_id=record.id, generation_id=record.generation_id))
        if record.parent_idea_id == record.child_idea_id or self._research_idea_lineage_creates_cycle(record):
            diagnostics.append(_lineage_diag("error", "idea_lineage_cycle", f"Idea lineage edge would create a cycle: {record.parent_idea_id} -> {record.child_idea_id}", edge_id=record.id))
        return diagnostics

    def validate_research_idea_lineage(
        self,
        *,
        topic_workspace_id: str | None = None,
    ) -> list[dict[str, object]]:
        if not _table_exists(self.connection, "research_ideas"):
            return [_lineage_diag("warning", "research_idea_schema_missing", "Workspace Runtime has no canonical research idea tables yet.")]
        diagnostics: list[dict[str, object]] = []
        for idea in self.list_research_ideas(topic_workspace_id=topic_workspace_id, include_archived=True):
            diagnostics.extend(self.validate_research_idea(idea))
        for realization in self.list_research_idea_realizations(topic_workspace_id=topic_workspace_id):
            diagnostics.extend(self.validate_research_idea_realization(realization))
        for edge in self.list_research_idea_lineage_edges(topic_workspace_id=topic_workspace_id, include_archived=True):
            diagnostics.extend(self.validate_research_idea_lineage_edge(edge))
        for transition in self.list_research_idea_state_transitions(topic_workspace_id=topic_workspace_id):
            diagnostics.extend(self.validate_research_idea_state_transition(transition, check_current=False))
        for option in self.list_research_idea_decision_options(topic_workspace_id=topic_workspace_id):
            diagnostics.extend(self.validate_research_idea_decision_option(option))
        for operation in self.list_research_idea_operations(topic_workspace_id=topic_workspace_id):
            diagnostics.extend(self.validate_research_idea_operation(operation))
        return diagnostics

    def _research_idea_lineage_creates_cycle(self, record: ResearchIdeaLineageEdge) -> bool:
        if not _table_exists(self.connection, "research_idea_lineage_edges"):
            return False
        row = self.connection.execute(
            """
            WITH RECURSIVE descendants(idea_id) AS (
                SELECT child_idea_id
                FROM research_idea_lineage_edges
                WHERE topic_workspace_id = ?
                    AND parent_idea_id = ?
                    AND status != 'archived'
                    AND id != ?
                UNION
                SELECT edge.child_idea_id
                FROM research_idea_lineage_edges edge
                JOIN descendants ON edge.parent_idea_id = descendants.idea_id
                WHERE edge.topic_workspace_id = ?
                    AND edge.status != 'archived'
                    AND edge.id != ?
            )
            SELECT 1 AS found FROM descendants WHERE idea_id = ? LIMIT 1
            """,
            (
                record.topic_workspace_id,
                record.child_idea_id,
                record.id,
                record.topic_workspace_id,
                record.id,
                record.parent_idea_id,
            ),
        ).fetchone()
        return row is not None

    def upsert_artifact_format_registration(self, record: ArtifactFormatRegistrationRecord) -> None:
        if record.source_kind not in ARTIFACT_FORMAT_REGISTRATION_SOURCE_KINDS:
            raise ValueError(f"Unsupported Artifact Format registration source kind: {record.source_kind}")
        self.connection.execute(
            """
            INSERT INTO artifact_format_registrations
                (
                    id, research_topic_id, topic_workspace_id, format_profile_ref,
                    schema_ref, template_ref, output_format, source_kind, profile_json,
                    schema_snapshot_path, template_snapshot_path, original_schema_path,
                    original_template_path, profile_digest, schema_digest, template_digest,
                    diagnostics_json, actor_ref, created_at, updated_at, provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                schema_ref = excluded.schema_ref,
                template_ref = excluded.template_ref,
                output_format = excluded.output_format,
                source_kind = excluded.source_kind,
                profile_json = excluded.profile_json,
                schema_snapshot_path = excluded.schema_snapshot_path,
                template_snapshot_path = excluded.template_snapshot_path,
                original_schema_path = excluded.original_schema_path,
                original_template_path = excluded.original_template_path,
                profile_digest = excluded.profile_digest,
                schema_digest = excluded.schema_digest,
                template_digest = excluded.template_digest,
                diagnostics_json = excluded.diagnostics_json,
                actor_ref = excluded.actor_ref,
                updated_at = excluded.updated_at,
                provenance_refs_json = excluded.provenance_refs_json
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.format_profile_ref,
                record.schema_ref,
                record.template_ref,
                record.output_format,
                record.source_kind,
                _dumps(record.profile_json),
                record.schema_snapshot_path,
                record.template_snapshot_path,
                record.original_schema_path,
                record.original_template_path,
                record.profile_digest,
                record.schema_digest,
                record.template_digest,
                _dumps(record.diagnostics),
                record.actor_ref,
                record.created_at,
                record.updated_at,
                _dumps(record.provenance_refs),
            ),
        )

    def get_artifact_format_registration(
        self,
        *,
        topic_workspace_id: str,
        format_profile_ref: str,
    ) -> ArtifactFormatRegistrationRecord | None:
        row = self.connection.execute(
            """
            SELECT * FROM artifact_format_registrations
            WHERE topic_workspace_id = ? AND format_profile_ref = ?
            """,
            (topic_workspace_id, format_profile_ref),
        ).fetchone()
        return _row_to_artifact_format_registration(row) if row is not None else None

    def list_artifact_format_registrations(
        self,
        *,
        topic_workspace_id: str | None = None,
    ) -> list[ArtifactFormatRegistrationRecord]:
        if topic_workspace_id is None:
            rows = self.connection.execute("SELECT * FROM artifact_format_registrations ORDER BY format_profile_ref")
        else:
            rows = self.connection.execute(
                """
                SELECT * FROM artifact_format_registrations
                WHERE topic_workspace_id = ?
                ORDER BY format_profile_ref
                """,
                (topic_workspace_id,),
            )
        return [_row_to_artifact_format_registration(row) for row in rows]

    def upsert_structured_payload(self, record: StructuredResearchPayloadRecord) -> None:
        if record.validation_status not in STRUCTURED_PAYLOAD_VALIDATION_STATUSES:
            raise ValueError(f"Unsupported structured payload validation status: {record.validation_status}")
        if record.render_status not in STRUCTURED_PAYLOAD_RENDER_STATUSES:
            raise ValueError(f"Unsupported structured payload render status: {record.render_status}")
        lifecycle_record = self.get_lifecycle_record(record.record_id)
        if lifecycle_record is not None and (
            lifecycle_record.research_topic_id != record.research_topic_id
            or lifecycle_record.topic_workspace_id != record.topic_workspace_id
        ):
            raise ValueError("Structured payload owner does not match the linked lifecycle record.")
        self.connection.execute(
            """
            INSERT INTO structured_research_payloads
                (
                    id, record_id, research_topic_id, topic_workspace_id,
                    format_profile_ref, schema_ref, schema_version, schema_source_kind,
                    template_ref, template_source_kind, payload_json, payload_digest,
                    payload_file_path, payload_media_type, payload_manifest_path,
                    payload_source_path, revision_of_record_id, supersedes_record_id,
                    latest_for_semantic_id, legacy_rendered_markdown_path,
                    legacy_rendered_markdown_digest,
                    validation_status, validation_diagnostics_json, render_status,
                    render_diagnostics_json, rendered_markdown_path, rendered_markdown_digest,
                    created_at, updated_at, provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(record_id) DO UPDATE SET
                format_profile_ref = excluded.format_profile_ref,
                schema_ref = excluded.schema_ref,
                schema_version = excluded.schema_version,
                schema_source_kind = excluded.schema_source_kind,
                template_ref = excluded.template_ref,
                template_source_kind = excluded.template_source_kind,
                payload_json = excluded.payload_json,
                payload_digest = excluded.payload_digest,
                payload_file_path = excluded.payload_file_path,
                payload_media_type = excluded.payload_media_type,
                payload_manifest_path = excluded.payload_manifest_path,
                payload_source_path = excluded.payload_source_path,
                revision_of_record_id = excluded.revision_of_record_id,
                supersedes_record_id = excluded.supersedes_record_id,
                latest_for_semantic_id = excluded.latest_for_semantic_id,
                legacy_rendered_markdown_path = excluded.legacy_rendered_markdown_path,
                legacy_rendered_markdown_digest = excluded.legacy_rendered_markdown_digest,
                validation_status = excluded.validation_status,
                validation_diagnostics_json = excluded.validation_diagnostics_json,
                render_status = excluded.render_status,
                render_diagnostics_json = excluded.render_diagnostics_json,
                rendered_markdown_path = excluded.rendered_markdown_path,
                rendered_markdown_digest = excluded.rendered_markdown_digest,
                updated_at = excluded.updated_at,
                provenance_refs_json = excluded.provenance_refs_json
            """,
            (
                record.id,
                record.record_id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.format_profile_ref,
                record.schema_ref,
                record.schema_version,
                record.schema_source_kind,
                record.template_ref,
                record.template_source_kind,
                _dumps(record.payload_json),
                record.payload_digest,
                record.payload_file_path,
                record.payload_media_type,
                record.payload_manifest_path,
                record.payload_source_path,
                record.revision_of_record_id,
                record.supersedes_record_id,
                record.latest_for_semantic_id,
                record.legacy_rendered_markdown_path,
                record.legacy_rendered_markdown_digest,
                record.validation_status,
                _dumps(record.validation_diagnostics),
                record.render_status,
                _dumps(record.render_diagnostics),
                record.rendered_markdown_path,
                record.rendered_markdown_digest,
                record.created_at,
                record.updated_at,
                _dumps(record.provenance_refs),
            ),
        )

    def get_structured_payload(self, record_id: str) -> StructuredResearchPayloadRecord | None:
        row = self.connection.execute(
            "SELECT * FROM structured_research_payloads WHERE record_id = ?",
            (record_id,),
        ).fetchone()
        return _row_to_structured_payload(row) if row is not None else None

    def list_structured_payloads(
        self,
        *,
        topic_workspace_id: str | None = None,
        format_profile_ref: str | None = None,
        schema_ref: str | None = None,
        template_ref: str | None = None,
        validation_status: str | None = None,
        render_status: str | None = None,
        limit: int | None = None,
    ) -> list[StructuredResearchPayloadRecord]:
        query = "SELECT * FROM structured_research_payloads"
        clauses: list[str] = []
        params: list[object] = []
        for column, value in (
            ("topic_workspace_id", topic_workspace_id),
            ("format_profile_ref", format_profile_ref),
            ("schema_ref", schema_ref),
            ("template_ref", template_ref),
            ("validation_status", validation_status),
            ("render_status", render_status),
        ):
            if value is not None:
                clauses.append(f"{column} = ?")
                params.append(value)
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY updated_at DESC, created_at DESC, record_id"
        if limit is not None:
            query += " LIMIT ?"
            params.append(limit)
        return [_row_to_structured_payload(row) for row in self.connection.execute(query, params)]

    def delete_structured_payload(self, record_id: str) -> None:
        self.connection.execute("DELETE FROM structured_research_payloads WHERE record_id = ?", (record_id,))

    def delete_lifecycle_record(self, record_id: str) -> None:
        self.connection.execute("DELETE FROM lifecycle_records WHERE id = ?", (record_id,))

    def delete_artifact_format_registration(self, registration_id: str) -> None:
        self.connection.execute("DELETE FROM artifact_format_registrations WHERE id = ?", (registration_id,))

    def delete_readiness_record(self, record_id: str) -> None:
        self.connection.execute("DELETE FROM readiness_records WHERE id = ?", (record_id,))

    def upsert_reset_checkpoint(self, record: ResetCheckpointRecord) -> None:
        if record.status not in RESET_CHECKPOINT_STATUSES:
            raise ValueError(f"Unsupported reset checkpoint status: {record.status}")
        self.connection.execute(
            """
            INSERT INTO topic_reset_checkpoints
                (
                    id, research_topic_id, topic_workspace_id, status, payload_json,
                    payload_digest, checkpoint_digest, actor_ref, source_record_id,
                    rendered_markdown_path, rendered_markdown_digest, diagnostics_json,
                    created_at, updated_at, provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                status = excluded.status,
                payload_json = excluded.payload_json,
                payload_digest = excluded.payload_digest,
                checkpoint_digest = excluded.checkpoint_digest,
                actor_ref = excluded.actor_ref,
                source_record_id = excluded.source_record_id,
                rendered_markdown_path = excluded.rendered_markdown_path,
                rendered_markdown_digest = excluded.rendered_markdown_digest,
                diagnostics_json = excluded.diagnostics_json,
                updated_at = excluded.updated_at,
                provenance_refs_json = excluded.provenance_refs_json
            """,
            (
                record.id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.status,
                _dumps(record.payload_json),
                record.payload_digest,
                record.checkpoint_digest,
                record.actor_ref,
                record.source_record_id,
                record.rendered_markdown_path,
                record.rendered_markdown_digest,
                _dumps(record.diagnostics),
                record.created_at,
                record.updated_at,
                _dumps(record.provenance_refs),
            ),
        )

    def get_reset_checkpoint(self, checkpoint_id: str) -> ResetCheckpointRecord | None:
        if not _table_exists(self.connection, "topic_reset_checkpoints"):
            return None
        row = self.connection.execute(
            "SELECT * FROM topic_reset_checkpoints WHERE id = ?",
            (checkpoint_id,),
        ).fetchone()
        return _row_to_reset_checkpoint(row) if row is not None else None

    def latest_reset_checkpoint(self, *, topic_workspace_id: str) -> ResetCheckpointRecord | None:
        if not _table_exists(self.connection, "topic_reset_checkpoints"):
            return None
        row = self.connection.execute(
            """
            SELECT * FROM topic_reset_checkpoints
            WHERE topic_workspace_id = ?
            ORDER BY updated_at DESC, created_at DESC, id DESC
            LIMIT 1
            """,
            (topic_workspace_id,),
        ).fetchone()
        return _row_to_reset_checkpoint(row) if row is not None else None

    def list_reset_checkpoints(self, *, topic_workspace_id: str | None = None) -> list[ResetCheckpointRecord]:
        if not _table_exists(self.connection, "topic_reset_checkpoints"):
            return []
        if topic_workspace_id is None:
            rows = self.connection.execute("SELECT * FROM topic_reset_checkpoints ORDER BY updated_at DESC, id")
        else:
            rows = self.connection.execute(
                "SELECT * FROM topic_reset_checkpoints WHERE topic_workspace_id = ? ORDER BY updated_at DESC, id",
                (topic_workspace_id,),
            )
        return [_row_to_reset_checkpoint(row) for row in rows]

    def upsert_reset_plan(self, record: ResetPlanRecord, actions: list[ResetPlanActionRecord] | None = None) -> None:
        if record.status not in RESET_PLAN_STATUSES:
            raise ValueError(f"Unsupported reset plan status: {record.status}")
        self.connection.execute(
            """
            INSERT INTO topic_reset_plans
                (
                    id, checkpoint_id, research_topic_id, topic_workspace_id, status,
                    payload_json, payload_digest, checkpoint_digest, precondition_digest,
                    actor_ref, rendered_markdown_path, rendered_markdown_digest,
                    diagnostics_json, created_at, updated_at, provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                status = excluded.status,
                payload_json = excluded.payload_json,
                payload_digest = excluded.payload_digest,
                checkpoint_digest = excluded.checkpoint_digest,
                precondition_digest = excluded.precondition_digest,
                actor_ref = excluded.actor_ref,
                rendered_markdown_path = excluded.rendered_markdown_path,
                rendered_markdown_digest = excluded.rendered_markdown_digest,
                diagnostics_json = excluded.diagnostics_json,
                updated_at = excluded.updated_at,
                provenance_refs_json = excluded.provenance_refs_json
            """,
            (
                record.id,
                record.checkpoint_id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.status,
                _dumps(record.payload_json),
                record.payload_digest,
                record.checkpoint_digest,
                record.precondition_digest,
                record.actor_ref,
                record.rendered_markdown_path,
                record.rendered_markdown_digest,
                _dumps(record.diagnostics),
                record.created_at,
                record.updated_at,
                _dumps(record.provenance_refs),
            ),
        )
        if actions is not None:
            self.connection.execute("DELETE FROM topic_reset_plan_actions WHERE plan_id = ?", (record.id,))
            for action in actions:
                self.upsert_reset_plan_action(action)

    def get_reset_plan(self, plan_id: str) -> ResetPlanRecord | None:
        if not _table_exists(self.connection, "topic_reset_plans"):
            return None
        row = self.connection.execute(
            "SELECT * FROM topic_reset_plans WHERE id = ?",
            (plan_id,),
        ).fetchone()
        return _row_to_reset_plan(row) if row is not None else None

    def list_reset_plans(
        self,
        *,
        topic_workspace_id: str | None = None,
        checkpoint_id: str | None = None,
    ) -> list[ResetPlanRecord]:
        if not _table_exists(self.connection, "topic_reset_plans"):
            return []
        query = "SELECT * FROM topic_reset_plans"
        clauses: list[str] = []
        params: list[object] = []
        if topic_workspace_id is not None:
            clauses.append("topic_workspace_id = ?")
            params.append(topic_workspace_id)
        if checkpoint_id is not None:
            clauses.append("checkpoint_id = ?")
            params.append(checkpoint_id)
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY created_at DESC, id"
        return [_row_to_reset_plan(row) for row in self.connection.execute(query, params)]

    def upsert_reset_plan_action(self, record: ResetPlanActionRecord) -> None:
        if record.action not in RESET_PLAN_ACTIONS:
            raise ValueError(f"Unsupported reset plan action: {record.action}")
        if record.status not in RESET_PLAN_ACTION_STATUSES:
            raise ValueError(f"Unsupported reset plan action status: {record.status}")
        self.connection.execute(
            """
            INSERT OR REPLACE INTO topic_reset_plan_actions
                (
                    id, plan_id, action, target_kind, target_ref, target_path,
                    semantic_label, source_kind, status, details_json, created_at
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.id,
                record.plan_id,
                record.action,
                record.target_kind,
                record.target_ref,
                record.target_path,
                record.semantic_label,
                record.source_kind,
                record.status,
                _dumps(record.details),
                record.created_at,
            ),
        )

    def list_reset_plan_actions(self, *, plan_id: str) -> list[ResetPlanActionRecord]:
        if not _table_exists(self.connection, "topic_reset_plan_actions"):
            return []
        return [
            _row_to_reset_plan_action(row)
            for row in self.connection.execute(
                "SELECT * FROM topic_reset_plan_actions WHERE plan_id = ? ORDER BY action, target_kind, target_ref, target_path, id",
                (plan_id,),
            )
        ]

    def upsert_reset_outcome(self, record: ResetOutcomeRecord) -> None:
        if record.status not in RESET_OUTCOME_STATUSES:
            raise ValueError(f"Unsupported reset outcome status: {record.status}")
        self.connection.execute(
            """
            INSERT OR REPLACE INTO topic_reset_outcomes
                (
                    id, checkpoint_id, plan_id, research_topic_id, topic_workspace_id,
                    status, payload_json, payload_digest, applied_actions_json,
                    skipped_actions_json, failed_actions_json, diagnostics_json,
                    actor_ref, started_at, finished_at, rendered_markdown_path,
                    rendered_markdown_digest, provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.id,
                record.checkpoint_id,
                record.plan_id,
                record.research_topic_id,
                record.topic_workspace_id,
                record.status,
                _dumps(record.payload_json),
                record.payload_digest,
                _dumps(record.applied_actions),
                _dumps(record.skipped_actions),
                _dumps(record.failed_actions),
                _dumps(record.diagnostics),
                record.actor_ref,
                record.started_at,
                record.finished_at,
                record.rendered_markdown_path,
                record.rendered_markdown_digest,
                _dumps(record.provenance_refs),
            ),
        )

    def get_reset_outcome(self, outcome_id: str) -> ResetOutcomeRecord | None:
        if not _table_exists(self.connection, "topic_reset_outcomes"):
            return None
        row = self.connection.execute(
            "SELECT * FROM topic_reset_outcomes WHERE id = ?",
            (outcome_id,),
        ).fetchone()
        return _row_to_reset_outcome(row) if row is not None else None

    def list_reset_outcomes(
        self,
        *,
        topic_workspace_id: str | None = None,
        plan_id: str | None = None,
    ) -> list[ResetOutcomeRecord]:
        if not _table_exists(self.connection, "topic_reset_outcomes"):
            return []
        query = "SELECT * FROM topic_reset_outcomes"
        clauses: list[str] = []
        params: list[object] = []
        if topic_workspace_id is not None:
            clauses.append("topic_workspace_id = ?")
            params.append(topic_workspace_id)
        if plan_id is not None:
            clauses.append("plan_id = ?")
            params.append(plan_id)
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY finished_at DESC, id"
        return [_row_to_reset_outcome(row) for row in self.connection.execute(query, params)]

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
        env: Mapping[str, str],
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
        if profile.raw.get("preview") is True:
            diagnostics.append(
                Diagnostic(
                    code="ISO097",
                    severity="error",
                    concept="Topic Agent Team Profile",
                    field="profile_materialization",
                    message="Agent Team Instance creation cannot use preview-only Topic Agent Team Profile material.",
                )
            )
            return None, diagnostics
        if profile.profile_bundle_ref is not None and (profile.instantiation_packet_ref is None or profile.approval_ref is None):
            diagnostics.append(
                Diagnostic(
                    code="ISO095",
                    severity="error",
                    concept="Topic Agent Team Profile provenance",
                    field="profile_bundle_ref",
                    message="Agent Team Instance creation from a profile bundle requires packet and approval provenance.",
                )
            )
            return None, diagnostics
        if profile.profile_bundle_ref is not None:
            existing_active = [
                record
                for record in self.list_agent_team_instances()
                if record.research_topic_id == context.research_topic.id
                and record.status in {"planned", "ready", "running", "blocked"}
            ]
            if existing_active:
                diagnostics.append(
                    Diagnostic(
                        code="ISO094",
                        severity="error",
                        concept="Agent Team Instance",
                        field="research_topic_id",
                        message="This Research Topic already has an active topic-team lineage; topic-level parallelism requires another Research Topic.",
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
        generated_ids = [
            (binding, runtime_records._agent_instance_id(context.topic_workspace_id, team_id, binding.role_id))
            for binding in active_bindings
        ]
        diagnostics.extend(
            self._agent_instance_id_conflict_diagnostics(
                context,
                [(binding.role_id, agent_id) for binding, agent_id in generated_ids],
            )
        )
        workspace_plans = {}
        semantic_agent_paths: dict[str, dict[str, SemanticPathResult]] = {}
        semantic_agent_tmp_paths: dict[str, SemanticPathResult] = {}
        for binding in active_bindings:
            plan, plan_diagnostics = resolve_role_binding_agent_workspace_plan(
                project=context.project,
                research_topic_id=context.research_topic.id,
                topic_workspace_id=context.topic_workspace_id,
                topic_workspace_path=context.topic_workspace_path,
                binding=binding,
                source_path=profile.source_path,
                field_prefix=f"role_bindings.{binding.role_id}",
                concept="Agent Workspace path plan",
            )
            diagnostics.extend(plan_diagnostics)
            if plan is not None:
                workspace_plans[binding.role_id] = plan
                label_results: dict[str, SemanticPathResult] = {}
                for label in AGENT_TEAM_INSTANCE_PATH_LABELS:
                    result, result_diagnostics = resolve_semantic_path(
                        context,
                        label,
                        env=env,
                        cwd=context.topic_workspace_path,
                        agent_name=plan.agent_name,
                        use_path_plan=False,
                    )
                    diagnostics.extend(result_diagnostics)
                    if result is not None:
                        label_results[label] = result
                agent_context = EffectiveAgentContext(
                    agent_name=plan.agent_name,
                    agent_workspace_path=label_results["agent.workspace"].path,
                    source="topic-team-instantiation-packet",
                )
                tmp_result, tmp_diagnostics = resolve_semantic_binding(
                    context,
                    "agent.tmp",
                    env=env,
                    agent_context=agent_context,
                )
                diagnostics.extend(tmp_diagnostics)
                if tmp_result is not None:
                    semantic_agent_tmp_paths[binding.role_id] = tmp_result
                semantic_agent_paths[binding.role_id] = label_results
        if has_errors(diagnostics):
            return None, diagnostics

        try:
            with self.connection:
                for binding, agent_id in generated_ids:
                    workspace_id = f"agent-workspace-{agent_id}"
                    plan = workspace_plans[binding.role_id]
                    resolved_paths = semantic_agent_paths[binding.role_id]
                    workspace_result = resolved_paths["agent.workspace"]
                    isomer_managed_result = resolved_paths["agent.isomer_managed"]
                    surface = f"agent_workspace:{plan.agent_name}"
                    workspace_path = workspace_result.path
                    path_source = plan.source
                    if plan.source == "compat.agent_workspace_ref":
                        path_source = (
                            "topic_team_instantiation_packet.agent_workspace_ref"
                            if profile.instantiation_packet_ref is not None
                            else "topic_agent_team_profile.agent_workspace_ref"
                        )
                    elif profile.instantiation_packet_ref is not None:
                        path_source = "topic_team_instantiation_packet.agent_name"
                    workspace_path_plan = self.record_path_plan(
                        topic_workspace_id=context.topic_workspace_id,
                        surface=surface,
                        path=workspace_path,
                        source=path_source,
                        source_detail=_agent_path_plan_source_detail(plan, workspace_result),
                        semantic_label="agent.workspace",
                        scope_ref=f"agent_name:{plan.agent_name}",
                        compatibility_surface=surface,
                        storage_profile=workspace_result.catalog.storage_profile,
                        storage_profile_traits=_storage_profile_traits_for_result(workspace_result),
                        created_at=now,
                    )
                    isomer_managed_path = isomer_managed_result.path
                    isomer_managed_path_plan = self.record_path_plan(
                        topic_workspace_id=context.topic_workspace_id,
                        surface=f"agent_isomer_managed:{plan.agent_name}",
                        path=isomer_managed_path,
                        source=path_source,
                        source_detail=_agent_path_plan_source_detail(plan, isomer_managed_result),
                        semantic_label="agent.isomer_managed",
                        scope_ref=f"agent_name:{plan.agent_name}",
                        compatibility_surface=f"agent_isomer_managed:{plan.agent_name}",
                        storage_profile=isomer_managed_result.catalog.storage_profile,
                        storage_profile_traits=_storage_profile_traits_for_result(isomer_managed_result),
                        created_at=now,
                    )
                    support_path_plans = [
                        self.record_path_plan(
                            topic_workspace_id=context.topic_workspace_id,
                            surface=compatibility_surface_for_label(label, agent_name=plan.agent_name) or label,
                            path=result.path,
                            source=path_source,
                            source_detail=_agent_path_plan_source_detail(plan, result),
                            semantic_label=label,
                            scope_ref=f"agent_name:{plan.agent_name}",
                            compatibility_surface=compatibility_surface_for_label(label, agent_name=plan.agent_name),
                            storage_profile=result.catalog.storage_profile,
                            storage_profile_traits=_storage_profile_traits_for_result(result),
                            created_at=now,
                        )
                        for label, result in resolved_paths.items()
                        if label not in {"agent.workspace", "agent.isomer_managed"}
                    ]
                    workspace_path.mkdir(parents=True, exist_ok=True)
                    for result in resolved_paths.values():
                        result.path.mkdir(parents=True, exist_ok=True)
                    tmp_result = semantic_agent_tmp_paths.get(binding.role_id)
                    if tmp_result is not None:
                        diagnostics.extend(
                            _prepare_agent_local_tmp_surface(
                                context,
                                env=env,
                                agent_name=plan.agent_name,
                                agent_workspace_path=workspace_path,
                                tmp_path=tmp_result.path,
                            )
                        )
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
                        path_plan_id=workspace_path_plan.id,
                        agent_name=plan.agent_name,
                        expected_repo_ref="topic_main_repo",
                        expected_branch_namespace=f"per-agent/{plan.agent_name}/",
                        current_branch=plan.branch,
                        isomer_managed_path_plan_id=isomer_managed_path_plan.id,
                        support_root_path=str(isomer_managed_path),
                        boundary_refs=[f"{workspace_id}:workspace-boundary"],
                        generated_link_summary={"links_root": str(resolved_paths["agent.links"].path), "links": []},
                        status="ready",
                        created_at=now,
                        updated_at=now,
                        provenance_refs=[_provenance_ref("agent-workspace", workspace_id)],
                    )
                    self._insert_agent_instance(agent_record)
                    self._insert_agent_workspace(workspace_record)
                    agent_instances.append(agent_record)
                    agent_workspaces.append(workspace_record)
                    path_plans.extend([workspace_path_plan, isomer_managed_path_plan, *support_path_plans])
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
                    topic_agent_team_profile_bundle_ref=profile.profile_bundle_ref,
                    instantiation_packet_ref=profile.instantiation_packet_ref,
                    approval_ref=profile.approval_ref,
                    project_operator_ref=profile.project_operator_ref,
                    topic_service_agent_refs=list(profile.topic_service_agent_refs),
                    validation_refs=list(profile.validation_refs),
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
        path_plan_ids = [
            path_plan_id
            for workspace in agent_workspaces
            for path_plan_id in (workspace.path_plan_id, workspace.isomer_managed_path_plan_id)
            if path_plan_id is not None
        ]
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

    def _agent_instance_id_conflict_diagnostics(
        self,
        context: EffectiveTopicContext,
        generated_ids: list[tuple[str, str]],
    ) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []
        by_id: dict[str, list[str]] = {}
        for role_id, agent_id in generated_ids:
            by_id.setdefault(agent_id, []).append(role_id)
        for agent_id, role_ids in by_id.items():
            if len(role_ids) > 1:
                diagnostics.append(
                    Diagnostic(
                        code="ISO041",
                        severity="error",
                        concept="Agent Instance Identity",
                        field=agent_id,
                        message=(
                            f"Generated Agent Instance id {agent_id} is assigned to multiple "
                            f"roles in the same creation request: {', '.join(role_ids)}."
                        ),
                    )
                )

        existing_locations, scan_issues = project_agent_instance_id_locations(context.project)
        for db_path, message in scan_issues:
            diagnostics.append(
                Diagnostic(
                    code="ISO040",
                    severity="error",
                    concept="Agent Instance Identity",
                    path=db_path,
                    message=f"Could not read Agent Instance ids for creation-time duplicate scan: {message}.",
                )
            )

        for _, agent_id in generated_ids:
            locations = existing_locations.get(agent_id, [])
            if locations:
                records = ", ".join(location.record_ref() for location in locations)
                diagnostics.append(
                    Diagnostic(
                        code="ISO041",
                        severity="error",
                        concept="Agent Instance Identity",
                        path=self.db_path,
                        field=agent_id,
                        message=(
                            f"Generated Agent Instance id {agent_id} already exists in the Project: "
                            f"{records}."
                        ),
                    )
                )
        return diagnostics

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
                    handoff_ids_json, provenance_refs_json,
                    topic_agent_team_profile_bundle_ref, instantiation_packet_ref,
                    approval_ref, project_operator_ref, topic_service_agent_refs_json,
                    validation_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                record.topic_agent_team_profile_bundle_ref,
                record.instantiation_packet_ref,
                record.approval_ref,
                record.project_operator_ref,
                _dumps(record.topic_service_agent_refs),
                _dumps(record.validation_refs),
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
                    id, agent_instance_id, topic_workspace_id, path_plan_id, agent_name,
                    expected_repo_ref, expected_branch_namespace, current_branch,
                    isomer_managed_path_plan_id, support_root_path, boundary_refs_json,
                    generated_link_summary_json, status, created_at, updated_at, provenance_refs_json
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.id,
                record.agent_instance_id,
                record.topic_workspace_id,
                record.path_plan_id,
                record.agent_name,
                record.expected_repo_ref,
                record.expected_branch_namespace,
                record.current_branch,
                record.isomer_managed_path_plan_id,
                record.support_root_path,
                _dumps(record.boundary_refs),
                _dumps(record.generated_link_summary),
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
        tmp_directories, tmp_diagnostics = _prepare_runtime_local_tmp_surfaces(context, env=env)
        directories.extend(tmp_directories)
        diagnostics.extend(tmp_diagnostics)
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
    tmp_directories, tmp_diagnostics = _prepare_runtime_local_tmp_surfaces(context, env=env)
    directories.extend(tmp_directories)
    diagnostics.extend(tmp_diagnostics)
    if has_errors(diagnostics):
        return None, diagnostics
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
                    semantic_label=entry.semantic_label,
                    scope_ref=entry.scope_ref,
                    compatibility_surface=entry.compatibility_surface,
                    storage_profile=entry.storage_profile,
                    storage_profile_traits=entry.storage_profile_traits,
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
    resolved_standalone_binding = topic_payload.get("resolved_standalone_pixi_binding") if topic_payload is not None else None
    resolved_standalone_manifest_ref = (
        resolved_standalone_binding.get("resolved_manifest_path")
        if isinstance(resolved_standalone_binding, dict)
        and isinstance(resolved_standalone_binding.get("resolved_manifest_path"), str)
        else None
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
        standalone_pixi_manifest_refs=(
            [resolved_standalone_manifest_ref]
            if resolved_standalone_manifest_ref is not None
            else [binding.manifest_path_or_dir_input for binding in standalone_bindings]
        ),
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
