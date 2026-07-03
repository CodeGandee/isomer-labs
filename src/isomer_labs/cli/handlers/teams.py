"""Team Repository, Template, and Profile CLI command handlers."""

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


def _cmd_team_templates_list(options: CliOptions) -> int:
    project, diagnostics = _discover_optional(options)
    templates = []
    for registration in discover_domain_agent_team_templates(project):
        report = validate_domain_agent_team_template(project, registration, include_harness=False)
        diagnostics.extend(report.diagnostics)
        templates.append(
            {
                "id": registration.id,
                "source_kind": registration.source_kind,
                "source_path": str(resolve_template_source_path(project, registration)),
                "team_repository_id": registration.team_repository_id,
                "validation_status": "valid" if report.ok else "invalid",
            }
        )
    payload = {"templates": sorted(templates, key=lambda item: str(item["id"]))}
    lines = ["Domain Agent Team Templates"]
    if not payload["templates"]:
        lines.append("No Domain Agent Team Templates are configured. Add Project registrations or configure Team Repositories.")
    lines.extend(
        f"- {template['id']} ({template['source_kind']}, {template['validation_status']}) {template['source_path']}"
        for template in payload["templates"]
    )
    return _emit("team-templates list", options, payload, diagnostics, lines)


def _cmd_team_templates_inspect(options: CliOptions, template_id: str) -> int:
    project, diagnostics = _discover_optional(options)
    registration = find_domain_agent_team_template(template_id, project)
    if registration is None:
        diagnostics.append(_unknown_template_diagnostic(template_id))
        return _emit("team-templates inspect", options, {"template": None}, diagnostics, [])
    report = validate_domain_agent_team_template(project, registration, include_harness=False)
    diagnostics.extend(report.diagnostics)
    payload = {"template": report.template.to_json() if report.template is not None else None}
    lines: list[str] = []
    if report.template is not None:
        lines = [
            f"Domain Agent Team Template: {report.template.id}",
            f"Source: {report.template.source_path}",
            "Agent Roles",
            *[f"- {role.id} ({role.role_kind}, required={role.required}, scalable={role.scalable})" for role in report.template.roles],
            "Workflow Stages",
            *[f"- {route.workflow_stage}: {route.owner_role}" for route in report.template.workflow_stage_routes],
        ]
    return _emit("team-templates inspect", options, payload, diagnostics, lines)


def _cmd_team_templates_validate(options: CliOptions, template_id: str) -> int:
    project, diagnostics = _discover_optional(options)
    registration = find_domain_agent_team_template(template_id, project)
    if registration is None:
        diagnostics.append(_unknown_template_diagnostic(template_id))
        return _emit("team-templates validate", options, {"ok": False, "template": None}, diagnostics, [])
    report = validate_domain_agent_team_template(project, registration, include_harness=True)
    diagnostics.extend(report.diagnostics)
    payload = {
        "ok": report.ok,
        "template": report.template.to_json() if report.template is not None else None,
    }
    lines = [f"Domain Agent Team Template {template_id} valid."] if report.ok else []
    return _emit("team-templates validate", options, payload, diagnostics, lines)


def _cmd_team_templates_register(
    options: CliOptions,
    template_id: str,
    *,
    repository_id: str | None,
    write_registration: bool,
) -> int:
    project, diagnostics = _discover(options)
    if project is None:
        return _emit("team-templates register", options, {"registration": None, "mutated": False}, diagnostics, [])
    repositories = discover_team_repositories(project, os.environ)
    for repository in repositories:
        diagnostics.extend(repository.diagnostics)
    candidate = None
    for repository in repositories:
        if repository_id is not None and repository.id != repository_id:
            continue
        for template in repository.templates:
            if template.id == template_id:
                candidate = (repository, template)
                break
        if candidate is not None:
            break
    if candidate is None:
        diagnostics.append(_unknown_template_diagnostic(template_id))
        return _emit("team-templates register", options, {"registration": None, "mutated": False}, diagnostics, [])
    repository, template = candidate
    registration = {
        "id": template.id,
        "source_path": template.source_path_input or str(resolve_template_source_path(project, template)),
        "source_kind": "team-repository",
        "team_repository_id": repository.id,
        "status": "active",
    }
    mutated = False
    if write_registration and not has_errors(diagnostics):
        if any(item.id == template.id and item.status != "archived" for item in project.manifest.domain_agent_team_templates):
            diagnostics.append(
                Diagnostic(
                    code="ISO004",
                    severity="error",
                    concept="Domain Agent Team Template registration",
                    path=project.manifest_path,
                    field="domain_agent_team_templates.id",
                    message=f"Domain Agent Team Template is already registered in the Project Manifest: {template.id}.",
                )
            )
        else:
            _append_template_registration(project.manifest_path, registration)
            mutated = True
    payload = {"registration": registration, "mutated": mutated}
    lines = [f"Domain Agent Team Template registration: {template.id} from {repository.id}"]
    if mutated:
        lines.append(f"Updated: {project.manifest_path}")
    return _emit("team-templates register", options, payload, diagnostics, lines)


