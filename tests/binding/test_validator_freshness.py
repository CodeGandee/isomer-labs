#!/usr/bin/env python3
"""regression suite — validator freshness / stale computed flags.

Each validator stamps a dependency FINGERPRINT onto its row; the consuming gates + gate status recompute it
and FAIL CLOSED (bound quests) when a dependency changed after validation. Scoping/advisory stays permissive
but staleness is still surfaced (gate status `stale_gates`). Waive with DEEPRESEARCH_FRESHNESS_GATE=0.

Run:  python3 tests/binding/test_validator_freshness.py   (exits non-zero on any failure)
"""
import json, os, subprocess, sqlite3, sys, tempfile, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
H = str(ROOT / "execplan" / "harness" / "bin" / "deepresearch")
AT = "2026-06-18T00:00:00Z"
FIN = {"DEEPRESEARCH_SCHOLARSHIP_MIN_REFS": "0", "DEEPRESEARCH_SCHOLARSHIP_MIN_REF_CLAIMS": "0",
       "DEEPRESEARCH_COMPLETENESS_GATE_RIGOR": "none"}  # neutralize the non-freshness finalize hygiene gates
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
    db = str(pathlib.Path(tmp) / ("s_%s.sqlite" % qid))
    run(db, ["state", "init"])
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    c.execute("INSERT INTO quest(quest_id,title,objective_ref,workspace_ref,run_state,rigor_level,baseline_gate,"
              "created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)", (qid, "t", "o", "w", "running", rigor, "pending", AT, AT))
    c.execute("INSERT INTO artifact(artifact_id,quest_id,kind,ref,created_at) VALUES(?,?,?,?,?)",
              (qid + ":rc", qid, "research-contract", "c", AT))
    c.execute("INSERT INTO experiment(experiment_id,quest_id,run_contract_ref,is_baseline,status,created_at,updated_at) "
              "VALUES('E1',?, 'rc',0,'done',?,?)", (qid, AT, AT))
    c.commit(); c.close()
    return db


def add_result(db, qid, rid, provenance_ok=1):
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    c.execute("INSERT INTO result(result_id,quest_id,experiment_id,validity,artifact_ref,provenance_route,"
              "provenance_ok,created_at) VALUES(?,?,?,?,?,?,?,?)", (rid, qid, "E1", "valid", "a", "executed", provenance_ok, AT))
    c.commit(); c.close()


def set_result_prov(db, rid, val):
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    c.execute("UPDATE result SET provenance_ok=? WHERE result_id=?", (val, rid)); c.commit(); c.close()


def baseline_reproduced(db, qid, result_ref):
    rec(db, {"record_type": "baseline.contract", "record_id": qid + ":bc", "at": AT, "quest_id": qid,
             "baseline_id": "b", "baseline_name": "BL", "comparison_policy": "higher-is-better",
             "primary_metric_id": "acc", "dataset": "D", "split": "test", "eval_protocol": "eval.py",
             "verification_verdict": "verified_match", "baseline_route": "reproduced", "evidence_ref": result_ref})
    return run(db, ["baseline", "validate", "--quest-id", qid])


def set_baseline_gate(db, qid, val, env=None):
    return rec(db, {"record_type": "quest.update", "record_id": qid, "at": AT, "baseline_gate": val}, env)


def add_claim(db, qid, cid):
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    c.execute("INSERT INTO claim(claim_id,quest_id,statement,status,kind,created_at,updated_at) "
              "VALUES(?,?,?,?,?,?,?)", (cid, qid, "s", "supported", "claim", AT, AT))
    c.commit(); c.close()


