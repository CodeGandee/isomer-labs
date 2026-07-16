---
name: isomer-kaoju-frame
description: Use when a Kaoju request needs a bounded Survey Contract, clarification-first choices, comparison intent, coverage limits, evidence depth, resources, Gates, or stop conditions.
---

# Kaoju Frame

## Overview

Turn the user's survey question into an explicit contract before discovery or execution changes its scope. Ambiguity that changes cost, evidence strength, or comparability must become a user-visible decision.

Before accepting durable output, read the shared artifact semantics and recording rules plus this skill's `artifact-bindings.md`. Use `KAOJU:DIRECTION-SET`, `KAOJU:SURVEY-CONTRACT`, or `KAOJU:COMPARISON-INTENT` exactly. If a binding or required surface is unavailable, return a storage blocker; never invent a path, profile, canonical Markdown file, or untracked JSON state.

## When to Use

Use at the start of a survey procedure, when a prior contract no longer fits, or when empirical comparison needs a user checkpoint. Do not use this skill to search, acquire, inspect, execute, audit, or synthesize evidence.

## Workflow

1. **Resolve context**. Read the Research Topic, Research Inquiry, user request, prior survey refs, and Workspace Readiness Artifact.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-frame --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Inspect ambiguity**. Identify unclear boundaries, source classes, time horizon, seed role, inclusion rules, desired depth, deliverables, resources, and Gates.
4. **Clarify when requested or material**. Use the A/B/C/D clarification contract, mark exactly one suggested option, then ask whether to clarify more or proceed.
5. **Propose and confirm directions when requested**. Propose three directions by default. Give each a stable id, scoped question, boundary, source classes, coverage date, expected depth, deliverables, and empirical-feasibility annotation. Mark one suggestion, accept multiple selections and custom directions, and revise or reject proposals until the actor explicitly confirms the set. Current host capability may annotate feasibility but cannot filter or rank directions by itself.
6. **Persist the confirmed set**. Put or revise one `KAOJU:DIRECTION-SET` in its topic scope with proposals, selections, custom inputs, rejected or revised entries, actor confirmation, and lineage. Never conflate it with a frozen Survey Contract.
7. **Freeze the contract**. Optionally derive one combined or per-direction Survey Contract with question, boundary, source classes, coverage date, inclusion and exclusion rules, evidence contract, resources, Gate posture, outputs, and stop conditions.
8. **Add empirical intent when applicable**. For actual-run comparison, create the Comparison Intent Document and wait for a Proceed Decision before preparation or Runs.
9. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-frame --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
10. **Return status**. Report the Direction Set, Survey Contract, or Comparison Intent Document ref and the next allowed stage.

Callback resolution returns a compact `callbacks` array. Process entries in returned order and read each absolute `instruction_path` as supplemental material according to `source_type`. For `skill_dir`, read the reported `SKILL.md` and any directly required relative resources; do not treat the directory as an installed system skill or execute its scripts solely because resolution returned it. During ordinary execution, do not request `--explain` or depend on registry, priority, scope, status, Toolbox registration, or gating fields. Use `--explain`, `list`, `show`, or `validate` only to diagnose or manage callback resolution. Preserve higher-priority instructions, the current user request, owning-skill and shared research rules, evidence discipline, required Gates, validation, and recording obligations; report any material conflict.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan from this skill's constraints.

## Survey Contract

Required fields are the user question, target audience, boundary, primary and linked source classes, seeds, coverage date, `searched_through` policy, inclusion and exclusion rules, desired verification depth, comparison mode, deliverables, resource envelope, Gate requirements, clarification mode, stop conditions, and accepted prior refs.

For comparative Runs, the Comparison Intent Document additionally states candidate identities and readiness, reusable prior evidence, acquisition and environment needs, reproduce or reimplement routes, datasets, metrics, evaluators, fairness rules, repetitions or uncertainty plan, resources, Gates, unresolved decisions, and the Proceed Decision.

## Artifact Operations

Resolve `KAOJU:DIRECTION-SET`, `KAOJU:SURVEY-CONTRACT`, and `KAOJU:COMPARISON-INTENT` with `isomer-cli --print-json ext kaoju bindings describe KAOJU:WHAT`. Use `project artifacts put` for a new scoped object and `project artifacts revise` for an actor-approved current-state update; the service infers all physical binding fields.

## Reference Routing

Use `$isomer-kaoju-shared` for interaction, evidence, Artifact, owner-routing, lineage, and terminal contracts. Use `$isomer-kaoju-workspace-mgr` when readiness evidence is missing or stale.

## Foundational Principle

A vague request is not an execution contract. Do not spend material resources or claim coverage beyond the boundary the user accepted.

## Rationalization Table

| Rationalization | Required response |
| --- | --- |
| “The field boundary is obvious.” | State it and its exclusions in the Survey Contract. |
| “We can choose metrics after the Runs.” | Define metric and evaluator semantics before comparative execution. |
| “The user asked to proceed quickly.” | Keep mandatory Gates and comparison intent; reduce scope instead. |

## Red Flags

- No coverage date or stop condition.
- Empirical candidates start preparation before a Proceed Decision.
- “Latest” appears without a `searched_through` boundary.

## Operational Notes

- Ask one material A/B/C/D choice at a time.
- It is an interaction mode inside the chosen procedure.

## Guardrails

- DO NOT treat repositories as primary related works when no paper or report relationship is established.
- DO NOT ask many unstructured questions.
- DO NOT use clarification-first as a procedure.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
