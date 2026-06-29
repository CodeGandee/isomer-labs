---
name: deepresearch-review-craft
description: Use when the reviewer role critiques a manuscript or experiment package, audits whether claims trace to real validated evidence, runs the evidence-authenticity / manuscript-coverage gate, benchmarks literature positioning against nearest neighbors, or writes a review report, revision log, or experiment-TODO. Keywords — review stage, 13 review dimensions, authenticity gate, fabrication-risk labels, lit-benchmark, novelty matrix, accept/revise/stop/branch disposition, evidence validate, lit audit, knowledge cards.
---

# review-craft

## Overview
Self-contained reviewer-craft methodology for the **review stage** of the loop: the 13 review dimensions, the evidence-authenticity / manuscript-coverage gate that catches polished-but-hollow or overclaimed papers, the qualitative literature-positioning benchmark, and the three output templates (review report, revision log, experiment-TODO). This is a read-only methodology lookup — it changes no canonical state.

## When to Use
- You hold the **reviewer** role and are critiquing a manuscript or an experiment package.
- You need to check whether each manuscript claim traces to real, validated, durable evidence (anti-fabrication audit on top of `evidence validate`).
- You are positioning the paper against its nearest neighbors / strong accepted papers.
- You are writing up review findings, a revision log, or follow-up experiment requests.

When NOT to use:
- You are not the reviewer (wrong role) — do not run this audit from a writer/operator/orchestrator seat.
- You want to finalize, mutate results, confirm GPU, or change quest state — this craft never does that; it is advisory only and the DB stays canonical.
- You would cross quest-isolation bounds — keep all evidence, refs, and comparators inside the current quest.

## Workflow
1. (Optional) Index the methodology surface for traceability:
   `$HARNESS --via skill:deepresearch-review-craft:<your-role> knowledge cards --query authenticity-gate`
   (or `knowledge query --kind reference`). This records no row (read-only).
2. Run an INDEPENDENT skeptical audit across the **13 review dimensions** (see `## Review Dimensions`). Do not mirror prior self-review notes; do not fabricate praise, flaws, citations, or fatal defects.
3. Run the **Evidence Authenticity & Manuscript Coverage gate** (see `## Authenticity Gate`): build an experiment inventory from durable artifacts, recompute the real paper-facing result count manually, and assign a fabrication-risk label per result. Run this before recommending `accept`.
4. Run the **literature-positioning benchmark** (see `## Literature Benchmark`): build a 3–8 paper comparator set, record refs via `lit fetch` → `reference.record` then `claim link`, and fill the novelty / related-work matrix against nearest neighbors. Decide whether each gap is a *writing* fix or a *missing-evidence* fix before requesting any experiment.
5. Separate blocker types before writing TODOs — analysis / manuscript / language-provenance / submission — and route each correctly (see `## Routing Discipline`). Never convert a manuscript/submission blocker into a fake experiment.
6. Produce the three outputs using the inlined templates: a **review report** (`## Review Report Template`), a **revision log** (`## Revision Log Template`, flag per issue whether it blocks finalize), and an **experiment-TODO list** (`## Experiment TODO Template`).
7. Recommend a **disposition** — `accept` · `revise` · `stop`/`branch` on a publishability or value collapse. A low-quality `stop` requires operator confirmation (`decision.requires_user_confirm=1` + `decision.confirm`), routed via the Orchestrator. Prefer narrowing/downgrading an over-broad claim over defending it with style.
8. Record outcomes through your role's normal skill/commands. Map any external tool names in legacy material (`artifact.*`, `memory.*`, `bash_exec`) to the `$HARNESS` surface. Return the method to the calling task and continue.

If the task does not map cleanly to these steps, use your native planning tool to build a plan from the commands/constraints in this skill, then execute it.

## Common Mistakes
- **Mirroring the self-review** instead of running an independent skeptical audit; fabricating praise, flaws, citations, or fatal defects.
- **Trusting ready-counts / checklist labels.** Status must come from durable artifacts — open the files; do not trust ready-counts when duplicate rows, stale outline refs, pending rows, or missing metrics are present. Recompute the real paper-facing result count manually.
- **Routing a manuscript/submission/positioning problem into a fake experiment** (or recommending rhetoric when the real problem is missing evidence). Separate blocker types first.
- **Writing a vague "run more ablations" list** instead of using the experiment-TODO template.
- **Requesting new experiments to answer a literature-positioning question** — first decide whether the fix is writing, positioning, claim narrowing, or genuinely missing evidence.
- **Padding the bibliography** to clear a citation floor instead of adding real, claim-linked positioning references against nearest neighbors.
- **Defending an over-broad claim with style** rather than narrowing/downgrading it.
- **Treating this craft as authoritative state.** It is advisory; never finalize, mutate results, confirm GPU, or change quest state from here. `evidence validate` only checks DB-row consistency; this gate is the human/agent audit layer on top.

