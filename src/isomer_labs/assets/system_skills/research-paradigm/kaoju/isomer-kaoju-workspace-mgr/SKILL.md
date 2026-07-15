---
name: isomer-kaoju-workspace-mgr
description: Use when Kaoju survey work needs Topic Workspace readiness, existing survey state, registered datasets, repository posture, resource boundaries, or mutation-owner checks.
---

# Kaoju Workspace Manager

## Overview

Prepare a trustworthy starting context for survey work without taking ownership of Topic Workspace mutation. Reuse registered materials before requesting new acquisition.

Before accepting durable output, read the shared artifact semantics and recording rules plus this skill's `artifact-bindings.md`. Use `KAOJU:BINDING-INDEX` and `KAOJU:WORKSPACE-READINESS` exactly. An unresolved binding, profile, label, query surface, actor posture, or reset decision is a storage blocker; never invent persistence.

## When to Use

Use before a Kaoju procedure when workspace or material readiness is unknown, and for read-only dataset-registry posture checks. Do not use this skill to create a Research Topic, mutate a Topic Workspace directly, install environments, or execute research Runs.

## Workflow

1. **Resolve scope**. Resolve Effective Topic Context, fresh Workspace Runtime state, the Research Topic, Research Inquiry, Topic Workspace, selected procedure and skills, accepted prior refs, selected actors, and worker output policy.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-workspace-mgr --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Validate record surfaces**. Resolve `topic.records.artifacts`, `topic.records.views`, and `topic.records.runs`; validate access to the Workspace Runtime state DB, the binding registry version, every selected profile and semantic label, each content mode, each selected `artifact-bindings.md`, scoped latest selection, lineage, render, and export support.
4. **Inspect current posture**. Query relevant candidates through `project artifacts latest|list|show` with exact semantic ids and binding-defined scope keys. Inspect legacy unscoped ambiguity, duplicates, supersession, stale or corrupt content links, Topic Dataset Manifest state, repositories, access, licenses, storage, compute, time, actor posture, worker output policy, required Gates, and selected reset checkpoint. Never scan directories as a discovery fallback.
5. **Classify and route gaps**. Separate missing read-only context from governed mutations, environment work, credentials, private data, large acquisition, builds, accelerator Runs, owner actions, and reset decisions. Retain returned refs.
6. **Record binding index**. Validate and write `KAOJU:BINDING-INDEX` with selected skills, every semantic id, exact profile and label availability, binding status, owner, blockers, and next allowed stage.
7. **Record readiness or blocker**. Validate and write `KAOJU:WORKSPACE-READINESS` through typed Artifact operations with reusable inputs, dataset posture, verified identities, content-mode and scope readiness, resource boundaries, query and actor posture, blockers, expected Run outputs, and next allowed stage. Prevent affected accepted writes when support is missing.
8. **Apply reset posture**. When bootstrap records or explicitly user-selected survey state should survive reset, call `isomer-cli project topic-reset update-checkpoint --topic <topic> <checkpoint-id>` with exact record ids, structured payload ids and files, export paths, semantic labels, actor refs, and provenance refs. Report all ordinary unpreserved state as subject to the accepted reset plan.
9. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-workspace-mgr --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
10. **Return status**. Report `complete`, `paused`, or `blocked` with binding-index and readiness refs, reset posture, next stage, and a resume point.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan from this skill's constraints.

## Readiness Contract

The Workspace Readiness Artifact records the resolved Topic Workspace, current survey refs, registered repositories and datasets, identity or staleness checks, access and license posture, available resource envelope, Gate requirements, owner handoffs, blockers, and accepted next stage. Empirical procedures query the Topic Dataset Manifest before asking the user for data or proposing a download.

Dataset compatibility requires availability, fingerprint, access, task, schema, split, evaluator, and license compatibility. A managed link proves neither identity nor suitability.

The Binding Index records selected skill coverage by exact semantic id, profile ref, record kind, semantic label, producer binding page, lifecycle availability, status, and blocker. A ready index and readiness result are canonical bound records, not direct Markdown setup notes. If two active latest candidates compete without explicit supersession, report ambiguity and block the dependent write.

Readiness also proves that each selected content mode has an authoritative link, the scoped-query surface selects one current candidate, the Run service can checkpoint and resume, and the worker output policy names staging, promotion, and cleanup posture. A filesystem path alone proves none of these conditions.

## Artifact Operations

Resolve `KAOJU:BINDING-INDEX` and `KAOJU:WORKSPACE-READINESS` with `isomer-cli --print-json ext kaoju bindings describe KAOJU:WHAT`. Persist them only through `project artifacts put` or binding-permitted `revise`; let the service infer physical fields and the managed locator.

## Reset Contract

Preserve only bootstrap records and exact survey refs that the user selects. Update the selected reset checkpoint after those records exist. If no checkpoint is selected or updated, report bootstrap and survey state as redo-after-reset or subject to the accepted reset plan; never imply survival from file presence alone.

## Reference Routing

Use `$isomer-kaoju-shared` for evidence and terminal semantics. Route Topic Workspace and managed-link mutation to `$isomer-op-topic-mgr`; route environment setup to the applicable service skill; use `$isomer-misc-bounded-run-tips` before resource-heavy execution.

## Foundational Principle

Workspace visibility is not mutation authority. Missing owner evidence is a blocker, not permission to improvise state changes.

## Rationalization Table

| Rationalization | Required response |
| --- | --- |
| “The dataset path exists, so it is ready.” | Validate its manifest identity, fingerprint, access, task, schema, split, evaluator, and license posture. |
| “A symlink is harmless.” | Route managed-link mutation to the Topic Workspace owner. |
| “The environment can be fixed during the Run.” | Route and verify environment work before claim-bearing execution. |

## Red Flags

- An empirical stage asks for data before checking the Topic Dataset Manifest.
- A local path is used without Workspace Path Resolution or a manifest identity.
- A readiness result omits resource or Gate posture.

## Operational Notes

- Register a managed link through its owner.
- Validate identity, audit state, and staleness before reuse.

## Guardrails

- DO NOT copy external datasets into the Topic Workspace.
- DO NOT treat old survey refs as current.

## Troubleshooting Guide

- A required resource is unavailable.
  - If a required resource is unavailable, then return a bounded blocker and resume condition.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
