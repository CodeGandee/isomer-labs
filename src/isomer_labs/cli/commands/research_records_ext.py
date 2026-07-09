"""Click registration for Isomer research record extension commands."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import click

from isomer_labs.cli.commands.research_ideas_ext import register_research_idea_commands
from isomer_labs.cli.handlers.shared import _context_for_options
from isomer_labs.cli.options import (
    common_options as _common_options,
    merge_options as _merge_options,
    topic_selection_options as _topic_selection_options,
)
from isomer_labs.deepsci_ext.tools import dumps_raw_json
from isomer_labs.core.diagnostics import has_errors
from isomer_labs.records.store import (
    ResearchRecordError,
    ResearchRecordRequest,
    add_lineage_edge,
    archive_record,
    backfill_lineage,
    create_record,
    list_records,
    migrate_structured_payload_files,
    parse_json_object_list,
    parse_json_object,
    parse_string_map,
    render_record,
    revise_record,
    show_record,
    update_record,
    validate_lineage,
    validate_record_payload,
)
from isomer_labs.records.index import (
    cleanup_query_index,
    query_index_export,
    query_index_facets,
    query_index_files,
    query_index_lineage,
    query_index_siblings,
    query_index_list,
    rebuild_query_index,
    validate_query_index,
)


def register_research_record_ext_commands(app: click.Group) -> None:
    ext_command = app.commands.get("ext")
    if isinstance(ext_command, click.Group):
        ext_group = ext_command
    else:
        ext_group = click.Group(name="ext", help="Use extension command surfaces for research records, ideas, and compatibility tooling.")
        app.add_command(ext_group)

    @ext_group.group(name="research", help="Isomer research extension commands.")
    def research_group() -> None:
        pass

    @research_group.group(name="records", help="CRUD commands for topic-scoped research records.")
    def records_group() -> None:
        pass

    register_research_idea_commands(
        research_group,
        with_context=_with_context,
        json_error_payload=_json_error_payload,
    )

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
    @click.option("--include-rendered-body", is_flag=True, help="Include legacy rendered Markdown body when present.")
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

    @records_group.command(name="revise", help="Create a descendant record for a content-changing revision.")
    @_common_options
    @_topic_selection_options
    @_record_request_options(require_kind=False, include_id=False)
    @click.option("--id", "new_record_id", default=None, help="Explicit descendant record id.")
    @click.argument("record_id")
    @click.pass_context
    def revise_command(ctx: click.Context, record_id: str, new_record_id: str | None = None, **kwargs: Any) -> int:
        values = {**kwargs, "record_id": new_record_id}
        return _with_context(
            ctx,
            values,
            lambda context, request: revise_record(context, record_id, request, env=os.environ, cwd=Path.cwd()),
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

    @records_group.command(name="migrate-payload-files", help="Export legacy structured payload rows into managed JSON payload files.")
    @_common_options
    @_topic_selection_options
    @click.pass_context
    def migrate_payload_files_command(ctx: click.Context, **kwargs: Any) -> int:
        return _with_context(
            ctx,
            dict(kwargs),
            lambda context, _request: migrate_structured_payload_files(context, env=os.environ, cwd=Path.cwd()),
            build_request=False,
        )

    @records_group.group(name="index", help="Maintain the research record query index.")
    def index_group() -> None:
        pass

    @index_group.command(name="rebuild", help="Refresh derived query-index rows from canonical records.")
    @_common_options
    @_topic_selection_options
    @click.option("--record-id", default=None, help="Refresh one record id instead of the whole Topic Workspace.")
    @click.option("--include-operation-set-files", is_flag=True, help="Include accepted operation-set files when extractors can resolve them.")
    @click.option("--dry-run", is_flag=True, help="Report the rebuild plan without mutating query-index rows.")
    @click.pass_context
    def index_rebuild_command(ctx: click.Context, record_id: str | None = None, include_operation_set_files: bool = False, dry_run: bool = False, **kwargs: Any) -> int:
        values = dict(kwargs)
        return _with_context(
            ctx,
            values,
            lambda context, _request: rebuild_query_index(
                context,
                env=os.environ,
                record_id=record_id,
                include_operation_set_files=include_operation_set_files,
                dry_run=dry_run,
            ),
            build_request=False,
        )

    @index_group.command(name="validate", help="Validate query-index consistency without mutating runtime state.")
    @_common_options
    @_topic_selection_options
    @click.option("--record-id", default=None, help="Validate one indexed record id.")
    @click.pass_context
    def index_validate_command(ctx: click.Context, record_id: str | None = None, **kwargs: Any) -> int:
        return _with_context(
            ctx,
            dict(kwargs),
            lambda context, _request: validate_query_index(context, env=os.environ, record_id=record_id),
            build_request=False,
        )

    @index_group.command(name="cleanup", help="Preview or apply safe query-index cleanup.")
    @_common_options
    @_topic_selection_options
    @click.option("--stale-derived", is_flag=True, help="Select stale derived index rows.")
    @click.option("--orphaned", is_flag=True, help="Select index rows whose canonical record is missing.")
    @click.option("--missing-files", is_flag=True, help="Select missing indexed file attachment rows.")
    @click.option("--dry-run", "dry_run", is_flag=True, help="Preview cleanup without mutating query-index rows.")
    @click.option("--apply", "apply_cleanup", is_flag=True, help="Apply selected cleanup to query-index rows only.")
    @click.pass_context
    def index_cleanup_command(
        ctx: click.Context,
        stale_derived: bool = False,
        orphaned: bool = False,
        missing_files: bool = False,
        dry_run: bool = False,
        apply_cleanup: bool = False,
        **kwargs: Any,
    ) -> int:
        return _with_context(
            ctx,
            dict(kwargs),
            lambda context, _request: cleanup_query_index(
                context,
                env=os.environ,
                stale_derived=stale_derived,
                orphaned=orphaned,
                missing_files=missing_files,
                apply=apply_cleanup and not dry_run,
            ),
            build_request=False,
        )

    @records_group.group(name="query", help="Read the research record query index.")
    def query_group() -> None:
        pass

    @query_group.command(name="list", help="List indexed research records.")
    @_common_options
    @_topic_selection_options
    @click.option("--record-kind", default=None, help="Filter by Workspace Runtime lifecycle record kind.")
    @click.option("--status", default=None, help="Filter by lifecycle status.")
    @click.option("--profile", default=None, help="Filter by profile or Artifact Format Profile ref.")
    @click.option("--facet", default=None, help="Filter to records that have a normalized facet.")
    @click.option("--limit", type=int, default=None, help="Maximum records to return.")
    @click.pass_context
    def query_list_command(ctx: click.Context, **kwargs: Any) -> int:
        values = dict(kwargs)
        return _with_context(
            ctx,
            values,
            lambda context, _request: query_index_list(
                context,
                env=os.environ,
                record_kind=values.get("record_kind"),
                status=values.get("status"),
                profile=values.get("profile"),
                facet=values.get("facet"),
                limit=values.get("limit"),
            ),
            build_request=False,
        )

    @query_group.command(name="export", help="Export indexed research records for GUI or operator views.")
    @_common_options
    @_topic_selection_options
    @click.option("--view", default="graph", show_default=True, help="Export view: graph, dashboard, timeline, ideas, experiments, or claims.")
    @click.option("--format", "export_format", default="json", show_default=True, help="Export format. Only json is currently supported.")
    @click.pass_context
    def query_export_command(ctx: click.Context, view: str = "graph", export_format: str = "json", **kwargs: Any) -> int:
        if export_format != "json":
            click.echo(dumps_raw_json({"ok": False, "mutated": False, "error": {"code": "unsupported_export_format", "message": "Research record query export currently supports only json."}}))
            return 1
        return _with_context(
            ctx,
            dict(kwargs),
            lambda context, _request: query_index_export(context, env=os.environ, view=view),
            build_request=False,
        )

    @query_group.command(name="lineage", help="Show indexed lineage for one record.")
    @_common_options
    @_topic_selection_options
    @click.option("--direction", default="both", show_default=True, help="Lineage direction: upstream, downstream, or both.")
    @click.argument("record_id")
    @click.pass_context
    def query_lineage_command(ctx: click.Context, record_id: str, direction: str = "both", **kwargs: Any) -> int:
        return _with_context(
            ctx,
            dict(kwargs),
            lambda context, _request: query_index_lineage(context, record_id, env=os.environ, direction=direction),
            build_request=False,
        )

    @query_group.command(name="siblings", help="Show canonical generation siblings for one record.")
    @_common_options
    @_topic_selection_options
    @click.argument("record_id")
    @click.pass_context
    def query_siblings_command(ctx: click.Context, record_id: str, **kwargs: Any) -> int:
        return _with_context(
            ctx,
            dict(kwargs),
            lambda context, _request: query_index_siblings(context, record_id, env=os.environ),
            build_request=False,
        )

    @query_group.command(name="files", help="Show indexed files for one record.")
    @_common_options
    @_topic_selection_options
    @click.argument("record_id")
    @click.pass_context
    def query_files_command(ctx: click.Context, record_id: str, **kwargs: Any) -> int:
        return _with_context(
            ctx,
            dict(kwargs),
            lambda context, _request: query_index_files(context, record_id, env=os.environ),
            build_request=False,
        )

    @query_group.command(name="facets", help="Show indexed normalized facets for one record.")
    @_common_options
    @_topic_selection_options
    @click.option("--facet", default=None, help="Facet to return: ideas, routes, metrics, claims, or facts.")
    @click.argument("record_id")
    @click.pass_context
    def query_facets_command(ctx: click.Context, record_id: str, facet: str | None = None, **kwargs: Any) -> int:
        return _with_context(
            ctx,
            dict(kwargs),
            lambda context, _request: query_index_facets(context, record_id, env=os.environ, facet=facet),
            build_request=False,
        )

    @records_group.group(name="lineage", help="Maintain canonical research record lineage.")
    def lineage_group() -> None:
        pass

    @lineage_group.command(name="add", help="Add one canonical parent-child lineage edge.")
    @_common_options
    @_topic_selection_options
    @click.option("--lineage-kind", required=True, help="Canonical lineage kind.")
    @click.option("--parent-role", default=None, help="Optional parent role.")
    @click.option("--generation-id", default=None, help="Optional generation group id.")
    @click.option("--generation-purpose", default=None, help="Optional generation group purpose.")
    @click.option("--decision-record-id", default=None, help="Optional decision record id.")
    @click.option("--rationale", default=None, help="Lineage rationale.")
    @click.option("--metadata-json", default=None, help="Additional lineage metadata as a JSON object.")
    @click.option("--status", default="ready", show_default=True, help="Lineage status.")
    @click.argument("parent_record_id")
    @click.argument("child_record_id")
    @click.pass_context
    def lineage_add_command(ctx: click.Context, parent_record_id: str, child_record_id: str, **kwargs: Any) -> int:
        values = dict(kwargs)
        try:
            metadata = parse_json_object(values.get("metadata_json"), field_name="metadata-json")
        except (ResearchRecordError, json.JSONDecodeError) as exc:
            payload = exc.to_payload() if isinstance(exc, ResearchRecordError) else _json_error_payload(exc)
            click.echo(dumps_raw_json(payload))
            return 1
        return _with_context(
            ctx,
            values,
            lambda context, _request: add_lineage_edge(
                context,
                parent_record_id=parent_record_id,
                child_record_id=child_record_id,
                lineage_kind=str(values.get("lineage_kind") or ""),
                env=os.environ,
                parent_role=values.get("parent_role"),
                generation_id=values.get("generation_id"),
                generation_purpose=values.get("generation_purpose"),
                decision_record_id=values.get("decision_record_id"),
                rationale=values.get("rationale"),
                metadata=metadata,
                status=str(values.get("status") or "ready"),
            ),
            build_request=False,
        )

    @lineage_group.command(name="validate", help="Validate canonical lineage DAG state.")
    @_common_options
    @_topic_selection_options
    @click.pass_context
    def lineage_validate_command(ctx: click.Context, **kwargs: Any) -> int:
        return _with_context(
            ctx,
            dict(kwargs),
            lambda context, _request: validate_lineage(context, env=os.environ),
            build_request=False,
        )

    @lineage_group.command(name="query", help="Query canonical lineage for one record.")
    @_common_options
    @_topic_selection_options
    @click.option("--direction", default="both", show_default=True, help="Lineage direction: upstream, downstream, or both.")
    @click.argument("record_id")
    @click.pass_context
    def lineage_query_command(ctx: click.Context, record_id: str, direction: str = "both", **kwargs: Any) -> int:
        return _with_context(
            ctx,
            dict(kwargs),
            lambda context, _request: query_index_lineage(context, record_id, env=os.environ, direction=direction),
            build_request=False,
        )

    @lineage_group.command(name="siblings", help="Query records in the same canonical generation group.")
    @_common_options
    @_topic_selection_options
    @click.argument("record_id")
    @click.pass_context
    def lineage_siblings_command(ctx: click.Context, record_id: str, **kwargs: Any) -> int:
        return _with_context(
            ctx,
            dict(kwargs),
            lambda context, _request: query_index_siblings(context, record_id, env=os.environ),
            build_request=False,
        )

    @lineage_group.command(name="backfill", help="Backfill canonical lineage from explicit stored refs.")
    @_common_options
    @_topic_selection_options
    @click.option("--dry-run/--apply", default=True, show_default=True, help="Preview or apply explicit-ref lineage backfill.")
    @click.pass_context
    def lineage_backfill_command(ctx: click.Context, dry_run: bool = True, **kwargs: Any) -> int:
        return _with_context(
            ctx,
            dict(kwargs),
            lambda context, _request: backfill_lineage(context, env=os.environ, dry_run=dry_run),
            build_request=False,
        )


def _record_request_options(*, require_kind: bool, include_id: bool) -> Any:
    def decorator(command: Any) -> Any:
        command = click.option("--primary-idea-json", default=None, help="Canonical primary idea object realized by this record.")(command)
        command = click.option("--idea-parents-json", default=None, help="Canonical idea parent edges as a JSON array of objects.")(command)
        command = click.option("--idea-realizations-json", default=None, help="Canonical idea realizations as a JSON array of objects.")(command)
        command = click.option("--realizes-idea-id", default=None, help="Canonical idea id realized by this record.")(command)
        command = click.option("--lifecycle-refs-json", default=None, help="Additional lifecycle refs as a JSON object.")(command)
        command = click.option("--lineage-rationale", default=None, help="Canonical lineage rationale for parent edges.")(command)
        command = click.option("--decision-record-id", default=None, help="Decision record id associated with canonical lineage.")(command)
        command = click.option("--generation-purpose", default=None, help="Generation group purpose for sibling candidates.")(command)
        command = click.option("--generation-id", default=None, help="Generation group id for sibling candidates.")(command)
        command = click.option("--lineage-kind", default=None, help="Default canonical lineage kind for parents-json.")(command)
        command = click.option("--parents-json", default=None, help="Canonical lineage parents as a JSON array of objects.")(command)
        command = click.option("--index-hints-json", default=None, help="Query-index hints as a JSON object.")(command)
        command = click.option("--files-json", default=None, help="Query-index file attachments as a JSON array of objects.")(command)
        command = click.option("--relationships-json", default=None, help="Query-index relationship refs as a JSON array of objects.")(command)
        command = click.option("--metadata-json", default=None, help="Additional transition metadata as a JSON object.")(command)
        command = click.option("--content-name", default=None, help="Stored body filename.")(command)
        command = click.option("--render", "render_format", default=None, help="Validate an on-demand render, for example markdown.")(command)
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
        relationships=parse_json_object_list(values.get("relationships_json"), field_name="relationships-json"),
        parents=parse_json_object_list(values.get("parents_json"), field_name="parents-json"),
        lineage_kind=values.get("lineage_kind"),
        generation_id=values.get("generation_id"),
        generation_purpose=values.get("generation_purpose"),
        decision_record_id=values.get("decision_record_id"),
        lineage_rationale=values.get("lineage_rationale"),
        file_attachments=parse_json_object_list(values.get("files_json"), field_name="files-json"),
        index_hints=parse_json_object(values.get("index_hints_json"), field_name="index-hints-json"),
        realizes_idea_id=values.get("realizes_idea_id"),
        idea_realizations=parse_json_object_list(values.get("idea_realizations_json"), field_name="idea-realizations-json"),
        idea_parents=parse_json_object_list(values.get("idea_parents_json"), field_name="idea-parents-json"),
        primary_idea=parse_json_object(values.get("primary_idea_json"), field_name="primary-idea-json"),
    )


def _json_error_payload(exc: Exception) -> dict[str, object]:
    return {
        "ok": False,
        "error": {
            "code": "invalid_json",
            "message": str(exc),
        },
    }
