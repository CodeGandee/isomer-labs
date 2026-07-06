"""Topic graph view projection for the local Project web API."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
from typing import Any

from isomer_labs.models import EffectiveTopicContext

from .graph_edges import graph_edges as build_graph_edges
from .graph_edges import idea_graph_edges

GRAPH_SCOPES = {"idea-lineage", "artifact-overview", "experiment-records", "paper-revisions"}
RENDERERS = {"auto", "react-flow", "sigma"}
SPARSE_GRAPH_LIMIT = 120
DENSE_GRAPH_LIMIT = 1000


def build_topic_graph_view(
    context: EffectiveTopicContext,
    export_payload: Mapping[str, Any],
    *,
    graph_scope: str,
    renderer: str = "auto",
    status: str | None = None,
    relation_kind: str | None = None,
    producer: str | None = None,
    time_range: str | None = None,
    search: str | None = None,
    limit: int | None = None,
    cursor: str | None = None,
    include_secondary: bool = False,
) -> dict[str, Any]:
    """Build a renderer-neutral graph view from query-index export data."""

    if graph_scope not in GRAPH_SCOPES:
        return _error_payload(
            context,
            graph_scope,
            "unsupported_graph_scope",
            f"Unsupported graph scope: {graph_scope}",
        )
    if renderer not in RENDERERS:
        return _error_payload(context, graph_scope, "unsupported_renderer", f"Unsupported renderer: {renderer}")

    records = _records(export_payload)
    edges = _rows(export_payload, "edges")
    files = _rows(export_payload, "files")
    ideas = _rows(export_payload, "ideas")
    routes = _rows(export_payload, "routes")
    metrics = _rows(export_payload, "metrics")
    claims = _rows(export_payload, "claims")
    facts = _rows(export_payload, "facts")
    diagnostics = list(_rows(export_payload, "diagnostics"))
    projection_diagnostics: list[dict[str, Any]] = []

    if graph_scope == "idea-lineage":
        nodes, record_node_ids = _idea_nodes(
            records,
            ideas,
            routes,
            claims,
            topic_id=context.research_topic.id,
            include_secondary=include_secondary,
        )
    else:
        scoped_records = _records_for_dense_scope(records, graph_scope)
        nodes = [_record_node(record, graph_scope, topic_id=context.research_topic.id) for record in scoped_records]
        record_node_ids = {str(record.get("record_id")): f"record:{record.get('record_id')}" for record in scoped_records if record.get("record_id")}
        if include_secondary:
            secondary_nodes, secondary_record_node_ids = _file_nodes(files, topic_id=context.research_topic.id)
            nodes.extend(secondary_nodes)
            record_node_ids.update(secondary_record_node_ids)

    if graph_scope == "idea-lineage":
        graph_edges = idea_graph_edges(
            edges,
            record_node_ids,
            relation_kind=relation_kind,
            include_secondary=include_secondary,
            diagnostics=projection_diagnostics,
        )
    else:
        graph_edges = build_graph_edges(edges, record_node_ids, relation_kind=relation_kind, diagnostics=projection_diagnostics)
    if include_secondary and graph_scope != "idea-lineage":
        graph_edges.extend(_file_edges(files, record_node_ids))

    nodes = _filter_nodes(nodes, status=status, producer=producer, time_range=time_range, search=search)
    allowed_node_ids = {str(node["id"]) for node in nodes}
    graph_edges = [edge for edge in graph_edges if edge["source"] in allowed_node_ids and edge["target"] in allowed_node_ids]
    groups = _groups(nodes, graph_edges, edges)
    facets = _facets(ideas=ideas, routes=routes, metrics=metrics, claims=claims, facts=facts, files=files, filters={
        "status": status,
        "relation_kind": relation_kind,
        "producer": producer,
        "time_range": time_range,
        "search": search,
        "include_secondary": include_secondary,
    })

    offset = _cursor_offset(cursor)
    selected_limit = limit or (SPARSE_GRAPH_LIMIT if graph_scope == "idea-lineage" else DENSE_GRAPH_LIMIT)
    total_nodes = len(nodes)
    truncated = offset > 0 or total_nodes > offset + selected_limit
    paged_nodes = nodes[offset : offset + selected_limit]
    paged_node_ids = {str(node["id"]) for node in paged_nodes}
    paged_edges = [edge for edge in graph_edges if edge["source"] in paged_node_ids and edge["target"] in paged_node_ids]
    next_cursor = str(offset + selected_limit) if total_nodes > offset + selected_limit else None

    renderer_hint = _renderer_hint(graph_scope, len(nodes), renderer)
    if renderer == "react-flow" and len(nodes) > SPARSE_GRAPH_LIMIT:
        payload = _base_payload(context, graph_scope, export_payload, renderer_hint="sigma-overview")
        payload.update(
            {
                "ok": False,
                "error": {
                    "code": "graph_too_large_for_renderer",
                    "message": "The requested graph is too large for the React Flow detail renderer.",
                    "fallback_renderer": "sigma",
                },
                "nodes": paged_nodes,
                "edges": paged_edges,
                "groups": groups,
                "facets": facets,
                "paging": {"cursor": cursor, "next_cursor": next_cursor, "truncated": True},
                "diagnostics": diagnostics + projection_diagnostics,
            }
        )
        return payload

    payload = _base_payload(context, graph_scope, export_payload, renderer_hint=renderer_hint)
    payload.update(
        {
            "nodes": paged_nodes,
            "edges": paged_edges,
            "groups": groups,
            "facets": facets,
            "paging": {"cursor": cursor, "next_cursor": next_cursor, "truncated": truncated},
            "diagnostics": diagnostics + projection_diagnostics,
        }
    )
    return payload


def _base_payload(
    context: EffectiveTopicContext,
    graph_scope: str,
    export_payload: Mapping[str, Any],
    *,
    renderer_hint: str,
) -> dict[str, Any]:
    return {
        "ok": bool(export_payload.get("ok", True)),
        "mutated": False,
        "topic_id": context.research_topic.id,
        "topic_workspace_id": context.topic_workspace_id,
        "graph_scope": graph_scope,
        "renderer_hint": renderer_hint,
        "index_revision": export_payload.get("index_revision"),
        "generated_at": datetime.now(UTC).isoformat(),
    }


def _error_payload(
    context: EffectiveTopicContext,
    graph_scope: str,
    code: str,
    message: str,
) -> dict[str, Any]:
    return {
        "ok": False,
        "mutated": False,
        "topic_id": context.research_topic.id,
        "topic_workspace_id": context.topic_workspace_id,
        "graph_scope": graph_scope,
        "renderer_hint": "sigma-overview",
        "index_revision": None,
        "generated_at": datetime.now(UTC).isoformat(),
        "nodes": [],
        "edges": [],
        "groups": [],
        "facets": {"counts": {}},
        "paging": {"cursor": None, "next_cursor": None, "truncated": False},
        "error": {"code": code, "message": message},
        "diagnostics": [_diag("error", code, message)],
    }


def _records(export_payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [dict(row) for row in _rows(export_payload, "nodes")]


def _rows(payload: Mapping[str, Any], key: str) -> list[dict[str, Any]]:
    value = payload.get(key)
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, Mapping)]


def _idea_nodes(
    records: list[dict[str, Any]],
    ideas: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    *,
    topic_id: str,
    include_secondary: bool,
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    records_by_id = {str(record.get("record_id")): record for record in records if record.get("record_id")}
    nodes: list[dict[str, Any]] = []
    record_node_ids: dict[str, str] = {}
    seen_node_ids: set[str] = set()

    for idea in ideas:
        record_id = str(idea.get("record_id") or "")
        if not record_id:
            continue
        record = records_by_id.get(record_id, {})
        idea_id = str(idea.get("idea_id") or idea.get("id") or record_id)
        node_id = f"idea:{idea_id}"
        if node_id in seen_node_ids:
            record_node_ids.setdefault(record_id, node_id)
            continue
        node = _node(
            node_id=node_id,
            record_id=record_id,
            material_kind="idea",
            density_class="sparse",
            title=str(idea.get("one_liner") or record.get("title") or idea_id),
            one_liner=idea.get("one_liner"),
            summary=record.get("summary"),
            status=idea.get("status") or record.get("status"),
            selected=bool(idea.get("selected")),
            producer=record.get("producer"),
            skill=record.get("skill"),
            created_at=idea.get("created_at") or record.get("created_at"),
            updated_at=record.get("updated_at"),
            source={"record_id": record_id, "idea_id": idea.get("idea_id"), "source_json_path": idea.get("source_json_path"), "source_classification": idea.get("source_classification") or record.get("source_classification")},
            topic_id=topic_id,
            renderer_hints={"card_variant": "idea", "cluster": idea.get("family"), "color": "#2b6cb0" if idea.get("selected") else "#64748b", "size": 18 if idea.get("selected") else 12},
        )
        nodes.append(node)
        seen_node_ids.add(node_id)
        record_node_ids.setdefault(record_id, node_id)

    if not nodes:
        for record in records:
            if str(record.get("record_kind")) not in {"research_inquiry", "decision_record", "finding", "research_claim"}:
                continue
            record_id = str(record.get("record_id") or "")
            if not record_id:
                continue
            node_id = f"record:{record_id}"
            nodes.append(_record_node(record, "idea-lineage", topic_id=topic_id, material_kind="idea", density_class="sparse"))
            record_node_ids[record_id] = node_id

    if include_secondary:
        for route in routes:
            record_id = str(route.get("record_id") or "")
            if not record_id:
                continue
            route_id = str(route.get("id") or record_id)
            node_id = f"decision:{route_id}"
            nodes.append(
                _node(
                    node_id=node_id,
                    record_id=record_id,
                    material_kind="decision",
                    density_class="sparse",
                    title=str(route.get("decision") or route.get("next_route") or "Route decision"),
                    one_liner=route.get("reason"),
                    summary=route.get("next_route"),
                    status=route.get("decision"),
                    selected=None,
                    producer=None,
                    skill=None,
                    created_at=route.get("created_at"),
                    updated_at=route.get("created_at"),
                    source={"record_id": record_id, "source_json_path": route.get("source_json_path"), "source_classification": route.get("source_classification")},
                    topic_id=topic_id,
                    renderer_hints={"card_variant": "decision", "color": "#7c3aed", "size": 11},
                )
            )
            record_node_ids.setdefault(record_id, node_id)
        for claim in claims:
            record_id = str(claim.get("record_id") or "")
            if not record_id:
                continue
            claim_id = str(claim.get("id") or record_id)
            node_id = f"claim:{claim_id}"
            nodes.append(
                _node(
                    node_id=node_id,
                    record_id=record_id,
                    material_kind="claim",
                    density_class="sparse",
                    title=str(claim.get("claim") or "Research claim"),
                    one_liner=claim.get("verdict"),
                    summary=claim.get("expected"),
                    status=claim.get("verdict"),
                    selected=None,
                    producer=None,
                    skill=None,
                    created_at=claim.get("created_at"),
                    updated_at=claim.get("created_at"),
                    source={"record_id": record_id, "source_json_path": claim.get("source_json_path"), "source_classification": claim.get("source_classification")},
                    topic_id=topic_id,
                    renderer_hints={"card_variant": "evidence", "color": "#0f766e", "size": 10},
                )
            )
            record_node_ids.setdefault(record_id, node_id)

    return nodes, record_node_ids


def _record_node(
    record: Mapping[str, Any],
    graph_scope: str,
    *,
    topic_id: str,
    material_kind: str | None = None,
    density_class: str | None = None,
) -> dict[str, Any]:
    record_id = str(record.get("record_id") or "")
    return _node(
        node_id=f"record:{record_id}",
        record_id=record_id,
        material_kind=material_kind or _material_kind(record, graph_scope),
        density_class=density_class or ("sparse" if graph_scope == "idea-lineage" else "dense"),
        title=str(record.get("title") or record_id),
        one_liner=record.get("summary"),
        summary=record.get("summary"),
        status=record.get("status"),
        selected=None,
        producer=record.get("producer"),
        skill=record.get("skill"),
        created_at=record.get("created_at"),
        updated_at=record.get("updated_at"),
        source={"record_id": record_id, "source_json_path": record.get("payload_file_path"), "source_classification": record.get("source_classification")},
        topic_id=topic_id,
        renderer_hints={"card_variant": "record", "cluster": record.get("record_kind"), "color": _record_color(record), "size": _record_size(record)},
    )


def _node(
    *,
    node_id: str,
    record_id: str,
    material_kind: str,
    density_class: str,
    title: str,
    one_liner: Any,
    summary: Any,
    status: Any,
    selected: bool | None,
    producer: Any,
    skill: Any,
    created_at: Any,
    updated_at: Any,
    source: Mapping[str, Any],
    topic_id: str,
    renderer_hints: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "id": node_id,
        "record_id": record_id,
        "material_kind": material_kind,
        "density_class": density_class,
        "title": title,
        "one_liner": one_liner,
        "summary": summary,
        "status": status,
        "selected": selected,
        "producer": producer,
        "skill": skill,
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


def _records_for_dense_scope(records: list[dict[str, Any]], graph_scope: str) -> list[dict[str, Any]]:
    if graph_scope == "artifact-overview":
        return records
    keywords = {
        "experiment-records": ("experiment", "run", "metric", "evidence", "result", "claim"),
        "paper-revisions": ("paper", "revision", "draft", "manuscript", "pdf", "figure"),
    }[graph_scope]
    selected: list[dict[str, Any]] = []
    for record in records:
        haystack = " ".join(str(record.get(key) or "").lower() for key in ("record_kind", "profile", "profile_name", "title", "summary", "content_path", "payload_file_path"))
        if any(keyword in haystack for keyword in keywords):
            selected.append(record)
    return selected


def _file_nodes(files: list[dict[str, Any]], *, topic_id: str) -> tuple[list[dict[str, Any]], dict[str, str]]:
    nodes: list[dict[str, Any]] = []
    record_node_ids: dict[str, str] = {}
    for file_row in files:
        file_id = str(file_row.get("id") or file_row.get("path") or "")
        record_id = str(file_row.get("record_id") or "")
        if not file_id or not record_id:
            continue
        node_id = f"file:{file_id}"
        nodes.append(
            _node(
                node_id=node_id,
                record_id=record_id,
                material_kind="file",
                density_class="dense",
                title=str(file_row.get("semantic_label") or file_row.get("file_role") or file_row.get("path")),
                one_liner=file_row.get("path"),
                summary=file_row.get("media_type"),
                status=file_row.get("status"),
                selected=None,
                producer=None,
                skill=None,
                created_at=file_row.get("created_at"),
                updated_at=file_row.get("updated_at"),
                source={"record_id": record_id, "source_json_path": file_row.get("source_field"), "source_classification": file_row.get("source_classification")},
                topic_id=topic_id,
                renderer_hints={"card_variant": "record", "cluster": "file", "color": "#475569", "size": 6},
            )
        )
        record_node_ids[f"file:{record_id}:{file_id}"] = node_id
    return nodes, record_node_ids


def _file_edges(files: list[dict[str, Any]], record_node_ids: Mapping[str, str]) -> list[dict[str, Any]]:
    edges: list[dict[str, Any]] = []
    for file_row in files:
        record_id = str(file_row.get("record_id") or "")
        file_id = str(file_row.get("id") or file_row.get("path") or "")
        source = record_node_ids.get(record_id)
        target = record_node_ids.get(f"file:{record_id}:{file_id}")
        if source and target:
            edges.append(
                {
                    "id": f"{source}->{target}:materializes_file",
                    "source": source,
                    "target": target,
                    "relation_kind": "materializes_file",
                    "canonical": False,
                    "lineage_kind": None,
                    "generation_id": None,
                    "status": file_row.get("status"),
                    "rationale": None,
                    "confidence": None,
                    "source_classification": file_row.get("source_classification"),
                }
            )
    return edges


def _filter_nodes(
    nodes: list[dict[str, Any]],
    *,
    status: str | None,
    producer: str | None,
    time_range: str | None,
    search: str | None,
) -> list[dict[str, Any]]:
    statuses = _split_filter(status)
    producers = _split_filter(producer)
    since = _since(time_range)
    search_text = search.lower().strip() if search else None
    selected: list[dict[str, Any]] = []
    for node in nodes:
        if statuses and str(node.get("status") or "") not in statuses:
            continue
        if producers and str(node.get("producer") or node.get("skill") or "") not in producers:
            continue
        if since is not None and not _node_after(node, since):
            continue
        if search_text and search_text not in _node_haystack(node):
            continue
        selected.append(node)
    return selected


def _node_after(node: Mapping[str, Any], since: datetime) -> bool:
    for key in ("updated_at", "created_at"):
        value = node.get(key)
        if not isinstance(value, str) or not value:
            continue
        try:
            candidate = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            continue
        if candidate.tzinfo is None:
            candidate = candidate.replace(tzinfo=UTC)
        if candidate >= since:
            return True
    return False


def _node_haystack(node: Mapping[str, Any]) -> str:
    fields = [
        node.get("id"),
        node.get("record_id"),
        node.get("title"),
        node.get("one_liner"),
        node.get("summary"),
        node.get("status"),
        node.get("producer"),
        node.get("skill"),
        node.get("material_kind"),
    ]
    return " ".join(str(value).lower() for value in fields if value is not None)


def _groups(nodes: list[dict[str, Any]], graph_edges: list[dict[str, Any]], raw_edges: list[dict[str, Any]]) -> list[dict[str, Any]]:
    incident: set[str] = set()
    for edge in graph_edges:
        incident.add(str(edge["source"]))
        incident.add(str(edge["target"]))
    result: list[dict[str, Any]] = []
    by_generation: dict[str, set[str]] = {}
    for edge in graph_edges:
        generation_id = edge.get("generation_id")
        if generation_id is None:
            continue
        group = by_generation.setdefault(str(generation_id), set())
        group.add(str(edge["source"]))
        group.add(str(edge["target"]))
    for generation_id, node_ids in sorted(by_generation.items()):
        result.append(
            {
                "id": f"generation:{generation_id}",
                "group_kind": "generation_group",
                "title": f"Generation group {generation_id}",
                "purpose": "Sibling or alternative records created from the same parent set.",
                "parent_set_digest": None,
                "node_ids": sorted(node_ids),
                "diagnostics": [],
            }
        )
    unconnected = sorted(str(node["id"]) for node in nodes if str(node["id"]) not in incident)
    if unconnected:
        ideas_only = all(str(node.get("material_kind")) == "idea" for node in nodes)
        result.append(
            {
                "id": "unconnected",
                "group_kind": "unconnected",
                "title": "Unconnected ideas" if ideas_only else "Unconnected materials",
                "purpose": "Ideas without in-scope typed relationships in the current read model." if ideas_only else "Materials without in-scope typed relationships in the current read model.",
                "parent_set_digest": None,
                "node_ids": unconnected,
                "diagnostics": [_diag("info", "graph_unconnected_nodes", f"{len(unconnected)} nodes have no in-scope graph edges.")],
            }
        )
    if raw_edges and not graph_edges:
        result.append(
            {
                "id": "partial-relationship-data",
                "group_kind": "artifact_cluster",
                "title": "Partial relationship data",
                "purpose": "Relationship rows exist, but none connect the selected graph nodes.",
                "parent_set_digest": None,
                "node_ids": [],
                "diagnostics": [_diag("warning", "graph_edges_not_projected", "No relationship rows connected the selected graph nodes.")],
            }
        )
    return result


def _facets(
    *,
    ideas: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    metrics: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    facts: list[dict[str, Any]],
    files: list[dict[str, Any]],
    filters: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "counts": {
            "ideas": len(ideas),
            "routes": len(routes),
            "metrics": len(metrics),
            "claims": len(claims),
            "facts": len(facts),
            "files": len(files),
            "missing_files": len([row for row in files if not row.get("exists")]),
            "openable_files": len([row for row in files if row.get("openable")]),
        },
        "filters": dict(filters),
        "status_values": sorted({str(row.get("status")) for row in ideas if row.get("status")}),
        "route_decisions": sorted({str(row.get("decision")) for row in routes if row.get("decision")}),
    }


def _renderer_hint(graph_scope: str, node_count: int, renderer: str) -> str:
    if renderer == "sigma":
        return "sigma-overview"
    if renderer == "react-flow" and node_count <= SPARSE_GRAPH_LIMIT:
        return "react-flow-detail"
    if graph_scope == "idea-lineage" and node_count <= SPARSE_GRAPH_LIMIT:
        return "react-flow-detail"
    return "sigma-overview"


def _material_kind(record: Mapping[str, Any], graph_scope: str) -> str:
    if graph_scope == "paper-revisions":
        return "paper_revision"
    kind = str(record.get("record_kind") or "")
    profile = str(record.get("profile") or record.get("profile_name") or "").lower()
    if "run" in kind or "experiment" in profile or "run" in profile:
        return "experiment"
    if kind == "decision_record":
        return "decision"
    if kind == "evidence_item":
        return "evidence"
    if kind == "research_claim":
        return "claim"
    if "metric" in profile:
        return "metric"
    if graph_scope == "idea-lineage":
        return "idea"
    return "record"


def _record_color(record: Mapping[str, Any]) -> str:
    kind = str(record.get("record_kind") or "")
    return {
        "run": "#2563eb",
        "artifact": "#475569",
        "decision_record": "#7c3aed",
        "evidence_item": "#0f766e",
        "research_claim": "#b45309",
        "finding": "#15803d",
    }.get(kind, "#64748b")


def _record_size(record: Mapping[str, Any]) -> int:
    kind = str(record.get("record_kind") or "")
    if kind in {"run", "artifact"}:
        return 9
    if kind in {"decision_record", "research_claim"}:
        return 11
    return 7


def _split_filter(value: str | None) -> set[str]:
    if not value:
        return set()
    return {item.strip() for item in value.split(",") if item.strip()}


def _since(time_range: str | None) -> datetime | None:
    if time_range is None or time_range == "" or time_range == "all":
        return None
    now = datetime.now(UTC)
    if time_range == "7d":
        return now - timedelta(days=7)
    if time_range == "30d":
        return now - timedelta(days=30)
    if time_range == "90d":
        return now - timedelta(days=90)
    if "/" in time_range:
        start, _end = time_range.split("/", 1)
        try:
            parsed = datetime.fromisoformat(start.replace("Z", "+00:00"))
        except ValueError:
            return None
        return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=UTC)
    return None


def _cursor_offset(cursor: str | None) -> int:
    if cursor is None:
        return 0
    try:
        return max(0, int(cursor))
    except ValueError:
        return 0


def _diag(severity: str, code: str, message: str, **extra: object) -> dict[str, Any]:
    return {"severity": severity, "code": code, "message": message, **extra}
