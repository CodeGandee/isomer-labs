# Review dimensions + disposition

Run an INDEPENDENT skeptical audit — do not mirror prior self-review notes; do not fabricate praise,
flaws, citations, or fatal defects.

## 13 review dimensions
1. Research question / value
2. Novelty / positioning (vs nearest neighbors, not just the broad family)
3. Method-to-problem fit
4. Evidence sufficiency
5. Experimental validity + baseline comparability
6. Claim scope / over-claiming risk
7. Writing defensibility / logical flow
8. Manuscript language hygiene + provenance leakage (no route/operator/worktree/loop wording)
9. Figure/table usefulness
10. Citation sufficiency (count verified refs vs nearby strong papers)
11. Full-paper style/pacing vs strong accepted papers
12. Experiment-package completeness vs nearby high-level papers
13. Submission readiness

## Routing discipline (the core rule)
Route the work correctly — do NOT recommend more experiments when the real problem is wording,
positioning, or claim scope; do NOT recommend rhetoric when the real problem is missing evidence.
Separate blocker types before writing TODOs: analysis blockers / manuscript blockers /
language-provenance blockers / submission blockers. Never turn a manuscript/submission blocker into a
fake experiment; never write a vague "run more ablations" list (use the experiment-todo template).

## Disposition (Houmao routes via the Orchestrator)
`accept` · `revise` · **`stop`/`branch` on a publishability or value collapse** — and a low-quality
`stop` requires operator confirmation (`decision.requires_user_confirm=1` + `decision.confirm`). Prefer
narrowing/downgrading an over-broad claim over defending it with style.

Outputs: a review report (`review-report-template.md`), a revision log (`revision-log-template.md`,
flag per issue whether it blocks finalize), and an experiment-TODO list (`experiment-todo-template.md`).
