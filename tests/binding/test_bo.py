#!/usr/bin/env python3
"""regression suite — DeepScientist-inspired idea-level BO: LLM-reviewer surrogate + UCB-like acquisition.

The `bo` group picks which candidate research move to try next: gather quest-local candidates
(`bo candidates`), score each into a `bo_review` valuation vector via a configurable independent LLM
Reviewer role (default backend=codex, effort=max), then select via a deterministic UCB-like acquisition
(`bo select`) recorded as a `bo_decision`. It is an LLM-reviewer surrogate + UCB-like acquisition, NOT full
statistical Bayesian optimization. Everything is QUEST-LOCAL and ADVISORY — no BO record enters
blocking_gates / finalize_readiness, none alters idea_select.valid, and there is no cross-quest memory.

Run:  python3 tests/binding/test_bo.py   (exits non-zero on any failure)
"""
import json, os, subprocess, sqlite3, sys, tempfile, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
H = str(ROOT / "execplan" / "harness" / "bin" / "deepresearch")
AT = "2026-06-24T00:00:00Z"
PASSED, FAILED = [], []


def run(db, args, extra_env=None):
    return subprocess.run([H, "--db", db, *args], capture_output=True, text=True,
                          env={**os.environ, **(extra_env or {})})


def rec(db, payload):
    return run(db, ["record", "apply", "--json", json.dumps(payload)])


def jdata(r):
    return json.loads(r.stdout)["data"]


def jwarn(r):
    return json.loads(r.stdout).get("warnings", [])


def check(label, cond, detail=""):
    (PASSED if cond else FAILED).append(label)
    print(("  PASS " if cond else "  FAIL ") + label + (("  -- " + detail) if detail and not cond else ""))


def setup(tmp, qid, rigor="standard"):
    db = str(pathlib.Path(tmp) / ("bo_%s.sqlite" % qid))
    run(db, ["state", "init"])
    c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
    c.execute("INSERT INTO quest(quest_id,title,objective_ref,workspace_ref,run_state,rigor_level,baseline_gate,"
              "created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)", (qid, "t", "o", "w", "running", rigor, "pending", AT, AT))
    c.execute("INSERT INTO artifact(artifact_id,quest_id,kind,ref,created_at) VALUES(?,?,?,?,?)",
              (qid + ":rc", qid, "research-contract", "c", AT))
    c.commit(); c.close()
    return db


def opp(db, qid, oid, kind="ablation", status="open", refs=None, sig=None, rationale="grounded next move"):
    p = {"record_type": "opportunity.record", "record_id": oid, "at": AT, "quest_id": qid, "kind": kind,
         "rationale": rationale, "status": status, "proposed_by": "orchestrator"}
    if refs is not None:
        p["motivating_refs"] = refs
    if sig is not None:
        p["attempt_signature"] = sig
    return rec(db, p)


def val(**kw):
    """A complete valuation vector with overridable dims (defaults mid-range)."""
    v = {"utility": 50, "quality": 50, "novelty": 50, "exploration_value": 50, "uncertainty": 50,
         "feasibility": 50, "cost": 20, "risk": 20, "expected_metric_direction": "unknown", "expected_effect": 50}
    v.update(kw)
    return v


def review_json(tmp, name, items):
    p = pathlib.Path(tmp) / name; p.write_text(json.dumps(items)); return str(p)


