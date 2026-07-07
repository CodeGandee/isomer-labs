# Component Bottleneck Proof

## Workflow

When a model predicts saturated hardware or a blocking path, execute the following steps in order.

1. **Name the predicted component set**. Examples include Tensor Core, FMA or FP pipe, SFU, TMA, TMEM, shared memory, L2, HBM, scheduler partition, or synchronization path.
2. **State the selection rule**. Use an explicit `argmax`, slack, reservation time, active-cycle, queueing, or critical-path rule.
3. **Design one-component or one-path stressors**. Choose inputs or regimes intended to stress one predicted component or blocking path at a time when feasible, and state what observation would support or refute that prediction before interpreting results.
4. **Collect matching hard evidence**. Use raw counters, derived counter mappings, instruction mix, pipeline activity, dependency-path evidence, microbenchmarks, measured timings, or an explicit evidence gap.
5. **Compare labels and magnitudes**. Report predicted component or path, intended stressor, observed dominant component or path, predicted latency or runtime, measured latency or runtime, key raw observations, and evidence mapping rationale.
6. **Explain matches and misses**. A match or miss is useful only if the interpretation and any model refinement path are named.

If the user's task does not map cleanly to these steps, use your native planning tool to build a component-proof plan from the predicted bottlenecks, available counters, execution-path evidence, and validation limits, then execute the plan. If only coarse compute or memory labels are available, present them as coarse support and do not claim component-level proof.

## Proof Table Shape

Use a table with input, intended stressor, predicted component or path, observed dominant component or path, predicted latency or runtime, measured latency or runtime, raw observation summary, evidence mapping rationale, match or miss, interpretation, and explicit gap if evidence is unavailable.

## Common Mistakes

- Calling every compute-bound result a successful component prediction.
- Designing only average-case inputs instead of inputs that stress each predicted node.
- Hiding observation values and reporting only "matches profiler counters."
- Reporting a bottleneck label without the stressor and observation that produced it.
