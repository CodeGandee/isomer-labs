#!/usr/bin/env python3
"""regression suite — LATER next-move BO wired into the research loop (closer to DeepScientist's full cycle):

  experiment/analysis result -> update quest-local Findings Memory -> enumerate next-move candidates ->
  BO-reviewer valuation -> acquisition decision -> orchestrator routes to the selected next move.

Proves the post-experiment / post-analysis routing choice is now BO-DECISIVE (not merely advisory): the
`bo_next_move` gate blocks the discovery-zone route until a CURRENT next-move `bo_decision` binds the move; BO
ranks only hard-gate-ELIGIBLE moves (it never bypasses a quality gate); a single eligible move is skipped with
an explicit reason; and BO-unavailable never silently bypasses a multi-candidate choice. STRICTLY quest-local.

Run:  python3 tests/binding/test_bo_next_move.py   (exits non-zero on any failure)
"""
import json, os, subprocess, sqlite3, sys, tempfile, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
H = str(ROOT / "execplan" / "harness" / "bin" / "deepresearch")
AT = "2026-06-29T00:00:00Z"
AT2 = "2026-06-29T02:00:00Z"
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


def setup(tmp, qid, baseline_gate="pending"):
    """A POST-experiment quest with PASSING campaign coverage (so no hard gate blocks) + result rows."""
    db = str(pathlib.Path(tmp) / ("nm_%s.sqlite" % qid))
    run(db, ["state", "init"])
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    c.execute("INSERT INTO quest(quest_id,title,objective_ref,workspace_ref,run_state,rigor_level,baseline_gate,"
              "autonomy_mode,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
              (qid, "t", "o", "w", "running", "standard", baseline_gate, "auto", AT, AT))
    c.execute("INSERT INTO artifact(artifact_id,quest_id,kind,ref,created_at) VALUES(?,?,?,?,?)",
              (qid + ":rc", qid, "research-contract", "c", AT))
    c.execute("INSERT INTO experiment(experiment_id,quest_id,run_contract_ref,status,created_at,updated_at) "
              "VALUES('E1',?,?,?,?,?)", (qid, "rc", "done", AT, AT))
    # one main claim with provenance-backed main_result + baseline_comparison + ablation -> campaign coverage passes
    c.execute("INSERT INTO claim(claim_id,quest_id,statement,status,kind,created_at,updated_at) "
              "VALUES(?,?,?,?,?,?,?)", (qid + ":C1", qid, "s", "supported", "claim", AT, AT))
    proof = {"main_result": {"metric": "acc", "direction": "higher"},
             "baseline_comparison": {"metric": "acc", "direction": "higher"},
             "ablation": {"changed_factor": "ln", "controls": "fixed", "delta": "+1.2"}}
    for ek in ("main_result", "baseline_comparison", "ablation"):
        ref = f"{qid}:R:{ek}"
        p = dict(proof[ek])
        if ek == "ablation":
            p["parent_result"] = ref
        c.execute("INSERT INTO claim_evidence(claim_id,source_kind,source_ref,relation,evidence_kind,"
                  "evidence_proof,created_at) VALUES(?,?,?,?,?,?,?)",
                  (qid + ":C1", "result", ref, "supports", ek, json.dumps(p), AT))
        c.execute("INSERT INTO result(result_id,quest_id,experiment_id,validity,artifact_ref,provenance_route,"
                  "provenance_ok,provenance_level,created_at) VALUES(?,?,?,?,?,?,?,?,?)",
                  (ref, qid, "E1", "valid", "a", "executed", 1, "artifact_backed", AT))
    c.commit(); c.close()
    return db


def opp(db, qid, oid, kind="next_experiment", status="open", sig=None, rationale="grounded next move"):
    p = {"record_type": "opportunity.record", "record_id": oid, "at": AT, "quest_id": qid, "kind": kind,
         "rationale": rationale, "status": status, "proposed_by": "orchestrator"}
    if sig is not None:
        p["attempt_signature"] = sig
    return rec(db, p)


def val(**kw):
    v = {"utility": 50, "quality": 50, "novelty": 50, "exploration_value": 50, "uncertainty": 50,
         "feasibility": 50, "cost": 20, "risk": 20, "expected_metric_direction": "unknown", "expected_effect": 50}
    v.update(kw); return v


def review_json(tmp, name, items):
    p = pathlib.Path(tmp) / name; p.write_text(json.dumps(items)); return str(p)


def nm_gate(db, qid, env=None):
    return jdata(run(db, ["gate", "status", "--quest-id", qid], env))["gates"].get("bo_next_move", {})


