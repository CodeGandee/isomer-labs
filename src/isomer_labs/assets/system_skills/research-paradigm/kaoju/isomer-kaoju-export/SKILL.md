---
name: isomer-kaoju-export
description: Use when accepted Kaoju records need a self-contained LLM Wiki export, packaged local viewer deployment, or governed viewer launch.
---

# Kaoju Export

## Overview

Export accepted state-DB records to a self-contained survey wiki, deploy the package-owned viewer, and launch it under an explicit network-exposure posture.

## Workflow

1. **Resolve accepted scope**. Query the state DB for explicit Artifact refs or the selected direction and paper-line scopes. Reject ambiguous, stale, missing, or checksum-mismatched candidates. Never discover durable inputs by scanning directories.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-export --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Export through the CLI**. Invoke only `isomer-cli ext kaoju wiki export`. Render managed Markdown pages and the canonical JSON mapping manifest with topic, Artifact, revision, checksum, page, relationship, provenance, target, version, and changelog metadata.
4. **Refresh in place**. Stage recognized managed files, preserve unrecognized human files, and report created, changed, unchanged, stale, and removed managed paths. Re-exporting unchanged state must be idempotent.
5. **Register output**. Use the typed Artifact service for `kaoju:llm-wiki-export` and `kaoju:llm-wiki-metadata` with an export-target scope and checksummed directory manifest.
6. **Deploy the packaged viewer**. Invoke `isomer-cli ext kaoju wiki deploy`. Use only installed `isomer_labs` package resources. A recognized deployment refreshes managed assets; a non-empty unrecognized target requires clarification.
7. **Launch through the adapter**. Invoke `isomer-cli ext kaoju wiki start`, bind to loopback by default, resolve port conflicts, and require a human Gate before network exposure. Record the Run, command request, log, and local URL.
8. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-export --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
9. **Return status**. Report export, metadata, viewer, viewer-manifest, Run, log, created-page, stale-page, and resume refs.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan from this skill's constraints.

## When to Use

Use for `export-survey-wiki` or direct Kaoju wiki export, deployment, refresh, and launch. Do not invoke, import, or route to the external `imsight-llm-wiki` skill. The packaged viewer is an independently implemented compatible reader for the Kaoju wiki manifest.

## Artifact Operations

Resolve bindings through `project artifacts describe` and persist only through typed Artifact operations. Read `artifact-bindings.md`, `references/wiki-contract.md`, and `$isomer-kaoju-shared` before mutation.

## Reference Routing

Use `$isomer-kaoju-shared` for Artifact, evidence, Gate, lineage, execution request, and terminal contracts. Use `$isomer-kaoju-workspace-mgr` when state-DB readiness or export-target ownership is missing.

## Common Mistakes

- Treating rendered pages as new evidence.
- Overwriting an unrecognized target or deleting a human file.
- Loading an external viewer checkout at runtime.
- Binding the viewer to a public interface without the network-exposure Gate.

## Chat Response

Lead with the export or launch outcome. Name the stable target, created and stale pages, manifest and viewer refs, local URL when launched, blockers, and resume point.
