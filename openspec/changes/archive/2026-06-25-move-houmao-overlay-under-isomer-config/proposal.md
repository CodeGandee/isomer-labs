## Why

Isomer currently bootstraps its Project-level Houmao overlay at the Project root as `.houmao/`, which can collide with a user's existing Houmao project in the same repository or workspace. Isomer should keep Houmao as an implementation layer and store Isomer-managed Houmao state under `.isomer-labs/`, where it cannot mix with user-owned Houmao state.

## What Changes

- Redirect Project-level Houmao bootstrap so Isomer passes `<project-root>/.isomer-labs/` as the Houmao project directory.
- Store the Isomer-managed Houmao overlay at `<project-root>/.isomer-labs/.houmao/`.
- Treat root `<project-root>/.houmao/` as user-owned external state: Isomer does not create, modify, inspect, or clean it.
- Update Project init, Project cleanup, path-safety diagnostics, Houmao adapter manifests, CLI output, and operator skill guidance to use the internal overlay path.
- Preserve existing runtime and launch side-effect boundaries: this change moves static/bootstrap state only and does not launch, stop, message, or inspect Houmao managed agents.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `isomer-cli-project-discovery`: Project init and Project-scoped cleanup output must report `.isomer-labs/.houmao/` as the Isomer-managed Houmao overlay and must ignore root `.houmao/`.
- `houmao-cli-adapter-layer`: Project-level Houmao bootstrap must invoke Houmao with `<project-root>/.isomer-labs/` as the redirected project directory and must record the internal overlay separately from per-team adapter material.
- `isomer-project-cleanup`: Cleanup planning and execution must target `.isomer-labs/.houmao/` for `houmao-overlay` and must preserve root `.houmao/`.
- `isomer-admin-project-manager-skill`: Operator guidance must describe the Isomer-managed Houmao overlay as `.isomer-labs/.houmao/` and stop instructing operators to use root `.houmao/` for Isomer Project bootstrap.

## Impact

- Affected code: Project initialization, Houmao bootstrap adapter calls, Project cleanup planning, content-root path-safety diagnostics, adapter link manifest generation, CLI text/JSON output, and unit tests.
- Affected operator material: `skillset/operator/isomer-admin-project-mgr` entrypoint and local reference pages.
- Affected compatibility: existing user-owned root `.houmao/` directories become explicitly outside Isomer ownership. Existing Isomer Projects created before this change may still have root `.houmao/`; new init and cleanup behavior should not delete or reuse that directory automatically.
