"""SQLite access for the DeepResearch platform DB (single DB holds all quests)."""
from __future__ import annotations
import sqlite3
import tomllib
from pathlib import Path

from paths import SCHEMA_SQL, SEED_TOML


def connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init(db_path: Path) -> dict:
    """Idempotent: schema uses IF NOT EXISTS / INSERT OR IGNORE, so re-init verifies in place."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    existed = db_path.exists()
    conn = connect(db_path)
    conn.executescript(SCHEMA_SQL.read_text())
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
