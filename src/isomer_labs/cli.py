"""Command line interface for Isomer Labs Milestone 1."""

from __future__ import annotations

from dataclasses import dataclass, replace
import os
from pathlib import Path
from typing import Any, Sequence

import click

from isomer_labs.builtins import list_built_in_schemas
from isomer_labs.context import resolve_effective_topic_context
from isomer_labs.diagnostics import Diagnostic, has_errors
from isomer_labs.init_project import initialize_project
from isomer_labs.models import EffectiveTopicContext, Project, ProjectState, SelectionRequest
from isomer_labs.paths import preview_paths
from isomer_labs.project import discover_project
from isomer_labs.rendering import render_diagnostics, render_json, render_key_values
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
from isomer_labs.toml_loader import load_toml
from isomer_labs.validation import build_project_state


@dataclass(frozen=True)
class CliOptions:
    project: str | None = None
    manifest: str | None = None
    output_format: str | None = None
    json_output: bool = False
    topic_id: str | None = None
    topic_id_option: str | None = None
    topic_statement: str | None = None
    research_topic_id: str | None = None
    topic_workspace_id: str | None = None
    research_inquiry_id: str | None = None
    research_task_id: str | None = None
    run_id: str | None = None
    agent_team_instance_id: str | None = None
    agent_instance_id: str | None = None
    topic_agent_team_profile_id: str | None = None


COMMAND_SURFACE = """Milestone 1 Isomer Labs Project discovery and path preview CLI.

\b
Command surface:
  init
  validate
  topics list
  workspaces list
  context show
  paths preview
  schemas list
  team-templates list
  team-templates inspect
  team-templates validate
  team-profiles specialize
  team-profiles validate
"""


def main(argv: Sequence[str] | None = None) -> int:
    """Run the Click-backed CLI and return a process status code."""

    try:
        result = app.main(
            args=list(argv) if argv is not None else None,
            prog_name="isomer-cli",
            standalone_mode=False,
        )
    except click.exceptions.Exit as exc:
        return int(exc.exit_code)
    except click.ClickException as exc:
        exc.show()
        return int(exc.exit_code)
    if result is None:
        return 0
    return int(result)


def build_parser() -> click.Group:
    """Return the Click command object used by the installed entrypoint."""

    return app


def _common_options(command: Any) -> Any:
    command = click.option("--json", "json_output", is_flag=True, help="Emit JSON.")(command)
    command = click.option(
        "--format",
        "output_format",
        type=click.Choice(("text", "json")),
        default=None,
        help="Output format.",
    )(command)
    command = click.option("--manifest", default=None, help="Explicit Project Manifest selector.")(command)
    command = click.option("--project", default=None, help="Explicit Project root selector.")(command)
    return command


def _topic_selection_options(command: Any) -> Any:
    command = click.option(
        "--topic-agent-team-profile",
        "topic_agent_team_profile_id",
        default=None,
        help="Topic Agent Team Profile id.",
    )(command)
    command = click.option("--agent-instance", "agent_instance_id", default=None, help="Agent Instance id.")(command)
    command = click.option(
        "--agent-team-instance",
        "agent_team_instance_id",
        default=None,
        help="Agent Team Instance id.",
    )(command)
    command = click.option("--run", "run_id", default=None, help="Run id.")(command)
    command = click.option("--task", "research_task_id", default=None, help="Research Task id.")(command)
    command = click.option("--research-inquiry", "research_inquiry_id", default=None, help="Research Inquiry id.")(command)
    command = click.option("--topic-workspace", "topic_workspace_id", default=None, help="Topic Workspace id.")(command)
    command = click.option("--topic", "research_topic_id", default=None, help="Research Topic id.")(command)
    return command


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    help=COMMAND_SURFACE,
    invoke_without_command=True,
)
@_common_options
@click.pass_context
def app(
    ctx: click.Context,
    project: str | None,
    manifest: str | None,
    output_format: str | None,
    json_output: bool,
) -> None:
    ctx.obj = CliOptions(
        project=project,
        manifest=manifest,
        output_format=output_format,
        json_output=json_output,
    )
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@app.command(name="init", help="Initialize the smallest valid Project configuration.")
@_common_options
@click.argument("topic_id", required=False)
@click.option("--topic-id", "topic_id_option", help="Research Topic id to initialize.")
@click.option("--topic-statement", help="Short inline Research Topic statement.")
@click.pass_context
def init_command(
    ctx: click.Context,
    project: str | None,
    manifest: str | None,
    output_format: str | None,
    json_output: bool,
    topic_id: str | None,
    topic_id_option: str | None,
    topic_statement: str | None,
) -> int:
    return _cmd_init(
        _merge_options(
            ctx,
            project=project,
            manifest=manifest,
            output_format=output_format,
            json_output=json_output,
            topic_id=topic_id,
            topic_id_option=topic_id_option,
            topic_statement=topic_statement,
        )
    )


