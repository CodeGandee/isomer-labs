"""Workspace Runtime records and constants."""

from __future__ import annotations

import re
import uuid

from dataclasses import dataclass, field
from datetime import UTC, datetime


ADAPTER_HANDOFF_DISPATCH_STATUSES = ("sent", "failed", "blocked")
SIGNAL_OBSERVATION_STATUSES = ("observed", "candidate_completion", "failed", "stale")
HANDOFF_NORMALIZATION_STATUSES = ("accepted", "rejected", "blocked", "superseded", "repair_routed", "follow_up")


@dataclass(frozen=True)
class AdapterHandoffDispatchRecord:
    id: str
    research_topic_id: str
    topic_workspace_id: str
    handoff_id: str
    agent_team_instance_id: str
    source_agent_instance_id: str
    target_agent_instance_id: str
    adapter_id: str
    status: str
    command_run_ids: list[str]
    payload_ref_ids: list[str]
    diagnostics: list[dict[str, object]]
    created_at: str
    updated_at: str
    research_task_id: str | None = None
    run_id: str | None = None
    actor_ref: str | None = None
    expected_output_refs: list[str] = field(default_factory=list)
    completion_watcher_contract_refs: list[str] = field(default_factory=list)
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "handoff_id": self.handoff_id,
            "agent_team_instance_id": self.agent_team_instance_id,
            "source_agent_instance_id": self.source_agent_instance_id,
            "target_agent_instance_id": self.target_agent_instance_id,
            "adapter_id": self.adapter_id,
            "status": self.status,
            "command_run_ids": self.command_run_ids,
            "payload_ref_ids": self.payload_ref_ids,
            "diagnostics": self.diagnostics,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "expected_output_refs": self.expected_output_refs,
            "completion_watcher_contract_refs": self.completion_watcher_contract_refs,
            "provenance_refs": self.provenance_refs,
        }
        for key, value in (
            ("research_task_id", self.research_task_id),
            ("run_id", self.run_id),
            ("actor_ref", self.actor_ref),
        ):
            if value is not None:
                data[key] = value
        return data


@dataclass(frozen=True)
class SignalObservationRecord:
    id: str
    research_topic_id: str
    topic_workspace_id: str
    handoff_id: str
    agent_team_instance_id: str
    adapter_id: str
    observation_kind: str
    status: str
    summary: str
    command_run_ids: list[str]
    payload_ref_ids: list[str]
    diagnostics: list[dict[str, object]]
    observed_at: str
    run_id: str | None = None
    source_agent_instance_id: str | None = None
    target_agent_instance_id: str | None = None
    actor_ref: str | None = None
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "handoff_id": self.handoff_id,
            "agent_team_instance_id": self.agent_team_instance_id,
            "adapter_id": self.adapter_id,
            "observation_kind": self.observation_kind,
            "status": self.status,
            "summary": self.summary,
            "command_run_ids": self.command_run_ids,
            "payload_ref_ids": self.payload_ref_ids,
            "diagnostics": self.diagnostics,
            "observed_at": self.observed_at,
            "provenance_refs": self.provenance_refs,
        }
        for key, value in (
            ("run_id", self.run_id),
            ("source_agent_instance_id", self.source_agent_instance_id),
            ("target_agent_instance_id", self.target_agent_instance_id),
            ("actor_ref", self.actor_ref),
        ):
            if value is not None:
                data[key] = value
        return data


@dataclass(frozen=True)
class HandoffNormalizationRecord:
    id: str
    research_topic_id: str
    topic_workspace_id: str
    handoff_id: str
    status: str
    rationale: str
    signal_observation_ids: list[str]
    output_artifact_refs: list[str]
    corrective_refs: list[str]
    payload_ref_ids: list[str]
    created_at: str
    run_id: str | None = None
    actor_ref: str | None = None
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "handoff_id": self.handoff_id,
            "status": self.status,
            "rationale": self.rationale,
            "signal_observation_ids": self.signal_observation_ids,
            "output_artifact_refs": self.output_artifact_refs,
            "corrective_refs": self.corrective_refs,
            "payload_ref_ids": self.payload_ref_ids,
            "created_at": self.created_at,
            "provenance_refs": self.provenance_refs,
        }
        for key, value in (("run_id", self.run_id), ("actor_ref", self.actor_ref)):
            if value is not None:
                data[key] = value
        return data


WORKSPACE_RUNTIME_SCHEMA_VERSION = "isomer-workspace-runtime.v1"
RUNTIME_DIRECTORIES = (
    "repos",
    "topic_main_repo",
    "topic_main_isomer_managed",
    "agents",
    "actors",
    "records",
    "records_artifacts",
    "records_tasks",
    "records_runs",
    "records_views",
    "records_logs",
    "runtime",
)
RUNTIME_PATH_SURFACES = ("workspace_runtime_db", *RUNTIME_DIRECTORIES)