## Rationalizations vs. Red Flags
| Rationalization an agent might make | Red flag — what to do instead |
| --- | --- |
| "The ready-count says N results, so the paper has N." | Open the artifacts and recompute the real paper-facing count manually. |
| "The checklist labels it done." | Status comes from durable artifacts, not checklist labels. |
| "The writing is weak, so let's run more experiments." | Wording/positioning/claim-scope problems route to write/claim-downgrade, never to a fake experiment. |
| "There's a positioning gap — request a new experiment." | First decide writing vs. positioning vs. claim-narrowing vs. genuinely missing evidence. |
| "Add a few more citations to clear the floor." | Add real, claim-linked positioning refs against nearest neighbors, not padding. |
| "The claim is bold; defend it with stronger prose." | Prefer narrowing/downgrading the over-broad claim. |
| "`evidence validate` passed, so it's submission-ready." | That only checks DB-row consistency; run the full authenticity + coverage gate. |
| "This is a clear low-quality stop, just finalize it." | A low-quality `stop` requires operator confirmation (`decision.requires_user_confirm=1` + `decision.confirm`), routed via the Orchestrator. |

---

## Review Dimensions

Run an INDEPENDENT skeptical audit — do not mirror prior self-review notes; do not fabricate praise, flaws, citations, or fatal defects.

### 13 review dimensions
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

### Routing discipline (the core rule)
Route the work correctly — do NOT recommend more experiments when the real problem is wording, positioning, or claim scope; do NOT recommend rhetoric when the real problem is missing evidence. Separate blocker types before writing TODOs: analysis blockers / manuscript blockers / language-provenance blockers / submission blockers. Never turn a manuscript/submission blocker into a fake experiment; never write a vague "run more ablations" list (use the experiment-TODO template).

### Disposition (Houmao routes via the Orchestrator)
`accept` · `revise` · **`stop`/`branch` on a publishability or value collapse** — and a low-quality `stop` requires operator confirmation (`decision.requires_user_confirm=1` + `decision.confirm`). Prefer narrowing/downgrading an over-broad claim over defending it with style.

Outputs: a review report (`## Review Report Template`), a revision log (`## Revision Log Template`, flag per issue whether it blocks finalize), and an experiment-TODO list (`## Experiment TODO Template`).

---

## Authenticity Gate

The anti-fabrication core of review. Houmao's `evidence validate` only checks DB-row consistency (supported-claims-without-support, open contradictions, orphans); this gate is the human/agent audit on top of it that catches a polished-but-hollow or overclaimed paper. Run it before recommending `accept`.

### Build an experiment inventory
From logs, result rows, measurements, summaries, and the manuscript claims. For each experiment record:
- expected id / purpose
- **status from durable artifacts, not checklist labels**
- artifact paths; metrics actually present (open the files; do not trust ready-counts)
- current / stale / duplicate / failed / negative / superseded?
- does it appear in the manuscript (table/figure/caption)? which exact claim does it support?

**Recompute the real paper-facing result count manually** — do not trust ready counts when duplicate rows, stale outline refs, pending rows, or missing metrics are present.

### Fabrication-risk labels (per result)
`no issue` · `provenance gap` · `manuscript overclaim` · `written-but-unsupported` · `contradiction` · `likely false or fabricated claim`.

### Gate verdict
A paper is NOT submission-ready unless ALL pass: compile/PDF, evidence provenance, manuscript coverage, citation sufficiency, language hygiene, and experiment-matrix consistency. Map any failure to a route (analysis / write / claim-downgrade / limitation), not to vague polishing.

---

## Literature Benchmark

Houmao's `lit audit` only counts reference rows + reference-backed claims against a floor. This procedure is the qualitative positioning audit that decides whether a gap is a *writing* fix or a *missing-evidence* fix — run it during review, before requesting any new experiment.

### Build a comparator set of 3–8 papers
- 1–3 closest technical neighbors
- 1–3 writing / story exemplars (top-venue accepted papers: ICLR/ICML/NeurIPS/CVPR/ACL/EMNLP/Nature/Science/Q1)
- 1–2 experiment-package exemplars

Record (via `lit fetch` → `reference.record`, then `claim link`): title / venue / relevance + what each teaches about abstract framing, problem→gap→method→evidence logic, reader onboarding, experiment design/ablations/baselines, figure/table roles, related-work positioning.

