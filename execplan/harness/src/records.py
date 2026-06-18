"""record apply / validate — the ONLY state write path.

Each payload is validated against its record schema (specs/state/records/*.schema.json), then written to
its target table per RECORD_MAP. Record fields mirror columns by name; record_id supplies single PKs or
is split on ':' for composite PKs. Timestamps come from payload['at'] (never generated here).
"""
from __future__ import annotations
import json
import os
import sqlite3
import glob
import jsonschema

from paths import RECORDS_DIR

# Tables carrying updated_at (set on every write); participant carries no timestamps.
UPDATED_TABLES = {"quest", "round", "branch", "idea", "experiment", "claim",
                  "finding_memory", "self_wakeup", "handoff", "intake_asset", "frontier_entry",
                  "gpu_allocation", "paper_spine"}
NO_CREATED = {"participant", "gpu_allocation"}

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
    "paper_spine.upsert":      dict(table="paper_spine", pk=["quest_id"], id_from="record_id", mode="upsert", force={"submission_ready": 0}),
    "review.verdict":          dict(table="review_verdict", pk=["verdict_id"], id_from="record_id", mode="insert", force={"valid": 0}),
    "idea.select":             dict(table="idea_select", pk=["select_id"], id_from="record_id", mode="insert", force={"valid": 0}),
    "baseline.contract":       dict(table="baseline_contract", pk=["contract_id"], id_from="record_id", mode="insert"),
    "analysis.bridge":         dict(table="analysis_bridge", pk=["bridge_id"], id_from="record_id", mode="insert", force={"valid": 0}),
    "operator_event.record":   dict(table="operator_intent_event", pk=["event_id"], id_from="record_id", mode="insert"),
    "quirk.append":            dict(table="quirk", pk=["quirk_id"], id_from="record_id", mode="insert"),
    "knowledge_pack.register": dict(table="knowledge_pack", pk=["pack_id"], id_from="record_id", mode="upsert"),
    "intake_asset.record":     dict(table="intake_asset", pk=["asset_id"], id_from="record_id", mode="upsert"),
    "frontier.record":         dict(table="frontier_entry", pk=["entry_id"], id_from="record_id", mode="upsert", unique=[["quest_id", "candidate_ref"]]),
    "finalize.record":         dict(table="finalize_outcome", pk=["outcome_id"], id_from="record_id", mode="insert"),
    "gpu.confirm":             dict(table="gpu_allocation", pk=["quest_id"], id_from="record_id", mode="upsert", force={"status": "confirmed", "confirmed_at": "AT"}),
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


# ── Skill-caller authority + audit (exposing commands/packs as agent-invokable skills) ──────────────────
# A write may carry a caller identity set from the CLI `--via` flag:
#   --via skill:<skill-id>:<role>   an agent invoked a wrapped skill (authority-checked + audited)
#   --via loop:<role> | operator    the loop / operator (UNRESTRICTED — default when --via is absent)
# Enforced HERE, the single write path, so it is caller-agnostic and composes with every existing gate (no
# gate is weakened). loop/operator/orchestrator callers bypass the allowlist (no regression). A skill caller
# is checked against a per-role allowlist (Tier C reserved → operator/orchestrator; Tier B science writes →
# owner role; Tier A → any specialist), optionally loop-context-guarded, and every skill-invoked mutation is
# stamped with a quest-owned audit artifact(kind='skill-invocation') so skill vs loop writes are distinguishable.
CALLER = {"kind": "loop", "role": None, "skill": None}


def set_caller(via):
    global CALLER
    if not via:
        CALLER = {"kind": "loop", "role": None, "skill": None}; return
    p = str(via).split(":")
    if p[0] == "skill" and len(p) >= 3:
        CALLER = {"kind": "skill", "skill": p[1], "role": p[2]}
    elif p[0] in ("loop", "operator"):
        CALLER = {"kind": p[0], "role": (p[1] if len(p) > 1 else None), "skill": None}
    else:
        CALLER = {"kind": "loop", "role": None, "skill": None}


_OPERATOR_ONLY_RT = {"gpu.confirm"}
_ORCH_ONLY_RT = {"decision.record", "decision.confirm", "finalize.record",
                 "round.open", "round.update", "round.close", "wakeup.arm", "wakeup.attach", "wakeup.resolve",
                 "handoff.open", "handoff.advance", "frontier.record", "operator_event.record",
                 "quest.create", "quest.update", "knowledge_pack.register"}
_OWNER_RT = {"experiment.upsert": {"experimenter"}, "result.record": {"experimenter"},
             "measurement.record": {"experimenter"}, "experiment_param.record": {"experimenter"},
             "search_space.define": {"scout-ideator"}, "analysis.record": {"analyst"},
             "idea.upsert": {"scout-ideator"}, "intake_asset.record": {"scout-ideator"},
             "reference.record": {"scout-ideator", "writer"},
             "claim.upsert": {"writer", "analyst", "reviewer"},
             "claim_evidence.link": {"writer", "analyst", "reviewer"},
             "claim_evidence.resolve": {"reviewer", "writer"}}
_TIER_B_RT = {"experiment.upsert", "result.record", "measurement.record", "experiment_param.record", "analysis.record"}
_CMD_ROLES = {"experiment run": {"experimenter", "analyst"}, "result validate": {"orchestrator"},
              "gpu confirm": {"operator"}}


def _deny(what, role):
    raise RecordError(f"skill authority: role {role!r} (via --via skill) may not perform {what!r}; it is "
                      "operator/orchestrator/owner-reserved. Route it through the Orchestrator (tree-loop) "
                      "or an operator.")


def authorize(record_type):
    """Per-role allowlist for a SKILL caller (loop/operator/orchestrator bypass)."""
    if CALLER["kind"] != "skill":
        return
    role = CALLER["role"]
    if role in ("operator", "orchestrator"):
        return
    if record_type in _OPERATOR_ONLY_RT or record_type in _ORCH_ONLY_RT:
        _deny(record_type, role)
    if record_type in _OWNER_RT and role not in _OWNER_RT[record_type]:
        _deny(record_type, role)


def authorize_command(command):
    """Role check for stateful COMMANDS not on the record-apply path (experiment run / result validate /
    gpu confirm). loop/operator/orchestrator bypass."""
    if CALLER["kind"] != "skill":
        return
    role = CALLER["role"]
    if role in ("operator", "orchestrator"):
        return
    allowed = _CMD_ROLES.get(command)
    if allowed is not None and role not in allowed:
        _deny(command, role)


