# Command Subcommand Structure

## Decision

`isomer-srv-env-setup` should be structured like a single command skill with many short kebab-case subcommands. The top-level `SKILL.md` should stay a lean router with a `Subcommands` table, and executable detail should live in linked reference pages.

## Rationale

The setup workflow has several independently useful stages: resolving the Topic Workspace, reading the source gate, acquiring repos, deriving the operational gate, installing dependencies, and verifying the desired command. A subcommand structure lets users or agents run one stage directly while preserving a default full setup path.

## Subcommands

The revised skill should expose these subcommands:

- `help`: explain the skill and list public subcommands.
- `topic-workspace`: run the full gate-driven Topic Workspace setup workflow; this remains the default when no subcommand is given.
- `resolve-workspace`: resolve Project root, Research Topic, Topic Workspace, Pixi binding, and preconditions.
- `read-gate`: read `user-intent/src/env-gate.md` and identify the runnable target.
- `get-repos`: find, infer, download, or verify required repos under `repos/<repo-name>`.
- `derive-gate`: generate or update `user-intent/derived/isomer-env-gate.md`.
- `install-deps`: infer package sources and install dependencies through the Topic Workspace Pixi environment.
- `verify-gate`: run the desired command through Pixi and report readiness.

## Formatting Rules

Each executable subcommand page should have a `## Workflow` section near the top, written as numbered steps, and should end with a freeform fallback that tells the agent to use its native planning tool when the task does not map cleanly. The entrypoint should route to one subcommand, load that subcommand's reference page, and execute its workflow.

## Implementation Impact

Implementation should create or revise one-level reference pages such as `references/topic-workspace.md`, `references/resolve-workspace.md`, `references/read-gate.md`, `references/get-repos.md`, `references/derive-gate.md`, `references/install-deps.md`, and `references/verify-gate.md`. The existing `topic-workspace` workflow should become the orchestrating full path that calls the step subcommands in order.
