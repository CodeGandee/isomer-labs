"""Agent Team Instance CLI command handlers."""

from __future__ import annotations

from isomer_labs.cli.handlers.shared import (
    adapter_manifest_path_plan_surface,
    Any,
    build_adapter_link_manifest,
    build_adapter_runtime_manifest,
    canonical_json_digest,
    CliOptions,
    Diagnostic,
    has_errors,
    HOUMAO_ADAPTER_ID,
    HoumaoAdapterFacade,
    manifest_paths,
    ManifestKind,
    ManifestValidationError,
    open_workspace_runtime,
    os,
    Path,
    reconcile_houmao_manifests,
    replace,
    write_json_manifest,
    _context_for_options,
    _emit,
    _value,
)

from isomer_labs.cli.handlers.team_instance_support import (
    _adapter_reconciliation_record,
    _agent_bindings_from_summary,
    _agent_team_summary_or_diagnostic,
    _append_path_boundary_diagnostic,
    _load_manifest_set,
    _load_or_collect_live_state,
    _load_selected_topic_agent_team_profile,
    _manifest_error_diagnostic,
    _manifest_output_path,
    _operator_provenance_from_summary,
    _record_adapter_manifest_ref,
    _resolve_optional_path,
    _unsupported_adapter_diagnostic,
)

def _cmd_team_instances_create(options: CliOptions, *, instance_id: str | None) -> int:
    context, diagnostics = _context_for_options(options)
    result = None
    if context is not None:
        profile, template, load_diagnostics = _load_selected_topic_agent_team_profile(context, options)
        diagnostics.extend(load_diagnostics)
        if profile is not None and template is not None and not has_errors(load_diagnostics):
            store, runtime_diagnostics = open_workspace_runtime(context, env=os.environ, read_only=False)
            diagnostics.extend(runtime_diagnostics)
            if store is not None:
                result, create_diagnostics = store.create_agent_team_instance(
                    context,
                    profile,
                    template,
                    requested_id=instance_id or _value(options, "agent_team_instance_id"),
                    env=os.environ,
                )
                diagnostics.extend(create_diagnostics)
                store.close()
    payload = {
        "ok": not has_errors(diagnostics),
        "mutated": result is not None,
        "creation": result.to_json() if result is not None else None,
    }
    lines: list[str] = []
    if result is not None:
        lines = [
            f"Agent Team Instance: {result.agent_team_instance.id}",
            f"Agent Instances: {len(result.agent_instances)}",
            f"Agent Workspaces: {len(result.agent_workspaces)}",
        ]
    return _emit("team-instances create", options, payload, diagnostics, lines)


def _cmd_team_instances_list(options: CliOptions) -> int:
    context, diagnostics = _context_for_options(options)
    instances: list[dict[str, object]] = []
    if context is not None:
        store, runtime_diagnostics = open_workspace_runtime(context, env=os.environ, read_only=True)
        diagnostics.extend(runtime_diagnostics)
        if store is not None:
            instances = [
                record.to_json()
                for record in store.list_agent_team_instances()
                if record.topic_workspace_id == context.topic_workspace_id
            ]
            store.close()
    payload = {"ok": not has_errors(diagnostics), "mutated": False, "agent_team_instances": instances}
    lines = ["Agent Team Instances", *[f"- {item['id']} ({item['status']})" for item in instances]]
    return _emit("team-instances list", options, payload, diagnostics, lines)


