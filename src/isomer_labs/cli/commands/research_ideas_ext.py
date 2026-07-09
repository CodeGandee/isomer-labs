"""Click registration for canonical Research Idea extension commands."""

from __future__ import annotations

import json
import os
from typing import Any, Callable

import click

from isomer_labs.cli.options import (
    common_options as _common_options,
    topic_selection_options as _topic_selection_options,
)
from isomer_labs.deepsci_ext.tools import dumps_raw_json
from isomer_labs.records.store import (
    ResearchRecordError,
    add_research_idea_lineage_edge,
    graph_research_ideas,
    import_research_ideas_from_record,
    parse_json_object,
    query_research_ideas,
    realize_research_idea,
    repair_research_ideas,
    upsert_research_idea,
    upsert_research_idea_generation_group,
    validate_research_ideas,
)


WithContext = Callable[..., int]
JsonErrorPayload = Callable[[Exception], dict[str, object]]


def register_research_idea_commands(
    research_group: click.Group,
    *,
    with_context: WithContext,
    json_error_payload: JsonErrorPayload,
) -> None:
    @research_group.group(name="ideas", help="Maintain canonical Research Ideas and idea lineage.")
    def ideas_group() -> None:
        pass

    @ideas_group.command(name="upsert", help="Create or update a canonical topic-scoped Research Idea.")
    @_common_options
    @_topic_selection_options
    @click.option("--idea-id", required=True, help="Stable semantic topic-scoped idea id.")
    @click.option("--title", required=True, help="Human-readable idea title.")
    @click.option("--summary", required=True, help="Short idea summary.")
    @click.option("--family", default=None, help="Optional idea family.")
    @click.option("--status", default="candidate", show_default=True, help="Idea status.")
    @click.option("--visibility", default="primary", show_default=True, help="primary, supporting, or hidden.")
    @click.option("--alias", "aliases", multiple=True, help="Source-local label such as R1 or C3.")
    @click.option("--source-record-id", default=None, help="Record that introduced or best expresses this idea.")
    @click.option("--source-json-path", default=None, help="JSON path inside the source record.")
    @click.option("--metadata-json", default=None, help="Additional idea metadata as a JSON object.")
    @click.pass_context
    def ideas_upsert_command(ctx: click.Context, **kwargs: Any) -> int:
        values = dict(kwargs)
        try:
            metadata = parse_json_object(values.get("metadata_json"), field_name="metadata-json")
        except (ResearchRecordError, json.JSONDecodeError) as exc:
            payload = exc.to_payload() if isinstance(exc, ResearchRecordError) else json_error_payload(exc)
            click.echo(dumps_raw_json(payload))
            return 1
        return with_context(
            ctx,
            values,
            lambda context, _request: upsert_research_idea(
                context,
                env=os.environ,
                idea_id=str(values["idea_id"]),
                title=str(values["title"]),
                summary=str(values["summary"]),
                family=values.get("family"),
                status=str(values.get("status") or "candidate"),
                visibility=str(values.get("visibility") or "primary"),
                aliases=[str(alias) for alias in values.get("aliases", ())],
                source_record_id=values.get("source_record_id"),
                source_json_path=values.get("source_json_path"),
                metadata=metadata,
            ),
            build_request=False,
        )

    @ideas_group.command(name="realize", help="Link a Research Idea to a durable research record.")
    @_common_options
    @_topic_selection_options
    @click.option("--idea-id", required=True, help="Canonical idea id.")
    @click.option("--record-id", required=True, help="Durable record id that realizes the idea.")
    @click.option("--source-json-path", default=None, help="JSON path inside the source record.")
    @click.option("--realization-stage", default=None, help="Workflow stage for this realization.")
    @click.option("--semantic-id", default=None, help="Optional semantic id within the record.")
    @click.option("--latest/--not-latest", default=True, show_default=True, help="Mark this as the latest realization for the idea.")
    @click.option("--metadata-json", default=None, help="Additional realization metadata as a JSON object.")
    @click.pass_context
    def ideas_realize_command(ctx: click.Context, **kwargs: Any) -> int:
        values = dict(kwargs)
        try:
            metadata = parse_json_object(values.get("metadata_json"), field_name="metadata-json")
        except (ResearchRecordError, json.JSONDecodeError) as exc:
            payload = exc.to_payload() if isinstance(exc, ResearchRecordError) else json_error_payload(exc)
            click.echo(dumps_raw_json(payload))
            return 1
        return with_context(
            ctx,
            values,
            lambda context, _request: realize_research_idea(
                context,
                env=os.environ,
                idea_id=str(values["idea_id"]),
                record_id=str(values["record_id"]),
                source_json_path=values.get("source_json_path"),
                realization_stage=values.get("realization_stage"),
                semantic_id=values.get("semantic_id"),
                latest=bool(values.get("latest", True)),
                metadata=metadata,
            ),
            build_request=False,
        )

    @ideas_group.group(name="lineage", help="Maintain canonical idea lineage edges.")
    def ideas_lineage_group() -> None:
        pass

    @ideas_lineage_group.command(name="add", help="Add one typed idea-level parent-child edge.")
    @_common_options
    @_topic_selection_options
    @click.option("--lineage-kind", required=True, help="Canonical idea lineage kind.")
    @click.option("--parent-role", default=None, help="Optional parent role.")
    @click.option("--generation-id", default=None, help="Optional idea generation group id.")
    @click.option("--decision-record-id", default=None, help="Optional decision record id.")
    @click.option("--rationale", default=None, help="Lineage rationale.")
    @click.option("--status", default="ready", show_default=True, help="Lineage status.")
    @click.option("--confidence", type=float, default=None, help="Optional confidence score.")
    @click.option("--metadata-json", default=None, help="Additional lineage metadata as a JSON object.")
    @click.argument("parent_idea_id")
    @click.argument("child_idea_id")
    @click.pass_context
    def ideas_lineage_add_command(ctx: click.Context, parent_idea_id: str, child_idea_id: str, **kwargs: Any) -> int:
        values = dict(kwargs)
        try:
            metadata = parse_json_object(values.get("metadata_json"), field_name="metadata-json")
        except (ResearchRecordError, json.JSONDecodeError) as exc:
            payload = exc.to_payload() if isinstance(exc, ResearchRecordError) else json_error_payload(exc)
            click.echo(dumps_raw_json(payload))
            return 1
        return with_context(
            ctx,
            values,
            lambda context, _request: add_research_idea_lineage_edge(
                context,
                env=os.environ,
                parent_idea_id=parent_idea_id,
                child_idea_id=child_idea_id,
                lineage_kind=str(values.get("lineage_kind") or ""),
                parent_role=values.get("parent_role"),
                generation_id=values.get("generation_id"),
                decision_record_id=values.get("decision_record_id"),
                rationale=values.get("rationale"),
                status=str(values.get("status") or "ready"),
                confidence=values.get("confidence"),
                metadata=metadata,
            ),
            build_request=False,
        )

    @ideas_group.group(name="generation", help="Maintain canonical idea generation groups.")
    def ideas_generation_group() -> None:
        pass

    @ideas_generation_group.command(name="upsert", help="Create or update an idea sibling generation group.")
    @_common_options
    @_topic_selection_options
    @click.option("--generation-id", required=True, help="Generation group id.")
    @click.option("--parent-idea-id", "parent_idea_ids", multiple=True, required=True, help="Parent idea id. Repeat for many parents.")
    @click.option("--purpose", default=None, help="Generation purpose.")
    @click.option("--producer-skill", default=None, help="Skill that produced the generation.")
    @click.option("--decision-record-id", default=None, help="Decision record id.")
    @click.option("--metadata-json", default=None, help="Additional group metadata as a JSON object.")
    @click.pass_context
    def ideas_generation_upsert_command(ctx: click.Context, **kwargs: Any) -> int:
        values = dict(kwargs)
        try:
            metadata = parse_json_object(values.get("metadata_json"), field_name="metadata-json")
        except (ResearchRecordError, json.JSONDecodeError) as exc:
            payload = exc.to_payload() if isinstance(exc, ResearchRecordError) else json_error_payload(exc)
            click.echo(dumps_raw_json(payload))
            return 1
        return with_context(
            ctx,
            values,
            lambda context, _request: upsert_research_idea_generation_group(
                context,
                env=os.environ,
                generation_id=str(values["generation_id"]),
                parent_idea_ids=[str(item) for item in values.get("parent_idea_ids", ())],
                purpose=values.get("purpose"),
                producer_skill=values.get("producer_skill"),
                decision_record_id=values.get("decision_record_id"),
                metadata=metadata,
            ),
            build_request=False,
        )

    @ideas_group.command(name="query", help="Read canonical Research Ideas and related rows.")
    @_common_options
    @_topic_selection_options
    @click.option("--visibility", default=None, help="Optional visibility filter.")
    @click.option("--include-archived", is_flag=True, help="Include archived ideas and edges.")
    @click.pass_context
    def ideas_query_command(ctx: click.Context, **kwargs: Any) -> int:
        values = dict(kwargs)
        return with_context(ctx, values, lambda context, _request: query_research_ideas(context, env=os.environ, visibility=values.get("visibility"), include_archived=bool(values.get("include_archived"))), build_request=False)

    @ideas_group.command(name="graph", help="Read the canonical idea graph.")
    @_common_options
    @_topic_selection_options
    @click.option("--visibility", default="primary", show_default=True, help="Visibility to show when supporting ideas are not included.")
    @click.option("--include-supporting", is_flag=True, help="Include supporting and hidden ideas.")
    @click.pass_context
    def ideas_graph_command(ctx: click.Context, **kwargs: Any) -> int:
        values = dict(kwargs)
        return with_context(ctx, values, lambda context, _request: graph_research_ideas(context, env=os.environ, visibility=str(values.get("visibility") or "primary"), include_supporting=bool(values.get("include_supporting"))), build_request=False)

    @ideas_group.command(name="validate", help="Validate canonical idea identity, realizations, lineage, and generation groups.")
    @_common_options
    @_topic_selection_options
    @click.pass_context
    def ideas_validate_command(ctx: click.Context, **kwargs: Any) -> int:
        return with_context(ctx, dict(kwargs), lambda context, _request: validate_research_ideas(context, env=os.environ), build_request=False)

    @ideas_group.command(name="import-from-record", help="Preview or apply a legacy record idea import plan.")
    @_common_options
    @_topic_selection_options
    @click.option("--apply", "apply_import", is_flag=True, help="Apply the import plan.")
    @click.argument("record_id")
    @click.pass_context
    def ideas_import_command(ctx: click.Context, record_id: str, apply_import: bool = False, **kwargs: Any) -> int:
        return with_context(ctx, dict(kwargs), lambda context, _request: import_research_ideas_from_record(context, record_id, env=os.environ, apply=apply_import), build_request=False)

    @ideas_group.command(name="repair", help="Preview canonical idea repair diagnostics.")
    @_common_options
    @_topic_selection_options
    @click.option("--apply", "apply_repair", is_flag=True, help="Reserved for future deterministic repair plans.")
    @click.option("--update-payloads", is_flag=True, help="Allow explicit payload-file updates when a repair path supports them.")
    @click.pass_context
    def ideas_repair_command(ctx: click.Context, apply_repair: bool = False, update_payloads: bool = False, **kwargs: Any) -> int:
        return with_context(ctx, dict(kwargs), lambda context, _request: repair_research_ideas(context, env=os.environ, apply=apply_repair, update_payloads=update_payloads), build_request=False)
