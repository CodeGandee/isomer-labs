---
name: isomer-rsch-decision-v2
description: Use when research work needs an explicit evidence-backed route choice, stop, branch, baseline reuse, writing, finalization, reset, or user-sensitive decision before continuing.
---

# Isomer Research Decision V2

## Overview

Decision makes one route judgment from durable evidence, records the verdict and smallest valid action, then gets the Research Topic moving again. It does not substitute for state reconciliation when the active line is still unclear.

Placeholder definitions live in `migrate/placeholders.md`.

## When to Use

Use this skill when:

- The next route is not obvious.
- Evidence is mixed or contradictory.
- A blocker needs an explicit route.
- A user preference, scope, cost, or publishability choice cannot be inferred safely.
- A line may need to stop, branch, reset, write, review, finalize, or reuse a comparator.

Do not use this skill when:

- The active state is too ambiguous and first needs intake or scout-style reconciliation.
- The next action is already obvious from durable evidence.
- The real task is baseline recovery, ideation, execution, or analysis rather than a route judgment.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Check decision readiness**. Build <DECISION_CONTEXT_BRIEF> and confirm the current line, latest decisive result, and stale-route state are clear enough to judge.
2. **State the route question**. Record <ROUTE_QUESTION> with the real choice, strongest support, strongest contradiction, main risk, main cost, and new evidence.
3. **Choose the smallest canonical action**. Use <DECISION_EVIDENCE_PACKET> to select one action from the canonical action set without hiding rejected alternatives.
4. **Record the verdict**. Create <ROUTE_DECISION_RECORD> with verdict, action, reason, evidence, rejected alternatives, and next route.
5. **Preserve the resume point**. Write <DECISION_CHECKPOINT_MEMORY> when the decision changes the active route, or create <USER_DECISION_REQUEST> or <DECISION_BLOCKER_RECORD> when local evidence cannot decide safely.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Reference Routing

Read these pages as needed:

- `references/canonical-actions.md` for use a stable action vocabulary so downstream stages know what changed.
- `references/route-criteria.md` for judge routes from evidence rather than optimism.
- `references/decision-record-template.md` for record a consequential route decision durably.
- `references/checkpoint-memory-template.md` for preserve a resume point after a route-changing decision.

## Exit Criteria

This skill can end only when the relevant placeholders are explicit enough for the next route, a blocker is recorded, and later v2 skills do not need to guess what changed or why.

## Common Mistakes

- Do not continue after the route, gate, or blocker is already clear.
- Do not replace evidence requirements with optimistic prose.
- Do not bind source paths, filenames, or DeepScientist harness outputs as final Isomer storage contracts.
- Do not ask the user routine technical questions before checking durable local evidence.
- Do not hide blocked states behind vague progress language.
