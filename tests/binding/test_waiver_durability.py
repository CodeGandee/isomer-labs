#!/usr/bin/env python3
"""regression suite — durable waiver acknowledgement / finalize acknowledgement.

Env-var gate waivers are visible in `gate status`, but a BOUND quest may not finalize 'complete' while a
finalize-sensitive gate is env-waived UNLESS a durable `quality_gate.waiver` (finalize_ack=true + reason)
exists for that gate. Scoping/advisory quests stay permissive. Recording uses the single write path
(`record apply --type quality_gate.waiver`); `gate waiver list` is the read-only audit view.

Run:  python3 tests/binding/test_waiver_durability.py   (exits non-zero on any failure)
"""
import json, os, subprocess, sqlite3, sys, tempfile, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
H = str(ROOT / "execplan" / "harness" / "bin" / "deepresearch")
AT = "2026-06-18T00:00:00Z"
# Neutralize the non-finalize-sensitive hygiene gates so the REVIEW gate is the one under test.
BASE = {"DEEPRESEARCH_SCHOLARSHIP_MIN_REFS": "0", "DEEPRESEARCH_SCHOLARSHIP_MIN_REF_CLAIMS": "0",
        "DEEPRESEARCH_COMPLETENESS_GATE_RIGOR": "none"}
REVIEW_WAIVED = {**BASE, "DEEPRESEARCH_REVIEW_GATE": "0"}  # review_verdict is finalize-sensitive

PASSED, FAILED = [], []


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
    """A bound, finalize-ready-EXCEPT-review quest: coverage submission_ready=1, no review verdict, no
    best_result_ref (authenticity vacuous). The only finalize blocker is the review gate."""
    db = str(pathlib.Path(tmp) / ("state_%s.sqlite" % qid))
    run(db, ["state", "init"])
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    c.execute("INSERT INTO quest(quest_id,title,objective_ref,workspace_ref,run_state,rigor_level,baseline_gate,"
              "created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)",
              (qid, "t", "o", "w", "running", rigor, "waived", AT, AT))
    c.execute("INSERT INTO artifact(artifact_id,quest_id,kind,ref,created_at) VALUES(?,?,?,?,?)",
              (qid + ":rc", qid, "research-contract", "c", AT))
    c.execute("INSERT INTO claim(claim_id,quest_id,statement,status,kind,created_at,updated_at) "
              "VALUES('C1',?, 's','supported','claim',?,?)", (qid, AT, AT))
    c.execute("INSERT INTO claim_evidence(claim_id,source_kind,source_ref,relation,created_at) "
              "VALUES('C1','result','R1','supports',?)", (AT,))
    c.execute("INSERT INTO result(result_id,quest_id,experiment_id,artifact_ref,created_at) "
              "VALUES('R1',?, 'E1','a',?)", (qid, AT))
    c.commit(); c.close()
    spine = {"thesis": "T", "core_contribution": "c", "central_mechanism": "m",
             "main_claims": [{"claim_id": "C1", "scope": "s", "what_would_falsify_it": "f", "evidence_needed": ["e"]}],
             "not_claiming": ["x"], "experiment_section_map": [{"section": "results", "thesis": "t"}],
             "display_plan": [{"display": "d", "claims": ["C1"]}],
             "reviewer_objections": [{"objection": "o", "answer_route": "a"}], "weak_points": ["w"]}
    ref = pathlib.Path(tmp) / (qid + "_spine.json"); ref.write_text(json.dumps(spine))
    rec(db, {"record_type": "paper_spine.upsert", "record_id": qid, "at": AT, "quest_id": qid,
             "spine_ref": str(ref), "thesis": "T", "n_core_claims": 1})
    man = pathlib.Path(tmp) / (qid + "_paper.md"); man.write_text("We study C1 on B200.")
    run(db, ["manuscript", "coverage", "--quest-id", qid, "--artifact-ref", str(man), "--at", AT])
    return db


def finalize(db, qid, extra_env):
    return rec(db, {"record_type": "finalize.record", "record_id": qid + ":fin", "at": AT, "quest_id": qid,
                    "outcome": "complete"}, extra_env)


