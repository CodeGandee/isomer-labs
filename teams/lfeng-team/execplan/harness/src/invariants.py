"""Run the named invariants from specs/state/invariants.toml + FK integrity."""
from __future__ import annotations
import sqlite3
import tomllib

from paths import INVARIANTS_TOML


def load() -> list[dict]:
    return tomllib.loads(INVARIANTS_TOML.read_text()).get("invariant", [])


def run_all(conn: sqlite3.Connection) -> dict:
    results = []
    for iv in load():
        try:
            v = conn.execute(iv["check"]).fetchone()[0]
            results.append({"name": iv["name"], "area": iv.get("area"),
                            "violations": v, "ok": v == iv.get("expect", 0)})
        except sqlite3.Error as e:
            results.append({"name": iv["name"], "error": str(e), "ok": False})
    fk = [dict(table=r[0], rowid=r[1], parent=r[2], fkid=r[3])
          for r in conn.execute("PRAGMA foreign_key_check")]
    failed = [r for r in results if not r["ok"]]
    return {
        "ok": not failed and not fk,
        "checked": len(results),
        "violations": failed,
        "fk_violations": fk,
    }
