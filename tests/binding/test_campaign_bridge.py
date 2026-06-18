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


def proof_for(ek, cid):
    """Minimal VALID kind-specific proof (Phase 4) for positive fixtures; ablation's parent_result resolves
    to the helper-inserted '<cid>-parent' result."""
    return {
        "main_result": {"metric": "acc", "direction": "higher"},
        "baseline_comparison": {"metric": "acc", "direction": "higher"},
        "ablation": {"changed_factor": "layernorm", "controls": "all else fixed", "delta": "+1.2 acc"},
        "robustness": {"varied_condition": "seqlen=4k", "original_condition": "seqlen=1k", "criterion": "<2% drop"},
        "negative": {"hypothesis": "X helps", "observed": "no change", "implication": "claim bound: X not needed"},
        "boundary": {"hypothesis": "holds <8k", "observed": "breaks >8k", "implication": "valid below 8k"},
        "significance": {"method": "paired t-test (n=5)", "effect": "p=0.01, d=0.8"},
        "efficiency": {"resource": "gpu_hours", "metric": "0.5x", "baseline": "FA2"},
        "error_analysis": {"error_category": "long-seq", "subset": "seqlen>8k", "implication": "add chunking"},
    }.get(ek, {})


def link(db, cid, kind, evkinds, provenance_ok=1, proof=True):
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    qid = (c.execute("SELECT quest_id FROM claim WHERE claim_id=?", (cid,)).fetchone() or [None])[0]
    for i, ek in enumerate(evkinds):
        ref = f"{cid}-{ek}-{i}"
        p = proof_for(ek, cid)
        if ek == "ablation":
            p = {**p, "parent_result": ref}  # resolves to this row's own (claim-mapped) result
        ep = json.dumps(p) if proof else None
        c.execute("INSERT INTO claim_evidence(claim_id,source_kind,source_ref,relation,evidence_kind,"
                  "evidence_proof,created_at) VALUES(?,?,?,?,?,?,?)", (cid, kind, ref, "supports", ek, ep, AT))
        if kind == "result":  # back the evidence with a result; provenance_ok controls whether coverage counts it
            c.execute("INSERT INTO result(result_id,quest_id,experiment_id,validity,artifact_ref,"
                      "provenance_route,provenance_ok,created_at) VALUES(?,?,?,?,?,?,?,?)",
                      (ref, qid, "E1", "valid", "a", "executed", provenance_ok, AT))
    c.commit(); c.close()


def link_raw(db, cid, source_kind, ek, proof, provenance_ok=1):
    """Insert ONE supporting evidence row with a CUSTOM proof (dict -> JSON; str -> stored verbatim for the
    malformed case; None -> NULL). Backs a result row when source_kind='result'."""
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    qid = (c.execute("SELECT quest_id FROM claim WHERE claim_id=?", (cid,)).fetchone() or [None])[0]
    ref = f"{cid}-{ek}-x"
    ep = proof if (proof is None or isinstance(proof, str)) else json.dumps(proof)
    c.execute("INSERT INTO claim_evidence(claim_id,source_kind,source_ref,relation,evidence_kind,evidence_proof,created_at) "
              "VALUES(?,?,?,?,?,?,?)", (cid, source_kind, ref, "supports", ek, ep, AT))
    if source_kind == "result":
        c.execute("INSERT INTO result(result_id,quest_id,experiment_id,validity,artifact_ref,provenance_route,"
                  "provenance_ok,created_at) VALUES(?,?,?,?,?,?,?,?)",
                  (ref, qid, "E1", "valid", "a", "executed", provenance_ok, AT))
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


def record_baseline(db, qid, verdict="verified_match", waiver=None, route=None, evidence_ref=None, validate=True):
    route = route or ("waived" if verdict == "waived" else "imported")
    p = {"record_type": "baseline.contract", "record_id": qid + ":bc1", "at": AT, "quest_id": qid,
         "baseline_id": "b", "baseline_name": "BL", "comparison_policy": "higher-is-better; within 1%",
         "primary_metric_id": "acc", "dataset": "D", "split": "test", "eval_protocol": "eval.py",
         "verification_verdict": verdict, "baseline_route": route}
    if evidence_ref is not None:
        p["evidence_ref"] = evidence_ref
    elif route in ("imported", "trusted"):
        p["evidence_ref"] = "Smith2023, Table 1 (imported baseline)"
    if waiver:
        p["waiver_reason"] = waiver
    r = rec(db, p)
    if validate:
        run(db, ["baseline", "validate", "--quest-id", qid])  # sets the validator-owned valid flag
    return r


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


