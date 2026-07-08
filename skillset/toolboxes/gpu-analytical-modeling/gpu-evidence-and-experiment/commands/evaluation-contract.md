# Evaluation Contract

## Workflow

When evaluation is planned or audited, execute the following steps in order.

1. **Name predicted outputs**. Include runtime, throughput, counter trends, saturated component, blocking path, or any subset actually claimed.
2. **Define metrics and thresholds**. State MAPE, max error, within-threshold rate, trend agreement, component accuracy, path agreement, or other metrics before interpreting results.
3. **Separate data roles**. Keep calibration, validation, and query inputs disjoint unless a deviation is explicitly recorded.
4. **State fair-comparison rules**. Fix hardware, clock assumptions, kernel version, input-shape generation, precision, and measurement method.
5. **Require predicted-versus-measured latency for latency claims**. For any analytical model that predicts latency or runtime, report predicted latency, measured latency, workload and hardware scope, metric definition, and evidence class together before making latency-accuracy claims.
6. **Declare evidence classes**. Identify whether each result comes from real hardware, profiler counters, microbenchmarks, simulator, emulator, synthetic data, derivation-only evidence, or analytical proxy.
7. **Block proxy substitution**. Do not let emulator, simulator, synthetic, analytical-proxy, or derivation-only evidence substitute for measured latency when claiming measured hardware accuracy.
8. **Block overclaiming**. If the result lacks evidence for a central claim, downgrade the claim or route to more evidence.

If the user's task does not map cleanly to these steps, use your native planning tool to build an evaluation plan from the available model outputs, metrics, evidence classes, and claim boundaries, then execute the plan. If an evaluation contract already exists, refresh only the missing or stale parts.

## Required Outputs

- Predicted outputs.
- Primary and secondary metrics.
- Calibration, validation, and query split.
- Fair-comparison rules.
- Predicted latency, measured latency, workload scope, hardware scope, metric definition, and evidence class for latency-accuracy claims.
- Evidence classes and caveats.
- Acceptance, partial-support, or blocker criteria.

## Common Mistakes

- Changing thresholds after seeing results.
- Using the target input runtime as a model input.
- Treating a proxy system as held-out silicon validation.
- Reporting model error without saying what latency was predicted, what latency was measured, and what measurement scope produced the comparison.
