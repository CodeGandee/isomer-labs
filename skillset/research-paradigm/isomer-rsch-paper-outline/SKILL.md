---
name: isomer-rsch-paper-outline
description: Build or repair a paper-native outline with scoped claims, method abstraction, evaluation plan, and evidence boundaries.
---

# Isomer Research Paper Outline

## Overview

Use this skill before serious writing when a paper, report, or manuscript needs a paper-native outline that separates reader-facing claims from evidence inventory, run details, reproducibility facts, and unsupported ideas.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Load required context**. Read `references/outline-contract.md` first and read `references/provenance.md` when source provenance or license context matters.
2. **Select supporting references** from **Reference Routing** when a detailed template, maturity checklist, claim-evidence boundary, analysis-plan roles, or outline pattern examples matter.
3. **Confirm entry fit and lock inputs**. Use **Entry Signals** to confirm the task is outline creation, validation, or repair before drafting.
4. **Separate paper view from evidence view**. Identify the one-sentence reader-facing idea, measured facts, allowed interpretations, must-not-claim items, and reproducibility details.
5. **Build or repair the outline**. Define story spine, novelty boundary, scoped claims, method abstraction, evaluation plan, analysis plan, reviewer objections, and evidence grounding.
6. **Validate maturity and evidence boundaries**. Check claim support, falsification conditions, analysis count or waiver, reviewer objections, stale ids, and local process leakage.
7. **Route to writing or repair**. Produce a writing plan when the outline is valid, or route missing evidence, baselines, literature, or route choices to the right skill.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the constraints, references, and user request, then execute the plan.

## Reference Routing

Read first:

- `references/outline-contract.md` for paper-view and evidence-view rules, source-term mappings, runtime boundaries, and TBD-surface rules.
- `references/provenance.md` when source provenance or license context matters.

Read references as needed:

- `references/paper-outline-template.md` when producing a detailed durable outline Artifact.
- `references/mature-outline-checklist.md` when checking whether a full empirical outline is ready for writing.
- `references/claim-evidence-boundary.md` when deciding what may become paper text, appendix-only reproducibility detail, or must-not-claim material.
- `references/analysis-plan-roles.md` when choosing reviewer-facing analysis jobs and evidence group targets.
- `references/outline-patterns.md` when repairing outlines that read like implementation notes, run logs, or result dumps.

## Entry Signals

- A report or paper needs an outline before drafting.
- An existing outline does not match evidence, claims, method abstraction, evaluation plan, or reviewer-facing analysis plan.
- The paper idea must be separated from raw run details, local process facts, unsupported claims, or unstructured result dumps.

## Exit Criteria

- Paper view, evidence view, and section-level writing plan are durable.
- Scoped claims have Evidence Items, boundaries, and falsification conditions.
- Unsupported claims, missing evidence, stale ids, and process-language risks are visible before writing.
- The next route is write, analysis, scout, baseline, decision, review, or blocker.

## Durable Outputs

- Candidate, selected, or revised outline Artifact.
- Paper view and evidence view.
- Section-level writing plan.
- Claim-evidence boundary list, reviewer objection list, and analysis-plan roles.
- Decision Record or Gate when evidence, novelty, baseline, route, or paper scope is unresolved.

## Guardrails

- Do not copy run logs, local process notes, operator instructions, or execution details into the paper plan.
- Do not treat a section list as a mature outline.
- Do not escalate observations into claims without evidence and falsification boundaries.
- Do not mark a mature full-empirical outline ready without visible reviewer objections and analysis-plan coverage, unless the paper scope is explicitly downgraded.
- Use `[[tbd-surface:api-artifact-record]]` for unsettled outline recording and `[[tbd-surface:path-paper-layout]]` for unsettled paper layouts.
