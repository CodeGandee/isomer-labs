"""Click registration for Project discovery commands."""

from __future__ import annotations

from typing import Any

import click

from isomer_labs.cli.handlers.project import (
    _cmd_cleanup,
    _cmd_content_root_move,
    _cmd_context_show,
    _cmd_init,
    _cmd_skill_callbacks_disable,
    _cmd_skill_callbacks_install,
    _cmd_skill_callbacks_list,
    _cmd_skill_callbacks_register,
    _cmd_skill_callbacks_resolve,
    _cmd_skill_callbacks_show,
    _cmd_skill_callbacks_validate,
    _cmd_topics_create,
    _cmd_topics_delete,
    _cmd_topics_list,
    _cmd_topics_show,
    _cmd_topics_update,
    _cmd_toolbox_param_import_add,
    _cmd_toolbox_param_import_list,
    _cmd_toolbox_param_import_remove,
    _cmd_toolbox_param_import_show,
    _cmd_toolbox_params_define,
    _cmd_toolbox_params_explain,
    _cmd_toolbox_params_get,
    _cmd_toolbox_params_list,
    _cmd_toolbox_params_set,
    _cmd_toolbox_params_unset,
    _cmd_toolbox_params_validate,
    _cmd_toolboxes_disable,
    _cmd_toolboxes_enable,
    _cmd_toolboxes_explain,
    _cmd_toolboxes_install,
    _cmd_toolboxes_list,
    _cmd_toolboxes_show,
    _cmd_toolboxes_uninstall,
    _cmd_toolboxes_update_source,
    _cmd_toolboxes_validate,
    _cmd_validate,
)
from isomer_labs.cli.handlers.schemas import _cmd_schemas_list
from isomer_labs.cli.handlers.self import (
    _cmd_self_env,
    _cmd_self_identity,
    _cmd_self_paths,
    _cmd_self_pixi,
    _cmd_self_queries,
    _cmd_self_show,
)
from isomer_labs.cli.handlers.workspace import (
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
    _cmd_workspaces_list,
)
from isomer_labs.cli.handlers.workspace_paths import (
    _cmd_outputs_policy,
    _cmd_paths_default,
    _cmd_paths_explain,
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
)
from isomer_labs.cli.options import (
    common_options as _common_options,
    merge_options as _merge_options,
    topic_selection_options as _topic_selection_options,
)
from isomer_labs.project.cleanup import CLEANUP_PARTS


def _self_selection_options(command: Any) -> Any:
    command = click.option("--topic-actor", "topic_actor_name", default=None, help="Topic Actor name for self context.")(command)
    command = click.option("--agent", "agent_name", default=None, help="Topic-local Agent Name for self context.")(command)
    command = _topic_selection_options(command)
    return command


def _toolbox_selection_options(command: Any) -> Any:
    command = click.option("--topic-agent", "--agent", "agent_name", default=None, help="Topic-local Agent Name selector.")(command)
    command = click.option("--topic-actor", "topic_actor_name", default=None, help="Topic Actor name selector.")(command)
    command = _topic_selection_options(command)
    return command


