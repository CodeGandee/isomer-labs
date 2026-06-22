"""Click registration for Topic Agent Team Profile commands."""

from __future__ import annotations

import click

from isomer_labs.cli.app import _cmd_team_profiles_specialize, _cmd_team_profiles_validate
from isomer_labs.cli.options import (
    common_options as _common_options,
    merge_options as _merge_options,
    topic_selection_options as _topic_selection_options,
)


def register_team_profile_commands(app: click.Group) -> None:
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
        project: str | None = None,
        manifest: str | None = None,
        output_format: str | None = None,
        json_output: bool = False,
        research_topic_id: str | None = None,
        topic_workspace_id: str | None = None,
        research_inquiry_id: str | None = None,
        research_task_id: str | None = None,
        run_id: str | None = None,
        agent_team_instance_id: str | None = None,
        agent_instance_id: str | None = None,
        topic_agent_team_profile_id: str | None = None,
        template_id: str | None = None,
        profile_id: str | None = None,
        roles: tuple[str, ...] = (),
        expected_artifacts: tuple[str, ...] = (),
        use_case: str | None = None,
        write_profile: bool = False,
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
        project: str | None = None,
        manifest: str | None = None,
        output_format: str | None = None,
        json_output: bool = False,
        template_id: str | None = None,
        profile_path: str | None = None,
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
