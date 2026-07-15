"""Workspace path and output-policy CLI command handlers."""

# ruff: noqa: F401
from __future__ import annotations

from isomer_labs.cli.handlers.shared import (
    adapter_manifest_path_plan_surface,
    AdapterManifestRefRecord,
    AdapterReconciliationRecord,
    AgentBinding,
    Any,
    archive_topic_actor,
    build_adapter_link_manifest,
    build_adapter_runtime_manifest,
    build_doctor_report,
    build_project_state,
    build_self_env_payload,
    build_self_identity_payload,
    build_self_paths_payload,
    build_self_pixi_payload,
    build_self_queries_payload,
    build_self_show_payload,
    canonical_json_digest,
    CliOptions,
    collect_houmao_read_only_state,
    create_research_topic,
    dataclass,
    default_semantic_path,
    default_topic_workspace_path,
    delete_research_topic,
    diagnose_topic_actor,
    Diagnostic,
    discover_domain_agent_team_templates,
    discover_project,
    discover_team_repositories,
    display_path,
    EffectiveTopicContext,
    emit_output,
    ensure_topic_main_guidance,
    execute_project_cleanup,
    execute_project_content_root_move,
    explain_semantic_path,
    find_ancestor_manifest,
    find_domain_agent_team_template,
    guidance_metadata,
    has_errors,
    HOUMAO_ADAPTER_ID,
    houmao_project_dir_for_root,
    HoumaoAdapterFacade,
    initialize_project,
    initialize_workspace_runtime,
    inspect_topic_main_guidance,
    inspect_workspace_runtime,
    is_grouped_topic_repo_label,
    json,
    list_built_in_schemas,
    list_semantic_paths,
    load_topic_workspace_manifest,
    list_topic_actors,
    load_json_manifest,
    load_toml,
    manifest_paths,
    ManifestKind,
    ManifestValidationError,
    materialize_default_paths,
    materialize_semantic_path,
    materialize_topic_actor_workspace,
    materialize_topic_agent_team_profile_bundle,
    open_workspace_runtime,
    os,
    output_format,
    parse_topic_agent_team_profile,
    parse_topic_team_instantiation_packet,
    Path,
    plan_delete_research_topic,
    plan_project_cleanup,
    plan_project_content_root_move,
    prepare_topic_environment_readiness,
    preview_paths,
    profile_to_toml,
    Project,
    project_root_for_manifest,
    ProjectState,
    reconcile_houmao_manifests,
    register_manifest_binding,
    register_topic_actor,
    render_cleanup_text,
    render_content_root_move_text,
    render_doctor_text,
    render_key_values,
    render_topic_create_text,
    render_topic_delete_text,
    render_topic_main_guidance_block,
    render_topic_show_text,
    render_topic_update_text,
    replace,
    reset_manifest_binding,
    resolve_binding_path,
    resolve_effective_agent_context,
    resolve_effective_topic_actor_context,
    resolve_effective_topic_context,
    resolve_self_identity_contexts,
    resolve_semantic_path,
    resolve_template_source_path,
    resolve_worker_output_policy,
    SelectionRequest,
    Sequence,
    show_research_topic,
    show_topic_actor,
    specialize_topic_agent_team_profile,
    tomlkit,
    TopicAgentTeamProfile,
    unregister_manifest_binding,
    update_manifest_binding,
    update_research_topic,
    update_topic_actor,
    utc_timestamp,
    validate_domain_agent_team_template,
    validate_topic_agent_team_profile,
    validate_workspace_runtime,
    WORKER_OUTPUT_TRACKING_AUTHORITY,
    write_json_manifest,
    _append_template_registration,
    _context_for_options,
    _context_for_path_options,
    _discover,
    _discover_optional,
    _emit,
    _missing_template_diagnostic,
    _output_format,
    _path_label_requires_selected_topic,
    _profile_registration_suggestion,
    _project_relative_path,
    _project_selector_requested,
    _render_validate_text,
    _resolve_cli_path,
    _resolve_profile_cli_path,
    _resolved_name,
    _selection_request_from_options,
    _self_identity_inputs,
    _topic_selector_requested,
    _unknown_template_diagnostic,
    _value,
)

