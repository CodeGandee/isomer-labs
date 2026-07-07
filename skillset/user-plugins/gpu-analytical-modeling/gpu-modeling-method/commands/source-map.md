# Source Map

## Workflow

When source priority matters, execute the following steps in order.

1. **Start with local topic context**. Read the current Research Topic intent, evaluation contract, durable records, local model code, benchmark scripts, and prior decisions before broad search.
2. **Inspect kernel implementation sources**. Prefer the real kernel repository, generated code, compiler flags, launch harness, and input-shape contract over secondary summaries.
3. **Ground hardware facts in authoritative sources**. Use vendor architecture guides, tuning guides, programming guides, PTX/SASS documentation, profiler docs, and hardware queries for concrete limits.
4. **Use measurement sources by evidence class**. Separate full-kernel timings, NCU counters, microbenchmarks, disassembly, and hardware specs.
5. **Use simulator sources carefully**. Treat AccelSim, GPGPU-Sim, and similar projects as architecture and execution-path references, not direct truth for a target GPU unless separately validated.
6. **Name source gaps**. If a parameter or execution path lacks a trustworthy source, mark it as an assumption, a calibration parameter, or a blocker.

If the user's task does not map cleanly to these steps, use your native planning tool to build a source-selection plan from the available topic context, modeling constraints, and evidence needs, then execute the plan while preserving the same evidence-class distinctions.

## Preferred Source Order

1. Current topic intent, records, and local outputs.
2. Kernel source, compiler output, launch harness, and generated configuration.
3. Vendor GPU documentation, PTX/SASS references, and profiler documentation.
4. Local hardware queries, NCU measurements, and microbenchmark records.
5. Peer-reviewed or vendor-supported performance modeling papers.
6. Simulator implementation and documentation for architectural concepts, queues, schedulers, issue paths, memory partitions, and dependency-path abstractions.
7. Blogs, issue threads, and informal notes only as leads to verify.

## Common Mistakes

- Citing a simulator implementation as if it were a vendor hardware specification.
- Copying simulator parameters into the target model without source, measurement, or explicit assumption boundaries.
- Reading a paper first when local topic records already define the metric, split, or scope.
- Using a benchmark table without checking kernel version, GPU SKU, clock, precision, and input shape.
