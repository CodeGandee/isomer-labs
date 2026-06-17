# Main Experiment Checklist

Use this checklist while planning, modifying code, running pilots, monitoring the main Run, and validating the result. For a lightweight Run, keep only the core planning, validation, and closeout items active.

```md
# Main Experiment Checklist

## Identity

- parent_stage_or_decision:
- loop_id:
- run_id:
- route_id:
- stage:

## In Progress

- [ ] one concrete experiment frontier item is actively in progress

## Next

- [ ] next code, Run, or validation step is explicit
- [ ] next route transition is explicit
- [ ] next reporting checkpoint is explicit

## Later

- [ ] deferred but still relevant items live here

## Blocked

- [ ] blockers or unresolved dependencies are recorded here

## Planning

- [ ] selected route summarized in one or two sentences
- [ ] comparator and comparability contract confirmed
- [ ] code touchpoints listed
- [ ] smoke plan written when needed
- [ ] full Run plan written
- [ ] fallback options written

## Implementation

- [ ] intended files modified
- [ ] unrelated changes avoided or justified
- [ ] risky logic guarded or sanity-checked
- [ ] plan updated if implementation route changed

## Pilot or Smoke

- [ ] smoke command or adapter call executed when needed
- [ ] outputs look valid
- [ ] metrics and logs are interpretable
- [ ] comparability still holds

## Main Run

- [ ] real Run launched
- [ ] health signals confirmed when monitoring is needed
- [ ] major runtime deviations reflected in the plan

## Validation

- [ ] outputs exist
- [ ] metrics are complete
- [ ] comparator delta is comparable
- [ ] main claim is classified as supported, refuted, or inconclusive
- [ ] result recorded durably

## Done

- [ ] completed frontier items are moved here instead of staying mixed into Next

## Closeout

- [ ] main experiment summarized in one or two sentences
- [ ] next action is explicit
```

## Checklist Rule

The checklist should show one real in-progress item and a short next list. If it becomes a parking lot, rewrite it before continuing.
