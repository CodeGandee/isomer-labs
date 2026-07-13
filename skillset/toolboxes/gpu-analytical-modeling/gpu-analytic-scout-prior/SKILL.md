---
name: gpu-analytic-scout-prior
description: Use when DeepSci scout work needs GPU analytical-modeling priors for source framing, model-shape framing, or output checks.
---

# GPU Analytic Scout Prior

## Overview

This prior helps scout-stage agents frame GPU kernel analytical-modeling work before research direction hardens. It keeps early scouting focused on source families, model shape, evidence boundaries, and output readiness.

## Workflow

1. Use `framing-prior` at `isomer-deepsci-scout:begin`.
2. Use `output-check` at `isomer-deepsci-scout:end`.
3. Keep the result supplemental to the active DeepSci scout workflow, topic context, and user request.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `framing-prior` | Source and model-shape framing before scout work | `commands/framing-prior.md` |
| `output-check` | Source, model-shape, and evidence readiness check after scout work | `commands/output-check.md` |

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
