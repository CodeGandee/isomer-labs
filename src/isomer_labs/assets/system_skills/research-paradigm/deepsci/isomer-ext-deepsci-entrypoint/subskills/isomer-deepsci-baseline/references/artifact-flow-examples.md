# Baseline Evidence Flow Examples

Use this reference when the baseline route is clear but the exact durable evidence sequence is not. The examples preserve the source flow while replacing source harness calls with native Isomer evidence records. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Choose the flow**. Decide whether the route is attach, import, verify-local-existing, reproduce, repair, publish, waive, or block.
2. **Materialize and inspect evidence**. Record package, path, service, outputs, provenance, and metric contract before acceptance.
3. **Verify only what trust requires**. Run or inspect the minimum evidence needed for the acceptance target.
4. **Write the comparison contract**. Ensure DEEPSCI:COMPARABILITY-CONTRACT exists before acceptance.
5. **Close gate explicitly**. Produce DEEPSCI:ACCEPTED-BASELINE-RECORD, DEEPSCI:BASELINE-WAIVER-RECORD, or DEEPSCI:BASELINE-BLOCKER-RECORD.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer reuse when registry or package evidence is trustworthy (if output and contract are traceable, otherwise verify).
- Prefer import when the user already provides a prepared package or snapshot (if provenance is durable, otherwise block or verify).
- Prefer local-existing verification when it is cheaper and more faithful than clean reproduction (if split, metric, and command are clear, otherwise audit).
- Prefer publishing only after the local gate is already trusted (if verification is incomplete, otherwise do not publish).
- Prefer waiver only when the route genuinely must continue without comparator trust (if the route is merely inconvenient, otherwise continue verification or block).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- Attach, import, or publish alone must not open the gate.
- DEEPSCI:COMPARABILITY-CONTRACT must precede acceptance.
- Attached or imported packages require durable provenance.
- Published baseline material must not be half-verified.
- Waiver must record what was tried, what remains missing, and why continuation is justified.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Contract-before-acceptance coverage: fraction of acceptance, import, verify, publish, or waiver flows where DEEPSCI:COMPARABILITY-CONTRACT exists before accepted closeout; higher is better.
- Incomplete-trust closeout count: number of attach, import, publish, or waiver flows treated as accepted before verification, provenance, metric contract, and caveats are durable; lower is better.

### Checks

- Flow gate: selected flow matches route and acceptance target.
- Evidence gate: outputs, provenance, metrics, and package or service identity are inspected.
- Verification gate: minimum evidence needed for trust is collected.
- Contract gate: DEEPSCI:COMPARABILITY-CONTRACT exists.
- Closeout gate: acceptance, waiver, blocker, or route decision is durable.

## Examples

### Reuse an Existing Registry Baseline

1. Attach or materialize the reusable baseline.
2. Inspect package, outputs, provenance, and metric contract.
3. Run only minimum extra verification needed for current trust.
4. Produce or reuse DEEPSCI:COMPARABILITY-CONTRACT.
5. Produce DEEPSCI:ACCEPTED-BASELINE-RECORD.

### Import a Local Package or Bundle

1. Materialize the imported package under the Topic Workspace baseline surface.
2. Preserve DEEPSCI:BASELINE-PROVENANCE-RECORD.
3. Inspect outputs, metrics, and provenance.
4. Produce or reuse DEEPSCI:COMPARABILITY-CONTRACT.
5. Produce DEEPSCI:ACCEPTED-BASELINE-RECORD or DEEPSCI:BASELINE-BLOCKER-RECORD.

### Verify a Local-Existing Comparator

1. Identify the user-provided comparator location or endpoint.
2. Identify the real evaluation command or endpoint.
3. Verify outputs or metrics under the intended contract.
4. Produce DEEPSCI:COMPARABILITY-CONTRACT.
5. Produce DEEPSCI:ACCEPTED-BASELINE-RECORD.

### Publish a Reusable Baseline

1. Finish verification first.
2. Ensure provenance, caveats, and metrics are trustworthy.
3. Accept the current gate if unresolved.
4. Publish only after trust is established.

### Waive the Baseline Gate

1. Record why the gate cannot be cleared now.
2. Record what was tried and what remains missing.
3. Produce DEEPSCI:BASELINE-WAIVER-RECORD with the next route.
