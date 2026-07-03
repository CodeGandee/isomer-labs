"""Topic Workspace CLI command handlers."""

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
from isomer_labs.cli.handlers.workspace_paths import (
    _render_topic_main_guidance_summary,
    _resolve_topic_main_guidance_repo,
)

def _cmd_workspaces_list(options: CliOptions) -> int:
    project, diagnostics = _discover(options)
    workspaces: list[dict[str, object]] = []
    if project is not None:
        state = build_project_state(project)
        diagnostics.extend(state.diagnostics)
        seen_workspace_ids: set[str] = set()
        for workspace in project.manifest.topic_workspaces:
            seen_workspace_ids.add(workspace.id)
            effective_path = workspace.path_input
            if effective_path is None and workspace.research_topic_id is not None:
                effective_path = display_path(
                    default_topic_workspace_path(project.root, workspace.research_topic_id, project.manifest.path_defaults),
                    project.root,
                )
            workspaces.append(
                {
                    **workspace.to_json(),
                    "source": "Project Manifest",
                    "effective_path": effective_path,
                }
            )
        for topic in project.manifest.research_topics:
            has_registered_workspace = (
                topic.topic_workspace_id in seen_workspace_ids
                if topic.topic_workspace_id is not None
                else any(workspace.get("research_topic_id") == topic.id for workspace in workspaces)
            )
            if not has_registered_workspace:
                path_input = display_path(
                    default_topic_workspace_path(project.root, topic.id, project.manifest.path_defaults),
                    project.root,
                )
                workspaces.append(
                    {
                        "id": topic.id,
                        "research_topic_id": topic.id,
                        "path": path_input,
                        "schema_version": "isomer-topic-workspace.v1",
                        "status": "active",
                        "source": "default",
                        "effective_path": path_input,
                    }
                )
    payload = {"workspaces": workspaces}
    lines = ["Topic Workspaces"]
    lines.extend(
        f"- {workspace['id']} (topic: {workspace['research_topic_id']}, path: {workspace['effective_path']}, source: {workspace['source']})"
        for workspace in workspaces
    )
    return _emit("workspaces list", options, payload, diagnostics, lines)


def _cmd_topic_actors_list(options: CliOptions) -> int:
    context, diagnostics = _context_for_path_options(options)
    payload: dict[str, Any] = {"ok": False, "mutated": False, "topic_actors": []}
    if context is not None:
        payload, actor_diagnostics = list_topic_actors(context)
        diagnostics.extend(actor_diagnostics)
    lines = ["Topic Actors"]
    for actor in payload.get("topic_actors", []):
        if isinstance(actor, dict):
            lines.append(f"- {actor.get('topic_actor_name')} ({actor.get('runtime_kind')}, {actor.get('status')})")
    return _emit("topic-actors list", options, payload, diagnostics, lines)


def _cmd_topic_actors_show(options: CliOptions, topic_actor_name: str) -> int:
    context, diagnostics = _context_for_path_options(options)
    payload: dict[str, Any] = {"ok": False, "mutated": False, "topic_actor": None}
    if context is not None:
        payload, actor_diagnostics = show_topic_actor(context, topic_actor_name)
        diagnostics.extend(actor_diagnostics)
    actor = payload.get("topic_actor")
    lines = []
    if isinstance(actor, dict):
        lines = [
            f"Topic Actor: {actor.get('topic_actor_name')}",
            f"Workspace label: {actor.get('workspace_label')}",
            f"Branch: {actor.get('branch')}",
        ]
    return _emit("topic-actors show", options, payload, diagnostics, lines)


def _cmd_topic_actors_register(
    options: CliOptions,
    topic_actor_name: str,
    *,
    actor_kind: str | None,
    runtime_kind: str | None,
    role_kind: str | None,
    controller_kind: str | None,
    controller_ref: str | None,
    workspace_path: str | None,
    branch: str | None,
    adapter_ref: str | None,
    status: str,
    replace_existing: bool,
    materialize: bool,
) -> int:
    context, diagnostics = _context_for_path_options(options)
    payload: dict[str, Any] = {"ok": False, "mutated": False, "topic_actor": None}
    if context is not None:
        payload, actor_diagnostics = register_topic_actor(
            context,
            env=os.environ,
            topic_actor_name=topic_actor_name,
            actor_kind=actor_kind,
            runtime_kind=runtime_kind,
            role_kind=role_kind,
            controller_kind=controller_kind,
            controller_ref=controller_ref,
            workspace_path=workspace_path,
            branch=branch,
            adapter_ref=adapter_ref,
            status=status,
            replace_existing=replace_existing,
            materialize=materialize,
        )
        diagnostics.extend(actor_diagnostics)
    lines = [f"Registered Topic Actor: {topic_actor_name}"] if payload.get("topic_actor") is not None else []
    return _emit("topic-actors register", options, payload, diagnostics, lines)


def _cmd_topic_actors_update(
    options: CliOptions,
    topic_actor_name: str,
    *,
    actor_kind: str | None,
    runtime_kind: str | None,
    role_kind: str | None,
    controller_kind: str | None,
    controller_ref: str | None,
    workspace_path: str | None,
    branch: str | None,
    adapter_ref: str | None,
    status: str | None,
) -> int:
    context, diagnostics = _context_for_path_options(options)
    payload: dict[str, Any] = {"ok": False, "mutated": False, "topic_actor": None}
    if context is not None:
        payload, actor_diagnostics = update_topic_actor(
            context,
            env=os.environ,
            topic_actor_name=topic_actor_name,
            actor_kind=actor_kind,
            runtime_kind=runtime_kind,
            role_kind=role_kind,
            controller_kind=controller_kind,
            controller_ref=controller_ref,
            workspace_path=workspace_path,
            branch=branch,
            adapter_ref=adapter_ref,
            status=status,
        )
        diagnostics.extend(actor_diagnostics)
    lines = [f"Updated Topic Actor: {topic_actor_name}"] if payload.get("topic_actor") is not None else []
    return _emit("topic-actors update", options, payload, diagnostics, lines)


