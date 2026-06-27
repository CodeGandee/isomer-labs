"""Workspace Path Resolution for topic and semantic workspace surfaces."""

from __future__ import annotations

from pathlib import Path
import sqlite3
from typing import Mapping

from isomer_labs.content_layout import (
    content_root_path as default_content_root_path,
    topic_workspace_base_path as default_topic_workspace_base_path,
    topic_workspace_path as default_topic_workspace_path,
)
from isomer_labs.diagnostics import Diagnostic
from isomer_labs.local_tmp_surfaces import ensure_tmp_surface_ignore_policy
from isomer_labs.models import EffectiveTopicContext, ResolvedPathEntry
from isomer_labs.path_utils import canonicalize, is_within, resolve_project_path
from isomer_labs.project import root_houmao_overlay_dir_for_root
from isomer_labs.semantic_surfaces import SemanticSurface, storage_profile_by_id
from isomer_labs.topic_workspace_manifest import (
    DEFAULT_PROFILE_SOURCE,
    PATH_PLAN_SOURCE,
    EffectiveAgentContext,
    SemanticPathResult,
    catalog,
    compatibility_aliases,
    compatibility_surface_for_label,
    default_path_for_label,
    effective_catalog,
    load_topic_workspace_manifest,
    match_agent_name_from_template,
    materialize_default_manifest,
    resolve_binding_path,
    resolve_semantic_binding,
    surface_for_label,
)


