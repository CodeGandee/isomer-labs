## Why

The system-skill CLI currently exposes `--home` as an exact skill-root override even though the name suggests a user or tool home directory, and it mixes project-local defaults with a user-global Codex default. Callers must know terminal tool-specific skill subdirectories and cannot state whether an installation is intended for one Project or the current OS user.

## What Changes

- **BREAKING** Remove `--home` from `system-skills install`, `status`, `upgrade`, and `uninstall`.
- **BREAKING** Require `--scope user|project` on commands that resolve system-skill installation targets.
- Resolve `project` scope from the current working directory and each target's supported project skill directory.
- Resolve `user` scope from the current user's target-supported global skill directory, honoring target-specific home environment variables where the host defines them.
- Handle target aliases that resolve to the same physical skill root without duplicate mutation or contradictory receipts.
- Record and report the selected scope with the resolved skill root so status, upgrade, and uninstall operate against the same explicit target-scope contract.
- Revise operator system-skill management guidance to select an explicit target and scope instead of passing a host-known root through `--home`.
- Update CLI help, documentation, tests, and migration guidance for the breaking command syntax.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `system-skill-installer-cli`: Replace exact `--home` overrides and mixed implicit roots with required target-and-scope resolution, scope-aware receipts, and safe handling of shared physical roots.
- `isomer-op-system-skill-mgr-skill`: Replace `--home`-based extension installation guidance with explicit user or project scope selection while preserving verification, registration, and host-refresh behavior.

## Impact

This change affects `src/isomer_labs/skills/installer.py`, system-skill receipt and result models, Click options and renderers under `src/isomer_labs/cli/commands/system_skills.py`, packaged `isomer-op-system-skill-mgr` guidance, unit and validation tests, and system-skill CLI documentation. Existing automation that supplies `--home` or omits `--scope` must migrate. Existing v2 receipts remain readable, while new mutations write scope-aware receipt metadata.
