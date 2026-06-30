# Canonical Actions

Use this reference to apply a stable action vocabulary so downstream stages know what changed. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **List eligible actions**. Consider `continue`, `launch_experiment`, `launch_analysis_campaign`, `branch`, `prepare_branch`, `activate_branch`, `reuse_baseline`, `attach_baseline`, `publish_baseline`, `write`, `review`, `finalize`, `iterate`, `reset`, `stop`, and `request_user_decision`.
2. **Match action to state**. Choose the smallest action that genuinely resolves the current route question.
3. **Check special routes**. Apply baseline reuse, paper-route, algorithm-first, branch, stop, and user-decision rules when the action touches those surfaces.
4. **Record rejected actions**. Name the serious alternatives and why they lost.

## Preferences

- Prefer the smallest canonical action that changes the route correctly (if a richer action is tempting, otherwise justify why the smaller action is insufficient).
- Prefer continuing automatically when durable evidence makes the next action obvious (if the choice is preference-sensitive, otherwise request the user decision).
- Prefer `reuse_baseline` or `attach_baseline` only when the concrete attachment and confirmation path is clear.

## Constraints

- The selected action must match the actual durable state, not the desired state.
- `launch_analysis_campaign` must not be selected unless expected information gain justifies the cost.
- `finalize` must not be selected for a paper line unless submission readiness is durable.
- A stop decision for low paper quality must ask the user when publication, scope, cost, or non-paper preferences materially affect the choice.

## Quality Gates

- Action fit: the chosen action resolves the route question with no larger move than necessary.
- Alternative visibility: main rejected actions and decisive reasons are recorded.
- Downstream clarity: the next v2 skill or blocker can act from <ROUTE_DECISION_RECORD>.
- Special-route compliance: baseline, paper, optimization, branch, and user-sensitive routes satisfy their extra rules.
