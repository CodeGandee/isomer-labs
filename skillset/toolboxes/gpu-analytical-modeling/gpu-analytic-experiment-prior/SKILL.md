---
name: gpu-analytic-experiment-prior
description: Use when DeepSci experiment work needs GPU analytical-modeling priors for evaluation contracts, profiler evidence, component proof, and result checks.
---

# GPU Analytic Experiment Prior

## Overview

This prior turns GPU analytical-modeling experiments into falsifiable checks. It aligns predicted outputs, metrics, profiler counters, component stressors, evidence classes, and mismatch routes.

## Workflow

1. Use `evaluation-and-profiler-contract` at `isomer-deepsci-experiment:begin`.
2. Use `result-evidence-check` at `isomer-deepsci-experiment:end`.
3. Keep profiler and measurement failures visible rather than smoothing them into confident claims.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `evaluation-and-profiler-contract` | Evaluation, NCU/profiler, and component-proof planning | `commands/evaluation-and-profiler-contract.md` |
| `result-evidence-check` | Result evidence, proxy boundary, and mismatch check | `commands/result-evidence-check.md` |
