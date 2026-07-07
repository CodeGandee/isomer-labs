# Measurement Sources

## Workflow

When measured behavior matters, execute the following steps in order.

1. **Classify the measurement source**. Distinguish full-kernel timing, microbenchmark, hardware query, profiler run, emulator output, simulator trace, and synthetic data.
2. **Preserve measurement context**. Record hardware scope, clock or mode assumptions when available, kernel selector, input shape, precision, run count, warmup or repetition policy, timing method, and command or script.
3. **Separate calibration and validation roles**. State whether the measurement trains, calibrates, validates, queries, or only debugs the model.
4. **Capture uncertainty and caveats**. Preserve variance, outliers, failed runs, profiler overhead, unsupported regimes, busy-device caveats, missing counters, and any known measurement-path repairs.
5. **Link measurement to model claims**. State whether the measurement supports, refutes, or leaves unresolved predicted latency, throughput, counter trend, saturated component, or blocking path.

If the user's task does not map cleanly to these steps, use your native planning tool to build a measurement-source plan from the measurement type, run context, data role, uncertainty, and target claim, then execute the plan.

## Can Justify

- Predicted-versus-measured latency checks, throughput checks, calibration data, validation data, isolated hardware behavior, hardware query facts, and observed claim evidence within the recorded scope.

## Cannot Justify

- Claims outside the measured workload, hardware scope, precision, clock/mode assumptions, or data role.
- Component/path proof when the measurement only records end-to-end runtime and lacks matching observations.

## Preserve

- Measurement type, hardware scope, command or script, kernel selector, input shape, precision, run count, timing method, warmup/repetition policy, calibration or validation role, raw values, summary statistic, uncertainty, failures, and caveats.
