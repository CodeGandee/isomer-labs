"""record apply / validate — the ONLY state write path.

Each payload is validated against its record schema (specs/state/records/*.schema.json), then written to
its target table per RECORD_MAP. Record fields mirror columns by name; record_id supplies single PKs or
is split on ':' for composite PKs. Timestamps come from payload['at'] (never generated here).
"""
from __future__ import annotations
import json
import sqlite3
import glob
import jsonschema

from paths import RECORDS_DIR

# Tables carrying updated_at (set on every write); participant carries no timestamps.
UPDATED_TABLES = {"quest", "round", "branch", "idea", "experiment", "claim",
                  "finding_memory", "self_wakeup", "handoff", "intake_asset", "frontier_entry"}
NO_CREATED = {"participant"}

# record_type -> write spec. id_from: 'record_id' (pk[0]=record_id) | 'fields' (pk cols in payload) |
# 'split' (record_id split on ':' into pk). mode: upsert | insert | update | special.
RECORD_MAP = {
    "quest.create":            dict(table="quest", pk=["quest_id"], id_from="record_id", mode="upsert"),
    "quest.update":            dict(table="quest", pk=["quest_id"], id_from="record_id", mode="update"),
    "round.open":              dict(table="round", pk=["quest_id", "round_index"], id_from="fields", mode="upsert", force={"status": "open"}),
    "round.update":            dict(table="round", pk=["quest_id", "round_index"], id_from="split", mode="update"),
    "round.close":             dict(table="round", pk=["quest_id", "round_index"], id_from="split", mode="update", force={"status": "closed"}),
    "branch.record":           dict(table="branch", pk=["branch_id"], id_from="record_id", mode="upsert"),
    "participant.register":    dict(table="participant", pk=["quest_id", "instance_id"], id_from="fields", mode="upsert"),
    "idea.upsert":             dict(table="idea", pk=["idea_id"], id_from="record_id", mode="upsert"),
    "experiment.upsert":       dict(table="experiment", pk=["experiment_id"], id_from="record_id", mode="upsert"),
    "result.record":           dict(table="result", pk=["result_id"], id_from="record_id", mode="upsert"),
    "measurement.record":      dict(table="measurement", pk=["measurement_id"], id_from="record_id", mode="upsert"),
    "analysis.record":         dict(table="analysis", pk=["analysis_id"], id_from="record_id", mode="upsert"),
    "claim.upsert":            dict(table="claim", pk=["claim_id"], id_from="record_id", mode="upsert"),
    "claim_evidence.link":     dict(table="claim_evidence", pk=["claim_id", "source_kind", "source_ref"], id_from="fields", mode="upsert"),
    "claim_evidence.resolve":  dict(table="claim_evidence", pk=["claim_id", "source_kind", "source_ref"], id_from="fields", mode="update", force={"resolved": 1, "resolved_at": "AT"}),
    "decision.record":         dict(table="decision", pk=["decision_id"], id_from="record_id", mode="insert"),
    "decision.confirm":        dict(table="decision", pk=["decision_id"], id_from="record_id", mode="update", force={"confirmed": 1}),
    "finding.add":             dict(table="finding_memory", pk=["memory_id"], id_from="record_id", mode="upsert"),
    "reference.record":        dict(table="reference", pk=["reference_id"], id_from="record_id", mode="upsert"),
    "search_space.define":     dict(table="search_space", pk=["quest_id", "space_id", "dim_name"], id_from="fields", mode="upsert"),
    "experiment_param.record": dict(table="experiment_param", pk=["experiment_id", "dim_name"], id_from="fields", mode="upsert"),
    "handoff.open":            dict(table="handoff", pk=["quest_id", "handoff_id"], id_from="fields", mode="special", special="handoff_open"),
    "handoff.advance":         dict(table="handoff", pk=["quest_id", "handoff_id"], id_from="split", mode="special", special="handoff_advance"),
    "wakeup.arm":              dict(table="self_wakeup", pk=["wakeup_id"], id_from="record_id", mode="upsert", force={"status": "armed"}),
    "wakeup.attach":           dict(table="self_wakeup", pk=["wakeup_id"], id_from="record_id", mode="update"),
    "wakeup.resolve":          dict(table="self_wakeup", pk=["wakeup_id"], id_from="record_id", mode="update"),
    "artifact.record":         dict(table="artifact", pk=["artifact_id"], id_from="record_id", mode="upsert"),
    "operator_event.record":   dict(table="operator_intent_event", pk=["event_id"], id_from="record_id", mode="insert"),
    "quirk.append":            dict(table="quirk", pk=["quirk_id"], id_from="record_id", mode="insert"),
    "knowledge_pack.register": dict(table="knowledge_pack", pk=["pack_id"], id_from="record_id", mode="upsert"),
    "intake_asset.record":     dict(table="intake_asset", pk=["asset_id"], id_from="record_id", mode="upsert"),
    "frontier.record":         dict(table="frontier_entry", pk=["entry_id"], id_from="record_id", mode="upsert"),
    "finalize.record":         dict(table="finalize_outcome", pk=["outcome_id"], id_from="record_id", mode="insert"),
}