PATH_ENV_VARS = {
    "isomer_content_root": "ISOMER_CONTENT_ROOT_DIR",
    "topic_workspace_base": "ISOMER_TOPIC_WORKSPACE_BASE_DIR",
    "topic_workspace": "ISOMER_CURRENT_TOPIC_WORKSPACE_DIR",
    "workspace_runtime_db": "ISOMER_TOPIC_WORKSPACE_RUNTIME_DB",
    "topic_tmp": "ISOMER_TOPIC_WORKSPACE_TMP_DIR",
    "topic_main_repo": "ISOMER_TOPIC_MAIN_REPO_DIR",
    "topic_main_tmp": "ISOMER_TOPIC_MAIN_TMP_DIR",
    "topic_main_isomer_managed": "ISOMER_TOPIC_MAIN_ISOMER_MANAGED_DIR",
    "topic_main_tracked": "ISOMER_TOPIC_MAIN_TRACKED_DIR",
    "records": "ISOMER_TOPIC_WORKSPACE_RECORDS_DIR",
    "records_artifacts": "ISOMER_TOPIC_WORKSPACE_ARTIFACTS_DIR",
    "records_tasks": "ISOMER_TOPIC_WORKSPACE_TASKS_DIR",
    "records_runs": "ISOMER_TOPIC_WORKSPACE_RUNS_DIR",
    "records_views": "ISOMER_TOPIC_WORKSPACE_VIEWS_DIR",
    "records_logs": "ISOMER_TOPIC_WORKSPACE_LOGS_DIR",
    "runtime": "ISOMER_TOPIC_WORKSPACE_RUNTIME_DIR",
    "agent_workspace": "ISOMER_AGENT_WORKSPACE_DIR",
    "agent_tmp": "ISOMER_AGENT_WORKSPACE_TMP_DIR",
    "agent_isomer_managed": "ISOMER_AGENT_ISOMER_MANAGED_DIR",
    "agent_owned": "ISOMER_AGENT_OWNED_DIR",
    "agent_runtime": "ISOMER_AGENT_WORKSPACE_RUNTIME_DIR",
    "agent_artifacts": "ISOMER_AGENT_WORKSPACE_ARTIFACTS_DIR",
    "agent_scratch": "ISOMER_AGENT_WORKSPACE_SCRATCH_DIR",
    "agent_logs": "ISOMER_AGENT_WORKSPACE_LOGS_DIR",
    "agent_topic_owned": "ISOMER_AGENT_TOPIC_OWNED_DIR",
    "agent_links": "ISOMER_AGENT_LINKS_DIR",
}
MANIFEST_PATH_KEYS = {
    "isomer_content_root": ("isomer_content_root",),
    "topic_workspace_base": ("topic_workspace_base_dir",),
    "topic_workspace": ("current_topic_workspace_dir", "topic_workspace_dir"),
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
LEGACY_RECORD_ENV_SURFACES = frozenset(
    {
        "records_artifacts",
        "records_tasks",
        "records_runs",
        "records_views",
        "records_logs",
    }
)
LEGACY_AGENT_ENV_SURFACES = frozenset(
    {
        "agent_runtime",
        "agent_artifacts",
        "agent_scratch",
        "agent_logs",
    }
)
TOPIC_LABELS = (
    "topic.runtime.db",
    "topic.tmp",
    "topic.repos.main",
    "topic.repos.main.tmp",
    "topic.repos.main.isomer_managed",
    "topic.repos.main.tracked",
    "topic.repos.main.tracked.shared",
    "topic.repos.main.tracked.artifacts",
    "topic.repos.main.tracked.tasks",
    "topic.repos.main.tracked.runs",
    "topic.repos.main.tracked.views",
    "topic.repos.main.tracked.tools",
    "topic.repos.main.tracked.boundaries",
    "topic.repos.main.tracked.manifests",
    "topic.agents_root",
    "topic.records",
    "topic.records.artifacts",
    "topic.records.tasks",
    "topic.records.runs",
    "topic.records.views",
    "topic.records.logs",
    "topic.runtime",
)
AGENT_LABELS = (
    "agent.workspace",
    "agent.tmp",
    "agent.isomer_managed",
    "agent.owned",
    "agent.runtime",
    "agent.private_artifacts",
    "agent.scratch",
    "agent.logs",
    "agent.public_share",
    "agent.inbox",
    "agent.topic_owned",
    "agent.topic_readonly",
    "agent.topic_writable",
    "agent.links",
)


def preview_paths(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
) -> tuple[list[ResolvedPathEntry], list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    project_root = context.project.root
    content_root = _select_project_path(
        context,
        env,
        "isomer_content_root",
        default=default_content_root_path(project_root, context.project.manifest.path_defaults),
    )
    topic_workspace_base_source = (
        "Project Manifest" if _manifest_value(context, "isomer_content_root") is not None else "default"
    )
    topic_workspace_path = _select_project_path(
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
        _select_project_path(
            context,
            env,
            "topic_workspace_base",
            default=default_topic_workspace_base_path(project_root, context.project.manifest.path_defaults),
            default_source=topic_workspace_base_source,
        ),
        _with_semantic(topic_workspace_path, "topic.workspace", f"topic_workspace:{context.topic_workspace_id}"),
        ResolvedPathEntry("repos", topic_workspace_path.path / "repos", DEFAULT_PROFILE_SOURCE),
    ]

    for label in TOPIC_LABELS:
        entry, label_diagnostics = _entry_for_label(context, label, env=env, agent_context=None, use_path_plan=False)
        diagnostics.extend(label_diagnostics)
        if entry is not None:
            entries.append(entry)

    run_id = context.lifecycle_refs.get("run_id")
    if run_id is not None:
        records_runs = next(entry.path for entry in entries if entry.surface == "records_runs")
        run_root = records_runs / run_id
        entries.extend(
            [
                ResolvedPathEntry("run", run_root, DEFAULT_PROFILE_SOURCE),
                ResolvedPathEntry("run_prompts", run_root / "prompts", DEFAULT_PROFILE_SOURCE),
                ResolvedPathEntry("run_tool_calls", run_root / "tool-calls", DEFAULT_PROFILE_SOURCE),
                ResolvedPathEntry("run_logs", run_root / "logs", DEFAULT_PROFILE_SOURCE),
                ResolvedPathEntry("run_outputs", run_root / "outputs", DEFAULT_PROFILE_SOURCE),
            ]
        )

    agent_context, agent_diagnostics = _agent_context_from_refs(context, env)
    diagnostics.extend(agent_diagnostics)
    if agent_context is not None:
        for label in AGENT_LABELS:
            entry, label_diagnostics = _entry_for_label(context, label, env=env, agent_context=agent_context, use_path_plan=False)
            diagnostics.extend(label_diagnostics)
            if entry is not None:
                entries.append(entry)

    artifact_entry = next((entry for entry in entries if entry.surface == "records_artifacts"), None)
    if artifact_entry is not None:
        for artifact_class in ARTIFACT_CLASS_DIRS:
            entries.append(ResolvedPathEntry(f"artifact_{artifact_class}", artifact_entry.path / artifact_class, DEFAULT_PROFILE_SOURCE))

    canonical_entries: list[ResolvedPathEntry] = []
    for entry in entries:
        path = entry.path.resolve(strict=False)
        diagnostics.extend(_legacy_env_diagnostics(entry))
        diagnostics.extend(_project_path_safety_diagnostics(context, entry.surface, path))
        if any(diagnostic.is_error and diagnostic.field == entry.surface for diagnostic in diagnostics):
            continue
        canonical_entries.append(
            ResolvedPathEntry(
                surface=entry.surface,
                path=path,
                source=entry.source,
                source_detail=entry.source_detail,
                semantic_label=entry.semantic_label,
                scope_ref=entry.scope_ref,
                compatibility_surface=entry.compatibility_surface,
                storage_profile=entry.storage_profile,
                storage_profile_traits=entry.storage_profile_traits,
                owner=entry.owner,
                durability=entry.durability,
                sharing=entry.sharing,
                path_kind=entry.path_kind,
                path_exists=path.exists(),
            )
        )
    return canonical_entries, diagnostics


def resolve_semantic_path(
    context: EffectiveTopicContext,
    label_or_surface: str,
    *,
    env: Mapping[str, str],
    cwd: Path,
    agent_name: str | None = None,
    agent_instance_id: str | None = None,
    use_path_plan: bool = True,
) -> tuple[SemanticPathResult | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    label = _normalize_label(label_or_surface)
    surface, surface_diagnostics = surface_for_label(context, label)
    diagnostics.extend(surface_diagnostics)
    if surface is None:
        diagnostics.append(
            Diagnostic(
                code="ISO061",
                severity="error",
                concept="Workspace Path Resolution",
                field=label_or_surface,
                message="Unknown semantic surface label.",
            )
        )
        return None, diagnostics
    agent_context = None
    if surface.scope == "agent":
        agent_context, agent_diagnostics = resolve_effective_agent_context(
            context,
            env=env,
            cwd=cwd,
            explicit_agent_name=agent_name,
            explicit_agent_instance_id=agent_instance_id,
        )
        diagnostics.extend(agent_diagnostics)
        if agent_context is None:
            return None, diagnostics
    if use_path_plan:
        plan = _path_plan_result(context, label, env=env, agent_context=agent_context)
        if plan is not None:
            return plan, diagnostics
    result, binding_diagnostics = resolve_semantic_binding(
        context,
        label,
        env=env,
        agent_context=agent_context,
    )
    diagnostics.extend(binding_diagnostics)
    return result, diagnostics


def list_semantic_paths(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    cwd: Path,
    agent_name: str | None = None,
    agent_instance_id: str | None = None,
) -> tuple[list[dict[str, object]], list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    agent_context, agent_diagnostics = resolve_effective_agent_context(
        context,
        env=env,
        cwd=cwd,
        explicit_agent_name=agent_name,
        explicit_agent_instance_id=agent_instance_id,
        missing_is_error=False,
    )
    diagnostics.extend(agent_diagnostics)
    surfaces, catalog_diagnostics = effective_catalog(context)
    diagnostics.extend(catalog_diagnostics)
    rows: list[dict[str, object]] = []
    for surface in sorted(surfaces.values(), key=lambda item: item.label):
        if surface.scope == "agent" and agent_context is None:
            rows.append(
                {
                    "semantic_label": surface.label,
                    "scope": surface.scope,
                    "required_context": surface.required_context,
                    "resolved": False,
                    "diagnostics": ["Agent-scoped label requires Agent Name or Agent Instance context."],
                }
            )
            continue
        result, result_diagnostics = resolve_semantic_path(
            context,
            surface.label,
            env=env,
            cwd=cwd,
            agent_name=agent_context.agent_name if agent_context is not None and surface.scope == "agent" else None,
            agent_instance_id=agent_context.agent_instance_id if agent_context is not None and surface.scope == "agent" else None,
        )
        non_blocking = [diagnostic.render() for diagnostic in result_diagnostics]
        if result is None:
            rows.append(
                {
                    "semantic_label": surface.label,
                    "scope": surface.scope,
                    "required_context": surface.required_context,
                    "resolved": False,
                    "diagnostics": non_blocking,
                }
            )
            continue
        item = result.to_json()
        item["resolved"] = True
        if non_blocking:
            item["diagnostics"] = non_blocking
        rows.append(item)
    return rows, diagnostics


def materialize_default_paths(
    context: EffectiveTopicContext,
    *,
    labels: tuple[str, ...],
    agent_name: str | None,
) -> tuple[dict[str, object] | None, list[Diagnostic]]:
    manifest, created, diagnostics = materialize_default_manifest(context, labels=labels, agent_name=agent_name)
    if manifest is None:
        return None, diagnostics
    return {
        "manifest": manifest.to_json(),
        "created_paths": [str(path.resolve(strict=False)) for path in created],
    }, diagnostics


def default_semantic_path(
    context: EffectiveTopicContext,
    label_or_surface: str,
    *,
    agent_name: str | None = None,
) -> tuple[dict[str, object] | None, list[Diagnostic]]:
    label = _normalize_label(label_or_surface)
    surface = catalog().get(label)
    diagnostics: list[Diagnostic] = []
    if surface is None:
        diagnostics.append(
            Diagnostic(
                code="ISO061",
                severity="error",
                concept="Workspace Path Resolution",
                field=label_or_surface,
                message="Only built-in reserved semantic labels have default-layout paths.",
            )
        )
        return None, diagnostics
    if surface.scope == "agent" and agent_name is None:
        diagnostics.append(
            Diagnostic(
                code="ISO061",
                severity="error",
                concept="Effective Agent Context",
                field=label,
                message="Default path query for agent-scoped labels requires an Agent Name selector.",
            )
        )
        return None, diagnostics
    path = default_path_for_label(context, label, agent_name=agent_name)
    profile = storage_profile_by_id(surface.storage_profile)
    return (
        {
            "semantic_label": label,
            "path": str(path.resolve(strict=False)),
            "source": DEFAULT_PROFILE_SOURCE,
            "source_detail": DEFAULT_PROFILE_SOURCE,
            "storage_profile": surface.storage_profile,
            "storage_profile_traits": profile.to_json() if profile is not None else None,
            "path_kind": surface.path_kind,
            "exists": path.exists(),
        },
        diagnostics,
    )


def materialize_semantic_path(
    context: EffectiveTopicContext,
    label_or_surface: str,
    *,
    env: Mapping[str, str],
    cwd: Path,
    agent_name: str | None = None,
    agent_instance_id: str | None = None,
) -> tuple[dict[str, object] | None, list[Diagnostic]]:
    result, diagnostics = resolve_semantic_path(
        context,
        label_or_surface,
        env=env,
        cwd=cwd,
        agent_name=agent_name,
        agent_instance_id=agent_instance_id,
        use_path_plan=False,
    )
    if result is None or any(diagnostic.is_error for diagnostic in diagnostics):
        return None, diagnostics
    created: list[Path] = []
    if result.catalog.path_kind == "file":
        result.path.parent.mkdir(parents=True, exist_ok=True)
        created.append(result.path.parent)
    else:
        result.path.mkdir(parents=True, exist_ok=True)
        created.append(result.path)
    if result.label in ("topic.tmp", "topic.repos.main.tmp", "agent.tmp"):
        diagnostics.extend(_ensure_materialized_tmp_policy(context, result, env=env))
    return {
        "path": result.to_json(),
        "created_paths": [str(path.resolve(strict=False)) for path in created],
    }, diagnostics


def explain_semantic_path(
    context: EffectiveTopicContext,
    label_or_surface: str,
    *,
    env: Mapping[str, str],
    cwd: Path,
    agent_name: str | None = None,
    agent_instance_id: str | None = None,
) -> tuple[dict[str, object] | None, list[Diagnostic]]:
    recorded, recorded_diagnostics = resolve_semantic_path(
        context,
        label_or_surface,
        env=env,
        cwd=cwd,
        agent_name=agent_name,
        agent_instance_id=agent_instance_id,
        use_path_plan=True,
    )
    configured, configured_diagnostics = resolve_semantic_path(
        context,
        label_or_surface,
        env=env,
        cwd=cwd,
        agent_name=agent_name,
        agent_instance_id=agent_instance_id,
        use_path_plan=False,
    )
    diagnostics = [*recorded_diagnostics, *configured_diagnostics]
    if recorded is None and configured is None:
        return None, diagnostics
    selected = recorded or configured
    candidates: list[dict[str, object]] = []
    if recorded is not None:
        candidates.append({"mode": "recorded", **recorded.to_json()})
    if configured is not None:
        candidates.append({"mode": "configured", **configured.to_json()})
    return {
        "semantic_label": selected.label if selected is not None else _normalize_label(label_or_surface),
        "selected_mode": "recorded" if recorded is not None and recorded.source == PATH_PLAN_SOURCE else "configured",
        "selected": selected.to_json() if selected is not None else None,
        "candidates": candidates,
    }, diagnostics


def resolve_effective_agent_context(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    cwd: Path,
    explicit_agent_name: str | None = None,
    explicit_agent_instance_id: str | None = None,
    missing_is_error: bool = True,
) -> tuple[EffectiveAgentContext | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    if explicit_agent_name is not None:
        agent_context, agent_diagnostics = _agent_context_for_name(context, explicit_agent_name, "explicit selector")
        diagnostics.extend(agent_diagnostics)
        return agent_context, diagnostics
    if explicit_agent_instance_id is not None:
        runtime_context = _agent_context_from_runtime_instance(context, explicit_agent_instance_id, env=env)
        if runtime_context is not None:
            return runtime_context, diagnostics
        diagnostics.append(
            Diagnostic(
                code="ISO061",
                severity="error",
                concept="Effective Agent Context",
                field="agent_instance_id",
                message="Selected Agent Instance does not have a Workspace Runtime Agent Workspace record.",
            )
        )
        return None, diagnostics

    env_agent_name = env.get("ISOMER_AGENT_NAME") or env.get("ISOMER_AGENT_WORKSPACE_NAME")
    env_agent_instance_id = env.get("ISOMER_AGENT_INSTANCE_ID")
    env_agent_workspace = env.get("ISOMER_AGENT_WORKSPACE_DIR")
    env_context = None
    if env_agent_name:
        env_context, _ = _agent_context_for_name(context, env_agent_name, "environment")
    elif env_agent_instance_id:
        env_context = _agent_context_from_runtime_instance(context, env_agent_instance_id, env=env)
    elif env_agent_workspace:
        workspace_path = resolve_project_path(context.project.root, env_agent_workspace)
        env_context = EffectiveAgentContext(
            agent_name=workspace_path.name,
            agent_workspace_path=workspace_path,
            source="environment",
            agent_instance_id=None,
        )

    cwd_context, cwd_diagnostics = _agent_context_from_cwd(context, cwd, env=env)
    diagnostics.extend(cwd_diagnostics)
    if env_context is not None:
        if cwd_context is not None and cwd_context.agent_name != env_context.agent_name:
            diagnostics.append(
                Diagnostic(
                    code="ISO061",
                    severity="error",
                    concept="Effective Agent Context",
                    field="agent_name",
                    message="Environment agent context conflicts with cwd-derived Agent Workspace context.",
                )
            )
            return None, diagnostics
        return env_context, diagnostics
    if cwd_context is not None:
        return cwd_context, diagnostics

    lifecycle_agent_name = context.lifecycle_refs.get("agent_name")
    lifecycle_agent_instance_id = context.lifecycle_refs.get("agent_instance_id")
    if lifecycle_agent_name is not None:
        return _agent_context_for_name(context, lifecycle_agent_name, "recorded context")
    if lifecycle_agent_instance_id is not None:
        runtime_context = _agent_context_from_runtime_instance(context, lifecycle_agent_instance_id, env=env)
        if runtime_context is not None:
            return runtime_context, diagnostics

    if missing_is_error:
        diagnostics.append(
            Diagnostic(
                code="ISO061",
                severity="error",
                concept="Effective Agent Context",
                message="Agent-scoped command requires an Agent Name or Agent Instance selector.",
            )
        )
    return None, diagnostics


def _entry_for_label(
    context: EffectiveTopicContext,
    label: str,
    *,
    env: Mapping[str, str],
    agent_context: EffectiveAgentContext | None,
    use_path_plan: bool,
) -> tuple[ResolvedPathEntry | None, list[Diagnostic]]:
    result, diagnostics = resolve_semantic_binding(context, label, env=env, agent_context=agent_context)
    if use_path_plan:
        plan = _path_plan_result(context, label, env=env, agent_context=agent_context)
        if plan is not None:
            result = plan
    if result is None:
        return None, diagnostics
    return _entry_from_result(result), diagnostics


def _ensure_materialized_tmp_policy(
    context: EffectiveTopicContext,
    result: SemanticPathResult,
    *,
    env: Mapping[str, str],
) -> list[Diagnostic]:
    agent_context = None
    if result.agent_name is not None:
        agent_context = EffectiveAgentContext(
            agent_name=result.agent_name,
            agent_workspace_path=result.path.parent if result.label == "agent.tmp" else result.path,
            source=result.agent_context_source or "materialize",
            agent_instance_id=result.agent_instance_id,
        )
    return ensure_tmp_surface_ignore_policy(context, result.label, result.path, env=env, agent_context=agent_context)


def _entry_from_result(result: SemanticPathResult) -> ResolvedPathEntry:
    profile = storage_profile_by_id(result.catalog.storage_profile)
    return ResolvedPathEntry(
        surface=result.catalog.compatibility_surface,
        path=result.path,
        source=result.source,
        source_detail=result.source_detail,
        semantic_label=result.label,
        scope_ref=result.scope_ref,
        compatibility_surface=result.compatibility_surface,
        storage_profile=result.catalog.storage_profile,
        storage_profile_traits=profile.to_json() if profile is not None else None,
        owner=result.catalog.owner,
        durability=result.catalog.durability,
        sharing=result.catalog.sharing,
        path_kind=result.catalog.path_kind,
        path_exists=result.exists,
    )


def _with_semantic(entry: ResolvedPathEntry, label: str, scope_ref: str) -> ResolvedPathEntry:
    return ResolvedPathEntry(
        surface=entry.surface,
        path=entry.path,
        source=entry.source,
        source_detail=entry.source_detail,
        semantic_label=label,
        scope_ref=scope_ref,
        compatibility_surface=entry.surface,
        path_kind="directory",
        path_exists=entry.path.exists(),
    )


def _runtime_db_lookup_path(context: EffectiveTopicContext, *, env: Mapping[str, str]) -> Path:
    result, _ = resolve_semantic_binding(context, "topic.runtime.db", env=env, agent_context=None)
    if result is not None:
        return result.path
    return default_path_for_label(context, "topic.runtime.db", agent_name=None)


def _topic_main_lookup_path(context: EffectiveTopicContext, *, env: Mapping[str, str]) -> Path:
    result, _ = resolve_semantic_binding(context, "topic.repos.main", env=env, agent_context=None)
    if result is not None:
        return result.path
    return default_path_for_label(context, "topic.repos.main", agent_name=None)


def _path_plan_result(
    context: EffectiveTopicContext,
    label: str,
    *,
    env: Mapping[str, str],
    agent_context: EffectiveAgentContext | None,
) -> SemanticPathResult | None:
    runtime_db = _runtime_db_lookup_path(context, env=env)
    if not runtime_db.exists():
        return None
    surface, _ = surface_for_label(context, label)
    if surface is None:
        return None
    scope_ref = f"topic_workspace:{context.topic_workspace_id}"
    agent_name = None
    agent_instance_id = None
    agent_source = None
    if surface.scope == "agent":
        if agent_context is None:
            return None
        scope_ref = agent_context.scope_ref
        agent_name = agent_context.agent_name
        agent_instance_id = agent_context.agent_instance_id
        agent_source = agent_context.source
    compatibility_surface = compatibility_surface_for_label(label, agent_name=agent_name)
    try:
        with sqlite3.connect(runtime_db) as connection:
            connection.row_factory = sqlite3.Row
            if _table_has_column(connection, "path_plans", "semantic_label"):
                row = connection.execute(
                    """
                    SELECT * FROM path_plans
                    WHERE topic_workspace_id = ?
                    AND semantic_label = ?
                    AND (scope_ref = ? OR scope_ref IS NULL)
                    ORDER BY created_at DESC, id
                    LIMIT 1
                    """,
                    (context.topic_workspace_id, label, scope_ref),
                ).fetchone()
                if row is not None:
                    return _semantic_result_from_plan(context, row, label, surface, scope_ref, agent_name, agent_instance_id, agent_source)
            if compatibility_surface is not None:
                row = connection.execute(
                    """
                    SELECT * FROM path_plans
                    WHERE topic_workspace_id = ? AND surface = ?
                    LIMIT 1
                    """,
                    (context.topic_workspace_id, compatibility_surface),
                ).fetchone()
                if row is not None:
                    return _semantic_result_from_plan(context, row, label, surface, scope_ref, agent_name, agent_instance_id, agent_source)
    except sqlite3.Error:
        return None
    return None


def _semantic_result_from_plan(
    context: EffectiveTopicContext,
    row: sqlite3.Row,
    label: str,
    surface: SemanticSurface,
    scope_ref: str,
    agent_name: str | None,
    agent_instance_id: str | None,
    agent_source: str | None,
) -> SemanticPathResult:
    compatibility_surface = row["surface"]
    return SemanticPathResult(
        label=label,
        path=Path(row["path"]).resolve(strict=False),
        source=PATH_PLAN_SOURCE,
        source_detail=row["id"],
        catalog=surface,
        scope_ref=row["scope_ref"] if _row_has_key(row, "scope_ref") and row["scope_ref"] else scope_ref,
        compatibility_surface=compatibility_surface,
        exists=Path(row["path"]).exists(),
        agent_name=agent_name,
        agent_instance_id=agent_instance_id,
        agent_context_source=agent_source,
    )


def _agent_context_from_refs(
    context: EffectiveTopicContext,
    env: Mapping[str, str],
) -> tuple[EffectiveAgentContext | None, list[Diagnostic]]:
    agent_name = context.lifecycle_refs.get("agent_name") or env.get("ISOMER_AGENT_NAME")
    if agent_name is not None:
        return _agent_context_for_name(context, agent_name, "recorded context")
    workspace_value = env.get(PATH_ENV_VARS["agent_workspace"])
    if workspace_value:
        workspace_path = resolve_project_path(context.project.root, workspace_value)
        return (
            EffectiveAgentContext(
                agent_name=workspace_path.name,
                agent_workspace_path=workspace_path,
                source="env",
            ),
            [],
        )
    agent_id = context.lifecycle_refs.get("agent_instance_id")
    if agent_id is not None:
        return (
            None,
            [
                Diagnostic(
                    code="ISO005",
                    severity="error",
                    concept="Workspace Path Resolution",
                    field="agent_name",
                    message=(
                        "Agent Workspace preview is missing a topic-local agent_name; "
                        "provide an approved Agent Workspace plan instead of deriving a path from Agent Instance id."
                    ),
                )
            ],
        )
    return None, []


def _agent_context_for_name(
    context: EffectiveTopicContext,
    agent_name: str,
    source: str,
) -> tuple[EffectiveAgentContext, list[Diagnostic]]:
    workspace_path = default_path_for_label(context, "agent.workspace", agent_name=agent_name)
    manifest, diagnostics = load_topic_workspace_manifest(context)
    binding = manifest.binding_for("agent.workspace")
    if binding is not None:
        workspace_path = resolve_binding_path(context, binding, agent_name=agent_name)
    return (
        EffectiveAgentContext(
            agent_name=agent_name,
            agent_workspace_path=workspace_path,
            source=source,
        ),
        diagnostics,
    )


def _agent_context_from_runtime_instance(
    context: EffectiveTopicContext,
    agent_instance_id: str,
    *,
    env: Mapping[str, str],
) -> EffectiveAgentContext | None:
    runtime_db = _runtime_db_lookup_path(context, env=env)
    if not runtime_db.exists():
        return None
    try:
        with sqlite3.connect(runtime_db) as connection:
            connection.row_factory = sqlite3.Row
            row = connection.execute(
                """
                SELECT aw.agent_name, aw.agent_instance_id, pp.path
                FROM agent_workspaces aw
                JOIN path_plans pp ON pp.id = aw.path_plan_id
                WHERE aw.agent_instance_id = ? AND aw.topic_workspace_id = ?
                LIMIT 1
                """,
                (agent_instance_id, context.topic_workspace_id),
            ).fetchone()
    except sqlite3.Error:
        return None
    if row is None or row["agent_name"] is None:
        return None
    return EffectiveAgentContext(
        agent_name=row["agent_name"],
        agent_workspace_path=Path(row["path"]).resolve(strict=False),
        source="runtime",
        agent_instance_id=row["agent_instance_id"],
    )


def _agent_context_from_cwd(
    context: EffectiveTopicContext,
    cwd: Path,
    *,
    env: Mapping[str, str],
) -> tuple[EffectiveAgentContext | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    canonical_cwd = canonicalize(cwd)
    topic_main = _topic_main_lookup_path(context, env=env)
    try:
        canonical_cwd.relative_to(topic_main)
        return None, diagnostics
    except ValueError:
        pass

    runtime_contexts = _agent_contexts_from_runtime_cwd(context, canonical_cwd, env=env)
    if len(runtime_contexts) == 1:
        return runtime_contexts[0], diagnostics
    if len(runtime_contexts) > 1:
        diagnostics.append(
            Diagnostic(
                code="ISO061",
                severity="error",
                concept="Effective Agent Context",
                field="cwd",
                message="Current directory matches more than one Agent Workspace.",
            )
        )
        return None, diagnostics

    manifest, manifest_diagnostics = load_topic_workspace_manifest(context)
    diagnostics.extend(manifest_diagnostics)
    binding = manifest.binding_for("agent.workspace")
    if binding is not None:
        agent_name, workspace_root, issue = match_agent_name_from_template(context.topic_workspace_path, binding.path_template, canonical_cwd)
        if issue is not None:
            diagnostics.append(
                Diagnostic(
                    code="ISO061",
                    severity="warning",
                    concept="Effective Agent Context",
                    path=manifest.path,
                    field="agent.workspace",
                    message=issue,
                )
            )
            return None, diagnostics
        if agent_name is not None and workspace_root is not None:
            return EffectiveAgentContext(agent_name=agent_name, agent_workspace_path=workspace_root, source="cwd"), diagnostics
        cross_topic = _cross_topic_cwd_diagnostic(context, canonical_cwd)
        if cross_topic is not None:
            diagnostics.append(cross_topic)
        return None, diagnostics

    agent_name, workspace_root, _ = match_agent_name_from_template(
        context.topic_workspace_path,
        "agents/{agent_name}",
        canonical_cwd,
    )
    if agent_name is not None and workspace_root is not None:
        return EffectiveAgentContext(agent_name=agent_name, agent_workspace_path=workspace_root, source="cwd"), diagnostics
    cross_topic = _cross_topic_cwd_diagnostic(context, canonical_cwd)
    if cross_topic is not None:
        diagnostics.append(cross_topic)
    return None, diagnostics


def _cross_topic_cwd_diagnostic(context: EffectiveTopicContext, cwd: Path) -> Diagnostic | None:
    for topic in context.project.manifest.research_topics:
        if topic.id == context.research_topic.id:
            continue
        workspace_path = _registered_topic_workspace_path(context, topic.id, topic.topic_workspace_id)
        try:
            cwd.relative_to(canonicalize(workspace_path))
        except ValueError:
            continue
        return Diagnostic(
            code="ISO061",
            severity="error",
            concept="Effective Agent Context",
            field="cwd",
            message=(
                "Current directory is inside another Research Topic's Topic Workspace; "
                "select that Research Topic or change cwd before resolving agent-scoped paths."
            ),
        )
    return None


def _registered_topic_workspace_path(
    context: EffectiveTopicContext,
    topic_id: str,
    topic_workspace_id: str | None,
) -> Path:
    workspace = context.project.manifest.first_workspace(topic_workspace_id) if topic_workspace_id is not None else None
    if workspace is None:
        matching = [
            item
            for item in context.project.manifest.topic_workspaces
            if item.research_topic_id == topic_id
        ]
        if len(matching) == 1:
            workspace = matching[0]
    if workspace is not None and workspace.path_input is not None:
        return resolve_project_path(context.project.root, workspace.path_input)
    return default_topic_workspace_path(context.project.root, topic_id, context.project.manifest.path_defaults)


def _agent_contexts_from_runtime_cwd(
    context: EffectiveTopicContext,
    cwd: Path,
    *,
    env: Mapping[str, str],
) -> list[EffectiveAgentContext]:
    runtime_db = _runtime_db_lookup_path(context, env=env)
    if not runtime_db.exists():
        return []
    contexts: list[EffectiveAgentContext] = []
    try:
        with sqlite3.connect(runtime_db) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                """
                SELECT aw.agent_name, aw.agent_instance_id, pp.path
                FROM agent_workspaces aw
                JOIN path_plans pp ON pp.id = aw.path_plan_id
                WHERE aw.topic_workspace_id = ?
                ORDER BY length(pp.path) DESC
                """,
                (context.topic_workspace_id,),
            )
            for row in rows:
                workspace_path = Path(row["path"]).resolve(strict=False)
                try:
                    cwd.relative_to(workspace_path)
                except ValueError:
                    continue
                if row["agent_name"] is not None:
                    contexts.append(
                        EffectiveAgentContext(
                            agent_name=row["agent_name"],
                            agent_workspace_path=workspace_path,
                            source="cwd",
                            agent_instance_id=row["agent_instance_id"],
                        )
                    )
    except sqlite3.Error:
        return []
    if not contexts:
        return []
    longest = len(str(contexts[0].agent_workspace_path))
    return [context for context in contexts if len(str(context.agent_workspace_path)) == longest]


def _select_project_path(
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


def _normalize_label(label_or_surface: str) -> str:
    if label_or_surface in catalog():
        return label_or_surface
    if label_or_surface in compatibility_aliases():
        return compatibility_aliases()[label_or_surface]
    if ":" in label_or_surface:
        prefix, _ = label_or_surface.split(":", 1)
        mapped = compatibility_aliases().get(prefix)
        if mapped is not None:
            return mapped
    return label_or_surface


def _legacy_env_diagnostics(entry: ResolvedPathEntry) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if entry.surface in LEGACY_RECORD_ENV_SURFACES and entry.source == "env":
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="warning",
                concept="Workspace Path Resolution",
                field=entry.surface,
                message=(
                    "Legacy Topic Workspace path environment variable was used as an owner-preserved "
                    "`records/*` compatibility override."
                ),
            )
        )
    if entry.surface in LEGACY_AGENT_ENV_SURFACES and entry.source == "env":
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="warning",
                concept="Workspace Path Resolution",
                field=entry.surface,
                message=(
                    "Legacy Agent Workspace support environment variable was used as a compatibility "
                    "override for `isomer-managed/agent-owned/*`."
                ),
            )
        )
    return diagnostics


def _project_path_safety_diagnostics(
    context: EffectiveTopicContext,
    surface: str,
    path: Path,
) -> list[Diagnostic]:
    project_root = context.project.root
    diagnostics: list[Diagnostic] = []
    if not is_within(path, project_root):
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="Workspace Path Resolution",
                field=surface,
                message="Resolved path points outside the Project root.",
            )
        )
    if surface == "isomer_content_root" and is_within(path, context.project.config_dir):
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="Workspace Path Resolution",
                field=surface,
                message="Project generated content root must not live inside the Project Config Directory.",
            )
        )
    if surface == "isomer_content_root" and is_within(path, root_houmao_overlay_dir_for_root(project_root)):
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="Workspace Path Resolution",
                field=surface,
                message="Project generated content root must not collide with root .houmao external Houmao state.",
            )
        )
    return diagnostics


def _table_has_column(connection: sqlite3.Connection, table: str, column: str) -> bool:
    return any(row[1] == column for row in connection.execute(f"PRAGMA table_info({table})"))


def _row_has_key(row: sqlite3.Row, key: str) -> bool:
    return key in set(row.keys())
