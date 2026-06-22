#!/usr/bin/env python3
"""regression suite — typed scope/eval contract.

A vague research prompt cannot flow into baseline/idea/experiment: the UPSTREAM `scope.contract` (objective +
evaluation plan) must pass `scope validate` (validator-owned `valid`, author cannot self-certify). In bound
mode idea selection requires a valid, non-stale scope contract; `methodology check --stage scope` resolves to
it; gate status surfaces it. Scoping/advisory stays permissive. Waive with DEEPRESEARCH_SCOPE_GATE=0.

Run:  python3 tests/binding/test_scope_contract.py   (exits non-zero on any failure)
"""
import json, os, subprocess, sqlite3, sys, tempfile, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
H = str(ROOT / "execplan" / "harness" / "bin" / "deepresearch")
AT = "2026-06-18T00:00:00Z"
PASSED, FAILED = [], []

GOOD_SCOPE = {"objective": "Predict FA4 forward latency within 6% MAPE across configs",
              "research_question": "Can a learned cost model predict FA4 latency?", "non_goals": "no backward pass",
              "primary_metric": "MAPE", "metric_direction": "minimize", "dataset": "FA4-bench", "split": "test",
              "eval_protocol": "eval.py --split test", "false_progress_signals": "metric on train split; one GPU only",
              "baseline_route_expectation": "imported", "acceptance_criteria": "MAPE < 8% on test",
              "constraints": "single GPU generation"}


def run(db, args, extra_env=None):
    return subprocess.run([H, "--db", db, *args], capture_output=True, text=True, env={**os.environ, **(extra_env or {})})


def rec(db, payload, extra_env=None):
    return run(db, ["record", "apply", "--json", json.dumps(payload)], extra_env)


def jdata(r):
    return json.loads(r.stdout)["data"]


def check(label, cond, detail=""):
    (PASSED if cond else FAILED).append(label)
    print(("  PASS " if cond else "  FAIL ") + label + (("  -- " + detail) if detail and not cond else ""))


def setup(tmp, qid, rigor="standard"):
    db = str(pathlib.Path(tmp) / ("sc_%s.sqlite" % qid))
    run(db, ["state", "init"])
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    c.execute("INSERT INTO quest(quest_id,title,objective_ref,workspace_ref,run_state,rigor_level,baseline_gate,"
              "created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)", (qid, "t", "o", "w", "running", rigor, "pending", AT, AT))
    c.execute("INSERT INTO artifact(artifact_id,quest_id,kind,ref,created_at) VALUES(?,?,?,?,?)",
              (qid + ":rc", qid, "research-contract", "c", AT))
    c.commit(); c.close()
    return db


def record_scope(db, qid, contract, validate=True):
    r = rec(db, {"record_type": "scope.contract", "record_id": qid + ":sc", "at": AT, "quest_id": qid, "contract": contract})
    sv = run(db, ["scope", "validate", "--quest-id", qid]) if validate else None
    return r, sv


def good_idea(without=None):
    """A valid idea.select content (so only the scope requirement is under test)."""
    def cand(x): return {"candidate_id": x, "title": x, "hypothesis": "h", "mechanism": "m",
                         "expected_evidence": ["e"], "risk": "r"}
    return {"objective_contract_ref": "o", "baseline_contract_ref": "w",
            "raw_slate": [cand(x) for x in ("A", "B", "C")],
            "challenge": {"strongest_rejection": "x", "outside_family_alternative": "y", "why_retained_survives": "z"},
            "novelty_risk": {"novelty_label": "novel", "novelty_argument": "a", "risk_notes": "n",
                             "known_near_neighbors": ["Doe2024: prior (differs: our mechanism)"]},
            "selection_gate": [{"candidate_id": "A", "scores": {"novelty": 2, "falsifiability": 2, "feasibility": 2,
                                "evidence_potential": 1, "fit_to_objective": 1}, "total": 8, "verdict": "retain"},
                               {"candidate_id": "B", "scores": {"novelty": 1, "falsifiability": 1, "feasibility": 1,
                                "evidence_potential": 1, "fit_to_objective": 0}, "total": 4, "verdict": "reject"},
                               {"candidate_id": "C", "scores": {"novelty": 1, "falsifiability": 0, "feasibility": 1,
                                "evidence_potential": 0, "fit_to_objective": 0}, "total": 2, "verdict": "reject"}],
            "rejected": [{"candidate_id": "B", "reason": "weaker mechanism"}, {"candidate_id": "C", "reason": "infeasible"}],
            "retained": {"candidate_id": "A", "hypothesis": "h", "mechanism": "m", "claim_candidate": "c",
                         "mvp_experiment_plan": "run minimal X", "expected_failure_mode": "f", "boundary_condition": "b"}}