def _cmd_team_instances_show(options: CliOptions, agent_team_instance_id: str) -> int:
    context, diagnostics = _context_for_options(options)
    summary = None
    if context is not None:
        store, runtime_diagnostics = open_workspace_runtime(context, env=os.environ, read_only=True)
        diagnostics.extend(runtime_diagnostics)
        if store is not None:
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
            elif summary.agent_team_instance.topic_workspace_id != context.topic_workspace_id:
                diagnostics.append(
                    Diagnostic(
                        code="ISO041",
                        severity="error",
                        concept="Agent Team Instance",
                        field="agent_team_instance_id",
                        message="Agent Team Instance belongs to another Topic Workspace.",
                    )
                )
            store.close()
    payload = {
        "ok": not has_errors(diagnostics),
        "mutated": False,
        "summary": summary.to_json() if summary is not None else None,
    }
    lines: list[str] = []
    if summary is not None:
        team = summary.agent_team_instance
        lines = [
            f"Agent Team Instance: {team.id}",
            f"Status: {team.status}",
            f"Agent Instances: {len(summary.agent_instances)}",
            f"Agent Workspaces: {len(summary.agent_workspaces)}",
            f"Runs: {len(team.run_ids)}",
            f"Workflow Stage Cursors: {len(summary.workflow_stage_cursors)}",
            f"Blockers: {len(team.blocker_refs)}",
        ]
    return _emit("team-instances show", options, payload, diagnostics, lines)


def _cmd_team_instances_adapter_link_export(
    options: CliOptions,
    *,
    agent_team_instance_id: str,
    output_path: str | None = None,
    print_manifest: bool = False,
    houmao_project_dir: str | None = None,
    actor_ref: str | None = None,
) -> int:
    context, diagnostics = _context_for_options(options)
    payload: dict[str, Any] = {
        "ok": False,
        "mutated": False,
        "manifest": None,
        "manifest_path": None,
        "manifest_digest": None,
    }
    if context is None:
        return _emit("team-instances adapter-link export", options, payload, diagnostics, [])

    store, runtime_diagnostics = open_workspace_runtime(context, env=os.environ, read_only=print_manifest)
    diagnostics.extend(runtime_diagnostics)
    if store is None:
        return _emit("team-instances adapter-link export", options, payload, diagnostics, [])

    summary = _agent_team_summary_or_diagnostic(store, context, agent_team_instance_id, diagnostics)
    if summary is None:
        store.close()
        return _emit("team-instances adapter-link export", options, payload, diagnostics, [])

    houmao_dir = _resolve_optional_path(context.project.root, houmao_project_dir)
    manifest = build_adapter_link_manifest(
        project_root=context.project.root,
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        topic_workspace_path=context.topic_workspace_path,
        agent_team_instance_id=summary.agent_team_instance.id,
        topic_agent_team_profile_id=summary.agent_team_instance.topic_agent_team_profile_id,
        domain_agent_team_template_id=summary.agent_team_instance.domain_agent_team_template_id,
        agent_bindings=_agent_bindings_from_summary(summary),
        houmao_project_dir=houmao_dir,
        actor_ref=actor_ref,
        operator_provenance=_operator_provenance_from_summary(summary, actor_ref),
    )
    digest = canonical_json_digest(manifest)
    written_path: Path | None = None
    if not print_manifest:
        target = _manifest_output_path(context, agent_team_instance_id, output_path, ManifestKind.ADAPTER_LINK.value)
        if _append_path_boundary_diagnostic(context, target, diagnostics):
            store.close()
            return _emit("team-instances adapter-link export", options, payload, diagnostics, [])
        with store.connection:
            path_plan = store.record_path_plan(
                topic_workspace_id=context.topic_workspace_id,
                surface=adapter_manifest_path_plan_surface(agent_team_instance_id, ManifestKind.ADAPTER_LINK.value),
                path=target,
                source="default" if output_path is None else "explicit",
                source_detail="Houmao adapter link manifest",
            )
            try:
                digest = write_json_manifest(target, manifest, expected_kind=ManifestKind.ADAPTER_LINK.value)
            except ManifestValidationError as exc:
                diagnostics.append(_manifest_error_diagnostic(str(exc), path=target))
                store.close()
                return _emit("team-instances adapter-link export", options, payload, diagnostics, [])
            _record_adapter_manifest_ref(
                store,
                context=context,
                agent_team_instance_id=agent_team_instance_id,
                adapter_manifest_kind=ManifestKind.ADAPTER_LINK.value,
                manifest_path=target,
                manifest_digest=digest,
                source="isomer_cli_export",
                path_plan_id=path_plan.id,
                agent_instance_ids=[record.id for record in summary.agent_instances],
            )
        written_path = target
    store.close()

    payload.update(
        {
            "ok": not has_errors(diagnostics),
            "mutated": written_path is not None,
            "manifest": manifest,
            "manifest_path": str(written_path) if written_path is not None else None,
            "manifest_digest": digest,
        }
    )
    lines = [
        f"Houmao adapter link manifest: {written_path if written_path is not None else 'printed'}",
        f"Digest: {digest}",
    ]
    return _emit("team-instances adapter-link export", options, payload, diagnostics, lines)


