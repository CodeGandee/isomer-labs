#!/usr/bin/env python3
"""regression suite — proves the Reviewer verdict is now a typed, validator-backed, finalize-blocking,
routing-driving gate (not an advisory artifact).

Old system: a review produced an artifact (review.md) that nothing consumed; `finalize_outcome=complete`
never checked any verdict, and there was no notion of an actionable/valid verdict or verdict-driven routing.

Run:  python3 tests/binding/test_review_verdict.py   (exits non-zero on any failure)
"""
import json, os, subprocess, sqlite3, sys, tempfile, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
H = str(ROOT / "execplan" / "harness" / "bin" / "deepresearch")
AT = "2026-06-18T00:00:00Z"
# Waive the non-finalize gates so review (and, where noted, coverage) is the active gate. Authenticity passes
# vacuously here (no best_result_ref), so it needs NO env waiver — waiving it would trip the
# finalize-ack gate (an env-waived finalize-sensitive gate without a durable acknowledgement).
BASE = {"DEEPRESEARCH_SCHOLARSHIP_MIN_REFS": "0", "DEEPRESEARCH_SCHOLARSHIP_MIN_REF_CLAIMS": "0",
        "DEEPRESEARCH_COMPLETENESS_GATE_RIGOR": "none"}
REVIEW_ONLY = {**BASE, "DEEPRESEARCH_COVERAGE_GATE": "0"}  # isolate the review gate (J1-J5 block on review first)

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
    return db


def record_verdict(db, qid, vid, verdict, ref):
    p = {"record_type": "review.verdict", "record_id": vid, "at": AT, "quest_id": qid,
         "verdict": verdict, "verdict_ref": ref, "summary": "s"}
    return run(db, ["record", "apply", "--json", json.dumps(p)])


def finalize(db, qid, extra_env):
    p = {"record_type": "finalize.record", "record_id": qid + ":fin", "at": AT, "quest_id": qid, "outcome": "complete"}
    return run(db, ["record", "apply", "--json", json.dumps(p)], extra_env)


def write_json(tmp, name, obj):
    p = pathlib.Path(tmp) / name; p.write_text(json.dumps(obj)); return str(p)


def make_coverage_ready(db, qid, tmp):
    """Make coverage submission_ready=true (so J6/J7 isolate the review side)."""
    spine = {"thesis": "T", "core_contribution": "c", "central_mechanism": "m",
             "main_claims": [{"claim_id": "C1", "scope": "s", "what_would_falsify_it": "f", "evidence_needed": ["e"]}],
             "not_claiming": ["x"], "experiment_section_map": [{"section": "results", "thesis": "t"}],
             "display_plan": [{"display": "d", "claims": ["C1"]}],
             "reviewer_objections": [{"objection": "o", "answer_route": "a"}], "weak_points": ["w"]}
    ref = write_json(tmp, qid + "_spine.json", spine)
    run(db, ["record", "apply", "--json", json.dumps(
        {"record_type": "paper_spine.upsert", "record_id": qid, "at": AT, "quest_id": qid,
         "spine_ref": ref, "thesis": "T", "n_core_claims": 1})])
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    c.execute("INSERT INTO claim(claim_id,quest_id,statement,status,kind,created_at,updated_at) "
              "VALUES('C1',?, 's','supported','claim',?,?)", (qid, AT, AT))
    c.execute("INSERT INTO claim_evidence(claim_id,source_kind,source_ref,relation,created_at) "
              "VALUES('C1','result','R1','supports',?)", (AT,))
    c.execute("INSERT INTO result(result_id,quest_id,experiment_id,artifact_ref,created_at) "
              "VALUES('R1',?, 'E1','a',?)", (qid, AT))
    c.commit(); c.close()
    man = pathlib.Path(tmp) / (qid + "_paper.md"); man.write_text("We study C1 on B200.")
    run(db, ["manuscript", "coverage", "--quest-id", qid, "--artifact-ref", str(man), "--at", AT])


def check(label, cond, detail=""):
    (PASSED if cond else FAILED).append(label)
    print(("  PASS " if cond else "  FAIL ") + label + (("  -- " + detail) if detail and not cond else ""))