### Novelty / related-work matrix
`Topic | This paper | Closest prior work | Overlap | Residual novelty/value` — forces genuine positioning against the *nearest neighbors*, not the broad method family.

### Critical discipline
Do NOT request new experiments just to answer a literature-positioning question. First decide whether the fix is writing, positioning, claim narrowing, or genuinely missing evidence. Citation floor for a mature empirical paper trends well above the harness `min_refs` default — aim for real, claim-linked positioning references, not a padded bibliography (see `execplan/docs/publication-quality.md`).

---

## Review Report Template

```text
## Review mode

- review_followup_policy:
- manuscript_edit_mode:
- manuscript_source_status:

## Summary

- paper / draft:
- overall judgment:
- top 3 highest-risk issues:

## Strengths

-

## Weaknesses

-

## Key Issues

### Issue 1

- why it matters:
- evidence anchor:
- risk level:
- likely route:

### Issue 2

- why it matters:
- evidence anchor:
- risk level:
- likely route:

## Actionable Suggestions

- problem:
- cause:
- actionable fix:
- acceptance criterion:
- copy-ready revision text:
- latex-ready revision text:

## Storyline Options + Writing Outlines

- current narrative weakness:
- stronger storyline option:
- outline change needed:

## Priority Revision Plan

1.
2.
3.

## Manuscript Revision Package

- section:
- old wording / weakness:
- new wording:
- evidence basis:
- latex-ready replacement block:

## Experiment Inventory & Research Experiment Plan

- what existing experiments already cover:
- what still lacks evidence:
- which gaps are text-only rather than experiment-only:

## Novelty Verification & Related-Work Matrix

### Taxonomy

Root
├── Branch A
│   └── Leaf A1
└── Branch B
    └── Leaf B1

### Comparison Matrix

| Topic | This paper | Closest prior work | Overlap | Residual novelty / value |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## References

-

## Optional Internal Score

- overall score:
- post-revision target:
```

---

## Revision Log Template

```text
## Revision Summary

- current draft state:
- review_followup_policy:
- manuscript_edit_mode:
- highest-priority fixes:
- blockers:

## Issue-by-issue log

### Issue REV-001

- source issue:
- severity:
- why it matters:
- fix type:
  - text revision
  - literature positioning
  - baseline recovery
  - supplementary experiment
  - claim downgrade
- concrete change:
- copy-ready revision text:
- latex-ready revision text:
- status:
- blocks finalize:

### Issue REV-002

- source issue:
- severity:
- why it matters:
- fix type:
- concrete change:
- status:
- blocks finalize:

## Deferred / downgraded items

- item:
- reason:
- how the manuscript should reflect the limitation:
```

---

## Experiment TODO Template

```text
## Follow-up experiment / analysis TODOs

### TODO EXP-001

- source review issue:
- matrix exp id:
- why current evidence is insufficient:
- route type:
  - existing-result analysis
  - comparator baseline
  - supplementary experiment
  - figure / table regeneration
- experiment type:
  - component_ablation
  - sensitivity
  - robustness
  - efficiency_cost
  - highlight_validation
  - failure_boundary
  - case_study_optional
- tier:
  - main_required
  - main_optional
  - appendix
  - optional
- minimum task:
- required metric(s):
- minimal success criterion:
- likely paper placement:
  - main_text
  - appendix
  - maybe
  - omit
- expected manuscript impact:
- owner / next step:

### TODO EXP-002

- source review issue:
- matrix exp id:
- why current evidence is insufficient:
- route type:
- experiment type:
- tier:
- minimum task:
- required metric(s):
- minimal success criterion:
- likely paper placement:
- expected manuscript impact:
- owner / next step:
```

---

## Commands & Audit Stamps

- Index the methodology surface (read-only, records no row):
  `$HARNESS --via skill:deepresearch-review-craft:<your-role> knowledge cards --query authenticity-gate`
  (or `knowledge query --kind reference`).
- DB-row consistency precheck (supported-claims-without-support, open contradictions, orphans): `evidence validate`. This is necessary but not sufficient — the Authenticity Gate above runs on top of it.
- Reference-count / reference-backed-claim floor check: `lit audit`. The Literature Benchmark above is the qualitative layer on top.
- Record positioning references: `lit fetch` → `reference.record`, then `claim link`.
- Disposition with a low-quality stop: set `decision.requires_user_confirm=1` and `decision.confirm` (operator confirmation, routed via the Orchestrator).

## Audit / Boundaries
- `--via skill:deepresearch-review-craft:<role>` is passed for traceability; read-only, so it records no row.
- Never finalize, mutate results, confirm GPU, or change quest state from here.
- The DB stays canonical; this craft is advisory, never an authoritative state surface.