def _cmd_team_instances_launch_material_prepare(
    options: CliOptions,
    *,
    agent_team_instance_id: str = "",
    adapter: str = "",
    houmao_project_dir: str | None = None,
    actor_ref: str | None = None,
) -> int:
    command_name = "team-instances launch-material prepare"
    context, diagnostics = _context_for_options(options)
    payload: dict[str, Any] = {
        "ok": False,
        "mutated": False,
        "execution_adapter": adapter,
        "preflight": None,
        "materialization": None,
    }
    if context is None:
        return _emit(command_name, options, payload, diagnostics, [])
    if adapter != HOUMAO_ADAPTER_ID:
        diagnostics.append(_unsupported_adapter_diagnostic(adapter))
        return _emit(command_name, options, payload, diagnostics, [])
    store, runtime_diagnostics = open_workspace_runtime(context, env=os.environ, read_only=False)
    diagnostics.extend(runtime_diagnostics)
    if store is None:
        return _emit(command_name, options, payload, diagnostics, [])
    summary = _agent_team_summary_or_diagnostic(store, context, agent_team_instance_id, diagnostics)
    if summary is None:
        store.close()
        return _emit(command_name, options, payload, diagnostics, [])
    profile, _, profile_diagnostics = _load_selected_topic_agent_team_profile(
        context,
        replace(options, topic_agent_team_profile_id=summary.agent_team_instance.topic_agent_team_profile_id),
    )
    diagnostics.extend(profile_diagnostics)
    if profile is None:
        store.close()
        return _emit(command_name, options, payload, diagnostics, [])
    facade = HoumaoAdapterFacade(env=os.environ)
    project_dir = _resolve_optional_path(context.project.root, houmao_project_dir)
    preflight = facade.preflight(
        context=context,
        store=store,
        agent_team_instance_id=agent_team_instance_id,
        houmao_project_dir=project_dir,
        run_probes=False,
    )
    diagnostics.extend(preflight.diagnostics)
    payload["preflight"] = preflight.to_json()
    if has_errors(diagnostics):
        store.close()
        return _emit(command_name, options, payload, diagnostics, [])
    with store.connection:
        materialization = facade.materialize(
            context=context,
            store=store,
            summary=summary,
            profile=profile,
            houmao_project_dir=project_dir,
            actor_ref=actor_ref,
            source="isomer_prepare_only",
        )
    diagnostics.extend(materialization.diagnostics)
    store.close()
    payload.update(
        {
            "ok": not has_errors(diagnostics),
            "mutated": not has_errors(diagnostics),
            "materialization": materialization.to_json(),
            "manual_guidance": materialization.manual_guidance(),
        }
    )
    lines = [
        f"Houmao launch material: {materialization.paths.launch_material_root}",
        f"Adapter link manifest: {materialization.link_manifest_path}",
        f"Launch material manifest: {materialization.launch_material_manifest_path}",
        f"Manual Houmao commands: {len(materialization.manual_guidance())}",
    ]
    return _emit(command_name, options, payload, diagnostics, lines)


