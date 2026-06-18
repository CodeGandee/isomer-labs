#!/usr/bin/env python3
"""regression suite — proves empirical sufficiency is now claim-level and binding (baseline contract +
per-claim campaign coverage by evidence_kind + a paper-facing analysis bridge gating analysis -> write).

Old system: baseline_gate was a bare enum an agent set freely; `result validate` checked per-run hygiene only
(no claim-level coverage, no evidence_kind); analysis was an artifact the Writer could consume as raw logs;
nothing blocked write on incomplete campaigns or a missing paper-facing bridge.

Run:  python3 tests/binding/test_campaign_bridge.py   (exits non-zero on any failure)
"""
import json, os, subprocess, sqlite3, sys, tempfile, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
H = str(ROOT / "execplan" / "harness" / "bin" / "deepresearch")
AT = "2026-06-18T00:00:00Z"
PASSED, FAILED = [], []


def run(db, args, extra_env=None):
    return subprocess.run([H, "--db", db, *args], capture_output=True, text=True, env={**os.environ, **(extra_env or {})})


def setup(tmp, qid, rigor="standard"):
    db = str(pathlib.Path(tmp) / ("state_%s.sqlite" % qid))
    run(db, ["state", "init"])
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    c.execute("INSERT INTO quest(quest_id,title,objective_ref,workspace_ref,run_state,rigor_level,baseline_gate,"
              "created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)",
              (qid, "t", "o", "w", "running", rigor, "pending", AT, AT))
    c.execute("INSERT INTO artifact(artifact_id,quest_id,kind,ref,created_at) VALUES(?,?,?,?,?)",
              (qid + ":rc", qid, "research-contract", "c", AT))
    c.commit(); c.close()
    return db


def add_claim(db, qid, cid):
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    c.execute("INSERT INTO claim(claim_id,quest_id,statement,status,kind,created_at,updated_at) "
              "VALUES(?,?,?,?,?,?,?)", (cid, qid, "s", "supported", "claim", AT, AT))
    c.commit(); c.close()


def link(db, cid, kind, evkinds):
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    for i, ek in enumerate(evkinds):
        c.execute("INSERT INTO claim_evidence(claim_id,source_kind,source_ref,relation,evidence_kind,created_at) "
                  "VALUES(?,?,?,?,?,?)", (cid, kind, f"{cid}-{ek}-{i}", "supports", ek, AT))
    c.commit(); c.close()


def add_round_write(db, qid):
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    c.execute("INSERT INTO round(quest_id,round_index,stage,status,created_at,updated_at) "
              "VALUES(?,?,?,?,?,?)", (qid, 7, "write", "open", AT, AT))
    c.commit(); c.close()


def rec(db, payload, extra_env=None):
    return run(db, ["record", "apply", "--json", json.dumps(payload)], extra_env)


def record_bridge(db, qid, ref):
    return rec(db, {"record_type": "analysis.bridge", "record_id": qid + ":b1", "at": AT, "quest_id": qid, "bridge_ref": ref})


def record_baseline(db, qid, verdict, waiver=None):
    p = {"record_type": "baseline.contract", "record_id": qid + ":bc1", "at": AT, "quest_id": qid,
         "baseline_id": "b", "verification_verdict": verdict}
    if waiver:
        p["waiver_reason"] = waiver
    return rec(db, p)


def set_baseline_gate(db, qid, value):
    return rec(db, {"record_type": "quest.update", "record_id": qid, "at": AT, "baseline_gate": value})


def open_write_handoff(db, qid):
    return rec(db, {"record_type": "handoff.open", "record_id": "%s:h1" % qid, "at": AT, "quest_id": qid,
                    "handoff_id": "h1", "round_index": 7, "schema_id": "deepresearch.email.task-request"})


def wj(tmp, name, obj):
    p = pathlib.Path(tmp) / name; p.write_text(json.dumps(obj)); return str(p)


def good_bridge():
    return {"supported_claims": ["C1"], "weakened_or_refuted_claims": [],
            "mechanism_interpretation": "the model is pipeline-bound",
            "alternative_explanations": ["memory-bound"], "limitations": ["single GPU generation"],
            "failure_modes": ["fails at tiny seqlen"], "recommended_claim_boundaries": ["forward only"],
            "figure_table_recommendations": ["predicted-vs-measured scatter"],
            "paper_facing_result_paragraphs": ["The model predicts FA4 forward latency within 6% MAPE across configs."],
            "claim_to_evidence_map": {"C1": ["R1", "ablate1"]},
            "evidence_to_section_recommendations": {"R1": "results"}}


def check(label, cond, detail=""):
    (PASSED if cond else FAILED).append(label)
    print(("  PASS " if cond else "  FAIL ") + label + (("  -- " + detail) if detail and not cond else ""))


def cov_valid(db, qid):
    r = run(db, ["campaign", "validate", "--quest-id", qid])
    return r