def record_idea(db, qid, content):
    ref = pathlib.Path(_tmp) / (qid + "_idea.json"); ref.write_text(json.dumps(content))
    rec(db, {"record_type": "idea.select", "record_id": qid + ":s1", "at": AT, "quest_id": qid, "select_ref": str(ref)})
    return run(db, ["idea", "validate", "--quest-id", qid])


def gate(db, qid, env=None):
    return jdata(run(db, ["gate", "status", "--quest-id", qid], env))


_tmp = None


def main():
    global _tmp
    with tempfile.TemporaryDirectory() as tmp:
        _tmp = tmp
        # SC1: vague objective -> rejected
        print("SC1 vague objective rejected:")
        db = setup(tmp, "c1")
        _, sv = record_scope(db, "c1", {**GOOD_SCOPE, "objective": "tbd"})
        check("SC1 new: vague objective fails scope validate", sv.returncode != 0 and "objective" in sv.stdout, sv.stdout[:200])

        # SC2: missing core field (primary_metric, unwaivable) -> rejected even if 'waived'
        print("SC2 missing/unwaivable core field rejected:")
        db = setup(tmp, "c2")
        bad = {**GOOD_SCOPE}; del bad["primary_metric"]; bad["waivers"] = {"primary_metric": "later"}
        _, sv = record_scope(db, "c2", bad)
        check("SC2 new: missing primary_metric fails (core field not waivable)",
              sv.returncode != 0 and "primary_metric" in sv.stdout, sv.stdout[:200])

        # SC3: valid contract -> accepted, valid=1
        print("SC3 valid scope contract accepted:")
        db = setup(tmp, "c3")
        _, sv = record_scope(db, "c3", GOOD_SCOPE)
        check("SC3 new: full contract -> valid", sv.returncode == 0 and jdata(sv)["valid"] is True, sv.stdout[:200])

        # SC4: a waivable field deferred with a reason -> accepted
        print("SC4 waivable field deferred with reason accepted:")
        db = setup(tmp, "c4")
        w = {**GOOD_SCOPE}; del w["dataset"]; w["waivers"] = {"dataset": "dataset chosen after baseline survey"}
        _, sv = record_scope(db, "c4", w)
        check("SC4 new: waived dataset -> valid", sv.returncode == 0 and jdata(sv)["valid"] is True, sv.stdout[:200])

        # SC5: author cannot self-certify validity (valid not a settable field)
        print("SC5 author cannot self-certify:")
        db = setup(tmp, "c5")
        r = rec(db, {"record_type": "scope.contract", "record_id": "c5:sc", "at": AT, "quest_id": "c5",
                     "contract": GOOD_SCOPE, "valid": 1})
        v_before = sqlite3.connect(db).execute("SELECT valid FROM scope_contract WHERE quest_id='c5'").fetchone()
        check("SC5 new: payload 'valid' rejected by schema (or never stored as 1)",
              r.returncode != 0 or (v_before and v_before[0] == 0), r.stdout[:200])

        # SC6: idea selection without a valid scope contract fails in bound mode; with it, passes
        print("SC6 idea selection requires a valid scope contract (bound):")
        db = setup(tmp, "c6")
        rv_no = record_idea(db, "c6", good_idea())  # NO scope contract yet
        record_scope(db, "c6", GOOD_SCOPE)
        rv_yes = record_idea(db, "c6", good_idea())
        check("SC6 new: idea validate fails without scope, passes with a valid scope",
              rv_no.returncode != 0 and "scope" in rv_no.stdout and rv_yes.returncode == 0,
              "no=%s yes=%s" % (rv_no.stdout[:160], rv_yes.returncode))

        # SC7: a valid scope contract coexists with baseline validation (reference/alignment)
        print("SC7 baseline validation alongside a valid scope contract:")
        db = setup(tmp, "c7")
        record_scope(db, "c7", GOOD_SCOPE)
        rec(db, {"record_type": "baseline.contract", "record_id": "c7:bc", "at": AT, "quest_id": "c7",
                 "baseline_id": "b", "baseline_name": "BL", "comparison_policy": "lower MAPE wins",
                 "primary_metric_id": "MAPE", "dataset": "FA4-bench", "split": "test", "eval_protocol": "eval.py",
                 "verification_verdict": "trusted_with_caveats", "baseline_route": "imported", "evidence_ref": "Vaswani2017"})
        bv = run(db, ["baseline", "validate", "--quest-id", "c7"])
        check("SC7 new: baseline validate passes with a valid scope contract present",
              bv.returncode == 0 and jdata(bv)["valid"] is True, bv.stdout[:200])

        # SC8: scoping/advisory -> idea selection NOT blocked by a missing scope contract
        print("SC8 scoping advisory permissive:")
        db = setup(tmp, "c8", rigor="scoping")
        rv = record_idea(db, "c8", good_idea())  # no scope contract, scoping
        g = gate(db, "c8")["gates"]["scope_contract"]
        check("SC8 new: scoping idea validate not blocked by missing scope; gate advisory",
              rv.returncode == 0 and g["status"] == "advisory", "rv=%s gate=%s" % (rv.returncode, g))

        # SC9: gate status surfaces missing + invalid scope contract (bound)
        print("SC9 gate status surfaces missing/invalid scope:")
        db = setup(tmp, "c9")
        g_missing = gate(db, "c9")["gates"]["scope_contract"]
        record_scope(db, "c9", {**GOOD_SCOPE, "objective": "tbd"})  # invalid
        g_invalid = gate(db, "c9")["gates"]["scope_contract"]
        check("SC9 new: gate status scope_contract missing then fail-with-reason",
              g_missing["status"] == "missing" and g_invalid["status"] == "fail" and "objective" in (g_invalid["reason"] or ""),
              "missing=%s invalid=%s" % (g_missing, g_invalid))

        # SC10: stale scope contract -> idea validate fails + gate status stale
        print("SC10 stale scope contract:")
        db = setup(tmp, "c10")
        record_scope(db, "c10", GOOD_SCOPE)  # valid
        c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
        c.execute("UPDATE scope_contract SET contract=? WHERE quest_id='c10'",
                  (json.dumps({**GOOD_SCOPE, "objective": "a different objective entirely now"}),)); c.commit(); c.close()
        g = gate(db, "c10")["gates"]["scope_contract"]
        rv = record_idea(db, "c10", good_idea())
        check("SC10 new: contract changed after validate -> gate stale + idea validate blocked",
              g["status"] == "fail" and "stale" in (g["reason"] or "") and rv.returncode != 0 and "STALE" in rv.stdout,
              "gate=%s idea=%s" % (g, rv.stdout[:160]))

        # SC11: DEEPRESEARCH_SCOPE_GATE=0 waives the requirement and is visible
        print("SC11 scope waiver:")
        db = setup(tmp, "c11")
        rv = record_idea(db, "c11", good_idea())  # no scope, bound -> would fail
        rv_w = run(db, ["idea", "validate", "--quest-id", "c11"], {"DEEPRESEARCH_SCOPE_GATE": "0"})
        d = gate(db, "c11", {"DEEPRESEARCH_SCOPE_GATE": "0"})
        check("SC11 new: SCOPE_GATE=0 lets idea validate pass + waiver visible",
              rv.returncode != 0 and rv_w.returncode == 0 and "DEEPRESEARCH_SCOPE_GATE" in d["active_waivers"],
              "no=%s waived=%s active=%s" % (rv.returncode, rv_w.returncode, d.get("active_waivers")))

        # SC12: methodology check --stage scope resolves to the validated scope contract
        print("SC12 methodology check --stage scope:")
        db = setup(tmp, "c12")
        record_scope(db, "c12", GOOD_SCOPE)
        ok = run(db, ["methodology", "check", "--quest-id", "c12", "--stage", "scope", "--applied-as", "c12:sc"])
        bad = run(db, ["methodology", "check", "--quest-id", "c12", "--stage", "scope", "--applied-as", "nonexistent"])
        check("SC12 new: scope methodology resolves to the validated contract, rejects unresolvable",
              ok.returncode == 0 and jdata(ok)["resolves"] and bad.returncode != 0 and not jdata(bad)["resolves"],
              "ok=%s bad=%s" % (ok.stdout[:120], bad.returncode))

    print("\n%d passed, %d failed" % (len(PASSED), len(FAILED)))
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
