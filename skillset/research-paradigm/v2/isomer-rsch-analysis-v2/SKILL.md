---
name: isomer-rsch-analysis-v2
description: Use when a result needs focused follow-up such as ablation, robustness checking, error analysis, failure analysis, or claim-boundary interpretation.
---

# Isomer Research Analysis V2

## Overview

Analysis answers the smallest follow-up question that can change how a result is understood. It is not a second main experiment hidden under another name.

## When to Use

Use this skill after [[rsch-object:experiment-result]] exists and a specific follow-up question would confirm, weaken, explain, or block a claim. Do not use it to widen into unrelated experiments.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Name the parent result**. Identify the result, claim, anomaly, or reviewer-style question that motivates analysis.
2. **Choose the lightest check**. Pick the smallest ablation, slice, robustness check, error analysis, or failure analysis that can change the interpretation.
3. **Run the focused check**. Keep scope tied to the parent result and preserve contradictory or null findings.
4. **Interpret the impact**. State whether the result is confirmed, weakened, narrowed, contradicted, or blocked.
5. **Produce [[rsch-object:analysis-finding]]**. Route to decision, optimize, experiment, science, or finalization.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the v2 shared loop, the placeholder registry, and the user's request, then execute the plan.

## Semantic Inputs

- [[rsch-object:experiment-result]]
- Optional [[rsch-object:comparator-contract]]
- Optional [[rsch-object:selected-hypothesis]]
- Optional [[rsch-object:science-validity-note]]

## Semantic Outputs

- [[rsch-object:analysis-finding]]
- Optional [[rsch-object:route-decision]] when the interpretation determines the next action.

## Reference Routing

- Read `isomer-rsch-shared-v2` for the core loop and placeholder rule.

## Guardrails

- Do not disguise a new main experiment as analysis.
- Do not expand slices after the route is already clear.
- Do not strengthen a claim when contradictory evidence remains unresolved.

## Source Lineage

Distilled from the DeepScientist analysis-campaign process analysis: lock the parent object, ask the smallest evidence question, run critical slices, interpret the claim impact, and route onward.