READINESS_STATUSES = ("ready", "failed", "blocked", "stale", "superseded")
LIFECYCLE_RECORD_KINDS = (
    "research_topic",
    "research_inquiry",
    "research_task",
    "run",
    "workflow_stage_cursor",
    "topic_workspace",
    "topic_agent_team_profile",
    "artifact",
    "gate",
    "finding",
    "research_claim",
    "evidence_item",
    "decision_record",
    "view_manifest",
    "provenance_record",
)
LIFECYCLE_STATUSES = (
    "planned",
    "active",
    "ready",
    "running",
    "blocked",
    "complete",
    "failed",
    "stale",
    "stopped",
    "cancelled",
    "superseded",
    "archived",
    "open",
    "resolved",
    "candidate",
    "supported",
)
STRUCTURED_PAYLOAD_VALIDATION_STATUSES = ("valid", "invalid", "error")
STRUCTURED_PAYLOAD_RENDER_STATUSES = ("rendered", "not_requested", "error")
ARTIFACT_FORMAT_REGISTRATION_SOURCE_KINDS = ("runtime_registration", "file_snapshot")
RESEARCH_RECORD_LINEAGE_KINDS = (
    "derived_from",
    "revision_of",
    "selected_from",
    "merged_from",
    "follow_up_to",
)
RESEARCH_RECORD_LINEAGE_STATUSES = ("ready", "stale", "archived")
RESET_CHECKPOINT_STATUSES = ("ready", "blocked", "stale")
RESET_PLAN_STATUSES = ("ready", "blocked", "stale", "applied", "failed")
RESET_PLAN_ACTIONS = (
    "preserve",
    "delete_record",
    "delete_file",
    "delete_generated_view",
    "regenerate",
    "skip",
    "blocked",
)
RESET_PLAN_ACTION_STATUSES = ("planned", "applied", "skipped", "failed")
RESET_OUTCOME_STATUSES = ("succeeded", "partial", "failed")
AGENT_TEAM_INSTANCE_STATUSES = ("planned", "ready", "running", "blocked", "failed", "stale", "stopped", "cancelled", "superseded", "archived")
AGENT_INSTANCE_STATUSES = (
    "planned",
    "active",
    "paused",
    "blocked",
    "completed",
    "stopped",
    "failed",
    "archived",
    "ready",
    "running",
    "stale",
)
AGENT_WORKSPACE_STATUSES = ("planned", "ready", "active", "missing", "stale", "archived", "invalid")
HANDOFF_STATUSES = (
    "draft",
    "sent",
    "observing",
    "candidate",
    "accepted",
    "complete",
    "rejected",
    "blocked",
    "failed",
    "repair",
    "follow_up",
    "stale",
    "cancelled",
    "superseded",
    "archived",
)
ADAPTER_MANIFEST_KINDS = ("adapter_link", "launch_material", "adapter_runtime")
ADAPTER_RECONCILIATION_STATES = (
    "linked",
    "launched_by_isomer",
    "external_detected",
    "adopted",
    "drifted",
    "conflicted",
    "stale",
    "rejected",
)
ADAPTER_COMMAND_RUN_STATUSES = ("succeeded", "failed", "timed_out", "invalid_json")
ADAPTER_MATERIALIZATION_STATUSES = ("prepared", "failed")
ADAPTER_LAUNCH_ATTEMPT_STATUSES = ("prepared", "running", "launched", "partial", "failed")
ADAPTER_INSPECTION_STATUSES = ("observed", "failed", "stale")
ADAPTER_STOP_OUTCOME_STATUSES = ("stopped", "failed", "partial", "stale")


def utc_timestamp() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _path_plan_id(topic_workspace_id: str, surface: str) -> str:
    return f"path-plan-{_slug(topic_workspace_id)}-{_slug(surface)}"


def _provenance_ref(record_kind: str, record_id: str) -> str:
    return f"provenance:{record_kind}:{record_id}"


def _slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "-", value).strip("-") or "record"


def _agent_instance_id(topic_workspace_id: str, team_id: str, role_id: str) -> str:
    """Return a globally unique Agent Instance id.

    The id embeds the owning Topic Workspace, Agent Team Instance, and Agent
    Role for readability, and appends a short random suffix so that ids are
    unique across the whole Project.
    """
    short_uuid = uuid.uuid4().hex[:8]
    return f"agent-{_slug(topic_workspace_id)}-{_slug(team_id)}-{_slug(role_id)}-{short_uuid}"


