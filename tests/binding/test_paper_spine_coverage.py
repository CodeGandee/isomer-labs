#!/usr/bin/env python3
"""regression suite — proves the paper-spine + structural outline validator + validator-computed
manuscript coverage + finalize coverage gate REJECT failures the old system would accept.

Old system (for reference):
  - `outline validate` was a case-insensitive TOKEN GREP (_OUTLINE_CHECKS): any outline text containing the
    words thesis/claim/scope/evaluation_plan/evidence_grounding PASSED, regardless of structure.
  - there was NO manuscript-coverage validator and NO finalize coverage gate: `finalize_outcome=complete`
    passed once scholarship/authenticity (waivable) were met — a paper with unmapped results, evidence-less
    claims, or process traces could finalize.

Run:  python3 tests/binding/test_paper_spine_coverage.py   (exits non-zero on any failure)
"""
import json, os, subprocess, sqlite3, sys, tempfile, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
H = str(ROOT / "execplan" / "harness" / "bin" / "deepresearch")
AT = "2026-06-18T00:00:00Z"
# Waive the OTHER finalize gates so each test isolates the coverage gate (incl. the review gate).
WAIVE = {"DEEPRESEARCH_SCHOLARSHIP_MIN_REFS": "0", "DEEPRESEARCH_SCHOLARSHIP_MIN_REF_CLAIMS": "0",
         "DEEPRESEARCH_AUTHENTICITY_GATE": "0", "DEEPRESEARCH_COMPLETENESS_GATE_RIGOR": "none",
         "DEEPRESEARCH_REVIEW_GATE": "0"}
# Legacy token check (what `outline validate` used to be), reproduced to show the old grep is fooled.
_OLD_TOKENS = ["thesis", "claim", "scope", "evaluation_plan", "evidence_grounding"]

PASSED, FAILED = [], []


def run(db, args, stdin=None, extra_env=None):
    env = {**os.environ, **WAIVE, **(extra_env or {})}
    return subprocess.run([H, "--db", db, *args], capture_output=True, text=True, input=stdin, env=env)


def setup(tmp, qid, rigor="standard", contract=True):
    db = str(pathlib.Path(tmp) / ("state_%s.sqlite" % qid))
    run(db, ["state", "init"])
    c = sqlite3.connect(db)
    c.execute("INSERT INTO quest(quest_id,title,objective_ref,workspace_ref,run_state,rigor_level,"
              "created_at,updated_at) VALUES(?,?,?,?,?,?,?,?)", (qid, "t", "o:r", "w", "running", rigor, AT, AT))
    if contract:
        c.execute("INSERT INTO artifact(artifact_id,quest_id,kind,ref,created_at) VALUES(?,?,?,?,?)",
                  (qid + ":rc", qid, "research-contract", "runs/%s/contract.md" % qid, AT))
    c.commit(); c.close()
    return db


def add_spine_row(db, qid, spine_ref, thesis="T", n=1):
    payload = {"record_type": "paper_spine.upsert", "record_id": qid, "at": AT, "quest_id": qid,
               "spine_ref": spine_ref, "thesis": thesis, "n_core_claims": n}
    return run(db, ["record", "apply", "--json", json.dumps(payload)])


def _scaffold(db):
    c = sqlite3.connect(db)
    c.execute("PRAGMA foreign_keys=OFF")  # direct test scaffolding; harness writes keep FK on
    return c


def add_claim(db, qid, cid, status="supported", kind="claim"):
    c = _scaffold(db)
    c.execute("INSERT INTO claim(claim_id,quest_id,statement,status,kind,created_at,updated_at) "
              "VALUES(?,?,?,?,?,?,?)", (cid, qid, "s", status, kind, AT, AT))
    c.commit(); c.close()


def link_ev(db, cid, kind, ref):
    c = _scaffold(db)
    c.execute("INSERT INTO claim_evidence(claim_id,source_kind,source_ref,relation,created_at) "
              "VALUES(?,?,?,'supports',?)", (cid, kind, ref, AT))
    c.commit(); c.close()


def add_result(db, qid, rid):
    c = _scaffold(db)
    c.execute("INSERT INTO result(result_id,quest_id,experiment_id,artifact_ref,created_at) "
              "VALUES(?,?,?,?,?)", (rid, qid, "E1", "runs/%s/result.json" % qid, AT))
    c.commit(); c.close()


def finalize(db, qid):
    payload = {"record_type": "finalize.record", "record_id": qid + ":fin", "at": AT,
               "quest_id": qid, "outcome": "complete"}
    return run(db, ["record", "apply", "--json", json.dumps(payload)])


def write_json(tmp, name, obj):
    p = pathlib.Path(tmp) / name
    p.write_text(json.dumps(obj))
    return str(p)


def write_text(tmp, name, txt):
    p = pathlib.Path(tmp) / name
    p.write_text(txt)
    return str(p)


def check(label, cond, detail=""):
    (PASSED if cond else FAILED).append(label)
    print(("  PASS " if cond else "  FAIL ") + label + (("  -- " + detail) if detail and not cond else ""))


GOOD_SPINE = {
    "thesis": "A no-fitting cycle-level model predicts FA4 forward latency.",
    "core_contribution": "An analytic latency model with zero fitted constants.",
    "venue_style": "iclr", "central_mechanism": "pipeline-bound cost accounting",
    "main_claims": [{"claim_id": "C1", "scope": "FA4 forward on B200",
                     "what_would_falsify_it": "held-out MAPE > 10%", "evidence_needed": ["pred_vs_meas"]}],
    "not_claiming": ["does not model the backward pass"],
    "claim_evidence_map": {"C1": ["R1"]},
    "experiment_section_map": [{"section": "results", "thesis": "the model tracks measured latency",
                               "experiments": ["E1"], "claims": ["C1"]}],
    "display_plan": [{"display": "predicted-vs-measured scatter", "claims": ["C1"]}],
    "reviewer_objections": [{"objection": "is it overfit?", "answer_route": "no fitted constants; held-out eval",
                             "linked_claims": ["C1"]}],
    "weak_points": ["single GPU generation"], "followups": [],
}


