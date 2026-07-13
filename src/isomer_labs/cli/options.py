"""Shared Click option helpers and resolved CLI options."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

import click

from isomer_labs.cli.output import OutputMode


@dataclass(frozen=True)
class CliOptions:
    project: str | None = None
    manifest: str | None = None
    output_format: str | None = None
    json_output: bool = False
    output_mode: OutputMode = OutputMode()
    debug: bool = False
    topic_id: str | None = None
    topic_id_option: str | None = None
    topic_statement: str | None = None
    topic_workspace_dir: str | None = None
    topic_status: str | None = None
    topic_set_default: bool = False
    topic_new_id: str | None = None
    topic_delete_dry_run: bool = False
    topic_delete_yes: bool = False
    content_dir: str | None = None
    research_topic_id: str | None = None
    topic_workspace_id: str | None = None
    doctor_topics: tuple[str, ...] = ()
    research_inquiry_id: str | None = None
    research_task_id: str | None = None
    run_id: str | None = None
    agent_team_instance_id: str | None = None
    agent_instance_id: str | None = None
    agent_name: str | None = None
    topic_actor_name: str | None = None
    topic_agent_team_profile_id: str | None = None
    cleanup_parts: tuple[str, ...] = ()
    cleanup_topics: tuple[str, ...] = ()
    cleanup_all_topics: bool = False
    cleanup_purge_content_root: bool = False
    cleanup_dry_run: bool = False
    cleanup_yes: bool = False
    content_root_to: str | None = None
    content_root_move_dry_run: bool = False
    content_root_move_yes: bool = False
    paths_configured: bool = False
    callback_id: str | None = None
    callback_skill: str | None = None
    callback_stage: str | None = None
    callback_scope: str | None = None
    callback_prompt: str | None = None
    callback_prompt_file: str | None = None
    callback_skill_dir: str | None = None
    callback_priority: int | None = None
    callback_allow_external_source: bool = False
    callback_toolbox_dir: str | None = None
    callback_replace_toolbox_source: bool = False
    callback_extensions: tuple[str, ...] = ()
    callback_all_catalog_extensions: bool = False
    callback_core_only: bool = False
    extension_id: str | None = None
    system_extension_targets: tuple[str, ...] = ()
    toolbox_dir: str | None = None
    toolbox_id: str | None = None
    toolbox_source_path: str | None = None
    toolbox_scope: str | None = None
    toolbox_status: str | None = None
    toolbox_install_runtime_defaults: bool = False
    toolbox_param_id: str | None = None
    toolbox_param_key: str | None = None
    toolbox_param_value: str | None = None
    toolbox_param_value_type: str | None = None
    toolbox_param_allowed_values: tuple[str, ...] = ()
    toolbox_param_description: str | None = None
    toolbox_import_path: str | None = None
    houmao_skill_route: str | None = None
    topic_service_master_status: str | None = None
    topic_service_master_specialist_name: str | None = None
    topic_service_master_launch_profile_name: str | None = None
    topic_service_master_managed_agent_name: str | None = None
    topic_service_master_specialist_ref: str | None = None
    topic_service_master_launch_profile_ref: str | None = None
    topic_service_master_managed_agent_ref: str | None = None
    topic_service_master_updated_by: str | None = None


def common_options(command: Any) -> Any:
    command = click.option("--manifest", default=None, hidden=True, help="Explicit Project Manifest selector.")(command)
    command = click.option("--project", default=None, hidden=True, help="Explicit Project root selector.")(command)
    return command


def topic_selection_options(command: Any) -> Any:
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


def merge_options(
    ctx: click.Context,
    *,
    project: str | None = None,
    manifest: str | None = None,
    output_format: str | None = None,
    json_output: bool = False,
    **values: Any,
) -> CliOptions:
    current = ctx.obj
    root = ctx.find_root().obj
    root_options = (
        current
        if isinstance(current, CliOptions)
        else root
        if isinstance(root, CliOptions)
        else CliOptions()
    )
    print_json = root_options.output_mode.print_json or json_output or output_format == "json"
    return replace(
        root_options,
        project=project if project is not None else root_options.project,
        manifest=manifest if manifest is not None else root_options.manifest,
        output_format=output_format if output_format is not None else root_options.output_format,
        json_output=root_options.json_output or json_output,
        output_mode=OutputMode(print_json=print_json),
        **values,
    )


def value(options: CliOptions, name: str, default: object | None = None) -> Any:
    return getattr(options, name, default)
