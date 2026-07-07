# Hardware Model Contract

## Workflow

When defining or auditing a GPU kernel analytical model, execute the following steps in order.

1. **Name the model claim**. State whether the model predicts runtime, throughput, counter trends, saturated component, blocking execution path, or a narrower subset.
2. **Build the hardware component graph**. Name the relevant internal components, such as schedulers, issue slots, tensor or vector pipes, special-function units, shared memory, caches, memory fabric, HBM, synchronization paths, and launch overhead.
3. **Inventory physical parameters**. For every coefficient, efficiency, latency, bandwidth, probability, threshold, or factor, state its physical meaning, units or dimensionless status, source or calibration role, allowed range, and affected component or path.
4. **Trace the execution path**. Map workload inputs through ordered stages and component visits, including which stages can overlap, serialize, queue, or form a critical path.
5. **Write per-stage equations**. For each stage that affects the claim, name the cost equation, units, component capacity or latency term, dependency on workload inputs, and whether the stage contributes by sum, max, overlap, queueing, recurrence, expectation, or piecewise regime.
6. **Model data movement explicitly**. Identify what data moves, how it is sliced or batched, which components each slice traverses, the cost of each hop, and which hops can overlap or serialize.
7. **Write bottleneck selection rules**. Define how the model chooses the saturated component and blocking path, such as `argmax`, slack, reservation time, active-cycle proxy, queueing bottleneck, dependency-chain cost, or critical-path rule.
8. **State assumptions and validity limits**. Record hardware, workload, precision, occupancy, cache, scheduling, synchronization, and calibration assumptions, plus the regimes where the model should not be used.
9. **State observation checks**. Name what observation would support or refute each predicted component or path, such as counter trends, active-cycle evidence, instruction mix, dependency-chain evidence, microbenchmark behavior, or an explicit evidence gap.

If the user's task does not map cleanly to these steps, use your native planning tool to build a hardware-model contract from the available workload inputs, hardware components, model claims, and evidence boundaries, then execute the plan.

## Required Slots

- Claim: predicted output and intended use.
- Components: hardware nodes and edges relevant to the claim.
- Parameters: name, physical meaning, units or dimensionless status, source or calibration role, bound, and component or path effect.
- Execution path: ordered stages, component visits, dependencies, and possible overlap.
- Per-stage equations: stage cost, units, hardware term, workload dependency, and aggregation contribution.
- Data movement: objects moved, slicing or batching, source and destination components, per-hop cost, and overlap or serialization.
- Aggregation: max, sum, overlap, queueing, recurrence, expectation, or piecewise regime rule.
- Bottleneck selection: saturated component rule and blocking path rule.
- Assumptions and validity: assumed hardware behavior, workload regime, calibration scope, unsupported cases, and evidence gaps.
- Observation check: evidence that would support, refute, or leave unresolved each bottleneck claim.

## Analytical Boundary

Mini-simulator-style reasoning is useful when it stays analytical. Use explicit equations, bounded recurrence, expectation, queueing, or piecewise rules. Do not turn this guidance into an event-driven simulator, and do not treat simulator output as target-hardware truth without separate validation.

## Common Mistakes

- Using `efficiency_factor` as a free parameter without saying what physical behavior it represents.
- Collapsing all data movement into one bandwidth term when the claim depends on cache, fabric, or component-level transfer behavior.
- Claiming a bottleneck path from a runtime fit without a component graph and selection rule.
- Treating runtime agreement as proof that the predicted saturated component or blocking path is correct.
