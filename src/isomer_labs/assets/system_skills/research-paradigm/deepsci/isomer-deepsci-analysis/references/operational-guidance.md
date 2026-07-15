# Operational Guidance

Use this reference to run analysis work without turning it into an unbounded campaign. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Select the durable evidence route**. Use a light durable report for one bounded answer, or a campaign lineage route when multiple slices, branch isolation, reviewability, writing traceability, or later replay matter.
2. **Verify executable slices before launch**. Confirm assets, comparators, dependencies, services, credentials, runtime, and workspace needs before committing to DEEPSCI:ANALYSIS-CAMPAIGN-PLAN.
3. **Use faithful execution tactics**. Choose direct verification, a bounded smoke check, or a real slice run based on command uncertainty, output uncertainty, metric-path uncertainty, and evidence value.
4. **Monitor long-running slices through durable signals**. Use managed Execution Adapter sessions, durable logs, stall signals, and structured progress markers when runtime is long or uncertain.
5. **Record every launched slice promptly**. After each slice completes, fails, becomes infeasible, or is superseded, update DEEPSCI:ANALYSIS-SLICE-RECORD and the campaign frontier before summarizing.
6. **Use memory selectively**. Check Workspace Runtime memory when resuming, reopening old command paths, repeated failures, prior slice outcomes, or comparability caveats may affect the route; preserve reusable campaign lessons before exit.
7. **Keep connector-facing visuals restrained**. If the campaign produces milestone visuals, show the main boundary change clearly, use restrained project palettes, and do not decorate every slice equally.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer the shortest durable route that preserves trust and auditability (if lineage or write-back matters, otherwise use a campaign object).
- Prefer direct verification when the path is concrete (if command or evaluator wiring is uncertain, otherwise use a bounded smoke check).
- Prefer one decisive runnable slice over several speculative expensive slices (if resources are tight, otherwise prioritize soundness gain per cost).
- Prefer recording non-success slices immediately (if a replacement slice is launched, otherwise keep the original blocker visible).
- Prefer memory only for repeated-failure avoidance or reusable lessons (if it is just a run record, otherwise keep it in the evidence record).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- DEEPSCI:ANALYSIS-CAMPAIGN-PLAN must not launch slices before assets, comparators, dependencies, and current runtime feasibility are checked or blockers are recorded.
- Long-running execution should preserve durable logs and monitoring state.
- If a slice is invalid, wedged, unsupported by the environment, or superseded, it should be stopped or marked honestly before replacement.
- Repeated failure with no route, evidence, environment, or design change should route through decision, redesign, experiment, or blocker rather than widening silently.
- Connector-facing charts must not imply stronger evidence than the slice records support.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Smoke budget fit: number of smoke checks used when command, output, metric path, or evaluator wiring is uncertain; closer to the source 0-2 default budget is better.
- Repeated-failure count: number of repeated slice failures with the same failure class and no new evidence or route change; lower is better.

### Checks

- Route gate: the chosen durable evidence route matches slice count, lineage, reviewability, and write-back needs.
- Resource gate: DEEPSCI:ANALYSIS-RESOURCE-ENVELOPE covers machine class, memory, storage, wall-clock, concurrency, services, credentials, dependencies, and infeasible slices when relevant.
- Execution gate: smoke, direct verification, or real run choice is justified by the uncertainty and evidence value.
- Recording gate: every launched, failed, infeasible, partial, or superseded slice has an DEEPSCI:ANALYSIS-SLICE-RECORD.
- Continuity gate: reusable lessons, comparability caveats, and route-changing outcomes are preserved in DEEPSCI:ANALYSIS-CONTINUITY-UPDATE.
- Visual gate: any connector-facing chart highlights the boundary change and stays aligned with the project visual language.
