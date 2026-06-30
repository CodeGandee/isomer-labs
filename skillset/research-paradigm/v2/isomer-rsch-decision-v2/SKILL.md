---
name: isomer-rsch-decision-v2
description: Use when evidence requires an explicit route choice such as continue, stop, branch, reframe, repair, finalize, or ask the user for a real preference.
---

# Isomer Research Decision V2

## Overview

Decision turns available evidence into one route judgment. It prevents loops that continue only because no one named the choice.

## When to Use

Use this skill when several next actions are plausible, when cost or scope requires user preference, when evidence blocks progress, or when a stage has enough information to route onward. Do not use it to restate an obvious next step unless the route needs justification.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **State the decision question**. Name the concrete route choice and why it matters now.
2. **Gather only decisive evidence**. Use the relevant semantic objects, not every available note.
3. **Compare options**. Include continue, stop, reframe, repair comparator, optimize, experiment, analyze, finalize, or ask user when relevant.
4. **Choose the smallest valid next action**. Ask the user only when preference, cost, safety, scope, or authorization is genuinely theirs to decide.
5. **Produce [[rsch-object:route-decision]]**. Include the chosen route, rationale, rejected alternatives, and next action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the v2 shared loop, the placeholder registry, and the user's request, then execute the plan.

## Semantic Inputs

- Optional [[rsch-object:research-frame]]
- Optional [[rsch-object:comparator-contract]]
- Optional [[rsch-object:selected-hypothesis]]
- Optional [[rsch-object:experiment-result]]
- Optional [[rsch-object:analysis-finding]]
- Optional [[rsch-object:science-validity-note]]
- Optional [[rsch-object:optimization-frontier]]

## Semantic Outputs

- [[rsch-object:route-decision]]
- Optional updated [[rsch-object:research-frame]], [[rsch-object:comparator-contract]], or [[rsch-object:selected-hypothesis]] when the decision changes the research state.

## Reference Routing

- Read `isomer-rsch-shared-v2` for the core loop and placeholder rule.

## Guardrails

- Do not repeat a decision without new evidence or a new user constraint.
- Do not hide a blocker behind "continue".
- Do not ask the user to choose when the evidence already determines the responsible next action.

## Source Lineage

Distilled from the DeepScientist decision process analysis: state the route question, compare actions against durable evidence, ask only for real preference or scope, and choose the smallest valid next stage.
