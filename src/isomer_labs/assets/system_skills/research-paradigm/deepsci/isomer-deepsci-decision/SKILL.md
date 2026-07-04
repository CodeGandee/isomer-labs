---
name: isomer-deepsci-decision
description: Use when research work needs an explicit evidence-backed route choice, stop, branch, baseline reuse, writing, finalization, reset, or user-sensitive decision before continuing.
---

# Isomer Research Decision

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`, and request `--render markdown` only for the generated review view.

Latest-context reminder: before accepted durable record writes, record refreshes, or durable route, claim, context, evidence, result, or publication-facing decisions, follow `isomer-deepsci-shared` Latest Context Preflight. Resolve current Effective Topic Context and Workspace Runtime, inspect relevant durable records, capture or update `latest-context-snapshot`, and treat prompt memory, chat memory, prior prose, older rendered records, and worker-local files as candidate context until checked. Standalone source-only reading may skip this preflight until accepted Isomer records are written or refreshed.

Worker-output reminder: before writing JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, or other plain generated files, follow `isomer-deepsci-shared` Worker Output Policy: resolve `project outputs policy`, write under an operation-specific child set of the returned root, preserve durable records on their semantic bindings, and act on `commit_after_operation` as the post-action commit preference.

Decision makes one route judgment from durable evidence, records the verdict and smallest valid action, then gets the Research Topic moving again. It does not substitute for state reconciliation when the active line is still unclear.

Placeholder definitions live in `migrate/placeholders.md`; storage bindings live in `placeholder-bindings.md`.

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
2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-decision --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
3. **State the route question**. Record <ROUTE_QUESTION> with the real choice, strongest support, strongest contradiction, main risk, main cost, and new evidence. Read `references/research-route-criteria.md` before evidence compression.
4. **Choose the smallest canonical action**. Use <DECISION_EVIDENCE_PACKET> to select one action from the canonical action set without hiding rejected alternatives. Read `references/canonical-actions.md` and `references/research-route-criteria.md`.
5. **Record the verdict**. Create <ROUTE_DECISION_RECORD> with verdict, action, reason, evidence, rejected alternatives, and next route. Read `references/strategic-decision-template.md`.
6. **Preserve the resume point**. Write <DECISION_CHECKPOINT_MEMORY> when the decision changes the active route, or create <USER_DECISION_REQUEST> or <DECISION_BLOCKER_RECORD> when local evidence cannot decide safely. Read `references/checkpoint-memory-template.md` and `references/operational-guidance.md`.
7. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-decision --stage end`. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Reference Routing

Read these pages as needed:

- `references/operational-guidance.md` for tactical route judgment, baseline reuse, user-input, blocker, and checkpoint rules.
- `references/canonical-actions.md` for use a stable action vocabulary so downstream stages know what changed.
- `references/research-route-criteria.md` for judge routes from evidence rather than optimism.
- `references/strategic-decision-template.md` for record a consequential route decision durably.
- `references/checkpoint-memory-template.md` for preserve a resume point after a route-changing decision.

## Cross-Step Quality Gates

Read these gates before claiming the skill output is ready for handoff. Use `Metrics` to judge directional quality across the workflow and `Checks` to decide whether the output must be revised, blocked, or rerouted.

### Metrics

- Route-blocking unknown count: number of unresolved state, evidence, preference, scope, or cost unknowns that would change the chosen canonical action; lower is better.
- Rejected-alternative coverage: fraction of serious rejected alternatives or blockers in <ROUTE_DECISION_RECORD> with a decisive reason and evidence basis; higher is better.

### Checks

- Readiness check: <DECISION_CONTEXT_BRIEF> makes the current line, latest decisive result, and stale-route state clear enough to judge or routes to a reconciliation skill.
- Question check: <ROUTE_QUESTION> names the real decision, strongest support, strongest contradiction, main risk, main cost, and genuinely new evidence.
- Action check: the chosen canonical action is the smallest action that resolves the current state and does not hide a blocker behind vague continuation.
- Record check: <ROUTE_DECISION_RECORD> includes verdict, action, reason, evidence, rejected alternatives, and next route.
- User-decision check: <USER_DECISION_REQUEST> appears only when local evidence cannot safely resolve a real preference, scope, or cost choice.
- Continuity check: <DECISION_CHECKPOINT_MEMORY> or the next route record is explicit enough that later production DeepSci skills do not need to guess what changed.

## Exit Criteria

This skill can end only when the relevant placeholders are explicit enough for the next route, a blocker is recorded, and later production DeepSci skills do not need to guess what changed or why.

## Common Mistakes

- Do not continue after the route, gate, or blocker is already clear.
- Do not replace evidence requirements with optimistic prose.
- Do not bind source paths, filenames, or source harness outputs as final Isomer storage contracts.
- Do not ask the user routine technical questions before checking durable local evidence.
- Do not hide blocked states behind vague progress language.