def loop_guard(conn, record_type, quest_id):
    """Optional (DEEPRESEARCH_SKILL_LOOP_GUARD=1): a skill-invoked Tier-B science write must run inside an
    OPEN round for the quest, so free invocation cannot desync round/handoff accounting."""
    if CALLER["kind"] != "skill" or os.environ.get("DEEPRESEARCH_SKILL_LOOP_GUARD") not in ("1", "true", "yes"):
        return
    if record_type not in _TIER_B_RT or not quest_id:
        return
    try:
        n = conn.execute("SELECT COUNT(*) FROM round WHERE quest_id=? AND status='open'", (quest_id,)).fetchone()[0]
    except sqlite3.OperationalError:
        return
    if not n:
        raise RecordError(f"skill loop-context guard: no OPEN round for quest {quest_id!r}; a Tier-B science "
                          "write must run inside an active round (set DEEPRESEARCH_SKILL_LOOP_GUARD=0 to relax).")


def audit_write(conn, record_type, quest_id, at, detail="", rid=""):
    """Stamp a quest-owned audit artifact for a skill-invoked mutation (distinguishes skill vs loop writes).
    Free-text artifact.kind → no schema change; quest-isolated. The id includes the written record_id so two
    same-record_type writes at the same `at` don't collide (each gets its own audit row)."""
    if CALLER["kind"] != "skill" or not quest_id or not at:
        return
    aid = f"{quest_id}:skillaudit:{record_type}:{rid}:{at}"
    ref = f"skill={CALLER['skill']} role={CALLER['role']} rt={record_type} {detail}".strip()
    try:
        conn.execute("INSERT OR IGNORE INTO artifact(artifact_id,quest_id,kind,ref,created_at) VALUES(?,?,?,?,?)",
                     (aid, quest_id, "skill-invocation", ref, at))
    except sqlite3.OperationalError:
        pass


def apply(conn: sqlite3.Connection, payload: dict) -> dict:
    validate(payload)
    rt = payload["record_type"]
    spec = RECORD_MAP[rt]
    table, pk = spec["table"], spec["pk"]
    at = payload["at"]
    # Skill-caller authority + loop-context guard (caller-agnostic; loop/operator bypass).
    authorize(rt)
    loop_guard(conn, rt, payload.get("quest_id"))

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

    # Pre-loop launch gates: a quest may not START (not_started -> running) unless (a) the operator has
    # confirmed its GPU device set, and (b) the mandatory pre-launch ambiguity check has been recorded.
    # Both are launch preconditions, not mid-loop prompts. Only the initial launch is gated; resume
    # transitions (paused/recovering/parked -> running) are NOT re-gated.
    if table == "quest" and cols.get("run_state") == "running":
        _clarification_gate(conn, pkvals["quest_id"])
        _contract_gate(conn, pkvals["quest_id"])
        _effort_gate(conn, pkvals["quest_id"])
        _gpu_launch_gate(conn, pkvals["quest_id"])
        _autonomy_gate(conn, pkvals["quest_id"])

    # Contract freeze: objective is immutable post-launch; acceptance changes only via a confirmed
    # amend-acceptance decision. Pre-launch (not_started) and unchanged refs are free; both gates fail-closed.
    if table == "quest":
        if "objective_ref" in cols:
            _objective_frozen_gate(conn, pkvals["quest_id"], cols["objective_ref"])
        if "acceptance_ref" in cols:
            _acceptance_amend_gate(conn, pkvals["quest_id"], cols["acceptance_ref"])
        if "baseline_gate" in cols:
            _baseline_contract_gate(conn, pkvals["quest_id"], cols["baseline_gate"])

    # Pre-finalize gates: a `complete` finalize must meet the scholarship bar and — in auto mode at
    # the gating rigor — the research-completeness checklist.
    if table == "finalize_outcome" and cols.get("outcome") == "complete":
        _finalize_scholarship_gate(conn, cols.get("quest_id"))
        _finalize_completeness_gate(conn, cols.get("quest_id"))
        _finalize_authenticity_gate(conn, cols.get("quest_id"))
        _finalize_coverage_gate(conn, cols.get("quest_id"))
        _finalize_review_gate(conn, cols.get("quest_id"))

    # Detect an open->closed round transition BEFORE the write so the plan_revision bump (below) fires once.
    round_closing = False
    if table == "round" and cols.get("status") == "closed":
        prev = conn.execute("SELECT status FROM round WHERE quest_id=? AND round_index=?",
                            (pkvals["quest_id"], pkvals["round_index"])).fetchone()
        round_closing = prev is not None and prev[0] != "closed"

    if spec["mode"] == "insert":
        _insert_or_ignore(conn, table, cols)
    elif spec["mode"] == "upsert":
        _upsert(conn, table, pk, cols, spec.get("unique", ()))
    elif spec["mode"] == "update":
        _update(conn, table, pk, pkvals, cols)

    # one plan_revision bump per round close (bounded; the Revisions ledger is one row per change).
    if round_closing:
        _bump_plan_revision(conn, pkvals["quest_id"])

    audit_write(conn, rt, payload.get("quest_id") or pkvals.get("quest_id"), at,
                detail="rid=" + str(payload.get("record_id", "")), rid=str(payload.get("record_id", "")))
    conn.commit()
    return {"record_type": rt, "table": table, "pk": pkvals, "via": CALLER}


def _insert_or_ignore(conn, table, cols):
    keys = list(cols)
    conn.execute(
        f"INSERT OR IGNORE INTO {table} ({','.join(keys)}) VALUES ({','.join('?' * len(keys))})",
        [cols[k] for k in keys],
    )


def _upsert(conn, table, pk, cols, unique=()):
    keys = list(cols)
    setcols = [k for k in keys if k not in pk and k != "created_at"]
    # Secondary UNIQUE constraints: a row may already exist under a DIFFERENT primary key but the same unique
    # tuple — e.g. frontier_entry has a surrogate entry_id PK plus UNIQUE(quest_id, candidate_ref). A plain
    # ON CONFLICT(pk) upsert would not see that collision and would raise IntegrityError. So for any declared
    # secondary unique tuple, resolve a pre-existing row and UPDATE it in place (preserving its PK) — keeping
    # the write idempotent on the natural key. The unique tuple scopes the match (it includes quest_id for
    # frontier_entry), so this introduces no cross-quest behavior. Single-PK tables only (frontier is the
    # sole user); other upserts pass unique=() and are unaffected.
    for ucols in unique:
        if all(c in cols for c in ucols):
            where = " AND ".join(f"{c}=?" for c in ucols)
            row = conn.execute(f"SELECT {pk[0]} FROM {table} WHERE {where}",
                               [cols[c] for c in ucols]).fetchone()
            if row is not None and row[0] != cols.get(pk[0]):
                conn.execute(
                    f"UPDATE {table} SET {', '.join(f'{c}=?' for c in setcols)} WHERE {pk[0]}=?",
                    [cols[c] for c in setcols] + [row[0]])
                return
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


