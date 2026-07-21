---
name: isomer-kaoju-audit
description: Use when survey evidence, a Survey Delta, comparison, method trial, or draft conclusion needs a non-mutating coverage, identity, provenance, traceability, or fairness audit.
skill_invocation_notation: >
  Top-level skill entrypoints use SKILL.md. Parent-scoped subskill entrypoints use
  SKILL-MAIN.md and are loaded explicitly through their parent; nested SKILL.md is
  accepted only as legacy input when SKILL-MAIN.md is absent.
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Kaoju Audit

## Overview

Audit diagnoses whether the requested survey conclusions are supported by accepted evidence. It never repairs or rewrites evidence silently.

Before accepting durable output, read the shared artifact semantics and recording rules plus this skill's `artifact-bindings.md`. Use `KAOJU:AUDIT-REPORT` exactly. Return a storage blocker rather than inventing a path, profile, canonical Markdown file, or untracked JSON.

Portfolio reminder: audit findings, defects, claim statuses, repair routes, and readiness decisions are not Research Ideas. If an accepted audit directly assesses an existing direction's evidence, invoke `isomer-op-entrypoint->research-ideas` and record an explicit evidence transition with the Audit Report and affected evidence refs. The audit never changes decision state or silently creates a repair concept.

## When to Use

Use before synthesis, when a Survey Delta is proposed, or when evidence drift or comparability is questioned. Do not use this skill to discover missing works, repair code, rerun experiments, relabel evidence, or write final conclusions.

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

Callback resolution returns a compact `callbacks` array. Process entries in returned order and read each absolute `instruction_path` as supplemental material according to `source_type`. For `skill_dir`, read the reported `SKILL.md` and any directly required relative resources; do not treat the directory as an installed system skill or execute its scripts solely because resolution returned it. During ordinary execution, do not request `--explain` or depend on registry, priority, scope, status, Toolbox registration, or gating fields. Use `--explain`, `list`, `show`, or `validate` only to diagnose or manage callback resolution. Preserve higher-priority instructions, the current user request, owning-skill and shared research rules, evidence discipline, required Gates, validation, and recording obligations; report any material conflict.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan from this skill's constraints.

## Audit Report Contract

Record the frozen target refs, checks performed, defects and severity, affected Research Claims and Artifacts, accepted evidence that remains valid, contradictions, missing exact locators, source drift, patch and failed-Run posture, metric traceability, fairness and variability findings, bounded repair routes, and readiness decision.

The readiness decision is `ready`, `ready-with-narrowed-claims`, or `not-ready`. Only the first two can become an accepted input to synthesis, and narrowed claims must be explicit.

## Artifact Operations

Resolve `KAOJU:AUDIT-REPORT` and `KAOJU:CLAIM-STATUS-TABLE` through `ext kaoju bindings describe KAOJU:WHAT`. Use typed `project artifacts put` for every non-mutating audit event. Do not revise the audited target or repeat physical binding fields in the command.

## Reference Routing

Use `isomer-ext-kaoju-entrypoint->shared` for evidence, lineage, Artifact, and terminal contracts. Route a chosen repair to the owning stage skill; do not perform it inside the audit.

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

## Operational Notes

- Audit both.
- Report the gap.

## Guardrails

- DO NOT audit prose without freezing its evidence refs.
- DO NOT treat blocked access as exclusion from the coverage denominator.
- DO NOT return a repair plan without a readiness decision and affected claims.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
