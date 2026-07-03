"""Click registration for Isomer research record extension commands."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import click

from isomer_labs.cli.app import _context_for_options
from isomer_labs.cli.options import (
    common_options as _common_options,
    merge_options as _merge_options,
    topic_selection_options as _topic_selection_options,
)
from isomer_labs.deepsci_ext.rendering import dumps_raw_json
from isomer_labs.diagnostics import has_errors
from isomer_labs.research_records import (
    ResearchRecordError,
    ResearchRecordRequest,
    archive_record,
    create_record,
    list_records,
    parse_json_object,
    parse_string_map,
    render_record,
    show_record,
    update_record,
    validate_record_payload,
)


def register_research_record_ext_commands(app: click.Group) -> None:
    ext_command = app.commands.get("ext")
    if isinstance(ext_command, click.Group):
        ext_group = ext_command
    else:
        ext_group = click.Group(name="ext", help="Extension commands.")
        app.add_command(ext_group)

    @ext_group.group(name="research", help="Isomer research extension commands.")
    def research_group() -> None:
        pass

    @research_group.group(name="records", help="CRUD commands for topic-scoped research records.")
    def records_group() -> None:
        pass

    @records_group.command(name="create", help="Create a topic-scoped research record.")
    @_common_options
    @_topic_selection_options
    @_record_request_options(require_kind=True, include_id=True)
    @click.pass_context
    def create_command(ctx: click.Context, **kwargs: Any) -> int:
        return _with_context(ctx, kwargs, lambda context, request: create_record(context, request, env=os.environ, cwd=Path.cwd()))

    @records_group.command(name="show", help="Show one topic-scoped research record.")
    @_common_options
    @_topic_selection_options
    @click.option("--include-body", is_flag=True, help="Include body text when the record has a readable local content path.")
    @click.option("--include-payload", is_flag=True, help="Include structured payload JSON when present.")
    @click.option("--include-validation-diagnostics", is_flag=True, help="Include structured validation diagnostics.")
    @click.option("--include-render-diagnostics", is_flag=True, help="Include structured render diagnostics.")
    @click.option("--include-rendered-body", is_flag=True, help="Include generated Markdown body when present.")
    @click.argument("record_id")
    @click.pass_context
    def show_command(
        ctx: click.Context,
        record_id: str,
        include_body: bool = False,
        include_payload: bool = False,
        include_validation_diagnostics: bool = False,
        include_render_diagnostics: bool = False,
        include_rendered_body: bool = False,
        **kwargs: Any,
    ) -> int:
        return _with_context(
            ctx,
            kwargs,
            lambda context, _request: show_record(
                context,
                record_id,
                env=os.environ,
                include_body=include_body,
                include_payload=include_payload,
                include_validation_diagnostics=include_validation_diagnostics,
                include_render_diagnostics=include_render_diagnostics,
                include_rendered_body=include_rendered_body,
            ),
        )

    @records_group.command(name="list", help="List topic-scoped research records.")
    @_common_options
    @_topic_selection_options
    @click.option("--record-kind", default=None, help="Filter by Workspace Runtime lifecycle record kind.")
    @click.option("--status", default=None, help="Filter by lifecycle status.")
    @click.option("--placeholder", default=None, help="Filter by exact research placeholder token.")
    @click.option("--profile", default=None, help="Filter by artifact or record profile.")
    @click.option("--skill", default=None, help="Filter by producing skill name.")
    @click.option("--producer", default=None, help="Filter by producer metadata.")
    @click.option("--consumer", default=None, help="Filter by consumer metadata.")
    @click.option("--topic-actor", "topic_actor_name", default=None, help="Filter by Topic Actor name.")
    @click.option("--actor-kind", default=None, help="Filter by Topic Actor kind metadata.")
    @click.option("--runtime-kind", default=None, help="Filter by Topic Actor runtime kind metadata.")
    @click.option("--controller-kind", default=None, help="Filter by Topic Actor controller kind metadata.")
    @click.option("--adapter-ref", default=None, help="Filter by Topic Actor adapter ref metadata.")
    @click.option("--format-profile", "format_profile_ref", default=None, help="Filter by Artifact Format Profile ref.")
    @click.option("--schema-ref", default=None, help="Filter by structured schema ref.")
    @click.option("--template-ref", default=None, help="Filter by structured template ref.")
    @click.option("--validation-status", default=None, help="Filter by structured validation status.")
    @click.option("--render-status", default=None, help="Filter by structured render status.")
    @click.option("--limit", type=int, default=None, help="Maximum records to return.")
    @click.pass_context
    def list_command(ctx: click.Context, **kwargs: Any) -> int:
        filters = dict(kwargs)
        return _with_context(
            ctx,
            filters,
            lambda context, _request: list_records(
                context,
                env=os.environ,
                record_kind=filters.get("record_kind"),
                status=filters.get("status"),
                placeholder=filters.get("placeholder"),
                profile=filters.get("profile"),
                skill=filters.get("skill"),
                producer=filters.get("producer"),
                consumer=filters.get("consumer"),
                topic_actor_name=filters.get("topic_actor_name"),
                actor_kind=filters.get("actor_kind"),
                runtime_kind=filters.get("runtime_kind"),
                controller_kind=filters.get("controller_kind"),
                adapter_ref=filters.get("adapter_ref"),
                format_profile_ref=filters.get("format_profile_ref"),
                schema_ref=filters.get("schema_ref"),
                template_ref=filters.get("template_ref"),
                validation_status=filters.get("validation_status"),
                render_status=filters.get("render_status"),
                limit=filters.get("limit"),
            ),
            build_request=False,
        )

    @records_group.command(name="update", help="Update a topic-scoped research record.")
    @_common_options
    @_topic_selection_options
    @_record_request_options(require_kind=True, include_id=False)
    @click.argument("record_id")
    @click.pass_context
    def update_command(ctx: click.Context, record_id: str, **kwargs: Any) -> int:
        return _with_context(
            ctx,
            kwargs,
            lambda context, request: update_record(context, record_id, request, env=os.environ, cwd=Path.cwd()),
        )

    @records_group.command(name="delete", help="Archive a topic-scoped research record.")
    @_common_options
    @_topic_selection_options
    @click.option("--reason", default=None, help="Reason for archiving the record.")
    @click.argument("record_id")
    @click.pass_context
    def delete_command(ctx: click.Context, record_id: str, reason: str | None = None, **kwargs: Any) -> int:
        return _with_context(
            ctx,
            kwargs,
            lambda context, _request: archive_record(context, record_id, env=os.environ, reason=reason),
            build_request=False,
        )

    @records_group.command(name="validate", help="Validate a structured research record payload without mutation.")
    @_common_options
    @_topic_selection_options
    @_record_request_options(require_kind=False, include_id=False)
    @click.pass_context
    def validate_command(ctx: click.Context, **kwargs: Any) -> int:
        values = dict(kwargs)
        if values.get("record_kind") is None:
            values["record_kind"] = "artifact"
        return _with_context(
            ctx,
            values,
            lambda context, request: validate_record_payload(context, request, env=os.environ, cwd=Path.cwd()),
        )

    @records_group.command(name="render", help="Render a stored structured research record without changing its locator.")
    @_common_options
    @_topic_selection_options
    @click.option("--output-file", type=click.Path(path_type=Path), default=None, help="Optional file path for rendered Markdown.")
    @click.argument("record_id")
    @click.pass_context
    def render_command(ctx: click.Context, record_id: str, output_file: Path | None = None, **kwargs: Any) -> int:
        return _with_context(
            ctx,
            kwargs,
            lambda context, _request: render_record(context, record_id, env=os.environ, output_file=output_file),
            build_request=False,
        )


def _record_request_options(*, require_kind: bool, include_id: bool) -> Any:
    def decorator(command: Any) -> Any:
        command = click.option("--lifecycle-refs-json", default=None, help="Additional lifecycle refs as a JSON object.")(command)
        command = click.option("--metadata-json", default=None, help="Additional transition metadata as a JSON object.")(command)
        command = click.option("--content-name", default=None, help="Stored body filename.")(command)
        command = click.option("--render", "render_format", default=None, help="Render a generated view, for example markdown.")(command)
        command = click.option("--template-file", type=click.Path(path_type=Path), default=None, help="Plain Jinja2 template file for structured payloads.")(command)
        command = click.option("--schema-file", type=click.Path(path_type=Path), default=None, help="Plain JSON Schema file for structured payloads.")(command)
        command = click.option("--template-ref", default=None, help="Artifact Format template ref for structured payloads.")(command)
        command = click.option("--schema-ref", default=None, help="Artifact Format schema ref for structured payloads.")(command)
        command = click.option("--format-profile", "format_profile_ref", default=None, help="Artifact Format Profile ref for structured payloads.")(command)
        command = click.option("--payload-file", type=click.Path(path_type=Path), default=None, help="JSON payload file for structured records.")(command)
        command = click.option("--body-file", type=click.Path(path_type=Path), default=None, help="File to copy as the record body.")(command)
        command = click.option("--body", default=None, help="Inline UTF-8 body to store for the record.")(command)
        command = click.option("--semantic-label", default=None, help="Semantic label used for optional body storage.")(command)
        command = click.option("--consumer", default=None, help="Consumer metadata.")(command)
        command = click.option("--producer", default=None, help="Producer metadata.")(command)
        command = click.option("--skill", default=None, help="Producing or owning skill name.")(command)
        command = click.option("--profile", default=None, help="Artifact or record profile.")(command)
        command = click.option("--placeholder", default=None, help="Exact research placeholder token.")(command)
        command = click.option("--topic-actor", "topic_actor_name", default=None, help="Topic Actor name metadata.")(command)
        command = click.option("--actor-kind", default=None, help="Topic Actor kind metadata.")(command)
        command = click.option("--runtime-kind", default=None, help="Topic Actor runtime kind metadata.")(command)
        command = click.option("--controller-kind", default=None, help="Topic Actor controller kind metadata.")(command)
        command = click.option("--adapter-ref", default=None, help="Topic Actor adapter ref metadata.")(command)
        command = click.option("--status", default="ready", show_default=True, help="Lifecycle status.")(command)
        if include_id:
            command = click.option("--id", "record_id", default=None, help="Explicit record id.")(command)
        command = click.option("--record-kind", required=require_kind, help="Workspace Runtime lifecycle record kind.")(command)
        return command
    return decorator


def _with_context(
    ctx: click.Context,
    values: dict[str, Any],
    callback: Any,
    *,
    build_request: bool = True,
) -> int:
    try:
        request = _request_from_values(values) if build_request else None
    except (ResearchRecordError, json.JSONDecodeError) as exc:
        payload = exc.to_payload() if isinstance(exc, ResearchRecordError) else _json_error_payload(exc)
        click.echo(dumps_raw_json(payload))
        return 1
    options = _merge_options(
        ctx,
        project=values.get("project"),
        manifest=values.get("manifest"),
        output_format=values.get("output_format"),
        json_output=bool(values.get("json_output", False)),
        research_topic_id=values.get("research_topic_id"),
        topic_workspace_id=values.get("topic_workspace_id"),
        research_inquiry_id=values.get("research_inquiry_id"),
        research_task_id=values.get("research_task_id"),
        run_id=values.get("run_id"),
        agent_team_instance_id=values.get("agent_team_instance_id"),
        agent_instance_id=values.get("agent_instance_id"),
        topic_agent_team_profile_id=values.get("topic_agent_team_profile_id"),
    )
    context, diagnostics = _context_for_options(options)
    if context is None or has_errors(diagnostics):
        click.echo(
            dumps_raw_json(
                {
                    "ok": False,
                    "mutated": False,
                    "error": {
                        "code": "context_resolution_failed",
                        "message": "Research record commands require a selected Isomer Topic Workspace.",
                    },
                    "diagnostics": [diagnostic.to_json() for diagnostic in diagnostics],
                }
            )
        )
        return 1
    try:
        payload, call_diagnostics = callback(context, request)
    except ResearchRecordError as exc:
        click.echo(dumps_raw_json(exc.to_payload()))
        return 1
    if call_diagnostics and has_errors(call_diagnostics):
        payload = {
            **payload,
            "diagnostics": [diagnostic.to_json() for diagnostic in call_diagnostics],
        }
    click.echo(dumps_raw_json(payload))
    return 0 if payload.get("ok") is not False and not has_errors(call_diagnostics) else 1


def _request_from_values(values: dict[str, Any]) -> ResearchRecordRequest:
    return ResearchRecordRequest(
        record_kind=str(values.get("record_kind") or ""),
        record_id=values.get("record_id"),
        status=str(values.get("status") or "ready"),
        placeholder=values.get("placeholder"),
        profile=values.get("profile"),
        skill=values.get("skill"),
        producer=values.get("producer"),
        consumer=values.get("consumer"),
        topic_actor_name=values.get("topic_actor_name"),
        actor_kind=values.get("actor_kind"),
        runtime_kind=values.get("runtime_kind"),
        controller_kind=values.get("controller_kind"),
        adapter_ref=values.get("adapter_ref"),
        semantic_label=values.get("semantic_label"),
        body=values.get("body"),
        body_file=values.get("body_file"),
        content_name=values.get("content_name"),
        payload_file=values.get("payload_file"),
        format_profile_ref=values.get("format_profile_ref"),
        schema_ref=values.get("schema_ref"),
        template_ref=values.get("template_ref"),
        schema_file=values.get("schema_file"),
        template_file=values.get("template_file"),
        render_format=values.get("render_format"),
        metadata=parse_json_object(values.get("metadata_json"), field_name="metadata-json"),
        lifecycle_refs=parse_string_map(values.get("lifecycle_refs_json"), field_name="lifecycle-refs-json"),
    )


def _json_error_payload(exc: Exception) -> dict[str, object]:
    return {
        "ok": False,
        "error": {
            "code": "invalid_json",
            "message": str(exc),
        },
    }
