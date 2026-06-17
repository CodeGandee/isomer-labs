---
name: isomer-rsch-review
description: Run a skeptical audit of a substantial draft, report, or paper-like artifact before revision or finalization.
---

# Isomer Research Review

## Overview

Use this skill when a substantial draft, report, or paper-like Artifact needs an independent, evidence-grounded audit before revision, rebuttal, finalization, or a stop or branch decision.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Load required context**. Read `references/audit-gate.md` first and read `references/provenance.md` when source provenance or license context matters.
2. **Select supporting references** from **Reference Routing** when evidence authenticity, literature benchmarking, report writing, revision logs, follow-up TODOs, or route decisions matter.
3. **Confirm entry fit and review scope**. Use **Entry Signals** to confirm the work is review, not ordinary drafting or response to concrete external reviewer comments.
4. **Plan the audit**. Identify package maturity, core claims, strongest evidence, weakest evidence, likely rejection routes, coverage count, manuscript hygiene risks, and likely next route.
5. **Run evidence and literature checks**. Audit Evidence Items against claims, figures, tables, citations, bundle state, and nearby high-quality papers unless the user explicitly limits scope.
6. **Write durable review artifacts**. Produce the review report, revision log, and evidence TODO list only where evidence is truly missing.
7. **Route the next stage**. Send text fixes to write, novelty uncertainty to scout, comparator gaps to baseline, evidence gaps to analysis, non-trivial choices to decision, and final-ready packages to finalize.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the constraints, references, and user request, then execute the plan.

## Reference Routing

Read first:

- `references/audit-gate.md` for review purpose, scope rules, stop-loss behavior, source-term mappings, and TBD-surface rules.
- `references/provenance.md` when source provenance or license context matters.

Read references as needed:

- `references/evidence-authenticity-checklist.md` before judging manuscript strength, submission readiness, or evidence sufficiency.
- `references/literature-benchmark.md` when novelty, positioning, venue norms, citation sufficiency, or paper quality standards matter.
- `references/review-report-template.md` when producing the durable review Artifact.
- `references/revision-log-template.md` when converting serious issues into concrete manuscript or route fixes.
- `references/experiment-todo-template.md` when true evidence gaps require analysis, baseline recovery, figure regeneration, or supplementary runs.
- `references/follow-up-routing.md` when choosing between write, scout, baseline, analysis, decision, finalize, or blocker.

## Entry Signals

- A substantial manuscript, report, or paper-like Artifact exists and needs a skeptical gate.
- Claims, novelty, evidence sufficiency, figures, language hygiene, citation support, or likely rejection paths need independent audit.
- The output should reduce revision ambiguity and choose a next route.

## Exit Criteria

- A review Artifact, revision log, and any evidence TODO Artifact are durable.
- Major weaknesses, missing evidence, novelty risks, manuscript hygiene issues, and likely rejection routes are explicit.
- The next route is write, scout, baseline, analysis, decision, finalize, rebuttal, or blocker, with the reason recorded.

## Durable Outputs

- Review report Artifact.
- Revision log Artifact.
- Evidence TODO Artifact when the review finds true evidence gaps.
- Literature benchmark or comparison matrix when novelty or venue standards affect the judgment.
- Decision Record or Gate for route choice, claim downgrade, stop, branch, review closure, or finalization readiness.

## Guardrails

- Do not mirror earlier self-review notes without independent audit.
- Do not write "no weaknesses" unless likely rejection paths have been listed and resolved, downgraded, or accepted as out of scope.
- Do not recommend experiments when the real fix is wording, positioning, claim scope, figure presentation, or citation repair.
- Do not recommend rhetoric when the real blocker is missing evidence.
- Do not hide a fatal publishability, value, or evidence collapse behind another cosmetic revision pass.
- Do not call a manuscript submission-ready unless evidence provenance, manuscript coverage, citation sufficiency, language cleanliness, figure/table status, bundle state, and unresolved Gates all pass.