def _cmd_topic_actors_archive(options: CliOptions, topic_actor_name: str) -> int:
    context, diagnostics = _context_for_path_options(options)
    payload: dict[str, Any] = {"ok": False, "mutated": False, "topic_actor": None}
    if context is not None:
        payload, actor_diagnostics = archive_topic_actor(context, env=os.environ, topic_actor_name=topic_actor_name)
        diagnostics.extend(actor_diagnostics)
    lines = [f"Archived Topic Actor: {topic_actor_name}"] if payload.get("topic_actor") is not None else []
    return _emit("topic-actors archive", options, payload, diagnostics, lines)


def _cmd_topic_actors_materialize(
    options: CliOptions,
    topic_actor_name: str,
    *,
    source_repo: str | None,
    command_name: str = "topic-actors materialize",
) -> int:
    context, diagnostics = _context_for_path_options(options)
    payload: dict[str, Any] = {"ok": False, "mutated": False, "materialization": None}
    if context is not None:
        payload, actor_diagnostics = materialize_topic_actor_workspace(
            context,
            env=os.environ,
            topic_actor_name=topic_actor_name,
            source_repo=source_repo,
        )
        diagnostics.extend(actor_diagnostics)
    lines: list[str] = []
    materialization = payload.get("materialization")
    if isinstance(materialization, dict):
        workspace = materialization.get("workspace")
        if isinstance(workspace, dict):
            lines.append(f"Topic Actor Workspace: {workspace.get('path')}")
        lines.append(f"Branch: {materialization.get('branch')}")
    return _emit(command_name, options, payload, diagnostics, lines)


def _cmd_topic_actors_diagnose(options: CliOptions, topic_actor_name: str | None) -> int:
    context, diagnostics = _context_for_path_options(options)
    payload: dict[str, Any] = {"ok": False, "mutated": False, "topic_actors": [], "actor_paths": []}
    if context is not None:
        payload, actor_diagnostics = diagnose_topic_actor(context, env=os.environ, topic_actor_name=topic_actor_name)
        diagnostics.extend(actor_diagnostics)
    lines = ["Topic Actor Diagnostics"]
    for item in payload.get("actor_paths", []):
        if isinstance(item, dict):
            lines.append(f"- {item.get('semantic_label')}: {item.get('path')}")
    return _emit("topic-actors diagnose", options, payload, diagnostics, lines)


def _cmd_topic_main_guidance_render(options: CliOptions) -> int:
    rendered = render_topic_main_guidance_block()
    payload = {
        "ok": True,
        "mutated": False,
        "guidance": guidance_metadata(),
        "rendered": rendered,
    }
    return _emit("topic-main-guidance render", options, payload, [], [rendered.rstrip()])


def _cmd_topic_main_guidance_inspect(options: CliOptions) -> int:
    repo_path, diagnostics = _resolve_topic_main_guidance_repo(options)
    if repo_path is None:
        payload: dict[str, Any] = {
            "ok": False,
            "mutated": False,
            "guidance": guidance_metadata(),
            "topic_main_repo": None,
            "targets": [],
            "changed_files": [],
        }
    else:
        payload, guidance_diagnostics = inspect_topic_main_guidance(repo_path)
        diagnostics.extend(guidance_diagnostics)
        payload["ok"] = not has_errors(diagnostics)
    lines = _render_topic_main_guidance_summary("Topic Main Guidance", payload)
    return _emit("topic-main-guidance inspect", options, payload, diagnostics, lines)


def _cmd_topic_main_guidance_ensure(options: CliOptions, *, approved: bool) -> int:
    if not approved:
        diagnostics = [
            Diagnostic(
                code="ISO087",
                severity="error",
                concept="Topic Main Guidance",
                field="--yes",
                message="Guidance ensure requires explicit --yes confirmation before writing AGENTS.md or CLAUDE.md.",
                usage="isomer-cli project topic-main-guidance ensure --topic <topic> --yes",
            )
        ]
        payload: dict[str, Any] = {
            "ok": False,
            "mutated": False,
            "guidance": guidance_metadata(),
            "topic_main_repo": None,
            "targets": [],
            "changed_files": [],
        }
        return _emit("topic-main-guidance ensure", options, payload, diagnostics, [])
    repo_path, diagnostics = _resolve_topic_main_guidance_repo(options)
    if repo_path is None:
        payload = {
            "ok": False,
            "mutated": False,
            "guidance": guidance_metadata(),
            "topic_main_repo": None,
            "targets": [],
            "changed_files": [],
        }
    else:
        payload, guidance_diagnostics = ensure_topic_main_guidance(repo_path)
        diagnostics.extend(guidance_diagnostics)
        payload["ok"] = not has_errors(diagnostics)
    lines = _render_topic_main_guidance_summary("Topic Main Guidance Ensure", payload)
    return _emit("topic-main-guidance ensure", options, payload, diagnostics, lines)
__all__ = [
    "_cmd_workspaces_list",
    "_cmd_topic_actors_list",
    "_cmd_topic_actors_show",
    "_cmd_topic_actors_register",
    "_cmd_topic_actors_update",
    "_cmd_topic_actors_archive",
    "_cmd_topic_actors_materialize",
    "_cmd_topic_actors_diagnose",
    "_cmd_topic_main_guidance_render",
    "_cmd_topic_main_guidance_inspect",
    "_cmd_topic_main_guidance_ensure",
]
