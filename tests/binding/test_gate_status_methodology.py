#!/usr/bin/env python3
"""integration suite — unified gate status, deterministic routing, methodology-evidence resolution, and the
integrated control loop catching old failure paths.

Run:  python3 tests/binding/test_gate_status_methodology.py   (exits non-zero on any failure)
"""
import json, os, subprocess, sqlite3, sys, tempfile, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
H = str(ROOT / "execplan" / "harness" / "bin" / "deepresearch")
AT = "2026-06-18T00:00:00Z"
WAIVE_SCHOL = {"DEEPRESEARCH_SCHOLARSHIP_MIN_REFS": "0", "DEEPRESEARCH_SCHOLARSHIP_MIN_REF_CLAIMS": "0"}
PASSED, FAILED = [], []


def run(db, args, extra_env=None):
    return subprocess.run([H, "--db", db, *args], capture_output=True, text=True, env={**os.environ, **(extra_env or {})})


def jdata(r):
    return json.loads(r.stdout)["data"]


def setup(tmp, qid, rigor="standard"):
    db = str(pathlib.Path(tmp) / ("state_%s.sqlite" % qid))
    run(db, ["state", "init"])
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    c.execute("INSERT INTO quest(quest_id,title,objective_ref,workspace_ref,run_state,rigor_level,baseline_gate,"
              "created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)", (qid, "t", "o", "w", "running", rigor, "pending", AT, AT))
    c.execute("INSERT INTO artifact(artifact_id,quest_id,kind,ref,created_at) VALUES(?,?,?,?,?)",
              (qid + ":rc", qid, "research-contract", "c", AT))
    c.commit(); c.close()
    return db


def rec(db, p, env=None):
    return run(db, ["record", "apply", "--json", json.dumps(p)], env)


def wj(tmp, name, obj):
    p = pathlib.Path(tmp) / name; p.write_text(json.dumps(obj)); return str(p)


def add_claim(db, qid, cid):
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    c.execute("INSERT INTO claim(claim_id,quest_id,statement,status,kind,created_at,updated_at) "
              "VALUES(?,?,?,?,?,?,?)", (cid, qid, "s", "supported", "claim", AT, AT))
    c.commit(); c.close()


_PROOF = {"main_result": {"metric": "acc", "direction": "higher"},
          "baseline_comparison": {"metric": "acc", "direction": "higher"},
          "ablation": {"changed_factor": "ln", "controls": "fixed", "delta": "+1.2"},
          "robustness": {"varied_condition": "4k", "original_condition": "1k", "criterion": "<2%"},
          "significance": {"method": "t-test", "effect": "p=0.01"}}


def link(db, cid, kinds, provenance_ok=1, proof=True):
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    qid = (c.execute("SELECT quest_id FROM claim WHERE claim_id=?", (cid,)).fetchone() or [None])[0]
    for i, ek in enumerate(kinds):
        ref = f"{cid}-{ek}-{i}"
        p = dict(_PROOF.get(ek, {}))
        if ek == "ablation":
            p["parent_result"] = ref  # resolves to this row's own (claim-mapped) result
        ep = json.dumps(p) if proof else None
        c.execute("INSERT INTO claim_evidence(claim_id,source_kind,source_ref,relation,evidence_kind,"
                  "evidence_proof,created_at) VALUES(?,?,?,?,?,?,?)", (cid, "result", ref, "supports", ek, ep, AT))
        c.execute("INSERT INTO result(result_id,quest_id,experiment_id,validity,artifact_ref,"
                  "provenance_route,provenance_ok,created_at) VALUES(?,?,?,?,?,?,?,?)",
                  (ref, qid, "E1", "valid", "a", "executed", provenance_ok, AT))
    c.commit(); c.close()


def good_idea(tmp, qid):
    s = {"objective_contract_ref": "o", "baseline_contract_ref": "WAIVER",
         "raw_slate": [{"candidate_id": x, "title": x, "hypothesis": "h", "mechanism": "m",
                        "expected_evidence": ["e"], "risk": "r"} for x in ("A", "B", "C")],
         "challenge": {"strongest_rejection": "x", "outside_family_alternative": "y", "why_retained_survives": "z"},
         "novelty_risk": {"novelty_label": "novel", "novelty_argument": "a", "risk_notes": "n",
                          "known_near_neighbors": ["Doe2024: closest prior (differs: our mechanism)"]},
         "selection_gate": [{"candidate_id": "A", "scores": {"novelty": 2, "falsifiability": 2, "feasibility": 2,
                             "evidence_potential": 1, "fit_to_objective": 1}, "total": 8, "verdict": "retain"},
                            {"candidate_id": "B", "scores": {"novelty": 1, "falsifiability": 1, "feasibility": 1,
                             "evidence_potential": 1, "fit_to_objective": 0}, "total": 4, "verdict": "reject"},
                            {"candidate_id": "C", "scores": {"novelty": 1, "falsifiability": 0, "feasibility": 1,
                             "evidence_potential": 1, "fit_to_objective": 0}, "total": 3, "verdict": "reject"}],
         "rejected": [{"candidate_id": "B", "reason": "weaker"}, {"candidate_id": "C", "reason": "infeasible"}],
         "retained": {"candidate_id": "A", "hypothesis": "h", "mechanism": "m", "claim_candidate": "C1",
                      "mvp_experiment_plan": "run X", "expected_failure_mode": "f", "boundary_condition": "b"}}
    ref = wj(tmp, qid + "_idea.json", s)
    rec(db_of[qid], {"record_type": "idea.select", "record_id": qid + ":s1", "at": AT, "quest_id": qid, "select_ref": ref})
    return run(db_of[qid], ["idea", "validate", "--quest-id", qid])


