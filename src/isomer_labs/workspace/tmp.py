"""Local Tmp Surface ignore-policy helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Mapping

from isomer_labs.core.diagnostics import Diagnostic
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.core.path_utils import is_within

if TYPE_CHECKING:
    from isomer_labs.workspace.manifest import EffectiveAgentContext, EffectiveTopicActorContext


@dataclass(frozen=True)
class TmpSurfaceIgnorePolicy:
    label: str
    gitignore_path: Path
    ignored_path: Path
    relative_root: Path
    entry: str

    def to_json(self) -> dict[str, object]:
        return {
            "semantic_label": self.label,
            "gitignore_path": str(self.gitignore_path),
            "ignored_path": str(self.ignored_path),
            "relative_root": str(self.relative_root),
            "entry": self.entry,
        }


def tmp_surface_ignore_policy(
    context: EffectiveTopicContext,
    label: str,
    tmp_path: Path,
    *,
    env: Mapping[str, str],
    agent_context: EffectiveAgentContext | None = None,
    topic_actor_context: EffectiveTopicActorContext | None = None,
) -> tuple[TmpSurfaceIgnorePolicy | None, list[Diagnostic]]:
    diagnostics = _tmp_surface_boundary_diagnostics(context, label, tmp_path, env=env, agent_context=agent_context, topic_actor_context=topic_actor_context)
    if any(diagnostic.is_error for diagnostic in diagnostics):
        return None, diagnostics
    if label == "topic.tmp":
        entry = _gitignore_entry(context.topic_workspace_path, tmp_path)
        if entry is None:
            return None, diagnostics
        return (
            TmpSurfaceIgnorePolicy(label, context.topic_workspace_path / ".gitignore", tmp_path, context.topic_workspace_path, entry),
            diagnostics,
        )
    if label == "topic.repos.main.tmp":
        topic_main, topic_main_diagnostics = _resolve_topic_main(context, env)
        diagnostics.extend(topic_main_diagnostics)
        if topic_main is None or any(diagnostic.is_error for diagnostic in diagnostics):
            return None, diagnostics
        entry = _gitignore_entry(topic_main, tmp_path)
        if entry is None:
            return None, diagnostics
        return TmpSurfaceIgnorePolicy(label, topic_main / ".gitignore", tmp_path, topic_main, entry), diagnostics
    if label == "agent.tmp" and agent_context is not None:
        topic_main, topic_main_diagnostics = _resolve_topic_main(context, env)
        diagnostics.extend(topic_main_diagnostics)
        if topic_main is None or any(diagnostic.is_error for diagnostic in diagnostics):
            return None, diagnostics
        entry = _gitignore_entry(agent_context.agent_workspace_path, tmp_path)
        if entry is None:
            return None, diagnostics
        return (
            TmpSurfaceIgnorePolicy(label, topic_main / ".gitignore", tmp_path, agent_context.agent_workspace_path, entry),
            diagnostics,
        )
    if label == "topic.actors.tmp" and topic_actor_context is not None:
        entry = _gitignore_entry(topic_actor_context.topic_actor_workspace_path, tmp_path)
        if entry is None:
            return None, diagnostics
        return (
            TmpSurfaceIgnorePolicy(label, topic_actor_context.topic_actor_workspace_path / ".gitignore", tmp_path, topic_actor_context.topic_actor_workspace_path, entry),
            diagnostics,
        )
    return None, diagnostics


def ensure_tmp_surface_ignore_policy(
    context: EffectiveTopicContext,
    label: str,
    tmp_path: Path,
    *,
    env: Mapping[str, str],
    agent_context: EffectiveAgentContext | None = None,
    topic_actor_context: EffectiveTopicActorContext | None = None,
) -> list[Diagnostic]:
    policy, diagnostics = tmp_surface_ignore_policy(
        context,
        label,
        tmp_path,
        env=env,
        agent_context=agent_context,
        topic_actor_context=topic_actor_context,
    )
    if policy is None or any(diagnostic.is_error for diagnostic in diagnostics):
        return diagnostics
    policy.gitignore_path.parent.mkdir(parents=True, exist_ok=True)
    existing = policy.gitignore_path.read_text(encoding="utf-8") if policy.gitignore_path.exists() else ""
    entries = {line.strip() for line in existing.splitlines() if line.strip() and not line.lstrip().startswith("#")}
    if policy.entry not in entries:
        prefix = "" if not existing or existing.endswith("\n") else "\n"
        with policy.gitignore_path.open("a", encoding="utf-8") as stream:
            stream.write(f"{prefix}{policy.entry}\n")
    return diagnostics


def _tmp_surface_boundary_diagnostics(
    context: EffectiveTopicContext,
    label: str,
    path: Path,
    *,
    env: Mapping[str, str],
    agent_context: EffectiveAgentContext | None,
    topic_actor_context: EffectiveTopicActorContext | None,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if label == "topic.tmp":
        if not is_within(path, context.topic_workspace_path):
            diagnostics.append(_tmp_boundary_diagnostic(label, "Local Tmp Surface must stay inside the selected Topic Workspace."))
        return diagnostics
    if label == "topic.repos.main.tmp":
        topic_main, topic_main_diagnostics = _resolve_topic_main(context, env)
        diagnostics.extend(topic_main_diagnostics)
        if topic_main is not None and not is_within(path, topic_main):
            diagnostics.append(_tmp_boundary_diagnostic(label, "`topic.repos.main.tmp` must stay inside `topic.repos.main`."))
        return diagnostics
    if label == "agent.tmp" and agent_context is not None and not is_within(path, agent_context.agent_workspace_path):
        diagnostics.append(_tmp_boundary_diagnostic(label, "`agent.tmp` must stay inside the resolved `agent.workspace`."))
    if label == "topic.actors.tmp" and topic_actor_context is not None and not is_within(path, topic_actor_context.topic_actor_workspace_path):
        diagnostics.append(_tmp_boundary_diagnostic(label, "`topic.actors.tmp` must stay inside the resolved `topic.actors.workspace`."))
    return diagnostics


def _resolve_topic_main(context: EffectiveTopicContext, env: Mapping[str, str]) -> tuple[Path | None, list[Diagnostic]]:
    from isomer_labs.workspace.manifest import resolve_semantic_binding

    result, diagnostics = resolve_semantic_binding(context, "topic.repos.main", env=env, agent_context=None)
    return (result.path if result is not None else None), diagnostics


def _tmp_boundary_diagnostic(label: str, message: str) -> Diagnostic:
    return Diagnostic(code="ISO005", severity="error", concept="Workspace Path Resolution", field=label, message=message)


def _gitignore_entry(root: Path, ignored_path: Path) -> str | None:
    try:
        relative = ignored_path.resolve(strict=False).relative_to(root.resolve(strict=False))
    except ValueError:
        return None
    value = relative.as_posix().rstrip("/")
    if value in ("", "."):
        return None
    return f"{value}/"
