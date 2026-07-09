# Evaluation and Profiler Contract

Before experiment design, name predicted outputs: runtime, throughput, counter trends, saturated component, blocking path, or a narrower subset. Define metrics and thresholds before interpreting results, such as MAPE, max error, within-threshold rate, trend agreement, component accuracy, or path agreement.

Separate calibration, validation, and query inputs. Fix hardware, clock assumptions, kernel version, input-shape generation, precision, measurement method, and fair-comparison rules. For latency claims, require predicted latency, measured latency, workload scope, hardware scope, metric definition, and evidence class together.

For profiler evidence, record command shape. In Pixi-managed projects, prefer `pixi run ncu ...` over `ncu pixi run ...` unless local evidence proves another wrapper is required. Record device, kernel selector, input shape, precision, run count, raw metric names, section choices, normalization, failures, and counter-to-component mapping.

For bottleneck claims, design stressors or regimes that target one predicted component or blocking path when feasible. State the observation that would support or refute the prediction before interpreting results.
