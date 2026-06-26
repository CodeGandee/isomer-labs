## Why

`isomer-srv-env-setup` already routes Topic Workspace setup through Pixi, but its instructions do not yet define how agents should handle native runtimes, shared libraries, activation scripts, or fallback installs while preserving an enclosed environment. Without a clear enclosure policy, an agent may drift into ambient shell state, global package managers, or sudo-backed system mutation that cannot be replayed from the Topic Workspace.

## What Changes

- Add an explicit environment enclosure policy for `skillset/service/isomer-srv-env-setup`.
- Define a dependency-handling ladder: Pixi-managed install first, Pixi-mediated external runtime wiring second, topic-local user-space fallback third, and blocker reporting when setup would require privileged or global mutation.
- Require `derive-gate` to record an environment enclosure strategy in `isomer-env-gate.md`.
- Require `install-deps` to classify dependencies by enclosure strategy before mutating the Topic Workspace environment.
- Require `verify-gate` to treat unrecorded ambient shell state as non-ready, even if a command happens to pass locally.
- Permit explicit runtime wiring through Pixi-run commands, including PATH, library path, compiler path, CUDA variables, package-config variables, and explicitly sourced setup scripts, when the wiring is recorded in the derived gate and command log.
- Allow user-space installation outside Pixi only as a secondary fallback under a topic-local ignored prefix, with commands and paths recorded.
- Forbid sudo, system package manager mutation, global shell profile edits, global Python or Node package installs, `/etc` changes, `ldconfig`, and other machine-global mutations from this skill.

## Capabilities

### New Capabilities

- `isomer-service-env-setup-enclosure`: define the service environment setup skill's environment enclosure policy for Pixi-first dependency setup, explicit runtime wiring, topic-local fallback installs, and no-sudo blockers.

### Modified Capabilities

None.

## Impact

- Affects `skillset/service/isomer-srv-env-setup/SKILL.md`.
- Affects `skillset/service/isomer-srv-env-setup/references/derive-gate.md`, `install-deps.md`, `verify-gate.md`, and likely `setup-for-topic-workspace.md`.
- Adds OpenSpec coverage for environment enclosure behavior in the service env setup skill.
