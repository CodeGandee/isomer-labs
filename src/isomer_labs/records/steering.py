"""Atomic Research Idea steering and post-commit topic-actor dispatch service."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
import sqlite3
from typing import Any, Literal, Mapping, cast

from isomer_labs.artifact_formats import digest_json
from isomer_labs.houmao.adapter import HoumaoAdapterFacade
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.records.index import query_index_revision
from isomer_labs.runtime.records import (
    RESEARCH_IDEA_CLOSURE_REASONS,
    HandoffRecord,
    ResearchIdea,
    ResearchIdeaDecisionOption,
    ResearchIdeaDecisionOptionOutcome,
    ResearchIdeaOperation,
    ResearchIdeaStateTransition,
    RuntimeLifecycleRecord,
    _provenance_ref,
    _slug,
    utc_timestamp,
)
from isomer_labs.runtime.store import WorkspaceRuntimeStore, open_workspace_runtime


SteeringAction = Literal["explore", "explore_instead"]
SteeringGatePolicy = Literal["none", "reopen", "replace", "all"]


@dataclass(frozen=True)
class ResearchIdeaSteeringRequest:
    action: SteeringAction
    target_idea_id: str
    actor_ref: str
    idempotency_key: str
    expected_index_revision: str | None = None
    expected_states: dict[str, dict[str, str]] = field(default_factory=dict)
    replaced_idea_ids: list[str] = field(default_factory=list)
    replacement_dispositions: dict[str, str] = field(default_factory=dict)
    replacement_closure_reasons: dict[str, str] = field(default_factory=dict)
    rationale: str | None = None
    user_prompt: str | None = None
    reopen_confirmed: bool = False
    gate_policy: SteeringGatePolicy = "none"
    gate_resolution_ref: str | None = None
    agent_team_instance_id: str | None = None
    source_agent_instance_id: str | None = None
    target_agent_instance_id: str | None = None

    def normalized_input(self, topic_workspace_id: str) -> dict[str, object]:
        return {
            "topic_workspace_id": topic_workspace_id,
            "action": self.action,
            "target_idea_id": self.target_idea_id,
            "actor_ref": self.actor_ref,
            "idempotency_key": self.idempotency_key,
            "expected_index_revision": self.expected_index_revision,
            "expected_states": {key: dict(sorted(value.items())) for key, value in sorted(self.expected_states.items())},
            "replaced_idea_ids": sorted(set(self.replaced_idea_ids)),
            "replacement_dispositions": dict(sorted(self.replacement_dispositions.items())),
            "replacement_closure_reasons": dict(sorted(self.replacement_closure_reasons.items())),
            "rationale": self.rationale,
            "user_prompt": self.user_prompt,
            "reopen_confirmed": self.reopen_confirmed,
            "gate_policy": self.gate_policy,
            "gate_resolution_ref": self.gate_resolution_ref,
            "agent_team_instance_id": self.agent_team_instance_id,
            "source_agent_instance_id": self.source_agent_instance_id,
            "target_agent_instance_id": self.target_agent_instance_id,
        }


def steer_research_idea(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    request: ResearchIdeaSteeringRequest,
    dispatch: bool = True,
) -> tuple[dict[str, Any], list[Any]]:
    """Commit one steering action and then attempt adapter delivery."""

    validation = _validate_request_shape(request)
    if validation is not None:
        return validation, []
    input_payload = request.normalized_input(context.topic_workspace_id)
    input_digest = digest_json(input_payload)
    operation_id = f"idea-steering-{input_digest[:20]}"
    store, diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    if store is None:
        return _failure("steering_runtime_unavailable", "Workspace Runtime is unavailable for Research Idea steering."), diagnostics
    try:
        existing = store.get_research_idea_operation_by_idempotency_key(
            request.idempotency_key,
            topic_workspace_id=context.topic_workspace_id,
        )
        if existing is not None:
            if existing.input_digest != input_digest:
                return _conflict_payload(
                    context,
                    operation_id=existing.operation_id,
                    code="steering_idempotency_conflict",
                    message="The idempotency key is already associated with a different steering request.",
                    current_revision=_current_revision(context, env),
                    ideas=[],
                ), diagnostics
            replay = existing.result.get("response") if isinstance(existing.result.get("response"), dict) else existing.result
            return {
                **cast(dict[str, Any], replay),
                "ok": True,
                "mutated": False,
                "replayed": True,
                "operation_id": existing.operation_id,
            }, diagnostics

        store.connection.execute("BEGIN IMMEDIATE")
        try:
            current_revision = _current_revision(context, env)
            if request.expected_index_revision is not None and request.expected_index_revision != current_revision:
                store.connection.rollback()
                return _conflict_payload(
                    context,
                    operation_id=operation_id,
                    code="steering_index_revision_conflict",
                    message="The Research Idea portfolio changed after the steering action was prepared.",
                    current_revision=current_revision,
                    ideas=_selected_ideas(store, context, [request.target_idea_id, *request.replaced_idea_ids]),
                ), diagnostics

            target = store.get_research_idea(request.target_idea_id, topic_workspace_id=context.topic_workspace_id)
            if target is None:
                store.connection.rollback()
                return _failure("steering_target_missing", f"Research Idea is not available: {request.target_idea_id}"), diagnostics
            replaced_ids = list(dict.fromkeys(request.replaced_idea_ids))
            replacements = [store.get_research_idea(idea_id, topic_workspace_id=context.topic_workspace_id) for idea_id in replaced_ids]
            if any(idea is None for idea in replacements):
                store.connection.rollback()
                missing = [idea_id for idea_id, idea in zip(replaced_ids, replacements, strict=True) if idea is None]
                return _failure("steering_replacement_missing", f"Replacement Research Idea is unavailable: {', '.join(missing)}"), diagnostics
            replacement_records = cast(list[ResearchIdea], replacements)

            state_conflict = _expected_state_conflict(request, [target, *replacement_records])
            if state_conflict is not None:
                store.connection.rollback()
                return _conflict_payload(
                    context,
                    operation_id=operation_id,
                    code="steering_expected_state_conflict",
                    message=state_conflict,
                    current_revision=current_revision,
                    ideas=[item.to_json() for item in [target, *replacement_records]],
                ), diagnostics
            if request.action == "explore_instead" and any(item.decision_state != "selected" for item in replacement_records):
                store.connection.rollback()
                return _conflict_payload(
                    context,
                    operation_id=operation_id,
                    code="steering_replacement_not_selected",
                    message="Explore instead can replace only the exact Research Ideas currently selected in canonical state.",
                    current_revision=current_revision,
                    ideas=[item.to_json() for item in replacement_records],
                ), diagnostics

            reopening_required = target.decision_state in {"closed", "deferred"}
            if reopening_required and (not request.reopen_confirmed or not _present(request.rationale)):
                store.connection.rollback()
                return _gate_payload(
                    context,
                    operation_id,
                    "steering_reopen_confirmation_required",
                    "A closed or deferred Research Idea requires an explicit reopening confirmation and rationale.",
                    target,
                    current_revision,
                ), diagnostics
            gate_reason = _required_gate_reason(request, reopening_required=reopening_required)
            if gate_reason is not None and not _present(request.gate_resolution_ref):
                store.connection.rollback()
                return _gate_payload(
                    context,
                    operation_id,
                    "steering_gate_required",
                    gate_reason,
                    target,
                    current_revision,
                ), diagnostics

            now = utc_timestamp()
            decision_record_id = f"decision-{operation_id}" if request.action == "explore_instead" or reopening_required else None
            inquiry_id = f"research-inquiry-{operation_id}"
            task_id = f"research-task-{operation_id}"
            provenance_id = f"provenance:{operation_id}"
            handoff_id = f"handoff-{operation_id}"
            target_actor_ref = request.target_agent_instance_id or "topic-research-actor:pending"
            lifecycle_records = _steering_lifecycle_records(
                context,
                request=request,
                target=target,
                replacements=replacement_records,
                operation_id=operation_id,
                decision_record_id=decision_record_id,
                inquiry_id=inquiry_id,
                task_id=task_id,
                provenance_id=provenance_id,
                now=now,
            )
            for record in lifecycle_records:
                store.upsert_lifecycle_record(record)
            handoff = HandoffRecord(
                id=handoff_id,
                research_topic_id=context.research_topic.id,
                topic_workspace_id=context.topic_workspace_id,
                source_actor_ref=request.actor_ref,
                target_actor_ref=target_actor_ref,
                research_task_id=task_id,
                status="draft",
                created_at=now,
                updated_at=now,
                expected_output_refs=[f"research-idea:{target.idea_id}"],
                provenance_refs=[_provenance_ref("research-idea-steering-handoff", handoff_id)],
            )
            store.record_handoff(handoff)
            transitions = _steering_transitions(
                context,
                request=request,
                target=target,
                replacements=replacement_records,
                operation_id=operation_id,
                decision_record_id=decision_record_id,
                task_id=task_id,
                provenance_id=provenance_id,
                now=now,
            )
            options = _steering_options(
                context,
                request=request,
                target=target,
                replacements=replacement_records,
                operation_id=operation_id,
                decision_record_id=decision_record_id,
                now=now,
            )
            canonical_result = {
                "status": "accepted",
                "operation_id": operation_id,
                "decision_record_ref": decision_record_id,
                "research_inquiry_ref": inquiry_id,
                "research_task_ref": task_id,
                "provenance_record_ref": provenance_id,
                "handoff_ref": handoff_id,
                "transition_refs": [item.id for item in transitions],
                "decision_option_refs": [item.id for item in options],
                "dispatch_status": "planned",
                "dispatch_retry_ref": handoff_id,
            }
            operation = ResearchIdeaOperation(
                id=f"idea-operation-{_slug(context.topic_workspace_id)}-{_slug(operation_id)}",
                research_topic_id=context.research_topic.id,
                topic_workspace_id=context.topic_workspace_id,
                operation_id=operation_id,
                idempotency_key=request.idempotency_key,
                action_kind=f"ideas.steer.{request.action}",
                input_digest=input_digest,
                status="committed",
                result={"response": canonical_result},
                actor_ref=request.actor_ref,
                metadata={"gate_resolution_ref": request.gate_resolution_ref, "handoff_id": handoff_id},
                created_at=now,
                updated_at=now,
                provenance_refs=[_provenance_ref("research-idea-operation", operation_id)],
            )
            store.apply_research_idea_mutation(
                transitions=transitions,
                decision_options=options,
                operation=operation,
                manage_transaction=False,
            )
            store.connection.commit()
        except Exception:
            store.connection.rollback()
            raise

        resulting_ideas = _selected_ideas(store, context, [target.idea_id, *replaced_ids])
        prompt = compose_steering_prompt(
            store,
            request=request,
            target=target,
            decision_record_id=decision_record_id,
            inquiry_id=inquiry_id,
            task_id=task_id,
        )
        dispatch_result = _dispatch_after_commit(
            context,
            store,
            env=env,
            request=request,
            handoff=handoff,
            task_id=task_id,
            prompt=prompt,
            dispatch=dispatch,
        )
        new_revision = _current_revision(context, env)
        response = {
            "ok": True,
            "mutated": True,
            "replayed": False,
            "topic_id": context.research_topic.id,
            "topic_workspace_id": context.topic_workspace_id,
            **canonical_result,
            "canonical_accepted": True,
            "resulting_ideas": resulting_ideas,
            "new_index_revision": new_revision,
            "pending_index_revision": new_revision is None,
            "dispatch_status": dispatch_result["status"],
            "dispatch": dispatch_result,
            "planned_prompt": prompt,
            "diagnostics": dispatch_result["diagnostics"],
        }
        with store.connection:
            current_operation = store.get_research_idea_operation(operation_id, topic_workspace_id=context.topic_workspace_id)
            if current_operation is not None:
                store.upsert_research_idea_operation(
                    replace(
                        current_operation,
                        result={"response": response},
                        updated_at=utc_timestamp(),
                    )
                )
        return response, diagnostics
    except (ValueError, sqlite3.Error) as exc:
        return _failure("steering_transaction_failed", f"Research Idea steering rolled back: {exc}"), diagnostics
    finally:
        store.close()


def compose_steering_prompt(
    store: WorkspaceRuntimeStore,
    *,
    request: ResearchIdeaSteeringRequest,
    target: ResearchIdea,
    decision_record_id: str | None,
    inquiry_id: str,
    task_id: str,
) -> str:
    realizations = store.list_research_idea_realizations(topic_workspace_id=target.topic_workspace_id, idea_id=target.idea_id)
    latest_realizations = [item.to_json() for item in realizations if item.latest]
    context_payload = {
        "action": request.action,
        "idea_id": target.idea_id,
        "display_key": target.display_key,
        "title": target.title,
        "summary": target.summary,
        "latest_idea_realizations": latest_realizations,
        "decision_record_ref": decision_record_id,
        "research_inquiry_ref": inquiry_id,
        "research_task_ref": task_id,
        "replaced_idea_ids": sorted(set(request.replaced_idea_ids)),
        "user_prompt": request.user_prompt or "Explore the named Research Idea within the bounded Research Task.",
    }
    return "Project Operator Research Idea steering instruction. Use the exact durable context below; do not infer another idea from a skill name or generated Markdown.\n\n" + _pretty_json(context_payload)


def _validate_request_shape(request: ResearchIdeaSteeringRequest) -> dict[str, Any] | None:
    if not _present(request.target_idea_id) or not _present(request.actor_ref) or not _present(request.idempotency_key):
        return _failure("steering_request_invalid", "Research Idea steering requires target_idea_id, actor_ref, and idempotency_key.")
    if request.action == "explore_instead" and not request.replaced_idea_ids:
        return _failure("steering_replacements_required", "Explore instead requires the exact selected Research Idea ids to replace.")
    if request.target_idea_id in request.replaced_idea_ids:
        return _failure("steering_target_replaced", "The target Research Idea cannot also be named as a replaced idea.")
    if request.action == "explore_instead" and not _present(request.rationale):
        return _failure("steering_rationale_required", "Explore instead requires an actor-authored rationale.")
    replaced_ids = set(request.replaced_idea_ids)
    unknown_disposition_ids = sorted(set(request.replacement_dispositions) - replaced_ids)
    if unknown_disposition_ids:
        return _failure("steering_replacement_disposition_unknown", f"Replacement dispositions name ideas outside the exact replacement set: {', '.join(unknown_disposition_ids)}")
    unknown_closure_reason_ids = sorted(set(request.replacement_closure_reasons) - replaced_ids)
    if unknown_closure_reason_ids:
        return _failure("steering_replacement_closure_reason_unknown", f"Replacement closure reasons name ideas outside the exact replacement set: {', '.join(unknown_closure_reason_ids)}")
    invalid_dispositions = sorted(set(request.replacement_dispositions.values()) - {"deferred", "closed"})
    if invalid_dispositions:
        return _failure("steering_disposition_unsupported", f"Unsupported replacement disposition: {', '.join(invalid_dispositions)}")
    invalid_reasons = sorted(set(request.replacement_closure_reasons.values()) - set(RESEARCH_IDEA_CLOSURE_REASONS))
    if invalid_reasons:
        return _failure("steering_closure_reason_unsupported", f"Unsupported closure reason: {', '.join(invalid_reasons)}")
    missing_closure_reasons = sorted(
        idea_id
        for idea_id, disposition in request.replacement_dispositions.items()
        if disposition == "closed" and not _present(request.replacement_closure_reasons.get(idea_id))
    )
    if missing_closure_reasons:
        return _failure("steering_closure_reason_required", f"Closed replacement ideas require canonical closure reasons: {', '.join(missing_closure_reasons)}")
    return None


def _steering_lifecycle_records(
    context: EffectiveTopicContext,
    *,
    request: ResearchIdeaSteeringRequest,
    target: ResearchIdea,
    replacements: list[ResearchIdea],
    operation_id: str,
    decision_record_id: str | None,
    inquiry_id: str,
    task_id: str,
    provenance_id: str,
    now: str,
) -> list[RuntimeLifecycleRecord]:
    common_refs = {"operation_id": operation_id, "research_idea_id": target.idea_id}
    records = [
        RuntimeLifecycleRecord(
            id=inquiry_id,
            record_kind="research_inquiry",
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            status="active",
            lifecycle_refs=common_refs,
            transition_metadata={"title": f"Explore {target.display_key or target.idea_id}: {target.title}", "summary": target.summary},
            created_at=now,
            updated_at=now,
            provenance_refs=[_provenance_ref("research-idea-steering-inquiry", inquiry_id)],
        ),
        RuntimeLifecycleRecord(
            id=task_id,
            record_kind="research_task",
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            status="planned",
            lifecycle_refs={**common_refs, "research_inquiry_id": inquiry_id},
            transition_metadata={"bounded_action": request.action, "user_prompt": request.user_prompt or ""},
            created_at=now,
            updated_at=now,
            provenance_refs=[_provenance_ref("research-idea-steering-task", task_id)],
        ),
        RuntimeLifecycleRecord(
            id=provenance_id,
            record_kind="provenance_record",
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            status="complete",
            lifecycle_refs={**common_refs, "research_inquiry_id": inquiry_id, "research_task_id": task_id},
            transition_metadata={"actor_ref": request.actor_ref, "action": request.action, "idempotency_key": request.idempotency_key},
            created_at=now,
            updated_at=now,
            provenance_refs=[_provenance_ref("research-idea-steering", operation_id)],
        ),
    ]
    if decision_record_id is not None:
        records.append(
            RuntimeLifecycleRecord(
                id=decision_record_id,
                record_kind="decision_record",
                research_topic_id=context.research_topic.id,
                topic_workspace_id=context.topic_workspace_id,
                status="complete",
                lifecycle_refs={**common_refs, "research_task_id": task_id},
                transition_metadata={
                    "action": request.action,
                    "rationale": request.rationale or "Reopen the target Research Idea for focused exploration.",
                    "target_idea_id": target.idea_id,
                    "replaced_idea_ids": ",".join(item.idea_id for item in replacements),
                    "option_set_complete": True,
                },
                created_at=now,
                updated_at=now,
                provenance_refs=[_provenance_ref("research-idea-steering-decision", decision_record_id)],
            )
        )
    return records


def _steering_transitions(
    context: EffectiveTopicContext,
    *,
    request: ResearchIdeaSteeringRequest,
    target: ResearchIdea,
    replacements: list[ResearchIdea],
    operation_id: str,
    decision_record_id: str | None,
    task_id: str,
    provenance_id: str,
    now: str,
) -> list[ResearchIdeaStateTransition]:
    transitions: list[ResearchIdeaStateTransition] = []

    def add(idea: ResearchIdea, facet: str, previous: str, next_value: str, *, reason_code: str | None = None) -> None:
        transition_id = f"idea-state-transition-{digest_json({'operation_id': operation_id, 'idea_id': idea.idea_id, 'facet': facet, 'previous': previous, 'next': next_value})[:20]}"
        transitions.append(
            ResearchIdeaStateTransition(
                id=transition_id,
                research_topic_id=context.research_topic.id,
                topic_workspace_id=context.topic_workspace_id,
                idea_id=idea.idea_id,
                facet=cast(Any, facet),
                previous_value=previous,
                next_value=next_value,
                operation_id=operation_id,
                actor_ref=request.actor_ref,
                rationale=request.rationale or f"Explore {target.display_key or target.idea_id} through the named Research Task.",
                reason_code=reason_code,
                decision_record_id=decision_record_id if facet == "decision_state" else None,
                gate_id=request.gate_resolution_ref,
                research_task_id=task_id,
                provenance_record_refs=[provenance_id],
                metadata={"steering_action": request.action},
                transitioned_at=now,
                provenance_refs=[_provenance_ref("research-idea-steering-transition", transition_id)],
            )
        )

    target_decision = target.decision_state
    if target_decision in {"closed", "deferred"}:
        add(target, "decision_state", target_decision, "open", reason_code="reopened_for_exploration")
        target_decision = "open"
    if request.action == "explore_instead" and target_decision != "selected":
        add(target, "decision_state", target_decision, "selected")
    if target.exploration_state != "exploring":
        add(target, "exploration_state", target.exploration_state, "exploring")
    if request.action == "explore_instead":
        for idea in replacements:
            disposition = request.replacement_dispositions.get(idea.idea_id, "deferred")
            closure_reason = request.replacement_closure_reasons.get(idea.idea_id)
            add(idea, "decision_state", idea.decision_state, disposition, reason_code=closure_reason)
    return transitions


def _steering_options(
    context: EffectiveTopicContext,
    *,
    request: ResearchIdeaSteeringRequest,
    target: ResearchIdea,
    replacements: list[ResearchIdea],
    operation_id: str,
    decision_record_id: str | None,
    now: str,
) -> list[ResearchIdeaDecisionOption]:
    if decision_record_id is None:
        return []
    options: list[ResearchIdeaDecisionOption] = []
    option_specs: list[tuple[ResearchIdea, ResearchIdeaDecisionOptionOutcome]] = [(target, "selected" if request.action == "explore_instead" else "reopened")]
    option_specs.extend((idea, cast(ResearchIdeaDecisionOptionOutcome, request.replacement_dispositions.get(idea.idea_id, "deferred"))) for idea in replacements)
    for ordinal, (idea, outcome) in enumerate(option_specs):
        option_id = f"idea-decision-option-{digest_json({'decision_record_id': decision_record_id, 'idea_id': idea.idea_id})[:20]}"
        options.append(
            ResearchIdeaDecisionOption(
                id=option_id,
                research_topic_id=context.research_topic.id,
                topic_workspace_id=context.topic_workspace_id,
                decision_record_id=decision_record_id,
                idea_id=idea.idea_id,
                outcome=outcome,
                operation_id=operation_id,
                option_role="target" if idea.idea_id == target.idea_id else "replaced_selection",
                ordinal=ordinal,
                rationale=request.rationale,
                consequence="Focused exploration starts." if idea.idea_id == target.idea_id else f"Decision state becomes {outcome}.",
                actor_ref=request.actor_ref,
                supporting_refs=[],
                metadata={"option_set_complete": True, "steering_action": request.action},
                created_at=now,
                updated_at=now,
                provenance_refs=[_provenance_ref("research-idea-steering-option", option_id)],
            )
        )
    return options


def _dispatch_after_commit(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    *,
    env: Mapping[str, str],
    request: ResearchIdeaSteeringRequest,
    handoff: HandoffRecord,
    task_id: str,
    prompt: str,
    dispatch: bool,
) -> dict[str, Any]:
    if not dispatch:
        return {"status": "pending", "handoff_ref": handoff.id, "retry_ref": handoff.id, "diagnostics": []}
    routing = _resolve_dispatch_routing(store, request)
    if routing is None:
        return {
            "status": "pending",
            "handoff_ref": handoff.id,
            "retry_ref": handoff.id,
            "diagnostics": [_diag("warning", "steering_dispatch_pending", "Canonical steering was accepted, but no unique live topic research actor route is configured.")],
        }
    team_id, source_id, target_id = routing
    summary = store.get_agent_team_instance_summary(team_id)
    if summary is None:
        return _mark_dispatch_blocked(store, handoff, "Configured Agent Team Instance is unavailable.")
    facade = HoumaoAdapterFacade(env=env)
    try:
        with store.connection:
            result = facade.dispatch_handoff(
                context=context,
                store=store,
                summary=summary,
                source_agent_instance_id=source_id,
                target_agent_instance_id=target_id,
                message=prompt,
                run_id=None,
                research_task_id=task_id,
                expected_output_refs=handoff.expected_output_refs,
                completion_watcher_contract_refs=[],
                actor_ref=request.actor_ref,
            )
        if result.status == "sent":
            with store.connection:
                store.record_handoff(replace(handoff, target_actor_ref=target_id, agent_team_instance_id=team_id, status="sent", updated_at=utc_timestamp()))
            return {"status": "accepted", "handoff_ref": handoff.id, "adapter_result": result.to_json(), "retry_ref": handoff.id, "diagnostics": [item.to_json() for item in result.diagnostics]}
        return _mark_dispatch_blocked(store, handoff, "The configured topic research actor adapter did not accept the prompt.", extra=[item.to_json() for item in result.diagnostics])
    except Exception as exc:
        return _mark_dispatch_blocked(store, handoff, f"Topic research actor dispatch failed after canonical commit: {exc}")


def _resolve_dispatch_routing(store: WorkspaceRuntimeStore, request: ResearchIdeaSteeringRequest) -> tuple[str, str, str] | None:
    teams = store.list_agent_team_instances()
    if request.agent_team_instance_id is not None:
        team_id = request.agent_team_instance_id
    else:
        active = [team for team in teams if team.status in {"ready", "running", "active"}]
        if len(active) != 1:
            return None
        team_id = active[0].id
    summary = store.get_agent_team_instance_summary(team_id)
    if summary is None:
        return None
    source_id = request.source_agent_instance_id
    if source_id is None:
        source = next((agent for agent in summary.agent_instances if "operator" in agent.agent_role_id.lower()), None)
        source_id = source.id if source is not None else None
    target_id = request.target_agent_instance_id
    if target_id is None:
        candidates = [agent for agent in summary.agent_instances if any(token in agent.agent_role_id.lower() for token in ("topic-master", "topic-lead", "research-lead", "research-master"))]
        target_id = candidates[0].id if len(candidates) == 1 else None
    if source_id is None or target_id is None:
        return None
    return team_id, source_id, target_id


def _mark_dispatch_blocked(store: WorkspaceRuntimeStore, handoff: HandoffRecord, message: str, *, extra: list[dict[str, object]] | None = None) -> dict[str, Any]:
    with store.connection:
        store.record_handoff(replace(handoff, status="blocked", updated_at=utc_timestamp()))
    return {
        "status": "blocked",
        "handoff_ref": handoff.id,
        "retry_ref": handoff.id,
        "diagnostics": [_diag("error", "steering_dispatch_blocked", message), *(extra or [])],
    }


def _required_gate_reason(request: ResearchIdeaSteeringRequest, *, reopening_required: bool) -> str | None:
    if request.gate_policy == "all":
        return "Configured Gate policy requires resolution before this steering action."
    if request.gate_policy == "reopen" and reopening_required:
        return "Configured Gate policy requires resolution before reopening this Research Idea."
    if request.gate_policy == "replace" and request.action == "explore_instead":
        return "Configured Gate policy requires resolution before replacing selected Research Ideas."
    return None


def _expected_state_conflict(request: ResearchIdeaSteeringRequest, ideas: list[ResearchIdea]) -> str | None:
    by_id = {idea.idea_id: idea for idea in ideas}
    for idea_id, expected in request.expected_states.items():
        idea = by_id.get(idea_id)
        if idea is None:
            return f"Expected-state Research Idea is unavailable: {idea_id}"
        actual = idea.to_json()
        for facet, expected_value in expected.items():
            if str(actual.get(facet)) != expected_value:
                return f"Research Idea {idea_id} has {facet}={actual.get(facet)}, not expected {expected_value}."
    return None


def _selected_ideas(store: WorkspaceRuntimeStore, context: EffectiveTopicContext, idea_ids: list[str]) -> list[dict[str, object]]:
    selected: list[dict[str, object]] = []
    for idea_id in dict.fromkeys(idea_ids):
        idea = store.get_research_idea(idea_id, topic_workspace_id=context.topic_workspace_id)
        if idea is not None:
            selected.append(idea.to_json())
    return selected


def _current_revision(context: EffectiveTopicContext, env: Mapping[str, str]) -> str | None:
    payload, _diagnostics = query_index_revision(context, env=env)
    value = payload.get("index_revision")
    return str(value) if value is not None else None


def _conflict_payload(
    context: EffectiveTopicContext,
    *,
    operation_id: str,
    code: str,
    message: str,
    current_revision: str | None,
    ideas: list[dict[str, object]],
) -> dict[str, Any]:
    return {
        "ok": False,
        "mutated": False,
        "status": "conflict",
        "operation_id": operation_id,
        "topic_id": context.research_topic.id,
        "current_index_revision": current_revision,
        "current_ideas": ideas,
        "error": {"code": code, "message": message},
        "diagnostics": [_diag("warning", code, message)],
    }


def _gate_payload(
    context: EffectiveTopicContext,
    operation_id: str,
    code: str,
    message: str,
    target: ResearchIdea,
    current_revision: str | None,
) -> dict[str, Any]:
    return {
        "ok": False,
        "mutated": False,
        "status": "gate_required",
        "operation_id": operation_id,
        "topic_id": context.research_topic.id,
        "gate": {"required": True, "suggested_gate_id": f"gate-{operation_id}", "reason": message},
        "current_index_revision": current_revision,
        "current_ideas": [target.to_json()],
        "error": {"code": code, "message": message},
        "diagnostics": [_diag("warning", code, message)],
    }


def _failure(code: str, message: str) -> dict[str, Any]:
    return {
        "ok": False,
        "mutated": False,
        "status": "blocked",
        "error": {"code": code, "message": message},
        "diagnostics": [_diag("error", code, message)],
    }


def _diag(severity: str, code: str, message: str, **details: object) -> dict[str, object]:
    payload: dict[str, object] = {"severity": severity, "code": code, "message": message}
    payload.update(details)
    return payload


def _pretty_json(value: object) -> str:
    import json

    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)


def _present(value: str | None) -> bool:
    return bool(value and value.strip())