# Stages whose handoffs may execute code on a GPU (experiment runs/benchmarks/profiling; analyst
# ablations / mechanism-isolation re-runs). Any handoff in one of these rounds is GPU-gated.
GPU_GATED_STAGES = ("experiment", "analysis")

# Methodology packs each stage MUST cite. A WORKER stage binds methodology through its TYPED RECORD + validator
# (idea.select / baseline.contract / analysis.bridge / paper_spine / review.verdict; `methodology check` resolves
# task-result.methodology_used[].applied_as to it). An ORCHESTRATOR-INTERNAL stage (decision/optimize/finalize)
# has no worker task-result and no typed record, so the Orchestrator records an advisory
# artifact(kind='methodology-usage') at round close; `plan validate` warns (advisory, regime-gated) when a closed
# orchestrator-internal round lacks it. NOT authoritative over DB state — an audit/advisory overlay only.
# ORCHESTRATOR_INTERNAL_STAGES marks the ones the Orchestrator self-audits (vs worker-dispatched stages).
ORCHESTRATOR_INTERNAL_STAGES = ("decision", "optimize", "finalize")
REQUIRED_PACKS = {
    # worker-dispatched stages (enforced via on-task-request 3b + the on-task-result fold check)
    "intake-audit": ["intake-rubric"],
    "scope":        ["ideation-rubric"],
    "baseline":     ["ideation-rubric", "research-method"],
    "idea":         ["ideation-rubric"],
    "experiment":   ["research-method"],
    "analysis":     ["research-method"],
    "outline":      ["paper-craft"],
    "write":        ["paper-craft"],
    "review":       ["review-craft"],
    "rebuttal":     ["rebuttal-craft"],
    # orchestrator-internal stages (Orchestrator self-records the methodology-usage artifact at round close)
    "decision":     ["research-method"],
    "optimize":     ["research-method"],
    "finalize":     ["research-method"],
}


def _gpu_gate(conn, quest_id, round_index, handoff_id):
    """Hard gate: a handoff whose round is a GPU-gated stage (experiment or analysis) may not open unless
    the quest has an operator-CONFIRMED gpu_allocation. Stage is read from the `round` (handoff has no
    stage column). Fail-closed (confirmed-but-missing devices => blocked). Handoffs in other / unknown
    stages pass. The Experimenter additionally restricts CUDA_VISIBLE_DEVICES to the confirmed set at run
    time (`experiment run` injects it and itself fails closed)."""
    if round_index is None:
        return  # round-less handoff: cannot be a code-executing dispatch
    rr = conn.execute("SELECT stage FROM round WHERE quest_id=? AND round_index=?", (quest_id, round_index)).fetchone()
    if not rr or rr[0] not in GPU_GATED_STAGES:
        return
    stage = rr[0]
    try:
        row = conn.execute("SELECT status, devices FROM gpu_allocation WHERE quest_id=?", (quest_id,)).fetchone()
    except sqlite3.OperationalError:
        row = None
    if not row or row[0] != "confirmed" or not row[1]:
        raise RecordError(
            f"{stage} dispatch blocked for quest {quest_id!r} (handoff {handoff_id!r}): GPU use is not "
            f"operator-confirmed. An operator must run `gpu confirm --quest-id {quest_id} --devices <list>` "
            f"(or record gpu.confirm) before any GPU-using stage ({'/'.join(GPU_GATED_STAGES)}) may run.")


