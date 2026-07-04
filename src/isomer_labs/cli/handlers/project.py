"""Project CLI command handlers."""

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
    json,
    list_built_in_schemas,
    list_semantic_paths,
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
from isomer_labs.project.skill_callback_commands import (
    CallbackCommandResult,
    disable_user_skill_callback,
    list_user_skill_callbacks,
    register_user_skill_callback,
    resolve_user_skill_callbacks,
    show_user_skill_callback,
    validate_user_skill_callbacks,
)


def _cmd_init(options: CliOptions) -> int:
    project_root = Path(_value(options, "project") or os.getcwd())
    legacy_topic_id = _value(options, "topic_id_option") or _value(options, "topic_id")
    legacy_topic_statement = _value(options, "topic_statement")
    if legacy_topic_id is not None or legacy_topic_statement is not None:
        diagnostics = [
            Diagnostic(
                code="ISO003",
                severity="error",
                concept="Project initialization",
                field="topic_id",
                message="Project init does not create Research Topics. Create one explicitly with `isomer-cli project topics create <topic-id> --statement \"<research topic>\"`.",
            )
        ]
        payload = {
            "ok": False,
            "mutated": False,
            "project_root": str(project_root.resolve(strict=False)),
        }
        return _emit("init", options, payload, diagnostics, [])
    nested_project = find_ancestor_manifest(project_root)
    if nested_project is not None:
        ancestor_root = project_root_for_manifest(nested_project)
        if ancestor_root != project_root.resolve(strict=False):
            diagnostics = [
                Diagnostic(
                    code="ISO003",
                    severity="error",
                    concept="Project",
                    path=nested_project,
                    message=f"Refusing to initialize a nested Isomer Project inside existing Project root: {ancestor_root}.",
                )
            ]
            payload = {
                "ok": False,
                "mutated": False,
                "project_root": str(project_root.resolve(strict=False)),
                "ancestor_project_root": str(ancestor_root),
            }
            return _emit("project init", options, payload, diagnostics, [])
    result = initialize_project(
        project_root,
        content_dir=_value(options, "content_dir"),
        env=os.environ,
    )
    diagnostics = result.diagnostics
    houmao_bootstrap = result.houmao_bootstrap_result.to_json() if result.houmao_bootstrap_result is not None else None
    payload = {
        "ok": not has_errors(diagnostics),
        "mutated": not has_errors(diagnostics),
        "project_root": str(result.project_root),
        "project_manifest_path": str(result.project_manifest_path),
        "content_root_path": str(result.content_root_path),
        "topic_workspace_base_path": str(result.topic_workspace_base_path),
        "houmao_project_dir": str(result.houmao_project_dir),
        "houmao_overlay_dir": str(result.houmao_overlay_dir),
        "houmao_bootstrap": houmao_bootstrap,
    }
    lines = []
    if not diagnostics:
        lines = [
            f"Initialized Project: {result.project_root}",
            f"Project Manifest: {result.project_manifest_path}",
            f"Generated Content Root: {result.content_root_path}",
            f"Topic Workspace Base: {result.topic_workspace_base_path}",
            f"Houmao Project Directory: {result.houmao_project_dir}",
            f"Houmao Overlay: {result.houmao_overlay_dir}",
            "Research Topics: none registered; create one with `isomer-cli project topics create <topic-id> --statement \"<research topic>\"`.",
        ]
    return _emit("init", options, payload, diagnostics, lines)


def _cmd_validate(options: CliOptions) -> int:
    project, diagnostics = _discover(options)
    state: ProjectState | None = None
    if project is not None:
        state = build_project_state(project)
        diagnostics.extend(state.diagnostics)
    payload: dict[str, Any] = {
        "ok": not has_errors(diagnostics),
        "project": project.to_json() if project is not None else None,
    }
    if state is not None:
        payload["manifest"] = state.project.manifest.to_json()
        payload["topic_configs"] = {
            topic_id: config.to_json() for topic_id, config in sorted(state.topic_configs.items())
        }
    return _emit("validate", options, payload, diagnostics, _render_validate_text(project is not None, diagnostics))


def _cmd_cleanup(options: CliOptions) -> int:
    plan = plan_project_cleanup(
        cwd=Path.cwd(),
        project_selector=_value(options, "project"),
        manifest_selector=_value(options, "manifest"),
        parts=tuple(_value(options, "cleanup_parts") or ()),
        topics=tuple(_value(options, "cleanup_topics") or ()),
        all_topics=bool(_value(options, "cleanup_all_topics")),
        content_dir=_value(options, "content_dir"),
        purge_content_root=bool(_value(options, "cleanup_purge_content_root")),
        dry_run=bool(_value(options, "cleanup_dry_run")),
        yes=bool(_value(options, "cleanup_yes")),
    )
    execution = execute_project_cleanup(plan)
    return _emit("cleanup", options, execution.to_json(), list(execution.diagnostics), render_cleanup_text(execution))


