---
name: isomer-rsch-analysis-v2
description: Use when a Research Inquiry or Research Task needs bounded follow-up evidence, ablations, robustness checks, failure analysis, or limitation analysis after a parent result already exists.
---

# Isomer Research Analysis V2

## Overview

Analysis answers focused follow-up questions about an existing result. It decomposes a parent result into bounded evidence slices, records slice-level interpretations before campaign-level claims, and routes from the updated claim boundary.

Placeholder definitions live in `migrate/placeholders.md`.

## When to Use

Use this skill when:

- A measured result, selected route, paper gap, reviewer item, or failure mode needs follow-up evidence.
- A claim needs ablation, robustness, sensitivity, qualitative, or boundary-case checks.
- The next route depends on whether a parent result survives a focused analysis slice.
- Writing-facing or review-facing evidence needs a bounded analysis plan rather than a new main run.

Do not use this skill when:

- No parent result or parent claim exists yet.
- The work is a new main experiment rather than follow-up evidence.
- The route question is still ideation or baseline recovery.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Check the parent boundary**. Build <ANALYSIS_CONTEXT_BRIEF> and confirm the parent result, claim, route decision, paper gap, or reviewer item is specific enough for follow-up work.
2. **Choose the smallest useful campaign**. Use <PARENT_RESULT_EVIDENCE> to draft <ANALYSIS_SLICE_PLAN> with only slices that can change the parent claim, limitation, or next route.
3. **Gate resources and comparability**. Confirm each slice has feasible compute, data, metric, and comparison assumptions before execution.
4. **Run and record slices**. For every executed slice, produce <ANALYSIS_SLICE_RECORD> before making campaign-level conclusions.
5. **Interpret the campaign**. Aggregate slice evidence into <ANALYSIS_CAMPAIGN_SUMMARY> without claiming more than the slices support.
6. **Route from evidence**. Return <ANALYSIS_ROUTE_DECISION> or <ANALYSIS_BLOCKER_RECORD>, then preserve <ANALYSIS_CONTINUITY_UPDATE> when the result changes future work.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Reference Routing

Read these pages as needed:

- `references/campaign-design.md` for design the smallest analysis campaign that can change a parent claim or route.
- `references/slice-record-template.md` for record one follow-up analysis slice before campaign-level interpretation.
- `references/evidence-gate.md` for check whether slice evidence is strong enough to update a claim or route.
- `references/operational-guidance.md` for run analysis work without turning it into an unbounded campaign.

## Exit Criteria

This skill can end only when the relevant placeholders are explicit enough for the next route, a blocker is recorded, and later v2 skills do not need to guess what changed or why.

## Common Mistakes

- Do not continue after the route, gate, or blocker is already clear.
- Do not replace evidence requirements with optimistic prose.
- Do not bind source paths, filenames, or DeepScientist harness outputs as final Isomer storage contracts.
- Do not ask the user routine technical questions before checking durable local evidence.
- Do not hide blocked states behind vague progress language.
