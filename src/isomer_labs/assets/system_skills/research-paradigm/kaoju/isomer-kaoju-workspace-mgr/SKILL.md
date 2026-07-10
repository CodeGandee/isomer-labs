---
name: isomer-kaoju-workspace-mgr
description: Use when Kaoju survey work needs Topic Workspace readiness, existing survey state, registered datasets, repository posture, resource boundaries, or mutation-owner checks.
---

# Kaoju Workspace Manager

## Overview

Prepare a trustworthy starting context for survey work without taking ownership of Topic Workspace mutation. Reuse registered materials before requesting new acquisition.

## Workflow

1. **Resolve scope**. Identify the Research Topic, Research Inquiry, Topic Workspace through Workspace Path Resolution, selected procedure, and accepted prior refs.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-workspace-mgr --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Inspect readiness**. Check existing survey Artifacts, repository registrations, Topic Dataset Manifest entries, access posture, storage, compute, time, and required Gates.
4. **Classify gaps**. Separate missing read-only context from governed mutations, environment work, credentials, private data, large acquisition, builds, and accelerator Runs.
5. **Route owned changes**. Send each governed operation to the applicable Topic Workspace, environment, provider, execution, or Gate owner and retain returned refs.
6. **Record readiness**. Produce a Workspace Readiness Artifact with reusable inputs, verified identities, resource boundaries, blockers, and the next allowed stage.
7. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-workspace-mgr --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
8. **Return status**. Report `complete`, `paused`, or `blocked` with output refs and a resume point.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan from this skill's constraints.

## When to Use

Use before a Kaoju procedure when workspace or material readiness is unknown, and for read-only dataset-registry posture checks. Do not use this skill to create a Research Topic, mutate a Topic Workspace directly, install environments, or execute research Runs.

## Readiness Contract

The Workspace Readiness Artifact records the resolved Topic Workspace, current survey refs, registered repositories and datasets, identity or staleness checks, access and license posture, available resource envelope, Gate requirements, owner handoffs, blockers, and accepted next stage. Empirical procedures query the Topic Dataset Manifest before asking the user for data or proposing a download.

Dataset compatibility requires availability, fingerprint, access, task, schema, split, evaluator, and license compatibility. A managed link proves neither identity nor suitability.

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

## Common Mistakes

- Copying external datasets into the Topic Workspace. Register a managed link through its owner.
- Treating old survey refs as current. Validate identity, audit state, and staleness before reuse.
- Hiding unavailable resources. Return a bounded blocker and resume condition.
