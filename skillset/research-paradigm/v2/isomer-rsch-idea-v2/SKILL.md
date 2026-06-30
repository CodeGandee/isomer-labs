---
name: isomer-rsch-idea-v2
description: Use when a framed research task needs candidate hypotheses, limitation analysis, a differentiated frontier, or one selected falsifiable route.
---

# Isomer Research Idea V2

## Overview

Idea turns the current research situation into one falsifiable route. It favors small, testable hypotheses over decorative variations.

## When to Use

Use this skill when [[rsch-object:research-frame]] and usually [[rsch-object:comparator-contract]] are available, but the next hypothesis or route is not selected. Do not use it to brainstorm before the objective and evaluation boundary are clear.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Restate the objective contract**. Name the target improvement, constraint, or explanation the idea must serve.
2. **Read the current situation**. Identify the comparator, failure pattern, limitation, gap, or contradiction that justifies ideation.
3. **Generate bounded candidates**. Produce a small set of meaningfully different routes and reject cosmetic changes.
4. **Select one hypothesis**. Choose the route with the best balance of novelty, feasibility, expected effect, and falsifiability.
5. **Produce [[rsch-object:selected-hypothesis]]**. Include the expected effect, risk, falsification condition, and next experiment.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the v2 shared loop, the placeholder registry, and the user's request, then execute the plan.

## Semantic Inputs

- [[rsch-object:research-frame]]
- Optional [[rsch-object:comparator-contract]]
- Optional [[rsch-object:analysis-finding]]
- Optional [[rsch-object:optimization-frontier]]

## Semantic Outputs

- [[rsch-object:selected-hypothesis]]
- Optional [[rsch-object:route-decision]] when the best route is to stop, reframe, or repair the comparator first.

## Reference Routing

- Read `isomer-rsch-shared-v2` for the core loop and placeholder rule.

## Guardrails

- Do not brainstorm before naming the bottleneck.
- Do not select ideas that cannot be falsified by a near-term experiment.
- Do not hide rejected candidates if their rejection explains the chosen route.

## Source Lineage

Distilled from the DeepScientist idea process analysis: recover the objective, read the current board, identify limitation patterns, create bounded candidates, and select one route.
