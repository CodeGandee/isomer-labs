---
name: gpu-analytic-baseline-prior
description: Use when DeepSci baseline work needs GPU analytical-modeling priors for baseline classes, evidence classes, and fair comparison.
---

# GPU Analytic Baseline Prior

## Overview

This prior keeps GPU analytical-modeling baselines comparable and honestly labeled. It separates analytical derivation, roofline baselines, simulator traces, emulator outputs, microbenchmarks, profiler counters, and real hardware timing.

## Workflow

1. Use `evidence-baseline-contract` at `isomer-deepsci-baseline:begin`.
2. Classify every comparator by role and evidence class before acceptance.
3. Reserve real-hardware accuracy language for matching measured hardware evidence.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `evidence-baseline-contract` | Baseline role, evidence class, and fair-comparison prior | `commands/evidence-baseline-contract.md` |