# Apply-time lifecycle transition guards. Maps current_status -> allowed next states (same-status and
# new-row inserts are always allowed). Illegal transitions raise RecordError at write time.
HANDOFF_TX = {
    "pending": {"sent", "failed"},
    "sent": {"acked", "result_received", "processed", "failed"},
    "acked": {"result_received", "processed", "failed"},
    "result_received": {"processed", "failed"},
    "processed": set(),
    "failed": set(),
}
WAKEUP_TX = {
    "armed": {"delivered", "superseded", "failed"},
    "delivered": {"consumed", "superseded", "failed"},
    "consumed": set(),
    "superseded": set(),
    "failed": set(),
}
QUEST_TX = {
    "not_started": {"running"},
    "running": {"paused", "recovering", "waiting_user", "parked", "stopped", "completed"},
    "paused": {"running", "recovering", "stopped"},
    "recovering": {"running", "stopped", "completed"},
    "waiting_user": {"running", "paused", "stopped", "completed"},
    "parked": {"running", "recovering", "stopped"},
    "stopped": set(),
    "completed": set(),
}
ROUND_TX = {"open": {"closed"}, "closed": set()}
CLAIM_TX = {
    "open": {"supported", "refuted", "withdrawn"},
    "supported": {"refuted", "withdrawn"},
    "refuted": {"supported", "withdrawn"},
    "withdrawn": set(),
}
STATUS_GUARDS = {
    "handoff": ("status", HANDOFF_TX),
    "self_wakeup": ("status", WAKEUP_TX),
    "quest": ("run_state", QUEST_TX),
    "round": ("status", ROUND_TX),
    "claim": ("status", CLAIM_TX),
}


def _guard_transition(conn, table, pk, pkvals, new_status):
    """Raise RecordError if changing a guarded status column to an illegal next state."""
    g = STATUS_GUARDS.get(table)
    if not g or new_status is None:
        return
    col, tx = g
    where = " AND ".join(f"{c}=?" for c in pk)
    row = conn.execute(f"SELECT {col} FROM {table} WHERE {where}", [pkvals[c] for c in pk]).fetchone()
    if row is None:
        return  # new row: initial state is allowed
    cur = row[0]
    if cur == new_status:
        return  # idempotent
    if new_status in tx.get(cur, set()):
        return
    raise RecordError(f"illegal {table}.{col} transition: {cur!r} -> {new_status!r}")


_TYPE_INDEX = None


def type_index() -> dict:
    """record_type -> the file schema (oneOf) that validates it."""
    global _TYPE_INDEX
    if _TYPE_INDEX is None:
        idx = {}
        for path in glob.glob(str(RECORDS_DIR / "*.schema.json")):
            if path.endswith("_envelope.schema.json"):
                continue
            schema = json.load(open(path))
            for branch in (schema["oneOf"] if "oneOf" in schema else [schema]):
                const = branch.get("properties", {}).get("record_type", {}).get("const")
                if const:
                    idx[const] = schema
        _TYPE_INDEX = idx
    return _TYPE_INDEX


class RecordError(Exception):
    pass


def validate(payload: dict) -> None:
    rt = payload.get("record_type")
    idx = type_index()
    if rt not in idx:
        raise RecordError(f"unknown record_type: {rt!r}")
    if rt not in RECORD_MAP:
        raise RecordError(f"no write mapping for record_type: {rt!r}")
    try:
        jsonschema.validate(payload, idx[rt])
    except jsonschema.ValidationError as e:
        raise RecordError(f"schema validation failed for {rt}: {e.message}")


def _norm(v):
    return int(v) if isinstance(v, bool) else v