@app.command(name="validate", help="Validate the Project Manifest and registered configs.")
@_common_options
@click.pass_context
def validate_command(
    ctx: click.Context,
    project: str | None,
    manifest: str | None,
    output_format: str | None,
    json_output: bool,
) -> int:
    return _cmd_validate(
        _merge_options(
            ctx,
            project=project,
            manifest=manifest,
            output_format=output_format,
            json_output=json_output,
        )
    )


@app.group(name="topics", help="Research Topic commands.")
def topics_group() -> None:
    pass


@topics_group.command(name="list", help="List registered Research Topics.")
@_common_options
@click.pass_context
def topics_list_command(
    ctx: click.Context,
    project: str | None,
    manifest: str | None,
    output_format: str | None,
    json_output: bool,
) -> int:
    return _cmd_topics_list(
        _merge_options(
            ctx,
            project=project,
            manifest=manifest,
            output_format=output_format,
            json_output=json_output,
        )
    )


@app.group(name="workspaces", help="Topic Workspace commands.")
def workspaces_group() -> None:
    pass


@workspaces_group.command(name="list", help="List registered Topic Workspaces.")
@_common_options
@click.pass_context
def workspaces_list_command(
    ctx: click.Context,
    project: str | None,
    manifest: str | None,
    output_format: str | None,
    json_output: bool,
) -> int:
    return _cmd_workspaces_list(
        _merge_options(
            ctx,
            project=project,
            manifest=manifest,
            output_format=output_format,
            json_output=json_output,
        )
    )


@app.group(name="context", help="Effective Topic Context commands.")
def context_group() -> None:
    pass


@context_group.command(name="show", help="Show resolved Effective Topic Context.")
@_common_options
@_topic_selection_options
@click.pass_context
def context_show_command(
    ctx: click.Context,
    project: str | None,
    manifest: str | None,
    output_format: str | None,
    json_output: bool,
    research_topic_id: str | None,
    topic_workspace_id: str | None,
    research_inquiry_id: str | None,
    research_task_id: str | None,
    run_id: str | None,
    agent_team_instance_id: str | None,
    agent_instance_id: str | None,
    topic_agent_team_profile_id: str | None,
) -> int:
    return _cmd_context_show(
        _merge_options(
            ctx,
            project=project,
            manifest=manifest,
            output_format=output_format,
            json_output=json_output,
            research_topic_id=research_topic_id,
            topic_workspace_id=topic_workspace_id,
            research_inquiry_id=research_inquiry_id,
            research_task_id=research_task_id,
            run_id=run_id,
            agent_team_instance_id=agent_team_instance_id,
            agent_instance_id=agent_instance_id,
            topic_agent_team_profile_id=topic_agent_team_profile_id,
        )
    )


@app.group(name="paths", help="Workspace Path Resolution commands.")
def paths_group() -> None:
    pass


