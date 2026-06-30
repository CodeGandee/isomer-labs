---
name: isomer-rsch-scout-v2
description: Use when a research task needs framing, metric clarification, literature orientation, benchmark neighborhood discovery, or next-stage routing before deeper work.
---

# Isomer Research Scout V2

## Overview

Scout clarifies the research problem enough to choose the next useful stage. It narrows uncertainty instead of producing a broad survey.

## When to Use

Use this skill when the objective, metric, benchmark neighborhood, baseline direction, or immediate next research action is unclear. Do not use it when a trusted [[rsch-object:research-frame]] and next stage already exist.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Reconstruct the frame**. State the task, intended reader or user, constraints, and the decision the scout work must enable.
2. **Find the minimum unknowns**. List only the unknowns that block the next research stage.
3. **Inspect local and external context selectively**. Reuse available context first, then inspect papers, code, data, or benchmarks only enough to answer the blocking unknowns.
4. **Define the evaluation direction**. Name the likely metric, comparator neighborhood, feasibility boundary, and uncertainty that remains.
5. **Produce [[rsch-object:research-frame]]**. Include next-stage routing to baseline, idea, decision, science, or blocker.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the v2 shared loop, the placeholder registry, and the user's request, then execute the plan.

## Semantic Inputs

- Optional [[rsch-object:research-frame]] when prior framing exists but may be stale or incomplete.
- Optional [[rsch-object:route-decision]] when a previous stage requested reframing.

## Semantic Outputs

- [[rsch-object:research-frame]]
- Optional [[rsch-object:route-decision]] when the next action is non-obvious or blocked.

## Reference Routing

- Read `isomer-rsch-shared-v2` for the core loop and placeholder rule.

## Guardrails

- Do not widen into an open-ended literature review.
- Do not invent a metric when the task needs the user, topic context, or domain facts to settle it.
- Do not route to ideation when the comparator or measurement basis is still too vague.

## Source Lineage

Distilled from the DeepScientist scout process analysis: frame the problem, identify minimum unknowns, narrow search, shortlist comparator directions, and route to the next anchor.
