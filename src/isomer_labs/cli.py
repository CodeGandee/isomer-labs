"""Command line interface for Isomer Labs Milestone 1."""

from __future__ import annotations

from dataclasses import dataclass, replace
import json
import os
from pathlib import Path
from typing import Any, Sequence

import click

from isomer_labs.builtins import list_built_in_schemas
from isomer_labs.context import resolve_effective_topic_context
from isomer_labs.diagnostics import Diagnostic, has_errors
from isomer_labs.doctor import build_doctor_report, render_doctor_text
from isomer_labs.houmao_manifests import (
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
from isomer_labs.houmao_cli_adapter import HoumaoAdapterFacade
from isomer_labs.init_project import initialize_project
from isomer_labs.models import EffectiveTopicContext, Project, ProjectState, SelectionRequest, TopicAgentTeamProfile
from isomer_labs.paths import preview_paths
from isomer_labs.project import discover_project
from isomer_labs.rendering import render_diagnostics, render_json, render_key_values
from isomer_labs.runtime_store import (
    initialize_workspace_runtime,
    open_workspace_runtime,
    prepare_topic_environment_readiness,
)
from isomer_labs.runtime_models import AdapterManifestRefRecord, AdapterReconciliationRecord, utc_timestamp
from isomer_labs.runtime_validation import inspect_workspace_runtime, validate_workspace_runtime
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
  doctor
  validate
  topics list
  workspaces list
  context show
  paths preview
  schemas list
  runtime init
  runtime prepare
  runtime inspect
  runtime validate
  team-instances create
  team-instances list
  team-instances show
  team-instances adapter-link export
  team-instances launch-material prepare
  team-instances launch
  team-instances inspect-live
  team-instances stop
  team-instances reconcile
  team-instances adopt
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


@app.command(name="doctor", help="Run read-only dependency, Project, and topic diagnostics.")
@_common_options
@_topic_selection_options
@click.pass_context
def doctor_command(
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
    return _cmd_doctor(
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


@app.group(name="runtime", help="Workspace Runtime commands.")
def runtime_group() -> None:
    pass


@runtime_group.command(name="init", help="Initialize or reopen the selected Workspace Runtime.")
@_common_options
@_topic_selection_options
@click.pass_context
def runtime_init_command(
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
    return _cmd_runtime_init(
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


@runtime_group.command(name="prepare", help="Record selected topic environment readiness.")
@_common_options
@_topic_selection_options
@click.option("--actor", "actor_ref", default=None, help="Actor ref to record on the readiness check.")
@click.pass_context
def runtime_prepare_command(
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
    actor_ref: str | None,
) -> int:
    return _cmd_runtime_prepare(
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
        actor_ref=actor_ref,
    )


@runtime_group.command(name="inspect", help="Inspect Workspace Runtime metadata without mutation.")
@_common_options
@_topic_selection_options
@click.pass_context
def runtime_inspect_command(
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
    return _cmd_runtime_inspect(
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


@runtime_group.command(name="validate", help="Validate Workspace Runtime records without mutation.")
@_common_options
@_topic_selection_options
@click.option(
    "--require-ready-readiness",
    is_flag=True,
    help="Treat missing or failed readiness as a launch-facing error.",
)
@click.pass_context
def runtime_validate_command(
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
    require_ready_readiness: bool,
) -> int:
    return _cmd_runtime_validate(
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
        require_ready_readiness=require_ready_readiness,
    )


@app.group(name="team-instances", help="Agent Team Instance commands.")
def team_instances_group() -> None:
    pass


@team_instances_group.command(name="create", help="Create an Agent Team Instance record.")
@_common_options
@_topic_selection_options
@click.option("--id", "instance_id", default=None, help="Agent Team Instance id.")
@click.pass_context
def team_instances_create_command(
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
    instance_id: str | None,
) -> int:
    return _cmd_team_instances_create(
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
        instance_id=instance_id,
    )


@team_instances_group.command(name="list", help="List Agent Team Instance records.")
@_common_options
@_topic_selection_options
@click.pass_context
def team_instances_list_command(
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
    return _cmd_team_instances_list(
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


@team_instances_group.command(name="show", help="Show one Agent Team Instance record.")
@_common_options
@_topic_selection_options
@click.argument("agent_team_instance_id_arg")
@click.pass_context
def team_instances_show_command(
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
    agent_team_instance_id_arg: str,
) -> int:
    return _cmd_team_instances_show(
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
        agent_team_instance_id_arg,
    )


@team_instances_group.group(name="adapter-link", help="Houmao adapter link manifest commands.")
def team_instances_adapter_link_group() -> None:
    pass


@team_instances_adapter_link_group.command(name="export", help="Write or print a Houmao adapter link JSON manifest.")
@_common_options
@_topic_selection_options
@click.argument("agent_team_instance_id_arg")
@click.option("--output", "output_path", default=None, help="Output path for adapter-link.json.")
@click.option("--print", "print_manifest", is_flag=True, help="Print the manifest instead of writing it.")
@click.option("--houmao-project-dir", default=None, help="Houmao project overlay directory ref.")
@click.option("--actor", "actor_ref", default=None, help="Actor ref for manifest provenance.")
@click.pass_context
def team_instances_adapter_link_export_command(
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
    agent_team_instance_id_arg: str,
    output_path: str | None,
    print_manifest: bool,
    houmao_project_dir: str | None,
    actor_ref: str | None,
) -> int:
    return _cmd_team_instances_adapter_link_export(
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
        agent_team_instance_id=agent_team_instance_id_arg,
        output_path=output_path,
        print_manifest=print_manifest,
        houmao_project_dir=houmao_project_dir,
        actor_ref=actor_ref,
    )


@team_instances_group.group(name="launch-material", help="Agent Team Instance launch material commands.")
def team_instances_launch_material_group() -> None:
    pass


@team_instances_launch_material_group.command(name="prepare", help="Prepare Houmao launch material without launching agents.")
@_common_options
@_topic_selection_options
@click.argument("agent_team_instance_id_arg")
@click.option("--adapter", default="houmao", type=click.Choice(("houmao",)), help="Execution Adapter.")
@click.option("--houmao-project-dir", default=None, help="Houmao project overlay directory ref.")
@click.option("--actor", "actor_ref", default=None, help="Actor ref for materialization provenance.")
@click.pass_context
def team_instances_launch_material_prepare_command(
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
    agent_team_instance_id_arg: str,
    adapter: str,
    houmao_project_dir: str | None,
    actor_ref: str | None,
) -> int:
    return _cmd_team_instances_launch_material_prepare(
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
        agent_team_instance_id=agent_team_instance_id_arg,
        adapter=adapter,
        houmao_project_dir=houmao_project_dir,
        actor_ref=actor_ref,
    )


@team_instances_group.command(name="launch", help="Quick-launch a Houmao-backed Agent Team Instance.")
@_common_options
@_topic_selection_options
@click.argument("agent_team_instance_id_arg")
@click.option("--adapter", default="houmao", type=click.Choice(("houmao",)), help="Execution Adapter.")
@click.option("--houmao-project-dir", default=None, help="Houmao project overlay directory ref.")
@click.option("--actor", "actor_ref", default=None, help="Actor ref for launch provenance.")
@click.pass_context
def team_instances_launch_command(
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
    agent_team_instance_id_arg: str,
    adapter: str,
    houmao_project_dir: str | None,
    actor_ref: str | None,
) -> int:
    return _cmd_team_instances_launch(
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
        agent_team_instance_id=agent_team_instance_id_arg,
        adapter=adapter,
        houmao_project_dir=houmao_project_dir,
        actor_ref=actor_ref,
    )


@team_instances_group.command(name="inspect-live", help="Inspect Houmao adapter manifest integrity without mutation.")
@_common_options
@_topic_selection_options
@click.argument("agent_team_instance_id_arg")
@click.option("--adapter", default=None, type=click.Choice(("houmao",)), help="Execution Adapter for live inspection.")
@click.option("--integrity", is_flag=True, help="Include manifest and material integrity status.")
@click.option("--link-manifest", default=None, help="Explicit adapter-link.json path.")
@click.option("--launch-material-manifest", default=None, help="Explicit launch-material-manifest.json path.")
@click.option("--runtime-manifest", default=None, help="Explicit adapter-runtime-manifest.json path.")
@click.option("--live-state-json", default=None, help="Path to deterministic Houmao live-state JSON for tests or offline inspection.")
@click.option("--houmao-project-dir", default=None, help="Houmao project overlay directory ref for read-only inspection.")
@click.option("--actor", "actor_ref", default=None, help="Actor ref for inspection provenance.")
@click.pass_context
def team_instances_inspect_live_command(
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
    agent_team_instance_id_arg: str,
    adapter: str | None,
    integrity: bool,
    link_manifest: str | None,
    launch_material_manifest: str | None,
    runtime_manifest: str | None,
    live_state_json: str | None,
    houmao_project_dir: str | None,
    actor_ref: str | None,
) -> int:
    return _cmd_team_instances_manifest_inspect(
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
        agent_team_instance_id=agent_team_instance_id_arg,
        link_manifest=link_manifest,
        launch_material_manifest=launch_material_manifest,
        runtime_manifest=runtime_manifest,
        live_state_json=live_state_json,
        houmao_project_dir=houmao_project_dir,
        include_integrity=integrity,
        adapter=adapter,
        actor_ref=actor_ref,
    )


@team_instances_group.command(name="stop", help="Stop a Houmao-backed Agent Team Instance.")
@_common_options
@_topic_selection_options
@click.argument("agent_team_instance_id_arg")
@click.option("--adapter", default="houmao", type=click.Choice(("houmao",)), help="Execution Adapter.")
@click.option("--link-manifest", default=None, help="Explicit adapter-link.json path.")
@click.option("--actor", "actor_ref", default=None, help="Actor ref for stop provenance.")
@click.pass_context
def team_instances_stop_command(
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
    agent_team_instance_id_arg: str,
    adapter: str,
    link_manifest: str | None,
    actor_ref: str | None,
) -> int:
    return _cmd_team_instances_stop(
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
        agent_team_instance_id=agent_team_instance_id_arg,
        adapter=adapter,
        link_manifest=link_manifest,
        actor_ref=actor_ref,
    )


@team_instances_group.command(name="reconcile", help="Record Houmao adapter manifest reconciliation state.")
@_common_options
@_topic_selection_options
@click.argument("agent_team_instance_id_arg")
@click.option("--link-manifest", default=None, help="Explicit adapter-link.json path.")
@click.option("--launch-material-manifest", default=None, help="Explicit launch-material-manifest.json path.")
@click.option("--runtime-manifest", default=None, help="Explicit adapter-runtime-manifest.json path.")
@click.option("--live-state-json", default=None, help="Path to deterministic Houmao live-state JSON for tests or offline reconciliation.")
@click.option("--houmao-project-dir", default=None, help="Houmao project overlay directory ref for read-only inspection.")
@click.option("--actor", "actor_ref", default=None, help="Actor ref for reconciliation provenance.")
@click.pass_context
def team_instances_reconcile_command(
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
    agent_team_instance_id_arg: str,
    link_manifest: str | None,
    launch_material_manifest: str | None,
    runtime_manifest: str | None,
    live_state_json: str | None,
    houmao_project_dir: str | None,
    actor_ref: str | None,
) -> int:
    return _cmd_team_instances_reconcile(
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
        agent_team_instance_id=agent_team_instance_id_arg,
        link_manifest=link_manifest,
        launch_material_manifest=launch_material_manifest,
        runtime_manifest=runtime_manifest,
        live_state_json=live_state_json,
        houmao_project_dir=houmao_project_dir,
        actor_ref=actor_ref,
        adopt=False,
    )


@team_instances_group.command(name="adopt", help="Adopt externally launched Houmao runtime state.")
@_common_options
@_topic_selection_options
@click.argument("agent_team_instance_id_arg")
@click.option("--yes", "approved", is_flag=True, help="Confirm adoption of externally launched adapter state.")
@click.option("--link-manifest", default=None, help="Explicit adapter-link.json path.")
@click.option("--launch-material-manifest", default=None, help="Explicit launch-material-manifest.json path.")
@click.option("--runtime-manifest", default=None, help="Explicit adapter-runtime-manifest.json path.")
@click.option("--live-state-json", default=None, help="Path to deterministic Houmao live-state JSON for tests or offline adoption.")
@click.option("--houmao-project-dir", default=None, help="Houmao project overlay directory ref for read-only inspection.")
@click.option("--actor", "actor_ref", default=None, help="Actor ref for adoption provenance.")
@click.pass_context
def team_instances_adopt_command(
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
    agent_team_instance_id_arg: str,
    approved: bool,
    link_manifest: str | None,
    launch_material_manifest: str | None,
    runtime_manifest: str | None,
    live_state_json: str | None,
    houmao_project_dir: str | None,
    actor_ref: str | None,
) -> int:
    return _cmd_team_instances_reconcile(
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
        agent_team_instance_id=agent_team_instance_id_arg,
        link_manifest=link_manifest,
        launch_material_manifest=launch_material_manifest,
        runtime_manifest=runtime_manifest,
        live_state_json=live_state_json,
        houmao_project_dir=houmao_project_dir,
        actor_ref=actor_ref,
        adopt=True,
        approved=approved,
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
    if _output_format(options) == "json":
        click.echo(render_json("doctor", report.to_payload(), report.diagnostics))
    else:
        lines = [*render_doctor_text(report), *render_diagnostics(report.diagnostics)]
        if lines:
            click.echo("\n".join(lines))
    return 0 if report.ok else 1


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
    registration_suggestion: dict[str, str] | None = None
    if write_profile and not has_errors(diagnostics):
        profile.source_path.parent.mkdir(parents=True, exist_ok=True)
        profile.source_path.write_text(profile_to_toml(profile), encoding="utf-8")
        written_path = str(profile.source_path)
        registration_suggestion = _profile_registration_suggestion(context.project.root, profile)
    payload = {
        "profile": profile.to_json(),
        "validation": profile_report.to_json(),
        "written_path": written_path,
        "registration_suggestion": registration_suggestion,
    }
    lines = [
        f"Topic Agent Team Profile: {profile.id}",
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
    output_path: str | None,
    print_manifest: bool,
    houmao_project_dir: str | None,
    actor_ref: str | None,
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
    agent_team_instance_id: str,
    adapter: str,
    houmao_project_dir: str | None,
    actor_ref: str | None,
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
    agent_team_instance_id: str,
    adapter: str,
    houmao_project_dir: str | None,
    actor_ref: str | None,
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
    agent_team_instance_id: str,
    link_manifest: str | None,
    launch_material_manifest: str | None,
    runtime_manifest: str | None,
    live_state_json: str | None,
    houmao_project_dir: str | None,
    include_integrity: bool,
    adapter: str | None,
    actor_ref: str | None,
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
    agent_team_instance_id: str,
    adapter: str,
    link_manifest: str | None,
    actor_ref: str | None,
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
    agent_team_instance_id: str,
    link_manifest: str | None,
    launch_material_manifest: str | None,
    runtime_manifest: str | None,
    live_state_json: str | None,
    houmao_project_dir: str | None,
    actor_ref: str | None,
    adopt: bool,
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


def _manifest_output_path(
    context: EffectiveTopicContext,
    agent_team_instance_id: str,
    output_path: str | None,
    manifest_kind: str,
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
    agent_team_instance_id: str,
    link_manifest: str | None,
    launch_material_manifest: str | None,
    runtime_manifest: str | None,
    diagnostics: list[Diagnostic],
    require_link: bool,
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
    expected_kind: str,
    diagnostics: list[Diagnostic],
    required: bool,
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
    live_state_json: str | None,
    houmao_project_dir: str | None,
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
    agent_team_instance_id: str,
    adapter_manifest_kind: str,
    manifest_path: Path,
    manifest_digest: str,
    source: str,
    path_plan_id: str | None,
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
    agent_team_instance_id: str,
    result: Any,
    actor_ref: str | None,
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
