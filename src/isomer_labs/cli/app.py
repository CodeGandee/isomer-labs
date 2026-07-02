"""Command line interface for Isomer Labs."""

from __future__ import annotations

from dataclasses import dataclass, replace
import json
import os
from pathlib import Path
from typing import Any, Sequence

import click

from isomer_labs.builtins import list_built_in_schemas
from isomer_labs.cli.errors import (
    emit_click_exception,
    emit_keyboard_interrupt,
    emit_unexpected_exception,
    normalize_raw_args,
    raw_debug_enabled,
)
from isomer_labs.cli.options import CliOptions, value as _value
from isomer_labs.cli.output import OutputMode, emit_output, output_format
from isomer_labs.content_layout import topic_workspace_path as default_topic_workspace_path
from isomer_labs.context import resolve_effective_topic_context
from isomer_labs.diagnostics import Diagnostic, has_errors
from isomer_labs.doctor import build_doctor_report, render_doctor_text
from isomer_labs.houmao.manifests import (
    HOUMAO_ADAPTER_ID,
    AgentBinding,
    ManifestKind,
    ManifestValidationError,
    adapter_manifest_path_plan_surface,
    build_adapter_link_manifest,
    build_adapter_runtime_manifest,
    canonical_json_digest,
    collect_houmao_read_only_state,
    load_json_manifest,
    manifest_paths,
    reconcile_houmao_manifests,
    write_json_manifest,
)
from isomer_labs.houmao.adapter import HoumaoAdapterFacade
from isomer_labs.init_project import initialize_project
from isomer_labs.models import EffectiveTopicContext, Project, ProjectState, SelectionRequest, TopicAgentTeamProfile
from isomer_labs.path_utils import display_path
from isomer_labs.paths import (
    default_semantic_path,
    explain_semantic_path,
    list_semantic_paths,
    materialize_default_paths,
    materialize_semantic_path,
    preview_paths,
    resolve_effective_agent_context,
    resolve_effective_topic_actor_context,
    resolve_semantic_path,
)
from isomer_labs.topic_workspace_manifest import (
    register_manifest_binding,
    reset_manifest_binding,
    unregister_manifest_binding,
    update_manifest_binding,
)
from isomer_labs.topic_actors import (
    archive_topic_actor,
    diagnose_topic_actor,
    list_topic_actors,
    materialize_topic_actor_workspace,
    register_topic_actor,
    show_topic_actor,
    update_topic_actor,
)
from isomer_labs.profile_bundles import materialize_topic_agent_team_profile_bundle
from isomer_labs.project import (
    discover_project,
    find_ancestor_manifest,
    houmao_project_dir_for_root,
    project_root_for_manifest,
)
from isomer_labs.project_cleanup import execute_project_cleanup, plan_project_cleanup, render_cleanup_text
from isomer_labs.project_content_root import (
    execute_project_content_root_move,
    plan_project_content_root_move,
    render_content_root_move_text,
)
from isomer_labs.rendering import render_key_values
from isomer_labs.research_topics import (
    create_research_topic,
    delete_research_topic,
    plan_delete_research_topic,
    render_topic_create_text,
    render_topic_delete_text,
    render_topic_show_text,
    render_topic_update_text,
    show_research_topic,
    update_research_topic,
)
from isomer_labs.runtime.store import (
    initialize_workspace_runtime,
    open_workspace_runtime,
    prepare_topic_environment_readiness,
)
from isomer_labs.runtime.models import AdapterManifestRefRecord, AdapterReconciliationRecord, utc_timestamp
from isomer_labs.runtime.validation import inspect_workspace_runtime, validate_workspace_runtime
from isomer_labs.team_profiles import (
    parse_topic_agent_team_profile,
    profile_to_toml,
    specialize_topic_agent_team_profile,
    validate_topic_agent_team_profile,
)
from isomer_labs.team_templates import (
    BUILT_IN_DEEPSCI_ORG_ID,
    discover_domain_agent_team_templates,
    find_domain_agent_team_template,
    resolve_template_source_path,
    validate_domain_agent_team_template,
)
from isomer_labs.topic_team_instantiation import parse_topic_team_instantiation_packet
from isomer_labs.toml_loader import load_toml
from isomer_labs.validation import build_project_state