def _cmd_team_repositories_list(options: CliOptions) -> int:
    project, diagnostics = _discover_optional(options)
    repositories = discover_team_repositories(project, os.environ)
    payload = {"team_repositories": [repository.to_json() for repository in repositories]}
    for repository in repositories:
        diagnostics.extend(repository.diagnostics)
    lines = ["Team Repositories"]
    if not repositories:
        lines.append("No Team Repositories are configured.")
    lines.extend(
        f"- {repository.id} ({repository.status}, templates={len(repository.templates)}) {repository.root}"
        for repository in repositories
    )
    return _emit("team-repositories list", options, payload, diagnostics, lines)


def _cmd_team_repositories_inspect(options: CliOptions, repository_id: str) -> int:
    project, diagnostics = _discover_optional(options)
    repositories = discover_team_repositories(project, os.environ)
    repository = next((item for item in repositories if item.id == repository_id), None)
    if repository is None:
        diagnostics.append(
            Diagnostic(
                code="ISO016",
                severity="error",
                concept="Team Repository",
                field="team_repository_id",
                message=f"Unknown Team Repository: {repository_id}.",
            )
        )
        return _emit("team-repositories inspect", options, {"team_repository": None}, diagnostics, [])
    diagnostics.extend(repository.diagnostics)
    lines = [
        f"Team Repository: {repository.id}",
        f"Root: {repository.root}",
        "Templates",
        *[f"- {template.id}: {template.source_path_input}" for template in repository.templates],
    ]
    return _emit("team-repositories inspect", options, {"team_repository": repository.to_json()}, diagnostics, lines)


def _cmd_team_profiles_specialize(
    options: CliOptions,
    *,
    template_id: str | None = None,
    profile_id: str | None = None,
    roles: Sequence[str] = (),
    expected_artifacts: Sequence[str] = (),
    use_case: str | None = None,
    write_profile: bool = False,
) -> int:
    context, diagnostics = _context_for_options(options)
    if context is None:
        return _emit("team-profiles specialize", options, {"profile": None}, diagnostics, [])
    selected_template_id = template_id or context.domain_agent_team_template_id
    if selected_template_id is None:
        diagnostics.append(_missing_template_diagnostic())
        return _emit("team-profiles specialize", options, {"profile": None}, diagnostics, [])
    registration = find_domain_agent_team_template(selected_template_id, context.project)
    if registration is None:
        diagnostics.append(_unknown_template_diagnostic(selected_template_id))
        return _emit("team-profiles specialize", options, {"profile": None}, diagnostics, [])
    template_report = validate_domain_agent_team_template(context.project, registration, include_harness=False)
    diagnostics.extend(template_report.diagnostics)
    if template_report.template is None:
        return _emit("team-profiles specialize", options, {"profile": None}, diagnostics, [])
    profile = specialize_topic_agent_team_profile(
        context,
        template_report.template,
        profile_id=profile_id,
        selected_role_ids=list(roles) or None,
        expected_artifacts=list(expected_artifacts) or None,
        use_case=use_case,
    )
    profile_report = validate_topic_agent_team_profile(profile, template_report.template, project=context.project)
    diagnostics.extend(profile_report.diagnostics)
    written_path = None
    registration_suggestion: dict[str, str] | None = None
    if write_profile and not has_errors(diagnostics):
        profile.source_path.parent.mkdir(parents=True, exist_ok=True)
        profile.source_path.write_text(profile_to_toml(profile), encoding="utf-8")
        written_path = str(profile.source_path)
        registration_suggestion = _profile_registration_suggestion(context.project.root, profile)
    payload = {
        "profile": profile.to_json(),
        "materialization": "preview",
        "validation": profile_report.to_json(),
        "written_path": written_path,
        "registration_suggestion": registration_suggestion,
    }
    lines = [
        f"Topic Agent Team Profile preview: {profile.id}",
        f"Template: {profile.domain_agent_team_template_id}",
        f"Research Topic: {profile.research_topic_id}",
    ]
    if written_path is not None:
        lines.append(f"Written: {written_path}")
        if registration_suggestion is not None:
            lines.append(
                "Registration suggestion: add [[topic_agent_team_profiles]] "
                f'id="{registration_suggestion["id"]}" '
                f'path="{registration_suggestion["path"]}" '
                f'domain_agent_team_template_id="{registration_suggestion["domain_agent_team_template_id"]}" '
                f'research_topic_id="{registration_suggestion["research_topic_id"]}".'
            )
    return _emit("team-profiles specialize", options, payload, diagnostics, lines)


