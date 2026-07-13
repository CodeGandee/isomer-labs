"""Bounded read-only neighborhood projection for Topic Graph views."""

from __future__ import annotations

from collections import deque
from typing import Any

MAX_NEIGHBORHOOD_SEEDS = 64
MAX_NEIGHBORHOOD_HOPS = 8
MAX_NEIGHBORHOOD_NODES = 2000
MAX_NEIGHBORHOOD_EDGES = 10000
NEIGHBORHOOD_DIRECTIONS = {"incoming", "outgoing", "both"}
NEIGHBORHOOD_EDGE_MODES = {"induced", "traversal"}


def project_graph_neighborhood(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    *,
    seed_node_ids: list[str],
    hop_radius: int,
    direction: str,
    relation_kinds: set[str] | None = None,
    edge_mode: str = "induced",
) -> dict[str, Any]:
    """Return a deterministic, renderer-neutral multi-source N-hop projection."""

    unique_seeds = list(dict.fromkeys(str(seed_id) for seed_id in seed_node_ids if str(seed_id)))
    node_ids = {str(node.get("id")) for node in nodes}
    resolved_seeds = [seed_id for seed_id in unique_seeds if seed_id in node_ids]
    unresolved_seeds = [seed_id for seed_id in unique_seeds if seed_id not in node_ids]
    selected_relations = relation_kinds or set()
    eligible_edges = sorted(
        (
            edge
            for edge in edges
            if str(edge.get("source")) in node_ids
            and str(edge.get("target")) in node_ids
            and (not selected_relations or str(edge.get("relation_kind")) in selected_relations)
        ),
        key=lambda edge: (str(edge.get("id")), str(edge.get("source")), str(edge.get("target"))),
    )
    diagnostics = [
        _diagnostic(
            "warning",
            "graph_projection_seed_not_found",
            f"Idea Graph projection seed does not exist: {seed_id}",
            seed_node_id=seed_id,
        )
        for seed_id in unresolved_seeds
    ]
    adjacency: dict[str, list[tuple[str, str]]] = {node_id: [] for node_id in node_ids}
    for edge in eligible_edges:
        source = str(edge["source"])
        target = str(edge["target"])
        edge_id = str(edge["id"])
        if direction in {"outgoing", "both"}:
            adjacency[source].append((target, edge_id))
        if direction in {"incoming", "both"}:
            adjacency[target].append((source, edge_id))
    for neighbors in adjacency.values():
        neighbors.sort()

    distances = {seed_id: 0 for seed_id in resolved_seeds}
    queue = deque(resolved_seeds)
    traversal_edge_ids: set[str] = set()
    while queue:
        current = queue.popleft()
        distance = distances[current]
        if distance >= hop_radius:
            continue
        for neighbor, edge_id in adjacency[current]:
            if neighbor in distances:
                continue
            distances[neighbor] = distance + 1
            traversal_edge_ids.add(edge_id)
            queue.append(neighbor)

    visible_node_ids = set(distances)
    projected_nodes = sorted((node for node in nodes if str(node.get("id")) in visible_node_ids), key=lambda node: str(node.get("id")))
    if edge_mode == "traversal":
        projected_edges = [edge for edge in eligible_edges if str(edge.get("id")) in traversal_edge_ids]
    else:
        projected_edges = [edge for edge in eligible_edges if str(edge.get("source")) in visible_node_ids and str(edge.get("target")) in visible_node_ids]

    projection = {
        "seed_node_ids": unique_seeds,
        "resolved_seed_node_ids": resolved_seeds,
        "unresolved_seed_node_ids": unresolved_seeds,
        "hop_radius": hop_radius,
        "direction": direction,
        "relation_kinds": sorted(selected_relations),
        "edge_mode": edge_mode,
        "source_node_count": len(nodes),
        "source_edge_count": len(edges),
        "visible_node_count": len(projected_nodes),
        "visible_edge_count": len(projected_edges),
        "source_index_revision": None,
        "topology_complete": True,
    }
    if len(projected_nodes) > MAX_NEIGHBORHOOD_NODES or len(projected_edges) > MAX_NEIGHBORHOOD_EDGES:
        message = f"Idea Graph neighborhood exceeds the configured projection safety bound ({len(projected_nodes)} nodes, {len(projected_edges)} edges)."
        projection["topology_complete"] = False
        diagnostics.append(_diagnostic("error", "graph_projection_too_large", message))
        return {
            "ok": False,
            "nodes": [],
            "edges": [],
            "projection": projection,
            "diagnostics": diagnostics,
            "error": {"code": "graph_projection_too_large", "message": message},
        }
    return {
        "ok": True,
        "nodes": projected_nodes,
        "edges": projected_edges,
        "projection": projection,
        "diagnostics": diagnostics,
        "error": None,
    }


def projection_input_error(
    *,
    seed_node_ids: list[str] | None,
    hop_radius: int | None,
    direction: str,
    edge_mode: str,
) -> tuple[str, str] | None:
    seeds = list(dict.fromkeys(str(seed_id) for seed_id in (seed_node_ids or []) if str(seed_id)))
    if hop_radius is not None and not seeds:
        return "graph_projection_requires_seeds", "Idea Graph neighborhood projection requires at least one selected seed node."
    if len(seeds) > MAX_NEIGHBORHOOD_SEEDS:
        return "graph_projection_too_many_seeds", f"Idea Graph neighborhood projection accepts at most {MAX_NEIGHBORHOOD_SEEDS} seed nodes."
    if hop_radius is not None and (hop_radius < 0 or hop_radius > MAX_NEIGHBORHOOD_HOPS):
        return "graph_projection_invalid_radius", f"Idea Graph neighborhood radius must be between 0 and {MAX_NEIGHBORHOOD_HOPS}."
    if direction not in NEIGHBORHOOD_DIRECTIONS:
        return "graph_projection_invalid_direction", f"Unsupported Idea Graph neighborhood direction: {direction}"
    if edge_mode not in NEIGHBORHOOD_EDGE_MODES:
        return "graph_projection_invalid_edge_mode", f"Unsupported Idea Graph neighborhood edge mode: {edge_mode}"
    return None


def _diagnostic(severity: str, code: str, message: str, **context: Any) -> dict[str, Any]:
    return {"severity": severity, "code": code, "message": message, **context}
