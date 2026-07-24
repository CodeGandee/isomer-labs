# Explore: Directions

## Workflow

1. **Clarify the survey question**. Ask: what field boundary, exclusion, coverage date, and desired depth fit the task?
2. **Identify candidate directions**. Suggest up to three bounded directions, each with a title, scope, and source-class hint.
3. **Ask the user to select, merge, or revise** the directions.
4. **Map the agreed directions to a Kaoju command**. Usually `choose-directions` or `landscape-pass`. Produce the exact public invocation.
5. **Resolve plan review**. Ask for explicit human consent by default, or use explicit target-scoped prompt delegation to review and hand off without another user turn. Materially unresolved direction scope still pauses.

If the task does not map cleanly to these steps, use the native planning tool to build a framing plan from the user's question.

## Gates, Blockers, and Resume

Pause if the field boundary or coverage date remains unclear. Resume by re-invoking `explore()->directions()` with the same context.
