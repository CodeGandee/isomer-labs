# Model Shape

## Workflow

When evaluating or creating a GPU analytical model, execute the following steps in order.

1. **Name model inputs and outputs**. Include workload shape, precision, kernel variant, hardware profile, and outputs such as runtime, throughput, counter trend, saturated component, or blocking path.
2. **Apply the hardware-model contract**. Ensure the model has physical parameters, a hardware component graph, execution path, data-movement path, bottleneck selection rule, and observation checks. See `hardware-model-contract.md`.
3. **Write equations with units**. Each term must have units or dimensionless status and a traceable source: hardware spec, measured quantity, disassembly count, calibrated parameter, or explicit assumption.
4. **Prefer bounded analytical expressions**. Use closed-form, expectation, recurrence, queueing, or piecewise terms only when they are named, bounded, and justified.
5. **State aggregation logic**. Use max, sum, overlap, pipeline, queueing, recurrence, expectation, or piecewise regime logic explicitly instead of hiding it inside prose.
6. **Bound calibration**. Keep fitted constants few, named, physically interpretable, bounded, and separated from held-out validation data.
7. **Declare validity limits**. State unsupported GPUs, kernel variants, shapes, precisions, cache regimes, occupancy regimes, and evidence gaps.

If the user's task does not map cleanly to these steps, use your native planning tool to build a model-shape plan from the available equations, hardware facts, assumptions, and validation needs, then execute the plan. If the model cannot meet this shape, label it as a baseline, sketch, or blocker rather than an accepted analytical model.

## Required Slots

- Inputs: workload shape, precision, kernel variant, hardware profile, and runtime assumptions.
- Outputs: predicted runtime or throughput plus any predicted counter trend, saturated component, or blocking path.
- Hardware contract: component graph, execution path, data-movement path, bottleneck selection rule, and observation check.
- Terms: equation, unit or dimensionless status, source, physical meaning, component or path effect, and uncertainty or bound.
- Stochastic terms: probability, expectation, bound, calibrated parameter, or uncertainty statement for cache misses, contention, scheduling variability, or reuse.
- Regimes: piecewise conditions, overlap rule, queueing rule, recurrence, or bottleneck selection rule.
- Calibration: parameter name, training split, bound, physical interpretation, and affected component or path.
- Validity: supported and unsupported operating regions.

## Common Mistakes

- Letting a neural regressor or unconstrained curve fit masquerade as an analytical model.
- Reporting a single efficiency factor without explaining what hardware behavior it absorbs.
- Treating anonymous fitted constants as acceptable model parameters.
- Claiming component-level bottlenecks without a component-level equation or selection rule.
- Claiming bottleneck understanding from runtime accuracy alone.
