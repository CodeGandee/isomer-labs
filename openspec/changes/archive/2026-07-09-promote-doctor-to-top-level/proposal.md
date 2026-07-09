## Why

`doctor` diagnoses the local Isomer environment as a whole: required host tools, optional Houmao availability, Project discovery, and Research Topic Workspace readiness when a Project exists. Keeping it under `project` makes the command harder to find and gives users and agents the wrong mental model.

## What Changes

- **BREAKING**: Move the canonical doctor command from `isomer-cli project doctor` to `isomer-cli doctor`.
- **BREAKING**: Remove `project doctor`; invoking it shall fail as an unknown Project subcommand rather than running a compatibility alias.
- Add optional host Houmao diagnostics to doctor output by checking the `houmao-mgr` command boundary when available.
- Always perform Project discovery and report whether a Project exists.
- By default, detect and scan registered Topic Workspaces when a Project exists.
- Add repeatable `--with-topic <research-topic-id>` filters; when one or more filters are provided, `doctor` scans only the requested Research Topics instead of all detected topics.
- Keep doctor read-only: it must not create Project files, Workspace Runtime state, Topic Workspace artifacts, Houmao state, or Pixi environments.
- Update CLI help, examples, docs, tests, self-query guidance, and bundled system skills so they reference `isomer-cli doctor`.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `isomer-cli-doctor-diagnostics`: change the command contract from `isomer-cli project doctor` to `isomer-cli doctor`, remove compatibility expectations, add optional Houmao host checks, and define default/all versus filtered topic scan behavior.
- `isomer-cli-project-discovery`: update the top-level and Project command surfaces so `doctor` is global and absent from `project`.
- `isomer-admin-welcome-skill`: update safe diagnostic command guidance to use top-level `doctor`.
- `isomer-op-entrypoint-skill`: update safe context discovery guidance to use top-level `doctor`.

## Impact

- CLI registration in `src/isomer_labs/cli/app.py` and doctor command registration in `src/isomer_labs/cli/commands/doctor.py`.
- Doctor diagnostics model, topic scan selection, and rendering in `src/isomer_labs/project/doctor.py`.
- CLI examples, self-query usage strings, documentation, system skill assets, and specs that mention `project doctor`.
- Unit tests in `tests/unit/test_isomer_cli.py` and related validation tests that assert command coverage or skill text.