def main():
    with tempfile.TemporaryDirectory() as tmp:

        # ── N1: Findings Memory update after experiment/analysis is quest-local + summarized
        print("N1 Findings Memory updated after experiment/analysis:")
        db = setup(tmp, "fm")
        run(db, ["findings", "update", "--quest-id", "fm", "--slug", "r4-result", "--kind", "knowledge",
                 "--summary", "round-4 ablation: +1.2 acc; main effect holds", "--grounded-by", "fm:R:main_result", "--at", AT])
        run(db, ["findings", "update", "--quest-id", "fm", "--slug", "fa3-refuted", "--kind", "lesson",
                 "--summary", "additive cross-term variant refuted (compensating error)", "--at", AT])
        fs = jdata(run(db, ["findings", "summarize", "--quest-id", "fm"]))
        check("N1: findings summarize digest has the result (knowledge) + refuted alternative (lesson), quest-local",
              fs["total"] == 2 and fs["counts"].get("knowledge") == 1 and fs["counts"].get("lesson") == 1
              and "frontier" in fs and "evidence_gaps" in fs, "counts=%s" % fs.get("counts"))

        # ── N2: generation of MULTIPLE next-move candidates with hard-gate eligibility
        print("N2 enumerable next-move candidates with eligibility:")
        db = setup(tmp, "en")
        opp(db, "en", "en:o1", kind="ablation")
        opp(db, "en", "en:o2", kind="robustness")
        nm = jdata(run(db, ["bo", "next-moves", "--quest-id", "en"]))
        kinds = {c["candidate_ref"]: c["eligible"] for c in nm["candidates"]}
        check("N2: opportunities + synthetic write/finalize/stop enumerated; >=2 eligible; ineligible ones tagged",
              nm["post_experiment"] is True and nm["n_eligible"] >= 2 and kinds.get("en:o1") is True
              and kinds.get("en:o2") is True and kinds.get("en:move:finalize") is False
              and kinds.get("en:move:write") is False, "nm=%s" % kinds)

        # ── N7 (pre): the gate BLOCKS the discovery-zone route until a current next-move bo_decision exists
        print("N7 bo_next_move blocks the route until a current decision binds the move:")
        g_pre = nm_gate(db, "en")
        check("N7a: bo_next_move blocking (route bo-review) with >=2 eligible moves + no decision",
              g_pre.get("status") == "fail" and g_pre.get("blocking") is True and g_pre.get("route_target") == "bo-review"
              and "bo_next_move" in jdata(run(db, ["gate", "status", "--quest-id", "en"]))["blocking_gates"],
              "gate=%s" % g_pre)

        # ── N3 + N4 + N7(post): BO-reviewer valuation for next-move + experiment-selection + routing bind
        print("N3/N4 next-move BO valuation -> experiment-selection -> routing bound:")
        rj = review_json(tmp, "en.json", [
            {"candidate_ref": "en:o1", "valuation": val(utility=40, quality=40, exploration_value=30)},
            {"candidate_ref": "en:o2", "valuation": val(utility=80, quality=70, exploration_value=90)}])
        rv = run(db, ["bo", "review", "--quest-id", "en", "--next-move", "--from-json", rj, "--at", AT])
        c = sqlite3.connect(db); nrev = c.execute("SELECT COUNT(*) FROM bo_review WHERE quest_id='en'").fetchone()[0]; c.close()
        sel = jdata(run(db, ["bo", "select", "--quest-id", "en", "--next-move", "--at", AT2]))
        c = sqlite3.connect(db)
        drow = c.execute("SELECT decision_kind,selected_candidate_ref FROM bo_decision WHERE quest_id='en'").fetchone()
        c.close()
        check("N3: one bo_review per viable next-move candidate", jdata(rv)["reviewed"] == 2 and nrev == 2)
        check("N4: official acquisition picks o2; decision_kind=experiment-selection; route bound to experiment",
              sel["selected_candidate_ref"] == "en:o2" and sel["decision_kind"] == "experiment-selection"
              and sel["selected_route"] == "experiment" and drow[0] == "experiment-selection" and drow[1] == "en:o2",
              "sel=%s drow=%s" % ({k: sel.get(k) for k in ("selected_candidate_ref", "decision_kind", "selected_route")}, drow))
        g_post = nm_gate(db, "en")
        check("N7b: bo_next_move PASSES after a current next-move decision binds the route (idea->route unblocked)",
              g_post.get("status") == "pass" and g_post.get("blocking") is False
              and "bo_next_move" not in jdata(run(db, ["gate", "status", "--quest-id", "en"]))["blocking_gates"],
              "gate=%s" % g_post)

        # ── N5: opportunity-selection (a non-experiment 'new_idea' opportunity wins -> route analysis)
        print("N5 opportunity-selection decision kind:")
        db = setup(tmp, "op")
        opp(db, "op", "op:exp", kind="ablation")
        opp(db, "op", "op:idea", kind="new_idea")  # routes to analysis -> opportunity-selection
        rj = review_json(tmp, "op.json", [
            {"candidate_ref": "op:exp", "valuation": val(utility=30, quality=30, exploration_value=20)},
            {"candidate_ref": "op:idea", "valuation": val(utility=85, quality=80, exploration_value=80)}])
        run(db, ["bo", "review", "--quest-id", "op", "--next-move", "--from-json", rj, "--at", AT])
        selo = jdata(run(db, ["bo", "select", "--quest-id", "op", "--next-move", "--at", AT2]))
        check("N5: winning non-experiment opportunity -> decision_kind=opportunity-selection, route analysis",
              selo["selected_candidate_ref"] == "op:idea" and selo["decision_kind"] == "opportunity-selection"
              and selo["selected_route"] == "analysis",
              "selo=%s" % {k: selo.get(k) for k in ("selected_candidate_ref", "decision_kind", "selected_route")})

        # ── N6: stop-write-finalize-selection (a synthetic 'stop' move wins under repeated-failure dominance)
        print("N6 stop-write-finalize-selection decision kind:")
        db = setup(tmp, "st")
        opp(db, "st", "st:drop", kind="ablation", status="dropped", sig={"method_key": "mk"})
        opp(db, "st", "st:open", kind="ablation", status="open", sig={"method_key": "mk"})  # repeated-failure signature
        nmst = {c["candidate_ref"]: c["eligible"] for c in jdata(run(db, ["bo", "next-moves", "--quest-id", "st"]))["candidates"]}
        rj = review_json(tmp, "st.json", [
            {"candidate_ref": "st:open", "valuation": val(utility=30, quality=30, exploration_value=20)},
            {"candidate_ref": "st:move:stop", "valuation": val(utility=80, quality=80, exploration_value=70)}])
        run(db, ["bo", "review", "--quest-id", "st", "--next-move", "--from-json", rj, "--at", AT])
        sels = jdata(run(db, ["bo", "select", "--quest-id", "st", "--next-move", "--at", AT2]))
        check("N6: repeated-failure makes 'stop' eligible; winning stop -> stop-write-finalize-selection, route decision",
              nmst.get("st:move:stop") is True and sels["selected_candidate_ref"] == "st:move:stop"
              and sels["decision_kind"] == "stop-write-finalize-selection" and sels["selected_route"] == "decision",
              "stop_elig=%s sels=%s" % (nmst.get("st:move:stop"), {k: sels.get(k) for k in ("selected_candidate_ref", "decision_kind")}))

        # ── N8: single eligible next move -> explicit SKIP decision (no forced reviewer work)
        print("N8 single eligible next move -> explicit skip:")
        db = setup(tmp, "sk")
        opp(db, "sk", "sk:o1", kind="ablation")  # the only eligible move (write/finalize/stop all ineligible)
        g_sk = nm_gate(db, "sk")
        skip = jdata(run(db, ["bo", "select", "--quest-id", "sk", "--next-move",
                              "--skip-reason", "single eligible next move", "--at", AT]))
        c = sqlite3.connect(db)
        drow = c.execute("SELECT acquisition_method,selected_candidate_ref,decision_kind,selection_rationale "
                         "FROM bo_decision WHERE quest_id='sk'").fetchone()
        c.close()
        check("N8: single eligible -> gate pass; skip records method='skipped' + kind + route + reason",
              g_sk.get("status") == "pass" and drow is not None and drow[0] == "skipped"
              and drow[1] == "sk:o1" and drow[2] == "experiment-selection" and "single eligible" in (drow[3] or "")
              and skip["selected_route"] == "experiment", "g=%s drow=%s" % (g_sk.get("status"), drow))

        # ── N9: BO unavailable does NOT silently bypass a multi-candidate next-move choice
        print("N9 BO unavailable does not silently bypass:")
        db = setup(tmp, "un")
        opp(db, "un", "un:o1", kind="ablation"); opp(db, "un", "un:o2", kind="robustness")
        r_noavail = run(db, ["bo", "review", "--quest-id", "un", "--next-move", "--at", AT])  # no creds, no --allow-bo-stub
        g_un = nm_gate(db, "un")
        check("N9: `bo review --next-move` REFUSES (exit!=0) without creds/stub; gate stays blocking (no silent route)",
              r_noavail.returncode != 0 and "OFFLINE stub is NOT permitted" in (r_noavail.stdout + r_noavail.stderr)
              and g_un.get("status") == "fail" and g_un.get("blocking") is True,
              "rc=%s gate=%s" % (r_noavail.returncode, g_un.get("status")))

        # ── N10 + N11: BO cannot select a gate-INVALID next move; write/finalize stay gate-protected
        print("N10/N11 gate-invalid next moves excluded; write/finalize protected:")
        db = setup(tmp, "gi")
        opp(db, "gi", "gi:o1", kind="ablation"); opp(db, "gi", "gi:o2", kind="robustness")
        # inject a MAX-score review for the INELIGIBLE finalize move directly (finalize not gate-satisfied)
        rec(db, {"record_type": "bo_review.record", "record_id": "gi:rev:fin", "at": AT, "quest_id": "gi",
                 "candidate_ref": "gi:move:finalize", "candidate_kind": "finalize", "reviewer_backend": "codex",
                 "reviewer_model": "x", "reviewer_effort": "max", "is_stub": False,
                 "valuation": val(utility=100, quality=100, exploration_value=100)})
        rj = review_json(tmp, "gi.json", [
            {"candidate_ref": "gi:o1", "valuation": val(utility=40, quality=40, exploration_value=40)},
            {"candidate_ref": "gi:o2", "valuation": val(utility=70, quality=60, exploration_value=60)}])
        run(db, ["bo", "review", "--quest-id", "gi", "--next-move", "--from-json", rj, "--at", AT])
        selg = jdata(run(db, ["bo", "select", "--quest-id", "gi", "--next-move", "--at", AT2]))
        refs = {s["candidate_ref"] for s in selg["acquisition_scores"]}
        nmg = {c["candidate_ref"]: c for c in jdata(run(db, ["bo", "next-moves", "--quest-id", "gi"]))["candidates"]}
        check("N10: ineligible finalize excluded from acquisition despite a max-score review; eligible move wins",
              "gi:move:finalize" not in refs and selg["selected_candidate_ref"] == "gi:o2", "refs=%s" % refs)
        check("N11: write/finalize are gate-protected (ineligible with a reason) in the enumerated slate",
              nmg["gi:move:write"]["eligible"] is False and nmg["gi:move:finalize"]["eligible"] is False
              and "review" in nmg["gi:move:finalize"]["eligibility_reason"].lower(),
              "write=%s fin=%s" % (nmg["gi:move:write"]["eligible"], nmg["gi:move:finalize"]["eligibility_reason"]))

        # ── N12: no cross-quest / global Findings Memory; invariants intact
        print("N12 strictly quest-local Findings Memory:")
        db = setup(tmp, "ql")
        gl = rec(db, {"record_type": "finding.add", "record_id": "ql:bad", "at": AT, "quest_id": "ql",
                      "scope": "global", "kind": "knowledge", "summary": "reject me"})
        sv = run(db, ["state", "validate"])
        check("N12: a global-scope finding is rejected; state validate passes (no cross-quest memory)",
              gl.returncode != 0 and sv.returncode == 0, "gl=%s sv=%s" % (gl.returncode, sv.returncode))

        # ── N13: backward compatibility — a non-active (finalized) quest is never retroactively blocked
        print("N13 backward compatibility (finalized quest not retroactively blocked):")
        db = setup(tmp, "done")
        opp(db, "done", "done:o1", kind="ablation"); opp(db, "done", "done:o2", kind="robustness")
        c = sqlite3.connect(db); c.execute("UPDATE quest SET run_state='completed' WHERE quest_id='done'"); c.commit(); c.close()
        gdone = nm_gate(db, "done")
        check("N13: completed quest -> bo_next_move not_applicable, never in blocking_gates",
              gdone.get("status") == "not_applicable" and gdone.get("blocking") is False
              and "bo_next_move" not in jdata(run(db, ["gate", "status", "--quest-id", "done"]))["blocking_gates"],
              "gate=%s" % gdone)

    print("\n%d passed, %d failed" % (len(PASSED), len(FAILED)))
    if FAILED:
        print("FAILED:", *FAILED, sep="\n  ")
        sys.exit(1)


if __name__ == "__main__":
    main()
