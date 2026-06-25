## 1. Path Model and Project Init

- [x] 1.1 Add or reuse helper functions that derive the Isomer-managed Houmao project directory as `<project-root>/.isomer-labs/` and the overlay as `<project-root>/.isomer-labs/.houmao/`.
- [x] 1.2 Update Project initialization to create or prepare `.isomer-labs/` before Houmao bootstrap, pass `.isomer-labs/` to the Houmao project init command, and verify `.isomer-labs/.houmao/`.
- [x] 1.3 Update Project initialization results and CLI text/JSON output to distinguish the Houmao project directory from the Houmao overlay path.
- [x] 1.4 Ensure an existing root `.houmao/` does not block initialization and is left untouched as external user-owned Houmao state.

## 2. Cleanup and Path Safety

- [x] 2.1 Update `isomer-cli project cleanup --part houmao-overlay` to target `.isomer-labs/.houmao/` and preserve root `.houmao/`.
- [x] 2.2 Update bootstrap cleanup planning so Project config, internal Houmao overlay, content policy files, and known Topic Workspaces are planned without double-removing nested `.isomer-labs/.houmao/`.
- [x] 2.3 Update malformed-manifest and missing-manifest cleanup authority paths to use `.isomer-labs/.houmao/` and skip root `.houmao/`.
- [x] 2.4 Update content-root purge and generated-content relocation safety checks so `.isomer-labs/`, `.isomer-labs/.houmao/`, and root `.houmao/` receive correct refusal diagnostics.

## 3. Houmao Adapter and Manifests

- [x] 3.1 Update Project-level Houmao bootstrap call sites to pass the internal Houmao project directory rather than the Project root.
- [x] 3.2 Update adapter link manifest defaults so new manifests record the internal Houmao project directory and do not default to root `.houmao/`.
- [x] 3.3 Update read-only Houmao project status and reconciliation helpers to use the internal Houmao project directory when deriving Project-level state.
- [x] 3.4 Preserve existing per-Agent Team Instance adapter material paths under Topic Workspaces.

## 4. Operator Skill Guidance

- [x] 4.1 Update `skillset/operator/isomer-admin-project-mgr/SKILL.md` and local references to describe `.isomer-labs/.houmao/` as the Isomer-managed Houmao overlay.
- [x] 4.2 Update project-manager init, check, cleanup, concepts, runtime-boundary, help, and CLI-boundary references so they do not instruct operators to use root `.houmao/` as Isomer-owned state.
- [x] 4.3 Ensure the skill still keeps required execution guidance inside its own skill directory and continues to use `isomer-cli project ...` command shapes.

## 5. Tests and Validation

- [x] 5.1 Update fake Houmao command behavior and Project init tests to create and assert `.isomer-labs/.houmao/`.
- [x] 5.2 Add or update tests showing root `.houmao/` is preserved by init and cleanup.
- [x] 5.3 Update cleanup, content-root safety, adapter manifest, CLI JSON output, and project-manager skill validation tests for the internal overlay path.
- [x] 5.4 Run `openspec validate move-houmao-overlay-under-isomer-config --strict`.
- [x] 5.5 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
