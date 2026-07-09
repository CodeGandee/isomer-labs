---
name: gpu-analytic-finalize-prior
description: Use when DeepSci finalization needs GPU analytical-modeling priors for closure readiness and final evidence classification.
---

# GPU Analytic Finalize Prior

## Overview

This prior prevents closure when central GPU analytical-modeling claims lack visible evidence or have stronger wording than their evidence class supports.

## Workflow

1. Use `closure-readiness` at `isomer-deepsci-finalize:begin`.
2. Use `final-evidence-class` at `isomer-deepsci-finalize:end`.
3. Do not close as publishable or complete when central evidence remains missing.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `closure-readiness` | Finalization-start closure posture prior | `commands/closure-readiness.md` |
| `final-evidence-class` | Final evidence-class check before closure | `commands/final-evidence-class.md` |
