---
name: gpu-analytic-pipeline-prior
description: Use when DeepSci pipeline work needs GPU analytical-modeling priors for choosing the next evidence route.
---

# GPU Analytic Pipeline Prior

## Overview

This prior steers multi-stage GPU analytical-modeling passes toward the evidence route that the current model lacks most.

## Workflow

1. Use `evidence-route` at `isomer-deepsci-pipeline:begin`.
2. Identify whether the next pass should scout sources, refine the idea, build a baseline, analyze evidence, run an experiment, review claims, decide a route, write, or finalize.
3. Preserve evidence-class boundaries across the pass.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `evidence-route` | Pipeline prior for selecting the next GPU modeling evidence route | `commands/evidence-route.md` |
