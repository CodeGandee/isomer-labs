"""Topic Workspace visibility layout validation."""

from __future__ import annotations

from typing import Mapping

from isomer_labs.diagnostics import Diagnostic
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.paths import preview_paths


def validate_topic_workspace_visibility_layout(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    current_entries, path_diagnostics = preview_paths(context, env=env)
    diagnostics.extend(path_diagnostics)
    current_by_surface = {entry.surface: entry for entry in current_entries}
    required_surfaces = (
        "topic_main_repo",
        "agents",
        "records_artifacts",
        "records_tasks",
        "records_runs",
        "records_views",
        "records_logs",
        "runtime",
    )
    for surface in required_surfaces:
        entry = current_by_surface.get(surface)
        if entry is not None and not entry.path.exists():
            diagnostics.append(
                Diagnostic(
                    code="ISO042",
                    severity="warning",
                    concept="Topic Workspace visibility layout",
                    path=entry.path,
                    field=surface,
                    message="Standard Topic Workspace visibility path is missing.",
                )
            )

    for legacy_name in ("shared", "artifacts", "tasks", "runs", "views", "logs"):
        legacy_path = context.topic_workspace_path / legacy_name
        if legacy_path.exists():
            diagnostics.append(
                Diagnostic(
                    code="ISO042",
                    severity="warning",
                    concept="Topic Workspace visibility layout",
                    path=legacy_path,
                    field=legacy_name,
                    message=(
                        "Legacy root collaboration directory exists. Move worker-visible material into "
                        "`repos/topic-main` or owner-preserved material into `records/*` through explicit operator action."
                    ),
                )
            )
    return diagnostics
