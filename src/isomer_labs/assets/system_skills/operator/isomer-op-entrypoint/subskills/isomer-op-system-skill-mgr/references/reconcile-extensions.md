# Reconcile Extensions

Use this subcommand for additive Project bookkeeping after operator-controlled initialization, an explicit reconciliation request, or a concrete undeclared extension-use request. If the user opts out, run `detect-extensions` instead.

## Workflow

1. Require a selected Project and list its declarations.
2. Preserve every existing declaration without filesystem preflight.
3. Apply the shared evidence order to each undeclared extension.
4. Call `isomer-cli --print-json project system-extensions remember <extension-id>` only for each pack whose explicit-root inspection reports a current v5 receipt, complete public-pair and protected nested coverage, managed receipt evidence, and usable compatibility.
5. Re-list declarations and report each added id and evidence basis.

If the user's task does not map cleanly to these steps, use your native planning tool to build an additive reconciliation plan from Project declarations and the shared evidence order, then execute the plan.

The operation is additive and idempotent. Never infer removal from a missing root, partial inventory, different agent host, or compatibility warning. Do not register an unmanaged complete root, `welcome_seen`, `entrypoint_seen`, `public_pair_seen`, or legacy observation as a complete managed pack. Report those states with install, upgrade, repair, or refresh advice.
