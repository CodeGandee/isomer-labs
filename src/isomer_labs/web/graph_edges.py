"""Relationship edge projection helpers for Topic graph views."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

OVERVIEW_DIRECT_RELATIONS = {
    "derived_from",
    "revision_of",
    "selected_from",
    "follow_up_to",
    "alternative_to",
    "supersedes",
    "follows_from",
    "supports",
    "contradicts",
}
OVERVIEW_COLLAPSED_RELATIONS = {
    "derived_from",
    "revision_of",
    "selected_from",
    "follow_up_to",
    "alternative_to",
    "supersedes",
    "follows_from",
}


def graph_edges(
    rows: list[dict[str, Any]],
    record_node_ids: Mapping[str, str],
    *,
    relation_kind: str | None,
    diagnostics: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    accepted_relations = _split_filter(relation_kind)
    edges: list[dict[str, Any]] = []
    skipped = 0
    for row in rows:
        raw_relation = str(row.get("relation_kind") or "")
        if accepted_relations and raw_relation not in accepted_relations:
            continue
        source_record = str(row.get("source_record_id") or "")
        target_record = str(row.get("target_record_id") or "")
        source = record_node_ids.get(source_record)
        target = record_node_ids.get(target_record)
        if source is None or target is None:
            skipped += 1
            continue
        edges.append(_edge_payload(row, source=source, target=target, collapsed=False))
    if skipped:
        diagnostics.append(_diag("info", "graph_edges_outside_scope", f"{skipped} relationship edges were outside the selected graph scope."))
    return edges


def idea_graph_edges(
    rows: list[dict[str, Any]],
    record_node_ids: Mapping[str, str],
    *,
    relation_kind: str | None,
    include_secondary: bool,
    diagnostics: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if include_secondary:
        return graph_edges(rows, record_node_ids, relation_kind=relation_kind, diagnostics=diagnostics)
    return idea_overview_edges(rows, record_node_ids, relation_kind=relation_kind, diagnostics=diagnostics)


def idea_overview_edges(
    rows: list[dict[str, Any]],
    record_node_ids: Mapping[str, str],
    *,
    relation_kind: str | None,
    diagnostics: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    accepted_relations = _split_filter(relation_kind)
    idea_record_ids = set(record_node_ids)
    edges: list[dict[str, Any]] = []
    emitted: set[tuple[str, str, str]] = set()
    skipped_relation = 0

    for row in rows:
        raw_relation = str(row.get("relation_kind") or "")
        if accepted_relations and raw_relation not in accepted_relations:
            continue
        source_record = str(row.get("source_record_id") or "")
        target_record = str(row.get("target_record_id") or "")
        if source_record not in idea_record_ids or target_record not in idea_record_ids:
            continue
        if raw_relation not in OVERVIEW_DIRECT_RELATIONS:
            skipped_relation += 1
            continue
        source = record_node_ids[source_record]
        target = record_node_ids[target_record]
        key = (source, target, raw_relation)
        if key in emitted:
            continue
        emitted.add(key)
        edges.append(_edge_payload(row, source=source, target=target, collapsed=False))

    by_source: dict[str, list[dict[str, Any]]] = {}
    by_target: dict[str, list[dict[str, Any]]] = {}
    middle_record_ids: set[str] = set()
    for row in rows:
        raw_relation = str(row.get("relation_kind") or "")
        if accepted_relations and raw_relation not in accepted_relations:
            continue
        if raw_relation not in OVERVIEW_COLLAPSED_RELATIONS:
            continue
        source_record = str(row.get("source_record_id") or "")
        target_record = str(row.get("target_record_id") or "")
        by_source.setdefault(source_record, []).append(row)
        by_target.setdefault(target_record, []).append(row)
        if source_record not in idea_record_ids:
            middle_record_ids.add(source_record)
        if target_record not in idea_record_ids:
            middle_record_ids.add(target_record)

    ambiguous = 0
    for middle_record in sorted(middle_record_ids):
        incoming = [row for row in by_target.get(middle_record, []) if str(row.get("source_record_id") or "") in idea_record_ids]
        outgoing = [row for row in by_source.get(middle_record, []) if str(row.get("target_record_id") or "") in idea_record_ids]
        source_ideas = {str(row.get("source_record_id") or "") for row in incoming}
        target_ideas = {str(row.get("target_record_id") or "") for row in outgoing}
        if not incoming and not outgoing:
            continue
        if len(source_ideas) != 1 or len(target_ideas) != 1:
            ambiguous += 1
            continue
        source_record = next(iter(source_ideas))
        target_record = next(iter(target_ideas))
        if source_record == target_record:
            ambiguous += 1
            continue
        source = record_node_ids[source_record]
        target = record_node_ids[target_record]
        relation = _collapsed_relation(incoming, outgoing)
        key = (source, target, relation)
        if key in emitted:
            continue
        emitted.add(key)
        path_rows = [*incoming, *outgoing]
        edges.append(_collapsed_edge_payload(path_rows, source=source, target=target, source_record=source_record, middle_record=middle_record, target_record=target_record, relation=relation))

    if skipped_relation:
        diagnostics.append(_diag("info", "idea_edge_relation_not_overview", f"{skipped_relation} idea-to-idea edges use relation kinds reserved for detail views."))
    if ambiguous:
        diagnostics.append(_diag("warning", "idea_edge_projection_ambiguous", f"{ambiguous} supporting-record paths could not be collapsed into unambiguous idea edges."))
    if rows and not edges:
        diagnostics.append(_diag("warning", "idea_edges_not_projected", "No relationship rows could be projected into idea-to-idea overview edges."))
    return edges


def _edge_payload(row: Mapping[str, Any], *, source: str, target: str, collapsed: bool) -> dict[str, Any]:
    raw_relation = str(row.get("relation_kind") or "")
    source_record = str(row.get("source_record_id") or "")
    target_record = str(row.get("target_record_id") or "")
    return {
        "id": str(row.get("id") or f"{source}->{target}:{raw_relation}"),
        "source": source,
        "target": target,
        "relation_kind": raw_relation,
        "canonical": row.get("source_classification") == "canonical-lineage",
        "lineage_kind": raw_relation if row.get("source_classification") == "canonical-lineage" else None,
        "generation_id": _edge_generation_id(row),
        "status": row.get("status"),
        "rationale": row.get("rationale"),
        "confidence": row.get("confidence"),
        "source_classification": row.get("source_classification"),
        "collapsed": collapsed,
        "source_relationship_refs": [str(row.get("id"))] if row.get("id") else [],
        "source_record_refs": [source_record, target_record] if source_record and target_record else [],
    }


def _collapsed_edge_payload(
    path_rows: list[dict[str, Any]],
    *,
    source: str,
    target: str,
    source_record: str,
    middle_record: str,
    target_record: str,
    relation: str,
) -> dict[str, Any]:
    return {
        "id": f"collapsed:{middle_record}:{source}->{target}:{relation}",
        "source": source,
        "target": target,
        "relation_kind": relation,
        "canonical": any(row.get("source_classification") == "canonical-lineage" for row in path_rows),
        "lineage_kind": relation if any(row.get("source_classification") == "canonical-lineage" for row in path_rows) else None,
        "generation_id": _first_non_empty(_edge_generation_id(row) for row in path_rows),
        "status": _first_non_empty(row.get("status") for row in path_rows),
        "rationale": _first_non_empty(row.get("rationale") for row in path_rows),
        "confidence": _min_confidence(path_rows),
        "source_classification": "collapsed-projection",
        "collapsed": True,
        "source_relationship_refs": [str(row.get("id")) for row in path_rows if row.get("id")],
        "source_record_refs": [source_record, middle_record, target_record],
        "source_classifications": sorted({str(row.get("source_classification")) for row in path_rows if row.get("source_classification")}),
        "projection_path": [
            {
                "source_record_id": row.get("source_record_id"),
                "target_record_id": row.get("target_record_id"),
                "relation_kind": row.get("relation_kind"),
                "source_classification": row.get("source_classification"),
            }
            for row in path_rows
        ],
    }


def _edge_generation_id(row: Mapping[str, Any]) -> Any:
    metadata_value = row.get("metadata")
    metadata = metadata_value if isinstance(metadata_value, Mapping) else {}
    return row.get("generation_id") or metadata.get("generation_id")


def _collapsed_relation(incoming: list[dict[str, Any]], outgoing: list[dict[str, Any]]) -> str:
    for row in [*outgoing, *incoming]:
        relation = str(row.get("relation_kind") or "")
        if relation in OVERVIEW_COLLAPSED_RELATIONS:
            return relation
    return str((outgoing or incoming)[0].get("relation_kind") or "derived_from")


def _first_non_empty(values: Iterable[Any]) -> Any:
    for value in values:
        if value not in (None, ""):
            return value
    return None


def _min_confidence(rows: list[dict[str, Any]]) -> float | None:
    values: list[float] = []
    for row in rows:
        value = row.get("confidence")
        if isinstance(value, (int, float)):
            values.append(float(value))
    return min(values) if values else None


def _split_filter(value: str | None) -> set[str]:
    if not value:
        return set()
    return {item.strip() for item in value.split(",") if item.strip()}


def _diag(severity: str, code: str, message: str, **extra: object) -> dict[str, Any]:
    return {"severity": severity, "code": code, "message": message, **extra}
