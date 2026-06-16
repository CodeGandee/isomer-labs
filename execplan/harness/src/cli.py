"""DeepResearch harness CLI (click). Groups mirror commands.toml. State writes go through records.apply.

Stub-safe domain-pluggable commands (experiment run, metric validate, render *, bo, lit search, git
checkpoint/status, manuscript/outline validate) return ok with data.stub=true and do only the minimal
state writes their contract promises; a domain knowledge-pack adapter replaces the stub later.
"""
from __future__ import annotations
import json
import sys
import click

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
@click.pass_context
def cli(ctx, db_path, vaw):
    ctx.obj = {"db": db_path, "vaw": vaw}


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


# ───────────────── plan (DB-rendered living research map; Phases 2/3/6) ─────────────────
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
    """Warn on consequential decisions that did not name their losers (Phase 4; read-only)."""
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
    """Advisory (Tier-3 methodology-usage): for a quest under the research-contract regime, warn when a CLOSED
    round whose stage requires a methodology pack (records.REQUIRED_PACKS) has no artifact(kind='methodology-
    usage') for that round_index. Existence check only — per-pack correctness is enforced by the Orchestrator/
    Reviewer reading task-result.methodology_used. Pre-regime quests (no research-contract artifact) are exempt,
    so history (q1/q2/q3) never warns. Read-only; never an invariant (so `state validate` stays unaffected)."""
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
    """List recorded acceptance revisions (acceptance.md@rev-*) and confirmed amendment decisions (Phase 6)."""
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


# ───────────────── completeness (research-completeness audit; Phase 5) ─────────────────
@cli.group()
def completeness(): ...


