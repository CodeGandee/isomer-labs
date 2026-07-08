# Profiler Counter Sources

## Workflow

When profiler or counter evidence matters, execute the following steps in order.

1. **Record collection context**. In Pixi-managed Isomer projects, prefer `pixi run ncu ...` for NCU unless local evidence proves another wrapper is required; for other profiler backends, record the equivalent command shape and collection context.
2. **List raw metrics before interpretation**. Preserve raw metric names, section choices, normalization, sampling or replay mode, kernel selector, input shape, precision, run count, device, and collection status.
3. **Separate raw and derived evidence**. Keep raw counters distinct from derived dominant component, trend agreement, bottleneck labels, or path labels.
4. **Map counters conservatively**. State the counter-to-component mapping rationale and why the mapping is valid for the target hardware scope and kernel behavior.
5. **Link counters to claims**. State whether each counter supports, refutes, or leaves unresolved each runtime, counter-trend, saturated-component, or blocking-path claim.
6. **Preserve failures and gaps**. Record unavailable counters, permission issues, section errors, timeouts, wrapper failures, empty results, and alternate evidence routes.

If the user's task does not map cleanly to these steps, use your native planning tool to build a profiler-counter source plan from the available profiler backend, metric list, target hardware scope, kernel selector, and claim map, then execute the plan.

## Can Justify

- Counter trends, profiler-observed activity, raw metric evidence, derived component labels when mapping is valid, and support/refute/unresolved status for specific claims.

## Cannot Justify

- Exact component or path proof from coarse profiler labels alone.
- Measured hardware accuracy when only profiler summaries, screenshots, failed runs, or missing counters are available.

## Preserve

- Command shape, profiler backend and version when available, device, kernel selector, input shape, precision, run count, raw metric names, normalized values, mapping rationale, derived labels, failures, and caveats.