@dataclass(frozen=True)
class ProvenanceRef:
    id: str
    source: str
    created_at: str

    def to_json(self) -> dict[str, object]:
        return {
            "id": self.id,
            "source": self.source,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class WorkspaceRuntimeMetadata:
    schema_version: str
    project_root: str
    project_manifest_path: str
    research_topic_id: str
    topic_workspace_id: str
    topic_workspace_path: str
    created_at: str
    updated_at: str
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "project_root": self.project_root,
            "project_manifest_path": self.project_manifest_path,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "topic_workspace_path": self.topic_workspace_path,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "provenance_refs": self.provenance_refs,
        }


@dataclass(frozen=True)
class PathPlanRecord:
    id: str
    topic_workspace_id: str
    surface: str
    path: str
    source: str
    source_detail: str | None
    created_at: str
    semantic_label: str | None = None
    scope_ref: str | None = None
    compatibility_surface: str | None = None
    storage_profile: str | None = None
    storage_profile_traits: dict[str, object] = field(default_factory=dict)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "topic_workspace_id": self.topic_workspace_id,
            "surface": self.surface,
            "path": self.path,
            "source": self.source,
            "created_at": self.created_at,
        }
        if self.source_detail is not None:
            data["source_detail"] = self.source_detail
        if self.semantic_label is not None:
            data["semantic_label"] = self.semantic_label
        if self.scope_ref is not None:
            data["scope_ref"] = self.scope_ref
        if self.compatibility_surface is not None:
            data["compatibility_surface"] = self.compatibility_surface
        if self.storage_profile is not None:
            data["storage_profile"] = self.storage_profile
        if self.storage_profile_traits:
            data["storage_profile_traits"] = self.storage_profile_traits
        return data


@dataclass(frozen=True)
class RuntimeLifecycleRecord:
    id: str
    record_kind: str
    research_topic_id: str
    topic_workspace_id: str
    status: str
    created_at: str
    updated_at: str
    lifecycle_refs: dict[str, str] = field(default_factory=dict)
    transition_metadata: dict[str, object] = field(default_factory=dict)
    content_path: str | None = None
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "record_kind": self.record_kind,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "lifecycle_refs": self.lifecycle_refs,
            "transition_metadata": self.transition_metadata,
            "provenance_refs": self.provenance_refs,
        }
        if self.content_path is not None:
            data["content_path"] = self.content_path
        return data


@dataclass(frozen=True)
class ResearchRecordGenerationGroup:
    id: str
    research_topic_id: str
    topic_workspace_id: str
    purpose: str | None
    parent_set_digest: str
    producer_skill: str | None
    decision_record_id: str | None
    metadata: dict[str, object]
    created_at: str
    updated_at: str
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "parent_set_digest": self.parent_set_digest,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "provenance_refs": self.provenance_refs,
        }
        for key, value in (
            ("purpose", self.purpose),
            ("producer_skill", self.producer_skill),
            ("decision_record_id", self.decision_record_id),
        ):
            if value is not None:
                data[key] = value
        return data


@dataclass(frozen=True)
class ResearchRecordLineageEdge:
    id: str
    research_topic_id: str
    topic_workspace_id: str
    parent_record_id: str
    child_record_id: str
    lineage_kind: str
    parent_role: str | None
    generation_id: str | None
    decision_record_id: str | None
    rationale: str | None
    status: str
    metadata: dict[str, object]
    created_at: str
    updated_at: str
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "parent_record_id": self.parent_record_id,
            "child_record_id": self.child_record_id,
            "lineage_kind": self.lineage_kind,
            "status": self.status,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "provenance_refs": self.provenance_refs,
        }
        for key, value in (
            ("parent_role", self.parent_role),
            ("generation_id", self.generation_id),
            ("decision_record_id", self.decision_record_id),
            ("rationale", self.rationale),
        ):
            if value is not None:
                data[key] = value
        return data


