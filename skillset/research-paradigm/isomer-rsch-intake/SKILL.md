---
name: isomer-rsch-intake
description: Audit and reconcile an existing research state before choosing the next Isomer Labs research-stage handoff.
---

# Isomer Research Intake

## Overview

Use this skill when a Research Thread or Research Task already has drafts, baselines, runs, reviews, files, or user-provided state and the next Workflow Stage is not trustworthy yet.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Load required context**. Read `references/isomer-research-contract.md` first and read `references/provenance.md` when source provenance or license context matters.
2. **Select supporting references** from **Reference Routing** when state audit structure, trust taxonomy, current-board fields, or routing detail matters.
3. **Confirm entry fit** using **Entry Signals**. If the task is blank or the next stage is already obvious from durable evidence, route directly to scout, baseline, experiment, write, decision, or finalize instead of running intake.
4. **Read durable intent before inspecting files**. Start from the Research Goal, Operator Agent instruction, active Research Task, existing Decision Records, Findings, Artifacts, Evidence Items, and any known status surfaces.
5. **Inventory only decision-relevant assets** across baselines, Runs, analysis outputs, writing outputs, review packages, provenance, and blockers.
6. **Trust-rank and reconcile assets** into accepted, usable-with-verification, reference-only, stale-or-conflicting, or missing-context states, then record the honest repair or backfill need.
7. **Compile one current-board packet and route the handoff** with the trusted mainline, active blocker, stale routes to ignore, budget class, recommended Workflow Stage, Gate, Decision Record, or blocker.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the constraints, references, and user request, then execute the plan.

## Reference Routing

Read first:

- `references/isomer-research-contract.md` for local terminology, truth-source, runtime-boundary, and TBD-surface rules.
- `references/provenance.md` when source provenance or license context matters.

Read references as needed:

- `references/state-audit-template.md` when creating or refreshing the state audit Artifact.
- `references/current-board-packet.md` when the next skill needs one authoritative handoff surface.
- `references/asset-trust-taxonomy.md` when classifying reusable, stale, conflicting, or missing assets.
- `references/intake-routing.md` when choosing the next Workflow Stage, Gate, Decision Record, or blocker.

## Entry Signals

- The Research Thread or Research Task already has drafts, baselines, Runs, reviews, files, or user-provided state.
- The current board is stale, conflicting, incomplete, or not trustworthy enough for a stage transition.
- The Operator Agent needs a recommended next Workflow Stage, Gate, Decision Record, or blocker.

## Exit Criteria

- A trust-ranked current-board packet exists as a durable Artifact.
- Conflicts, stale assets, blockers, and missing evidence are visible.
- The handoff names the recommended next Workflow Stage, Gate, Decision Record, or blocker.
- Reused assets have provenance and trust rationale.

## Durable Outputs

- State audit Artifact.
- Current-board packet Artifact.
- Recommended next Workflow Stage, Gate, Decision Record, or blocker.
- Repair notes for missing or conflicting durable evidence.
- Optional Provenance Records when external or legacy assets are reused.

## Guardrails

- Do not trust conversation memory over durable state.
- Do not invent a cleaned-up history when evidence conflicts.
- Do not inspect the whole repository when a smaller evidence set answers the routing issue.
- Do not mark an existing baseline, Run, analysis result, draft, or review package as trusted unless provenance, role, and comparability are clear enough.
- Do not import paper-facing assets as current-method support until legacy-method, comparator, negative-evidence, appendix-only, and latest-method roles are separated.
- Use a Capability Binding through an Execution Adapter for command, git, repository, or environment inspection, and use `[[tbd-surface:api-execution-command]]` only when the concrete execution surface must be named.