def ack(db, qid, gate, reason="operator-acknowledged env waiver", finalize_ack=True, rid=None):
    return rec(db, {"record_type": "quality_gate.waiver", "record_id": rid or (qid + ":wv:" + gate), "at": AT,
                    "quest_id": qid, "gate": gate, "source": "env", "reason": reason, "finalize_ack": finalize_ack})


def main():
    with tempfile.TemporaryDirectory() as tmp:
        # W1: an env waiver of a finalize-sensitive gate is visible in gate status (active + ack-missing)
        print("W1 env waiver visible in gate status:")
        db = setup(tmp, "w1")
        d = jdata(run(db, ["gate", "status", "--quest-id", "w1"], REVIEW_WAIVED))
        check("W1 new: active_waivers + finalize_ack_missing surface the env waiver",
              "DEEPRESEARCH_REVIEW_GATE" in d["active_waivers"] and "review_verdict" in d["finalize_ack_missing"],
              "active=%s missing=%s" % (d["active_waivers"], d["finalize_ack_missing"]))

        # W2: env waiver ALONE is not enough to finalize a finalize-sensitive gate
        print("W2 env waiver alone does not finalize:")
        db = setup(tmp, "w2")
        r = finalize(db, "w2", REVIEW_WAIVED)
        check("W2 new: finalize BLOCKED (env waiver without durable acknowledgement)",
              r.returncode != 0 and "acknowledg" in (r.stdout + r.stderr).lower(), r.stdout[:220])

        # W3: durable acknowledgement (finalize_ack + reason) allows finalize where policy permits
        print("W3 durable ack with reason allows finalize:")
        db = setup(tmp, "w3")
        ack(db, "w3", "review_verdict", reason="reviewer unavailable; operator accepts the risk")
        r = finalize(db, "w3", REVIEW_WAIVED)
        check("W3 new: durable review_verdict ack allows finalize", r.returncode == 0, r.stdout[:220])

        # W4: a durable waiver WITHOUT a reason is rejected (schema requires reason)
        print("W4 durable waiver without reason rejected:")
        db = setup(tmp, "w4")
        r = rec(db, {"record_type": "quality_gate.waiver", "record_id": "w4:wv", "at": AT, "quest_id": "w4",
                     "gate": "review_verdict", "source": "env", "reason": "", "finalize_ack": True})
        check("W4 new: empty-reason waiver rejected at record apply", r.returncode != 0, r.stdout[:200])

        # W5: a waiver for one gate does NOT acknowledge an unrelated gate
        print("W5 waiver for one gate does not waive another:")
        db = setup(tmp, "w5")
        ack(db, "w5", "baseline_contract", reason="unrelated gate ack")  # wrong gate
        r = finalize(db, "w5", REVIEW_WAIVED)
        check("W5 new: ack for baseline_contract does not satisfy the review waiver (finalize still blocked)",
              r.returncode != 0 and "review_verdict" in (r.stdout + r.stderr), r.stdout[:220])

        # W6: scoping/advisory rigor stays permissive (no ack needed), waiver still visible
        print("W6 scoping rigor stays permissive:")
        db = setup(tmp, "w6", rigor="scoping")
        r = finalize(db, "w6", REVIEW_WAIVED)
        d = jdata(run(db, ["gate", "status", "--quest-id", "w6"], REVIEW_WAIVED))
        check("W6 new: scoping finalize allowed unacked AND waiver still visible",
              r.returncode == 0 and "DEEPRESEARCH_REVIEW_GATE" in d["active_waivers"], r.stdout[:200])

        # W7: gate status + gate waiver list expose the durable acknowledgement
        print("W7 durable waiver shown in gate status + gate waiver list:")
        db = setup(tmp, "w7")
        ack(db, "w7", "review_verdict", reason="documented exception")
        d = jdata(run(db, ["gate", "status", "--quest-id", "w7"], REVIEW_WAIVED))
        lst = jdata(run(db, ["gate", "waiver", "list", "--quest-id", "w7"]))
        check("W7 new: gate status shows ack present + nothing missing; gate waiver list shows the row",
              "review_verdict" in d["finalize_ack_present"] and d["finalize_ack_missing"] == []
              and lst["count"] == 1 and "review_verdict" in lst["finalize_ack_gates"],
              "present=%s missing=%s list=%s" % (d["finalize_ack_present"], d["finalize_ack_missing"], lst))

    print("\n%d passed, %d failed" % (len(PASSED), len(FAILED)))
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
