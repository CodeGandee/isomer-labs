## Why

Fresh Project initialization now has a generated content root, but users cannot choose its location during `isomer-cli project init`. This forces them to accept `isomer-content/` and hand-edit the Project Manifest afterward when they already know they want generated Isomer material under a different project-local directory.

## What Changes

- Add `isomer-cli project init --content-dir <content-dir>` to choose the Project generated-content root during fresh initialization.
- When `--content-dir` is supplied, initialize that directory with the same generated `README.md` and `.gitignore` policy files used by the default content root.
- Derive the default Topic Workspace base from the selected content root as `<content-dir>/topic-ws` and create the first Topic Workspace under `<content-dir>/topic-ws/<topic-id>/`.
- Write Project Manifest `[paths]` defaults using the supplied content root and derived Topic Workspace base.
- Reject content roots that resolve outside the Project root, inside `.isomer-labs/`, or collide unsafely with the Project Config Directory or Houmao overlay.
- Keep the existing default behavior unchanged when `--content-dir` is omitted.
- Update project-manager operator guidance and docs so init-project can explain and use the new option.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `isomer-cli-project-discovery`: Project initialization accepts a content-root selector and records matching path defaults.
- `isomer-admin-project-manager-skill`: project initialization guidance describes the optional content directory argument and reports custom generated-content roots.

## Impact

- Affected CLI/code: `src/isomer_labs/cli/commands/project.py`, `src/isomer_labs/cli/app.py`, `src/isomer_labs/init_project.py`, and shared generated-content layout helpers.
- Affected validation/tests: CLI init tests for custom content roots, invalid content roots, JSON/text output, and failure no-leftover behavior.
- Affected docs/skills: `docs/getting-started.md`, `docs/isomer-cli.md`, `docs/runtime-and-files.md`, `docs/workflows.md`, `skillset/operator/isomer-admin-project-mgr/`, and local operator skill validation fixtures if they assert init command shapes.
