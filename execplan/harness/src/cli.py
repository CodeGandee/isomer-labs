"""DeepResearch harness CLI (click). Groups mirror commands.toml. State writes go through records.apply.

Stub-safe domain-pluggable commands (experiment run, metric validate, render *, bo, lit search, git
checkpoint/status, manuscript/outline validate) return ok with data.stub=true and do only the minimal
state writes their contract promises; a domain knowledge-pack adapter replaces the stub later.
"""
from __future__ import annotations
import json
import os
import sys
import click
import jsonschema

import db
import records
import invariants as inv
import mail
from envelope import envelope, emit
from paths import resolve_db, COMMS_SCHEMAS, COMMS_RENDERERS, LOOP_DIR


def _conn(ctx):
    return db.connect(resolve_db(ctx.obj.get("db")))


def _finish(ctx, conn, cmd, data, *, quest_id=None, warnings=None):
    """Optionally run post-write `state validate` (when --validate-after-write), then close + emit.

    Exits non-zero if post-write validation finds violations, so smoke tests catch regressions.
    """
    warnings = list(warnings or [])
    ok, diag = True, []
    if ctx.obj.get("vaw"):
        res = inv.run_all(conn)
        data = {**data, "post_validate": res}
        if not res["ok"]:
            ok, diag = False, ["post-write validation failed"]
    conn.close()
    emit(envelope(cmd, ok=ok, data=data, diagnostics=diag, quest_id=quest_id, warnings=warnings))
    if not ok:
        sys.exit(1)


def _payload(json_opt, file_opt):
    if json_opt:
        return json.loads(json_opt)
    if file_opt:
        return json.loads(open(file_opt).read())
    return json.loads(sys.stdin.read())


def _apply(ctx, cmd, payload, *, quest_id=None):
    try:
        conn = _conn(ctx)
        data = records.apply(conn, payload)
    except records.RecordError as e:
        emit(envelope(cmd, ok=False, diagnostics=[str(e)], quest_id=quest_id))
        sys.exit(1)
    _finish(ctx, conn, cmd, data, quest_id=quest_id)


@click.group()
@click.option("--db", "db_path", default=None, help="Override state DB path (default <loop-dir>/runs/state.sqlite).")
@click.option("--validate-after-write", "vaw", is_flag=True, default=False,
              help="Run `state validate` after each mutating command; fail the command on violations. Off by default.")
@click.option("--via", default=None,
              help="Caller identity for authority + audit: 'skill:<skill-id>:<role>' (an agent-invoked skill, "
                   "authority-checked + audited), or 'loop:<role>'/'operator' (unrestricted; default when omitted).")
@click.pass_context
def cli(ctx, db_path, vaw, via):
    ctx.obj = {"db": db_path, "vaw": vaw, "via": via}
    records.set_caller(via)  # caller-agnostic gates still apply; this only adds skill-authority + audit


def _authz_cmd(command):
    """Enforce role for a stateful COMMAND invoked as a skill (clean envelope error on denial)."""
    try:
        records.authorize_command(command)
    except records.RecordError as e:
        emit(envelope(command, ok=False, diagnostics=[str(e)])); sys.exit(1)


# ───────────────── state ─────────────────
@cli.group()
def state(): ...


@state.command("init")
@click.pass_context
def state_init(ctx):
    emit(envelope("state init", data=db.init(resolve_db(ctx.obj.get("db")))))


@state.command("validate")
@click.pass_context
def state_validate(ctx):
    conn = _conn(ctx)
    res = inv.run_all(conn)
    conn.close()
    emit(envelope("state validate", ok=res["ok"], data=res,
                  diagnostics=[] if res["ok"] else ["invariant or FK violations present"]))
    if not res["ok"]:
        sys.exit(1)


_VIEWS = {
    "cursor": ("SELECT quest_id, run_state, round_index, current_stage, baseline_gate, "
               "active_branch_id, active_idea_id, best_result_ref FROM quest", False),
    "open-wakeups": ("SELECT * FROM self_wakeup WHERE status IN ('armed','delivered')", True),
    "due-handoffs": ("SELECT * FROM handoff WHERE status NOT IN ('processed','failed')", True),
    "best-result": ("SELECT quest_id, best_result_ref FROM quest", True),
    "open-claims": ("SELECT * FROM claim WHERE status='open'", True),
    "branches": ("SELECT * FROM branch", True),
    "bo-observations": ("SELECT ep.experiment_id, ep.dim_name, ep.value_num, m.metric_name, m.value_num AS objective "
                        "FROM experiment_param ep JOIN result r ON r.experiment_id=ep.experiment_id "
                        "JOIN measurement m ON m.result_id=r.result_id AND m.is_primary=1", False),
    "frontier": ("SELECT * FROM frontier_entry ORDER BY rank", True),
    "intake": ("SELECT * FROM intake_asset", True),
}


@state.command("query")
@click.argument("view")
@click.option("--quest-id", default=None)
@click.pass_context
def state_query(ctx, view, quest_id):
    if view not in _VIEWS:
        emit(envelope("state query", ok=False, diagnostics=[f"unknown view {view}; have {sorted(_VIEWS)}"]))
        sys.exit(1)
    sql, has_quest = _VIEWS[view]
    conn = _conn(ctx)
    if quest_id and has_quest:
        sql += (" AND " if " WHERE " in sql else " WHERE ") + "quest_id=?"
        data = db.rows(conn, sql, (quest_id,))
    else:
        data = db.rows(conn, sql)
    conn.close()
    emit(envelope("state query", quest_id=quest_id, data={"view": view, "rows": data}))


@state.command("export")
@click.option("--quest-id", required=True)
@click.pass_context
def state_export(ctx, quest_id):
    conn = _conn(ctx)
    q = db.rows(conn, "SELECT * FROM quest WHERE quest_id=?", (quest_id,))
    branches = db.rows(conn, "SELECT branch_id,status FROM branch WHERE quest_id=?", (quest_id,))
    wk = db.rows(conn, "SELECT wakeup_id,status,next_stage FROM self_wakeup WHERE quest_id=? AND status IN ('armed','delivered')", (quest_id,))
    conn.close()
    md = f"# Quest {quest_id}\n\n```json\n{json.dumps(q, indent=2)}\n```\n\nBranches: {branches}\nOpen wakeups: {wk}\n"
    emit(envelope("state export", quest_id=quest_id, data={"markdown": md}))


# ───────────────── plan (DB-rendered living research map) ─────────────────
@cli.group()
def plan(): ...