COMMAND_SURFACE = """Milestone 1 Isomer Labs Project discovery and path preview CLI.

\b
Command surface:
  project init
  project content-root move
  project cleanup
  project doctor
  project validate
  project topics list
  project topics show
  project topics create
  project topics update
  project topics delete
  project topic-actors list
  project topic-actors show
  project topic-actors register
  project topic-actors update
  project topic-actors archive
  project topic-actors materialize
  project topic-actors repair
  project topic-actors diagnose
  project workspaces list
  project context show
  project repos create
  project paths default
  project paths explain
  project paths get
  project paths list
  project paths materialize
  project paths materialize-default
  project paths preview
  project paths register
  project paths reset
  project paths unregister
  project paths update
  project runtime init
  project runtime prepare
  project runtime inspect
  project runtime validate
  project artifact-formats validate
  project artifact-formats render
  project artifact-formats register
  project team-instances create
  project team-instances list
  project team-instances show
  project team-instances adapter-link export
  project team-instances launch-material prepare
  project team-instances launch
  project team-instances inspect-live
  project team-instances stop
  project team-instances reconcile
  project team-instances adopt
  project handoffs dispatch
  project handoffs observe
  project handoffs normalize
  project team-templates list
  project team-templates inspect
  project team-templates validate
  project team-profiles specialize
  project team-profiles materialize
  project team-profiles validate
  ext deepsci call
  ext deepsci tools
  ext research records create
  ext research records show
  ext research records list
  ext research records update
  ext research records delete
  schemas list
"""


def main(argv: Sequence[str] | None = None) -> int:
    """Run the Click-backed CLI and return a process status code."""

    raw_args = normalize_raw_args(argv)
    debug = raw_debug_enabled(raw_args)
    try:
        result = app.main(
            args=raw_args,
            prog_name="isomer-cli",
            standalone_mode=False,
        )
    except click.exceptions.Exit as exc:
        return int(exc.exit_code)
    except click.UsageError as exc:
        return emit_click_exception(exc, raw_args, debug=debug)
    except click.ClickException as exc:
        return emit_click_exception(exc, raw_args, debug=debug)
    except click.Abort:
        return emit_keyboard_interrupt(raw_args, debug=debug)
    except KeyboardInterrupt:
        return emit_keyboard_interrupt(raw_args, debug=debug)
    except Exception as exc:
        return emit_unexpected_exception(exc, raw_args, debug=debug)
    if result is None:
        return 0
    return int(result)


def build_parser() -> click.Group:
    """Return the Click command object used by the installed entrypoint."""

    return app

@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    help=COMMAND_SURFACE,
    invoke_without_command=True,
)
@click.option("--print-json", "print_json", is_flag=True, help="Emit deterministic JSON for the selected command.")
@click.option("--debug", "debug", is_flag=True, help="Include debug details for unexpected CLI errors.")
@click.pass_context
def app(
    ctx: click.Context,
    print_json: bool = False,
    debug: bool = False,
) -> None:
    output_mode = OutputMode(print_json=print_json)
    ctx.obj = CliOptions(
        output_mode=output_mode,
        debug=debug,
    )
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@app.group(name="project", help="Project-scoped commands.")
@click.option("--root", "project_root", default=None, help="Explicit Project root selector.")
@click.option("--project", "project_alias", default=None, hidden=True, help="Compatibility alias for --root.")
@click.option("--manifest", default=None, help="Explicit Project Manifest selector.")
@click.pass_context
def project_group(
    ctx: click.Context,
    project_root: str | None = None,
    project_alias: str | None = None,
    manifest: str | None = None,
) -> None:
    root_options = ctx.find_root().obj
    options = root_options if isinstance(root_options, CliOptions) else CliOptions()
    selected_root = project_root if project_root is not None else project_alias
    ctx.obj = replace(
        options,
        project=selected_root if selected_root is not None else options.project,
        manifest=manifest if manifest is not None else options.manifest,
    )
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


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


