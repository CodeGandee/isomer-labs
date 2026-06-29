#!/usr/bin/env python3
"""regression suite — DeepScientist-style idea-level BO integrated into the research loop via quest-local
Findings Memory.

Proves the BO machinery is now WIRED into the loop (it previously existed but was never triggered):
  * each idea-slate candidate is persisted as an ENUMERABLE idea row (not collapsed inside idea_select JSON);
  * `bo candidates` enumerates the gate-ELIGIBLE idea rows;
  * a multi-candidate idea selection is DECISIVE — the orchestrator's idea->baseline route blocks on the
    `bo_idea_decision` gate until an idea-selection bo_decision binds the winner into idea_select;
  * the default acquisition is the official DeepScientist-style score utility+quality+exploration_value;
  * a single viable candidate may be SKIPPED, but the skip reason is recorded explicitly;
  * BO can also choose a LATER research move (experiment/opportunity selection);
  * BO cannot select a gate-ineligible candidate;
  * Findings Memory is strictly QUEST-LOCAL (no cross-quest / global memory);
  * legacy quests (idea_select, no idea rows) stay readable.

Run:  python3 tests/binding/test_bo_findings_integration.py   (exits non-zero on any failure)
"""
import json, os, subprocess, sqlite3, sys, tempfile, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
H = str(ROOT / "execplan" / "harness" / "bin" / "deepresearch")
AT = "2026-06-26T00:00:00Z"
STUB = {"DEEPRESEARCH_BO_ALLOW_STUB": "1"}
PASSED, FAILED = [], []


def run(db, args, extra_env=None):
    return subprocess.run([H, "--db", db, *args], capture_output=True, text=True,
                          env={**os.environ, **(extra_env or {})})


def rec(db, payload, extra_env=None):
    return run(db, ["record", "apply", "--json", json.dumps(payload)], extra_env)


def jdata(r):
    return json.loads(r.stdout)["data"]


def check(label, cond, detail=""):
    (PASSED if cond else FAILED).append(label)
    print(("  PASS " if cond else "  FAIL ") + label + (("  -- " + detail) if detail and not cond else ""))


GOOD_SCOPE = {"objective": "Predict FA4 forward latency within 6% MAPE", "research_question": "learned cost model?",
              "non_goals": "no backward pass", "primary_metric": "MAPE", "metric_direction": "minimize",
              "dataset": "FA4-bench", "split": "test", "eval_protocol": "eval.py --split test",
              "false_progress_signals": "train split", "baseline_route_expectation": "imported",
              "acceptance_criteria": "MAPE < 8% on test", "constraints": "single GPU"}


def setup(tmp, qid, rigor="standard"):
    db = str(pathlib.Path(tmp) / ("bofi_%s.sqlite" % qid))
    run(db, ["state", "init"])
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    c.execute("INSERT INTO quest(quest_id,title,objective_ref,workspace_ref,run_state,rigor_level,baseline_gate,"
              "autonomy_mode,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
              (qid, "t", "o", "w", "running", rigor, "pending", "auto", AT, AT))
    c.execute("INSERT INTO artifact(artifact_id,quest_id,kind,ref,created_at) VALUES(?,?,?,?,?)",
              (qid + ":rc", qid, "research-contract", "c", AT))
    c.execute("INSERT INTO reference(reference_id,quest_id,source,uri,fetched_at,created_at) "
              "VALUES('REF1',?,?,?,?,?)", (qid, "manual", "doi:10.0/prior", AT, AT))
    c.commit(); c.close()
    rec(db, {"record_type": "scope.contract", "record_id": qid + ":sc", "at": AT, "quest_id": qid, "contract": GOOD_SCOPE})
    run(db, ["scope", "validate", "--quest-id", qid])
    return db


def cand(cid):
    return {"candidate_id": cid, "title": cid, "hypothesis": "hypothesis for " + cid, "mechanism": "m",
            "expected_evidence": ["e"], "risk": "r"}


