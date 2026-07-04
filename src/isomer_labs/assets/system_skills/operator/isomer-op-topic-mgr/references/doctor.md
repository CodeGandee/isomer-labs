# Doctor

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the selected Project, Research Topic, Topic Workspace, and semantic path evidence through `storage-resolve`.
2. Inspect initialized-topic storage with `storage-validate`, including `topic.repos.main`, `topic.repos.main.tmp`, projection roots, `custom.*` bindings, and path sources.
3. Inspect Topic Actor topology with `actors-diagnose` when Topic Actor bindings, actor cwd labels, or actor support labels are present or requested.
4. Inspect topic agent team topology with `team-validate-workspaces` when Agent Names, role bindings, packet/profile material, or `agent.workspace` refs are present or requested.
5. Inspect environment evidence without mutating packages: topic env setup evidence, actor cwd gate evidence, agent env service evidence, package blockers, and stale verification notes.
6. Report each finding as ready, warning, or blocker, with the owner command that can repair it.

If the user's task does not map cleanly to these steps, run the read-only checks that match the prompt, skip unrelated surfaces, and report skipped checks explicitly.

## Output

Report `status`, `topic`, `semantic_paths`, storage diagnostics, actor diagnostics, team diagnostics, environment diagnostics, retired-skill routing findings, blockers, and `next_action`.

## Guardrails

This subcommand is diagnostic by default. Do not mutate storage bindings, repositories, actors, worktrees, package environments, or service evidence unless the user explicitly asks for a follow-up repair command.