def _cmd_content_root_move(options: CliOptions) -> int:
    plan = plan_project_content_root_move(
        cwd=Path.cwd(),
        project_selector=_value(options, "project"),
        manifest_selector=_value(options, "manifest"),
        to_content_dir=_value(options, "content_root_to"),
        dry_run=bool(_value(options, "content_root_move_dry_run")),
        yes=bool(_value(options, "content_root_move_yes")),
    )
    execution = execute_project_content_root_move(plan)
    return _emit("content-root move", options, execution.to_json(), list(execution.diagnostics), render_content_root_move_text(execution))


def _cmd_doctor(options: CliOptions) -> int:
    project, discovery_diagnostics = _discover(options)
    if project is None and not _project_selector_requested(options):
        discovery_diagnostics = [
            diagnostic for diagnostic in discovery_diagnostics if diagnostic.code != "ISO001"
        ]
    state: ProjectState | None = None
    project_diagnostics: list[Diagnostic] = []
    context: EffectiveTopicContext | None = None
    context_diagnostics: list[Diagnostic] = []
    topic_skipped = True
    if project is not None:
        state = build_project_state(project)
        project_diagnostics = list(state.diagnostics)
        request = _selection_request_from_options(options)
        resolved_context, resolved_diagnostics = resolve_effective_topic_context(
            state,
            request,
            cwd=Path.cwd(),
            env=os.environ,
        )
        if resolved_context is None and not _topic_selector_requested(options):
            context_diagnostics = [
                diagnostic for diagnostic in resolved_diagnostics if diagnostic.code != "ISO013"
            ]
            topic_skipped = True
        else:
            context = resolved_context
            context_diagnostics = list(resolved_diagnostics)
            topic_skipped = False
    report = build_doctor_report(
        project=project,
        discovery_diagnostics=discovery_diagnostics,
        project_diagnostics=project_diagnostics,
        context=context,
        context_diagnostics=context_diagnostics,
        topic_skipped=topic_skipped,
    )
    return _emit("doctor", options, report.to_payload(), report.diagnostics, render_doctor_text(report))


def _cmd_topics_list(options: CliOptions) -> int:
    project, diagnostics = _discover(options)
    topics: list[dict[str, object]] = []
    if project is not None:
        state = build_project_state(project)
        diagnostics.extend(state.diagnostics)
        topics = [topic.to_json() for topic in project.manifest.research_topics]
    payload = {"topics": topics}
    lines = ["Research Topics"]
    lines.extend(
        f"- {topic['id']} (config: {topic['config_path']}, workspace: {topic['topic_workspace_id'] or topic['id']})"
        for topic in topics
    )
    return _emit("topics list", options, payload, diagnostics, lines)


def _cmd_topics_show(options: CliOptions) -> int:
    project, diagnostics = _discover(options)
    if project is None:
        payload = {"ok": False, "mutated": False, "topic": None}
        return _emit("topics show", options, payload, diagnostics, [])
    state = build_project_state(project)
    diagnostics.extend(state.diagnostics)
    topic_id = _value(options, "topic_id")
    result = show_research_topic(state, topic_id)
    diagnostics.extend(result.diagnostics)
    return _emit("topics show", options, result.to_json(), diagnostics, render_topic_show_text(result))


def _cmd_topics_create(options: CliOptions) -> int:
    project, diagnostics = _discover(options)
    if project is None:
        payload = {"ok": False, "mutated": False}
        return _emit("topics create", options, payload, diagnostics, [])
    state = build_project_state(project)
    diagnostics.extend(state.diagnostics)
    if has_errors(diagnostics):
        payload = {"ok": False, "mutated": False}
        return _emit("topics create", options, payload, diagnostics, [])
    result = create_research_topic(
        project,
        topic_id=_value(options, "topic_id"),
        statement=_value(options, "topic_statement"),
        workspace_dir=_value(options, "topic_workspace_dir"),
        set_default=bool(_value(options, "topic_set_default")),
    )
    diagnostics.extend(result.diagnostics)
    return _emit("topics create", options, result.to_json(), diagnostics, render_topic_create_text(result))