@paths_group.command(name="preview", help="Preview workspace paths without creating them.")
@_common_options
@_topic_selection_options
@click.pass_context
def paths_preview_command(
    ctx: click.Context,
    project: str | None,
    manifest: str | None,
    output_format: str | None,
    json_output: bool,
    research_topic_id: str | None,
    topic_workspace_id: str | None,
    research_inquiry_id: str | None,
    research_task_id: str | None,
    run_id: str | None,
    agent_team_instance_id: str | None,
    agent_instance_id: str | None,
    topic_agent_team_profile_id: str | None,
) -> int:
    return _cmd_paths_preview(
        _merge_options(
            ctx,
            project=project,
            manifest=manifest,
            output_format=output_format,
            json_output=json_output,
            research_topic_id=research_topic_id,
            topic_workspace_id=topic_workspace_id,
            research_inquiry_id=research_inquiry_id,
            research_task_id=research_task_id,
            run_id=run_id,
            agent_team_instance_id=agent_team_instance_id,
            agent_instance_id=agent_instance_id,
            topic_agent_team_profile_id=topic_agent_team_profile_id,
        )
    )


@app.group(name="schemas", help="Built-in schema commands.")
def schemas_group() -> None:
    pass


@schemas_group.command(name="list", help="List Isomer built-in schemas and contracts.")
@_common_options
@click.pass_context
def schemas_list_command(
    ctx: click.Context,
    project: str | None,
    manifest: str | None,
    output_format: str | None,
    json_output: bool,
) -> int:
    return _cmd_schemas_list(
        _merge_options(
            ctx,
            project=project,
            manifest=manifest,
            output_format=output_format,
            json_output=json_output,
        )
    )


@app.group(name="team-templates", help="Domain Agent Team Template commands.")
def team_templates_group() -> None:
    pass


@team_templates_group.command(name="list", help="List registered Domain Agent Team Templates.")
@_common_options
@click.pass_context
def team_templates_list_command(
    ctx: click.Context,
    project: str | None,
    manifest: str | None,
    output_format: str | None,
    json_output: bool,
) -> int:
    return _cmd_team_templates_list(
        _merge_options(
            ctx,
            project=project,
            manifest=manifest,
            output_format=output_format,
            json_output=json_output,
        )
    )


@team_templates_group.command(name="inspect", help="Inspect a registered Domain Agent Team Template.")
@_common_options
@click.argument("template_id")
@click.pass_context
def team_templates_inspect_command(
    ctx: click.Context,
    project: str | None,
    manifest: str | None,
    output_format: str | None,
    json_output: bool,
    template_id: str,
) -> int:
    return _cmd_team_templates_inspect(
        _merge_options(
            ctx,
            project=project,
            manifest=manifest,
            output_format=output_format,
            json_output=json_output,
        ),
        template_id,
    )


@team_templates_group.command(name="validate", help="Validate a registered Domain Agent Team Template.")
@_common_options
@click.argument("template_id")
@click.pass_context
def team_templates_validate_command(
    ctx: click.Context,
    project: str | None,
    manifest: str | None,
    output_format: str | None,
    json_output: bool,
    template_id: str,
) -> int:
    return _cmd_team_templates_validate(
        _merge_options(
            ctx,
            project=project,
            manifest=manifest,
            output_format=output_format,
            json_output=json_output,
        ),
        template_id,
    )


@app.group(name="team-profiles", help="Topic Agent Team Profile commands.")
def team_profiles_group() -> None:
    pass


