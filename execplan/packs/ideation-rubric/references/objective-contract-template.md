# Objective Contract Template

Use this reference at the start of an `idea` pass whenever the real target might differ from the easiest available surrogate.

The goal is to prevent ideation from drifting into "optimize what is measurable" when the real objective is narrower, more fragile, or more deployment-constrained.

## Minimal fields

- `primary_objective`
  - the real target the next route should improve
- `scoreboard_metric`
  - the single metric or ranking surface the quest is actually judged by
- `trusted_proxy_metrics`
  - the proxies that are allowed to influence direction choice
- `false_progress_signals`
  - local improvements that must not be mistaken for route health
- `hard_constraints`
  - constraints that invalidate a route even if metrics improve

## Questions to answer

1. What metric or region of behavior actually matters most?
2. Which proxies are trustworthy, and why?
3. Which proxies are only convenience signals rather than real progress?
4. What kind of apparent improvement would still count as failure?
5. Which leakage, deployment, submission-time, or comparability constraints must remain inviolable?

## Example shape

```md
# Objective Contract

- primary_objective:
  - Improve the real target metric, not just the easiest averaged surrogate.
- scoreboard_metric:
  - The metric or ranking surface that actually decides whether the route is better.
- trusted_proxy_metrics:
  - Proxy A because it tracks the head of the decision surface.
  - Proxy B because it reflects the main deployment tradeoff.
- false_progress_signals:
  - Lower average loss without improvement on the real decision region.
  - Better offline score using a feature that will not exist at deployment time.
- hard_constraints:
  - No submit-time unavailable features.
  - No leakage-prone labels or post-hoc ranking information in training.
```

## Exit rule

Do not widen the frontier until this contract is explicit enough to distinguish:

- true progress
- false progress
- invalid routes
