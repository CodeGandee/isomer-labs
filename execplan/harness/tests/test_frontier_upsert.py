#!/usr/bin/env python3
"""Regression test for the frontier_entry upsert latent bug.

frontier_entry has a surrogate `entry_id` PRIMARY KEY plus UNIQUE(quest_id, candidate_ref). The generic
upsert used ON CONFLICT(entry_id) only, so recording the same (quest_id, candidate_ref) under a DIFFERENT
entry_id raised IntegrityError. records._upsert now resolves the secondary-unique row and updates it in
place (preserving its entry_id), keeping the write idempotent on the natural key with no cross-quest effect.

Covers: (1) first insert; (2) same entry_id update; (3) different entry_id, same (quest_id, candidate_ref)
does not crash and updates in place; (4) same candidate_ref in a DIFFERENT quest stays isolated.

Run: python3 execplan/harness/tests/test_frontier_upsert.py   (exits non-zero on failure).
Builds its own throwaway DB from the real schema.sql; does NOT touch runs/state.sqlite.
"""
import sys
import tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

import db          # noqa: E402
import records     # noqa: E402

AT = "2026-06-15T00:00:00Z"


def _quest(conn, qid):
    records.apply(conn, {
        "record_type": "quest.create", "record_id": qid, "at": AT,
        "title": f"t-{qid}", "objective_ref": "o", "workspace_ref": "w"})


def _frontier(conn, entry_id, quest_id, candidate_ref, *, score, status="candidate"):
    records.apply(conn, {
        "record_type": "frontier.record", "record_id": entry_id, "at": AT,
        "quest_id": quest_id, "candidate_kind": "experiment",
        "candidate_ref": candidate_ref, "score": score, "status": status})


def _rows(conn, quest_id, candidate_ref):
    return conn.execute(
        "SELECT entry_id, score, status FROM frontier_entry WHERE quest_id=? AND candidate_ref=?",
        (quest_id, candidate_ref)).fetchall()


def main():
    checks = []

    def check(name, cond):
        checks.append((name, bool(cond)))
        print(("  PASS " if cond else "  FAIL ") + name)

    with tempfile.TemporaryDirectory() as d:
        dbp = Path(d) / "t.sqlite"
        db.init(dbp)
        conn = db.connect(dbp)
        _quest(conn, "qA")
        _quest(conn, "qB")

        # (1) first insert succeeds
        _frontier(conn, "f1", "qA", "cand1", score=1.0)
        r = _rows(conn, "qA", "cand1")
        check("1) first insert -> one row, entry f1, score 1.0",
              len(r) == 1 and r[0]["entry_id"] == "f1" and r[0]["score"] == 1.0)

        # (2) same entry_id update succeeds (idempotent on PK)
        _frontier(conn, "f1", "qA", "cand1", score=2.0, status="incumbent")
        r = _rows(conn, "qA", "cand1")
        check("2) same entry_id update -> still one row, entry f1, score 2.0, incumbent",
              len(r) == 1 and r[0]["entry_id"] == "f1" and r[0]["score"] == 2.0
              and r[0]["status"] == "incumbent")

        # (3) DIFFERENT entry_id, SAME (quest_id, candidate_ref) must NOT crash; updates existing row in
        #     place, preserving entry_id f1; f2 is not created as a separate row.
        crashed = False
        try:
            _frontier(conn, "f2", "qA", "cand1", score=3.0, status="promoted")
        except Exception as e:  # noqa: BLE001
            crashed = True
            print("    raised:", type(e).__name__, e)
        r = _rows(conn, "qA", "cand1")
        f2 = conn.execute("SELECT 1 FROM frontier_entry WHERE entry_id='f2'").fetchone()
        check("3a) different entry_id, same (quest,candidate) does not crash", not crashed)
        check("3b) still one row for (qA,cand1), entry_id preserved as f1, score 3.0, promoted",
              len(r) == 1 and r[0]["entry_id"] == "f1" and r[0]["score"] == 3.0
              and r[0]["status"] == "promoted")
        check("3c) surrogate id f2 did not create a separate row", f2 is None)

        # (4) same candidate_ref in a DIFFERENT quest stays isolated (no cross-quest behavior)
        _frontier(conn, "f3", "qB", "cand1", score=9.0)
        rb = _rows(conn, "qB", "cand1")
        ra = _rows(conn, "qA", "cand1")
        total = conn.execute("SELECT COUNT(*) FROM frontier_entry").fetchone()[0]
        check("4a) (qB,cand1) is its own row, entry f3, score 9.0",
              len(rb) == 1 and rb[0]["entry_id"] == "f3" and rb[0]["score"] == 9.0)
        check("4b) (qA,cand1) untouched by the qB write (entry f1, score 3.0)",
              len(ra) == 1 and ra[0]["entry_id"] == "f1" and ra[0]["score"] == 3.0)
        check("4c) exactly two frontier rows total (no cross-quest merge)", total == 2)

        # integrity: no FK violations introduced
        fk = conn.execute("PRAGMA foreign_key_check").fetchall()
        check("integrity) no foreign-key violations", not fk)
        conn.close()

    failed = [n for n, ok in checks if not ok]
    print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed")
    if failed:
        print("FAILED:", ", ".join(failed))
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
