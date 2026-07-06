"""Read-only freshness metadata for the research record query index."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from sqlalchemy import func, select, text
from sqlalchemy.engine import Engine

from isomer_labs.models import EffectiveTopicContext

from .index_schema import (
    record_claims,
    record_edges,
    record_files,
    record_ideas,
    record_index,
    record_json_facts,
    record_metrics,
    record_routes,
)


def index_revision_payload(engine: Engine, context: EffectiveTopicContext) -> dict[str, object]:
    table_state = _index_revision_table_state(engine, context)
    encoded = json.dumps(
        {
            "topic_workspace_id": context.topic_workspace_id,
            "tables": table_state,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:20]
    return {
        "index_revision": f"qidx:{digest}",
        "index_revision_state": table_state,
    }


def _index_revision_table_state(engine: Engine, context: EffectiveTopicContext) -> list[dict[str, object]]:
    tables = (
        record_index,
        record_edges,
        record_files,
        record_ideas,
        record_routes,
        record_metrics,
        record_claims,
        record_json_facts,
    )
    state: list[dict[str, object]] = []
    with engine.connect() as connection:
        for table in tables:
            if not _table_exists(connection, table.name):
                state.append({"table": table.name, "exists": False, "count": 0, "max_changed_at": None})
                continue
            timestamp_column = None
            for column_name in ("indexed_at", "updated_at", "created_at"):
                if column_name in table.c:
                    timestamp_column = table.c[column_name]
                    break
            count_label = "row_count"
            max_label = "max_changed_at"
            if timestamp_column is None:
                count_statement = select(func.count().label(count_label)).where(table.c.topic_workspace_id == context.topic_workspace_id)
                row = connection.execute(count_statement).mappings().one()
                state.append({"table": table.name, "exists": True, "count": int(row[count_label]), "max_changed_at": None})
                continue
            timestamp_statement = select(
                func.count().label(count_label),
                func.max(timestamp_column).label(max_label),
            ).where(table.c.topic_workspace_id == context.topic_workspace_id)
            row = connection.execute(timestamp_statement).mappings().one()
            state.append(
                {
                    "table": table.name,
                    "exists": True,
                    "count": int(row[count_label]),
                    "max_changed_at": row[max_label],
                }
            )
    return state


def _table_exists(connection: Any, table_name: str) -> bool:
    return connection.execute(
        text("SELECT name FROM sqlite_master WHERE type = 'table' AND name = :name"),
        {"name": table_name},
    ).fetchone() is not None
