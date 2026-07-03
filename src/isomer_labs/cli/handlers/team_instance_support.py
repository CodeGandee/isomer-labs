"""Support helpers for Agent Team Instance CLI handlers."""

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

@dataclass(frozen=True)
class _LoadedManifestSet:
    paths: Any
    link_manifest: dict[str, object] | None
    launch_material_manifest: dict[str, object] | None
    runtime_manifest: dict[str, object] | None
    link_path: Path | None
    launch_material_path: Path | None
    runtime_path: Path | None


def _agent_team_summary_or_diagnostic(
    store: Any,
    context: EffectiveTopicContext,
    agent_team_instance_id: str,
    diagnostics: list[Diagnostic],
) -> Any | None:
    summary = store.get_agent_team_instance_summary(agent_team_instance_id)
    if summary is None:
        diagnostics.append(
            Diagnostic(
                code="ISO041",
                severity="error",
                concept="Agent Team Instance",
                field="agent_team_instance_id",
                message=f"Unknown Agent Team Instance: {agent_team_instance_id}.",
            )
        )
        return None
    if summary.agent_team_instance.topic_workspace_id != context.topic_workspace_id:
        diagnostics.append(
            Diagnostic(
                code="ISO041",
                severity="error",
                concept="Agent Team Instance",
                field="agent_team_instance_id",
                message="Agent Team Instance belongs to another Topic Workspace.",
            )
        )
        return None
    return summary


def _agent_bindings_from_summary(summary: Any) -> list[AgentBinding]:
    return [
        AgentBinding(
            agent_instance_id=record.id,
            agent_role_id=record.agent_role_id,
            houmao_profile=record.agent_role_id,
            houmao_agent_name=record.agent_role_id,
            mapping_confidence="manual",
        )
        for record in summary.agent_instances
    ]


def _operator_provenance_from_summary(summary: Any, actor_ref: str | None) -> dict[str, object]:
    team = summary.agent_team_instance
    data: dict[str, object] = {}
    if actor_ref:
        data["actor_ref"] = actor_ref
    for key in (
        "topic_agent_team_profile_bundle_ref",
        "instantiation_packet_ref",
        "approval_ref",
        "project_operator_ref",
    ):
        value = getattr(team, key, None)
        if value:
            data[key] = value
    for key in ("topic_service_agent_refs", "validation_refs"):
        value = getattr(team, key, None)
        if value:
            data[key] = list(value)
    return data


def _manifest_output_path(
    context: EffectiveTopicContext,
    agent_team_instance_id: str = "",
    output_path: str | None = None,
    manifest_kind: str = "",
) -> Path:
    if output_path is not None:
        path = Path(output_path)
        if path.is_absolute():
            return path.expanduser().resolve(strict=False)
        return (context.project.root / path).expanduser().resolve(strict=False)
    paths = manifest_paths(context.topic_workspace_path, agent_team_instance_id)
    if manifest_kind == ManifestKind.ADAPTER_LINK.value:
        return paths.adapter_link
    if manifest_kind == ManifestKind.LAUNCH_MATERIAL.value:
        return paths.launch_material
    return paths.adapter_runtime


def _load_manifest_set(
    context: EffectiveTopicContext,
    *,
    agent_team_instance_id: str = "",
    link_manifest: str | None = None,
    launch_material_manifest: str | None = None,
    runtime_manifest: str | None = None,
    diagnostics: list[Diagnostic],
    require_link: bool = False,
) -> _LoadedManifestSet:
    paths = manifest_paths(context.topic_workspace_path, agent_team_instance_id)
    link_path = _resolve_manifest_cli_path(context, link_manifest, paths.adapter_link)
    launch_path = _resolve_manifest_cli_path(context, launch_material_manifest, paths.launch_material)
    runtime_path = _resolve_manifest_cli_path(context, runtime_manifest, paths.adapter_runtime)
    link_doc = _load_manifest_if_present(
        link_path,
        expected_kind=ManifestKind.ADAPTER_LINK.value,
        diagnostics=diagnostics,
        required=require_link,
    )
    launch_doc = _load_manifest_if_present(
        launch_path,
        expected_kind=ManifestKind.LAUNCH_MATERIAL.value,
        diagnostics=diagnostics,
        required=False,
    )
    runtime_doc = _load_manifest_if_present(
        runtime_path,
        expected_kind=ManifestKind.ADAPTER_RUNTIME.value,
        diagnostics=diagnostics,
        required=False,
    )
    return _LoadedManifestSet(
        paths=paths,
        link_manifest=link_doc,
        launch_material_manifest=launch_doc,
        runtime_manifest=runtime_doc,
        link_path=link_path,
        launch_material_path=launch_path,
        runtime_path=runtime_path,
    )


