# Manage Paper Template

## Workflow

1. Resolve the paper line, canonical MyST refs, current export manifest, actor target, and requested action.
2. Select and execute exactly one action:

- `export`: resolve the actor target or managed default, assign an automatic export revision, write the MyST template and versioned manifest, and register `KAOJU:PAPER-TEMPLATE-EXPORT` plus `KAOJU:PAPER-TEMPLATE-MANIFEST` with base digest, source revision, paper line, tied draft, and source refs. An actor target requires explicit update or overwrite policy.
- `apply`: validate the manifest, base digest, optimistic concurrency, required sections, placeholders, citation roles, and source refs before mutation. Report orphaned grounded content and require confirmation before removing it. Create a canonical template revision and draft-regeneration handoff only after every check passes.
- `inspect`: show manifest, base and current revisions, checksums, placeholders, source refs, conflicts, and derived-draft posture without mutation.
- `status`: report current export and template refs, stale or conflicting state, and the next permitted action.

3. Record affected refs and checkpoint the Run at the first incomplete stage.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Owner, Inputs, and Outputs

Owner: `$isomer-kaoju-write`; CLI: `isomer-cli ext kaoju paper export-template|apply-template`. Inputs: paper-line and canonical MyST refs. Outputs: export, manifest, template revision, conflict, and handoff refs.

## Gates, Blockers, and Resume

Stale base, invalid MyST, unresolved placeholder, missing source, or unconfirmed orphaned content causes no canonical mutation. Resume at export, edit, validate, conflict resolution, confirm-orphans, or apply.
