"""Read-only ambient workspace classification and task-context alignment."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Mapping

from isomer_labs.core.diagnostics import Diagnostic
from isomer_labs.core.path_utils import canonicalize, is_within
from isomer_labs.models import EffectiveTopicContext, Project, SelectionRequest
from isomer_labs.project.context import resolve_effective_topic_context
from isomer_labs.project.validation import build_project_state
from isomer_labs.workspace.manifest import EffectiveAgentContext, EffectiveTopicActorContext
from isomer_labs.workspace.path_resolution import (
    resolve_effective_agent_context,
    resolve_effective_topic_actor_context,
    resolve_semantic_path,
)


IMPLICIT_TOPIC_SELECTION_SOURCES = frozenset(
    {
        "Project Manifest default",
        "single Project Manifest registration",
    }
)


class WorkspaceKind(str, Enum):
    """Stable ambient workspace classifications."""

    PROJECT_ROOT = "project_root"
    PROJECT_SUBPATH = "project_subpath"
    TOPIC_WORKSPACE = "topic_workspace"
    TOPIC_MAIN = "topic_main"
    TOPIC_ACTOR_WORKSPACE = "topic_actor_workspace"
    AGENT_WORKSPACE = "agent_workspace"
    OUTSIDE_PROJECT = "outside_project"
    AMBIGUOUS = "ambiguous"


class OperationScope(str, Enum):
    """Scopes accepted by the context-alignment query."""

    PROJECT = "project"
    TOPIC = "topic"
    TOPIC_ACTOR = "topic-actor"
    AGENT = "agent"


class AlignmentVerdict(str, Enum):
    """Stable task-context alignment verdicts."""

    ALIGNED = "aligned"
    EXPLICIT_OVERRIDE = "explicit_override"
    UNRESOLVED = "unresolved"
    CONFLICT = "conflict"


@dataclass(frozen=True)
class AmbientWorkspaceMatch:
    """One registered semantic workspace containing cwd."""

    workspace_kind: WorkspaceKind
    workspace_root: Path
    research_topic_id: str
    topic_workspace_id: str
    worker_kind: str | None = None
    worker_name: str | None = None

    def identity(self) -> tuple[str, str, str, str, str | None, str | None]:
        return (
            self.workspace_kind.value,
            str(self.workspace_root),
            self.research_topic_id,
            self.topic_workspace_id,
            self.worker_kind,
            self.worker_name,
        )

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "workspace_kind": self.workspace_kind.value,
            "workspace_root": str(self.workspace_root),
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
        }
        if self.worker_kind is not None:
            data["worker_kind"] = self.worker_kind
        if self.worker_name is not None:
            data["worker_name"] = self.worker_name
        return data


@dataclass(frozen=True)
class AmbientWorkspaceLocation:
    """Canonical cwd classification independent from selection defaults."""

    cwd: Path
    project_root: Path
    workspace_kind: WorkspaceKind
    source: str = "cwd"
    workspace_root: Path | None = None
    research_topic_id: str | None = None
    topic_workspace_id: str | None = None
    worker_kind: str | None = None
    worker_name: str | None = None
    candidates: tuple[AmbientWorkspaceMatch, ...] = ()

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "resolved": self.workspace_kind is not WorkspaceKind.AMBIGUOUS,
            "cwd": str(self.cwd),
            "project_root": str(self.project_root),
            "workspace_kind": self.workspace_kind.value,
            "source": self.source,
        }
        if self.workspace_root is not None:
            data["workspace_root"] = str(self.workspace_root)
        if self.research_topic_id is not None:
            data["research_topic_id"] = self.research_topic_id
        if self.topic_workspace_id is not None:
            data["topic_workspace_id"] = self.topic_workspace_id
        if self.worker_kind is not None:
            data["worker_kind"] = self.worker_kind
        if self.worker_name is not None:
            data["worker_name"] = self.worker_name
        if self.candidates:
            data["candidates"] = [candidate.to_json() for candidate in self.candidates]
        return data


@dataclass(frozen=True)
class ContextDefault:
    """One fallback source considered by Effective Context resolution."""

    kind: str
    value: str
    source: str

    def to_json(self) -> dict[str, str]:
        return {"kind": self.kind, "value": self.value, "source": self.source}


@dataclass(frozen=True)
class TaskContextTarget:
    """Selected target for one declared operation scope."""

    scope: OperationScope
    project_root: Path
    sources: dict[str, str]
    research_topic_id: str | None = None
    topic_workspace_id: str | None = None
    worker_kind: str | None = None
    worker_name: str | None = None
    worker_workspace: Path | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "scope": self.scope.value,
            "project_root": str(self.project_root),
            "sources": dict(self.sources),
        }
        if self.research_topic_id is not None:
            data["research_topic_id"] = self.research_topic_id
        if self.topic_workspace_id is not None:
            data["topic_workspace_id"] = self.topic_workspace_id
        if self.worker_kind is not None:
            data["worker_kind"] = self.worker_kind
        if self.worker_name is not None:
            data["worker_name"] = self.worker_name
        if self.worker_workspace is not None:
            data["worker_workspace"] = str(self.worker_workspace)
        return data


@dataclass(frozen=True)
class ContextAlignmentResult:
    """Read-only comparison between task target and ambient location."""

    requested_scope: OperationScope
    verdict: AlignmentVerdict
    ambient_location: AmbientWorkspaceLocation
    selected_target: TaskContextTarget | None
    defaults_considered: tuple[ContextDefault, ...]
    reasons: tuple[str, ...]
    expected_cwd: Path | None = None
    ambient_cwd_matches_expected: bool | None = None

    @property
    def blocking(self) -> bool:
        return self.verdict in {AlignmentVerdict.UNRESOLVED, AlignmentVerdict.CONFLICT}

    def to_json(self) -> dict[str, object]:
        return {
            "requested_scope": self.requested_scope.value,
            "verdict": self.verdict.value,
            "blocking": self.blocking,
            "ambient_location": self.ambient_location.to_json(),
            "selected_target": self.selected_target.to_json() if self.selected_target is not None else None,
            "defaults_considered": [default.to_json() for default in self.defaults_considered],
            "expected_cwd": str(self.expected_cwd) if self.expected_cwd is not None else None,
            "ambient_cwd_matches_expected": self.ambient_cwd_matches_expected,
            "acting_posture": {
                "established": False,
                "source": None,
                "note": "Acting posture is session-local and is not inferred or persisted by this query.",
            },
            "reasons": list(self.reasons),
        }


def resolve_ambient_workspace_location(
    project: Project,
    *,
    cwd: Path,
    env: Mapping[str, str],
) -> tuple[AmbientWorkspaceLocation, list[Diagnostic]]:
    """Classify cwd against every registered Topic Workspace and worker surface."""

    canonical_cwd = canonicalize(cwd)
    project_root = canonicalize(project.root)
    state = build_project_state(project)
    diagnostics = list(state.diagnostics)
    matches: list[AmbientWorkspaceMatch] = []

    for registration in project.manifest.research_topics:
        context, context_diagnostics = resolve_effective_topic_context(
            state,
            SelectionRequest(research_topic_id=registration.id),
            cwd=canonical_cwd,
            env={},
        )
        _extend_unique(diagnostics, context_diagnostics)
        if context is None:
            continue
        topic_root = canonicalize(context.topic_workspace_path)
        if not is_within(canonical_cwd, topic_root):
            continue
        matches.append(_match_for_context(WorkspaceKind.TOPIC_WORKSPACE, topic_root, context))

        topic_main, topic_main_diagnostics = resolve_semantic_path(
            context,
            "topic.repos.main",
            env=env,
            cwd=canonical_cwd,
        )
        _extend_unique(diagnostics, topic_main_diagnostics)
        if topic_main is not None and is_within(canonical_cwd, topic_main.path):
            matches.append(_match_for_context(WorkspaceKind.TOPIC_MAIN, canonicalize(topic_main.path), context))

        actor_context, actor_diagnostics = resolve_effective_topic_actor_context(
            context,
            env={},
            cwd=canonical_cwd,
            missing_is_error=False,
        )
        _extend_unique(diagnostics, actor_diagnostics)
        if actor_context is not None and actor_context.source == "cwd":
            matches.append(
                _match_for_context(
                    WorkspaceKind.TOPIC_ACTOR_WORKSPACE,
                    canonicalize(actor_context.topic_actor_workspace_path),
                    context,
                    worker_kind="topic_actor",
                    worker_name=actor_context.topic_actor_name,
                )
            )

        agent_context, agent_diagnostics = resolve_effective_agent_context(
            context,
            env={},
            cwd=canonical_cwd,
            missing_is_error=False,
        )
        _extend_unique(diagnostics, agent_diagnostics)
        if agent_context is not None and agent_context.source == "cwd":
            matches.append(
                _match_for_context(
                    WorkspaceKind.AGENT_WORKSPACE,
                    canonicalize(agent_context.agent_workspace_path),
                    context,
                    worker_kind="agent",
                    worker_name=agent_context.agent_name,
                )
            )

    unique_matches = {match.identity(): match for match in matches}
    matches = list(unique_matches.values())
    if matches:
        longest = max(len(match.workspace_root.parts) for match in matches)
        selected_matches = tuple(
            sorted(
                (match for match in matches if len(match.workspace_root.parts) == longest),
                key=lambda match: match.identity(),
            )
        )
        if len(selected_matches) > 1:
            diagnostics.append(
                Diagnostic(
                    code="ISO088",
                    severity="error",
                    concept="Ambient Workspace Location",
                    field="cwd",
                    message="Current directory matches more than one equally specific registered workspace owner.",
                )
            )
            return (
                AmbientWorkspaceLocation(
                    cwd=canonical_cwd,
                    project_root=project_root,
                    workspace_kind=WorkspaceKind.AMBIGUOUS,
                    candidates=selected_matches,
                ),
                diagnostics,
            )
        selected = selected_matches[0]
        return (
            AmbientWorkspaceLocation(
                cwd=canonical_cwd,
                project_root=project_root,
                workspace_kind=selected.workspace_kind,
                workspace_root=selected.workspace_root,
                research_topic_id=selected.research_topic_id,
                topic_workspace_id=selected.topic_workspace_id,
                worker_kind=selected.worker_kind,
                worker_name=selected.worker_name,
                candidates=selected_matches,
            ),
            diagnostics,
        )

    if canonical_cwd == project_root:
        workspace_kind = WorkspaceKind.PROJECT_ROOT
        workspace_root: Path | None = project_root
    elif is_within(canonical_cwd, project_root):
        workspace_kind = WorkspaceKind.PROJECT_SUBPATH
        workspace_root = project_root
    else:
        workspace_kind = WorkspaceKind.OUTSIDE_PROJECT
        workspace_root = None
    return (
        AmbientWorkspaceLocation(
            cwd=canonical_cwd,
            project_root=project_root,
            workspace_kind=workspace_kind,
            workspace_root=workspace_root,
        ),
        diagnostics,
    )


def resolve_task_context_alignment(
    project: Project,
    *,
    scope: OperationScope,
    ambient_location: AmbientWorkspaceLocation,
    context: EffectiveTopicContext | None,
    topic_actor_context: EffectiveTopicActorContext | None,
    agent_context: EffectiveAgentContext | None,
    explicit_topic_selection: bool,
    explicit_worker_selection: bool,
) -> tuple[ContextAlignmentResult, list[Diagnostic]]:
    """Compare a declared operation scope with selected and ambient context."""

    diagnostics: list[Diagnostic] = []
    defaults = _context_defaults(context, topic_actor_context)
    if ambient_location.workspace_kind is WorkspaceKind.AMBIGUOUS:
        return (
            ContextAlignmentResult(
                requested_scope=scope,
                verdict=AlignmentVerdict.CONFLICT,
                ambient_location=ambient_location,
                selected_target=None,
                defaults_considered=defaults,
                reasons=("Ambient cwd has multiple equally specific registered workspace owners.",),
            ),
            diagnostics,
        )

    if scope is OperationScope.PROJECT:
        project_target = TaskContextTarget(
            scope=scope,
            project_root=canonicalize(project.root),
            sources={"project": project.discovery_source},
        )
        return (
            ContextAlignmentResult(
                requested_scope=scope,
                verdict=AlignmentVerdict.ALIGNED,
                ambient_location=ambient_location,
                selected_target=project_target,
                defaults_considered=(),
                reasons=("Project-scoped operation does not acquire a topic or worker target from defaults.",),
            ),
            diagnostics,
        )

    if context is None:
        diagnostics.append(_unresolved_diagnostic(scope, "Effective Topic Context could not be resolved."))
        return (
            ContextAlignmentResult(
                requested_scope=scope,
                verdict=AlignmentVerdict.UNRESOLVED,
                ambient_location=ambient_location,
                selected_target=None,
                defaults_considered=defaults,
                reasons=("The requested scope requires a resolved Research Topic.",),
            ),
            diagnostics,
        )

    target = _target_for_scope(scope, context, topic_actor_context, agent_context)
    if target is None:
        diagnostics.append(_unresolved_diagnostic(scope, f"{scope.value} target could not be resolved."))
        return (
            ContextAlignmentResult(
                requested_scope=scope,
                verdict=AlignmentVerdict.UNRESOLVED,
                ambient_location=ambient_location,
                selected_target=None,
                defaults_considered=defaults,
                reasons=(f"The requested {scope.value} scope requires a selected worker.",),
            ),
            diagnostics,
        )

    if (
        scope is OperationScope.TOPIC_ACTOR
        and topic_actor_context is not None
        and topic_actor_context.source == "manifest default"
        and not explicit_worker_selection
    ):
        diagnostics.append(
            Diagnostic(
                code="ISO088",
                severity="error",
                concept="Operator Context Preflight",
                field="topic_actor_name",
                message=(
                    "A sole manifest Topic Actor is an Effective Context fallback, not active acting posture; "
                    "pass --topic-actor or switch identity explicitly."
                ),
            )
        )
        return (
            ContextAlignmentResult(
                requested_scope=scope,
                verdict=AlignmentVerdict.UNRESOLVED,
                ambient_location=ambient_location,
                selected_target=target,
                defaults_considered=defaults,
                reasons=("Manifest-default Topic Actor did not establish active acting posture.",),
                expected_cwd=target.worker_workspace,
                ambient_cwd_matches_expected=False,
            ),
            diagnostics,
        )

    if scope in {OperationScope.TOPIC_ACTOR, OperationScope.AGENT}:
        expected_cwd = target.worker_workspace
        cwd_matches = expected_cwd is not None and is_within(ambient_location.cwd, expected_cwd)
        if not cwd_matches:
            diagnostics.append(
                Diagnostic(
                    code="ISO088",
                    severity="error",
                    concept="Operator Context Preflight",
                    field="cwd",
                    message=f"Current directory does not match the selected {scope.value} workspace.",
                    hint=f"Run switched work from {expected_cwd}." if expected_cwd is not None else None,
                )
            )
            return (
                ContextAlignmentResult(
                    requested_scope=scope,
                    verdict=AlignmentVerdict.CONFLICT,
                    ambient_location=ambient_location,
                    selected_target=target,
                    defaults_considered=defaults,
                    reasons=("Selected worker target and ambient cwd do not align.",),
                    expected_cwd=expected_cwd,
                    ambient_cwd_matches_expected=False,
                ),
                diagnostics,
            )
        return (
            ContextAlignmentResult(
                requested_scope=scope,
                verdict=AlignmentVerdict.ALIGNED,
                ambient_location=ambient_location,
                selected_target=target,
                defaults_considered=defaults,
                reasons=("Ambient cwd is inside the selected worker workspace.",),
                expected_cwd=expected_cwd,
                ambient_cwd_matches_expected=True,
            ),
            diagnostics,
        )

    ambient_topic = ambient_location.research_topic_id
    selected_topic = context.research_topic.id
    if explicit_topic_selection and ambient_topic != selected_topic:
        return (
            ContextAlignmentResult(
                requested_scope=scope,
                verdict=AlignmentVerdict.EXPLICIT_OVERRIDE,
                ambient_location=ambient_location,
                selected_target=target,
                defaults_considered=defaults,
                reasons=("Explicit topic selection overrides the ambient workspace topic.",),
            ),
            diagnostics,
        )
    if ambient_topic is not None and ambient_topic != selected_topic:
        diagnostics.append(
            Diagnostic(
                code="ISO088",
                severity="error",
                concept="Operator Context Preflight",
                field="research_topic_id",
                message="Implicit selected Research Topic conflicts with the ambient Topic Workspace.",
            )
        )
        return (
            ContextAlignmentResult(
                requested_scope=scope,
                verdict=AlignmentVerdict.CONFLICT,
                ambient_location=ambient_location,
                selected_target=target,
                defaults_considered=defaults,
                reasons=("Implicit topic sources disagree.",),
            ),
            diagnostics,
        )
    return (
        ContextAlignmentResult(
            requested_scope=scope,
            verdict=AlignmentVerdict.ALIGNED,
            ambient_location=ambient_location,
            selected_target=target,
            defaults_considered=defaults,
            reasons=("Selected task target is compatible with ambient location and source precedence.",),
        ),
        diagnostics,
    )


def _match_for_context(
    workspace_kind: WorkspaceKind,
    workspace_root: Path,
    context: EffectiveTopicContext,
    *,
    worker_kind: str | None = None,
    worker_name: str | None = None,
) -> AmbientWorkspaceMatch:
    return AmbientWorkspaceMatch(
        workspace_kind=workspace_kind,
        workspace_root=workspace_root,
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        worker_kind=worker_kind,
        worker_name=worker_name,
    )


def _context_defaults(
    context: EffectiveTopicContext | None,
    topic_actor_context: EffectiveTopicActorContext | None,
) -> tuple[ContextDefault, ...]:
    defaults: list[ContextDefault] = []
    if context is not None:
        source = context.sources.get("research_topic_id")
        if source in IMPLICIT_TOPIC_SELECTION_SOURCES:
            defaults.append(ContextDefault("research_topic", context.research_topic.id, source))
    if topic_actor_context is not None and topic_actor_context.source == "manifest default":
        defaults.append(ContextDefault("topic_actor", topic_actor_context.topic_actor_name, topic_actor_context.source))
    return tuple(defaults)


def _target_for_scope(
    scope: OperationScope,
    context: EffectiveTopicContext,
    topic_actor_context: EffectiveTopicActorContext | None,
    agent_context: EffectiveAgentContext | None,
) -> TaskContextTarget | None:
    sources = dict(context.sources)
    project_root = canonicalize(context.project.root)
    research_topic_id = context.research_topic.id
    topic_workspace_id = context.topic_workspace_id
    if scope is OperationScope.TOPIC:
        return TaskContextTarget(
            scope=scope,
            project_root=project_root,
            sources=sources,
            research_topic_id=research_topic_id,
            topic_workspace_id=topic_workspace_id,
        )
    if scope is OperationScope.TOPIC_ACTOR and topic_actor_context is not None:
        sources["topic_actor_name"] = topic_actor_context.source
        return TaskContextTarget(
            scope=scope,
            project_root=project_root,
            sources=sources,
            research_topic_id=research_topic_id,
            topic_workspace_id=topic_workspace_id,
            worker_kind="topic_actor",
            worker_name=topic_actor_context.topic_actor_name,
            worker_workspace=canonicalize(topic_actor_context.topic_actor_workspace_path),
        )
    if scope is OperationScope.AGENT and agent_context is not None:
        sources["agent_name"] = agent_context.source
        return TaskContextTarget(
            scope=scope,
            project_root=project_root,
            sources=sources,
            research_topic_id=research_topic_id,
            topic_workspace_id=topic_workspace_id,
            worker_kind="agent",
            worker_name=agent_context.agent_name,
            worker_workspace=canonicalize(agent_context.agent_workspace_path),
        )
    return None


def _unresolved_diagnostic(scope: OperationScope, message: str) -> Diagnostic:
    return Diagnostic(
        code="ISO088",
        severity="error",
        concept="Operator Context Preflight",
        field="scope",
        message=message,
    )


def _extend_unique(target: list[Diagnostic], values: list[Diagnostic]) -> None:
    for value in values:
        if value not in target:
            target.append(value)
