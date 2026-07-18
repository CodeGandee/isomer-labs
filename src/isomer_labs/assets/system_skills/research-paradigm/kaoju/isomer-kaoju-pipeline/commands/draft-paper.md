# Draft Paper

## Workflow

1. Require accepted Audit Report, Field Summary, Related-Work Catalog, Claim Status Table, and the selected paper-line scope. Missing, contradicted, or stale prerequisites with known audit or synthesis producers yield `paused` prerequisite recovery before writing; report their routes and the draft resume point rather than invoking them inside this procedure.
2. Resolve an explicitly named content template through `template show --kind content`, or default to content `main`. Read its stable ref, current state token and tree digest, authored entrypoint, and use guidance, then interpret the arbitrary MyST-oriented tree for the requested paper. Do not inspect or select LaTeX stock during content-structure selection, and do not select another content name by timestamp, paper line, or record order.
3. Use `$isomer-kaoju-write` to select an adaptive structure profile from taxonomy, comparison, empirical survey, or general survey and explain the choice from the accepted direction. Present the structure for actor revision, then create canonical `KAOJU:PAPER-STRUCTURE-MYST` and `KAOJU:PAPER-DRAFT-MYST` state tied to the selected content-template name, stable ref, state token, and observed digest. Create or change the content template only through the role-explicit named-template workflow when the request authorizes that separate mutation.
4. Record `KAOJU:CITATION-MAP` and append-only `KAOJU:PAPER-REVISION-LOG`. Figures and tables remain separate file-backed Artifacts referenced through typed placeholders.
5. Validate MyST structure, required sections, directives, roles, citations, placeholders, displays, source refs, and evidence boundaries with file-location diagnostics.
6. Optionally derive `KAOJU:PAPER-DRAFT-MD`. It is a deterministic review view and never editable canonical state.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Owner, Inputs, and Outputs

Owner: `$isomer-kaoju-write`. Inputs: accepted audit and synthesis refs, paper line, and an explicit content template or content `main`. Outputs: selected content-template name, stable ref, state token and observed digest, canonical MyST structure and draft, citation map, revision log, and optional derived Markdown refs.

## Gates, Blockers, and Resume

Human structure and draft acceptance are required. Resume at prerequisite resolution, structure selection, template, draft, validation, or acceptance.