def _toolbox_scope_option(command: Any) -> Any:
    return click.option(
        "--scope",
        "toolbox_scope",
        type=click.Choice(["project", "research_topic", "topic_actor", "topic_agent"]),
        default=None,
        help="Toolbox configuration scope.",
    )(command)


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


    @app.group(name="skill-callbacks", help="User Skill Callback commands.")
    def skill_callbacks_group() -> None:
        pass


    @skill_callbacks_group.command(name="register", help="Register a User Skill Callback.")
    @_common_options
    @_topic_selection_options
    @click.option("--id", "callback_id", default=None, help="Stable callback id. Generated when omitted.")
    @click.option("--skill", "callback_skill", required=True, help="Target packaged system skill name.")
    @click.option("--stage", "callback_stage", type=click.Choice(["begin", "end"]), required=True, help="Callback stage.")
    @click.option(
        "--scope",
        "callback_scope",
        type=click.Choice(["project", "research_topic"]),
        default="research_topic",
        show_default=True,
        help="Callback registry scope.",
    )
    @click.option("--prompt", "callback_prompt", default=None, help="Inline callback prompt to materialize.")
    @click.option("--prompt-file", "callback_prompt_file", default=None, help="Prompt file source.")
    @click.option("--skill-dir", "callback_skill_dir", default=None, help="External skill directory source containing SKILL.md.")
    @click.option("--priority", "callback_priority", default=100, show_default=True, type=int, help="Lower values resolve first within one scope.")
    @click.option("--allow-external-source", "callback_allow_external_source", is_flag=True, help="Allow a callback source path outside the Project root.")
    @click.pass_context
    def skill_callbacks_register_command(
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
        callback_id: str | None = None,
        callback_skill: str | None = None,
        callback_stage: str | None = None,
        callback_scope: str | None = None,
        callback_prompt: str | None = None,
        callback_prompt_file: str | None = None,
        callback_skill_dir: str | None = None,
        callback_priority: int | None = None,
        callback_allow_external_source: bool = False,
    ) -> int:
        return _cmd_skill_callbacks_register(
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
                callback_id=callback_id,
                callback_skill=callback_skill,
                callback_stage=callback_stage,
                callback_scope=callback_scope,
                callback_prompt=callback_prompt,
                callback_prompt_file=callback_prompt_file,
                callback_skill_dir=callback_skill_dir,
                callback_priority=callback_priority,
                callback_allow_external_source=callback_allow_external_source,
            )
        )


    @skill_callbacks_group.command(name="install", help="Install callbacks from a toolbox manifest.")
    @_common_options
    @_topic_selection_options
    @click.option("--toolbox-dir", "callback_toolbox_dir", required=True, help="Toolbox directory containing manifest.toml.")
    @click.option(
        "--scope",
        "callback_scope",
        type=click.Choice(["project", "research_topic"]),
        default="research_topic",
        show_default=True,
        help="Callback registry scope.",
    )
    @click.option("--replace", "callback_replace_toolbox_source", is_flag=True, help="Replace callbacks from a different source with the same toolbox_id.")
    @click.pass_context
    def skill_callbacks_install_command(
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
        callback_toolbox_dir: str | None = None,
        callback_scope: str | None = None,
        callback_replace_toolbox_source: bool = False,
    ) -> int:
        return _cmd_skill_callbacks_install(
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
                callback_toolbox_dir=callback_toolbox_dir,
                callback_scope=callback_scope,
                callback_replace_toolbox_source=callback_replace_toolbox_source,
            )
        )


    @skill_callbacks_group.command(name="resolve", help="Resolve User Skill Callbacks for one system skill stage.")
    @_common_options
    @_topic_selection_options
    @click.option("--skill", "callback_skill", required=True, help="Target packaged system skill name.")
    @click.option("--stage", "callback_stage", type=click.Choice(["begin", "end"]), required=True, help="Callback stage.")
    @click.pass_context
    def skill_callbacks_resolve_command(
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
        callback_skill: str | None = None,
        callback_stage: str | None = None,
    ) -> int:
        return _cmd_skill_callbacks_resolve(
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
                callback_skill=callback_skill,
                callback_stage=callback_stage,
            )
        )


    @skill_callbacks_group.command(name="list", help="List visible User Skill Callbacks.")
    @_common_options
    @_topic_selection_options
    @click.pass_context
    def skill_callbacks_list_command(
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
        return _cmd_skill_callbacks_list(
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


    @skill_callbacks_group.command(name="show", help="Show one User Skill Callback.")
    @_common_options
    @_topic_selection_options
    @click.argument("callback_id")
    @click.pass_context
    def skill_callbacks_show_command(
        ctx: click.Context,
        callback_id: str,
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
        return _cmd_skill_callbacks_show(
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
                callback_id=callback_id,
            )
        )


    @skill_callbacks_group.command(name="disable", help="Disable one User Skill Callback.")
    @_common_options
    @_topic_selection_options
    @click.argument("callback_id")
    @click.pass_context
    def skill_callbacks_disable_command(
        ctx: click.Context,
        callback_id: str,
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
        return _cmd_skill_callbacks_disable(
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
                callback_id=callback_id,
            )
        )


    @skill_callbacks_group.command(name="validate", help="Validate visible User Skill Callback registries.")
    @_common_options
    @_topic_selection_options
    @click.pass_context
    def skill_callbacks_validate_command(
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
        return _cmd_skill_callbacks_validate(
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

    def _merge_toolbox_command_options(ctx: click.Context, kwargs: dict[str, Any], **extra: Any) -> Any:
        values = dict(kwargs)
        project = values.pop("project", None)
        manifest = values.pop("manifest", None)
        output_format = values.pop("output_format", None)
        json_output = values.pop("json_output", False)
        values.update(extra)
        return _merge_options(
            ctx,
            project=project,
            manifest=manifest,
            output_format=output_format,
            json_output=json_output,
            **values,
        )


    @app.group(name="toolboxes", help="Toolbox registration commands.")
    def toolboxes_group() -> None:
        pass


    @toolboxes_group.command(name="install", help="Install or update a Toolbox registration.")
    @_common_options
    @_toolbox_selection_options
    @_toolbox_scope_option
    @click.option("--toolbox-dir", "toolbox_dir", required=True, help="Toolbox directory containing manifest.toml.")
    @click.option("--status", "toolbox_status", type=click.Choice(["active", "disabled"]), default="active", show_default=True)
    @click.pass_context
    def toolboxes_install_command(ctx: click.Context, **kwargs: Any) -> int:
        return _cmd_toolboxes_install(_merge_toolbox_command_options(ctx, kwargs))


    @toolboxes_group.command(name="list", help="List Toolbox registrations visible from the selected context.")
    @_common_options
    @_toolbox_selection_options
    @click.pass_context
    def toolboxes_list_command(ctx: click.Context, **kwargs: Any) -> int:
        return _cmd_toolboxes_list(_merge_toolbox_command_options(ctx, kwargs))


    @toolboxes_group.command(name="show", help="Show one Toolbox registration.")
    @_common_options
    @_toolbox_selection_options
    @click.argument("toolbox_id")
    @click.pass_context
    def toolboxes_show_command(ctx: click.Context, toolbox_id: str, **kwargs: Any) -> int:
        return _cmd_toolboxes_show(_merge_toolbox_command_options(ctx, kwargs, toolbox_id=toolbox_id))


    @toolboxes_group.command(name="explain", help="Explain effective Toolbox status.")
    @_common_options
    @_toolbox_selection_options
    @click.argument("toolbox_id")
    @click.pass_context
    def toolboxes_explain_command(ctx: click.Context, toolbox_id: str, **kwargs: Any) -> int:
        return _cmd_toolboxes_explain(_merge_toolbox_command_options(ctx, kwargs, toolbox_id=toolbox_id))


    @toolboxes_group.command(name="enable", help="Enable a Toolbox at the selected scope.")
    @_common_options
    @_toolbox_selection_options
    @_toolbox_scope_option
    @click.argument("toolbox_id")
    @click.pass_context
    def toolboxes_enable_command(ctx: click.Context, toolbox_id: str, **kwargs: Any) -> int:
        return _cmd_toolboxes_enable(_merge_toolbox_command_options(ctx, kwargs, toolbox_id=toolbox_id))


    @toolboxes_group.command(name="disable", help="Disable a Toolbox at the selected scope.")
    @_common_options
    @_toolbox_selection_options
    @_toolbox_scope_option
    @click.argument("toolbox_id")
    @click.pass_context
    def toolboxes_disable_command(ctx: click.Context, toolbox_id: str, **kwargs: Any) -> int:
        return _cmd_toolboxes_disable(_merge_toolbox_command_options(ctx, kwargs, toolbox_id=toolbox_id))


    @toolboxes_group.command(name="update-source", help="Update a Toolbox source path.")
    @_common_options
    @_toolbox_selection_options
    @_toolbox_scope_option
    @click.argument("toolbox_id")
    @click.option("--source-path", "toolbox_source_path", required=True, help="Replacement Toolbox source path.")
    @click.pass_context
    def toolboxes_update_source_command(ctx: click.Context, toolbox_id: str, **kwargs: Any) -> int:
        return _cmd_toolboxes_update_source(_merge_toolbox_command_options(ctx, kwargs, toolbox_id=toolbox_id))


    @toolboxes_group.command(name="uninstall", help="Remove a Toolbox registration at the selected scope.")
    @_common_options
    @_toolbox_selection_options
    @_toolbox_scope_option
    @click.argument("toolbox_id")
    @click.pass_context
    def toolboxes_uninstall_command(ctx: click.Context, toolbox_id: str, **kwargs: Any) -> int:
        return _cmd_toolboxes_uninstall(_merge_toolbox_command_options(ctx, kwargs, toolbox_id=toolbox_id))


    @toolboxes_group.command(name="validate", help="Validate Toolbox registrations and runtime params.")
    @_common_options
    @_toolbox_selection_options
    @click.pass_context
    def toolboxes_validate_command(ctx: click.Context, **kwargs: Any) -> int:
        return _cmd_toolboxes_validate(_merge_toolbox_command_options(ctx, kwargs))


    @app.group(name="toolbox-params", help="Toolbox runtime param commands.")
    def toolbox_params_group() -> None:
        pass


    def _param_value_options(command: Any) -> Any:
        command = click.option("--description", "toolbox_param_description", default=None, help="Runtime param description.")(command)
        command = click.option("--allowed-value", "toolbox_param_allowed_values", multiple=True, help="Allowed enum value. Repeat for multiple values.")(command)
        command = click.option("--value-type", "toolbox_param_value_type", type=click.Choice(["string", "bool", "integer", "number", "enum", "string_list"]), default=None, help="Runtime param value type.")(command)
        command = click.option("--value", "toolbox_param_value", required=True, help="Runtime param value.")(command)
        return command


    @toolbox_params_group.command(name="define", help="Define a Toolbox runtime param at the selected scope.")
    @_common_options
    @_toolbox_selection_options
    @_toolbox_scope_option
    @_param_value_options
    @click.argument("param_id")
    @click.pass_context
    def toolbox_params_define_command(ctx: click.Context, param_id: str, **kwargs: Any) -> int:
        return _cmd_toolbox_params_define(_merge_toolbox_command_options(ctx, kwargs, toolbox_param_id=param_id))


    @toolbox_params_group.command(name="set", help="Set a Toolbox runtime param at the selected scope.")
    @_common_options
    @_toolbox_selection_options
    @_toolbox_scope_option
    @_param_value_options
    @click.argument("param_id")
    @click.pass_context
    def toolbox_params_set_command(ctx: click.Context, param_id: str, **kwargs: Any) -> int:
        return _cmd_toolbox_params_set(_merge_toolbox_command_options(ctx, kwargs, toolbox_param_id=param_id))


    @toolbox_params_group.command(name="get", help="Get an effective Toolbox runtime param.")
    @_common_options
    @_toolbox_selection_options
    @click.argument("param_id")
    @click.pass_context
    def toolbox_params_get_command(ctx: click.Context, param_id: str, **kwargs: Any) -> int:
        return _cmd_toolbox_params_get(_merge_toolbox_command_options(ctx, kwargs, toolbox_param_id=param_id))


    @toolbox_params_group.command(name="list", help="List effective Toolbox runtime params.")
    @_common_options
    @_toolbox_selection_options
    @click.pass_context
    def toolbox_params_list_command(ctx: click.Context, **kwargs: Any) -> int:
        return _cmd_toolbox_params_list(_merge_toolbox_command_options(ctx, kwargs))


    @toolbox_params_group.command(name="explain", help="Explain runtime param candidates and selected value.")
    @_common_options
    @_toolbox_selection_options
    @click.argument("param_id")
    @click.pass_context
    def toolbox_params_explain_command(ctx: click.Context, param_id: str, **kwargs: Any) -> int:
        return _cmd_toolbox_params_explain(_merge_toolbox_command_options(ctx, kwargs, toolbox_param_id=param_id))


    @toolbox_params_group.command(name="unset", help="Remove a runtime param row at the selected scope.")
    @_common_options
    @_toolbox_selection_options
    @_toolbox_scope_option
    @click.argument("param_id")
    @click.pass_context
    def toolbox_params_unset_command(ctx: click.Context, param_id: str, **kwargs: Any) -> int:
        return _cmd_toolbox_params_unset(_merge_toolbox_command_options(ctx, kwargs, toolbox_param_id=param_id))


    @toolbox_params_group.command(name="validate", help="Validate and resolve Toolbox runtime params.")
    @_common_options
    @_toolbox_selection_options
    @click.pass_context
    def toolbox_params_validate_command(ctx: click.Context, **kwargs: Any) -> int:
        return _cmd_toolbox_params_validate(_merge_toolbox_command_options(ctx, kwargs))


    @toolbox_params_group.group(name="import", help="Runtime param import commands.")
    def toolbox_params_import_group() -> None:
        pass


    @toolbox_params_import_group.command(name="add", help="Add a runtime param import row.")
    @_common_options
    @_toolbox_selection_options
    @_toolbox_scope_option
    @click.argument("toolbox_id")
    @click.argument("path")
    @click.pass_context
    def toolbox_params_import_add_command(ctx: click.Context, toolbox_id: str, path: str, **kwargs: Any) -> int:
        return _cmd_toolbox_param_import_add(_merge_toolbox_command_options(ctx, kwargs, toolbox_id=toolbox_id, toolbox_import_path=path))


    @toolbox_params_import_group.command(name="list", help="List runtime param imports visible from the selected context.")
    @_common_options
    @_toolbox_selection_options
    @click.pass_context
    def toolbox_params_import_list_command(ctx: click.Context, **kwargs: Any) -> int:
        return _cmd_toolbox_param_import_list(_merge_toolbox_command_options(ctx, kwargs))


    @toolbox_params_import_group.command(name="show", help="Show runtime param imports.")
    @_common_options
    @_toolbox_selection_options
    @click.pass_context
    def toolbox_params_import_show_command(ctx: click.Context, **kwargs: Any) -> int:
        return _cmd_toolbox_param_import_show(_merge_toolbox_command_options(ctx, kwargs))


    @toolbox_params_import_group.command(name="remove", help="Remove a runtime param import row.")
    @_common_options
    @_toolbox_selection_options
    @_toolbox_scope_option
    @click.argument("toolbox_id")
    @click.argument("path")
    @click.pass_context
    def toolbox_params_import_remove_command(ctx: click.Context, toolbox_id: str, path: str, **kwargs: Any) -> int:
        return _cmd_toolbox_param_import_remove(_merge_toolbox_command_options(ctx, kwargs, toolbox_id=toolbox_id, toolbox_import_path=path))


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