def main():
    with tempfile.TemporaryDirectory() as tmp:

        # B1: bo candidates gathers quest-local open opportunities
        print("B1 bo candidates gathers quest-local opportunities:")
        db = setup(tmp, "b1")
        opp(db, "b1", "b1:o1", kind="new_idea")
        opp(db, "b1", "b1:o2", kind="ablation")
        opp(db, "b1", "b1:o3", kind="boundary", status="dropped")  # not open -> excluded
        cd = jdata(run(db, ["bo", "candidates", "--quest-id", "b1"]))
        refs = {c["candidate_ref"] for c in cd["candidates"]}
        check("B1: bo candidates lists the 2 OPEN opportunities (dropped excluded), has_idea_level_candidates",
              cd["count"] == 2 and refs == {"b1:o1", "b1:o2"} and cd["has_idea_level_candidates"] is True,
              "count=%s refs=%s" % (cd["count"], refs))

        # B2: the DURABLE product default is always Codex / max (invariant), regardless of any machine-local
        # override; acquisition method ucb_like_v1; required=false. We assert product_default_* (not the
        # effective backend, which a local override file / env may legitimately change on a given machine).
        print("B2 product-default reviewer config invariant (codex / max):")
        db = setup(tmp, "b2"); opp(db, "b2", "b2:o1")
        rv = jdata(run(db, ["bo", "review", "--quest-id", "b2", "--at", AT]))
        st = jdata(run(db, ["bo", "status", "--quest-id", "b2"]))
        rc = st["reviewer_config"]
        check("B2: product default backend=codex effort=max (durable); method=ucb_like_v1; required_before_select=false",
              rv["reviewer"]["product_default_backend"] == "codex" and rv["reviewer"]["product_default_effort"] == "max"
              and rc["product_default_backend"] == "codex" and rc["product_default_effort"] == "max"
              and rc["acquisition_method"] == "ucb_like_v1" and rc["required_before_select"] is False,
              "reviewer=%s rc=%s" % (rv["reviewer"], rc))

        # B2b: an env override changes the EFFECTIVE backend + backend_source, but NOT the product default
        # (portable: uses env, independent of any machine-local override file).
        print("B2b env override changes effective backend, preserves product default:")
        db = setup(tmp, "b2b"); opp(db, "b2b", "b2b:o1")
        env = {"DEEPRESEARCH_BO_REVIEWER_BACKEND": "claude", "DEEPRESEARCH_BO_REVIEWER_EFFORT": "high"}
        rco = jdata(run(db, ["bo", "status", "--quest-id", "b2b"], env))["reviewer_config"]
        check("B2b: env override => effective claude/high + backend_source=env_override; product default still codex/max",
              rco["backend"] == "claude" and rco["effort"] == "high" and rco["backend_source"] == "env_override"
              and rco["product_default_backend"] == "codex" and rco["product_default_effort"] == "max", str(rco))

        # B3: user can override backend/effort
        print("B3 override backend/effort:")
        db = setup(tmp, "b3"); opp(db, "b3", "b3:o1")
        rv = jdata(run(db, ["bo", "review", "--quest-id", "b3", "--backend", "gemini", "--effort", "low", "--at", AT]))
        check("B3: --backend/--effort override config (backend_source=cli_override); product default unchanged",
              rv["reviewer"]["backend"] == "gemini" and rv["reviewer"]["effort"] == "low"
              and rv["reviewer"]["backend_source"] == "cli_override"
              and rv["reviewer"]["product_default_backend"] == "codex", str(rv["reviewer"]))

        # B4: missing / cross-quest motivating refs are WARNED and never followed
        print("B4 cross-quest / missing motivating refs warned, not followed:")
        db = setup(tmp, "b4")
        c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
        c.execute("INSERT INTO quest(quest_id,title,objective_ref,workspace_ref,run_state,rigor_level,created_at,updated_at)"
                  " VALUES('other','t','o','w','running','standard',?,?)", (AT, AT))
        c.execute("INSERT INTO finding_memory(memory_id,quest_id,scope,kind,summary,created_at,updated_at)"
                  " VALUES('other:f1','other','quest','lesson','x',?,?)", (AT, AT))
        c.commit(); c.close()
        opp(db, "b4", "b4:o1", kind="new_idea", refs={"finding": ["other:f1"], "result": ["b4:missing"]})
        cw = jwarn(run(db, ["bo", "candidates", "--quest-id", "b4"]))
        cdat = jdata(run(db, ["bo", "candidates", "--quest-id", "b4"]))
        cand = cdat["candidates"][0] if cdat["candidates"] else {}
        statuses = {u["status"] for u in cand.get("unresolved_refs", [])}
        check("B4: candidate still listed but cross_quest+missing refs flagged (never followed)",
              cdat["count"] == 1 and statuses == {"cross_quest", "missing"}
              and any("cross_quest" in w and "NOT followed" in w for w in cw), "statuses=%s" % statuses)

        # B5: bo review --from-json creates structured bo_review records (is_stub=0); B6 validation rejects bad valuations
        print("B5 bo review --from-json records structured bo_review:")
        db = setup(tmp, "b5"); opp(db, "b5", "b5:o1", kind="new_idea")
        rj = review_json(tmp, "b5.json", [{"candidate_ref": "b5:o1", "reviewer_backend": "codex",
                                           "valuation": val(utility=80), "rationale": "strong", "risks": ["r1"]}])
        rv = jdata(run(db, ["bo", "review", "--quest-id", "b5", "--from-json", rj, "--at", AT]))
        c = sqlite3.connect(db)
        row = c.execute("SELECT candidate_ref,valuation,is_stub,reviewer_backend FROM bo_review WHERE quest_id='b5'").fetchone()
        c.close()
        v = json.loads(row[1]) if row else {}
        check("B5: real bo_review row written (is_stub=0, full valuation vector, used_stub=false)",
              rv["reviewed"] == 1 and rv["used_stub"] is False and row is not None and row[2] == 0
              and row[3] == "codex" and v.get("utility") == 80 and all(k in v for k in
              ("utility", "quality", "novelty", "exploration_value", "uncertainty", "feasibility", "cost", "risk")),
              "row=%s" % (row,))

        print("B6 valuation validation rejects missing / out-of-range fields:")
        db = setup(tmp, "b6"); opp(db, "b6", "b6:o1")
        bad_missing = val(); del bad_missing["risk"]
        rj1 = review_json(tmp, "b6a.json", [{"candidate_ref": "b6:o1", "valuation": bad_missing}])
        r1 = run(db, ["bo", "review", "--quest-id", "b6", "--from-json", rj1, "--at", AT])
        rj2 = review_json(tmp, "b6b.json", [{"candidate_ref": "b6:o1", "valuation": val(utility=150)}])
        r2 = run(db, ["bo", "review", "--quest-id", "b6", "--from-json", rj2, "--at", "2026-06-24T02:00:00Z"])
        check("B6: missing dim (risk) rejected by schema", jdata(r1)["reviewed"] == 0
              and any("risk" in w or "required" in w for w in jwarn(r1)), str(jwarn(r1))[:120])
        check("B6: out-of-range dim (utility=150) rejected by schema", jdata(r2)["reviewed"] == 0
              and any("100" in w or "maximum" in w for w in jwarn(r2)), str(jwarn(r2))[:120])

        # B7 + B8: bo select creates bo_decision; UCB-like formula is deterministic with an exact expected score
        print("B7/B8 bo select creates bo_decision + deterministic UCB-like score:")
        db = setup(tmp, "b7"); opp(db, "b7", "b7:o1", kind="new_idea")
        # utility80 quality60 feas40 ee50 / expl20 nov20 unc20 / cost20 risk20 ; beta0.5
        # exploitation=0.4*80+0.25*60+0.2*40+0.15*50=62.5 ; exploration=20 ; penalty=0.35*20+0.25*20=12
        # score = 62.5 + 0.5*20 - 12 = 60.5
        rj = review_json(tmp, "b7.json", [{"candidate_ref": "b7:o1", "valuation":
                         val(utility=80, quality=60, feasibility=40, exploration_value=20, novelty=20,
                             uncertainty=20, cost=20, risk=20, expected_effect=50)}])
        run(db, ["bo", "review", "--quest-id", "b7", "--from-json", rj, "--at", AT])
        sel = jdata(run(db, ["bo", "select", "--quest-id", "b7", "--beta", "0.5", "--at", AT]))
        c = sqlite3.connect(db)
        drow = c.execute("SELECT selected_candidate_ref,acquisition_method FROM bo_decision WHERE quest_id='b7'").fetchone()
        c.close()
        top = sel["acquisition_scores"][0]
        check("B7: bo_decision recorded with selected candidate + method", drow is not None
              and drow[0] == "b7:o1" and drow[1] == "ucb_like_v1" and sel["selected_candidate_ref"] == "b7:o1",
              "drow=%s" % (drow,))
        check("B8: UCB-like score deterministic and exact (60.5)", top["score"] == 60.5
              and top["exploitation"] == 62.5 and top["exploration"] == 20.0 and top["penalty"] == 12.0,
              "top=%s" % top)

        # B9: high-exploration candidate beats high-utility candidate when beta is high (and loses when low)
        print("B9 exploration vs utility flips with beta:")
        db = setup(tmp, "b9"); opp(db, "b9", "b9:U", kind="next_experiment"); opp(db, "b9", "b9:E", kind="new_idea")
        rj = review_json(tmp, "b9.json", [
            {"candidate_ref": "b9:U", "valuation": val(utility=90, novelty=10, exploration_value=10, uncertainty=10)},
            {"candidate_ref": "b9:E", "valuation": val(utility=30, novelty=90, exploration_value=90, uncertainty=90)}])
        run(db, ["bo", "review", "--quest-id", "b9", "--from-json", rj, "--at", AT])
        lo = jdata(run(db, ["bo", "select", "--quest-id", "b9", "--beta", "0.1"]))["selected_candidate_ref"]
        hi = jdata(run(db, ["bo", "select", "--quest-id", "b9", "--beta", "0.9"]))["selected_candidate_ref"]
        check("B9: low beta picks high-utility, high beta picks high-exploration", lo == "b9:U" and hi == "b9:E",
              "lo=%s hi=%s" % (lo, hi))

        # B10: high risk/cost candidate is penalized (lower score than an otherwise-equal low risk/cost one)
        print("B10 high risk/cost penalized:")
        db = setup(tmp, "b10"); opp(db, "b10", "b10:lo"); opp(db, "b10", "b10:hi")
        rj = review_json(tmp, "b10.json", [
            {"candidate_ref": "b10:lo", "valuation": val(cost=10, risk=10)},
            {"candidate_ref": "b10:hi", "valuation": val(cost=90, risk=90)}])
        run(db, ["bo", "review", "--quest-id", "b10", "--from-json", rj, "--at", AT])
        scs = {s["candidate_ref"]: s for s in jdata(run(db, ["bo", "select", "--quest-id", "b10", "--beta", "0.5"]))["acquisition_scores"]}
        check("B10: higher risk/cost => higher penalty => lower score",
              scs["b10:hi"]["penalty"] > scs["b10:lo"]["penalty"] and scs["b10:hi"]["score"] < scs["b10:lo"]["score"]
              and jdata(run(db, ["bo", "select", "--quest-id", "b10", "--beta", "0.5"]))["selected_candidate_ref"] == "b10:lo",
              "lo=%s hi=%s" % (scs["b10:lo"]["score"], scs["b10:hi"]["score"]))

        # B11: repeated-failure warnings penalize/annotate but never block
        print("B11 repeated-failure penalizes/annotates but does not block:")
        db = setup(tmp, "b11")
        opp(db, "b11", "b11:drop", kind="ablation", status="dropped", sig={"method_key": "mk-fail"})
        opp(db, "b11", "b11:open", kind="ablation", status="open", sig={"method_key": "mk-fail"})
        cdat = jdata(run(db, ["bo", "candidates", "--quest-id", "b11"]))
        opencand = [c for c in cdat["candidates"] if c["candidate_ref"] == "b11:open"][0]
        rj = review_json(tmp, "b11.json", [{"candidate_ref": "b11:open", "valuation": val()}])
        rev = run(db, ["bo", "review", "--quest-id", "b11", "--from-json", rj, "--at", AT])
        selr = run(db, ["bo", "select", "--quest-id", "b11", "--beta", "0.5", "--at", AT])
        sc = jdata(selr)["acquisition_scores"][0]
        check("B11: repeat warning annotated on candidate + context_penalty applied, commands still succeed (no block)",
              bool(opencand["repeat_failure_warnings"]) and sc["context_penalty"] >= 15.0
              and rev.returncode == 0 and selr.returncode == 0, "warnings=%s ctx=%s" %
              (opencand["repeat_failure_warnings"], sc.get("context_penalty")))

        # B12: bo suggest uses reviewed candidates before falling back to the search_space midpoint
        print("B12 bo suggest prefers reviewed candidates over midpoint fallback:")
        db = setup(tmp, "b12")
        rec(db, {"record_type": "search_space.define", "record_id": "x", "at": AT, "quest_id": "b12",
                 "space_id": "s1", "dim_name": "lr", "dim_kind": "real", "low": 0.0, "high": 1.0})
        sug_fb = jdata(run(db, ["bo", "suggest", "--quest-id", "b12"]))
        opp(db, "b12", "b12:o1", kind="new_idea")
        sug_idea = jdata(run(db, ["bo", "suggest", "--quest-id", "b12", "--at", AT]))
        check("B12: search_space-only => labelled fallback; adding a candidate => idea-level-bo mode",
              sug_fb["mode"] == "search-space-fallback" and sug_fb.get("stub") is True
              and sug_idea["mode"] == "idea-level-bo" and sug_idea["selected_candidate_ref"] == "b12:o1",
              "fb=%s idea=%s" % (sug_fb["mode"], sug_idea["mode"]))

        # B13: bo status reports reviewer/acquisition state honestly (stub vs real, counts, latest decision)
        print("B13 bo status honest reviewer/acquisition state:")
        db = setup(tmp, "b13"); opp(db, "b13", "b13:o1")
        run(db, ["bo", "review", "--quest-id", "b13", "--at", AT])  # offline stub
        run(db, ["bo", "select", "--quest-id", "b13", "--beta", "0.5", "--at", AT])
        st = jdata(run(db, ["bo", "status", "--quest-id", "b13"]))
        check("B13: status shows stub honesty (used_real_reviewer false, n_stub>0), latest decision, honest method",
              st["n_candidates"] == 1 and st["n_reviewed_candidates"] == 1 and st["n_stub_reviews"] == 1
              and st["used_real_reviewer"] is False and st["latest_decision"] is not None
              and "NOT full statistical" in st["method"], str({k: st[k] for k in
              ("n_candidates", "n_stub_reviews", "used_real_reviewer")}))

        # B14 + B15: no BO record enters blocking_gates; bo_decision does not affect finalize_readiness
        print("B14/B15 BO advisory: not in blocking_gates, no effect on finalize_readiness:")
        db = setup(tmp, "b14")
        gs0 = jdata(run(db, ["gate", "status", "--quest-id", "b14"]))
        fr0 = gs0["finalize_readiness"]
        opp(db, "b14", "b14:o1", kind="new_idea")
        run(db, ["bo", "review", "--quest-id", "b14", "--at", AT])
        run(db, ["bo", "select", "--quest-id", "b14", "--beta", "0.5", "--at", AT])
        gs1 = jdata(run(db, ["gate", "status", "--quest-id", "b14"]))
        bg = " ".join(gs1["blocking_gates"])
        check("B14: no bo/review/decision key in blocking_gates", "bo_" not in bg and "bo " not in bg
              and "review_id" not in bg, "blocking_gates=%s" % gs1["blocking_gates"])
        check("B15: recording bo_review + bo_decision leaves finalize_readiness unchanged",
              gs1["finalize_readiness"] == fr0, "fr0=%s fr1=%s" % (fr0, gs1["finalize_readiness"]))

        # B16: no cross-quest memory — bo candidates for a quest never includes another quest's candidates
        print("B16 no cross-quest memory in candidate gathering:")
        db = setup(tmp, "b16")
        c = sqlite3.connect(db); c.execute("PRAGMA foreign_keys=OFF")
        c.execute("INSERT INTO quest(quest_id,title,objective_ref,workspace_ref,run_state,rigor_level,created_at,updated_at)"
                  " VALUES('sib','t','o','w','running','standard',?,?)", (AT, AT))
        c.commit(); c.close()
        opp(db, "sib", "sib:o1", kind="new_idea")   # sibling quest's opportunity
        opp(db, "b16", "b16:o1", kind="ablation")   # this quest's opportunity
        cdat = jdata(run(db, ["bo", "candidates", "--quest-id", "b16"]))
        refs = {c["candidate_ref"] for c in cdat["candidates"]}
        check("B16: candidates are strictly quest-local (sibling's opportunity never appears)",
              refs == {"b16:o1"}, "refs=%s" % refs)

        # B17: the BO-reviewer role owns bo_review.record (skill-authority), a non-owner role is denied
        print("B17 BO-reviewer role owns bo_review.record (skill authority):")
        db = setup(tmp, "b17"); opp(db, "b17", "b17:o1")
        rj = review_json(tmp, "b17.json", [{"candidate_ref": "b17:o1", "valuation": val()}])
        ok_role = jdata(run(db, ["--via", "skill:deepresearch-llm-reviewer:BO-reviewer",
                                 "bo", "review", "--quest-id", "b17", "--from-json", rj, "--at", AT]))
        bad = run(db, ["--via", "skill:deepresearch-llm-reviewer:experimenter",
                       "bo", "review", "--quest-id", "b17", "--from-json", rj, "--at", "2026-06-24T03:00:00Z"])
        bad_warns = " ".join(jwarn(bad))
        check("B17: BO-reviewer may write bo_review.record; experimenter is denied by skill authority",
              ok_role["reviewed"] == 1 and jdata(bad)["reviewed"] == 0 and "skill authority" in bad_warns,
              "ok=%s bad_warns=%s" % (ok_role["reviewed"], bad_warns[:120]))

    print("\n%d passed, %d failed" % (len(PASSED), len(FAILED)))
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
