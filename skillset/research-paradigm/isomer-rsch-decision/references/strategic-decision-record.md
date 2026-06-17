# Strategic Decision Record

Use this reference when a route-changing decision needs more than a one-line verdict.

## Minimum Fields

- route question:
- verdict: good | neutral | bad | blocked
- chosen action:
- rationale:
- evidence:
- strongest support:
- strongest contradiction:
- main risk:
- main cost:
- rejected alternatives:
- consequences:
- actor:
- timestamp or run context:
- next Workflow Stage, pause, or blocker:

## Structured Shape

```json
{
  "kind": "decision_record",
  "route_question": "",
  "verdict": "good | neutral | bad | blocked",
  "action": "continue | launch_experiment | launch_analysis | branch | reuse_baseline | write | review | finalize | iterate | reset | stop | request_operator_gate",
  "reason": "Concrete evidence-backed reason.",
  "evidence_items": [],
  "rejected_alternatives": [],
  "reflection": {
    "what_worked": "",
    "what_failed": "",
    "learned_constraints": ""
  },
  "next_direction": {
    "objective": "",
    "key_steps": [],
    "success_criteria": [],
    "abandonment_criteria": []
  }
}
```

## Use Cases

This structure is most helpful for choosing among idea candidates, selecting experiment groups, launching follow-up analysis, routing after Run results, deciding to pivot or reset, deciding to write or review, and deciding to finalize or stop.

If the concrete Decision Record schema matters, use `[[tbd-surface:schema-decision-record]]`.
