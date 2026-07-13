## Why

System-extension availability depends on the working agent's live skill inventory and provider-owned discovery roots, context that `isomer-cli` does not possess and cannot safely infer as agent tools evolve. Requiring users to install an extension and separately remember it in every Project creates avoidable failures, while hard-coded CLI root scanning still cannot distinguish the active operator from unrelated installations.

## What Changes

- Add a core `isomer-op-system-skill-mgr` skill that owns agent-guided system-skill inspection, additive Project extension reconciliation, operator-managed extension installation, and refresh guidance.
- Teach operator workflows to resolve extensions in this order: trust Project declarations, inspect Isomer receipts in agent-supplied project skill roots, then classify the live skill inventory by packaged catalog names.
- Add a read-only `isomer-cli internals inspect-system-skill-root --skill-root <path>` primitive that hides receipt filenames and schemas, catalog membership, projection shapes, symlink handling, and version compatibility from agents.
- Add an inventory-classification primitive so an agent can submit host-visible skill names or paths without remembering extension-family membership.
- Make operator-controlled Project initialization and extension installation register complete detected extensions by default unless the user opts out, using existing idempotent Project registration primitives.
- Keep direct CLI Project initialization, low-level skill installation, and explicit-root inspection conservative: they do not guess provider roots or mutate extension declarations automatically.
- Replace CLI-side default scanning of hard-coded project or user skill roots with explicit-root inspection orchestrated by system skills.
- Treat reconciliation as additive. Missing skills in one operator environment never cause automatic declaration removal.

## Capabilities

### New Capabilities

- `isomer-op-system-skill-mgr-skill`: Defines the core operator owner skill, its detection, reconciliation, installation, status, and repair subcommands, and its use of live agent inventory.
- `isomer-internal-system-skill-inspection`: Defines stable, read-only, explicit-root and explicit-inventory CLI primitives for receipt-backed and live-inventory extension classification.

### Modified Capabilities

- `operator-system-extension-declarations`: Changes extension registration from a second manual installation step into additive operator-managed bookkeeping with a declaration-first trust order.
- `isomer-op-entrypoint-skill`: Routes system-skill management to the new owner and trusts Project declarations before fallback discovery.
- `isomer-admin-project-manager-skill`: Reconciles extensions after operator-controlled Project initialization while preserving direct CLI initialization as conservative.
- `packaged-system-skills`: Adds the system-skill manager to the packaged core group and catalog.
- `isomer-cli-project-discovery`: Removes hard-coded skill-root discovery and declaration mutation from the direct Project initialization boundary.

## Impact

The change affects packaged operator skills and validation, the system-skill catalog, CLI command registration and JSON contracts, receipt-backed installer inspection helpers, Project extension registration guidance, Project initialization reporting, documentation, and focused unit tests. It revises the routing and initialization decisions in the unarchived `detect-versioned-system-extensions` change; that change should be archived or synchronized first so this delta applies in order.
