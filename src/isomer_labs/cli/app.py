"""Click app bootstrap for Isomer Labs."""

from __future__ import annotations

from dataclasses import replace
from typing import Sequence

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
  project topic-main-guidance render
  project topic-main-guidance inspect
  project topic-main-guidance ensure
  project workspaces list
  project skill-callbacks register
  project skill-callbacks resolve
  project skill-callbacks list
  project skill-callbacks show
  project skill-callbacks disable
  project skill-callbacks validate
  project context show
  project self show
  project self identity
  project self pixi
  project self env
  project self paths
  project self queries
  project repos create
  project outputs policy
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
  project topic-reset checkpoint
  project topic-reset update-checkpoint
  project topic-reset list
  project topic-reset show
  project topic-reset plan
  project topic-reset show-plan
  project topic-reset apply
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
  project team-templates register
  project team-repositories list
  project team-repositories inspect
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
    from isomer_labs.cli.commands.team_repositories import register_team_repository_commands
    from isomer_labs.cli.commands.team_templates import register_team_template_commands
    from isomer_labs.cli.commands.topic_reset import register_topic_reset_commands

    register_project_commands(project_group)
    register_doctor_commands(project_group)
    register_runtime_commands(project_group)
    register_artifact_format_commands(project_group)
    register_topic_reset_commands(project_group)
    register_team_instance_commands(project_group)
    register_handoff_commands(project_group)
    register_team_repository_commands(project_group)
    register_team_template_commands(project_group)
    register_team_profile_commands(project_group)
    register_deepsci_ext_commands(app)
    register_research_record_ext_commands(app)
    register_schema_commands(app)


_register_commands()


if __name__ == "__main__":
    raise SystemExit(main())
