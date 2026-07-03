"""Click registration for Agent Team Instance commands."""

from __future__ import annotations

import click

from isomer_labs.cli.handlers.team_instances import (
    _cmd_team_instances_adapter_link_export,
    _cmd_team_instances_create,
    _cmd_team_instances_launch,
    _cmd_team_instances_launch_material_prepare,
    _cmd_team_instances_list,
    _cmd_team_instances_manifest_inspect,
    _cmd_team_instances_reconcile,
    _cmd_team_instances_show,
    _cmd_team_instances_stop,
)
from isomer_labs.cli.options import (
    common_options as _common_options,
    merge_options as _merge_options,
    topic_selection_options as _topic_selection_options,
)


def register_team_instance_commands(app: click.Group) -> None:
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
        instance_id: str | None = None,
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
        agent_team_instance_id_arg: str = "",
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
        agent_team_instance_id_arg: str = "",
        output_path: str | None = None,
        print_manifest: bool = False,
        houmao_project_dir: str | None = None,
        actor_ref: str | None = None,
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
        agent_team_instance_id_arg: str = "",
        adapter: str = "",
        houmao_project_dir: str | None = None,
        actor_ref: str | None = None,
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
        agent_team_instance_id_arg: str = "",
        adapter: str = "",
        houmao_project_dir: str | None = None,
        actor_ref: str | None = None,
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
        agent_team_instance_id_arg: str = "",
        adapter: str | None = None,
        integrity: bool = False,
        link_manifest: str | None = None,
        launch_material_manifest: str | None = None,
        runtime_manifest: str | None = None,
        live_state_json: str | None = None,
        houmao_project_dir: str | None = None,
        actor_ref: str | None = None,
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
        agent_team_instance_id_arg: str = "",
        adapter: str = "",
        link_manifest: str | None = None,
        actor_ref: str | None = None,
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
        agent_team_instance_id_arg: str = "",
        link_manifest: str | None = None,
        launch_material_manifest: str | None = None,
        runtime_manifest: str | None = None,
        live_state_json: str | None = None,
        houmao_project_dir: str | None = None,
        actor_ref: str | None = None,
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
        agent_team_instance_id_arg: str = "",
        approved: bool = False,
        link_manifest: str | None = None,
        launch_material_manifest: str | None = None,
        runtime_manifest: str | None = None,
        live_state_json: str | None = None,
        houmao_project_dir: str | None = None,
        actor_ref: str | None = None,
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