@dataclass(frozen=True)
class ArtifactFormatRegistrationRecord:
    id: str
    research_topic_id: str
    topic_workspace_id: str
    format_profile_ref: str
    schema_ref: str
    template_ref: str | None
    output_format: str
    source_kind: str
    profile_json: dict[str, object]
    schema_snapshot_path: str | None
    template_snapshot_path: str | None
    original_schema_path: str | None
    original_template_path: str | None
    profile_digest: str
    schema_digest: str
    template_digest: str | None
    diagnostics: list[dict[str, object]]
    actor_ref: str | None
    created_at: str
    updated_at: str
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "format_profile_ref": self.format_profile_ref,
            "schema_ref": self.schema_ref,
            "output_format": self.output_format,
            "source_kind": self.source_kind,
            "profile": self.profile_json,
            "profile_digest": self.profile_digest,
            "schema_digest": self.schema_digest,
            "diagnostics": self.diagnostics,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "provenance_refs": self.provenance_refs,
        }
        for key, value in (
            ("template_ref", self.template_ref),
            ("schema_snapshot_path", self.schema_snapshot_path),
            ("template_snapshot_path", self.template_snapshot_path),
            ("original_schema_path", self.original_schema_path),
            ("original_template_path", self.original_template_path),
            ("template_digest", self.template_digest),
            ("actor_ref", self.actor_ref),
        ):
            if value is not None:
                data[key] = value
        return data


@dataclass(frozen=True)
class StructuredResearchPayloadRecord:
    id: str
    record_id: str
    research_topic_id: str
    topic_workspace_id: str
    format_profile_ref: str | None
    schema_ref: str
    schema_version: str | None
    schema_source_kind: str
    template_ref: str | None
    template_source_kind: str | None
    payload_json: dict[str, object]
    payload_digest: str
    payload_file_path: str | None
    payload_media_type: str
    payload_manifest_path: str | None
    payload_source_path: str | None
    revision_of_record_id: str | None
    supersedes_record_id: str | None
    latest_for_semantic_id: str | None
    legacy_rendered_markdown_path: str | None
    legacy_rendered_markdown_digest: str | None
    validation_status: str
    validation_diagnostics: list[dict[str, object]]
    render_status: str
    render_diagnostics: list[dict[str, object]]
    rendered_markdown_path: str | None
    rendered_markdown_digest: str | None
    created_at: str
    updated_at: str
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self, *, include_payload: bool = True, include_diagnostics: bool = True) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "record_id": self.record_id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "schema_ref": self.schema_ref,
            "schema_source_kind": self.schema_source_kind,
            "payload_digest": self.payload_digest,
            "payload_media_type": self.payload_media_type,
            "validation_status": self.validation_status,
            "render_status": self.render_status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "provenance_refs": self.provenance_refs,
        }
        for key, value in (
            ("format_profile_ref", self.format_profile_ref),
            ("schema_version", self.schema_version),
            ("template_ref", self.template_ref),
            ("template_source_kind", self.template_source_kind),
            ("payload_file_path", self.payload_file_path),
            ("payload_manifest_path", self.payload_manifest_path),
            ("payload_source_path", self.payload_source_path),
            ("revision_of_record_id", self.revision_of_record_id),
            ("supersedes_record_id", self.supersedes_record_id),
            ("latest_for_semantic_id", self.latest_for_semantic_id),
            ("legacy_rendered_markdown_path", self.legacy_rendered_markdown_path),
            ("legacy_rendered_markdown_digest", self.legacy_rendered_markdown_digest),
            ("rendered_markdown_path", self.rendered_markdown_path),
            ("rendered_markdown_digest", self.rendered_markdown_digest),
        ):
            if value is not None:
                data[key] = value
        if include_payload:
            data["payload"] = self.payload_json
        if include_diagnostics:
            data["validation_diagnostics"] = self.validation_diagnostics
            data["render_diagnostics"] = self.render_diagnostics
        return data

    def to_summary_json(self) -> dict[str, object]:
        return self.to_json(include_payload=False, include_diagnostics=False)


@dataclass(frozen=True)
class ResetCheckpointRecord:
    id: str
    research_topic_id: str
    topic_workspace_id: str
    status: str
    payload_json: dict[str, object]
    payload_digest: str
    checkpoint_digest: str
    created_at: str
    updated_at: str
    actor_ref: str | None = None
    source_record_id: str | None = None
    rendered_markdown_path: str | None = None
    rendered_markdown_digest: str | None = None
    diagnostics: list[dict[str, object]] = field(default_factory=list)
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self, *, include_payload: bool = True, include_diagnostics: bool = True) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "status": self.status,
            "payload_digest": self.payload_digest,
            "checkpoint_digest": self.checkpoint_digest,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "provenance_refs": self.provenance_refs,
        }
        for key, value in (
            ("actor_ref", self.actor_ref),
            ("source_record_id", self.source_record_id),
            ("rendered_markdown_path", self.rendered_markdown_path),
            ("rendered_markdown_digest", self.rendered_markdown_digest),
        ):
            if value is not None:
                data[key] = value
        if include_payload:
            data["payload"] = self.payload_json
        if include_diagnostics:
            data["diagnostics"] = self.diagnostics
        return data

    def to_summary_json(self) -> dict[str, object]:
        return self.to_json(include_payload=False, include_diagnostics=False)


