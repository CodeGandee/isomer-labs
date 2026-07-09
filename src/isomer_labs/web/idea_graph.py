"""Canonical Research Idea graph projection helpers."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def canonical_idea_nodes(
    ideas: list[dict[str, Any]],
    realizations: list[dict[str, Any]],
    *,
    topic_id: str,
    include_secondary: bool,
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    by_idea: dict[str, list[dict[str, Any]]] = {}
    for realization in realizations:
        by_idea.setdefault(str(realization.get("idea_id") or ""), []).append(realization)
    nodes: list[dict[str, Any]] = []
    node_ids: dict[str, str] = {}
    for idea in ideas:
        if not include_secondary and str(idea.get("visibility") or "primary") != "primary":
            continue
        idea_id = str(idea.get("idea_id") or idea.get("id") or "")
        if not idea_id:
            continue
        history = by_idea.get(idea_id, [])
        latest = next((item for item in history if item.get("latest")), history[0] if history else {})
        record_id = str(latest.get("record_id") or idea.get("source_record_id") or "")
        node_id = f"idea:{idea_id}"
        node = _node(
            node_id=node_id,
            record_id=record_id,
            title=str(idea.get("title") or idea_id),
            summary=idea.get("summary"),
            status=idea.get("status"),
            selected=str(idea.get("status") or "") == "selected",
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
                "color": _idea_color(str(idea.get("status") or "")),
                "size": 18 if str(idea.get("visibility") or "") == "primary" else 11,
            },
        )
        node["idea_id"] = idea_id
        node["display_key"] = idea.get("display_key")
        node["visibility"] = idea.get("visibility")
        node["realizations"] = history
        node["detail_refs"] = {
            **node["detail_refs"],
            "idea_detail": f"/api/topics/{topic_id}/ideas/{idea_id}",
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


def _idea_color(status: str) -> str:
    return {
        "selected": "#166534",
        "active": "#0f766e",
        "supported": "#2563eb",
        "candidate": "#2b6cb0",
        "raw": "#64748b",
        "deferred": "#a16207",
        "rejected": "#991b1b",
        "refuted": "#991b1b",
        "superseded": "#6b7280",
    }.get(status, "#64748b")


def _split_filter(value: str | None) -> set[str]:
    if value is None or not value.strip():
        return set()
    return {item.strip() for item in value.split(",") if item.strip()}


def _diag(severity: str, code: str, message: str, **details: Any) -> dict[str, Any]:
    data: dict[str, Any] = {"severity": severity, "code": code, "message": message}
    data.update(details)
    return data
