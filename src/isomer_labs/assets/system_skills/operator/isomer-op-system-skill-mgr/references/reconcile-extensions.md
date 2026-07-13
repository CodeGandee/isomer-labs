# Reconcile Extensions

Use this subcommand for additive Project bookkeeping after operator-controlled initialization, an explicit reconciliation request, or a concrete undeclared extension-use request. If the user opts out, run `detect-extensions` instead.

1. Require a selected Project and list its declarations.
2. Preserve every existing declaration without filesystem preflight.
3. Apply the shared evidence order to each undeclared extension.
4. Call `isomer-cli project system-extensions remember <extension-id> --json` for each complete usable managed-receipt or live-inventory family.
5. Re-list declarations and report each added id and evidence basis.

The operation is additive and idempotent. Never infer removal from a missing root, partial inventory, different agent host, or compatibility warning. Report partial and incompatible evidence as advice without registration.