def _resolve_manifest_cli_path(
    context: EffectiveTopicContext,
    value: str | None,
    default: Path,
) -> Path:
    if value is None:
        return default.resolve(strict=False)
    path = Path(value)
    if path.is_absolute():
        return path.expanduser().resolve(strict=False)
    return (context.project.root / path).expanduser().resolve(strict=False)


def _load_manifest_if_present(
    path: Path,
    *,
    expected_kind: str = "",
    diagnostics: list[Diagnostic],
    required: bool = False,
) -> dict[str, object] | None:
    if not path.exists():
        if required:
            diagnostics.append(_manifest_error_diagnostic(f"Required manifest does not exist: {path}.", path=path))
        return None
    try:
        return load_json_manifest(path, expected_kind=expected_kind)
    except ManifestValidationError as exc:
        diagnostics.append(_manifest_error_diagnostic(str(exc), path=path))
        return None


def _load_or_collect_live_state(
    context: EffectiveTopicContext,
    *,
    live_state_json: str | None = None,
    houmao_project_dir: str | None = None,
    link_manifest: dict[str, object] | None,
) -> tuple[dict[str, object], list[Diagnostic]]:
    if live_state_json is not None:
        path = _resolve_manifest_cli_path(context, live_state_json, Path(live_state_json))
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError) as exc:
            return {"available": False, "agents": []}, [
                Diagnostic(
                    code="ISO063",
                    severity="error",
                    concept="Houmao adapter reconciliation",
                    path=path,
                    message=f"Live-state JSON could not be read: {exc}.",
                )
            ]
        if not isinstance(loaded, dict):
            return {"available": False, "agents": []}, [
                Diagnostic(
                    code="ISO063",
                    severity="error",
                    concept="Houmao adapter reconciliation",
                    path=path,
                    message="Live-state JSON root must be an object.",
                )
            ]
        return loaded, []
    project_dir = _resolve_optional_path(context.project.root, houmao_project_dir)
    if project_dir is None and link_manifest is not None:
        houmao_payload = link_manifest.get("houmao")
        if isinstance(houmao_payload, dict) and isinstance(houmao_payload.get("project_dir"), str):
            project_dir = Path(str(houmao_payload["project_dir"])).expanduser().resolve(strict=False)
    if project_dir is None:
        project_dir = houmao_project_dir_for_root(context.project.root)
    return collect_houmao_read_only_state(houmao_project_dir=project_dir)


def _resolve_optional_path(project_root: Path, value: str | None) -> Path | None:
    if value is None:
        return None
    path = Path(value)
    if path.is_absolute():
        return path.expanduser().resolve(strict=False)
    return (project_root / path).expanduser().resolve(strict=False)


def _append_path_boundary_diagnostic(
    context: EffectiveTopicContext,
    path: Path,
    diagnostics: list[Diagnostic],
) -> bool:
    topic_workspace = context.topic_workspace_path.resolve(strict=False)
    candidate = path.resolve(strict=False)
    try:
        candidate.relative_to(topic_workspace)
    except ValueError:
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="Workspace Path Resolution",
                path=candidate,
                message="Adapter manifest path must resolve under the selected Topic Workspace.",
            )
        )
        return True
    return False


def _record_adapter_manifest_ref(
    store: Any,
    *,
    context: EffectiveTopicContext,
    agent_team_instance_id: str = "",
    adapter_manifest_kind: str = "",
    manifest_path: Path,
    manifest_digest: str = "",
    source: str = "",
    path_plan_id: str | None = None,
    agent_instance_ids: list[str],
) -> None:
    timestamp = utc_timestamp()
    record = AdapterManifestRefRecord(
        id=f"adapter-manifest-ref-{_slug(agent_team_instance_id)}-{_slug(adapter_manifest_kind)}",
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        agent_team_instance_id=agent_team_instance_id,
        adapter_id=HOUMAO_ADAPTER_ID,
        manifest_kind=adapter_manifest_kind,
        manifest_path=str(manifest_path.resolve(strict=False)),
        manifest_digest=manifest_digest,
        source=source,
        path_plan_id=path_plan_id,
        agent_instance_ids=agent_instance_ids,
        created_at=timestamp,
        updated_at=timestamp,
        provenance_refs=[f"provenance:houmao-manifest:{agent_team_instance_id}:{adapter_manifest_kind}"],
    )
    store.record_adapter_manifest_ref(record)


