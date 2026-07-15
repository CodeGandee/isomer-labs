---
name: isomer-kaoju-acquire
description: Use when a Kaoju survey needs a source checkout, paper full text, dataset, model, manifest-first data reuse, immutable revision, license or access metadata, or governed acquisition.
---

# Kaoju Acquire

## Overview

Acquire only the material needed for the accepted evidence purpose, pin its identity, and route governed state changes through existing owners. Availability never substitutes for identity, license, or access checks.

Before accepting durable output, read the shared artifact semantics and recording rules plus this skill's `artifact-bindings.md`. Use `KAOJU:MATERIAL-ACQUISITION-MANIFEST` and `KAOJU:TOPIC-DATASET-MANIFEST` exactly. Return a storage blocker instead of inventing persistence, and keep material bytes outside canonical JSON.

## When to Use

Use after discovery or framing identifies material that must be read, checked out, registered, or executed. Do not use this skill for broad discovery, ungoverned workspace mutation, environment improvisation, or claim synthesis.

## Workflow

1. **Accept requested identities**. Read the Survey Contract, Discovery Ledger, material purpose, destination posture, and resource boundary.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-acquire --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Check registered materials first**. Query typed Artifacts, repository semantic bindings, and the Topic Dataset Manifest; validate availability, immutable identity, access, task, schema, split, evaluator, and license compatibility.
4. **Resolve the requested source**. Resolve a supplied locator, repository name, paper ref, or Reading List item to one accepted source identity and record the requested and resolved locators. Preserve ambiguity as a clarification or blocker.
5. **Plan a candidate target without mutation**. For a new repository, choose a valid non-main `topic.repos.*` label and query `isomer-cli --print-json project paths default <label>` unless the user selected another safe Project-local target. This query must not create a directory or binding.
6. **Resolve source-code requests**. Accept a URL, repository name, paper ref, or Reading List item ref. Search the Artifact Library first. When a paper association is unknown, perform bounded metadata discovery, present normal candidates for selection and approval, and preserve ambiguity or access blockers. Candidate metadata receives no evidentiary authority before verification and normal intake approval.
7. **Plan governed acquisition**. Honor exact user-supplied clone, fetch, checkout, sparse, partial, submodule, LFS, local-copy, provider-CLI, credential-wrapper, or multi-command procedures. When none is supplied, select external commands that fit the source, revision, authentication posture, repository features, resources, and approved inspection need. State size, storage, network, credentials, private-data, license, build, and accelerator implications and obtain required Gates.
8. **Run acquisition outside Isomer**. Run the selected commands through the acting user or agent's ordinary command surface, not `isomer-cli`, a Service Request, or an Execution Adapter Command Request. Do not treat one provider, remote name, history depth, or clone sequence as canonical.
9. **Verify externally**. Before semantic registration, use external source-specific checks to confirm the target path, requested and resolved locators, intended relationship, immutable commit or digest, repository feature posture, access, license, integrity, and deviations. If acquisition or verification fails or leaves partial content, do not register it and do not ask Isomer to clean it; record a sanitized `KAOJU:SOURCE-ACCESS-BLOCKER` with filesystem posture, impact, and resume condition.
10. **Register verified topology**. Run `isomer-cli --print-json project repos register <label> --path <existing-target>`. Registration records only the semantic path binding and never executes, repairs, moves, or removes repository content. A registration conflict leaves the externally acquired target untouched and pauses at registration.
11. **Record accepted identity and provenance**. Create or revise `KAOJU:ASSOCIATED-SOURCE-CODE`, `KAOJU:ARTIFACT-LIBRARY`, and applicable acquisition provenance only after registration succeeds. Record the semantic label, requested and resolved locators, immutable commit or digest, selected external method, sanitized command descriptions, observation time, access and license posture, relationship basis, limitations, blockers, and lineage refs. Omit credentials, signed query strings, headers, environment values, credential-helper output, and raw stdout or stderr.
12. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-acquire --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
13. **Return status**. Produce Artifact Library, Associated Source Code, Material Acquisition Manifest, or Source Access Blocker refs and the next inspect or execute stage.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan from this skill's constraints.

## Acquisition Contract

The Material Acquisition Artifact records requested and resolved Source Identity, source class, evidence purpose, registered Canonical External Repository semantic label when applicable, immutable revision or fingerprint, selected external method, sanitized command evidence, observation time, selected subpaths, access and license posture, size, owner and Gate refs, integrity checks, provenance, limitations, and blockers. The Topic Workspace Manifest stores only the repository label, canonical path, storage profile, and manifest metadata.

For datasets, query the Topic Dataset Manifest first. Registration creates a managed link through the Topic Workspace owner; it never copies, moves, rewrites, or deletes the external target.

## Artifact Operations

Resolve `KAOJU:ARTIFACT-LIBRARY`, `KAOJU:ASSOCIATED-SOURCE-CODE`, `KAOJU:MATERIAL-ACQUISITION-MANIFEST`, and `KAOJU:SOURCE-ACCESS-BLOCKER` through `ext kaoju bindings describe KAOJU:WHAT`. Persist only through typed `project artifacts put` or binding-permitted `revise`; repository bytes and external materials remain outside structured payloads.

## Reference Routing

Use `$isomer-kaoju-shared` for identity, evidence, owner, lineage, Gate, and terminal contracts. Use `$isomer-kaoju-workspace-mgr` when workspace posture is unknown; use `$isomer-op-topic-mgr` for semantic path registration or managed-link mutation; use the applicable environment skill and `$isomer-misc-bounded-run-tips` for build or resource-heavy preparation. Repository source-control commands remain direct external user or agent operations.

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

## Operational Notes

- Keep the canonical external locator and immutable identity.
- Record requested versus observed materials and their effect on fidelity.

## Guardrails

- DO NOT record only a local checkout path.
- DO NOT hide substitutions.
- DO NOT register a repository until external source and immutable-identity verification succeeds.
- DO NOT store raw credential-bearing commands or output.

## Troubleshooting Guide

- Source material cannot be accessed.
  - If source material cannot be accessed, then return an access blocker without concluding that the material does not exist.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
