# Simulator Sources

## Workflow

When simulator projects may inform a model, execute the following steps in order.

1. **Use simulators for structure first**. Treat AccelSim, GPGPU-Sim, and similar projects as references for architecture concepts, execution paths, queues, schedulers, issue paths, memory partitions, and dependency abstractions.
2. **Identify the modeled architecture boundary**. Check which architecture generation, ISA behavior, memory hierarchy, scheduling model, and timing abstractions the simulator source actually represents.
3. **Separate structure from truth**. Simulator code and traces can suggest model structure, but target-hardware parameters and claims need vendor sources, hardware queries, measurements, counters, or explicit assumptions.
4. **Avoid importing parameters blindly**. Do not copy simulator constants, latencies, bandwidths, queue depths, or policies into a target model without source, measurement, calibration role, and validity bounds.
5. **Record validation status**. If simulator output is used as evidence, state whether it has been separately validated against the target hardware scope and what claim it can support.

If the user's task does not map cleanly to these steps, use your native planning tool to build a simulator-source plan from the needed architecture concept, simulator source, target hardware scope, and validation boundary, then execute the plan.

## Can Justify

- Architectural decomposition ideas, execution-path abstractions, queueing concepts, scheduler and memory-system model structure, and candidate variables for analytical modeling.

## Cannot Justify

- Target-hardware truth, measured latency, target-specific component saturation, or exact counter behavior unless separately validated for the target scope.

## Preserve

- Simulator project, version or revision, modeled architecture, source file or documentation path, abstraction used, copied parameter status, validation status, and assumption boundary.
