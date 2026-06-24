#!/usr/bin/env python3
"""regression suite — quest-local discovery: research opportunity ledger (research_opportunity).

A typed, ADVISORY, QUEST-LOCAL record of "what to try next and why", grounded in this quest's evidence.
It is NOT a gate: open opportunities never block a transition or finalize. Surfaced via `opportunity list`,
the `gate status` data.discovery block, and the `plan render` Discovery section. There is NO cross-quest /
global / shared discovery memory. Also covers the `bo status` honesty fix (heuristic streak, not real BO).

Run:  python3 tests/binding/test_discovery.py   (exits non-zero on any failure)
"""
import json, os, subprocess, sqlite3, sys, tempfile, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
H = str(ROOT / "execplan" / "harness" / "bin" / "deepresearch")
AT = "2026-06-18T00:00:00Z"
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
    db = str(pathlib.Path(tmp) / ("d_%s.sqlite" % qid))
    run(db, ["state", "init"])
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    c.execute("INSERT INTO quest(quest_id,title,objective_ref,workspace_ref,run_state,rigor_level,baseline_gate,"
              "created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)", (qid, "t", "o", "w", "running", rigor, "pending", AT, AT))
    c.execute("INSERT INTO artifact(artifact_id,quest_id,kind,ref,created_at) VALUES(?,?,?,?,?)",
              (qid + ":rc", qid, "research-contract", "c", AT))
    c.commit(); c.close()
    return db


