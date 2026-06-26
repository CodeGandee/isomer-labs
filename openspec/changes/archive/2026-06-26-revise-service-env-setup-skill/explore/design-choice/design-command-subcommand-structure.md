# Command Subcommand Structure

## Decision

`isomer-srv-env-setup` should be structured like a single command skill with many short kebab-case subcommands. The top-level `SKILL.md` should stay a lean router with a grouped `Subcommands` section, and executable detail should live in linked reference pages.

## Rationale

The setup workflow has several independently useful stages: resolving the Topic Workspace, reading the source gate, acquiring repos, deriving the operational gate, installing dependencies, and verifying the desired command. A subcommand structure lets users or agents run one stage directly while preserving a default full setup path.

## Subcommand Groups

Procedural subcommands are public single-step workflow actions:

- `resolve-workspace`: resolve Project root, Research Topic, Topic Workspace, Pixi binding, and preconditions.
- `read-gate`: read `user-intent/src/env-gate.md` and identify the runnable target.
- `ensure-repos`: find existing repos or acquire missing required repos under `repos/<repo-name>`.
- `derive-gate`: generate or update `user-intent/derived/isomer-env-gate.md`.
- `install-deps`: infer package sources and install dependencies through the Topic Workspace Pixi environment.
- `verify-gate`: run the desired command through Pixi and report readiness.

Helper subcommands are lower-level commands called by procedural subcommands. The revised skill currently exposes none; future helpers should stay in their own group and out of help unless promoted.

Misc subcommands are public support commands and shortcuts:

- `help`: explain the skill and list public subcommands.
- `setup-for-topic-workspace`: run the full gate-driven Topic Workspace setup workflow; this is the default for concrete setup tasks that do not name a subcommand.

`setup-for-topic-workspace` should select `fast-forward`/`auto` or `step-by-step`/`manual` from the prompt. Fast-forward mode runs the full ordered workflow directly. Step-by-step mode pauses before each step, presents user choices in a compact `Option | Explain | Pros and Cons` table, states the recommended option outside the table with its reason, waits for consent, and then executes one chosen action before continuing.

## Formatting Rules

Each executable subcommand page should have a `## Workflow` section near the top, written as numbered steps, and should end with a freeform fallback that tells the agent to use its native planning tool when the task does not map cleanly. The entrypoint should route to one subcommand, load that subcommand's reference page, and execute its workflow.

## Implementation Impact

Implementation should create or revise one-level reference pages such as `references/setup-for-topic-workspace.md`, `references/resolve-workspace.md`, `references/read-gate.md`, `references/ensure-repos.md`, `references/derive-gate.md`, `references/install-deps.md`, and `references/verify-gate.md`. The entrypoint should present those pages in procedural/helper/misc groups. The existing full setup workflow should become the `setup-for-topic-workspace` path that calls the procedural subcommands in order and switches behavior by execution mode.
