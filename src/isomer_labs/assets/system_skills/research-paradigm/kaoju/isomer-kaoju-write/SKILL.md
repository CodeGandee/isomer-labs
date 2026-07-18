---
name: isomer-kaoju-write
description: Use when an accepted Kaoju Audit Report and accepted synthesis are ready for canonical MyST paper drafting, template exchange, derived Markdown or TeX, PDF construction, validation, and publication bundling.
---

# Kaoju Write

## Overview

Own the transformation of audited survey knowledge into a publication-facing paper. Canonical paper state is MyST. Markdown, TeX, compile logs, PDF files, and publication bundles are derived Artifacts with explicit lineage.

Before accepting durable output, read `$isomer-kaoju-shared`, this skill's `artifact-bindings.md`, and the applicable references. Resolve each semantic id through the binding registry and typed Artifact service. Return a storage blocker instead of inventing a profile, semantic label, state-DB entry, path, or untracked file.

Portfolio reminder: paper structures, section jobs, claims, displays, templates, manuscripts, build products, and publication bundles are not Research Ideas. Invoke `$isomer-research-idea-recording` only to add an exact paper-facing realization of an existing direction or when an actor explicitly promotes a distinct new research concept. Writing never changes evidence or decision facets by implication.

## When to Use

Use only after audit accepts the requested synthesis. Use for canonical MyST drafting and revision, actor template exchange, derived Markdown or TeX, PDF builds, validation, and publication bundling. Do not use this skill to discover sources, repair evidence, run scientific trials, change accepted verdicts, or bypass a missing audit.

## Workflow

1. **Accept audited inputs**. Require an accepted `KAOJU:AUDIT-REPORT`, the exact accepted synthesis refs, source and display refs, a paper-line scope, target reader or venue, and publication Gate policy. A missing or not-ready audit blocks drafting.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-write --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Select an adaptive structure profile**. Choose and explain a typed structure based on the accepted direction, target reader, evidence shape, and venue. Record section jobs, display jobs, evidence boundaries, and required limitations in `KAOJU:PAPER-STRUCTURE-MYST`; do not impose one empirical-paper outline on every survey.
4. **Lock the paper contract**. Record survey questions, scope, contribution posture, paper line, accepted evidence, canonical MyST policy, typed structure profile, citation roles, display expectations, quality checks, and Gates. Record content-template and LaTeX-template selection policies as separate fields; the latter may remain unresolved until PDF construction.
5. **Create canonical MyST state**. Resolve an explicitly named content template or content `main` through `ext kaoju paper template show --kind content`, then record its name, stable ref, state token, and observed tree digest in paper state. Use the role-explicit named-template service for mutable template state; never use generic Artifact revise. Create or revise `KAOJU:PAPER-DRAFT-MYST`, `KAOJU:CITATION-MAP`, and `KAOJU:PAPER-REVISION-LOG` through their binding-permitted operations. Store every selected figure or table as a separate file-backed `KAOJU:PAPER-DISPLAY`, then refer to its stable ref through a typed `{{figure:<artifact-ref>}}` or `{{table:<artifact-ref>}}` placeholder. Existing drafts retain the content-template state they observed; later content-template or LaTeX-template updates do not rewrite them.
6. **Validate before promotion**. Run `isomer-cli ext kaoju paper validate` for MyST syntax, required sections, directives, roles, citations, placeholders, displays, source refs, and evidence boundaries. Report structured file and line diagnostics. Invalid staging content never mutates canonical state.
7. **Handle both named template roles**. Resolve role before using `ext kaoju paper template --kind KIND` for list, show, create, copy, replacement, file edit, metadata edit, archive, delete, migration, or exchange. A content template is an arbitrary MyST-oriented tree. A LaTeX template is an arbitrary safe multi-file presentation tree with an entrypoint and checked preamble, marker, or include contract, registered build profile, provenance, and license posture. Inspect and prepare arbitrary source trees; the CLI owns role-safe identity, integrity, concurrency, atomic replacement, and mutation audit, not arbitrary conversion or merge.
8. **Apply role-local discovery for an unnamed update**. Explicit role and locator win. Otherwise run `template exports --kind KIND`: use exactly one eligible edited export of that role; ask when several selected-role candidates qualify; if none qualifies, inspect `<topic.paper.template_exchange_root>/<kind>/main/`; if neither exists, ask for a source. Same-named records or exports of the other role are ineligible. Do not choose by timestamp, paper line, or database order.
9. **Explain destructive named state**. Before update, report target name, stable ref, current token and digest, source, assessment, and whether an ordinary named copy was explicitly requested. Ordinary updates preserve no prior bytes and create no additional name. Map “save before changing” to create-from-template with a chosen ordinary name, “restore or replace from NAME” to update-from-template, and “merge” to agent candidate construction followed by update-from-directory. Create an extra name on the agent's initiative only when the request authorizes it and report that name first.
10. **Derive review Markdown when requested**. Run `derive-markdown` deterministically from the accepted MyST revision. Register checksum, source revision, unsupported-construct diagnostics, lineage, and `canonical: false`; never edit the Markdown as canonical paper state.
11. **Compose and inspect TeX when requested**. Resolve an explicit LaTeX template or LaTeX `main` independently of the content template. Run `init-tex --content-template-ref REF` with the LaTeX selector, snapshot the exact multi-file stock into `KAOJU:PAPER-TEMPLATE-TEX`, and compose a self-contained `KAOJU:PAPER-DRAFT-TEX`. Keep the presentation fingerprint independent of the content-template digest; record the canonical MyST checksum separately. Run `tex-status`, then inspect and repair derived directives, tables, citations, floats, raw blocks, entrypoint behavior, and venue structure before claiming build readiness.
12. **Build and validate PDF**. After build authorization, run `build-pdf` through the `document_build` Research Operation Extension Point. Require pinned-snapshot verification, the declared entrypoint, and the registered build profile. Record the exact command, distinct Run, compile log, template drift, paper-local repair posture, source and output checksums, PDF inspection, repair classification, and publication Gate. Presentation-only repairs stay in the paper-specific TeX draft. Promote one into LaTeX stock only after an explicit user request through `template update --kind latex`; canonical content, dependencies, build-profile, or interpretation changes require a revised plan and human Gate.
13. **Assemble publication state**. When validation is `ready` or actor-accepted `ready-with-warnings`, register the paper contract, canonical MyST refs, observed content-template identity, observed LaTeX-template identity, TeX snapshot, citation map, derived files, build Run, validation report, limitations, and provenance in a publication bundle. The bundle is an assembly, not new evidence.
14. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-write --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
15. **Return terminal state**. Report `complete`, `paused`, or `blocked` with canonical and derived refs, diagnostics, validation and Gate posture, Run checkpoint, blockers, and the first incomplete stage as the resume point.

