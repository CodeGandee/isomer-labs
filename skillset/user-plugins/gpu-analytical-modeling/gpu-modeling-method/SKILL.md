---
name: gpu-modeling-method
description: Use when a GPU kernel research workflow needs hardware-grounded analytical model shape, source-map handoff, baseline separation, or protection from black-box fitting.
---

# GPU Modeling Method

## Overview

This callback skill keeps GPU kernel models analytical, hardware-grounded, interpretable, and falsifiable. It turns "make a model" into explicit physical parameters, equations, assumptions, internal components, execution paths, bottleneck rules, evidence classes, and source-map handoffs.

## When to Use

Use this callback when a DeepSci workflow is framing a GPU kernel modeling topic, choosing baselines, forming hypotheses, or starting analysis of a proposed model.

Do not use it as a benchmark runner, profiler wrapper, simulator, or replacement for the owning DeepSci skill's evidence and recording rules.

## Workflow

When this callback is applied, execute the following steps in order.

1. **Classify the current stage**. Decide whether the owning workflow needs source-map handoff, hardware-model contract, model-shape discipline, baseline separation, or all of them.
2. **Apply source-map handoff** when the workflow may search or cite model inputs. See `commands/source-map.md` and consult `gpu-reference-map` for detailed source families.
3. **Apply the hardware-model contract** when the workflow proposes, accepts, or analyzes a GPU analytical model. See `commands/hardware-model-contract.md`.
4. **Apply model-shape requirements** when the workflow turns the hardware contract into equations, outputs, and validity limits. See `commands/model-shape.md`.
5. **Apply baseline and evidence-class separation** when the workflow compares models or reports support. See `commands/baseline-contract.md`.
6. **Report conflicts and gaps** if this guidance cannot be followed within the owning DeepSci skill, current user request, or available evidence.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this callback, the owning DeepSci skill, and the current topic context, then execute the plan.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `source-map` | Bridge source needs to `gpu-reference-map` and avoid weak provenance | `commands/source-map.md` |
| `hardware-model-contract` | Define physical parameters, internal components, execution path, and bottleneck verification | `commands/hardware-model-contract.md` |
| `model-shape` | Define the required analytical model form | `commands/model-shape.md` |
| `baseline-contract` | Separate baselines and evidence classes | `commands/baseline-contract.md` |

## Common Mistakes

- Treating roofline commentary as the full analytical model instead of a comparator.
- Accepting a fitted function without mapping terms to GPU hardware, measured quantities, or explicit assumptions.
- Accepting anonymous efficiency factors that lack physical meaning, units or dimensions, bounds, and a named component or path effect.
- Reporting runtime accuracy as proof of bottleneck understanding without predicted-vs-observed component or path evidence.
- Mixing emulator, simulator, NCU, microbenchmark, and real-hardware evidence under one "validated" label.
- Inventing GPU parameters without source, measurement, or an explicit assumption boundary.
- Maintaining detailed source taxonomy inside this operational skill instead of consulting `gpu-reference-map`.
