"""Click registration for canonical Research Idea extension commands."""

from __future__ import annotations

import json
import os
from typing import Any, Callable, Mapping

import click

from isomer_labs.cli.options import (
    common_options as _common_options,
    topic_selection_options as _topic_selection_options,
)
from isomer_labs.deepsci_ext.tools import dumps_raw_json
from isomer_labs.records.steering import ResearchIdeaSteeringRequest, steer_research_idea
from isomer_labs.records.store import (
    ResearchRecordError,
    add_research_idea_lineage_edge,
    graph_research_ideas,
    import_research_ideas_from_record,
    migrate_legacy_kaoju_direction_set,
    migrate_research_idea_portfolio,
    parse_json_object,
    query_research_idea_decision_context,
    query_research_ideas,
    realize_research_idea,
    repair_research_ideas,
    transition_research_idea,
    traverse_research_ideas,
    upsert_research_idea,
    upsert_research_idea_decision_option,
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
    @click.option("--exploration-state", type=click.Choice(("unknown", "unexplored", "exploring", "explored")), default=None, help="Initial canonical exploration state.")
    @click.option("--decision-state", type=click.Choice(("unknown", "open", "shortlisted", "selected", "deferred", "closed")), default=None, help="Initial canonical decision state.")
    @click.option("--evidence-state", type=click.Choice(("unknown", "unassessed", "inconclusive", "supported", "mixed", "refuted")), default=None, help="Initial canonical evidence state.")
    @click.option("--archive-state", type=click.Choice(("active", "archived")), default=None, help="Initial canonical archive state.")
    @click.option("--status", default=None, help="Deprecated compatibility status; use canonical facet options.")
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
                status=str(values["status"]) if values.get("status") is not None else None,
                exploration_state=values.get("exploration_state"),
                decision_state=values.get("decision_state"),
                evidence_state=values.get("evidence_state"),
                archive_state=values.get("archive_state"),
                visibility=str(values.get("visibility") or "primary"),
                aliases=[str(alias) for alias in values.get("aliases", ())],
                source_record_id=values.get("source_record_id"),
                source_json_path=values.get("source_json_path"),
                metadata=metadata,
            ),
            build_request=False,
        )

    @ideas_group.command(name="transition", help="Change one canonical Research Idea facet with durable context.")
    @_common_options
    @_topic_selection_options
    @click.argument("idea_id")
    @click.option("--facet", required=True, type=click.Choice(("exploration_state", "decision_state", "evidence_state", "archive_state", "visibility")), help="Canonical facet to change.")
    @click.option("--expected-from", required=True, help="Required current facet value.")
    @click.option("--to", "next_value", required=True, help="New canonical facet value.")
    @click.option("--actor-ref", "--actor", required=True, help="Actor responsible for the change.")
    @click.option("--rationale", required=True, help="Why this state change is justified.")
    @click.option("--reason-code", default=None, help="Reason code, required for closure.")
    @click.option("--decision-record-id", default=None, help="Decision Record supporting the transition.")
    @click.option("--gate-id", default=None, help="Gate supporting the transition.")
    @click.option("--evidence-item-ref", "evidence_item_refs", multiple=True, help="Evidence Item ref. Repeat as needed.")
    @click.option("--artifact-ref", "artifact_refs", multiple=True, help="Artifact ref. Repeat as needed.")
    @click.option("--finding-ref", "finding_refs", multiple=True, help="Finding ref. Repeat as needed.")
    @click.option("--research-task-id", default=None, help="Research Task supporting the transition.")
    @click.option("--run-id", default=None, help="Run supporting the transition.")
    @click.option("--provenance-record-ref", "provenance_record_refs", multiple=True, help="Provenance Record ref. Repeat as needed.")
    @click.option("--operation-id", default=None, help="Explicit operation correlation id.")
    @click.option("--idempotency-key", default=None, help="Idempotency key; defaults to the operation id.")
    @click.option("--metadata-json", default=None, help="Additional transition metadata as a JSON object.")
    @click.pass_context
    def ideas_transition_command(ctx: click.Context, idea_id: str, **kwargs: Any) -> int:
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
            lambda context, _request: transition_research_idea(
                context,
                env=os.environ,
                idea_id=idea_id,
                facet=str(values["facet"]),
                expected_from=str(values["expected_from"]),
                next_value=str(values["next_value"]),
                actor_ref=str(values["actor_ref"]),
                rationale=str(values["rationale"]),
                reason_code=values.get("reason_code"),
                decision_record_id=values.get("decision_record_id"),
                gate_id=values.get("gate_id"),
                evidence_item_refs=[str(item) for item in values.get("evidence_item_refs", ())],
                artifact_refs=[str(item) for item in values.get("artifact_refs", ())],
                finding_refs=[str(item) for item in values.get("finding_refs", ())],
                research_task_id=values.get("research_task_id"),
                run_id=values.get("run_id"),
                provenance_record_refs=[str(item) for item in values.get("provenance_record_refs", ())],
                operation_id=values.get("operation_id"),
                idempotency_key=values.get("idempotency_key"),
                metadata=metadata,
            ),
            build_request=False,
        )

    @ideas_group.command(name="steer", help="Start focused exploration alongside current work or instead of exact selected ideas.")
    @_common_options
    @_topic_selection_options
    @click.option("--action", required=True, type=click.Choice(("explore", "explore-instead")), help="Explicit steering action.")
    @click.option("--target-idea-id", required=True, help="Canonical Research Idea to explore.")
    @click.option("--replace-idea-id", "replaced_idea_ids", multiple=True, help="Exact selected Research Idea to replace. Repeat as needed.")
    @click.option("--actor-ref", "--actor", required=True, help="Actor confirming the steering action.")
    @click.option("--idempotency-key", required=True, help="Stable retry key for this steering request.")
    @click.option("--expected-index-revision", default=None, help="Portfolio index revision shown during confirmation.")
    @click.option("--expected-states-json", default=None, help="Expected canonical facets keyed by idea id.")
    @click.option("--replacement-dispositions-json", default=None, help="Replacement idea ids mapped to deferred or closed.")
    @click.option("--replacement-closure-reasons-json", default=None, help="Closed replacement idea ids mapped to canonical closure reasons.")
    @click.option("--rationale", default=None, help="Actor-authored steering rationale.")
    @click.option("--prompt", "user_prompt", default=None, help="Prompt context sent with exact durable Research Idea refs.")
    @click.option("--reopen-confirmed", is_flag=True, help="Confirm reopening a deferred or closed target.")
    @click.option("--gate-policy", type=click.Choice(("none", "reopen", "replace", "all")), default="none", show_default=True, help="Gate policy for governed consequences.")
    @click.option("--gate-resolution-ref", default=None, help="Resolved Gate ref when policy requires one.")
    @click.option("--source-agent-instance-id", default=None, help="Project Operator Agent Instance used for dispatch.")
    @click.option("--target-agent-instance-id", default=None, help="Topic research actor Agent Instance used for dispatch.")
    @click.option("--no-dispatch", is_flag=True, help="Commit canonical steering and leave actor dispatch pending.")
    @click.pass_context
    def ideas_steer_command(ctx: click.Context, **kwargs: Any) -> int:
        values = dict(kwargs)
        try:
            expected_states = _nested_string_map(parse_json_object(values.get("expected_states_json"), field_name="expected-states-json"), field_name="expected-states-json")
            replacement_dispositions = _string_map(parse_json_object(values.get("replacement_dispositions_json"), field_name="replacement-dispositions-json"), field_name="replacement-dispositions-json")
            replacement_closure_reasons = _string_map(parse_json_object(values.get("replacement_closure_reasons_json"), field_name="replacement-closure-reasons-json"), field_name="replacement-closure-reasons-json")
        except (ResearchRecordError, json.JSONDecodeError) as exc:
            payload = exc.to_payload() if isinstance(exc, ResearchRecordError) else json_error_payload(exc)
            click.echo(dumps_raw_json(payload))
            return 1
        request = ResearchIdeaSteeringRequest(
            action="explore_instead" if values["action"] == "explore-instead" else "explore",
            target_idea_id=str(values["target_idea_id"]),
            actor_ref=str(values["actor_ref"]),
            idempotency_key=str(values["idempotency_key"]),
            expected_index_revision=values.get("expected_index_revision"),
            expected_states=expected_states,
            replaced_idea_ids=[str(item) for item in values.get("replaced_idea_ids", ())],
            replacement_dispositions=replacement_dispositions,
            replacement_closure_reasons=replacement_closure_reasons,
            rationale=values.get("rationale"),
            user_prompt=values.get("user_prompt"),
            reopen_confirmed=bool(values.get("reopen_confirmed")),
            gate_policy=values.get("gate_policy") or "none",
            gate_resolution_ref=values.get("gate_resolution_ref"),
            agent_team_instance_id=values.get("agent_team_instance_id"),
            source_agent_instance_id=values.get("source_agent_instance_id"),
            target_agent_instance_id=values.get("target_agent_instance_id"),
        )
        return with_context(
            ctx,
            values,
            lambda context, _request: steer_research_idea(
                context,
                env=os.environ,
                request=request,
                dispatch=not bool(values.get("no_dispatch")),
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
    @click.option("--parent-idea-id", "parent_idea_ids", multiple=True, help="Parent idea id. Repeat for many parents; omit for a root proposal slate.")
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

    @ideas_group.group(name="decision-options", help="Maintain explicit Research Idea membership in Decision Records.")
    def ideas_decision_options_group() -> None:
        pass

    @ideas_decision_options_group.command(name="upsert", help="Create or update one considered Research Idea option.")
    @_common_options
    @_topic_selection_options
    @click.option("--decision-record-id", required=True, help="Decision Record containing the option set.")
    @click.option("--idea-id", required=True, help="Canonical Research Idea considered by the decision.")
    @click.option("--outcome", required=True, type=click.Choice(("considered", "selected", "not_selected", "shortlisted", "deferred", "closed", "reopened")), help="Authored option outcome.")
    @click.option("--actor-ref", "--actor", required=True, help="Actor responsible for the option outcome.")
    @click.option("--option-role", default=None, help="Optional option role.")
    @click.option("--ordinal", type=int, default=None, help="Optional authored ordering.")
    @click.option("--generation-id", default=None, help="Relevant Idea Generation Group.")
    @click.option("--rationale", default=None, help="Option-specific rationale.")
    @click.option("--consequence", default=None, help="Option-specific consequence.")
    @click.option("--supporting-ref", "supporting_refs", multiple=True, help="Supporting durable ref. Repeat as needed.")
    @click.option("--operation-id", default=None, help="Explicit operation correlation id.")
    @click.option("--idempotency-key", default=None, help="Idempotency key; defaults to the operation id.")
    @click.option("--metadata-json", default=None, help="Additional option metadata as a JSON object.")
    @click.pass_context
    def ideas_decision_options_upsert_command(ctx: click.Context, **kwargs: Any) -> int:
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
            lambda context, _request: upsert_research_idea_decision_option(
                context,
                env=os.environ,
                decision_record_id=str(values["decision_record_id"]),
                idea_id=str(values["idea_id"]),
                outcome=str(values["outcome"]),
                actor_ref=str(values["actor_ref"]),
                option_role=values.get("option_role"),
                ordinal=values.get("ordinal"),
                generation_id=values.get("generation_id"),
                rationale=values.get("rationale"),
                consequence=values.get("consequence"),
                supporting_refs=[str(item) for item in values.get("supporting_refs", ())],
                operation_id=values.get("operation_id"),
                idempotency_key=values.get("idempotency_key"),
                metadata=metadata,
            ),
            build_request=False,
        )

    @ideas_group.command(name="decision-context", help="Read complete recorded Research Idea decision context.")
    @_common_options
    @_topic_selection_options
    @click.option("--idea-id", default=None, help="Restrict context to decisions involving one Research Idea.")
    @click.option("--decision-record-id", default=None, help="Restrict context to one Decision Record.")
    @click.pass_context
    def ideas_decision_context_command(ctx: click.Context, **kwargs: Any) -> int:
        values = dict(kwargs)
        return with_context(
            ctx,
            values,
            lambda context, _request: query_research_idea_decision_context(
                context,
                env=os.environ,
                idea_id=values.get("idea_id"),
                decision_record_id=values.get("decision_record_id"),
            ),
            build_request=False,
        )

    @ideas_group.command(name="query", help="Read canonical Research Ideas and related rows.")
    @_common_options
    @_topic_selection_options
    @click.option("--exploration-state", "exploration_states", multiple=True, type=click.Choice(("unknown", "unexplored", "exploring", "explored")), help="Exploration-state filter. Repeat for OR semantics.")
    @click.option("--decision-state", "decision_states", multiple=True, type=click.Choice(("unknown", "open", "shortlisted", "selected", "deferred", "closed")), help="Decision-state filter. Repeat for OR semantics.")
    @click.option("--evidence-state", "evidence_states", multiple=True, type=click.Choice(("unknown", "unassessed", "inconclusive", "supported", "mixed", "refuted")), help="Evidence-state filter. Repeat for OR semantics.")
    @click.option("--archive-state", "archive_states", multiple=True, type=click.Choice(("active", "archived")), help="Archive-state filter. Repeat for OR semantics.")
    @click.option("--visibility", "visibilities", multiple=True, type=click.Choice(("primary", "supporting", "hidden")), help="Visibility filter. Repeat for OR semantics.")
    @click.option("--generation-id", default=None, help="Restrict to members associated with an Idea Generation Group.")
    @click.option("--decision-record-id", default=None, help="Restrict to explicitly recorded options of one Decision Record.")
    @click.option("--include-archived", is_flag=True, help="Include archived ideas and edges.")
    @click.pass_context
    def ideas_query_command(ctx: click.Context, **kwargs: Any) -> int:
        values = dict(kwargs)
        return with_context(
            ctx,
            values,
            lambda context, _request: query_research_ideas(
                context,
                env=os.environ,
                include_archived=bool(values.get("include_archived")),
                exploration_states=[str(item) for item in values.get("exploration_states", ())],
                decision_states=[str(item) for item in values.get("decision_states", ())],
                evidence_states=[str(item) for item in values.get("evidence_states", ())],
                archive_states=[str(item) for item in values.get("archive_states", ())],
                visibilities=[str(item) for item in values.get("visibilities", ())],
                generation_id=values.get("generation_id"),
                decision_record_id=values.get("decision_record_id"),
            ),
            build_request=False,
        )

    @ideas_group.command(name="graph", help="Read the canonical idea graph.")
    @_common_options
    @_topic_selection_options
    @click.option("--visibility", default="primary", show_default=True, help="Visibility to show when supporting ideas are not included.")
    @click.option("--include-supporting", is_flag=True, help="Include supporting and hidden ideas.")
    @click.pass_context
    def ideas_graph_command(ctx: click.Context, **kwargs: Any) -> int:
        values = dict(kwargs)
        return with_context(ctx, values, lambda context, _request: graph_research_ideas(context, env=os.environ, visibility=str(values.get("visibility") or "primary"), include_supporting=bool(values.get("include_supporting"))), build_request=False)

    @ideas_group.command(name="traverse", help="Traverse bounded canonical Research Idea ancestors or descendants.")
    @_common_options
    @_topic_selection_options
    @click.option("--root-idea-id", "root_idea_ids", multiple=True, required=True, help="Traversal root. Repeat for multiple roots.")
    @click.option("--direction", required=True, type=click.Choice(("ancestors", "descendants")), help="Traversal direction.")
    @click.option("--relation-kind", "relation_kinds", multiple=True, help="Eligible Idea Lineage Edge kind. Repeat as needed.")
    @click.option("--max-depth", type=click.IntRange(min=0), default=8, show_default=True, help="Maximum traversal depth.")
    @click.option("--max-nodes", type=click.IntRange(min=1), default=500, show_default=True, help="Maximum returned nodes.")
    @click.option("--max-edges", type=click.IntRange(min=0), default=1000, show_default=True, help="Maximum returned edges.")
    @click.pass_context
    def ideas_traverse_command(ctx: click.Context, **kwargs: Any) -> int:
        values = dict(kwargs)
        return with_context(
            ctx,
            values,
            lambda context, _request: traverse_research_ideas(
                context,
                env=os.environ,
                root_idea_ids=[str(item) for item in values.get("root_idea_ids", ())],
                direction=str(values["direction"]),
                relation_kinds=[str(item) for item in values.get("relation_kinds", ())],
                max_depth=int(values["max_depth"]),
                max_nodes=int(values["max_nodes"]),
                max_edges=int(values["max_edges"]),
            ),
            build_request=False,
        )

    @ideas_group.command(name="validate", help="Validate canonical idea identity, realizations, lineage, and generation groups.")
    @_common_options
    @_topic_selection_options
    @click.pass_context
    def ideas_validate_command(ctx: click.Context, **kwargs: Any) -> int:
        return with_context(ctx, dict(kwargs), lambda context, _request: validate_research_ideas(context, env=os.environ), build_request=False)

    @ideas_group.command(name="migrate-status", help="Preview or apply conservative legacy Research Idea status migration.")
    @_common_options
    @_topic_selection_options
    @click.option("--apply", "apply_migration", is_flag=True, help="Apply the previewed migration atomically.")
    @click.pass_context
    def ideas_migrate_status_command(ctx: click.Context, apply_migration: bool = False, **kwargs: Any) -> int:
        return with_context(
            ctx,
            dict(kwargs),
            lambda context, _request: migrate_research_idea_portfolio(context, env=os.environ, apply=apply_migration),
            build_request=False,
        )

    @ideas_group.command(name="import-from-record", help="Preview or apply a legacy record idea import plan.")
    @_common_options
    @_topic_selection_options
    @click.option("--apply", "apply_import", is_flag=True, help="Apply the import plan.")
    @click.argument("record_id")
    @click.pass_context
    def ideas_import_command(ctx: click.Context, record_id: str, apply_import: bool = False, **kwargs: Any) -> int:
        return with_context(ctx, dict(kwargs), lambda context, _request: import_research_ideas_from_record(context, record_id, env=os.environ, apply=apply_import), build_request=False)

    @ideas_group.command(name="migrate-kaoju-direction-set", help="Preview or apply canonical Research Ideas from one legacy Kaoju Direction Set v1.")
    @_common_options
    @_topic_selection_options
    @click.option("--apply", "apply_migration", is_flag=True, help="Apply the validated migration plan atomically.")
    @click.argument("record_id")
    @click.pass_context
    def ideas_migrate_kaoju_direction_set_command(ctx: click.Context, record_id: str, apply_migration: bool = False, **kwargs: Any) -> int:
        return with_context(ctx, dict(kwargs), lambda context, _request: migrate_legacy_kaoju_direction_set(context, record_id, env=os.environ, apply=apply_migration), build_request=False)

    @ideas_group.command(name="repair", help="Preview canonical idea repair diagnostics.")
    @_common_options
    @_topic_selection_options
    @click.option("--apply", "apply_repair", is_flag=True, help="Reserved for future deterministic repair plans.")
    @click.option("--update-payloads", is_flag=True, help="Allow explicit payload-file updates when a repair path supports them.")
    @click.pass_context
    def ideas_repair_command(ctx: click.Context, apply_repair: bool = False, update_payloads: bool = False, **kwargs: Any) -> int:
        return with_context(ctx, dict(kwargs), lambda context, _request: repair_research_ideas(context, env=os.environ, apply=apply_repair, update_payloads=update_payloads), build_request=False)


def _string_map(value: Mapping[str, object], *, field_name: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for key, item in value.items():
        if not isinstance(item, str) or not item.strip():
            raise ResearchRecordError(f"{field_name} values must be non-empty strings.", code="research_idea_steering_json_invalid")
        result[str(key)] = item
    return result


def _nested_string_map(value: Mapping[str, object], *, field_name: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for key, item in value.items():
        if not isinstance(item, Mapping):
            raise ResearchRecordError(f"{field_name} values must be JSON objects.", code="research_idea_steering_json_invalid")
        result[str(key)] = _string_map(item, field_name=field_name)
    return result
