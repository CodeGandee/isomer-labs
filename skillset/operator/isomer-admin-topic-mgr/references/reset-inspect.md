# Reset Inspect

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the selected Project, Research Topic, Topic Workspace, and Workspace Runtime through Project Manifest-backed context.
2. Use `isomer-cli project topic-reset list --topic <research-topic-id>` to list available structured reset checkpoints, statuses, timestamps, and review paths.
3. Use `isomer-cli project topic-reset show --topic <research-topic-id> <checkpoint-id>` for checkpoint details when a checkpoint id is selected.
4. Use `isomer-cli project topic-reset show-plan --topic <research-topic-id> <plan-id>` for reset plan actions, blockers, precondition digest, and generated review path when a reset plan id is selected.
5. Report checkpoint status, plan status, blockers, generated Markdown review paths, preserved setup evidence, and whether a fresh read-only plan is needed before apply.

If the user's task does not map cleanly to these steps, inspect only the selected checkpoint or plan refs that can be resolved and report any missing selector or Workspace Runtime blocker.

## Boundary

`reset-inspect` is read-only. It consumes structured records and Workspace Runtime state, names generated Markdown review material, and must not mutate records or files.

Do not route reset inspection through research workflow skills. Operator reset inspection depends on checkpoint, plan, outcome, Workspace Runtime, and semantic path evidence only.