def _cmd_paths_get(options: CliOptions, semantic_label: str) -> int:
    context, diagnostics = _context_for_path_options(options, semantic_label)
    result = None
    if context is not None:
        result, path_diagnostics = resolve_semantic_path(
            context,
            semantic_label,
            env=os.environ,
            cwd=Path.cwd(),
            agent_name=_value(options, "agent_name"),
            agent_instance_id=_value(options, "agent_instance_id"),
            topic_actor_name=_value(options, "topic_actor_name"),
            use_path_plan=not bool(_value(options, "paths_configured")),
        )
        diagnostics.extend(path_diagnostics)
    payload = {
        "ok": not has_errors(diagnostics),
        "mutated": False,
        "path": result.to_json() if result is not None else None,
    }
    lines = []
    if result is not None:
        lines = [
            f"{result.label}: {result.path}",
            f"Source: {result.source}",
        ]
        if result.agent_name is not None:
            lines.append(f"Agent Name: {result.agent_name}")
        if result.topic_actor_name is not None:
            lines.append(f"Topic Actor: {result.topic_actor_name}")
    return _emit("paths get", options, payload, diagnostics, lines)


def _cmd_outputs_policy(options: CliOptions) -> int:
    context, diagnostics = _context_for_path_options(options, "agent.output_root")
    policy = None
    if context is not None:
        agent_name = _value(options, "agent_name")
        topic_actor_name = _value(options, "topic_actor_name")
        if bool(agent_name) == bool(topic_actor_name):
            diagnostics.append(
                Diagnostic(
                    code="ISO061",
                    severity="error",
                    concept="Worker Output Policy",
                    message="Use exactly one of `--agent` or `--topic-actor`.",
                )
            )
        elif agent_name:
            agent_context, agent_diagnostics = resolve_effective_agent_context(
                context,
                env=os.environ,
                cwd=Path.cwd(),
                explicit_agent_name=agent_name,
            )
            diagnostics.extend(agent_diagnostics)
            if agent_context is not None:
                policy, policy_diagnostics = resolve_worker_output_policy(context, env=os.environ, agent_context=agent_context)
                diagnostics.extend(policy_diagnostics)
        elif topic_actor_name:
            topic_actor_context, actor_diagnostics = resolve_effective_topic_actor_context(
                context,
                env=os.environ,
                cwd=Path.cwd(),
                explicit_topic_actor_name=topic_actor_name,
            )
            diagnostics.extend(actor_diagnostics)
            if topic_actor_context is not None:
                policy, policy_diagnostics = resolve_worker_output_policy(context, env=os.environ, topic_actor_context=topic_actor_context)
                diagnostics.extend(policy_diagnostics)
    payload = {
        "ok": not has_errors(diagnostics),
        "mutated": False,
        "output_policy": policy.to_json() if policy is not None else None,
    }
    lines: list[str] = []
    if policy is not None:
        lines = [
            f"{policy.worker_kind} {policy.worker_name}: {policy.output_root.path}",
            f"Relative root: {policy.worker_relative_root}",
            f"Operation sets: {policy.operation_set_pattern}",
            f"Commit after operation: {str(policy.commit_after_operation).lower()}",
            f"Tracking authority: {WORKER_OUTPUT_TRACKING_AUTHORITY}",
        ]
    return _emit("outputs policy", options, payload, diagnostics, lines)


def _resolve_topic_main_guidance_repo(options: CliOptions) -> tuple[Path | None, list[Diagnostic]]:
    context, diagnostics = _context_for_path_options(options, "topic.repos.main")
    if context is None:
        return None, diagnostics
    result, path_diagnostics = resolve_semantic_path(
        context,
        "topic.repos.main",
        env=os.environ,
        cwd=Path.cwd(),
    )
    diagnostics.extend(path_diagnostics)
    if result is None:
        return None, diagnostics
    return result.path, diagnostics


