"""Family-neutral research-record identity query helpers."""

from __future__ import annotations

import json
import re
from typing import Any, Iterable, Mapping

from sqlalchemy import create_engine, select, text

from isomer_labs.models import EffectiveTopicContext
from isomer_labs.runtime.store import open_workspace_runtime

from .index_schema import record_index


SEMANTIC_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*:[a-z0-9][a-z0-9-]*$")


def valid_semantic_id(value: str) -> bool:
    """Return whether a semantic id uses canonical family syntax."""

    return SEMANTIC_ID_RE.fullmatch(value) is not None


def invalid_query_payload(operation: str, message: str) -> tuple[dict[str, object], list[Any]]:
    """Build a deterministic invalid-query response."""

    return {
        "ok": False,
        "mutated": False,
        "operation": operation,
        "error": {"code": "invalid_query_index_request", "message": message},
        "diagnostics": [],
    }, []


def index_diagnostic(severity: str, code: str, message: str, **details: object) -> dict[str, object]:
    """Build one query-index diagnostic mapping."""

    return {"severity": severity, "code": code, "message": message, **details}


def latest_record_candidates(
    rows: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Select explicit latest candidates and retain ambiguous competitors."""

    grouped: dict[str, list[dict[str, object]]] = {}
    ungrouped: list[dict[str, object]] = []
    for row in rows:
        semantic_id = row.get("semantic_id") or row.get("latest_for_semantic_id")
        if not isinstance(semantic_id, str) or not semantic_id:
            ungrouped.append(row)
            continue
        grouped.setdefault(semantic_id, []).append(row)
    selected = list(ungrouped)
    diagnostics: list[dict[str, object]] = []
    for semantic_id, candidates in sorted(grouped.items()):
        superseded = {
            str(candidate["supersedes_record_id"])
            for candidate in candidates
            if candidate.get("supersedes_record_id")
        }
        active = [
            candidate
            for candidate in candidates
            if candidate.get("record_id") not in superseded and candidate.get("status") != "archived"
        ]
        if not active:
            active = [candidate for candidate in candidates if candidate.get("record_id") not in superseded]
        if len(active) > 1:
            record_ids = sorted(str(candidate["record_id"]) for candidate in active)
            diagnostics.append(
                {
                    "severity": "warning",
                    "code": "query_index_latest_ambiguous",
                    "message": f"Semantic id {semantic_id} has competing latest candidates: {', '.join(record_ids)}.",
                    "semantic_id": semantic_id,
                    "record_ids": record_ids,
                }
            )
            for candidate in active:
                candidate["latest_ambiguity"] = True
        selected.extend(active)
    return sorted(
        selected,
        key=lambda row: (str(row.get("updated_at") or ""), str(row.get("record_id") or "")),
        reverse=True,
    ), diagnostics


def query_index_record_summary(
    context: EffectiveTopicContext,
    record_id: str,
    *,
    env: Mapping[str, str],
) -> tuple[dict[str, object], list[Any]]:
    """Read one generic indexed record summary by stable record id."""

    store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if store is None:
        return {
            "ok": False,
            "mutated": False,
            "operation": "query.record",
            "record_id": record_id,
            "record": None,
            "diagnostics": [],
        }, diagnostics
    engine = create_engine(f"sqlite+pysqlite:///file:{store.db_path}?mode=ro&uri=true")
    try:
        with engine.connect() as connection:
            exists = connection.execute(
                text("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'research_record_index'")
            ).fetchone()
            row = None
            if exists is not None:
                row = connection.execute(
                    select(record_index).where(
                        record_index.c.topic_workspace_id == context.topic_workspace_id,
                        record_index.c.record_id == record_id,
                    )
                ).mappings().fetchone()
        return {
            "ok": row is not None,
            "mutated": False,
            "operation": "query.record",
            "record_id": record_id,
            "record": _row_dict(row) if row is not None else None,
            "diagnostics": [],
        }, diagnostics
    finally:
        engine.dispose()
        store.close()


def records_by_id(
    engine: Any,
    context: EffectiveTopicContext,
    record_ids: Iterable[str],
) -> list[dict[str, object]]:
    """Read indexed summaries for stable record ids."""

    ids = list(record_ids)
    if not ids:
        return []
    with engine.connect() as connection:
        rows = connection.execute(
            select(record_index).where(
                record_index.c.topic_workspace_id == context.topic_workspace_id,
                record_index.c.record_id.in_(ids),
            )
        ).mappings()
        return [_row_dict(row) for row in rows]


def _row_dict(row: Any) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in row.items():
        if key.endswith("_json") and isinstance(value, str):
            try:
                result[key[:-5]] = json.loads(value)
            except json.JSONDecodeError:
                result[key] = value
        else:
            result[key] = value
    return result
