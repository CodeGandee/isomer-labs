# Source Map Bridge

## Workflow

When source priority matters inside the modeling-method skill, execute the following steps in order.

1. **Identify the missing source claim**. State whether the model needs local topic context, kernel implementation detail, hardware fact, profiler/counter evidence, simulator architecture, measurement evidence, literature, or another source family.
2. **Consult `gpu-reference-map` for detailed source taxonomy**. Use `gpu-reference-map` command pages to decide where to look, what each source class can justify, what it cannot justify, and what metadata to preserve.
3. **Keep this skill focused on model method**. Use the selected sources to support hardware contracts, model shape, baseline separation, assumptions, and validity limits rather than maintaining source-family lists here.
4. **Preserve evidence-class boundaries**. Do not let simulator structure, profiler labels, benchmark tables, informal notes, or local records justify stronger claims than their source class allows.
5. **Name source gaps**. If a parameter, component, execution path, or evidence claim lacks a trustworthy source, mark it as an assumption, calibration parameter, blocker, or route back to source discovery.

If the user's task does not map cleanly to these steps, use your native planning tool to build a source-handoff plan from the missing model claim, available source classes in `gpu-reference-map`, and modeling constraints, then execute the plan while preserving the same evidence-class distinctions.

## Delegation Map

- Local scope, decisions, scripts, and outputs: consult `gpu-reference-map/commands/local-topic-sources.md`.
- Kernel source, compiler output, launch configuration, and disassembly: consult `gpu-reference-map/commands/kernel-sources.md`.
- Vendor architecture facts and concrete hardware limits: consult `gpu-reference-map/commands/hardware-doc-sources.md`.
- Profiler metrics, NCU/Pixi posture, raw counters, and counter-to-component mapping: consult `gpu-reference-map/commands/profiler-counter-sources.md`.
- Simulator architecture and execution-path references such as AccelSim or GPGPU-Sim: consult `gpu-reference-map/commands/simulator-sources.md`.
- Timings, microbenchmarks, hardware queries, and measurement caveats: consult `gpu-reference-map/commands/measurement-sources.md`.
- Prior analytical forms, validation methods, and modeling papers: consult `gpu-reference-map/commands/literature-sources.md`.

## Common Mistakes

- Updating detailed source taxonomy here instead of updating `gpu-reference-map`.
- Citing a source family as if it justifies every model claim.
- Skipping local topic context when it already defines the metric, split, or scope.
- Using a source without preserving the metadata that `gpu-reference-map` requires.
