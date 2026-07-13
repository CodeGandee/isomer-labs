---
name: gpu-analytic-review-prior
description: Use when DeepSci review work needs GPU analytical-modeling priors for source provenance, evidence boundaries, and claim strength.
---

# GPU Analytic Review Prior

## Overview

This prior helps reviewers check whether GPU analytical-modeling claims have the right source provenance, evidence class, and claim strength before the work moves on.

## Workflow

1. Use `source-and-evidence-review` at `isomer-deepsci-review:begin`.
2. Use `claim-strength-review` at `isomer-deepsci-review:end`.
3. Downgrade, route back, or block unsupported central claims.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `source-and-evidence-review` | Start-stage provenance and evidence review | `commands/source-and-evidence-review.md` |
| `claim-strength-review` | End-stage claim strength and proof visibility review | `commands/claim-strength-review.md` |

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
