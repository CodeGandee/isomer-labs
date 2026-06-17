---
name: isomer-rsch-decision
description: Make one explicit research route judgment from durable evidence and record the smallest valid next action.
---

Use this skill when evidence needs a go, stop, branch, reuse-comparator,
write, finalize, reset, Gate, or blocker decision.

Read first:

- `../isomer-rsch-shared/SKILL.md`
- Source analysis: `../../../context/explore/deepscientist-skill-analysis/decision.md`

## Entry Signals

- Durable evidence needs a go, stop, branch, reuse-comparator, write, finalize,
  reset, Gate, or blocker judgment.
- The board is clear enough to decide, or intake can be routed first.
- A user-facing or operator-facing choice needs rationale and consequences.

## Exit Criteria

- Verdict, rationale, evidence, rejected alternatives, consequences, actor, and
  timestamp are recorded.
- Any true user preference, scope, cost, safety, privacy, or finality choice is
  represented as a Gate.
- The next Workflow Stage, pause, or blocker is explicit.

## Procedure

1. Check whether the board is clear enough to judge; route to intake if not.
2. State the exact route decision being made.
3. Gather only evidence that can change the decision.
4. Compare winning action, rejected alternatives, strongest support,
   strongest contradiction, cost, risk, and changed facts.
5. Open a Gate only for true user preference, scope, cost, safety, privacy, or
   finality choices.
6. Record verdict, rationale, evidence, rejected alternatives, consequences,
   actor, timestamp, and next stage.

## Durable Outputs

- Decision Record.
- Optional Gate and user-facing milestone.
- Next Workflow Stage, pause, or blocker.

## Guardrails

- Do not repeat a decision without new evidence.
- Do not hide a blocker behind vague continuation.
- Do not choose finalization unless closure criteria are satisfied.
- Use `[[tbd-surface:schema-decision-record]]` for unsettled decision fields.
