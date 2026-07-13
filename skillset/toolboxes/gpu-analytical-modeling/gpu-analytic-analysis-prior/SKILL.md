---
name: gpu-analytic-analysis-prior
description: Use when DeepSci analysis work needs GPU analytical-modeling priors for hardware-grounded interpretation and component proof checks.
---

# GPU Analytic Analysis Prior

## Overview

This prior keeps analysis tied to hardware mechanisms, evidence classes, and mismatch routes. It prevents black-box fit language from replacing component and path interpretation.

## Workflow

1. Use `hardware-grounded-interpretation` at `isomer-deepsci-analysis:begin`.
2. Use `component-proof-check` at `isomer-deepsci-analysis:end`.
3. Route mismatches to model refinement, added evidence, narrowed claims, parking, or blocking.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `hardware-grounded-interpretation` | Analysis prior before interpreting model or evidence outputs | `commands/hardware-grounded-interpretation.md` |
| `component-proof-check` | End-stage check for bottleneck proof and mismatch handling | `commands/component-proof-check.md` |

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
