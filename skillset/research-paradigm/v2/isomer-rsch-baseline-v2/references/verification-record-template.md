# Verification Record Template

Use this reference to capture baseline evidence before acceptance. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **State the route and comparator**. Record acceptance target, route, baseline id, variant, comparator identity, source identity, command, endpoint, trusted-output path, package, or registry record.
2. **Verify real evidence**. Confirm the run, service call, package import, trusted-output inspection, or source record actually exists and corresponds to the intended comparator.
3. **Verify data and metrics**. Check intended dataset, split, metric definitions, metric directions, required metric ids, metric values, and output pointers.
4. **Record environment and deviations**. Capture environment or hardware facts that affect comparability, plus implementation, data, split, metric, evaluation, source, or package deviations.
5. **Classify the verdict**. Label verified match, verified close, verified diverged, trusted with caveats, broken, waived, or blocked.
6. **Block honestly when needed**. If evidence is incomplete, record <BASELINE_BLOCKER_RECORD> instead of accepting.

## Preferences

- Prefer objective evidence over paper-table copying (if the acceptance target requires local verification, otherwise treat copied numbers as insufficient).
- Prefer real verification over attach/import ceremony (if the package is attached or imported, otherwise inspect outputs, provenance, and metrics).
- Prefer direct verification when the path is concrete (if command path or schema is uncertain, otherwise use a bounded smoke check).
- Prefer recording failure class and next move over repeated unchanged retries (if new evidence or route changes exist, otherwise continue once).

## Constraints

- <BASELINE_VERIFICATION_EVIDENCE> must trace metrics or outputs to real files, logs, service responses, source artifacts, registry records, or package records.
- Attach, import, or publish must not count as acceptance without verification.
- Fabricated, copied, paraphrased, or weak-provenance metrics must not be accepted.
- A completed local run must not be accepted if it used a materially different protocol without a recorded caveat.
- Verification must separate likely implementation mismatch, environment mismatch, data or split mismatch, stochastic variance, and unexplained divergence when those distinctions matter.

## Quality Gates

- Evidence gate: trusted metrics or outputs are traceable to real evidence.
- Dataset gate: intended dataset and split are checked.
- Metric gate: metric definitions, metric directions, required ids, and values are checked.
- Source gate: comparator source, package, service, or registry identity is stable.
- Deviation gate: known deviations and caveats are recorded.
- Verdict gate: acceptance, waiver, blocker, or route change follows from the evidence.

## Template

### Route

- acceptance target:
- route:
- baseline id:
- baseline variant:
- comparator identity:
- source identity:

### Evidence

- command, endpoint, package, source, registry, or trusted-output path:
- output pointers:
- metric values:
- required metric ids and directions:
- dataset and split:
- environment facts:
- deviations:

### Verdict

- verification verdict:
- caveats:
- acceptance, waiver, blocker, or route decision:
- next action:
