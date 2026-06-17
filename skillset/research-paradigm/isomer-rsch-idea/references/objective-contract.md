# Objective Contract

Use this reference at the start of an idea pass whenever the real target might differ from the easiest available surrogate. The goal is to prevent ideation from drifting into optimizing what is measurable when the real objective is narrower, more fragile, or more deployment-constrained.

## Minimal Fields

- `primary_objective`: the real target the next route should improve.
- `scoreboard_metric`: the single metric or ranking surface the Research Task is actually judged by.
- `trusted_proxy_metrics`: proxies that may influence direction choice, with reasons.
- `false_progress_signals`: local improvements that must not be mistaken for route health.
- `hard_constraints`: constraints that invalidate a route even if metrics improve.
- `abandonment_conditions`: outcomes that should stop this route rather than trigger more retries.

## Questions to Answer

1. What metric, behavior region, or claim boundary matters most?
2. Which proxies are trustworthy, and why?
3. Which proxies are convenience signals rather than real progress?
4. What apparent improvement would still count as failure?
5. Which leakage, deployment, privacy, submission-time, or comparability constraints must remain inviolable?

## Template

```md
# Objective Contract

- primary_objective:
- scoreboard_metric:
- trusted_proxy_metrics:
- false_progress_signals:
- hard_constraints:
- abandonment_conditions:
```

## Exit Rule

Do not widen the candidate frontier until this contract is explicit enough to distinguish true progress, false progress, and invalid routes.
