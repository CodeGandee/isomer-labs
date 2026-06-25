"""Agent Workspace ref resolution and scope validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from isomer_labs.context import resolve_topic_workspace
from isomer_labs.diagnostics import Diagnostic
from isomer_labs.models import Project, TopicAgentTeamProfile
from isomer_labs.path_utils import canonicalize, is_within, resolve_project_path


@dataclass(frozen=True)
class AgentWorkspaceRefResolution:
    ref: str
    path: Path


def resolve_agent_workspace_ref(project: Project, workspace_ref: str) -> AgentWorkspaceRefResolution:
    return AgentWorkspaceRefResolution(
        ref=workspace_ref,
        path=resolve_project_path(project.root, workspace_ref),
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
        if not binding.active or binding.agent_workspace_ref is None:
            continue
        diagnostics.extend(
            validate_agent_workspace_ref_scope(
                project=project,
                research_topic_id=profile.research_topic_id,
                topic_workspace_id=topic_workspace_id,
                topic_workspace_path=workspace_path,
                workspace_ref=binding.agent_workspace_ref,
                source_path=profile.source_path,
                field=f"role_bindings.{binding.role_id}.agent_workspace_ref",
                concept="Topic Agent Team Profile isolation",
            )
        )
    return diagnostics


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