def scores(total):
    s = {k: 0 for k in ("novelty", "falsifiability", "feasibility", "evidence_potential", "fit_to_objective")}
    for k in s:
        s[k] = max(0, min(2, total - sum(s.values())))
    return s


def gate(cid, total, verdict="reject"):
    return {"candidate_id": cid, "scores": scores(total), "total": total, "verdict": verdict}


def slate_content(totals, retained_id="A", novelty="novel"):
    """totals: dict candidate_id -> selection_gate total. retained is the scout's pick (advisory)."""
    ids = list(totals)
    return {
        "objective_contract_ref": "runs/q/idea/obj.md", "baseline_contract_ref": "WAIVER: deferred",
        "raw_slate": [cand(x) for x in ids],
        "challenge": {"strongest_rejection": "x", "outside_family_alternative": "y", "why_retained_survives": "z"},
        "novelty_risk": {"novelty_label": novelty, "novelty_argument": "arg", "risk_notes": "n",
                         "known_near_neighbors": ["Smith2023 (differs: mechanism Y)"]},
        "prior_comparison": {"closest_prior_refs": ["REF1"], "prior_did": "heuristic cost model",
                             "proposed_difference": "learned end-to-end", "novelty_type": "mechanistic",
                             "why_prior_insufficient": "misses cross-config effects",
                             "distinguishing_experiment": "MAPE on held-out configs"},
        "selection_gate": [gate(x, t, "retain" if x == retained_id else "reject") for x, t in totals.items()],
        "rejected": [{"candidate_id": x, "reason": "scout: weaker mechanism"} for x in ids if x != retained_id]
                    or [{"candidate_id": "Z", "reason": "infeasible"}],
        "retained": {"candidate_id": retained_id, "hypothesis": "h", "mechanism": "m", "claim_candidate": "c",
                     "mvp_experiment_plan": "run minimal X", "expected_failure_mode": "f", "boundary_condition": "b"},
    }


def write_select(tmp, db, qid, totals, retained_id="A"):
    ref = str(pathlib.Path(tmp) / ("select_%s.json" % qid))
    pathlib.Path(ref).write_text(json.dumps(slate_content(totals, retained_id)))
    rec(db, {"record_type": "idea.select", "record_id": qid + ":isel", "at": AT, "quest_id": qid, "select_ref": ref})
    return run(db, ["idea", "validate", "--quest-id", qid])


def val(**kw):
    v = {"utility": 50, "quality": 50, "novelty": 50, "exploration_value": 50, "uncertainty": 50,
         "feasibility": 50, "cost": 20, "risk": 20, "expected_metric_direction": "unknown", "expected_effect": 50}
    v.update(kw); return v


def review_json(tmp, name, items):
    p = pathlib.Path(tmp) / name; p.write_text(json.dumps(items)); return str(p)


def gate_of(db, qid, name):
    return jdata(run(db, ["gate", "status", "--quest-id", qid]))["gates"].get(name, {})