def _gpu_launch_gate(conn, quest_id):
    """Pre-loop gate: a quest may not START (not_started -> running) without an operator-confirmed
    gpu_allocation. GPU confirmation is a launch precondition established during quest setup, NOT a
    mid-loop prompt. Resume transitions (paused/recovering/parked -> running) are exempt — confirmation
    was already required at first launch, so the live loop never re-asks. Fail-closed."""
    cur = conn.execute("SELECT run_state FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    if cur is not None and cur[0] != "not_started":
        return  # resume, not initial launch
    try:
        row = conn.execute("SELECT status, devices FROM gpu_allocation WHERE quest_id=?", (quest_id,)).fetchone()
    except sqlite3.OperationalError:
        row = None
    if not row or row[0] != "confirmed" or not row[1]:
        raise RecordError(
            f"quest {quest_id!r} cannot start (run_state -> running): GPU use is not operator-confirmed. "
            f"Run `gpu confirm --quest-id {quest_id} --devices <list>` during quest setup, BEFORE launching "
            f"the loop. GPU confirmation is a pre-loop requirement, not a mid-loop prompt.")


def _clarification_gate(conn, quest_id):
    """Pre-loop gate: a quest may not START (not_started -> running) until the mandatory pre-launch
    ambiguity check has been recorded — a kind='clarification' artifact for the quest (pointing at
    runs/<q>/objective/clarification.md), capturing either 'no blocking ambiguity' or the operator's
    resolved clarifications folded into the objective/acceptance brief. Fail-closed. Resume transitions
    (paused/recovering/parked -> running) are exempt — the check was already done at first launch."""
    cur = conn.execute("SELECT run_state FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    if cur is not None and cur[0] != "not_started":
        return  # resume, not initial launch
    try:
        n = conn.execute("SELECT COUNT(*) FROM artifact WHERE quest_id=? AND kind='clarification'",
                         (quest_id,)).fetchone()[0]
    except sqlite3.OperationalError:
        n = 0
    if not n:
        raise RecordError(
            f"quest {quest_id!r} cannot start (run_state -> running): the mandatory pre-launch ambiguity "
            f"check has not been recorded. Run the clarification step during quest setup and record a "
            f"kind='clarification' artifact (runs/{quest_id}/objective/clarification.md) BEFORE launching. "
            f"The objective must be reviewed for unclear/underspecified parts (objective, acceptance, GPU, "
            f"domain, workspace, budget, domain constraints) and confirmed by the operator first.")


def _contract_gate(conn, quest_id):
    """Pre-loop gate: a quest may not START (not_started -> running) until an operator-approved
    research contract has been recorded — a kind='research-contract' artifact for the quest (the expanded +
    approved objective/acceptance done-bar; see execplan/docs/research-contract.md). This turns a minimal
    operator prompt into a deeper scientific done-bar before the loop optimizes anything. Fail-closed. Resume
    transitions (paused/recovering/parked -> running) are exempt — the contract was approved at first launch."""
    cur = conn.execute("SELECT run_state FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    if cur is not None and cur[0] != "not_started":
        return  # resume, not initial launch
    try:
        n = conn.execute("SELECT COUNT(*) FROM artifact WHERE quest_id=? AND kind='research-contract'",
                         (quest_id,)).fetchone()[0]
    except sqlite3.OperationalError:
        n = 0
    if not n:
        raise RecordError(
            f"quest {quest_id!r} cannot start (run_state -> running): no operator-approved research contract "
            f"recorded. Run the pre-launch research-contract expansion (deepresearch-research-contract / "
            f"execplan/docs/research-contract.md): expand the minimal Objective/Acceptance into a deeper "
            f"done-bar, get the operator to approve/edit/trim it, fold it into runs/{quest_id}/objective/, and "
            f"record a kind='research-contract' artifact (runs/{quest_id}/objective/contract.md) BEFORE "
            f"launching — a sibling of the clarification, (Claude) effort, and GPU gates.")


def _effort_gate(conn, quest_id):
    """Pre-loop gate: a Claude-backed quest may not START (not_started -> running) until the operator's
    Claude effort/reasoning level has been recorded — a kind='effort-selection' artifact for the quest
    (runs/<q>/objective/effort.md). CLAUDE-CONDITIONAL: only quests with >=1 participant whose tool='claude'
    are gated; non-Claude backends are exempt (effort selection is Claude-specific). Fail-closed. Resume
    transitions (paused/recovering/parked -> running) are exempt — the level was chosen at first launch.
    The effort level itself is applied out-of-band as a launch-time override (`agents launch
    --reasoning-level`), NOT via `profile set` (the shared deepresearch-* profiles stay pristine); this gate
    only enforces that the operator's choice is recorded before the quest goes live. See
    execplan/docs/claude-effort.md + start-runbook Step 3c."""
    cur = conn.execute("SELECT run_state FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    if cur is not None and cur[0] != "not_started":
        return  # resume, not initial launch
    try:
        claude = conn.execute(
            "SELECT COUNT(*) FROM participant WHERE quest_id=? AND tool='claude'", (quest_id,)).fetchone()[0]
    except sqlite3.OperationalError:
        claude = 0
    if not claude:
        return  # non-Claude backend (or no participants registered yet): effort selection N/A
    try:
        n = conn.execute("SELECT COUNT(*) FROM artifact WHERE quest_id=? AND kind='effort-selection'",
                         (quest_id,)).fetchone()[0]
    except sqlite3.OperationalError:
        n = 0
    if not n:
        raise RecordError(
            f"quest {quest_id!r} cannot start (run_state -> running): Claude agents are in use but no Claude "
            f"effort level has been recorded. Run the pre-launch effort selection (start-runbook Step 3c): "
            f"ask the operator to choose an effort level, apply it as a launch-time override "
            f"(`agents launch --reasoning-level`, NOT `profile set`), write runs/{quest_id}/objective/effort.md, and record a "
            f"kind='effort-selection' artifact BEFORE launching — a sibling of the clarification + "
            f"research-contract + GPU gates. Mapping: execplan/docs/claude-effort.md.")


# ── Run mode + plan revision (Phases 1, 3) ───────────────────────────────────
def _autonomy_gate(conn, quest_id):
    """Pre-loop gate: a quest may not START (not_started -> running) until the operator has chosen a
    run mode (quest.autonomy_mode IN ('auto','assistant')). Orthogonal to execution_mode. Resume transitions
    are exempt — the mode was chosen at first launch. Fail-closed."""
    try:
        cur = conn.execute("SELECT run_state, autonomy_mode FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    except sqlite3.OperationalError:
        return  # column not migrated yet (older schema): do not block
    if cur is not None and cur[0] != "not_started":
        return  # resume, not initial launch
    mode = cur[1] if cur else None
    if mode not in ("auto", "assistant"):
        raise RecordError(
            f"quest {quest_id!r} cannot start (run_state -> running): no run mode chosen. The operator must set "
            f"quest.autonomy_mode to 'auto' (loop self-disposes; completeness checks hard-gate at publication "
            f"rigor) or 'assistant' (advisory; operator disposes) BEFORE launch — a sibling of the GPU / "
            f"clarification / research-contract / effort gates. See start-runbook Step 3d.")


def _bump_plan_revision(conn, quest_id):
    """Increment the quest's plan_revision. Called on each round close and on a confirmed acceptance
    amendment, so the rendered plan.md `## Revisions` ledger gets one entry per meaningful change."""
    try:
        conn.execute("UPDATE quest SET plan_revision = plan_revision + 1 WHERE quest_id=?", (quest_id,))
    except sqlite3.OperationalError:
        pass


# ── Contract freeze: objective immutable; acceptance append-only + operator-gated ──────────────
def _objective_frozen_gate(conn, quest_id, new_objective_ref):
    """objective_ref is IMMUTABLE post-launch in this roadmap (acceptance-only amendments). Reject any change
    once the quest has left not_started. Pre-launch edits are free."""
    cur = conn.execute("SELECT run_state, objective_ref FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    if cur is None or cur[0] == "not_started":
        return
    if new_objective_ref != cur[1]:
        raise RecordError(
            f"quest {quest_id!r}: objective_ref is frozen post-launch (acceptance-only amendments are "
            f"supported; objective amendments are not in this roadmap). No moving the objective.")


def _acceptance_amend_gate(conn, quest_id, new_acceptance_ref):
    """A post-launch change to quest.acceptance_ref is allowed ONLY when backed by a CONFIRMED
    decision(route='amend-acceptance') the operator approved. Pre-launch (not_started) edits are free
    (the contract isn't frozen yet). Append-only: callers write acceptance.md@rev-K and never overwrite rev 1."""
    cur = conn.execute("SELECT run_state, acceptance_ref FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    if cur is None or cur[0] == "not_started":
        return  # pre-launch: contract not yet frozen
    if new_acceptance_ref == cur[1]:
        return  # no change
    ok = conn.execute(
        "SELECT COUNT(*) FROM decision WHERE quest_id=? AND route='amend-acceptance' AND confirmed=1",
        (quest_id,)).fetchone()[0]
    if not ok:
        raise RecordError(
            f"quest {quest_id!r}: acceptance_ref may not change post-launch without an operator-confirmed "
            f"decision(route='amend-acceptance'). Record the amendment decision + decision.confirm first, write "
            f"a new acceptance.md@rev-K (append-only) — never overwrite the original contract.")


# ── Research-completeness checklist + finalize gate ─────────────────────────────────────────
def _completeness_flag(name, default=True):
    """Per-item required toggle (env override). DEEPRESEARCH_COMPLETENESS_REQUIRE_<NAME>=0 makes an item
    advisory; =1 forces it required. Default 'required' for the new mechanism/alternative/ablation items."""
    raw = os.environ.get(f"DEEPRESEARCH_COMPLETENESS_REQUIRE_{name.upper()}")
    if raw is None:
        return default
    return raw not in ("0", "false", "no")


def completeness_audit(conn, quest_id, rigor="standard"):
    """The seven general scientific-quality checks. Composes existing checks (evidence traceability /
    no-orphan-claims / lit audit) with new mechanism / named-alternative / ablation-or-infeasibility /
    discrepancy reads. Returns {ok, required, reasons, items}. `ok` reflects only the REQUIRED items; advisory
    items surface in `items` but never set ok=False. Mirrors scholarship_audit in shape."""
    items, reasons, required = {}, [], []

    def q1(sql, *p):
        return conn.execute(sql, p).fetchone()[0]

    # 1 evidence traceability: every supported claim has supports-evidence (also an invariant).
    untraceable = q1("SELECT COUNT(*) FROM claim c WHERE c.quest_id=? AND c.status='supported' AND NOT EXISTS "
                     "(SELECT 1 FROM claim_evidence e WHERE e.claim_id=c.claim_id AND e.relation='supports')", quest_id)
    items["evidence_traceability"] = untraceable == 0
    # 2 no orphan claims.
    orphan = q1("SELECT COUNT(*) FROM claim c WHERE c.quest_id=? AND NOT EXISTS "
                "(SELECT 1 FROM claim_evidence e WHERE e.claim_id=c.claim_id)", quest_id)
    items["no_orphan_claims"] = orphan == 0
    # 3 mechanism explanation: >=1 analysis-backed link on a main claim, or any analysis row.
    mech = q1("SELECT COUNT(*) FROM claim_evidence e JOIN claim c ON c.claim_id=e.claim_id "
              "WHERE c.quest_id=? AND e.source_kind='analysis'", quest_id) \
        or q1("SELECT COUNT(*) FROM analysis WHERE quest_id=?", quest_id)
    items["mechanism_explanation"] = mech > 0
    # 4 named alternatives: a rival explanation is on record.
    alts = q1("SELECT COUNT(*) FROM claim WHERE quest_id=? AND kind IN ('alternative','competing_hypothesis')", quest_id)
    items["named_alternatives"] = alts > 0
    # 5 ablation OR documented infeasibility (a limitation claim).
    abl = q1("SELECT COUNT(*) FROM analysis WHERE quest_id=?", quest_id)
    lim = q1("SELECT COUNT(*) FROM claim WHERE quest_id=? AND kind='limitation'", quest_id)
    items["ablation_or_infeasibility"] = (abl > 0) or (lim > 0)
    # 6 reference / lit audit (reuses the scholarship bar).
    try:
        items["reference_lit_audit"] = scholarship_audit(conn, quest_id)["ok"]
    except sqlite3.OperationalError:
        items["reference_lit_audit"] = True
    # 7 unresolved-discrepancy handling: no open contradiction on a supported claim.
    open_contra = q1("SELECT COUNT(*) FROM claim c WHERE c.quest_id=? AND c.status='supported' AND EXISTS "
                     "(SELECT 1 FROM claim_evidence e WHERE e.claim_id=c.claim_id AND e.relation='contradicts' "
                     "AND e.resolved=0)", quest_id)
    items["discrepancy_handling"] = open_contra == 0

    # Required subset: 1,2,6,7 are always required (mirror existing hard checks); 3,4,5 (the new science-depth
    # items) are required by default but individually waivable via env to scale a focused vs flagship study.
    always = {"evidence_traceability": True, "no_orphan_claims": True,
              "reference_lit_audit": True, "discrepancy_handling": True}
    waivable = {"mechanism_explanation": _completeness_flag("MECHANISM"),
                "named_alternatives": _completeness_flag("ALTERNATIVES"),
                "ablation_or_infeasibility": _completeness_flag("ABLATION")}
    for name, req in {**always, **waivable}.items():
        if req:
            required.append(name)
            if not items[name]:
                reasons.append(f"{name} not satisfied")
    return {"ok": not reasons, "required": required, "reasons": reasons, "items": items, "rigor": rigor}


def _rigor_order(level):
    return {"scoping": 0, "standard": 1, "publication": 2}.get(level or "standard", 1)


def _finalize_completeness_gate(conn, quest_id):
    """Pre-finalize gate: a 'complete' finalize is HARD-BLOCKED only when BOTH autonomy_mode='auto'
    and the contract rigor meets the gating threshold (default 'publication'). Otherwise (assistant any rigor,
    or auto below threshold) the checklist is advisory — the tick recommends and the operator disposes.
    Idempotent; legacy NULL columns exempt; older schemas never break."""
    if not quest_id:
        return
    try:
        if conn.execute("SELECT COUNT(*) FROM finalize_outcome WHERE quest_id=? AND outcome='complete'",
                        (quest_id,)).fetchone()[0]:
            return  # idempotent re-finalize / recovery replay
        row = conn.execute("SELECT autonomy_mode, rigor_level FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    except sqlite3.OperationalError:
        return  # schema predates the columns: do not block
    if not row:
        return
    mode, rigor = row[0], (row[1] or "standard")
    threshold = os.environ.get("DEEPRESEARCH_COMPLETENESS_GATE_RIGOR", "publication")
    if threshold == "none" or mode != "auto" or _rigor_order(rigor) < _rigor_order(threshold):
        return  # advisory only: assistant, or auto below the rigor threshold — tick recommends, never hard-block
    try:
        audit = completeness_audit(conn, quest_id, rigor)
    except sqlite3.OperationalError:
        return
    if not audit["ok"]:
        raise RecordError(
            f"quest {quest_id!r} cannot finalize 'complete' (auto, rigor={rigor}): research-completeness not "
            "met — " + "; ".join(audit["reasons"]) + ". Continue the science (route back to experiment/analysis) "
            "or finalize as 'park' with explicit reopen_conditions. Scale rigor: "
            "DEEPRESEARCH_COMPLETENESS_GATE_RIGOR / DEEPRESEARCH_COMPLETENESS_REQUIRE_* env knobs.")


# ── Literature / scholarship bar ─────────────────────────────────
# Tunable via env (the config knob). Defaults are deliberately modest: the teeth come from claim↔reference
# linkage, not raw reference count. Set both env vars to 0 to waive the bar (deliberate operator override).
def _scholarship_thresholds():
    def _int(name, default):
        try:
            return max(0, int(os.environ.get(name, default)))
        except (TypeError, ValueError):
            return default
    return (_int("DEEPRESEARCH_SCHOLARSHIP_MIN_REFS", 3),
            _int("DEEPRESEARCH_SCHOLARSHIP_MIN_REF_CLAIMS", 1))


def scholarship_audit(conn, quest_id):
    """Shared scholarship check. Used by `lit audit` (advisory) and the finalize gate (hard).

    HARD-fail signals (set `ok=False`): too few `reference` rows, or no claim positioned against a reference
    (claim_evidence source_kind='reference'). The claim↔reference link is the real teeth — it forces genuine
    scholarly positioning, not a padded bibliography. SOFT signals (warnings, never fail): an all-`manual`
    bibliography (possible tool-doc-only) and a missing 'Related Work' heading — quality cues the harness
    cannot adjudicate, left to the Reviewer + `execplan/docs/publication-quality.md`."""
    min_refs, min_ref_claims = _scholarship_thresholds()
    # Count this quest's references for the bar. References are quest-owned (no cross-quest/global refs
    # exist — schema requires quest_id; invariant reference_quest_owned), so this is the full bibliography.
    refs_total = conn.execute(
        "SELECT COUNT(*) FROM reference WHERE quest_id=?", (quest_id,)).fetchone()[0]
    refs_external = conn.execute(
        "SELECT COUNT(*) FROM reference WHERE quest_id=? AND source IN ('arxiv','doi','web')",
        (quest_id,)).fetchone()[0]
    ref_claims = conn.execute(
        "SELECT COUNT(DISTINCT e.claim_id) FROM claim_evidence e JOIN claim c ON c.claim_id=e.claim_id "
        "WHERE c.quest_id=? AND e.source_kind='reference'", (quest_id,)).fetchone()[0]
    related_work = _has_related_work(quest_id)
    reasons, warnings = [], []
    if refs_total < min_refs:
        reasons.append(f"only {refs_total} reference row(s); need >= {min_refs} "
                       f"(record prior art via `lit fetch` / reference.record)")
    if ref_claims < min_ref_claims:
        reasons.append(f"{ref_claims} claim(s) positioned against a reference; need >= {min_ref_claims} "
                       f"(link a positioning claim with claim_evidence.link source_kind='reference')")
    if refs_total and refs_external == 0:
        warnings.append("all references are source='manual' — confirm these are real external academic "
                        "citations, not only tool/vendor docs")
    if related_work is False:
        warnings.append("no 'Related Work' heading found in runs/<q>/report/paper.md|tex — confirm genuine "
                        "scholarly positioning, not an internal-provenance note")
    return {"ok": not reasons, "reasons": reasons, "warnings": warnings,
            "refs_total": refs_total, "refs_external": refs_external,
            "reference_backed_claims": ref_claims, "related_work_present": related_work,
            "thresholds": {"min_refs": min_refs, "min_reference_backed_claims": min_ref_claims}}


def _has_related_work(quest_id):
    """True/False whether a manuscript carries a Related Work heading; None if no manuscript exists yet."""
    from paths import LOOP_DIR
    found_any = False
    for name in ("paper.md", "paper.tex"):
        p = LOOP_DIR / "runs" / str(quest_id) / "report" / name
        if p.exists():
            found_any = True
            try:
                txt = p.read_text(encoding="utf-8", errors="ignore").lower()
            except OSError:
                continue
            if "related work" in txt or "related-work" in txt:
                return True
    return False if found_any else None


def _finalize_scholarship_gate(conn, quest_id):
    """Pre-finalize gate: a `complete` finalize is blocked unless the scholarship bar is met
    (>= min reference rows AND >= min reference-backed claim). Only `complete` is gated (stop/park/publish
    are not). Fail-closed; the error routes the loop back to `write`. Waive via the env knobs in
    `_scholarship_thresholds` (both 0)."""
    if not quest_id:
        return
    try:
        already = conn.execute(
            "SELECT COUNT(*) FROM finalize_outcome WHERE quest_id=? AND outcome='complete'",
            (quest_id,)).fetchone()[0]
    except sqlite3.OperationalError:
        already = 0
    if already:
        return  # idempotent re-finalize / recovery replay of an already-completed quest: do not re-gate
    try:
        audit = scholarship_audit(conn, quest_id)
    except sqlite3.OperationalError:
        return  # schema predates the literature tables; do not block
    if not audit["ok"]:
        raise RecordError(
            f"quest {quest_id!r} cannot finalize as 'complete': scholarship bar not met — "
            + "; ".join(audit["reasons"])
            + ". Route back to `write` to add a genuine Related Work section with real, claim-linked "
            "citations (see execplan/docs/publication-quality.md). Override: set "
            "DEEPRESEARCH_SCHOLARSHIP_MIN_REFS=0 and DEEPRESEARCH_SCHOLARSHIP_MIN_REF_CLAIMS=0.")


def _finalize_authenticity_gate(conn, quest_id):
    """Pre-finalize gate (evidence authenticity, from the review-craft authenticity gate — the q1 Finding B
    defect made hard): a `complete` finalize is blocked unless the quest's headline result
    (quest.best_result_ref) backs at least one claim via a claim_evidence link of source_kind='result'. This
    stops the central empirical result from being 'supported' only by a positioning citation. Only `complete`
    is gated; idempotent re-finalize and quests with no best_result_ref are exempt. Waive with
    DEEPRESEARCH_AUTHENTICITY_GATE=0. See execplan/packs/review-craft/references/authenticity-gate.md."""
    if not quest_id or os.environ.get("DEEPRESEARCH_AUTHENTICITY_GATE") in ("0", "false", "no"):
        return
    try:
        if conn.execute("SELECT COUNT(*) FROM finalize_outcome WHERE quest_id=? AND outcome='complete'",
                        (quest_id,)).fetchone()[0]:
            return  # idempotent re-finalize / recovery replay
        best = conn.execute("SELECT best_result_ref FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    except sqlite3.OperationalError:
        return  # schema predates the columns: do not block
    best = best[0] if best else None
    if not best:
        return  # no headline result recorded: nothing to authenticate (other gates still apply)
    backed = conn.execute(
        "SELECT COUNT(*) FROM claim_evidence e JOIN claim c ON c.claim_id=e.claim_id "
        "WHERE c.quest_id=? AND e.source_kind='result' AND e.source_ref=? AND e.relation='supports'",
        (quest_id, best)).fetchone()[0]
    if not backed:
        raise RecordError(
            f"quest {quest_id!r} cannot finalize as 'complete': the headline result best_result_ref={best!r} "
            "backs no supported claim (claim_evidence source_kind='result'). The central empirical result must "
            "substantiate its own claim — a positioning citation cannot stand in for it (review-craft "
            "authenticity gate, Finding B). Add a result-backed headline claim "
            "(`claim_evidence.link source_kind='result' source_ref=<best_result_ref>`) and re-bundle, then "
            "finalize. Override: DEEPRESEARCH_AUTHENTICITY_GATE=0.")


def _has_research_contract(conn, quest_id):
    """True if the quest was launched under the research-contract regime (has a kind='research-contract'
    artifact). The coverage gate binds only for these quests, so pre-feature / ad-hoc quests are exempt."""
    try:
        return conn.execute("SELECT COUNT(*) FROM artifact WHERE quest_id=? AND kind='research-contract'",
                            (quest_id,)).fetchone()[0] > 0
    except sqlite3.OperationalError:
        return False


def _finalize_coverage_gate(conn, quest_id):
    """Pre-finalize gate: a `complete` finalize is HARD-BLOCKED unless the manuscript-coverage validator
    has computed `paper_spine.submission_ready=1`. Gates on the VALIDATOR-COMPUTED flag — a paper-spine
    artifact merely existing is NOT sufficient (the writer's paper_spine.upsert force-resets the flag to 0;
    only `manuscript coverage` sets it). Binds for research-contract quests at rigor >= 'standard'; advisory
    (no block) for scoping rigor, pre-contract/history quests, or older DBs without the paper_spine table.
    Idempotent re-finalize is exempt. Waive: DEEPRESEARCH_COVERAGE_GATE=0."""
    if not quest_id or os.environ.get("DEEPRESEARCH_COVERAGE_GATE") in ("0", "false", "no"):
        return
    try:
        if conn.execute("SELECT COUNT(*) FROM finalize_outcome WHERE quest_id=? AND outcome='complete'",
                        (quest_id,)).fetchone()[0]:
            return  # idempotent re-finalize / recovery replay
        qrow = conn.execute("SELECT rigor_level FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    except sqlite3.OperationalError:
        return  # schema predates the columns: do not block
    if not qrow:
        return
    rigor = qrow[0] or "standard"
    # Regime: bind only for research-contract quests at standard/publication rigor; scoping is advisory.
    if not _has_research_contract(conn, quest_id) or _rigor_order(rigor) < _rigor_order("standard"):
        return
    try:
        sp = conn.execute("SELECT submission_ready FROM paper_spine WHERE quest_id=?", (quest_id,)).fetchone()
    except sqlite3.OperationalError:
        return  # paper_spine table absent on an un-reinited DB: do not block
    if not (sp and sp[0]):
        raise RecordError(
            f"quest {quest_id!r} cannot finalize as 'complete' (rigor={rigor}): manuscript coverage is not "
            "validator-confirmed submission_ready. Run `manuscript coverage --quest-id <q> --artifact-ref "
            "<runs/<q>/report/paper.md> --spine-ref <runs/<q>/paper/spine.json>` and resolve every reported gap "
            "(unmapped results, main claims without supporting evidence, empty not_claiming/limitations, "
            "process/draft traces), then re-finalize. A paper-spine artifact existing is NOT sufficient — the "
            "gate reads the validator-computed flag. Override: DEEPRESEARCH_COVERAGE_GATE=0.")


def _finalize_review_gate(conn, quest_id):
    """Pre-finalize gate: a `complete` finalize is HARD-BLOCKED unless the LATEST review verdict is
    validator-confirmed actionable (`valid=1`, set by `review validate`) AND permits finalization — `accept`
    at any bound rigor, or operator-confirmed `borderline` at standard rigor (publication never permits
    borderline). `reject` / missing / invalid / unconfirmed-borderline all block. Gates on the typed valid
    verdict, never on a review artifact's existence. Binds for research-contract quests at rigor >= 'standard';
    advisory for scoping / pre-contract / older DBs. INDEPENDENT of the coverage gate — both must pass
    (accept AND submission_ready). Idempotent re-finalize exempt. Waive: DEEPRESEARCH_REVIEW_GATE=0."""
    if not quest_id or os.environ.get("DEEPRESEARCH_REVIEW_GATE") in ("0", "false", "no"):
        return
    try:
        if conn.execute("SELECT COUNT(*) FROM finalize_outcome WHERE quest_id=? AND outcome='complete'",
                        (quest_id,)).fetchone()[0]:
            return  # idempotent re-finalize / recovery replay
        qrow = conn.execute("SELECT rigor_level FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    except sqlite3.OperationalError:
        return
    if not qrow:
        return
    rigor = qrow[0] or "standard"
    if not _has_research_contract(conn, quest_id) or _rigor_order(rigor) < _rigor_order("standard"):
        return  # advisory for scoping / pre-contract quests
    try:
        row = conn.execute("SELECT verdict, valid, operator_confirmed FROM review_verdict WHERE quest_id=? "
                           "ORDER BY created_at DESC, verdict_id DESC LIMIT 1", (quest_id,)).fetchone()
    except sqlite3.OperationalError:
        return  # review_verdict table absent on an un-reinited DB: do not block
    base = f"quest {quest_id!r} cannot finalize as 'complete' (rigor={rigor}): "
    tail = " Override: DEEPRESEARCH_REVIEW_GATE=0."
    if row is None:
        raise RecordError(base + "no review verdict recorded. Run the review stage, record a `review.verdict`, "
                          "and `review validate` it to an 'accept' before finalizing." + tail)
    verdict, valid, confirmed = row[0], row[1], row[2]
    if not valid:
        raise RecordError(base + f"the latest review verdict ({verdict!r}) is not validator-confirmed actionable "
                          "— run `review validate` and add the missing todos for the flaws it raised." + tail)
    if verdict == "reject":
        raise RecordError(base + "the latest review verdict is 'reject'. Route its follow-ups (`review route`) "
                          "and re-review to an 'accept' before finalizing." + tail)
    if verdict == "borderline":
        if _rigor_order(rigor) >= _rigor_order("publication"):
            raise RecordError(base + "publication rigor requires an 'accept' verdict; 'borderline' is not "
                              "sufficient. Route a revision to reach 'accept'." + tail)
        if not confirmed:
            raise RecordError(base + "the latest verdict is 'borderline'; it needs operator confirmation "
                              "(`review confirm`) to finalize at standard rigor, or route a revision to "
                              "reach 'accept'." + tail)
    # accept, or operator-confirmed borderline at standard -> the review side passes. The coverage gate is
    # enforced separately by _finalize_coverage_gate; BOTH are required for a complete finalize.


_BASELINE_OK_VERDICTS = {"verified_match", "close_match", "trusted_with_caveats"}


def _baseline_contract_gate(conn, quest_id, new_gate):
    """Pre-write gate: STRENGTHENS the existing quest.baseline_gate. Setting baseline_gate='passed' requires
    the latest `baseline.contract` to carry an acceptable verification_verdict (verified_match / close_match /
    trusted_with_caveats); setting 'waived' requires verification_verdict='waived' AND a non-empty waiver_reason.
    'pending'/'blocked' are unconstrained. Binds for research-contract quests at rigor >= 'standard'; advisory
    for scoping / pre-contract / older DBs. Waive: DEEPRESEARCH_BASELINE_CONTRACT_GATE=0."""
    if not quest_id or os.environ.get("DEEPRESEARCH_BASELINE_CONTRACT_GATE") in ("0", "false", "no"):
        return
    if new_gate not in ("passed", "waived"):
        return
    try:
        qrow = conn.execute("SELECT rigor_level FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    except sqlite3.OperationalError:
        return
    rigor = (qrow[0] if qrow else None) or "standard"
    if not _has_research_contract(conn, quest_id) or _rigor_order(rigor) < _rigor_order("standard"):
        return
    try:
        row = conn.execute("SELECT verification_verdict, waiver_reason FROM baseline_contract WHERE quest_id=? "
                           "ORDER BY created_at DESC, contract_id DESC LIMIT 1", (quest_id,)).fetchone()
    except sqlite3.OperationalError:
        return  # baseline_contract table absent on an un-reinited DB: do not block
    base = f"quest {quest_id!r} cannot set baseline_gate={new_gate!r}: "
    tail = " Override: DEEPRESEARCH_BASELINE_CONTRACT_GATE=0."
    if row is None:
        raise RecordError(base + "no typed baseline.contract recorded. Record one (baseline id/name, comparison "
                          "policy, metric ids, dataset/split, eval protocol, verification verdict) before opening "
                          "the baseline gate." + tail)
    verdict, waiver = row[0], row[1]
    if new_gate == "passed" and verdict not in _BASELINE_OK_VERDICTS:
        raise RecordError(base + f"latest baseline.contract verdict is {verdict!r}; 'passed' requires one of "
                          f"{sorted(_BASELINE_OK_VERDICTS)} (or set baseline_gate='waived' with a waiver)." + tail)
    if new_gate == "waived" and (verdict != "waived" or not (waiver or "").strip()):
        raise RecordError(base + "'waived' requires a baseline.contract with verification_verdict='waived' AND a "
                          "non-empty waiver_reason." + tail)


def _analysis_bridge_gate(conn, quest_id, round_index, handoff_id):
    """Hard gate: a handoff whose round stage is 'outline' or 'write' may not open unless the quest has a
    validator-confirmed analysis bridge (`analysis_bridge.valid=1`, set by `campaign validate`, which requires
    BOTH a paper-facing bridge AND sufficient per-claim campaign coverage). This stops the Writer from drafting
    from raw experiment logs / an incomplete campaign. Gates on the typed VALID bridge, never on analysis
    artifact existence. Binds for research-contract quests at rigor >= 'standard'; advisory otherwise. Waive:
    DEEPRESEARCH_BRIDGE_GATE=0."""
    if round_index is None or os.environ.get("DEEPRESEARCH_BRIDGE_GATE") in ("0", "false", "no"):
        return
    try:
        rr = conn.execute("SELECT stage FROM round WHERE quest_id=? AND round_index=?",
                          (quest_id, round_index)).fetchone()
    except sqlite3.OperationalError:
        return
    if not rr or rr[0] not in ("outline", "write"):
        return  # guards the analysis -> outline/write transition only
    try:
        qrow = conn.execute("SELECT rigor_level FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    except sqlite3.OperationalError:
        return
    rigor = (qrow[0] if qrow else None) or "standard"
    if not _has_research_contract(conn, quest_id) or _rigor_order(rigor) < _rigor_order("standard"):
        return
    try:
        n = conn.execute("SELECT COUNT(*) FROM analysis_bridge WHERE quest_id=? AND valid=1",
                         (quest_id,)).fetchone()[0]
    except sqlite3.OperationalError:
        return  # analysis_bridge table absent on an un-reinited DB: do not block
    if not n:
        raise RecordError(
            f"{rr[0]} dispatch blocked for quest {quest_id!r} (handoff {handoff_id!r}, rigor={rigor}): no "
            "validator-confirmed analysis bridge / sufficient campaign coverage. Record a typed `analysis.bridge` "
            "(claim->evidence map, mechanism interpretation, alternatives, limitations, paper-facing result "
            "paragraphs) and pass `campaign validate --quest-id <q>` (per-claim coverage by evidence_kind under "
            "the rigor floor) before the Writer may consume analysis. Override: DEEPRESEARCH_BRIDGE_GATE=0.")


def _idea_gate(conn, quest_id, round_index, handoff_id):
    """Hard gate: a handoff whose round stage is 'experiment' may not open unless the quest has a
    validator-confirmed idea selection (`idea_select.valid=1`, set by `idea validate`). Blocks shallow /
    single-proposal / decorative / non-differentiated / below-floor ideas from advancing to experiment. Gates
    on the typed VALID selection, never on an idea artifact's existence. Binds for research-contract quests at
    rigor >= 'standard'; advisory for scoping / pre-contract / older DBs. Stage read from the `round` (handoff
    has no stage column), mirroring _gpu_gate. Waive: DEEPRESEARCH_IDEA_GATE=0."""
    if round_index is None or os.environ.get("DEEPRESEARCH_IDEA_GATE") in ("0", "false", "no"):
        return
    try:
        rr = conn.execute("SELECT stage FROM round WHERE quest_id=? AND round_index=?",
                          (quest_id, round_index)).fetchone()
    except sqlite3.OperationalError:
        return
    if not rr or rr[0] != "experiment":
        return  # the idea gate guards the idea -> experiment transition only
    try:
        qrow = conn.execute("SELECT rigor_level FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    except sqlite3.OperationalError:
        return
    rigor = (qrow[0] if qrow else None) or "standard"
    if not _has_research_contract(conn, quest_id) or _rigor_order(rigor) < _rigor_order("standard"):
        return  # advisory for scoping / pre-contract quests
    try:
        n = conn.execute("SELECT COUNT(*) FROM idea_select WHERE quest_id=? AND valid=1",
                         (quest_id,)).fetchone()[0]
    except sqlite3.OperationalError:
        return  # idea_select table absent on an un-reinited DB: do not block
    if not n:
        raise RecordError(
            f"experiment dispatch blocked for quest {quest_id!r} (handoff {handoff_id!r}, rigor={rigor}): no "
            "validator-confirmed idea selection. Record an `idea.select` (multi-candidate raw_slate + challenge "
            "+ scored selection_gate + concrete rejected[] + a retained idea with mechanism & MVP plan) and pass "
            "`idea validate --quest-id <q>` (it enforces the rigor slate/score floor and rejects single-proposal/"
            "decorative/non-differentiated ideas) before the idea may advance to experiment. "
            "Override: DEEPRESEARCH_IDEA_GATE=0.")


def _special(conn, kind, pkvals, payload, at):
    q, h = pkvals["quest_id"], pkvals["handoff_id"]
    if kind == "handoff_open":
        # GPU-use confirmation gate (experiment-stage rounds only; stage derived from the round).
        ri = payload.get("round_index")
        if ri is None:
            r = conn.execute("SELECT round_index FROM handoff WHERE quest_id=? AND handoff_id=?", (q, h)).fetchone()
            ri = r[0] if r else None
        _gpu_gate(conn, q, ri, h)
        _idea_gate(conn, q, ri, h)
        _analysis_bridge_gate(conn, q, ri, h)
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
