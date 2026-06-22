#!/usr/bin/env python3
"""Run all research-quality binding-gate regression suites from one entrypoint.

Usage:  python3 tests/binding/run_all.py     (exits non-zero if any suite fails)
"""
import subprocess, sys, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
SUITES = [
    ("paper spine / manuscript coverage", "test_paper_spine_coverage.py"),
    ("review verdict gate", "test_review_verdict.py"),
    ("idea selection gate", "test_idea_selection.py"),
    ("baseline contract / campaign coverage / analysis bridge", "test_campaign_bridge.py"),
    ("unified gate status / methodology resolution", "test_gate_status_methodology.py"),
    ("waiver durability / finalize acknowledgement", "test_waiver_durability.py"),
    ("validator freshness / stale computed flags", "test_validator_freshness.py"),
    ("typed scope / eval contract", "test_scope_contract.py"),
]


def main():
    failures, total_pass, total_fail = [], 0, 0
    for label, fname in SUITES:
        r = subprocess.run([sys.executable, str(HERE / fname)], capture_output=True, text=True)
        last = (r.stdout.strip().splitlines() or ["(no output)"])[-1]
        ok = r.returncode == 0
        print(f"{'OK  ' if ok else 'FAIL'}  {label:<56} {last}")
        if not ok:
            failures.append(label)
            if r.stderr.strip():
                print("      stderr:", r.stderr.strip().splitlines()[-1])
        m = re.search(r"(\d+) passed, (\d+) failed", last)
        if m:
            total_pass += int(m.group(1)); total_fail += int(m.group(2))
    print(f"\n=== {len(SUITES) - len(failures)}/{len(SUITES)} suites OK · {total_pass} assertions passed, "
          f"{total_fail} failed ===")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
