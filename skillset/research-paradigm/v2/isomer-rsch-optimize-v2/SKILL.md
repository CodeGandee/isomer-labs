---
name: isomer-rsch-optimize-v2
description: Use when an algorithm-first research task needs candidate shaping, frontier ranking, fusion, debug routing, or promotion of one route into experiment work.
---

# Isomer Research Optimize V2

## Overview

Optimize manages candidate search when the research problem is mostly algorithmic. It keeps the frontier small enough to act on and promotes one route at a time.

## When to Use

Use this skill when [[rsch-object:selected-hypothesis]] needs algorithm-first refinement, multiple candidate variants compete, or a result points to fusion or debug search. Do not use it to turn every tiny attempt into a new research branch.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Refresh the frontier**. State the active candidate set, current best line, rejected lines, and the reason search is still useful.
2. **Choose the optimization mode**. Pick explore, exploit, fuse, debug, simplify, or stop based on the bottleneck.
3. **Shape candidate briefs**. Keep each candidate tied to a mechanism, expected effect, risk, and falsification cue.
4. **Promote one route**. Select the next hypothesis or experimental attempt that should receive attention.
5. **Produce [[rsch-object:optimization-frontier]] and, when ready, [[rsch-object:selected-hypothesis]]**.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the v2 shared loop, the placeholder registry, and the user's request, then execute the plan.

## Semantic Inputs

- [[rsch-object:research-frame]]
- Optional [[rsch-object:comparator-contract]]
- Optional [[rsch-object:selected-hypothesis]]
- Optional [[rsch-object:experiment-result]]
- Optional [[rsch-object:analysis-finding]]

## Semantic Outputs

- [[rsch-object:optimization-frontier]]
- Optional [[rsch-object:selected-hypothesis]]
- Optional [[rsch-object:route-decision]] when search should stop, reset, or move to experiment work.

## Reference Routing

- Read `isomer-rsch-shared-v2` for the core loop and placeholder rule.

## Guardrails

- Do not promote every plausible variant.
- Do not optimize without a comparator or metric unless the goal is explicitly exploratory.
- Do not let search continue after the next decisive experiment is clear.

## Source Lineage

Distilled from the DeepScientist optimize process analysis: manage candidate briefs, frontier ranking, line promotion, fusion, debug, and stop decisions.