def _cmd_team_instances_launch(
    options: CliOptions,
    *,
    agent_team_instance_id: str = "",
    adapter: str = "",
    houmao_project_dir: str | None = None,
    actor_ref: str | None = None,
) -> int:
    command_name = "team-instances launch"
    context, diagnostics = _context_for_options(options)
    payload: dict[str, Any] = {
        "ok": False,
        "mutated": False,
        "execution_adapter": adapter,
        "preflight": None,
        "launch": None,
    }
    if context is None:
        return _emit(command_name, options, payload, diagnostics, [])
    if adapter != HOUMAO_ADAPTER_ID:
        diagnostics.append(_unsupported_adapter_diagnostic(adapter))
        return _emit(command_name, options, payload, diagnostics, [])
    store, runtime_diagnostics = open_workspace_runtime(context, env=os.environ, read_only=False)
    diagnostics.extend(runtime_diagnostics)
    if store is None:
        return _emit(command_name, options, payload, diagnostics, [])
    summary = _agent_team_summary_or_diagnostic(store, context, agent_team_instance_id, diagnostics)
    if summary is None:
        store.close()
        return _emit(command_name, options, payload, diagnostics, [])
    profile, _, profile_diagnostics = _load_selected_topic_agent_team_profile(
        context,
        replace(options, topic_agent_team_profile_id=summary.agent_team_instance.topic_agent_team_profile_id),
    )
    diagnostics.extend(profile_diagnostics)
    if profile is None:
        store.close()
        return _emit(command_name, options, payload, diagnostics, [])
    facade = HoumaoAdapterFacade(env=os.environ)
    default_project_dir = manifest_paths(context.topic_workspace_path, agent_team_instance_id).root / "houmao-project"
    project_dir = _resolve_optional_path(context.project.root, houmao_project_dir) or default_project_dir
    preflight = facade.preflight(
        context=context,
        store=store,
        agent_team_instance_id=agent_team_instance_id,
        houmao_project_dir=project_dir,
        run_probes=False,
    )
    diagnostics.extend(preflight.diagnostics)
    payload["preflight"] = preflight.to_json()
    if has_errors(diagnostics):
        store.close()
        return _emit(command_name, options, payload, diagnostics, [])
    with store.connection:
        launch_result = facade.quick_launch(
            context=context,
            store=store,
            summary=summary,
            profile=profile,
            houmao_project_dir=project_dir,
            actor_ref=actor_ref,
        )
    diagnostics.extend(launch_result.diagnostics)
    store.close()
    payload.update(
        {
            "ok": not has_errors(diagnostics),
            "mutated": True,
            "launch": launch_result.to_json(),
        }
    )
    lines = [
        f"Houmao launch status: {launch_result.status}",
        f"Launch attempt: {launch_result.launch_attempt_id}",
        f"Command runs: {len(launch_result.command_run_ids)}",
    ]
    return _emit(command_name, options, payload, diagnostics, lines)


