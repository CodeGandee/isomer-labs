---
name: gpu-analytic-write-prior
description: Use when DeepSci write work needs GPU analytical-modeling priors for claim gates, proxy-evidence wording, and mathematical notation.
---

# GPU Analytic Write Prior

## Overview

This prior keeps GPU analytical-modeling writing honest and readable. It aligns prose, formulas, claim strength, and evidence class before user-facing handoff.

## Workflow

1. Use `claim-and-proxy-check` at `isomer-deepsci-write:end`.
2. Classify central claims and downgrade proxy-evidence overclaims.
3. Use concise mathematical notation with local definitions and units.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `claim-and-proxy-check` | Writing-stage claim gate, proxy boundary, and math-writing prior | `commands/claim-and-proxy-check.md` |

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
