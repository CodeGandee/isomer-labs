# Draft Paper

## Workflow

1. Require accepted Audit Report, Field Summary, Related-Work Catalog, Claim Status Table, and the selected paper-line scope. Missing, contradicted, or stale prerequisites pause before writing.
2. Use `$isomer-kaoju-write` to select an adaptive structure profile from taxonomy, comparison, empirical survey, or general survey and explain the choice from the accepted direction.
3. Present the structure for actor revision, then create canonical `kaoju:paper-structure-myst`, `kaoju:paper-template-myst`, and `kaoju:paper-draft-myst` files.
4. Record `kaoju:citation-map` and append-only `kaoju:paper-revision-log`. Figures and tables remain separate file-backed Artifacts referenced through typed placeholders.
5. Validate MyST structure, required sections, directives, roles, citations, placeholders, displays, source refs, and evidence boundaries with file-location diagnostics.
6. Optionally derive `kaoju:paper-draft-md`. It is a deterministic review view and never editable canonical state.

## Owner, Inputs, and Outputs

Owner: `$isomer-kaoju-write`. Inputs: accepted audit and synthesis refs plus paper line. Outputs: canonical MyST structure, template, draft, citation map, revision log, and optional derived Markdown refs.

## Gates, Blockers, and Resume

Human structure and draft acceptance are required. Resume at prerequisite resolution, structure selection, template, draft, validation, or acceptance.
