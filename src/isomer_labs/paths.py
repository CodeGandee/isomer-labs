"""Workspace Path Resolution preview for Milestone 1."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from isomer_labs.content_layout import (
    content_root_path as default_content_root_path,
    topic_workspace_base_path as default_topic_workspace_base_path,
)
from isomer_labs.diagnostics import Diagnostic
from isomer_labs.models import EffectiveTopicContext, ResolvedPathEntry
from isomer_labs.path_utils import is_within, resolve_project_path
from isomer_labs.project import root_houmao_overlay_dir_for_root


PATH_ENV_VARS = {
    "isomer_content_root": "ISOMER_CONTENT_ROOT_DIR",
    "topic_workspace_base": "ISOMER_TOPIC_WORKSPACE_BASE_DIR",
    "topic_workspace": "ISOMER_CURRENT_TOPIC_WORKSPACE_DIR",
    "workspace_runtime_db": "ISOMER_TOPIC_WORKSPACE_RUNTIME_DB",
    "artifacts": "ISOMER_TOPIC_WORKSPACE_ARTIFACTS_DIR",
    "tasks": "ISOMER_TOPIC_WORKSPACE_TASKS_DIR",
    "runs": "ISOMER_TOPIC_WORKSPACE_RUNS_DIR",
    "views": "ISOMER_TOPIC_WORKSPACE_VIEWS_DIR",
    "logs": "ISOMER_TOPIC_WORKSPACE_LOGS_DIR",
    "agent_workspace": "ISOMER_AGENT_WORKSPACE_DIR",
    "agent_runtime": "ISOMER_AGENT_WORKSPACE_RUNTIME_DIR",
    "agent_artifacts": "ISOMER_AGENT_WORKSPACE_ARTIFACTS_DIR",
    "agent_scratch": "ISOMER_AGENT_WORKSPACE_SCRATCH_DIR",
    "agent_logs": "ISOMER_AGENT_WORKSPACE_LOGS_DIR",
}
MANIFEST_PATH_KEYS = {
    "isomer_content_root": ("isomer_content_root",),
    "topic_workspace_base": ("topic_workspace_base_dir",),
    "topic_workspace": ("current_topic_workspace_dir", "topic_workspace_dir"),
    "workspace_runtime_db": ("topic_workspace_runtime_db", "state_sqlite"),
    "artifacts": ("topic_workspace_artifacts_dir", "artifacts_dir"),
    "tasks": ("topic_workspace_tasks_dir", "tasks_dir"),
    "runs": ("topic_workspace_runs_dir", "runs_dir"),
    "views": ("topic_workspace_views_dir", "views_dir"),
    "logs": ("topic_workspace_logs_dir", "logs_dir"),
}
ARTIFACT_CLASS_DIRS = (
    "intake",
    "baselines",
    "experiments",
    "analysis",
    "figures",
    "paper",
    "decisions",
    "evidence",
    "findings",
    "handoffs",
)


def preview_paths(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
) -> tuple[list[ResolvedPathEntry], list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    project_root = context.project.root
    content_root = _select_path(
        context,
        env,
        "isomer_content_root",
        default=default_content_root_path(project_root, context.project.manifest.path_defaults),
    )
    topic_workspace_base_source = "Project Manifest" if _manifest_value(context, "isomer_content_root") is not None else "default"
    topic_workspace_path = _select_path(
        context,
        env,
        "topic_workspace",
        default=context.topic_workspace_path,
        manifest_value=context.topic_workspace_path_input,
        manifest_source="Project Manifest" if context.topic_workspace_path_input is not None else None,
        default_source=context.sources.get("topic_workspace_path", "default"),
    )
    entries = [
        ResolvedPathEntry("project_root", project_root, context.project.discovery_source),
        ResolvedPathEntry("project_config_directory", context.project.config_dir, context.project.discovery_source),
        ResolvedPathEntry("project_manifest", context.project.manifest_path, context.project.discovery_source),
        content_root,
        _select_path(
            context,
            env,
            "topic_workspace_base",
            default=default_topic_workspace_base_path(project_root, context.project.manifest.path_defaults),
            default_source=topic_workspace_base_source,
        ),
        topic_workspace_path,
        _select_path(
            context,
            env,
            "workspace_runtime_db",
            default=topic_workspace_path.path / "state.sqlite",
        ),
        _select_path(context, env, "artifacts", default=topic_workspace_path.path / "artifacts"),
        ResolvedPathEntry("agents", topic_workspace_path.path / "agents", "default"),
        _select_path(context, env, "tasks", default=topic_workspace_path.path / "tasks"),
        _select_path(context, env, "runs", default=topic_workspace_path.path / "runs"),
        _select_path(context, env, "views", default=topic_workspace_path.path / "views"),
        _select_path(context, env, "logs", default=topic_workspace_path.path / "logs"),
    ]

    run_id = context.lifecycle_refs.get("run_id")
    if run_id is not None:
        run_root = next(entry.path for entry in entries if entry.surface == "runs") / run_id
        entries.extend(
            [
                ResolvedPathEntry("run", run_root, "default"),
                ResolvedPathEntry("run_prompts", run_root / "prompts", "default"),
                ResolvedPathEntry("run_tool_calls", run_root / "tool-calls", "default"),
                ResolvedPathEntry("run_logs", run_root / "logs", "default"),
                ResolvedPathEntry("run_outputs", run_root / "outputs", "default"),
            ]
        )

    agent_id = context.lifecycle_refs.get("agent_instance_id")
    if agent_id is not None or any(env.get(PATH_ENV_VARS[surface]) for surface in _agent_surfaces()):
        agent_root = _select_path(
            context,
            env,
            "agent_workspace",
            default=topic_workspace_path.path / "agents" / (agent_id or "agent-instance"),
        )
        entries.extend(
            [
                agent_root,
                _select_path(context, env, "agent_runtime", default=agent_root.path / "runtime"),
                _select_path(context, env, "agent_artifacts", default=agent_root.path / "artifacts"),
                _select_path(context, env, "agent_scratch", default=agent_root.path / "scratch"),
                _select_path(context, env, "agent_logs", default=agent_root.path / "logs"),
            ]
        )

    artifact_root = next(entry.path for entry in entries if entry.surface == "artifacts")
    for artifact_class in ARTIFACT_CLASS_DIRS:
        entries.append(ResolvedPathEntry(f"artifact_{artifact_class}", artifact_root / artifact_class, "default"))

    canonical_entries: list[ResolvedPathEntry] = []
    for entry in entries:
        path = entry.path.resolve(strict=False)
        if not is_within(path, project_root):
            diagnostics.append(
                Diagnostic(
                    code="ISO005",
                    severity="error",
                    concept="Workspace Path Resolution",
                    field=entry.surface,
                    message="Resolved path points outside the Project root.",
                )
            )
            continue
        if entry.surface == "isomer_content_root" and is_within(path, context.project.config_dir):
            diagnostics.append(
                Diagnostic(
                    code="ISO005",
                    severity="error",
                    concept="Workspace Path Resolution",
                    field=entry.surface,
                    message="Project generated content root must not live inside the Project Config Directory.",
                )
            )
            continue
        if entry.surface == "isomer_content_root" and is_within(path, root_houmao_overlay_dir_for_root(project_root)):
            diagnostics.append(
                Diagnostic(
                    code="ISO005",
                    severity="error",
                    concept="Workspace Path Resolution",
                    field=entry.surface,
                    message="Project generated content root must not collide with root .houmao external Houmao state.",
                )
            )
            continue
        canonical_entries.append(
            ResolvedPathEntry(
                surface=entry.surface,
                path=path,
                source=entry.source,
                source_detail=entry.source_detail,
            )
        )
    return canonical_entries, diagnostics


def _select_path(
    context: EffectiveTopicContext,
    env: Mapping[str, str],
    surface: str,
    *,
    default: Path,
    manifest_value: str | None = None,
    manifest_source: str | None = None,
    default_source: str = "default",
) -> ResolvedPathEntry:
    env_var = PATH_ENV_VARS.get(surface)
    if env_var is not None and env.get(env_var):
        return ResolvedPathEntry(
            surface=surface,
            path=resolve_project_path(context.project.root, env[env_var]),
            source="env",
            source_detail=env_var,
        )
    manifest_candidate = manifest_value or _manifest_value(context, surface)
    if manifest_candidate is not None:
        return ResolvedPathEntry(
            surface=surface,
            path=resolve_project_path(context.project.root, manifest_candidate),
            source=manifest_source or "manifest",
        )
    return ResolvedPathEntry(surface=surface, path=default, source=default_source)


def _manifest_value(context: EffectiveTopicContext, surface: str) -> str | None:
    keys = MANIFEST_PATH_KEYS.get(surface, ())
    for key in keys:
        value = context.project.manifest.path_defaults.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def _agent_surfaces() -> tuple[str, ...]:
    return ("agent_workspace", "agent_runtime", "agent_artifacts", "agent_scratch", "agent_logs")
