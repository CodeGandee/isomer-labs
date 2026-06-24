## Why

`isomer-cli project init` deliberately refuses to overwrite an existing `.isomer-labs/manifest.toml`, but users currently have no supported way to remove Isomer-managed bootstrap material when they need to reinitialize or reset part of a Project. Manual deletion is risky because generated content, Project config, Topic Workspaces, Workspace Runtime state, and the Project-level Houmao overlay have different ownership and safety boundaries.

## What Changes

- Add a Project cleanup command surface that plans and removes selected Isomer-managed Project material.
- Require `--dry-run` support for every destructive cleanup operation, with deterministic text and JSON output that lists planned removals before mutation.
- Support partial cleanup by target part, including Project config, Project-level Houmao overlay, content-root policy files, selected Topic Workspace material, Workspace Runtime material, and a higher-risk whole content-root purge mode.
- Preserve `isomer-cli project init` overwrite refusal; cleanup is the explicit path for removing existing managed material before reinitialization.
- Add safety rules that refuse out-of-project paths, refuse Project-root deletion, compute the removal plan before mutation, and avoid deleting unknown user content unless the user selects an explicit purge option.
- Update the project-manager operator skill so it can route cleanup requests through the supported CLI boundary and explain the dry-run and confirmation posture.

## Capabilities

### New Capabilities

- `isomer-project-cleanup`: Project cleanup planning and deletion for selected Isomer-managed Project material.

### Modified Capabilities

- `isomer-cli-project-discovery`: Expose the cleanup command in the CLI surface, deterministic output, diagnostics, and side-effect boundaries while keeping `project init` overwrite refusal.
- `isomer-admin-project-manager-skill`: Add operator guidance for cleanup, dry-run review, partial removal, and reinitialization workflows.

## Impact

- Affected CLI code: project command registration, CLI options, command dispatch/output helpers, cleanup planning/removal helpers, diagnostics.
- Affected Project surfaces: `.isomer-labs/`, `.houmao/`, selected generated content root, content-root policy files, Topic Workspace directories, Workspace Runtime files and directories.
- Affected tests: CLI cleanup dry-run/apply tests, partial cleanup tests, malformed/missing manifest cleanup tests, path safety tests, operator skill validation tests.
- Affected docs and skills: `docs/isomer-cli.md`, troubleshooting/workflow docs, and `skillset/operator/isomer-admin-project-mgr`.