def main():
    with tempfile.TemporaryDirectory() as tmp:
        # J1: baseline_gate=passed with NO baseline.contract -> blocked
        print("J1 baseline_gate=passed without a baseline.contract:")
        db = setup(tmp, "j1")
        r = set_baseline_gate(db, "j1", "passed")
        check("J1 new: baseline_gate=passed blocked without a contract",
              r.returncode != 0 and "baseline.contract" in (r.stdout + r.stderr), r.stdout[:160])

        # J2: baseline waiver without a 'waived' verdict -> blocked
        print("J2 baseline_gate=waived without waived verdict/reason:")
        db = setup(tmp, "j2")
        record_baseline(db, "j2", "diverged")  # not waived, no waiver_reason
        r = set_baseline_gate(db, "j2", "waived")
        check("J2 new: baseline_gate=waived blocked without waived verdict + reason", r.returncode != 0, r.stdout[:160])

        # J3: claim with only one positive main_result -> coverage fails
        print("J3 claim with only main_result (no baseline/ablation/...):")
        db = setup(tmp, "j3"); add_claim(db, "j3", "C1"); link(db, "C1", "result", ["main_result"])
        record_bridge(db, "j3", wj(tmp, "j3.json", good_bridge()))
        r = cov_valid(db, "j3")
        check("J3 new: campaign validate REJECTS single-positive claim", r.returncode != 0, r.stdout[:200])

        # J4: superiority claim with no significance at publication rigor -> fails
        print("J4 superiority claim (baseline_comparison) without significance @ publication:")
        db = setup(tmp, "j4", rigor="publication"); add_claim(db, "j4", "C1")
        link(db, "C1", "result", ["main_result", "baseline_comparison", "ablation", "robustness"])
        record_bridge(db, "j4", wj(tmp, "j4.json", good_bridge()))
        r = cov_valid(db, "j4")
        check("J4 new: publication superiority needs significance", r.returncode != 0 and "significance" in r.stdout, r.stdout[:200])

        # J5: analysis bridge with no claim-evidence mapping -> fails
        print("J5 bridge with empty claim_to_evidence_map:")
        db = setup(tmp, "j5"); add_claim(db, "j5", "C1")
        link(db, "C1", "result", ["main_result", "baseline_comparison", "ablation"])
        b = good_bridge(); b["claim_to_evidence_map"] = {}
        record_bridge(db, "j5", wj(tmp, "j5.json", b))
        r = cov_valid(db, "j5")
        check("J5 new: bridge without claim->evidence map rejected", r.returncode != 0, r.stdout[:200])

        # J6: bridge with no paper-facing result paragraphs -> fails
        print("J6 bridge with no paper_facing_result_paragraphs:")
        db = setup(tmp, "j6"); add_claim(db, "j6", "C1")
        link(db, "C1", "result", ["main_result", "baseline_comparison", "ablation"])
        b = good_bridge(); b["paper_facing_result_paragraphs"] = []
        record_bridge(db, "j6", wj(tmp, "j6.json", b))
        r = cov_valid(db, "j6")
        check("J6 new: bridge without paper-facing paragraphs rejected", r.returncode != 0, r.stdout[:200])

        # J7: write handoff with NO analysis bridge -> blocked
        print("J7 write handoff without an analysis.bridge:")
        db = setup(tmp, "j7"); add_round_write(db, "j7")
        r = open_write_handoff(db, "j7")
        check("J7 new: write handoff blocked (no analysis bridge)",
              r.returncode != 0 and "analysis bridge" in (r.stdout + r.stderr), r.stdout[:160])

        # J8: write handoff with structurally-valid bridge but insufficient coverage -> blocked
        print("J8 write handoff with bridge but insufficient coverage:")
        db = setup(tmp, "j8"); add_round_write(db, "j8"); add_claim(db, "j8", "C1")
        link(db, "C1", "result", ["main_result"])  # insufficient
        record_bridge(db, "j8", wj(tmp, "j8.json", good_bridge()))
        cov_valid(db, "j8")  # sets valid=0 (coverage fails)
        r = open_write_handoff(db, "j8")
        check("J8 new: write handoff blocked (coverage insufficient -> bridge not valid)", r.returncode != 0, r.stdout[:160])

        # J9: valid baseline contract + sufficient coverage + valid bridge -> write handoff allowed
        print("J9 sufficient coverage + valid bridge:")
        db = setup(tmp, "j9"); add_round_write(db, "j9"); add_claim(db, "j9", "C1")
        link(db, "C1", "result", ["main_result", "baseline_comparison", "ablation"])
        record_baseline(db, "j9", "verified_match")
        rb = set_baseline_gate(db, "j9", "passed")
        record_bridge(db, "j9", wj(tmp, "j9.json", good_bridge()))
        rc = cov_valid(db, "j9")
        rh = open_write_handoff(db, "j9")
        check("J9 new: valid contract+coverage+bridge allows write handoff",
              rb.returncode == 0 and rc.returncode == 0 and rh.returncode == 0,
              "baseline=%s campaign=%s handoff=%s %s" % (rb.returncode, rc.returncode, rh.returncode,
                                                         (rc.stdout + rh.stdout + rh.stderr)[:200]))

        print("Regime: scoping rigor advisory:")
        db = setup(tmp, "sc", rigor="scoping"); add_round_write(db, "sc")
        r = open_write_handoff(db, "sc")
        check("scoping: analysis-bridge gate advisory (write not blocked)", r.returncode == 0, r.stdout[:160])

    print("\n%d passed, %d failed" % (len(PASSED), len(FAILED)))
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
