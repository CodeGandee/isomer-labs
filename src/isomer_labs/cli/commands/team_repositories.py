"""Click registration for Team Repository commands."""

from __future__ import annotations

import click

from isomer_labs.cli.app import (
    _cmd_team_repositories_inspect,
    _cmd_team_repositories_list,
)
from isomer_labs.cli.options import common_options as _common_options, merge_options as _merge_options


def register_team_repository_commands(app: click.Group) -> None:
    @app.group(name="team-repositories", help="Team Repository commands.")
    def team_repositories_group() -> None:
        pass

    @team_repositories_group.command(name="list", help="List configured Team Repositories.")
    @_common_options
    @click.pass_context
    def team_repositories_list_command(
        ctx: click.Context,
        project: str | None = None,
        manifest: str | None = None,
        output_format: str | None = None,
        json_output: bool = False,
    ) -> int:
        return _cmd_team_repositories_list(
            _merge_options(
                ctx,
                project=project,
                manifest=manifest,
                output_format=output_format,
                json_output=json_output,
            )
        )

    @team_repositories_group.command(name="inspect", help="Inspect a configured Team Repository.")
    @_common_options
    @click.argument("repository_id")
    @click.pass_context
    def team_repositories_inspect_command(
        ctx: click.Context,
        project: str | None = None,
        manifest: str | None = None,
        output_format: str | None = None,
        json_output: bool = False,
        repository_id: str = "",
    ) -> int:
        return _cmd_team_repositories_inspect(
            _merge_options(
                ctx,
                project=project,
                manifest=manifest,
                output_format=output_format,
                json_output=json_output,
            ),
            repository_id,
        )
