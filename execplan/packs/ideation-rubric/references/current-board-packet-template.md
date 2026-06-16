# Current Board Packet Template

Use this reference before widening the idea frontier.

The goal is to compress all currently relevant durable state into one board surface so ideation does not continue from stale branches, stale narratives, or stale blockers.

## Minimal fields

- `incumbent`
  - the current strongest line
- `current_mainline`
  - the route that should be treated as active now
- `latest_decisive_result`
  - the most recent result that actually changed route quality
- `strongest_negative_evidence`
  - the clearest recent reason the current line may be wrong or incomplete
- `active_blocker`
  - the current gating problem
- `stale_routes_to_ignore`
  - routes that should not be reopened by default
- `next_decision_scope`
  - what kind of choice ideation is actually making now
- `budget_class`
  - cheap-to-check vs expensive-to-check route class

## Questions to answer

1. What is the current mainline, really?
2. Which result changed the route most recently?
3. What is the strongest reason to distrust the current mainline?
4. Which old routes should not be reopened unless new evidence appears?
5. Is the next step about mechanism choice, objective correction, evaluator repair, or infrastructure?
6. Is this a cheap-falsification pass or an expensive-validation pass?

## Example shape

```md
# Current Board Packet

- incumbent:
  - current best durable line
- current_mainline:
  - the route that new candidates should be compared against
- latest_decisive_result:
  - the last result that changed route quality materially
- strongest_negative_evidence:
  - the strongest observed reason the current line may still be wrong
- active_blocker:
  - the specific thing preventing clean progress now
- stale_routes_to_ignore:
  - old routes that should not be reopened by default
- next_decision_scope:
  - mechanism / objective / measurement / infrastructure
- budget_class:
  - fast-check or slow-check
```

## Exit rule

If this packet cannot be made coherent, do not widen the frontier yet.
Route through `decision` or `intake-audit` first.