def _cmd_schemas_list(options: CliOptions) -> int:
    schemas = list_built_in_schemas()
    payload = {"schemas": [schema.to_json() for schema in schemas]}
    lines = ["Built-In Isomer Schemas"]
    lines.extend(f"- {schema.name} ({schema.kind}, {schema.schema_version})" for schema in schemas)
    return _emit("schemas list", options, payload, [], lines)


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
                "validation_status": "valid" if report.ok else "invalid",
            }
        )
    payload = {"templates": sorted(templates, key=lambda item: str(item["id"]))}
    lines = ["Domain Agent Team Templates"]
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
    selected_template_id = template_id or context.domain_agent_team_template_id or BUILT_IN_DEEPSCI_ORG_ID
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
    selected_template_id = template_id or (packet.source_template_ref if packet is not None else None) or context.domain_agent_team_template_id or BUILT_IN_DEEPSCI_ORG_ID
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
    selected_template_id = template_id or (profile.domain_agent_team_template_id if profile is not None else None) or BUILT_IN_DEEPSCI_ORG_ID
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


def _cmd_runtime_init(options: CliOptions) -> int:
    context, diagnostics = _context_for_options(options)
    result = None
    if context is not None:
        result, runtime_diagnostics = initialize_workspace_runtime(context, env=os.environ)
        diagnostics.extend(runtime_diagnostics)
    payload = {
        "ok": not has_errors(diagnostics),
        "mutated": bool(result is not None and result.created),
        "runtime": result.to_json() if result is not None else None,
    }
    lines: list[str] = []
    if result is not None:
        lines = [
            f"Workspace Runtime: {result.runtime_path}",
            f"Schema: {result.metadata.schema_version}",
            f"Created: {str(result.created).lower()}",
        ]
    return _emit("runtime init", options, payload, diagnostics, lines)


def _cmd_runtime_prepare(options: CliOptions, *, actor_ref: str | None) -> int:
    context, diagnostics = _context_for_options(options)
    result = None
    if context is not None:
        result, runtime_diagnostics = prepare_topic_environment_readiness(
            context,
            env=os.environ,
            actor_ref=actor_ref,
        )
        diagnostics.extend(runtime_diagnostics)
    payload = {
        "ok": not has_errors(diagnostics),
        "mutated": result is not None and result.readiness is not None,
        "preparation": result.to_json() if result is not None else None,
    }
    lines: list[str] = []
    if result is not None and result.readiness is not None:
        lines = [
            f"Topic Environment Readiness: {result.readiness.status}",
            f"Readiness record: {result.readiness.id}",
        ]
        if result.readiness.repair_service_request_hint is not None:
            lines.append(result.readiness.repair_service_request_hint)
    return _emit("runtime prepare", options, payload, diagnostics, lines)


def _cmd_runtime_inspect(options: CliOptions) -> int:
    context, diagnostics = _context_for_options(options)
    inspection = None
    if context is not None:
        inspection, runtime_diagnostics = inspect_workspace_runtime(context, env=os.environ)
        diagnostics.extend(runtime_diagnostics)
    payload = {
        "ok": not has_errors(diagnostics),
        "mutated": False,
        "runtime": inspection.to_json() if inspection is not None else None,
    }
    lines: list[str] = []
    if inspection is not None:
        lines = [
            f"Workspace Runtime exists: {str(inspection.exists).lower()}",
            f"Workspace Runtime path: {inspection.runtime_path}",
        ]
        if inspection.metadata is not None:
            lines.append(f"Schema: {inspection.metadata['schema_version']}")
            lines.append(f"Agent Team Instances: {len(inspection.agent_team_instances)}")
    return _emit("runtime inspect", options, payload, diagnostics, lines)


def _cmd_runtime_validate(options: CliOptions, *, require_ready_readiness: bool) -> int:
    context, diagnostics = _context_for_options(options)
    inspection = None
    if context is not None:
        inspection, runtime_diagnostics = validate_workspace_runtime(
            context,
            env=os.environ,
            require_ready_readiness=require_ready_readiness,
        )
        diagnostics.extend(runtime_diagnostics)
    payload = {
        "ok": not has_errors(diagnostics),
        "mutated": False,
        "runtime": inspection.to_json() if inspection is not None else None,
    }
    lines = ["Workspace Runtime valid."] if inspection is not None and not has_errors(diagnostics) else []
    return _emit("runtime validate", options, payload, diagnostics, lines)


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