def main():
    with tempfile.TemporaryDirectory() as tmp:

        # ── T1: a multi-candidate slate persists as ENUMERABLE idea rows (eligible=proposed, below-floor=rejected)
        print("T1 idea-slate persists as enumerable idea rows (floor-tagged eligibility):")
        db = setup(tmp, "m")  # standard floor=6: A=8,B=7 eligible ; C=4 ineligible
        iv = write_select(tmp, db, "m", {"A": 8, "B": 7, "C": 4}, retained_id="A")
        c = sqlite3.connect(db)
        rows = {r[0]: r[1] for r in c.execute("SELECT idea_id,status FROM idea WHERE quest_id='m'")}
        c.close()
        prop = sorted(k for k, v in rows.items() if v == "proposed")
        check("T1: 3 idea rows materialized; A,B eligible(proposed), C below-floor(rejected)",
              len(rows) == 3 and prop == ["m:idea:A", "m:idea:B"] and rows.get("m:idea:C") == "rejected"
              and jdata(iv)["eligible_candidates"] == 2, "rows=%s" % rows)

        # ── bo candidates enumerates the eligible idea rows (and NOT the ineligible one)
        cd = jdata(run(db, ["bo", "candidates", "--quest-id", "m"]))
        crefs = sorted(c["candidate_ref"] for c in cd["candidates"] if c["candidate_kind"] == "idea")
        check("T1b: bo candidates enumerates the 2 eligible idea rows, excludes ineligible C",
              crefs == ["m:idea:A", "m:idea:B"], "crefs=%s" % crefs)

        # ── T5 (pre): orchestrator BLOCKS idea->baseline when a multi-candidate BO decision is missing
        print("T5 idea->baseline blocks until a multi-candidate bo_decision exists:")
        g = gate_of(db, "m", "bo_idea_decision")
        check("T5a: bo_idea_decision is blocking (route bo-review) before any decision",
              g.get("status") == "fail" and g.get("blocking") is True and g.get("route_target") == "bo-review",
              "gate=%s" % g)
        check("T5a2: bo_idea_decision is in blocking_gates",
              "bo_idea_decision" in jdata(run(db, ["gate", "status", "--quest-id", "m"]))["blocking_gates"])

        # ── T2: BO-reviewer produces ONE valuation per viable candidate
        print("T2 one bo_review per viable candidate:")
        rj = review_json(tmp, "m.json", [
            {"candidate_ref": "m:idea:A", "valuation": val(utility=70, quality=60, exploration_value=20)},
            {"candidate_ref": "m:idea:B", "valuation": val(utility=80, quality=70, exploration_value=90)}])
        rv = run(db, ["bo", "review", "--quest-id", "m", "--from-json", rj, "--at", AT])
        c = sqlite3.connect(db)
        nrev = c.execute("SELECT COUNT(*) FROM bo_review WHERE quest_id='m' AND is_stub=0").fetchone()[0]
        c.close()
        check("T2: 2 real bo_review rows (one per viable candidate)", jdata(rv)["reviewed"] == 2 and nrev == 2,
              "reviewed=%s nrev=%s" % (jdata(rv).get("reviewed"), nrev))

        # ── T3 + T4: bo select (official default) picks the winner, binds it into idea_select.retained_candidate
        print("T3/T4 official acquisition selects + binds the winner:")
        sel = jdata(run(db, ["bo", "select", "--quest-id", "m", "--at", AT]))  # default decision-kind idea-selection + bind
        # B official score = 80+70+90 = 240 ; A = 70+60+20 = 150 -> B wins
        topB = [s for s in sel["acquisition_scores"] if s["candidate_ref"] == "m:idea:B"][0]
        check("T3: default method ucb_official_v1; B wins with score u+q+ev=240",
              sel["acquisition_method"] == "ucb_official_v1" and sel["selected_candidate_ref"] == "m:idea:B"
              and topB["score"] == 240.0, "sel=%s" % {k: sel.get(k) for k in ("acquisition_method", "selected_candidate_ref")})
        c = sqlite3.connect(db)
        retained = c.execute("SELECT retained_candidate FROM idea_select WHERE quest_id='m'").fetchone()[0]
        statB = c.execute("SELECT status FROM idea WHERE idea_id='m:idea:B'").fetchone()[0]
        statA = c.execute("SELECT status FROM idea WHERE idea_id='m:idea:A'").fetchone()[0]
        dkind = c.execute("SELECT decision_kind FROM bo_decision WHERE quest_id='m'").fetchone()[0]
        c.close()
        check("T4: idea_select.retained_candidate bound to BO winner B; idea row B selected, A demoted to proposed",
              retained == "B" and statB == "selected" and statA == "proposed" and dkind == "idea-selection",
              "retained=%s statB=%s statA=%s" % (retained, statB, statA))

        # ── T5 (post): the gate now passes and idea->baseline is unblocked
        g2 = gate_of(db, "m", "bo_idea_decision")
        check("T5b: bo_idea_decision passes after the winner is bound (idea->baseline unblocked)",
              g2.get("status") == "pass" and g2.get("blocking") is False
              and "bo_idea_decision" not in jdata(run(db, ["gate", "status", "--quest-id", "m"]))["blocking_gates"],
              "gate=%s" % g2)

        # ── T9: BO cannot select a gate-INVALID candidate. Inject a MAX-score review for the ineligible C
        # directly (C is status='rejected', so `bo candidates` never surfaces it); acquisition must exclude it.
        print("T9 gate-ineligible candidate excluded from acquisition:")
        rec(db, {"record_type": "bo_review.record", "record_id": "m:borev:C", "at": "2026-06-26T01:00:00Z",
                 "quest_id": "m", "candidate_ref": "m:idea:C", "candidate_kind": "idea", "reviewer_backend": "codex",
                 "reviewer_model": "x", "reviewer_effort": "max", "is_stub": False,
                 "valuation": val(utility=100, quality=100, exploration_value=100)})
        sel2 = jdata(run(db, ["bo", "select", "--quest-id", "m"]))
        refs2 = {s["candidate_ref"] for s in sel2["acquisition_scores"]}
        check("T9: ineligible C (status rejected) never enters acquisition despite a max-score review",
              "m:idea:C" not in refs2 and sel2["selected_candidate_ref"] == "m:idea:B",
              "refs=%s selected=%s" % (refs2, sel2.get("selected_candidate_ref")))

        # ── T6: single viable candidate -> explicit SKIP decision (recorded reason), gate passes
        print("T6 single-candidate BO skip records an explicit reason:")
        db1 = setup(tmp, "s")  # only A eligible (8); B,C below floor
        write_select(tmp, db1, "s", {"A": 8, "B": 4, "C": 3}, retained_id="A")
        g_pre = gate_of(db1, "s", "bo_idea_decision")
        skip = jdata(run(db1, ["bo", "select", "--quest-id", "s", "--skip-reason",
                               "only one gate-eligible candidate (A); no slate to optimize over", "--at", AT]))
        c = sqlite3.connect(db1)
        drow = c.execute("SELECT acquisition_method,selected_candidate_ref,selection_rationale,decision_kind "
                         "FROM bo_decision WHERE quest_id='s'").fetchone()
        retained_s = c.execute("SELECT retained_candidate FROM idea_select WHERE quest_id='s'").fetchone()[0]
        c.close()
        check("T6: single viable candidate => gate already pass; skip records method='skipped' + reason + binds A",
              g_pre.get("status") == "pass" and drow is not None and drow[0] == "skipped"
              and drow[1] == "s:idea:A" and "only one gate-eligible" in (drow[2] or "") and retained_s == "A",
              "g_pre=%s drow=%s" % (g_pre.get("status"), drow))

        # ── T8: BO selects a LATER research move (experiment/opportunity selection) over open opportunities
        print("T8 BO selects a later research move from quest-local opportunities:")
        db2 = setup(tmp, "nx")
        for oid, k in (("nx:o1", "ablation"), ("nx:o2", "robustness")):
            rec(db2, {"record_type": "opportunity.record", "record_id": oid, "at": AT, "quest_id": "nx", "kind": k,
                      "rationale": "grounded next move", "status": "open", "proposed_by": "orchestrator"})
        rjn = review_json(tmp, "nx.json", [
            {"candidate_ref": "nx:o1", "valuation": val(utility=40, quality=40, exploration_value=30)},
            {"candidate_ref": "nx:o2", "valuation": val(utility=60, quality=70, exploration_value=80)}])
        run(db2, ["bo", "review", "--quest-id", "nx", "--from-json", rjn, "--at", AT])
        nxt = jdata(run(db2, ["bo", "select", "--quest-id", "nx", "--decision-kind", "experiment-selection", "--at", AT]))
        c = sqlite3.connect(db2)
        ndk = c.execute("SELECT decision_kind,selected_candidate_ref FROM bo_decision WHERE quest_id='nx'").fetchone()
        c.close()
        check("T8: next-move bo_decision (decision_kind=experiment-selection) selects the higher-value opportunity o2",
              nxt["selected_candidate_ref"] == "nx:o2" and ndk[0] == "experiment-selection" and ndk[1] == "nx:o2",
              "nxt=%s ndk=%s" % (nxt.get("selected_candidate_ref"), ndk))

        # ── T7: experiment/analysis findings update quest-local Findings Memory; summarize surfaces them
        print("T7 Findings Memory is populated + summarized (quest-local):")
        run(db2, ["findings", "update", "--quest-id", "nx", "--slug", "fa3-refuted", "--kind", "lesson",
                  "--summary", "additive cross-term model refuted by round-4 ablation", "--at", AT])
        run(db2, ["findings", "update", "--quest-id", "nx", "--slug", "frontier", "--kind", "knowledge",
                  "--summary", "frontier: decode-latency regime unexplained; evidence gap on TC fragment", "--at", AT])
        fs = jdata(run(db2, ["findings", "summarize", "--quest-id", "nx"]))
        check("T7: findings summarize reports the lesson + frontier (quest-local digest)",
              fs["total"] == 2 and fs["counts"].get("lesson") == 1 and len(fs["lessons"]) == 1
              and "frontier" in fs and "evidence_gaps" in fs, "fs=%s" % fs.get("counts"))

        # ── T10: no cross-quest / global memory — findings are quest-scoped; global scope is rejected
        print("T10 strictly quest-local Findings Memory (no cross-quest/global):")
        gl = rec(db2, {"record_type": "finding.add", "record_id": "nx:bad", "at": AT, "quest_id": "nx",
                       "scope": "global", "kind": "knowledge", "summary": "should be rejected"})
        sv = run(db2, ["state", "validate"])
        c = sqlite3.connect(db2)
        nbad = c.execute("SELECT COUNT(*) FROM finding_memory WHERE scope<>'quest'").fetchone()[0]
        c.close()
        check("T10: a global-scope finding is rejected; all findings stay scope='quest'; invariants pass",
              gl.returncode != 0 and nbad == 0 and sv.returncode == 0, "rc=%s nbad=%s sv=%s" % (gl.returncode, nbad, sv.returncode))

        # ── T11: legacy quest (idea_select, NO idea rows) stays readable; bo_idea_decision is not_applicable
        print("T11 legacy/lazy compatibility (idea_select without enumerable idea rows):")
        db3 = setup(tmp, "lg")
        ref = str(pathlib.Path(tmp) / "lg.json"); pathlib.Path(ref).write_text(json.dumps(slate_content({"A": 8, "B": 7}, "A")))
        rec(db3, {"record_type": "idea.select", "record_id": "lg:isel", "at": AT, "quest_id": "lg", "select_ref": ref})
        # NOTE: deliberately do NOT run `idea validate`, so no idea rows are materialized (legacy posture).
        cdl = jdata(run(db3, ["bo", "candidates", "--quest-id", "lg"]))
        srcs = {c["source"] for c in cdl["candidates"]}
        glg = gate_of(db3, "lg", "bo_idea_decision")
        check("T11: no idea rows => bo candidates falls back to the single idea_select; gate not_applicable",
              cdl["count"] == 1 and srcs == {"idea_select"} and glg.get("status") == "not_applicable",
              "count=%s srcs=%s gate=%s" % (cdl["count"], srcs, glg.get("status")))

    print("\n%d passed, %d failed" % (len(PASSED), len(FAILED)))
    if FAILED:
        print("FAILED:", *FAILED, sep="\n  ")
        sys.exit(1)


if __name__ == "__main__":
    main()
