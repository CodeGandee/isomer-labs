# Main Experiment Checklist Template

Use this reference as the live control checklist while planning, modifying code, running pilots, monitoring the full run, validating the result, and closing the route. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Create identity and frontier fields**. Record topic or workspace, route, run id, hypothesis id when available, stage, active item, next step, next route decision, and blockers.
2. **Activate only relevant sections**. Keep planning, implementation, smoke or pilot, main run, validation, and closeout items that matter for the current run; remove or defer irrelevant lightweight-run items.
3. **Update during execution**. Move items from `Next` to `In Progress` to `Done`, keep blockers explicit, and revise the next reporting checkpoint as the frontier changes.
4. **Synchronize with the plan**. When <EXPERIMENT_PLAN> changes materially, update the checklist before more code or compute work continues.
5. **Close the route**. Mark validation and closeout only after outputs, metrics, comparability, durable recording, and next action are explicit.

## Preferences

- Prefer a compact active checklist over a long stale checklist (if the run is complex, otherwise keep all relevant control sections).
- Prefer moving completed items to `Done` instead of leaving them mixed into `Next` (if historical detail matters, otherwise preserve it in the run record).
- Prefer blockers as explicit checklist items (if they prevent execution or validation, otherwise keep them as caveats).

## Constraints

- <EXPERIMENT_CHECKLIST> must keep the current active item, next step, next route, and blockers visible.
- <EXPERIMENT_CHECKLIST> should be updated before and after material implementation, smoke, main run, validation, and closeout transitions.
- Closeout must not be checked complete until the run or blocker is durably recorded and routed.

## Quality Gates

### Metrics

- Checklist completion: fraction of checklist items satisfied or explicitly marked not applicable across idea summary, baseline/comparability, execution, result, and route sections; higher is better.
- Unresolved required-item count: number of required checklist items still unchecked without a blocker, waiver, or route change; lower is better.

### Checks

- Frontier clarity: one concrete item is in progress and the next step is explicit.
- Planning coverage: selected hypothesis, comparator, code touchpoints, smoke plan, full run plan, and fallback options are checked or explicitly not needed.
- Implementation coverage: intended files, unrelated-change avoidance, risky logic guards, and route changes are tracked.
- Execution coverage: smoke, outputs, metrics, long-run health signals, and runtime deviations are tracked.
- Validation coverage: outputs, complete metrics, comparable baseline delta, claim verdict, durable record, and next action are complete before closeout.

## Template

### Identity

- topic or workspace:
- route or inquiry:
- run id:
- hypothesis id:
- stage:

### In Progress

- [ ] one concrete experiment frontier item is actively in progress

### Next

- [ ] next code, run, or validation step is explicit
- [ ] next route decision is explicit
- [ ] next reporting checkpoint is explicit

### Later

- [ ] deferred but still relevant items live here

### Blocked

- [ ] blockers or unresolved dependencies are recorded here

### Planning

- [ ] selected hypothesis summarized in `1-2` sentences
- [ ] comparator and comparability contract confirmed
- [ ] code touchpoints listed
- [ ] smoke or pilot plan written
- [ ] full run plan written
- [ ] fallback options written

### Implementation

- [ ] intended files modified
- [ ] unrelated changes avoided or justified
- [ ] risky logic guarded or sanity-checked
- [ ] plan updated if the implementation route changed

### Pilot or Smoke

- [ ] smoke command executed when needed
- [ ] outputs look valid
- [ ] metrics or logs are interpretable
- [ ] comparability still holds

### Main Run

- [ ] real run launched
- [ ] health signals confirmed when monitoring is needed
- [ ] major runtime deviations reflected in <EXPERIMENT_PLAN>

### Validation

- [ ] outputs exist
- [ ] metrics are complete
- [ ] comparator delta is comparable
- [ ] main claim is classified as supported, refuted, inconclusive, partial, or blocked
- [ ] result or blocker recorded durably

### Done

- [ ] completed frontier items are moved here instead of staying mixed into `Next`

### Closeout

- [ ] main experiment summarized in `1-2` sentences
- [ ] next action is explicit
