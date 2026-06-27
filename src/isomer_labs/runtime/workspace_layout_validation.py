"""Validation helpers for Agent Workspace isomer-managed layout."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from isomer_labs.diagnostics import Diagnostic
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.path_utils import is_within
from isomer_labs.runtime.models import AgentWorkspaceRecord, PathPlanRecord


def workspace_isomer_managed_path(
    workspace: AgentWorkspaceRecord,
    path_plans: Mapping[str, PathPlanRecord],
    workspace_path: Path,
) -> Path:
    if workspace.isomer_managed_path_plan_id is not None:
        plan = path_plans.get(workspace.isomer_managed_path_plan_id)
        if plan is not None:
            return Path(plan.path)
    if workspace.support_root_path is not None and ".isomer-agent" not in Path(workspace.support_root_path).parts:
        return Path(workspace.support_root_path)
    return workspace_path / "isomer-managed"


def missing_isomer_managed_support_paths(isomer_managed_path: Path) -> list[Path]:
    required = (
        "agent-owned/runtime",
        "agent-owned/artifacts",
        "agent-owned/scratch",
        "agent-owned/logs",
        "agent-owned/public",
        "agent-owned/inbox",
        "topic-owned/readonly",
        "topic-owned/writable",
        "links",
    )
    return [isomer_managed_path / relative for relative in required if not (isomer_managed_path / relative).exists()]


def unsafe_generated_link_diagnostics(
    context: EffectiveTopicContext,
    workspace: AgentWorkspaceRecord,
    isomer_managed_path: Path,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    links_root = isomer_managed_path / "links"
    if not links_root.exists():
        return diagnostics
    pending = [links_root]
    while pending:
        current = pending.pop()
        try:
            children = list(current.iterdir())
        except OSError as exc:
            diagnostics.append(
                Diagnostic(
                    code="ISO044",
                    severity="warning",
                    concept="Agent Workspace generated links",
                    path=current,
                    field=workspace.id,
                    message=f"Could not inspect generated links: {exc}.",
                )
            )
            continue
        for child in children:
            if child.is_symlink():
                target = child.resolve(strict=False)
                if not is_within(target, context.topic_workspace_path):
                    diagnostics.append(
                        Diagnostic(
                            code="ISO044",
                            severity="error",
                            concept="Agent Workspace generated links",
                            path=child,
                            field=workspace.id,
                            message=(
                                "Generated `isomer-managed/links/` target points outside the selected "
                                "Topic Workspace without an accepted external-root contract."
                            ),
                        )
                    )
                continue
            if child.is_dir():
                pending.append(child)
    return diagnostics


def is_unpromoted_isomer_managed_dependency(path: Path) -> bool:
    parts = path.parts
    return _contains_parts(parts, ("isomer-managed", "agent-owned")) or _contains_parts(
        parts,
        ("isomer-managed", "topic-owned"),
    )


def _contains_parts(parts: tuple[str, ...], needle: tuple[str, ...]) -> bool:
    if len(parts) < len(needle):
        return False
    return any(parts[index : index + len(needle)] == needle for index in range(len(parts) - len(needle) + 1))
