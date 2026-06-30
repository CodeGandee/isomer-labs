---
name: isomer-rsch-finalize-v2
description: Use when a research inquiry may be ready to close, pause, publish onward, hand off, or summarize with clear claims and limitations.
---

# Isomer Research Finalize V2

## Overview

Finalize produces the responsible end state of a research loop. It separates what can be claimed from what remains uncertain.

## When to Use

Use this skill when the current loop has enough frame, comparator, result, analysis, or decision material to stop or hand off responsibly. Do not use it to make weak evidence look complete.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Check closure readiness**. Decide whether the work can responsibly stop, pause, hand off, or proceed to paper-facing work.
2. **Consolidate the claim boundary**. State supported claims, weakened claims, refuted ideas, open questions, and limits.
3. **Summarize the path taken**. Link the final position to the frame, comparator, hypotheses, results, analysis, and decisions that matter.
4. **Name the recommendation**. Choose finish, park, continue, reframe, repair, or hand off.
5. **Produce [[rsch-object:final-summary]]**. Include the final position, limitations, unresolved risks, and next responsible action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the v2 shared loop, the placeholder registry, and the user's request, then execute the plan.

## Semantic Inputs

- Optional [[rsch-object:research-frame]]
- Optional [[rsch-object:comparator-contract]]
- Optional [[rsch-object:selected-hypothesis]]
- Optional [[rsch-object:experiment-result]]
- Optional [[rsch-object:analysis-finding]]
- Optional [[rsch-object:science-validity-note]]
- Optional [[rsch-object:route-decision]]

## Semantic Outputs

- [[rsch-object:final-summary]]
- Optional [[rsch-object:route-decision]] when closure is not justified and another route is required.

## Reference Routing

- Read `isomer-rsch-shared-v2` for the core loop and placeholder rule.

## Guardrails

- Do not finalize from memory when the semantic evidence is missing.
- Do not hide failures, null results, or contradicted claims.
- Do not call work complete when the responsible route is decision, analysis, comparator repair, or another experiment.

## Source Lineage

Distilled from the DeepScientist finalize process analysis: gather state, check the finalization gate, consolidate claims and limitations, recommend closure or handoff, and avoid hiding failure.