def main():
    with tempfile.TemporaryDirectory() as tmp:
        # ---- J1: fragmented outline (no single thesis, >3 claims) ----
        print("J1 fragmented outline (no thesis, 4 claims):")
        bad = {**GOOD_SPINE, "thesis": "",
               "main_claims": [{"claim_id": f"C{i}", "scope": "s", "what_would_falsify_it": "f",
                                "evidence_needed": ["e"]} for i in range(4)]}
        ref = write_json(tmp, "j1.json", bad)
        db = setup(tmp, "j1")
        r = run(db, ["outline", "validate", "--spine-ref", ref])
        check("J1 new: outline validate REJECTS fragmented spine (structural)", r.returncode != 0)
        # old behavior: the legacy token-grep path accepts a structurally fragmented doc that merely contains
        # the keywords (no single thesis, no falsifiable claims).
        frag = ("# Working title\nWe discuss the thesis loosely. Some claims with scope. method_abstraction "
                "noted. evaluation_plan: baselines. evidence_grounding: must_not_claim X.")
        oldmd = write_text(tmp, "j1_old.md", frag)
        r_old = run(db, ["outline", "validate", "--artifact-ref", oldmd])
        check("J1 old: legacy token-grep path ACCEPTS the same fragmented doc", r_old.returncode == 0,
              r_old.stdout[:200])

        # ---- J2: non-falsifiable claim ----
        print("J2 non-falsifiable claim (empty what_would_falsify_it):")
        bad = json.loads(json.dumps(GOOD_SPINE))
        bad["main_claims"][0]["what_would_falsify_it"] = ""
        ref = write_json(tmp, "j2.json", bad)
        r = run(setup(tmp, "j2"), ["outline", "validate", "--spine-ref", ref])
        check("J2 new: outline validate REJECTS non-falsifiable claim", r.returncode != 0)

        # ---- J3: manuscript with process traces ----
        print("J3 manuscript with process traces (handoff/TODO/worktree):")
        db = setup(tmp, "j3")
        ref = write_json(tmp, "j3.json", GOOD_SPINE)
        add_spine_row(db, "j3", ref); add_claim(db, "j3", "C1"); link_ev(db, "C1", "result", "R1")
        add_result(db, "j3", "R1")
        man = write_text(tmp, "j3.md", "We study C1. See the handoff to the writer worktree. TODO: add table.")
        r = run(db, ["manuscript", "coverage", "--quest-id", "j3", "--artifact-ref", man, "--at", AT])
        ready = json.loads(r.stdout)["data"]["submission_ready"]
        check("J3 new: coverage marks NOT submission_ready (traces)", (not ready) and r.returncode != 0,
              r.stdout[:200])

        # ---- J4: claim not linked to evidence ----
        print("J4 main claim with no supporting evidence:")
        db = setup(tmp, "j4")
        ref = write_json(tmp, "j4.json", GOOD_SPINE)
        add_spine_row(db, "j4", ref); add_claim(db, "j4", "C1")  # NO link_ev
        man = write_text(tmp, "j4.md", "We study C1 on B200.")
        r = run(db, ["manuscript", "coverage", "--quest-id", "j4", "--artifact-ref", man, "--at", AT])
        ready = json.loads(r.stdout)["data"]["submission_ready"]
        check("J4 new: coverage marks NOT submission_ready (no evidence)", (not ready) and r.returncode != 0)

        # ---- J5: finalize gate (blocked without computed readiness; allowed after) ----
        print("J5 finalize coverage gate:")
        db = setup(tmp, "j5")
        ref = write_json(tmp, "j5.json", GOOD_SPINE)
        add_spine_row(db, "j5", ref); add_claim(db, "j5", "C1"); link_ev(db, "C1", "result", "R1")
        add_result(db, "j5", "R1")
        # 5a: finalize BEFORE coverage computed → blocked (submission_ready defaults 0)
        r = finalize(db, "j5")
        check("J5a new: finalize COMPLETE blocked (no validator-computed readiness)",
              r.returncode != 0 and "submission_ready" in (r.stdout + r.stderr), r.stdout[:200])
        # prove old behavior: a paper_spine artifact merely existing did NOT gate finalize (no coverage gate existed)
        # 5b: run coverage on a complete, clean manuscript → ready → finalize passes
        man = write_text(tmp, "j5.md", "We study C1 on B200; predicted-vs-measured scatter shown.")
        rc = run(db, ["manuscript", "coverage", "--quest-id", "j5", "--artifact-ref", man, "--at", AT])
        ready = json.loads(rc.stdout)["data"]["submission_ready"]
        check("J5b coverage computes submission_ready=true on a clean paper", ready, rc.stdout[:300])
        r = finalize(db, "j5")
        check("J5b new: finalize COMPLETE now allowed (coverage-confirmed)", r.returncode == 0, r.stdout[:200])

        # ---- regime: scoping rigor is advisory (does not block) ----
        print("Regime: scoping rigor is advisory:")
        db = setup(tmp, "sc", rigor="scoping")
        r = finalize(db, "sc")
        check("scoping rigor: coverage gate is advisory (finalize not blocked here)", r.returncode == 0,
              r.stdout[:200])

    print("\n%d passed, %d failed" % (len(PASSED), len(FAILED)))
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
