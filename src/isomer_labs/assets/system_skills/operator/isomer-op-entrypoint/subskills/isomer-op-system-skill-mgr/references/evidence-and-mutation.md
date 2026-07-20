# Evidence and Mutation Contract

## Safe CLI Primitives

Use global `isomer-cli` from the working environment. Do not prefix it with a repository-local environment command.

```text
isomer-cli project system-extensions list --json
isomer-cli internals inspect-system-skill-root --skill-root <root> --category extensions [--extension <id>]
isomer-cli internals classify-system-skill-inventory --skill-name <name>... [--inventory-json <file-or-stdin>]
isomer-cli project system-extensions remember <extension-id> --json
isomer-cli --print-json system-skills install --target <host-known-target> --scope <selected-scope> --extension <extension-id>
isomer-cli --print-json system-skills upgrade --target <host-known-target> --scope <selected-scope> --extension <extension-id>
```

The internal commands are read-only, use a versioned payload, and never search for roots or mutate Project declarations. `project system-extensions detect --skill-root <root>` is a Project-facing explicit-root wrapper; without a root it reports catalog and declaration state only. The scoped installer requires a concrete host target. Direct CLI install defaults to project scope when `--scope` is omitted, but this manager always passes `--scope <selected-scope>` to preserve its recorded choice. It selects project scope for a normal Project Operator request and user scope only after explicit user-wide intent.

## Ordered Resolution

Read Project declarations first. A declaration is authoritative Project routing intent, so return `project_manifest` evidence and preserve it even when the current operator lacks the extension. When the requested task needs current-host execution, continue through root and inventory evidence rather than treating the declaration as pack-integrity proof.

Inspect only project-scope roots known to the current agent. First interpret the receipt. Treat `receipt.status=current`, `coverage_status=complete`, `evidence_basis=managed_receipt`, complete welcome and entrypoint projections, and a usable compatibility state as managed v5 evidence. Then interpret explicit-root integrity. `coverage_status=unmanaged_complete` verifies material but does not establish Isomer ownership or permit automatic registration. Receipt v1 through v4 and legacy flat rows identify migration candidates without proving public-pair integrity. Partial, invalid, malformed, unsupported, drifted, obsolete, and newer-than-CLI results require advice, upgrade, or repair rather than silent registration.

Last, classify the live skill inventory. Use names from the host-provided inventory, not a guessed directory listing. `coverage_status=welcome_seen`, `entrypoint_seen`, or `public_pair_seen` records which public names are visible, but receipt ownership and protected integrity remain unverified. `coverage_status=legacy_observed` means old flat member or alias names are visible. None of these statuses establishes a complete pack or permits `remember`.

## Registration Boundary

Call `remember` only during Project initialization reconciliation, explicit reconciliation, authorized extension installation, repair that explicitly includes registration, or a concrete extension-use request that implies Project bookkeeping. Repeated calls are safe and should report whether the declaration changed.

Never call `forget` automatically. Absence in the current session does not prove absence in another agent host.

## Partial Outcomes

Report installation and registration independently. If files are installed but `remember` fails, retain the installation, report the Project as needing registration, and retry inspection plus `remember` on the next run. Do not reinstall a complete compatible family merely to retry bookkeeping.

After installation or upgrade, classify a refreshed inventory if the host supports refresh. Otherwise state that the current agent session may cache old discovery, require a host refresh, and recommend a new turn, thread, or host-native reload before claiming live usability.

Read `skill_root` from the successful installation JSON result and use that exact path for explicit-root verification. If the host target is unknown, or the requested destination is an arbitrary plugin, extra, or custom root, block the scoped installation instead of guessing a path.
