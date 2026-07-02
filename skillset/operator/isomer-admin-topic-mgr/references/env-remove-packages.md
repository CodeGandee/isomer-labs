# Env Remove Packages

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the selected Project, Research Topic, Topic Workspace, Pixi manifest, Pixi environment, and semantic paths through `storage-resolve`.
2. Load the removal request from the prompt or a named Markdown, YAML, JSON, TOML, requirements-style, or copied blocker file.
3. Infer package names, package ecosystem, removal purpose, dependent workflows, requester skill, and desired post-removal verification checks.
4. Plan a Pixi-scoped removal route and identify likely dependency, lockfile, and gate risks before mutation.
5. Mutate only after clear operator intent, using Pixi-bound commands for the selected Topic Workspace manifest and environment.
6. Verify that relevant topic, actor, agent, figure, document, PPTX, CLI, or task-specific checks still pass after removal.
7. Report removed, not-present, skipped, failed, and blocked packages with commands, changed files, verification evidence, repair guidance, and next action.

If the user's task does not map cleanly to these steps, produce an inspect-only removal plan and ask for missing package names or mutation approval.

## Output

Report `status`, `topic`, `pixi`, `request`, `plan`, `commands_run`, `verification`, `changed_paths`, blockers, and `next_action`.

## Guardrails

Package removal can break topic readiness. Do not remove packages from the selected Topic Workspace Pixi environment until dependency risks and verification checks are explicit.
