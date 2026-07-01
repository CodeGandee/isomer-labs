# Current Board Packet Template

Use this reference before widening the idea frontier. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Recover the incumbent**. Identify the current strongest line, current mainline, and comparator basis from durable evidence.
2. **Name decisive evidence**. Record the latest result that changed route quality, the strongest negative evidence, and any active blocker.
3. **Mark stale routes**. List routes that should not be reopened unless new evidence weakens the current mainline.
4. **Set decision scope and budget class**. Classify whether this pass is choosing a mechanism, objective, measurement, or infrastructure route, and whether validation is `fast-check` or `slow-check`.
5. **Gate widening**. If the packet cannot be made coherent, produce <IDEA_BLOCKER_RECORD> and route to decision, intake audit, scout, or baseline instead of generating candidates.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer the current research head as the default foundation (if durable evidence identifies a stronger recent measured branch, otherwise record why the default foundation changed).
- Prefer a compact single board surface over scattered status notes (if several records conflict, otherwise reconcile them before ideation).
- Prefer `fast-check` candidates with cheap orthogonal falsification paths (if validation is slow, otherwise keep the serious frontier tighter).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- <CURRENT_BOARD_PACKET> must include incumbent, current mainline, latest decisive result, strongest negative evidence, active blocker, stale routes, next decision scope, and budget class.
- The idea pass must not reopen stale routes without new evidence.
- The idea pass must not continue from an incoherent board state.
- The board packet should identify whether the next route is about mechanism, objective, measurement, or infrastructure.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Board-question coverage: fraction of current mainline, route-changing result, distrust reason, do-not-reopen route, mechanism/objective/evaluator/infrastructure focus, and budget-class questions answered; higher is better.
- Stale-route ambiguity count: number of old routes that might be reopened without new evidence because the packet lacks a do-not-reopen note; lower is better.

### Checks

- Incumbent clarity: the packet identifies what each candidate must beat or replace.
- Staleness control: routes to ignore are explicit enough to prevent rediscovery of rejected work.
- Decision scope: the packet makes the current decision type visible before candidate generation.
- Budget fit: the frontier width can be justified from `fast-check` or `slow-check` validation cost.