def _cmd_team_profiles_materialize(
    options: CliOptions,
    *,
    packet_path: str,
    template_id: str | None = None,
    write_bundle: bool = False,
    overwrite: bool = False,
) -> int:
    context, diagnostics = _context_for_options(options)
    if context is None:
        return _emit("team-profiles materialize", options, {"materialization": None, "ok": False}, diagnostics, [])
    packet_file = _resolve_cli_path(context.project.root, packet_path)
    raw, load_diagnostics = load_toml(packet_file, "Topic Team Instantiation Packet")
    diagnostics.extend(load_diagnostics)
    packet = None
    if raw is not None:
        packet, parse_diagnostics = parse_topic_team_instantiation_packet(packet_file, raw)
        diagnostics.extend(parse_diagnostics)
    selected_template_id = template_id or (packet.source_template_ref if packet is not None else None) or context.domain_agent_team_template_id
    if selected_template_id is None:
        diagnostics.append(_missing_template_diagnostic())
        return _emit("team-profiles materialize", options, {"materialization": None, "ok": False}, diagnostics, [])
    registration = find_domain_agent_team_template(selected_template_id, context.project)
    if registration is None:
        diagnostics.append(_unknown_template_diagnostic(selected_template_id))
        return _emit("team-profiles materialize", options, {"materialization": None, "ok": False}, diagnostics, [])
    template_report = validate_domain_agent_team_template(context.project, registration, include_harness=False)
    diagnostics.extend(template_report.diagnostics)
    if packet is None or template_report.template is None:
        return _emit("team-profiles materialize", options, {"materialization": None, "ok": False}, diagnostics, [])
    result = materialize_topic_agent_team_profile_bundle(
        context,
        template_report.template,
        packet,
        write=write_bundle,
        overwrite=overwrite,
    )
    diagnostics.extend(result.diagnostics)
    payload = {
        "ok": not has_errors(diagnostics),
        "mutated": result.written,
        "materialization": result.to_json(),
        "registration_suggestion": (
            _profile_registration_suggestion(context.project.root, result.profile)
            if result.profile is not None and not has_errors(diagnostics)
            else None
        ),
    }
    lines = [
        f"Topic Agent Team Profile Bundle: {result.bundle_path}",
        f"Profile: {result.profile_path}",
        f"Written: {str(result.written).lower()}",
    ]
    return _emit("team-profiles materialize", options, payload, diagnostics, lines)


def _cmd_team_profiles_validate(
    options: CliOptions,
    *,
    template_id: str | None = None,
    profile_path: str | None = None,
) -> int:
    project, diagnostics = _discover_optional(options)
    path = _resolve_profile_cli_path(project, profile_path, diagnostics)
    if path is None:
        return _emit("team-profiles validate", options, {"profile": None, "ok": False}, diagnostics, [])
    raw, load_diagnostics = load_toml(path, "Topic Agent Team Profile")
    diagnostics.extend(load_diagnostics)
    profile = None
    if raw is not None:
        profile, parse_diagnostics = parse_topic_agent_team_profile(path, raw)
        diagnostics.extend(parse_diagnostics)
    selected_template_id = template_id or (profile.domain_agent_team_template_id if profile is not None else None)
    if selected_template_id is None:
        diagnostics.append(_missing_template_diagnostic())
        report = validate_topic_agent_team_profile(profile, None, project=project, source_path=path)
        diagnostics.extend(report.diagnostics)
        payload = {
            "ok": False,
            "profile": profile.to_json() if profile is not None else None,
            "validation": report.to_json(),
        }
        return _emit("team-profiles validate", options, payload, diagnostics, [])
    registration = find_domain_agent_team_template(selected_template_id, project)
    template = None
    if registration is None:
        diagnostics.append(_unknown_template_diagnostic(selected_template_id))
    else:
        template_report = validate_domain_agent_team_template(project, registration, include_harness=False)
        diagnostics.extend(template_report.diagnostics)
        template = template_report.template
    report = validate_topic_agent_team_profile(profile, template, project=project, source_path=path)
    diagnostics.extend(report.diagnostics)
    payload = {
        "ok": report.ok and not has_errors(diagnostics),
        "profile": profile.to_json() if profile is not None else None,
        "validation": report.to_json(),
    }
    lines = [f"Topic Agent Team Profile {profile.id} valid."] if profile is not None and payload["ok"] else []
    return _emit("team-profiles validate", options, payload, diagnostics, lines)

__all__ = [
    "_cmd_team_templates_list",
    "_cmd_team_templates_inspect",
    "_cmd_team_templates_validate",
    "_cmd_team_templates_register",
    "_cmd_team_repositories_list",
    "_cmd_team_repositories_inspect",
    "_cmd_team_profiles_specialize",
    "_cmd_team_profiles_materialize",
    "_cmd_team_profiles_validate",
]