def _render_topic_main_guidance_summary(title: str, payload: dict[str, Any]) -> list[str]:
    lines = [title]
    repo_path = payload.get("topic_main_repo")
    if repo_path is not None:
        lines.append(f"Topic Main Repository: {repo_path}")
    targets = payload.get("targets", [])
    if isinstance(targets, list):
        for target in targets:
            if isinstance(target, dict):
                action = target.get("action")
                status = target.get("status")
                filename = target.get("filename")
                if action and action != "unchanged":
                    lines.append(f"- {filename}: {status} ({action})")
                else:
                    lines.append(f"- {filename}: {status}")
    changed_files = payload.get("changed_files", [])
    if isinstance(changed_files, list) and changed_files:
        lines.append("Changed files:")
        lines.extend(f"- {path}" for path in changed_files)
    return lines


def _cmd_paths_default(options: CliOptions, semantic_label: str) -> int:
    context, diagnostics = _context_for_path_options(options, semantic_label)
    result = None
    if context is not None:
        result, path_diagnostics = default_semantic_path(
            context,
            semantic_label,
            agent_name=_value(options, "agent_name"),
            topic_actor_name=_value(options, "topic_actor_name"),
        )
        diagnostics.extend(path_diagnostics)
    payload = {
        "ok": not has_errors(diagnostics),
        "mutated": False,
        "path": result,
    }
    lines = []
    if result is not None:
        lines = [
            f"{result['semantic_label']}: {result['path']}",
            f"Source: {result['source']}",
        ]
    return _emit("paths default", options, payload, diagnostics, lines)


def _cmd_paths_explain(options: CliOptions, semantic_label: str) -> int:
    context, diagnostics = _context_for_path_options(options, semantic_label)
    explanation = None
    if context is not None:
        explanation, path_diagnostics = explain_semantic_path(
            context,
            semantic_label,
            env=os.environ,
            cwd=Path.cwd(),
            agent_name=_value(options, "agent_name"),
            agent_instance_id=_value(options, "agent_instance_id"),
            topic_actor_name=_value(options, "topic_actor_name"),
        )
        diagnostics.extend(path_diagnostics)
    payload = {
        "ok": not has_errors(diagnostics),
        "mutated": False,
        "explanation": explanation,
    }
    lines = []
    if explanation is not None:
        lines = [f"{explanation['semantic_label']}: {explanation['selected_mode']}"]
        candidates = explanation.get("candidates", [])
        if isinstance(candidates, list):
            for candidate in candidates:
                if isinstance(candidate, dict):
                    lines.append(f"- {candidate.get('mode')}: {candidate.get('path')} ({candidate.get('source')})")
    return _emit("paths explain", options, payload, diagnostics, lines)


def _cmd_paths_list(options: CliOptions) -> int:
    context, diagnostics = _context_for_path_options(options)
    paths: list[dict[str, object]] = []
    if context is not None:
        paths, path_diagnostics = list_semantic_paths(
            context,
            env=os.environ,
            cwd=Path.cwd(),
            agent_name=_value(options, "agent_name"),
            agent_instance_id=_value(options, "agent_instance_id"),
            topic_actor_name=_value(options, "topic_actor_name"),
        )
        diagnostics.extend(path_diagnostics)
    payload = {
        "ok": not has_errors(diagnostics),
        "mutated": False,
        "paths": paths,
    }
    lines = ["Semantic Workspace Paths"]
    for item in paths:
        status = "resolved" if item.get("resolved") else "unresolved"
        path = f" -> {item['path']}" if item.get("path") else ""
        lines.append(f"- {item['semantic_label']}: {status}{path}")
    return _emit("paths list", options, payload, diagnostics, lines)


