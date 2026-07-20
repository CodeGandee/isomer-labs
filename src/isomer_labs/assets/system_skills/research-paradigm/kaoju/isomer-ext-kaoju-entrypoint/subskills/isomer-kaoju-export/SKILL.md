---
name: isomer-kaoju-export
description: Use when accepted Kaoju records need a self-contained LLM Wiki export, packaged local viewer deployment, or governed viewer launch.
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Kaoju Export

## Overview

Export accepted state-DB records to a self-contained survey wiki, deploy the package-owned viewer, and launch it under an explicit network-exposure posture.

## When to Use

Use for `export-survey-wiki` or direct Kaoju wiki export, deployment, refresh, and launch. Do not invoke, import, or route to the external `imsight-llm-wiki` skill. The packaged viewer is an independently implemented compatible reader for the Kaoju wiki manifest.

## Workflow

1. **Resolve accepted scope**. Query the state DB for explicit Artifact refs or the selected direction and paper-line scopes. Reject ambiguous, stale, missing, or checksum-mismatched candidates. Never discover durable inputs by scanning directories.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-export --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Export through the CLI**. Invoke only `isomer-cli ext kaoju wiki export`. Render managed Markdown pages and the canonical JSON mapping manifest with topic, Artifact, revision, checksum, page, relationship, provenance, target, version, and changelog metadata.
4. **Refresh in place**. Stage recognized managed files, preserve unrecognized human files, and report created, changed, unchanged, stale, and removed managed paths. Re-exporting unchanged state must be idempotent.
5. **Register output**. Use the typed Artifact service for `KAOJU:LLM-WIKI-EXPORT` and `KAOJU:LLM-WIKI-METADATA` with an export-target scope and checksummed directory manifest.
6. **Deploy the packaged viewer**. Invoke `isomer-cli ext kaoju wiki deploy`. Use only installed `isomer_labs` package resources. A recognized deployment refreshes managed assets; a non-empty unrecognized target requires clarification.
7. **Launch through the adapter**. Invoke `isomer-cli ext kaoju wiki start`, bind to loopback by default, resolve port conflicts, and require a human Gate before network exposure. Record the Run, command request, log, and local URL.
8. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-export --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
9. **Return status**. Report export, metadata, viewer, viewer-manifest, Run, log, created-page, stale-page, and resume refs.

Callback resolution returns a compact `callbacks` array. Process entries in returned order and read each absolute `instruction_path` as supplemental material according to `source_type`. For `skill_dir`, read the reported `SKILL.md` and any directly required relative resources; do not treat the directory as an installed system skill or execute its scripts solely because resolution returned it. During ordinary execution, do not request `--explain` or depend on registry, priority, scope, status, Toolbox registration, or gating fields. Use `--explain`, `list`, `show`, or `validate` only to diagnose or manage callback resolution. Preserve higher-priority instructions, the current user request, owning-skill and shared research rules, evidence discipline, required Gates, validation, and recording obligations; report any material conflict.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan from this skill's constraints.

## Artifact Operations

Resolve bindings through `ext kaoju bindings describe KAOJU:WHAT` and persist only through typed Artifact operations. Read `artifact-bindings.md`, `references/wiki-contract.md`, and `isomer-ext-kaoju-entrypoint->shared` before mutation.

## Reference Routing

Use `isomer-ext-kaoju-entrypoint->shared` for Artifact, evidence, Gate, lineage, execution request, and terminal contracts. Use `isomer-ext-kaoju-entrypoint->workspace` when state-DB readiness or export-target ownership is missing.

## Guardrails

- DO NOT treat rendered pages as new evidence.
- DO NOT overwrite an unrecognized target or delete a human file.
- DO NOT load an external viewer checkout at runtime.
- DO NOT bind the viewer to a public interface without the network-exposure Gate.

## Chat Response

Present normal chat responses in natural-language Markdown. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat. Lead with the export or launch outcome. Name the stable target, created and stale pages, manifest and viewer refs, local URL when launched, blockers, and resume point.
