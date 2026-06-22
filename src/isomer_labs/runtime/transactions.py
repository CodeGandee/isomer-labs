"""Transaction helpers for Workspace Runtime stores."""

from __future__ import annotations

import sqlite3
from typing import Any, Callable


def _table_names(connection: sqlite3.Connection) -> set[str]:
    return {
        row["name"]
        for row in connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    }


def _table_exists(connection: sqlite3.Connection, table_name: str) -> bool:
    return table_name in _table_names(connection)


def run_runtime_transaction(
    store: Any,
    callback: Callable[[Any], None],
) -> None:
    """Run a caller-supplied mutation inside the store transaction boundary."""

    with store.connection:
        callback(store)
