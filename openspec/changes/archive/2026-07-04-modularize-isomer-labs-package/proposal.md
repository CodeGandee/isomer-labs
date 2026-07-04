## Why

`src/isomer_labs` now follows a PyPI-safe `src/` boundary, but the package root still contains many domain-sized modules that mix Project, Topic Workspace, Team Template, Profile, records, and CLI handler concerns. This makes future refactors risky because import ownership is unclear and large root files keep growing behind architecture-test exemptions.

## What Changes

- Group root-level implementation modules into bounded-context packages such as `core`, `project`, `workspace`, `teams`, and `records`.
- Preserve public CLI command names, JSON output contracts, and package import smoke behavior while updating internal imports to canonical package paths.
- Split large monolithic modules by responsibility, especially `models.py`, `topic_workspace_manifest.py`, `paths.py`, `team_templates.py`, `team_profiles.py`, `validation.py`, `research_records.py`, and `doctor.py`.
- Move CLI command handler implementations out of `cli/app.py` into focused handler modules, leaving `cli/app.py` as command bootstrap, shared option context, and command registration glue.
- Replace broad architecture-test exemptions with enforceable root-module and size limits.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `isomer-python-module-architecture`: Require the Python package to use bounded-context subpackages, keep root modules minimal, and prevent `cli/app.py` from remaining a command-handler monolith.

## Impact

- Affected code: `src/isomer_labs` module layout, internal imports, CLI handler wiring, and architecture tests.
- Affected tests: source architecture tests and any tests that import relocated internal modules.
- Public behavior should remain compatible: CLI command surface, output schemas, and runtime behavior are not intended to change.
- No new runtime dependencies are expected.
