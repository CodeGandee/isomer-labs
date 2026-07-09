---
name: gpu-analytic-decision-prior
description: Use when DeepSci decision work needs GPU analytical-modeling priors for routing mismatches, missing evidence, or unsupported claims.
---

# GPU Analytic Decision Prior

## Overview

This prior helps route GPU analytical-modeling work when model predictions, measurements, profiler evidence, or claims do not line up.

## Workflow

1. Use `mismatch-route` at `isomer-deepsci-decision:begin`.
2. Choose the smallest honest route: refine, add evidence, limit, park, block, or accept partial support.
3. Record what evidence or repair would change the decision.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `mismatch-route` | Decision prior for failed or incomplete model evidence | `commands/mismatch-route.md` |