def _cmd_team_instances_manifest_inspect(
    options: CliOptions,
    *,
    agent_team_instance_id: str = "",
    link_manifest: str | None = None,
    launch_material_manifest: str | None = None,
    runtime_manifest: str | None = None,
    live_state_json: str | None = None,
    houmao_project_dir: str | None = None,
    include_integrity: bool = False,
    adapter: str | None = None,
    actor_ref: str | None = None,
) -> int:
    context, diagnostics = _context_for_options(options)
    payload: dict[str, Any] = {
        "ok": False,
        "mutated": False,
        "reconciliation": None,
        "manifest_paths": None,
    }
    if context is None:
        return _emit("team-instances inspect-live", options, payload, diagnostics, [])
    store, runtime_diagnostics = open_workspace_runtime(context, env=os.environ, read_only=True)
    diagnostics.extend(runtime_diagnostics)
    if store is None:
        return _emit("team-instances inspect-live", options, payload, diagnostics, [])
    summary = _agent_team_summary_or_diagnostic(store, context, agent_team_instance_id, diagnostics)
    if summary is None:
        store.close()
        return _emit("team-instances inspect-live", options, payload, diagnostics, [])
    loaded = _load_manifest_set(
        context,
        agent_team_instance_id=agent_team_instance_id,
        link_manifest=link_manifest,
        launch_material_manifest=launch_material_manifest,
        runtime_manifest=runtime_manifest,
        diagnostics=diagnostics,
        require_link=True,
    )
    if adapter == HOUMAO_ADAPTER_ID:
        store.close()
        store, runtime_diagnostics = open_workspace_runtime(context, env=os.environ, read_only=False)
        diagnostics.extend(runtime_diagnostics)
        if store is None:
            return _emit("team-instances inspect-live", options, payload, diagnostics, [])
        summary = _agent_team_summary_or_diagnostic(store, context, agent_team_instance_id, diagnostics)
        if summary is None:
            store.close()
            return _emit("team-instances inspect-live", options, payload, diagnostics, [])
        facade = HoumaoAdapterFacade(env=os.environ)
        with store.connection:
            inspection_result = facade.inspect_live(
                context=context,
                store=store,
                summary=summary,
                link_manifest=loaded.link_manifest,
                launch_material_manifest=loaded.launch_material_manifest,
                runtime_manifest=loaded.runtime_manifest,
                actor_ref=actor_ref,
            )
        diagnostics.extend(inspection_result.diagnostics)
        store.close()
        payload.update(
            {
                "ok": not has_errors(diagnostics),
                "mutated": True,
                "inspection": inspection_result.to_json(),
                "reconciliation": inspection_result.reconciliation.to_json() if inspection_result.reconciliation is not None else None,
                "manifest_paths": loaded.paths.to_json(),
            }
        )
        lines = [
            f"Houmao live inspection status: {inspection_result.status}",
            f"Command runs: {len(inspection_result.command_run_ids)}",
            f"Snapshot: {inspection_result.snapshot_record_id}",
        ]
        return _emit("team-instances inspect-live", options, payload, diagnostics, lines)
    live_state, live_diagnostics = _load_or_collect_live_state(
        context,
        live_state_json=live_state_json,
        houmao_project_dir=houmao_project_dir,
        link_manifest=loaded.link_manifest,
    )
    diagnostics.extend(live_diagnostics)
    reconciliation_result = reconcile_houmao_manifests(
        link_manifest=loaded.link_manifest,
        launch_material_manifest=loaded.launch_material_manifest if include_integrity else None,
        runtime_manifest=loaded.runtime_manifest,
        live_state=live_state,
        material_base_dir=context.topic_workspace_path,
    )
    diagnostics.extend(reconciliation_result.diagnostics)
    store.close()
    payload.update(
        {
            "ok": not has_errors(diagnostics),
            "reconciliation": reconciliation_result.to_json(),
            "manifest_paths": loaded.paths.to_json(),
        }
    )
    lines = [
        f"Houmao adapter reconciliation state: {reconciliation_result.state}",
        f"Mapping confidence: {reconciliation_result.mapping_confidence}",
    ]
    return _emit("team-instances inspect-live", options, payload, diagnostics, lines)


def _cmd_team_instances_stop(
    options: CliOptions,
    *,
    agent_team_instance_id: str = "",
    adapter: str = "",
    link_manifest: str | None = None,
    actor_ref: str | None = None,
) -> int:
    command_name = "team-instances stop"
    context, diagnostics = _context_for_options(options)
    payload: dict[str, Any] = {
        "ok": False,
        "mutated": False,
        "execution_adapter": adapter,
        "stop": None,
    }
    if context is None:
        return _emit(command_name, options, payload, diagnostics, [])
    if adapter != HOUMAO_ADAPTER_ID:
        diagnostics.append(_unsupported_adapter_diagnostic(adapter))
        return _emit(command_name, options, payload, diagnostics, [])
    store, runtime_diagnostics = open_workspace_runtime(context, env=os.environ, read_only=False)
    diagnostics.extend(runtime_diagnostics)
    if store is None:
        return _emit(command_name, options, payload, diagnostics, [])
    summary = _agent_team_summary_or_diagnostic(store, context, agent_team_instance_id, diagnostics)
    if summary is None:
        store.close()
        return _emit(command_name, options, payload, diagnostics, [])
    loaded = _load_manifest_set(
        context,
        agent_team_instance_id=agent_team_instance_id,
        link_manifest=link_manifest,
        launch_material_manifest=None,
        runtime_manifest=None,
        diagnostics=diagnostics,
        require_link=False,
    )
    facade = HoumaoAdapterFacade(env=os.environ)
    with store.connection:
        result = facade.stop(
            context=context,
            store=store,
            summary=summary,
            link_manifest=loaded.link_manifest,
            actor_ref=actor_ref,
        )
    diagnostics.extend(result.diagnostics)
    store.close()
    payload.update({"ok": not has_errors(diagnostics), "mutated": True, "stop": result.to_json()})
    lines = [
        f"Houmao stop status: {result.status}",
        f"Stop outcome: {result.stop_outcome_id}",
        f"Command runs: {len(result.command_run_ids)}",
    ]
    return _emit(command_name, options, payload, diagnostics, lines)


