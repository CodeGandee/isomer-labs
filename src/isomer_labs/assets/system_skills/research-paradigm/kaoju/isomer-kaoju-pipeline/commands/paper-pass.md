# Paper Pass

## Workflow

1. Resolve the Research Topic, accepted Audit Report and synthesis refs, paper-line scope, target reader or venue, and requested stopping point. A missing or not-ready audit with a known producer or repair owner yields `paused` prerequisite recovery and an exact paper-pass resume point.
2. Route the canonical drafting stages to `draft-paper` and `$isomer-kaoju-write`. Resolve an explicit named template or canonical `main`, record its stable ref and observed digest, and require adaptive typed structure, MyST draft, citation map, revision log, and structured MyST validation.
3. When template construction, editing, copying, replacement, export, or reconciliation is requested, compose `manage-paper-template`. Keep arbitrary-tree interpretation agent-owned; reject ambiguous discovery, stale tokens, unsafe content, edited-target overwrite, or material unconfirmed choices without canonical mutation.
4. Derive review Markdown only when requested and label it non-canonical.
5. When PDF output is requested, compose `build-paper-pdf`. Initialize and inspect derived TeX, obtain build authorization, execute through `document_build`, inspect the PDF, and apply the publication Gate.
6. Return `complete`, `paused`, or `blocked` with canonical MyST refs, derived refs, Run and Gate posture, diagnostics, and the first incomplete stage.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Compatibility Mapping

`paper-pass` is a retained compatibility composition. It maps to `draft-paper` and optionally `build-paper-pdf`; it does not restore LaTeX-first authorship. A draft-only request stops after accepted MyST state tied to the selected template name, stable ref, and observed digest. A build request continues from those exact observed inputs.

## Gates, Blockers, and Resume

A missing or not-ready audit pauses drafting when an audit or repair route is available; reserve `blocked` for an unavailable external state change. An ambiguous unnamed template update, stale token, invalid tree, or edited export refresh causes no mutation. TeX syntax and presentation repair may proceed only inside the approved build policy; material content, dependency, toolchain, or interpretation repair requires a revised plan and human Gate. Resume at the first incomplete audit, repair, template discovery or construction, draft, exchange, conversion, inspection, build, validation, or publication stage.
