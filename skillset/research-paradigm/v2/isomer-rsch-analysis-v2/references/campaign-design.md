# Campaign Design

Use this reference to design the smallest analysis campaign that can change a parent claim or route. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Name the parent boundary**. State the parent object, parent claim or gap, evidence question, comparison target, and stop condition in <ANALYSIS_CONTEXT_BRIEF>.
2. **Choose the route shape**. Select analysis-lite, artifact-backed campaign, writing-facing campaign, review or rebuttal campaign, or failure-analysis route based on traceability, lineage, paper utility, and slice count.
3. **Audit the real envelope**. Record current devices, memory, storage, wall-clock, dependencies, credentials, services, queue, and concurrency constraints in <ANALYSIS_RESOURCE_ENVELOPE>.
4. **Prioritize by soundness gain**. Rank claim-critical contradiction checks first, then robustness or sensitivity checks, failure-mode explanation, and efficiency or secondary support.
5. **Screen candidate slices**. Tag each candidate as runnable now, runnable with downscope, or blocked by resources; replace infeasible high-value slices with honest proxies only when the proxy still answers the question.
6. **Finalize the smallest frontier**. Create <ANALYSIS_SLICE_PLAN> with slice class, evidence question, fixed conditions, metric or observable, priority, expected output, and stop condition.

## Preferences

- Prefer the smallest slice set that can change the evidence boundary (if more slices would only add polish, otherwise stop).
- Prefer claim-carrying and contradiction slices before supporting slices (if the main claim is already credible, otherwise broaden confidence only after the core boundary is stable).
- Prefer slices runnable under the current envelope (if a blocked high-value slice matters, otherwise record the blocker and choose a lower-cost alternative).
- Prefer writing-facing slices only when write-back metadata is available or recoverable (if no selected outline exists, otherwise mark the slice as pre-outline analysis).

## Constraints

- <ANALYSIS_SLICE_PLAN> must not include slices that lack a parent claim, parent result, paper gap, reviewer item, rebuttal item, or route decision.
- Campaign scope must not assume hardware, memory, storage, runtime, services, or credentials that are not actually available.
- Infeasible slices must be downscoped, replaced, deferred with a blocker, or dropped explicitly.
- A slice frontier must not keep widening after the next route is already clear.

## Quality Gates

### Metrics

- Priority-tier coverage: number of source priority tiers considered across claim-critical contradiction, robustness or sensitivity, failure-mode explanation, and efficiency or secondary support; higher is better until all relevant tiers are considered.
- Resource-budget fit: expected wall-clock and compute demand of the selected slice set relative to the current execution envelope; lower is better when evidence value is preserved.

### Checks

- Boundary gate: parent object, evidence question, comparison target, and stop condition are explicit.
- Route-shape gate: the selected analysis route matches the required traceability and slice count.
- Resource gate: candidate slices are screened against the actual execution envelope.
- Priority gate: claim-critical, robustness, failure, and support slices are ordered by decision value per cost.
- Frontier gate: <ANALYSIS_SLICE_PLAN> contains only slices that can change, confirm, narrow, or block the parent evidence boundary.