def link(db, qid, cid, ek_list):
    """campaign-grade supporting evidence: result-backed, provenance_ok=1, valid kind proof."""
    proofs = {"main_result": {"metric": "acc", "direction": "higher"},
              "baseline_comparison": {"metric": "acc", "direction": "higher"},
              "ablation": {"changed_factor": "ln", "controls": "fixed", "delta": "+1"}}
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    for i, ek in enumerate(ek_list):
        ref = f"{cid}-{ek}-{i}"
        p = dict(proofs.get(ek, {}))
        if ek == "ablation":
            p["parent_result"] = ref
        c.execute("INSERT INTO claim_evidence(claim_id,source_kind,source_ref,relation,evidence_kind,evidence_proof,"
                  "created_at) VALUES(?,?,?,?,?,?,?)", (cid, "result", ref, "supports", ek, json.dumps(p), AT))
        c.execute("INSERT INTO result(result_id,quest_id,experiment_id,validity,artifact_ref,provenance_route,"
                  "provenance_ok,created_at) VALUES(?,?,?,?,?,?,?,?)", (ref, qid, "E1", "valid", "a", "executed", 1, AT))
    c.commit(); c.close()


def add_plain_evidence(db, qid, cid, rid):
    """A plain supporting result link (used for manuscript coverage / mutation), no evidence_kind."""
    add_result(db, qid, rid)
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    c.execute("INSERT INTO claim_evidence(claim_id,source_kind,source_ref,relation,created_at) "
              "VALUES(?,?,?,?,?)", (cid, "result", rid, "supports", AT))
    c.commit(); c.close()


def good_bridge(tmp, qid):
    obj = {"supported_claims": ["C1"], "weakened_or_refuted_claims": [], "mechanism_interpretation": "x",
           "alternative_explanations": ["y"], "limitations": ["z"], "failure_modes": ["f"],
           "recommended_claim_boundaries": ["b"], "figure_table_recommendations": ["t"],
           "paper_facing_result_paragraphs": ["The method improves acc by 1.2 within 1%."],
           "claim_to_evidence_map": {"C1": ["r"]}, "evidence_to_section_recommendations": {"C1": ["results"]}}
    p = pathlib.Path(tmp) / (qid + "_bridge.json"); p.write_text(json.dumps(obj))
    rec(db_of[qid], {"record_type": "analysis.bridge", "record_id": qid + ":b1", "at": AT, "quest_id": qid,
                     "bridge_ref": str(p)})
    return run(db_of[qid], ["campaign", "validate", "--quest-id", qid])


def spine_and_coverage(tmp, qid, db):
    spine = {"thesis": "T", "core_contribution": "c", "central_mechanism": "m",
             "main_claims": [{"claim_id": "C1", "scope": "s", "what_would_falsify_it": "f", "evidence_needed": ["e"]}],
             "not_claiming": ["x"], "experiment_section_map": [{"section": "results", "thesis": "t"}],
             "display_plan": [{"display": "d", "claims": ["C1"]}],
             "reviewer_objections": [{"objection": "o", "answer_route": "a"}], "weak_points": ["w"]}
    ref = pathlib.Path(tmp) / (qid + "_spine.json"); ref.write_text(json.dumps(spine))
    rec(db, {"record_type": "paper_spine.upsert", "record_id": qid, "at": AT, "quest_id": qid,
             "spine_ref": str(ref), "thesis": "T", "n_core_claims": 1})
    man = pathlib.Path(tmp) / (qid + "_paper.md"); man.write_text("We study C1 on B200.")
    return run(db, ["manuscript", "coverage", "--quest-id", qid, "--artifact-ref", str(man), "--at", AT])


def review_accept(tmp, qid, db):
    ref = pathlib.Path(tmp) / (qid + "_v.json"); ref.write_text(json.dumps({"verdict": "accept", "summary": "clean"}))
    rec(db, {"record_type": "review.verdict", "record_id": qid + ":v1", "at": AT, "quest_id": qid,
             "verdict": "accept", "verdict_ref": str(ref)})
    return run(db, ["review", "validate", "--quest-id", qid])


def finalize(db, qid, env=None):
    return rec(db, {"record_type": "finalize.record", "record_id": qid + ":fin", "at": AT, "quest_id": qid,
                    "outcome": "complete"}, {**FIN, **(env or {})})


def gate(db, qid, env=None):
    return jdata(run(db, ["gate", "status", "--quest-id", qid], env))