def _context_for_options(options: CliOptions) -> tuple[EffectiveTopicContext | None, list[Diagnostic]]:
    project, diagnostics = _discover(options)
    if project is None:
        return None, diagnostics
    state = build_project_state(project)
    diagnostics.extend(state.diagnostics)
    request = SelectionRequest(
        research_topic_id=_value(options, "research_topic_id"),
        topic_workspace_id=_value(options, "topic_workspace_id"),
        research_inquiry_id=_value(options, "research_inquiry_id"),
        research_task_id=_value(options, "research_task_id"),
        run_id=_value(options, "run_id"),
        agent_team_instance_id=_value(options, "agent_team_instance_id"),
        agent_instance_id=_value(options, "agent_instance_id"),
        topic_agent_team_profile_id=_value(options, "topic_agent_team_profile_id"),
    )
    context, context_diagnostics = resolve_effective_topic_context(
        state,
        request,
        cwd=Path.cwd(),
        env=os.environ,
    )
    diagnostics.extend(context_diagnostics)
    return context, diagnostics


_IMPLICIT_TOPIC_SELECTION_SOURCES = {
    "Project Manifest default",
    "single Project Manifest registration",
}


def _context_for_path_options(
    options: CliOptions,
    semantic_label: str | None = None,
) -> tuple[EffectiveTopicContext | None, list[Diagnostic]]:
    context, diagnostics = _context_for_options(options)
    if context is None:
        return None, diagnostics
    if not _path_label_requires_selected_topic(semantic_label):
        return context, diagnostics
    source = context.sources.get("research_topic_id")
    if source not in _IMPLICIT_TOPIC_SELECTION_SOURCES:
        return context, diagnostics
    diagnostics.append(
        Diagnostic(
            code="ISO013",
            severity="error",
            concept="Workspace Path Resolution",
            field=semantic_label or "semantic_label",
            message=(
                "Semantic storage labels that require a Topic context need an explicit "
                "`--topic` or `--topic-workspace` selector unless the command is run inside "
                "the selected Topic Workspace."
            ),
        )
    )
    return None, diagnostics


def _path_label_requires_selected_topic(semantic_label: str | None) -> bool:
    if semantic_label is None:
        return True
    return semantic_label.startswith(("topic.", "agent.", "custom."))


def _selection_request_from_options(options: CliOptions) -> SelectionRequest:
    return SelectionRequest(
        research_topic_id=_value(options, "research_topic_id"),
        topic_workspace_id=_value(options, "topic_workspace_id"),
        research_inquiry_id=_value(options, "research_inquiry_id"),
        research_task_id=_value(options, "research_task_id"),
        run_id=_value(options, "run_id"),
        agent_team_instance_id=_value(options, "agent_team_instance_id"),
        agent_instance_id=_value(options, "agent_instance_id"),
        topic_agent_team_profile_id=_value(options, "topic_agent_team_profile_id"),
    )


def _discover(options: CliOptions) -> tuple[Project | None, list[Diagnostic]]:
    return discover_project(
        cwd=Path.cwd(),
        env=os.environ,
        project_selector=_value(options, "project"),
        manifest_selector=_value(options, "manifest"),
    )


def _discover_optional(options: CliOptions) -> tuple[Project | None, list[Diagnostic]]:
    project, diagnostics = _discover(options)
    if project is not None:
        return project, diagnostics
    if _value(options, "project") is None and _value(options, "manifest") is None:
        return None, []
    return project, diagnostics


def _project_selector_requested(options: CliOptions) -> bool:
    return _value(options, "project") is not None or _value(options, "manifest") is not None


def _topic_selector_requested(options: CliOptions) -> bool:
    return any(
        _value(options, name) is not None
        for name in (
            "research_topic_id",
            "topic_workspace_id",
            "research_inquiry_id",
            "research_task_id",
            "run_id",
            "agent_team_instance_id",
            "agent_instance_id",
            "topic_agent_team_profile_id",
        )
    )


def _unknown_template_diagnostic(template_id: str) -> Diagnostic:
    return Diagnostic(
        code="ISO016",
        severity="error",
        concept="Domain Agent Team Template",
        field="template_id",
        message=f"Unknown Domain Agent Team Template: {template_id}.",
    )