def good_bridge_obj():
    return {"supported_claims": ["C1"], "mechanism_interpretation": "pipeline-bound",
            "alternative_explanations": ["x"], "limitations": ["single GPU gen"], "failure_modes": ["tiny seqlen"],
            "recommended_claim_boundaries": ["fwd only"], "figure_table_recommendations": ["scatter"],
            "paper_facing_result_paragraphs": ["The model predicts FA4 latency within 6% MAPE."],
            "claim_to_evidence_map": {"C1": ["e1"]}, "evidence_to_section_recommendations": {"e1": "results"}}


def good_spine_obj():
    return {"thesis": "T", "core_contribution": "c", "central_mechanism": "m",
            "main_claims": [{"claim_id": "C1", "scope": "s", "what_would_falsify_it": "f", "evidence_needed": ["e"]}],
            "not_claiming": ["x"], "experiment_section_map": [{"section": "results", "thesis": "t"}],
            "display_plan": [{"display": "d", "claims": ["C1"]}],
            "reviewer_objections": [{"objection": "o", "answer_route": "a"}], "weak_points": ["w"]}


db_of = {}


def check(label, cond, detail=""):
    (PASSED if cond else FAILED).append(label)
    print(("  PASS " if cond else "  FAIL ") + label + (("  -- " + detail) if detail and not cond else ""))