def _cmd_topics_update(options: CliOptions) -> int:
    project, diagnostics = _discover(options)
    if project is None:
        payload = {"ok": False, "mutated": False}
        return _emit("topics update", options, payload, diagnostics, [])
    state = build_project_state(project)
    diagnostics.extend(state.diagnostics)
    if has_errors(diagnostics):
        payload = {"ok": False, "mutated": False}
        return _emit("topics update", options, payload, diagnostics, [])
    result = update_research_topic(
        state,
        topic_id=_value(options, "topic_id"),
        statement=_value(options, "topic_statement"),
        status=_value(options, "topic_status"),
        set_default=bool(_value(options, "topic_set_default")),
        new_id=_value(options, "topic_new_id"),
    )
    diagnostics.extend(result.diagnostics)
    return _emit("topics update", options, result.to_json(), diagnostics, render_topic_update_text(result))


def _cmd_topics_delete(options: CliOptions) -> int:
    project, diagnostics = _discover(options)
    if project is None:
        payload = {"ok": False, "mutated": False}
        return _emit("topics delete", options, payload, diagnostics, [])
    state = build_project_state(project)
    diagnostics.extend(state.diagnostics)
    if has_errors(diagnostics):
        payload = {"ok": False, "mutated": False}
        return _emit("topics delete", options, payload, diagnostics, [])
    plan = plan_delete_research_topic(
        state,
        topic_id=_value(options, "topic_id"),
        dry_run=bool(_value(options, "topic_delete_dry_run")),
        yes=bool(_value(options, "topic_delete_yes")),
    )
    result = delete_research_topic(plan, project)
    diagnostics.extend(result.diagnostics)
    return _emit("topics delete", options, result.to_json(), diagnostics, render_topic_delete_text(result))


def _cmd_context_show(options: CliOptions) -> int:
    context, diagnostics = _context_for_options(options)
    agent_context = None
    topic_actor_context = None
    payload = {"context": context.to_json() if context is not None else None}
    if context is None:
        lines = []
    else:
        topic_actor_context, topic_actor_diagnostics = resolve_effective_topic_actor_context(
            context,
            env=os.environ,
            cwd=Path.cwd(),
            explicit_topic_actor_name=_value(options, "topic_actor_name"),
            missing_is_error=False,
        )
        diagnostics.extend(topic_actor_diagnostics)
        if topic_actor_context is not None:
            payload["effective_topic_actor_context"] = topic_actor_context.to_json()
        agent_context, agent_diagnostics = resolve_effective_agent_context(
            context,
            env=os.environ,
            cwd=Path.cwd(),
            explicit_agent_name=_value(options, "agent_name"),
            explicit_agent_instance_id=_value(options, "agent_instance_id"),
            missing_is_error=False,
        )
        diagnostics.extend(agent_diagnostics)
        if agent_context is not None:
            payload["effective_agent_context"] = agent_context.to_json()
        lines = render_key_values(
            [
                ("Project", context.project.root),
                ("Project Config Directory", context.project.config_dir),
                ("Project Manifest", context.project.manifest_path),
                ("Research Topic", context.research_topic.id),
                (
                    "Research Topic Config",
                    context.research_topic_config.source_path if context.research_topic_config is not None else "missing",
                ),
                ("Topic Workspace", context.topic_workspace_id),
                ("Topic Workspace Path", context.topic_workspace_path),
                ("Research Topic Source", context.sources["research_topic_id"]),
                ("Topic Actor", topic_actor_context.topic_actor_name if topic_actor_context is not None else "none"),
                ("Agent Name", agent_context.agent_name if agent_context is not None else "none"),
            ]
        )
    return _emit("context show", options, payload, diagnostics, lines)


def _cmd_skill_callbacks_register(options: CliOptions) -> int:
    state, context, diagnostics = _callback_state_and_context(
        options,
        require_topic=_value(options, "callback_scope") == "research_topic",
    )
    if state is None or has_errors(diagnostics):
        payload = {"ok": False, "mutated": False}
        return _emit("skill-callbacks register", options, payload, diagnostics, [])
    result = register_user_skill_callback(
        state,
        context,
        callback_id=_value(options, "callback_id"),
        skill=_value(options, "callback_skill"),
        stage=_value(options, "callback_stage"),
        scope=_value(options, "callback_scope") or "research_topic",
        priority=_value(options, "callback_priority"),
        prompt=_value(options, "callback_prompt"),
        prompt_file=_value(options, "callback_prompt_file"),
        skill_dir=_value(options, "callback_skill_dir"),
        allow_external_source=bool(_value(options, "callback_allow_external_source")),
    )
    return _emit(
        "skill-callbacks register",
        options,
        result.to_json(),
        list(result.diagnostics),
        _render_callback_result("Registered User Skill Callback", result),
    )


