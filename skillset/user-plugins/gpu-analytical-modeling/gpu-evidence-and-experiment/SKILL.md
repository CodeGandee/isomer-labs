---
name: gpu-evidence-and-experiment
description: Use when a GPU kernel analytical model needs falsifiable evaluation, NCU evidence, component bottleneck proof, or model-refinement routing.
---

# GPU Evidence and Experiment

## Overview

This callback skill turns GPU analytical models into testable claims. It focuses experiments and analysis on measured runtime, counter trends, saturated hardware components, blocking execution paths, and honest mismatch handling.

## When to Use

Use this callback when a DeepSci workflow designs experiments, runs validation, analyzes measurements, reviews evidence, or decides what to do after model and hardware evidence disagree.

Do not use it to bypass environment gates, run profilers automatically, or claim that missing evidence is acceptable because the analytical story sounds plausible.

## Workflow

When this callback is applied, execute the following steps in order.

1. **Check the evaluation contract** before collecting or interpreting results. See `commands/evaluation-contract.md`.
2. **Apply the NCU protocol** when profiling or discussing profiler evidence. See `commands/ncu-protocol.md`.
3. **Require component and path proof** when the model predicts saturated units or blocking execution paths. See `commands/component-bottleneck-proof.md`.
4. **Classify mismatches** when predictions and evidence disagree. See `commands/failure-refinement.md`.
5. **Route honestly** through the owning DeepSci workflow: refine, limit, park, block, or proceed only when the evidence supports the claim.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step evidence plan from this callback, the owning DeepSci skill, and current topic records, then execute the plan.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `evaluation-contract` | Define metrics, splits, and fairness before claims | `commands/evaluation-contract.md` |
| `ncu-protocol` | Specify profiler command and counter evidence | `commands/ncu-protocol.md` |
| `component-bottleneck-proof` | Validate saturated component and blocking path claims | `commands/component-bottleneck-proof.md` |
| `failure-refinement` | Explain mismatches and choose a route | `commands/failure-refinement.md` |

## Common Mistakes

- Reporting MAPE without saying whether ground truth is real hardware, emulator, simulator, or synthetic.
- Accepting coarse compute-bound or memory-bound labels when the claim is about a specific pipe, cache, scheduler, or dependency path.
- Hiding profiler command failures behind vague "NCU was infeasible" language.
- Recalibrating on validation data and then reporting the result as held-out accuracy.
