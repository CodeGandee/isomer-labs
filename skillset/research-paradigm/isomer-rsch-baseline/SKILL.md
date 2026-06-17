---
name: isomer-rsch-baseline
description: Establish a trustworthy comparator, metric contract, waiver, or blocker before downstream research work.
---

# Isomer Research Baseline

## Overview

Use this skill when a Research Task needs one trusted comparator, metric contract, baseline waiver, or baseline blocker before ideation, experimentation, writing, or decision work can proceed.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Load required context**. Read `references/isomer-research-contract.md` first and read `references/provenance.md` when source provenance, license context, or source-term mapping matters.
2. **Select supporting references** from **Reference Routing** when route choice, comparability, evidence flow, gate closure, codebase audit, payload shape, boundary cases, or operations matter.
3. **Confirm entry fit and acceptance target**. Use **Entry Signals** and **Acceptance Targets** to decide whether the goal is comparison-ready, paper-repro-ready, reusable package, waived, blocked, or route-changed.
4. **Choose the lightest trustworthy route**. Prefer attach, import, or verify-local-existing before full reproduction when they can satisfy the current acceptance target; use `references/route-selection.md` for route criteria.
5. **Define the metric contract and evidence boundary**. Record comparator identity, task, dataset, split, evaluation path or evaluation Capability Binding, required metric ids, metric directions, source identity, and known deviations.
6. **Collect only decision-relevant evidence and verify it**. Trace metrics or outputs to durable Evidence Items, Artifacts, Run records, source documents, or accepted reusable packages, then classify comparability with `references/comparability-contract.md`.
7. **Close the baseline Gate explicitly**. Record a Decision Record that accepts, waives, replaces, blocks, or changes route, and carry caveats into the next Workflow Stage.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the constraints, references, and user request, then execute the plan.

## Reference Routing

Read first:

- `references/isomer-research-contract.md` for local terminology, truth-source, runtime-boundary, source-term mapping, and TBD-surface rules.
- `references/provenance.md` when source provenance, Apache 2.0 license context, or source-to-Isomer adaptation notes matter.

Read references as needed:

- `references/route-selection.md` when choosing among attach, import, verify-local-existing, reproduce, repair, waive, block, or route-change.
- `references/comparability-contract.md` before accepting, waiving, replacing, or blocking a comparator.
- `references/route-record-template.md` when a durable route record would reduce ambiguity.
- `references/gate-checklist.md` before closing a baseline Gate.
- `references/evidence-flow.md` when deciding how to record attach, import, local verification, reproduction, repair, reusable package, waiver, or blocker evidence.
- `references/payload-template.md` when a compact Artifact, Evidence Item, or Decision Record shape is needed.
- `references/boundary-cases.md` when the route is not blocked but success, caveats, or stopping rules are fuzzy.
- `references/codebase-audit.md` when attach, import, or local verification is insufficient and a source/package audit is needed.
- `references/operational-guidance.md` when execution tactics, environment choices, reuse, monitoring, or durable context materially affect the route.

## Entry Signals

- No trusted baseline exists for the Research Task.
- The current comparator is unverified, stale, weakly sourced, or missing a metric contract.
- A provided package, local implementation, source repository, source document, or reusable baseline bundle needs attach, import, verification, reproduction, or repair.
- Ideation, experimentation, writing, or final decision work would otherwise guess the comparator, dataset, split, metric definitions, evaluation path, provenance, or caveats.

Do not use this skill when a verified active baseline already exists for the current route, unless the user asks for a refresh or a material comparison risk has appeared.

## Acceptance Targets

- `comparison-ready`: one comparator is trustworthy enough for downstream comparison and the core metric contract is durable.
- `paper-repro-ready`: the comparator can support paper-facing reproduction or comparison claims.
- `reusable-package`: the baseline evidence and provenance are clean enough to package as a reusable Artifact after verification.
- `waived`: the Research Task must continue without a baseline and the reason is durable.
- `blocked`: the current route cannot clear the Gate cleanly and the next best move is explicit.
- `route-changed`: the previous route is no longer the best trust-per-cost path and a Decision Record names the replacement.

## Core Metric Contract

Before treating a baseline as usable, make these fields explicit: comparator identity, baseline id, route, task identity, dataset identity, split contract, evaluation path or evaluation Capability Binding, required metric ids, metric directions, source identity, trusted metrics or output pointers, material environment facts, and known deviations.

The accepted metric contract should be an Artifact. If a concrete storage layout or schema must be named, use `[[tbd-surface:path-artifact-layout]]` or `[[tbd-surface:schema-evidence-item]]` until Isomer accepts that surface.

## Verification

Verification is mandatory before acceptance. Check that the run, package import, local implementation, reusable package, source document, or trusted-output inspection actually supports the intended dataset, split, metric definitions, metric directions, and comparator identity.

Classify the outcome as `verified-match`, `verified-close`, `verified-diverged`, `trusted-with-caveats`, or `broken`. Separate implementation mismatch, environment mismatch, data or split mismatch, expected stochastic variance, and unexplained divergence when those distinctions matter.

## Durable Outputs

- Metric-contract Artifact and supporting Evidence Items.
- Comparator identity, source identity, route, acceptance target, and known deviations.
- Verification Evidence Items for logs, outputs, source documents, package records, local evaluation results, or Run records.
- Decision Record that accepts, waives, replaces, blocks, or changes the baseline route.
- Gate state and next recommended Workflow Stage.

## Guardrails

- Do not accept copied, paraphrased, fabricated, or weakly sourced metrics as trusted evidence.
- Do not treat attach, import, package materialization, or reusable-package publication as baseline acceptance by itself.
- Do not hide dataset, split, evaluator, metric definition, metric direction, source identity, or environment deviations.
- Do not force full reproduction when a lighter route satisfies the acceptance target.
- Do not keep doing baseline work after one comparator is accepted, waived, blocked, or route-changed, unless a named comparison risk remains.
- Do not repeat the same failure class without new evidence, a code change, an environment change, or a route change.
- Use `[[tbd-surface:policy-baseline-waiver]]` for unsettled waiver rules and `[[tbd-surface:api-gate]]` when a concrete Gate API must be named.
