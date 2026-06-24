"""Click registration for Project discovery commands."""

from __future__ import annotations

import click

from isomer_labs.cli.app import (
    _cmd_cleanup,
    _cmd_content_root_move,
    _cmd_context_show,
    _cmd_init,
    _cmd_paths_preview,
    _cmd_schemas_list,
    _cmd_topics_list,
    _cmd_validate,
    _cmd_workspaces_list,
)
from isomer_labs.cli.options import (
    common_options as _common_options,
    merge_options as _merge_options,
    topic_selection_options as _topic_selection_options,
)
from isomer_labs.project_cleanup import CLEANUP_PARTS


def register_project_commands(app: click.Group) -> None:
    @app.command(name="init", help="Initialize the smallest valid Project configuration.")
    @_common_options
    @click.argument("topic_id", required=False)
    @click.option("--topic-id", "topic_id_option", help="Research Topic id to initialize.")
    @click.option("--topic-statement", help="Short inline Research Topic statement.")
    @click.option("--content-dir", help="Project-local generated content root to create during init.")
    @click.pass_context
    def init_command(
        ctx: click.Context,
        project: str | None = None,
        manifest: str | None = None,
        output_format: str | None = None,
        json_output: bool = False,
        topic_id: str | None = None,
        topic_id_option: str | None = None,
        topic_statement: str | None = None,
        content_dir: str | None = None,
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
                content_dir=content_dir,
            )
        )


    @app.command(name="cleanup", help="Plan or apply cleanup of selected Isomer-managed Project material.")
    @_common_options
    @click.option(
        "--part",
        "parts",
        multiple=True,
        type=click.Choice(CLEANUP_PARTS),
        required=True,
        help="Cleanup part to plan or remove. Repeat to select multiple parts.",
    )
    @click.option("--topic", "topics", multiple=True, help="Research Topic id for topic-scoped cleanup. Repeat to select multiple topics.")
    @click.option("--all-topics", is_flag=True, help="Apply topic-scoped cleanup to all registered Research Topics.")
    @click.option("--content-dir", help="Project-local generated content root to use when planning content cleanup.")
    @click.option("--purge-content-root", is_flag=True, help="Allow --part content-root to remove the whole selected content root.")
    @click.option("--dry-run", is_flag=True, help="Build the cleanup plan without deleting files.")
    @click.option("--yes", is_flag=True, help="Delete the reviewed cleanup plan.")
    @click.pass_context
    def cleanup_command(
        ctx: click.Context,
        project: str | None = None,
        manifest: str | None = None,
        output_format: str | None = None,
        json_output: bool = False,
        parts: tuple[str, ...] = (),
        topics: tuple[str, ...] = (),
        all_topics: bool = False,
        content_dir: str | None = None,
        purge_content_root: bool = False,
        dry_run: bool = False,
        yes: bool = False,
    ) -> int:
        return _cmd_cleanup(
            _merge_options(
                ctx,
                project=project,
                manifest=manifest,
                output_format=output_format,
                json_output=json_output,
                cleanup_parts=parts,
                cleanup_topics=topics,
                cleanup_all_topics=all_topics,
                content_dir=content_dir,
                cleanup_purge_content_root=purge_content_root,
                cleanup_dry_run=dry_run,
                cleanup_yes=yes,
            )
        )


    @app.group(name="content-root", help="Generated content-root commands.")
    def content_root_group() -> None:
        pass


    @content_root_group.command(name="move", help="Plan or apply relocation of the Project generated content root.")
    @_common_options
    @click.option("--to", "content_root_to", required=True, help="Project-local destination generated content root.")
    @click.option("--dry-run", is_flag=True, help="Build the relocation plan without moving files or writing the manifest.")
    @click.option("--yes", is_flag=True, help="Apply the reviewed relocation plan.")
    @click.pass_context
    def content_root_move_command(
        ctx: click.Context,
        project: str | None = None,
        manifest: str | None = None,
        output_format: str | None = None,
        json_output: bool = False,
        content_root_to: str | None = None,
        dry_run: bool = False,
        yes: bool = False,
    ) -> int:
        return _cmd_content_root_move(
            _merge_options(
                ctx,
                project=project,
                manifest=manifest,
                output_format=output_format,
                json_output=json_output,
                content_root_to=content_root_to,
                content_root_move_dry_run=dry_run,
                content_root_move_yes=yes,
            )
        )


    @app.command(name="validate", help="Validate the Project Manifest and registered configs.")
    @_common_options
    @click.pass_context
    def validate_command(
        ctx: click.Context,
        project: str | None = None,
        manifest: str | None = None,
        output_format: str | None = None,
        json_output: bool = False,
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
        project: str | None = None,
        manifest: str | None = None,
        output_format: str | None = None,
        json_output: bool = False,
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
        project: str | None = None,
        manifest: str | None = None,
        output_format: str | None = None,
        json_output: bool = False,
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
def register_schema_commands(app: click.Group) -> None:
    @app.group(name="schemas", help="Built-in schema commands.")
    def schemas_group() -> None:
        pass


    @schemas_group.command(name="list", help="List Isomer built-in schemas and contracts.")
    @click.pass_context
    def schemas_list_command(
        ctx: click.Context,
    ) -> int:
        return _cmd_schemas_list(
            _merge_options(
                ctx,
            )
        )