@dataclass(frozen=True)
class ResetPlanRecord:
    id: str
    checkpoint_id: str
    research_topic_id: str
    topic_workspace_id: str
    status: str
    payload_json: dict[str, object]
    payload_digest: str
    checkpoint_digest: str
    precondition_digest: str
    created_at: str
    updated_at: str
    actor_ref: str | None = None
    rendered_markdown_path: str | None = None
    rendered_markdown_digest: str | None = None
    diagnostics: list[dict[str, object]] = field(default_factory=list)
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self, *, include_payload: bool = True, include_diagnostics: bool = True) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "checkpoint_id": self.checkpoint_id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "status": self.status,
            "payload_digest": self.payload_digest,
            "checkpoint_digest": self.checkpoint_digest,
            "precondition_digest": self.precondition_digest,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "provenance_refs": self.provenance_refs,
        }
        for key, value in (
            ("actor_ref", self.actor_ref),
            ("rendered_markdown_path", self.rendered_markdown_path),
            ("rendered_markdown_digest", self.rendered_markdown_digest),
        ):
            if value is not None:
                data[key] = value
        if include_payload:
            data["payload"] = self.payload_json
        if include_diagnostics:
            data["diagnostics"] = self.diagnostics
        return data

    def to_summary_json(self) -> dict[str, object]:
        return self.to_json(include_payload=False, include_diagnostics=False)


@dataclass(frozen=True)
class ResetPlanActionRecord:
    id: str
    plan_id: str
    action: str
    target_kind: str
    status: str
    created_at: str
    target_ref: str | None = None
    target_path: str | None = None
    semantic_label: str | None = None
    source_kind: str | None = None
    details: dict[str, object] = field(default_factory=dict)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "plan_id": self.plan_id,
            "action": self.action,
            "target_kind": self.target_kind,
            "status": self.status,
            "created_at": self.created_at,
            "details": self.details,
        }
        for key, value in (
            ("target_ref", self.target_ref),
            ("target_path", self.target_path),
            ("semantic_label", self.semantic_label),
            ("source_kind", self.source_kind),
        ):
            if value is not None:
                data[key] = value
        return data


@dataclass(frozen=True)
class ResetOutcomeRecord:
    id: str
    checkpoint_id: str
    plan_id: str
    research_topic_id: str
    topic_workspace_id: str
    status: str
    payload_json: dict[str, object]
    payload_digest: str
    applied_actions: list[dict[str, object]]
    skipped_actions: list[dict[str, object]]
    failed_actions: list[dict[str, object]]
    diagnostics: list[dict[str, object]]
    actor_ref: str | None
    started_at: str
    finished_at: str
    rendered_markdown_path: str | None = None
    rendered_markdown_digest: str | None = None
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self, *, include_payload: bool = True, include_diagnostics: bool = True) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "checkpoint_id": self.checkpoint_id,
            "plan_id": self.plan_id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "status": self.status,
            "payload_digest": self.payload_digest,
            "applied_actions": self.applied_actions,
            "skipped_actions": self.skipped_actions,
            "failed_actions": self.failed_actions,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "provenance_refs": self.provenance_refs,
        }
        for key, value in (
            ("actor_ref", self.actor_ref),
            ("rendered_markdown_path", self.rendered_markdown_path),
            ("rendered_markdown_digest", self.rendered_markdown_digest),
        ):
            if value is not None:
                data[key] = value
        if include_payload:
            data["payload"] = self.payload_json
        if include_diagnostics:
            data["diagnostics"] = self.diagnostics
        return data

    def to_summary_json(self) -> dict[str, object]:
        return self.to_json(include_payload=False, include_diagnostics=False)


@dataclass(frozen=True)
class TopicEnvironmentReadinessRecord:
    id: str
    research_topic_id: str
    topic_workspace_id: str
    status: str
    project_pixi_environment_refs: list[str]
    standalone_pixi_manifest_refs: list[str]
    diagnostics: list[dict[str, object]]
    checked_at: str
    actor_ref: str | None = None
    repair_service_request_hint: str | None = None
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "status": self.status,
            "project_pixi_environment_refs": self.project_pixi_environment_refs,
            "standalone_pixi_manifest_refs": self.standalone_pixi_manifest_refs,
            "diagnostics": self.diagnostics,
            "checked_at": self.checked_at,
            "provenance_refs": self.provenance_refs,
        }
        if self.actor_ref is not None:
            data["actor_ref"] = self.actor_ref
        if self.repair_service_request_hint is not None:
            data["repair_service_request_hint"] = self.repair_service_request_hint
        return data


