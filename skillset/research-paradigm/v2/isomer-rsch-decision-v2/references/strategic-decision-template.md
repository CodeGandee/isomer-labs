# Strategic Decision Template

Use this when a decision must directly guide the next stage rather than merely record a verdict. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Write the verdict**. Mark the decision as good, neutral, bad, blocked, or another project-approved verdict label.
2. **Choose the action**. Select the smallest canonical action and the next route or next direction.
3. **State the evidence-backed reason**. Explain the decisive reason with evidence pointers, support, contradiction, cost, risk, and rejected alternatives.
4. **Record targets when needed**. Include target idea, run, branch, paper route, campaign, comparator, or blocker identifiers only when they affect the next route.
5. **Capture reflection**. Record what worked, what failed, learned constraints, and residual risk when the decision changes future routing.
6. **Define next direction**. State immediate objective, concrete steps, success criteria, abandonment criteria, and handoff route.

## Preferences

- Prefer a compact structured decision over loose prose (if the decision is minor, otherwise keep only fields that affect routing).
- Prefer conclusion-first verdict and action before rationale.
- Prefer evidence pointers over broad summaries when downstream work must inspect the source.

## Constraints

- <ROUTE_DECISION_RECORD> must include verdict, action, reason, evidence basis, rejected alternatives or blocker, and next route.
- The decision record must not repeat the same decision without new evidence.
- A consequential decision must not omit the decisive reason or main rejected alternative.
- The record must make the next stage or next action explicit.

## Quality Gates

- Record completeness: verdict, action, reason, evidence, rejected alternatives, and next route are present.
- Decision traceability: a later v2 skill can inspect the evidence basis without guessing.
- Action consistency: the action matches the actual state and canonical action set.
- Handoff clarity: the record makes the next route operational.
