---
name: isomer-rsch-decision-v1
description: Make one explicit research route judgment from durable evidence and record the smallest valid next action.
---

# Isomer Research Decision

## Overview

Use this skill when evidence needs a go, stop, Research Inquiry Relationship, reuse-comparator, write, finalize, reset, Gate, or blocker decision.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Load required context**. Read `references/isomer-research-contract.md` first and read `references/provenance.md` when source provenance or license context matters.
2. **Select supporting references** from **Reference Routing** when route criteria, action taxonomy, Decision Record structure, checkpoint state, or operational guidance matters.
3. **Check decision readiness**. If the current mainline, latest decisive result, stale routes, or blocker state is unclear, route through intake before judging.
4. **State the exact route question** and gather only evidence that can change that decision.
5. **Compare the smallest valid actions** using support, contradiction, cost, risk, user preference, scope, and changed facts.
6. **Use Gate Policy preflight for governed choices** such as cost, credential use, privacy, safety, publication-facing output, finality, external upload, or missing user-held source, and open a Gate only when the selected policy requires Operator Agent judgment.
7. **Record the Decision Record and handoff** with verdict, action, rationale, evidence, rejected alternatives, consequences, actor, timestamp, next Workflow Stage Cursor, pause, or blocker.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the constraints, references, and user request, then execute the plan.

## Reference Routing

Read first:

- `references/isomer-research-contract.md` for local terminology, truth-source, runtime-boundary, and TBD-surface rules.
- `references/provenance.md` when source provenance or license context matters.

Read references as needed:

- `references/strategic-decision-record.md` when a route-changing Decision Record needs a durable structure.
- `references/route-criteria.md` when choosing among Research Inquiry Relationships, candidate packages, experiments, paper routes, or blockers.
- `references/canonical-actions.md` when translating the route outcome into the smallest valid next action.
- `references/checkpoint-resume-template.md` when the decision changes the authoritative resume point.
- `references/operational-guidance.md` when user input, baseline reuse, paper-route stop-loss, or algorithm-first frontier judgment matters.

## Entry Signals

- Durable evidence needs a go, stop, Research Inquiry Relationship, reuse-comparator, write, finalize, reset, Gate, or blocker judgment.
- The board is clear enough to decide, or intake can be routed first.
- A user-facing or operator-facing choice needs rationale and consequences.

## Exit Criteria

- Verdict, rationale, evidence, rejected alternatives, consequences, actor, and timestamp are recorded.
- Any true user preference, scope, cost, safety, privacy, publication-facing, or finality choice is represented by Gate Policy preflight and a Gate when human judgment is required.
- The next Workflow Stage Cursor, pause, or blocker is explicit.
- The route does not need later stages to guess what was decided or why.

## Durable Outputs

- Decision Record.
- Optional Gate and user-facing milestone.
- Next Workflow Stage Cursor, pause, or blocker.
- Optional checkpoint or resume packet when the authoritative active node changes.

## Guardrails

- Do not repeat a decision without new evidence.
- Do not hide a blocker behind vague continuation.
- Do not choose finalization unless closure criteria are satisfied.
- Do not choose among candidate packages without naming the winner, rejected alternatives, and criteria.
- Do not launch follow-up analysis unless the expected information gain justifies the cost.
- For paper-facing routes, stop or open a Research Inquiry Relationship when evidence shows that novelty, evidence sufficiency, or reader value has collapsed beyond reasonable narrowing; run Gate Policy preflight and open a Gate before executing a preference-sensitive paper stop.
- Use the accepted Decision Record fields for decision fields.