@dataclass(frozen=True)
class AgentTeamInstanceRecord:
    id: str
    research_topic_id: str
    topic_workspace_id: str
    topic_agent_team_profile_id: str
    domain_agent_team_template_id: str
    status: str
    created_at: str
    updated_at: str
    agent_instance_ids: list[str] = field(default_factory=list)
    agent_workspace_ids: list[str] = field(default_factory=list)
    run_ids: list[str] = field(default_factory=list)
    workflow_stage_cursor_ids: list[str] = field(default_factory=list)
    blocker_refs: list[str] = field(default_factory=list)
    handoff_ids: list[str] = field(default_factory=list)
    provenance_refs: list[str] = field(default_factory=list)
    topic_agent_team_profile_bundle_ref: str | None = None
    instantiation_packet_ref: str | None = None
    approval_ref: str | None = None
    project_operator_ref: str | None = None
    topic_service_agent_refs: list[str] = field(default_factory=list)
    validation_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        return {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "topic_agent_team_profile_id": self.topic_agent_team_profile_id,
            "domain_agent_team_template_id": self.domain_agent_team_template_id,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "agent_instance_ids": self.agent_instance_ids,
            "agent_workspace_ids": self.agent_workspace_ids,
            "run_ids": self.run_ids,
            "workflow_stage_cursor_ids": self.workflow_stage_cursor_ids,
            "blocker_refs": self.blocker_refs,
            "handoff_ids": self.handoff_ids,
            "provenance_refs": self.provenance_refs,
            "topic_agent_team_profile_bundle_ref": self.topic_agent_team_profile_bundle_ref,
            "instantiation_packet_ref": self.instantiation_packet_ref,
            "approval_ref": self.approval_ref,
            "project_operator_ref": self.project_operator_ref,
            "topic_service_agent_refs": self.topic_service_agent_refs,
            "validation_refs": self.validation_refs,
        }


@dataclass(frozen=True)
class AgentInstanceRecord:
    id: str
    agent_team_instance_id: str
    agent_role_id: str
    research_topic_id: str
    topic_workspace_id: str
    agent_profile_ref: str | None
    status: str
    created_at: str
    updated_at: str
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "agent_team_instance_id": self.agent_team_instance_id,
            "agent_role_id": self.agent_role_id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "provenance_refs": self.provenance_refs,
        }
        if self.agent_profile_ref is not None:
            data["agent_profile_ref"] = self.agent_profile_ref
        return data


@dataclass(frozen=True)
class AgentWorkspaceRecord:
    id: str
    agent_instance_id: str
    topic_workspace_id: str
    path_plan_id: str
    status: str
    created_at: str
    updated_at: str
    agent_name: str | None = None
    expected_repo_ref: str | None = None
    expected_branch_namespace: str | None = None
    current_branch: str | None = None
    isomer_managed_path_plan_id: str | None = None
    support_root_path: str | None = None
    boundary_refs: list[str] = field(default_factory=list)
    generated_link_summary: dict[str, object] = field(default_factory=dict)
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "agent_instance_id": self.agent_instance_id,
            "topic_workspace_id": self.topic_workspace_id,
            "path_plan_id": self.path_plan_id,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "provenance_refs": self.provenance_refs,
        }
        for key, value in (
            ("agent_name", self.agent_name),
            ("expected_repo_ref", self.expected_repo_ref),
            ("expected_branch_namespace", self.expected_branch_namespace),
            ("current_branch", self.current_branch),
            ("isomer_managed_path_plan_id", self.isomer_managed_path_plan_id),
            ("support_root_path", self.support_root_path),
        ):
            if value is not None:
                data[key] = value
        if self.boundary_refs:
            data["boundary_refs"] = self.boundary_refs
        if self.generated_link_summary:
            data["generated_link_summary"] = self.generated_link_summary
        return data


@dataclass(frozen=True)
class HandoffRecord:
    id: str
    research_topic_id: str
    topic_workspace_id: str
    source_actor_ref: str
    target_actor_ref: str
    status: str
    created_at: str
    updated_at: str
    research_task_id: str | None = None
    run_id: str | None = None
    agent_team_instance_id: str | None = None
    completion_watcher_contract_refs: list[str] = field(default_factory=list)
    expected_output_refs: list[str] = field(default_factory=list)
    stale_after: str | None = None
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "source_actor_ref": self.source_actor_ref,
            "target_actor_ref": self.target_actor_ref,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "completion_watcher_contract_refs": self.completion_watcher_contract_refs,
            "expected_output_refs": self.expected_output_refs,
            "provenance_refs": self.provenance_refs,
        }
        for key, value in (
            ("research_task_id", self.research_task_id),
            ("run_id", self.run_id),
            ("agent_team_instance_id", self.agent_team_instance_id),
            ("stale_after", self.stale_after),
        ):
            if value is not None:
                data[key] = value
        return data


