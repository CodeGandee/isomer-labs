# Draft Paper

## Workflow

1. Require accepted Audit Report, Field Summary, Related-Work Catalog, Claim Status Table, and the selected paper-line scope. Missing, contradicted, or stale prerequisites pause before writing.
2. Use `$isomer-kaoju-write` to select an adaptive structure profile from taxonomy, comparison, empirical survey, or general survey and explain the choice from the accepted direction.
3. Present the structure for actor revision, then create canonical `KAOJU:PAPER-STRUCTURE-MYST`, `KAOJU:PAPER-TEMPLATE-MYST`, and `KAOJU:PAPER-DRAFT-MYST` files.
4. Record `KAOJU:CITATION-MAP` and append-only `KAOJU:PAPER-REVISION-LOG`. Figures and tables remain separate file-backed Artifacts referenced through typed placeholders.
5. Validate MyST structure, required sections, directives, roles, citations, placeholders, displays, source refs, and evidence boundaries with file-location diagnostics.
6. Optionally derive `KAOJU:PAPER-DRAFT-MD`. It is a deterministic review view and never editable canonical state.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Owner, Inputs, and Outputs

Owner: `$isomer-kaoju-write`. Inputs: accepted audit and synthesis refs plus paper line. Outputs: canonical MyST structure, template, draft, citation map, revision log, and optional derived Markdown refs.

## Gates, Blockers, and Resume

Human structure and draft acceptance are required. Resume at prerequisite resolution, structure selection, template, draft, validation, or acceptance.