def _cmd_skill_callbacks_resolve(options: CliOptions) -> int:
    state, context, diagnostics = _callback_state_and_context(options, require_topic=False)
    if state is None:
        payload = {"ok": False, "mutated": False, "callbacks": []}
        return _emit("skill-callbacks resolve", options, payload, diagnostics, [])
    result = resolve_user_skill_callbacks(
        state,
        context,
        skill=_value(options, "callback_skill"),
        stage=_value(options, "callback_stage"),
    )
    diagnostics.extend(result.diagnostics)
    return _emit(
        "skill-callbacks resolve",
        options,
        result.to_json(),
        diagnostics,
        _render_callback_result("Resolved User Skill Callbacks", result),
    )


def _cmd_skill_callbacks_list(options: CliOptions) -> int:
    state, context, diagnostics = _callback_state_and_context(options, require_topic=False)
    if state is None:
        payload = {"ok": False, "mutated": False, "callbacks": []}
        return _emit("skill-callbacks list", options, payload, diagnostics, [])
    result = list_user_skill_callbacks(state, context)
    diagnostics.extend(result.diagnostics)
    return _emit(
        "skill-callbacks list",
        options,
        result.to_json(),
        diagnostics,
        _render_callback_result("User Skill Callbacks", result),
    )


def _cmd_skill_callbacks_show(options: CliOptions) -> int:
    state, context, diagnostics = _callback_state_and_context(options, require_topic=False)
    if state is None:
        payload = {"ok": False, "mutated": False, "callbacks": []}
        return _emit("skill-callbacks show", options, payload, diagnostics, [])
    result = show_user_skill_callback(state, context, callback_id=_value(options, "callback_id"))
    diagnostics.extend(result.diagnostics)
    return _emit(
        "skill-callbacks show",
        options,
        result.to_json(),
        diagnostics,
        _render_callback_result("User Skill Callback", result),
    )


def _cmd_skill_callbacks_disable(options: CliOptions) -> int:
    state, context, diagnostics = _callback_state_and_context(options, require_topic=False)
    if state is None or has_errors(diagnostics):
        payload = {"ok": False, "mutated": False, "callbacks": []}
        return _emit("skill-callbacks disable", options, payload, diagnostics, [])
    result = disable_user_skill_callback(state, context, callback_id=_value(options, "callback_id"))
    diagnostics.extend(result.diagnostics)
    return _emit(
        "skill-callbacks disable",
        options,
        result.to_json(),
        diagnostics,
        _render_callback_result("Disabled User Skill Callback", result),
    )


def _cmd_skill_callbacks_validate(options: CliOptions) -> int:
    state, context, diagnostics = _callback_state_and_context(options, require_topic=False)
    if state is None:
        payload = {"ok": False, "mutated": False, "callbacks": []}
        return _emit("skill-callbacks validate", options, payload, diagnostics, [])
    result = validate_user_skill_callbacks(state, context)
    diagnostics.extend(result.diagnostics)
    return _emit(
        "skill-callbacks validate",
        options,
        result.to_json(),
        diagnostics,
        _render_callback_result("Validated User Skill Callbacks", result),
    )


def _callback_state_and_context(
    options: CliOptions,
    *,
    require_topic: bool,
) -> tuple[ProjectState | None, EffectiveTopicContext | None, list[Diagnostic]]:
    project, diagnostics = _discover(options)
    if project is None:
        return None, None, diagnostics
    state = build_project_state(project)
    diagnostics.extend(state.diagnostics)
    context, context_diagnostics = resolve_effective_topic_context(
        state,
        _selection_request_from_options(options),
        cwd=Path.cwd(),
        env=os.environ,
    )
    if context is None:
        if require_topic or _topic_selector_requested(options):
            diagnostics.extend(context_diagnostics)
    else:
        diagnostics.extend(context_diagnostics)
    return state, context, diagnostics


def _render_callback_result(title: str, result: CallbackCommandResult) -> list[str]:
    lines = [title]
    if not result.callbacks:
        lines.append("- none")
    for callback in result.callbacks:
        data = callback.to_json(result.project_root)
        source = data["source_summary"]
        lines.append(
            f"- {callback.id} ({callback.scope} {callback.skill} {callback.stage}, status={callback.status}, priority={callback.priority}, source={source})"
        )
    if result.previous_status is not None and result.new_status is not None:
        lines.append(f"Status: {result.previous_status} -> {result.new_status}")
    return lines

__all__ = [
    "_cmd_init",
    "_cmd_validate",
    "_cmd_cleanup",
    "_cmd_content_root_move",
    "_cmd_doctor",
    "_cmd_topics_list",
    "_cmd_topics_show",
    "_cmd_topics_create",
    "_cmd_topics_update",
    "_cmd_topics_delete",
    "_cmd_context_show",
    "_cmd_skill_callbacks_register",
    "_cmd_skill_callbacks_resolve",
    "_cmd_skill_callbacks_list",
    "_cmd_skill_callbacks_show",
    "_cmd_skill_callbacks_disable",
    "_cmd_skill_callbacks_validate",
]
