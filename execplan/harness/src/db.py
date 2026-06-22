"""SQLite access for the DeepResearch platform DB (single DB holds all quests)."""
from __future__ import annotations
import sqlite3
import tomllib
from pathlib import Path

from paths import SCHEMA_SQL, SEED_TOML


# Guarded lazy migrations (additive ADD COLUMN only). Fresh DBs get these columns from schema.sql (with CHECK);
# existing DBs (holding completed quests) get them via ALTER here. Purely additive — NO row is rewritten, so
# historical quests keep NULL (autonomy_mode/rigor_level) or the column default ('claim'). Enum is enforced at
# the record layer for migrated columns (SQLite cannot ADD a CHECK via ALTER).
MIGRATIONS = [
    ("quest", "autonomy_mode", "ALTER TABLE quest ADD COLUMN autonomy_mode TEXT"),
    ("quest", "rigor_level",   "ALTER TABLE quest ADD COLUMN rigor_level TEXT"),
    ("claim", "kind",          "ALTER TABLE claim ADD COLUMN kind TEXT NOT NULL DEFAULT 'claim'"),
    ("claim_evidence", "evidence_kind", "ALTER TABLE claim_evidence ADD COLUMN evidence_kind TEXT"),
    ("claim_evidence", "evidence_proof", "ALTER TABLE claim_evidence ADD COLUMN evidence_proof TEXT"),
    ("result", "provenance_route", "ALTER TABLE result ADD COLUMN provenance_route TEXT"),
    ("result", "provenance",       "ALTER TABLE result ADD COLUMN provenance TEXT"),
    ("result", "provenance_ok",    "ALTER TABLE result ADD COLUMN provenance_ok INTEGER NOT NULL DEFAULT 0"),
    ("baseline_contract", "baseline_route", "ALTER TABLE baseline_contract ADD COLUMN baseline_route TEXT"),
    ("baseline_contract", "evidence_ref",   "ALTER TABLE baseline_contract ADD COLUMN evidence_ref TEXT"),
    ("baseline_contract", "valid",          "ALTER TABLE baseline_contract ADD COLUMN valid INTEGER NOT NULL DEFAULT 0"),
    ("baseline_contract", "validated_fingerprint", "ALTER TABLE baseline_contract ADD COLUMN validated_fingerprint TEXT"),
    ("analysis_bridge", "validated_fingerprint",    "ALTER TABLE analysis_bridge ADD COLUMN validated_fingerprint TEXT"),
    ("paper_spine", "validated_fingerprint",        "ALTER TABLE paper_spine ADD COLUMN validated_fingerprint TEXT"),
    ("review_verdict", "validated_fingerprint",     "ALTER TABLE review_verdict ADD COLUMN validated_fingerprint TEXT"),
]


# New TABLES added after the initial schema. Existing DBs (not re-init'd) get them here on connect; fresh DBs
# also get them from schema.sql. Purely additive (CREATE TABLE IF NOT EXISTS) — no row is ever rewritten.
NEW_TABLES = [
    ("scope_contract",
     "CREATE TABLE IF NOT EXISTS scope_contract ("
     "  contract_id TEXT PRIMARY KEY,"
     "  quest_id TEXT NOT NULL REFERENCES quest(quest_id),"
     "  round_index INTEGER,"
     "  contract TEXT,"
     "  contract_ref TEXT,"
     "  valid INTEGER NOT NULL DEFAULT 0,"
     "  validated_fingerprint TEXT,"
     "  created_at TEXT NOT NULL"
     ")"),
    ("quality_gate_waiver",
     "CREATE TABLE IF NOT EXISTS quality_gate_waiver ("
     "  waiver_id TEXT PRIMARY KEY,"
     "  quest_id TEXT NOT NULL REFERENCES quest(quest_id),"
     "  gate TEXT NOT NULL,"
     "  source TEXT NOT NULL DEFAULT 'operator' CHECK (source IN ('env','operator','record','scoping')),"
     "  reason TEXT NOT NULL,"
     "  actor TEXT,"
     "  finalize_ack INTEGER NOT NULL DEFAULT 0,"
     "  expiry TEXT,"
     "  scope TEXT,"
     "  created_at TEXT NOT NULL"
     ")"),
]


def migrate(conn: sqlite3.Connection) -> dict:
    """Idempotent, history-safe column + table additions. Skips tables that don't exist yet (fresh pre-schema
    conn) and columns already present. Never rewrites a row."""
    applied = []
    for table, ddl in NEW_TABLES:
        try:
            exists = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)).fetchone()
        except sqlite3.OperationalError:
            exists = None
        if exists:
            continue
        try:
            conn.execute(ddl)
            applied.append(f"table:{table}")
        except sqlite3.OperationalError:
            pass
    for table, col, ddl in MIGRATIONS:
        try:
            cols = {r[1] for r in conn.execute(f"PRAGMA table_info({table})")}
        except sqlite3.OperationalError:
            continue  # table not created yet
        if not cols or col in cols:
            continue
        try:
            conn.execute(ddl)
            applied.append(f"{table}.{col}")
        except sqlite3.OperationalError:
            pass  # concurrent/duplicate add: tolerate
    if applied:
        conn.commit()
    return {"applied": applied}


def connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    migrate(conn)  # guarded lazy upgrade on every connection (covers state validate / record-apply / query)
    return conn


def init(db_path: Path) -> dict:
    """Idempotent: schema uses IF NOT EXISTS / INSERT OR IGNORE, so re-init verifies in place."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    existed = db_path.exists()
    conn = connect(db_path)
    conn.executescript(SCHEMA_SQL.read_text())
    migrate(conn)  # ensure additive columns exist after (re)creating tables on an existing DB
    # Apply domain-neutral seed DATA (stage extensions + knowledge packs); none by default.
    seed = tomllib.loads(SEED_TOML.read_text()) if SEED_TOML.exists() else {}
    for s in seed.get("stage", []):
        conn.execute(
            "INSERT OR IGNORE INTO stage_catalog(stage,ordinal,description,is_builtin,owning_role) "
            "VALUES(?,?,?,?,?)",
            (s["stage"], s["ordinal"], s["description"], s.get("is_builtin", 0), s.get("owning_role")),
        )
    for k in seed.get("knowledge_pack", []):
        conn.execute(
            "INSERT OR IGNORE INTO knowledge_pack(pack_id,domain,name,kind,ref,enabled,priority,created_at) "
            "VALUES(?,?,?,?,?,?,?,?)",
            (k["pack_id"], k["domain"], k["name"], k["kind"], k["ref"],
             int(k.get("enabled", 1)), int(k.get("priority", 100)), seed.get("_at", "1970-01-01T00:00:00Z")),
        )
    conn.commit()
    n_stages = conn.execute("SELECT COUNT(*) FROM stage_catalog").fetchone()[0]
    n_tables = conn.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
    conn.close()
    return {"db": str(db_path), "verified_existing": existed, "tables": n_tables, "stages": n_stages}


def table_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    return {r[1] for r in conn.execute(f"PRAGMA table_info({table})")}


def rows(conn: sqlite3.Connection, sql: str, params=()) -> list[dict]:
    return [dict(r) for r in conn.execute(sql, params).fetchall()]