def main():
    with tempfile.TemporaryDirectory() as tmp:
        # J1: review artifact exists, but NO typed verdict -> finalize blocked
        print("J1 review artifact present but no typed verdict:")
        db = setup(tmp, "j1")
        c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
        c.execute("INSERT INTO artifact(artifact_id,quest_id,kind,ref,created_at) VALUES('j1:rev','j1','review','runs/j1/review.md',?)", (AT,))
        c.commit(); c.close()
        r = finalize(db, "j1", REVIEW_ONLY)
        check("J1 new: finalize blocked with no typed review verdict",
              r.returncode != 0 and "review verdict" in (r.stdout + r.stderr), r.stdout[:160])

        # J2: reject with generic criticism, no todos -> verdict INVALID -> finalize blocked
        print("J2 reject with no actionable todos:")
        db = setup(tmp, "j2")
        ref = write_json(tmp, "j2.json", {"verdict": "reject", "summary": "weak", "fatal_flaws": ["unconvincing"]})
        record_verdict(db, "j2", "j2:v1", "reject", ref)
        rv = run(db, ["review", "validate", "--quest-id", "j2"])
        check("J2 new: review validate REJECTS non-actionable reject", rv.returncode != 0)
        r = finalize(db, "j2", REVIEW_ONLY)
        check("J2 new: finalize blocked (verdict invalid)", r.returncode != 0)

        # J3: borderline with no follow-up todos -> invalid
        print("J3 borderline with no follow-up:")
        db = setup(tmp, "j3")
        ref = write_json(tmp, "j3.json", {"verdict": "borderline", "summary": "meh"})
        record_verdict(db, "j3", "j3:v1", "borderline", ref)
        rv = run(db, ["review", "validate", "--quest-id", "j3"])
        check("J3 new: review validate REJECTS non-actionable borderline", rv.returncode != 0)

        # J4: reject with missing_experiments -> routes to experiment
        print("J4 reject + missing_experiments routes to experiment:")
        db = setup(tmp, "j4")
        ref = write_json(tmp, "j4.json", {"verdict": "reject", "summary": "s",
                         "missing_experiments": ["baseline X"], "experiment_todo": ["run baseline X"]})
        record_verdict(db, "j4", "j4:v1", "reject", ref)
        rv = run(db, ["review", "validate", "--quest-id", "j4"])
        rt = run(db, ["review", "route", "--quest-id", "j4"])
        target = json.loads(rt.stdout)["data"]["route_target"]
        check("J4 new: valid reject routes to 'experiment'", rv.returncode == 0 and target == "experiment",
              "valid=%s target=%s" % (rv.returncode == 0, target))

        # J5: reject with overclaims -> routes to write
        print("J5 reject + overclaims routes to write:")
        db = setup(tmp, "j5")
        ref = write_json(tmp, "j5.json", {"verdict": "reject", "summary": "s",
                         "overclaims": ["claims SOTA without test"], "rewrite_todo": ["soften abstract"]})
        record_verdict(db, "j5", "j5:v1", "reject", ref)
        run(db, ["review", "validate", "--quest-id", "j5"])
        target = json.loads(run(db, ["review", "route", "--quest-id", "j5"]).stdout)["data"]["route_target"]
        check("J5 new: valid reject(overclaims) routes to 'write'", target == "write", "target=%s" % target)

        # J6: accept verdict but coverage NOT ready -> finalize blocked (by coverage gate)
        print("J6 accept but submission_ready=false:")
        db = setup(tmp, "j6")
        ref = write_json(tmp, "j6.json", {"verdict": "accept", "summary": "clean"})
        record_verdict(db, "j6", "j6:v1", "accept", ref)
        run(db, ["review", "validate", "--quest-id", "j6"])  # review side OK
        r = finalize(db, "j6", BASE)  # coverage gate ACTIVE, no spine -> not ready
        check("J6 new: accept does NOT bypass the coverage gate (finalize blocked, coverage)",
              r.returncode != 0 and "submission_ready" in (r.stdout + r.stderr), r.stdout[:160])

        # J7: accept + coverage ready -> finalize allowed
        print("J7 accept + submission_ready=true:")
        db = setup(tmp, "j7")
        make_coverage_ready(db, "j7", tmp)
        ref = write_json(tmp, "j7.json", {"verdict": "accept", "summary": "clean"})
        record_verdict(db, "j7", "j7:v1", "accept", ref)
        rv = run(db, ["review", "validate", "--quest-id", "j7"])
        r = finalize(db, "j7", BASE)
        check("J7 new: accept + coverage-ready finalizes", rv.returncode == 0 and r.returncode == 0,
              "rv=%s fin=%s %s" % (rv.returncode, r.returncode, (r.stdout[:160])))

        # regime: scoping rigor is advisory (review gate does not block)
        print("Regime: scoping rigor advisory:")
        db = setup(tmp, "sc", rigor="scoping")
        r = finalize(db, "sc", BASE)
        check("scoping: review gate advisory (finalize not blocked here)", r.returncode == 0, r.stdout[:160])

    print("\n%d passed, %d failed" % (len(PASSED), len(FAILED)))
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