def _adapter_reconciliation_record(
    context: EffectiveTopicContext,
    *,
    agent_team_instance_id: str = "",
    result: Any,
    actor_ref: str | None = None,
) -> AdapterReconciliationRecord:
    timestamp = utc_timestamp()
    state = str(result.state)
    return AdapterReconciliationRecord(
        id=f"adapter-reconciliation-{_slug(agent_team_instance_id)}-{_slug(state)}-{timestamp.replace(':', '').replace('-', '')}",
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        agent_team_instance_id=agent_team_instance_id,
        adapter_id=HOUMAO_ADAPTER_ID,
        state=state,
        mapping_confidence=str(result.mapping_confidence),
        manifest_refs=list(result.manifest_refs),
        manifest_digest_summary=dict(result.manifest_digest_summary),
        live_observation_summary=dict(result.live_observation_summary),
        diagnostics=[diagnostic.to_json() for diagnostic in result.diagnostics],
        actor_ref=actor_ref,
        created_at=timestamp,
        provenance_refs=[f"provenance:houmao-reconciliation:{agent_team_instance_id}:{timestamp}"],
    )


def _manifest_error_diagnostic(message: str, *, path: Path | None = None) -> Diagnostic:
    return Diagnostic(
        code="ISO060",
        severity="error",
        concept="Houmao adapter manifest",
        path=path,
        message=message,
    )


def _unsupported_adapter_diagnostic(adapter: str) -> Diagnostic:
    return Diagnostic(
        code="ISO070",
        severity="error",
        concept="Execution Adapter",
        field="--adapter",
        message=f"Unsupported Execution Adapter: {adapter}.",
    )


def _slug(value: str) -> str:
    return "".join(character if character.isalnum() or character in "._-" else "-" for character in value).strip("-") or "record"


def _load_selected_topic_agent_team_profile(
    context: EffectiveTopicContext,
    options: CliOptions,
) -> tuple[TopicAgentTeamProfile | None, Any | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    profile_id = _value(options, "topic_agent_team_profile_id") or context.topic_agent_team_profile_id
    if profile_id is None:
        diagnostics.append(
            Diagnostic(
                code="ISO020",
                severity="error",
                concept="Topic Agent Team Profile",
                field="topic_agent_team_profile_id",
                message="No Topic Agent Team Profile was selected for Agent Team Instance creation.",
            )
        )
        return None, None, diagnostics
    registration = context.project.manifest.first_topic_agent_team_profile(profile_id)
    if registration is None:
        diagnostics.append(
            Diagnostic(
                code="ISO020",
                severity="error",
                concept="Topic Agent Team Profile",
                field="topic_agent_team_profile_id",
                message=f"Selected Topic Agent Team Profile is not registered: {profile_id}.",
            )
        )
        return None, None, diagnostics
    profile_path = context.project.root / registration.path_input
    raw, load_diagnostics = load_toml(profile_path, "Topic Agent Team Profile")
    diagnostics.extend(load_diagnostics)
    profile = None
    if raw is not None:
        profile, parse_diagnostics = parse_topic_agent_team_profile(profile_path, raw)
        diagnostics.extend(parse_diagnostics)
    template_id = registration.domain_agent_team_template_id
    template_registration = find_domain_agent_team_template(template_id, context.project)
    if template_registration is None:
        diagnostics.append(_unknown_template_diagnostic(template_id))
        return profile, None, diagnostics
    template_report = validate_domain_agent_team_template(
        context.project,
        template_registration,
        include_harness=False,
    )
    diagnostics.extend(template_report.diagnostics)
    profile_report = validate_topic_agent_team_profile(
        profile,
        template_report.template,
        project=context.project,
        source_path=profile_path,
    )
    diagnostics.extend(profile_report.diagnostics)
    if profile is not None and profile.research_topic_id != context.research_topic.id:
        diagnostics.append(
            Diagnostic(
                code="ISO020",
                severity="error",
                concept="Topic Agent Team Profile",
                field="research_topic_id",
                message="Selected Topic Agent Team Profile belongs to another Research Topic.",
            )
        )
    return profile, template_report.template, diagnostics
__all__ = [
    "_LoadedManifestSet",
    "_agent_team_summary_or_diagnostic",
    "_agent_bindings_from_summary",
    "_operator_provenance_from_summary",
    "_manifest_output_path",
    "_load_manifest_set",
    "_resolve_manifest_cli_path",
    "_load_manifest_if_present",
    "_load_or_collect_live_state",
    "_resolve_optional_path",
    "_append_path_boundary_diagnostic",
    "_record_adapter_manifest_ref",
    "_adapter_reconciliation_record",
    "_manifest_error_diagnostic",
    "_unsupported_adapter_diagnostic",
    "_slug",
    "_load_selected_topic_agent_team_profile",
]
