"""Agent Workspace ref resolution and scope validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from isomer_labs.context import resolve_topic_workspace
from isomer_labs.diagnostics import Diagnostic
from isomer_labs.models import Project, RoleBinding, TopicAgentTeamProfile
from isomer_labs.path_utils import canonicalize, is_within, resolve_project_path

AGENT_NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?$")


@dataclass(frozen=True)
class AgentWorkspaceRefResolution:
    ref: str
    path: Path


@dataclass(frozen=True)
class AgentWorkspacePlan:
    agent_name: str
    branch: str
    path: Path
    source: str
    source_detail: str


def resolve_agent_workspace_ref(project: Project, workspace_ref: str) -> AgentWorkspaceRefResolution:
    return AgentWorkspaceRefResolution(
        ref=workspace_ref,
        path=resolve_project_path(project.root, workspace_ref),
    )


def default_agent_branch(agent_name: str) -> str:
    return f"per-agent/{agent_name}/main"


def validate_agent_name_value(
    *,
    agent_name: str | None,
    source_path: Path | None,
    field: str,
    concept: str,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if agent_name is None:
        diagnostics.append(
            Diagnostic(
                code="ISO019",
                severity="error",
                concept=concept,
                path=source_path,
                field=field,
                message="Active role binding is missing topic-local agent_name.",
            )
        )
        return diagnostics
    if agent_name in {".", ".."} or "/" in agent_name or "\\" in agent_name or agent_name.endswith(".lock"):
        diagnostics.append(
            Diagnostic(
                code="ISO019",
                severity="error",
                concept=concept,
                path=source_path,
                field=field,
                message="Agent name is not a safe topic-local path and Git branch segment.",
            )
        )
    elif AGENT_NAME_RE.fullmatch(agent_name) is None:
        diagnostics.append(
            Diagnostic(
                code="ISO019",
                severity="error",
                concept=concept,
                path=source_path,
                field=field,
                message="Agent name must use lowercase letters, digits, dot, underscore, or hyphen and must start and end with a letter or digit.",
            )
        )
    return diagnostics


def resolve_role_binding_agent_workspace_plan(
    *,
    project: Project,
    research_topic_id: str,
    topic_workspace_id: str,
    topic_workspace_path: Path,
    binding: RoleBinding,
    source_path: Path | None,
    field_prefix: str,
    concept: str,
) -> tuple[AgentWorkspacePlan | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    derived_name = _derive_agent_name_from_workspace_ref(
        project=project,
        topic_workspace_path=topic_workspace_path,
        workspace_ref=binding.agent_workspace_ref,
    )
    agent_name = binding.agent_name or derived_name
    diagnostics.extend(
        validate_agent_name_value(
            agent_name=agent_name,
            source_path=source_path,
            field=f"{field_prefix}.agent_name",
            concept=concept,
        )
    )
    if agent_name is None:
        return None, diagnostics

    expected_branch = default_agent_branch(agent_name)
    branch = binding.agent_branch or expected_branch
    if not branch.startswith(f"per-agent/{agent_name}/"):
        diagnostics.append(
            Diagnostic(
                code="ISO019",
                severity="error",
                concept=concept,
                path=source_path,
                field=f"{field_prefix}.agent_branch",
                message="Agent branch must stay under the topic-local agent namespace.",
            )
        )

    expected_path = canonicalize(topic_workspace_path / "agents" / agent_name)
    workspace_path = expected_path
    source = "topic_agent_team_profile.agent_name"
    source_detail = f"{field_prefix}.agent_name={agent_name}"
    if binding.agent_workspace_ref is not None:
        ref_diagnostics = validate_agent_workspace_ref_scope(
            project=project,
            research_topic_id=research_topic_id,
            topic_workspace_id=topic_workspace_id,
            topic_workspace_path=topic_workspace_path,
            workspace_ref=binding.agent_workspace_ref,
            source_path=source_path,
            field=f"{field_prefix}.agent_workspace_ref",
            concept=concept,
        )
        diagnostics.extend(ref_diagnostics)
        compatibility_path = canonicalize(resolve_agent_workspace_ref(project, binding.agent_workspace_ref).path)
        if compatibility_path != expected_path:
            diagnostics.append(
                Diagnostic(
                    code="ISO019",
                    severity="error",
                    concept=concept,
                    path=source_path,
                    field=f"{field_prefix}.agent_workspace_ref",
                    message="Agent Workspace ref does not match the derived topic-local agent_name path.",
                )
            )
        if binding.agent_name is None:
            workspace_path = compatibility_path
            source = "compat.agent_workspace_ref"
            source_detail = f"{field_prefix}.agent_workspace_ref={binding.agent_workspace_ref}"
    elif binding.agent_name is None:
        diagnostics.append(
            Diagnostic(
                code="ISO019",
                severity="error",
                concept=concept,
                path=source_path,
                field=f"{field_prefix}.agent_workspace_ref",
                message="Legacy Agent Workspace ref must point directly at agents/<agent-name> so agent_name can be derived.",
            )
        )

    if diagnostics:
        return None, diagnostics
    return (
        AgentWorkspacePlan(
            agent_name=agent_name,
            branch=branch,
            path=workspace_path,
            source=source,
            source_detail=source_detail,
        ),
        diagnostics,
    )


def validate_agent_workspace_ref_scope(
    *,
    project: Project,
    research_topic_id: str,
    topic_workspace_id: str,
    topic_workspace_path: Path,
    workspace_ref: str,
    source_path: Path | None,
    field: str,
    concept: str,
) -> list[Diagnostic]:
    resolution = resolve_agent_workspace_ref(project, workspace_ref)
    workspace_path = canonicalize(topic_workspace_path)
    resolved_path = canonicalize(resolution.path)
    diagnostics: list[Diagnostic] = []
    if not is_within(resolved_path, project.root):
        diagnostics.append(
            Diagnostic(
                code="ISO019",
                severity="error",
                concept=concept,
                path=source_path,
                field=field,
                message="Agent Workspace ref resolves outside the Project root.",
            )
        )
        return diagnostics
    if resolved_path == workspace_path or not is_within(resolved_path, workspace_path):
        leaked_workspace = _containing_other_topic_workspace(
            project,
            research_topic_id=research_topic_id,
            selected_topic_workspace_id=topic_workspace_id,
            path=resolved_path,
        )
        message = "Agent Workspace ref resolves outside the selected Topic Workspace."
        if leaked_workspace is not None:
            message = "Agent Workspace ref points at another Research Topic's Topic Workspace."
        diagnostics.append(
            Diagnostic(
                code="ISO019",
                severity="error",
                concept=concept,
                path=source_path,
                field=field,
                message=message,
            )
        )
    return diagnostics


def validate_profile_agent_workspace_refs(
    profile: TopicAgentTeamProfile,
    project: Project,
) -> list[Diagnostic]:
    topic = project.manifest.first_topic(profile.research_topic_id)
    if topic is None:
        return []
    workspace, workspace_path, _, diagnostics = resolve_topic_workspace(
        project,
        topic,
        profile.topic_workspace_id,
    )
    if workspace_path is None:
        return diagnostics
    topic_workspace_id = workspace.id if workspace is not None else topic.id
    for binding in profile.role_bindings:
        if not binding.active:
            continue
        _, plan_diagnostics = resolve_role_binding_agent_workspace_plan(
            project=project,
            research_topic_id=profile.research_topic_id,
            topic_workspace_id=topic_workspace_id,
            topic_workspace_path=workspace_path,
            binding=binding,
            source_path=profile.source_path,
            field_prefix=f"role_bindings.{binding.role_id}",
            concept="Topic Agent Team Profile isolation",
        )
        diagnostics.extend(plan_diagnostics)
    return diagnostics


def _derive_agent_name_from_workspace_ref(
    *,
    project: Project,
    topic_workspace_path: Path,
    workspace_ref: str | None,
) -> str | None:
    if workspace_ref is None:
        return None
    resolved_path = canonicalize(resolve_agent_workspace_ref(project, workspace_ref).path)
    agents_root = canonicalize(topic_workspace_path / "agents")
    try:
        relative = resolved_path.relative_to(agents_root)
    except ValueError:
        return None
    parts = relative.parts
    if len(parts) != 1:
        return None
    return parts[0]


def _containing_other_topic_workspace(
    project: Project,
    *,
    research_topic_id: str,
    selected_topic_workspace_id: str,
    path: Path,
) -> str | None:
    for workspace in project.manifest.topic_workspaces:
        if workspace.id == selected_topic_workspace_id:
            continue
        other_topic_id = workspace.research_topic_id
        if other_topic_id is None or other_topic_id == research_topic_id:
            continue
        topic = project.manifest.first_topic(other_topic_id)
        if topic is None:
            continue
        _, workspace_path, _, diagnostics = resolve_topic_workspace(project, topic, workspace.id)
        if diagnostics or workspace_path is None:
            continue
        if is_within(path, workspace_path):
            return workspace.id
    return None
