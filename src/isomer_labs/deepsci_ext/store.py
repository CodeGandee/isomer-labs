"""SQLite persistence for DeepScientist compatibility mocks."""

from __future__ import annotations

from dataclasses import dataclass
import json
import sqlite3
from typing import Any, Iterable

from isomer_labs.models import EffectiveTopicContext
from isomer_labs.runtime.records import utc_timestamp
from isomer_labs.runtime.store import WorkspaceRuntimeStore


def dumps_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def loads_object(value: str | None) -> dict[str, Any]:
    if not value:
        return {}
    loaded = json.loads(value)
    return loaded if isinstance(loaded, dict) else {}


def loads_list(value: str | None) -> list[str]:
    if not value:
        return []
    loaded = json.loads(value)
    if not isinstance(loaded, list):
        return []
    return [str(item) for item in loaded if str(item).strip()]


def _bool_to_int(value: bool) -> int:
    return 1 if value else 0


def _int_to_bool(value: object) -> bool:
    try:
        return int(str(value or 0)) != 0
    except (TypeError, ValueError):
        return False


@dataclass(frozen=True)
class StoredMemoryCard:
    id: str
    scope: str
    kind: str
    title: str
    body: str
    path: str
    document_id: str
    metadata: dict[str, Any]
    tags: list[str]
    created_at: str
    updated_at: str
    writable: bool
    shared: bool
    source_quest_id: str | None


@dataclass(frozen=True)
class StoredBashSession:
    bash_id: str
    command: str
    status: str
    kind: str | None
    comment: object | None
    label: str | None
    workdir: str | None
    cwd: str
    log_path: str
    started_at: str
    finished_at: str | None
    exit_code: int | None
    stop_reason: str | None
    last_progress: str | None
    last_progress_at: str | None
    last_output_at: str | None
    last_output_seq: int
    metadata: dict[str, Any]


