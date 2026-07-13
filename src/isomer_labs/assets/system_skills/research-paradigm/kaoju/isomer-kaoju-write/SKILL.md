---
name: isomer-kaoju-write
description: Use when an accepted Kaoju Audit Report and accepted synthesis records are ready to become a publication-facing paper contract, LaTeX manuscript, document build, validation report, and publication bundle.
---

# Kaoju Write

## Overview

Own the transformation of audited, synthesized survey knowledge into a publication-ready manuscript and bundle. Keep the audited evidence meaning intact while deciding how to communicate it to a target reader.

Before accepting durable output, read the shared artifact semantics and recording rules plus this skill's `artifact-bindings.md`. Use `kaoju:paper-contract`, `kaoju:survey-manuscript`, `kaoju:paper-build-run`, `kaoju:paper-validation-report`, and `kaoju:publication-bundle` exactly. Return a storage blocker rather than inventing a path, profile, canonical Markdown file, or untracked JSON.

## Workflow

1. **Accept audited inputs**. Require an accepted Audit Report, the exact accepted synthesis records named by the paper contract, and a resolved template ref.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-write --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Lock the paper contract**. Record target reader or venue, survey questions, scope, contribution posture, evidence boundary, template ref, quality metrics, thresholds, Tectonic-first build policy, and validation requirements.
4. **Separate views**. Build a reader-facing paper view (organizing spine, section jobs, displays, scoped conclusions) and a separate evidence view (source identities, locators, verification depths, contradictions, audit limits).
5. **Prepare citation state**. Resolve citation identities and bibliography entries from accepted Source Identities before drafting prose or displays.
6. **Draft the manuscript**. Produce a `.tex` source tree that uses compiler-owned numbering, template-native unnumbered front and back matter, and verified citations. Do not author numeric section prefixes or use Markdown-to-PDF conversion.
7. **Build and validate**. Route compilation through the resolved `document_build` extension point, Tectonic-first, with recorded fallback. Apply structural, textual, survey-quality, and visual validation. Compilation success alone does not yield `ready`.
8. **Assemble the bundle**. When the validation report is `ready` or accepted `ready-with-warnings`, reference the contract, manuscript, build Run, validation report, sources, bibliography, PDF, limitations, and Provenance Records.
9. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-write --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
10. **Return status**. Report `complete`, `paused`, or `blocked` with output refs, validation verdict, blockers, and a resume point when applicable.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan from this skill's constraints.

## When to Use

Use only after an accepted Audit Report and the requested synthesis records exist. Use for manuscript drafting, revision, rebuild, or validation when the evidence boundary is unchanged. Do not use this skill to discover new sources, repair evidence gaps, run experiments, change accepted verdicts, or bypass a missing audit.

## Output Contract

Every output preserves the accepted evidence boundary and lineage. The paper contract records the publication boundary. The manuscript stores the `.tex` source tree, bibliography, citation ledger, section jobs, and claim-to-section mapping. The build Run records the exact command, engine, template digests, logs, and outputs. The validation report records the survey-quality profile plus structural, citation, compile, extracted-text, and visual findings. The publication bundle is a navigable assembly of refs, not new evidence.

## Reference Routing

Use `$isomer-kaoju-shared` for evidence, survey Artifact, lineage, and terminal contracts. Use `references/paper-contract.md`, `references/manuscript-structure.md`, `references/latex-build.md`, `references/validation.md`, and `references/survey-quality-profile.md` for discipline details. Return evidence gaps to the owning Kaoju stage with a resume point.

## Foundational Principle

Writing communicates accepted evidence; it does not repair, strengthen, or invent evidence.

## Rationalization Table

| Rationalization | Required response |
| --- | --- |
| "The paper needs a stronger novelty claim." | Describe only contributions supported by accepted records; novelty is optional. |
| "Markdown to PDF is faster and looks fine." | Reject Markdown-to-PDF; produce and validate `.tex` source. |
| "The PDF compiled, so the paper is ready." | Require post-render validation; compilation success alone is not readiness. |
| "Section numbers in the source make review easier." | Use compiler-owned numbering; remove authored numeric prefixes. |

## Red Flags

- A manuscript claim is not mapped to an accepted record.
- A limitation or contradiction from the Audit Report disappears in the paper.
- A Markdown-to-PDF command appears in the publication build path.
- A compiled PDF is described as ready despite failed validation.
- Section structure uses authored numeric prefixes.

## Common Mistakes

- Writing from memory instead of accepted refs. Build every section from the audited evidence set.
- Treating a generated PDF as new evidence. The bundle is a derived assembly.
- Inventing novelty to imitate an empirical paper. Survey contributions include taxonomy, synthesis, coverage, and comparative perspective when records support them.
- Hiding gaps behind aggregate counts. Report denominators, exclusions, unknowns, and unresolved cases explicitly.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
