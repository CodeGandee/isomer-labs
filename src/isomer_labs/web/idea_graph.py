"""Canonical Research Idea graph projection helpers."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .idea_portfolio import classification_fields


def idea_display_key_diagnostics(ideas: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Report canonical ideas whose GUI display keys need repair."""

    diagnostics: list[dict[str, Any]] = []
    for idea in ideas:
        idea_id = str(idea.get("idea_id") or idea.get("id") or "").strip()
        display_key = str(idea.get("display_key") or "").strip()
        if not idea_id:
            continue
        if not display_key:
            diagnostics.append(_diag("warning", "idea_display_key_missing", f"Research Idea has no GUI display key: {idea_id}", idea_id=idea_id))
        elif display_key.startswith("I") and not display_key.startswith("I-"):
            diagnostics.append(
                _diag(
                    "warning",
                    "idea_display_key_legacy_format",
                    f"Research Idea display key needs explicit migration: {display_key}",
                    idea_id=idea_id,
                    display_key=display_key,
                )
            )
    return diagnostics


def canonical_idea_nodes(
    ideas: list[dict[str, Any]],
    realizations: list[dict[str, Any]],
    *,
    topic_id: str,
    include_secondary: bool,
    transitions: list[dict[str, Any]] | None = None,
    decision_options: list[dict[str, Any]] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    by_idea: dict[str, list[dict[str, Any]]] = {}
    for realization in realizations:
        by_idea.setdefault(str(realization.get("idea_id") or ""), []).append(realization)
    transitions_by_idea: dict[str, list[dict[str, Any]]] = {}
    for transition in transitions or []:
        transitions_by_idea.setdefault(str(transition.get("idea_id") or ""), []).append(transition)
    options_by_idea: dict[str, list[dict[str, Any]]] = {}
    for option in decision_options or []:
        options_by_idea.setdefault(str(option.get("idea_id") or ""), []).append(option)
    nodes: list[dict[str, Any]] = []
    node_ids: dict[str, str] = {}
    for idea in ideas:
        idea_id = str(idea.get("idea_id") or idea.get("id") or "")
        if not idea_id:
            continue
        history = by_idea.get(idea_id, [])
        idea_transitions = sorted(transitions_by_idea.get(idea_id, []), key=lambda item: (str(item.get("transitioned_at") or ""), str(item.get("id") or "")))
        idea_options = sorted(options_by_idea.get(idea_id, []), key=lambda item: (str(item.get("created_at") or ""), item["ordinal"] if isinstance(item.get("ordinal"), int) else 2**31, str(item.get("id") or "")))
        latest = next((item for item in history if item.get("latest")), history[0] if history else {})
        record_id = str(latest.get("record_id") or idea.get("source_record_id") or "")
        node_id = f"idea:{idea_id}"
        decision_state = str(idea.get("decision_state") or "unknown")
        exploration_state = str(idea.get("exploration_state") or "unknown")
        evidence_state = str(idea.get("evidence_state") or "unknown")
        archive_state = str(idea.get("archive_state") or "active")
        visibility = str(idea.get("visibility") or "primary")
        node = _node(
            node_id=node_id,
            record_id=record_id,
            title=str(idea.get("title") or idea_id),
            summary=idea.get("summary"),
            status=idea.get("status"),
            selected=decision_state == "selected",
            created_at=idea.get("created_at"),
            updated_at=idea.get("updated_at"),
            source={
                "idea_id": idea_id,
                "display_key": idea.get("display_key"),
                "aliases": idea.get("aliases") or [],
                "family": idea.get("family"),
                "source_record_id": idea.get("source_record_id"),
                "source_json_path": idea.get("source_json_path"),
                "realization_count": len(history),
                "latest_realization": latest or None,
            },
            topic_id=topic_id,
            renderer_hints={
                "card_variant": "idea",
                "cluster": idea.get("family"),
                "color": _idea_color(decision_state, evidence_state=evidence_state, archive_state=archive_state),
                "size": 18 if visibility == "primary" else 11,
            },
        )
        node["idea_id"] = idea_id
        node["display_key"] = idea.get("display_key")
        node["exploration_state"] = exploration_state
        node["decision_state"] = decision_state
        node["evidence_state"] = evidence_state
        node["archive_state"] = archive_state
        node["visibility"] = visibility
        node["backend_selected"] = decision_state == "selected"
        node["needs_classification"] = classification_fields(node)
        node["transition_refs"] = [str(item.get("id")) for item in idea_transitions if item.get("id")]
        node["decision_record_ids"] = sorted({str(item.get("decision_record_id")) for item in [*idea_transitions, *idea_options] if item.get("decision_record_id")})
        node["generation_ids"] = sorted({str(item.get("generation_id")) for item in idea_options if item.get("generation_id")})
        node["decision_summary"] = _decision_summary(idea_transitions, idea_options, decision_state=decision_state)
        node["steering_eligibility"] = {
            "eligible": visibility != "hidden" and archive_state == "active",
            "reopening_required": decision_state in {"deferred", "closed"},
        }
        node["detail_refs"] = {
            **node["detail_refs"],
            "idea_detail": f"/api/topics/{topic_id}/ideas/{idea_id}",
            "decision_context": f"/api/topics/{topic_id}/ideas/{idea_id}/decisions",
            "ancestry": f"/api/topics/{topic_id}/ideas/traverse?root_idea_id={idea_id}&direction=ancestors",
            "descendants": f"/api/topics/{topic_id}/ideas/traverse?root_idea_id={idea_id}&direction=descendants",
            "latest_record_detail": f"/api/topics/{topic_id}/records/{record_id}" if record_id else None,
        }
        nodes.append(node)
        node_ids[idea_id] = node_id
        if record_id:
            node_ids.setdefault(record_id, node_id)
    return nodes, node_ids


def canonical_idea_edges(
    rows: list[dict[str, Any]],
    node_ids: Mapping[str, str],
    *,
    relation_kind: str | None,
    diagnostics: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    accepted = _split_filter(relation_kind)
    edges: list[dict[str, Any]] = []
    skipped = 0
    for row in rows:
        lineage_kind = str(row.get("lineage_kind") or "")
        if accepted and lineage_kind not in accepted:
            continue
        source = node_ids.get(str(row.get("parent_idea_id") or ""))
        target = node_ids.get(str(row.get("child_idea_id") or ""))
        if source is None or target is None:
            skipped += 1
            continue
        edges.append(
            {
                "id": str(row.get("id") or f"{source}->{target}:{lineage_kind}"),
                "source": source,
                "target": target,
                "relation_kind": lineage_kind,
                "canonical": True,
                "lineage_kind": lineage_kind,
                "generation_id": row.get("generation_id"),
                "status": row.get("status"),
                "rationale": row.get("rationale"),
                "confidence": row.get("confidence"),
                "source_classification": "canonical-idea-lineage",
                "source_record_refs": [row.get("child_idea_id"), row.get("parent_idea_id")],
                "metadata": row.get("metadata") or {},
            }
        )
    if skipped:
        diagnostics.append(_diag("info", "canonical_idea_edges_outside_scope", f"{skipped} canonical idea edges were outside the selected graph scope."))
    return edges


def canonical_idea_groups(
    nodes: list[dict[str, Any]],
    graph_edges: list[dict[str, Any]],
    groups: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    nodes_by_idea = {str(node.get("idea_id") or "").strip(): str(node["id"]) for node in nodes if node.get("idea_id")}
    for group in groups:
        metadata = group.get("metadata") if isinstance(group.get("metadata"), Mapping) else {}
        raw_parent_ids = metadata.get("parent_idea_ids") if isinstance(metadata, Mapping) else None
        parent_ids = [nodes_by_idea[str(item)] for item in raw_parent_ids if str(item) in nodes_by_idea] if isinstance(raw_parent_ids, list) else []
        edge_nodes = sorted({str(edge["source"]) for edge in graph_edges if edge.get("generation_id") == group.get("id")} | {str(edge["target"]) for edge in graph_edges if edge.get("generation_id") == group.get("id")})
        node_ids = sorted(set(parent_ids + edge_nodes))
        if not node_ids:
            continue
        result.append(
            {
                "id": f"idea-generation:{group.get('id')}",
                "group_kind": "idea_generation_group",
                "title": f"Idea generation {group.get('id')}",
                "purpose": group.get("purpose") or "Sibling or alternative Research Ideas produced from the same idea pass.",
                "parent_set_digest": group.get("parent_set_digest"),
                "node_ids": node_ids,
                "diagnostics": [],
            }
        )
    return result


def _node(
    *,
    node_id: str,
    record_id: str,
    title: str,
    summary: Any,
    status: Any,
    selected: bool | None,
    created_at: Any,
    updated_at: Any,
    source: Mapping[str, Any],
    topic_id: str,
    renderer_hints: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "id": node_id,
        "record_id": record_id,
        "material_kind": "idea",
        "density_class": "sparse",
        "title": title,
        "summary": summary,
        "status": status,
        "selected": selected,
        "producer": None,
        "skill": None,
        "created_at": created_at,
        "updated_at": updated_at,
        "source": dict(source),
        "detail_refs": {
            "record_detail": f"/api/topics/{topic_id}/records/{record_id}",
            "rendered_markdown": f"/api/topics/{topic_id}/records/{record_id}/render",
            "files": f"/api/topics/{topic_id}/records/{record_id}/files",
            "facets": f"/api/topics/{topic_id}/records/{record_id}/facets",
            "lineage": f"/api/topics/{topic_id}/records/{record_id}/lineage",
            "siblings": f"/api/topics/{topic_id}/records/{record_id}/siblings",
        },
        "renderer_hints": dict(renderer_hints),
    }


def _decision_summary(
    transitions: list[dict[str, Any]],
    options: list[dict[str, Any]],
    *,
    decision_state: str,
) -> dict[str, Any]:
    decision_transitions = [item for item in transitions if item.get("facet") == "decision_state"]
    latest_transition = decision_transitions[-1] if decision_transitions else None
    latest_option = options[-1] if options else None
    latest_decision_id = None
    if latest_transition is not None:
        latest_decision_id = latest_transition.get("decision_record_id")
    if latest_decision_id is None and latest_option is not None:
        latest_decision_id = latest_option.get("decision_record_id")
    return {
        "decision_count": len({str(item.get("decision_record_id")) for item in [*transitions, *options] if item.get("decision_record_id")}),
        "option_count": len(options),
        "latest_decision_record_id": latest_decision_id,
        "latest_outcome": latest_option.get("outcome") if latest_option is not None else None,
        "current_decision_state": decision_state,
        "reason_code": latest_transition.get("reason_code") if latest_transition is not None else None,
        "rationale": latest_transition.get("rationale") if latest_transition is not None else (latest_option.get("rationale") if latest_option is not None else None),
        "actor_ref": latest_transition.get("actor_ref") if latest_transition is not None else (latest_option.get("actor_ref") if latest_option is not None else None),
        "decided_at": latest_transition.get("transitioned_at") if latest_transition is not None else (latest_option.get("created_at") if latest_option is not None else None),
        "reopen_count": sum(1 for item in decision_transitions if item.get("previous_value") in {"closed", "deferred"} and item.get("next_value") in {"open", "shortlisted", "selected"}),
    }


def _idea_color(decision_state: str, *, evidence_state: str, archive_state: str) -> str:
    if archive_state == "archived":
        return "#6b7280"
    if decision_state == "closed":
        return "#991b1b"
    if decision_state == "deferred":
        return "#a16207"
    if decision_state == "selected":
        return "#166534"
    if evidence_state == "refuted":
        return "#b91c1c"
    if evidence_state == "supported":
        return "#2563eb"
    if decision_state in {"open", "shortlisted"}:
        return "#2b6cb0"
    return "#64748b"


def _split_filter(value: str | None) -> set[str]:
    if value is None or not value.strip():
        return set()
    return {item.strip() for item in value.split(",") if item.strip()}


def _diag(severity: str, code: str, message: str, **details: Any) -> dict[str, Any]:
    data: dict[str, Any] = {"severity": severity, "code": code, "message": message}
    data.update(details)
    return data