class DeepSciCompatStore:
    """Extension-owned tables inside a Workspace Runtime database."""

    def __init__(self, runtime_store: WorkspaceRuntimeStore) -> None:
        self.runtime_store = runtime_store
        self.connection = runtime_store.connection
        self.db_path = runtime_store.db_path
        self.connection.row_factory = sqlite3.Row

    def close(self) -> None:
        self.runtime_store.close()

    def ensure_schema(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS deepsci_compat_memory_cards (
                id TEXT PRIMARY KEY,
                research_topic_id TEXT NOT NULL,
                topic_workspace_id TEXT NOT NULL,
                scope TEXT NOT NULL,
                kind TEXT NOT NULL,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                path TEXT NOT NULL UNIQUE,
                document_id TEXT NOT NULL,
                metadata_json TEXT NOT NULL,
                tags_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                writable INTEGER NOT NULL,
                shared INTEGER NOT NULL,
                source_quest_id TEXT
            );

            CREATE TABLE IF NOT EXISTS deepsci_compat_artifact_calls (
                sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                id TEXT NOT NULL UNIQUE,
                research_topic_id TEXT NOT NULL,
                topic_workspace_id TEXT NOT NULL,
                tool_name TEXT NOT NULL,
                request_json TEXT NOT NULL,
                response_json TEXT NOT NULL,
                mocked INTEGER NOT NULL,
                context_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS deepsci_compat_artifact_records (
                id TEXT PRIMARY KEY,
                research_topic_id TEXT NOT NULL,
                topic_workspace_id TEXT NOT NULL,
                artifact_kind TEXT,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS deepsci_compat_bash_sessions (
                bash_id TEXT PRIMARY KEY,
                research_topic_id TEXT NOT NULL,
                topic_workspace_id TEXT NOT NULL,
                command TEXT NOT NULL,
                status TEXT NOT NULL,
                kind TEXT,
                comment_json TEXT,
                label TEXT,
                workdir TEXT,
                cwd TEXT NOT NULL,
                log_path TEXT NOT NULL,
                started_at TEXT NOT NULL,
                finished_at TEXT,
                exit_code INTEGER,
                stop_reason TEXT,
                last_progress TEXT,
                last_progress_at TEXT,
                last_output_at TEXT,
                last_output_seq INTEGER NOT NULL DEFAULT 0,
                metadata_json TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS deepsci_compat_bash_log_entries (
                sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                bash_id TEXT NOT NULL,
                stream TEXT NOT NULL,
                text TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )

    def insert_memory_card(
        self,
        context: EffectiveTopicContext,
        *,
        card_id: str,
        scope: str,
        kind: str,
        title: str,
        body: str,
        path: str,
        document_id: str,
        metadata: dict[str, Any],
        tags: list[str],
        created_at: str,
        updated_at: str,
        writable: bool,
        shared: bool,
        source_quest_id: str | None,
    ) -> StoredMemoryCard:
        with self.connection:
            self.connection.execute(
                """
                INSERT INTO deepsci_compat_memory_cards
                    (
                        id, research_topic_id, topic_workspace_id, scope, kind, title,
                        body, path, document_id, metadata_json, tags_json, created_at,
                        updated_at, writable, shared, source_quest_id
                    )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    scope = excluded.scope,
                    kind = excluded.kind,
                    title = excluded.title,
                    body = excluded.body,
                    path = excluded.path,
                    document_id = excluded.document_id,
                    metadata_json = excluded.metadata_json,
                    tags_json = excluded.tags_json,
                    updated_at = excluded.updated_at,
                    writable = excluded.writable,
                    shared = excluded.shared,
                    source_quest_id = excluded.source_quest_id
                """,
                (
                    card_id,
                    context.research_topic.id,
                    context.topic_workspace_id,
                    scope,
                    kind,
                    title,
                    body,
                    path,
                    document_id,
                    dumps_json(metadata),
                    dumps_json(tags),
                    created_at,
                    updated_at,
                    _bool_to_int(writable),
                    _bool_to_int(shared),
                    source_quest_id,
                ),
            )
        card = self.get_memory_card(card_id=card_id)
        if card is None:
            raise RuntimeError(f"DeepScientist compatibility memory card was not stored: {card_id}")
        return card

    def get_memory_card(self, *, card_id: str | None = None, path: str | None = None) -> StoredMemoryCard | None:
        row: sqlite3.Row | None = None
        if card_id:
            row = self.connection.execute(
                "SELECT * FROM deepsci_compat_memory_cards WHERE id = ?",
                (card_id,),
            ).fetchone()
        if row is None and path:
            row = self.connection.execute(
                "SELECT * FROM deepsci_compat_memory_cards WHERE path = ? OR document_id = ?",
                (path, path),
            ).fetchone()
        return self._row_to_memory_card(row) if row is not None else None

    def list_memory_cards(
        self,
        context: EffectiveTopicContext,
        *,
        scopes: Iterable[str],
        kind: str | None = None,
    ) -> list[StoredMemoryCard]:
        selected_scopes = tuple(scopes)
        if not selected_scopes:
            return []
        placeholders = ", ".join("?" for _ in selected_scopes)
        params: list[object] = [
            context.research_topic.id,
            context.topic_workspace_id,
            *selected_scopes,
        ]
        query = f"""
            SELECT * FROM deepsci_compat_memory_cards
            WHERE research_topic_id = ?
              AND topic_workspace_id = ?
              AND scope IN ({placeholders})
        """
        if kind:
            query += " AND kind = ?"
            params.append(kind)
        query += " ORDER BY updated_at DESC, path DESC"
        return [
            self._row_to_memory_card(row)
            for row in self.connection.execute(query, tuple(params))
        ]

    def update_memory_scope(
        self,
        *,
        card_id: str,
        scope: str,
        metadata: dict[str, Any],
        updated_at: str,
    ) -> StoredMemoryCard | None:
        with self.connection:
            self.connection.execute(
                """
                UPDATE deepsci_compat_memory_cards
                SET scope = ?, metadata_json = ?, updated_at = ?, shared = ?
                WHERE id = ?
                """,
                (scope, dumps_json(metadata), updated_at, _bool_to_int(scope == "global"), card_id),
            )
        return self.get_memory_card(card_id=card_id)

    def record_artifact_call(
        self,
        context: EffectiveTopicContext,
        *,
        call_id: str,
        tool_name: str,
        request: dict[str, Any],
        response: dict[str, Any],
        mocked: bool,
        created_at: str | None = None,
    ) -> None:
        timestamp = created_at or utc_timestamp()
        context_payload = {
            "project_root": str(context.project.root),
            "research_topic_id": context.research_topic.id,
            "topic_workspace_id": context.topic_workspace_id,
            "topic_workspace_path": str(context.topic_workspace_path),
        }
        with self.connection:
            self.connection.execute(
                """
                INSERT INTO deepsci_compat_artifact_calls
                    (
                        id, research_topic_id, topic_workspace_id, tool_name,
                        request_json, response_json, mocked, context_json, created_at
                    )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    call_id,
                    context.research_topic.id,
                    context.topic_workspace_id,
                    tool_name,
                    dumps_json(request),
                    dumps_json(response),
                    _bool_to_int(mocked),
                    dumps_json(context_payload),
                    timestamp,
                ),
            )

    def record_artifact_record(
        self,
        context: EffectiveTopicContext,
        *,
        artifact_id: str,
        artifact_kind: str | None,
        payload: dict[str, Any],
        created_at: str | None = None,
    ) -> None:
        with self.connection:
            self.connection.execute(
                """
                INSERT OR REPLACE INTO deepsci_compat_artifact_records
                    (id, research_topic_id, topic_workspace_id, artifact_kind, payload_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    artifact_id,
                    context.research_topic.id,
                    context.topic_workspace_id,
                    artifact_kind,
                    dumps_json(payload),
                    created_at or utc_timestamp(),
                ),
            )

    def count_artifact_calls(self, *, tool_name: str | None = None) -> int:
        if tool_name is None:
            row = self.connection.execute("SELECT COUNT(*) AS count FROM deepsci_compat_artifact_calls").fetchone()
        else:
            row = self.connection.execute(
                "SELECT COUNT(*) AS count FROM deepsci_compat_artifact_calls WHERE tool_name = ?",
                (tool_name,),
            ).fetchone()
        return int(row["count"]) if row is not None else 0

    def upsert_bash_session(
        self,
        context: EffectiveTopicContext,
        *,
        session: StoredBashSession,
    ) -> StoredBashSession:
        with self.connection:
            self.connection.execute(
                """
                INSERT INTO deepsci_compat_bash_sessions
                    (
                        bash_id, research_topic_id, topic_workspace_id, command, status,
                        kind, comment_json, label, workdir, cwd, log_path, started_at,
                        finished_at, exit_code, stop_reason, last_progress, last_progress_at,
                        last_output_at, last_output_seq, metadata_json
                    )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(bash_id) DO UPDATE SET
                    command = excluded.command,
                    status = excluded.status,
                    kind = excluded.kind,
                    comment_json = excluded.comment_json,
                    label = excluded.label,
                    workdir = excluded.workdir,
                    cwd = excluded.cwd,
                    log_path = excluded.log_path,
                    finished_at = excluded.finished_at,
                    exit_code = excluded.exit_code,
                    stop_reason = excluded.stop_reason,
                    last_progress = excluded.last_progress,
                    last_progress_at = excluded.last_progress_at,
                    last_output_at = excluded.last_output_at,
                    last_output_seq = excluded.last_output_seq,
                    metadata_json = excluded.metadata_json
                """,
                (
                    session.bash_id,
                    context.research_topic.id,
                    context.topic_workspace_id,
                    session.command,
                    session.status,
                    session.kind,
                    dumps_json(session.comment),
                    session.label,
                    session.workdir,
                    session.cwd,
                    session.log_path,
                    session.started_at,
                    session.finished_at,
                    session.exit_code,
                    session.stop_reason,
                    session.last_progress,
                    session.last_progress_at,
                    session.last_output_at,
                    session.last_output_seq,
                    dumps_json(session.metadata),
                ),
            )
        stored = self.get_bash_session(session.bash_id)
        if stored is None:
            raise RuntimeError(f"DeepScientist compatibility bash session was not stored: {session.bash_id}")
        return stored

    def add_bash_log_entry(
        self,
        *,
        bash_id: str,
        text: str,
        stream: str = "stdout",
        created_at: str | None = None,
    ) -> int:
        with self.connection:
            cursor = self.connection.execute(
                """
                INSERT INTO deepsci_compat_bash_log_entries (bash_id, stream, text, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (bash_id, stream, text, created_at or utc_timestamp()),
            )
        return int(cursor.lastrowid or 0)

    def get_bash_session(self, bash_id: str) -> StoredBashSession | None:
        row = self.connection.execute(
            "SELECT * FROM deepsci_compat_bash_sessions WHERE bash_id = ?",
            (bash_id,),
        ).fetchone()
        return self._row_to_bash_session(row) if row is not None else None

    def latest_bash_session(self) -> StoredBashSession | None:
        row = self.connection.execute(
            "SELECT * FROM deepsci_compat_bash_sessions ORDER BY started_at DESC, bash_id DESC LIMIT 1"
        ).fetchone()
        return self._row_to_bash_session(row) if row is not None else None

    def list_bash_sessions(
        self,
        context: EffectiveTopicContext,
        *,
        status: str | None = None,
        kind: str | None = None,
        limit: int = 20,
    ) -> list[StoredBashSession]:
        params: list[object] = [context.research_topic.id, context.topic_workspace_id]
        query = """
            SELECT * FROM deepsci_compat_bash_sessions
            WHERE research_topic_id = ? AND topic_workspace_id = ?
        """
        if status:
            query += " AND status = ?"
            params.append(status)
        if kind:
            query += " AND kind = ?"
            params.append(kind)
        query += " ORDER BY started_at DESC, bash_id DESC LIMIT ?"
        params.append(max(1, min(int(limit), 500)))
        return [
            self._row_to_bash_session(row)
            for row in self.connection.execute(query, tuple(params))
        ]

    def bash_log_entries(
        self,
        *,
        bash_id: str,
        order: str = "asc",
        limit: int | None = None,
    ) -> list[sqlite3.Row]:
        selected_order = "DESC" if order == "desc" else "ASC"
        query = f"""
            SELECT * FROM deepsci_compat_bash_log_entries
            WHERE bash_id = ?
            ORDER BY sequence {selected_order}
        """
        params: list[object] = [bash_id]
        if limit is not None:
            query += " LIMIT ?"
            params.append(max(1, int(limit)))
        return list(self.connection.execute(query, tuple(params)))

    def mark_bash_session_stopped(self, *, bash_id: str, reason: str | None) -> StoredBashSession | None:
        timestamp = utc_timestamp()
        with self.connection:
            self.connection.execute(
                """
                UPDATE deepsci_compat_bash_sessions
                SET status = 'stopped', finished_at = ?, stop_reason = ?
                WHERE bash_id = ?
                """,
                (timestamp, reason or "mock kill requested", bash_id),
            )
        return self.get_bash_session(bash_id)

    @staticmethod
    def _row_to_memory_card(row: sqlite3.Row) -> StoredMemoryCard:
        return StoredMemoryCard(
            id=str(row["id"]),
            scope=str(row["scope"]),
            kind=str(row["kind"]),
            title=str(row["title"]),
            body=str(row["body"]),
            path=str(row["path"]),
            document_id=str(row["document_id"]),
            metadata=loads_object(str(row["metadata_json"])),
            tags=loads_list(str(row["tags_json"])),
            created_at=str(row["created_at"]),
            updated_at=str(row["updated_at"]),
            writable=_int_to_bool(row["writable"]),
            shared=_int_to_bool(row["shared"]),
            source_quest_id=str(row["source_quest_id"]) if row["source_quest_id"] is not None else None,
        )

    @staticmethod
    def _row_to_bash_session(row: sqlite3.Row) -> StoredBashSession:
        return StoredBashSession(
            bash_id=str(row["bash_id"]),
            command=str(row["command"]),
            status=str(row["status"]),
            kind=str(row["kind"]) if row["kind"] is not None else None,
            comment=json.loads(str(row["comment_json"])) if row["comment_json"] else None,
            label=str(row["label"]) if row["label"] is not None else None,
            workdir=str(row["workdir"]) if row["workdir"] is not None else None,
            cwd=str(row["cwd"]),
            log_path=str(row["log_path"]),
            started_at=str(row["started_at"]),
            finished_at=str(row["finished_at"]) if row["finished_at"] is not None else None,
            exit_code=int(row["exit_code"]) if row["exit_code"] is not None else None,
            stop_reason=str(row["stop_reason"]) if row["stop_reason"] is not None else None,
            last_progress=str(row["last_progress"]) if row["last_progress"] is not None else None,
            last_progress_at=str(row["last_progress_at"]) if row["last_progress_at"] is not None else None,
            last_output_at=str(row["last_output_at"]) if row["last_output_at"] is not None else None,
            last_output_seq=int(row["last_output_seq"] or 0),
            metadata=loads_object(str(row["metadata_json"])),
        )


def compatibility_table_names(connection: sqlite3.Connection) -> list[str]:
    return [
        str(row["name"])
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name LIKE 'deepsci_compat_%' ORDER BY name"
        )
    ]
