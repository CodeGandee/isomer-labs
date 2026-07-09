## Why

The current name `isomer-op-toolbox-creator` undersells the skill's actual responsibility: it creates Toolboxes, but it also converts skills, inserts callbacks, defines Runtime Params, installs, inspects, updates, disables, uninstalls, and explains effective Toolbox state. Rename it to `isomer-op-toolbox-mgr` before the pending packaged skill becomes a stable public operator surface.

## What Changes

- Rename the packaged operator skill from `isomer-op-toolbox-creator` to `isomer-op-toolbox-mgr`.
- Rename the skill folder, frontmatter `name`, `agents/openai.yaml` display/default prompt, operator README entry, packaged manifest entry, package asset tests, and OpenSpec artifacts that still use the creator name.
- Update the skill title and user-facing wording from "Toolbox Creator" to "Toolbox Manager" where the broader management responsibility is meant.
- Preserve the existing command surface: `author-toolbox`, `convert-skill`, `insert-callback`, `define-runtime-params`, `manage-toolbox`, `identify-insertion-points`, and the grouped helper commands.
- Do not add a compatibility shim, alias folder, or duplicate active packaged skill for `isomer-op-toolbox-creator`.

## Capabilities

### New Capabilities
- `isomer-op-toolbox-mgr-skill`: packaged operator skill guidance for creating and managing project-local Toolboxes under the corrected manager name.

### Modified Capabilities
- `packaged-system-skills`: package the manager skill path in the core group instead of the creator skill path.

## Impact

- Affected assets: `src/isomer_labs/assets/system_skills/operator/isomer-op-toolbox-mgr/`, `src/isomer_labs/assets/system_skills/manifest.toml`, `src/isomer_labs/assets/system_skills/operator/README.md`.
- Affected tests: package asset tests that assert the core manifest entry, materialized path, command pages, and frontmatter identity.
- Affected planning/context: pending `create-toolbox-creator-system-skill` artifacts and feature design references should be updated or superseded so active instructions point to `isomer-op-toolbox-mgr`.
- No CLI, schema, runtime behavior, or Toolbox command behavior changes.
