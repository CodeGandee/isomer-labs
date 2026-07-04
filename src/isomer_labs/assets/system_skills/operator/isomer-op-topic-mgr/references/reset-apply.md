# Reset Apply

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the selected Project, Research Topic, Topic Workspace, Workspace Runtime, checkpoint id, and reset plan id through Project Manifest-backed context and the operator prompt.
2. Inspect the selected plan with `isomer-cli project topic-reset show-plan --topic <research-topic-id> <plan-id>` and stop with a blocker if the plan has blockers, stale preconditions, unexpected destructive actions, or no explicit user approval.
3. Confirm the operator understands that reset apply is destructive for only the runtime rows, structured payloads, generated views, and managed actor or agent workspace paths named by the approved plan.
4. Run `isomer-cli project topic-reset apply --topic <research-topic-id> --yes <checkpoint-id> <plan-id> --render markdown` only after explicit confirmation.
5. Report reset outcome id, status, applied/skipped/failed action counts, generated Markdown review path, diagnostics, and any follow-up blocker.

If the user's task does not map cleanly to these steps, inspect the selected plan and stop before mutation until checkpoint id, reset plan id, selected topic, and explicit approval are all concrete.

## Boundary

`reset-apply` applies only an approved structured reset plan. It must reject stale plans and blockers, and it must delete only paths and records named by the plan.

Use structured records and Workspace Runtime state only. Do not use Git operations, project-root tracking, branch state, or stash material during reset apply.
