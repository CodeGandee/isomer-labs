---
name: isomer-kaoju-write
description: Use when an accepted Kaoju Audit Report and accepted synthesis are ready for canonical MyST paper drafting, template exchange, derived Markdown or TeX, PDF construction, validation, and publication bundling.
---

# Kaoju Write

## Overview

Own the transformation of audited survey knowledge into a publication-facing paper. Canonical paper state is MyST. Markdown, TeX, compile logs, PDF files, and publication bundles are derived Artifacts with explicit lineage.

Before accepting durable output, read `$isomer-kaoju-shared`, this skill's `artifact-bindings.md`, and the applicable references. Resolve each semantic id through the binding registry and typed Artifact service. Return a storage blocker instead of inventing a profile, semantic label, state-DB entry, path, or untracked file.

## When to Use

Use only after audit accepts the requested synthesis. Use for canonical MyST drafting and revision, actor template exchange, derived Markdown or TeX, PDF builds, validation, and publication bundling. Do not use this skill to discover sources, repair evidence, run scientific trials, change accepted verdicts, or bypass a missing audit.

## Workflow

1. **Accept audited inputs**. Require an accepted `KAOJU:AUDIT-REPORT`, the exact accepted synthesis refs, source and display refs, a paper-line scope, target reader or venue, and publication Gate policy. A missing or not-ready audit blocks drafting.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-write --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Select an adaptive structure profile**. Choose and explain a typed structure based on the accepted direction, target reader, evidence shape, and venue. Record section jobs, display jobs, evidence boundaries, and required limitations in `KAOJU:PAPER-STRUCTURE-MYST`; do not impose one empirical-paper outline on every survey.
4. **Lock the paper contract**. Record survey questions, scope, contribution posture, paper line, accepted evidence, canonical MyST policy, typed structure profile, citation roles, display expectations, build policy, quality checks, and Gates.
5. **Create canonical MyST state**. Resolve an explicitly named mutable `KAOJU:PAPER-TEMPLATE-MYST` tree or canonical `main` through `ext kaoju paper template show`, then record the selected name, stable ref, and observed tree digest in the paper state. Use named-template create or update only for template state; never use generic Artifact revise for this mutable binding. Create or revise `KAOJU:PAPER-DRAFT-MYST`, `KAOJU:CITATION-MAP`, and `KAOJU:PAPER-REVISION-LOG` through their binding-permitted operations. Store every selected figure or table as a separate file-backed `KAOJU:PAPER-DISPLAY`, then refer to its stable ref through a typed `{{figure:<artifact-ref>}}` or `{{table:<artifact-ref>}}` placeholder. Existing drafts retain the template ref and digest they observed when produced; a later template update does not silently rewrite them.
6. **Validate before promotion**. Run `isomer-cli ext kaoju paper validate` for MyST syntax, required sections, directives, roles, citations, placeholders, displays, source refs, and evidence boundaries. Report structured file and line diagnostics. Invalid staging content never mutates canonical state.
7. **Handle named template construction and exchange**. Use `ext kaoju paper template` for low-level list, show, create, exact named copy, exact named replacement, file edit, metadata edit, archive, delete, export inspection, export, and export observation. A template is an arbitrary MyST-oriented directory tree, so inspect arbitrary source and target trees, identify entrypoints, interpret intended changes, resolve material ambiguity, and prepare a clean candidate before update. Isomer CLI owns name safety, managed-tree integrity, state-token concurrency, atomic replacement, and lightweight mutation audit; it does not construct or merge a template for you.
8. **Apply ordered discovery for an unnamed database update**. Explicit name, canonical ref, template path, or export path always wins after validation. Otherwise run `template exports`: use exactly one eligible edited registered export; ask the user when several edited or identity-inconsistent candidates exist; if none qualifies, resolve `topic.paper.template_exchange_root` and use its `main/` child when it exists, regardless of database `main`; if neither exists, ask the user for a source. Do not choose by timestamp or unrelated database order.
9. **Explain destructive named state**. Before update, report target name, stable ref, current token and digest, source, assessment, and whether an ordinary named copy was explicitly requested. Ordinary updates preserve no prior bytes and create no additional name. Map “save before changing” to create-from-template with a chosen ordinary name, “restore or replace from NAME” to update-from-template, and “merge” to agent candidate construction followed by update-from-directory. Create an extra name on the agent's initiative only when the request authorizes it and report that name first.
10. **Derive review Markdown when requested**. Run `derive-markdown` deterministically from the accepted MyST revision. Register checksum, source revision, unsupported-construct diagnostics, lineage, and `canonical: false`; never edit the Markdown as canonical paper state.
11. **Initialize and inspect TeX when requested**. Run `init-tex` with the selected template name, stable ref, observed digest, venue or document class, toolchain policy, and required constructs in the compatibility fingerprint. Reuse only an exact compatible derivation. Directly inspect and repair derived TeX directives, tables, citations, floats, raw blocks, and venue structure before claiming build readiness. TeX changes never silently promote back into MyST.
12. **Build and validate PDF**. After build authorization, run `build-pdf` through the `document_build` Research Operation Extension Point and Execution Adapter Command Request. Record the engine, exact command, fallback rationale, distinct Run, compile log, source and output checksums, PDF inspection, repair classification, and publication Gate. Automatic repair is limited to presentation-only or TeX syntax changes; canonical content, dependencies, toolchain policy, or interpretation changes require a revised plan and human Gate.
13. **Assemble publication state**. When validation is `ready` or actor-accepted `ready-with-warnings`, register the paper contract, canonical MyST refs, selected template name, stable ref and observed digest, citation map, derived files, build Run, validation report, limitations, and provenance in a publication bundle. The bundle is an assembly, not new evidence.
14. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-write --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
15. **Return terminal state**. Report `complete`, `paused`, or `blocked` with canonical and derived refs, diagnostics, validation and Gate posture, Run checkpoint, blockers, and the first incomplete stage as the resume point.