db_of = {}


def main():
    with tempfile.TemporaryDirectory() as tmp:
        # S1: baseline.valid goes STALE when the referenced result's provenance changes after baseline validate
        print("S1 baseline stale after referenced result provenance changes:")
        db = setup(tmp, "s1"); add_result(db, "s1", "BR", provenance_ok=1)
        bv = baseline_reproduced(db, "s1", "BR")
        ok_gate = set_baseline_gate(db, "s1", "passed")  # fresh -> allowed
        set_result_prov(db, "BR", 0)                     # dependency changes AFTER validation
        g = gate(db, "s1")["gates"]["baseline_contract"]
        stale_gate = set_baseline_gate(db, "s1", "passed")  # now blocked: stale
        check("S1 new: fresh baseline passes; stale (result prov changed) -> gate status fail + hard gate blocks",
              bv.returncode == 0 and ok_gate.returncode == 0 and g["status"] == "fail" and "stale" in g["reason"]
              and stale_gate.returncode != 0 and "STALE" in (stale_gate.stdout + stale_gate.stderr),
              "ok=%s gate=%s stale=%s" % (ok_gate.returncode, g, stale_gate.returncode))

        # S2: analysis_bridge.valid goes STALE when claim evidence changes after campaign validate
        print("S2 analysis bridge stale after claim evidence changes:")
        db = setup(tmp, "s2"); db_of["s2"] = db; add_claim(db, "s2", "C1")
        link(db, "s2", "C1", ["main_result", "baseline_comparison", "ablation"])
        rec(db, {"record_type": "baseline.contract", "record_id": "s2:bc", "at": AT, "quest_id": "s2",
                 "baseline_id": "b", "baseline_name": "BL", "comparison_policy": "x", "primary_metric_id": "acc",
                 "dataset": "D", "split": "t", "eval_protocol": "e", "verification_verdict": "trusted_with_caveats",
                 "baseline_route": "imported", "evidence_ref": "cite"})
        run(db, ["baseline", "validate", "--quest-id", "s2"]); set_baseline_gate(db, "s2", "passed")
        cv = good_bridge(tmp, "s2")
        c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
        c.execute("INSERT INTO round(quest_id,round_index,stage,status,created_at,updated_at) VALUES('s2',7,'write','open',?,?)", (AT, AT))
        c.commit(); c.close()
        fresh_h = rec(db, {"record_type": "handoff.open", "record_id": "s2:h0", "at": AT, "quest_id": "s2",
                           "handoff_id": "h0", "round_index": 7, "schema_id": "deepresearch.email.task-request"})
        link(db, "s2", "C1", ["robustness"])  # evidence changes AFTER campaign validate
        g = gate(db, "s2")["gates"]["analysis_bridge"]
        stale_h = rec(db, {"record_type": "handoff.open", "record_id": "s2:h1", "at": AT, "quest_id": "s2",
                           "handoff_id": "h1", "round_index": 7, "schema_id": "deepresearch.email.task-request"})
        check("S2 new: fresh bridge allows write; stale (evidence changed) -> gate status fail + write handoff blocks",
              cv.returncode == 0 and fresh_h.returncode == 0 and g["status"] == "fail" and "stale" in g["reason"]
              and stale_h.returncode != 0 and "STALE" in (stale_h.stdout + stale_h.stderr),
              "cv=%s fresh=%s gate=%s stale=%s" % (cv.returncode, fresh_h.returncode, g, stale_h.returncode))

        # S3: manuscript coverage goes STALE when a claim is added after the coverage check
        print("S3 manuscript coverage stale after claims/evidence change:")
        db = setup(tmp, "s3"); add_claim(db, "s3", "C1"); add_plain_evidence(db, "s3", "C1", "R1")
        mc = spine_and_coverage(tmp, "s3", db)
        review_accept(tmp, "s3", db)
        fin_fresh = finalize(db, "s3")  # fresh -> allowed
        # undo the finalize marker so we can re-test the gate after mutation
        c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF"); c.execute("DELETE FROM finalize_outcome WHERE quest_id='s3'"); c.commit(); c.close()
        add_claim(db, "s3", "C2")  # manuscript dependency changes AFTER coverage
        g = gate(db, "s3")["gates"]["manuscript_coverage"]
        fin_stale = finalize(db, "s3")
        check("S3 new: fresh coverage finalizes; stale (claim added) -> gate status fail + finalize blocks",
              mc.returncode == 0 and fin_fresh.returncode == 0 and g["status"] == "fail" and "stale" in g["reason"]
              and fin_stale.returncode != 0 and "STALE" in (fin_stale.stdout + fin_stale.stderr),
              "mc=%s finfresh=%s gate=%s finstale=%s" % (mc.returncode, fin_fresh.returncode, g, fin_stale.stdout[:120]))

        # S4: review_verdict goes STALE when evidence changes after review validate (coverage re-freshened)
        print("S4 review verdict stale after reviewed paper state changes:")
        db = setup(tmp, "s4"); add_claim(db, "s4", "C1"); add_plain_evidence(db, "s4", "C1", "R1")
        spine_and_coverage(tmp, "s4", db)
        rvv = review_accept(tmp, "s4", db)
        add_plain_evidence(db, "s4", "C1", "R2")          # reviewed state changes AFTER review validate
        spine_and_coverage(tmp, "s4", db)                 # re-freshen ONLY coverage (not review)
        g = gate(db, "s4")["gates"]["review_verdict"]
        fin_stale = finalize(db, "s4")
        check("S4 new: stale review (evidence changed, review not re-run) -> gate status fail + finalize blocks",
              rvv.returncode == 0 and g["status"] == "fail" and "stale" in g["reason"]
              and fin_stale.returncode != 0 and "review" in (fin_stale.stdout + fin_stale.stderr).lower()
              and "STALE" in (fin_stale.stdout + fin_stale.stderr),
              "review_gate=%s finstale=%s" % (g, fin_stale.stdout[:160]))

        # S5: scoping/advisory stays permissive but staleness is still VISIBLE
        print("S5 scoping advisory: permissive but staleness visible:")
        db = setup(tmp, "s5", rigor="scoping"); add_result(db, "s5", "BR", provenance_ok=1)
        baseline_reproduced(db, "s5", "BR")
        set_result_prov(db, "BR", 0)  # make it stale
        rg = set_baseline_gate(db, "s5", "passed")  # scoping -> not blocked
        d = gate(db, "s5")
        check("S5 new: scoping baseline gate not blocked by staleness, but stale_gates lists it",
              rg.returncode == 0 and "baseline_contract" in d["stale_gates"],
              "gate=%s stale_gates=%s" % (rg.returncode, d.get("stale_gates")))

        # S6: DEEPRESEARCH_FRESHNESS_GATE=0 waives the freshness check (visible in active_waivers)
        print("S6 freshness waiver:")
        db = setup(tmp, "s6"); add_result(db, "s6", "BR", provenance_ok=1)
        baseline_reproduced(db, "s6", "BR"); set_baseline_gate(db, "s6", "passed")
        set_result_prov(db, "BR", 0)  # stale
        blocked = set_baseline_gate(db, "s6", "passed")  # bound -> blocked by staleness
        waived = set_baseline_gate(db, "s6", "passed", {"DEEPRESEARCH_FRESHNESS_GATE": "0"})  # waived -> allowed
        d = gate(db, "s6", {"DEEPRESEARCH_FRESHNESS_GATE": "0"})
        check("S6 new: staleness blocks bound; FRESHNESS_GATE=0 allows + is visible in active_waivers",
              blocked.returncode != 0 and waived.returncode == 0
              and "DEEPRESEARCH_FRESHNESS_GATE" in d["active_waivers"],
              "blocked=%s waived=%s active=%s" % (blocked.returncode, waived.returncode, d.get("active_waivers")))

    print("\n%d passed, %d failed" % (len(PASSED), len(FAILED)))
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
