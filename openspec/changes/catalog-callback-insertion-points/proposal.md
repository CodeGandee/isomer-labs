## Why

Toolbox authors need a reliable `isomer-cli` query for callback insertion points, but the current implementation only validates hardcoded `begin` and `end` stages against active packaged skill names. Future users may install only selected system extensions, or manually copy extension skills into their operator, so Isomer needs catalog-backed discovery plus a user-declared Project record of which optional system extensions are meaningful for the Project operator.

## What Changes

- Add manifest-declared callback insertion point metadata to packaged system skills, with stage definitions and per-skill insertion point declarations stored in `src/isomer_labs/assets/system_skills/manifest.toml`.
- Distinguish always-available core system skills from optional system extension groups in the packaged system-skill manifest.
- Add Project Manifest support for user-declared operator system extensions, so users can ask Isomer to remember that extensions such as `deepsci` are installed in the Project operator.
- Add CLI commands to list known system extensions and remember or forget Project-declared operator system extensions.
- Add a callback insertion-point query command that lists core insertion points plus Project-declared extension insertion points by default, with filters for explicit extensions or all catalog extensions.
- Update callback and Toolbox callback validation to use manifest-declared insertion points instead of accepting every active packaged system skill for every hardcoded stage.

## Capabilities

### New Capabilities
- `operator-system-extension-declarations`: Project Manifest storage and CLI operations for user-declared operator system extensions.

### Modified Capabilities
- `packaged-system-skills`: Packaged system-skill manifests declare core versus extension groups, callback stages, and per-skill callback insertion points.
- `user-skill-callbacks`: Callback insertion-point validation and query behavior use the packaged catalog and Project-declared operator extensions.
- `toolbox-callback-manifests`: Toolbox callback target validation uses manifest-declared callback insertion points.
- `isomer-cli-project-discovery`: Project CLI help and command behavior expose system-extension memory and callback insertion-point discovery.

## Impact

- Affected package assets: `src/isomer_labs/assets/system_skills/manifest.toml`.
- Affected Python modules: packaged system-skill asset loading, Project Manifest parsing and writing, callback registry validation, Toolbox callback manifest validation, and project CLI command handlers.
- Affected CLI surface: new system-extension memory commands and a read-only callback insertion-point query command.
- Affected docs and tests: CLI reference, packaged system-skill asset tests, callback validation tests, Toolbox callback tests, Project Manifest tests, and CLI tests.