@dataclass(frozen=True)
class ValidationIssueRecord:
    id: str
    research_topic_id: str
    topic_workspace_id: str
    severity: str
    code: str
    concept: str
    message: str
    created_at: str
    record_ref: str | None = None
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "severity": self.severity,
            "code": self.code,
            "concept": self.concept,
            "message": self.message,
            "created_at": self.created_at,
            "provenance_refs": self.provenance_refs,
        }
        if self.record_ref is not None:
            data["record_ref"] = self.record_ref
        return data


@dataclass(frozen=True)
class AdapterManifestRefRecord:
    id: str
    research_topic_id: str
    topic_workspace_id: str
    agent_team_instance_id: str
    adapter_id: str
    manifest_kind: str
    manifest_path: str
    manifest_digest: str
    source: str
    path_plan_id: str | None
    created_at: str
    updated_at: str
    agent_instance_ids: list[str] = field(default_factory=list)
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "agent_team_instance_id": self.agent_team_instance_id,
            "adapter_id": self.adapter_id,
            "manifest_kind": self.manifest_kind,
            "manifest_path": self.manifest_path,
            "manifest_digest": self.manifest_digest,
            "source": self.source,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "agent_instance_ids": self.agent_instance_ids,
            "provenance_refs": self.provenance_refs,
        }
        if self.path_plan_id is not None:
            data["path_plan_id"] = self.path_plan_id
        return data


@dataclass(frozen=True)
class AdapterReconciliationRecord:
    id: str
    research_topic_id: str
    topic_workspace_id: str
    agent_team_instance_id: str
    adapter_id: str
    state: str
    mapping_confidence: str
    manifest_refs: list[str]
    manifest_digest_summary: dict[str, object]
    live_observation_summary: dict[str, object]
    diagnostics: list[dict[str, object]]
    created_at: str
    actor_ref: str | None = None
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "agent_team_instance_id": self.agent_team_instance_id,
            "adapter_id": self.adapter_id,
            "state": self.state,
            "mapping_confidence": self.mapping_confidence,
            "manifest_refs": self.manifest_refs,
            "manifest_digest_summary": self.manifest_digest_summary,
            "live_observation_summary": self.live_observation_summary,
            "diagnostics": self.diagnostics,
            "created_at": self.created_at,
            "provenance_refs": self.provenance_refs,
        }
        if self.actor_ref is not None:
            data["actor_ref"] = self.actor_ref
        return data


@dataclass(frozen=True)
class AdapterPayloadRefRecord:
    id: str
    research_topic_id: str
    topic_workspace_id: str
    agent_team_instance_id: str
    adapter_id: str
    payload_kind: str
    payload_path: str
    payload_digest: str
    source: str
    created_at: str
    agent_instance_id: str | None = None
    command_run_id: str | None = None
    path_plan_id: str | None = None
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "agent_team_instance_id": self.agent_team_instance_id,
            "adapter_id": self.adapter_id,
            "payload_kind": self.payload_kind,
            "payload_path": self.payload_path,
            "payload_digest": self.payload_digest,
            "source": self.source,
            "created_at": self.created_at,
            "provenance_refs": self.provenance_refs,
        }
        for key, value in (
            ("agent_instance_id", self.agent_instance_id),
            ("command_run_id", self.command_run_id),
            ("path_plan_id", self.path_plan_id),
        ):
            if value is not None:
                data[key] = value
        return data


@dataclass(frozen=True)
class AdapterCommandRunRecord:
    id: str
    research_topic_id: str
    topic_workspace_id: str
    agent_team_instance_id: str
    adapter_id: str
    operation_kind: str
    argv: list[str]
    cwd: str | None
    env_hints: dict[str, str]
    status: str
    returncode: int | None
    started_at: str
    finished_at: str
    duration_seconds: float
    payload_ref_ids: list[str]
    diagnostics: list[dict[str, object]]
    agent_instance_id: str | None = None
    actor_ref: str | None = None
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "agent_team_instance_id": self.agent_team_instance_id,
            "adapter_id": self.adapter_id,
            "operation_kind": self.operation_kind,
            "argv": self.argv,
            "cwd": self.cwd,
            "env_hints": self.env_hints,
            "status": self.status,
            "returncode": self.returncode,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "duration_seconds": self.duration_seconds,
            "payload_ref_ids": self.payload_ref_ids,
            "diagnostics": self.diagnostics,
            "provenance_refs": self.provenance_refs,
        }
        if self.agent_instance_id is not None:
            data["agent_instance_id"] = self.agent_instance_id
        if self.actor_ref is not None:
            data["actor_ref"] = self.actor_ref
        return data