def _render_plan_md(conn, quest_id):
    """Build the plan.md projection PURELY from DB rows (DB stays canonical; plan.md is a derived view)."""
    q = conn.execute("SELECT * FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    if q is None:
        return None
    q = dict(q)
    branches = db.rows(conn, "SELECT branch_id,parent_branch_id,status,git_branch FROM branch WHERE quest_id=? ORDER BY created_at", (quest_id,))
    ideas = db.rows(conn, "SELECT idea_id,parent_idea_id,status,round_index,statement FROM idea WHERE quest_id=? ORDER BY round_index", (quest_id,))
    frontier = db.rows(conn, "SELECT entry_id,candidate_ref,rank,score,status FROM frontier_entry WHERE quest_id=? ORDER BY rank", (quest_id,))
    decisions = db.rows(conn, "SELECT decision_id,route,to_stage,requires_user_confirm,confirmed,round_index FROM decision WHERE quest_id=? ORDER BY created_at", (quest_id,))
    finals = db.rows(conn, "SELECT outcome,reopen_conditions,next_incumbent_ref,created_at FROM finalize_outcome WHERE quest_id=? ORDER BY created_at", (quest_id,))
    rounds = db.rows(conn, "SELECT round_index,stage,status,summary_ref,updated_at FROM round WHERE quest_id=? ORDER BY round_index", (quest_id,))
    artifacts = db.rows(conn, "SELECT kind,ref FROM artifact WHERE quest_id=? AND kind IN ('clarification','research-contract','effort-selection') ORDER BY kind", (quest_id,))
    def _safe(sql):  # tables that may be absent on an un-reinited DB
        try:
            return db.rows(conn, sql, (quest_id,))
        except sqlite3.OperationalError:
            return []
    findings = _safe("SELECT kind,summary FROM finding_memory WHERE quest_id=? ORDER BY created_at DESC LIMIT 8")
    opps = _safe("SELECT opportunity_id,kind,status,motivating_refs FROM research_opportunity WHERE quest_id=? "
                 "ORDER BY (status='open') DESC, created_at DESC LIMIT 10")
    unsupported = _safe("SELECT claim_id,status FROM claim WHERE quest_id=? AND kind='claim' "
                        "AND status IN ('open','refuted') ORDER BY created_at")
    L = []
    L.append(f"# Plan — {quest_id}  (plan_revision {q['plan_revision']} · stage {q.get('current_stage')} · round {q['round_index']})")
    L.append("\n> Rendered projection of DB state. The DB is canonical; this file is never read back as truth.\n")
    L.append("## Contract  [FIXED — acceptance amendable only via operator-confirmed decision; objective frozen]")
    L.append(f"- run mode (autonomy_mode): **{q.get('autonomy_mode') or '(unset)'}**  ·  rigor_level: **{q.get('rigor_level') or 'standard (default)'}**")
    L.append(f"- objective_ref: `{q['objective_ref']}`")
    L.append(f"- acceptance_ref: `{q.get('acceptance_ref')}`")
    for a in artifacts:
        L.append(f"- {a['kind']}: `{a['ref']}`")
    L.append("\n## Active node  [LIVING]")
    L.append(f"- stage=`{q.get('current_stage')}` round={q['round_index']} branch=`{q.get('active_branch_id')}` "
             f"idea=`{q.get('active_idea_id')}` best_result=`{q.get('best_result_ref')}` baseline_gate={q['baseline_gate']} run_state={q['run_state']}")
    L.append("\n## Route / frontier tree  [LIVING]")
    L.append("Branches: " + (", ".join(f"{b['branch_id']}[{b['status']}]" for b in branches) or "(none)"))
    L.append("Ideas: " + (", ".join(f"{i['idea_id']}[{i['status']}]" for i in ideas) or "(none)"))
    L.append("Frontier: " + (", ".join(f"{f['candidate_ref']}#{f['rank']}[{f['status']}]" for f in frontier) or "(none)"))
    L.append("\n## Discovery  [LIVING · advisory quest-local, not a gate]")
    L.append("Findings: " + (", ".join(f"{f['kind']}:{str(f['summary'])[:40]}" for f in findings) or "(none)"))
    L.append("Open questions / unsupported claims: "
             + (", ".join(f"{c['claim_id']}[{c['status']}]" for c in unsupported) or "(none)"))
    def _opp_label(o):
        try:
            mr = json.loads(o["motivating_refs"]) if o["motivating_refs"] else None
        except Exception:
            mr = None
        tag = "!unresolved-refs" if _resolve_quest_refs(conn, quest_id, mr if isinstance(mr, dict) else None) else ""
        return f"{o['opportunity_id']}({o['kind']}){tag}"
    L.append("Next candidates: "
             + (", ".join(_opp_label(o) for o in opps if o['status'] == 'open') or "(none)"))
    L.append("Parked / failed routes: "
             + (", ".join(f"{b['branch_id']}[{b['status']}]" for b in branches if b['status'] in ('parked', 'abandoned')) or "(none)"))
    rfw = _repeat_failure_warnings(conn, quest_id)
    if rfw:
        for e in rfw:
            L.append(f"Repeated-failure advisory ({e['source']} {e['ref']}): " + "; ".join(e["warnings"]))
    L.append("\n## Next decision options  [LIVING]")
    open_dec = [d for d in decisions if not d["confirmed"] and d["requires_user_confirm"]]
    if open_dec:
        for d in open_dec:
            L.append(f"- `{d['route']}` → {d.get('to_stage')} (awaiting operator confirm; decision {d['decision_id']})")
    else:
        L.append("- (none pending operator confirmation)")
    L.append("\n## Disposition  [LIVING]")
    if finals:
        for f in finals:
            extra = f.get("reopen_conditions") or f.get("next_incumbent_ref") or ""
            L.append(f"- {f['outcome']} {('· ' + extra) if extra else ''} @ {f['created_at']}")
    else:
        L.append("- (not finalized)")
    L.append("\n## Revisions  [APPEND-ONLY LEDGER]")
    # One projected entry per closed round (round-close bump) + per confirmed acceptance amendment.
    amends = db.rows(conn, "SELECT decision_id,round_index,created_at FROM decision WHERE quest_id=? AND route='amend-acceptance' AND confirmed=1 ORDER BY created_at", (quest_id,))
    closed = [r for r in rounds if r["status"] == "closed"]
    if not closed and not amends:
        L.append(f"- rev 1 — launch contract (plan_revision={q['plan_revision']})")
    for r in closed:
        L.append(f"- round-close r{r['round_index']} ({r['stage']}) @ {r['updated_at']} — {r.get('summary_ref') or ''}")
    for a in amends:
        L.append(f"- acceptance-amendment @ {a['created_at']} — decision {a['decision_id']} (round {a['round_index']})")
    return "\n".join(L) + "\n"


@plan.command("render")
@click.option("--quest-id", required=True)
@click.option("--at", required=True)
@click.option("--out", default=None, help="Output path (default runs/<q>/plan.md).")
@click.pass_context
def plan_render(ctx, quest_id, at, out):
    """Render runs/<q>/plan.md from DB state and index it as artifact(kind='plan'). Pure projection."""
    conn = _conn(ctx)
    md = _render_plan_md(conn, quest_id)
    if md is None:
        conn.close()
        emit(envelope("plan render", ok=False, quest_id=quest_id, diagnostics=[f"unknown quest {quest_id}"])); sys.exit(1)
    path = out or str(LOOP_DIR / "runs" / quest_id / "plan.md")
    import os as _os
    _os.makedirs(_os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(md)
    ref = path.replace(str(LOOP_DIR) + "/", "")
    try:
        records.apply(conn, {"record_type": "artifact.record", "record_id": f"{quest_id}:plan",
                             "at": at, "quest_id": quest_id, "kind": "plan", "ref": ref})
    except records.RecordError as e:
        conn.close(); emit(envelope("plan render", ok=False, quest_id=quest_id, diagnostics=[str(e)])); sys.exit(1)
    pr = conn.execute("SELECT plan_revision FROM quest WHERE quest_id=?", (quest_id,)).fetchone()[0]
    _finish(ctx, conn, "plan render", {"path": ref, "bytes": len(md)}, quest_id=quest_id)


@plan.command("status")
@click.option("--quest-id", required=True)
@click.pass_context
def plan_status(ctx, quest_id):
    """Print the rendered plan map WITHOUT writing the artifact (inspection)."""
    conn = _conn(ctx)
    md = _render_plan_md(conn, quest_id)
    pr = conn.execute("SELECT plan_revision FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    conn.close()
    if md is None:
        emit(envelope("plan status", ok=False, quest_id=quest_id, diagnostics=[f"unknown quest {quest_id}"])); sys.exit(1)
    emit(envelope("plan status", quest_id=quest_id, plan_revision=pr[0] if pr else None, data={"markdown": md}))


def _decision_lint(conn, quest_id):
    """Warn on consequential decisions that did not name their losers (read-only)."""
    warns = []
    consequential = ("branch", "reset", "stop", "finalize", "idea", "optimize")
    decs = db.rows(conn, "SELECT decision_id,route,round_index FROM decision WHERE quest_id=?", (quest_id,))
    for d in decs:
        if d["route"] not in consequential or d["round_index"] is None:
            continue
        ri = d["round_index"]
        cand = conn.execute("SELECT COUNT(*) FROM idea WHERE quest_id=? AND round_index=?", (quest_id, ri)).fetchone()[0] \
            + conn.execute("SELECT COUNT(*) FROM frontier_entry WHERE quest_id=? AND round_index=?", (quest_id, ri)).fetchone()[0]
        losers = conn.execute("SELECT COUNT(*) FROM idea WHERE quest_id=? AND round_index=? AND status IN ('rejected','exhausted')", (quest_id, ri)).fetchone()[0] \
            + conn.execute("SELECT COUNT(*) FROM frontier_entry WHERE quest_id=? AND round_index=? AND status IN ('parked','rejected')", (quest_id, ri)).fetchone()[0]
        if cand < 2:
            warns.append(f"decision {d['decision_id']} (route={d['route']}, round {ri}) chose among <2 named candidates")
        elif losers < 1:
            warns.append(f"decision {d['decision_id']} (route={d['route']}, round {ri}) has no marked rejected alternative")
    return warns


def _methodology_lint(conn, quest_id):
    """Advisory methodology-usage lint for ORCHESTRATOR-INTERNAL stages only (decision/optimize/finalize) —
    warn when such a closed round has no artifact(kind='methodology-usage') for its round_index. WORKER stages
    (idea/baseline/experiment/analysis/write/review) are NOT linted here: their methodology is bound by the
    typed-record gates + `methodology check` (task-result.methodology_used[].applied_as must resolve to the
    stage's validated typed record), which supersedes this existence check. Pre-regime quests (no
    research-contract artifact) are exempt. Read-only; never an invariant (so `state validate` is unaffected)."""
    warns = []
    try:
        regime = conn.execute("SELECT COUNT(*) FROM artifact WHERE quest_id=? AND kind='research-contract'",
                              (quest_id,)).fetchone()[0]
    except Exception:
        return warns
    if not regime:
        return warns  # pre-feature / non-regime quest: exempt
    rounds = db.rows(conn, "SELECT round_index,stage FROM round WHERE quest_id=? AND status='closed'", (quest_id,))
    for r in rounds:
        # Worker stages are bound by their typed-record gates + `methodology check`; lint only the internal stages.
        if r["stage"] not in records.ORCHESTRATOR_INTERNAL_STAGES:
            continue
        req = records.REQUIRED_PACKS.get(r["stage"])
        if not req or r["round_index"] is None:
            continue
        n = conn.execute("SELECT COUNT(*) FROM artifact WHERE quest_id=? AND round_index=? AND kind='methodology-usage'",
                         (quest_id, r["round_index"])).fetchone()[0]
        if not n:
            warns.append(f"round r{r['round_index']} ({r['stage']}) closed without a methodology-usage artifact "
                         f"(required packs: {req})")
    return warns


@plan.command("validate")
@click.option("--quest-id", required=True)
@click.pass_context
def plan_validate(ctx, quest_id):
    """Read-only: plan-map invariants (plan_map_fresh, plan_revision_monotonic) + decision lint + methodology
    lint warnings (advisory; never fail the command on a lint)."""
    conn = _conn(ctx)
    allres = inv.run_all(conn)
    plan_invs = [r for r in allres["violations"] if r["name"] in ("plan_map_fresh", "plan_revision_monotonic")]
    lint = _decision_lint(conn, quest_id)
    mlint = _methodology_lint(conn, quest_id)
    conn.close()
    ok = not plan_invs
    emit(envelope("plan validate", ok=ok, quest_id=quest_id,
                  data={"plan_invariant_violations": plan_invs, "decision_lint": lint, "methodology_lint": mlint},
                  warnings=lint + mlint, diagnostics=[] if ok else ["plan invariant violation"]))
    if not ok:
        sys.exit(1)


@plan.command("diff")
@click.option("--quest-id", required=True)
@click.pass_context
def plan_diff(ctx, quest_id):
    """List recorded acceptance revisions (acceptance.md@rev-*) and confirmed amendment decisions."""
    conn = _conn(ctx)
    amends = db.rows(conn, "SELECT decision_id,round_index,rationale_ref,created_at FROM decision WHERE quest_id=? AND route='amend-acceptance' AND confirmed=1 ORDER BY created_at", (quest_id,))
    cur = conn.execute("SELECT acceptance_ref FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    conn.close()
    import glob as _glob
    revs = sorted(_glob.glob(str(LOOP_DIR / "runs" / quest_id / "objective" / "acceptance.md@rev-*")))
    emit(envelope("plan diff", quest_id=quest_id,
                  data={"current_acceptance_ref": cur[0] if cur else None,
                        "acceptance_revisions": [r.replace(str(LOOP_DIR) + "/", "") for r in revs],
                        "amendments": amends}))


# ───────────────── completeness (research-completeness audit) ─────────────────
@cli.group()
def completeness(): ...


@completeness.command("audit")
@click.option("--quest-id", required=True)
@click.pass_context
def completeness_audit_cmd(ctx, quest_id):
    """Run the seven research-completeness checks. Advisory by default; the finalize gate enforces
    them only in auto mode at the gating rigor (DEEPRESEARCH_COMPLETENESS_GATE_RIGOR, default 'publication')."""
    conn = _conn(ctx)
    row = conn.execute("SELECT autonomy_mode, rigor_level FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    rigor = (row[1] if row else None) or "standard"
    audit = records.completeness_audit(conn, quest_id, rigor)
    conn.close()
    audit["autonomy_mode"] = row[0] if row else None
    emit(envelope("completeness audit", ok=audit["ok"], quest_id=quest_id, data=audit,
                  diagnostics=audit["reasons"]))


# ───────────────── record ─────────────────
@cli.group()
def record(): ...


@record.command("apply")
@click.option("--json", "json_opt", default=None)
@click.option("--file", "file_opt", default=None)
@click.pass_context
def record_apply(ctx, json_opt, file_opt):
    _apply(ctx, "record apply", _payload(json_opt, file_opt))


@record.command("validate")
@click.option("--json", "json_opt", default=None)
@click.option("--file", "file_opt", default=None)
def record_validate(json_opt, file_opt):
    try:
        records.validate(_payload(json_opt, file_opt))
        emit(envelope("record validate", data={"valid": True}))
    except records.RecordError as e:
        emit(envelope("record validate", ok=False, diagnostics=[str(e)]))
        sys.exit(1)


# ───────────────── handoff ─────────────────
@cli.group()
def handoff(): ...


@handoff.command("open")
@click.option("--quest-id", required=True)
@click.option("--handoff-id", required=True)
@click.option("--schema-id", required=True)
@click.option("--round-index", type=int, default=None)
@click.option("--from-role", default=None)
@click.option("--to-role", default=None)
@click.option("--max-attempts", type=int, default=None)
@click.option("--receipt-due-at", default=None)
@click.option("--result-due-at", default=None)
@click.option("--bump-attempt", is_flag=True)
@click.option("--at", required=True)
@click.pass_context
def handoff_open(ctx, quest_id, handoff_id, schema_id, round_index, from_role, to_role,
                 max_attempts, receipt_due_at, result_due_at, bump_attempt, at):
    p = {"record_type": "handoff.open", "record_id": f"{quest_id}:{handoff_id}", "at": at,
         "quest_id": quest_id, "handoff_id": handoff_id, "schema_id": schema_id}
    for k, v in dict(round_index=round_index, from_role=from_role, to_role=to_role,
                     max_attempts=max_attempts, receipt_due_at=receipt_due_at,
                     result_due_at=result_due_at).items():
        if v is not None:
            p[k] = v
    if bump_attempt:
        p["bump_attempt"] = True
    _apply(ctx, "handoff open", p, quest_id=quest_id)


@handoff.command("advance")
@click.option("--quest-id", required=True)
@click.option("--handoff-id", required=True)
@click.option("--status", required=True)
@click.option("--bump-attempt", is_flag=True)
@click.option("--at", required=True)
@click.pass_context
def handoff_advance(ctx, quest_id, handoff_id, status, bump_attempt, at):
    p = {"record_type": "handoff.advance", "record_id": f"{quest_id}:{handoff_id}", "at": at, "status": status}
    if bump_attempt:
        p["bump_attempt"] = True
    _apply(ctx, "handoff advance", p, quest_id=quest_id)


@handoff.command("query")
@click.option("--quest-id", default=None)
@click.option("--due", is_flag=True)
@click.option("--seen", default=None)
@click.option("--stalled", is_flag=True, help="In-flight handoffs (sent|acked) past their due time with attempts left.")
@click.option("--now", default=None, help="Caller-supplied ISO-8601 'now' (required with --stalled).")
@click.pass_context
def handoff_query(ctx, quest_id, due, seen, stalled, now):
    conn = _conn(ctx)
    if seen:
        # Dedup lookup: handoff PK is (quest_id, handoff_id). When --quest-id is omitted, scope to the single
        # running quest (single_active_quest) so the dedup actually matches instead of binding quest_id=NULL.
        if quest_id is None:
            r = conn.execute("SELECT quest_id FROM quest WHERE run_state='running' ORDER BY quest_id LIMIT 1").fetchone()
            quest_id = r[0] if r else None
        row = conn.execute("SELECT status FROM handoff WHERE quest_id=? AND handoff_id=?", (quest_id, seen)).fetchone()
        data = {"handoff_id": seen, "processed": bool(row) and row[0] == "processed", "status": row[0] if row else None}
    elif stalled:
        if not now:
            conn.close(); emit(envelope("handoff query", ok=False, diagnostics=["--stalled requires --now <iso8601>"], quest_id=quest_id)); sys.exit(1)
        # in-flight (sent|acked), attempts remaining, and past a due time → candidates for retry/fail
        sql = ("SELECT *, (attempt_count >= max_attempts) AS at_max FROM handoff "
               "WHERE status IN ('sent','acked') "
               "AND ((result_due_at IS NOT NULL AND result_due_at < ?) OR (receipt_due_at IS NOT NULL AND receipt_due_at < ?))")
        params = [now, now]
        if quest_id:
            sql += " AND quest_id=?"; params.append(quest_id)
        rows = db.rows(conn, sql, tuple(params))
        for r in rows:
            r["action"] = "fail+decision" if r.get("at_max") else "resend (reuse handoff_id, bump_attempt)"
        data = {"now": now, "stalled": rows, "count": len(rows)}
    else:
        sql = "SELECT * FROM handoff"
        cond, params = [], []
        if due:
            cond.append("status NOT IN ('processed','failed')")
        if quest_id:
            cond.append("quest_id=?"); params.append(quest_id)
        if cond:
            sql += " WHERE " + " AND ".join(cond)
        data = {"rows": db.rows(conn, sql, tuple(params))}
    conn.close()
    emit(envelope("handoff query", quest_id=quest_id, data=data))


# ───────────────── wakeup ─────────────────
@cli.group()
def wakeup(): ...


@wakeup.command("arm")
@click.option("--wakeup-id", required=True)
@click.option("--quest-id", required=True)
@click.option("--handoff-id", required=True)
@click.option("--reason", required=True)
@click.option("--lane", default="main")
@click.option("--next-stage", default=None)
@click.option("--next-action", default=None)
@click.option("--deliver-after", default=None)
@click.option("--at", required=True)
@click.pass_context
def wakeup_arm(ctx, wakeup_id, quest_id, handoff_id, reason, lane, next_stage, next_action, deliver_after, at):
    p = {"record_type": "wakeup.arm", "record_id": wakeup_id, "at": at, "quest_id": quest_id,
         "handoff_id": handoff_id, "reason": reason, "continuation_lane": lane}
    for k, v in dict(next_stage=next_stage, next_action=next_action, deliver_after=deliver_after).items():
        if v is not None:
            p[k] = v
    _apply(ctx, "wakeup arm", p, quest_id=quest_id)


@wakeup.command("attach")
@click.option("--wakeup-id", required=True)
@click.option("--message-ref", required=True)
@click.option("--at", required=True)
@click.pass_context
def wakeup_attach(ctx, wakeup_id, message_ref, at):
    _apply(ctx, "wakeup attach", {"record_type": "wakeup.attach", "record_id": wakeup_id, "at": at, "message_ref": message_ref})


@wakeup.command("resolve")
@click.option("--wakeup-id", required=True)
@click.option("--status", required=True)
@click.option("--at", required=True)
@click.pass_context
def wakeup_resolve(ctx, wakeup_id, status, at):
    _apply(ctx, "wakeup resolve", {"record_type": "wakeup.resolve", "record_id": wakeup_id, "at": at, "status": status})


@wakeup.command("list")
@click.option("--quest-id", default=None)
@click.pass_context
def wakeup_list(ctx, quest_id):
    conn = _conn(ctx)
    sql = "SELECT * FROM self_wakeup WHERE status IN ('armed','delivered')"
    params = ()
    if quest_id:
        sql += " AND quest_id=?"; params = (quest_id,)
    data = db.rows(conn, sql, params)
    conn.close()
    emit(envelope("wakeup list", quest_id=quest_id, data={"rows": data}))


# ───────────────── email ─────────────────
@cli.group()
def email(): ...


@email.command("schema")
@click.option("--schema-id", required=True)
def email_schema(schema_id):
    try:
        fam = mail.resolve(schema_id)
        emit(envelope("email schema", data={"schema": f"schemas/{fam['name']}.schema.json",
                                             "renderer": f"renderers/{fam['name']}.md.j2", "family": fam["name"]}))
    except KeyError as e:
        emit(envelope("email schema", ok=False, diagnostics=[str(e)])); sys.exit(1)


@email.command("validate")
@click.option("--json", "json_opt", default=None)
@click.option("--file", "file_opt", default=None)
def email_validate(json_opt, file_opt):
    try:
        mail.validate(_payload(json_opt, file_opt))
        emit(envelope("email validate", data={"valid": True}))
    except Exception as e:
        emit(envelope("email validate", ok=False, diagnostics=[str(e)])); sys.exit(1)


@email.command("render")
@click.option("--json", "json_opt", default=None)
@click.option("--file", "file_opt", default=None)
def email_render(json_opt, file_opt):
    try:
        p = _payload(json_opt, file_opt)
        mail.validate(p)
        body = mail.render(p)
        emit(envelope("email render", data={"body": body}))
    except Exception as e:
        emit(envelope("email render", ok=False, diagnostics=[str(e)])); sys.exit(1)


@email.command("apply")
@click.option("--payload-id", required=True)
@click.option("--quest-id", required=True)
@click.option("--schema-id", required=True)
@click.option("--direction", required=True, type=click.Choice(["out", "in"]))
@click.option("--handoff-id", default=None)
@click.option("--round-index", type=int, default=None)
@click.option("--sender", default=None)
@click.option("--recipient", default=None)
@click.option("--message-ref", default=None)
@click.option("--status", default="sent")
@click.option("--at", required=True)
@click.pass_context
def email_apply(ctx, payload_id, quest_id, schema_id, direction, handoff_id, round_index,
                sender, recipient, message_ref, status, at):
    conn = _conn(ctx)
    conn.execute(
        "INSERT OR IGNORE INTO mail_log(payload_id,quest_id,handoff_id,round_index,schema_id,"
        "direction,sender,recipient,message_ref,status,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
        (payload_id, quest_id, handoff_id, round_index, schema_id, direction, sender, recipient,
         message_ref, status, at))
    conn.commit()
    _finish(ctx, conn, "email apply", {"payload_id": payload_id, "logged": True}, quest_id=quest_id)


@email.command("query")
@click.option("--quest-id", required=True)
@click.pass_context
def email_query(ctx, quest_id):
    conn = _conn(ctx)
    data = db.rows(conn, "SELECT * FROM mail_log WHERE quest_id=?", (quest_id,))
    conn.close()
    emit(envelope("email query", quest_id=quest_id, data={"rows": data}))


# ───────────────── findings ─────────────────
@cli.group()
def findings(): ...


@findings.command("add")
@click.option("--memory-id", required=True)
@click.option("--kind", required=True)
@click.option("--summary", required=True)
@click.option("--scope", default="quest")
@click.option("--quest-id", required=True)  # findings are always quest-owned (total isolation)
@click.option("--artifact-ref", default=None)
@click.option("--grounded-by", default=None)
@click.option("--at", required=True)
@click.pass_context
def findings_add(ctx, memory_id, kind, summary, scope, quest_id, artifact_ref, grounded_by, at):
    p = {"record_type": "finding.add", "record_id": memory_id, "at": at, "scope": scope,
         "kind": kind, "summary": summary}
    for k, v in dict(quest_id=quest_id, artifact_ref=artifact_ref, grounded_by=grounded_by).items():
        if v is not None:
            p[k] = v
    _apply(ctx, "findings add", p, quest_id=quest_id)


@findings.command("query")
@click.option("--quest-id", default=None)
@click.option("--scope", default=None)
@click.option("--kind", default=None)
@click.option("--all-quests", is_flag=True, default=False,
              help="Operator-only cross-quest view. Agents MUST NOT use this — quests are fully isolated.")
@click.pass_context
def findings_query(ctx, quest_id, scope, kind, all_quests):
    conn = _conn(ctx)
    # QUEST ISOLATION: never surface another quest's findings to the loop. When no quest is named and
    # --all-quests is not set, scope to the single running quest (single_active_quest); an explicit
    # --quest-id or --all-quests is required for any cross-quest view (operator repair only).
    if quest_id is None and not all_quests:
        r = conn.execute("SELECT quest_id FROM quest WHERE run_state='running' ORDER BY quest_id LIMIT 1").fetchone()
        if not r:
            conn.close(); emit(envelope("findings query", quest_id=None, data={"rows": []})); return
        quest_id = r[0]
    cond, params = [], []
    for col, val in (("quest_id", quest_id), ("scope", scope), ("kind", kind)):
        if val:
            cond.append(f"{col}=?"); params.append(val)
    sql = "SELECT * FROM finding_memory" + (" WHERE " + " AND ".join(cond) if cond else "")
    data = db.rows(conn, sql, tuple(params)); conn.close()
    emit(envelope("findings query", quest_id=quest_id, data={"rows": data}))


@findings.command("update")
@click.option("--quest-id", required=True)  # findings are always quest-owned (total isolation)
@click.option("--slug", required=True, help="short stable slug; memory_id = <quest>:find:<slug> (idempotent upsert).")
@click.option("--kind", required=True,
              type=click.Choice(["idea", "decision", "knowledge", "lesson", "reference"]),
              help="lesson = failed attempt / refuted alternative; knowledge = frontier / evidence gap / bridge.")
@click.option("--summary", required=True)
@click.option("--artifact-ref", default=None)
@click.option("--grounded-by", default=None, help="quest-local result/measurement id this finding is grounded in.")
@click.option("--links", "links", default=None,
              help="OPTIONAL quest-local lineage JSON (idea_select_id, idea_ids[], experiment_id, result_ids[], "
                   "claim_ids[], analysis_bridge_id, opportunity_ids[]). All ids must belong to THIS quest.")
@click.option("--at", required=True)
@click.pass_context
def findings_update(ctx, quest_id, slug, kind, summary, artifact_ref, grounded_by, links, at):
    """Add/update a QUEST-LOCAL Findings-Memory entry (convenience over `finding.add` that mints a stable
    memory_id from --slug). Use across the loop to durably record selected/rejected ideas, novelty grounding,
    scope constraints, baseline/experiment results, FAILED attempts + refuted alternatives (kind=lesson),
    analysis bridges, limitations, research opportunities, evidence gaps, review feedback, and the current
    frontier. STRICTLY quest-local (scope='quest'); no cross-quest/global memory."""
    p = {"record_type": "finding.add", "record_id": f"{quest_id}:find:{slug}", "at": at, "scope": "quest",
         "kind": kind, "summary": summary, "quest_id": quest_id}
    for k, v in dict(artifact_ref=artifact_ref, grounded_by=grounded_by).items():
        if v is not None:
            p[k] = v
    if links is not None:
        lk = _loads(links)
        if lk is not None:
            p["links"] = lk
    _apply(ctx, "findings update", p, quest_id=quest_id)


@findings.command("summarize")
@click.option("--quest-id", required=True)
@click.pass_context
def findings_summarize(ctx, quest_id):
    """Read-only QUEST-LOCAL Findings-Memory DIGEST for the BO-reviewer's exploit/explore context: findings by
    kind, the failed-attempt/refuted LESSONS (so BO can avoid repeating them + penalize unresolved repeats),
    the current frontier (open opportunities, refuted/unsupported claims, parked routes, negative-findings
    count, repeated-failure warnings) and evidence gaps. Strictly this quest's rows — no cross-quest recall."""
    conn = _conn(ctx)
    rows = []
    try:
        rows = [dict(memory_id=r["memory_id"], kind=r["kind"], summary=r["summary"],
                     grounded_by=r["grounded_by"], artifact_ref=r["artifact_ref"])
                for r in conn.execute("SELECT memory_id, kind, summary, grounded_by, artifact_ref FROM "
                                      "finding_memory WHERE quest_id=? AND scope='quest' ORDER BY created_at, "
                                      "memory_id", (quest_id,))]
    except sqlite3.OperationalError:
        rows = []
    by_kind = {}
    for r in rows:
        by_kind.setdefault(r["kind"], []).append(r)
    disc = _discovery(conn, quest_id)
    # current selected idea (the bound BO winner, if any) for frontier context
    try:
        sel_idea = conn.execute("SELECT idea_id, statement FROM idea WHERE quest_id=? AND status='selected' "
                                "ORDER BY idea_id LIMIT 1", (quest_id,)).fetchone()
        selected_idea = {"idea_id": sel_idea["idea_id"], "statement": sel_idea["statement"]} if sel_idea else None
    except sqlite3.OperationalError:
        selected_idea = None
    conn.close()
    frontier = {"selected_idea": selected_idea,
                "open_opportunities": disc.get("open_opportunities", []),
                "recommended_next_actions": disc.get("recommended_next_actions", []),
                "refuted_claims": disc.get("refuted_claims", []),
                "unsupported_claims": disc.get("unsupported_claims", []),
                "parked_routes": disc.get("parked_routes", []),
                "negative_findings": disc.get("negative_findings", 0),
                "repeated_failure_warnings": disc.get("repeated_failure_warnings", [])}
    evidence_gaps = {"unsupported_claims": disc.get("unsupported_claims", []),
                     "opportunities_with_unresolved_refs": disc.get("opportunities_with_unresolved_refs", [])}
    emit(envelope("findings summarize", quest_id=quest_id,
                  data={"counts": {k: len(v) for k, v in by_kind.items()}, "total": len(rows),
                        "lessons": by_kind.get("lesson", []), "findings_by_kind": by_kind,
                        "frontier": frontier, "evidence_gaps": evidence_gaps}))


# ───────────────── claim / evidence ─────────────────
@cli.group()
def claim(): ...


@claim.command("upsert")
@click.option("--claim-id", required=True)
@click.option("--quest-id", required=True)
@click.option("--statement", required=True)
@click.option("--status", default="open")
@click.option("--at", required=True)
@click.pass_context
def claim_upsert(ctx, claim_id, quest_id, statement, status, at):
    _apply(ctx, "claim upsert", {"record_type": "claim.upsert", "record_id": claim_id, "at": at,
                                 "quest_id": quest_id, "statement": statement, "status": status}, quest_id=quest_id)


@claim.command("link")
@click.option("--claim-id", required=True)
@click.option("--source-kind", required=True)
@click.option("--source-ref", required=True)
@click.option("--relation", default="supports")
@click.option("--at", required=True)
@click.pass_context
def claim_link(ctx, claim_id, source_kind, source_ref, relation, at):
    p = {"record_type": "claim_evidence.link", "record_id": f"{claim_id}:{source_kind}:{source_ref}",
         "at": at, "claim_id": claim_id, "source_kind": source_kind, "source_ref": source_ref, "relation": relation}
    _apply(ctx, "claim link", p)


@claim.command("resolve")
@click.option("--claim-id", required=True)
@click.option("--source-kind", required=True)
@click.option("--source-ref", required=True)
@click.option("--resolution-ref", required=True)
@click.option("--at", required=True)
@click.pass_context
def claim_resolve(ctx, claim_id, source_kind, source_ref, resolution_ref, at):
    p = {"record_type": "claim_evidence.resolve", "record_id": f"{claim_id}:{source_kind}:{source_ref}",
         "at": at, "claim_id": claim_id, "source_kind": source_kind, "source_ref": source_ref,
         "resolution_ref": resolution_ref}
    _apply(ctx, "claim resolve", p)


@cli.group()
def evidence(): ...


@evidence.command("validate")
@click.option("--quest-id", default=None)
@click.pass_context
def evidence_validate(ctx, quest_id):
    conn = _conn(ctx)
    qf = " AND c.quest_id=?" if quest_id else ""
    p = (quest_id,) if quest_id else ()
    unsupported = conn.execute(
        "SELECT COUNT(*) FROM claim c WHERE c.status='supported' AND NOT EXISTS "
        "(SELECT 1 FROM claim_evidence e WHERE e.claim_id=c.claim_id AND e.relation='supports')" + qf, p).fetchone()[0]
    open_contra = conn.execute(
        "SELECT COUNT(*) FROM claim c WHERE c.status='supported' AND EXISTS "
        "(SELECT 1 FROM claim_evidence e WHERE e.claim_id=c.claim_id AND e.relation='contradicts' AND e.resolved=0)" + qf, p).fetchone()[0]
    orphan = conn.execute(
        "SELECT COUNT(*) FROM claim c WHERE NOT EXISTS "
        "(SELECT 1 FROM claim_evidence e WHERE e.claim_id=c.claim_id)" + qf, p).fetchone()[0]
    conn.close()
    ok = unsupported == 0 and open_contra == 0
    emit(envelope("evidence validate", ok=ok, quest_id=quest_id,
                  data={"supported_without_support": unsupported, "supported_with_open_contradiction": open_contra,
                        "orphan_claims": orphan},
                  warnings=([f"{orphan} orphan claim(s)"] if orphan else [])))


# ───────────────── bo (DeepScientist-inspired idea-level BO: LLM-reviewer surrogate + UCB-like acquisition) ─────
# HONEST FRAMING: this is NOT full statistical Bayesian optimization (no probabilistic surrogate / posterior).
# A configurable independent LLM Reviewer (default backend=codex, effort=max; agents/bo-reviewer.toml) scores
# each candidate research move into a structured valuation vector; a deterministic, documented UCB-like rule
# selects the next candidate. Everything is QUEST-LOCAL and ADVISORY (never a gate; never alters
# idea_select.valid; never enters blocking_gates / finalize_readiness). The search_space midpoint remains only
# a labelled FALLBACK when no idea-level candidate exists.
# DEFAULT acquisition is the OFFICIAL DeepScientist-style score: w_u*utility + w_q*quality + kappa*exploration_value
# (defaults 1/1/1 => utility+quality+exploration_value). The richer Houmao formula (exploitation/exploration/
# penalty with beta) stays selectable as 'ucb_like_v1'. Both are LLM-reviewer surrogate + UCB-like acquisition,
# NOT full statistical BO.
_REVIEWER_DEFAULTS = {"backend": "codex", "model": "default", "effort": "max", "temperature": "",
                      "max_candidates": 8, "required_before_select": False,
                      "acquisition_method": "ucb_official_v1", "beta": 0.5,
                      "w_u": 1.0, "w_q": 1.0, "kappa": 1.0}
_VALUATION_KEYS = ("utility", "quality", "novelty", "exploration_value", "uncertainty", "feasibility", "cost", "risk")


def _loads(s):
    try:
        return json.loads(s) if s else None
    except Exception:
        return None


def _reviewer_config(overrides=None):
    """Resolve reviewer + acquisition config with explicit precedence + provenance:

        built-in defaults
          < agents/bo-reviewer.toml          (DURABLE product default — codex / max; never overwritten here)
          < agents/bo-reviewer.local.toml [reviewer_override]   (machine-LOCAL, gitignored; not the product)
          < DEEPRESEARCH_BO_REVIEWER_{BACKEND,EFFORT,CREDENTIAL} env   (ephemeral)
          < CLI --backend / --effort                            (highest)

    `backend_source` records which layer set the EFFECTIVE backend (built_in | product_default |
    local_override_file | env_override | cli_override); `product_default_backend`/`product_default_effort`
    always expose the durable default so callers can report both. NO SECRETS — `credential`/
    `credential_override` name a credential-store bundle, never a secret."""
    import os as _os
    cfg = dict(_REVIEWER_DEFAULTS)
    cfg["config_source"] = "built-in defaults"
    cfg["backend_source"] = "built_in"
    try:
        import tomllib
        from paths import BO_REVIEWER_TOML
        if BO_REVIEWER_TOML.exists():
            doc = tomllib.load(open(BO_REVIEWER_TOML, "rb"))
            rv = doc.get("reviewer", {}) or {}
            for k in ("backend", "model", "effort", "temperature", "max_candidates", "required_before_select"):
                if k in rv and rv[k] != "":
                    cfg[k] = rv[k]
            aq = doc.get("acquisition", {}) or {}
            if aq.get("method"):
                cfg["acquisition_method"] = aq["method"]
            if aq.get("beta") is not None:
                cfg["beta"] = aq["beta"]
            for wk in ("w_u", "w_q", "kappa"):
                if aq.get(wk) is not None:
                    cfg[wk] = aq[wk]
            cfg["config_source"] = str(BO_REVIEWER_TOML)
            cfg["backend_source"] = "product_default"
    except Exception as e:
        cfg["config_warning"] = f"could not read bo-reviewer.toml ({e}); using built-in defaults"
    # The DURABLE product default is whatever bo-reviewer.toml declared (codex / max) — captured BEFORE any
    # local/ephemeral override, so it is always reportable even when the effective backend is overridden.
    cfg["product_default_backend"] = cfg["backend"]
    cfg["product_default_effort"] = cfg["effort"]
    cfg["credential_override"] = None
    # LOCAL override file (machine-local, gitignored) — a temporary per-machine override that does NOT change
    # the product default. Use when the default backend's credential is unavailable on this machine.
    try:
        import tomllib
        from paths import BO_REVIEWER_LOCAL_TOML
        if BO_REVIEWER_LOCAL_TOML.exists():
            ov = (tomllib.load(open(BO_REVIEWER_LOCAL_TOML, "rb")).get("reviewer_override", {}) or {})
            if ov.get("backend_override"):
                cfg["backend"] = ov["backend_override"]; cfg["backend_source"] = "local_override_file"
            if ov.get("effort_override"):
                cfg["effort"] = ov["effort_override"]
            if ov.get("model_override"):
                cfg["model"] = ov["model_override"]
            if ov.get("credential_override"):
                cfg["credential_override"] = ov["credential_override"]
            cfg["local_override_source"] = str(BO_REVIEWER_LOCAL_TOML)
    except Exception as e:
        cfg["local_override_warning"] = f"could not read bo-reviewer.local.toml ({e})"
    # Ephemeral env override.
    eb = _os.environ.get("DEEPRESEARCH_BO_REVIEWER_BACKEND")
    ee = _os.environ.get("DEEPRESEARCH_BO_REVIEWER_EFFORT")
    ec = _os.environ.get("DEEPRESEARCH_BO_REVIEWER_CREDENTIAL")
    if eb:
        cfg["backend"] = eb; cfg["backend_source"] = "env_override"
    if ee:
        cfg["effort"] = ee
    if ec:
        cfg["credential_override"] = ec
    # CLI overrides (highest precedence).
    for k, v in (overrides or {}).items():
        if v is not None:
            cfg[k] = v
            if k in ("backend", "effort"):
                cfg["backend_source"] = "cli_override"
    return cfg


_EXPERIMENT_OPP_KINDS = {"next_experiment", "ablation", "robustness", "boundary", "baseline_repair",
                         "failure_followup"}


def _next_move_gate_eligibility(conn, quest_id):
    """Hard-gate eligibility for the LATER next-move candidates — mirrors the gate-status predicates so BO can
    only choose a move the hard gates already permit (BO never bypasses a quality gate). Returns
    {move: (eligible_bool, reason)} for write / finalize / experiment / stop. QUEST-LOCAL."""
    qr = conn.execute("SELECT rigor_level, baseline_gate FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    rigor = (qr["rigor_level"] if qr else None) or "standard"
    floors = _gate_floors(rigor)
    # finalize readiness -> may finalize: manuscript submission-ready AND a validated, accepted review verdict.
    sp = conn.execute("SELECT submission_ready FROM paper_spine WHERE quest_id=?", (quest_id,)).fetchone()
    rv = _latest_verdict_row(conn, quest_id)
    review_ok = bool(rv is not None and rv["valid"] and rv["verdict"] == "accept")
    finalize_ok = bool(sp is not None and sp["submission_ready"] and review_ok)
    finalize_reason = ("manuscript submission-ready + validated accepted review verdict" if finalize_ok else
                       "finalize gates unmet (manuscript coverage and/or review verdict)")
    # evidence sufficiency -> may write/outline: campaign coverage ok AND a validator-confirmed analysis bridge.
    # 'write' is a move TOWARD the paper, so it is NOT an eligible next move once the quest is already
    # finalize-ready (then 'finalize' is the move), keeping the all-satisfied state to a single eligible move.
    try:
        cov_ok, cov_reasons, _ = _claim_coverage(conn, quest_id, floors)
    except Exception:
        cov_ok, cov_reasons = False, ["coverage uncomputable"]
    br = _latest_bridge_row(conn, quest_id)
    bridge_ok = bool(br is not None and br["valid"])
    write_ok = bool(cov_ok and bridge_ok and not finalize_ok)
    write_reason = ("evidence sufficient (campaign coverage + validated analysis bridge); write/outline the paper"
                    if write_ok else ("already finalize-ready (finalize, don't keep writing)" if finalize_ok else
                                      "evidence not yet sufficient: " + ("; ".join(cov_reasons) if not cov_ok else
                                                                         "analysis bridge not validator-confirmed")))
    # another experiment -> baseline/provenance constraints valid (validated contract, or baseline not yet required).
    bc = conn.execute("SELECT valid FROM baseline_contract WHERE quest_id=? ORDER BY created_at DESC, "
                      "contract_id DESC LIMIT 1", (quest_id,)).fetchone()
    bgate = (qr["baseline_gate"] if qr else None)
    experiment_ok = bool((bc is not None and bc["valid"]) or bgate in (None, "pending") or bgate == "waived")
    experiment_reason = ("baseline/provenance constraints valid" if experiment_ok else
                         "baseline.contract not validator-confirmed")
    # stop -> repeated-failure dominance, or unsupported claims with no sufficient-evidence path.
    rfw = _repeat_failure_warnings(conn, quest_id)
    try:
        unsupported = conn.execute("SELECT COUNT(*) FROM claim WHERE quest_id=? AND kind='claim' AND "
                                   "status='open'", (quest_id,)).fetchone()[0]
    except sqlite3.OperationalError:
        unsupported = 0
    stop_ok = bool(rfw) or bool(unsupported and not write_ok)
    stop_reason = ("repeated failures dominate" if rfw else
                   ("claims unsupported and evidence insufficient" if stop_ok else "claim still has a viable path"))
    return {"write": (write_ok, write_reason), "finalize": (finalize_ok, finalize_reason),
            "experiment": (experiment_ok, experiment_reason), "stop": (stop_ok, stop_reason)}


def _next_move_candidates(conn, quest_id):
    """Enumerate the LATER next-move candidate slate from quest-local state (post-experiment/analysis): open
    research_opportunity rows + synthetic write / finalize / stop moves derived from the hard gates. Each carries
    route_target + hard-gate ELIGIBILITY (+reason) + provenance. QUEST-LOCAL; the acquisition only scores
    ELIGIBLE candidates, so BO can never pick a gate-invalid move. Returns the full list (eligible + ineligible)
    for transparency."""
    rfw = {w["ref"]: w["warnings"] for w in _repeat_failure_warnings(conn, quest_id)}
    elig = _next_move_gate_eligibility(conn, quest_id)
    cands = []
    try:
        opps = conn.execute("SELECT opportunity_id, kind, rationale, motivating_refs, attempt_signature, status "
                            "FROM research_opportunity WHERE quest_id=? AND status='open' "
                            "ORDER BY created_at, opportunity_id", (quest_id,)).fetchall()
    except sqlite3.OperationalError:
        opps = []
    for o in opps:
        mr = _loads(o["motivating_refs"])
        un = _resolve_quest_refs(conn, quest_id, mr if isinstance(mr, dict) else None)
        is_exp = o["kind"] in _EXPERIMENT_OPP_KINDS
        route = "experiment" if is_exp else "analysis"
        grounded = not un
        gate_ok = (elig["experiment"][0] if is_exp else True)
        eligible = bool(grounded and gate_ok)
        if not grounded:
            reason = "ungrounded: unresolved/cross-quest motivating refs (not followed)"
        elif not gate_ok:
            reason = "experiment move blocked: " + elig["experiment"][1]
        else:
            reason = "grounded quest-local opportunity"
        cands.append({"candidate_ref": o["opportunity_id"], "candidate_kind": "opportunity:" + o["kind"],
                      "source": "opportunity", "route_target": route, "eligible": eligible,
                      "eligibility_reason": reason, "rationale": o["rationale"], "motivating_refs": mr,
                      "attempt_signature": _loads(o["attempt_signature"]), "status": o["status"],
                      "unresolved_refs": un, "repeat_failure_warnings": rfw.get(o["opportunity_id"], [])})
    for key, kind, route in (("write", "write", "outline"), ("finalize", "finalize", "finalize"),
                             ("stop", "stop", "decision")):
        e_ok, e_reason = elig[key]
        cands.append({"candidate_ref": f"{quest_id}:move:{key}", "candidate_kind": kind, "source": "frontier-move",
                      "route_target": route, "eligible": bool(e_ok), "eligibility_reason": e_reason,
                      "rationale": f"{kind} the quest ({e_reason})", "motivating_refs": None,
                      "attempt_signature": None, "status": "candidate", "unresolved_refs": [],
                      "repeat_failure_warnings": []})
    return cands


def _derive_next_move_kind(selected_ref, cands):
    """Map a selected next-move candidate to its bo_decision decision_kind."""
    c = next((x for x in cands if x["candidate_ref"] == selected_ref), None)
    if c is None:
        return "next-move-selection"
    k = c.get("candidate_kind") or ""
    if k in ("write", "finalize", "stop"):
        return "stop-write-finalize-selection"
    if k.startswith("opportunity:"):
        return "experiment-selection" if c.get("route_target") == "experiment" else "opportunity-selection"
    return "next-move-selection"


def _bo_candidates(conn, quest_id, limit=None, mode="all"):
    """Gather QUEST-LOCAL candidate research moves for reviewer evaluation. mode='all' (default): open
    research_opportunity rows; enumerable idea rows (or the latest idea_select, legacy); frontier_entry; and a
    search_space midpoint only as a labelled FALLBACK. mode='next-move': the LATER next-move slate
    (`_next_move_candidates`), filtered to hard-gate-ELIGIBLE moves only (BO never scores a gate-invalid move).
    Each candidate carries a durable ref, kind, rationale, motivating_refs, attempt_signature, status,
    unresolved_refs (cross-quest/missing — flagged, NEVER followed as memory) and repeat-failure warnings.
    Returns (candidates, fallback)."""
    if mode == "next-move":
        cands = [c for c in _next_move_candidates(conn, quest_id) if c.get("eligible")]
        if limit:
            cands = cands[:int(limit)]
        return cands, None

    def rows(sql, *a):
        try:
            return conn.execute(sql, (quest_id, *a)).fetchall()
        except sqlite3.OperationalError:
            return []
    rfw = {w["ref"]: w["warnings"] for w in _repeat_failure_warnings(conn, quest_id)}
    cands = []
    for o in rows("SELECT opportunity_id, kind, rationale, motivating_refs, attempt_signature, status "
                  "FROM research_opportunity WHERE quest_id=? AND status='open' ORDER BY created_at, opportunity_id"):
        mr = _loads(o["motivating_refs"])
        un = _resolve_quest_refs(conn, quest_id, mr if isinstance(mr, dict) else None)
        cands.append({"candidate_ref": o["opportunity_id"], "candidate_kind": o["kind"], "source": "opportunity",
                      "rationale": o["rationale"], "motivating_refs": mr, "attempt_signature": _loads(o["attempt_signature"]),
                      "status": o["status"], "unresolved_refs": un,
                      "repeat_failure_warnings": rfw.get(o["opportunity_id"], [])})
    # Enumerable idea candidates: each gate-ELIGIBLE idea row (status proposed/selected) is its own candidate, so
    # BO can value a multi-candidate slate (not the whole slate collapsed to one idea_select ref). Gate-ineligible
    # rows (status rejected/exhausted) are EXCLUDED from acquisition (BO must not select gate-invalid candidates).
    idea_rows = rows("SELECT idea_id, statement, route, status FROM idea WHERE quest_id=? "
                     "AND status IN ('proposed','selected') ORDER BY idea_id")
    for ir in idea_rows:
        cands.append({"candidate_ref": ir["idea_id"], "candidate_kind": "idea", "source": "idea",
                      "rationale": (ir["statement"] or "")[:200], "route": ir["route"],
                      "motivating_refs": None, "attempt_signature": None, "status": ir["status"],
                      "unresolved_refs": [], "repeat_failure_warnings": rfw.get(ir["idea_id"], [])})
    if not idea_rows:
        # Backward-compatible lazy read: quests that never materialized idea rows (e.g. legacy q1) still expose
        # their latest idea selection as ONE candidate so existing tooling keeps working.
        idr = _latest_idea_select_row(conn, quest_id)
        if idr is not None and idr["select_id"]:
            cands.append({"candidate_ref": idr["select_id"], "candidate_kind": "idea", "source": "idea_select",
                          "rationale": "latest idea selection (idea_select; no enumerable idea rows)",
                          "motivating_refs": None, "attempt_signature": None,
                          "status": ("valid" if idr["valid"] else "unvalidated"),
                          "unresolved_refs": [], "repeat_failure_warnings": rfw.get(idr["select_id"], [])})
    for f in rows("SELECT entry_id, candidate_kind, candidate_ref, status FROM frontier_entry WHERE quest_id=? "
                  "AND status IN ('candidate','incumbent') ORDER BY rank, entry_id"):
        cands.append({"candidate_ref": f["entry_id"], "candidate_kind": "frontier", "source": "frontier",
                      "rationale": f"frontier {f['candidate_kind']} candidate -> {f['candidate_ref']}",
                      "motivating_refs": None, "attempt_signature": None, "status": f["status"],
                      "unresolved_refs": [], "repeat_failure_warnings": []})
    fallback = None
    if not cands:
        dims = rows("SELECT * FROM search_space WHERE quest_id=?")
        if dims:
            sug = {}
            for d in dims:
                try:
                    if d["dim_kind"] in ("real", "int") and d["low"] is not None and d["high"] is not None:
                        mid = (d["low"] + d["high"]) / 2
                        sug[d["dim_name"]] = int(mid) if d["dim_kind"] == "int" else mid
                except Exception:
                    pass
            fallback = {"candidate_ref": f"{quest_id}:search-space-midpoint", "candidate_kind": "param",
                        "source": "search_space", "params": sug, "status": "fallback",
                        "rationale": "midpoint/default over the declared search_space (FALLBACK heuristic — NOT "
                                     "real BO; ignores observed results and does not update on negative findings)",
                        "motivating_refs": None, "attempt_signature": None, "unresolved_refs": [],
                        "repeat_failure_warnings": []}
    if limit:
        cands = cands[:int(limit)]
    return cands, fallback


def _ucb_score(valuation, beta, *, has_repeat_warning=False, has_unresolved_ref=False,
               has_cross_quest_ref=False, missing_provenance=False):
    """Deterministic, documented UCB-like acquisition score over one reviewer valuation (dims 0-100):

        exploitation = 0.40*utility + 0.25*quality + 0.20*feasibility + 0.15*expected_effect   (expected_effect
                       defaults to 50 if absent/non-numeric)
        exploration  = (exploration_value + novelty + uncertainty) / 3
        penalty      = 0.35*risk + 0.25*cost
                       + 15 (repeat-failure warning) + 15 (unresolved ref) + 10 (cross-quest ref)
                       + 10 (missing provenance)
        score        = exploitation + beta*exploration - penalty

    Higher beta weighs exploration (novelty / info-gain / uncertainty) more. NOT full statistical BO."""
    v = valuation or {}

    def g(k, default=0.0):
        try:
            return float(v.get(k, default))
        except (TypeError, ValueError):
            return default
    ee = g("expected_effect", 50.0)
    exploitation = 0.40 * g("utility") + 0.25 * g("quality") + 0.20 * g("feasibility") + 0.15 * ee
    exploration = (g("exploration_value") + g("novelty") + g("uncertainty")) / 3.0
    ctx = (15.0 if has_repeat_warning else 0.0) + (15.0 if has_unresolved_ref else 0.0) \
        + (10.0 if has_cross_quest_ref else 0.0) + (10.0 if missing_provenance else 0.0)
    penalty = 0.35 * g("risk") + 0.25 * g("cost") + ctx
    return {"score": round(exploitation + beta * exploration - penalty, 4),
            "exploitation": round(exploitation, 4), "exploration": round(exploration, 4),
            "beta": beta, "penalty": round(penalty, 4), "context_penalty": round(ctx, 4)}


def _official_score(valuation, w_u=1.0, w_q=1.0, kappa=1.0, *, has_repeat_warning=False,
                    has_unresolved_ref=False, has_cross_quest_ref=False, missing_provenance=False):
    """OFFICIAL DeepScientist-style acquisition (the DEFAULT): a UCB-like weighted sum of the three core
    valuation dimensions (dims 0-100):

        score = w_u*utility + w_q*quality + kappa*exploration_value     (defaults w_u=w_q=kappa=1)

    `kappa` is the exploration coefficient (the UCB-like knob — higher kappa weighs exploration_value /
    information gain more). The official score is a pure weighted sum of the three core dims; the
    Findings-Memory penalty FLAGS (repeat-failure / unresolved / cross-quest / missing-provenance) are carried
    as transparency metadata but NOT subtracted here (use acquisition='houmao' / ucb_like_v1 for the richer
    formula that subtracts them). NOT full statistical BO."""
    v = valuation or {}

    def g(k, default=0.0):
        try:
            return float(v.get(k, default))
        except (TypeError, ValueError):
            return default
    u, q, ev = g("utility"), g("quality"), g("exploration_value")
    flags = {"has_repeat_warning": has_repeat_warning, "has_unresolved_ref": has_unresolved_ref,
             "has_cross_quest_ref": has_cross_quest_ref, "missing_provenance": missing_provenance}
    return {"score": round(w_u * u + w_q * q + kappa * ev, 4),
            "utility": round(u, 4), "quality": round(q, 4), "exploration_value": round(ev, 4),
            "w_u": w_u, "w_q": w_q, "kappa": kappa, "penalty_flags": flags}


def _stub_valuation(cand):
    """Deterministic OFFLINE stub valuation (is_stub=1) for tests / advisory use when no real reviewer ran.
    Derived ONLY from quest-local candidate signals — it is NOT a model and NOT proof; loudly labelled."""
    kind = (cand.get("candidate_kind") or "").lower()
    novelty = {"new_idea": 75, "idea": 65, "boundary": 55, "robustness": 45, "ablation": 40,
               "failure_followup": 50, "next_experiment": 50, "frontier": 55, "baseline_repair": 30,
               "param": 25}.get(kind, 50)
    explore = {"new_idea": 70, "boundary": 65, "robustness": 60, "failure_followup": 60}.get(kind, 45)
    feas = {"param": 80, "baseline_repair": 70, "ablation": 65, "next_experiment": 60}.get(kind, 55)
    risk = min(40 + (20 if cand.get("repeat_failure_warnings") else 0) + (15 if cand.get("unresolved_refs") else 0), 100)
    return {"utility": 55, "quality": 55, "novelty": novelty, "exploration_value": explore, "uncertainty": 50,
            "feasibility": feas, "cost": 40, "risk": risk, "expected_metric_direction": "unknown",
            "expected_effect": 50, "confidence": 40}


def _cand_penalty_flags(cand):
    un = cand.get("unresolved_refs") or []
    return {"has_repeat_warning": bool(cand.get("repeat_failure_warnings")),
            "has_unresolved_ref": bool(un),
            "has_cross_quest_ref": any(u.get("status") == "cross_quest" for u in un),
            "missing_provenance": False}


def _stub_allowed(cli_flag=False):
    """The OFFLINE stub (is_stub=1) is NOT a silent fallback when a real reviewer didn't run. It is permitted
    ONLY by an explicit signal: the `--allow-bo-stub` CLI flag (operator/test choice) or the
    DEEPRESEARCH_BO_ALLOW_STUB=1 env (non-interactive / CI). Returns (allowed: bool, source: str|None).
    When neither is set, callers must FAIL with an actionable error rather than record placeholder valuations —
    the default product behaviour is to launch the BO-reviewer agent (codex/max) or, if codex is unavailable,
    persist the documented claude fallback (agents/bo-reviewer.local.toml)."""
    import os as _os
    if cli_flag:
        return True, "cli_flag(--allow-bo-stub)"
    ev = (_os.environ.get("DEEPRESEARCH_BO_ALLOW_STUB") or "").strip().lower()
    if ev in ("1", "true", "yes", "on"):
        return True, "env(DEEPRESEARCH_BO_ALLOW_STUB)"
    return False, None


def _stub_blocked_diagnostic(cfg, n_missing):
    """Actionable error when the offline stub is needed but not permitted (no real reviewer output)."""
    return (f"{n_missing} candidate(s) have no real reviewer valuation and the OFFLINE stub is NOT permitted by "
            f"default. Resolve one of: (1) launch the BO-reviewer agent (product default backend "
            f"{cfg['product_default_backend']}/{cfg['product_default_effort']}) and pass its output via "
            f"--from-json; (2) if codex is unavailable, configure the claude fallback "
            f"(agents/bo-reviewer.local.toml [reviewer_override] backend_override=\"claude\" "
            f"credential_override=\"default\") and launch the BO-reviewer with claude; (3) for explicit "
            f"test/advisory use only, pass --allow-bo-stub or set DEEPRESEARCH_BO_ALLOW_STUB=1 (CI). The offline "
            f"stub is a deterministic placeholder, never evidence.")


@cli.group()
def bo(): ...


@bo.command("candidates")
@click.option("--quest-id", required=True)
@click.option("--next-move", "next_move", is_flag=True, default=False,
              help="enumerate the LATER next-move slate (eligible open opportunities + write/finalize/stop) "
                   "instead of the idea/opportunity slate.")
@click.pass_context
def bo_candidates(ctx, quest_id, next_move):
    """List the QUEST-LOCAL candidate research moves for reviewer evaluation (open opportunities, the latest idea
    selection, quest-local frontier entries; a search_space midpoint only as a labelled fallback). With
    --next-move, list the hard-gate-eligible LATER next-move slate. Read-only. Cross-quest / missing motivating
    refs are WARNED and never followed as memory."""
    conn = _conn(ctx)
    mode = "next-move" if next_move else "all"
    cands, fallback = _bo_candidates(conn, quest_id, limit=_reviewer_config()["max_candidates"], mode=mode)
    conn.close()
    warns = []
    for c in cands:
        for u in c.get("unresolved_refs") or []:
            warns.append(f"candidate {c['candidate_ref']} motivating ref {u['ref_type']}:{u['id']} is {u['status']} "
                         "(NOT followed as memory)")
        if c.get("repeat_failure_warnings"):
            warns.append(f"candidate {c['candidate_ref']}: " + "; ".join(c["repeat_failure_warnings"]))
    emit(envelope("bo candidates", ok=True, quest_id=quest_id,
                  data={"candidates": cands, "count": len(cands), "fallback": fallback,
                        "has_idea_level_candidates": bool(cands)}, warnings=warns))


@bo.command("next-moves")
@click.option("--quest-id", required=True)
@click.pass_context
def bo_next_moves(ctx, quest_id):
    """List the LATER next-move candidate slate with hard-gate ELIGIBILITY for transparency (read-only): every
    open research_opportunity + the synthetic write / finalize / stop moves, each tagged eligible/ineligible
    with a reason and a route_target. The acquisition (`bo select --next-move`) scores ONLY the eligible ones,
    so BO can never select a gate-invalid move. STRICTLY quest-local."""
    conn = _conn(ctx)
    cands = _next_move_candidates(conn, quest_id)
    has_results = bool(conn.execute("SELECT 1 FROM result WHERE quest_id=? LIMIT 1", (quest_id,)).fetchone())
    conn.close()
    eligible = [c for c in cands if c["eligible"]]
    emit(envelope("bo next-moves", ok=True, quest_id=quest_id,
                  data={"candidates": cands, "eligible": eligible, "n_eligible": len(eligible),
                        "count": len(cands), "post_experiment": has_results,
                        "routes": sorted({c["route_target"] for c in eligible})},
                  warnings=([] if has_results else
                            ["no experiment results yet — next-move BO applies post-experiment/analysis"])))


def _bo_write(conn, payload):
    """records.apply for a BO record; returns (ok, error)."""
    try:
        records.apply(conn, payload)
        return True, None
    except records.RecordError as e:
        return False, str(e)


@bo.command("review")
@click.option("--quest-id", required=True)
@click.option("--candidate-ref", default=None, help="review only this candidate (else all gathered candidates).")
@click.option("--backend", default=None, help="reviewer backend (default from agents/bo-reviewer.toml: codex).")
@click.option("--effort", default=None, help="reviewer effort (default from config: max).")
@click.option("--from-json", "from_json", default=None,
              help="path to reviewer-produced valuations [{candidate_ref,valuation,rationale,risks,...}]; records "
                   "them as real bo_review rows (is_stub=0). The DEFAULT path: launch the BO-reviewer agent and "
                   "pass its output here.")
@click.option("--allow-bo-stub", "allow_bo_stub", is_flag=True, default=False,
              help="permit the OFFLINE deterministic stub (is_stub=1) for candidates with no --from-json valuation. "
                   "Explicit test/advisory use ONLY (or set DEEPRESEARCH_BO_ALLOW_STUB=1 in CI). Without it, the "
                   "stub is REFUSED and the command fails with an actionable error — never a silent downgrade.")
@click.option("--next-move", "next_move", is_flag=True, default=False,
              help="value the LATER next-move slate (eligible opportunities + write/finalize/stop) instead of "
                   "the idea/opportunity slate.")
@click.option("--at", default=None, help="ISO-8601 timestamp (required to persist bo_review rows).")
@click.pass_context
def bo_review(ctx, quest_id, candidate_ref, backend, effort, from_json, at, allow_bo_stub, next_move):
    """Run/record the LLM Reviewer's surrogate valuation of candidate research moves (the BO scoring step).
    Default backend/effort come from agents/bo-reviewer.toml (codex / max). The harness does NOT call a
    provider itself: pass `--from-json` with valuations a launched reviewer agent produced (recorded as real
    bo_review rows), or omit it to record a clearly-labelled OFFLINE deterministic stub (is_stub=1) for
    tests/advisory. With --next-move it scores the later next-move slate. Valuations are validated against the
    bo_review schema (0-100 dims; missing/out-of-range rejected). QUEST-LOCAL only."""
    cfg = _reviewer_config({"backend": backend, "effort": effort})
    conn = _conn(ctx)
    cands, _fb = _bo_candidates(conn, quest_id, limit=cfg["max_candidates"], mode=("next-move" if next_move else "all"))
    if candidate_ref:
        cands = [c for c in cands if c["candidate_ref"] == candidate_ref]
    supplied = {}
    if from_json:
        for item in (_loads(open(from_json).read()) or []):
            if isinstance(item, dict) and item.get("candidate_ref"):
                supplied[item["candidate_ref"]] = item
    if not cands and not supplied:
        conn.close()
        emit(envelope("bo review", ok=True, quest_id=quest_id,
                      data={"reviewed": 0, "reviewer": cfg, "note": "no quest-local candidates to review"},
                      warnings=["no candidates — record research_opportunity rows or an idea selection first"]))
        return
    if not at:
        conn.close()
        emit(envelope("bo review", ok=False, quest_id=quest_id,
                      diagnostics=["--at <ISO-8601> is required to persist bo_review rows"]))
        sys.exit(1)
    reviewed, warns, used_stub = [], [], False
    targets = cands if cands else [{"candidate_ref": k, "candidate_kind": (v.get("candidate_kind") or ""),
                                    "unresolved_refs": [], "repeat_failure_warnings": []}
                                   for k, v in supplied.items()]
    # Offline stub is NOT a silent fallback: if any target has no real (--from-json) valuation it would be
    # stubbed — refuse unless explicitly allowed (--allow-bo-stub / DEEPRESEARCH_BO_ALLOW_STUB).
    n_missing = sum(1 for c in targets if supplied.get(c["candidate_ref"]) is None)
    allowed, allow_src = _stub_allowed(allow_bo_stub)
    if n_missing and not allowed:
        conn.close()
        emit(envelope("bo review", ok=False, quest_id=quest_id,
                      data={"reviewed": 0, "reviewer": cfg, "would_stub_candidates": n_missing,
                            "offline_stub_allowed": False},
                      diagnostics=[_stub_blocked_diagnostic(cfg, n_missing)]))
        sys.exit(1)
    for c in targets:
        ref = c["candidate_ref"]
        item = supplied.get(ref)
        if item is not None:
            valuation = item.get("valuation"); rationale = item.get("rationale", ""); risks = item.get("risks", [])
            rbackend = item.get("reviewer_backend") or cfg["backend"]; is_stub = bool(item.get("is_stub", False))
            rmodel = item.get("reviewer_model") or cfg["model"]; reffort = item.get("reviewer_effort") or cfg["effort"]
        else:
            valuation = _stub_valuation(c); rationale = "OFFLINE stub valuation (no real reviewer backend invoked)"
            risks = [w for w in (c.get("repeat_failure_warnings") or [])]; is_stub = True; used_stub = True
            rbackend, rmodel, reffort = "stub", "stub", cfg["effort"]
        rid = f"{quest_id}:borev:{ref}:{at}"
        payload = {"record_type": "bo_review.record", "record_id": rid, "at": at, "quest_id": quest_id,
                   "candidate_ref": ref, "candidate_kind": c.get("candidate_kind") or None,
                   "reviewer_backend": rbackend, "reviewer_model": rmodel, "reviewer_effort": reffort,
                   "is_stub": is_stub, "valuation": valuation, "rationale": rationale,
                   "risks": risks if isinstance(risks, list) else [str(risks)]}
        if c.get("motivating_refs") or c.get("unresolved_refs"):
            payload["context_refs"] = {"motivating_refs": c.get("motivating_refs"),
                                       "unresolved_refs": c.get("unresolved_refs")}
        ok, err = _bo_write(conn, payload)
        if ok:
            reviewed.append({"review_id": rid, "candidate_ref": ref, "is_stub": is_stub})
        else:
            warns.append(f"candidate {ref}: {err}")
    conn.commit(); conn.close()
    if used_stub:
        warns.append(f"OFFLINE STUB reviewer used (is_stub=1; permitted via {allow_src}): these valuations are a "
                     "deterministic placeholder, NOT a real LLM-reviewer call. Pass --from-json with a launched "
                     "reviewer's output for real valuations; never treat stub scores as evidence.")
    emit(envelope("bo review", ok=True, quest_id=quest_id,
                  data={"reviewed": len(reviewed), "reviews": reviewed, "used_stub": used_stub,
                        "stub_allowed_via": (allow_src if used_stub else None), "reviewer": cfg},
                  warnings=warns))


def _latest_reviews(conn, quest_id):
    """Latest bo_review per candidate_ref for the quest (most recent created_at wins)."""
    try:
        rs = conn.execute("SELECT review_id, candidate_ref, candidate_kind, valuation, is_stub, created_at "
                          "FROM bo_review WHERE quest_id=? ORDER BY created_at, review_id", (quest_id,)).fetchall()
    except sqlite3.OperationalError:
        return {}
    latest = {}
    for r in rs:
        latest[r["candidate_ref"]] = r  # ordered ascending -> last wins
    return latest


def _acq_score_one(method, val, beta, weights, flags):
    """Score a single valuation under the chosen acquisition method. 'ucb_official_v1' (default) is the official
    weighted-sum of the three core dims; 'ucb_like_v1' is the richer Houmao exploitation/exploration/penalty
    formula. Both consume the same Findings-Memory penalty flags."""
    fk = {k: flags.get(k, False) for k in
          ("has_repeat_warning", "has_unresolved_ref", "has_cross_quest_ref", "missing_provenance")}
    if method == "ucb_like_v1":
        return _ucb_score(val, beta, **fk)
    w = weights or {}
    return _official_score(val, w_u=float(w.get("w_u", 1.0)), w_q=float(w.get("w_q", 1.0)),
                           kappa=float(w.get("kappa", 1.0)), **fk)


def _bo_acquire(conn, quest_id, beta, method="ucb_official_v1", weights=None, mode="all"):
    """Compute the acquisition over the latest bo_review per candidate. Returns (scores_sorted, selected_ref,
    any_stub, review_refs). scores carry the full term breakdown + candidate_kind for auditability. Only
    candidates surfaced by _bo_candidates (gate-eligible) are scored — gate-ineligible idea/next-move candidates
    never appear. mode='next-move' scores the later next-move slate; default scores the idea/opportunity slate."""
    cands, _fb = _bo_candidates(conn, quest_id, limit=None, mode=mode)
    eligible_refs = {c["candidate_ref"] for c in cands}
    route_by_ref = {c["candidate_ref"]: c.get("route_target") for c in cands}
    flags_by_ref = {c["candidate_ref"]: _cand_penalty_flags(c) for c in cands}
    latest = _latest_reviews(conn, quest_id)
    scores, review_refs, any_stub = [], [], False
    for ref, r in latest.items():
        if eligible_refs and ref not in eligible_refs:
            continue  # a review exists but the candidate is no longer gate-eligible -> excluded from acquisition
        val = _loads(r["valuation"]) or {}
        sc = _acq_score_one(method, val, beta, weights, flags_by_ref.get(ref, {}))
        any_stub = any_stub or bool(r["is_stub"])
        review_refs.append(r["review_id"])
        entry = {"candidate_ref": ref, "candidate_kind": r["candidate_kind"], "review_id": r["review_id"],
                 "is_stub": bool(r["is_stub"]), "eligible": True, **sc}
        if route_by_ref.get(ref):
            entry["route_target"] = route_by_ref[ref]
        scores.append(entry)
    scores.sort(key=lambda s: (-s["score"], s["candidate_ref"]))
    selected = scores[0]["candidate_ref"] if scores else None
    return scores, selected, any_stub, review_refs


def _bind_idea_select(conn, quest_id, selected_ref):
    """Bind idea_select.retained_candidate to the BO-selected winner and flip its idea row to status='selected'
    (other eligible idea rows revert to 'proposed'). Only applies when the winner is an enumerable idea row.
    Returns (bound_candidate_id | None, note)."""
    if not selected_ref:
        return None, "no selected candidate to bind"
    irow = conn.execute("SELECT idea_id FROM idea WHERE quest_id=? AND idea_id=?",
                        (quest_id, selected_ref)).fetchone()
    if irow is None:
        return None, f"selected candidate {selected_ref!r} is not an enumerable idea row (nothing to bind)"
    cid = _idea_candidate_id(selected_ref)
    # demote other currently-selected idea rows for this quest, then promote the winner
    conn.execute("UPDATE idea SET status='proposed' WHERE quest_id=? AND status='selected' AND idea_id<>?",
                (quest_id, selected_ref))
    conn.execute("UPDATE idea SET status='selected' WHERE quest_id=? AND idea_id=?", (quest_id, selected_ref))
    isr = _latest_idea_select_row(conn, quest_id)
    if isr is not None:
        conn.execute("UPDATE idea_select SET retained_candidate=? WHERE select_id=?", (cid, isr["select_id"]))
    return cid, f"bound idea_select.retained_candidate={cid} and flipped idea row {selected_ref} to selected"


def _ineligible_idea_candidates(conn, quest_id):
    """Gate-ineligible idea rows (status rejected/exhausted) with the scout's rejection reason (from the slate
    artifact when readable) — surfaced in the bo_decision for transparency. Quest-local."""
    try:
        rows = conn.execute("SELECT idea_id, status, artifact_ref FROM idea WHERE quest_id=? "
                            "AND status IN ('rejected','exhausted') ORDER BY idea_id", (quest_id,)).fetchall()
    except sqlite3.OperationalError:
        return []
    reasons = {}
    for r in rows:
        if r["artifact_ref"] and r["artifact_ref"] not in reasons:
            try:
                doc = json.loads(_read_artifact_text(r["artifact_ref"]) or "null")
                reasons[r["artifact_ref"]] = {x.get("candidate_id"): x.get("reason")
                                              for x in (doc.get("rejected") or [])} if isinstance(doc, dict) else {}
            except Exception:
                reasons[r["artifact_ref"]] = {}
    out = []
    for r in rows:
        cid = _idea_candidate_id(r["idea_id"])
        rr = (reasons.get(r["artifact_ref"]) or {}).get(cid)
        out.append({"candidate_ref": r["idea_id"], "candidate_id": cid, "eligible": False,
                    "rejection_reason": rr or "below idea_score_min floor / gate-ineligible"})
    return out


@bo.command("select")
@click.option("--quest-id", required=True)
@click.option("--beta", type=float, default=None, help="ucb_like_v1 exploration coefficient (default 0.5).")
@click.option("--acquisition", "acquisition", default=None,
              help="acquisition rule: 'official'/'ucb_official_v1' (DEFAULT: w_u*utility+w_q*quality+"
                   "kappa*exploration_value) or 'houmao'/'ucb_like_v1' (richer exploitation/exploration/penalty).")
@click.option("--w-u", "w_u", type=float, default=None, help="official utility weight (default 1).")
@click.option("--w-q", "w_q", type=float, default=None, help="official quality weight (default 1).")
@click.option("--kappa", "kappa", type=float, default=None, help="official exploration coefficient (default 1).")
@click.option("--decision-kind", "decision_kind", default="idea-selection",
              type=click.Choice(["idea-selection", "experiment-selection", "opportunity-selection",
                                 "stop-write-finalize-selection", "next-move-selection"]),
              help="which research move this acquisition decides (default idea-selection). For --next-move it is "
                   "auto-derived from the winner unless explicitly set.")
@click.option("--next-move", "next_move", is_flag=True, default=False,
              help="select over the LATER next-move slate (eligible opportunities + write/finalize/stop) and "
                   "BIND the routing target to the winner (no idea_select binding).")
@click.option("--bind/--no-bind", "bind", default=None,
              help="bind idea_select.retained_candidate to the BO winner (default: on for idea-selection).")
@click.option("--skip-reason", "skip_reason", default=None,
              help="record an EXPLICIT single-candidate skip (acquisition_method='skipped'): selects the one "
                   "viable candidate without scoring and records the reason. Use when only one viable candidate.")
@click.option("--at", default=None, help="ISO-8601 timestamp (required to persist the bo_decision).")
@click.pass_context
def bo_select(ctx, quest_id, beta, acquisition, w_u, w_q, kappa, decision_kind, next_move, bind, skip_reason, at):
    """Compute the ACQUISITION over the latest bo_review valuations and record a bo_decision (which research move
    to make next and why the others lost). DEFAULT method 'ucb_official_v1' = w_u*utility + w_q*quality +
    kappa*exploration_value (1/1/1); 'houmao'/'ucb_like_v1' selects the richer Houmao formula. For
    decision-kind=idea-selection the winner BINDS idea_select.retained_candidate; for --next-move the winner's
    route_target is the BOUND next stage (decision_kind auto-derived: experiment-/opportunity-/stop-write-
    finalize-selection). A single viable candidate may be skipped with --skip-reason (recorded explicitly).
    LLM-reviewer surrogate + UCB-like acquisition, NOT full statistical Bayesian optimization. Run `bo review`."""
    method = {"official": "ucb_official_v1", "houmao": "ucb_like_v1"}.get(acquisition, acquisition)
    cfg = _reviewer_config({"beta": beta, "acquisition_method": method, "w_u": w_u, "w_q": w_q, "kappa": kappa})
    method = cfg["acquisition_method"]
    beta = float(cfg["beta"])
    weights = {"w_u": float(cfg["w_u"]), "w_q": float(cfg["w_q"]), "kappa": float(cfg["kappa"])}
    acq_config = weights if method == "ucb_official_v1" else {"beta": beta}
    mode = "next-move" if next_move else "all"
    # idea-selection binds idea_select; next-move binds routing (no idea binding); default per decision_kind.
    do_bind = bind if bind is not None else (decision_kind == "idea-selection" and not next_move)
    conn = _conn(ctx)
    nm_cands = _next_move_candidates(conn, quest_id) if next_move else []
    ineligible = ([c for c in nm_cands if not c["eligible"]] if next_move
                  else _ineligible_idea_candidates(conn, quest_id))
    warns = []

    def _route_of(ref):
        c = next((x for x in nm_cands if x["candidate_ref"] == ref), None)
        return c.get("route_target") if c else None

    # ── Explicit single-candidate SKIP path: record a bo_decision without scoring, then bind. ──
    if skip_reason is not None:
        cands, _fb = _bo_candidates(conn, quest_id, limit=None, mode=mode)
        viable = (cands if next_move else
                  ([c for c in cands if c["candidate_kind"] == "idea"] if decision_kind == "idea-selection" else cands))
        if len(viable) != 1:
            conn.close()
            emit(envelope("bo select", ok=False, quest_id=quest_id,
                          data={"viable_candidates": len(viable)},
                          diagnostics=[f"--skip-reason requires exactly ONE viable candidate; found {len(viable)}. "
                                       "Run `bo review` + `bo select` to choose among multiple candidates."]))
            sys.exit(1)
        selected = viable[0]["candidate_ref"]
        dkind = _derive_next_move_kind(selected, nm_cands) if next_move else decision_kind
        sel_route = _route_of(selected) if next_move else None
        rationale = f"single viable {'next move' if next_move else 'candidate'} skip: {skip_reason}"
        sc_entry = {"candidate_ref": selected, "eligible": True, "score": None, "skipped": True}
        if sel_route:
            sc_entry["route_target"] = sel_route
        data = {"selected_candidate_ref": selected, "acquisition_method": "skipped", "decision_kind": dkind,
                "acquisition_config": {}, "acquisition_scores": [sc_entry], "selected_route": sel_route,
                "ineligible_candidates": ineligible, "selection_rationale": rationale, "skipped": True}
        if at:
            did = f"{quest_id}:bodec:{at}"
            ok, err = _bo_write(conn, {"record_type": "bo_decision.record", "record_id": did, "at": at,
                                       "quest_id": quest_id, "candidate_refs": [selected], "review_refs": [],
                                       "selected_candidate_ref": selected, "acquisition_method": "skipped",
                                       "acquisition_config": {}, "decision_kind": dkind,
                                       "acquisition_scores": [sc_entry], "selection_rationale": rationale})
            if ok:
                data["decision_id"] = did
                if do_bind and dkind == "idea-selection":
                    cid, note = _bind_idea_select(conn, quest_id, selected)
                    data["bound_candidate"] = cid; data["bind_note"] = note
                conn.commit()
            else:
                warns.append(f"bo_decision not persisted: {err}")
        else:
            warns.append("pass --at <ISO-8601> to persist the skip bo_decision")
        conn.close()
        emit(envelope("bo select", ok=True, quest_id=quest_id, data=data, warnings=warns))
        return

    scores, selected, any_stub, review_refs = _bo_acquire(conn, quest_id, beta, method=method, weights=weights, mode=mode)
    if not scores:
        conn.close()
        emit(envelope("bo select", ok=True, quest_id=quest_id,
                      data={"selected_candidate_ref": None, "acquisition_method": method,
                            "decision_kind": decision_kind, "acquisition_scores": [],
                            "ineligible_candidates": ineligible},
                      warnings=["no bo_review valuations to select over — run `bo review`" +
                                (" --next-move" if next_move else "") + " first (or pass --skip-reason for a "
                                "single viable candidate)"]))
        return
    # next-move decision_kind is auto-derived from the winner unless the caller pinned a non-default one.
    dkind = decision_kind
    if next_move and decision_kind == "idea-selection":
        dkind = _derive_next_move_kind(selected, nm_cands)
    sel_route = _route_of(selected) if next_move else None
    top = scores[0]
    rationale = (f"selected {selected}" + (f" -> route {sel_route}" if sel_route else "") +
                 f" via {method} (score {top['score']}); "
                 + (f"beat {len(scores) - 1} other candidate(s)" if len(scores) > 1 else "only candidate"))
    data = {"selected_candidate_ref": selected, "acquisition_method": method, "decision_kind": dkind,
            "acquisition_config": acq_config, "acquisition_scores": scores, "ineligible_candidates": ineligible,
            "selected_route": sel_route, "selection_rationale": rationale, "used_stub_reviews": any_stub}
    warns += (["selection used OFFLINE STUB reviews (is_stub=1) — advisory only, not evidence"] if any_stub else [])
    if at:
        did = f"{quest_id}:bodec:{at}"
        payload = {"record_type": "bo_decision.record", "record_id": did, "at": at, "quest_id": quest_id,
                   "candidate_refs": [s["candidate_ref"] for s in scores], "review_refs": review_refs,
                   "selected_candidate_ref": selected, "acquisition_method": method, "decision_kind": dkind,
                   "acquisition_config": acq_config,
                   "acquisition_scores": scores + ineligible, "selection_rationale": rationale}
        ok, err = _bo_write(conn, payload)
        if ok:
            data["decision_id"] = did
            if do_bind and dkind == "idea-selection":
                cid, note = _bind_idea_select(conn, quest_id, selected)
                data["bound_candidate"] = cid; data["bind_note"] = note
            conn.commit()
        else:
            warns.append(f"bo_decision not persisted: {err}")
    else:
        warns.append("pass --at <ISO-8601> to persist the bo_decision (returned advisory-only without it)")
    conn.close()
    emit(envelope("bo select", ok=True, quest_id=quest_id, data=data, warnings=warns))


@bo.command("suggest")
@click.option("--quest-id", required=True)
@click.option("--space-id", default=None)
@click.option("--beta", type=float, default=None, help="UCB exploration coefficient (default from config: 0.5).")
@click.option("--allow-bo-stub", "allow_bo_stub", is_flag=True, default=False,
              help="permit OFFLINE stub valuations for unreviewed candidates (explicit test/advisory ONLY; or "
                   "DEEPRESEARCH_BO_ALLOW_STUB=1). Without it, suggest scores only REAL reviews and reports "
                   "'needs-reviewer' when none exist — never a silent stub.")
@click.option("--at", default=None, help="ISO-8601 timestamp (required to persist reviews/decision).")
@click.pass_context
def bo_suggest(ctx, quest_id, space_id, beta, at, allow_bo_stub):
    """Recommend the next research move (high-level idea-level BO entry point). When quest-local candidates exist:
    gather them, use existing bo_review valuations (or, if none, a clearly-labelled OFFLINE stub pass), compute
    the UCB-like acquisition, optionally persist a bo_decision (with --at), and return the selected candidate +
    rationale. When NO idea-level candidate exists but a search_space does, fall back to the labelled
    midpoint/default heuristic (NOT real BO). Otherwise returns a clear no-candidate message."""
    cfg = _reviewer_config({"beta": beta})
    beta = float(cfg["beta"])
    method = cfg["acquisition_method"]
    weights = {"w_u": float(cfg["w_u"]), "w_q": float(cfg["w_q"]), "kappa": float(cfg["kappa"])}
    acq_config = weights if method == "ucb_official_v1" else {"beta": beta}
    conn = _conn(ctx)
    cands, fallback = _bo_candidates(conn, quest_id, limit=cfg["max_candidates"])
    if cands:
        latest = _latest_reviews(conn, quest_id)
        reviewed_refs = set(latest.keys())
        warns, used_stub = [], False
        allowed, allow_src = _stub_allowed(allow_bo_stub)
        # Unreviewed candidates are only stub-scored when the stub is EXPLICITLY allowed; otherwise suggest
        # scores REAL reviews only and reports 'needs-reviewer' below if none exist (no silent stub).
        missing = [c for c in cands if c["candidate_ref"] not in reviewed_refs]
        if missing and not allowed and not reviewed_refs:
            conn.close()
            emit(envelope("bo suggest", ok=True, quest_id=quest_id,
                          data={"mode": "needs-reviewer", "selected_candidate_ref": None, "reviewer": cfg,
                                "n_candidates": len(cands), "n_real_reviews": 0, "offline_stub_allowed": False},
                          warnings=[_stub_blocked_diagnostic(cfg, len(missing))]))
            return
        if missing and allowed and at:
            for c in missing:
                rid = f"{quest_id}:borev:{c['candidate_ref']}:{at}"
                payload = {"record_type": "bo_review.record", "record_id": rid, "at": at, "quest_id": quest_id,
                           "candidate_ref": c["candidate_ref"], "candidate_kind": c.get("candidate_kind") or None,
                           "reviewer_backend": "stub", "reviewer_model": "stub", "reviewer_effort": cfg["effort"],
                           "is_stub": True, "valuation": _stub_valuation(c),
                           "rationale": "OFFLINE stub valuation (no real reviewer backend invoked)",
                           "risks": list(c.get("repeat_failure_warnings") or [])}
                _bo_write(conn, payload)
            conn.commit()
            used_stub = True
        if missing and allowed and not at:
            used_stub = True  # in-memory stub for the advisory computation below
        # Acquisition over whatever reviews now exist; if none persisted (no --at), score in-memory.
        scores, selected, any_stub, review_refs = _bo_acquire(conn, quest_id, beta, method=method, weights=weights)
        if not scores and allowed:  # no persisted reviews (no --at): compute in-memory stub scores (stub allowed)
            scores = []
            for c in cands:
                sc = _acq_score_one(method, _stub_valuation(c), beta, weights, _cand_penalty_flags(c))
                scores.append({"candidate_ref": c["candidate_ref"], "candidate_kind": c.get("candidate_kind"),
                               "is_stub": True, **sc})
            scores.sort(key=lambda s: (-s["score"], s["candidate_ref"]))
            selected, any_stub, review_refs = (scores[0]["candidate_ref"] if scores else None), True, []
        if not scores:  # real reviews exist for some candidates but none scored (no --at, stub not allowed)
            conn.close()
            emit(envelope("bo suggest", ok=True, quest_id=quest_id,
                          data={"mode": "needs-reviewer", "selected_candidate_ref": None, "reviewer": cfg,
                                "n_candidates": len(cands), "offline_stub_allowed": False},
                          warnings=["pass --at to score persisted real reviews, or --allow-bo-stub for an "
                                    "advisory stub computation"]))
            return
        top = scores[0]
        rationale = f"selected {selected} via {method} acquisition (score {top['score']})"
        data = {"mode": "idea-level-bo", "selected_candidate_ref": selected, "acquisition_method": method,
                "acquisition_config": acq_config, "acquisition_scores": scores, "selection_rationale": rationale,
                "used_stub_reviews": any_stub, "reviewer": cfg, "n_candidates": len(cands)}
        if at and review_refs:
            did = f"{quest_id}:bodec:{at}"
            ok, err = _bo_write(conn, {"record_type": "bo_decision.record", "record_id": did, "at": at,
                                       "quest_id": quest_id, "candidate_refs": [s["candidate_ref"] for s in scores],
                                       "review_refs": review_refs, "selected_candidate_ref": selected,
                                       "acquisition_method": method, "acquisition_config": acq_config,
                                       "acquisition_scores": scores, "selection_rationale": rationale})
            conn.commit()
            if ok:
                data["decision_id"] = did
            else:
                warns.append(f"bo_decision not persisted: {err}")
        elif not at:
            warns.append("advisory-only (no --at): pass --at <ISO-8601> to persist bo_review/bo_decision rows")
        if any_stub:
            warns.append("used OFFLINE STUB valuations (is_stub=1) — advisory placeholder, NOT a real reviewer "
                         "call or optimization evidence; run `bo review --from-json` with a launched reviewer.")
        conn.close()
        emit(envelope("bo suggest", ok=True, quest_id=quest_id, data=data, warnings=warns))
        return
    # No idea-level candidate: labelled search_space midpoint FALLBACK (NOT real BO), else no-candidate.
    nobs = conn.execute("SELECT COUNT(*) FROM experiment_param p JOIN experiment e ON e.experiment_id=p.experiment_id "
                        "WHERE e.quest_id=?", (quest_id,)).fetchone()[0]
    conn.close()
    if fallback is None:
        emit(envelope("bo suggest", ok=True, quest_id=quest_id,
                      data={"mode": "none", "suggestion": None,
                            "note": "no idea-level candidates and no search_space; record research_opportunity "
                                    "rows / an idea selection, or define a search_space"},
                      warnings=["no candidates available"]))
        return
    emit(envelope("bo suggest", ok=True, quest_id=quest_id,
                  data={"mode": "search-space-fallback", "stub": True, "strategy": "midpoint-default",
                        "observations": nobs, "suggestion": fallback["params"]},
                  warnings=["FALLBACK (NOT real BO): no idea-level candidates exist, so this is the search_space "
                            f"'midpoint-default' — it ignores all {nobs} observed result(s) and does not update on "
                            "negative findings. Prefer recording research_opportunity candidates and running "
                            "`bo review` + `bo select`. Do NOT treat this fallback as optimization evidence."]))


@bo.command("status")
@click.option("--quest-id", required=True)
@click.pass_context
def bo_status(ctx, quest_id):
    """Quest-local BO posture. Reports the best primary measurement + an HONEST trailing no-improvement streak
    (objective sense from the validated scope contract's metric_direction), PLUS the idea-level BO state:
    candidate count, reviewed-candidate count, the latest bo_decision (method + selected candidate), and whether
    the latest reviews were a real reviewer backend or the OFFLINE stub. LLM-reviewer surrogate + UCB-like
    acquisition — NOT full statistical Bayesian optimization."""
    conn = _conn(ctx)
    vals = [r[0] for r in conn.execute(
        "SELECT m.value_num FROM measurement m JOIN result r ON r.result_id=m.result_id "
        "WHERE r.quest_id=? AND m.is_primary=1 AND m.value_num IS NOT NULL "
        "ORDER BY r.created_at, r.result_id", (quest_id,)).fetchall()]
    lower = False
    try:
        sc = conn.execute("SELECT contract FROM scope_contract WHERE quest_id=? AND valid=1 "
                          "ORDER BY created_at DESC, contract_id DESC LIMIT 1", (quest_id,)).fetchone()
        md = (json.loads(sc[0]).get("metric_direction") if sc and sc[0] else "") or ""
        lower = any(t in md.lower() for t in ("min", "lower", "decrease", "down", "less"))
        sense_src = "scope_contract.metric_direction" if (sc and sc[0]) else "default"
    except Exception:
        sense_src = "default"
    better = (lambda v, b: v < b) if lower else (lambda v, b: v > b)
    best = (min(vals) if lower else max(vals)) if vals else None
    streak, run_best = 0, None
    for v in vals:
        if run_best is None or better(v, run_best):
            run_best, streak = v, 0
        else:
            streak += 1
    # idea-level BO state
    cands, _fb = _bo_candidates(conn, quest_id, limit=None)
    latest = _latest_reviews(conn, quest_id)
    real_reviews = sum(1 for r in latest.values() if not r["is_stub"])
    cfg = _reviewer_config()
    dec = None
    try:
        d = conn.execute("SELECT decision_id, selected_candidate_ref, acquisition_method, created_at FROM bo_decision "
                         "WHERE quest_id=? ORDER BY created_at DESC, decision_id DESC LIMIT 1", (quest_id,)).fetchone()
        if d:
            dec = {"decision_id": d["decision_id"], "selected_candidate_ref": d["selected_candidate_ref"],
                   "acquisition_method": d["acquisition_method"], "created_at": d["created_at"]}
    except sqlite3.OperationalError:
        dec = None
    conn.close()
    stub_env_on, _ = _stub_allowed(False)
    backend_overridden = cfg["backend_source"] not in ("built_in", "product_default")
    emit(envelope("bo status", quest_id=quest_id,
                  data={"best_primary": best, "observations": len(vals), "no_improvement_streak": streak,
                        "objective_sense": ("lower_is_better" if lower else "higher_is_better"),
                        "objective_sense_source": sense_src,
                        "method": "LLM-reviewer surrogate + UCB-like acquisition (NOT full statistical BO)",
                        "n_candidates": len(cands), "n_reviewed_candidates": len(latest),
                        "n_real_reviews": real_reviews, "n_stub_reviews": len(latest) - real_reviews,
                        "used_real_reviewer": real_reviews > 0 and real_reviews == len(latest),
                        # Honest live-vs-stub posture of the latest reviews: 'real' if every reviewed candidate
                        # has a real (is_stub=0) review, 'stub' if any is a placeholder, 'none' if unreviewed.
                        "reviews_posture": ("none" if not latest else
                                            ("real" if real_reviews == len(latest) else "stub")),
                        "latest_decision": dec,
                        # The OFFLINE stub is explicit-only — never a silent fallback when creds are missing.
                        "offline_stub_policy": "explicit-only (--allow-bo-stub or DEEPRESEARCH_BO_ALLOW_STUB=1)",
                        "offline_stub_env_enabled": stub_env_on,
                        "reviewer_config": {"backend": cfg["backend"], "effort": cfg["effort"],
                                            "backend_source": cfg["backend_source"],
                                            "backend_is_overridden": backend_overridden,
                                            "product_default_backend": cfg["product_default_backend"],
                                            "product_default_effort": cfg["product_default_effort"],
                                            "effective_backend": cfg["backend"], "effective_effort": cfg["effort"],
                                            "credential_override": cfg.get("credential_override"),
                                            "local_override_source": cfg.get("local_override_source"),
                                            "acquisition_method": cfg["acquisition_method"], "beta": cfg["beta"],
                                            "required_before_select": cfg["required_before_select"]}}))


# ───────────────── lit (core; real arxiv backend with graceful fallback) ─────────────────
@cli.group()
def lit(): ...


def _arxiv_query(query=None, arxiv_id=None, max_results=8, timeout=12):
    """Query the public arXiv API (no key). Returns a list of {arxiv_id,title,authors,year,uri,summary}.
    Network-dependent; raises on failure so callers can fall back to the stub."""
    import urllib.parse, urllib.request, xml.etree.ElementTree as ET
    if arxiv_id:
        q = "id_list=" + urllib.parse.quote(arxiv_id)
    else:
        q = "search_query=" + urllib.parse.quote("all:" + (query or "")) + "&sortBy=relevance"
    url = f"http://export.arxiv.org/api/query?{q}&max_results={max_results}"
    raw = urllib.request.urlopen(url, timeout=timeout).read()
    ns = {"a": "http://www.w3.org/2005/Atom"}
    out = []
    for e in ET.fromstring(raw).findall("a:entry", ns):
        idu = (e.findtext("a:id", "", ns) or "").strip()
        aid = idu.rsplit("/abs/", 1)[-1]
        out.append({
            "arxiv_id": aid,
            "title": " ".join((e.findtext("a:title", "", ns) or "").split()),
            "authors": [a.findtext("a:name", "", ns) for a in e.findall("a:author", ns)],
            "year": (e.findtext("a:published", "", ns) or "")[:4],
            "uri": idu,
            "summary": " ".join((e.findtext("a:summary", "", ns) or "").split())[:600],
        })
    return out


@lit.command("search")
@click.option("--query", required=True)
@click.option("--max-results", type=int, default=8)
def lit_search(query, max_results):
    """Search arXiv for sources matching a query (real backend; falls back to an empty stub if offline)."""
    try:
        res = _arxiv_query(query=query, max_results=max_results)
        emit(envelope("lit search", data={"query": query, "backend": "arxiv", "count": len(res),
                                          "results": [{"source": "arxiv", "title": r["title"], "uri": r["uri"],
                                                       "arxiv_id": r["arxiv_id"], "year": r["year"],
                                                       "authors": r["authors"]} for r in res]}))
    except Exception as e:
        emit(envelope("lit search", ok=True, data={"query": query, "backend": "offline-stub", "results": [],
                                                   "note": f"arxiv query failed ({e}); record references manually via lit fetch"},
                      warnings=["arxiv search unavailable; offline fallback"]))


@lit.command("fetch")
@click.option("--reference-id", required=True)
@click.option("--quest-id", default=None)
@click.option("--source", required=True, type=click.Choice(["arxiv", "web", "doi", "manual"]))
@click.option("--uri", required=True)
@click.option("--title", default=None)
@click.option("--cite-key", default=None)
@click.option("--artifact-ref", default=None)
@click.option("--at", required=True)
@click.pass_context
def lit_fetch(ctx, reference_id, quest_id, source, uri, title, cite_key, artifact_ref, at):
    # Stub fetch: no real download; record a reference row. arxiv/web require a cached artifact_ref.
    ref = artifact_ref or (f"runs/{quest_id}/refs/{reference_id}.cache" if source in ("arxiv", "web") else None)
    p = {"record_type": "reference.record", "record_id": reference_id, "at": at, "source": source,
         "uri": uri, "fetched_at": at}
    for k, v in dict(quest_id=quest_id, title=title, cite_key=cite_key, artifact_ref=ref).items():
        if v is not None:
            p[k] = v
    _apply(ctx, "lit fetch", p, quest_id=quest_id)


@lit.command("query")
@click.option("--quest-id", required=True)
@click.pass_context
def lit_query(ctx, quest_id):
    conn = _conn(ctx)
    data = db.rows(conn, "SELECT * FROM reference WHERE quest_id=?", (quest_id,))
    conn.close()
    emit(envelope("lit query", quest_id=quest_id, data={"rows": data}))


@lit.command("bib")
@click.option("--quest-id", required=True)
@click.option("--out", "out_path", required=True, help="Output .bib path the Writer cites against.")
@click.pass_context
def lit_bib(ctx, quest_id, out_path):
    """Emit a BibTeX file from the quest's recorded `reference` rows (for the paper-latex `--bib`)."""
    from paths import LOOP_DIR
    from pathlib import Path
    conn = _conn(ctx)
    rows = db.rows(conn, "SELECT * FROM reference WHERE quest_id=?", (quest_id,))
    conn.close()
    def key(r, i):
        return (r.get("cite_key") or r.get("reference_id") or f"ref{i}").replace(" ", "_")

    def _arxiv_id_from_uri(u):
        u = u or ""
        if "arxiv.org" in u:
            return u.rsplit("/abs/", 1)[-1].rsplit("/pdf/", 1)[-1].replace(".pdf", "")
        return None

    entries, enriched = [], 0
    for i, r in enumerate(rows, 1):
        k = key(r, i)
        title = (r.get("title") or r.get("reference_id") or "Untitled").replace("{", "").replace("}", "")
        url = r.get("uri") or ""
        # arXiv refs: fetch author/year for a proper @article (graceful fallback to @misc when offline).
        aid = _arxiv_id_from_uri(url) if r.get("source") == "arxiv" else None
        meta = None
        if aid:
            try:
                hits = _arxiv_query(arxiv_id=aid, max_results=1)
                meta = hits[0] if hits else None
            except Exception:
                meta = None
        if meta and meta.get("authors"):
            authors = " and ".join(meta["authors"])
            year = meta.get("year") or ""
            entries.append(f"@article{{{k},\n  title = {{{meta['title'] or title}}},\n  author = {{{authors}}},\n"
                           f"  year = {{{year}}},\n  eprint = {{{aid}}},\n  archivePrefix = {{arXiv}},\n"
                           f"  howpublished = {{\\url{{{url}}}}}\n}}")
            enriched += 1
        else:
            entries.append(f"@misc{{{k},\n  title = {{{title}}},\n  howpublished = {{\\url{{{url}}}}},\n"
                           f"  note = {{source: {r.get('source','manual')}}}\n}}")
    bib = (f"% Generated by `deepresearch lit bib` from recorded reference rows ({enriched}/{len(entries)} "
           f"arXiv-enriched).\n\n" + "\n\n".join(entries) + "\n")
    out_abs = out_path if out_path.startswith("/") else str(LOOP_DIR / out_path)
    Path(out_abs).parent.mkdir(parents=True, exist_ok=True)
    Path(out_abs).write_text(bib, encoding="utf-8")
    emit(envelope("lit bib", quest_id=quest_id, data={"out_path": out_path, "entries": len(entries),
                                                       "cite_keys": [key(r, i) for i, r in enumerate(rows, 1)]}))


@lit.command("audit")
@click.option("--quest-id", required=True)
@click.pass_context
def lit_audit(ctx, quest_id):
    """Scholarship-bar audit: checks the quest meets the literature bar — enough real reference
    rows AND >= 1 claim positioned against a reference — plus soft warnings (all-`manual` bib, missing
    Related Work heading). The same check backs the hard finalize gate; run it before review/finalize. See
    execplan/docs/publication-quality.md."""
    conn = _conn(ctx)
    audit = records.scholarship_audit(conn, quest_id)
    conn.close()
    emit(envelope("lit audit", ok=audit["ok"], quest_id=quest_id, data=audit,
                  diagnostics=audit["reasons"], warnings=audit["warnings"]))
    if not audit["ok"]:
        sys.exit(1)


# ───────────────── git ─────────────────
@cli.group()
def git(): ...


@git.command("branch-record")
@click.option("--branch-id", required=True)
@click.option("--quest-id", required=True)
@click.option("--git-branch", required=True)
@click.option("--status", default="active")
@click.option("--parent-branch-id", default=None)
@click.option("--worktree-ref", default=None)
@click.option("--at", required=True)
@click.pass_context
def git_branch_record(ctx, branch_id, quest_id, git_branch, status, parent_branch_id, worktree_ref, at):
    p = {"record_type": "branch.record", "record_id": branch_id, "at": at, "quest_id": quest_id,
         "git_branch": git_branch, "status": status}
    for k, v in dict(parent_branch_id=parent_branch_id, worktree_ref=worktree_ref).items():
        if v is not None:
            p[k] = v
    _apply(ctx, "git branch-record", p, quest_id=quest_id)


@git.command("checkpoint")
@click.option("--quest-id", required=True)
@click.option("--artifact-id", required=True)
@click.option("--ref", required=True)
@click.option("--kind", default="bundle")
@click.option("--round-index", type=int, default=None)
@click.option("--at", required=True)
@click.pass_context
def git_checkpoint(ctx, quest_id, artifact_id, ref, kind, round_index, at):
    # Stub: no real `git commit`; index the artifact so downstream stages can find it.
    p = {"record_type": "artifact.record", "record_id": artifact_id, "at": at, "quest_id": quest_id,
         "kind": kind, "ref": ref}
    if round_index is not None:
        p["round_index"] = round_index
    try:
        conn = _conn(ctx)
        data = records.apply(conn, p)
    except records.RecordError as e:
        emit(envelope("git checkpoint", ok=False, diagnostics=[str(e)])); sys.exit(1)
    _finish(ctx, conn, "git checkpoint", {"stub": True, "committed": False, "artifact": data,
                                          "note": "records artifact; real git commit pending implementation"}, quest_id=quest_id)


@git.command("status")
@click.option("--quest-id", default=None)
def git_status(quest_id):
    emit(envelope("git status", quest_id=quest_id, data={"stub": True, "clean": None,
                                                         "note": "real working-tree status pending implementation"}))


# ───────────────── experiment / result / metric (domain-pluggable) ─────────────────
@cli.group()
def experiment(): ...


@experiment.command("run")
@click.option("--experiment-id", required=True)
@click.option("--quest-id", required=True)
@click.option("--cmd", default=None, help="Shell command to execute under the operator-confirmed GPU device set. CUDA_VISIBLE_DEVICES is injected from gpu_allocation; runs only if confirmed.")
@click.option("--cwd", default=None, help="Working directory for --cmd (e.g. the experiment worktree).")
@click.option("--timeout", default=None, type=int, help="Optional timeout (seconds) for --cmd.")
@click.pass_context
def experiment_run(ctx, experiment_id, quest_id, cmd, cwd, timeout):
    """Domain-pluggable runner. FAIL-CLOSED GPU gate: refuses to run unless the quest has an
    operator-confirmed gpu_allocation, and injects CUDA_VISIBLE_DEVICES=<confirmed devices> into the
    child environment so executed code is physically restricted to the confirmed set."""
    import os
    import subprocess
    _authz_cmd("experiment run")  # skill caller must be experimenter/analyst (loop/operator bypass)
    conn = _conn(ctx)
    try:
        records.loop_guard(conn, "experiment.upsert", quest_id)  # optional Tier-B loop-context guard (skill caller)
    except records.RecordError as e:
        conn.close(); emit(envelope("experiment run", ok=False, quest_id=quest_id, diagnostics=[str(e)])); sys.exit(1)
    try:
        row = conn.execute("SELECT status, devices FROM gpu_allocation WHERE quest_id=?", (quest_id,)).fetchone()
    except Exception:
        row = None
    conn.close()
    confirmed = bool(row) and row[0] == "confirmed" and bool(row[1])
    devices = row[1] if confirmed else None
    # Fail closed: no confirmed allocation => never execute GPU-capable work.
    if not confirmed:
        emit(envelope("experiment run", ok=False, quest_id=quest_id,
                      diagnostics=[f"GPU use not operator-confirmed for quest {quest_id!r}: refusing to run. "
                                   f"An operator must `gpu confirm --quest-id {quest_id} --devices <list>` first."],
                      data={"experiment_id": experiment_id, "confirmed": False}))
        sys.exit(1)
    if not cmd:
        # No command to run: report the confirmed device set the Experimenter must restrict to.
        emit(envelope("experiment run", ok=True, quest_id=quest_id,
                      data={"stub": True, "experiment_id": experiment_id, "confirmed": True,
                            "devices": devices, "cuda_visible_devices": devices,
                            "note": "no --cmd given and no runner adapter enabled (knowledge_pack kind=runner). "
                                    "Run GPU work via --cmd (CUDA_VISIBLE_DEVICES is injected) or export "
                                    f"CUDA_VISIBLE_DEVICES={devices} for direct runs, then record via `record apply`."},
                      warnings=["experiment run is a domain-pluggable stub; --cmd enforces the device set"]))
        return
    # Execute the command with the confirmed device set injected (deterministic enforcement).
    env = {**os.environ, "CUDA_VISIBLE_DEVICES": devices}
    try:
        proc = subprocess.run(cmd, shell=True, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        emit(envelope("experiment run", ok=False, quest_id=quest_id,
                      diagnostics=[f"--cmd timed out after {timeout}s"],
                      data={"experiment_id": experiment_id, "devices": devices}))
        sys.exit(1)
    tail = lambda s: s if len(s) <= 8000 else s[-8000:]
    emit(envelope("experiment run", ok=(proc.returncode == 0), quest_id=quest_id,
                  data={"experiment_id": experiment_id, "confirmed": True, "devices": devices,
                        "cuda_visible_devices": devices, "returncode": proc.returncode,
                        "stdout": tail(proc.stdout), "stderr": tail(proc.stderr)},
                  diagnostics=([] if proc.returncode == 0 else [f"--cmd exited {proc.returncode}"])))
    if proc.returncode != 0:
        sys.exit(1)


def _provenance_waived():
    """Operator override: turn provenance enforcement off (advisory). Surfaced in gate status active_waivers."""
    return os.environ.get("DEEPRESEARCH_PROVENANCE_GATE") in ("0", "false", "no")


def _artifact_provenance_waived():
    """Operator override: waive the publication-rigor artifact-backed-provenance requirement. Visible in
    gate status active_waivers."""
    return os.environ.get("DEEPRESEARCH_ARTIFACT_PROVENANCE_GATE") in ("0", "false", "no")


def _is_hex(v):
    s = str(v)
    return len(s) >= 6 and all(c in "0123456789abcdefABCDEF" for c in s)


def _artifact_backed_ok(conn, quest_id, prov):
    """Second provenance layer: is an executed result's provenance backed by a RESOLVABLE artifact? Returns
    (ok, reasons). Requires metric_source + at least one log/config/output reference that resolves to an
    `artifact` row (or the result's own artifact) for the quest; any provided hash must be hex-shaped. Does
    NOT verify metric-file CONTENTS (re-execution territory)."""
    prov = prov or {}
    reasons = []
    ms = prov.get("metric_source")
    if not (str(ms).strip() if ms is not None else ""):
        reasons.append("artifact-backed provenance missing metric_source")
    refs = []
    for k in ("log_ref", "config_ref", "metric_source"):
        v = prov.get(k)
        if isinstance(v, str) and v.strip():
            refs.append(v.strip())
    oa = prov.get("output_artifacts") or []
    if isinstance(oa, list):
        refs += [str(x).strip() for x in oa if str(x).strip()]
    resolved = False
    for r in refs:
        try:
            hit = conn.execute("SELECT 1 FROM artifact WHERE quest_id=? AND (ref=? OR artifact_id=?)",
                               (quest_id, r, r)).fetchone()
        except sqlite3.OperationalError:
            hit = None
        if hit:
            resolved = True
            break
    if not resolved:
        reasons.append("artifact reference unresolved: no log/config/output reference resolves to an artifact row")
    for hk in ("config_hash", "checksum", "artifact_hash"):
        if prov.get(hk) and not _is_hex(prov.get(hk)):
            reasons.append(f"provenance.{hk} is not a valid hex checksum")
    return (not reasons), reasons


def _provenance_level(conn, quest_id, route, prov):
    """VALIDATOR-computed provenance strength. waived/imported/trusted map directly; an executed result is
    `artifact_backed` when its references resolve to artifacts (else `declared`). `reexecuted` is reserved
    (only via a trusted/manual route — re-execution is not auto-performed here)."""
    if route == "waived":
        return "waived"
    if route in ("imported", "trusted"):
        return "external_trusted"
    if route == "executed":
        ok_art, _ = _artifact_backed_ok(conn, quest_id, prov or {})
        return "artifact_backed" if ok_art else "declared"
    return "declared"


def _provenance_verdict(route, prov):
    """Validator for a result's reconstructable-run provenance. Returns (ok, reasons). `prov` is the parsed
    provenance manifest (dict). The author declares `route`; this decides whether it actually holds up.
      executed -> needs command + (code_revision|worktree) + a metric source + run_status (failed => failure_mode)
      imported/trusted -> needs a 'source' or 'note' citing the origin (legitimate non-execution route)
      waived -> needs a non-empty waiver_reason (provenance intentionally deferred, but EXPLICIT)
    """
    prov = prov or {}
    s = lambda k: (prov.get(k) or "").strip() if isinstance(prov.get(k), str) else prov.get(k)
    if not route:
        return False, ["no provenance_route declared (set executed|imported|trusted|waived on result.record)"]
    if route == "waived":
        return (bool(s("waiver_reason")),
                [] if s("waiver_reason") else ["provenance_route='waived' requires provenance.waiver_reason"])
    if route in ("imported", "trusted"):
        return (bool(s("source") or s("note")),
                [] if (s("source") or s("note")) else
                [f"provenance_route={route!r} requires provenance.source or provenance.note citing the origin"])
    # executed
    reasons = []
    if not s("command"):
        reasons.append("missing provenance.command")
    if not (s("code_revision") or s("worktree")):
        reasons.append("missing provenance.code_revision or provenance.worktree")
    if not (s("metric_source") or s("log_ref") or prov.get("output_artifacts")):
        reasons.append("missing metric source (provenance.metric_source / log_ref / output_artifacts)")
    status = s("run_status")
    if not status:
        reasons.append("missing provenance.run_status")
    elif status in ("failed", "error", "aborted") and not s("failure_mode"):
        reasons.append(f"run_status={status!r} (failure) requires provenance.failure_mode")
    return (not reasons), reasons


@cli.group()
def result(): ...


@result.command("validate")
@click.option("--result-id", required=True)
@click.option("--validity", default=None, type=click.Choice(["unchecked", "valid", "invalid", "incomparable"]),
              help="Explicit override (operator / domain validator adapter). Omit to compute the default gate.")
@click.pass_context
def result_validate(ctx, result_id, validity):
    """Default validity gate (domain-neutral). With --validity it honors the override; otherwise it COMPUTES
    validity from metric completeness + baseline comparability: no measurements -> invalid; no is_primary
    (objective) measurement -> incomparable; baseline_gate not passed/waived -> incomparable; else valid. A
    knowledge_pack(kind='validator') adapter can supersede this with a domain correctness gate. ALSO computes
    the validator-owned provenance_ok flag from the result's declared provenance_route + manifest (campaign
    coverage will not count this result's evidence unless provenance_ok=1, or an explicit route waives it)."""
    _authz_cmd("result validate")  # skill caller must be orchestrator (loop/operator bypass)
    conn = _conn(ctx)
    row = conn.execute("SELECT quest_id FROM result WHERE result_id=?", (result_id,)).fetchone()
    if row is None:
        conn.close(); emit(envelope("result validate", ok=False, diagnostics=[f"no result {result_id}"])); sys.exit(1)
    quest_id = row[0]
    reasons, computed = [], None
    if validity:
        computed = validity  # explicit override path (unchanged behavior for callers passing --validity)
    else:
        n_meas = conn.execute("SELECT COUNT(*) FROM measurement WHERE result_id=?", (result_id,)).fetchone()[0]
        n_prim = conn.execute("SELECT COUNT(*) FROM measurement WHERE result_id=? AND is_primary=1", (result_id,)).fetchone()[0]
        gate = conn.execute("SELECT baseline_gate FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
        gate = gate[0] if gate else None
        if n_meas == 0:
            computed = "invalid"; reasons.append("no measurements recorded for this result")
        elif n_prim == 0:
            computed = "incomparable"; reasons.append("no is_primary (objective) measurement — nothing to compare on")
        elif gate in ("pending", "blocked"):
            computed = "incomparable"; reasons.append(f"baseline_gate={gate!r} — no trustworthy comparator yet")
        else:
            computed = "valid"
    conn.execute("UPDATE result SET validity=? WHERE result_id=?", (computed, result_id))
    # Provenance: compute the validator-OWNED provenance_ok from the declared route + manifest, so
    # the author cannot self-certify it. Campaign coverage will not count this result's evidence unless ok=1.
    prow = conn.execute("SELECT provenance_route, provenance FROM result WHERE result_id=?", (result_id,)).fetchone()
    try:
        prov = json.loads(prow["provenance"]) if prow and prow["provenance"] else {}
    except Exception:
        prov = {}
    prov_route = prow["provenance_route"] if prow else None
    prov_ok, prov_reasons = _provenance_verdict(prov_route, prov)
    prov_level = _provenance_level(conn, quest_id, prov_route, prov) if prov_ok else "declared"
    _art_ok, art_reasons = _artifact_backed_ok(conn, quest_id, prov) if prov_route == "executed" else (True, [])
    conn.execute("UPDATE result SET provenance_ok=?, provenance_level=? WHERE result_id=?",
                 (1 if prov_ok else 0, prov_level, result_id))
    conn.commit()
    _finish(ctx, conn, "result validate",
            {"result_id": result_id, "validity": computed, "source": "override" if validity else "computed",
             "reasons": reasons, "provenance_ok": prov_ok, "provenance_route": prov_route,
             "provenance_level": prov_level, "artifact_backed_reasons": art_reasons,
             "provenance_reasons": prov_reasons, "quest_id": quest_id}, quest_id=quest_id)


_SCOPE_REQUIRED = ["objective", "research_question", "non_goals", "primary_metric", "metric_direction",
                   "dataset", "split", "eval_protocol", "false_progress_signals",
                   "baseline_route_expectation", "acceptance_criteria"]
# objective / primary_metric / metric_direction are the core target — never waivable.
_SCOPE_WAIVABLE = {"research_question", "non_goals", "dataset", "split", "eval_protocol",
                   "false_progress_signals", "baseline_route_expectation", "acceptance_criteria"}
_SCOPE_VAGUE = {"", "tbd", "todo", "n/a", "na", "?", "unknown", "tba", "later"}


def _scope_waived():
    """Operator override: skip the scope/eval-contract requirement (advisory). Surfaced in gate status."""
    return os.environ.get("DEEPRESEARCH_SCOPE_GATE") in ("0", "false", "no")


def _load_scope_contract(conn, quest_id):
    try:
        row = conn.execute("SELECT contract FROM scope_contract WHERE quest_id=? "
                           "ORDER BY created_at DESC, contract_id DESC LIMIT 1", (quest_id,)).fetchone()
    except sqlite3.OperationalError:
        return {}
    if not row or not row["contract"]:
        return {}
    try:
        return json.loads(row["contract"]) or {}
    except Exception:
        return {}


def _latest_scope_row(conn, quest_id):
    try:
        return conn.execute("SELECT contract_id, valid, validated_fingerprint FROM scope_contract WHERE quest_id=? "
                           "ORDER BY created_at DESC, contract_id DESC LIMIT 1", (quest_id,)).fetchone()
    except sqlite3.OperationalError:
        return None


def _scope_verdict(contract):
    """Validator for the typed scope/eval contract. Returns (ok, reasons). objective must be concrete (not
    vague/placeholder); each required field must be present, or — if waivable — listed in contract.waivers
    with a reason. objective/primary_metric/metric_direction are the core target and cannot be waived."""
    contract = contract or {}
    waivers = contract.get("waivers") or {}
    s = lambda k: (str(contract.get(k)).strip() if contract.get(k) is not None else "")
    reasons = []
    obj = s("objective")
    if (not obj) or obj.lower() in _SCOPE_VAGUE or len(obj) < 12:
        reasons.append("vague or missing objective (state a concrete research target)")
    for f in _SCOPE_REQUIRED:
        if f == "objective" or s(f):
            continue
        if f in _SCOPE_WAIVABLE and isinstance(waivers, dict) and str(waivers.get(f) or "").strip():
            continue  # intentionally deferred with a reason
        reasons.append(f"missing {f}" + (" (or waive it in contract.waivers with a reason)" if f in _SCOPE_WAIVABLE else ""))
    return (not reasons), reasons


@cli.group()
def scope(): ...


@scope.command("validate")
@click.option("--quest-id", required=True)
@click.pass_context
def scope_validate(ctx, quest_id):
    """Validator-owned scope/eval-contract gate. Computes whether the latest scope.contract is sufficiently
    specific (concrete objective; research question; non-goals; primary metric + direction; dataset/split/eval
    protocol; false-progress signals; baseline-route expectation; acceptance criteria — waivable fields may be
    deferred via contract.waivers{field: reason}) and writes the validator-owned `valid` flag + a freshness
    fingerprint. Idea selection requires a valid contract in bound mode; the author cannot self-certify.
    Exits non-zero (+reasons) on a gap."""
    _authz_cmd("scope validate")  # orchestrator (loop/operator bypass)
    conn = _conn(ctx)
    row = conn.execute("SELECT contract_id FROM scope_contract WHERE quest_id=? "
                       "ORDER BY created_at DESC, contract_id DESC LIMIT 1", (quest_id,)).fetchone()
    if row is None:
        conn.close()
        emit(envelope("scope validate", ok=False, quest_id=quest_id,
                      diagnostics=["no scope.contract recorded (record one first)"]))
        sys.exit(1)
    ok, reasons = _scope_verdict(_load_scope_contract(conn, quest_id))
    fp = records.dep_fingerprint(conn, quest_id, "scope") if ok else None
    conn.execute("UPDATE scope_contract SET valid=?, validated_fingerprint=? WHERE contract_id=?",
                 (1 if ok else 0, fp, row["contract_id"]))
    conn.commit(); conn.close()
    emit(envelope("scope validate", ok=ok, quest_id=quest_id,
                  data={"valid": ok, "contract_id": row["contract_id"], "reasons": reasons},
                  diagnostics=[] if ok else ["scope/eval contract gate FAILED: " + "; ".join(reasons)]))
    if not ok:
        sys.exit(1)


def _baseline_result_provenance(conn, evidence_ref):
    """A 'reproduced' baseline must cite a baseline result_id that carries validated provenance (validator flag)."""
    if not (evidence_ref or "").strip():
        return False, "reproduced baseline requires evidence_ref pointing to a baseline result_id"
    try:
        r = conn.execute("SELECT provenance_ok FROM result WHERE result_id=?", (evidence_ref,)).fetchone()
    except sqlite3.OperationalError:
        return False, "reproduced baseline result not resolvable (no result table)"
    if r is None:
        return False, f"reproduced baseline evidence_ref {evidence_ref!r} does not resolve to a result"
    if not r["provenance_ok"]:
        return False, f"reproduced baseline result {evidence_ref!r} lacks validated provenance (run `result validate`)"
    return True, ""


def _baseline_validity(conn, quest_id):
    """Compute whether the latest baseline.contract is acceptable. Returns (ok, reasons, route). Used by
    `baseline validate` (persists the `valid` flag) and by `gate status` (read-only, for live reasons)."""
    row = conn.execute(
        "SELECT contract_id, baseline_route, evidence_ref, verification_verdict, waiver_reason, baseline_id, "
        "baseline_name, comparison_policy, primary_metric_id, dataset, split, eval_protocol, contract_ref "
        "FROM baseline_contract WHERE quest_id=? ORDER BY created_at DESC, contract_id DESC LIMIT 1",
        (quest_id,)).fetchone()
    if row is None:
        return False, ["no baseline.contract recorded"], None
    route = (row["baseline_route"] or "").strip()
    verdict = row["verification_verdict"]
    s = lambda k: (row[k] or "").strip()
    reasons = []
    if route not in ("reproduced", "imported", "trusted", "waived"):
        reasons.append("no baseline_route declared (reproduced|imported|trusted|waived)")
    if route != "waived":  # eval-contract substance (skipped only for an explicit waiver)
        if not s("primary_metric_id"):
            reasons.append("missing primary_metric_id")
        if not s("comparison_policy"):
            reasons.append("missing comparison_policy (metric direction/threshold)")
        for f in ("dataset", "split", "eval_protocol"):
            if not s(f):
                reasons.append(f"missing {f} (specify it, or use a baseline waiver)")
        if not (s("baseline_id") or s("baseline_name") or s("contract_ref")):
            reasons.append("no expected-baseline reference / acceptance criteria (baseline_id|baseline_name|contract_ref)")
    if route == "waived":
        if verdict != "waived":
            reasons.append("baseline_route='waived' requires verification_verdict='waived'")
        if not s("waiver_reason"):
            reasons.append("waived baseline requires a non-empty waiver_reason")
    elif route in ("reproduced", "imported", "trusted"):
        if verdict not in _OK_BASELINE_V:
            reasons.append(f"verification_verdict={verdict!r} not acceptable for a {route} baseline "
                           f"(need one of {sorted(_OK_BASELINE_V)}, or waive)")
        if route == "reproduced":
            okp, why = _baseline_result_provenance(conn, row["evidence_ref"])
            if not okp:
                reasons.append(why)
        elif not s("evidence_ref"):
            reasons.append(f"{route} baseline requires evidence_ref citing the source (paper/repo/leaderboard)")
    return (not reasons), reasons, route


@cli.group()
def baseline(): ...


@baseline.command("validate")
@click.option("--quest-id", required=True)
@click.pass_context
def baseline_validate(ctx, quest_id):
    """Validator-owned baseline-contract gate. Computes whether the latest baseline.contract is acceptable
    (route declared; primary metric + comparison policy; dataset/split/eval protocol or waiver; expected-baseline
    reference; route-specific verification — reproduced -> provenance-backed result; imported/trusted ->
    source/citation; waived -> waiver reason) and writes the validator-owned `valid` flag. The baseline gate
    consumes `valid`; the author cannot pass on verification_verdict alone. Exits non-zero (+reasons) on a gap."""
    _authz_cmd("baseline validate")  # orchestrator (loop/operator bypass)
    conn = _conn(ctx)
    row = conn.execute("SELECT contract_id FROM baseline_contract WHERE quest_id=? "
                       "ORDER BY created_at DESC, contract_id DESC LIMIT 1", (quest_id,)).fetchone()
    if row is None:
        conn.close()
        emit(envelope("baseline validate", ok=False, quest_id=quest_id,
                      diagnostics=["no baseline.contract recorded (record one first)"]))
        sys.exit(1)
    ok, reasons, route = _baseline_validity(conn, quest_id)
    fp = records.dep_fingerprint(conn, quest_id, "baseline") if ok else None  # staleness signature
    conn.execute("UPDATE baseline_contract SET valid=?, validated_fingerprint=? WHERE contract_id=?",
                 (1 if ok else 0, fp, row["contract_id"]))
    conn.commit(); conn.close()
    emit(envelope("baseline validate", ok=ok, quest_id=quest_id,
                  data={"valid": ok, "baseline_route": route, "contract_id": row["contract_id"], "reasons": reasons},
                  diagnostics=[] if ok else ["baseline gate FAILED: " + "; ".join(reasons)]))
    if not ok:
        sys.exit(1)


@cli.group()
def metric(): ...


@metric.command("validate")
@click.option("--quest-id", default=None)
def metric_validate(quest_id):
    emit(envelope("metric validate", ok=True, quest_id=quest_id,
                  data={"stub": True, "note": "no metric_vocab pack enabled; any metric name accepted"}))


# ───────────────── render (domain-pluggable) ─────────────────
@cli.group()
def render(): ...


def _load_adapter(pack):
    """Import <pack ref>/adapter.py and return (module, entrypoint_name) or (None, None)."""
    import importlib.util
    import tomllib as _toml
    from paths import LOOP_DIR
    ref = pack["ref"]
    pack_dir = (LOOP_DIR / ref) if not str(ref).startswith("/") else __import__("pathlib").Path(ref)
    adapter_py = pack_dir / "adapter.py"
    if not adapter_py.exists():
        return None, None
    entry = "render"
    man = pack_dir / "pack.toml"
    if man.exists():
        ep = _toml.loads(man.read_text()).get("entrypoint", "adapter:render")
        entry = ep.split(":", 1)[1] if ":" in ep else ep
    spec = importlib.util.spec_from_file_location(f"deepresearch_pack_{pack['pack_id'].replace('-', '_')}", adapter_py)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, entry


def _resolve_for_command(conn, kind, quest_id, command):
    """Command-aware pack resolution: among enabled packs of `kind` for the quest's domain (→general),
    prefer those whose pack.toml `backs` includes `command`; pick the lowest priority. Falls back to any
    pack of that kind if none declare backing the command."""
    import tomllib as _toml
    from pathlib import Path
    from paths import LOOP_DIR
    dom = None
    if quest_id:
        r = conn.execute("SELECT domain FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
        dom = r[0] if r else None
    doms = [d for d in (dom, "general") if d]
    if doms:
        rows = conn.execute(f"SELECT pack_id,domain,ref,priority FROM knowledge_pack WHERE enabled=1 "
                            f"AND kind=? AND domain IN ({','.join('?'*len(doms))}) ORDER BY priority",
                            [kind] + doms).fetchall()
    else:
        rows = conn.execute("SELECT pack_id,domain,ref,priority FROM knowledge_pack WHERE enabled=1 "
                            "AND kind=? ORDER BY priority", [kind]).fetchall()
    rows = [dict(r) for r in rows]

    def backs(ref):
        rd = (LOOP_DIR / ref) if not str(ref).startswith("/") else Path(ref)
        man = rd / "pack.toml"
        return set(_toml.loads(man.read_text()).get("backs", [])) if man.exists() else set()

    # Strict command-aware resolution: a pack serves ONLY commands its pack.toml `backs` declares.
    # (No loose fall-through to an unrelated pack of the same kind — e.g. the render-report compiler must
    # not hijack render-figure. A command with no backing pack returns None → generic stub.)
    backing = [r for r in rows if command in backs(r["ref"])]
    return backing[0] if backing else None


def _run_adapter(ctx, cmd, *, adapter_kind, entry_default, quest_id, artifact_id, ref, input_path,
                 params, artifact_kind, at):
    """Resolve the enabled pack that backs `cmd`, load its adapter, call its entrypoint to write `ref`,
    then record an artifact via the normal state path. Generic stub when no pack is enabled."""
    from paths import LOOP_DIR
    from pathlib import Path as _Path
    conn = _conn(ctx)
    pack = _resolve_for_command(conn, adapter_kind, quest_id, cmd)
    out_abs = ref if ref.startswith("/") else str(LOOP_DIR / ref)
    # Resolve --input loop-relative too (consistent with --ref), so a loop-relative path works regardless of
    # the agent's CWD (agents run from their per-role work root, not the loop dir).
    if input_path and not input_path.startswith("/"):
        cand = str(LOOP_DIR / input_path)
        if _Path(cand).exists():
            input_path = cand
    used, meta, err = False, None, None
    if pack:
        try:
            mod, entry = _load_adapter(pack)
            entry = entry or entry_default
            fn = getattr(mod, entry, None) if mod else None
            if fn:
                meta = fn(command=cmd, input_path=input_path, out_path=out_abs, params=params, quest_id=quest_id)
                used = True
        except Exception as e:
            err = f"adapter '{pack['pack_id']}' failed: {e}"
    if err:
        conn.close(); emit(envelope(cmd, ok=False, diagnostics=[err], quest_id=quest_id)); sys.exit(1)
    try:
        data = records.apply(conn, {"record_type": "artifact.record", "record_id": artifact_id, "at": at,
                                    "quest_id": quest_id, "kind": artifact_kind, "ref": ref})
    except records.RecordError as e:
        conn.close(); emit(envelope(cmd, ok=False, diagnostics=[str(e)], quest_id=quest_id)); sys.exit(1)
    note = (f"adapter '{pack['pack_id']}' produced {ref}" if used
            else f"no enabled {adapter_kind} pack; generic stub (artifact recorded, nothing produced)")
    _finish(ctx, conn, cmd, {"stub": not used, "adapter": pack, "produced": used,
                             "out_path": out_abs if used else None, "result": meta, "artifact": data,
                             "note": note}, quest_id=quest_id)


def _opts(f):
    for o in (click.option("--quest-id", required=True), click.option("--artifact-id", required=True),
              click.option("--ref", required=True, help="Output path the adapter writes."),
              click.option("--input", "input_path", default=None, help="Input data/text file for the adapter."),
              click.option("--title", default=None), click.option("--at", required=True)):
        f = o(f)
    return f


# ── DeepScientist venue-template policy ───────────────────────────────────────────────────────────────
# A paper is drafted inside a REAL venue template by default; the generic pandoc `article` is an EXPLICIT
# opt-out only (`--venue generic`). Selection precedence:
#   explicit --venue  >  paper_spine.venue_style  >  quest.domain  >  iclr2026 (general ML/AI default).
# Inference maps to venues that actually compile in this toolchain. Systems papers prefer a systems venue
# (ASPLOS is the ideal architecture-performance venue but its acmart class may be absent — the closest
# RENDERABLE systems template, the USENIX OSDI/NSDI suite, is chosen then).
_RENDERABLE_VENUES = {"iclr2026", "neurips2025", "osdi2026", "nsdi2027"}


def _infer_venue(text):
    """Map a free-text domain / paper_spine venue-style hint to a venue template. Returns (venue, why)."""
    t = (text or "").lower()
    for tok, v in (("iclr", "iclr2026"), ("neurips", "neurips2025"), ("nips", "neurips2025"),
                   ("osdi", "osdi2026"), ("nsdi", "nsdi2027"), ("usenix", "osdi2026"),
                   ("asplos", "osdi2026"), ("sosp", "osdi2026"), ("isca", "osdi2026"), ("micro", "osdi2026"),
                   ("ispass", "osdi2026"), ("mlsys", "osdi2026"), ("hpca", "osdi2026"),
                   ("icml", "iclr2026"), ("colm", "iclr2026"), ("acl", "iclr2026"), ("aaai", "iclr2026")):
        if tok in t:
            return v, "venue token '%s' in hint" % tok
    net_kw = ("network", "rdma", "congestion", "datacenter network", "packet", "sdn", "switch fabric")
    sys_kw = ("system", "architecture", "cuda", "gpu", "kernel", "blackwell", "hopper", "microarch",
              "hardware", "accelerator", "latency", "throughput", "performance model", "perf model",
              "compiler", "runtime", "operating system", "scheduler", "cache", "interconnect",
              "memory system", "tensor core", "cuda core", "fpga", "asic")
    if any(k in t for k in net_kw):
        return "nsdi2027", "networking-systems keywords"
    if any(k in t for k in sys_kw):
        return "osdi2026", "systems/architecture keywords (ASPLOS ideal but needs acmart; OSDI is the closest renderable systems venue)"
    return "iclr2026", "general ML/AI default"


def _resolve_report_venue(ctx, quest_id, explicit):
    """Apply the venue precedence. Returns (venue_or_'generic', rationale)."""
    if explicit:
        if explicit.lower() == "generic":
            return "generic", "explicit --venue generic (operator opted out of a venue template)"
        return explicit, "explicit --venue %s" % explicit
    spine_style = domain = None
    try:
        conn = _conn(ctx)
        r = conn.execute("SELECT venue_style FROM paper_spine WHERE quest_id=?", (quest_id,)).fetchone()
        spine_style = r[0] if r else None
        d = conn.execute("SELECT domain FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
        domain = d[0] if d else None
        conn.close()
    except Exception:
        pass
    if spine_style:
        v, why = _infer_venue(spine_style)
        return v, "inferred from paper_spine.venue_style (%s)" % why
    if domain and domain != "general":
        v, why = _infer_venue(domain)
        return v, "inferred from quest.domain '%s' (%s)" % (domain, why)
    return "iclr2026", "default: general ML/AI, no stronger venue signal"


@render.command("report")
@_opts
@click.option("--bib", default=None, help="Path to a .bib (enables a real BibTeX pass via the compiler adapter).")
@click.option("--venue", default=None,
              help="Venue template (e.g. iclr2026, osdi2026; see paper-latex/templates/). DEFAULT POLICY: a real "
                   "venue is auto-selected (explicit > paper_spine > domain > iclr2026); pass '--venue generic' "
                   "to deliberately emit a plain pandoc article.")
@click.pass_context
def render_report(ctx, quest_id, artifact_id, ref, input_path, title, at, bib, venue):
    params = {"title": title}
    if bib:
        params["bib"] = bib if bib.startswith("/") else str(LOOP_DIR / bib)
    resolved, rationale = _resolve_report_venue(ctx, quest_id, venue)
    params["venue"] = resolved
    params["venue_rationale"] = rationale
    _run_adapter(ctx, "render report", adapter_kind="compiler", entry_default="render", quest_id=quest_id,
                 artifact_id=artifact_id, ref=ref, input_path=input_path, params=params,
                 artifact_kind="report", at=at)


@render.command("figure")
@_opts
@click.pass_context
def render_figure(ctx, quest_id, artifact_id, ref, input_path, title, at):
    _run_adapter(ctx, "render figure", adapter_kind="compiler", entry_default="render", quest_id=quest_id,
                 artifact_id=artifact_id, ref=ref, input_path=input_path, params={"title": title},
                 artifact_kind="figure", at=at)


@render.command("plot")
@_opts
@click.option("--kind", default=None, type=click.Choice(["line", "scatter", "bar"]),
              help="Chart type for the compiler adapter (paper-plot). Default: line.")
@click.option("--y-label", "y_label", default=None)
@click.pass_context
def render_plot(ctx, quest_id, artifact_id, ref, input_path, title, at, kind, y_label):
    """Publication-quality plot; consumes the enabled compiler adapter (paper-plot → matplotlib vector PDF
    when --ref ends in .pdf, so the figure embeds cleanly in the manuscript)."""
    params = {"title": title}
    if kind:
        params["kind"] = kind
    if y_label:
        params["y_label"] = y_label
    _run_adapter(ctx, "render plot", adapter_kind="compiler", entry_default="render", quest_id=quest_id,
                 artifact_id=artifact_id, ref=ref, input_path=input_path, params=params,
                 artifact_kind="figure", at=at)


@render.command("polish")
@_opts
@click.pass_context
def render_polish(ctx, quest_id, artifact_id, ref, input_path, title, at):
    _run_adapter(ctx, "render polish", adapter_kind="compiler", entry_default="render", quest_id=quest_id,
                 artifact_id=artifact_id, ref=ref, input_path=input_path, params={"title": title},
                 artifact_kind="figure", at=at)


@render.command("slides")
@_opts
@click.pass_context
def render_slides(ctx, quest_id, artifact_id, ref, input_path, title, at):
    _run_adapter(ctx, "render slides", adapter_kind="compiler", entry_default="render", quest_id=quest_id,
                 artifact_id=artifact_id, ref=ref, input_path=input_path, params={"title": title},
                 artifact_kind="bundle", at=at)


# ───────────────── manuscript / outline validators (core, stub-safe) ─────────────────
@cli.group()
def outline(): ...


def _read_artifact_text(artifact_ref):
    """Resolve a loop-relative (or absolute) artifact path and return its text, or None if unreadable."""
    if not artifact_ref:
        return None
    from pathlib import Path as _P
    p = _P(artifact_ref) if str(artifact_ref).startswith("/") else (LOOP_DIR / artifact_ref)
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None


# Legacy advisory token markers — used ONLY when no typed paper-spine is available. The finalize coverage
# gate depends on the STRUCTURAL spine validation below, never on this token grep.
_OUTLINE_CHECKS = {
    "paper_idea":          ("central_thesis", "working_title", "paper idea", "story_spine", "thesis"),
    "scoped_claims":       ("core_claims", "scoped claim", "scope", "claim"),
    "method_abstraction":  ("method_abstraction", "method abstraction", "mechanism_steps", "intuition"),
    "evaluation_plan":     ("evaluation_plan", "evaluation plan", "analysis_plan", "baselines", "evaluation/analysis"),
    "evidence_boundaries": ("evidence_grounding", "must_not_claim", "evidence boundaries", "evidence_view", "evidence-view"),
}

# Typed paper-spine CONTENT schema (the rich spine in runs/<q>/paper/spine.json; the thin paper_spine DB row
# points at it). Enforced by `outline validate` (structural) and `manuscript coverage` (readiness). This is
# what makes the spine a typed contract, not a free-text artifact.
_SPINE_CONTENT_SCHEMA = {
    "type": "object",
    "required": ["thesis", "core_contribution", "main_claims", "not_claiming",
                 "experiment_section_map", "display_plan", "reviewer_objections"],
    "properties": {
        "thesis": {"type": "string", "minLength": 1},
        "core_contribution": {"type": "string", "minLength": 1},
        "venue_style": {"type": "string"},
        "central_mechanism": {"type": "string"},
        "main_claims": {
            "type": "array", "minItems": 1, "maxItems": 3,
            "items": {"type": "object",
                      "required": ["claim_id", "scope", "what_would_falsify_it", "evidence_needed"],
                      "properties": {"claim_id": {"type": "string", "minLength": 1},
                                     "scope": {"type": "string", "minLength": 1},
                                     "what_would_falsify_it": {"type": "string", "minLength": 1},
                                     "evidence_needed": {"type": "array", "minItems": 1}}}},
        "not_claiming": {"type": "array", "minItems": 1, "items": {"type": "string"}},
        "claim_evidence_map": {"type": "object"},
        "experiment_section_map": {
            "type": "array", "minItems": 1,
            "items": {"type": "object", "required": ["section", "thesis"],
                      "properties": {"section": {"type": "string"}, "thesis": {"type": "string", "minLength": 1}}}},
        "display_plan": {
            "type": "array", "minItems": 1,
            "items": {"type": "object", "required": ["display", "claims"],
                      "properties": {"display": {"type": "string"}, "claims": {"type": "array", "minItems": 1}}}},
        "reviewer_objections": {
            "type": "array", "minItems": 1,
            "items": {"type": "object", "required": ["objection"],
                      "anyOf": [{"required": ["answer_route"]}, {"required": ["linked_claims"]},
                                {"required": ["needed_evidence"]}]}},
        "weak_points": {"type": "array"},
        "followups": {"type": "array"}
    }
}


def _spine_structural_reasons(spine):
    """Structural validity reasons for a typed paper-spine ([] = valid). Shared by `outline validate` and
    `gate status` so the structural contract is defined once."""
    reasons = []
    try:
        jsonschema.validate(spine, _SPINE_CONTENT_SCHEMA)
    except jsonschema.ValidationError as e:
        reasons.append(f"spine schema: {e.message}")
    mc = spine.get("main_claims") or []
    if not (1 <= len(mc) <= 3):
        reasons.append(f"main_claims must be 1-3 (got {len(mc)})")
    for c in mc:
        if not (c.get("what_would_falsify_it") or "").strip():
            reasons.append(f"claim {c.get('claim_id')!r} is not falsifiable (no what_would_falsify_it)")
        if not c.get("evidence_needed"):
            reasons.append(f"claim {c.get('claim_id')!r} has no evidence_needed")
    if not spine.get("not_claiming"):
        reasons.append("not_claiming boundary is empty")
    for o in (spine.get("reviewer_objections") or []):
        if not (o.get("answer_route") or o.get("linked_claims") or o.get("needed_evidence")):
            reasons.append(f"reviewer objection {str(o.get('objection',''))[:40]!r} not mapped to evidence/follow-up")
    for s in (spine.get("experiment_section_map") or []):
        if not (s.get("thesis") or "").strip():
            reasons.append(f"section {s.get('section','?')!r} has no thesis")
    if not spine.get("display_plan"):
        reasons.append("display_plan is empty")
    return reasons


def _load_spine(ctx, quest_id, spine_ref):
    """Resolve the typed spine JSON from --spine-ref or the quest's paper_spine row; None if missing/unparseable."""
    ref = spine_ref
    if not ref and quest_id:
        try:
            conn = _conn(ctx)
            row = conn.execute("SELECT spine_ref FROM paper_spine WHERE quest_id=?", (quest_id,)).fetchone()
            conn.close()
            ref = row[0] if row else None
        except Exception:
            ref = None
    txt = _read_artifact_text(ref)
    if txt is None:
        return None
    try:
        return json.loads(txt)
    except Exception:
        return None


@outline.command("validate")
@click.option("--quest-id", default=None)
@click.option("--spine-ref", default=None, help="Path to the typed paper-spine JSON (else read from the paper_spine row).")
@click.option("--artifact-ref", default=None, help="LEGACY markdown outline for the advisory token scan only.")
@click.pass_context
def outline_validate(ctx, quest_id, spine_ref, artifact_ref):
    """Structural pre-write gate. With a typed paper-spine (--spine-ref, or the quest's paper_spine row) it
    validates: exactly one thesis; 1-3 falsifiable main_claims (each with what_would_falsify_it + evidence_needed);
    a non-empty not_claiming boundary; reviewer_objections each mapped to evidence or follow-up; a section thesis
    per experiment-section; and a display plan connected to claims — FAILING on any miss. The legacy
    --artifact-ref markdown token scan is only an advisory fallback and does NOT gate finalize."""
    spine = _load_spine(ctx, quest_id, spine_ref)
    if spine is None:
        text = _read_artifact_text(artifact_ref)
        if text is None:
            emit(envelope("outline validate", ok=True, quest_id=quest_id,
                          data={"mode": "advisory", "checks": list(_OUTLINE_CHECKS),
                                "note": "no typed paper-spine found; pass --spine-ref or record paper_spine.upsert "
                                        "to enforce the structural contract"}))
            return
        low = text.lower()
        results = {name: any(tok in low for tok in toks) for name, toks in _OUTLINE_CHECKS.items()}
        missing = [n for n, ok in results.items() if not ok]
        ok = not missing
        emit(envelope("outline validate", ok=ok, quest_id=quest_id,
                      data={"mode": "advisory-legacy-token-scan", "checks": results, "missing": missing},
                      diagnostics=[] if ok else [f"(advisory) outline missing tokens: {missing}"]))
        if not ok:
            sys.exit(1)
        return
    reasons = _spine_structural_reasons(spine)
    mc = spine.get("main_claims") or []
    ok = not reasons
    emit(envelope("outline validate", ok=ok, quest_id=quest_id,
                  data={"mode": "structural", "thesis": spine.get("thesis"), "n_core_claims": len(mc),
                        "reasons": reasons},
                  diagnostics=[] if ok else ["outline not structurally valid: " + "; ".join(reasons)]))
    if not ok:
        sys.exit(1)


# ───────────────── idea selection (idea selection as a binding, handoff-blocking gate) ─────────────────
@cli.group()
def idea(): ...


# Configurable rigor floors (introduces [gate_floors]). Precedence: seed.toml [gate_floors.<rigor>] overrides
# these defaults; env DEEPRESEARCH_IDEA_SLATE_MIN / DEEPRESEARCH_IDEA_SCORE_MIN override per-run (and waive).
_DEFAULT_FLOORS = {
    "scoping":     {"idea_slate_min": 0, "idea_score_min": 0,
                    "campaign_required": [], "campaign_baseline": False, "campaign_anyof": [],
                    "campaign_significance_superiority": False},
    "standard":    {"idea_slate_min": 3, "idea_score_min": 6,
                    "campaign_required": ["main_result"], "campaign_baseline": True,
                    "campaign_anyof": ["ablation", "robustness", "negative", "boundary", "error_analysis"],
                    "campaign_significance_superiority": False},
    "publication": {"idea_slate_min": 5, "idea_score_min": 7,
                    "campaign_required": ["main_result", "ablation"], "campaign_baseline": True,
                    "campaign_anyof": ["robustness", "negative", "boundary", "error_analysis"],
                    "campaign_significance_superiority": True},
    "strict":      {"idea_slate_min": 6, "idea_score_min": 8,
                    "campaign_required": ["main_result", "ablation", "robustness"], "campaign_baseline": True,
                    "campaign_anyof": ["negative", "boundary", "error_analysis"],
                    "campaign_significance_superiority": True},
}
_IDEA_SCORE_KEYS = ["novelty", "falsifiability", "feasibility", "evidence_potential", "fit_to_objective"]
_IDEA_CONTENT_SCHEMA = {
    "type": "object",
    "required": ["objective_contract_ref", "baseline_contract_ref", "raw_slate", "challenge",
                 "novelty_risk", "selection_gate", "rejected", "retained"],
    "properties": {
        "objective_contract_ref": {"type": "string", "minLength": 1},
        "baseline_contract_ref": {"type": "string", "minLength": 1},
        "raw_slate": {"type": "array", "minItems": 1, "items": {
            "type": "object", "required": ["candidate_id", "title", "hypothesis", "mechanism",
                                           "expected_evidence", "risk"],
            "properties": {"candidate_id": {"type": "string", "minLength": 1}, "title": {"type": "string"},
                           "hypothesis": {"type": "string", "minLength": 1},
                           "mechanism": {"type": "string", "minLength": 1},
                           "expected_evidence": {}, "risk": {"type": "string"}}}},
        "challenge": {"type": "object",
                      "required": ["strongest_rejection", "outside_family_alternative", "why_retained_survives"],
                      "properties": {"strongest_rejection": {"type": "string", "minLength": 1},
                                     "outside_family_alternative": {"type": "string", "minLength": 1},
                                     "why_retained_survives": {"type": "string", "minLength": 1}}},
        "novelty_risk": {"type": "object", "required": ["novelty_label", "novelty_argument", "risk_notes"],
                         "properties": {"novelty_label": {"enum": ["novel", "incremental_valuable",
                                                                   "not_differentiated"]},
                                        "novelty_argument": {"type": "string", "minLength": 1},
                                        "risk_notes": {"type": "string"},
                                        "known_near_neighbors": {"type": "array"}}},
        "selection_gate": {"type": "array", "minItems": 1, "items": {
            "type": "object", "required": ["candidate_id", "scores", "total", "verdict"],
            "properties": {"candidate_id": {"type": "string"},
                           "scores": {"type": "object", "required": _IDEA_SCORE_KEYS,
                                      "properties": {k: {"type": "integer", "minimum": 0, "maximum": 2}
                                                     for k in _IDEA_SCORE_KEYS}},
                           "total": {"type": "integer"}, "verdict": {"type": "string"}}}},
        "rejected": {"type": "array", "minItems": 1, "items": {
            "type": "object", "required": ["candidate_id", "reason"],
            "properties": {"candidate_id": {"type": "string"}, "reason": {"type": "string", "minLength": 1},
                           "what_would_make_viable": {"type": "string"}}}},
        "retained": {"type": "object",
                     "required": ["candidate_id", "hypothesis", "mechanism", "claim_candidate",
                                  "mvp_experiment_plan", "expected_failure_mode", "boundary_condition"],
                     "properties": {"candidate_id": {"type": "string", "minLength": 1},
                                    "hypothesis": {"type": "string", "minLength": 1},
                                    "mechanism": {"type": "string", "minLength": 1},
                                    "claim_candidate": {"type": "string"},
                                    "mvp_experiment_plan": {"type": "string", "minLength": 1},
                                    "expected_failure_mode": {"type": "string"},
                                    "boundary_condition": {"type": "string"}}},
        "experiment_plan_ref": {"type": "string"},
        "novelty_waiver": {"type": "string"},
        "prior_comparison": {"type": "object",
                             "description": "closest_prior_refs[] (resolve to reference rows) + prior_did, "
                                            "proposed_difference, why_prior_insufficient, distinguishing_experiment, "
                                            "novelty_type (mechanistic|empirical|dataset_task|efficiency|negative_result)"},
        "attempt_signature": {"type": "object",
                              "description": "OPTIONAL coarse signature (idea_key/method_key/dataset/metric/"
                                             "parameter_key/baseline_id/condition/route/notes) for ADVISORY "
                                             "quest-local repeated-failure detection. Never affects idea_select.valid."}
    }
}


def _gate_floors(rigor):
    rigor = rigor or "standard"
    floors = dict(_DEFAULT_FLOORS.get(rigor, _DEFAULT_FLOORS["standard"]))
    try:
        import tomllib
        from paths import SEED_TOML
        gf = (tomllib.load(open(SEED_TOML, "rb")).get("gate_floors", {}) or {}).get(rigor, {})
        for k, v in gf.items():
            if k in floors:
                floors[k] = v  # seed overrides defaults (ints, bools, and list subsets)
    except Exception:
        pass
    for k, env in (("idea_slate_min", "DEEPRESEARCH_IDEA_SLATE_MIN"),
                   ("idea_score_min", "DEEPRESEARCH_IDEA_SCORE_MIN")):
        if os.environ.get(env) is not None:
            try:
                floors[k] = int(os.environ[env])
            except ValueError:
                pass
    return floors


def _latest_idea_select_row(conn, quest_id):
    return conn.execute(
        "SELECT select_id, select_ref, valid, created_at FROM idea_select WHERE quest_id=? "
        "ORDER BY created_at DESC, select_id DESC LIMIT 1", (quest_id,)).fetchone()


def _idea_row_id(quest_id, candidate_id):
    """Deterministic idea_id for a slate candidate so re-validation upserts the same row (and binding can
    recover the candidate_id by splitting on the ':idea:' marker)."""
    return f"{quest_id}:idea:{candidate_id}"


def _idea_candidate_id(idea_id):
    """Recover a slate candidate_id (e.g. 'C1') from an idea_id minted by _idea_row_id."""
    marker = ":idea:"
    return idea_id.split(marker, 1)[1] if marker in idea_id else idea_id


def _materialize_idea_rows(conn, quest_id, content, gate_by_id, floors, retained_id, select_ref, at):
    """Persist each idea-slate candidate as an ENUMERABLE idea row (so the slate is no longer collapsed inside
    idea_select JSON). Hard-gate ELIGIBILITY = selection_gate total >= the rigor idea_score_min floor: eligible
    candidates land as status='proposed' (BO will choose among them); below-floor candidates land as
    status='rejected' and are EXCLUDED from acquisition (BO cannot select gate-invalid candidates). The scout's
    retained/reject verdicts stay advisory; the FINAL pick is bound from the BO decision. Idempotent (upsert by
    deterministic idea_id). QUEST-LOCAL only. Returns the count of eligible candidates."""
    floor = floors.get("idea_score_min", 0)
    n_eligible = 0
    for cand in content.get("raw_slate", []):
        cid = cand.get("candidate_id")
        if not cid:
            continue
        total = gate_by_id.get(cid)
        eligible = (total is not None and total >= floor)
        if eligible:
            n_eligible += 1
        status = "proposed" if eligible else "rejected"
        iid = _idea_row_id(quest_id, cid)
        stmt = (cand.get("hypothesis") or cand.get("title") or cid)[:1000]
        conn.execute(
            "INSERT INTO idea(idea_id,quest_id,branch_id,parent_idea_id,round_index,statement,route,artifact_ref,"
            "status,created_at,updated_at) VALUES(?,?,NULL,NULL,NULL,?,?,?,?,?,?) "
            "ON CONFLICT(idea_id) DO UPDATE SET statement=excluded.statement, route=excluded.route, "
            "artifact_ref=excluded.artifact_ref, status=excluded.status, updated_at=excluded.updated_at",
            (iid, quest_id, stmt, cand.get("title"), select_ref, status, at, at))
    return n_eligible


_NOVELTY_TYPES = {"mechanistic", "empirical", "dataset_task", "efficiency", "negative_result"}


def _novelty_grounding(conn, quest_id, content, rigor, bound):
    """Validator-owned novelty grounding. Returns (ok, reasons). Waivable (novelty_waiver /
    DEEPRESEARCH_IDEA_NOVELTY_WAIVER). Always: reject `not_differentiated`; a `novel` idea must NAME its closest
    prior (known_near_neighbors). BOUND escalation for a `novel` idea (or any non-decorative idea at
    publication rigor): a structured `prior_comparison` whose `closest_prior_refs` resolve to durable
    `reference` rows (publication needs >= 2) + prior_did / proposed_difference / why_prior_insufficient /
    distinguishing_experiment + a typed novelty_type. Decorative free-text novelty does not pass alone."""
    content = content or {}
    nr = content.get("novelty_risk", {}) or {}
    novelty = nr.get("novelty_label")
    if content.get("novelty_waiver") or os.environ.get("DEEPRESEARCH_IDEA_NOVELTY_WAIVER"):
        return True, []  # explicit, reasoned waiver (surfaced in gate status)
    reasons = []
    if novelty == "not_differentiated":
        return False, ["novelty_label='not_differentiated' (decorative tweak): add real differentiation "
                       "or an explicit novelty_waiver"]
    if novelty == "novel" and not (nr.get("known_near_neighbors") or []):
        reasons.append("novelty_label='novel' but known_near_neighbors is empty: name the closest prior work")
    pub = records._rigor_order(rigor) >= records._rigor_order("publication")
    if bound and (novelty == "novel" or pub):
        pc = content.get("prior_comparison") or {}
        refs = pc.get("closest_prior_refs") or []
        if not refs:
            reasons.append("novel idea missing closest-prior reference (prior_comparison.closest_prior_refs)")
        resolved = []
        for rid in refs:
            try:
                hit = conn.execute("SELECT 1 FROM reference WHERE reference_id=? AND quest_id=?",
                                   (str(rid), quest_id)).fetchone()
            except sqlite3.OperationalError:
                hit = None
            if hit:
                resolved.append(rid)
            else:
                reasons.append(f"closest-prior reference {rid!r} unresolved (no durable reference row)")
        for f in ("prior_did", "proposed_difference", "why_prior_insufficient", "distinguishing_experiment"):
            if not str(pc.get(f) or "").strip():
                reasons.append(f"prior comparison missing {f}")
        if str(pc.get("novelty_type") or "").strip() not in _NOVELTY_TYPES:
            reasons.append(f"prior_comparison.novelty_type must be one of {sorted(_NOVELTY_TYPES)}")
        if pub and len(resolved) < 2:
            reasons.append("publication rigor requires >= 2 resolvable closest-prior references (or a novelty_waiver)")
    return (not reasons), reasons


@idea.command("validate")
@click.option("--quest-id", required=True)
@click.option("--select-ref", default=None, help="Typed idea-select.json (else the latest idea_select row's ref).")
@click.pass_context
def idea_validate(ctx, quest_id, select_ref):
    """Validate the latest idea selection against the typed schema + selection-pressure rules under the quest's
    rigor floor. REJECTS: single-proposal / below-floor slate; missing strongest_rejection or
    outside_family_alternative; no rejected (or rejections without reasons); retained score below floor;
    novelty_label='not_differentiated' (without a waiver); retained with no mechanism / no MVP plan; retained
    not in the raw slate; selection scores that don't sum. Writes valid + gate_score onto the idea_select row
    (the worker cannot self-certify). Exits non-zero on failure. The experiment-handoff idea gate reads valid."""
    conn = _conn(ctx)
    row = _latest_idea_select_row(conn, quest_id)
    if row is None:
        conn.close()
        emit(envelope("idea validate", ok=False, quest_id=quest_id,
                      diagnostics=["no idea.select recorded (record one first)"]))
        sys.exit(1)
    qr = conn.execute("SELECT rigor_level FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    rigor = (qr[0] if qr else None) or "standard"
    floors = _gate_floors(rigor)
    ref = select_ref or row["select_ref"]
    txt = _read_artifact_text(ref)
    reasons, content = [], None
    if txt is None:
        reasons.append(f"idea-select artifact not readable at {ref}")
    else:
        try:
            content = json.loads(txt)
            jsonschema.validate(content, _IDEA_CONTENT_SCHEMA)
        except jsonschema.ValidationError as e:
            reasons.append(f"idea-select schema: {e.message}"); content = None
        except Exception as e:
            reasons.append(f"idea-select not parseable: {e}"); content = None
    score = retained_id = novelty = None
    if content is not None:
        slate = content.get("raw_slate", [])
        slate_ids = {c.get("candidate_id") for c in slate}
        retained_id = content.get("retained", {}).get("candidate_id")
        novelty = content.get("novelty_risk", {}).get("novelty_label")
        if len(slate) < floors["idea_slate_min"]:
            reasons.append(f"raw_slate has {len(slate)} candidate(s); rigor '{rigor}' requires "
                           f">= {floors['idea_slate_min']} (single-proposal / below-floor)")
        if retained_id not in slate_ids:
            reasons.append(f"retained candidate {retained_id!r} is not present in raw_slate")
        gate_by_id = {}
        for g in content.get("selection_gate", []):
            sc = g.get("scores", {})
            summed = sum(int(sc.get(k, 0)) for k in _IDEA_SCORE_KEYS)
            if g.get("total") != summed:
                reasons.append(f"selection_gate total for {g.get('candidate_id')!r} ({g.get('total')}) "
                               f"!= sum of its scores ({summed})")
            gate_by_id[g.get("candidate_id")] = g.get("total")
        if retained_id not in gate_by_id:
            reasons.append(f"retained candidate {retained_id!r} has no selection_gate entry")
        else:
            score = gate_by_id[retained_id]
            if score is not None and score < floors["idea_score_min"]:
                reasons.append(f"retained score {score} < rigor '{rigor}' floor {floors['idea_score_min']}")
        n_ok, n_reasons = _novelty_grounding(conn, quest_id, content, rigor, _is_bound(conn, quest_id, rigor))
        reasons += n_reasons
    # Upstream scope/eval contract: in bound mode, idea selection must proceed from a validator-confirmed,
    # non-stale scope.contract (waivable with DEEPRESEARCH_SCOPE_GATE=0).
    if _is_bound(conn, quest_id, rigor) and not _scope_waived():
        sc = _latest_scope_row(conn, quest_id)
        if sc is None or not sc["valid"]:
            reasons.append("no validator-confirmed scope/eval contract — record a `scope.contract` (objective + "
                           "evaluation plan) and run `scope validate` before promoting an idea")
        elif records.is_stale(conn, quest_id, "scope", sc["validated_fingerprint"]):
            reasons.append("scope/eval contract is STALE (changed after `scope validate`) — re-run `scope validate`")
    valid = not reasons
    conn.execute("UPDATE idea_select SET valid=?, gate_score=?, retained_candidate=?, novelty_label=? "
                 "WHERE select_id=?", (1 if valid else 0, score, retained_id, novelty, row["select_id"]))
    # Persist the slate as ENUMERABLE, gate-eligibility-tagged idea rows (the BO candidate slate). Done even on a
    # failed validation so the rows self-heal on re-validate; idempotent upsert keyed by deterministic idea_id.
    n_eligible = None
    if content is not None:
        n_eligible = _materialize_idea_rows(conn, quest_id, content, gate_by_id, floors, retained_id,
                                            ref, row["created_at"])
    conn.commit(); conn.close()
    emit(envelope("idea validate", ok=valid, quest_id=quest_id,
                  data={"valid": valid, "rigor": rigor, "floors": floors, "retained": retained_id,
                        "gate_score": score, "novelty_label": novelty, "reasons": reasons,
                        "eligible_candidates": n_eligible},
                  diagnostics=[] if valid else ["idea selection gate FAILED: " + "; ".join(reasons)]))
    if not valid:
        sys.exit(1)


# ───────────────── campaign coverage + analysis bridge (claim-level empirical sufficiency) ─────────────────
@cli.group()
def campaign(): ...


# Typed analysis-bridge CONTENT schema (the bridge.json artifact). Enforced by `campaign validate`.
_BRIDGE_CONTENT_SCHEMA = {
    "type": "object",
    "required": ["supported_claims", "mechanism_interpretation", "limitations", "failure_modes",
                 "recommended_claim_boundaries", "figure_table_recommendations",
                 "paper_facing_result_paragraphs", "claim_to_evidence_map", "evidence_to_section_recommendations"],
    "properties": {
        "supported_claims": {"type": "array"},
        "weakened_or_refuted_claims": {"type": "array"},
        "mechanism_interpretation": {"type": "string", "minLength": 1},
        "alternative_explanations": {"type": "array"},
        "limitations": {"type": "array", "minItems": 1},
        "failure_modes": {"type": "array"},
        "recommended_claim_boundaries": {"type": "array"},
        "figure_table_recommendations": {"type": "array", "minItems": 1},
        "paper_facing_result_paragraphs": {"type": "array", "minItems": 1, "items": {"type": "string", "minLength": 1}},
        "claim_to_evidence_map": {"type": "object", "minProperties": 1},
        "evidence_to_section_recommendations": {}
    }
}


def _latest_bridge_row(conn, quest_id):
    return conn.execute(
        "SELECT bridge_id, bridge_ref, valid, validated_fingerprint FROM analysis_bridge WHERE quest_id=? "
        "ORDER BY created_at DESC, bridge_id DESC LIMIT 1", (quest_id,)).fetchone()


def _evidence_provenance_ok(conn, source_kind, source_ref, waived, pub=False, art_waived=False):
    """Provenance check for one claim_evidence row. reference/external = the trusted-external route;
    analysis/measurement are not result-direct — all pass. A 'result' source counts only if its result row
    carries provenance_ok=1 (set by `result validate`), unless waived (DEEPRESEARCH_PROVENANCE_GATE=0).
    At PUBLICATION rigor a local (declared-only) result additionally needs artifact-backed provenance
    (provenance_level != 'declared') unless DEEPRESEARCH_ARTIFACT_PROVENANCE_GATE=0 waives it."""
    if waived:
        return True, ""
    if source_kind in ("reference", "external", "analysis", "measurement"):
        return True, ""
    try:
        row = conn.execute("SELECT provenance_ok, provenance_level FROM result WHERE result_id=?",
                           (source_ref,)).fetchone()
    except sqlite3.OperationalError:
        return True, ""  # provenance column absent on an un-migrated DB: grandfather (fail-safe, like other gates)
    if row is None:
        return False, f"result {source_ref!r} not found"
    if not row["provenance_ok"]:
        return (False, f"result {source_ref!r} provenance not validated — run `result validate` "
                       "(or declare provenance_route imported/trusted/waived on the result)")
    if pub and not art_waived and (row["provenance_level"] or "declared") == "declared":
        return (False, f"result {source_ref!r} provenance is declared only — publication rigor requires "
                       "artifact-backed provenance (record the run's log/config/output artifacts + re-run "
                       "`result validate`) or a waiver")
    return True, ""


# Kind-specific PROOF requirements: (required descriptive fields, required result-reference fields).
# An evidence_kind not listed here (e.g. qualitative) needs no structural proof. Reference fields must resolve
# to a result row. Aligned to the evidence_kind enum that campaign coverage reasons over.
_PROOF_SPEC = {
    "main_result":         (["metric", "direction"], []),
    "baseline_comparison": (["metric", "direction"], []),
    "ablation":            (["changed_factor", "controls", "delta"], ["parent_result"]),
    "robustness":          (["varied_condition", "original_condition", "criterion"], []),
    "negative":            (["hypothesis", "observed", "implication"], []),
    "boundary":            (["hypothesis", "observed", "implication"], []),
    "significance":        (["method", "effect"], []),
    "efficiency":          (["resource", "metric", "baseline"], []),
    "error_analysis":      (["error_category", "subset", "implication"], []),
}


def _evidence_proof_waived():
    """Operator override: turn evidence-kind PROOF enforcement off (advisory). Surfaced in gate status."""
    return os.environ.get("DEEPRESEARCH_EVIDENCE_PROOF_GATE") in ("0", "false", "no")


def _evidence_proof_ok(conn, row, waived):
    """Kind-specific proof check for one supporting claim_evidence row. Returns (ok, reason). A
    reference/external source must cite an explicit source/citation; a result/analysis source must carry the
    kind's required proof fields, and any result-reference field (e.g. ablation.parent_result) must resolve."""
    if waived:
        return True, ""
    ek = row["evidence_kind"]
    sk = row["source_kind"]
    spec = _PROOF_SPEC.get(ek)
    raw = row["evidence_proof"] if "evidence_proof" in row.keys() else None
    try:
        proof = json.loads(raw) if raw else {}
    except Exception:
        return False, f"{ek} evidence not counted: malformed proof"
    if not isinstance(proof, dict):
        return False, f"{ek} evidence not counted: malformed proof"
    # reference/external evidence must be an explicit, cited source — never silently a local experimental proof.
    if sk in ("reference", "external") and not str(proof.get("source") or proof.get("citation") or "").strip():
        return False, f"{ek} evidence not counted: {sk} source needs an explicit source/citation in proof"
    if spec is None:
        return True, ""  # kinds with no structural requirement (e.g. qualitative)
    desc_fields, ref_fields = spec
    for f in desc_fields:
        if not str(proof.get(f, "")).strip():
            return False, f"{ek} evidence not counted: missing {f}"
    for f in ref_fields:
        val = str(proof.get(f, "")).strip()
        if not val:
            return False, f"{ek} evidence not counted: missing {f}"
        try:
            r = conn.execute("SELECT 1 FROM result WHERE result_id=?", (val,)).fetchone()
        except sqlite3.OperationalError:
            r = None
        if r is None:
            return False, f"{ek} evidence not counted: {f} unresolved ({val!r})"
    return True, ""


def _claim_coverage(conn, quest_id, floors):
    """Per-main-claim empirical coverage by evidence_kind under the rigor floor. Returns (ok, reasons, detail).
    Main claims = claim rows of kind='claim' in status open/supported. baseline satisfied if the claim has a
    baseline_comparison evidence OR the quest's baseline_gate is 'waived'. An evidence_kind is counted ONLY
    when its result has validated provenance AND it carries valid kind-specific proof;
    an evidence_kind present only on provenance-less / proof-less rows is reported as not-counted (visible
    reason) rather than silently dropped."""
    reasons, detail = [], {}
    prov_waived = _provenance_waived()
    proof_waived = _evidence_proof_waived()
    _qr = conn.execute("SELECT rigor_level FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    _pub = records._rigor_order((_qr[0] if _qr else None) or "standard") >= records._rigor_order("publication")
    _art_waived = _artifact_provenance_waived()
    bg = conn.execute("SELECT baseline_gate FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    baseline_waived = bool(bg) and bg[0] == "waived"
    claims = conn.execute("SELECT claim_id FROM claim WHERE quest_id=? AND kind='claim' "
                          "AND status IN ('open','supported')", (quest_id,)).fetchall()
    if not claims:
        return False, ["no main claims (kind='claim') to cover"], detail
    req = set(floors.get("campaign_required", []))
    anyof = set(floors.get("campaign_anyof", []))
    need_baseline = bool(floors.get("campaign_baseline"))
    need_sig = bool(floors.get("campaign_significance_superiority"))
    for (cid,) in claims:
        erows = conn.execute(
            "SELECT source_kind, source_ref, evidence_kind, evidence_proof FROM claim_evidence WHERE claim_id=? "
            "AND relation='supports' AND evidence_kind IS NOT NULL", (cid,)).fetchall()
        kinds, unproven = set(), {}
        for er in erows:
            ok, why = _evidence_provenance_ok(conn, er["source_kind"], er["source_ref"], prov_waived, _pub, _art_waived)
            if ok:
                ok, why = _evidence_proof_ok(conn, er, proof_waived)  # kind-specific proof
            if ok:
                kinds.add(er["evidence_kind"])
            else:
                unproven.setdefault(er["evidence_kind"], why)
        detail[cid] = sorted(kinds)
        gaps = []
        # An evidence_kind provided ONLY by provenance-less results is not counted — say so (visible reason).
        for ek, why in sorted({e: w for e, w in unproven.items() if e not in kinds}.items()):
            gaps.append(f"'{ek}' evidence not counted ({why})")
        for k in req:
            if k not in kinds:
                gaps.append(f"needs {k}")
        if need_baseline and "baseline_comparison" not in kinds and not baseline_waived:
            gaps.append("needs baseline_comparison (or a baseline waiver)")
        if anyof and not (kinds & anyof):
            gaps.append("needs one of " + "/".join(sorted(anyof)))
        if need_sig and "baseline_comparison" in kinds and "significance" not in kinds:
            gaps.append("superiority claim needs significance/uncertainty evidence")
        if gaps:
            reasons.append(f"claim {cid}: " + "; ".join(gaps))
    return (not reasons), reasons, detail


@campaign.command("validate")
@click.option("--quest-id", required=True)
@click.option("--bridge-ref", default=None, help="Typed analysis-bridge.json (else the latest analysis_bridge row's ref).")
@click.pass_context
def campaign_validate(ctx, quest_id, bridge_ref):
    """analysis->write readiness validator. FAILS unless (a) the latest analysis.bridge is paper-facing
    (typed schema: claim->evidence map, paper-facing result paragraphs, limitations, figure/table recs), AND
    (b) per-MAIN-CLAIM empirical coverage by evidence_kind meets the rigor floor ([gate_floors]). Writes the
    validator-computed valid flag + coverage onto the analysis_bridge row (the analyst cannot self-certify).
    The analysis->write handoff gate reads valid. Exits non-zero on any gap."""
    conn = _conn(ctx)
    row = _latest_bridge_row(conn, quest_id)
    if row is None:
        conn.close()
        emit(envelope("campaign validate", ok=False, quest_id=quest_id,
                      diagnostics=["no analysis.bridge recorded (record one first)"]))
        sys.exit(1)
    qr = conn.execute("SELECT rigor_level FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    rigor = (qr[0] if qr else None) or "standard"
    floors = _gate_floors(rigor)
    reasons = []
    # (a) bridge structure / paper-facing
    ref = bridge_ref or row["bridge_ref"]
    txt = _read_artifact_text(ref)
    if txt is None:
        reasons.append(f"analysis-bridge artifact not readable at {ref}")
    else:
        try:
            jsonschema.validate(json.loads(txt), _BRIDGE_CONTENT_SCHEMA)
        except jsonschema.ValidationError as e:
            reasons.append(f"analysis-bridge schema (not paper-facing): {e.message}")
        except Exception as e:
            reasons.append(f"analysis-bridge not parseable: {e}")
    # (b) per-claim coverage
    cov_ok, cov_reasons, cov_detail = _claim_coverage(conn, quest_id, floors)
    reasons += cov_reasons
    valid = not reasons
    coverage = {"valid": valid, "rigor": rigor, "coverage_ok": cov_ok, "per_claim": cov_detail,
                "reasons": reasons, "floors": {k: floors[k] for k in floors if k.startswith("campaign")}}
    fp = records.dep_fingerprint(conn, quest_id, "campaign") if valid else None  # staleness signature
    conn.execute("UPDATE analysis_bridge SET valid=?, coverage_json=?, validated_fingerprint=? WHERE bridge_id=?",
                 (1 if valid else 0, json.dumps(coverage), fp, row["bridge_id"]))
    conn.commit(); conn.close()
    emit(envelope("campaign validate", ok=valid, quest_id=quest_id, data=coverage,
                  diagnostics=[] if valid else ["analysis->write gate FAILED: " + "; ".join(reasons)]))
    if not valid:
        sys.exit(1)


# ───────────────── review verdict (reviewer verdict as a binding, routing-driving gate) ─────────────────
@cli.group()
def review(): ...


# Typed review-verdict CONTENT schema (the verdict.json artifact). Enforced by `review validate`.
_VERDICT_CONTENT_SCHEMA = {
    "type": "object",
    "required": ["verdict", "summary"],
    "properties": {
        "verdict": {"enum": ["accept", "borderline", "reject"]},
        "summary": {"type": "string", "minLength": 1},
        "fatal_flaws": {"type": "array", "items": {"type": "string"}},
        "missing_experiments": {"type": "array", "items": {"type": "string"}},
        "missing_analysis": {"type": "array", "items": {"type": "string"}},
        "overclaims": {"type": "array", "items": {"type": "string"}},
        "unsupported_claims": {"type": "array", "items": {"type": "string"}},
        "rewrite_requirements": {"type": "array", "items": {"type": "string"}},
        "external_benchmark": {"type": "array"},
        "experiment_todo": {"type": "array", "items": {"type": "string"}},
        "analysis_todo": {"type": "array", "items": {"type": "string"}},
        "rewrite_todo": {"type": "array", "items": {"type": "string"}},
        "routing_recommendation": {"type": "string"}
    }
}


def _latest_verdict_row(conn, quest_id):
    return conn.execute(
        "SELECT verdict_id, verdict, verdict_ref, valid, operator_confirmed, route_target, validated_fingerprint "
        "FROM review_verdict WHERE quest_id=? ORDER BY created_at DESC, verdict_id DESC LIMIT 1",
        (quest_id,)).fetchone()


def _verdict_route_target(v):
    """Deterministic follow-up stage from the verdict content (most-upstream flaw first)."""
    if v.get("verdict") == "accept":
        return "finalize"
    if v.get("missing_experiments"):
        return "experiment"
    if v.get("missing_analysis"):
        return "analysis"
    if v.get("overclaims") or v.get("unsupported_claims") or v.get("rewrite_requirements"):
        return "write"
    if v.get("experiment_todo"):
        return "experiment"
    if v.get("analysis_todo"):
        return "analysis"
    return "write"


def _verdict_actionability(v):
    """B-rules. Returns the list of reasons a verdict is NOT actionable ([] = actionable)."""
    reasons = []
    verdict = v.get("verdict")
    if verdict in ("borderline", "reject"):
        if not (v.get("experiment_todo") or v.get("analysis_todo") or v.get("rewrite_todo")):
            reasons.append(f"{verdict} verdict has no actionable todo "
                           "(needs >=1 of experiment_todo/analysis_todo/rewrite_todo)")
    if v.get("missing_experiments") and not v.get("experiment_todo"):
        reasons.append("missing_experiments present but no experiment_todo")
    if v.get("missing_analysis") and not v.get("analysis_todo"):
        reasons.append("missing_analysis present but no analysis_todo")
    if (v.get("overclaims") or v.get("unsupported_claims") or v.get("rewrite_requirements")) \
            and not v.get("rewrite_todo"):
        reasons.append("overclaims/unsupported_claims/rewrite_requirements present but no rewrite_todo")
    return reasons


@review.command("validate")
@click.option("--quest-id", required=True)
@click.option("--verdict-ref", default=None, help="Typed verdict.json (else the latest review_verdict row's ref).")
@click.pass_context
def review_validate(ctx, quest_id, verdict_ref):
    """Validate the latest review verdict: typed schema + ACTIONABILITY (a borderline/reject verdict MUST carry
    todos that cover the flaws it raises). Computes route_target and writes valid+route_target onto the
    review_verdict row — the Reviewer cannot self-certify validity. Exits non-zero when invalid/non-actionable."""
    conn = _conn(ctx)
    row = _latest_verdict_row(conn, quest_id)
    if row is None:
        conn.close()
        emit(envelope("review validate", ok=False, quest_id=quest_id,
                      diagnostics=["no review verdict recorded (record a review.verdict first)"]))
        sys.exit(1)
    ref = verdict_ref or row["verdict_ref"]
    txt = _read_artifact_text(ref)
    reasons, content = [], None
    if txt is None:
        reasons.append(f"verdict artifact not readable at {ref}")
    else:
        try:
            content = json.loads(txt)
            jsonschema.validate(content, _VERDICT_CONTENT_SCHEMA)
        except jsonschema.ValidationError as e:
            reasons.append(f"verdict schema: {e.message}"); content = None
        except Exception as e:
            reasons.append(f"verdict not parseable: {e}"); content = None
    if content is not None:
        if content.get("verdict") != row["verdict"]:
            reasons.append(f"verdict mismatch: row={row['verdict']!r} artifact={content.get('verdict')!r}")
        reasons += _verdict_actionability(content)
    target = _verdict_route_target(content) if content else None
    valid = not reasons
    fp = records.dep_fingerprint(conn, quest_id, "review") if valid else None  # staleness signature
    conn.execute("UPDATE review_verdict SET valid=?, route_target=?, validated_fingerprint=? WHERE verdict_id=?",
                 (1 if valid else 0, target, fp, row["verdict_id"]))
    conn.commit(); conn.close()
    emit(envelope("review validate", ok=valid, quest_id=quest_id,
                  data={"verdict": row["verdict"], "valid": valid, "route_target": target, "reasons": reasons},
                  diagnostics=[] if valid else ["review verdict invalid/non-actionable: " + "; ".join(reasons)]))
    if not valid:
        sys.exit(1)


@review.command("route")
@click.option("--quest-id", required=True)
@click.pass_context
def review_route(ctx, quest_id):
    """Deterministic follow-up routing for the latest review verdict (the Orchestrator consumes this): reject/
    borderline -> experiment|analysis|write (by the verdict's flaws); accept -> finalize. Read-only."""
    conn = _conn(ctx)
    row = _latest_verdict_row(conn, quest_id)
    conn.close()
    if row is None:
        emit(envelope("review route", ok=True, quest_id=quest_id,
                      data={"verdict": None, "route_target": None, "note": "no review verdict yet"}))
        return
    finalize_ok = bool(row["valid"]) and (row["verdict"] == "accept"
                                          or (row["verdict"] == "borderline" and row["operator_confirmed"]))
    emit(envelope("review route", ok=True, quest_id=quest_id,
                  data={"verdict": row["verdict"], "valid": bool(row["valid"]),
                        "operator_confirmed": bool(row["operator_confirmed"]),
                        "route_target": row["route_target"], "finalize_permitted_by_review": finalize_ok}))


@review.command("confirm")
@click.option("--quest-id", required=True)
@click.pass_context
def review_confirm(ctx, quest_id):
    """Operator: confirm the latest BORDERLINE verdict so it may finalize at standard rigor (publication never
    permits borderline). Errors if the latest verdict is not 'borderline'."""
    conn = _conn(ctx)
    row = _latest_verdict_row(conn, quest_id)
    if row is None or row["verdict"] != "borderline":
        conn.close()
        emit(envelope("review confirm", ok=False, quest_id=quest_id,
                      diagnostics=["latest verdict is not 'borderline' (nothing to confirm)"]))
        sys.exit(1)
    conn.execute("UPDATE review_verdict SET operator_confirmed=1 WHERE verdict_id=?", (row["verdict_id"],))
    conn.commit(); conn.close()
    emit(envelope("review confirm", ok=True, quest_id=quest_id,
                  data={"verdict_id": row["verdict_id"], "operator_confirmed": True}))


# ───────────────── unified gate status + methodology resolution (integration) ─────────────────
# quest-local ref resolution for opportunity.motivating_refs / finding.links (ADVISORY; no cross-quest refs).
_REF_TABLES = {  # ref_type -> (table, id_column) resolved with an explicit quest_id column
    "finding": ("finding_memory", "memory_id"), "result": ("result", "result_id"),
    "claim": ("claim", "claim_id"), "idea_select": ("idea_select", "select_id"),
    "experiment": ("experiment", "experiment_id"), "analysis_bridge": ("analysis_bridge", "bridge_id"),
    "paper_spine": ("paper_spine", "quest_id"), "branch": ("branch", "branch_id"),
    "artifact": ("artifact", "artifact_id"), "scope_contract": ("scope_contract", "contract_id"),
    "opportunity": ("research_opportunity", "opportunity_id"),
}
_REF_KEY_TYPE = {  # accept both type-name and *_id/_ids key styles
    "finding": "finding", "findings": "finding", "finding_ids": "finding",
    "result": "result", "results": "result", "result_ids": "result",
    "claim": "claim", "claims": "claim", "claim_ids": "claim",
    "claim_evidence": "claim_evidence", "claim_evidence_ids": "claim_evidence",
    "idea_select": "idea_select", "idea_select_id": "idea_select",
    "experiment": "experiment", "experiment_id": "experiment", "experiment_ids": "experiment",
    "analysis_bridge": "analysis_bridge", "analysis_bridge_id": "analysis_bridge",
    "paper_spine": "paper_spine", "paper_spine_id": "paper_spine",
    "branch": "branch", "branch_id": "branch", "branch_ids": "branch",
    "artifact": "artifact", "artifact_id": "artifact", "artifact_ids": "artifact",
    "scope_contract": "scope_contract", "scope_contract_id": "scope_contract",
    "opportunity": "opportunity", "opportunity_ids": "opportunity", "opportunity_id": "opportunity",
}


def _ref_status(conn, quest_id, rtype, rid):
    """'' if the ref resolves for THIS quest; 'cross_quest' if it exists for another quest; 'missing' otherwise."""
    try:
        if rtype == "claim_evidence":  # composite PK, no quest_id column -> resolve via its claim
            if conn.execute("SELECT 1 FROM claim_evidence e JOIN claim c ON c.claim_id=e.claim_id "
                            "WHERE e.claim_id=? AND c.quest_id=? LIMIT 1", (rid, quest_id)).fetchone():
                return ""
            return "cross_quest" if conn.execute("SELECT 1 FROM claim_evidence WHERE claim_id=? LIMIT 1",
                                                 (rid,)).fetchone() else "missing"
        table, idc = _REF_TABLES[rtype]
        if conn.execute(f"SELECT 1 FROM {table} WHERE {idc}=? AND quest_id=? LIMIT 1", (rid, quest_id)).fetchone():
            return ""
        return "cross_quest" if conn.execute(f"SELECT 1 FROM {table} WHERE {idc}=? LIMIT 1", (rid,)).fetchone() else "missing"
    except sqlite3.OperationalError:
        return ""  # table absent on an un-reinited DB: grandfather (advisory, never blocks)


def _resolve_quest_refs(conn, quest_id, refs):
    """ADVISORY quest-local resolution of a refs dict (opportunity.motivating_refs / finding.links). Returns a
    list of {ref_type, id, status: 'missing'|'cross_quest'} for refs that do NOT resolve to this quest; an
    empty list means all provided refs resolve (or none were given). NEVER blocks — surfaced as warnings only."""
    if not isinstance(refs, dict):
        return []
    out = []
    for key, val in refs.items():
        rtype = _REF_KEY_TYPE.get(key)
        if rtype is None:
            continue  # unknown key -> ignore (forward-compatible, advisory)
        for rid in (val if isinstance(val, list) else [val]):
            rid = str(rid).strip()
            if not rid:
                continue
            st = _ref_status(conn, quest_id, rtype, rid)
            if st:
                out.append({"ref_type": rtype, "id": rid, "status": st})
    return out


_SIG_KEYS = ("idea_key", "method_key", "parameter_key", "condition", "route", "baseline_id")


def _sig_overlap(a, b):
    """Discriminating key shared (case-insensitive, non-empty) by two attempt_signatures, else None."""
    a, b = a or {}, b or {}
    for k in _SIG_KEYS:
        va = str(a.get(k) or "").strip().lower()
        if va and va == str(b.get(k) or "").strip().lower():
            return k
    da, db_ = str(a.get("dataset") or "").strip().lower(), str(a.get("metric") or "").strip().lower()
    if da and db_ and da == str(b.get("dataset") or "").strip().lower() and db_ == str(b.get("metric") or "").strip().lower():
        return "dataset+metric"
    return None


def _repeat_failure_warnings(conn, quest_id):
    """ADVISORY quest-local repeated-failure detector. For each OPEN opportunity (and the latest idea selection)
    whose attempt_signature / motivating_refs resemble prior FAILED signals of THIS quest — dropped
    opportunities, refuted claims, negative/boundary evidence, lesson findings — return
    [{source, ref, warnings:[...]}]. NEVER blocks; quest-local only (no cross-quest attempts considered)."""
    def rows(sql, *a):
        try:
            return conn.execute(sql, (quest_id, *a)).fetchall()
        except sqlite3.OperationalError:
            return []
    dropped = []
    for r in rows("SELECT opportunity_id, attempt_signature FROM research_opportunity WHERE quest_id=? AND status='dropped'"):
        try:
            sig = json.loads(r["attempt_signature"]) if r["attempt_signature"] else {}
        except Exception:
            sig = {}
        dropped.append((r["opportunity_id"], sig))
    refuted = {r[0]: str(r[1] or "") for r in rows("SELECT claim_id, statement FROM claim WHERE quest_id=? AND status='refuted'")}
    negtext = [str(r[0]) for r in rows("SELECT e.evidence_proof FROM claim_evidence e JOIN claim c ON c.claim_id=e.claim_id "
                                       "WHERE c.quest_id=? AND e.evidence_kind IN ('negative','boundary') AND e.evidence_proof IS NOT NULL")]
    lessons = [(r[0], str(r[1] or "")) for r in rows("SELECT memory_id, summary FROM finding_memory WHERE quest_id=? AND kind='lesson'")]

    def warnings_for(sig, refs):
        sig, refs, w = sig or {}, refs or {}, []
        for oid, dsig in dropped:
            k = _sig_overlap(sig, dsig)
            if k:
                w.append(f"possible repeat of dropped opportunity {oid} (shared {k})")
        for cid in (refs.get("claim") or refs.get("claim_ids") or []):
            if str(cid) in refuted:
                w.append(f"possible repeat of refuted claim {cid}")
        cond = str(sig.get("condition") or "").strip().lower()
        if cond:
            if any(cond in t.lower() for t in negtext):
                w.append(f"possible repeat of negative/boundary evidence for condition {sig.get('condition')!r}")
            for cid, stmt in refuted.items():
                if cond in stmt.lower():
                    w.append(f"possible repeat of refuted claim {cid} (condition {sig.get('condition')!r})")
        for key in ("method_key", "idea_key"):
            kv = str(sig.get(key) or "").strip().lower()
            if kv:
                for fid, summ in lessons:
                    if kv in summ.lower():
                        w.append(f"similar failed-path lesson exists: {fid}")
        return sorted(set(w))

    out = []
    for r in rows("SELECT opportunity_id, attempt_signature, motivating_refs FROM research_opportunity WHERE quest_id=? AND status='open'"):
        try:
            sig = json.loads(r["attempt_signature"]) if r["attempt_signature"] else {}
        except Exception:
            sig = {}
        try:
            refs = json.loads(r["motivating_refs"]) if r["motivating_refs"] else {}
        except Exception:
            refs = {}
        w = warnings_for(sig, refs)
        if w:
            out.append({"source": "opportunity", "ref": r["opportunity_id"], "warnings": w})
    idr = _latest_idea_select_row(conn, quest_id)
    if idr is not None and idr["select_ref"]:
        try:
            content = json.loads(_read_artifact_text(idr["select_ref"]) or "null")
        except Exception:
            content = None
        if isinstance(content, dict) and isinstance(content.get("attempt_signature"), dict):
            w = warnings_for(content["attempt_signature"], {})
            if w:
                out.append({"source": "idea_select", "ref": idr["select_id"], "warnings": w})
    return out


@cli.group()
def opportunity(): ...


@opportunity.command("list")
@click.option("--quest-id", required=True)
@click.option("--status", default=None, help="filter by status: open|addressed|dropped|superseded")
@click.pass_context
def opportunity_list(ctx, quest_id, status):
    """List the quest-local research-opportunity ledger (ADVISORY 'what to try next and why'; never a gate).
    Open opportunities first, then most-recent. Record via `record apply --type opportunity.record`."""
    conn = _conn(ctx)
    try:
        sql = ("SELECT opportunity_id, kind, status, rationale, motivating_refs, proposed_by, round_index, "
               "created_at FROM research_opportunity WHERE quest_id=?")
        args = [quest_id]
        if status:
            sql += " AND status=?"; args.append(status)
        sql += " ORDER BY (status='open') DESC, created_at DESC, opportunity_id"
        rows = []
        for r in conn.execute(sql, args):
            try:
                mr = json.loads(r["motivating_refs"]) if r["motivating_refs"] else None
            except Exception:
                mr = r["motivating_refs"]
            unresolved = _resolve_quest_refs(conn, quest_id, mr if isinstance(mr, dict) else None)
            rows.append(dict(opportunity_id=r["opportunity_id"], kind=r["kind"], status=r["status"],
                             rationale=r["rationale"], motivating_refs=mr, proposed_by=r["proposed_by"],
                             round_index=r["round_index"], created_at=r["created_at"],
                             unresolved_refs=unresolved))
    except sqlite3.OperationalError:
        rows = []
    conn.close()
    warns = [f"opportunity {r['opportunity_id']} has unresolved motivating_refs: "
             + ", ".join(f"{u['ref_type']}:{u['id']}[{u['status']}]" for u in r["unresolved_refs"])
             for r in rows if r["unresolved_refs"]]
    emit(envelope("opportunity list", ok=True, quest_id=quest_id,
                  data={"opportunities": rows, "count": len(rows),
                        "open": sum(1 for r in rows if r["status"] == "open"),
                        "with_unresolved_refs": sum(1 for r in rows if r["unresolved_refs"])},
                  warnings=warns))


@opportunity.command("check")
@click.option("--quest-id", required=True)
@click.pass_context
def opportunity_check(ctx, quest_id):
    """Read-only ADVISORY check: resolve every opportunity's motivating_refs against THIS quest's rows. Reports
    refs that are missing or belong to another quest (cross_quest). NEVER blocks — purely informational."""
    conn = _conn(ctx)
    try:
        opps = conn.execute("SELECT opportunity_id, motivating_refs FROM research_opportunity WHERE quest_id=? "
                            "ORDER BY created_at, opportunity_id", (quest_id,)).fetchall()
    except sqlite3.OperationalError:
        opps = []
    report = []
    for o in opps:
        try:
            mr = json.loads(o["motivating_refs"]) if o["motivating_refs"] else None
        except Exception:
            mr = None
        un = _resolve_quest_refs(conn, quest_id, mr if isinstance(mr, dict) else None)
        if un:
            report.append({"opportunity_id": o["opportunity_id"], "unresolved_refs": un})
    repeat = _repeat_failure_warnings(conn, quest_id)
    conn.close()
    emit(envelope("opportunity check", ok=True, quest_id=quest_id,
                  data={"opportunities_checked": len(opps), "unresolved": report, "all_resolved": not report,
                        "repeated_failure": repeat, "no_repeat_risk": not repeat}))


def _discovery(conn, quest_id):
    """ADVISORY quest-local discovery summary (never blocking). Open opportunities + recommended next actions,
    plus unsupported/refuted claims, parked/abandoned routes, and a negative/boundary findings count — all
    derived from existing quest-local rows. Returns a plain dict for gate status."""
    def rows(sql, *a):
        try:
            return conn.execute(sql, (quest_id, *a)).fetchall()
        except sqlite3.OperationalError:
            return []
    opps = rows("SELECT opportunity_id, kind, rationale, motivating_refs FROM research_opportunity WHERE "
                "quest_id=? AND status='open' ORDER BY created_at DESC, opportunity_id")
    unresolved_opps = []
    for o in opps:
        try:
            mr = json.loads(o["motivating_refs"]) if ("motivating_refs" in o.keys() and o["motivating_refs"]) else None
        except Exception:
            mr = None
        un = _resolve_quest_refs(conn, quest_id, mr if isinstance(mr, dict) else None)
        if un:
            unresolved_opps.append({"opportunity_id": o["opportunity_id"], "unresolved_refs": un})
    refuted = [r[0] for r in rows("SELECT claim_id FROM claim WHERE quest_id=? AND status='refuted'")]
    unsupported = [r[0] for r in rows("SELECT claim_id FROM claim WHERE quest_id=? AND kind='claim' "
                                      "AND status='open'")]
    parked = [r[0] for r in rows("SELECT branch_id FROM branch WHERE quest_id=? AND status IN ('parked','abandoned')")]
    neg = (rows("SELECT COUNT(*) FROM analysis WHERE quest_id=? AND verdict='blocks'") or [[0]])[0][0]
    negev = (rows("SELECT COUNT(*) FROM claim_evidence e JOIN claim c ON c.claim_id=e.claim_id "
                  "WHERE c.quest_id=? AND e.evidence_kind IN ('negative','boundary')") or [[0]])[0][0]
    return {
        "open_opportunities": [dict(opportunity_id=o["opportunity_id"], kind=o["kind"], rationale=o["rationale"]) for o in opps],
        "recommended_next_actions": [f"{o['kind']}: {str(o['rationale'])[:80]}" for o in opps[:5]],
        "opportunities_with_unresolved_refs": unresolved_opps,
        "repeated_failure_warnings": _repeat_failure_warnings(conn, quest_id),
        "refuted_claims": refuted,
        "unsupported_claims": unsupported,
        "parked_routes": parked,
        "negative_findings": int(neg) + int(negev),
    }


@cli.group()
def gate(): ...


@gate.group("waiver")
def gate_waiver(): ...


@gate_waiver.command("list")
@click.option("--quest-id", required=True)
@click.pass_context
def gate_waiver_list(ctx, quest_id):
    """List the durable quality_gate.waiver records for a quest (read-only audit view). Record a waiver via
    `record apply --type quality_gate.waiver` (gate, source, reason [required], finalize_ack)."""
    conn = _conn(ctx)
    try:
        rows = [dict(waiver_id=r["waiver_id"], gate=r["gate"], source=r["source"], reason=r["reason"],
                     finalize_ack=bool(r["finalize_ack"]), actor=r["actor"], expiry=r["expiry"],
                     scope=r["scope"], created_at=r["created_at"])
                for r in conn.execute("SELECT * FROM quality_gate_waiver WHERE quest_id=? "
                                      "ORDER BY created_at, waiver_id", (quest_id,))]
    except sqlite3.OperationalError:
        rows = []
    conn.close()
    emit(envelope("gate waiver list", ok=True, quest_id=quest_id,
                  data={"waivers": rows, "count": len(rows),
                        "finalize_ack_gates": sorted({r["gate"] for r in rows if r["finalize_ack"]})}))


_OK_BASELINE_V = {"verified_match", "close_match", "trusted_with_caveats"}


def _is_bound(conn, quest_id, rigor):
    """A binding regime (the binding gates bite): research-contract quest at rigor >= standard."""
    return (records._has_research_contract(conn, quest_id)
            and records._rigor_order(rigor) >= records._rigor_order("standard"))


@gate.command("status")
@click.option("--quest-id", required=True)
@click.pass_context
def gate_status(ctx, quest_id):
    """Unified, MACHINE-READABLE status of every binding gate + finalize readiness, for deterministic
    Orchestrator routing. READ-ONLY: it summarizes and guides routing; the hard guards remain
    authoritative (this does NOT replace them). Each gate: status(pass|fail|advisory|not_applicable|missing|
    waived), rigor_level, blocking, reason, latest_record_ref, route_target, required_next_action, waived,
    waiver_source. Env-var gate waivers are surfaced as status='waived' (non-blocking) + listed in
    data.active_waivers so an operator override is auditable, never silent."""
    conn = _conn(ctx)
    q = conn.execute("SELECT rigor_level, baseline_gate, best_result_ref, run_state FROM quest WHERE quest_id=?",
                     (quest_id,)).fetchone()
    if not q:
        conn.close(); emit(envelope("gate status", ok=False, quest_id=quest_id, diagnostics=["no such quest"])); sys.exit(1)
    rigor = q["rigor_level"] or "standard"
    bound = _is_bound(conn, quest_id, rigor)
    adv = not bound
    floors = _gate_floors(rigor)
    gates = {}

    # Env-var waivers (operator overrides) are otherwise INVISIBLE here — they silently bypass the write-path
    # hard guards while gate status keeps reporting fail/missing, so the routing view disagrees with what the
    # guards will actually do. Surface them: a waived gate reports status='waived' (non-blocking, carrying a
    # waiver_source) and every active waiver is listed at the top level (`active_waivers`).
    _GATE_WAIVERS = {"scope_contract": "DEEPRESEARCH_SCOPE_GATE",
                     "idea_gate": "DEEPRESEARCH_IDEA_GATE",
                     "bo_idea_decision": "DEEPRESEARCH_BO_IDEA_GATE",
                     "bo_next_move": "DEEPRESEARCH_BO_NEXT_MOVE_GATE",
                     "baseline_contract": "DEEPRESEARCH_BASELINE_CONTRACT_GATE",
                     "analysis_bridge": "DEEPRESEARCH_BRIDGE_GATE",
                     "manuscript_coverage": "DEEPRESEARCH_COVERAGE_GATE",
                     "review_verdict": "DEEPRESEARCH_REVIEW_GATE"}
    def _waived(var):
        return os.environ.get(var) in ("0", "false", "no")
    active_waivers = sorted({v for v in _GATE_WAIVERS.values() if _waived(v)}
                            | {v for v in ("DEEPRESEARCH_AUTHENTICITY_GATE", "DEEPRESEARCH_PROVENANCE_GATE",
                                           "DEEPRESEARCH_EVIDENCE_PROOF_GATE", "DEEPRESEARCH_FRESHNESS_GATE",
                                           "DEEPRESEARCH_ARTIFACT_PROVENANCE_GATE") if _waived(v)}
                            | ({"DEEPRESEARCH_IDEA_NOVELTY_WAIVER"}  # truthy-to-enable, not =0
                               if os.environ.get("DEEPRESEARCH_IDEA_NOVELTY_WAIVER") else set()))

    def put(name, status, reason="", route=None, ref=None, action=None):
        wv = _GATE_WAIVERS.get(name)
        waived = bool(wv and bound and _waived(wv) and status in ("fail", "missing"))
        gates[name] = {"status": "waived" if waived else status, "rigor_level": rigor,
                       "blocking": bool(bound and status == "fail" and not waived),
                       "reason": (f"env waiver {wv}=0 active; gate NOT enforced at the write path" if waived else reason),
                       "latest_record_ref": ref, "route_target": None if waived else route,
                       "required_next_action": None if waived else action,
                       "waived": waived, "waiver_source": (f"env:{wv}" if waived else None)}

    sc = _latest_scope_row(conn, quest_id)
    if adv: put("scope_contract", "advisory")
    elif sc is None: put("scope_contract", "missing", "no scope/eval contract", "scope", None, "record scope.contract + scope validate")
    elif sc["valid"] and records.is_stale(conn, quest_id, "scope", sc["validated_fingerprint"]):
        put("scope_contract", "fail", "scope/eval contract is stale: contract changed after `scope validate`",
            "scope", sc["contract_id"], "re-run `scope validate`")
    elif sc["valid"]: put("scope_contract", "pass", ref=sc["contract_id"])
    else:
        _sok, _sreasons = _scope_verdict(_load_scope_contract(conn, quest_id))
        put("scope_contract", "fail", "scope/eval contract not validator-confirmed: "
            + ("; ".join(_sreasons) if _sreasons else "run `scope validate`"), "scope", sc["contract_id"],
            "fix the contract + run `scope validate`")

    r = _latest_idea_select_row(conn, quest_id)
    icontent = None
    if r is not None and r["select_ref"]:
        try:
            icontent = json.loads(_read_artifact_text(r["select_ref"]) or "null")
        except Exception:
            icontent = None
    nwaiver = (icontent or {}).get("novelty_waiver") if isinstance(icontent, dict) else None
    if adv: put("idea_gate", "advisory")
    elif r is None: put("idea_gate", "missing", "no idea.select", "idea", None, "record idea.select + idea validate")
    elif r["valid"]:
        put("idea_gate", "pass", ("novelty grounding waived: " + str(nwaiver)[:80]) if nwaiver else "", ref=r["select_id"])
    else:
        _nok, nreasons = _novelty_grounding(conn, quest_id, icontent, rigor, True) if isinstance(icontent, dict) else (False, [])
        put("idea_gate", "fail", "idea selection not validated" + ("; " + "; ".join(nreasons) if nreasons else ""),
            "idea", r["select_id"], "fix + idea validate")

    # bo_idea_decision: when the idea stage produced MULTIPLE gate-eligible enumerable candidates, the BO choice
    # is DECISIVE — idea->baseline waits for an idea-selection bo_decision whose winner is BOUND into
    # idea_select.retained_candidate. A single viable candidate may proceed (BO optional; the binding step records
    # an explicit skip). Advisory off-bound; not_applicable until the idea gate itself passes / when no enumerable
    # idea rows exist (legacy lazy idea_select). NEVER overrides the hard idea gate — it only decides among
    # candidates the idea gate already deemed eligible.
    try:
        eligible_ideas = conn.execute("SELECT idea_id, status FROM idea WHERE quest_id=? AND status IN "
                                       "('proposed','selected') ORDER BY idea_id", (quest_id,)).fetchall()
    except sqlite3.OperationalError:
        eligible_ideas = []
    n_viable = len(eligible_ideas)
    idea_passed = gates.get("idea_gate", {}).get("status") in ("pass", "waived")
    try:
        bdec = conn.execute("SELECT decision_id, selected_candidate_ref FROM bo_decision WHERE quest_id=? AND "
                            "decision_kind='idea-selection' ORDER BY created_at DESC, decision_id DESC LIMIT 1",
                            (quest_id,)).fetchone()
    except sqlite3.OperationalError:
        bdec = None  # un-migrated DB without decision_kind: treat as no decision (gate stays advisory/N-A)
    if adv:
        put("bo_idea_decision", "advisory")
    elif not idea_passed:
        put("bo_idea_decision", "not_applicable", "idea selection not yet validated")
    elif n_viable == 0:
        put("bo_idea_decision", "not_applicable", "no enumerable idea candidates (legacy/lazy idea_select)")
    elif n_viable == 1:
        put("bo_idea_decision", "pass", "single viable idea candidate — BO selection optional (record an explicit "
            "skip via `bo select --skip-reason` for a fully auditable trail)")
    elif bdec is None:
        put("bo_idea_decision", "fail", f"{n_viable} gate-eligible idea candidates and no idea-selection "
            "bo_decision — BO must choose the winner before baseline", "bo-review", None,
            "run `bo review` (BO-reviewer valuations) then `bo select --decision-kind idea-selection --bind`")
    else:
        sel = bdec["selected_candidate_ref"]
        winner_cid = _idea_candidate_id(sel) if sel else None
        isr2 = conn.execute("SELECT retained_candidate FROM idea_select WHERE quest_id=? "
                            "ORDER BY created_at DESC, select_id DESC LIMIT 1", (quest_id,)).fetchone()
        retained = isr2["retained_candidate"] if isr2 else None
        srow = conn.execute("SELECT status FROM idea WHERE quest_id=? AND idea_id=?", (quest_id, sel)).fetchone() if sel else None
        bound_ok = bool(sel and retained == winner_cid and srow is not None and srow["status"] == "selected")
        if bound_ok:
            put("bo_idea_decision", "pass", f"BO selected {winner_cid}; bound to idea_select.retained_candidate", ref=bdec["decision_id"])
        else:
            put("bo_idea_decision", "fail", f"idea-selection bo_decision exists but its winner ({winner_cid!r}) is not "
                f"bound to idea_select.retained_candidate ({retained!r})", "bo-review", bdec["decision_id"],
                "re-run `bo select --decision-kind idea-selection --bind`")

    bc = conn.execute("SELECT contract_id, valid, validated_fingerprint FROM baseline_contract "
                      "WHERE quest_id=? ORDER BY created_at DESC, contract_id DESC LIMIT 1", (quest_id,)).fetchone()
    if adv: put("baseline_contract", "advisory")
    elif q["baseline_gate"] in ("pending", "blocked") and bc is None:
        put("baseline_contract", "not_applicable", "baseline not yet established")
    elif bc is None:
        put("baseline_contract", "fail", "baseline_gate set without a baseline.contract", "baseline", None, "record baseline.contract")
    elif bc["valid"] and records.is_stale(conn, quest_id, "baseline", bc["validated_fingerprint"]):
        put("baseline_contract", "fail", "baseline contract validation is stale: a dependency (contract or "
            "referenced result provenance) changed after `baseline validate`", "baseline", bc["contract_id"],
            "re-run `baseline validate`")
    elif bc["valid"]:
        put("baseline_contract", "pass", ref=bc["contract_id"])
    else:
        _bok, _breasons, _broute = _baseline_validity(conn, quest_id)
        reason = "baseline.contract not validator-confirmed: " + ("; ".join(_breasons) if _breasons else "run `baseline validate`")
        put("baseline_contract", "fail", reason, "baseline", bc["contract_id"], "fix the contract + run `baseline validate`")

    if adv: put("campaign_coverage", "advisory")
    else:
        cov_ok, cov_reasons, _ = _claim_coverage(conn, quest_id, floors)
        if cov_ok: put("campaign_coverage", "pass")
        else:
            route = "experiment" if any(("main_result" in x or "baseline_comparison" in x or "significance" in x)
                                        for x in cov_reasons) else "analysis"
            put("campaign_coverage", "fail", "; ".join(cov_reasons), route, None,
                "add the missing evidence_kind links + campaign validate")

    ab = _latest_bridge_row(conn, quest_id)
    if adv: put("analysis_bridge", "advisory")
    elif ab is None: put("analysis_bridge", "missing", "no analysis.bridge", "analysis", None, "record analysis.bridge + campaign validate")
    elif ab["valid"] and records.is_stale(conn, quest_id, "campaign", ab["validated_fingerprint"]):
        put("analysis_bridge", "fail", "analysis bridge is stale: claims/evidence/results/baseline changed after "
            "`campaign validate`", "analysis", ab["bridge_id"], "re-run `campaign validate`")
    elif ab["valid"]: put("analysis_bridge", "pass", ref=ab["bridge_id"])
    else: put("analysis_bridge", "fail", "analysis bridge not validated", "analysis", ab["bridge_id"], "campaign validate")

    sp = conn.execute("SELECT submission_ready, validated_fingerprint FROM paper_spine WHERE quest_id=?",
                      (quest_id,)).fetchone()
    if adv:
        put("paper_spine", "advisory"); put("outline_valid", "advisory"); put("manuscript_coverage", "advisory")
    elif sp is None:
        put("paper_spine", "missing", "no paper_spine", "outline", None, "record paper_spine.upsert")
        put("outline_valid", "missing", "no paper_spine", "outline")
        put("manuscript_coverage", "missing", "no paper_spine", "write")
    else:
        put("paper_spine", "pass", ref=quest_id)
        spine = _load_spine(ctx, quest_id, None)
        if spine is None:
            put("outline_valid", "fail", "spine artifact unreadable", "outline", quest_id, "fix spine + outline validate")
        else:
            orx = _spine_structural_reasons(spine)
            put("outline_valid", "pass" if not orx else "fail", "; ".join(orx),
                None if not orx else "outline", quest_id, None if not orx else "fix spine + outline validate")
        ready = bool(sp["submission_ready"])
        if ready and records.is_stale(conn, quest_id, "manuscript", sp["validated_fingerprint"]):
            put("manuscript_coverage", "fail", "manuscript coverage is stale: paper spine / claims / evidence "
                "changed after the coverage check", "write", None, "re-run `manuscript coverage`")
        else:
            put("manuscript_coverage", "pass" if ready else "fail",
                "" if ready else "submission_ready not validator-confirmed", None if ready else "write", None,
                None if ready else "resolve gaps + manuscript coverage")

    rv = _latest_verdict_row(conn, quest_id)
    if adv: put("review_verdict", "advisory")
    elif rv is None: put("review_verdict", "missing", "no review verdict", "review", None, "record review.verdict + review validate")
    else:
        v, valid, conf, rt = rv["verdict"], rv["valid"], rv["operator_confirmed"], rv["route_target"]
        stale = valid and records.is_stale(conn, quest_id, "review", rv["validated_fingerprint"])
        if not valid: put("review_verdict", "fail", "verdict not validated/actionable", "review", rv["verdict_id"], "review validate")
        elif v == "reject": put("review_verdict", "fail", "verdict is reject", rt or "write", rv["verdict_id"], "route follow-ups + re-review")
        elif records._rigor_order(rigor) >= records._rigor_order("publication") and v == "borderline":
            put("review_verdict", "fail", "borderline not allowed at publication", rt or "write", rv["verdict_id"], "revise to accept")
        elif v == "borderline" and not conf:
            put("review_verdict", "fail", "borderline needs operator confirmation", rt or "write", rv["verdict_id"], "review confirm")
        elif stale:
            put("review_verdict", "fail", "review verdict is stale: paper spine / claims / evidence changed after "
                "`review validate`", "review", rv["verdict_id"], "re-review + re-run `review validate`")
        else: put("review_verdict", "pass", ref=rv["verdict_id"])

    # Durable waiver records + finalize-acknowledgement status. An env-waived finalize-sensitive gate
    # needs a durable quality_gate.waiver(finalize_ack) on a bound quest before finalize is allowed.
    try:
        durable_waivers = [dict(gate=r["gate"], source=r["source"], reason=r["reason"],
                                finalize_ack=bool(r["finalize_ack"]), actor=r["actor"], created_at=r["created_at"])
                           for r in conn.execute(
                               "SELECT gate, source, reason, finalize_ack, actor, created_at FROM "
                               "quality_gate_waiver WHERE quest_id=? ORDER BY created_at, waiver_id", (quest_id,))]
    except sqlite3.OperationalError:
        durable_waivers = []
    env_waived_sensitive = records.env_waived_finalize_gates()
    acked = records.acked_finalize_gates(conn, quest_id)
    finalize_ack_missing = sorted(set(env_waived_sensitive) - acked) if bound else []

    # Validator freshness: which computed flags are stale (dependencies changed after validation).
    # Computed regardless of rigor so staleness is visible even in advisory/scoping mode.
    def _sfp(rw):
        return rw["validated_fingerprint"] if rw is not None else None
    stale_gates = sorted({name for name, kind, fpv in (
        ("scope_contract", "scope", _sfp(sc)),
        ("baseline_contract", "baseline", _sfp(bc)),
        ("analysis_bridge", "campaign", _sfp(ab)),
        ("manuscript_coverage", "manuscript", _sfp(sp)),
        ("review_verdict", "review", _sfp(rv)),
    ) if fpv and records.is_stale(conn, quest_id, kind, fpv)})

    fin = []
    if not adv:
        if gates["manuscript_coverage"]["status"] not in ("pass", "waived"): fin.append("manuscript coverage not ready")
        if gates["review_verdict"]["status"] not in ("pass", "waived"): fin.append("review not accepted")
        try:
            if not records.scholarship_audit(conn, quest_id)["ok"]: fin.append("scholarship bar unmet")
        except Exception:
            pass
        best = q["best_result_ref"]
        if best and not _waived("DEEPRESEARCH_AUTHENTICITY_GATE"):
            backed = conn.execute("SELECT COUNT(*) FROM claim_evidence e JOIN claim c ON c.claim_id=e.claim_id "
                                  "WHERE c.quest_id=? AND e.source_kind='result' AND e.source_ref=? "
                                  "AND e.relation='supports'", (quest_id, best)).fetchone()[0]
            if not backed: fin.append("headline result not claim-backed (authenticity)")
        if finalize_ack_missing:
            fin.append("waiver acknowledgement missing for env-waived gate(s): " + ", ".join(finalize_ack_missing))
    if adv: put("finalize_readiness", "advisory")
    elif fin: put("finalize_readiness", "fail", "; ".join(fin), None, None, "resolve blocking gates above")
    else: put("finalize_readiness", "pass")

    # bo_next_move: LATER next-move BO. Post-experiment/analysis, when NO hard gate forces the route and there are
    # ≥2 hard-gate-ELIGIBLE next moves, the choice is BO-DECISIVE — route to bo-review until a CURRENT next-move
    # bo_decision (recorded at/after the newest result/analysis, selecting an eligible move) binds the route.
    # Never competes with a hard gate (not_applicable while any blocks); pre-experiment and on non-active quests
    # it is not_applicable (so finalized quests like q1 are never retroactively blocked). Waiver
    # DEEPRESEARCH_BO_NEXT_MOVE_GATE. BO only ranks moves the hard gates already permit — it bypasses none.
    _NM_HARD = ["scope_contract", "idea_gate", "bo_idea_decision", "baseline_contract", "campaign_coverage",
                "analysis_bridge", "paper_spine", "outline_valid", "manuscript_coverage", "review_verdict"]
    nm_hard_blocking = any(gates.get(g, {}).get("blocking") for g in _NM_HARD)
    active_quest = (q["run_state"] in ("running", "paused", "recovering", "waiting_user"))
    has_results = bool(conn.execute("SELECT 1 FROM result WHERE quest_id=? LIMIT 1", (quest_id,)).fetchone())
    nm_cands = _next_move_candidates(conn, quest_id)
    nm_eligible = [c for c in nm_cands if c["eligible"]]

    def _maxts(sql):
        try:
            r = conn.execute(sql, (quest_id,)).fetchone()
            return (r[0] if r and r[0] else "")
        except sqlite3.OperationalError:
            return ""
    newest_evidence = max(_maxts("SELECT MAX(created_at) FROM result WHERE quest_id=?"),
                          _maxts("SELECT MAX(created_at) FROM analysis WHERE quest_id=?"))
    try:
        nm_dec = conn.execute(
            "SELECT decision_id, selected_candidate_ref, created_at FROM bo_decision WHERE quest_id=? AND "
            "decision_kind IN ('next-move-selection','experiment-selection','opportunity-selection',"
            "'stop-write-finalize-selection') ORDER BY created_at DESC, decision_id DESC LIMIT 1", (quest_id,)).fetchone()
    except sqlite3.OperationalError:
        nm_dec = None
    nm_elig_refs = {c["candidate_ref"] for c in nm_eligible}
    nm_fresh = bool(nm_dec and (nm_dec["created_at"] or "") >= newest_evidence
                    and nm_dec["selected_candidate_ref"] in nm_elig_refs)
    if adv:
        put("bo_next_move", "advisory")
    elif not active_quest:
        put("bo_next_move", "not_applicable", "quest not in an active run state")
    elif not has_results:
        put("bo_next_move", "not_applicable", "no experiment results yet (next-move BO applies post-experiment)")
    elif nm_hard_blocking:
        put("bo_next_move", "not_applicable", "a hard gate determines the next move")
    elif len(nm_eligible) <= 1:
        put("bo_next_move", "pass", ("single eligible next move — BO optional (record an explicit skip via "
            "`bo select --next-move --skip-reason`)" if len(nm_eligible) == 1 else "no eligible next move yet"))
    elif nm_fresh:
        put("bo_next_move", "pass", f"next-move bo_decision binds {nm_dec['selected_candidate_ref']} "
            f"(route via `bo next-moves`)", ref=nm_dec["decision_id"])
    else:
        put("bo_next_move", "fail", f"{len(nm_eligible)} eligible next moves and no current next-move bo_decision "
            "— BO must choose the next move", "bo-review", (nm_dec["decision_id"] if nm_dec else None),
            "run `bo review --next-move` (BO-reviewer valuations) then `bo select --next-move --at <ts>` to bind "
            "the route (or `--skip-reason` if only one is eligible)")

    discovery = _discovery(conn, quest_id)  # ADVISORY quest-local discovery (compute before closing the conn)
    conn.close()
    emit(envelope("gate status", ok=True, quest_id=quest_id,
                  data={"rigor_level": rigor, "bound": bound, "gates": gates,
                        "active_waivers": active_waivers,
                        "durable_waivers": durable_waivers,
                        "finalize_ack_present": sorted(acked),
                        "finalize_ack_missing": finalize_ack_missing,
                        "stale_gates": stale_gates,
                        "discovery": discovery,
                        "next_moves": {"eligible": nm_eligible, "all": nm_cands,
                                       "current_decision": (nm_dec["decision_id"] if nm_dec else None),
                                       "decision_fresh": nm_fresh},
                        "finalize_readiness": gates["finalize_readiness"]["status"],
                        "blocking_gates": [k for k, gv in gates.items() if gv["blocking"]]}))


# stage -> (table, id column, ref column) the methodology must resolve to (validated where applicable).
_STAGE_METHODOLOGY = {
    "scope": ("scope_contract", "contract_id", "contract_ref"),
    "idea": ("idea_select", "select_id", "select_ref"),
    "baseline": ("baseline_contract", "contract_id", "contract_ref"),
    # NOTE: `scope` resolves to the validator-confirmed `scope_contract` (set by `scope validate`). The
    # `experiment` stage has NO fold-time typed methodology record, so it resolves as not_applicable here (see
    # methodology_check) — NOT a failure: `experiment` tags claim evidence by evidence_kind, enforced
    # DOWNSTREAM by campaign coverage at analysis->write. `analysis` resolves to the validated analysis_bridge.
    "analysis": ("analysis_bridge", "bridge_id", "bridge_ref"),
    "outline": ("paper_spine", "quest_id", "spine_ref"),
    "write": ("paper_spine", "quest_id", "spine_ref"),
    "review": ("review_verdict", "verdict_id", "verdict_ref"),
}


@cli.group()
def methodology(): ...


@methodology.command("check")
@click.option("--quest-id", required=True)
@click.option("--stage", required=True)
@click.option("--applied-as", required=True, help="A task-result methodology_used[].applied_as ref.")
@click.pass_context
def methodology_check(ctx, quest_id, stage, applied_as):
    """resolve a task-result `methodology_used[].applied_as` to the stage's expected VALIDATED typed record
    for THIS quest. Exits non-zero (resolves=false) unless applied_as points at a real, same-quest record that
    passed its validator — so methodology usage can no longer be claimed with free text. Background-only reading
    belongs in `methodology_consulted`, not here."""
    m = _STAGE_METHODOLOGY.get(stage)
    conn = _conn(ctx)
    if m is None:
        # Stages with no fold-time typed methodology record (e.g. experiment -> enforced downstream by campaign
        # coverage; orchestrator-internal decision/optimize/finalize -> the methodology-usage advisory). Resolution
        # is not_applicable here, NOT a failure — the binding lives in that stage's own gate.
        conn.close()
        emit(envelope("methodology check", ok=True, quest_id=quest_id,
                      data={"resolves": True, "status": "not_applicable", "stage": stage,
                            "reason": f"stage {stage!r} has no fold-time typed methodology record; "
                                      "enforced by its own gate (campaign coverage / methodology-usage advisory)"}))
        return
    table, idcol, refcol = m
    try:
        row = conn.execute(f"SELECT * FROM {table} WHERE quest_id=? AND ({idcol}=? OR {refcol}=?) "
                           f"ORDER BY created_at DESC LIMIT 1", (quest_id, applied_as, applied_as)).fetchone()
    except sqlite3.OperationalError:
        row = None
    resolves, reason = False, ""
    if row is None:
        reason = f"applied_as {applied_as!r} does not resolve to a {table} for quest {quest_id!r}"
    elif table == "baseline_contract":
        resolves = bool(row["valid"])
        reason = "" if resolves else "baseline.contract not validator-confirmed (run `baseline validate`)"
    elif table == "paper_spine":
        resolves = bool(row["submission_ready"])
        reason = "" if resolves else "paper_spine.submission_ready not validator-confirmed"
    else:  # idea_select / analysis_bridge / review_verdict carry a `valid` column
        resolves = bool(row["valid"])
        reason = "" if resolves else f"{table} referenced by applied_as is not validator-confirmed (valid=0)"
    conn.close()
    emit(envelope("methodology check", ok=resolves, quest_id=quest_id,
                  data={"resolves": resolves, "stage": stage, "table": table, "applied_as": applied_as, "reason": reason},
                  diagnostics=[] if resolves else [reason]))
    if not resolves:
        sys.exit(1)


@cli.group()
def manuscript(): ...


# Loop/operator jargon that must never surface in paper-facing prose (validate_manuscript_language).
_MANUSCRIPT_FORBIDDEN = ["route", "handoff", "worktree", "lane", "notifier", "self-wakeup",
                         "the user requested", "paper restart", "this quest", "64 + 64", "64+64", "todo"]


@manuscript.command("validate")
@click.option("--quest-id", default=None)
@click.option("--artifact-ref", default=None, help="Path to the manuscript artifact (loop-relative) to scan.")
def manuscript_validate(quest_id, artifact_ref):
    """Language-hygiene gate (validate_manuscript_language). With --artifact-ref it scans the
    manuscript for loop-internal/process wording (route/handoff/worktree/notifier/self-wakeup/"the user
    requested"/"paper restart"/batch-arithmetic/TODO) and FAILS on any hit; without --artifact-ref it stays
    advisory (lists the forbidden terms). Matching is word/substring, case-insensitive, line-located."""
    text = _read_artifact_text(artifact_ref)
    if text is None:
        emit(envelope("manuscript validate", ok=True, quest_id=quest_id,
                      data={"forbidden_terms": _MANUSCRIPT_FORBIDDEN, "artifact_ref": artifact_ref,
                            "note": "advisory: pass --artifact-ref <manuscript path> to enforce the scan"}))
        return
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        low = line.lower()
        for term in _MANUSCRIPT_FORBIDDEN:
            if term in low:
                hits.append({"line": i, "term": term, "context": line.strip()[:160]})
    ok = not hits
    emit(envelope("manuscript validate", ok=ok, quest_id=quest_id,
                  data={"hits": hits, "hit_count": len(hits), "artifact_ref": artifact_ref,
                        "forbidden_terms": _MANUSCRIPT_FORBIDDEN},
                  diagnostics=[] if ok else [f"{len(hits)} loop/process-jargon hit(s) in paper-facing prose"]))
    if not ok:
        sys.exit(1)


@manuscript.command("coverage")
@click.option("--quest-id", required=True)
@click.option("--artifact-ref", default=None, help="Manuscript markdown/tex to scan (paper-facing prose).")
@click.option("--spine-ref", default=None, help="Typed paper-spine JSON (else read from the paper_spine row).")
@click.option("--at", default=None, help="Caller-supplied ISO-8601 timestamp stamped onto the coverage verdict.")
@click.pass_context
def manuscript_coverage(ctx, quest_id, artifact_ref, spine_ref, at):
    """Validator-COMPUTED submission readiness (the finalize coverage gate's input). Computes submission_ready
    from: the typed paper-spine validates; every main_claim resolves to a claim row WITH supporting evidence;
    no 'supported' claim lacks evidence; no result row is unmapped (each referenced by claim_evidence
    source_kind='result'); not_claiming + weak_points/limitations present; the manuscript names each main claim
    and carries no process/draft traces (language firewall); display_plan present. WRITES submission_ready +
    coverage_json onto the paper_spine row — the Writer can NEVER self-certify it. Exits non-zero when not ready."""
    conn = _conn(ctx)
    spine = _load_spine(ctx, quest_id, spine_ref)
    reasons = []
    if spine is None:
        reasons.append("no paper-spine found (record paper_spine.upsert + write the typed spine.json first)")
    else:
        try:
            jsonschema.validate(spine, _SPINE_CONTENT_SCHEMA)
        except jsonschema.ValidationError as e:
            reasons.append(f"spine invalid: {e.message}")
    claim_status = {r[0]: r[1] for r in conn.execute(
        "SELECT claim_id, status FROM claim WHERE quest_id=?", (quest_id,))}
    supported_ev = {r[0] for r in conn.execute(
        "SELECT DISTINCT e.claim_id FROM claim_evidence e JOIN claim c ON c.claim_id=e.claim_id "
        "WHERE c.quest_id=? AND e.relation='supports'", (quest_id,))}
    main_claims = (spine.get("main_claims") if spine else []) or []
    for c in main_claims:
        cid = c.get("claim_id")
        if cid not in claim_status:
            reasons.append(f"main claim {cid!r} has no claim row (record claim.upsert)")
        elif cid not in supported_ev:
            reasons.append(f"main claim {cid!r} has no supporting claim_evidence")
    unsupported = conn.execute(
        "SELECT COUNT(*) FROM claim c WHERE c.quest_id=? AND c.status='supported' AND NOT EXISTS "
        "(SELECT 1 FROM claim_evidence e WHERE e.claim_id=c.claim_id AND e.relation='supports')",
        (quest_id,)).fetchone()[0]
    if unsupported:
        reasons.append(f"{unsupported} 'supported' claim(s) lack supporting evidence")
    unmapped = conn.execute(
        "SELECT COUNT(*) FROM result r WHERE r.quest_id=? AND NOT EXISTS "
        "(SELECT 1 FROM claim_evidence e WHERE e.source_kind='result' AND e.source_ref=r.result_id)",
        (quest_id,)).fetchone()[0]
    if unmapped:
        reasons.append(f"{unmapped} result row(s) not mapped to any claim (claim_evidence source_kind='result')")
    if spine and not spine.get("not_claiming"):
        reasons.append("not_claiming boundary is empty")
    has_limitation = conn.execute(
        "SELECT COUNT(*) FROM claim WHERE quest_id=? AND kind='limitation'", (quest_id,)).fetchone()[0]
    if spine and not (spine.get("weak_points") or has_limitation):
        reasons.append("no limitations / weak_points recorded")
    if spine and not spine.get("display_plan"):
        reasons.append("display_plan is empty")
    text = _read_artifact_text(artifact_ref)
    if artifact_ref and text is None:
        reasons.append(f"manuscript not readable at {artifact_ref}")
    if text is not None:
        low = text.lower()
        traces = sorted({t for t in _MANUSCRIPT_FORBIDDEN if t in low})
        if traces:
            reasons.append(f"process/draft traces in manuscript prose: {traces}")
        missing_claims = [c.get("claim_id") for c in main_claims
                          if c.get("claim_id") and str(c.get("claim_id")).lower() not in low
                          and str(c.get("scope", ""))[:24].lower() not in low]
        if missing_claims:
            reasons.append(f"main claim(s) not stated in the manuscript: {missing_claims}")
    elif spine is not None:
        reasons.append("no manuscript --artifact-ref provided to scan for coverage/traces")
    ready = not reasons
    coverage = {"submission_ready": ready, "reasons": reasons,
                "n_main_claims": len(main_claims), "unmapped_results": unmapped, "at": at}
    fp = records.dep_fingerprint(conn, quest_id, "manuscript") if ready else None  # staleness signature
    written = conn.execute(
        "UPDATE paper_spine SET submission_ready=?, coverage_json=?, coverage_at=?, validated_fingerprint=?, "
        "updated_at=COALESCE(?, updated_at) WHERE quest_id=?",
        (1 if ready else 0, json.dumps(coverage), at, fp, at, quest_id)).rowcount
    conn.commit()
    conn.close()
    if not written:
        coverage["note"] = "no paper_spine row to write submission_ready onto (record paper_spine.upsert first)"
    emit(envelope("manuscript coverage", ok=ready, quest_id=quest_id, data=coverage,
                  diagnostics=[] if ready else ["manuscript not submission_ready: " + "; ".join(reasons)]))
    if not ready:
        sys.exit(1)


@manuscript.command("polish")
@_opts
@click.pass_context
def manuscript_polish(ctx, quest_id, artifact_id, ref, input_path, title, at):
    """Polish manuscript prose via the enabled template adapter (style only; no new claims)."""
    _run_adapter(ctx, "manuscript polish", adapter_kind="template", entry_default="generate", quest_id=quest_id,
                 artifact_id=artifact_id, ref=ref, input_path=input_path, params={"title": title},
                 artifact_kind="report", at=at)


@manuscript.command("datastmt")
@_opts
@click.pass_context
def manuscript_datastmt(ctx, quest_id, artifact_id, ref, input_path, title, at):
    """Generate a Data Availability statement via the enabled template adapter (drafts only from inventory)."""
    _run_adapter(ctx, "manuscript datastmt", adapter_kind="template", entry_default="generate", quest_id=quest_id,
                 artifact_id=artifact_id, ref=ref, input_path=input_path, params={"title": title},
                 artifact_kind="report", at=at)


@manuscript.command("bundle")
@click.option("--quest-id", required=True)
@click.option("--out-dir", required=True, help="Directory to write the submission bundle into.")
@click.pass_context
def manuscript_bundle(ctx, quest_id, out_dir):
    """Emit a submission bundle from durable state: evidence_ledger.md,
    claim_evidence_map.json, and submission_checklist.md (read-only over the DB; writes files only)."""
    import json as _json
    from paths import LOOP_DIR
    from pathlib import Path
    conn = _conn(ctx)
    claims = db.rows(conn, "SELECT claim_id,status,statement FROM claim WHERE quest_id=?", (quest_id,))
    ev = db.rows(conn, "SELECT claim_id,source_kind,source_ref,resolved FROM claim_evidence WHERE claim_id IN "
                       "(SELECT claim_id FROM claim WHERE quest_id=?)", (quest_id,))
    analyses = db.rows(conn, "SELECT analysis_id,round_index,verdict,finding FROM analysis WHERE quest_id=? ORDER BY round_index", (quest_id,))
    refs = db.rows(conn, "SELECT reference_id,cite_key,title,uri FROM reference WHERE quest_id=?", (quest_id,))
    arts = db.rows(conn, "SELECT artifact_id,kind,ref FROM artifact WHERE quest_id=?", (quest_id,))
    conn.close()
    out_abs = Path(out_dir if out_dir.startswith("/") else str(LOOP_DIR / out_dir))
    out_abs.mkdir(parents=True, exist_ok=True)
    # claim_evidence_map.json
    cmap = {c["claim_id"]: {"status": c["status"], "statement": c.get("statement"),
                            "evidence": [{"kind": e["source_kind"], "ref": e["source_ref"], "resolved": e["resolved"]}
                                         for e in ev if e["claim_id"] == c["claim_id"]]} for c in claims}
    (out_abs / "claim_evidence_map.json").write_text(_json.dumps(cmap, indent=2), encoding="utf-8")
    # evidence_ledger.md
    el = ["# Evidence ledger — quest %s" % quest_id, "", "## Claims", ""]
    for c in claims:
        el.append(f"- **{c['claim_id']}** [{c['status']}] — {(c.get('statement') or '')[:200]}")
        for e in [e for e in ev if e["claim_id"] == c["claim_id"]]:
            el.append(f"  - evidence: `{e['source_kind']}:{e['source_ref']}`{' (resolved)' if e['resolved'] else ''}")
    el += ["", "## Analyses", ""]
    for a in analyses:
        el.append(f"- `{a['analysis_id']}` (round {a['round_index']}) → **{a['verdict']}** — {(a.get('finding') or '')[:160]}")
    el += ["", "## References", ""] + [f"- `{r.get('cite_key') or r['reference_id']}` — {r.get('title') or ''} {r.get('uri') or ''}" for r in refs]
    (out_abs / "evidence_ledger.md").write_text("\n".join(el) + "\n", encoding="utf-8")
    # submission_checklist.md (auto-derived booleans)
    supported = [c for c in claims if c["status"] == "supported"]
    orphan = [c for c in supported if not any(e["claim_id"] == c["claim_id"] for e in ev)]
    figs = [a for a in arts if a["kind"] == "figure"]
    pdf = [a for a in arts if str(a["ref"]).endswith(".pdf")]
    zh = [a for a in arts if str(a["ref"]).endswith("-zh.pdf")]
    en = [a for a in pdf if a not in zh]
    def box(b): return "[x]" if b else "[ ]"
    cl = ["# Submission checklist — quest %s" % quest_id, "",
          f"- {box(claims)} Claims recorded ({len(claims)}; {len(supported)} supported)",
          f"- {box(not orphan)} Every supported claim has ≥1 evidence link" + (f" — ORPHANS: {[c['claim_id'] for c in orphan]}" if orphan else ""),
          f"- {box(figs)} Figures present ({len(figs)})",
          f"- {box(en)} Compiled PDF (English) present ({len(en)})",
          f"- {box(zh)} Chinese edition (paper-zh.pdf) present ({len(zh)})",
          f"- {box(refs)} References / bibliography ({len(refs)})",
          f"- {box(analyses)} Analyses recorded ({len(analyses)})",
          "- [ ] External venue formatting (apply template at submission time)"]
    (out_abs / "submission_checklist.md").write_text("\n".join(cl) + "\n", encoding="utf-8")
    emit(envelope("manuscript bundle", quest_id=quest_id,
                  data={"out_dir": out_dir, "files": ["evidence_ledger.md", "claim_evidence_map.json", "submission_checklist.md"],
                        "claims": len(claims), "supported": len(supported), "orphan_supported": len(orphan),
                        "figures": len(figs), "pdf_artifacts": len(pdf), "pdf_en": len(en), "pdf_zh": len(zh),
                        "references": len(refs), "analyses": len(analyses)}))


@cli.group()
def knowledge(): ...


@knowledge.command("query")
@click.option("--quest-id", default=None)
@click.option("--kind", default=None)
@click.option("--domain", default=None)
@click.option("--enabled-only/--all", default=True)
@click.pass_context
def knowledge_query(ctx, quest_id, kind, domain, enabled_only):
    conn = _conn(ctx)
    cond, params = [], []
    if enabled_only: cond.append("enabled=1")
    if kind: cond.append("kind=?"); params.append(kind)
    if domain: cond.append("domain=?"); params.append(domain)
    sql = "SELECT pack_id,domain,name,kind,ref,enabled,priority FROM knowledge_pack"
    if cond: sql += " WHERE " + " AND ".join(cond)
    sql += " ORDER BY domain,kind,priority"
    data = db.rows(conn, sql, tuple(params)); conn.close()
    emit(envelope("knowledge query", quest_id=quest_id, data={"packs": data, "count": len(data)}))


@knowledge.command("cards")
@click.option("--quest-id", default=None)
@click.option("--domain", default=None)
@click.option("--query", "query", default=None)
@click.pass_context
def knowledge_cards(ctx, quest_id, domain, query):
    """Aggregate cards from enabled reference packs (e.g. science-scipkg, mentor-standards)."""
    import json as _json
    from paths import LOOP_DIR
    conn = _conn(ctx)
    cond = ["enabled=1", "kind='reference'"]
    p = []
    if domain:
        cond.append("domain=?"); p.append(domain)
    packs = db.rows(conn, "SELECT pack_id,domain,ref FROM knowledge_pack WHERE " + " AND ".join(cond), tuple(p))
    conn.close()
    out = []
    for pk in packs:
        ref = pk["ref"]
        pdir = (LOOP_DIR / ref) if not str(ref).startswith("/") else __import__("pathlib").Path(ref)
        cards = []
        try:
            mod, _ = _load_adapter(pk)
            if mod and hasattr(mod, "cards"):
                cards = mod.cards(query=query, quest_id=quest_id)
            elif (pdir / "catalog.json").exists():
                cards = _json.loads((pdir / "catalog.json").read_text())
        except Exception as e:
            cards = [{"error": str(e)}]
        if query and cards:
            ql = query.lower()
            cards = [c for c in cards if ql in _json.dumps(c).lower()]
        out.append({"pack": pk["pack_id"], "domain": pk["domain"], "cards": cards, "count": len(cards)})
    emit(envelope("knowledge cards", quest_id=quest_id, data={"sources": out,
                                                              "total_cards": sum(s["count"] for s in out)}))


# ───────────────── control ─────────────────
@cli.group()
def control(): ...


@control.command("status")
@click.option("--quest-id", default=None)
@click.pass_context
def control_status(ctx, quest_id):
    conn = _conn(ctx)
    sql = "SELECT quest_id,run_state,execution_mode,autonomy_mode,rigor_level,round_index,current_stage,baseline_gate FROM quest"
    quests = db.rows(conn, sql + (" WHERE quest_id=?" if quest_id else ""), (quest_id,) if quest_id else ())
    pending = db.rows(conn, "SELECT quest_id,COUNT(*) AS open_handoffs FROM handoff WHERE status NOT IN ('processed','failed') GROUP BY quest_id")
    conn.close()
    emit(envelope("control status", quest_id=quest_id, data={"quests": quests, "pending_handoffs": pending}))


@control.command("get-mode")
@click.option("--quest-id", required=True)
@click.pass_context
def control_get_mode(ctx, quest_id):
    conn = _conn(ctx)
    row = conn.execute("SELECT execution_mode FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    conn.close()
    emit(envelope("control get-mode", quest_id=quest_id, data={"execution_mode": row[0] if row else "auto", "source": "quest" if row else "default"}))


def _control_change(ctx, cmd, quest_id, kind, at, quest_updates, detail=None):
    try:
        conn = _conn(ctx)
        if quest_updates:
            records.apply(conn, {"record_type": "quest.update", "record_id": quest_id, "at": at, **quest_updates})
        records.apply(conn, {"record_type": "operator_event.record", "record_id": f"{quest_id}:{kind}:{at}",
                             "at": at, "quest_id": quest_id, "kind": kind, **({"detail": detail} if detail else {})})
    except records.RecordError as e:
        emit(envelope(cmd, ok=False, diagnostics=[str(e)])); sys.exit(1)
    _finish(ctx, conn, cmd, {"applied": kind, **quest_updates}, quest_id=quest_id)


@control.command("set-mode")
@click.option("--quest-id", required=True)
@click.option("--mode", default=None, type=click.Choice(["auto", "manual"]), help="execution_mode (drive cadence) — unchanged axis.")
@click.option("--autonomy", default=None, type=click.Choice(["auto", "assistant"]), help="autonomy_mode (authority/strictness) — orthogonal to --mode.")
@click.option("--at", required=True)
@click.pass_context
def control_set_mode(ctx, quest_id, mode, autonomy, at):
    """Set the execution-mode (--mode auto|manual) and/or the run mode (--autonomy auto|assistant). The two are
    independent axes; at least one must be supplied."""
    if not mode and not autonomy:
        emit(envelope("control set-mode", ok=False, quest_id=quest_id,
                      diagnostics=["supply --mode and/or --autonomy"])); sys.exit(1)
    updates = {}
    if mode:
        updates["execution_mode"] = mode
    if autonomy:
        updates["autonomy_mode"] = autonomy
    _control_change(ctx, "control set-mode", quest_id, "set-mode", at, updates)


@control.command("pause")
@click.option("--quest-id", required=True)
@click.option("--at", required=True)
@click.pass_context
def control_pause(ctx, quest_id, at):
    _control_change(ctx, "control pause", quest_id, "pause", at, {"run_state": "paused"})


@control.command("resume")
@click.option("--quest-id", required=True)
@click.option("--recovering", is_flag=True)
@click.option("--at", required=True)
@click.pass_context
def control_resume(ctx, quest_id, recovering, at):
    _control_change(ctx, "control resume", quest_id, "resume", at, {"run_state": "recovering" if recovering else "running"})


@control.command("stop")
@click.option("--quest-id", required=True)
@click.option("--reason", default=None)
@click.option("--at", required=True)
@click.pass_context
def control_stop(ctx, quest_id, reason, at):
    upd = {"run_state": "stopped"}
    if reason:
        upd["stop_reason"] = reason
    _control_change(ctx, "control stop", quest_id, "stop", at, upd, detail=reason)


@control.command("manual-context")
@click.option("--quest-id", required=True)
@click.pass_context
def control_manual_context(ctx, quest_id):
    conn = _conn(ctx)
    q = conn.execute("SELECT run_state,execution_mode,plan_revision FROM quest WHERE quest_id=?", (quest_id,)).fetchone()
    pend = db.rows(conn, "SELECT handoff_id,status FROM handoff WHERE quest_id=? AND status NOT IN ('processed','failed')", (quest_id,))
    conn.close()
    emit(envelope("control manual-context", quest_id=quest_id,
                  data={"run_state": q["run_state"] if q else None, "execution_mode": q["execution_mode"] if q else "auto",
                        "plan_revision": q["plan_revision"] if q else None, "pending_handoffs": pend,
                        "stop_after_one_pass": True}))


# ───────────────── selfcheck ─────────────────
@cli.command("selfcheck")
def selfcheck():
    import importlib
    data = {"deps": {}, "record_types": {}, "invariants": {}, "ok": True}
    for m in ("click", "jinja2", "jsonschema", "tomllib"):
        try:
            importlib.import_module(m); data["deps"][m] = "ok"
        except Exception as e:
            data["deps"][m] = f"MISSING: {e}"; data["ok"] = False
    idx = set(records.type_index())
    mapped = set(records.RECORD_MAP)
    missing_map = sorted(idx - mapped)
    extra_map = sorted(mapped - idx)
    data["record_types"] = {"schemas": len(idx), "mapped": len(mapped),
                            "unmapped_schema_types": missing_map, "map_without_schema": extra_map}
    if missing_map or extra_map:
        data["ok"] = False
    data["invariants"]["count"] = len(inv.load())
    emit(envelope("selfcheck", ok=data["ok"], data=data,
                  diagnostics=[] if data["ok"] else ["selfcheck found gaps"]))
    if not data["ok"]:
        sys.exit(1)


# ───────────────── gpu (operator-confirmed compute) ─────────────────
@cli.group()
def gpu(): ...


@gpu.command("status")
@click.option("--quest-id", required=True)
@click.pass_context
def gpu_status(ctx, quest_id):
    conn = _conn(ctx)
    try:
        rows = db.rows(conn, "SELECT quest_id,status,devices,confirmed_by,confirmed_at,note FROM gpu_allocation WHERE quest_id=?", (quest_id,))
    except Exception:
        rows = []
    conn.close()
    alloc = rows[0] if rows else {"quest_id": quest_id, "status": "pending", "devices": None}
    confirmed = alloc.get("status") == "confirmed" and bool(alloc.get("devices"))
    emit(envelope("gpu status", quest_id=quest_id,
                  data={"confirmed": confirmed, "devices": alloc.get("devices"), "allocation": alloc}))


@gpu.command("confirm")
@click.option("--quest-id", required=True)
@click.option("--devices", required=True, help="CUDA device set the quest's experiments may use; comma list e.g. '0' or '0,1'.")
@click.option("--by", "confirmed_by", default="operator", help="operator identity confirming the allocation")
@click.option("--note", default=None)
@click.option("--at", required=True)
@click.pass_context
def gpu_confirm(ctx, quest_id, devices, confirmed_by, note, at):
    p = {"record_type": "gpu.confirm", "record_id": quest_id, "at": at,
         "devices": devices, "confirmed_by": confirmed_by}
    if note:
        p["note"] = note
    _apply(ctx, "gpu confirm", p, quest_id=quest_id)


def main():
    cli()


if __name__ == "__main__":
    main()
