#!/usr/bin/env python3
"""regression suite — proves the idea selection gate is now typed, validator-backed, and handoff-blocking
(shallow / single-proposal / decorative / below-floor / non-differentiated ideas cannot advance to experiment).

Old system: `idea` produced an idea row + advisory selection prose in the ideation-rubric pack; nothing checked
a slate, a scored veto, real rejections, or novelty, and nothing blocked the idea -> experiment handoff. An
agent could promote a single decorative tweak and dispatch experiments.

Run:  python3 tests/binding/test_idea_selection.py   (exits non-zero on any failure)
"""
import json, os, subprocess, sqlite3, sys, tempfile, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
H = str(ROOT / "execplan" / "harness" / "bin" / "deepresearch")
AT = "2026-06-18T00:00:00Z"
PASSED, FAILED = [], []


def run(db, args, extra_env=None):
    env = {**os.environ, **(extra_env or {})}
    return subprocess.run([H, "--db", db, *args], capture_output=True, text=True, env=env)


def setup(tmp, qid, rigor="standard"):
    db = str(pathlib.Path(tmp) / ("state_%s.sqlite" % qid))
    run(db, ["state", "init"])
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    c.execute("INSERT INTO quest(quest_id,title,objective_ref,workspace_ref,run_state,rigor_level,"
              "created_at,updated_at) VALUES(?,?,?,?,?,?,?,?)", (qid, "t", "o", "w", "running", rigor, AT, AT))
    c.execute("INSERT INTO artifact(artifact_id,quest_id,kind,ref,created_at) VALUES(?,?,?,?,?)",
              (qid + ":rc", qid, "research-contract", "c", AT))
    c.commit(); c.close()
    add_valid_scope(db, qid)  # idea selection (bound) requires a validator-confirmed scope/eval contract
    return db


GOOD_SCOPE = {"objective": "Predict FA4 forward latency within 6% MAPE across configs",
              "research_question": "Can a learned cost model predict FA4 latency?", "non_goals": "no backward pass",
              "primary_metric": "MAPE", "metric_direction": "minimize", "dataset": "FA4-bench", "split": "test",
              "eval_protocol": "eval.py --split test", "false_progress_signals": "metric on train split; one GPU only",
              "baseline_route_expectation": "imported", "acceptance_criteria": "MAPE < 8% on test",
              "constraints": "single GPU generation"}


def add_valid_scope(db, qid, contract=None):
    run(db, ["record", "apply", "--json", json.dumps(
        {"record_type": "scope.contract", "record_id": qid + ":sc", "at": AT, "quest_id": qid,
         "contract": contract or GOOD_SCOPE})])
    return run(db, ["scope", "validate", "--quest-id", qid])


def record_select(db, qid, sid, ref):
    p = {"record_type": "idea.select", "record_id": sid, "at": AT, "quest_id": qid, "select_ref": ref}
    return run(db, ["record", "apply", "--json", json.dumps(p)])


def write_json(tmp, name, obj):
    p = pathlib.Path(tmp) / name; p.write_text(json.dumps(obj)); return str(p)


def cand(cid):
    return {"candidate_id": cid, "title": cid, "hypothesis": "h", "mechanism": "m",
            "expected_evidence": ["e"], "risk": "r"}


def scores(total):
    # distribute `total` across the 5 criteria as evenly as possible (each 0..2)
    s = {k: 0 for k in ("novelty", "falsifiability", "feasibility", "evidence_potential", "fit_to_objective")}
    i = 0
    for k in s:
        add = min(2, total - sum(s.values()))
        s[k] = max(0, add); i += 1
    return s


def gate(cid, total, verdict="reject"):
    return {"candidate_id": cid, "scores": scores(total), "total": total, "verdict": verdict}


def good(retained_total=8, slate=("A", "B", "C"), novelty="novel", retained_id="A"):
    return {
        "objective_contract_ref": "runs/q/idea/obj.md",
        "baseline_contract_ref": "WAIVER: baseline contract deferred",
        "raw_slate": [cand(x) for x in slate],
        "challenge": {"strongest_rejection": "x", "outside_family_alternative": "y", "why_retained_survives": "z"},
        "novelty_risk": {"novelty_label": novelty, "novelty_argument": "arg", "risk_notes": "n",
                         "known_near_neighbors": ["Smith2023: prior method X (differs: our mechanism Y)"]},
        "selection_gate": [gate("A", retained_total, "retain")] + [gate(x, 4) for x in slate if x != "A"],
        "rejected": [{"candidate_id": x, "reason": "weaker mechanism"} for x in slate if x != "A"] or
                    [{"candidate_id": "Z", "reason": "infeasible"}],
        "retained": {"candidate_id": retained_id, "hypothesis": "h", "mechanism": "m", "claim_candidate": "c",
                     "mvp_experiment_plan": "run minimal X", "expected_failure_mode": "f", "boundary_condition": "b"},
    }


