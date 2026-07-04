## Why

Project Operators sometimes need to take over work assigned to a Topic Actor or Agent without launching that worker. Today the operator can manually change directories, but there is no official skill that resolves the target identity, uses the correct actor or agent workspace as cwd, and remembers whether the switch is only for one task or should persist for the current operator session.

## What Changes

- Add a new operator skill named `isomer-op-switch-identity`.
- Support switching the Project Operator's working identity posture to a selected Topic Actor or Agent.
- Require each switch to resolve the target workspace through Isomer context and Workspace Path Resolution rather than hand-built paths.
- Support non-persistent switches for one requested task and persistent switches that remain active until the user switches again or resets identity.
- Add `act-as` for one-time execution of the following prompt as a selected identity, with automatic restoration afterward.
- Require switched work to plan and run from the target actor or agent workspace cwd by default.
- Preserve provenance language: the Project Operator is working as the selected identity posture, not proving that a launched Agent Instance or Topic Actor process actually ran.
- Follow `$imsight-agent-skill-handling create` conventions for skill shape: minimal `SKILL.md`, `agents/openai.yaml`, concise numbered workflow with fallback, `Use when...` description, and command detail pages only where needed.

## Capabilities

### New Capabilities
- `operator-switch-identity-skill`: Defines the `isomer-op-switch-identity` operator skill, its target resolution, persistence modes, cwd behavior, provenance rules, and skill-creation structure.

### Modified Capabilities
- `operator-admin-skills`: Adds `isomer-op-switch-identity` to the active operator skill inventory and validation expectations.

## Impact

- Adds `src/isomer_labs/assets/system_skills/operator/isomer-op-switch-identity/` and packaged manifest entries.
- May add or mirror `skillset/operator/isomer-op-switch-identity/` if the repository keeps source skillset and packaged assets in sync for operator skills.
- Updates operator skill validation so the new skill is recognized and checked.
- Updates operator docs or manifests that list active operator skills.
- Does not add a new CLI command, persistent storage schema, or runtime identity record in this change.
