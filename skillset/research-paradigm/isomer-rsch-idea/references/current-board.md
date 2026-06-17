# Current Board Packet

Use this reference before widening the idea frontier. The goal is to compress the currently relevant durable state into one board surface so ideation does not continue from stale Research Branches, stale narratives, or stale blockers.

## Minimal Fields

- `incumbent`: the current strongest line or comparator.
- `current_mainline`: the route that new candidates should be compared against.
- `latest_decisive_result`: the most recent Evidence Item or Run that changed route quality.
- `strongest_negative_evidence`: the clearest reason the current line may be wrong or incomplete.
- `active_blocker`: the current gating problem.
- `stale_routes_to_ignore`: routes that should not be reopened without new evidence.
- `next_decision_scope`: whether ideation is choosing a mechanism, objective, measurement, or infrastructure route.
- `budget_class`: cheap-to-check or expensive-to-check route class.

## Questions to Answer

1. What is the current mainline?
2. Which result changed the route most recently?
3. What is the strongest reason to distrust the current mainline?
4. Which old routes should stay closed unless new evidence appears?
5. Is the next step about mechanism choice, objective correction, evaluator repair, or infrastructure?
6. Is this a cheap-falsification pass or an expensive-validation pass?

## Template

```md
# Current Board Packet

- incumbent:
- current_mainline:
- latest_decisive_result:
- strongest_negative_evidence:
- active_blocker:
- stale_routes_to_ignore:
- next_decision_scope:
- budget_class:
```

## Exit Rule

If this packet cannot be made coherent, do not widen the frontier. Route through `isomer-rsch-decision` or `isomer-rsch-intake` first.