Callback resolution returns a compact `callbacks` array. Process entries in returned order and read each absolute `instruction_path` as supplemental material according to `source_type`. For `skill_dir`, read the reported `SKILL.md` and any directly required relative resources; do not treat the directory as an installed system skill or execute its scripts solely because resolution returned it. During ordinary execution, do not request `--explain` or depend on registry, priority, scope, status, Toolbox registration, or gating fields. Use `--explain`, `list`, `show`, or `validate` only to diagnose or manage callback resolution. Preserve higher-priority instructions, the current user request, owning-skill and shared research rules, evidence discipline, required Gates, validation, and recording obligations; report any material conflict.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan without weakening the accepted evidence boundary or MyST authority.

## MyST Paper Graph

`KAOJU:PAPER-TEMPLATE-MYST` is mutable named content-template state. `KAOJU:PAPER-TEMPLATE-LATEX` is independent mutable named LaTeX presentation stock. Each role has its own `main`, state tokens, exports, and updates. `KAOJU:PAPER-STRUCTURE-MYST`, `KAOJU:PAPER-DRAFT-MYST`, `KAOJU:CITATION-MAP`, and `KAOJU:PAPER-REVISION-LOG` retain canonical content lineage. `KAOJU:PAPER-TEMPLATE-TEX` is an exact paper-line snapshot of observed LaTeX stock, while `KAOJU:PAPER-DRAFT-TEX` is the self-contained composition and may carry paper-local repair. Compile logs, PDFs, validation reports, and publication bundles preserve both upstream template identities.

Legacy writing, manuscript, and TeX snapshot records remain readable. Never infer canonical MyST from them. Contract migration annotates existing content-template records in place. Actor-authorized LaTeX adoption copies one exact selected `KAOJU:PAPER-TEMPLATE-TEX` or `KAOJU:WRITING-TEMPLATE` directory into named LaTeX stock with checked metadata and preserves every source and historical record. Legacy `ext research templates` mutation remains disabled.

## Artifact Operations

Resolve every semantic id in `artifact-bindings.md` with `isomer-cli --print-json ext kaoju bindings describe KAOJU:WHAT`. Use typed `project artifacts put` and binding-permitted `revise` for ordinary bindings. Use `ext kaoju paper template --kind content|latex` for every mutable named-template mutation and export operation, and use the other `ext kaoju paper` commands for validation, derivation, TeX composition, drift inspection, and PDF build orchestration. Never edit SQL rows or managed Artifact files directly.

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
- A template action does not resolve content versus LaTeX role before discovery.
- An unnamed update skips the selected role's single-edited-export, `<exchange-root>/<kind>/main/`, then user-clarification order.
- A paper-local TeX repair silently changes named LaTeX stock.
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
