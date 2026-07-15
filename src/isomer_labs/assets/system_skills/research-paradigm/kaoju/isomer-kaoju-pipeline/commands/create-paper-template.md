# Create Paper Template

## Workflow

1. Resolve the paper-line scope, accepted audit and synthesis basis, target reader or venue, and current canonical MyST state.
2. Use `$isomer-kaoju-write` to select and explain an adaptive typed structure profile.
3. Create or revise `KAOJU:PAPER-STRUCTURE-MYST` and `KAOJU:PAPER-TEMPLATE-MYST` through typed Artifact operations. Include required section jobs, citation roles, typed display and source-ref placeholders, limitations, and venue constraints.
4. Validate MyST syntax, headings, roles, directives, placeholders, and evidence boundaries with `isomer-cli ext kaoju paper validate` before acceptance.
5. When the actor wants a manual-edit copy, compose `manage-paper-template` and run `ext kaoju paper export-template`. The export is versioned and derived; it is not canonical state.
6. Return the canonical structure and template refs, diagnostics, optional export refs, and resume point.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Compatibility Mapping

`create-paper-template` is retained for callers that use the historical procedure name. It now creates a canonical MyST template. It never creates canonical LaTeX, writes a producer-selected internal path, or uses `KAOJU:WRITING-TEMPLATE` for new state. Derived TeX is initialized later by `build-paper-pdf`.

## Gates, Blockers, and Resume

Missing accepted evidence, an unresolved paper line, invalid MyST, missing sources, or unsupported binding state blocks acceptance. Resume at structure selection, template validation, or optional export.
