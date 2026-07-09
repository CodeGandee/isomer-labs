## Why

`isomer-op-toolbox-mgr` exists as an active operator skill, but `isomer-op-welcome` and `isomer-op-entrypoint` do not expose it as an owner workflow. Users can only find Toolbox work by directly naming the skill or reading lower-level operator docs, which breaks the intended welcome-menu and route-and-proceed flow.

## What Changes

- Add Toolbox authoring, conversion, installation, callback insertion, Runtime Param, insertion-point, and effective-state work to the welcome skill's active owner workflow guidance.
- Add `isomer-op-toolbox-mgr` to the entrypoint operator route index and route-precedence guidance for concrete Toolbox tasks.
- Add Toolbox CLI command families to entrypoint CLI routing so explicit `isomer-cli project toolboxes`, `skill-callbacks`, and `toolbox-params` requests are discoverable.
- Keep Toolbox work separate from `isomer-misc-tool-packs`; installable toolset guidance remains an explicit misc helper route, while project-local Toolbox management routes to `isomer-op-toolbox-mgr`.
- Update both source skillset copies and packaged system-skill asset copies so installed operators and repository skill material agree.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `isomer-admin-welcome-skill`: Welcome guidance must expose Toolbox management as an active owner workflow while staying read-only.
- `isomer-op-entrypoint-skill`: Entrypoint routing must recognize Toolbox tasks, route them to `isomer-op-toolbox-mgr`, and index the related CLI command families.
- `operator-admin-skills`: Operator skillset documentation and active-owner inventory must include `isomer-op-toolbox-mgr` consistently.

## Impact

- Affected skill files under `skillset/operator/isomer-op-welcome/` and `skillset/operator/isomer-op-entrypoint/`.
- Matching packaged asset files under `src/isomer_labs/assets/system_skills/operator/isomer-op-welcome/` and `src/isomer_labs/assets/system_skills/operator/isomer-op-entrypoint/`.
- OpenSpec delta specs for the welcome, entrypoint, and operator-admin capability contracts.
- No Python runtime behavior, schema, CLI implementation, or dependency changes.