def _resolve_profile_cli_path(
    project: Project | None,
    profile_path: str | None,
    diagnostics: list[Diagnostic],
) -> Path | None:
    if profile_path is not None:
        path = Path(profile_path)
        if path.is_absolute() or project is None:
            return path.expanduser().resolve(strict=False)
        return (project.root / path).expanduser().resolve(strict=False)
    if project is None:
        diagnostics.append(
            Diagnostic(
                code="ISO020",
                severity="error",
                concept="Topic Agent Team Profile",
                message="A Project or explicit profile path is required to validate a Topic Agent Team Profile.",
            )
        )
        return None
    profile_id = project.manifest.default_topic_agent_team_profile_id()
    if profile_id is None:
        diagnostics.append(
            Diagnostic(
                code="ISO020",
                severity="error",
                concept="Topic Agent Team Profile",
                path=project.manifest_path,
                field="defaults.topic_agent_team_profile_id",
                message="No Topic Agent Team Profile path was provided and the Project Manifest has no default profile.",
            )
        )
        return None
    registration = project.manifest.first_topic_agent_team_profile(profile_id)
    if registration is None:
        diagnostics.append(
            Diagnostic(
                code="ISO020",
                severity="error",
                concept="Topic Agent Team Profile",
                path=project.manifest_path,
                field="defaults.topic_agent_team_profile_id",
                message="Project Manifest default profile id is not registered.",
            )
        )
        return None
    return (project.root / registration.path_input).expanduser().resolve(strict=False)


def _resolve_cli_path(project_root: Path, path_input: str) -> Path:
    path = Path(path_input).expanduser()
    if path.is_absolute():
        return path.resolve(strict=False)
    return (project_root / path).resolve(strict=False)


def _profile_registration_suggestion(project_root: Path, profile: TopicAgentTeamProfile) -> dict[str, str]:
    return {
        "target": "Project Manifest",
        "section": "topic_agent_team_profiles",
        "id": profile.id,
        "path": _project_relative_path(project_root, profile.source_path),
        "domain_agent_team_template_id": profile.domain_agent_team_template_id,
        "research_topic_id": profile.research_topic_id,
        "status": "active",
    }


def _project_relative_path(project_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(project_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def _emit(
    command: str,
    options: CliOptions,
    payload: dict[str, Any],
    diagnostics: list[Diagnostic],
    text_lines: list[str],
) -> int:
    output_command = command
    if not command.startswith("project ") and command != "schemas list":
        output_command = f"project {command}"
    return emit_output(output_command, options, payload, diagnostics, text_lines)


def _render_validate_text(project_found: bool, diagnostics: list[Diagnostic]) -> list[str]:
    if project_found and not has_errors(diagnostics):
        return ["Project valid."]
    return []


def _output_format(options: CliOptions) -> str:
    return output_format(options)


def _register_commands() -> None:
    from isomer_labs.cli.commands.artifact_formats import register_artifact_format_commands
    from isomer_labs.cli.commands.deepsci_ext import register_deepsci_ext_commands
    from isomer_labs.cli.commands.doctor import register_doctor_commands
    from isomer_labs.cli.commands.handoffs import register_handoff_commands
    from isomer_labs.cli.commands.project import register_project_commands, register_schema_commands
    from isomer_labs.cli.commands.research_records_ext import register_research_record_ext_commands
    from isomer_labs.cli.commands.runtime import register_runtime_commands
    from isomer_labs.cli.commands.team_instances import register_team_instance_commands
    from isomer_labs.cli.commands.team_profiles import register_team_profile_commands
    from isomer_labs.cli.commands.team_templates import register_team_template_commands

    register_project_commands(project_group)
    register_doctor_commands(project_group)
    register_runtime_commands(project_group)
    register_artifact_format_commands(project_group)
    register_team_instance_commands(project_group)
    register_handoff_commands(project_group)
    register_team_template_commands(project_group)
    register_team_profile_commands(project_group)
    register_deepsci_ext_commands(app)
    register_research_record_ext_commands(app)
    register_schema_commands(app)


_register_commands()


if __name__ == "__main__":
    raise SystemExit(main())
