---
name: gpu-reporting-and-closure
description: Use when GPU kernel analytical modeling results need claim gating, math-writing discipline, proof placement, or closure limits before review or finalization.
---

# GPU Reporting and Closure

## Overview

This callback skill keeps GPU analytical-modeling writeups honest and readable. It aligns claims with evidence, turns code-like formulas into mathematical notation, requires visible hard evidence for central claims, and prevents closure when central proof is missing.

## When to Use

Use this callback when a DeepSci workflow writes, reviews, revises, or finalizes GPU kernel analytical-modeling results.

Do not use it to weaken evidence requirements for publication, hide failed validation, or convert unsupported claims into confident prose.

## Workflow

When this callback is applied, execute the following steps in order.

1. **Classify claims by evidence** before final user-facing prose is accepted, and require visible evidence packets for supported central claims. See `commands/claim-gate.md`.
2. **Apply math-writing discipline** when formulas, notation, or equation prose appear. See `commands/math-writing.md`.
3. **Check proof placement and closure limits** when results are central to a report, paper, or final summary, without prescribing a fixed section or layout. See `commands/closure-limits.md`.
4. **Downgrade or route back** if evidence does not support the claimed runtime, counter trend, saturated component, or blocking path.
5. **Report unresolved gaps** in the final response, handoff, or closure record.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step reporting plan from this callback, the owning DeepSci skill, and the current evidence base, then execute the plan.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `claim-gate` | Classify claim support before writing or closure | `commands/claim-gate.md` |
| `math-writing` | Improve formula notation and local definitions | `commands/math-writing.md` |
| `closure-limits` | Decide publish, park, defer, limit, or route back | `commands/closure-limits.md` |

## Common Mistakes

- Letting final prose say "validated on hardware" when only proxy evidence exists.
- Saying a central runtime or bottleneck claim is supported without showing inputs, predictions, measured latency, observed evidence, and interpretation.
- Hiding central component-saturation proof where final readers cannot inspect it.
- Using long code variable names as mathematical symbols.
- Closing a topic as publishable while the central bottleneck claim is unsupported.
