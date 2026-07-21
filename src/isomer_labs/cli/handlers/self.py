"""Self-inspection CLI command handlers."""

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
    build_self_check_payload,
    build_self_env_payload,
    build_self_identity_payload,
    build_self_location_payload,
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
    OperationScope,
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
    resolve_ambient_workspace_location,
    resolve_self_identity_contexts,
    resolve_semantic_path,
    resolve_task_context_alignment,
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


def _cmd_self_show(options: CliOptions) -> int:
    context, topic_actor_context, agent_context, diagnostics = _self_identity_inputs(options)
    payload = build_self_show_payload(
        context,
        diagnostics=diagnostics,
        topic_actor_context=topic_actor_context,
        agent_context=agent_context,
    )
    summary = payload.get("summary", {})
    lines = ["Self Summary"]
    if isinstance(summary, dict):
        topic = summary.get("topic")
        actor = summary.get("topic_actor")
        agent = summary.get("agent")
        counts = summary.get("diagnostic_counts")
        if isinstance(topic, dict):
            lines.append(f"Research Topic: {topic.get('research_topic_id', 'unresolved')}")
            lines.append(f"Topic Workspace: {topic.get('topic_workspace_id', 'unresolved')}")
        if isinstance(actor, dict):
            lines.append(f"Topic Actor: {_resolved_name(actor, 'topic_actor_name')}")
        if isinstance(agent, dict):
            lines.append(f"Agent: {_resolved_name(agent, 'agent_name')}")
        if isinstance(counts, dict):
            lines.append(f"Diagnostics: {counts.get('errors', 0)} errors, {counts.get('warnings', 0)} warnings")
    lines.append(
        "Available: self identity, self location, self check --scope <scope>, self pixi, self env, "
        "self paths <label>, self queries"
    )
    return _emit("self show", options, payload, diagnostics, lines)


def _cmd_self_identity(options: CliOptions) -> int:
    context, topic_actor_context, agent_context, diagnostics = _self_identity_inputs(options)
    payload = build_self_identity_payload(
        context,
        diagnostics=diagnostics,
        topic_actor_context=topic_actor_context,
        agent_context=agent_context,
    )
    if agent_context is None:
        payload["agent_resolution_help"] = (
            "Provide --agent, --agent-instance, ISOMER_AGENT_NAME, or ISOMER_AGENT_INSTANCE_ID."
        )
    lines = ["Self Identity"]
    if context is not None:
        lines.extend(
            [
                f"Research Topic: {context.research_topic.id}",
                f"Topic Workspace: {context.topic_workspace_id}",
                f"Topic Actor: {topic_actor_context.topic_actor_name if topic_actor_context is not None else 'unresolved'}",
                f"Agent: {agent_context.agent_name if agent_context is not None else 'unresolved'}",
            ]
        )
    return _emit("self identity", options, payload, diagnostics, lines)


def _cmd_self_location(options: CliOptions) -> int:
    project, diagnostics = _discover(options)
    location = None
    if project is not None:
        location, location_diagnostics = resolve_ambient_workspace_location(
            project,
            cwd=Path.cwd(),
            env=os.environ,
        )
        diagnostics.extend(location_diagnostics)
    payload = build_self_location_payload(location, diagnostics=diagnostics)
    lines = ["Self Location"]
    if location is not None:
        lines.extend(
            [
                f"Cwd: {location.cwd}",
                f"Workspace Kind: {location.workspace_kind.value}",
                f"Workspace Root: {location.workspace_root or 'unresolved'}",
                f"Research Topic: {location.research_topic_id or 'none'}",
                f"Worker: {location.worker_kind + ':' + location.worker_name if location.worker_kind and location.worker_name else 'none'}",
            ]
        )
    return _emit("self location", options, payload, diagnostics, lines)


def _cmd_self_check(options: CliOptions, *, scope: str) -> int:
    operation_scope = OperationScope(scope)
    context = None
    topic_actor_context = None
    agent_context = None
    if operation_scope is OperationScope.PROJECT:
        project, diagnostics = _discover(options)
    else:
        context, diagnostics = _context_for_options(options)
        project = context.project if context is not None else None
        if context is not None:
            if operation_scope is OperationScope.TOPIC_ACTOR:
                topic_actor_context, worker_diagnostics = resolve_effective_topic_actor_context(
                    context,
                    env=os.environ,
                    cwd=Path.cwd(),
                    explicit_topic_actor_name=_value(options, "topic_actor_name"),
                )
                diagnostics.extend(worker_diagnostics)
            elif operation_scope is OperationScope.AGENT:
                agent_context, worker_diagnostics = resolve_effective_agent_context(
                    context,
                    env=os.environ,
                    cwd=Path.cwd(),
                    explicit_agent_name=_value(options, "agent_name"),
                    explicit_agent_instance_id=_value(options, "agent_instance_id"),
                )
                diagnostics.extend(worker_diagnostics)
        if project is None:
            project, discovery_diagnostics = _discover(options)
            diagnostics.extend(discovery_diagnostics)

    location = None
    alignment = None
    if project is not None:
        location, location_diagnostics = resolve_ambient_workspace_location(
            project,
            cwd=Path.cwd(),
            env=os.environ,
        )
        diagnostics.extend(location_diagnostics)
        alignment, alignment_diagnostics = resolve_task_context_alignment(
            project,
            scope=operation_scope,
            ambient_location=location,
            context=context,
            topic_actor_context=topic_actor_context,
            agent_context=agent_context,
            explicit_topic_selection=_topic_selector_requested(options),
            explicit_worker_selection=(
                operation_scope is OperationScope.TOPIC_ACTOR
                and _value(options, "topic_actor_name") is not None
            )
            or (
                operation_scope is OperationScope.AGENT
                and (_value(options, "agent_name") is not None or _value(options, "agent_instance_id") is not None)
            ),
        )
        diagnostics.extend(alignment_diagnostics)

    payload = build_self_check_payload(alignment, diagnostics=diagnostics)
    lines = ["Self Context Check"]
    if alignment is not None:
        target = alignment.selected_target
        lines.extend(
            [
                f"Scope: {alignment.requested_scope.value}",
                f"Target: {_alignment_target_text(target)}",
                f"Source: {_alignment_source_text(target)}",
                f"Ambient: {alignment.ambient_location.workspace_kind.value}",
                f"Verdict: {alignment.verdict.value}",
            ]
        )
        if alignment.expected_cwd is not None:
            lines.append(f"Expected Cwd: {alignment.expected_cwd}")
        if alignment.blocking and alignment.reasons:
            lines.append(f"Action: {alignment.reasons[0]}")
    return _emit("self check", options, payload, diagnostics, lines)