Callback resolution returns a compact `callbacks` array. Process entries in returned order and read each absolute `instruction_path` as supplemental material according to `source_type`. For `skill_dir`, read the reported `SKILL.md` and any directly required relative resources; do not treat the directory as an installed system skill or execute its scripts solely because resolution returned it. During ordinary execution, do not request `--explain` or depend on registry, priority, scope, status, Toolbox registration, or gating fields. Use `--explain`, `list`, `show`, or `validate` only to diagnose or manage callback resolution. Preserve higher-priority instructions, the current user request, owning-skill and shared research rules, evidence discipline, required Gates, validation, and recording obligations; report any material conflict.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan without weakening the accepted evidence boundary or MyST authority.

## MyST Paper Graph

`KAOJU:PAPER-TEMPLATE-MYST` is one stable mutable named canonical tree per exact name. `KAOJU:PAPER-STRUCTURE-MYST`, `KAOJU:PAPER-DRAFT-MYST`, `KAOJU:CITATION-MAP`, and `KAOJU:PAPER-REVISION-LOG` retain their own binding-defined state and lineage behavior. An exported template directory is a non-canonical user-editable copy. `KAOJU:PAPER-DRAFT-MD` is a deterministic review view. TeX templates and drafts are derived conversion products. Compile logs, PDF files, PDF revision logs, build Runs, validation reports, and publication bundles descend from exact observed MyST state.

Legacy writing and manuscript records remain readable. Never auto-promote historical TeX or Markdown into canonical MyST. Actor-authorized migration inspects active candidates, wraps one unambiguous selected tree without semantic rewriting, and preserves historical records and old export directories. New template work uses `ext kaoju paper template`; legacy `ext research templates` mutation is disabled.

## Artifact Operations

Resolve every semantic id in `artifact-bindings.md` with `isomer-cli --print-json ext kaoju bindings describe KAOJU:WHAT`. Use typed `project artifacts put` and binding-permitted `revise` for ordinary bindings. Use `ext kaoju paper template` for every mutable named-template mutation and export operation, and use the other `ext kaoju paper` commands for validation, derivation, TeX initialization, and PDF build orchestration. Never edit SQL rows or managed Artifact files directly.

## Reference Routing

Use `$isomer-kaoju-shared` for evidence, state-DB, file-authority, lineage, Gate, Service Request, Run, and terminal contracts. Use `references/paper-contract.md`, `references/manuscript-structure.md`, `references/latex-build.md`, `references/validation.md`, and `references/survey-quality-profile.md` for paper discipline. Return evidence gaps to their owning Kaoju stage with the exact resume point.

## Foundational Principle

Writing communicates accepted evidence; format conversion, compilation, and visual polish cannot repair or strengthen it.

## Rationalization Table

| Rationalization | Required response |
| --- | --- |
| “The paper needs a stronger novelty claim.” | Describe only contributions supported by accepted records; novelty is optional. |
| “Editing the derived Markdown or TeX is simpler.” | Apply content changes to canonical MyST and regenerate derived files. |
| “The PDF compiled, so the paper is ready.” | Require structural, citation, extracted-text, visual, and publication-Gate validation. |
| “The old TeX manuscript is close enough.” | Keep it readable as derived legacy content; require actor-authorized migration into a new MyST line. |

## Red Flags

- A manuscript claim is not mapped to an accepted record.
- A limitation or contradiction from the Audit Report disappears.
- Markdown or TeX is treated as canonical paper state.
- An edited template working tree is overwritten or promoted without agent assessment and a current target token.
- An unnamed update skips the single-edited-export, topic `main/`, then user-clarification order.
- An ordinary update silently creates another name or claims that prior bytes remain recoverable.
- A material repair runs without a revised plan and Gate.
- A PDF is described as ready despite failed or unavailable required validation.

## Operational Notes

- Build every section from the audited evidence set.
- Register them separately and use placeholders.
- It is a derived assembly.
- Report denominators, exclusions, unknowns, and unresolved cases.

## Guardrails

- DO NOT write from memory instead of accepted refs.
- DO NOT embed figures or tables without typed display and source refs.
- DO NOT treat a generated PDF as evidence.
- DO NOT hide gaps behind aggregate counts.

## Chat Response

Present normal chat responses in natural-language Markdown. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat. Lead with the outcome. Name canonical MyST refs separately from derived Markdown, TeX, build, and PDF refs. Include every pending Gate, blocker, Run checkpoint, and resume point that affects completion.