def apply(conn: sqlite3.Connection, payload: dict) -> dict:
    validate(payload)
    rt = payload["record_type"]
    spec = RECORD_MAP[rt]
    table, pk = spec["table"], spec["pk"]
    at = payload["at"]

    # Resolve PK values.
    pkvals = {}
    if spec["id_from"] == "record_id":
        pkvals[pk[0]] = payload["record_id"]
    elif spec["id_from"] == "split":
        parts = payload["record_id"].split(":")
        if len(parts) != len(pk):
            raise RecordError(f"record_id {payload['record_id']!r} must split into {pk} (got {len(parts)})")
        for col, val in zip(pk, parts):
            pkvals[col] = int(val) if col == "round_index" else val
    else:  # fields
        for col in pk:
            if col not in payload:
                raise RecordError(f"missing pk field {col} for {rt}")
            pkvals[col] = payload[col]

    if spec["mode"] == "special":
        return _special(conn, spec["special"], pkvals, payload, at)

    # Build column values from payload fields (mirror columns), minus envelope keys.
    cols = {k: _norm(v) for k, v in payload.items()
            if k not in ("record_type", "record_id", "at", "bump_attempt")}
    cols.update(pkvals)
    for fcol, fval in spec.get("force", {}).items():
        cols[fcol] = at if fval == "AT" else fval
    if table not in NO_CREATED:
        if spec["mode"] in ("insert", "upsert"):
            cols.setdefault("created_at", at)
    if table in UPDATED_TABLES:
        cols["updated_at"] = at

    # Apply-time lifecycle guard before any write.
    guard_col = STATUS_GUARDS.get(table, (None,))[0]
    if guard_col and guard_col in cols:
        _guard_transition(conn, table, pk, pkvals, cols[guard_col])

    if spec["mode"] == "insert":
        _insert_or_ignore(conn, table, cols)
    elif spec["mode"] == "upsert":
        _upsert(conn, table, pk, cols)
    elif spec["mode"] == "update":
        _update(conn, table, pk, pkvals, cols)
    conn.commit()
    return {"record_type": rt, "table": table, "pk": pkvals}


def _insert_or_ignore(conn, table, cols):
    keys = list(cols)
    conn.execute(
        f"INSERT OR IGNORE INTO {table} ({','.join(keys)}) VALUES ({','.join('?' * len(keys))})",
        [cols[k] for k in keys],
    )


def _upsert(conn, table, pk, cols):
    keys = list(cols)
    setcols = [k for k in keys if k not in pk and k != "created_at"]
    sql = (f"INSERT INTO {table} ({','.join(keys)}) VALUES ({','.join('?' * len(keys))}) "
           f"ON CONFLICT({','.join(pk)}) DO UPDATE SET "
           + ", ".join(f"{c}=excluded.{c}" for c in setcols))
    conn.execute(sql, [cols[k] for k in keys])


def _update(conn, table, pk, pkvals, cols):
    setcols = [k for k in cols if k not in pk]
    if not setcols:
        raise RecordError(f"update for {table} has no columns to set")
    where = " AND ".join(f"{c}=?" for c in pk)
    sql = f"UPDATE {table} SET {', '.join(f'{c}=?' for c in setcols)} WHERE {where}"
    cur = conn.execute(sql, [cols[c] for c in setcols] + [pkvals[c] for c in pk])
    if cur.rowcount == 0:
        raise RecordError(f"update matched no row in {table} for {pkvals}")


def _special(conn, kind, pkvals, payload, at):
    q, h = pkvals["quest_id"], pkvals["handoff_id"]
    if kind == "handoff_open":
        existing = conn.execute("SELECT attempt_count FROM handoff WHERE quest_id=? AND handoff_id=?", (q, h)).fetchone()
        if existing is None:
            cols = {k: _norm(v) for k, v in payload.items()
                    if k not in ("record_type", "record_id", "at", "bump_attempt")}
            cols.update(quest_id=q, handoff_id=h, status="sent", attempt_count=1,
                        created_at=at, updated_at=at)
            cols.setdefault("schema_id", payload.get("schema_id"))
            _insert_or_ignore(conn, "handoff", cols)
        else:
            _guard_transition(conn, "handoff", ["quest_id", "handoff_id"], pkvals, "sent")
            bump = 1 if payload.get("bump_attempt") else 0
            conn.execute(
                "UPDATE handoff SET status='sent', attempt_count=attempt_count+?, updated_at=? "
                "WHERE quest_id=? AND handoff_id=?", (bump, at, q, h))
        conn.commit()
        return {"record_type": "handoff.open", "pk": pkvals}
    if kind == "handoff_advance":
        _guard_transition(conn, "handoff", ["quest_id", "handoff_id"], pkvals, payload["status"])
        bump = 1 if payload.get("bump_attempt") else 0
        cur = conn.execute(
            "UPDATE handoff SET status=?, attempt_count=attempt_count+?, updated_at=? "
            "WHERE quest_id=? AND handoff_id=?", (payload["status"], bump, at, q, h))
        if cur.rowcount == 0:
            raise RecordError(f"handoff.advance matched no row for {pkvals}")
        conn.commit()
        return {"record_type": "handoff.advance", "pk": pkvals, "status": payload["status"]}
    raise RecordError(f"unknown special writer {kind}")
