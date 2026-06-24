## Why

After Project initialization, users can choose a generated content root, but there is no supported way to change it later. Manual edits to `.isomer-labs/manifest.toml` and filesystem moves are error-prone because registered Topic Workspace paths, managed content policy files, and runtime artifacts have different ownership boundaries.

## What Changes

- Add a Project-scoped content-root relocation command that plans and applies moves for Isomer-managed generated content.
- Update Project Manifest path defaults and registered Topic Workspace paths when they point inside the old generated content root.
- Preserve unknown files under the old content root and report them as unmanaged leftovers instead of moving or deleting them implicitly.
- Warn that existing Workspace Runtime records, Pixi environments, installed packages, adapter runtime material, logs, and other internal runtime files may contain old paths and may need reinstall or reinitialization.
- Keep relocation separate from cleanup: cleanup removes selected managed material, while relocation changes the configured generated content root and moves managed content entries.

## Capabilities

### New Capabilities
- `isomer-project-content-root-relocation`: Defines planning, safety, manifest mutation, managed filesystem moves, unmanaged leftovers, runtime warning boundaries, and output contracts for moving a Project generated content root.

### Modified Capabilities
- `isomer-cli-project-discovery`: Adds the canonical Project-scoped command shape, help, JSON/text output behavior, and discovery expectations for content-root relocation.
- `isomer-admin-project-manager-skill`: Adds operator guidance for moving the generated content root through the supported CLI command, including dry-run review and runtime breakage warnings.

## Impact

- CLI: add a Project-scoped `isomer-cli project content-root move` command with `--to`, `--dry-run`, and `--yes`.
- Project path and manifest code: reuse existing content-root validation rules, add deterministic relocation planning, and atomically rewrite `.isomer-labs/manifest.toml`.
- Filesystem behavior: move only Isomer-managed content policy files and registered Topic Workspace directories that are inside the old content root; leave unmanaged entries behind.
- Runtime behavior: no rewriting of `state.sqlite`, stored path plans, Pixi environments, installed package metadata, adapter runtime records, or logs.
- Tests and docs: add unit coverage for planning, safety refusals, manifest updates, unmanaged leftovers, dry-run behavior, confirmed execution, and operator-skill command guidance.