@completeness.command("audit")
@click.option("--quest-id", required=True)
@click.pass_context
def completeness_audit_cmd(ctx, quest_id):
    """Run the seven research-completeness checks (Phase 5). Advisory by default; the finalize gate enforces
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


# ───────────────── bo (core, lightweight) ─────────────────
@cli.group()
def bo(): ...


@bo.command("suggest")
@click.option("--quest-id", required=True)
@click.option("--space-id", default=None)
@click.pass_context
def bo_suggest(ctx, quest_id, space_id):
    conn = _conn(ctx)
    dims = db.rows(conn, "SELECT * FROM search_space WHERE quest_id=?" + (" AND space_id=?" if space_id else ""),
                   (quest_id, space_id) if space_id else (quest_id,))
    nobs = conn.execute("SELECT COUNT(*) FROM experiment_param p JOIN experiment e ON e.experiment_id=p.experiment_id WHERE e.quest_id=?", (quest_id,)).fetchone()[0]
    conn.close()
    if not dims:
        emit(envelope("bo suggest", ok=True, quest_id=quest_id,
                      data={"suggestion": None, "note": "no search_space; use heuristic idea selection"},
                      warnings=["no search space defined"]))
        return
    # Lightweight default proposal: midpoint for real/int dims (a real adapter replaces this).
    sug = {}
    for d in dims:
        if d["dim_kind"] in ("real", "int") and d["low"] is not None and d["high"] is not None:
            mid = (d["low"] + d["high"]) / 2
            sug[d["dim_name"]] = int(mid) if d["dim_kind"] == "int" else mid
    emit(envelope("bo suggest", quest_id=quest_id,
                  data={"stub": True, "strategy": "midpoint-default", "observations": nobs, "suggestion": sug}))


@bo.command("status")
@click.option("--quest-id", required=True)
@click.pass_context
def bo_status(ctx, quest_id):
    conn = _conn(ctx)
    best = conn.execute(
        "SELECT MAX(m.value_num) FROM measurement m JOIN result r ON r.result_id=m.result_id "
        "WHERE r.quest_id=? AND m.is_primary=1", (quest_id,)).fetchone()[0]
    conn.close()
    emit(envelope("bo status", quest_id=quest_id, data={"best_primary": best}))


# ───────────────── lit (core; search stubbed) ─────────────────
@cli.group()
def lit(): ...


@lit.command("search")
@click.option("--query", required=True)
def lit_search(query):
    emit(envelope("lit search", data={"stub": True, "query": query, "results": [],
                                      "note": "wire a web/arxiv backend or knowledge-pack to populate results"}))


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
    entries = []
    for i, r in enumerate(rows, 1):
        k = key(r, i)
        title = (r.get("title") or r.get("reference_id") or "Untitled").replace("{", "").replace("}", "")
        url = r.get("uri") or ""
        etype = "misc"
        entries.append(f"@{etype}{{{k},\n  title = {{{title}}},\n  howpublished = {{\\url{{{url}}}}},\n  note = {{source: {r.get('source','manual')}}}\n}}")
    bib = "% Generated by `deepresearch lit bib` from recorded reference rows.\n\n" + "\n\n".join(entries) + "\n"
    out_abs = out_path if out_path.startswith("/") else str(LOOP_DIR / out_path)
    Path(out_abs).parent.mkdir(parents=True, exist_ok=True)
    Path(out_abs).write_text(bib, encoding="utf-8")
    emit(envelope("lit bib", quest_id=quest_id, data={"out_path": out_path, "entries": len(entries),
                                                       "cite_keys": [key(r, i) for i, r in enumerate(rows, 1)]}))


@lit.command("audit")
@click.option("--quest-id", required=True)
@click.pass_context
def lit_audit(ctx, quest_id):
    """Scholarship-bar audit (Upgrade 1): checks the quest meets the literature bar — enough real reference
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
    conn = _conn(ctx)
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
    knowledge_pack(kind='validator') adapter can supersede this with a domain correctness gate."""
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
    cur = conn.execute("UPDATE result SET validity=? WHERE result_id=?", (computed, result_id))
    conn.commit()
    _finish(ctx, conn, "result validate",
            {"result_id": result_id, "validity": computed, "source": "override" if validity else "computed",
             "reasons": reasons, "quest_id": quest_id}, quest_id=quest_id)


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


@render.command("report")
@_opts
@click.pass_context
def render_report(ctx, quest_id, artifact_id, ref, input_path, title, at):
    _run_adapter(ctx, "render report", adapter_kind="compiler", entry_default="render", quest_id=quest_id,
                 artifact_id=artifact_id, ref=ref, input_path=input_path, params={"title": title},
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
@click.pass_context
def render_plot(ctx, quest_id, artifact_id, ref, input_path, title, at):
    """Publication-quality plot; consumes the enabled compiler adapter (e.g. paper-plot)."""
    _run_adapter(ctx, "render plot", adapter_kind="compiler", entry_default="render", quest_id=quest_id,
                 artifact_id=artifact_id, ref=ref, input_path=input_path, params={"title": title},
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


# Outline-contract markers (paper-craft/references/outline-contract.md). Each check passes if ANY of its
# tokens appears in the outline artifact (JSON field name or prose heading) — tolerant of md or json shape.
_OUTLINE_CHECKS = {
    "paper_idea":          ("central_thesis", "working_title", "paper idea", "story_spine", "thesis"),
    "scoped_claims":       ("core_claims", "scoped claim", "scope", "claim"),
    "method_abstraction":  ("method_abstraction", "method abstraction", "mechanism_steps", "intuition"),
    "evaluation_plan":     ("evaluation_plan", "evaluation plan", "analysis_plan", "baselines", "evaluation/analysis"),
    "evidence_boundaries": ("evidence_grounding", "must_not_claim", "evidence boundaries", "evidence_view", "evidence-view"),
}


@outline.command("validate")
@click.option("--quest-id", default=None)
@click.option("--artifact-ref", default=None, help="Path to the outline artifact (loop-relative) to validate.")
def outline_validate(quest_id, artifact_ref):
    """Structural pre-write gate (DeepScientist validate_academic_outline). With --artifact-ref it parses the
    outline and checks for a single paper idea, scoped claims, a method abstraction, an evaluation/analysis
    plan, and explicit evidence boundaries; falsification criteria are a soft warning. Without --artifact-ref
    it stays advisory (lists the checks)."""
    text = _read_artifact_text(artifact_ref)
    if text is None:
        emit(envelope("outline validate", ok=True, quest_id=quest_id,
                      data={"checks": list(_OUTLINE_CHECKS), "artifact_ref": artifact_ref,
                            "note": "advisory: pass --artifact-ref <outline path> to enforce the contract"}))
        return
    low = text.lower()
    results = {name: any(tok in low for tok in toks) for name, toks in _OUTLINE_CHECKS.items()}
    missing = [n for n, ok in results.items() if not ok]
    warnings = [] if ("what_would_falsify" in low or "falsif" in low) else ["no falsification criteria found (what_would_falsify_it)"]
    ok = not missing
    emit(envelope("outline validate", ok=ok, quest_id=quest_id,
                  data={"checks": results, "missing": missing, "artifact_ref": artifact_ref},
                  warnings=warnings, diagnostics=[] if ok else [f"outline missing required elements: {missing}"]))
    if not ok:
        sys.exit(1)


@cli.group()
def manuscript(): ...


# Loop/operator jargon that must never surface in paper-facing prose (DeepScientist validate_manuscript_language).
_MANUSCRIPT_FORBIDDEN = ["route", "handoff", "worktree", "lane", "notifier", "self-wakeup",
                         "the user requested", "paper restart", "this quest", "64 + 64", "64+64", "todo"]


@manuscript.command("validate")
@click.option("--quest-id", default=None)
@click.option("--artifact-ref", default=None, help="Path to the manuscript artifact (loop-relative) to scan.")
def manuscript_validate(quest_id, artifact_ref):
    """Language-hygiene gate (DeepScientist validate_manuscript_language). With --artifact-ref it scans the
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
    """Emit a DeepScientist-style submission bundle from durable state: evidence_ledger.md,
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
