"""Click registration for Project discovery commands."""

from __future__ import annotations

from typing import Any

import click

from isomer_labs.cli.app import (
    _cmd_cleanup,
    _cmd_content_root_move,
    _cmd_context_show,
    _cmd_paths_default,
    _cmd_paths_explain,
    _cmd_init,
    _cmd_outputs_policy,
    _cmd_paths_get,
    _cmd_paths_list,
    _cmd_paths_materialize,
    _cmd_paths_materialize_default,
    _cmd_paths_preview,
    _cmd_paths_register,
    _cmd_paths_reset,
    _cmd_paths_unregister,
    _cmd_paths_update,
    _cmd_repos_create,
    _cmd_schemas_list,
    _cmd_self_env,
    _cmd_self_identity,
    _cmd_self_paths,
    _cmd_self_pixi,
    _cmd_self_queries,
    _cmd_self_show,
    _cmd_topic_actors_archive,
    _cmd_topic_actors_diagnose,
    _cmd_topic_actors_list,
    _cmd_topic_actors_materialize,
    _cmd_topic_actors_register,
    _cmd_topic_actors_show,
    _cmd_topic_actors_update,
    _cmd_topic_main_guidance_ensure,
    _cmd_topic_main_guidance_inspect,
    _cmd_topic_main_guidance_render,
    _cmd_topics_create,
    _cmd_topics_delete,
    _cmd_topics_list,
    _cmd_topics_show,
    _cmd_topics_update,
    _cmd_validate,
    _cmd_workspaces_list,
)
from isomer_labs.cli.options import (
    common_options as _common_options,
    merge_options as _merge_options,
    topic_selection_options as _topic_selection_options,
)
from isomer_labs.project_cleanup import CLEANUP_PARTS


def _self_selection_options(command: Any) -> Any:
    command = click.option("--topic-actor", "topic_actor_name", default=None, help="Topic Actor name for self context.")(command)
    command = click.option("--agent", "agent_name", default=None, help="Topic-local Agent Name for self context.")(command)
    command = _topic_selection_options(command)
    return command