def _cmd_paths_materialize_default(
    options: CliOptions,
    *,
    labels: tuple[str, ...],
) -> int:
    context, diagnostics = _context_for_path_options(options)
    result = None
    if context is not None:
        result, path_diagnostics = materialize_default_paths(
            context,
            labels=labels,
            agent_name=_value(options, "agent_name"),
            topic_actor_name=_value(options, "topic_actor_name"),
        )
        diagnostics.extend(path_diagnostics)
    payload = {
        "ok": not has_errors(diagnostics),
        "mutated": result is not None and not has_errors(diagnostics),
        "materialization": result,
    }
    lines = ["Default semantic paths materialized."]
    if result is not None:
        created_paths = result.get("created_paths")
        if isinstance(created_paths, list):
            lines.extend(f"- {path}" for path in created_paths)
    return _emit("paths materialize-default", options, payload, diagnostics, lines if result is not None else [])


def _cmd_paths_materialize(options: CliOptions, semantic_label: str) -> int:
    context, diagnostics = _context_for_path_options(options, semantic_label)
    result = None
    if context is not None:
        result, path_diagnostics = materialize_semantic_path(
            context,
            semantic_label,
            env=os.environ,
            cwd=Path.cwd(),
            agent_name=_value(options, "agent_name"),
            agent_instance_id=_value(options, "agent_instance_id"),
            topic_actor_name=_value(options, "topic_actor_name"),
        )
        diagnostics.extend(path_diagnostics)
    payload = {
        "ok": not has_errors(diagnostics),
        "mutated": result is not None and not has_errors(diagnostics),
        "materialization": result,
    }
    lines = ["Semantic path materialized."]
    if result is not None:
        created_paths = result.get("created_paths")
        if isinstance(created_paths, list):
            lines.extend(f"- {path}" for path in created_paths)
    return _emit("paths materialize", options, payload, diagnostics, lines if result is not None else [])


def _cmd_paths_register(
    options: CliOptions,
    semantic_label: str,
    *,
    path: str,
    storage_profile: str,
    create: bool,
    replace_existing: bool,
) -> int:
    context, diagnostics = _context_for_path_options(options, semantic_label)
    result = None
    created: list[str] = []
    if context is not None:
        manifest, created_paths, binding_diagnostics = register_manifest_binding(
            context,
            label=semantic_label,
            path_template=path,
            storage_profile=storage_profile,
            create=create,
            replace_existing=replace_existing,
        )
        diagnostics.extend(binding_diagnostics)
        if manifest is not None:
            result = manifest.to_json()
            created = [str(item.resolve(strict=False)) for item in created_paths]
    payload = {
        "ok": not has_errors(diagnostics),
        "mutated": result is not None and not has_errors(diagnostics),
        "manifest": result,
        "created_paths": created,
    }
    lines = [f"Registered semantic path binding: {semantic_label}"] if result is not None else []
    return _emit("paths register", options, payload, diagnostics, lines)


def _cmd_paths_update(
    options: CliOptions,
    semantic_label: str,
    *,
    path: str | None,
    storage_profile: str | None,
    create: bool,
) -> int:
    context, diagnostics = _context_for_path_options(options, semantic_label)
    result = None
    created: list[str] = []
    if context is not None:
        manifest, created_paths, binding_diagnostics = update_manifest_binding(
            context,
            label=semantic_label,
            path_template=path,
            storage_profile=storage_profile,
            create=create,
        )
        diagnostics.extend(binding_diagnostics)
        if manifest is not None:
            result = manifest.to_json()
            created = [str(item.resolve(strict=False)) for item in created_paths]
    payload = {
        "ok": not has_errors(diagnostics),
        "mutated": result is not None and not has_errors(diagnostics),
        "manifest": result,
        "created_paths": created,
    }
    lines = [f"Updated semantic path binding: {semantic_label}"] if result is not None else []
    return _emit("paths update", options, payload, diagnostics, lines)


def _cmd_paths_unregister(options: CliOptions, semantic_label: str) -> int:
    context, diagnostics = _context_for_path_options(options, semantic_label)
    result = None
    if context is not None:
        manifest, binding_diagnostics = unregister_manifest_binding(context, label=semantic_label)
        diagnostics.extend(binding_diagnostics)
        if manifest is not None:
            result = manifest.to_json()
    payload = {
        "ok": not has_errors(diagnostics),
        "mutated": result is not None and not has_errors(diagnostics),
        "manifest": result,
    }
    lines = [f"Unregistered semantic path binding: {semantic_label}"] if result is not None else []
    return _emit("paths unregister", options, payload, diagnostics, lines)


