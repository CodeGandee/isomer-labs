"""Click app bootstrap for Isomer Labs."""

from __future__ import annotations

from dataclasses import replace
from importlib import metadata
from typing import Any, Sequence

import click

from isomer_labs.cli.errors import (
    emit_click_exception,
    emit_keyboard_interrupt,
    emit_unexpected_exception,
    normalize_raw_args,
    raw_debug_enabled,
)
from isomer_labs.cli.options import CliOptions
from isomer_labs.cli.output import OutputMode


REPOSITORY_URL = "https://github.com/CodeGandee/isomer-labs"
DOCUMENTATION_URL = "https://codegandee.github.io/isomer-labs/"
PACKAGE_NAME = "isomer-labs"


def _package_version() -> str:
    try:
        return metadata.version(PACKAGE_NAME)
    except metadata.PackageNotFoundError:
        return "unknown"


PACKAGE_VERSION = _package_version()

COMMAND_SURFACE = f"""Isomer Labs CLI for project setup, topic workspaces, research records, and the local web GUI.

\b
Repository: {REPOSITORY_URL}
Documentation: {DOCUMENTATION_URL}
"""


class HelpOnEmptyGroup(click.Group):
    """Click group that treats an empty group invocation as help."""

    group_class = type

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("invoke_without_command", True)
        super().__init__(*args, **kwargs)

    def invoke(self, ctx: click.Context) -> object:
        result = super().invoke(ctx)
        if ctx.invoked_subcommand is None and not ctx.resilient_parsing:
            click.echo(ctx.get_help())
        return result


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
    cls=HelpOnEmptyGroup,
    context_settings={"help_option_names": ["-h", "--help"]},
    help=COMMAND_SURFACE,
)
@click.option("--print-json", "print_json", is_flag=True, help="Emit deterministic JSON for the selected command.")
@click.option("--debug", "debug", is_flag=True, help="Include debug details for unexpected CLI errors.")
@click.version_option(PACKAGE_VERSION, "--version", prog_name="isomer-cli", message="%(prog)s %(version)s")
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


@app.group(name="project", help="Manage Isomer Projects, Research Topics, Workspace Runtime, records, and the local web GUI.")
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


def _register_commands() -> None:
    from isomer_labs.cli.commands.artifact_formats import register_artifact_format_commands
    from isomer_labs.cli.commands.deepsci_ext import register_deepsci_ext_commands
    from isomer_labs.cli.commands.doctor import register_doctor_commands
    from isomer_labs.cli.commands.handoffs import register_handoff_commands
    from isomer_labs.cli.commands.internals import register_internal_commands
    from isomer_labs.cli.commands.project import register_project_commands, register_schema_commands
    from isomer_labs.cli.commands.research_records_ext import register_research_record_ext_commands
    from isomer_labs.cli.commands.runtime import register_runtime_commands
    from isomer_labs.cli.commands.system_skills import register_system_skill_commands
    from isomer_labs.cli.commands.team_instances import register_team_instance_commands
    from isomer_labs.cli.commands.team_profiles import register_team_profile_commands
    from isomer_labs.cli.commands.team_repositories import register_team_repository_commands
    from isomer_labs.cli.commands.team_templates import register_team_template_commands
    from isomer_labs.cli.commands.topic_reset import register_topic_reset_commands
    from isomer_labs.cli.commands.web import register_web_commands

    register_doctor_commands(app)
    register_internal_commands(app)
    register_project_commands(project_group)
    register_runtime_commands(project_group)
    register_artifact_format_commands(project_group)
    register_topic_reset_commands(project_group)
    register_web_commands(project_group)
    register_team_instance_commands(project_group)
    register_handoff_commands(project_group)
    register_team_repository_commands(project_group)
    register_team_template_commands(project_group)
    register_team_profile_commands(project_group)
    register_deepsci_ext_commands(app)
    register_research_record_ext_commands(app)
    register_schema_commands(app)
    register_system_skill_commands(app)


_register_commands()


if __name__ == "__main__":
    raise SystemExit(main())
