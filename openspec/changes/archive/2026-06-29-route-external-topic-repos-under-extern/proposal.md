## Why

Additional topic repositories currently default to `repos/<name>`, which makes them look like peers of `repos/topic-main` even though `topic-main` is the primary development and collaboration repository. Moving non-main topic repositories under `repos/extern/...` makes their role clear while preserving semantic `topic.repos.*` labels as the real path contract.

## What Changes

- Keep `topic.repos.main` defaulting to `repos/topic-main`.
- Change non-main topic repository defaults created by `project repos create` to `repos/extern/<repo-label-path>`.
- Treat non-main `topic.repos.*` repositories as topic-local external/supporting repositories: downloaded or acquired for topic setup, inspectable and modifiable when the gate or user authorizes it, but not the primary Agent Workspace worktree source.
- Update environment setup and workspace-manager skill guidance to resolve non-main repositories through semantic labels and to describe the new default external repository location.
- Update documentation and tests that currently show or assert `repos/<group>/<repo-name>` for additional topic repositories.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `workspace-path-resolution`: non-main grouped topic repositories use the `repos/extern/...` default layout when created by repository helper commands.
- `topic-workspace-manifest`: repository creation guidance and manifest examples distinguish `topic.repos.main` from non-main grouped topic repositories.
- `isomer-service-env-setup-skill`: independent topic setup repositories resolve to semantic `topic.repos.*` paths, defaulting under `repos/extern/...` for non-main repositories.
- `operator-admin-skills`: operator skill guidance describes additional topic repositories as external/supporting repositories under the semantic storage contract.
- `isomer-documentation-system-guide`: public documentation examples describe the new default path and role split.

## Impact

- CLI: `project repos create` default path derivation and guardrails for the reserved main repository label.
- Tests: CLI and documentation/skill validation tests that assert additional repository paths or required wording.
- Docs: getting started, CLI reference, concepts, Topic Workspace definition, runtime/files, system design, and assumptions pages.
- Skills: `isomer-srv-topic-env-setup` and `isomer-admin-topic-workspace-mgr` references that mention independent repository roots.
