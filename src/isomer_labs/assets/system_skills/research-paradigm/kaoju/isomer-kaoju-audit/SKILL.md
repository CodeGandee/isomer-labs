---
name: isomer-kaoju-audit
description: Use when survey evidence, a Survey Delta, comparison, method trial, or draft conclusion needs a non-mutating coverage, identity, provenance, traceability, or fairness audit.
---

# Kaoju Audit

## Overview

Audit diagnoses whether the requested survey conclusions are supported by accepted evidence. It never repairs or rewrites evidence silently.

## Workflow

1. **Freeze the audit target**. Record the Survey Contract, target Artifact refs, accepted evidence, intended claims, and audit boundary.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-audit --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Check coverage and identity**. Inspect source-class coverage, inclusion records, work families, immutable material identities, drift, access blockers, and `searched_through` limits.
4. **Check evidence and lineage**. Inspect exact locators, Evidence Item linkage, depth, verdict, Run purpose, fidelity, inputs, patches, failures, Provenance Records, and derived Artifact lineage.
5. **Check comparison validity**. Inspect dimension bases, metric and evaluator traceability, candidate eligibility, fairness, variability, adaptations, and non-comparability decisions.
6. **Diagnose defects**. Record severity, affected claims and outputs, accepted partial evidence, and bounded repair routes without changing the target.
7. **Decide readiness**. Mark the Audit Report accepted for synthesis only when claim-bearing defects are resolved or conclusions are narrowed explicitly.
8. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-audit --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
9. **Return status**. Report the Audit Report ref, readiness decision, blockers, and resume point.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan from this skill's constraints.

## When to Use

Use before synthesis, when a Survey Delta is proposed, or when evidence drift or comparability is questioned. Do not use this skill to discover missing works, repair code, rerun experiments, relabel evidence, or write final conclusions.

## Audit Report Contract

Record the frozen target refs, checks performed, defects and severity, affected Research Claims and Artifacts, accepted evidence that remains valid, contradictions, missing exact locators, source drift, patch and failed-Run posture, metric traceability, fairness and variability findings, bounded repair routes, and readiness decision.

The readiness decision is `ready`, `ready-with-narrowed-claims`, or `not-ready`. Only the first two can become an accepted input to synthesis, and narrowed claims must be explicit.

## Reference Routing

Use `$isomer-kaoju-shared` for evidence, lineage, Artifact, and terminal contracts. Route a chosen repair to the owning stage skill; do not perform it inside the audit.

## Foundational Principle

An audit that changes its evidence while checking it destroys the distinction between diagnosis and repair.

## Rationalization Table

| Rationalization | Required response |
| --- | --- |
| “The missing locator is easy to add.” | Record the defect and route a bounded examination repair. |
| “The failed Run distracts from the conclusion.” | Retain it and state its effect on the verdict. |
| “The comparison is mostly fair.” | Identify each material mismatch and narrow or block the affected claim. |

## Red Flags

- Audit text contains newly invented source or Run evidence.
- A defect disappears without a new lineage-linked Artifact.
- Readiness is accepted while claim-bearing identity or metric traceability is unresolved.

## Common Mistakes

- Auditing prose without freezing its evidence refs. Audit both.
- Treating blocked access as exclusion from the coverage denominator. Report the gap.
- Returning a repair plan without a readiness decision and affected claims.
