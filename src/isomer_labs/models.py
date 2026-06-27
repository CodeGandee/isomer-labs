"""Typed Milestone 1 domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from isomer_labs.diagnostics import Diagnostic


OUTPUT_SCHEMA_VERSION = "isomer-cli-output.v1"
PROJECT_MANIFEST_SCHEMA_VERSION = "isomer-project-manifest.v1"
RESEARCH_TOPIC_CONFIG_SCHEMA_VERSION = "isomer-research-topic-config.v1"
LOCAL_ACTIVE_CONTEXT_SCHEMA_VERSION = "isomer-local-active-context.v1"
DOMAIN_AGENT_TEAM_TEMPLATE_REF_SCHEMA_VERSION = "isomer-domain-agent-team-template-ref.v1"
TOPIC_AGENT_TEAM_PROFILE_SCHEMA_VERSION = "isomer-topic-agent-team-profile.v1"


@dataclass(frozen=True)
class DomainAgentTeamTemplateRegistration:
    id: str
    source_path_input: str | None
    source_kind: str
    schema_version: str
    status: str
    source_path: Path

    def to_json(self) -> dict[str, object]:
        return {
            "id": self.id,
            "source_path": self.source_path_input,
            "source_kind": self.source_kind,
            "schema_version": self.schema_version,
            "status": self.status,
        }


@dataclass(frozen=True)
class TopicAgentTeamProfileRegistration:
    id: str
    path_input: str
    domain_agent_team_template_id: str
    research_topic_id: str
    schema_version: str
    status: str
    source_path: Path

    def to_json(self) -> dict[str, object]:
        return {
            "id": self.id,
            "path": self.path_input,
            "domain_agent_team_template_id": self.domain_agent_team_template_id,
            "research_topic_id": self.research_topic_id,
            "schema_version": self.schema_version,
            "status": self.status,
        }


@dataclass(frozen=True)
class TemplateArtifact:
    id: str
    path_input: str
    artifact_kind: str
    purpose: str | None = None
    description: str | None = None
    copyable: bool = False

    def to_json(self) -> dict[str, object]:
        return {
            "id": self.id,
            "path": self.path_input,
            "artifact_kind": self.artifact_kind,
            "purpose": self.purpose,
            "description": self.description,
            "copyable": self.copyable,
        }


@dataclass(frozen=True)
class AgentRoleDefinition:
    id: str
    role_kind: str
    description: str
    required: bool
    scalable: bool
    scaling_scope: str | None = None
    agent_profile_placeholder: str | None = None
    capability_binding_placeholder: str | None = None
    skill_projection_placeholder: str | None = None
    workspace_placeholder: str | None = None
    required_skills: list[str] = field(default_factory=list)
    optional_skills: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        return {
            "id": self.id,
            "role_kind": self.role_kind,
            "description": self.description,
            "required": self.required,
            "scalable": self.scalable,
            "scaling_scope": self.scaling_scope,
            "agent_profile_placeholder": self.agent_profile_placeholder,
            "capability_binding_placeholder": self.capability_binding_placeholder,
            "skill_projection_placeholder": self.skill_projection_placeholder,
            "workspace_placeholder": self.workspace_placeholder,
            "required_skills": self.required_skills,
            "optional_skills": self.optional_skills,
        }


@dataclass(frozen=True)
class WorkflowStageRoute:
    workflow_stage: str
    owner_role: str
    alternate_owner_role: str | None = None
    description: str | None = None

    def to_json(self) -> dict[str, object]:
        return {
            "workflow_stage": self.workflow_stage,
            "owner_role": self.owner_role,
            "alternate_owner_role": self.alternate_owner_role,
            "description": self.description,
        }


@dataclass(frozen=True)
class TemplateParameter:
    name: str
    description: str | None
    required_for_topic_profile: bool
    placeholder: str | None = None
    source_path: str | None = None
    expected_replacement_layer: str | None = None
    blocks_profile_save: bool = False
    blocks_launch: bool = False
    derived: bool = False

    def to_json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "description": self.description,
            "required_for_topic_profile": self.required_for_topic_profile,
            "placeholder": self.placeholder,
            "source_path": self.source_path,
            "expected_replacement_layer": self.expected_replacement_layer,
            "blocks_profile_save": self.blocks_profile_save,
            "blocks_launch": self.blocks_launch,
            "derived": self.derived,
        }


@dataclass(frozen=True)
class DomainAgentTeamTemplate:
    id: str
    source_path: Path
    source_kind: str
    root_role: str | None
    topology_mode: str | None
    default_execution_mode: str | None
    topic_instantiation_required: bool
    auto_mode_requires_topic_policy: bool
    artifacts: list[TemplateArtifact] = field(default_factory=list)
    roles: list[AgentRoleDefinition] = field(default_factory=list)
    workflow_stage_routes: list[WorkflowStageRoute] = field(default_factory=list)
    parameters: list[TemplateParameter] = field(default_factory=list)
    instantiation_schema_paths: list[str] = field(default_factory=list)
    copyable_materials: list[TemplateArtifact] = field(default_factory=list)
    raw_metadata: dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> dict[str, object]:
        return {
            "id": self.id,
            "source_path": str(self.source_path),
            "source_kind": self.source_kind,
            "root_role": self.root_role,
            "topology_mode": self.topology_mode,
            "default_execution_mode": self.default_execution_mode,
            "topic_instantiation_required": self.topic_instantiation_required,
            "auto_mode_requires_topic_policy": self.auto_mode_requires_topic_policy,
            "artifacts": [artifact.to_json() for artifact in self.artifacts],
            "roles": [role.to_json() for role in self.roles],
            "workflow_stage_routes": [route.to_json() for route in self.workflow_stage_routes],
            "parameters": [parameter.to_json() for parameter in self.parameters],
            "instantiation_schema_paths": self.instantiation_schema_paths,
            "copyable_materials": [artifact.to_json() for artifact in self.copyable_materials],
        }


@dataclass(frozen=True)
class RoleBinding:
    role_id: str
    active: bool
    agent_profile_ref: str | None = None
    capability_binding_ref: str | None = None
    skill_binding_projection_ref: str | None = None
    agent_name: str | None = None
    agent_branch: str | None = None
    agent_workspace_ref: str | None = None
    required_skills: list[str] = field(default_factory=list)
    optional_skills: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        return {
            "role_id": self.role_id,
            "active": self.active,
            "agent_profile_ref": self.agent_profile_ref,
            "capability_binding_ref": self.capability_binding_ref,
            "skill_binding_projection_ref": self.skill_binding_projection_ref,
            "agent_name": self.agent_name,
            "agent_branch": self.agent_branch,
            "agent_workspace_ref": self.agent_workspace_ref,
            "required_skills": self.required_skills,
            "optional_skills": self.optional_skills,
        }


@dataclass(frozen=True)
class FanoutPolicy:
    role_id: str
    parallel_execution_scope: str
    max_shards: int | None = None
    allocation_rule: str | None = None

    def to_json(self) -> dict[str, object]:
        return {
            "role_id": self.role_id,
            "parallel_execution_scope": self.parallel_execution_scope,
            "max_shards": self.max_shards,
            "allocation_rule": self.allocation_rule,
        }


@dataclass(frozen=True)
class TopicAgentTeamProfile:
    id: str
    domain_agent_team_template_id: str
    research_topic_id: str
    topic_workspace_id: str | None
    source_path: Path
    schema_version: str
    role_bindings: list[RoleBinding] = field(default_factory=list)
    expected_artifacts: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    coordination_policy_ref: str | None = None
    gate_policy_ref: str | None = None
    scheduler_policy_ref: str | None = None
    baseline_waiver_policy_ref: str | None = None
    literature_provider_ref: str | None = None
    default_execution_mode: str | None = None
    automatic_mode_policy_ref: str | None = None
    reviewer_read_access_policy: str | None = None
    fanout_policies: list[FanoutPolicy] = field(default_factory=list)
    profile_bundle_ref: str | None = None
    instantiation_packet_ref: str | None = None
    approval_ref: str | None = None
    approval_actor_ref: str | None = None
    approval_mode: str | None = None
    project_operator_ref: str | None = None
    topic_service_agent_refs: list[str] = field(default_factory=list)
    copied_material_refs: list[str] = field(default_factory=list)
    validation_refs: list[str] = field(default_factory=list)
    launch_blocker_refs: list[str] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> dict[str, object]:
        return {
            "id": self.id,
            "domain_agent_team_template_id": self.domain_agent_team_template_id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "path": str(self.source_path),
            "schema_version": self.schema_version,
            "role_bindings": [binding.to_json() for binding in self.role_bindings],
            "expected_artifacts": self.expected_artifacts,
            "constraints": self.constraints,
            "coordination_policy_ref": self.coordination_policy_ref,
            "gate_policy_ref": self.gate_policy_ref,
            "scheduler_policy_ref": self.scheduler_policy_ref,
            "baseline_waiver_policy_ref": self.baseline_waiver_policy_ref,
            "literature_provider_ref": self.literature_provider_ref,
            "default_execution_mode": self.default_execution_mode,
            "automatic_mode_policy_ref": self.automatic_mode_policy_ref,
            "reviewer_read_access_policy": self.reviewer_read_access_policy,
            "fanout_policies": [policy.to_json() for policy in self.fanout_policies],
            "profile_bundle_ref": self.profile_bundle_ref,
            "instantiation_packet_ref": self.instantiation_packet_ref,
            "approval_ref": self.approval_ref,
            "approval_actor_ref": self.approval_actor_ref,
            "approval_mode": self.approval_mode,
            "project_operator_ref": self.project_operator_ref,
            "topic_service_agent_refs": self.topic_service_agent_refs,
            "copied_material_refs": self.copied_material_refs,
            "validation_refs": self.validation_refs,
            "launch_blocker_refs": self.launch_blocker_refs,
        }


@dataclass(frozen=True)
class TemplateValidationReport:
    template_id: str
    source_path: Path
    ok: bool
    diagnostics: list[Diagnostic]
    template: DomainAgentTeamTemplate | None = None

    def to_json(self) -> dict[str, object]:
        return {
            "template_id": self.template_id,
            "source_path": str(self.source_path),
            "ok": self.ok,
            "template": self.template.to_json() if self.template is not None else None,
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
        }


@dataclass(frozen=True)
class ProfileValidationReport:
    profile_id: str
    source_path: Path
    ok: bool
    diagnostics: list[Diagnostic]
    profile: TopicAgentTeamProfile | None = None

    def to_json(self) -> dict[str, object]:
        return {
            "profile_id": self.profile_id,
            "source_path": str(self.source_path),
            "ok": self.ok,
            "profile": self.profile.to_json() if self.profile is not None else None,
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
        }


@dataclass(frozen=True)
class ResearchTopicRegistration:
    id: str
    config_path_input: str
    topic_workspace_id: str | None
    schema_version: str
    status: str
    source_path: Path

    def to_json(self) -> dict[str, object]:
        return {
            "id": self.id,
            "config_path": self.config_path_input,
            "topic_workspace_id": self.topic_workspace_id,
            "schema_version": self.schema_version,
            "status": self.status,
        }


@dataclass(frozen=True)
class TopicWorkspaceRegistration:
    id: str
    research_topic_id: str | None
    path_input: str | None
    schema_version: str
    status: str
    source_path: Path

    def to_json(self) -> dict[str, object]:
        return {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "path": self.path_input,
            "schema_version": self.schema_version,
            "status": self.status,
        }


@dataclass(frozen=True)
class TopicPixiEnvironmentBinding:
    research_topic_id: str
    pixi_environment: str
    purpose: str | None
    status: str
    source_path: Path

    def to_json(self) -> dict[str, object]:
        return {
            "research_topic_id": self.research_topic_id,
            "pixi_environment": self.pixi_environment,
            "purpose": self.purpose,
            "status": self.status,
        }


@dataclass(frozen=True)
class TopicStandalonePixiBinding:
    research_topic_id: str
    manifest_path_or_dir_input: str
    pixi_environment: str | None
    purpose: str | None
    status: str
    source_path: Path

    def to_json(self) -> dict[str, object]:
        return {
            "research_topic_id": self.research_topic_id,
            "manifest_path_or_dir": self.manifest_path_or_dir_input,
            "pixi_environment": self.pixi_environment,
            "purpose": self.purpose,
            "status": self.status,
        }


TopicStandalonePixiBindingSource = Literal["explicit", "implicit-default"]


@dataclass(frozen=True)
class TopicStandalonePixiBindingTarget:
    research_topic_id: str
    target_path_input: str
    pixi_environment: str
    source: TopicStandalonePixiBindingSource
    source_path: Path | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "research_topic_id": self.research_topic_id,
            "target_path": self.target_path_input,
            "pixi_environment": self.pixi_environment,
            "source": self.source,
        }
        if self.source_path is not None:
            data["source_path"] = str(self.source_path)
        return data


TopicStandalonePixiTargetKind = Literal["file", "directory", "missing", "unknown"]


@dataclass(frozen=True)
class ResolvedTopicStandalonePixiBinding:
    research_topic_id: str
    source: TopicStandalonePixiBindingSource
    target_path: Path
    target_path_input: str
    target_kind: TopicStandalonePixiTargetKind
    resolved_manifest_path: Path
    pixi_environment: str
    environment_prefix: Path

    def to_json(self, project_root: Path | None = None) -> dict[str, object]:
        return {
            "research_topic_id": self.research_topic_id,
            "source": self.source,
            "target_path": _display_model_path(self.target_path, project_root),
            "target_path_input": self.target_path_input,
            "target_kind": self.target_kind,
            "resolved_manifest_path": _display_model_path(self.resolved_manifest_path, project_root),
            "pixi_environment": self.pixi_environment,
            "environment_prefix": _display_model_path(self.environment_prefix, project_root),
        }


@dataclass(frozen=True)
class ProjectManifest:
    schema_version: str
    source_path: Path
    research_topics: list[ResearchTopicRegistration]
    topic_workspaces: list[TopicWorkspaceRegistration]
    topic_pixi_environment_bindings: list[TopicPixiEnvironmentBinding] = field(default_factory=list)
    topic_standalone_pixi_bindings: list[TopicStandalonePixiBinding] = field(default_factory=list)
    domain_agent_team_templates: list[DomainAgentTeamTemplateRegistration] = field(default_factory=list)
    topic_agent_team_profiles: list[TopicAgentTeamProfileRegistration] = field(default_factory=list)
    defaults: dict[str, Any] = field(default_factory=dict)
    path_defaults: dict[str, Any] = field(default_factory=dict)
    artifact_format_profiles: list[str] = field(default_factory=list)
    artifact_extensions: list[str] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)

    def first_topic(self, topic_id: str) -> ResearchTopicRegistration | None:
        return next((topic for topic in self.research_topics if topic.id == topic_id), None)

    def first_workspace(self, workspace_id: str) -> TopicWorkspaceRegistration | None:
        return next((workspace for workspace in self.topic_workspaces if workspace.id == workspace_id), None)

    def active_topic_pixi_environment_bindings(self, topic_id: str) -> list[TopicPixiEnvironmentBinding]:
        return [
            binding
            for binding in self.topic_pixi_environment_bindings
            if binding.research_topic_id == topic_id and binding.status == "active"
        ]

    def active_topic_standalone_pixi_bindings(self, topic_id: str) -> list[TopicStandalonePixiBinding]:
        return [
            binding
            for binding in self.topic_standalone_pixi_bindings
            if binding.research_topic_id == topic_id and binding.status == "active"
        ]

    def effective_topic_standalone_pixi_binding_target(
        self,
        topic_id: str,
        *,
        topic_workspace_path: Path,
        project_root: Path,
    ) -> TopicStandalonePixiBindingTarget:
        explicit = self.active_topic_standalone_pixi_bindings(topic_id)
        if explicit:
            binding = explicit[0]
            return TopicStandalonePixiBindingTarget(
                research_topic_id=topic_id,
                target_path_input=binding.manifest_path_or_dir_input,
                pixi_environment=binding.pixi_environment or "default",
                source="explicit",
                source_path=binding.source_path,
            )
        return TopicStandalonePixiBindingTarget(
            research_topic_id=topic_id,
            target_path_input=_display_model_path(topic_workspace_path, project_root),
            pixi_environment="default",
            source="implicit-default",
            source_path=self.source_path,
        )

    def first_domain_agent_team_template(self, template_id: str) -> DomainAgentTeamTemplateRegistration | None:
        return next((template for template in self.domain_agent_team_templates if template.id == template_id), None)

    def first_topic_agent_team_profile(self, profile_id: str) -> TopicAgentTeamProfileRegistration | None:
        return next((profile for profile in self.topic_agent_team_profiles if profile.id == profile_id), None)

    def default_research_topic_id(self) -> str | None:
        for key in ("research_topic_id", "default_research_topic_id", "default_topic_id"):
            value = self.defaults.get(key)
            if isinstance(value, str) and value:
                return value
        return None

    def default_topic_workspace_id(self) -> str | None:
        for key in ("topic_workspace_id", "default_topic_workspace_id", "default_workspace_id"):
            value = self.defaults.get(key)
            if isinstance(value, str) and value:
                return value
        return None

    def default_domain_agent_team_template_id(self) -> str | None:
        for key in ("domain_agent_team_template_id", "default_domain_agent_team_template_id"):
            value = self.defaults.get(key)
            if isinstance(value, str) and value:
                return value
        return None

    def default_topic_agent_team_profile_id(self) -> str | None:
        for key in ("topic_agent_team_profile_id", "default_topic_agent_team_profile_id"):
            value = self.defaults.get(key)
            if isinstance(value, str) and value:
                return value
        return None

    def to_json(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "path": str(self.source_path),
            "research_topics": [topic.to_json() for topic in self.research_topics],
            "topic_workspaces": [workspace.to_json() for workspace in self.topic_workspaces],
            "topic_pixi_environment_bindings": [
                binding.to_json() for binding in self.topic_pixi_environment_bindings
            ],
            "topic_standalone_pixi_bindings": [
                binding.to_json() for binding in self.topic_standalone_pixi_bindings
            ],
            "domain_agent_team_templates": [template.to_json() for template in self.domain_agent_team_templates],
            "topic_agent_team_profiles": [profile.to_json() for profile in self.topic_agent_team_profiles],
            "defaults": self.defaults,
            "path_defaults": self.path_defaults,
            "artifact_format_profiles": self.artifact_format_profiles,
            "artifact_extensions": self.artifact_extensions,
        }


@dataclass(frozen=True)
class ResearchTopicConfig:
    schema_version: str
    research_topic_id: str
    source_path: Path
    topic_statement: str | None = None
    measurable_objectives: list[str] = field(default_factory=list)
    defaults: dict[str, Any] = field(default_factory=dict)
    refs: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "research_topic_id": self.research_topic_id,
            "path": str(self.source_path),
            "topic_statement": self.topic_statement,
            "measurable_objectives": self.measurable_objectives,
            "defaults": self.defaults,
            "refs": self.refs,
        }

    def default_domain_agent_team_template_id(self) -> str | None:
        for key in (
            "default_domain_agent_team_template_id",
            "domain_agent_team_template_id",
            "default_domain_agent_team_template_ref",
            "domain_agent_team_template_ref",
        ):
            value = self.refs.get(key)
            if isinstance(value, str) and value:
                return value
        return None

    def default_topic_agent_team_profile_id(self) -> str | None:
        for key in (
            "default_topic_agent_team_profile_id",
            "topic_agent_team_profile_id",
            "default_topic_agent_team_profile_ref",
            "topic_agent_team_profile_ref",
        ):
            value = self.refs.get(key)
            if isinstance(value, str) and value:
                return value
        return None


@dataclass(frozen=True)
class LocalActiveContext:
    schema_version: str
    source_path: Path
    refs: dict[str, str]
    raw: dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "path": str(self.source_path),
            "refs": self.refs,
        }


@dataclass(frozen=True)
class Project:
    root: Path
    config_dir: Path
    manifest_path: Path
    manifest: ProjectManifest
    discovery_source: str

    def to_json(self) -> dict[str, object]:
        return {
            "root": str(self.root),
            "project_config_directory": str(self.config_dir),
            "project_manifest": str(self.manifest_path),
            "discovery_source": self.discovery_source,
        }


@dataclass(frozen=True)
class ProjectState:
    project: Project
    topic_configs: dict[str, ResearchTopicConfig]
    local_context: LocalActiveContext | None
    diagnostics: list[Diagnostic]


@dataclass(frozen=True)
class SelectionRequest:
    research_topic_id: str | None = None
    topic_workspace_id: str | None = None
    research_inquiry_id: str | None = None
    research_task_id: str | None = None
    run_id: str | None = None
    agent_team_instance_id: str | None = None
    agent_instance_id: str | None = None
    topic_agent_team_profile_id: str | None = None

    def lifecycle_refs(self) -> dict[str, str]:
        refs = {
            "research_inquiry_id": self.research_inquiry_id,
            "research_task_id": self.research_task_id,
            "run_id": self.run_id,
            "agent_team_instance_id": self.agent_team_instance_id,
            "agent_instance_id": self.agent_instance_id,
        }
        return {key: value for key, value in refs.items() if value is not None}


@dataclass(frozen=True)
class EffectiveTopicContext:
    project: Project
    research_topic: ResearchTopicRegistration
    research_topic_config: ResearchTopicConfig | None
    topic_workspace_id: str
    topic_workspace_path_input: str | None
    topic_workspace_path: Path
    schema_versions: dict[str, str]
    sources: dict[str, str]
    lifecycle_refs: dict[str, str] = field(default_factory=dict)
    domain_agent_team_template_id: str | None = None
    topic_agent_team_profile_id: str | None = None
    profile_refs: dict[str, object] = field(default_factory=dict)

    def to_json(self) -> dict[str, object]:
        return {
            "project": self.project.to_json(),
            "research_topic_id": self.research_topic.id,
            "research_topic_config_path": (
                str(self.research_topic_config.source_path) if self.research_topic_config is not None else None
            ),
            "topic_workspace_id": self.topic_workspace_id,
            "topic_workspace_path_input": self.topic_workspace_path_input,
            "topic_workspace_path": str(self.topic_workspace_path),
            "schema_versions": self.schema_versions,
            "sources": self.sources,
            "lifecycle_refs": self.lifecycle_refs,
            "domain_agent_team_template_id": self.domain_agent_team_template_id,
            "topic_agent_team_profile_id": self.topic_agent_team_profile_id,
            "profile_refs": self.profile_refs,
        }


@dataclass(frozen=True)
class ResolvedPathEntry:
    surface: str
    path: Path
    source: str
    source_detail: str | None = None
    semantic_label: str | None = None
    scope_ref: str | None = None
    compatibility_surface: str | None = None
    storage_profile: str | None = None
    storage_profile_traits: dict[str, object] | None = None
    owner: str | None = None
    durability: str | None = None
    sharing: str | None = None
    path_kind: str | None = None
    path_exists: bool | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "surface": self.surface,
            "path": str(self.path),
            "source": self.source,
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
        if self.storage_profile_traits is not None:
            data["storage_profile_traits"] = self.storage_profile_traits
        if self.owner is not None:
            data["owner"] = self.owner
        if self.durability is not None:
            data["durability"] = self.durability
        if self.sharing is not None:
            data["sharing"] = self.sharing
        if self.path_kind is not None:
            data["path_kind"] = self.path_kind
        if self.path_exists is not None:
            data["exists"] = self.path_exists
        return data


@dataclass(frozen=True)
class BuiltInSchema:
    name: str
    kind: str
    schema_version: str
    description: str

    def to_json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "kind": self.kind,
            "schema_version": self.schema_version,
            "description": self.description,
        }


def _display_model_path(path: Path, root: Path | None) -> str:
    canonical = path.expanduser().resolve(strict=False)
    if root is None:
        return str(canonical)
    try:
        return str(canonical.relative_to(root.expanduser().resolve(strict=False)))
    except ValueError:
        return str(canonical)