def _cmd_paths_reset(options: CliOptions, semantic_label: str) -> int:
    context, diagnostics = _context_for_path_options(options, semantic_label)
    result = None
    if context is not None:
        manifest, binding_diagnostics = reset_manifest_binding(context, label=semantic_label)
        diagnostics.extend(binding_diagnostics)
        if manifest is not None:
            result = manifest.to_json()
    payload = {
        "ok": not has_errors(diagnostics),
        "mutated": result is not None and not has_errors(diagnostics),
        "manifest": result,
    }
    lines = [f"Reset semantic path binding: {semantic_label}"] if result is not None else []
    return _emit("paths reset", options, payload, diagnostics, lines)


def _cmd_repos_create(
    options: CliOptions,
    repo_label: str,
    *,
    path: str | None,
    create: bool,
    replace_existing: bool,
) -> int:
    semantic_label = repo_label if repo_label.startswith("topic.repos.") else f"topic.repos.{repo_label}"
    if semantic_label == "topic.repos.main" and path is None:
        diagnostics = [
            Diagnostic(
                code="ISO061",
                severity="error",
                concept="Topic Workspace Manifest",
                field=semantic_label,
                message=(
                    "`topic.repos.main` is a built-in Topic Main Development Repository label. "
                    "Use `project paths materialize-default --label topic.repos.main` or "
                    "`project paths register topic.repos.main --path <path> --storage-profile topic_repo`."
                ),
            )
        ]
        payload: dict[str, Any] = {"ok": False, "mutated": False, "manifest": None, "created_paths": []}
        return _emit("repos create", options, payload, diagnostics, [])
    repo_suffix = semantic_label.removeprefix("topic.repos.")
    default_path = "repos/extern/" + "/".join(repo_suffix.split("."))
    return _cmd_paths_register(
        options,
        semantic_label,
        path=path or default_path,
        storage_profile="topic_repo",
        create=create,
        replace_existing=replace_existing,
    )