def confirm_gpu(db, qid):
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    c.execute("INSERT INTO gpu_allocation(quest_id,devices,status,confirmed_by,confirmed_at,updated_at) "
              "VALUES(?,?,?,?,?,?)", (qid, "0", "confirmed", "op", AT, AT))
    c.execute("INSERT INTO round(quest_id,round_index,stage,status,created_at,updated_at) "
              "VALUES(?,?,?,?,?,?)", (qid, 1, "experiment", "open", AT, AT))
    c.commit(); c.close()


def open_exp_handoff(db, qid):
    p = {"record_type": "handoff.open", "record_id": "%s:h1" % qid, "at": AT, "quest_id": qid,
         "handoff_id": "h1", "round_index": 1, "schema_id": "deepresearch.email.task-request"}
    return run(db, ["record", "apply", "--json", json.dumps(p)])


def check(label, cond, detail=""):
    (PASSED if cond else FAILED).append(label)
    print(("  PASS " if cond else "  FAIL ") + label + (("  -- " + detail) if detail and not cond else ""))


def validate_fails(tmp, qid, content, label):
    db = setup(tmp, qid)
    ref = write_json(tmp, qid + ".json", content)
    record_select(db, qid, qid + ":s1", ref)
    r = run(db, ["idea", "validate", "--quest-id", qid])
    check(label, r.returncode != 0, r.stdout[:200])


def main():
    with tempfile.TemporaryDirectory() as tmp:
        print("J1 single proposal (slate of 1):")
        validate_fails(tmp, "j1", good(slate=("A",)), "J1 new: idea validate REJECTS single-proposal slate")

        print("J2 slate below floor (2 < 3):")
        validate_fails(tmp, "j2", good(slate=("A", "B")), "J2 new: idea validate REJECTS below-floor slate")

        print("J3 decorative (not_differentiated):")
        validate_fails(tmp, "j3", good(novelty="not_differentiated"),
                       "J3 new: idea validate REJECTS not_differentiated")

        print("J4 missing challenge fields (no outside-family alternative):")
        bad = good(); bad["challenge"].pop("outside_family_alternative")
        validate_fails(tmp, "j4", bad, "J4 new: idea validate REJECTS missing strongest-rejection/outside-family")

        print("J5 retained score below floor (5 < 6):")
        validate_fails(tmp, "j5", good(retained_total=5), "J5 new: idea validate REJECTS retained below score floor")

        print("J6 retained not in slate:")
        validate_fails(tmp, "j6", good(retained_id="Q"), "J6 new: idea validate REJECTS retained not in slate")

        print("J7 rejected without concrete reason:")
        bad = good(); bad["rejected"] = [{"candidate_id": "B", "reason": ""}]
        validate_fails(tmp, "j7", bad, "J7 new: idea validate REJECTS rejection without a reason")

        print("J8 idea->experiment handoff without a passing idea.select:")
        db = setup(tmp, "j8"); confirm_gpu(db, "j8")  # GPU confirmed so only the idea gate can block
        r = open_exp_handoff(db, "j8")
        check("J8 new: experiment handoff BLOCKED (no valid idea.select)",
              r.returncode != 0 and "idea selection" in (r.stdout + r.stderr), r.stdout[:200])

        print("J9 valid idea.select passes + allows idea->experiment:")
        db = setup(tmp, "j9"); confirm_gpu(db, "j9")
        ref = write_json(tmp, "j9.json", good())
        record_select(db, "j9", "j9:s1", ref)
        rv = run(db, ["idea", "validate", "--quest-id", "j9"])
        rh = open_exp_handoff(db, "j9")
        check("J9 new: valid idea.select passes + experiment handoff allowed",
              rv.returncode == 0 and rh.returncode == 0, "validate=%s handoff=%s %s"
              % (rv.returncode, rh.returncode, (rh.stdout + rh.stderr)[:200]))

        print("J10 novelty=novel with no known_near_neighbors (ungrounded novelty):")
        bad = good(); bad["novelty_risk"]["known_near_neighbors"] = []
        validate_fails(tmp, "j10", bad, "J10 new: idea validate REJECTS novel with empty known_near_neighbors")

        print("J10b same but with an explicit novelty_waiver (escape hatch):")
        db = setup(tmp, "j10b")
        w = good(); w["novelty_risk"]["known_near_neighbors"] = []; w["novelty_waiver"] = "greenfield problem; no close prior"
        ref = write_json(tmp, "j10b.json", w)
        record_select(db, "j10b", "j10b:s1", ref)
        rw = run(db, ["idea", "validate", "--quest-id", "j10b"])
        check("J10b new: novelty_waiver allows ungrounded novel", rw.returncode == 0, rw.stdout[:200])

        print("Regime: scoping rigor advisory:")
        db = setup(tmp, "sc", rigor="scoping"); confirm_gpu(db, "sc")
        r = open_exp_handoff(db, "sc")
        check("scoping: idea gate advisory (handoff not blocked here)", r.returncode == 0, r.stdout[:160])

    print("\n%d passed, %d failed" % (len(PASSED), len(FAILED)))
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