@team_profiles_group.command(name="specialize", help="Derive a candidate Topic Agent Team Profile.")
@_common_options
@_topic_selection_options
@click.option("--template", "template_id", default=None, help="Domain Agent Team Template id.")
@click.option("--profile-id", default=None, help="Candidate Topic Agent Team Profile id.")
@click.option("--role", "roles", multiple=True, help="Agent Role id to activate. May be repeated.")
@click.option("--expected-artifact", "expected_artifacts", multiple=True, help="Expected Artifact ref. May be repeated.")
@click.option("--use-case", default=None, help="Use-case fixture label such as UC-01.")
@click.option("--write", "write_profile", is_flag=True, help="Write the generated profile to the Project Config Directory.")
@click.pass_context
def team_profiles_specialize_command(
    ctx: click.Context,
    project: str | None,
    manifest: str | None,
    output_format: str | None,
    json_output: bool,
    research_topic_id: str | None,
    topic_workspace_id: str | None,
    research_inquiry_id: str | None,
    research_task_id: str | None,
    run_id: str | None,
    agent_team_instance_id: str | None,
    agent_instance_id: str | None,
    topic_agent_team_profile_id: str | None,
    template_id: str | None,
    profile_id: str | None,
    roles: tuple[str, ...],
    expected_artifacts: tuple[str, ...],
    use_case: str | None,
    write_profile: bool,
) -> int:
    return _cmd_team_profiles_specialize(
        _merge_options(
            ctx,
            project=project,
            manifest=manifest,
            output_format=output_format,
            json_output=json_output,
            research_topic_id=research_topic_id,
            topic_workspace_id=topic_workspace_id,
            research_inquiry_id=research_inquiry_id,
            research_task_id=research_task_id,
            run_id=run_id,
            agent_team_instance_id=agent_team_instance_id,
            agent_instance_id=agent_instance_id,
            topic_agent_team_profile_id=topic_agent_team_profile_id,
        ),
        template_id=template_id,
        profile_id=profile_id,
        roles=list(roles),
        expected_artifacts=list(expected_artifacts),
        use_case=use_case,
        write_profile=write_profile,
    )


@team_profiles_group.command(name="validate", help="Validate a Topic Agent Team Profile file.")
@_common_options
@click.option("--template", "template_id", default=None, help="Domain Agent Team Template id.")
@click.argument("profile_path", required=False)
@click.pass_context
def team_profiles_validate_command(
    ctx: click.Context,
    project: str | None,
    manifest: str | None,
    output_format: str | None,
    json_output: bool,
    template_id: str | None,
    profile_path: str | None,
) -> int:
    return _cmd_team_profiles_validate(
        _merge_options(
            ctx,
            project=project,
            manifest=manifest,
            output_format=output_format,
            json_output=json_output,
        ),
        template_id=template_id,
        profile_path=profile_path,
    )


def _merge_options(
    ctx: click.Context,
    *,
    project: str | None = None,
    manifest: str | None = None,
    output_format: str | None = None,
    json_output: bool = False,
    **values: str | None,
) -> CliOptions:
    root = ctx.find_root().obj
    root_options = root if isinstance(root, CliOptions) else CliOptions()
    return replace(
        root_options,
        project=project if project is not None else root_options.project,
        manifest=manifest if manifest is not None else root_options.manifest,
        output_format=output_format if output_format is not None else root_options.output_format,
        json_output=root_options.json_output or json_output,
        **values,
    )


def _cmd_init(options: CliOptions) -> int:
    project_root = Path(_value(options, "project") or os.getcwd())
    topic_id = _value(options, "topic_id_option") or _value(options, "topic_id") or "default"
    diagnostics = initialize_project(
        project_root,
        topic_id=topic_id,
        topic_statement=_value(options, "topic_statement"),
    )
    payload = {
        "ok": not has_errors(diagnostics),
        "project_root": str(project_root.resolve(strict=False)),
        "research_topic_id": topic_id,
    }
    if _output_format(options) == "json":
        click.echo(render_json("init", payload, diagnostics))
    elif diagnostics:
        click.echo("\n".join(render_diagnostics(diagnostics)))
    else:
        click.echo(f"Initialized Project: {project_root.resolve(strict=False)}")
        click.echo(f"Research Topic: {topic_id}")
        click.echo(f"Project Manifest: {project_root.resolve(strict=False) / '.isomer-labs' / 'manifest.toml'}")
    return 1 if has_errors(diagnostics) else 0


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


