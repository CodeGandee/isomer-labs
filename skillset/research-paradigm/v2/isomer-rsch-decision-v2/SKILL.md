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

1. **Check decision readiness**. Build <DECISION_CONTEXT_BRIEF> and confirm the current line, latest decisive result, and stale-route state are clear enough to judge. Read `references/operational-guidance.md` before judging readiness.
2. **State the route question**. Record <ROUTE_QUESTION> with the real choice, strongest support, strongest contradiction, main risk, main cost, and new evidence. Read `references/research-route-criteria.md` before evidence compression.
3. **Choose the smallest canonical action**. Use <DECISION_EVIDENCE_PACKET> to select one action from the canonical action set without hiding rejected alternatives. Read `references/canonical-actions.md` and `references/research-route-criteria.md`.
4. **Record the verdict**. Create <ROUTE_DECISION_RECORD> with verdict, action, reason, evidence, rejected alternatives, and next route. Read `references/strategic-decision-template.md`.
5. **Preserve the resume point**. Write <DECISION_CHECKPOINT_MEMORY> when the decision changes the active route, or create <USER_DECISION_REQUEST> or <DECISION_BLOCKER_RECORD> when local evidence cannot decide safely. Read `references/checkpoint-memory-template.md` and `references/operational-guidance.md`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Reference Routing

Read these pages as needed:

- `references/operational-guidance.md` for tactical route judgment, baseline reuse, user-input, blocker, and checkpoint rules.
- `references/canonical-actions.md` for use a stable action vocabulary so downstream stages know what changed.
- `references/research-route-criteria.md` for judge routes from evidence rather than optimism.
- `references/strategic-decision-template.md` for record a consequential route decision durably.
- `references/checkpoint-memory-template.md` for preserve a resume point after a route-changing decision.

## Cross-Step Quality Gates

### Metrics

- Route-blocking unknown count: number of unresolved state, evidence, preference, scope, or cost unknowns that would change the chosen canonical action; lower is better.
- Rejected-alternative coverage: fraction of serious rejected alternatives or blockers in <ROUTE_DECISION_RECORD> with a decisive reason and evidence basis; higher is better.

### Checks

- Readiness check: <DECISION_CONTEXT_BRIEF> makes the current line, latest decisive result, and stale-route state clear enough to judge or routes to a reconciliation skill.
- Question check: <ROUTE_QUESTION> names the real decision, strongest support, strongest contradiction, main risk, main cost, and genuinely new evidence.
- Action check: the chosen canonical action is the smallest action that resolves the current state and does not hide a blocker behind vague continuation.
- Record check: <ROUTE_DECISION_RECORD> includes verdict, action, reason, evidence, rejected alternatives, and next route.
- User-decision check: <USER_DECISION_REQUEST> appears only when local evidence cannot safely resolve a real preference, scope, or cost choice.
- Continuity check: <DECISION_CHECKPOINT_MEMORY> or the next route record is explicit enough that later v2 skills do not need to guess what changed.

## Exit Criteria

This skill can end only when the relevant placeholders are explicit enough for the next route, a blocker is recorded, and later v2 skills do not need to guess what changed or why.

## Common Mistakes

- Do not continue after the route, gate, or blocker is already clear.
- Do not replace evidence requirements with optimistic prose.
- Do not bind source paths, filenames, or source harness outputs as final Isomer storage contracts.
- Do not ask the user routine technical questions before checking durable local evidence.
- Do not hide blocked states behind vague progress language.
