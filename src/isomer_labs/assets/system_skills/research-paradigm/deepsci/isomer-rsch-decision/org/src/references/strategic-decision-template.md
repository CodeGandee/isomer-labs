# Strategic Decision Template

Use this when a decision must directly guide the next stage rather than merely record a verdict.

## Recommended shape

```json
{
  "verdict": "good | neutral | bad | blocked",
  "action": "launch_experiment | launch_analysis_campaign | activate_branch | write | finalize | stop | ...",
  "reason": "Concrete evidence-backed reason.",
  "target_idea_id": "optional",
  "target_run_id": "optional",
  "campaign_id": "optional",
  "reflection": {
    "what_worked": "Durable evidence-backed successes.",
    "what_failed": "Specific failures and why they matter.",
    "learned_constraints": "New boundaries learned from the evidence."
  },
  "next_direction": {
    "objective": "Immediate strategic goal.",
    "key_steps": ["Concrete next step 1", "Concrete next step 2"],
    "success_criteria": ["Observable success threshold"],
    "abandonment_criteria": ["Explicit stop condition"]
  }
}
```

## Use cases

This richer structure is most helpful for:

- choosing among idea candidates
- selecting experiment groups
- launching an analysis campaign
- routing after campaign or run results
- deciding to pivot, reset, write, or finalize
