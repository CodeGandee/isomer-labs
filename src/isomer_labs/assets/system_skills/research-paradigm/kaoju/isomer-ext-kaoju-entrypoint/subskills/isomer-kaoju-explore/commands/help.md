# Explore: Help

## Workflow

1. **List the available exploration modes**: `auto`, `directions`, `reading-list`, `intake`, `comparison`, `trial`, `paper`, and `wiki`.
2. **For each mode, state when to use it and the exact public invocation** in the form `$isomer-ext-kaoju-entrypoint->explore()-><mode>()`.
3. **Offer the user a choice**: ask which mode fits their task, or run `auto` if they prefer the subskill to decide.
4. **Do not create files, artifacts, Runs, Gates, or Service Requests** while answering help.

If the user's question does not map cleanly to these modes, use the native planning tool to recommend the closest mode or a direct Kaoju command.

## Gates, Blockers, and Resume

Help is read-only and should not pause. If the user needs context resolution first, route to `auto` after resolving context.
