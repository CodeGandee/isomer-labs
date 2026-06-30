---
name: isomer-rsch-baseline-v2
description: Use when research work needs a trustworthy comparator, metric contract, accepted waiver, or blocker before hypotheses, experiments, or claims can proceed.
---

# Isomer Research Baseline V2

## Overview

Baseline establishes the comparison basis for later progress. It asks what the work must beat, reproduce, explain, or intentionally waive.

## When to Use

Use this skill when [[rsch-object:research-frame]] exists but the comparator, metric, or comparability rules are not yet trustworthy. Do not use it to run a full experiment unless the baseline question itself requires a minimal verification.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Select the comparator target**. Identify the lightest comparator that makes the research question meaningful.
2. **Define the metric contract**. State the metric, dataset or task boundary, expected direction, and comparability assumptions.
3. **Choose the lightest trust route**. Attach, import, verify, reproduce, or waive only as much as needed for a fair comparison.
4. **Check comparability**. Surface deviations, missing context, or conditions that make the comparator unusable.
5. **Produce [[rsch-object:comparator-contract]]**. Include the accepted comparator, waiver, or blocker and the downstream route.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the v2 shared loop, the placeholder registry, and the user's request, then execute the plan.

## Semantic Inputs

- [[rsch-object:research-frame]]
- Optional [[rsch-object:science-validity-note]] when comparator trust depends on computation, packages, data, or simulation.

## Semantic Outputs

- [[rsch-object:comparator-contract]]
- Optional [[rsch-object:route-decision]] when proceeding without a comparator is a real scope choice.

## Reference Routing

- Read `isomer-rsch-shared-v2` for the core loop and placeholder rule.

## Guardrails

- Do not accept copied headline numbers without knowing what they compare.
- Do not let a convenient comparator replace the metric the task actually needs.
- Do not treat a waiver as invisible; name why it is acceptable and what it weakens.

## Source Lineage

Distilled from the DeepScientist baseline process analysis: choose the lightest trustworthy route, define metric comparability, verify enough evidence, then confirm, waive, or block.
