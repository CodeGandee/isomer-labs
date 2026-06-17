---
name: isomer-rsch-decision
description: Make one explicit research route judgment from durable evidence and record the smallest valid next action.
---

# Isomer Research Decision

## Overview

Use this skill when evidence needs a go, stop, branch, reuse-comparator, write, finalize, reset, Gate, or blocker decision.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Load required context**. Read `references/isomer-research-contract.md` first and read `references/provenance.md` when source provenance or license context matters.
2. **Select supporting references** from **Reference Routing** when route criteria, action taxonomy, Decision Record structure, checkpoint state, or operational guidance matters.
3. **Check decision readiness**. If the current mainline, latest decisive result, stale routes, or blocker state is unclear, route through intake before judging.
4. **State the exact route question** and gather only evidence that can change that decision.
5. **Compare the smallest valid actions** using support, contradiction, cost, risk, user preference, scope, and changed facts.
6. **Open a Gate only for true Operator Agent choices** such as scope, cost, privacy, safety, publication preference, finality, or missing user-held source.
7. **Record the Decision Record and handoff** with verdict, action, rationale, evidence, rejected alternatives, consequences, actor, timestamp, next Workflow Stage, pause, or blocker.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the constraints, references, and user request, then execute the plan.

## Reference Routing

Read first:

- `references/isomer-research-contract.md` for local terminology, truth-source, runtime-boundary, and TBD-surface rules.
- `references/provenance.md` when source provenance or license context matters.

Read references as needed:

- `references/strategic-decision-record.md` when a route-changing Decision Record needs a durable structure.
- `references/route-criteria.md` when choosing among Research Branches, candidate packages, experiments, paper routes, or blockers.
- `references/canonical-actions.md` when translating the route outcome into the smallest valid next action.
- `references/checkpoint-resume-template.md` when the decision changes the authoritative resume point.
- `references/operational-guidance.md` when user input, baseline reuse, paper-route stop-loss, or algorithm-first frontier judgment matters.

## Entry Signals

- Durable evidence needs a go, stop, branch, reuse-comparator, write, finalize, reset, Gate, or blocker judgment.
- The board is clear enough to decide, or intake can be routed first.
- A user-facing or operator-facing choice needs rationale and consequences.

## Exit Criteria

- Verdict, rationale, evidence, rejected alternatives, consequences, actor, and timestamp are recorded.
- Any true user preference, scope, cost, safety, privacy, or finality choice is represented as a Gate.
- The next Workflow Stage, pause, or blocker is explicit.
- The route does not need later stages to guess what was decided or why.

## Durable Outputs

- Decision Record.
- Optional Gate and user-facing milestone.
- Next Workflow Stage, pause, or blocker.
- Optional checkpoint or resume packet when the authoritative active node changes.

## Guardrails

- Do not repeat a decision without new evidence.
- Do not hide a blocker behind vague continuation.
- Do not choose finalization unless closure criteria are satisfied.
- Do not choose among candidate packages without naming the winner, rejected alternatives, and criteria.
- Do not launch follow-up analysis unless the expected information gain justifies the cost.
- For paper-facing routes, stop or branch when evidence shows that novelty, evidence sufficiency, or reader value has collapsed beyond reasonable narrowing; ask the Operator Agent before executing a preference-sensitive paper stop.
- Use `[[tbd-surface:schema-decision-record]]` for unsettled decision fields.