def main():
    with tempfile.TemporaryDirectory() as tmp:
        # F1: methodology_used applied_as points to nothing -> rejected
        print("F1 methodology applied_as resolves to nothing:")
        db = setup(tmp, "f1")
        r = run(db, ["methodology", "check", "--quest-id", "f1", "--stage", "idea", "--applied-as", "nonexistent"])
        check("F1 new: methodology check REJECTS unresolvable applied_as", r.returncode != 0 and not jdata(r)["resolves"])

        # F2: idea methodology references an INVALID idea.select -> rejected
        print("F2 methodology references an invalid idea.select:")
        db = setup(tmp, "f2")
        ref = wj(tmp, "f2_idea.json", {"objective_contract_ref": "o", "baseline_contract_ref": "w",
                 "raw_slate": [], "challenge": {}, "novelty_risk": {}, "selection_gate": [], "rejected": [],
                 "retained": {}})  # invalid (will not pass idea validate)
        rec(db, {"record_type": "idea.select", "record_id": "f2:s1", "at": AT, "quest_id": "f2", "select_ref": ref})
        run(db, ["idea", "validate", "--quest-id", "f2"])  # leaves valid=0
        r = run(db, ["methodology", "check", "--quest-id", "f2", "--stage", "idea", "--applied-as", "f2:s1"])
        check("F2 new: methodology check REJECTS an unvalidated idea.select", r.returncode != 0 and not jdata(r)["resolves"])

        # F3: gate status with a failed idea gate -> route_target=idea
        print("F3 gate status routes a failed idea gate to 'idea':")
        db = setup(tmp, "f3")
        rec(db, {"record_type": "idea.select", "record_id": "f3:s1", "at": AT, "quest_id": "f3",
                 "select_ref": wj(tmp, "f3_idea.json", {"objective_contract_ref": "o", "baseline_contract_ref": "w",
                 "raw_slate": [], "challenge": {}, "novelty_risk": {}, "selection_gate": [], "rejected": [], "retained": {}})})
        run(db, ["idea", "validate", "--quest-id", "f3"])  # valid=0
        g = jdata(run(db, ["gate", "status", "--quest-id", "f3"]))["gates"]["idea_gate"]
        check("F3 new: gate status idea_gate fail -> route 'idea'", g["status"] == "fail" and g["route_target"] == "idea", str(g))

        # F4: insufficient campaign coverage -> route experiment/analysis
        print("F4 gate status routes insufficient coverage:")
        db = setup(tmp, "f4"); add_claim(db, "f4", "C1"); link(db, "C1", ["main_result"])  # missing baseline+anyof
        g = jdata(run(db, ["gate", "status", "--quest-id", "f4"]))["gates"]["campaign_coverage"]
        check("F4 new: campaign_coverage fail -> route experiment/analysis",
              g["status"] == "fail" and g["route_target"] in ("experiment", "analysis"), str(g))

        # F5: invalid review verdict -> route per review route
        print("F5 gate status routes an invalid/reject review verdict:")
        db = setup(tmp, "f5")
        ref = wj(tmp, "f5_v.json", {"verdict": "reject", "summary": "s", "missing_experiments": ["X"], "experiment_todo": ["run X"]})
        rec(db, {"record_type": "review.verdict", "record_id": "f5:v1", "at": AT, "quest_id": "f5", "verdict": "reject", "verdict_ref": ref})
        run(db, ["review", "validate", "--quest-id", "f5"])  # valid reject, route_target=experiment
        g = jdata(run(db, ["gate", "status", "--quest-id", "f5"]))["gates"]["review_verdict"]
        check("F5 new: review_verdict fail -> route per review route ('experiment')",
              g["status"] == "fail" and g["route_target"] == "experiment", str(g))

        # F6: all binding gates passing -> finalize_readiness=pass
        print("F6 all gates pass -> finalize_readiness=pass:")
        db = setup(tmp, "f6"); db_of["f6"] = db
        add_claim(db, "f6", "C1"); link(db, "C1", ["main_result", "baseline_comparison", "ablation"])
        rec(db, {"record_type": "scope.contract", "record_id": "f6:sc", "at": AT, "quest_id": "f6", "contract":
                 {"objective": "Predict FA4 forward latency within 6% MAPE", "research_question": "can a cost model predict it?",
                  "non_goals": "no backward", "primary_metric": "MAPE", "metric_direction": "minimize",
                  "dataset": "bench", "split": "test", "eval_protocol": "eval.py", "false_progress_signals": "train-split leak",
                  "baseline_route_expectation": "imported", "acceptance_criteria": "MAPE<8%"}})
        run(db, ["scope", "validate", "--quest-id", "f6"])  # idea selection (bound) requires a valid scope contract
        good_idea(tmp, "f6")
        rec(db, {"record_type": "baseline.contract", "record_id": "f6:bc", "at": AT, "quest_id": "f6",
                 "baseline_id": "b", "baseline_name": "BL", "comparison_policy": "higher-is-better",
                 "primary_metric_id": "acc", "dataset": "D", "split": "test", "eval_protocol": "eval.py",
                 "verification_verdict": "trusted_with_caveats", "baseline_route": "imported",
                 "evidence_ref": "Vaswani 2017, Table 2"})
        run(db, ["baseline", "validate", "--quest-id", "f6"])  # validator-owned valid=1
        rec(db, {"record_type": "quest.update", "record_id": "f6", "at": AT, "baseline_gate": "passed"})
        rec(db, {"record_type": "analysis.bridge", "record_id": "f6:b1", "at": AT, "quest_id": "f6",
                 "bridge_ref": wj(tmp, "f6_bridge.json", good_bridge_obj())})
        run(db, ["campaign", "validate", "--quest-id", "f6"])
        rec(db, {"record_type": "paper_spine.upsert", "record_id": "f6", "at": AT, "quest_id": "f6",
                 "spine_ref": wj(tmp, "f6_spine.json", good_spine_obj()), "thesis": "T", "n_core_claims": 1})
        man = pathlib.Path(tmp) / "f6_paper.md"; man.write_text("We study C1 on B200.")
        run(db, ["manuscript", "coverage", "--quest-id", "f6", "--artifact-ref", str(man), "--at", AT])
        rec(db, {"record_type": "review.verdict", "record_id": "f6:v1", "at": AT, "quest_id": "f6", "verdict": "accept",
                 "verdict_ref": wj(tmp, "f6_v.json", {"verdict": "accept", "summary": "clean"})})
        run(db, ["review", "validate", "--quest-id", "f6"])
        d = jdata(run(db, ["gate", "status", "--quest-id", "f6"], WAIVE_SCHOL))
        statuses = {k: v["status"] for k, v in d["gates"].items()}
        check("F6 new: every gate passes", all(s == "pass" for s in statuses.values()), str(statuses))
        check("F6 new: finalize_readiness=pass", d["finalize_readiness"] == "pass", d["finalize_readiness"])
        # F1b: a RESOLVING methodology check now passes (sanity)
        rr = run(db, ["methodology", "check", "--quest-id", "f6", "--stage", "idea", "--applied-as", "f6:s1"])
        check("F6 new: methodology check RESOLVES a valid idea.select", rr.returncode == 0 and jdata(rr)["resolves"])

        # F7: hard gate still blocks even if gate status is ignored (review reject -> finalize blocked)
        print("F7 hard gates remain authoritative (ignore gate status):")
        db = setup(tmp, "f7")
        # make coverage ready but leave review at reject -> the hard finalize REVIEW gate must block
        add_claim(db, "f7", "C1"); link(db, "C1", ["main_result"])
        rec(db, {"record_type": "paper_spine.upsert", "record_id": "f7", "at": AT, "quest_id": "f7",
                 "spine_ref": wj(tmp, "f7_spine.json", good_spine_obj()), "thesis": "T", "n_core_claims": 1})
        man = pathlib.Path(tmp) / "f7_paper.md"; man.write_text("We study C1 on B200.")
        run(db, ["manuscript", "coverage", "--quest-id", "f7", "--artifact-ref", str(man), "--at", AT])
        rec(db, {"record_type": "review.verdict", "record_id": "f7:v1", "at": AT, "quest_id": "f7", "verdict": "reject",
                 "verdict_ref": wj(tmp, "f7_v.json", {"verdict": "reject", "summary": "s", "rewrite_todo": ["fix"]})})
        run(db, ["review", "validate", "--quest-id", "f7"])
        fin = rec(db, {"record_type": "finalize.record", "record_id": "f7:fin", "at": AT, "quest_id": "f7", "outcome": "complete"},
                  WAIVE_SCHOL)
        check("F7 new: hard finalize gate blocks 'complete' despite gate status (review reject)",
              fin.returncode != 0 and "review" in (fin.stdout + fin.stderr).lower(), fin.stdout[:160])

        # F8: an env-var gate waiver is VISIBLE in gate status (status='waived', non-blocking, listed)
        print("F8 env-var gate waiver is surfaced, not silent:")
        db = setup(tmp, "f8")  # no idea.select -> idea_gate would be 'missing'/blocking when failing
        ref = wj(tmp, "f8_idea.json", {"objective_contract_ref": "o", "baseline_contract_ref": "w",
                 "raw_slate": [], "challenge": {}, "novelty_risk": {}, "selection_gate": [], "rejected": [], "retained": {}})
        rec(db, {"record_type": "idea.select", "record_id": "f8:s1", "at": AT, "quest_id": "f8", "select_ref": ref})
        run(db, ["idea", "validate", "--quest-id", "f8"])  # valid=0 -> idea_gate would fail
        base = jdata(run(db, ["gate", "status", "--quest-id", "f8"]))
        gw = jdata(run(db, ["gate", "status", "--quest-id", "f8"], {"DEEPRESEARCH_IDEA_GATE": "0"}))["gates"]["idea_gate"]
        check("F8 new: idea_gate blocks without waiver",
              base["gates"]["idea_gate"]["status"] == "fail" and base["gates"]["idea_gate"]["blocking"],
              str(base["gates"]["idea_gate"]))
        check("F8 new: env waiver surfaces status='waived', non-blocking, with source",
              gw["status"] == "waived" and gw["blocking"] is False and gw["waiver_source"] == "env:DEEPRESEARCH_IDEA_GATE",
              str(gw))
        d8 = jdata(run(db, ["gate", "status", "--quest-id", "f8"], {"DEEPRESEARCH_IDEA_GATE": "0"}))
        check("F8 new: active_waivers lists the override",
              "DEEPRESEARCH_IDEA_GATE" in d8.get("active_waivers", []), str(d8.get("active_waivers")))

        # F9: gate status reflects a provenance-less result (campaign coverage), and shows the waiver override
        print("F9 gate status reflects the provenance problem + waiver visibility:")
        db = setup(tmp, "f9"); add_claim(db, "f9", "C1")
        link(db, "C1", ["main_result", "baseline_comparison", "ablation"], provenance_ok=0)
        g9 = jdata(run(db, ["gate", "status", "--quest-id", "f9"]))["gates"]["campaign_coverage"]
        check("F9 new: campaign_coverage fail mentions provenance",
              g9["status"] == "fail" and "provenance" in (g9["reason"] or ""), str(g9))
        d9 = jdata(run(db, ["gate", "status", "--quest-id", "f9"], {"DEEPRESEARCH_PROVENANCE_GATE": "0"}))
        check("F9 new: PROVENANCE waiver listed + coverage passes when overridden",
              "DEEPRESEARCH_PROVENANCE_GATE" in d9.get("active_waivers", [])
              and d9["gates"]["campaign_coverage"]["status"] == "pass", str(d9.get("active_waivers")))

    print("\n%d passed, %d failed" % (len(PASSED), len(FAILED)))
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
