"""Canonical lineage projection helpers for the research record query index."""

from __future__ import annotations

import json
from typing import Any, Iterable

from sqlalchemy import delete, insert, or_, select
from sqlalchemy.engine import Engine

from isomer_labs.models import EffectiveTopicContext
from isomer_labs.runtime.records import ResearchRecordLineageEdge, RuntimeLifecycleRecord
from isomer_labs.runtime.store import WorkspaceRuntimeStore

from .index_schema import SOURCE_CANONICAL_LINEAGE, record_edges, record_index


def replace_canonical_lineage_rows_for_record(
    connection: Any,
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    record_id: str,
) -> None:
    connection.execute(
        delete(record_edges).where(
            record_edges.c.topic_workspace_id == context.topic_workspace_id,
            record_edges.c.source_classification == SOURCE_CANONICAL_LINEAGE,
            or_(record_edges.c.source_record_id == record_id, record_edges.c.target_record_id == record_id),
        )
    )
    rows = [
        _canonical_lineage_edge_row(context, edge)
        for edge in store.list_research_record_lineage_edges(topic_workspace_id=context.topic_workspace_id)
        if edge.parent_record_id == record_id or edge.child_record_id == record_id
    ]
    if rows:
        connection.execute(insert(record_edges), rows)


def replace_all_canonical_lineage_rows(
    connection: Any,
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
) -> None:
    connection.execute(
        delete(record_edges).where(
            record_edges.c.topic_workspace_id == context.topic_workspace_id,
            record_edges.c.source_classification == SOURCE_CANONICAL_LINEAGE,
        )
    )
    rows = [
        _canonical_lineage_edge_row(context, edge)
        for edge in store.list_research_record_lineage_edges(topic_workspace_id=context.topic_workspace_id)
    ]
    if rows:
        connection.execute(insert(record_edges), rows)


def canonical_lineage_edges_for_query(
    store: WorkspaceRuntimeStore,
    context: EffectiveTopicContext,
    record_id: str,
    direction: str,
) -> list[ResearchRecordLineageEdge]:
    edges: list[ResearchRecordLineageEdge] = []
    if direction in {"upstream", "both"}:
        edges.extend(
            store.list_research_record_lineage_edges(
                topic_workspace_id=context.topic_workspace_id,
                child_record_id=record_id,
            )
        )
    if direction in {"downstream", "both"}:
        edges.extend(
            store.list_research_record_lineage_edges(
                topic_workspace_id=context.topic_workspace_id,
                parent_record_id=record_id,
            )
        )
    deduped = {edge.id: edge for edge in edges}
    return [deduped[key] for key in sorted(deduped)]


def canonical_lineage_edge_json(edge: ResearchRecordLineageEdge) -> dict[str, object]:
    data = edge.to_json()
    data["source_record_id"] = edge.parent_record_id
    data["target_record_id"] = edge.child_record_id
    data["relation_kind"] = edge.lineage_kind
    data["relation_role"] = edge.parent_role
    data["source_classification"] = SOURCE_CANONICAL_LINEAGE
    return data


def records_by_id_with_lifecycle_fallback(
    engine: Engine,
    store: WorkspaceRuntimeStore,
    context: EffectiveTopicContext,
    record_ids: Iterable[str],
) -> list[dict[str, object]]:
    rows_by_id = {str(row["record_id"]): row for row in _records_by_id(engine, context, record_ids)}
    for record_id in record_ids:
        if record_id in rows_by_id:
            continue
        record = store.get_lifecycle_record(record_id)
        if record is None or not _belongs_to_context(record, context):
            continue
        rows_by_id[record_id] = {
            "record_id": record.id,
            "research_topic_id": record.research_topic_id,
            "topic_workspace_id": record.topic_workspace_id,
            "record_kind": record.record_kind,
            "status": record.status,
            "title": record.id,
            "summary": None,
            "content_path": record.content_path,
            "source_classification": "lifecycle-fallback",
            "created_at": record.created_at,
            "updated_at": record.updated_at,
            "metadata": {"lifecycle_refs": record.lifecycle_refs, "transition_metadata": record.transition_metadata},
        }
    return [rows_by_id[key] for key in sorted(rows_by_id)]


def _canonical_lineage_edge_row(
    context: EffectiveTopicContext,
    edge: ResearchRecordLineageEdge,
) -> dict[str, object]:
    return {
        "id": f"canonical-{edge.id}",
        "research_topic_id": context.research_topic.id,
        "topic_workspace_id": context.topic_workspace_id,
        "source_record_id": edge.parent_record_id,
        "target_record_id": edge.child_record_id,
        "relation_kind": edge.lineage_kind,
        "relation_role": edge.parent_role,
        "source_field": "research_record_lineage_edges",
        "source_classification": SOURCE_CANONICAL_LINEAGE,
        "confidence": 1.0,
        "status": edge.status,
        "rationale": edge.rationale,
        "metadata_json": json.dumps(
            {
                "canonical_lineage_edge_id": edge.id,
                "generation_id": edge.generation_id,
                "decision_record_id": edge.decision_record_id,
                "metadata": edge.metadata,
            },
            sort_keys=True,
            separators=(",", ":"),
        ),
        "created_at": edge.created_at,
        "updated_at": edge.updated_at,
    }


def _records_by_id(engine: Engine, context: EffectiveTopicContext, record_ids: Iterable[str]) -> list[dict[str, object]]:
    ids = list(record_ids)
    if not ids:
        return []
    with engine.connect() as connection:
        rows = connection.execute(
            select(record_index).where(record_index.c.topic_workspace_id == context.topic_workspace_id, record_index.c.record_id.in_(ids))
        ).mappings()
        return [dict(row) for row in rows]


def _belongs_to_context(record: RuntimeLifecycleRecord, context: EffectiveTopicContext) -> bool:
    return record.research_topic_id == context.research_topic.id and record.topic_workspace_id == context.topic_workspace_id
