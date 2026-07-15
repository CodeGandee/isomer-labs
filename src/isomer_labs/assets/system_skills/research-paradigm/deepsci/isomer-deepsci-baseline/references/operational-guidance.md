# Operational Guidance

Use this reference to keep comparator work bounded and evidence-first. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Choose the shortest durable route record**. Use DEEPSCI:BASELINE-ROUTE-PLAN and DEEPSCI:BASELINE-GATE-CHECKLIST when the route is non-trivial, code-touching, expensive, unstable, long-running, reuse-facing, or ambiguous; otherwise keep a compact record.
2. **Preserve provenance for attach or import**. Record DEEPSCI:BASELINE-PROVENANCE-RECORD for package identity, attachment metadata, source identity, outputs, metrics, and caveats.
3. **Use faithful execution tactics**. Choose the execution route that is most faithful, observable, and efficient while preserving verification gates; use source audit only when needed.
4. **Handle environment tactically**. Prefer a reproducible isolated environment, but follow the source package or repository's native route when it is more faithful to comparable evidence.
5. **Use memory selectively**. Check Workspace Runtime memory when resuming blocked or ambiguous routes, repeated failure patterns, or accepted caveats may affect trust; preserve reusable baseline lessons before exit.
6. **Stop once target is satisfied**. Once comparison-ready baseline is durably accepted, stop unless one named unresolved comparison risk remains.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer compact durable records for fast attach, import, or local verification (if the route is complex, otherwise use the plan and checklist templates).
- Prefer source paper and repository reading only when reproduction or repair is active (if reuse or local verification is enough, otherwise avoid broad audit).
- Prefer bounded smoke only when command path, environment viability, evaluator wiring, or output schema is unclear (if the path is concrete, otherwise verify directly).
- Prefer repo-native environment setup when it is more faithful than a generic isolated route (if the source has no stronger route, otherwise use the project default).
- Prefer memory only when it avoids repeated work or clarifies stale route state (if the route is fast and clear, otherwise skip it).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- Durable route records are required in substance, not in fixed filenames.
- DEEPSCI:BASELINE-PROVENANCE-RECORD is required for attached or imported baselines.
- DEEPSCI:COMPARABILITY-CONTRACT is required for accepted baselines.
- Reuse or publish must not proceed while verification is incomplete, metrics are untrusted, or provenance is weak.
- Environment details should record facts that affect trust or comparability, not incidental setup noise.
- Repeated unchanged checks must not continue without new evidence, code change, environment change, or route change.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Unchanged retry count: number of repeated validation or reproduction attempts run without new evidence, code change, environment change, or route change; lower is better.
- Smoke budget fit: number of smoke or pilot checks used before the route has evidence; closer to the source 0-2 default budget is better.

### Checks

- Route-record gate: chosen route, acceptance target, comparator identity, command or evaluation path, expected outputs, acceptance condition, blocker or fallback, and verification verdict are recoverable.
- Provenance gate: attached or imported package identity, source, outputs, metrics, and caveats are durable.
- Execution gate: smoke, direct verification, reproduce, or repair route is justified by uncertainty and trust need.
- Environment gate: environment facts that affect comparability are recorded.
- Reuse gate: reusable baseline material is published or shared only after trust and verification are complete.
- Stop gate: no extra baseline work continues after the acceptance target is satisfied without a named comparison risk.
