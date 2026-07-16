# Evidence and Mutation Contract

## Safe CLI Primitives

Use global `isomer-cli` from the working environment. Do not prefix it with a repository-local environment command.

```text
isomer-cli project system-extensions list --json
isomer-cli internals inspect-system-skill-root --skill-root <root> --category extensions [--extension <id>]
isomer-cli internals classify-system-skill-inventory --skill-name <name>... [--inventory-json <file-or-stdin>]
isomer-cli project system-extensions remember <extension-id> --json
isomer-cli --print-json system-skills install --target <host-known-target> --scope <selected-scope> --extension <extension-id>
```

The internal commands are read-only, use a versioned payload, and never search for roots or mutate Project declarations. `project system-extensions detect --skill-root <root>` is a Project-facing explicit-root wrapper; without a root it reports catalog and declaration state only. The scoped installer requires a concrete host target. Direct CLI install defaults to project scope when `--scope` is omitted, but this manager always passes `--scope <selected-scope>` to preserve its recorded choice. It selects project scope for a normal Project Operator request and user scope only after explicit user-wide intent.

## Ordered Resolution

Read Project declarations first. A declaration is authoritative claimed state, so return `project_manifest` evidence without demanding a matching root or live inventory. Preserve it even when the current operator lacks the extension.

For an undeclared extension, inspect only project-scope roots known to the current agent. Treat `coverage_status=complete` with `managed_receipt` and a usable compatibility state as managed evidence. Legacy, unmanaged, partial, invalid, malformed, drifted, obsolete, and newer-than-CLI results require advice or repair rather than silent registration.

If explicit roots do not establish the extension, classify the live skill inventory. Use names from the host-provided inventory, not a guessed directory listing. A family is usable only when `coverage_status=complete`; keep `live_inventory` visible as the evidence basis.

## Registration Boundary

Call `remember` only during Project initialization reconciliation, explicit reconciliation, authorized extension installation, repair that explicitly includes registration, or a concrete extension-use request that implies Project bookkeeping. Repeated calls are safe and should report whether the declaration changed.

Never call `forget` automatically. Absence in the current session does not prove absence in another agent host.

## Partial Outcomes

Report installation and registration independently. If files are installed but `remember` fails, retain the installation, report the Project as needing registration, and retry inspection plus `remember` on the next run. Do not reinstall a complete compatible family merely to retry bookkeeping.

After installation, classify a refreshed inventory if the host supports refresh. Otherwise state that a host refresh is required and recommend a new turn, thread, or host-native reload.

Read `skill_root` from the successful installation JSON result and use that exact path for explicit-root verification. If the host target is unknown, or the requested destination is an arbitrary plugin, extra, or custom root, block the scoped installation instead of guessing a path.
