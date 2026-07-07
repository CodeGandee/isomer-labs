# Component Bottleneck Proof

## Workflow

When a model predicts saturated hardware or a blocking path, execute the following steps in order.

1. **Name the predicted component set**. Examples include Tensor Core, FMA or FP pipe, SFU, TMA, TMEM, shared memory, L2, HBM, scheduler partition, or synchronization path.
2. **State the selection rule**. Use an explicit `argmax`, slack, reservation time, active-cycle, queueing, or critical-path rule.
3. **Design targeted inputs**. Choose shapes or precisions intended to stress one component at a time when feasible.
4. **Collect matching evidence**. Use per-unit counters, instruction mix, pipeline activity, SASS/PTX dependency path, microbenchmarks, or an explicit evidence gap.
5. **Compare labels and magnitudes**. Report predicted component, measured dominant component, predicted runtime, measured runtime, and key raw counters.
6. **Explain misses**. A miss is useful evidence only if the model refinement path is named.

If only coarse compute or memory labels are available, present them as coarse support and do not claim component-level proof.

## Proof Table Shape

Use a table with input, intended stressor, predicted component, measured dominant component, predicted runtime, measured runtime, raw counter summary, match or miss, and interpretation.

## Common Mistakes

- Calling every compute-bound result a successful component prediction.
- Designing only average-case inputs instead of inputs that stress each predicted node.
- Hiding counter values and reporting only "matches NCU."
