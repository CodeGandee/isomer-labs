---
name: gpu-reference-map
description: Use when a GPU kernel analytical-modeling workflow needs to know where to look for source material, what each source class can justify, and what caveats to preserve.
---

# GPU Reference Map

## Overview

This callback skill centralizes source lookup for GPU kernel analytical modeling. It tells agents where to look for facts, measurements, counters, implementation details, simulator structure, and literature, while keeping operational skills focused on model shape, evidence gates, and reporting.

## When to Use

Use this callback when a DeepSci workflow searches for sources, ranks source quality, checks provenance, maps a source to a model claim, or records source limitations.

Do not use it as a crawler, benchmark runner, profiler wrapper, simulator runner, paper downloader, or substitute for the owning DeepSci skill's evidence and recording rules.

## Workflow

When this callback is applied, execute the following steps in order.

1. **Classify the missing information**. Decide whether the workflow needs local topic context, kernel implementation details, hardware facts, profiler counters, simulator architecture, measurements, literature, or several of these.
2. **Consult local topic sources first** when the current topic may already define scope, metrics, decisions, or local outputs. See `commands/local-topic-sources.md`.
3. **Consult implementation and hardware sources** when the model needs kernel behavior, generated code, launch configuration, concrete hardware limits, or instruction-level facts. See `commands/kernel-sources.md` and `commands/hardware-doc-sources.md`.
4. **Consult evidence sources by class** when the workflow needs profiler counters, timings, microbenchmarks, hardware queries, or run metadata. See `commands/profiler-counter-sources.md` and `commands/measurement-sources.md`.
5. **Consult model-structure references** when the workflow needs architecture concepts, execution-path abstractions, or prior analytical model forms. See `commands/simulator-sources.md` and `commands/literature-sources.md`.
6. **Record source limits**. For every source used, state what it can justify, what it cannot justify, required metadata, and any assumption or validation boundary.

If the user's task does not map cleanly to these steps, use your native planning tool to build a source-map plan from the missing claim, available source classes, and evidence boundary, then execute the plan.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `local-topic-sources` | Current topic intent, durable records, scripts, prior decisions, and local outputs | `commands/local-topic-sources.md` |
| `kernel-sources` | Kernel repository, generated code, compiler output, launch configuration, harness, and disassembly | `commands/kernel-sources.md` |
| `hardware-doc-sources` | Vendor docs, architecture guides, programming guides, PTX/SASS references, and hardware queries | `commands/hardware-doc-sources.md` |
| `profiler-counter-sources` | Profiler docs, NCU/Pixi posture, raw metrics, normalization, and counter-to-component mapping | `commands/profiler-counter-sources.md` |
| `simulator-sources` | AccelSim, GPGPU-Sim, and similar architecture and execution-path references | `commands/simulator-sources.md` |
| `measurement-sources` | Full-kernel timing, microbenchmark, hardware query, run metadata, and measurement caveats | `commands/measurement-sources.md` |
| `literature-sources` | Peer-reviewed and vendor-supported modeling papers, surveys, equations, and validation methods | `commands/literature-sources.md` |

## Common Mistakes

- Using a source because it is nearby rather than because it can justify the claim.
- Treating simulator structure, profiler labels, benchmark tables, or informal notes as direct target-hardware truth.
- Repeating source taxonomy inside modeling, experiment, or reporting guidance instead of consulting this reference map.
- Dropping source metadata such as version, command shape, input shape, precision, clock assumptions, run context, or validation boundary.
- Treating missing source support as acceptable because the model narrative sounds plausible.
