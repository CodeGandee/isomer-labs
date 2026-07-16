## Why

Project-local installation is already the safe default in the system-skill manager, but the low-level CLI still rejects an install when `--scope` is omitted. Defaulting only `system-skills install` to Project scope removes routine boilerplate while preserving an explicit opt-in for user-wide mutation.

## What Changes

- Make `isomer-cli system-skills install --target <target>` behave as `--scope project` when `--scope` is omitted.
- Preserve explicit `--scope project` and `--scope user` behavior, with explicit user scope remaining the only route to user-wide installation.
- Keep `system-skills status`, `upgrade`, and `uninstall` scope-explicit so inspection, refresh, and removal never select a root implicitly.
- Report the effective `project` scope, exact-current-working-directory target root, target-scope bindings, and receipt metadata identically for omitted and explicit Project scope.
- Update CLI help, extension discovery templates, packaged operator guidance, public documentation, changelog guidance, and validation coverage to describe the install-only default accurately.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `system-skill-installer-cli`: Change the install command from requiring an explicit scope to defaulting omitted scope to `project`, while preserving explicit scope requirements for the other target-resolving commands.

## Impact

This change affects the Click option composition in `src/isomer_labs/cli/commands/system_skills.py`, install command help and structured discovery output, system-skill CLI and documentation tests, the packaged `isomer-op-system-skill-mgr` guidance, README and documentation examples, and the changelog. It does not change target-root resolution, installation receipts, projection modes, selection semantics, arbitrary-root policy, or package dependencies.