def _cmd_repos_register(
    options: CliOptions,
    repo_label: str,
    *,
    path: str,
) -> int:
    semantic_label = repo_label if repo_label.startswith("topic.repos.") else f"topic.repos.{repo_label}"
    diagnostics: list[Diagnostic] = []
    if semantic_label == "topic.repos.main":
        diagnostics.append(
            Diagnostic(
                code="ISO061",
                severity="error",
                concept="Canonical External Repository",
                field=semantic_label,
                message="`topic.repos.main` is the Topic Main Development Repository and cannot be registered as a Canonical External Repository.",
            )
        )
    elif not is_grouped_topic_repo_label(semantic_label):
        diagnostics.append(
            Diagnostic(
                code="ISO061",
                severity="error",
                concept="Canonical External Repository",
                field=semantic_label,
                message="Repository label must be a valid non-main `topic.repos.<group...>.<repo-name>` semantic label.",
            )
        )
    if diagnostics:
        return _emit(
            "repos register",
            options,
            {"ok": False, "mutated": False, "manifest": None, "repository": None, "created_paths": []},
            diagnostics,
            [],
        )

    context, context_diagnostics = _context_for_path_options(options, semantic_label)
    diagnostics.extend(context_diagnostics)
    if context is None:
        return _emit(
            "repos register",
            options,
            {"ok": False, "mutated": False, "manifest": None, "repository": None, "created_paths": []},
            diagnostics,
            [],
        )

    path_value = Path(path).expanduser()
    target_path = (
        path_value.resolve(strict=False)
        if path_value.is_absolute()
        else (context.topic_workspace_path / path_value).resolve(strict=False)
    )
    if not target_path.exists():
        diagnostics.append(
            Diagnostic(
                code="ISO061",
                severity="error",
                concept="Canonical External Repository",
                field=semantic_label,
                path=target_path,
                message="Repository registration requires an existing directory acquired and verified outside Isomer.",
            )
        )
    elif not target_path.is_dir():
        diagnostics.append(
            Diagnostic(
                code="ISO061",
                severity="error",
                concept="Canonical External Repository",
                field=semantic_label,
                path=target_path,
                message="Repository registration target exists but is not a directory.",
            )
        )
    if diagnostics:
        return _emit(
            "repos register",
            options,
            {"ok": False, "mutated": False, "manifest": None, "repository": None, "created_paths": []},
            diagnostics,
            [],
        )

    manifest, manifest_diagnostics = load_topic_workspace_manifest(context)
    diagnostics.extend(manifest_diagnostics)
    existing = manifest.binding_for(semantic_label)
    if existing is not None:
        existing_path = resolve_binding_path(context, existing, agent_name=None)
        if existing.storage_profile == "topic_repo" and existing_path == target_path:
            payload = {
                "ok": not has_errors(diagnostics),
                "mutated": False,
                "manifest": manifest.to_json(),
                "repository": {
                    "semantic_label": semantic_label,
                    "path": str(target_path),
                    "storage_profile": "topic_repo",
                },
                "created_paths": [],
            }
            lines = [f"Repository binding already registered: {semantic_label} -> {target_path}"]
            return _emit("repos register", options, payload, diagnostics, lines)
        diagnostics.append(
            Diagnostic(
                code="ISO061",
                severity="error",
                concept="Canonical External Repository",
                field=semantic_label,
                path=manifest.path,
                message=(
                    f"Repository label is already bound to `{existing_path}` and cannot be registered at `{target_path}`. "
                    "Use `project paths update` for an explicit topology change."
                ),
            )
        )
        return _emit(
            "repos register",
            options,
            {"ok": False, "mutated": False, "manifest": None, "repository": None, "created_paths": []},
            diagnostics,
            [],
        )

    next_manifest, _created, binding_diagnostics = register_manifest_binding(
        context,
        label=semantic_label,
        path_template=path,
        storage_profile="topic_repo",
        create=False,
        replace_existing=False,
    )
    diagnostics.extend(binding_diagnostics)
    payload = {
        "ok": next_manifest is not None and not has_errors(diagnostics),
        "mutated": next_manifest is not None and not has_errors(diagnostics),
        "manifest": next_manifest.to_json() if next_manifest is not None else None,
        "repository": (
            {
                "semantic_label": semantic_label,
                "path": str(target_path),
                "storage_profile": "topic_repo",
            }
            if next_manifest is not None
            else None
        ),
        "created_paths": [],
    }
    lines = [f"Registered existing repository: {semantic_label} -> {target_path}"] if next_manifest is not None else []
    return _emit("repos register", options, payload, diagnostics, lines)


def _cmd_paths_preview(options: CliOptions) -> int:
    context, diagnostics = _context_for_path_options(options)
    entries: list[dict[str, object]] = []
    text_lines: list[str] = []
    if context is not None:
        resolved, path_diagnostics = preview_paths(context, env=os.environ)
        diagnostics.extend(path_diagnostics)
        entries = [entry.to_json() for entry in resolved]
        text_lines = ["Workspace Paths"]
        text_lines.extend(
            f"- {entry.semantic_label or entry.surface}: {entry.path} ({entry.source})"
            for entry in resolved
        )
    payload = {"paths": entries}
    return _emit("paths preview", options, payload, diagnostics, text_lines)
__all__ = [
    "_cmd_paths_get",
    "_cmd_outputs_policy",
    "_resolve_topic_main_guidance_repo",
    "_render_topic_main_guidance_summary",
    "_cmd_paths_default",
    "_cmd_paths_explain",
    "_cmd_paths_list",
    "_cmd_paths_materialize_default",
    "_cmd_paths_materialize",
    "_cmd_paths_register",
    "_cmd_paths_update",
    "_cmd_paths_unregister",
    "_cmd_paths_reset",
    "_cmd_repos_create",
    "_cmd_repos_register",
    "_cmd_paths_preview",
]