def _alignment_target_text(target: Any) -> str:
    if target is None:
        return "unresolved"
    values = [target.research_topic_id, target.worker_name]
    selected = [value for value in values if value]
    return "/".join(selected) if selected else str(target.project_root)


def _alignment_source_text(target: Any) -> str:
    if target is None or not target.sources:
        return "unresolved"
    return ", ".join(f"{key}={value}" for key, value in sorted(target.sources.items()))


def _cmd_self_pixi(options: CliOptions) -> int:
    context, diagnostics = _context_for_options(options)
    payload = build_self_pixi_payload(context, diagnostics=diagnostics)
    pixi = payload.get("pixi", {})
    lines = ["Self Pixi"]
    if isinstance(pixi, dict):
        selected = pixi.get("selected")
        command = pixi.get("python_command")
        if isinstance(selected, dict):
            lines.append(f"Manifest: {selected.get('manifest_path_display', selected.get('manifest_path'))}")
            lines.append(f"Environment: {selected.get('pixi_environment')}")
        else:
            lines.append("Selected Pixi binding: unresolved")
        if command is not None:
            lines.append(f"Python: {command}")
    return _emit("self pixi", options, payload, diagnostics, lines)


def _cmd_self_env(options: CliOptions, *, include_values: bool) -> int:
    context, diagnostics = _context_for_options(options)
    payload = build_self_env_payload(context, diagnostics=diagnostics, env=os.environ, include_values=include_values)
    environment = payload.get("environment", {})
    lines = ["Self Environment"]
    if isinstance(environment, dict):
        recognized = environment.get("recognized", [])
        present = 0
        total = 0
        if isinstance(recognized, list):
            total = len(recognized)
            present = sum(1 for entry in recognized if isinstance(entry, dict) and bool(entry.get("present")))
        lines.append(f"Recognized inputs present: {present}/{total}")
        lines.append(f"Values included: {bool(environment.get('values_included'))}")
    return _emit("self env", options, payload, diagnostics, lines)


def _cmd_self_paths(options: CliOptions, semantic_labels: tuple[str, ...]) -> int:
    if not semantic_labels:
        diagnostics = [
            Diagnostic(
                code="ISO088",
                severity="error",
                concept="Agent Self Paths Query",
                field="semantic_label",
                message="project self paths requires at least one semantic label.",
                usage="isomer-cli --print-json project self paths topic.repos.main",
            )
        ]
        payload = {"ok": False, "mutated": False, "semantic_paths": []}
        return _emit("self paths", options, payload, diagnostics, [])

    guard_label = None if any(_path_label_requires_selected_topic(label) for label in semantic_labels) else semantic_labels[0]
    context, diagnostics = _context_for_path_options(options, guard_label)
    payload = build_self_paths_payload(
        context,
        diagnostics=diagnostics,
        env=os.environ,
        cwd=Path.cwd(),
        semantic_labels=semantic_labels,
        agent_name=_value(options, "agent_name"),
        agent_instance_id=_value(options, "agent_instance_id"),
        topic_actor_name=_value(options, "topic_actor_name"),
    )
    lines = ["Self Paths"]
    semantic_paths = payload.get("semantic_paths", [])
    if isinstance(semantic_paths, list):
        for entry in semantic_paths:
            if not isinstance(entry, dict):
                continue
            path_data = entry.get("path")
            if isinstance(path_data, dict):
                lines.append(f"{entry.get('semantic_label')}: {path_data.get('path')}")
            else:
                lines.append(f"{entry.get('semantic_label')}: unresolved")
    return _emit("self paths", options, payload, diagnostics, lines)


def _cmd_self_queries(options: CliOptions) -> int:
    context, diagnostics = _context_for_options(options)
    payload = build_self_queries_payload(context, diagnostics=diagnostics)
    lines = ["Self Queries"]
    queries = payload.get("queries", [])
    if isinstance(queries, list):
        for entry in queries:
            if isinstance(entry, dict) and entry.get("command"):
                lines.append(f"- {entry['command']}")
    return _emit("self queries", options, payload, diagnostics, lines)

__all__ = [
    "_cmd_self_show",
    "_cmd_self_identity",
    "_cmd_self_location",
    "_cmd_self_check",
    "_cmd_self_pixi",
    "_cmd_self_env",
    "_cmd_self_paths",
    "_cmd_self_queries",
]
