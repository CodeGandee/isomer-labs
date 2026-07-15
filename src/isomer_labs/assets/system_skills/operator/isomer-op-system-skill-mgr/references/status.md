# Status

Use this subcommand for a non-mutating summary.

## Workflow

1. List Project declarations when a Project is selected.
2. Inspect only host-known roots supplied for this request.
3. Classify the host-visible inventory when available.
4. Report each extension's first successful evidence level, complete and missing members, compatibility state, declaration state, and any refresh requirement.

If the user's task does not map cleanly to these steps, use your native planning tool to build a non-mutating status plan from declarations, host-known roots, and live inventory, then execute the plan.

Do not call `remember`, `forget`, install, upgrade, or repair commands. A declared extension remains `declared` even if the current host lacks matching skills; label a confirmed load failure as stale user-controlled state and point to `repair`.
