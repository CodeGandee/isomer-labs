"""Rebuildable local projection for canonical literature observations."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shlex
import sqlite3
from typing import Mapping

from isomer_labs.artifact_formats.models import digest_json
from isomer_labs.artifact_formats.research_record_formats import (
    LITERATURE_OBSERVATION_PROFILE_REF,
)
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.records.literature_contract import (
    PAPER_KEY_RE,
    mapping,
    normalized_optional_arxiv_id,
    normalized_optional_doi,
    object_array,
    optional_string,
    read_structured_payload,
    validate_observation_contract,
)
from isomer_labs.records.store import ResearchRecordError
from isomer_labs.runtime.records import StructuredResearchPayloadRecord, utc_timestamp
from isomer_labs.runtime.store import WorkspaceRuntimeStore, open_workspace_runtime


LITERATURE_QUERY_INDEX_SCHEMA_VERSION = "isomer-literature-query-index.v1"
LITERATURE_PROJECTION_ID = "literature-query-index"
LITERATURE_TABLES = {
    "literature_projection_metadata",
    "literature_observation_index",
    "literature_paper_occurrences",
    "literature_citation_edges",
}


def refresh_projection_after_commit(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
) -> dict[str, object]:
    """Refresh a compatible projection without weakening the canonical commit."""

    store, diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    if store is None:
        return {
            "status": "unavailable",
            "refreshed": False,
            "diagnostics": [item.to_json() for item in diagnostics],
            "rebuild_command": rebuild_command(context),
        }
    try:
        posture = projection_posture(store, context)
        if not posture["schema_compatible"]:
            return {
                **posture,
                "refreshed": False,
                "canonical_commit_preserved": True,
            }
        source, skipped = projection_source(store, context)
        try:
            with store.connection:
                clear_projection_rows(store.connection)
                counts = write_projection(store, context, source)
        except sqlite3.Error as exc:
            return {
                **posture,
                "status": "refresh-failed",
                "refreshed": False,
                "canonical_commit_preserved": True,
                "error": str(exc),
                "rebuild_command": rebuild_command(context),
            }
        return {
            **projection_posture(store, context),
            "refreshed": True,
            "counts": counts,
            "skipped_observations": skipped,
            "canonical_commit_preserved": True,
        }
    finally:
        store.close()


def projection_source(
    store: WorkspaceRuntimeStore,
    context: EffectiveTopicContext,
) -> tuple[list[tuple[StructuredResearchPayloadRecord, dict[str, object]]], list[dict[str, object]]]:
    """Return valid canonical observation payloads and deterministic skip reasons."""

    source: list[tuple[StructuredResearchPayloadRecord, dict[str, object]]] = []
    skipped: list[dict[str, object]] = []
    for structured in store.list_structured_payloads(
        topic_workspace_id=context.topic_workspace_id,
        format_profile_ref=LITERATURE_OBSERVATION_PROFILE_REF,
    ):
        reason: str | None = None
        payload: dict[str, object] | None = None
        record = store.get_lifecycle_record(structured.record_id)
        if record is None:
            reason = "source-lifecycle-record-missing"
        elif structured.validation_status != "valid":
            reason = f"structured-validation-{structured.validation_status}"
        else:
            try:
                payload = read_structured_payload(structured)
            except ResearchRecordError as exc:
                reason = exc.code
            if payload is not None and digest_json(payload) != structured.payload_digest:
                reason = "payload-digest-drift"
            if payload is not None and reason is None:
                try:
                    attachment_base = (
                        Path(structured.payload_file_path).parent
                        if structured.payload_file_path is not None
                        else store.db_path.parent
                    )
                    validate_observation_contract(
                        payload,
                        attachment_base=attachment_base,
                        check_attachments=False,
                    )
                except ResearchRecordError as exc:
                    reason = exc.code
        if reason is not None or payload is None:
            skipped.append({"observation_id": structured.record_id, "reason": reason or "payload-unavailable"})
            continue
        source.append((structured, payload))
    source.sort(key=lambda item: item[0].record_id)
    skipped.sort(key=lambda item: str(item["observation_id"]))
    return source, skipped


def write_projection(
    store: WorkspaceRuntimeStore,
    context: EffectiveTopicContext,
    source: list[tuple[StructuredResearchPayloadRecord, dict[str, object]]],
) -> dict[str, int]:
    """Write deterministic derived rows for a validated source snapshot."""

    paper_count = 0
    edge_count = 0
    for structured, payload in source:
        provider = mapping(payload["provider"])
        completeness = mapping(payload["completeness"])
        store.connection.execute(
            """
            INSERT INTO literature_observation_index
                (
                    source_record_id, payload_digest, observation_time, action,
                    provider_name, completeness_status, payload_file_path
                )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                structured.record_id,
                structured.payload_digest,
                str(payload["observation_time"]),
                str(payload["action"]),
                str(provider["name"]),
                str(completeness["status"]),
                structured.payload_file_path,
            ),
        )
        unique_papers: dict[str, Mapping[str, object]] = {}
        for paper in object_array(payload["papers"]):
            unique_papers[str(paper["paper_key"])] = paper
        for paper_key, paper in sorted(unique_papers.items()):
            qualified = paper.get("provider_qualified_id")
            provider_name = None
            provider_id = None
            if isinstance(qualified, Mapping):
                provider_name = optional_string(qualified.get("provider"))
                provider_id = optional_string(qualified.get("id"))
            occurrence_id = _stable_id("literature-paper", structured.record_id, paper_key)
            store.connection.execute(
                """
                INSERT INTO literature_paper_occurrences
                    (
                        occurrence_id, source_record_id, payload_digest, observation_time,
                        paper_key, doi, arxiv_id, provider_name, provider_id, title,
                        publication_year, locator, paper_json
                    )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    occurrence_id,
                    structured.record_id,
                    structured.payload_digest,
                    str(payload["observation_time"]),
                    paper_key,
                    normalized_optional_doi(paper.get("doi")),
                    normalized_optional_arxiv_id(paper.get("arxiv_id")),
                    provider_name,
                    provider_id,
                    optional_string(paper.get("title")),
                    paper.get("publication_year"),
                    optional_string(paper.get("locator")),
                    _canonical_json(paper),
                ),
            )
            paper_count += 1
        unique_edges: dict[str, Mapping[str, object]] = {}
        for edge in object_array(payload["citation_edges"]):
            edge_key = _canonical_json(edge)
            unique_edges[edge_key] = edge
        for edge_key, edge in sorted(unique_edges.items()):
            edge_id = _stable_id("literature-edge", structured.record_id, edge_key)
            store.connection.execute(
                """
                INSERT INTO literature_citation_edges
                    (
                        edge_id, source_record_id, payload_digest, observation_time,
                        citing_paper_key, cited_paper_key, route_direction,
                        parent_seed_key, provider_reported, edge_json
                    )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    edge_id,
                    structured.record_id,
                    structured.payload_digest,
                    str(payload["observation_time"]),
                    str(edge["citing_paper_key"]),
                    str(edge["cited_paper_key"]),
                    str(edge["route_direction"]),
                    edge.get("parent_seed_key"),
                    1,
                    edge_key,
                ),
            )
            edge_count += 1
    source_digest = _source_digest(source)
    rebuilt_at = utc_timestamp()
    store.connection.execute(
        """
        INSERT INTO literature_projection_metadata
            (
                projection_id, schema_version, workspace_runtime_schema_version,
                rebuilt_at, source_observation_count, source_payload_digest
            )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            LITERATURE_PROJECTION_ID,
            LITERATURE_QUERY_INDEX_SCHEMA_VERSION,
            store.metadata().schema_version,
            rebuilt_at,
            len(source),
            source_digest,
        ),
    )
    return {
        "observations": len(source),
        "paper_occurrences": paper_count,
        "citation_edges": edge_count,
    }


def projection_posture(
    store: WorkspaceRuntimeStore,
    context: EffectiveTopicContext,
) -> dict[str, object]:
    """Describe projection compatibility and source-digest freshness."""

    table_names = {
        str(row["name"])
        for row in store.connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    }
    missing_tables = sorted(LITERATURE_TABLES - table_names)
    runtime_version = store.metadata().schema_version
    base: dict[str, object] = {
        "schema_version": LITERATURE_QUERY_INDEX_SCHEMA_VERSION,
        "workspace_runtime_schema_version": runtime_version,
        "schema_compatible": False,
        "rebuild_command": rebuild_command(context),
    }
    if missing_tables:
        return {
            **base,
            "status": "missing",
            "missing_tables": missing_tables,
        }
    if not projection_columns_compatible(store.connection):
        return {
            **base,
            "status": "incompatible",
            "reason": "projection-table-shape",
        }
    row = store.connection.execute(
        "SELECT * FROM literature_projection_metadata WHERE projection_id = ?",
        (LITERATURE_PROJECTION_ID,),
    ).fetchone()
    if row is None or row["schema_version"] != LITERATURE_QUERY_INDEX_SCHEMA_VERSION:
        return {
            **base,
            "status": "incompatible",
            "found_schema_version": None if row is None else row["schema_version"],
        }
    source, skipped = projection_source(store, context)
    current_digest = _source_digest(source)
    stale = row["source_payload_digest"] != current_digest or int(row["source_observation_count"]) != len(source)
    return {
        **base,
        "status": "stale" if stale else "complete",
        "schema_compatible": True,
        "source_observation_count": int(row["source_observation_count"]),
        "current_source_observation_count": len(source),
        "source_payload_digest": row["source_payload_digest"],
        "current_source_payload_digest": current_digest,
        "payload_digest_posture": "drift" if stale else "matched",
        "rebuilt_at": row["rebuilt_at"],
        "skipped_observation_count": len(skipped),
    }


def projection_issues(
    store: WorkspaceRuntimeStore,
    context: EffectiveTopicContext,
) -> list[dict[str, object]]:
    """Return deterministic integrity issues without mutating projection state."""

    issues: list[dict[str, object]] = []
    source, skipped = projection_source(store, context)
    for item in skipped:
        issues.append({"code": "source-observation-invalid", **item})
    source_by_id = {structured.record_id: structured for structured, _payload in source}
    observation_rows = list(store.connection.execute("SELECT * FROM literature_observation_index"))
    occurrence_rows = list(store.connection.execute("SELECT * FROM literature_paper_occurrences"))
    edge_rows = list(store.connection.execute("SELECT * FROM literature_citation_edges"))
    observation_ids = {str(row["source_record_id"]) for row in observation_rows}
    for row in observation_rows:
        record_id = str(row["source_record_id"])
        structured = store.get_structured_payload(record_id)
        record = store.get_lifecycle_record(record_id)
        if record is None or structured is None:
            issues.append({"code": "orphan-observation-row", "source_record_id": record_id})
            continue
        if row["payload_digest"] != structured.payload_digest:
            issues.append({"code": "payload-digest-drift", "source_record_id": record_id})
    for record_id in sorted(set(source_by_id) - observation_ids):
        issues.append({"code": "source-observation-unindexed", "source_record_id": record_id})
    paper_keys: dict[str, set[str]] = {}
    for row in occurrence_rows:
        record_id = str(row["source_record_id"])
        paper_key = str(row["paper_key"])
        if record_id not in observation_ids:
            issues.append({"code": "orphan-paper-row", "source_record_id": record_id, "paper_key": paper_key})
        if PAPER_KEY_RE.fullmatch(paper_key) is None:
            issues.append({"code": "malformed-paper-key", "source_record_id": record_id, "paper_key": paper_key})
        paper_keys.setdefault(record_id, set()).add(paper_key)
        structured = source_by_id.get(record_id)
        if structured is not None and row["payload_digest"] != structured.payload_digest:
            issues.append({"code": "payload-digest-drift", "source_record_id": record_id, "paper_key": paper_key})
    duplicate_papers = store.connection.execute(
        """
        SELECT source_record_id, paper_key, COUNT(*) AS duplicate_count
        FROM literature_paper_occurrences
        GROUP BY source_record_id, paper_key
        HAVING COUNT(*) > 1
        """
    )
    for row in duplicate_papers:
        issues.append(
            {
                "code": "duplicate-paper-occurrence",
                "source_record_id": row["source_record_id"],
                "paper_key": row["paper_key"],
                "count": int(row["duplicate_count"]),
            }
        )
    duplicate_edges = store.connection.execute(
        """
        SELECT source_record_id, citing_paper_key, cited_paper_key, route_direction, parent_seed_key, COUNT(*) AS duplicate_count
        FROM literature_citation_edges
        GROUP BY source_record_id, citing_paper_key, cited_paper_key, route_direction, parent_seed_key
        HAVING COUNT(*) > 1
        """
    )
    for row in duplicate_edges:
        issues.append(
            {
                "code": "duplicate-citation-edge",
                "source_record_id": row["source_record_id"],
                "citing_paper_key": row["citing_paper_key"],
                "cited_paper_key": row["cited_paper_key"],
                "count": int(row["duplicate_count"]),
            }
        )
    for row in edge_rows:
        record_id = str(row["source_record_id"])
        citing = str(row["citing_paper_key"])
        cited = str(row["cited_paper_key"])
        if record_id not in observation_ids:
            issues.append({"code": "orphan-citation-row", "source_record_id": record_id})
        missing = sorted({citing, cited} - paper_keys.get(record_id, set()))
        if missing:
            issues.append(
                {
                    "code": "missing-citation-endpoint",
                    "source_record_id": record_id,
                    "edge_id": row["edge_id"],
                    "missing_paper_keys": missing,
                }
            )
        if int(row["provider_reported"]) != 1:
            issues.append({"code": "citation-posture-invalid", "edge_id": row["edge_id"]})
    posture = projection_posture(store, context)
    if posture["status"] == "stale":
        issues.append({"code": "projection-stale", "rebuild_command": rebuild_command(context)})
    return sorted(issues, key=_canonical_json)


def create_projection_tables(connection: sqlite3.Connection) -> None:
    """Create only the versioned literature projection tables and indexes."""

    statements = (
        """CREATE TABLE literature_projection_metadata (
            projection_id TEXT PRIMARY KEY,
            schema_version TEXT NOT NULL,
            workspace_runtime_schema_version TEXT NOT NULL,
            rebuilt_at TEXT NOT NULL,
            source_observation_count INTEGER NOT NULL,
            source_payload_digest TEXT NOT NULL
        )""",
        """CREATE TABLE literature_observation_index (
            source_record_id TEXT PRIMARY KEY,
            payload_digest TEXT NOT NULL,
            observation_time TEXT NOT NULL,
            action TEXT NOT NULL,
            provider_name TEXT NOT NULL,
            completeness_status TEXT NOT NULL,
            payload_file_path TEXT
        )""",
        """CREATE TABLE literature_paper_occurrences (
            occurrence_id TEXT PRIMARY KEY,
            source_record_id TEXT NOT NULL,
            payload_digest TEXT NOT NULL,
            observation_time TEXT NOT NULL,
            paper_key TEXT NOT NULL,
            doi TEXT,
            arxiv_id TEXT,
            provider_name TEXT,
            provider_id TEXT,
            title TEXT,
            publication_year INTEGER,
            locator TEXT,
            paper_json TEXT NOT NULL,
            UNIQUE (source_record_id, paper_key)
        )""",
        "CREATE INDEX literature_paper_doi_idx ON literature_paper_occurrences (doi)",
        "CREATE INDEX literature_paper_arxiv_idx ON literature_paper_occurrences (arxiv_id)",
        "CREATE INDEX literature_paper_provider_idx ON literature_paper_occurrences (provider_name, provider_id)",
        "CREATE INDEX literature_paper_title_idx ON literature_paper_occurrences (title)",
        "CREATE INDEX literature_paper_year_idx ON literature_paper_occurrences (publication_year)",
        """CREATE TABLE literature_citation_edges (
            edge_id TEXT PRIMARY KEY,
            source_record_id TEXT NOT NULL,
            payload_digest TEXT NOT NULL,
            observation_time TEXT NOT NULL,
            citing_paper_key TEXT NOT NULL,
            cited_paper_key TEXT NOT NULL,
            route_direction TEXT NOT NULL CHECK (route_direction IN ('forward', 'backward')),
            parent_seed_key TEXT,
            provider_reported INTEGER NOT NULL CHECK (provider_reported = 1),
            edge_json TEXT NOT NULL,
            UNIQUE (source_record_id, citing_paper_key, cited_paper_key, route_direction, parent_seed_key)
        )""",
        "CREATE INDEX literature_citation_citing_idx ON literature_citation_edges (citing_paper_key)",
        "CREATE INDEX literature_citation_cited_idx ON literature_citation_edges (cited_paper_key)",
    )
    for statement in statements:
        connection.execute(statement)


def drop_projection_tables(connection: sqlite3.Connection) -> None:
    """Drop only derived literature projection tables."""

    for table in (
        "literature_citation_edges",
        "literature_paper_occurrences",
        "literature_observation_index",
        "literature_projection_metadata",
    ):
        connection.execute(f"DROP TABLE IF EXISTS {table}")


def clear_projection_rows(connection: sqlite3.Connection) -> None:
    """Clear only derived literature projection rows."""

    connection.execute("DELETE FROM literature_citation_edges")
    connection.execute("DELETE FROM literature_paper_occurrences")
    connection.execute("DELETE FROM literature_observation_index")
    connection.execute("DELETE FROM literature_projection_metadata")


def projection_columns_compatible(connection: sqlite3.Connection) -> bool:
    """Return whether all required v1 projection columns are present."""

    expected = {
        "literature_projection_metadata": {
            "projection_id",
            "schema_version",
            "workspace_runtime_schema_version",
            "rebuilt_at",
            "source_observation_count",
            "source_payload_digest",
        },
        "literature_observation_index": {
            "source_record_id",
            "payload_digest",
            "observation_time",
            "action",
            "provider_name",
            "completeness_status",
            "payload_file_path",
        },
        "literature_paper_occurrences": {
            "occurrence_id",
            "source_record_id",
            "payload_digest",
            "observation_time",
            "paper_key",
            "doi",
            "arxiv_id",
            "provider_name",
            "provider_id",
            "title",
            "publication_year",
            "locator",
            "paper_json",
        },
        "literature_citation_edges": {
            "edge_id",
            "source_record_id",
            "payload_digest",
            "observation_time",
            "citing_paper_key",
            "cited_paper_key",
            "route_direction",
            "parent_seed_key",
            "provider_reported",
            "edge_json",
        },
    }
    for table, columns in expected.items():
        found = {str(row["name"]) for row in connection.execute(f"PRAGMA table_info({table})")}
        if not columns.issubset(found):
            return False
    return True


def projection_required_payload(operation: str, posture: Mapping[str, object]) -> dict[str, object]:
    """Return the stable no-mutation response for a missing or incompatible projection."""

    return {
        "ok": False,
        "mutated": False,
        "operation": operation,
        "error": {
            "code": "literature_projection_rebuild_required",
            "message": "A compatible local literature query projection is required.",
        },
        "projection": dict(posture),
        "rebuild_command": posture["rebuild_command"],
        "provider_io": False,
    }


def rebuild_command(context: EffectiveTopicContext) -> str:
    """Return the exact explicit rebuild command for the selected Topic."""

    return (
        "isomer-cli --print-json ext research literature index rebuild --topic "
        + shlex.quote(context.research_topic.id)
    )


def _source_digest(
    source: list[tuple[StructuredResearchPayloadRecord, dict[str, object]]],
) -> str:
    return digest_json(
        [
            {
                "source_record_id": structured.record_id,
                "payload_digest": structured.payload_digest,
            }
            for structured, _payload in source
        ]
    )


def _stable_id(prefix: str, *values: str) -> str:
    digest = hashlib.sha256("\0".join(values).encode("utf-8")).hexdigest()
    return f"{prefix}-{digest}"


def _canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