def cov_valid(db, qid, extra_env=None):
    return run(db, ["campaign", "validate", "--quest-id", qid], extra_env)


def jdata(r):
    return json.loads(r.stdout)["data"]


def add_experiment(db, qid, eid="E1"):
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    c.execute("INSERT INTO experiment(experiment_id,quest_id,run_contract_ref,is_baseline,status,created_at,updated_at) "
              "VALUES(?,?,?,?,?,?,?)", (eid, qid, "rc", 0, "done", AT, AT))
    c.commit(); c.close()


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

        # J10: result-backed evidence WITHOUT validated provenance is not counted -> coverage fails, visibly
        print("J10 provenance-less result evidence is not counted (clear reason):")
        db = setup(tmp, "j10"); add_claim(db, "j10", "C1")
        link(db, "C1", "result", ["main_result", "baseline_comparison", "ablation"], provenance_ok=0)
        record_baseline(db, "j10", "verified_match"); set_baseline_gate(db, "j10", "passed")
        record_bridge(db, "j10", wj(tmp, "j10.json", good_bridge()))
        r = cov_valid(db, "j10")
        check("J10 new: provenance-less result evidence not counted (campaign fails)",
              r.returncode != 0 and "provenance" in (r.stdout + r.stderr), r.stdout[:260])

        # J11: `result validate` computes provenance_ok from the declared route + manifest (the validator owns it)
        print("J11 result validate computes provenance_ok per route:")
        db = setup(tmp, "j11"); add_experiment(db, "j11")
        rg = rec(db, {"record_type": "result.record", "record_id": "j11:R_ok", "at": AT, "quest_id": "j11",
                      "experiment_id": "E1", "artifact_ref": "a", "provenance_route": "executed",
                      "provenance": {"command": "python train.py --cfg c.yaml", "code_revision": "abc123",
                                     "metric_source": "runs/m.json", "run_status": "completed", "seed": 7}})
        ok = run(db, ["result", "validate", "--result-id", "j11:R_ok"])
        check("J11 new: executed result w/ full manifest -> provenance_ok=1",
              ok.returncode == 0 and jdata(ok)["provenance_ok"] is True, ok.stdout[:240])
        rec(db, {"record_type": "result.record", "record_id": "j11:R_bad", "at": AT, "quest_id": "j11",
                 "experiment_id": "E1", "artifact_ref": "a", "provenance_route": "executed", "provenance": {"seed": 7}})
        bad = run(db, ["result", "validate", "--result-id", "j11:R_bad"])
        check("J11 new: executed result missing manifest -> provenance_ok=0 + reasons",
              jdata(bad)["provenance_ok"] is False and bool(jdata(bad)["provenance_reasons"]), bad.stdout[:240])
        # author cannot self-certify: even if payload tried provenance_ok, force zeroes it (schema also blocks it)
        rec(db, {"record_type": "result.record", "record_id": "j11:R_imp", "at": AT, "quest_id": "j11",
                 "experiment_id": "E1", "artifact_ref": "a", "provenance_route": "imported",
                 "provenance": {"source": "Vaswani 2017, Table 2 (imported baseline)"}})
        imp = run(db, ["result", "validate", "--result-id", "j11:R_imp"])
        check("J11 new: imported route w/ source -> provenance_ok=1 (non-execution route explicit)",
              jdata(imp)["provenance_ok"] is True, imp.stdout[:240])
        rec(db, {"record_type": "result.record", "record_id": "j11:R_wv", "at": AT, "quest_id": "j11",
                 "experiment_id": "E1", "artifact_ref": "a", "provenance_route": "waived", "provenance": {}})
        wv = run(db, ["result", "validate", "--result-id", "j11:R_wv"])
        check("J11 new: waived route w/o waiver_reason -> provenance_ok=0",
              jdata(wv)["provenance_ok"] is False, wv.stdout[:240])

        # J12: env waiver lets coverage count provenance-less evidence (explicit, visible operator override)
        print("J12 env waiver counts provenance-less evidence:")
        db = setup(tmp, "j12"); add_claim(db, "j12", "C1")
        link(db, "C1", "result", ["main_result", "baseline_comparison", "ablation"], provenance_ok=0)
        record_baseline(db, "j12", "verified_match"); set_baseline_gate(db, "j12", "passed")
        record_bridge(db, "j12", wj(tmp, "j12.json", good_bridge()))
        rno = cov_valid(db, "j12")
        rwv = cov_valid(db, "j12", {"DEEPRESEARCH_PROVENANCE_GATE": "0"})
        check("J12 new: blocked without waiver, counted with DEEPRESEARCH_PROVENANCE_GATE=0",
              rno.returncode != 0 and rwv.returncode == 0, "no=%s waived=%s" % (rno.returncode, rwv.returncode))

        # ---- Phase 2: baseline validator (validator-owned; author cannot self-certify) ----
        # B1: bare author-asserted verified_match (no route/eval evidence) -> validate fails + gate blocks
        print("B1 author-asserted verified_match without validation evidence:")
        db = setup(tmp, "b1")
        rec(db, {"record_type": "baseline.contract", "record_id": "b1:bc", "at": AT, "quest_id": "b1",
                 "baseline_id": "b", "verification_verdict": "verified_match"})
        bv = run(db, ["baseline", "validate", "--quest-id", "b1"])
        rg = set_baseline_gate(db, "b1", "passed")
        check("B1 new: bare verified_match fails baseline validate + gate blocks (valid=0)",
              bv.returncode != 0 and rg.returncode != 0, "validate=%s gate=%s" % (bv.returncode, rg.returncode))

        # B2: reproduced baseline backed by a provenance-valid result -> valid -> gate passes
        print("B2 reproduced baseline backed by a provenance-valid result:")
        db = setup(tmp, "b2"); add_experiment(db, "b2")
        c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
        c.execute("INSERT INTO result(result_id,quest_id,experiment_id,validity,artifact_ref,provenance_route,"
                  "provenance_ok,created_at) VALUES('b2:R','b2','E1','valid','a','executed',1,?)", (AT,))
        c.commit(); c.close()
        rec(db, {"record_type": "baseline.contract", "record_id": "b2:bc", "at": AT, "quest_id": "b2",
                 "baseline_id": "b", "baseline_name": "BL", "comparison_policy": "higher-is-better",
                 "primary_metric_id": "acc", "dataset": "D", "split": "test", "eval_protocol": "eval.py",
                 "verification_verdict": "verified_match", "baseline_route": "reproduced", "evidence_ref": "b2:R"})
        bv = run(db, ["baseline", "validate", "--quest-id", "b2"])
        rg = set_baseline_gate(db, "b2", "passed")
        check("B2 new: reproduced + provenance-backed result -> valid + gate passes",
              bv.returncode == 0 and jdata(bv)["valid"] is True and rg.returncode == 0,
              "validate=%s gate=%s %s" % (bv.returncode, rg.returncode, bv.stdout[:160]))

        # B2b: reproduced baseline whose result LACKS validated provenance -> validate fails (provenance reason)
        print("B2b reproduced baseline with a provenance-less result:")
        db = setup(tmp, "b2b"); add_experiment(db, "b2b")
        c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
        c.execute("INSERT INTO result(result_id,quest_id,experiment_id,validity,artifact_ref,provenance_route,"
                  "provenance_ok,created_at) VALUES('b2b:R','b2b','E1','valid','a','executed',0,?)", (AT,))
        c.commit(); c.close()
        rec(db, {"record_type": "baseline.contract", "record_id": "b2b:bc", "at": AT, "quest_id": "b2b",
                 "baseline_id": "b", "comparison_policy": "x", "primary_metric_id": "acc", "dataset": "D",
                 "split": "test", "eval_protocol": "e", "verification_verdict": "verified_match",
                 "baseline_route": "reproduced", "evidence_ref": "b2b:R"})
        bv = run(db, ["baseline", "validate", "--quest-id", "b2b"])
        check("B2b new: reproduced w/ provenance-less result -> validate fails (provenance reason)",
              bv.returncode != 0 and "provenance" in (bv.stdout + bv.stderr), bv.stdout[:220])

        # B3: imported baseline with a citation -> valid -> gate passes
        print("B3 imported baseline with citation:")
        db = setup(tmp, "b3")
        record_baseline(db, "b3", "trusted_with_caveats", route="imported")  # helper adds citation + validates
        rg = set_baseline_gate(db, "b3", "passed")
        check("B3 new: imported + citation -> gate passes", rg.returncode == 0, rg.stdout[:160])

        # B4: imported baseline WITHOUT a citation -> validate fails
        print("B4 imported baseline without citation:")
        db = setup(tmp, "b4")
        record_baseline(db, "b4", "trusted_with_caveats", route="imported", evidence_ref="", validate=False)
        bv = run(db, ["baseline", "validate", "--quest-id", "b4"])
        check("B4 new: imported w/o citation -> validate fails", bv.returncode != 0, bv.stdout[:200])

        # B5: waived baseline WITHOUT reason fails; WITH reason the waive gate passes (standard rigor)
        print("B5 waived baseline reason handling:")
        db = setup(tmp, "b5")
        record_baseline(db, "b5", "waived", route="waived", validate=False)  # no waiver_reason
        bv = run(db, ["baseline", "validate", "--quest-id", "b5"])
        rgno = set_baseline_gate(db, "b5", "waived")
        check("B5 new: waived w/o reason fails validate + waive gate blocks",
              bv.returncode != 0 and rgno.returncode != 0, "validate=%s gate=%s" % (bv.returncode, rgno.returncode))
        db = setup(tmp, "b5b")
        record_baseline(db, "b5b", "waived", route="waived", waiver="no public baseline; greenfield task")
        rgok = set_baseline_gate(db, "b5b", "waived")
        check("B5b new: waived w/ reason -> waive gate passes (standard rigor)", rgok.returncode == 0, rgok.stdout[:160])

        # B6: gate status surfaces the baseline validation failure reason
        print("B6 gate status surfaces baseline validation failure:")
        db = setup(tmp, "b6")
        rec(db, {"record_type": "baseline.contract", "record_id": "b6:bc", "at": AT, "quest_id": "b6",
                 "baseline_id": "b", "verification_verdict": "verified_match"})
        run(db, ["baseline", "validate", "--quest-id", "b6"])  # valid=0
        g = jdata(run(db, ["gate", "status", "--quest-id", "b6"]))["gates"]["baseline_contract"]
        check("B6 new: gate status baseline_contract=fail with a reason",
              g["status"] == "fail" and "baseline" in (g["reason"] or "").lower(), str(g))

        # B7: scoping rigor -> baseline gate advisory (not blocked even when unvalidated)
        print("B7 scoping rigor: baseline gate advisory:")
        db = setup(tmp, "b7", rigor="scoping")
        rec(db, {"record_type": "baseline.contract", "record_id": "b7:bc", "at": AT, "quest_id": "b7",
                 "baseline_id": "b", "verification_verdict": "verified_match"})  # unvalidated
        rg = set_baseline_gate(db, "b7", "passed")
        check("B7 new: scoping baseline gate advisory (unvalidated 'passed' allowed)", rg.returncode == 0, rg.stdout[:160])

        # ---- Phase 4: evidence-kind proof (a label is not proof) ----
        def cov_setup(qid, rigor="standard"):
            db = setup(tmp, qid, rigor); add_claim(db, qid, "C1")
            return db

        def finish_cov(db, qid):
            record_baseline(db, qid, "verified_match"); set_baseline_gate(db, qid, "passed")
            record_bridge(db, qid, wj(tmp, qid + ".json", good_bridge()))
            return cov_valid(db, qid)

        # E1: ablation labelled but UNPROVEN -> not counted, with the field-specific reason
        print("E1 ablation without proof is not counted:")
        db = cov_setup("e1")
        link(db, "C1", "result", ["main_result", "baseline_comparison"], proof=True)
        link(db, "C1", "result", ["ablation"], proof=False)
        r = finish_cov(db, "e1")
        check("E1 new: ablation w/o proof not counted (missing changed_factor)",
              r.returncode != 0 and "ablation evidence not counted" in r.stdout and "changed_factor" in r.stdout,
              r.stdout[:260])

        # E2: significance labelled but UNPROVEN -> not counted (missing method)
        print("E2 significance without uncertainty proof is not counted:")
        db = cov_setup("e2", rigor="publication")
        link(db, "C1", "result", ["main_result", "baseline_comparison", "ablation"], proof=True)
        link(db, "C1", "result", ["significance"], proof=False)
        r = finish_cov(db, "e2")
        check("E2 new: significance w/o proof not counted (missing method)",
              r.returncode != 0 and "significance evidence not counted" in r.stdout and "missing method" in r.stdout,
              r.stdout[:260])

        # E3: malformed proof JSON -> not counted with a clear reason
        print("E3 malformed proof not counted:")
        db = cov_setup("e3")
        link(db, "C1", "result", ["main_result", "ablation"], proof=True)
        link_raw(db, "C1", "result", "baseline_comparison", "{not valid json")
        r = finish_cov(db, "e3")
        check("E3 new: malformed proof not counted (malformed proof)",
              r.returncode != 0 and "malformed proof" in r.stdout, r.stdout[:260])

        # E4: result-backed evidence STILL requires provenance_ok=1 (Phase 1 preserved under Phase 4)
        print("E4 proven-kind but provenance-less result still not counted:")
        db = cov_setup("e4")
        link(db, "C1", "result", ["main_result", "baseline_comparison"], proof=True)
        link(db, "C1", "result", ["ablation"], proof=True, provenance_ok=0)  # valid proof, no provenance
        r = finish_cov(db, "e4")
        check("E4 new: valid proof + provenance-less result not counted (provenance)",
              r.returncode != 0 and "provenance" in r.stdout, r.stdout[:260])

        # E5: reference/external evidence needs an explicit source; without it, not counted
        print("E5 reference evidence requires explicit source:")
        db = cov_setup("e5")
        link(db, "C1", "result", ["main_result", "ablation"], proof=True)
        link_raw(db, "C1", "reference", "baseline_comparison", {"metric": "acc", "direction": "higher"})  # no source
        r = finish_cov(db, "e5")
        check("E5 new: reference baseline_comparison w/o source not counted",
              r.returncode != 0 and "explicit source" in r.stdout, r.stdout[:260])
        # E5b: same reference WITH a source counts -> coverage passes
        print("E5b reference evidence with source counts:")
        db = cov_setup("e5b")
        link(db, "C1", "result", ["main_result", "ablation"], proof=True)
        link_raw(db, "C1", "reference", "baseline_comparison",
                 {"metric": "acc", "direction": "higher", "source": "Smith2023, Table 1"})
        r = finish_cov(db, "e5b")
        check("E5b new: reference baseline_comparison WITH source -> coverage passes", r.returncode == 0, r.stdout[:260])

        # E6: ablation parent_result that does not resolve -> not counted (unresolved reference)
        print("E6 ablation parent_result unresolved:")
        db = cov_setup("e6")
        link(db, "C1", "result", ["main_result", "baseline_comparison"], proof=True)
        link_raw(db, "C1", "result", "ablation",
                 {"changed_factor": "ln", "controls": "fixed", "delta": "+1", "parent_result": "NOPE"})
        r = finish_cov(db, "e6")
        check("E6 new: ablation w/ unresolvable parent_result not counted",
              r.returncode != 0 and "parent_result unresolved" in r.stdout, r.stdout[:260])

        # E7: a fully-proven set is counted -> coverage passes (the positive path)
        print("E7 fully-proven evidence is counted:")
        db = cov_setup("e7")
        link(db, "C1", "result", ["main_result", "baseline_comparison", "ablation"], proof=True)
        r = finish_cov(db, "e7")
        check("E7 new: full valid proof -> coverage passes", r.returncode == 0, r.stdout[:260])

        # E8: env waiver counts proof-less evidence + is visible (gate status active_waivers)
        print("E8 evidence-proof waiver counts + is visible:")
        db = cov_setup("e8")
        link(db, "C1", "result", ["main_result", "baseline_comparison", "ablation"], proof=False)
        record_baseline(db, "e8", "verified_match"); set_baseline_gate(db, "e8", "passed")
        record_bridge(db, "e8", wj(tmp, "e8.json", good_bridge()))
        rno = cov_valid(db, "e8")
        rwv = cov_valid(db, "e8", {"DEEPRESEARCH_EVIDENCE_PROOF_GATE": "0"})
        g = jdata(run(db, ["gate", "status", "--quest-id", "e8"]))["gates"]["campaign_coverage"]
        check("E8 new: proof-less blocked; DEEPRESEARCH_EVIDENCE_PROOF_GATE=0 counts; gate status shows reason",
              rno.returncode != 0 and rwv.returncode == 0 and "not counted" in (g["reason"] or ""),
              "no=%s waived=%s reason=%s" % (rno.returncode, rwv.returncode, g["reason"]))

        print("Regime: scoping rigor advisory:")
        db = setup(tmp, "sc", rigor="scoping"); add_round_write(db, "sc")
        r = open_write_handoff(db, "sc")
        check("scoping: analysis-bridge gate advisory (write not blocked)", r.returncode == 0, r.stdout[:160])

    print("\n%d passed, %d failed" % (len(PASSED), len(FAILED)))
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