def _cmd_team_instances_reconcile(
    options: CliOptions,
    *,
    agent_team_instance_id: str = "",
    link_manifest: str | None = None,
    launch_material_manifest: str | None = None,
    runtime_manifest: str | None = None,
    live_state_json: str | None = None,
    houmao_project_dir: str | None = None,
    actor_ref: str | None = None,
    adopt: bool = False,
    approved: bool = False,
) -> int:
    command_name = "team-instances adopt" if adopt else "team-instances reconcile"
    context, diagnostics = _context_for_options(options)
    payload: dict[str, Any] = {
        "ok": False,
        "mutated": False,
        "reconciliation": None,
        "runtime_manifest_path": None,
    }
    if context is None:
        return _emit(command_name, options, payload, diagnostics, [])
    if adopt and not approved:
        diagnostics.append(
            Diagnostic(
                code="ISO064",
                severity="error",
                concept="Houmao adapter adoption",
                field="--yes",
                message="Adoption requires explicit --yes approval.",
            )
        )
        return _emit(command_name, options, payload, diagnostics, [])

    store, runtime_diagnostics = open_workspace_runtime(context, env=os.environ, read_only=False)
    diagnostics.extend(runtime_diagnostics)
    if store is None:
        return _emit(command_name, options, payload, diagnostics, [])
    summary = _agent_team_summary_or_diagnostic(store, context, agent_team_instance_id, diagnostics)
    if summary is None:
        store.close()
        return _emit(command_name, options, payload, diagnostics, [])
    loaded = _load_manifest_set(
        context,
        agent_team_instance_id=agent_team_instance_id,
        link_manifest=link_manifest,
        launch_material_manifest=launch_material_manifest,
        runtime_manifest=runtime_manifest,
        diagnostics=diagnostics,
        require_link=True,
    )
    live_state, live_diagnostics = _load_or_collect_live_state(
        context,
        live_state_json=live_state_json,
        houmao_project_dir=houmao_project_dir,
        link_manifest=loaded.link_manifest,
    )
    diagnostics.extend(live_diagnostics)
    if has_errors(diagnostics):
        store.close()
        return _emit(command_name, options, payload, diagnostics, [])

    result = reconcile_houmao_manifests(
        link_manifest=loaded.link_manifest,
        launch_material_manifest=loaded.launch_material_manifest,
        runtime_manifest=loaded.runtime_manifest,
        live_state=live_state,
        material_base_dir=context.topic_workspace_path,
        adopt=adopt,
    )
    diagnostics.extend(result.diagnostics)
    if has_errors(diagnostics):
        rejection_record = _adapter_reconciliation_record(
            context,
            agent_team_instance_id=agent_team_instance_id,
            result=result,
            actor_ref=actor_ref,
        )
        with store.connection:
            store.record_adapter_reconciliation(rejection_record)
        store.close()
        payload.update({"reconciliation": result.to_json(), "mutated": True})
        return _emit(command_name, options, payload, diagnostics, [])

    runtime_manifest_doc = build_adapter_runtime_manifest(
        link_manifest=loaded.link_manifest or {},
        result=result,
        source_mode="houmao_direct_adoption" if adopt else "houmao_reconciliation",
    )
    runtime_manifest_path = loaded.paths.adapter_runtime
    if _append_path_boundary_diagnostic(context, runtime_manifest_path, diagnostics):
        store.close()
        return _emit(command_name, options, payload, diagnostics, [])
    with store.connection:
        runtime_path_plan = store.record_path_plan(
            topic_workspace_id=context.topic_workspace_id,
            surface=adapter_manifest_path_plan_surface(agent_team_instance_id, ManifestKind.ADAPTER_RUNTIME.value),
            path=runtime_manifest_path,
            source="default",
            source_detail="Houmao adapter runtime manifest",
        )
        try:
            runtime_digest = write_json_manifest(
                runtime_manifest_path,
                runtime_manifest_doc,
                expected_kind=ManifestKind.ADAPTER_RUNTIME.value,
            )
        except ManifestValidationError as exc:
            diagnostics.append(_manifest_error_diagnostic(str(exc), path=runtime_manifest_path))
            store.close()
            return _emit(command_name, options, payload, diagnostics, [])
        _record_adapter_manifest_ref(
            store,
            context=context,
            agent_team_instance_id=agent_team_instance_id,
            adapter_manifest_kind=ManifestKind.ADAPTER_RUNTIME.value,
            manifest_path=runtime_manifest_path,
            manifest_digest=runtime_digest,
            source="isomer_cli_adopt" if adopt else "isomer_cli_reconcile",
            path_plan_id=runtime_path_plan.id,
            agent_instance_ids=[record.id for record in summary.agent_instances],
        )
        if loaded.link_path is not None and loaded.link_path.exists() and loaded.link_manifest is not None:
            _record_adapter_manifest_ref(
                store,
                context=context,
                agent_team_instance_id=agent_team_instance_id,
                adapter_manifest_kind=ManifestKind.ADAPTER_LINK.value,
                manifest_path=loaded.link_path,
                manifest_digest=canonical_json_digest(loaded.link_manifest),
                source="isomer_cli_reconcile",
                path_plan_id=None,
                agent_instance_ids=[record.id for record in summary.agent_instances],
            )
        if loaded.launch_material_path is not None and loaded.launch_material_path.exists() and loaded.launch_material_manifest is not None:
            _record_adapter_manifest_ref(
                store,
                context=context,
                agent_team_instance_id=agent_team_instance_id,
                adapter_manifest_kind=ManifestKind.LAUNCH_MATERIAL.value,
                manifest_path=loaded.launch_material_path,
                manifest_digest=canonical_json_digest(loaded.launch_material_manifest),
                source="isomer_cli_reconcile",
                path_plan_id=None,
                agent_instance_ids=[record.id for record in summary.agent_instances],
            )
        store.record_adapter_reconciliation(
            _adapter_reconciliation_record(
                context,
                agent_team_instance_id=agent_team_instance_id,
                result=result,
                actor_ref=actor_ref,
            )
        )
    store.close()
    payload.update(
        {
            "ok": not has_errors(diagnostics),
            "mutated": True,
            "reconciliation": result.to_json(),
            "runtime_manifest_path": str(runtime_manifest_path),
        }
    )
    lines = [
        f"Houmao adapter reconciliation state: {result.state}",
        f"Mapping confidence: {result.mapping_confidence}",
        f"Runtime manifest: {runtime_manifest_path}",
    ]
    return _emit(command_name, options, payload, diagnostics, lines)
__all__ = [
    "_cmd_team_instances_create",
    "_cmd_team_instances_list",
    "_cmd_team_instances_show",
    "_cmd_team_instances_adapter_link_export",
    "_cmd_team_instances_launch_material_prepare",
    "_cmd_team_instances_launch",
    "_cmd_team_instances_manifest_inspect",
    "_cmd_team_instances_stop",
    "_cmd_team_instances_reconcile",
]
