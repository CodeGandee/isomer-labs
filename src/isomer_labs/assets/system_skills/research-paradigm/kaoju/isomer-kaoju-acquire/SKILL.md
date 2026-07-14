---
name: isomer-kaoju-acquire
description: Use when a Kaoju survey needs a source checkout, paper full text, dataset, model, manifest-first data reuse, immutable revision, license or access metadata, or governed acquisition.
---

# Kaoju Acquire

## Overview

Acquire only the material needed for the accepted evidence purpose, pin its identity, and route governed state changes through existing owners. Availability never substitutes for identity, license, or access checks.

Before accepting durable output, read the shared artifact semantics and recording rules plus this skill's `artifact-bindings.md`. Use `kaoju:material-acquisition-manifest` and `kaoju:topic-dataset-manifest` exactly. Return a storage blocker instead of inventing persistence, and keep material bytes outside canonical JSON.

## Workflow

1. **Accept requested identities**. Read the Survey Contract, Discovery Ledger, material purpose, destination posture, and resource boundary.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-acquire --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Check registered materials first**. Query repository registrations and the Topic Dataset Manifest; validate availability, fingerprint, access, task, schema, split, evaluator, and license compatibility.
4. **Resolve immutable identity**. Pin paper version, Canonical External Repository revision, dataset version or fingerprint, model revision or digest, and relevant subpaths.
5. **Plan governed acquisition**. State size, storage, network, credentials, private-data, license, build, and accelerator implications; obtain required Gates.
6. **Resolve source-code requests**. Accept a URL, repository name, paper ref, or Reading List item ref. Search the Artifact Library first. When a paper association is unknown, perform bounded metadata discovery, present normal candidates for selection and approval, and preserve ambiguity or access blockers. Candidate metadata receives no evidentiary authority before verification and normal intake approval.
7. **Route acquisition**. Use `isomer-cli project repos acquire` for repositories and the applicable provider or owner service for other materials. Repository acquisition is depth one by default and deepens only when identity or approved historical inspection requires it. Retain the Service Request, Execution Adapter Command Request, logs, Gate, and provenance refs.
8. **Verify and register material**. Confirm observed identity, immutable commit or digest, depth posture, access, license, integrity, and deviation from the request. Update the scoped `kaoju:artifact-library`; record verified paper-to-repository relationships in `kaoju:associated-source-code` without merging paper and code identity.
9. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-acquire --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
10. **Return status**. Produce Artifact Library, Associated Source Code, Material Acquisition Manifest, or Source Access Blocker refs and the next inspect or execute stage.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan from this skill's constraints.

## When to Use

Use after discovery or framing identifies material that must be read, checked out, registered, or executed. Do not use this skill for broad discovery, ungoverned workspace mutation, environment improvisation, or claim synthesis.

## Acquisition Contract

The Material Acquisition Artifact records requested and observed Source Identity, source class, evidence purpose, Canonical External Repository locator when applicable, immutable revision or fingerprint, selected subpaths, access and license posture, size, owner and Gate refs, destination registration, integrity checks, provenance, and limitations.

For datasets, query the Topic Dataset Manifest first. Registration creates a managed link through the Topic Workspace owner; it never copies, moves, rewrites, or deletes the external target.

## Artifact Operations

Resolve `kaoju:artifact-library`, `kaoju:associated-source-code`, `kaoju:material-acquisition-manifest`, and `kaoju:source-access-blocker` through `project artifacts describe`. Persist only through typed `project artifacts put` or binding-permitted `revise`; repository bytes and external materials remain outside structured payloads.

## Reference Routing

Use `$isomer-kaoju-shared` for identity, evidence, owner, lineage, Gate, and terminal contracts. Use `$isomer-kaoju-workspace-mgr` when workspace posture is unknown; use `$isomer-op-topic-mgr` for repository or managed-link mutation; use the applicable environment skill and `$isomer-misc-bounded-run-tips` for build or resource-heavy preparation.

## Foundational Principle

Acquisition is not evidence acceptance. Pin and verify the acquired material before any later stage uses it for a Research Claim or Run.

## Rationalization Table

| Rationalization | Required response |
| --- | --- |
| “The default branch is current enough.” | Resolve and record the observed immutable revision. |
| “Downloading is faster than checking the manifest.” | Query compatible registered data first. |
| “The files are public, so license does not matter.” | Record license posture and use constraints. |

## Red Flags

- A claim-bearing Run depends on a moving revision.
- A large or restricted download begins without its required Gate.
- An external dataset is modified during registration.

## Common Mistakes

- Recording only a local checkout path. Keep the canonical external locator and immutable identity.
- Treating an access failure as evidence that the material does not exist. Return an access blocker.
- Hiding substitutions. Record requested versus observed materials and their effect on fidelity.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
