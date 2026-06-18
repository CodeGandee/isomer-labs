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
@click.option("--bib", default=None, help="Path to a .bib (enables a real BibTeX pass via the compiler adapter).")
@click.option("--venue", default=None, help="Venue template to compile against (e.g. iclr2026; see paper-latex/templates/).")
@click.pass_context
def render_report(ctx, quest_id, artifact_id, ref, input_path, title, at, bib, venue):
    params = {"title": title}
    if bib:
        params["bib"] = bib if bib.startswith("/") else str(LOOP_DIR / bib)
    if venue:
        params["venue"] = venue
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
        "novelty_waiver": {"type": "string"}
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
        "SELECT select_id, select_ref, valid FROM idea_select WHERE quest_id=? "
        "ORDER BY created_at DESC, select_id DESC LIMIT 1", (quest_id,)).fetchone()


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
        if novelty == "not_differentiated" and not (content.get("novelty_waiver")
                                                    or os.environ.get("DEEPRESEARCH_IDEA_NOVELTY_WAIVER")):
            reasons.append("novelty_label='not_differentiated' (decorative tweak): add real differentiation "
                           "or an explicit novelty_waiver")
    valid = not reasons
    conn.execute("UPDATE idea_select SET valid=?, gate_score=?, retained_candidate=?, novelty_label=? "
                 "WHERE select_id=?", (1 if valid else 0, score, retained_id, novelty, row["select_id"]))
    conn.commit(); conn.close()
    emit(envelope("idea validate", ok=valid, quest_id=quest_id,
                  data={"valid": valid, "rigor": rigor, "floors": floors, "retained": retained_id,
                        "gate_score": score, "novelty_label": novelty, "reasons": reasons},
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
        "SELECT bridge_id, bridge_ref, valid FROM analysis_bridge WHERE quest_id=? "
        "ORDER BY created_at DESC, bridge_id DESC LIMIT 1", (quest_id,)).fetchone()


def _claim_coverage(conn, quest_id, floors):
    """Per-main-claim empirical coverage by evidence_kind under the rigor floor. Returns (ok, reasons, detail).
    Main claims = claim rows of kind='claim' in status open/supported. baseline satisfied if the claim has a
    baseline_comparison evidence OR the quest's baseline_gate is 'waived'."""
    reasons, detail = [], {}
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
        kinds = {r[0] for r in conn.execute(
            "SELECT evidence_kind FROM claim_evidence WHERE claim_id=? AND relation='supports' "
            "AND evidence_kind IS NOT NULL", (cid,))}
        detail[cid] = sorted(kinds)
        gaps = []
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
    conn.execute("UPDATE analysis_bridge SET valid=?, coverage_json=? WHERE bridge_id=?",
                 (1 if valid else 0, json.dumps(coverage), row["bridge_id"]))
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
        "SELECT verdict_id, verdict, verdict_ref, valid, operator_confirmed, route_target "
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
    conn.execute("UPDATE review_verdict SET valid=?, route_target=? WHERE verdict_id=?",
                 (1 if valid else 0, target, row["verdict_id"]))
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
@cli.group()
def gate(): ...


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
    authoritative (this does NOT replace them). Each gate: status(pass|fail|advisory|not_applicable|missing),
    rigor_level, blocking, reason, latest_record_ref, route_target, required_next_action."""
    conn = _conn(ctx)
    q = conn.execute("SELECT rigor_level, baseline_gate, best_result_ref FROM quest WHERE quest_id=?",
                     (quest_id,)).fetchone()
    if not q:
        conn.close(); emit(envelope("gate status", ok=False, quest_id=quest_id, diagnostics=["no such quest"])); sys.exit(1)
    rigor = q["rigor_level"] or "standard"
    bound = _is_bound(conn, quest_id, rigor)
    adv = not bound
    floors = _gate_floors(rigor)
    gates = {}

    def put(name, status, reason="", route=None, ref=None, action=None):
        gates[name] = {"status": status, "rigor_level": rigor, "blocking": bool(bound and status == "fail"),
                       "reason": reason, "latest_record_ref": ref, "route_target": route,
                       "required_next_action": action}

    r = _latest_idea_select_row(conn, quest_id)
    if adv: put("idea_gate", "advisory")
    elif r is None: put("idea_gate", "missing", "no idea.select", "idea", None, "record idea.select + idea validate")
    elif r["valid"]: put("idea_gate", "pass", ref=r["select_id"])
    else: put("idea_gate", "fail", "idea selection not validated", "idea", r["select_id"], "fix + idea validate")

    bc = conn.execute("SELECT contract_id, verification_verdict, waiver_reason FROM baseline_contract "
                      "WHERE quest_id=? ORDER BY created_at DESC, contract_id DESC LIMIT 1", (quest_id,)).fetchone()
    if adv: put("baseline_contract", "advisory")
    elif q["baseline_gate"] in ("pending", "blocked") and bc is None:
        put("baseline_contract", "not_applicable", "baseline not yet established")
    elif bc is None:
        put("baseline_contract", "fail", "baseline_gate set without a baseline.contract", "baseline", None, "record baseline.contract")
    else:
        v = bc["verification_verdict"]
        okc = (v in _OK_BASELINE_V) or (v == "waived" and (bc["waiver_reason"] or "").strip())
        put("baseline_contract", "pass" if okc else "fail", "" if okc else f"verdict {v!r} not acceptable",
            None if okc else "baseline", bc["contract_id"], None if okc else "record an acceptable baseline.contract")

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
    elif ab["valid"]: put("analysis_bridge", "pass", ref=ab["bridge_id"])
    else: put("analysis_bridge", "fail", "analysis bridge not validated", "analysis", ab["bridge_id"], "campaign validate")

    sp = conn.execute("SELECT submission_ready FROM paper_spine WHERE quest_id=?", (quest_id,)).fetchone()
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
        put("manuscript_coverage", "pass" if ready else "fail",
            "" if ready else "submission_ready not validator-confirmed", None if ready else "write", None,
            None if ready else "resolve gaps + manuscript coverage")

    rv = _latest_verdict_row(conn, quest_id)
    if adv: put("review_verdict", "advisory")
    elif rv is None: put("review_verdict", "missing", "no review verdict", "review", None, "record review.verdict + review validate")
    else:
        v, valid, conf, rt = rv["verdict"], rv["valid"], rv["operator_confirmed"], rv["route_target"]
        if not valid: put("review_verdict", "fail", "verdict not validated/actionable", "review", rv["verdict_id"], "review validate")
        elif v == "accept": put("review_verdict", "pass", ref=rv["verdict_id"])
        elif v == "reject": put("review_verdict", "fail", "verdict is reject", rt or "write", rv["verdict_id"], "route follow-ups + re-review")
        elif records._rigor_order(rigor) >= records._rigor_order("publication"):
            put("review_verdict", "fail", "borderline not allowed at publication", rt or "write", rv["verdict_id"], "revise to accept")
        elif conf: put("review_verdict", "pass", ref=rv["verdict_id"])
        else: put("review_verdict", "fail", "borderline needs operator confirmation", rt or "write", rv["verdict_id"], "review confirm")

    fin = []
    if not adv:
        if gates["manuscript_coverage"]["status"] != "pass": fin.append("manuscript coverage not ready")
        if gates["review_verdict"]["status"] != "pass": fin.append("review not accepted")
        try:
            if not records.scholarship_audit(conn, quest_id)["ok"]: fin.append("scholarship bar unmet")
        except Exception:
            pass
        best = q["best_result_ref"]
        if best:
            backed = conn.execute("SELECT COUNT(*) FROM claim_evidence e JOIN claim c ON c.claim_id=e.claim_id "
                                  "WHERE c.quest_id=? AND e.source_kind='result' AND e.source_ref=? "
                                  "AND e.relation='supports'", (quest_id, best)).fetchone()[0]
            if not backed: fin.append("headline result not claim-backed (authenticity)")
    if adv: put("finalize_readiness", "advisory")
    elif fin: put("finalize_readiness", "fail", "; ".join(fin), None, None, "resolve blocking gates above")
    else: put("finalize_readiness", "pass")

    conn.close()
    emit(envelope("gate status", ok=True, quest_id=quest_id,
                  data={"rigor_level": rigor, "bound": bound, "gates": gates,
                        "finalize_readiness": gates["finalize_readiness"]["status"],
                        "blocking_gates": [k for k, gv in gates.items() if gv["blocking"]]}))


# stage -> (table, id column, ref column) the methodology must resolve to (validated where applicable).
_STAGE_METHODOLOGY = {
    "scope": ("idea_select", "select_id", "select_ref"),
    "idea": ("idea_select", "select_id", "select_ref"),
    "baseline": ("baseline_contract", "contract_id", "contract_ref"),
    # NOTE: the `experiment` stage has no fold-time typed methodology record — its methodology (claim evidence
    # tagged by evidence_kind) is enforced DOWNSTREAM by campaign coverage at analysis->write, so it resolves
    # as not_applicable here (see methodology_check). `analysis` resolves to the validated analysis_bridge.
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
        v = row["verification_verdict"]
        resolves = (v in _OK_BASELINE_V) or (v == "waived" and (row["waiver_reason"] or "").strip())
        reason = "" if resolves else f"baseline.contract verdict {v!r} not acceptable"
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
    written = conn.execute(
        "UPDATE paper_spine SET submission_ready=?, coverage_json=?, coverage_at=?, "
        "updated_at=COALESCE(?, updated_at) WHERE quest_id=?",
        (1 if ready else 0, json.dumps(coverage), at, at, quest_id)).rowcount
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
