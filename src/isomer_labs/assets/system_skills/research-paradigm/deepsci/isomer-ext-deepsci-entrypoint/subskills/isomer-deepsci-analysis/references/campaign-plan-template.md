# Analysis Campaign Plan Template

Use this reference when a durable campaign record would reduce ambiguity. It is a template, not a required filename. For analysis-lite, keep only the objective, first slice, evidence boundary, and next route. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **State the objective**. Record parent object, parent claim or gap, evidence question, success condition, stop or abandonment condition, and routes on support, contradiction, or blocker.
2. **State the comparability boundary**. Record the baseline or main comparison contract, fixed conditions, variables that may change, direct-comparison limits, and non-comparable slices to label explicitly.
3. **Define the slice frontier**. List slice id, slice class, evidence question, intervention or inspection target, metric or observable, priority, and paper or review role.
4. **List assets and dependencies**. Identify available assets, checkpoints, comparators, missing dependencies or credentials, and fallback if unavailable.
5. **Record the execution envelope**. Capture available machine class, memory, storage, wall-clock, concurrency, environment risk, and slices infeasible unless downscoped.
6. **Choose the execution path**. Decide whether lineage is needed, where the work happens, how to smoke or directly verify, expected outputs, and monitoring plan.
7. **Define interpretation and write-back**. State what counts as support, partial support, contradiction, unresolved ambiguity, and what paper, review, or route targets must be updated.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer a compact DEEPSCI:ANALYSIS-CAMPAIGN-PLAN for analysis-lite (if a multi-slice or writing-facing path is active, otherwise use the full template).
- Prefer frontier rows that make the decision value visible (if a slice has no decision value, otherwise drop or defer it).
- Prefer recording non-comparable slices before execution (if the difference is the point, otherwise state the label).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- DEEPSCI:ANALYSIS-CAMPAIGN-PLAN must not list planned slices as evidence.
- DEEPSCI:ANALYSIS-CAMPAIGN-PLAN must record resource blockers instead of assuming ideal resources.
- Writing-facing sections should not be filled with vague notes when concrete write-back targets are needed.
- If slice feasibility, ordering, comparators, or interpretation changes materially, the plan should be revised before more compute is spent.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Slice-frontier coverage: fraction of planned slices with class, evidence question, intervention or inspection target, metric or observable, priority, and paper role recorded; higher is better.
- Interpretation-boundary coverage: fraction of stable support, partial support, contradiction, unresolved ambiguity, and stop-condition fields completed; higher is better.

### Checks

- Objective gate: parent object, evidence question, success condition, stop condition, and route outcomes are explicit.
- Comparability gate: fixed conditions, variables, direct-comparison limits, and non-comparable labels are recorded.
- Frontier gate: each slice has class, question, target, metric or observable, priority, and role.
- Resource gate: assets, dependencies, environment risks, and downscope blockers are visible.
- Interpretation gate: support, partial support, contradiction, ambiguity, and stop rules are defined before results are interpreted.

## Template

### 1. Objective

- parent object:
- parent claim or gap:
- evidence question:
- success condition:
- stop or abandonment condition:
- next route on support:
- next route on contradiction or blocker:

### 2. Comparability Boundary

- baseline or main comparison contract:
- fixed conditions:
- variables that may change:
- direct-comparison limits:
- non-comparable slices to label explicitly:

### 3. Slice Frontier

| Slice ID | Slice Class | Evidence Question | Intervention or Inspection Target | Metric or Observable | Priority | Paper or Review Role |
| --- | --- | --- | --- | --- | --- | --- |
| | auxiliary / claim-carrying / supporting / failure-analysis | | | | | main_text / appendix / reference_only / reviewer / none |

### 4. Assets and Dependencies

- workspace assets already available:
- checkpoints or comparators already available:
- required comparators:
- missing dependencies or credentials:
- fallback if unavailable:

### 5. Execution Envelope

- available devices or machine class:
- available memory:
- available storage:
- wall-clock budget:
- concurrency or queue limits:
- environment or dependency risk:
- slices that are infeasible unless downscoped:

### 6. Execution Choice

- campaign lineage needed:
- working location:
- environment or service route:
- smoke, direct verification, or real-run decision:
- expected outputs or evidence paths:
- monitoring plan if long-running:

### 7. Interpretation Boundary

- what counts as stable support:
- what counts as partial support:
- what counts as contradiction:
- what counts as unresolved ambiguity:
- what result stops further slices:

### 8. Paper or Review Mapping

- selected outline reference:
- paper experiment matrix or evidence ledger:
- reviewer or rebuttal item:
- write-back target:

### 9. Current Frontier

- next action:
- active blocker:
- latest evidence:
- next route:
