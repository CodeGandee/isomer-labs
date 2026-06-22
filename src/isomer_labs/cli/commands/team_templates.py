"""Click registration for Domain Agent Team Template commands."""

from __future__ import annotations

import click

from isomer_labs.cli.app import (
    _cmd_team_templates_inspect,
    _cmd_team_templates_list,
    _cmd_team_templates_validate,
)
from isomer_labs.cli.options import common_options as _common_options, merge_options as _merge_options


def register_team_template_commands(app: click.Group) -> None:
    @app.group(name="team-templates", help="Domain Agent Team Template commands.")
    def team_templates_group() -> None:
        pass


    @team_templates_group.command(name="list", help="List registered Domain Agent Team Templates.")
    @_common_options
    @click.pass_context
    def team_templates_list_command(
        ctx: click.Context,
        project: str | None = None,
        manifest: str | None = None,
        output_format: str | None = None,
        json_output: bool = False,
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
        project: str | None = None,
        manifest: str | None = None,
        output_format: str | None = None,
        json_output: bool = False,
        template_id: str = "",
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
        project: str | None = None,
        manifest: str | None = None,
        output_format: str | None = None,
        json_output: bool = False,
        template_id: str = "",
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
