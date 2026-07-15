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
5. **Create canonical MyST state**. Create or revise `KAOJU:PAPER-TEMPLATE-MYST`, `KAOJU:PAPER-DRAFT-MYST`, `KAOJU:CITATION-MAP`, and `KAOJU:PAPER-REVISION-LOG`. Store every selected figure or table as a separate file-backed `KAOJU:PAPER-DISPLAY`, then refer to its stable ref through a typed `{{figure:<artifact-ref>}}` or `{{table:<artifact-ref>}}` placeholder. The citation map records its display role, evidence refs, caption or interpretation status, and insertion locator. Every supported, contradicted, inconclusive, and limited claim retains its accepted evidence lineage.
6. **Validate before promotion**. Run `isomer-cli ext kaoju paper validate` for MyST syntax, required sections, directives, roles, citations, placeholders, displays, source refs, and evidence boundaries. Report structured file and line diagnostics. Invalid staging content never mutates canonical state.
7. **Handle actor template exchange**. Use `ext kaoju paper export-template` for a versioned export with base digest, source revision, paper line, tied draft, source refs, and explicit actor-target update policy. Use `apply-template` only after manifest, optimistic-concurrency, required-section, placeholder, source, and orphan checks. Unconfirmed orphaned grounded content or a stale base causes no canonical mutation.
8. **Derive review Markdown when requested**. Run `derive-markdown` deterministically from the accepted MyST revision. Register checksum, source revision, unsupported-construct diagnostics, lineage, and `canonical: false`; never edit the Markdown as canonical paper state.
9. **Initialize and inspect TeX when requested**. Run `init-tex` with the current compatibility fingerprint over venue or document class, toolchain policy, and required constructs. Reuse a compatible template; revise an incompatible one. Directly inspect and repair derived TeX directives, tables, citations, floats, raw blocks, and venue structure before claiming build readiness. TeX changes never silently promote back into MyST.
10. **Build and validate PDF**. After build authorization, run `build-pdf` through the `document_build` Research Operation Extension Point and Execution Adapter Command Request. Record the engine, exact command, fallback rationale, distinct Run, compile log, source and output checksums, PDF inspection, repair classification, and publication Gate. Automatic repair is limited to presentation-only or TeX syntax changes; canonical content, dependencies, toolchain policy, or interpretation changes require a revised plan and human Gate.
11. **Assemble publication state**. When validation is `ready` or actor-accepted `ready-with-warnings`, register the paper contract, canonical MyST refs, citation map, derived files, build Run, validation report, limitations, and provenance in a publication bundle. The bundle is an assembly, not new evidence.
12. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-write --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
13. **Return terminal state**. Report `complete`, `paused`, or `blocked` with canonical and derived refs, diagnostics, validation and Gate posture, Run checkpoint, blockers, and the first incomplete stage as the resume point.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan without weakening the accepted evidence boundary or MyST authority.

## MyST Paper Graph

`KAOJU:PAPER-STRUCTURE-MYST`, `KAOJU:PAPER-TEMPLATE-MYST`, `KAOJU:PAPER-DRAFT-MYST`, `KAOJU:CITATION-MAP`, and `KAOJU:PAPER-REVISION-LOG` are canonical paper state. `KAOJU:PAPER-DRAFT-MD` is a deterministic review view. TeX templates and drafts are derived conversion products. Compile logs, PDF files, PDF revision logs, build Runs, validation reports, and publication bundles descend from the exact canonical MyST revision.

Legacy writing and manuscript records remain readable. Never auto-promote historical TeX or Markdown into canonical MyST. Actor-authorized legacy TeX registration records it only as a derived TeX Artifact with source identity and provenance. New template work uses `ext kaoju paper`; the historical `ext research templates` surface is inspection and repair compatibility only.

## Artifact Operations

Resolve every semantic id in `artifact-bindings.md` with `isomer-cli --print-json ext kaoju bindings describe KAOJU:WHAT`. Use typed `project artifacts put` and binding-permitted `revise`; use `ext kaoju paper` for validation, exchange, derivation, TeX initialization, and PDF build orchestration. Producers never repeat record kind, profile, semantic label, scope policy, or internal managed path.

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
- A stale template export overwrites a newer MyST revision.
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
