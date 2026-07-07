---
name: gpu-modeling-method
description: Use when a GPU kernel research workflow needs hardware-grounded analytical model shape, source priority, baseline separation, or protection from black-box fitting.
---

# GPU Modeling Method

## Overview

This callback skill keeps GPU kernel models analytical, hardware-grounded, and falsifiable. It turns "make a model" into explicit sources, equations, assumptions, components, and evidence classes.

## When to Use

Use this callback when a DeepSci workflow is framing a GPU kernel modeling topic, choosing baselines, forming hypotheses, or starting analysis of a proposed model.

Do not use it as a benchmark runner, profiler wrapper, simulator, or replacement for the owning DeepSci skill's evidence and recording rules.

## Workflow

When this callback is applied, execute the following steps in order.

1. **Classify the current stage**. Decide whether the owning workflow needs source selection, model-shape discipline, baseline separation, or all three.
2. **Apply source priority** when the workflow may search or cite model inputs. See `commands/source-map.md`.
3. **Apply model-shape requirements** when the workflow proposes, accepts, or analyzes a GPU analytical model. See `commands/model-shape.md`.
4. **Apply baseline and evidence-class separation** when the workflow compares models or reports support. See `commands/baseline-contract.md`.
5. **Report conflicts and gaps** if this guidance cannot be followed within the owning DeepSci skill, current user request, or available evidence.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this callback, the owning DeepSci skill, and the current topic context, then execute the plan.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `source-map` | Rank GPU modeling sources and avoid weak provenance | `commands/source-map.md` |
| `model-shape` | Define the required analytical model form | `commands/model-shape.md` |
| `baseline-contract` | Separate baselines and evidence classes | `commands/baseline-contract.md` |

## Common Mistakes

- Treating roofline commentary as the full analytical model instead of a comparator.
- Accepting a fitted function without mapping terms to GPU hardware, measured quantities, or explicit assumptions.
- Mixing emulator, simulator, NCU, microbenchmark, and real-hardware evidence under one "validated" label.
- Inventing GPU parameters without source, measurement, or an explicit assumption boundary.
