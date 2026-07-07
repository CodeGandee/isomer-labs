# Model Shape

## Workflow

When evaluating or creating a GPU analytical model, execute the following steps in order.

1. **Name model inputs and outputs**. Include shape, precision, kernel variant, hardware parameters, clock or bandwidth assumptions, and outputs such as runtime, throughput, saturated component, or blocking path.
2. **Decompose the execution path**. Split the model into relevant stages such as launch, data movement, cache access, shared memory, tensor or vector compute, synchronization, scheduler limits, and storeback.
3. **Write equations with units**. Each term must have units and a traceable source: hardware spec, measured quantity, disassembly count, calibrated parameter, or explicit assumption.
4. **State aggregation logic**. Use max, sum, overlap, pipeline, queueing, or piecewise regime logic explicitly instead of hiding it inside prose.
5. **Bound calibration**. Keep fitted constants few, named, bounded, and separated from held-out validation data.
6. **Declare validity limits**. State unsupported GPUs, kernel variants, shapes, precisions, cache regimes, and occupancy regimes.

If the model cannot meet this shape, label it as a baseline, sketch, or blocker rather than an accepted analytical model.

## Required Slots

- Inputs: workload shape, precision, kernel variant, hardware profile, and runtime environment assumptions.
- Outputs: predicted runtime or throughput plus any predicted saturated component or blocking path.
- Terms: equation, unit, source, and uncertainty or bound.
- Regimes: piecewise conditions or bottleneck selection rule.
- Calibration: parameter name, training split, bound, and interpretation.
- Validity: supported and unsupported operating regions.

## Common Mistakes

- Letting a neural regressor or unconstrained curve fit masquerade as an analytical model.
- Reporting a single efficiency factor without explaining what hardware behavior it absorbs.
- Claiming component-level bottlenecks without a component-level equation or selection rule.
