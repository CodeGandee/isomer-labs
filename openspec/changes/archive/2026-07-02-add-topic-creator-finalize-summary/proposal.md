## Why

`isomer-admin-topic-creator` currently reaches a handoff-shaped end state, but the user-facing job is better framed as preparing a Topic Workspace and honestly reporting its readiness. A terminal `finalize` step should validate the ladder, write a durable workspace summary, and print ready/verified/blocked status without routing the user to a next research action.

## What Changes

- Add a `finalize` subcommand to Topic Creator as the terminal readiness validation and reporting step.
- Add a `step-by-step` subcommand as the guided counterpart to `fast-forward`.
- Add a `run-to` subcommand as a targeted fast-forward mode that runs the main workflow up to a user-specified procedural subcommand.
- Remove `start-manual-research` from Topic Creator's command surface and fast-forward path.
- Make `fast-forward` end at `finalize` after topic env setup, optional actor setup, and research bootstrap.
- Make `step-by-step` walk the same main workflow as `fast-forward`, but before each step it explains the next action, lists decisions or options when they exist, recommends a choice, and waits for user acknowledgement before proceeding.
- Make `run-to <procedural-subcommand>` execute the same readiness ladder as `fast-forward` and stop before the target step by default, including the target step only when the user explicitly asks for inclusive execution.
- Make `finalize` write `<topic-workspace>/isomer-topic-workspace-summary.md` and print a compact status report with `ready`, `verified`, and `blocked` sections.
- Add a semantic path label for the summary, proposed as `topic.workspace.summary`, so skills resolve the summary path instead of hard-coding it.
- Keep actor env readiness optional: missing actor readiness blocks only when actors were requested or the default operator actor was not explicitly opted out.
- Remove next-step routing from Topic Creator's terminal output; it reports state and blockers, but does not recommend a next v2 skill or manual research route.

## Capabilities

### New Capabilities
- `topic-creator-finalize-summary`: Topic Creator terminal finalize behavior, summary contents, command-surface changes, and no-next-route reporting.
- `topic-creator-step-by-step`: Topic Creator guided execution mode that advances the main workflow one acknowledged step at a time.
- `topic-creator-run-to`: Topic Creator targeted fast-forward mode that stops before a selected procedural subcommand by default and can include that subcommand on explicit request.

### Modified Capabilities
- `manual-research-topic-workflow`: Human-orchestrated preparation should end in a workspace readiness summary rather than start-pack handoff routing.
- `workspace-path-resolution`: Add `topic.workspace.summary` for `<topic-workspace>/isomer-topic-workspace-summary.md`.
- `operator-admin-skills`: Operator skill validation should require the new `finalize`, `step-by-step`, and `run-to` commands and reject stale `start-manual-research` Topic Creator command guidance.

## Impact

- Affected skill files: `skillset/operator/isomer-admin-topic-creator/**`.
- Affected validation and tests: `scripts/validate_skillsets.py`, `tests/unit/test_validate_skillsets.py`, and Topic Creator contract tests.
- Affected storage/path catalog: Workspace Path Resolution semantic surfaces and path-resolution tests for `topic.workspace.summary`.
- No lower-level service setup ownership changes: Project setup, topic env setup, actor topology, and v2 bootstrap remain delegated to their existing owners.
