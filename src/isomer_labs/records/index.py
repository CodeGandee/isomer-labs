"""SQL-backed query index for topic-scoped research records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from sqlalchemy import Table, and_, create_engine, delete, or_, select, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError

from isomer_labs.models import EffectiveTopicContext
from isomer_labs.runtime.records import ResearchRecordLineageEdge, RuntimeLifecycleRecord
from isomer_labs.runtime.store import WorkspaceRuntimeStore, open_workspace_runtime

from .index_extractors import (
    _build_index_parts,
    _parts_counts,
    _replace_record_rows,
    _resolve_local_path,
    _sum_counts,
)
from .index_revision import index_revision_payload
from .idea_index import canonical_ideas_with_source_status, canonical_realizations_with_source_status, idea_export_diagnostics, legacy_idea_facet
from .lineage_index import (
    canonical_lineage_edge_json,
    canonical_lineage_edges_for_query,
    records_by_id_with_lifecycle_fallback,
    replace_all_canonical_lineage_rows,
    replace_canonical_lineage_rows_for_record,
)
from .semantic_index import index_diagnostic as _diag, invalid_query_payload as _invalid_query_payload
from .semantic_index import latest_record_candidates, records_by_id, valid_semantic_id
from .semantic_index import query_index_schema_unavailable_payload as _query_index_schema_unavailable_payload
from .index_schema import (
    EXPORT_VIEWS,
    QUERY_FACETS,
    QUERY_INDEX_RECORD_KINDS,
    QUERY_INDEX_TABLE_NAMES,
    RELATION_KINDS,
    SOURCE_AUTHORED,
    SOURCE_BODY,
    SOURCE_CANONICAL_LINEAGE,
    SOURCE_FILE,
    SOURCE_PAYLOAD,
    record_claims,
    record_edges,
    record_files,
    record_ideas,
    record_index,
    record_json_facts,
    record_metrics,
    record_routes,
)

def refresh_query_index_for_record(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    record_id: str,
) -> dict[str, object]:
    """Refresh query-index rows for one record after an explicit mutation."""

    record = store.get_lifecycle_record(record_id)
    if record is None or not _belongs_to_context(record, context):
        return _operation_payload("refresh", False, [{"severity": "error", "code": "query_index_record_missing", "message": f"Research record not found for query-index refresh: {record_id}"}])
    payload = store.get_structured_payload(record_id)
    parts = _build_index_parts(context, record, payload)
    engine = _engine_for_db_path(store.db_path, read_only=False)
    try:
        with engine.begin() as connection:
            _replace_record_rows(connection, record_id, parts)
            replace_canonical_lineage_rows_for_record(connection, context, store, record_id)
    finally:
        engine.dispose()
    return _operation_payload("refresh", True, [], counts=_parts_counts(parts))


def rebuild_query_index(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    record_id: str | None = None,
    include_operation_set_files: bool = False,
    dry_run: bool = False,
) -> tuple[dict[str, object], list[Any]]:
    store, diagnostics = open_workspace_runtime(context, env=env, read_only=dry_run)
    if store is None:
        return _runtime_missing_payload("index.rebuild", diagnostics), diagnostics
    try:
        records = _selected_lifecycle_records(context, store, record_id)
        parts = [_build_index_parts(context, record, store.get_structured_payload(record.id)) for record in records]
        counts = _sum_counts(_parts_counts(part) for part in parts)
        payload: dict[str, object] = {
            "ok": True,
            "mutated": not dry_run,
            "operation": "index.rebuild",
            "dry_run": dry_run,
            "include_operation_set_files": include_operation_set_files,
            "record_count": len(records),
            "counts": counts,
            "diagnostics": [],
        }
        if dry_run:
            return payload, diagnostics
        engine = _engine_for_db_path(store.db_path, read_only=False)
        try:
            with engine.begin() as connection:
                for record, part in zip(records, parts, strict=True):
                    _replace_record_rows(connection, record.id, part)
                replace_all_canonical_lineage_rows(connection, context, store)
        finally:
            engine.dispose()
        return payload, diagnostics
    finally:
        store.close()


def validate_query_index(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    record_id: str | None = None,
) -> tuple[dict[str, object], list[Any]]:
    store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if store is None:
        return _runtime_missing_payload("index.validate", diagnostics), diagnostics
    try:
        index_diagnostics = _validate_index_rows(context, store, record_id=record_id)
        return {
            "ok": not any(item["severity"] == "error" for item in index_diagnostics),
            "mutated": False,
            "operation": "index.validate",
            "record_id": record_id,
            "diagnostics": index_diagnostics,
            "count": len(index_diagnostics),
        }, diagnostics
    finally:
        store.close()


def query_index_diagnostics_for_store(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
) -> list[dict[str, object]]:
    """Return query-index diagnostics for Workspace Runtime validation."""

    return _validate_index_rows(context, store)


def cleanup_query_index(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    stale_derived: bool = False,
    orphaned: bool = False,
    missing_files: bool = False,
    apply: bool = False,
) -> tuple[dict[str, object], list[Any]]:
    selectors = {
        "stale_derived": stale_derived,
        "orphaned": orphaned,
        "missing_files": missing_files,
    }
    if not any(selectors.values()):
        selectors = {**selectors, "stale_derived": True, "orphaned": True, "missing_files": True}
    store, diagnostics = open_workspace_runtime(context, env=env, read_only=not apply)
    if store is None:
        return _runtime_missing_payload("index.cleanup", diagnostics), diagnostics
    try:
        engine = _engine_for_db_path(store.db_path, read_only=not apply)
        plan = _cleanup_plan(context, store, engine, selectors)
        payload: dict[str, object] = {
            "ok": True,
            "mutated": apply,
            "operation": "index.cleanup",
            "apply": apply,
            "selectors": selectors,
            "plan": plan,
            "diagnostics": plan["diagnostics"],
        }
        if apply:
            _apply_cleanup_plan(engine, plan)
            payload["applied"] = True
        try:
            engine.dispose()
        finally:
            pass
        return payload, diagnostics
    finally:
        store.close()


def query_index_list(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    record_kind: str | None = None,
    status: str | None = None,
    profile: str | None = None,
    artifact_family: str | None = None,
    semantic_id: str | None = None,
    scope_key: str | None = None,
    unscoped_only: bool = False,
    procedure: str | None = None,
    latest_only: bool = False,
    facet: str | None = None,
    limit: int | None = None,
) -> tuple[dict[str, object], list[Any]]:
    if facet is not None and facet not in QUERY_FACETS:
        return _invalid_query_payload("query.list", f"Unsupported query facet: {facet}")
    if semantic_id is not None and not valid_semantic_id(semantic_id):
        return _invalid_query_payload("query.list", "Semantic id must use exact uppercase EXTENSION-NAME:WHAT syntax.")
    store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if store is None:
        return _runtime_missing_payload("query.list", diagnostics), diagnostics
    engine = _engine_for_db_path(store.db_path, read_only=True)
    try:
        try:
            rows = _query_records(
                engine,
                context,
                record_kind=record_kind,
                status=status,
                profile=profile,
                artifact_family=artifact_family,
                semantic_id=semantic_id,
                scope_key=scope_key,
                unscoped_only=unscoped_only,
                procedure=procedure,
                facet=facet,
                limit=limit,
            )
            latest_diagnostics: list[dict[str, object]] = []
            if latest_only:
                rows, latest_diagnostics = latest_record_candidates(rows)
            return {
                "ok": True,
                "mutated": False,
                "operation": "query.list",
                **index_revision_payload(engine, context),
                "count": len(rows),
                "records": rows,
                "latest_only": latest_only,
                "diagnostics": latest_diagnostics,
            }, diagnostics
        except OperationalError as exc:
            if not any(marker in str(exc).lower() for marker in ("no such column", "no such table")):
                raise
            return _query_index_schema_unavailable_payload("query.list", diagnostics)
    finally:
        engine.dispose()
        store.close()


def query_index_export(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    view: str = "graph",
) -> tuple[dict[str, object], list[Any]]:
    if view not in EXPORT_VIEWS:
        return _invalid_query_payload("query.export", f"Unsupported export view: {view}")
    store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if store is None:
        return _runtime_missing_payload("query.export", diagnostics), diagnostics
    engine = _engine_for_db_path(store.db_path, read_only=True)
    try:
        records = _query_records(engine, context)
        index_diagnostics = _validate_index_rows(context, store)
        legacy_ideas = _select_table(engine, record_ideas, context)
        canonical_idea_records = store.list_research_ideas(topic_workspace_id=context.topic_workspace_id)
        canonical_realization_records = store.list_research_idea_realizations(topic_workspace_id=context.topic_workspace_id)
        canonical_ideas, canonical_idea_source_diagnostics = canonical_ideas_with_source_status(
            context,
            store,
            canonical_idea_records,
            canonical_realization_records,
        )
        canonical_realizations, canonical_realization_source_diagnostics = canonical_realizations_with_source_status(
            context,
            store,
            canonical_idea_records,
            canonical_realization_records,
        )
        idea_diagnostics = idea_export_diagnostics(legacy_ideas, canonical_ideas)
        diagnostics_out = [*index_diagnostics, *idea_diagnostics, *canonical_idea_source_diagnostics, *canonical_realization_source_diagnostics]
        payload = {
            "ok": True,
            "mutated": False,
            "operation": "query.export",
            "view": view,
            **index_revision_payload(engine, context),
            "nodes": records,
            "edges": _select_table(engine, record_edges, context),
            "files": _select_table(engine, record_files, context),
            "ideas": [legacy_idea_facet(row, has_canonical=bool(canonical_ideas)) for row in legacy_ideas],
            "canonical_ideas": canonical_ideas,
            "canonical_idea_realizations": canonical_realizations,
            "canonical_idea_edges": [edge.to_json() for edge in store.list_research_idea_lineage_edges(topic_workspace_id=context.topic_workspace_id)],
            "canonical_idea_generation_groups": [group.to_json() for group in store.list_research_idea_generation_groups(topic_workspace_id=context.topic_workspace_id)],
            "routes": _select_table(engine, record_routes, context),
            "metrics": _select_table(engine, record_metrics, context),
            "claims": _select_table(engine, record_claims, context),
            "facts": _select_table(engine, record_json_facts, context),
            "diagnostics": diagnostics_out,
            "diagnostic_summary": _diagnostic_summary(diagnostics_out),
        }
        return payload, diagnostics
    finally:
        engine.dispose()
        store.close()


def query_index_lineage(
    context: EffectiveTopicContext,
    record_id: str,
    *,
    env: Mapping[str, str],
    direction: str = "both",
) -> tuple[dict[str, object], list[Any]]:
    if direction not in {"upstream", "downstream", "both"}:
        return _invalid_query_payload("query.lineage", f"Unsupported lineage direction: {direction}")
    store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if store is None:
        return _runtime_missing_payload("query.lineage", diagnostics), diagnostics
    engine = _engine_for_db_path(store.db_path, read_only=True)
    try:
        canonical_edges = canonical_lineage_edges_for_query(store, context, record_id, direction)
        has_canonical_lineage = bool(
            canonical_edges
            or store.list_research_record_lineage_edges(topic_workspace_id=context.topic_workspace_id, parent_record_id=record_id)
            or store.list_research_record_lineage_edges(topic_workspace_id=context.topic_workspace_id, child_record_id=record_id)
        )
        if has_canonical_lineage:
            node_ids = sorted({record_id, *(edge.parent_record_id for edge in canonical_edges), *(edge.child_record_id for edge in canonical_edges)})
            nodes = records_by_id_with_lifecycle_fallback(engine, store, context, node_ids)
            return {
                "ok": True,
                "mutated": False,
                "operation": "query.lineage",
                "record_id": record_id,
                "direction": direction,
                "lineage_source": "canonical",
                "nodes": nodes,
                "edges": [canonical_lineage_edge_json(edge) for edge in canonical_edges],
                "diagnostics": store.validate_research_record_lineage(topic_workspace_id=context.topic_workspace_id),
            }, diagnostics
        with engine.connect() as connection:
            conditions = []
            if direction in {"downstream", "both"}:
                conditions.append(record_edges.c.source_record_id == record_id)
            if direction in {"upstream", "both"}:
                conditions.append(record_edges.c.target_record_id == record_id)
            rows = connection.execute(
                select(record_edges).where(
                    record_edges.c.topic_workspace_id == context.topic_workspace_id,
                    or_(*conditions),
                )
            ).mappings()
            edges = [_row_dict(row) for row in rows]
        node_ids = sorted({record_id, *(str(edge["source_record_id"]) for edge in edges), *(str(edge["target_record_id"]) for edge in edges)})
        nodes = records_by_id(engine, context, node_ids)
        return {
            "ok": True,
            "mutated": False,
            "operation": "query.lineage",
            "record_id": record_id,
            "direction": direction,
            "lineage_source": "query-index",
            "nodes": nodes,
            "edges": edges,
            "diagnostics": [],
        }, diagnostics
    finally:
        engine.dispose()
        store.close()


def query_index_siblings(
    context: EffectiveTopicContext,
    record_id: str,
    *,
    env: Mapping[str, str],
) -> tuple[dict[str, object], list[Any]]:
    store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if store is None:
        return _runtime_missing_payload("query.siblings", diagnostics), diagnostics
    engine = _engine_for_db_path(store.db_path, read_only=True)
    try:
        record_edges_for_child = store.list_research_record_lineage_edges(
            topic_workspace_id=context.topic_workspace_id,
            child_record_id=record_id,
        )
        generation_ids = sorted({edge.generation_id for edge in record_edges_for_child if edge.generation_id is not None})
        sibling_edges: list[ResearchRecordLineageEdge] = []
        generation_groups: list[dict[str, object]] = []
        sibling_ids: set[str] = set()
        diag: list[dict[str, object]] = []
        for generation_id in generation_ids:
            group = store.get_research_record_generation_group(generation_id)
            if group is None:
                diag.append(_diag("warning", "lineage_generation_group_missing", f"Lineage generation group is missing: {generation_id}", generation_id=generation_id))
                continue
            generation_groups.append(group.to_json())
            for edge in store.list_research_record_lineage_edges(topic_workspace_id=context.topic_workspace_id, generation_id=generation_id):
                if edge.child_record_id == record_id:
                    continue
                sibling_edges.append(edge)
                sibling_ids.add(edge.child_record_id)
        return {
            "ok": True,
            "mutated": False,
            "operation": "query.siblings",
            "record_id": record_id,
            "generation_groups": generation_groups,
            "nodes": records_by_id_with_lifecycle_fallback(engine, store, context, sorted(sibling_ids)),
            "edges": [canonical_lineage_edge_json(edge) for edge in sibling_edges],
            "diagnostics": diag,
        }, diagnostics
    finally:
        engine.dispose()
        store.close()


def query_index_files(
    context: EffectiveTopicContext,
    record_id: str,
    *,
    env: Mapping[str, str],
) -> tuple[dict[str, object], list[Any]]:
    return _query_single_table(context, env=env, record_id=record_id, table=record_files, operation="query.files", result_key="files")


def query_index_facets(
    context: EffectiveTopicContext,
    record_id: str,
    *,
    env: Mapping[str, str],
    facet: str | None = None,
) -> tuple[dict[str, object], list[Any]]:
    if facet is not None and facet not in QUERY_FACETS:
        return _invalid_query_payload("query.facets", f"Unsupported query facet: {facet}")
    store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if store is None:
        return _runtime_missing_payload("query.facets", diagnostics), diagnostics
    engine = _engine_for_db_path(store.db_path, read_only=True)
    try:
        selected = [facet] if facet is not None else sorted(QUERY_FACETS)
        payload: dict[str, object] = {
            "ok": True,
            "mutated": False,
            "operation": "query.facets",
            "record_id": record_id,
            "diagnostics": [],
        }
        table_by_facet = {
            "ideas": record_ideas,
            "routes": record_routes,
            "metrics": record_metrics,
            "claims": record_claims,
            "facts": record_json_facts,
        }
        for name in selected:
            payload[name] = _select_record_table(engine, table_by_facet[name], context, record_id)
        return payload, diagnostics
    finally:
        engine.dispose()
        store.close()


def _selected_lifecycle_records(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    record_id: str | None,
) -> list[RuntimeLifecycleRecord]:
    payload_record_ids = {
        payload.record_id
        for payload in store.list_structured_payloads(topic_workspace_id=context.topic_workspace_id)
    }
    return [
        record
        for record in store.list_lifecycle_records()
        if _belongs_to_context(record, context) and (record_id is None or record.id == record_id)
        and (record.record_kind in QUERY_INDEX_RECORD_KINDS or record.id in payload_record_ids)
    ]


def _validate_index_rows(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    *,
    record_id: str | None = None,
) -> list[dict[str, object]]:
    diagnostics: list[dict[str, object]] = []
    engine = _engine_for_db_path(store.db_path, read_only=True)
    try:
        with engine.connect() as connection:
            missing_tables = [name for name in QUERY_INDEX_TABLE_NAMES if not _table_exists(connection, name)]
            for table_name in missing_tables:
                diagnostics.append(_diag("error", "query_index_table_missing", f"Query-index table is missing: {table_name}", table=table_name))
            if missing_tables:
                return diagnostics
            lifecycle = {record.id: record for record in _selected_lifecycle_records(context, store, record_id)}
            indexed = {
                str(row["record_id"]): row
                for row in connection.execute(
                    select(record_index).where(record_index.c.topic_workspace_id == context.topic_workspace_id)
                ).mappings()
                if record_id is None or row["record_id"] == record_id
            }
            payloads = {payload.record_id: payload for payload in store.list_structured_payloads(topic_workspace_id=context.topic_workspace_id)}
            for selected_id, record in lifecycle.items():
                row = indexed.get(selected_id)
                if row is None:
                    diagnostics.append(_diag("warning", "query_index_record_missing", f"Record is missing from query index: {selected_id}", record_id=selected_id))
                    continue
                if row["updated_at"] != record.updated_at:
                    diagnostics.append(_diag("warning", "query_index_record_stale", f"Indexed record is stale: {selected_id}", record_id=selected_id))
                payload = payloads.get(selected_id)
                if payload is not None and row["payload_digest"] != payload.payload_digest:
                    diagnostics.append(_diag("warning", "query_index_payload_stale", f"Indexed payload digest is stale: {selected_id}", record_id=selected_id))
            for edge in connection.execute(select(record_edges).where(record_edges.c.topic_workspace_id == context.topic_workspace_id)).mappings():
                if edge["relation_kind"] not in RELATION_KINDS and not str(edge["relation_kind"]).startswith("custom."):
                    diagnostics.append(_diag("error", "query_index_relation_kind_unsupported", f"Unsupported relation kind: {edge['relation_kind']}", edge_id=edge["id"]))
                if edge["source_record_id"] not in lifecycle:
                    diagnostics.append(_diag("error", "query_index_edge_source_missing", f"Edge source record is missing: {edge['source_record_id']}", edge_id=edge["id"]))
                if edge["target_record_id"] not in lifecycle:
                    diagnostics.append(_diag("warning", "query_index_edge_target_missing", f"Edge target record is missing: {edge['target_record_id']}", edge_id=edge["id"]))
            for file_row in connection.execute(select(record_files).where(record_files.c.topic_workspace_id == context.topic_workspace_id)).mappings():
                local_path = _resolve_local_path(context, str(file_row["path"]))
                exists = bool(local_path is not None and local_path.exists())
                if not exists:
                    diagnostics.append(_diag("warning", "query_index_file_missing", f"Indexed file is missing: {file_row['path']}", file_id=file_row["id"], record_id=file_row["record_id"]))
    finally:
        engine.dispose()
    return diagnostics


def _cleanup_plan(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    engine: Engine,
    selectors: Mapping[str, bool],
) -> dict[str, object]:
    lifecycle = {record.id: record for record in _selected_lifecycle_records(context, store, None)}
    payloads = {payload.record_id: payload for payload in store.list_structured_payloads(topic_workspace_id=context.topic_workspace_id)}
    stale_record_ids: set[str] = set()
    orphaned_record_ids: set[str] = set()
    file_ids: set[str] = set()
    diagnostics: list[dict[str, object]] = []
    with engine.connect() as connection:
        if any(not _table_exists(connection, name) for name in QUERY_INDEX_TABLE_NAMES):
            diagnostics.append(_diag("error", "query_index_table_missing", "Query-index cleanup cannot run until query-index tables exist."))
            return {"diagnostics": diagnostics, "tables": {}, "record_ids": []}
        for row in connection.execute(select(record_index).where(record_index.c.topic_workspace_id == context.topic_workspace_id)).mappings():
            record = lifecycle.get(str(row["record_id"]))
            if record is None:
                orphaned_record_ids.add(str(row["record_id"]))
                continue
            payload = payloads.get(record.id)
            if row["updated_at"] != record.updated_at or (payload is not None and row["payload_digest"] != payload.payload_digest):
                stale_record_ids.add(record.id)
        for row in connection.execute(select(record_files).where(record_files.c.topic_workspace_id == context.topic_workspace_id)).mappings():
            local_path = _resolve_local_path(context, str(row["path"]))
            if local_path is None or not local_path.exists():
                file_ids.add(str(row["id"]))
    target_record_ids = set()
    if selectors.get("stale_derived"):
        target_record_ids.update(stale_record_ids)
    if selectors.get("orphaned"):
        target_record_ids.update(orphaned_record_ids)
    tables: dict[str, int] = {}
    if target_record_ids:
        for table_name in ("research_record_index", "research_record_files", "research_record_ideas", "research_record_routes", "research_record_metrics", "research_record_claims", "research_record_json_facts"):
            tables[table_name] = len(target_record_ids)
        tables["research_record_edges"] = len(target_record_ids)
    if selectors.get("missing_files") and file_ids:
        tables["research_record_files"] = max(tables.get("research_record_files", 0), len(file_ids))
    return {
        "diagnostics": diagnostics,
        "tables": tables,
        "record_ids": sorted(target_record_ids),
        "file_ids": sorted(file_ids) if selectors.get("missing_files") else [],
        "skipped_rows": [],
        "source_classifications": [SOURCE_AUTHORED, SOURCE_PAYLOAD, SOURCE_FILE, SOURCE_BODY, SOURCE_CANONICAL_LINEAGE],
    }


def _apply_cleanup_plan(engine: Engine, plan: Mapping[str, object]) -> None:
    record_id_values = plan.get("record_ids")
    file_id_values = plan.get("file_ids")
    record_ids = [str(item) for item in record_id_values if isinstance(item, str)] if isinstance(record_id_values, list) else []
    file_ids = [str(item) for item in file_id_values if isinstance(item, str)] if isinstance(file_id_values, list) else []
    with engine.begin() as connection:
        if record_ids:
            connection.execute(delete(record_index).where(record_index.c.record_id.in_(record_ids)))
            connection.execute(delete(record_edges).where(or_(record_edges.c.source_record_id.in_(record_ids), record_edges.c.target_record_id.in_(record_ids))))
            for table in (record_files, record_ideas, record_routes, record_metrics, record_claims, record_json_facts):
                connection.execute(delete(table).where(table.c.record_id.in_(record_ids)))
        if file_ids:
            connection.execute(delete(record_files).where(record_files.c.id.in_(file_ids)))


def _query_records(
    engine: Engine,
    context: EffectiveTopicContext,
    *,
    record_kind: str | None = None,
    status: str | None = None,
    profile: str | None = None,
    artifact_family: str | None = None,
    semantic_id: str | None = None,
    scope_key: str | None = None,
    unscoped_only: bool = False,
    procedure: str | None = None,
    facet: str | None = None,
    limit: int | None = None,
) -> list[dict[str, object]]:
    conditions = [record_index.c.topic_workspace_id == context.topic_workspace_id]
    if record_kind is not None:
        conditions.append(record_index.c.record_kind == record_kind)
    if status is not None:
        conditions.append(record_index.c.status == status)
    if profile is not None:
        conditions.append(or_(record_index.c.profile == profile, record_index.c.format_profile_ref == profile))
    if artifact_family is not None:
        conditions.append(record_index.c.artifact_family == artifact_family)
    if semantic_id is not None:
        conditions.append(record_index.c.semantic_id == semantic_id)
    if scope_key is not None:
        conditions.append(record_index.c.scope_key == scope_key)
    elif unscoped_only:
        conditions.append(record_index.c.scope_key.is_(None))
    if procedure is not None:
        conditions.append(record_index.c.procedure == procedure)
    statement = select(record_index).where(and_(*conditions)).order_by(record_index.c.updated_at.desc(), record_index.c.record_id.asc())
    if limit is not None:
        statement = statement.limit(limit)
    with engine.connect() as connection:
        if not _table_exists(connection, "research_record_index"):
            return []
        rows = [_row_dict(row) for row in connection.execute(statement).mappings()]
    if facet is not None:
        rows = [row for row in rows if _record_has_facet(engine, context, str(row["record_id"]), facet)]
    return rows


def _record_has_facet(engine: Engine, context: EffectiveTopicContext, record_id: str, facet: str) -> bool:
    table = {
        "ideas": record_ideas,
        "routes": record_routes,
        "metrics": record_metrics,
        "claims": record_claims,
        "facts": record_json_facts,
    }[facet]
    with engine.connect() as connection:
        row = connection.execute(
            select(table.c.id).where(table.c.topic_workspace_id == context.topic_workspace_id, table.c.record_id == record_id).limit(1)
        ).fetchone()
    return row is not None


def _select_table(engine: Engine, table: Table, context: EffectiveTopicContext) -> list[dict[str, object]]:
    with engine.connect() as connection:
        if not _table_exists(connection, table.name):
            return []
        rows = connection.execute(select(table).where(table.c.topic_workspace_id == context.topic_workspace_id)).mappings()
        return _decorate_rows(context, table, [_row_dict(row) for row in rows])


def _select_record_table(engine: Engine, table: Table, context: EffectiveTopicContext, record_id: str) -> list[dict[str, object]]:
    with engine.connect() as connection:
        if not _table_exists(connection, table.name):
            return []
        rows = connection.execute(select(table).where(table.c.topic_workspace_id == context.topic_workspace_id, table.c.record_id == record_id)).mappings()
        return _decorate_rows(context, table, [_row_dict(row) for row in rows])


def _query_single_table(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    record_id: str,
    table: Table,
    operation: str,
    result_key: str,
) -> tuple[dict[str, object], list[Any]]:
    store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if store is None:
        return _runtime_missing_payload(operation, diagnostics), diagnostics
    engine = _engine_for_db_path(store.db_path, read_only=True)
    try:
        return {
            "ok": True,
            "mutated": False,
            "operation": operation,
            "record_id": record_id,
            result_key: _select_record_table(engine, table, context, record_id),
            "diagnostics": [],
        }, diagnostics
    finally:
        engine.dispose()
        store.close()


def _engine_for_db_path(db_path: Path, *, read_only: bool) -> Engine:
    if read_only:
        return create_engine(f"sqlite+pysqlite:///file:{db_path}?mode=ro&uri=true")
    return create_engine(f"sqlite+pysqlite:///{db_path}")


def _table_exists(connection: Any, table_name: str) -> bool:
    return connection.execute(
        text("SELECT name FROM sqlite_master WHERE type = 'table' AND name = :name"),
        {"name": table_name},
    ).fetchone() is not None


def _row_dict(row: Any) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in row.items():
        if key.endswith("_json") and isinstance(value, str):
            try:
                result[key[:-5]] = json.loads(value)
            except json.JSONDecodeError:
                result[key] = value
        elif key == "exists_flag":
            result["exists"] = bool(value)
        elif key == "stale" or key == "selected":
            result[key] = bool(value)
        else:
            result[key] = value
    return result


def _decorate_rows(context: EffectiveTopicContext, table: Table, rows: list[dict[str, object]]) -> list[dict[str, object]]:
    if table.name != "research_record_files":
        return rows
    return [_with_file_openability(context, row) for row in rows]


def _with_file_openability(context: EffectiveTopicContext, row: dict[str, object]) -> dict[str, object]:
    path_text = str(row.get("path") or "")
    if not path_text:
        return {**row, "resolved_path": None, "openable": False, "open_blocked_reason": "missing_locator"}
    if "://" in path_text:
        return {**row, "resolved_path": None, "openable": False, "open_blocked_reason": "external_locator"}
    local_path = _resolve_local_path(context, path_text)
    if local_path is None:
        return {**row, "resolved_path": None, "openable": False, "open_blocked_reason": "unresolved_locator"}
    resolved = local_path.resolve(strict=False)
    allowed_roots = (context.project.root.resolve(strict=False), context.topic_workspace_path.resolve(strict=False))
    if not any(_is_relative_to(resolved, root) for root in allowed_roots):
        return {**row, "resolved_path": str(resolved), "openable": False, "open_blocked_reason": "outside_project"}
    if not resolved.exists():
        return {**row, "resolved_path": str(resolved), "openable": False, "open_blocked_reason": "missing"}
    if not resolved.is_file():
        return {**row, "resolved_path": str(resolved), "openable": False, "open_blocked_reason": "not_file"}
    return {**row, "resolved_path": str(resolved), "exists": True, "openable": True, "open_blocked_reason": None}


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _diagnostic_summary(diagnostics: list[dict[str, object]]) -> dict[str, object]:
    grouped: dict[tuple[str, str], int] = {}
    for diagnostic in diagnostics:
        severity = str(diagnostic.get("severity") or "unknown")
        code = str(diagnostic.get("code") or "unknown")
        grouped[(severity, code)] = grouped.get((severity, code), 0) + 1
    by_code = [
        {"severity": severity, "code": code, "count": count}
        for (severity, code), count in sorted(grouped.items(), key=lambda item: (item[0][0], item[0][1]))
    ]
    return {"total": len(diagnostics), "by_code": by_code}


def _operation_payload(operation: str, mutated: bool, diagnostics: list[dict[str, object]], *, counts: dict[str, int] | None = None) -> dict[str, object]:
    payload: dict[str, object] = {
        "ok": not any(item.get("severity") == "error" for item in diagnostics),
        "mutated": mutated,
        "operation": operation,
        "diagnostics": diagnostics,
    }
    if counts is not None:
        payload["counts"] = counts
    return payload


def _runtime_missing_payload(operation: str, diagnostics: list[Any]) -> dict[str, object]:
    return {
        "ok": False,
        "mutated": False,
        "operation": operation,
        "error": {
            "code": "workspace_runtime_missing",
            "message": "Workspace Runtime must be initialized before research record query-index operations can run.",
        },
        "diagnostics": [diagnostic.to_json() for diagnostic in diagnostics],
    }


def _belongs_to_context(record: RuntimeLifecycleRecord, context: EffectiveTopicContext) -> bool:
    return record.research_topic_id == context.research_topic.id and record.topic_workspace_id == context.topic_workspace_id