def opp(db, qid, oid, kind="ablation", status="open", refs=None, by="orchestrator", sig=None,
        rationale="prior run plateaued; isolate the layernorm factor"):
    p = {"record_type": "opportunity.record", "record_id": oid, "at": AT, "quest_id": qid, "kind": kind,
         "rationale": rationale, "status": status, "proposed_by": by}
    if refs is not None:
        p["motivating_refs"] = refs
    if sig is not None:
        p["attempt_signature"] = sig
    return rec(db, p)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        # D1: record an opportunity quest-locally + it shows in opportunity list (open first)
        print("D1 record opportunity + list:")
        db = setup(tmp, "d1")
        r1 = opp(db, "d1", "d1:o1", kind="ablation",
                 refs={"finding": ["d1:f1"], "result": ["d1:R1"], "claim": ["C1"]})
        lst = jdata(run(db, ["opportunity", "list", "--quest-id", "d1"]))
        row = lst["opportunities"][0] if lst["opportunities"] else {}
        check("D1 new: opportunity recorded + listed with kind/status/refs/proposed_by",
              r1.returncode == 0 and lst["count"] == 1 and lst["open"] == 1 and row.get("kind") == "ablation"
              and row.get("status") == "open" and row.get("motivating_refs", {}).get("result") == ["d1:R1"]
              and row.get("proposed_by") == "orchestrator", str(lst))

        # D2: required fields validated (kind enum + rationale required); bad records rejected
        print("D2 schema validation:")
        db = setup(tmp, "d2")
        bad_kind = rec(db, {"record_type": "opportunity.record", "record_id": "d2:o", "at": AT, "quest_id": "d2",
                            "kind": "wild_guess", "rationale": "x"})
        no_rat = rec(db, {"record_type": "opportunity.record", "record_id": "d2:o2", "at": AT, "quest_id": "d2",
                          "kind": "ablation"})
        check("D2 new: invalid kind + missing rationale rejected",
              bad_kind.returncode != 0 and no_rat.returncode != 0, "kind=%s rat=%s" % (bad_kind.returncode, no_rat.returncode))

        # D3: gate status carries a NON-BLOCKING discovery block (open opportunities + recommended next actions)
        print("D3 gate status discovery block (non-blocking):")
        db = setup(tmp, "d3")
        opp(db, "d3", "d3:o1", kind="robustness", status="open")
        opp(db, "d3", "d3:o2", kind="new_idea", status="addressed")  # not open -> not recommended
        d = jdata(run(db, ["gate", "status", "--quest-id", "d3"]))
        disc = d.get("discovery", {})
        check("D3 new: discovery shows the open opportunity + a recommended action; NOT in blocking_gates",
              len(disc.get("open_opportunities", [])) == 1 and disc["open_opportunities"][0]["kind"] == "robustness"
              and any("robustness" in a for a in disc.get("recommended_next_actions", []))
              and "scope_contract" not in [] and "discovery" not in d.get("blocking_gates", [])
              and not any("opportunity" in g for g in d.get("blocking_gates", [])), str(disc))

        # D3b: opportunities do NOT block finalize readiness (advisory only)
        print("D3b opportunities never block finalize:")
        # an open opportunity present, but finalize_readiness reflects the gates only (advisory quest here = bound w/o work)
        fr_before = d["finalize_readiness"]
        check("D3b new: finalize_readiness unaffected by open opportunities (no new blocker)",
              fr_before in ("fail", "pass") and not any("opportunity" in g or "discovery" in g for g in d["blocking_gates"]),
              "fr=%s blocking=%s" % (fr_before, d["blocking_gates"]))

        # D4: plan render shows a Discovery / Next candidates section
        print("D4 plan render discovery section:")
        db = setup(tmp, "d4")
        opp(db, "d4", "d4:o1", kind="boundary", status="open")
        ps = run(db, ["plan", "status", "--quest-id", "d4"])
        out = ps.stdout
        check("D4 new: plan render has a Discovery section listing the next candidate",
              "## Discovery" in out and "Next candidates:" in out and "d4:o1(boundary)" in out, out[-400:])

        # D5: bo status honesty — heuristic streak, not real BO
        print("D5 bo status honesty:")
        db = setup(tmp, "d5")
        c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
        c.execute("INSERT INTO experiment(experiment_id,quest_id,run_contract_ref,is_baseline,status,created_at,updated_at) "
                  "VALUES('E1','d5','rc',0,'done',?,?)", (AT, AT))
        # three primary observations: 0.5, 0.7 (new best), 0.6 (no improve) -> streak should be 1
        for i, (rid, val, ts) in enumerate([("R1", 0.5, "2026-06-18T00:00:01Z"), ("R2", 0.7, "2026-06-18T00:00:02Z"),
                                            ("R3", 0.6, "2026-06-18T00:00:03Z")]):
            c.execute("INSERT INTO result(result_id,quest_id,experiment_id,validity,artifact_ref,created_at) "
                      "VALUES(?,?,?,?,?,?)", (rid, "d5", "E1", "valid", "a", ts))
            c.execute("INSERT INTO measurement(measurement_id,result_id,metric_name,value_num,is_primary,created_at) "
                      "VALUES(?,?,?,?,?,?)", (f"m{i}", rid, "acc", val, 1, ts))
        c.commit(); c.close()
        bs = jdata(run(db, ["bo", "status", "--quest-id", "d5"]))
        check("D5 new: bo status computes the streak + declares NOT full statistical BO (honest)",
              bs["best_primary"] == 0.7 and bs["observations"] == 3 and bs["no_improvement_streak"] == 1
              and "NOT full statistical" in bs["method"], str(bs))

        # D6: scoping/advisory unchanged — discovery present, gates still advisory, nothing blocks
        print("D6 scoping advisory unchanged:")
        db = setup(tmp, "d6", rigor="scoping")
        opp(db, "d6", "d6:o1", status="open")
        d = jdata(run(db, ["gate", "status", "--quest-id", "d6"]))
        check("D6 new: scoping gates advisory + discovery present + no blocking gates",
              d["gates"]["scope_contract"]["status"] == "advisory" and d["blocking_gates"] == []
              and len(d["discovery"]["open_opportunities"]) == 1, str(d.get("blocking_gates")))

        # D7: QUEST-LOCAL — an opportunity in quest A is never listed for quest B
        print("D7 quest-local isolation:")
        dba = setup(tmp, "da"); dbb = setup(tmp, "db")
        opp(dba, "da", "da:o1", status="open")
        la = jdata(run(dba, ["opportunity", "list", "--quest-id", "da"]))
        lb = jdata(run(dbb, ["opportunity", "list", "--quest-id", "db"]))
        # also confirm querying db's quest never surfaces da's opportunity (separate DBs == strict isolation)
        check("D7 new: opportunities are quest-local (A has 1, B has 0)",
              la["count"] == 1 and lb["count"] == 0, "A=%s B=%s" % (la["count"], lb["count"]))

        # D8: upsert lifecycle — status can advance open -> addressed (planning ledger, not append-only)
        print("D8 opportunity status lifecycle:")
        db = setup(tmp, "d8")
        opp(db, "d8", "d8:o1", status="open")
        opp(db, "d8", "d8:o1", status="addressed")  # same id -> upsert
        lst = jdata(run(db, ["opportunity", "list", "--quest-id", "d8"]))
        check("D8 new: re-record advances status (1 row, addressed)",
              lst["count"] == 1 and lst["open"] == 0 and lst["opportunities"][0]["status"] == "addressed", str(lst))

        # ---- finding lineage + motivating-refs resolution ----
        print("B1 finding with quest-local lineage links:")
        db = setup(tmp, "b1")
        c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
        c.execute("INSERT INTO experiment(experiment_id,quest_id,run_contract_ref,is_baseline,status,created_at,updated_at) "
                  "VALUES('E1','b1','rc',0,'done',?,?)", (AT, AT))
        c.execute("INSERT INTO result(result_id,quest_id,experiment_id,validity,artifact_ref,created_at) "
                  "VALUES('b1:R1','b1','E1','valid','a',?)", (AT,))
        c.execute("INSERT INTO claim(claim_id,quest_id,statement,status,kind,created_at,updated_at) "
                  "VALUES('C1','b1','s','refuted','claim',?,?)", (AT, AT))
        c.commit(); c.close()
        rf = rec(db, {"record_type": "finding.add", "record_id": "b1:f1", "at": AT, "quest_id": "b1", "scope": "quest",
                      "kind": "lesson", "summary": "approach X failed on long-seq",
                      "links": {"result_ids": ["b1:R1"], "claim_ids": ["C1"], "experiment_id": "E1"}})
        fq = jdata(run(db, ["findings", "query", "--quest-id", "b1"]))
        row = next((x for x in fq["rows"] if x.get("memory_id") == "b1:f1"), {})
        links = json.loads(row["links"]) if row.get("links") else {}
        check("B1 new: finding stores + round-trips quest-local links",
              rf.returncode == 0 and links.get("result_ids") == ["b1:R1"] and links.get("claim_ids") == ["C1"]
              and links.get("experiment_id") == "E1", str(row))

        print("B2 opportunity with valid motivating_refs resolves cleanly:")
        db = setup(tmp, "b2")
        c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
        c.execute("INSERT INTO experiment(experiment_id,quest_id,run_contract_ref,is_baseline,status,created_at,updated_at) "
                  "VALUES('E1','b2','rc',0,'done',?,?)", (AT, AT))
        c.execute("INSERT INTO result(result_id,quest_id,experiment_id,validity,artifact_ref,created_at) "
                  "VALUES('b2:R1','b2','E1','valid','a',?)", (AT,))
        c.commit(); c.close()
        opp(db, "b2", "b2:o1", kind="ablation", refs={"result": ["b2:R1"], "experiment": ["E1"]})
        ck = jdata(run(db, ["opportunity", "check", "--quest-id", "b2"]))
        lst = jdata(run(db, ["opportunity", "list", "--quest-id", "b2"]))
        check("B2 new: valid refs -> check all_resolved + list reports 0 unresolved",
              ck["all_resolved"] is True and lst["with_unresolved_refs"] == 0
              and lst["opportunities"][0]["unresolved_refs"] == [], str(ck))

        print("B3 opportunity with missing refs surfaced as advisory warning:")
        db = setup(tmp, "b3")
        opp(db, "b3", "b3:o1", kind="robustness", refs={"result": ["b3:GHOST"]})
        lst = run(db, ["opportunity", "list", "--quest-id", "b3"])
        ck = jdata(run(db, ["opportunity", "check", "--quest-id", "b3"]))
        disc = jdata(run(db, ["gate", "status", "--quest-id", "b3"]))["discovery"]
        un = ck["unresolved"][0]["unresolved_refs"][0] if ck["unresolved"] else {}
        check("B3 new: missing ref -> list warning + check unresolved(missing) + gate-status discovery warns",
              json.loads(lst.stdout).get("warnings") and un.get("status") == "missing"
              and len(disc.get("opportunities_with_unresolved_refs", [])) == 1, "ck=%s disc=%s" % (ck, disc.get("opportunities_with_unresolved_refs")))

        print("B4 cross-quest motivating_ref flagged cross_quest (NOT cross-quest memory):")
        db = str(pathlib.Path(tmp) / "b4.sqlite"); run(db, ["state", "init"])
        c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
        for qid in ("qa", "qb"):
            c.execute("INSERT INTO quest(quest_id,title,objective_ref,workspace_ref,run_state,rigor_level,baseline_gate,"
                      "created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)", (qid, "t", "o", "w", "running", "standard", "pending", AT, AT))
            c.execute("INSERT INTO artifact(artifact_id,quest_id,kind,ref,created_at) VALUES(?,?,?,?,?)", (qid + ":rc", qid, "research-contract", "c", AT))
        c.execute("INSERT INTO experiment(experiment_id,quest_id,run_contract_ref,is_baseline,status,created_at,updated_at) VALUES('EA','qa','rc',0,'done',?,?)", (AT, AT))
        c.execute("INSERT INTO result(result_id,quest_id,experiment_id,validity,artifact_ref,created_at) VALUES('qa:R1','qa','EA','valid','a',?)", (AT,))
        c.commit(); c.close()
        opp(db, "qb", "qb:o1", kind="next_experiment", refs={"result": ["qa:R1"]})  # qb cites qa's result
        ck = jdata(run(db, ["opportunity", "check", "--quest-id", "qb"]))
        st = ck["unresolved"][0]["unresolved_refs"][0]["status"] if ck["unresolved"] else ""
        check("B4 new: a ref owned by another quest is flagged 'cross_quest' (advisory, not usable)",
              st == "cross_quest", str(ck))

        print("B5 unresolved refs never block (no blocking gate, finalize unaffected):")
        d = jdata(run(db, ["gate", "status", "--quest-id", "qb"]))
        check("B5 new: unresolved opportunity refs not in blocking_gates",
              not any("opportunity" in g or "discovery" in g for g in d["blocking_gates"])
              and len(d["discovery"]["opportunities_with_unresolved_refs"]) == 1, str(d["blocking_gates"]))

        print("B6 plan render marks an unresolved opportunity:")
        ps = run(db, ["plan", "status", "--quest-id", "qb"])
        check("B6 new: plan render flags !unresolved-refs on the next candidate",
              "!unresolved-refs" in ps.stdout, ps.stdout[-300:])

        print("B7 bo status objective_sense reads from scope contract (minimize):")
        db = setup(tmp, "b7")
        rec(db, {"record_type": "scope.contract", "record_id": "b7:sc", "at": AT, "quest_id": "b7", "contract":
                 {"objective": "Minimize FA4 latency MAPE on test", "research_question": "q", "non_goals": "n",
                  "primary_metric": "MAPE", "metric_direction": "minimize", "dataset": "d", "split": "test",
                  "eval_protocol": "e", "false_progress_signals": "s", "baseline_route_expectation": "imported",
                  "acceptance_criteria": "MAPE<8%"}})
        run(db, ["scope", "validate", "--quest-id", "b7"])
        c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
        c.execute("INSERT INTO experiment(experiment_id,quest_id,run_contract_ref,is_baseline,status,created_at,updated_at) VALUES('E1','b7','rc',0,'done',?,?)", (AT, AT))
        for i, (rid, val, ts) in enumerate([("R1", 0.9, "2026-06-18T00:00:01Z"), ("R2", 0.5, "2026-06-18T00:00:02Z"),
                                            ("R3", 0.6, "2026-06-18T00:00:03Z")]):  # min is best: 0.5, then 0.6 no-improve
            c.execute("INSERT INTO result(result_id,quest_id,experiment_id,validity,artifact_ref,created_at) VALUES(?,?,?,?,?,?)", (rid, "b7", "E1", "valid", "a", ts))
            c.execute("INSERT INTO measurement(measurement_id,result_id,metric_name,value_num,is_primary,created_at) VALUES(?,?,?,?,?,?)", (f"m{i}", rid, "MAPE", val, 1, ts))
        c.commit(); c.close()
        bs = jdata(run(db, ["bo", "status", "--quest-id", "b7"]))
        check("B7 new: objective_sense=lower_is_better from scope; best=min; streak counts non-improvement",
              bs["objective_sense"] == "lower_is_better" and bs["objective_sense_source"] == "scope_contract.metric_direction"
              and bs["best_primary"] == 0.5 and bs["no_improvement_streak"] == 1, str(bs))

        # ---- quest-local repeated-failure advisory guard ----
        print("C1 attempt_signature matches a dropped opportunity -> advisory warning:")
        db = setup(tmp, "c1")
        opp(db, "c1", "c1:dropped", kind="ablation", status="dropped", sig={"method_key": "layernorm-ablation"})
        opp(db, "c1", "c1:open", kind="ablation", status="open", sig={"method_key": "layernorm-ablation"})
        ck = jdata(run(db, ["opportunity", "check", "--quest-id", "c1"]))
        warns = [w for e in ck["repeated_failure"] for w in e["warnings"]]
        check("C1 new: open opp flagged as possible repeat of the dropped one (shared method_key)",
              ck["no_repeat_risk"] is False and any("dropped opportunity c1:dropped" in w for w in warns), str(ck["repeated_failure"]))

        print("C2 non-matching signature -> no warning:")
        db = setup(tmp, "c2")
        opp(db, "c2", "c2:dropped", status="dropped", sig={"method_key": "layernorm-ablation"})
        opp(db, "c2", "c2:open", status="open", sig={"method_key": "completely-different-route"})
        ck = jdata(run(db, ["opportunity", "check", "--quest-id", "c2"]))
        check("C2 new: disjoint signatures -> no repeat risk", ck["no_repeat_risk"] is True, str(ck["repeated_failure"]))

        print("C3 opportunity citing a refuted claim -> warning:")
        db = setup(tmp, "c3")
        c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
        c.execute("INSERT INTO claim(claim_id,quest_id,statement,status,kind,created_at,updated_at) "
                  "VALUES('CR','c3','X improves Y','refuted','claim',?,?)", (AT, AT)); c.commit(); c.close()
        opp(db, "c3", "c3:o1", status="open", refs={"claim": ["CR"]})
        ck = jdata(run(db, ["opportunity", "check", "--quest-id", "c3"]))
        warns = [w for e in ck["repeated_failure"] for w in e["warnings"]]
        check("C3 new: opp motivated by a refuted claim is flagged", any("refuted claim CR" in w for w in warns), str(warns))

        print("C4 condition matches negative/boundary evidence -> warning:")
        db = setup(tmp, "c4")
        c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
        c.execute("INSERT INTO claim(claim_id,quest_id,statement,status,kind,created_at,updated_at) VALUES('C1','c4','s','supported','claim',?,?)", (AT, AT))
        c.execute("INSERT INTO claim_evidence(claim_id,source_kind,source_ref,relation,evidence_kind,evidence_proof,created_at) "
                  "VALUES('C1','result','C1-neg','supports','negative',?,?)",
                  (json.dumps({"hypothesis": "helps", "observed": "no change at seqlen>8k", "implication": "bound"}), AT)); c.commit(); c.close()
        opp(db, "c4", "c4:o1", kind="boundary", status="open", sig={"condition": "seqlen>8k"})
        ck = jdata(run(db, ["opportunity", "check", "--quest-id", "c4"]))
        warns = [w for e in ck["repeated_failure"] for w in e["warnings"]]
        check("C4 new: condition matching prior negative evidence is flagged",
              any("negative/boundary evidence" in w and "seqlen>8k" in w for w in warns), str(warns))

        print("C5 lesson finding overlap on method_key -> warning:")
        db = setup(tmp, "c5")
        rec(db, {"record_type": "finding.add", "record_id": "c5:f1", "at": AT, "quest_id": "c5", "scope": "quest",
                 "kind": "lesson", "summary": "the layernorm-ablation route plateaued; do not retry blindly"})
        opp(db, "c5", "c5:o1", status="open", sig={"method_key": "layernorm-ablation"})
        ck = jdata(run(db, ["opportunity", "check", "--quest-id", "c5"]))
        warns = [w for e in ck["repeated_failure"] for w in e["warnings"]]
        check("C5 new: similar failed-path lesson surfaced", any("failed-path lesson exists: c5:f1" in w for w in warns), str(warns))

        print("C6 gate status surfaces repeat warnings, NON-blocking:")
        db = setup(tmp, "c6")
        opp(db, "c6", "c6:dropped", status="dropped", sig={"route": "fuse-A-B"})
        opp(db, "c6", "c6:open", status="open", sig={"route": "fuse-A-B"})
        d = jdata(run(db, ["gate", "status", "--quest-id", "c6"]))
        check("C6 new: discovery.repeated_failure_warnings present; not in blocking_gates; finalize unaffected",
              len(d["discovery"]["repeated_failure_warnings"]) == 1
              and not any("opportunity" in g or "discovery" in g or "repeat" in g for g in d["blocking_gates"])
              and d["finalize_readiness"] in ("pass", "fail"), str(d["blocking_gates"]))

        print("C7 plan render shows a repeated-failure advisory line:")
        ps = run(db, ["plan", "status", "--quest-id", "c6"])
        check("C7 new: plan render Discovery has a Repeated-failure advisory",
              "Repeated-failure advisory" in ps.stdout and "c6:dropped" in ps.stdout, ps.stdout[-400:])

        print("C8 latest idea selection signature match warns (advisory; valid unaffected):")
        db = setup(tmp, "c8")
        opp(db, "c8", "c8:dropped", status="dropped", sig={"method_key": "layernorm-ablation"})
        ref = pathlib.Path(tmp) / "c8_idea.json"
        ref.write_text(json.dumps({"attempt_signature": {"method_key": "layernorm-ablation"}}))
        rec(db, {"record_type": "idea.select", "record_id": "c8:s1", "at": AT, "quest_id": "c8", "select_ref": str(ref)})
        ck = jdata(run(db, ["opportunity", "check", "--quest-id", "c8"]))
        idw = [e for e in ck["repeated_failure"] if e["source"] == "idea_select"]
        check("C8 new: idea-selection signature match surfaces an advisory idea_select warning",
              bool(idw) and any("dropped opportunity c8:dropped" in w for w in idw[0]["warnings"]),
              str(ck["repeated_failure"]))

        print("C9 cross-quest attempts are NOT considered:")
        db = str(pathlib.Path(tmp) / "c9.sqlite"); run(db, ["state", "init"])
        c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
        for qid in ("qx", "qy"):
            c.execute("INSERT INTO quest(quest_id,title,objective_ref,workspace_ref,run_state,rigor_level,baseline_gate,"
                      "created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)", (qid, "t", "o", "w", "running", "standard", "pending", AT, AT))
        c.commit(); c.close()
        opp(db, "qx", "qx:dropped", status="dropped", sig={"method_key": "shared-key"})
        opp(db, "qy", "qy:open", status="open", sig={"method_key": "shared-key"})
        ck = jdata(run(db, ["opportunity", "check", "--quest-id", "qy"]))
        check("C9 new: qy's open opp does NOT match qx's dropped opp (quest-local only)",
              ck["no_repeat_risk"] is True, str(ck["repeated_failure"]))

    print("\n%d passed, %d failed" % (len(PASSED), len(FAILED)))
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
