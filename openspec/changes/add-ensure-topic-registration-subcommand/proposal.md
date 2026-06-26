## Why

The topic-team specialization skill can create a provisional topic workspace seed, but downstream setup now needs an authoritative Project Manifest-registered Research Topic, Topic Workspace, and environment binding before `isomer-srv-env-setup` can run safely. Without an explicit registration step in the skill flow, agents reach `setup-topic-env` with only a directory under `isomer-content/topic-ws/` and correctly block because the Project Manifest does not point to it.

## What Changes

- Add an `ensure-topic-registration` procedural subcommand to `skillset/operator/isomer-admin-topic-team-specialize`.
- Make `ensure-topic-registration` verify or create the authoritative Research Topic and Topic Workspace registration through supported Isomer CLI/API surfaces, not by hand-editing `.isomer-labs/manifest.toml`.
- Teach the subcommand to verify the active Topic Workspace Pixi binding needed by `isomer-srv-env-setup`, and to report a precise blocker when no supported CLI/API surface exists to create the missing binding.
- Insert `ensure-topic-registration` into the full topic-team flow after `init-topic` and optional `clarify-topic`, before `specialize-team`.
- Re-run or require `ensure-topic-registration` before any step that depends on manifest-backed topic state, especially `setup-topic-env`, profile materialization, validation, and finalization.
- Update help, fast-forward, step-by-step, output contract, and predecessor-artifact guidance so provisional topic seeds do not proceed silently into registration-dependent work.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `topic-team-specialization-module-skill`: add the `ensure-topic-registration` subcommand and require topic registration assurance before registration-dependent specialization and setup steps.

## Impact

- Affects `skillset/operator/isomer-admin-topic-team-specialize/`.
- May affect repository skill validation expectations for the topic-team specialization module skill.
- Does not require changing Isomer CLI topic CRUD behavior in this change; unsupported manifest mutation surfaces should remain blockers in the skill.
