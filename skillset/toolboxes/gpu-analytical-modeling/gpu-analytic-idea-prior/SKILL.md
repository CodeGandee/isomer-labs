---
name: gpu-analytic-idea-prior
description: Use when DeepSci idea work needs GPU analytical-modeling priors for hypothesis source maps and hardware-grounded model contracts.
---

# GPU Analytic Idea Prior

## Overview

This prior keeps GPU analytical-modeling ideas physically grounded while they are still cheap to reshape. It turns hypotheses into source-backed model contracts instead of broad modeling aspirations.

## Workflow

1. Use `hypothesis-model-contract` at `isomer-deepsci-idea:begin`.
2. Name the claim, source map, hardware components, equations, assumptions, and evidence needed to support the idea.
3. Keep unsupported details as assumptions, calibration slots, or follow-up evidence needs.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `hypothesis-model-contract` | Source-backed hypothesis and model-shape prior | `commands/hypothesis-model-contract.md` |

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