def register_project_commands(app: click.Group) -> None:
    @app.command(
        name="init",
        help="Initialize the smallest valid Project configuration.",
        context_settings={"allow_extra_args": True},
    )
    @_common_options
    @click.option("--topic-id", "topic_id_option", hidden=True, help="Deprecated. Use project topics create.")
    @click.option("--topic-statement", hidden=True, help="Deprecated. Use project topics create.")
    @click.option("--content-dir", help="Project-local generated content root to create during init.")
    @click.pass_context
    def init_command(
        ctx: click.Context,
        project: str | None = None,
        manifest: str | None = None,
        output_format: str | None = None,
        json_output: bool = False,
        topic_id_option: str | None = None,
        topic_statement: str | None = None,
        content_dir: str | None = None,
    ) -> int:
        topic_id = ctx.args[0] if ctx.args else None
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

    @topics_group.command(name="show", help="Show one registered Research Topic.")
    @_common_options
    @click.argument("topic_id")
    @click.pass_context
    def topics_show_command(
        ctx: click.Context,
        topic_id: str,
        project: str | None = None,
        manifest: str | None = None,
        output_format: str | None = None,
        json_output: bool = False,
    ) -> int:
        return _cmd_topics_show(
            _merge_options(
                ctx,
                project=project,
                manifest=manifest,
                output_format=output_format,
                json_output=json_output,
                topic_id=topic_id,
            )
        )


    @topics_group.command(name="create", help="Create and register a Research Topic.")
    @_common_options
    @click.argument("topic_id")
    @click.option("--statement", "topic_statement", help="Concrete Research Topic statement.")
    @click.option("--workspace-dir", "topic_workspace_dir", help="Project-local Topic Workspace path.")
    @click.option("--set-default", "topic_set_default", is_flag=True, help="Set Project defaults to this topic.")
    @click.pass_context
    def topics_create_command(
        ctx: click.Context,
        topic_id: str,
        project: str | None = None,
        manifest: str | None = None,
        output_format: str | None = None,
        json_output: bool = False,
        topic_statement: str | None = None,
        topic_workspace_dir: str | None = None,
        topic_set_default: bool = False,
    ) -> int:
        return _cmd_topics_create(
            _merge_options(
                ctx,
                project=project,
                manifest=manifest,
                output_format=output_format,
                json_output=json_output,
                topic_id=topic_id,
                topic_statement=topic_statement,
                topic_workspace_dir=topic_workspace_dir,
                topic_set_default=topic_set_default,
            )
        )


    @topics_group.command(name="update", help="Update bounded Research Topic metadata.")
    @_common_options
    @click.argument("topic_id")
    @click.option("--statement", "topic_statement", help="Concrete Research Topic statement.")
    @click.option("--status", "topic_status", help="Research Topic status. Must be active or archived.")
    @click.option("--set-default", "topic_set_default", is_flag=True, help="Set Project defaults to this topic.")
    @click.option("--new-id", "topic_new_id", hidden=True, help="Unsupported. Topic rename is not available.")
    @click.pass_context
    def topics_update_command(
        ctx: click.Context,
        topic_id: str,
        project: str | None = None,
        manifest: str | None = None,
        output_format: str | None = None,
        json_output: bool = False,
        topic_statement: str | None = None,
        topic_status: str | None = None,
        topic_set_default: bool = False,
        topic_new_id: str | None = None,
    ) -> int:
        return _cmd_topics_update(
            _merge_options(
                ctx,
                project=project,
                manifest=manifest,
                output_format=output_format,
                json_output=json_output,
                topic_id=topic_id,
                topic_statement=topic_statement,
                topic_status=topic_status,
                topic_set_default=topic_set_default,
                topic_new_id=topic_new_id,
            )
        )


    @topics_group.command(name="delete", help="Plan or apply Research Topic deletion.")
    @_common_options
    @click.argument("topic_id")
    @click.option("--dry-run", "topic_delete_dry_run", is_flag=True, help="Build the deletion plan without modifying files.")
    @click.option("--yes", "topic_delete_yes", is_flag=True, help="Apply the reviewed deletion plan.")
    @click.pass_context
    def topics_delete_command(
        ctx: click.Context,
        topic_id: str,
        project: str | None = None,
        manifest: str | None = None,
        output_format: str | None = None,
        json_output: bool = False,
        topic_delete_dry_run: bool = False,
        topic_delete_yes: bool = False,
    ) -> int:
        return _cmd_topics_delete(
            _merge_options(
                ctx,
                project=project,
                manifest=manifest,
                output_format=output_format,
                json_output=json_output,
                topic_id=topic_id,
                topic_delete_dry_run=topic_delete_dry_run,
                topic_delete_yes=topic_delete_yes,
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


    @app.group(name="topic-actors", help="Topic Actor and Topic Actor Workspace commands.")
    def topic_actors_group() -> None:
        pass


    @topic_actors_group.command(name="list", help="List Topic Actors registered in the Topic Workspace Manifest.")
    @_common_options
    @_topic_selection_options
    @click.pass_context
    def topic_actors_list_command(
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
        return _cmd_topic_actors_list(
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


    @topic_actors_group.command(name="show", help="Show one Topic Actor binding.")
    @_common_options
    @_topic_selection_options
    @click.argument("topic_actor_name")
    @click.pass_context
    def topic_actors_show_command(
        ctx: click.Context,
        topic_actor_name: str,
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
        return _cmd_topic_actors_show(
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
            topic_actor_name,
        )


    def _topic_actor_mutation_options(command: Any) -> Any:
        command = click.option("--adapter-ref", default=None, help="Optional runtime adapter ref.")(command)
        command = click.option("--branch", default=None, help="Worktree branch under per-topic-actor/<name>/.")(command)
        command = click.option("--workspace-path", default=None, help="Project-local Topic Actor Workspace path override.")(command)
        command = click.option("--controller-ref", default=None, help="Optional controller ref.")(command)
        command = click.option("--controller-kind", default=None, help="Controller kind. Core values allow custom.*.")(command)
        command = click.option("--role-kind", default=None, help="Role kind. Core values allow custom.*.")(command)
        command = click.option("--runtime-kind", default=None, help="Runtime kind. Core values allow custom.*.")(command)
        command = click.option("--actor-kind", default=None, help="Actor kind. Core values allow custom.*.")(command)
        return command


    @topic_actors_group.command(name="register", help="Register a Topic Actor binding.")
    @_common_options
    @_topic_selection_options
    @_topic_actor_mutation_options
    @click.option("--status", "actor_status", default="ready", show_default=True, help="Topic Actor status.")
    @click.option("--replace", "replace_existing", is_flag=True, help="Replace an existing Topic Actor binding explicitly.")
    @click.option("--materialize", is_flag=True, help="Materialize the Topic Actor Workspace after registration.")
    @click.argument("topic_actor_name")
    @click.pass_context
    def topic_actors_register_command(
        ctx: click.Context,
        topic_actor_name: str,
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
        actor_kind: str | None = None,
        runtime_kind: str | None = None,
        role_kind: str | None = None,
        controller_kind: str | None = None,
        controller_ref: str | None = None,
        workspace_path: str | None = None,
        branch: str | None = None,
        adapter_ref: str | None = None,
        actor_status: str = "ready",
        replace_existing: bool = False,
        materialize: bool = False,
    ) -> int:
        return _cmd_topic_actors_register(
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
            topic_actor_name,
            actor_kind=actor_kind,
            runtime_kind=runtime_kind,
            role_kind=role_kind,
            controller_kind=controller_kind,
            controller_ref=controller_ref,
            workspace_path=workspace_path,
            branch=branch,
            adapter_ref=adapter_ref,
            status=actor_status,
            replace_existing=replace_existing,
            materialize=materialize,
        )


    @topic_actors_group.command(name="update", help="Update an existing Topic Actor binding.")
    @_common_options
    @_topic_selection_options
    @_topic_actor_mutation_options
    @click.option("--status", "actor_status", default=None, help="Replacement Topic Actor status.")
    @click.argument("topic_actor_name")
    @click.pass_context
    def topic_actors_update_command(
        ctx: click.Context,
        topic_actor_name: str,
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
        actor_kind: str | None = None,
        runtime_kind: str | None = None,
        role_kind: str | None = None,
        controller_kind: str | None = None,
        controller_ref: str | None = None,
        workspace_path: str | None = None,
        branch: str | None = None,
        adapter_ref: str | None = None,
        actor_status: str | None = None,
    ) -> int:
        return _cmd_topic_actors_update(
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
            topic_actor_name,
            actor_kind=actor_kind,
            runtime_kind=runtime_kind,
            role_kind=role_kind,
            controller_kind=controller_kind,
            controller_ref=controller_ref,
            workspace_path=workspace_path,
            branch=branch,
            adapter_ref=adapter_ref,
            status=actor_status,
        )


    @topic_actors_group.command(name="archive", help="Archive a Topic Actor binding without deleting its workspace.")
    @_common_options
    @_topic_selection_options
    @click.argument("topic_actor_name")
    @click.pass_context
    def topic_actors_archive_command(
        ctx: click.Context,
        topic_actor_name: str,
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
        return _cmd_topic_actors_archive(
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
            topic_actor_name,
        )


    @topic_actors_group.command(name="materialize", help="Materialize or reuse a Topic Actor Workspace.")
    @_common_options
    @_topic_selection_options
    @click.option("--source-repo", default=None, help="Must resolve to topic.repos.main in this change.")
    @click.argument("topic_actor_name")
    @click.pass_context
    def topic_actors_materialize_command(
        ctx: click.Context,
        topic_actor_name: str,
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
        source_repo: str | None = None,
    ) -> int:
        return _cmd_topic_actors_materialize(
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
            topic_actor_name,
            source_repo=source_repo,
        )


    @topic_actors_group.command(name="repair", help="Repair Topic Actor Workspace materialization.")
    @_common_options
    @_topic_selection_options
    @click.option("--source-repo", default=None, help="Must resolve to topic.repos.main in this change.")
    @click.argument("topic_actor_name")
    @click.pass_context
    def topic_actors_repair_command(
        ctx: click.Context,
        topic_actor_name: str,
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
        source_repo: str | None = None,
    ) -> int:
        return _cmd_topic_actors_materialize(
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
            topic_actor_name,
            source_repo=source_repo,
            command_name="topic-actors repair",
        )


    @topic_actors_group.command(name="diagnose", help="Diagnose Topic Actor topology and paths.")
    @_common_options
    @_topic_selection_options
    @click.option("--topic-actor", "topic_actor_name", default=None, help="Topic Actor name to diagnose.")
    @click.pass_context
    def topic_actors_diagnose_command(
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
        topic_actor_name: str | None = None,
    ) -> int:
        return _cmd_topic_actors_diagnose(
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
            topic_actor_name,
        )


    @app.group(name="topic-main-guidance", help="Topic Main Development Repository agent guidance commands.")
    def topic_main_guidance_group() -> None:
        pass


    @topic_main_guidance_group.command(name="render", help="Render the canonical topic-main agent guidance block.")
    @_common_options
    @click.pass_context
    def topic_main_guidance_render_command(
        ctx: click.Context,
        project: str | None = None,
        manifest: str | None = None,
        output_format: str | None = None,
        json_output: bool = False,
    ) -> int:
        return _cmd_topic_main_guidance_render(
            _merge_options(
                ctx,
                project=project,
                manifest=manifest,
                output_format=output_format,
                json_output=json_output,
            )
        )


    @topic_main_guidance_group.command(name="inspect", help="Inspect topic-main AGENTS.md and CLAUDE.md guidance posture.")
    @_common_options
    @_topic_selection_options
    @click.pass_context
    def topic_main_guidance_inspect_command(
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
        return _cmd_topic_main_guidance_inspect(
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


    @topic_main_guidance_group.command(name="ensure", help="Create or update topic-main AGENTS.md and CLAUDE.md guidance.")
    @_common_options
    @_topic_selection_options
    @click.option("--yes", "approved", is_flag=True, help="Confirm writing AGENTS.md and CLAUDE.md guidance.")
    @click.pass_context
    def topic_main_guidance_ensure_command(
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
        approved: bool = False,
    ) -> int:
        return _cmd_topic_main_guidance_ensure(
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
            approved=approved,
        )


    @app.group(name="context", help="Effective Topic Context commands.")
    def context_group() -> None:
        pass


    @context_group.command(name="show", help="Show resolved Effective Topic Context.")
    @_common_options
    @_topic_selection_options
    @click.option("--agent", "agent_name", default=None, help="Topic-local Agent Name for agent-context display.")
    @click.option("--topic-actor", "topic_actor_name", default=None, help="Topic Actor name for actor-context display.")
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
        agent_name: str | None = None,
        topic_actor_name: str | None = None,
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
                agent_name=agent_name,
                topic_actor_name=topic_actor_name,
                topic_agent_team_profile_id=topic_agent_team_profile_id,
            )
        )


    def _merge_self_options(
        ctx: click.Context,
        *,
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
        agent_name: str | None,
        topic_actor_name: str | None,
        topic_agent_team_profile_id: str | None,
    ) -> Any:
        return _merge_options(
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
            agent_name=agent_name,
            topic_actor_name=topic_actor_name,
            topic_agent_team_profile_id=topic_agent_team_profile_id,
        )


    @app.group(name="self", help="Read-only agent self query commands.")
    def self_group() -> None:
        pass


    @self_group.command(name="show", help="Show a small self summary and available self query slices.")
    @_common_options
    @_self_selection_options
    @click.pass_context
    def self_show_command(
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
        agent_name: str | None = None,
        topic_actor_name: str | None = None,
        topic_agent_team_profile_id: str | None = None,
    ) -> int:
        return _cmd_self_show(
            _merge_self_options(
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
                agent_name=agent_name,
                topic_actor_name=topic_actor_name,
                topic_agent_team_profile_id=topic_agent_team_profile_id,
            )
        )


    @self_group.command(name="identity", help="Show resolved topic, Topic Actor, and Agent identity.")
    @_common_options
    @_self_selection_options
    @click.pass_context
    def self_identity_command(
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
        agent_name: str | None = None,
        topic_actor_name: str | None = None,
        topic_agent_team_profile_id: str | None = None,
    ) -> int:
        return _cmd_self_identity(
            _merge_self_options(
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
                agent_name=agent_name,
                topic_actor_name=topic_actor_name,
                topic_agent_team_profile_id=topic_agent_team_profile_id,
            )
        )


    @self_group.command(name="pixi", help="Show the selected Pixi binding and Python command hint.")
    @_common_options
    @_self_selection_options
    @click.pass_context
    def self_pixi_command(
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
        agent_name: str | None = None,
        topic_actor_name: str | None = None,
        topic_agent_team_profile_id: str | None = None,
    ) -> int:
        return _cmd_self_pixi(
            _merge_self_options(
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
                agent_name=agent_name,
                topic_actor_name=topic_actor_name,
                topic_agent_team_profile_id=topic_agent_team_profile_id,
            )
        )


    @self_group.command(name="env", help="Show recognized Isomer environment inputs.")
    @_common_options
    @_self_selection_options
    @click.option("--values", "include_values", is_flag=True, help="Include allowlisted non-secret values.")
    @click.pass_context
    def self_env_command(
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
        agent_name: str | None = None,
        topic_actor_name: str | None = None,
        topic_agent_team_profile_id: str | None = None,
        include_values: bool = False,
    ) -> int:
        return _cmd_self_env(
            _merge_self_options(
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
                agent_name=agent_name,
                topic_actor_name=topic_actor_name,
                topic_agent_team_profile_id=topic_agent_team_profile_id,
            ),
            include_values=include_values,
        )


    @self_group.command(name="paths", help="Resolve requested semantic path labels for this process.")
    @_common_options
    @_self_selection_options
    @click.argument("semantic_labels", nargs=-1)
    @click.pass_context
    def self_paths_command(
        ctx: click.Context,
        semantic_labels: tuple[str, ...],
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
        agent_name: str | None = None,
        topic_actor_name: str | None = None,
        topic_agent_team_profile_id: str | None = None,
    ) -> int:
        return _cmd_self_paths(
            _merge_self_options(
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
                agent_name=agent_name,
                topic_actor_name=topic_actor_name,
                topic_agent_team_profile_id=topic_agent_team_profile_id,
            ),
            semantic_labels,
        )


    @self_group.command(name="queries", help="List safe follow-up self and context query commands.")
    @_common_options
    @_self_selection_options
    @click.pass_context
    def self_queries_command(
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
        agent_name: str | None = None,
        topic_actor_name: str | None = None,
        topic_agent_team_profile_id: str | None = None,
    ) -> int:
        return _cmd_self_queries(
            _merge_self_options(
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
                agent_name=agent_name,
                topic_actor_name=topic_actor_name,
                topic_agent_team_profile_id=topic_agent_team_profile_id,
            )
        )


    @app.group(name="paths", help="Workspace Path Resolution commands.")
    def paths_group() -> None:
        pass

    @app.group(name="outputs", help="Worker output policy commands.")
    def outputs_group() -> None:
        pass

    @outputs_group.command(name="policy", help="Resolve a worker output root and post-operation commit preference.")
    @_common_options
    @_topic_selection_options
    @click.option("--agent", "agent_name", default=None, help="Topic-local Agent Name.")
    @click.option("--topic-actor", "topic_actor_name", default=None, help="Topic Actor name.")
    @click.pass_context
    def outputs_policy_command(
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
        agent_name: str | None = None,
        topic_actor_name: str | None = None,
        topic_agent_team_profile_id: str | None = None,
    ) -> int:
        return _cmd_outputs_policy(
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
                agent_name=agent_name,
                topic_actor_name=topic_actor_name,
                topic_agent_team_profile_id=topic_agent_team_profile_id,
            )
        )


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


    @paths_group.command(name="get", help="Resolve one semantic workspace path without creating files.")
    @_common_options
    @_topic_selection_options
    @click.option("--agent", "agent_name", default=None, help="Topic-local Agent Name for agent-scoped labels.")
    @click.option("--topic-actor", "topic_actor_name", default=None, help="Topic Actor name for actor-scoped labels.")
    @click.option("--configured", is_flag=True, help="Ignore stored Path Plans and use current configuration.")
    @click.argument("semantic_label")
    @click.pass_context
    def paths_get_command(
        ctx: click.Context,
        semantic_label: str,
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
        agent_name: str | None = None,
        topic_actor_name: str | None = None,
        topic_agent_team_profile_id: str | None = None,
        configured: bool = False,
    ) -> int:
        return _cmd_paths_get(
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
                agent_name=agent_name,
                topic_actor_name=topic_actor_name,
                topic_agent_team_profile_id=topic_agent_team_profile_id,
                paths_configured=configured,
            ),
            semantic_label,
        )

    @paths_group.command(name="default", help="Show the default-layout path for a built-in semantic label.")
    @_common_options
    @_topic_selection_options
    @click.option("--agent", "agent_name", default=None, help="Topic-local Agent Name for agent-scoped labels.")
    @click.option("--topic-actor", "topic_actor_name", default=None, help="Topic Actor name for actor-scoped labels.")
    @click.argument("semantic_label")
    @click.pass_context
    def paths_default_command(
        ctx: click.Context,
        semantic_label: str,
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
        agent_name: str | None = None,
        topic_actor_name: str | None = None,
        topic_agent_team_profile_id: str | None = None,
    ) -> int:
        return _cmd_paths_default(
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
                agent_name=agent_name,
                topic_actor_name=topic_actor_name,
                topic_agent_team_profile_id=topic_agent_team_profile_id,
            ),
            semantic_label,
        )

    @paths_group.command(name="explain", help="Explain candidate sources for one semantic workspace path.")
    @_common_options
    @_topic_selection_options
    @click.option("--agent", "agent_name", default=None, help="Topic-local Agent Name for agent-scoped labels.")
    @click.option("--topic-actor", "topic_actor_name", default=None, help="Topic Actor name for actor-scoped labels.")
    @click.argument("semantic_label")
    @click.pass_context
    def paths_explain_command(
        ctx: click.Context,
        semantic_label: str,
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
        agent_name: str | None = None,
        topic_actor_name: str | None = None,
        topic_agent_team_profile_id: str | None = None,
    ) -> int:
        return _cmd_paths_explain(
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
                agent_name=agent_name,
                topic_actor_name=topic_actor_name,
                topic_agent_team_profile_id=topic_agent_team_profile_id,
            ),
            semantic_label,
        )


    @paths_group.command(name="list", help="List semantic workspace labels and resolution status.")
    @_common_options
    @_topic_selection_options
    @click.option("--agent", "agent_name", default=None, help="Topic-local Agent Name for agent-scoped labels.")
    @click.option("--topic-actor", "topic_actor_name", default=None, help="Topic Actor name for actor-scoped labels.")
    @click.pass_context
    def paths_list_command(
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
        agent_name: str | None = None,
        topic_actor_name: str | None = None,
        topic_agent_team_profile_id: str | None = None,
    ) -> int:
        return _cmd_paths_list(
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
                agent_name=agent_name,
                topic_actor_name=topic_actor_name,
                topic_agent_team_profile_id=topic_agent_team_profile_id,
            )
        )


    @paths_group.command(name="materialize-default", help="Create selected default semantic directories.")
    @_common_options
    @_topic_selection_options
    @click.option("--agent", "agent_name", default=None, help="Topic-local Agent Name for agent-scoped labels.")
    @click.option("--topic-actor", "topic_actor_name", default=None, help="Topic Actor name for actor-scoped labels.")
    @click.option("--label", "labels", multiple=True, help="Semantic label to materialize. Repeat to select multiple labels.")
    @click.pass_context
    def paths_materialize_default_command(
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
        agent_name: str | None = None,
        topic_actor_name: str | None = None,
        topic_agent_team_profile_id: str | None = None,
        labels: tuple[str, ...] = (),
    ) -> int:
        return _cmd_paths_materialize_default(
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
                agent_name=agent_name,
                topic_actor_name=topic_actor_name,
                topic_agent_team_profile_id=topic_agent_team_profile_id,
            ),
            labels=labels,
        )

    @paths_group.command(name="materialize", help="Create the currently configured target for a semantic label.")
    @_common_options
    @_topic_selection_options
    @click.option("--agent", "agent_name", default=None, help="Topic-local Agent Name for agent-scoped labels.")
    @click.option("--topic-actor", "topic_actor_name", default=None, help="Topic Actor name for actor-scoped labels.")
    @click.argument("semantic_label")
    @click.pass_context
    def paths_materialize_command(
        ctx: click.Context,
        semantic_label: str,
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
        agent_name: str | None = None,
        topic_actor_name: str | None = None,
        topic_agent_team_profile_id: str | None = None,
    ) -> int:
        return _cmd_paths_materialize(
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
                agent_name=agent_name,
                topic_actor_name=topic_actor_name,
                topic_agent_team_profile_id=topic_agent_team_profile_id,
            ),
            semantic_label,
        )

    @paths_group.command(name="register", help="Register a semantic path binding in the Topic Workspace Manifest.")
    @_common_options
    @_topic_selection_options
    @click.argument("semantic_label")
    @click.option("--path", "path_value", required=True, help="Project-local path or accepted template for the binding.")
    @click.option("--storage-profile", "storage_profile", required=True, help="Accepted storage_profile id.")
    @click.option("--create", is_flag=True, help="Create the target path after validation.")
    @click.option("--replace", "replace_existing", is_flag=True, help="Replace an existing binding explicitly.")
    @click.pass_context
    def paths_register_command(
        ctx: click.Context,
        semantic_label: str,
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
        path_value: str | None = None,
        storage_profile: str | None = None,
        create: bool = False,
        replace_existing: bool = False,
    ) -> int:
        return _cmd_paths_register(
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
            semantic_label,
            path=path_value or "",
            storage_profile=storage_profile or "",
            create=create,
            replace_existing=replace_existing,
        )

    @paths_group.command(name="update", help="Update an existing semantic path binding.")
    @_common_options
    @_topic_selection_options
    @click.argument("semantic_label")
    @click.option("--path", "path_value", default=None, help="Replacement path or accepted template.")
    @click.option("--storage-profile", "storage_profile", default=None, help="Replacement accepted storage_profile id.")
    @click.option("--create", is_flag=True, help="Create the target path after validation.")
    @click.pass_context
    def paths_update_command(
        ctx: click.Context,
        semantic_label: str,
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
        path_value: str | None = None,
        storage_profile: str | None = None,
        create: bool = False,
    ) -> int:
        return _cmd_paths_update(
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
            semantic_label,
            path=path_value,
            storage_profile=storage_profile,
            create=create,
        )

    @paths_group.command(name="unregister", help="Remove a dynamic semantic path binding without deleting files.")
    @_common_options
    @_topic_selection_options
    @click.argument("semantic_label")
    @click.pass_context
    def paths_unregister_command(
        ctx: click.Context,
        semantic_label: str,
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
        return _cmd_paths_unregister(
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
            semantic_label,
        )

    @paths_group.command(name="reset", help="Remove a built-in label override without deleting files.")
    @_common_options
    @_topic_selection_options
    @click.argument("semantic_label")
    @click.pass_context
    def paths_reset_command(
        ctx: click.Context,
        semantic_label: str,
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
        return _cmd_paths_reset(
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
            semantic_label,
        )


    @app.group(name="repos", help="Topic repository semantic path commands.")
    def repos_group() -> None:
        pass


    @repos_group.command(name="create", help="Register and create a topic repository path.")
    @_common_options
    @_topic_selection_options
    @click.argument("repo_label")
    @click.option("--path", "path_value", default=None, help="Project-local repository path.")
    @click.option("--no-create", "no_create", is_flag=True, help="Only register the binding; do not create the target path.")
    @click.option("--replace", "replace_existing", is_flag=True, help="Replace an existing binding explicitly.")
    @click.pass_context
    def repos_create_command(
        ctx: click.Context,
        repo_label: str,
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
        path_value: str | None = None,
        no_create: bool = False,
        replace_existing: bool = False,
    ) -> int:
        return _cmd_repos_create(
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
            repo_label,
            path=path_value,
            create=not no_create,
            replace_existing=replace_existing,
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
