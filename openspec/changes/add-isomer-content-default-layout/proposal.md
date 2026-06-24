## Why

Isomer skills and CLI initialization need one predictable Project-local default for generated material when the user does not provide an output directory. The current built-in Topic Workspace layout still points to `topic-workspaces/<topic-id>/`, which leaves generated Isomer content mixed with ordinary repository content and forces `init-topic` to ask for a path even when a clear topic can be safely placed under a Project default.

## What Changes

- Add `isomer-content/` as the default Project-local root for Isomer-generated content.
- Generate `isomer-content/README.md` and `isomer-content/.gitignore` during `isomer-cli project init`; the `.gitignore` ignores generated content by default while keeping `README.md` and `.gitignore` trackable.
- Move the default Topic Workspace base from `topic-workspaces/` to `isomer-content/topic-ws/`.
- Update `isomer-cli project init`, Workspace Path Resolution defaults, path preview, docs, tests, and operator skills to use `isomer-content/topic-ws/<topic-id>/` for default Topic Workspaces.
- Update `isomer-admin-topic-team-specialize init-topic` so a clear Research Topic without an explicit output directory derives a provisional topic seed under the manifest or built-in Topic Workspace base instead of always asking for a directory.
- Keep Project Manifest registrations as authority; generated directories remain local filesystem material and do not become Research Topic or Topic Workspace registrations unless recorded through supported Isomer surfaces.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `isomer-cli-project-discovery`: `isomer-cli project init` now creates the `isomer-content/` root, records path defaults, and creates the initial Topic Workspace under `isomer-content/topic-ws/<topic-id>/`.
- `workspace-path-resolution`: built-in defaults and path preview now resolve default Topic Workspace roots under `isomer-content/topic-ws/`, and expose the Project generated-content root.
- `isomer-admin-project-manager-skill`: project initialization guidance now reports the `isomer-content/` root and the new default Topic Workspace path.
- `topic-team-specialization-module-skill`: `init-topic` now uses the default Topic Workspace base for clear topics without explicit output directories and reports the derived provisional seed path.

## Impact

- Affected code: `src/isomer_labs/init_project.py`, `src/isomer_labs/paths.py`, `src/isomer_labs/cli/app.py`, manifest validation, and tests under `tests/unit/`.
- Affected docs and skills: `docs/getting-started.md`, `docs/runtime-and-files.md`, `docs/system-design.md`, `docs/isomer-cli.md`, `skillset/operator/isomer-admin-project-mgr/`, and `skillset/operator/isomer-admin-topic-team-specialize/`.
- Existing Projects with explicit Topic Workspace paths remain valid; the change affects new initialization, derived defaults, and guidance.