def _cmd_workspaces_list(options: CliOptions) -> int:
    project, diagnostics = _discover(options)
    workspaces: list[dict[str, object]] = []
    if project is not None:
        state = build_project_state(project)
        diagnostics.extend(state.diagnostics)
        seen_workspace_ids: set[str] = set()
        for workspace in project.manifest.topic_workspaces:
            seen_workspace_ids.add(workspace.id)
            workspaces.append(
                {
                    **workspace.to_json(),
                    "source": "Project Manifest",
                    "effective_path": workspace.path_input or (
                        f"topic-workspaces/{workspace.research_topic_id}" if workspace.research_topic_id else None
                    ),
                }
            )
        for topic in project.manifest.research_topics:
            has_registered_workspace = (
                topic.topic_workspace_id in seen_workspace_ids
                if topic.topic_workspace_id is not None
                else any(workspace.get("research_topic_id") == topic.id for workspace in workspaces)
            )
            if not has_registered_workspace:
                workspaces.append(
                    {
                        "id": topic.id,
                        "research_topic_id": topic.id,
                        "path": f"topic-workspaces/{topic.id}",
                        "schema_version": "isomer-topic-workspace.v1",
                        "status": "active",
                        "source": "default",
                        "effective_path": f"topic-workspaces/{topic.id}",
                    }
                )
    payload = {"workspaces": workspaces}
    lines = ["Topic Workspaces"]
    lines.extend(
        f"- {workspace['id']} (topic: {workspace['research_topic_id']}, path: {workspace['effective_path']}, source: {workspace['source']})"
        for workspace in workspaces
    )
    return _emit("workspaces list", options, payload, diagnostics, lines)


def _cmd_context_show(options: CliOptions) -> int:
    context, diagnostics = _context_for_options(options)
    payload = {"context": context.to_json() if context is not None else None}
    if context is None:
        lines = []
    else:
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
            ]
        )
    return _emit("context show", options, payload, diagnostics, lines)


def _cmd_paths_preview(options: CliOptions) -> int:
    context, diagnostics = _context_for_options(options)
    entries: list[dict[str, object]] = []
    text_lines: list[str] = []
    if context is not None:
        resolved, path_diagnostics = preview_paths(context, env=os.environ)
        diagnostics.extend(path_diagnostics)
        entries = [entry.to_json() for entry in resolved]
        text_lines = ["Workspace Paths"]
        text_lines.extend(f"- {entry.surface}: {entry.path} ({entry.source})" for entry in resolved)
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
    template_id: str | None,
    profile_id: str | None,
    roles: list[str],
    expected_artifacts: list[str],
    use_case: str | None,
    write_profile: bool,
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
        selected_role_ids=roles or None,
        expected_artifacts=expected_artifacts or None,
        use_case=use_case,
    )
    profile_report = validate_topic_agent_team_profile(profile, template_report.template, project=context.project)
    diagnostics.extend(profile_report.diagnostics)
    written_path = None
    if write_profile and not has_errors(diagnostics):
        profile.source_path.parent.mkdir(parents=True, exist_ok=True)
        profile.source_path.write_text(profile_to_toml(profile), encoding="utf-8")
        written_path = str(profile.source_path)
    payload = {
        "profile": profile.to_json(),
        "validation": profile_report.to_json(),
        "written_path": written_path,
    }
    lines = [
        f"Topic Agent Team Profile: {profile.id}",
        f"Template: {profile.domain_agent_team_template_id}",
        f"Research Topic: {profile.research_topic_id}",
    ]
    if written_path is not None:
        lines.append(f"Written: {written_path}")
    return _emit("team-profiles specialize", options, payload, diagnostics, lines)


def _cmd_team_profiles_validate(
    options: CliOptions,
    *,
    template_id: str | None,
    profile_path: str | None,
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


def _emit(
    command: str,
    options: CliOptions,
    payload: dict[str, Any],
    diagnostics: list[Diagnostic],
    text_lines: list[str],
) -> int:
    if _output_format(options) == "json":
        click.echo(render_json(command, payload, diagnostics))
    else:
        lines = [*text_lines, *render_diagnostics(diagnostics)]
        if lines:
            click.echo("\n".join(lines))
    return 1 if has_errors(diagnostics) else 0


def _render_validate_text(project_found: bool, diagnostics: list[Diagnostic]) -> list[str]:
    if project_found and not has_errors(diagnostics):
        return ["Project valid."]
    return []


def _output_format(options: CliOptions) -> str:
    if bool(_value(options, "json_output", False)):
        return "json"
    return str(_value(options, "output_format", "text") or "text")


def _value(options: CliOptions, name: str, default: object | None = None) -> Any:
    return getattr(options, name, default)


if __name__ == "__main__":
    raise SystemExit(main())