@dataclass(frozen=True)
class AdapterMaterializationRecord:
    id: str
    research_topic_id: str
    topic_workspace_id: str
    agent_team_instance_id: str
    adapter_id: str
    status: str
    material_ref_ids: list[str]
    manifest_ref_ids: list[str]
    path_plan_ids: list[str]
    diagnostics: list[dict[str, object]]
    created_at: str
    updated_at: str
    actor_ref: str | None = None
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "agent_team_instance_id": self.agent_team_instance_id,
            "adapter_id": self.adapter_id,
            "status": self.status,
            "material_ref_ids": self.material_ref_ids,
            "manifest_ref_ids": self.manifest_ref_ids,
            "path_plan_ids": self.path_plan_ids,
            "diagnostics": self.diagnostics,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "provenance_refs": self.provenance_refs,
        }
        if self.actor_ref is not None:
            data["actor_ref"] = self.actor_ref
        return data


@dataclass(frozen=True)
class AdapterLaunchAttemptRecord:
    id: str
    research_topic_id: str
    topic_workspace_id: str
    agent_team_instance_id: str
    adapter_id: str
    status: str
    agent_instance_ids: list[str]
    command_run_ids: list[str]
    manifest_ref_ids: list[str]
    payload_ref_ids: list[str]
    adapter_refs: list[dict[str, object]]
    diagnostics: list[dict[str, object]]
    started_at: str
    updated_at: str
    finished_at: str | None = None
    actor_ref: str | None = None
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "agent_team_instance_id": self.agent_team_instance_id,
            "adapter_id": self.adapter_id,
            "status": self.status,
            "agent_instance_ids": self.agent_instance_ids,
            "command_run_ids": self.command_run_ids,
            "manifest_ref_ids": self.manifest_ref_ids,
            "payload_ref_ids": self.payload_ref_ids,
            "adapter_refs": self.adapter_refs,
            "diagnostics": self.diagnostics,
            "started_at": self.started_at,
            "updated_at": self.updated_at,
            "provenance_refs": self.provenance_refs,
        }
        if self.finished_at is not None:
            data["finished_at"] = self.finished_at
        if self.actor_ref is not None:
            data["actor_ref"] = self.actor_ref
        return data


@dataclass(frozen=True)
class AdapterInspectionSnapshotRecord:
    id: str
    research_topic_id: str
    topic_workspace_id: str
    agent_team_instance_id: str
    adapter_id: str
    status: str
    command_run_ids: list[str]
    manifest_ref_ids: list[str]
    snapshot_payload_ref_id: str | None
    live_observation_summary: dict[str, object]
    diagnostics: list[dict[str, object]]
    inspected_at: str
    actor_ref: str | None = None
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "agent_team_instance_id": self.agent_team_instance_id,
            "adapter_id": self.adapter_id,
            "status": self.status,
            "command_run_ids": self.command_run_ids,
            "manifest_ref_ids": self.manifest_ref_ids,
            "snapshot_payload_ref_id": self.snapshot_payload_ref_id,
            "live_observation_summary": self.live_observation_summary,
            "diagnostics": self.diagnostics,
            "inspected_at": self.inspected_at,
            "provenance_refs": self.provenance_refs,
        }
        if self.actor_ref is not None:
            data["actor_ref"] = self.actor_ref
        return data


@dataclass(frozen=True)
class AdapterStopOutcomeRecord:
    id: str
    research_topic_id: str
    topic_workspace_id: str
    agent_team_instance_id: str
    adapter_id: str
    status: str
    target_agent_instance_ids: list[str]
    command_run_ids: list[str]
    payload_ref_ids: list[str]
    remaining_live_refs: list[dict[str, object]]
    diagnostics: list[dict[str, object]]
    stopped_at: str
    actor_ref: str | None = None
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "agent_team_instance_id": self.agent_team_instance_id,
            "adapter_id": self.adapter_id,
            "status": self.status,
            "target_agent_instance_ids": self.target_agent_instance_ids,
            "command_run_ids": self.command_run_ids,
            "payload_ref_ids": self.payload_ref_ids,
            "remaining_live_refs": self.remaining_live_refs,
            "diagnostics": self.diagnostics,
            "stopped_at": self.stopped_at,
            "provenance_refs": self.provenance_refs,
        }
        if self.actor_ref is not None:
            data["actor_ref"] = self.actor_ref
        return data
