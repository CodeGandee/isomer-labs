---
name: isomer-rsch-experiment-v2
description: Use when one selected hypothesis needs a bounded implementation or test that produces an interpretable measured result.
---

# Isomer Research Experiment V2

## Overview

Experiment turns one selected hypothesis into one interpretable result. It protects comparability and makes failed or null outcomes as useful as successful ones.

## When to Use

Use this skill when [[rsch-object:selected-hypothesis]] is ready to test and the measurement basis is clear enough. Do not use it when the route, comparator, or metric is still ambiguous.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Lock the test question**. State the hypothesis, comparator basis, metric, input conditions, and stop condition.
2. **Produce [[rsch-object:experiment-contract]]**. Keep the contract small enough that the result will be interpretable.
3. **Run the smallest valid test**. Implement or execute only what the contract needs, preserving failures and deviations.
4. **Compare the outcome**. Relate the observed result to the comparator, metric, hypothesis, and known caveats.
5. **Produce [[rsch-object:experiment-result]]**. Route to analysis, decision, optimize, science, or another experiment based on what changed.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the v2 shared loop, the placeholder registry, and the user's request, then execute the plan.

## Semantic Inputs

- [[rsch-object:selected-hypothesis]]
- Optional [[rsch-object:comparator-contract]]
- Optional [[rsch-object:science-validity-note]]
- Optional [[rsch-object:optimization-frontier]]

## Semantic Outputs

- [[rsch-object:experiment-contract]]
- [[rsch-object:experiment-result]]
- Optional [[rsch-object:route-decision]] when evidence makes the next route clear.

## Reference Routing

- Read `isomer-rsch-shared-v2` for the core loop and placeholder rule.

## Guardrails

- Do not silently change metric, data boundary, comparator, or success criterion mid-test.
- Do not treat a smoke check as main evidence.
- Do not drop failed, null, interrupted, or non-comparable outcomes.

## Source Lineage

Distilled from the DeepScientist experiment process analysis: recover selected idea and baseline, lock a run contract, execute one measured attempt, validate comparability, and route from evidence.
