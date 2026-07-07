# Evaluation Contract

## Workflow

When evaluation is planned or audited, execute the following steps in order.

1. **Name predicted outputs**. Include runtime, throughput, counter trends, saturated component, blocking path, or any subset actually claimed.
2. **Define metrics and thresholds**. State MAPE, max error, within-threshold rate, trend agreement, component accuracy, path agreement, or other metrics before interpreting results.
3. **Separate data roles**. Keep calibration, validation, and query inputs disjoint unless a deviation is explicitly recorded.
4. **State fair-comparison rules**. Fix hardware, clock assumptions, kernel version, input-shape generation, precision, and measurement method.
5. **Declare evidence classes**. Identify whether each result comes from real hardware, NCU counters, microbenchmarks, simulator, emulator, synthetic data, or analytical proxy.
6. **Block overclaiming**. If the result lacks evidence for a central claim, downgrade the claim or route to more evidence.

If an evaluation contract already exists, refresh only the missing or stale parts.

## Required Outputs

- Predicted outputs.
- Primary and secondary metrics.
- Calibration, validation, and query split.
- Fair-comparison rules.
- Evidence classes and caveats.
- Acceptance, partial-support, or blocker criteria.

## Common Mistakes

- Changing thresholds after seeing results.
- Using the target input runtime as a model input.
- Treating a proxy system as held-out silicon validation.
