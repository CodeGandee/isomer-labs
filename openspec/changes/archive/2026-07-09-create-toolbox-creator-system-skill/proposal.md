## Why
Isomer now has accepted Toolbox concepts for callback manifests, callback insertion points, runtime params, and Toolbox registration, but operators do not yet have a packaged system skill that turns those mechanics into a practical authoring and management workflow.

The design overview at `context/features/2026-07-08-toolbox-creator-skill/design/isomer-op-toolbox-mgr/design-overview.md` defines the intended operator-facing skill. This change creates that system skill as packaged guidance while reusing the existing `isomer-cli` Toolbox, callback, runtime-param, and path-safety surfaces.

## What Changes
- Add packaged operator skill `isomer-op-toolbox-mgr` under `operator/` and include it in the packaged system-skill manifest.
- Define concise skill instructions for authoring, converting, installing, inspecting, updating, disabling, and uninstalling project-local Toolboxes.
- Provide procedural subcommands for `author-toolbox`, `convert-skill`, `insert-callback`, `define-runtime-params`, `manage-toolbox`, and `identify-insertion-points`.
- Provide grouped helper subcommand guidance for Toolbox source authoring, callback declaration edits, runtime-param edits, and effective-state inspection.
- Require the skill to use canonical Toolbox language, scope-aware reporting, safe project-local path handling, secret hygiene, `isomer-cli` validation, and the shared Essential Output / Complete Output convention.
- Do not add or change Toolbox schemas, callback registry semantics, runtime-param resolution, or CLI command behavior.

## Capabilities

### New
- `isomer-op-toolbox-mgr-skill`: packaged operator skill guidance for creating and managing project-local Toolboxes.

### Modified
- `packaged-system-skills`: include the new operator skill in the packaged core system-skill asset inventory.

## Impact
- Affected specs: `isomer-op-toolbox-mgr-skill`, `packaged-system-skills`.
- Affected code/assets: `src/isomer_labs/assets/system_skills/operator/isomer-op-toolbox-mgr/`, `src/isomer_labs/assets/system_skills/manifest.toml`, and package asset tests or validators that assert packaged skill inventory.
- Existing Toolbox CLI, manifest, callback, runtime-param, and workspace path behavior remains unchanged.
