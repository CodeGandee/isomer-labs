"""Effective Topic Context resolution."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping

from isomer_labs.diagnostics import Diagnostic
from isomer_labs.models import (
    EffectiveTopicContext,
    Project,
    ProjectState,
    ResearchTopicRegistration,
    ResearchTopicConfig,
    SelectionRequest,
    TopicWorkspaceRegistration,
)
from isomer_labs.path_utils import canonicalize, is_within, resolve_project_path
from isomer_labs.team_templates import BUILT_IN_DEEPSCI_ORG_ID


IDENTITY_ENV_FIELDS = {
    "ISOMER_RESEARCH_TOPIC_ID": "research_topic_id",
    "ISOMER_TOPIC_WORKSPACE_ID": "topic_workspace_id",
    "ISOMER_RESEARCH_INQUIRY_ID": "research_inquiry_id",
    "ISOMER_RESEARCH_TASK_ID": "research_task_id",
    "ISOMER_RUN_ID": "run_id",
    "ISOMER_AGENT_TEAM_INSTANCE_ID": "agent_team_instance_id",
    "ISOMER_AGENT_INSTANCE_ID": "agent_instance_id",
    "ISOMER_TOPIC_AGENT_TEAM_PROFILE_ID": "topic_agent_team_profile_id",
}


@dataclass(frozen=True)
class Candidate:
    source: str
    research_topic_id: str | None = None
    topic_workspace_id: str | None = None
    topic_agent_team_profile_id: str | None = None
    lifecycle_refs: dict[str, str] = field(default_factory=dict)


def resolve_effective_topic_context(
    state: ProjectState,
    request: SelectionRequest,
    *,
    cwd: Path,
    env: Mapping[str, str],
) -> tuple[EffectiveTopicContext | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    candidate_diagnostics: list[Diagnostic] = []
    candidates = _selection_candidates(state, request, cwd=cwd, env=env, diagnostics=candidate_diagnostics)
    diagnostics.extend(candidate_diagnostics)
    selected = next((candidate for candidate in candidates if candidate.research_topic_id is not None), None)
    if selected is None:
        diagnostics.append(
            Diagnostic(
                code="ISO013",
                severity="error",
                concept="Effective Topic Context",
                message="No Research Topic could be selected from explicit selectors, current directory, environment, local active context, or Project Manifest defaults.",
            )
        )
        return None, diagnostics

    selected_topic_id = selected.research_topic_id
    if selected_topic_id is None:
        return None, diagnostics
    topic = state.project.manifest.first_topic(selected_topic_id)
    if topic is None:
        diagnostics.append(
            Diagnostic(
                code="ISO013",
                severity="error",
                concept="Effective Topic Context",
                field="research_topic_id",
                message="Selected Research Topic is not registered by the Project Manifest.",
            )
        )
        return None, diagnostics

    workspace, workspace_path, workspace_source, workspace_diagnostics = resolve_topic_workspace(
        state.project,
        topic,
        selected.topic_workspace_id,
    )
    diagnostics.extend(workspace_diagnostics)
    if workspace_path is None:
        return None, diagnostics

    topic_config = state.topic_configs.get(topic.id)
    template_id, profile_id, profile_source, profile_refs = _select_template_and_profile(
        state,
        topic_config,
        selected,
        request,
    )
    schema_versions = {
        "project_manifest": state.project.manifest.schema_version,
        "research_topic_registration": topic.schema_version,
    }
    if topic_config is not None:
        schema_versions["research_topic_config"] = topic_config.schema_version
    if state.local_context is not None:
        schema_versions["local_active_context"] = state.local_context.schema_version

    lifecycle_refs = dict(selected.lifecycle_refs)
    for key in sorted(lifecycle_refs):
        diagnostics.append(
            Diagnostic(
                code="ISO015",
                severity="warning",
                concept="Effective Topic Context",
                field=key,
                message="Milestone 1 cannot validate this lifecycle ref without Workspace Runtime support.",
            )
        )

    context = EffectiveTopicContext(
        project=state.project,
        research_topic=topic,
        research_topic_config=topic_config,
        topic_workspace_id=workspace.id if workspace is not None else topic.id,
        topic_workspace_path_input=workspace.path_input if workspace is not None else None,
        topic_workspace_path=workspace_path,
        schema_versions=schema_versions,
        sources={
            "project": state.project.discovery_source,
            "research_topic_id": selected.source,
            "research_topic_config": "Project Manifest",
            "topic_workspace_id": selected.source if selected.topic_workspace_id is not None else workspace_source,
            "topic_workspace_path": workspace_source,
            "domain_agent_team_template_id": profile_source,
            "topic_agent_team_profile_id": profile_source,
        },
        lifecycle_refs=lifecycle_refs,
        domain_agent_team_template_id=template_id,
        topic_agent_team_profile_id=profile_id,
        profile_refs=profile_refs,
    )
    return context, diagnostics


def resolve_topic_workspace(
    project: Project,
    topic: ResearchTopicRegistration,
    requested_workspace_id: str | None,
) -> tuple[TopicWorkspaceRegistration | None, Path | None, str, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    manifest = project.manifest
    workspace: TopicWorkspaceRegistration | None = None
    source = "default"

    if requested_workspace_id is not None:
        workspace = manifest.first_workspace(requested_workspace_id)
        if workspace is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO014",
                    severity="error",
                    concept="Topic Workspace",
                    field="topic_workspace_id",
                    message="Selected Topic Workspace is not registered by the Project Manifest.",
                )
            )
            return None, None, source, diagnostics
        source = "Project Manifest"
    elif topic.topic_workspace_id is not None:
        workspace = manifest.first_workspace(topic.topic_workspace_id)
        if workspace is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO008",
                    severity="error",
                    concept="Topic Workspace",
                    field="topic_workspace_id",
                    message="Research Topic references a missing Topic Workspace.",
                )
            )
            return None, None, source, diagnostics
        source = "Project Manifest"
    else:
        matching = [workspace for workspace in manifest.topic_workspaces if workspace.research_topic_id == topic.id]
        if len(matching) == 1:
            workspace = matching[0]
            source = "Project Manifest"
        elif len(matching) > 1:
            diagnostics.append(
                Diagnostic(
                    code="ISO012",
                    severity="error",
                    concept="Effective Topic Context",
                    field="topic_workspace_id",
                    message="Multiple Topic Workspaces are registered for the selected Research Topic.",
                )
            )
            return None, None, source, diagnostics

    if workspace is not None and workspace.research_topic_id is not None and workspace.research_topic_id != topic.id:
        diagnostics.append(
            Diagnostic(
                code="ISO012",
                severity="error",
                concept="Effective Topic Context",
                field="topic_workspace_id",
                message="Selected Topic Workspace belongs to a different Research Topic.",
            )
        )
        return None, None, source, diagnostics

    path_input = workspace.path_input if workspace is not None else None
    if path_input is None:
        base = _manifest_path_default(project, "topic_workspace_base_dir")
        if base is None:
            workspace_path = resolve_project_path(project.root, f"topic-workspaces/{topic.id}")
            source = "default"
        else:
            workspace_path = resolve_project_path(project.root, f"{base}/{topic.id}")
            source = "Project Manifest"
    else:
        workspace_path = resolve_project_path(project.root, path_input)
        if source == "default":
            source = "Project Manifest"

    if not is_within(workspace_path, project.root):
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="Topic Workspace",
                field="path",
                message="Topic Workspace path resolves outside the Project root.",
            )
        )
        return workspace, None, source, diagnostics
    return workspace, workspace_path, source, diagnostics


def _selection_candidates(
    state: ProjectState,
    request: SelectionRequest,
    *,
    cwd: Path,
    env: Mapping[str, str],
    diagnostics: list[Diagnostic],
) -> list[Candidate]:
    candidates: list[Candidate] = []
    explicit = _candidate_from_refs(
        state,
        source="explicit selector",
        research_topic_id=request.research_topic_id,
        topic_workspace_id=request.topic_workspace_id,
        topic_agent_team_profile_id=request.topic_agent_team_profile_id,
        lifecycle_refs=request.lifecycle_refs(),
        diagnostics=diagnostics,
    )
    if explicit is not None:
        candidates.append(explicit)

    current_directory = _candidate_from_current_directory(state, cwd)
    if current_directory is not None:
        candidates.append(current_directory)

    env_refs = {
        field: env[var]
        for var, field in IDENTITY_ENV_FIELDS.items()
        if var in env and env[var]
    }
    env_candidate = _candidate_from_refs(
        state,
        source="environment",
        research_topic_id=env_refs.get("research_topic_id"),
        topic_workspace_id=env_refs.get("topic_workspace_id"),
        topic_agent_team_profile_id=env_refs.get("topic_agent_team_profile_id"),
        lifecycle_refs={
            key: value
            for key, value in env_refs.items()
            if key not in {"research_topic_id", "topic_workspace_id", "topic_agent_team_profile_id"}
        },
        diagnostics=diagnostics,
    )
    if env_candidate is not None:
        candidates.append(env_candidate)

    if state.local_context is not None:
        local_candidate = _candidate_from_refs(
            state,
            source=".isomer-labs/local.toml",
            research_topic_id=state.local_context.refs.get("research_topic_id"),
            topic_workspace_id=state.local_context.refs.get("topic_workspace_id"),
            topic_agent_team_profile_id=state.local_context.refs.get("topic_agent_team_profile_id"),
            lifecycle_refs={
                key: value
                for key, value in state.local_context.refs.items()
                if key not in {"research_topic_id", "topic_workspace_id", "topic_agent_team_profile_id"}
            },
            diagnostics=diagnostics,
        )
        if local_candidate is not None:
            candidates.append(local_candidate)

    default_topic_id = state.project.manifest.default_research_topic_id()
    if default_topic_id is not None:
        candidates.append(Candidate(source="Project Manifest default", research_topic_id=default_topic_id))
    elif len(state.project.manifest.research_topics) == 1:
        candidates.append(
            Candidate(
                source="single Project Manifest registration",
                research_topic_id=state.project.manifest.research_topics[0].id,
            )
        )
    return candidates


def _candidate_from_refs(
    state: ProjectState,
    *,
    source: str,
    research_topic_id: str | None,
    topic_workspace_id: str | None,
    topic_agent_team_profile_id: str | None,
    lifecycle_refs: dict[str, str],
    diagnostics: list[Diagnostic],
) -> Candidate | None:
    if research_topic_id is None and topic_workspace_id is None and topic_agent_team_profile_id is None and not lifecycle_refs:
        return None

    inferred_topic_id = research_topic_id
    if topic_agent_team_profile_id is not None:
        profile = state.project.manifest.first_topic_agent_team_profile(topic_agent_team_profile_id)
        if profile is not None:
            if inferred_topic_id is not None and inferred_topic_id != profile.research_topic_id:
                diagnostics.append(
                    Diagnostic(
                        code="ISO012",
                        severity="error",
                        concept="Effective Topic Context",
                        field="topic_agent_team_profile_id",
                        message=f"{source} selected conflicting Research Topic and Topic Agent Team Profile refs.",
                    )
                )
            inferred_topic_id = inferred_topic_id or profile.research_topic_id
    if topic_workspace_id is not None:
        workspace = state.project.manifest.first_workspace(topic_workspace_id)
        if workspace is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO014",
                    severity="error",
                    concept="Effective Topic Context",
                    field="topic_workspace_id",
                    message=f"{source} selected an unknown Topic Workspace.",
                )
            )
        elif workspace.research_topic_id is not None:
            if inferred_topic_id is not None and inferred_topic_id != workspace.research_topic_id:
                diagnostics.append(
                    Diagnostic(
                        code="ISO012",
                        severity="error",
                        concept="Effective Topic Context",
                        field="topic_workspace_id",
                        message=f"{source} selected conflicting Research Topic and Topic Workspace refs.",
                    )
                )
            inferred_topic_id = workspace.research_topic_id
        else:
            matching_topics = [
                topic.id
                for topic in state.project.manifest.research_topics
                if topic.topic_workspace_id == topic_workspace_id
            ]
            if len(matching_topics) == 1:
                inferred_topic_id = matching_topics[0]
            elif len(matching_topics) > 1:
                diagnostics.append(
                    Diagnostic(
                        code="ISO012",
                        severity="error",
                        concept="Effective Topic Context",
                        field="topic_workspace_id",
                        message=f"{source} selected a Topic Workspace referenced by multiple Research Topics.",
                    )
                )

    if inferred_topic_id is None and lifecycle_refs:
        diagnostics.append(
            Diagnostic(
                code="ISO015",
                severity="warning",
                concept="Effective Topic Context",
                message=f"{source} provided lifecycle refs, but Milestone 1 cannot infer a Research Topic from them without Workspace Runtime support.",
            )
        )
    return Candidate(
        source=source,
        research_topic_id=inferred_topic_id,
        topic_workspace_id=topic_workspace_id,
        topic_agent_team_profile_id=topic_agent_team_profile_id,
        lifecycle_refs=lifecycle_refs,
    )


def _candidate_from_current_directory(state: ProjectState, cwd: Path) -> Candidate | None:
    matches: list[tuple[int, str, str]] = []
    canonical_cwd = canonicalize(cwd)
    for topic in state.project.manifest.research_topics:
        workspace, workspace_path, _, diagnostics = resolve_topic_workspace(state.project, topic, None)
        if diagnostics or workspace_path is None:
            continue
        try:
            canonical_cwd.relative_to(workspace_path)
        except ValueError:
            continue
        workspace_id = workspace.id if workspace is not None else topic.id
        matches.append((len(str(workspace_path)), topic.id, workspace_id))
    if not matches:
        return None
    _, topic_id, workspace_id = sorted(matches, reverse=True)[0]
    return Candidate(
        source="current directory",
        research_topic_id=topic_id,
        topic_workspace_id=workspace_id,
    )


def _manifest_path_default(project: Project, key: str) -> str | None:
    value = project.manifest.path_defaults.get(key)
    if isinstance(value, str) and value:
        return value
    return None


def _select_template_and_profile(
    state: ProjectState,
    topic_config: ResearchTopicConfig | None,
    selected: Candidate,
    request: SelectionRequest,
) -> tuple[str | None, str | None, str, dict[str, object]]:
    profile_refs = dict(topic_config.refs) if topic_config is not None else {}
    profile_id = request.topic_agent_team_profile_id
    source = "explicit selector" if profile_id is not None else "none"
    if profile_id is None and topic_config is not None:
        profile_id = topic_config.default_topic_agent_team_profile_id()
        if profile_id is not None:
            source = "Research Topic Config default"
    if profile_id is None:
        profile_id = state.project.manifest.default_topic_agent_team_profile_id()
        if profile_id is not None:
            source = "Project Manifest default"
    if profile_id is None and selected.topic_agent_team_profile_id is not None:
        profile_id = selected.topic_agent_team_profile_id
        source = selected.source
    profile_registration = state.project.manifest.first_topic_agent_team_profile(profile_id) if profile_id is not None else None

    template_id = None
    if profile_registration is not None:
        template_id = profile_registration.domain_agent_team_template_id
    if template_id is None and topic_config is not None:
        template_id = topic_config.default_domain_agent_team_template_id()
        if template_id is not None and profile_id is None:
            source = "Research Topic Config default"
    if template_id is None:
        template_id = state.project.manifest.default_domain_agent_team_template_id()
        if template_id is not None and profile_id is None:
            source = "Project Manifest default"
    if template_id is None:
        template_id = BUILT_IN_DEEPSCI_ORG_ID
        if profile_id is None:
            source = "template default"
    return template_id, profile_id, source, profile_refs
