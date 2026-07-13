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

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
