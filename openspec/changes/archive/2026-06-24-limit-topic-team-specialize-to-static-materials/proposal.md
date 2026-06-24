## Why

`isomer-admin-topic-team-specialize` is drifting across two boundaries: producing durable Topic Team material and operating live teams. Topic Team Specialization should stay focused on static preparation artifacts and durable setup state, while runtime launch and adapter operation belong to later execution workflows.

## What Changes

- Remove live team launch from the `isomer-admin-topic-team-specialize` public workflow and local subcommand set.
- Keep `setup-topic-env` in scope because installed packages, environment files, setup commands, and validation records are durable static preparation for the Topic Team.
- Keep `setup-agent-workspace` only as static Agent Workspace directory and boundary preparation, not Agent Instance creation or Workspace Runtime registration.
- Reword validation, finalization, help, fast-forward, step-by-step, helper references, output fields, guardrails, and validator expectations so they stop at static Topic Team material readiness.
- Move runtime launch, Houmao Execution Adapter launch, Agent Team Instance creation, gateway, process, and live run concerns out of this skill's normal flow.

## Capabilities

### New Capabilities

### Modified Capabilities
- `topic-team-specialization-module-skill`: Limit the module skill to static Topic Team material and durable setup preparation, while removing live launch/runtime operation from its subcommands and workflow.

## Impact

- Affected skill files: `skillset/operator/isomer-admin-topic-team-specialize/SKILL.md`, `references/help.md`, `references/fast-forward.md`, `references/step-by-step.md`, `references/setup-agent-workspace.md`, `references/validate-topic-team.md`, `references/finalize-topic-team.md`, `references/resolve-project.md`, `references/resolve-context.md`, `references/draft-profile.md`, `references/materialize-profile.md`, and removal of `references/launch-team.md`.
- Affected validators and tests: `scripts/validate_skillsets.py` and `tests/unit/test_validate_skillsets.py`.
- Affected OpenSpec artifacts for the already-active topic-team flow may need compatible updates so the expected public subcommand list no longer includes runtime launch.
