# Explore: Paper

## Workflow

1. **Clarify the paper goal**. Ask: draft content, build PDF, manage a template, or run a full paper pass?
2. **Check prerequisites**. Accepted audit and synthesis, template role, and output form.
3. **Discuss template role** (`content` vs `latex`) and whether a new template is needed.
4. **Map to a Kaoju command**. Usually `draft-paper`, `build-paper-pdf`, `manage-paper-template`, `paper-pass`, or `create-paper-template`. Produce the exact public invocation.
5. **Resolve plan review**. Ask for explicit human consent by default, or use explicit target-scoped prompt delegation to review and hand off without another user turn. Missing audit, synthesis, or a material template-role decision still pauses.

If the task does not map cleanly to these steps, use the native planning tool to order paper stages.

## Gates, Blockers, and Resume

Pause if audit and synthesis are not accepted or the template role is unresolved. Resume by re-invoking `explore()->paper()` with the same context.
