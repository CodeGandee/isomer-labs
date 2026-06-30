---
name: isomer-rsch-idea-v2
description: Use when a framed research problem and comparator basis need one falsifiable hypothesis, route, or algorithm-first brief before experiment or optimization work.
---

# Isomer Research Idea V2

## Overview

Idea selects a research direction by grounding the objective, current board, literature, bottleneck, and candidate frontier. It promotes one falsifiable route to experiment or hands an algorithm-first frontier to optimize.

Placeholder definitions live in `migrate/placeholders.md`.

## When to Use

Use this skill when:

- The research frame and comparator basis are clear enough to choose a direction.
- The current route is stale, weak, or contradicted and needs re-ideation.
- Literature or local evidence must shape the next hypothesis.
- A set of candidate ideas needs selection before execution.

Do not use this skill when:

- The frame or metric is still unclear and scout should run first.
- The comparator gate is unresolved and baseline should run first.
- A selected route is already experiment-ready.
- The task is algorithm-first frontier management rather than direction selection.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Ground the objective**. Create <OBJECTIVE_CONTRACT> from <IDEA_CONTEXT_BRIEF> with true target, proxies, false-progress signals, constraints, metric, and contribution frame.
2. **Recover the current board**. Build <CURRENT_BOARD_PACKET> from incumbent, latest result, active blocker, stale routes, and current question.
3. **Refresh literature only where needed**. Produce <LITERATURE_SURVEY_REPORT> when prior work or novelty boundaries can change the candidate frontier.
4. **Generate a bounded frontier**. Create <CANDIDATE_IDEA_FRONTIER> with differentiated route families, mechanism sketches, risks, and falsification paths.
5. **Challenge serious candidates**. Use <PRE_IDEA_DRAFT> to expose assumptions, local-optimum risk, rejection case, and testability.
6. **Select one route**. Record <SELECTED_HYPOTHESIS> and <IDEA_ROUTE_DECISION>, or create <IDEA_BLOCKER_RECORD> when no candidate passes the selection gate.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Reference Routing

Read these pages as needed:

- `references/objective-contract.md` for keep ideation pointed at the real target.
- `references/idea-sourcing.md` for generate useful candidates from bottlenecks and contradictions.
- `references/selection-gate.md` for promote only one falsifiable route.
- `references/selected-hypothesis-template.md` for create the handoff to experiment or optimize.
- `references/literature-survey-template.md` for record route-changing literature context.

## Exit Criteria

This skill can end only when the relevant placeholders are explicit enough for the next route, a blocker is recorded, and later v2 skills do not need to guess what changed or why.

## Common Mistakes

- Do not continue after the route, gate, or blocker is already clear.
- Do not replace evidence requirements with optimistic prose.
- Do not bind source paths, filenames, or DeepScientist harness outputs as final Isomer storage contracts.
- Do not ask the user routine technical questions before checking durable local evidence.
- Do not hide blocked states behind vague progress language.
