# Reset Plan

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the selected Project, Research Topic, Topic Workspace, Workspace Runtime, and `topic.workspace.summary` through Project Manifest-backed context and Workspace Path Resolution.
2. Select the reset checkpoint id from the user prompt, the latest ready checkpoint, or `isomer-cli project topic-reset list --topic <research-topic-id>` output; report a blocker if no checkpoint can be selected.
3. Run `isomer-cli project topic-reset plan --topic <research-topic-id> <checkpoint-id> --render markdown` to create a read-only structured reset plan.
4. Inspect the plan action summary for preserve, delete_record, delete_file, delete_generated_view, regenerate, skip, and blocked actions, including managed `topic.actors.workspace` and `agent.workspace` deletion candidates.
5. Report checkpoint id, reset plan id, generated Markdown review path, blocker count, action counts, and the next safe operator action.

If the user's task does not map cleanly to these steps, run only the read-only checkpoint selection and plan inspection steps that match the prompt, then report the missing checkpoint, topic selector, or Workspace Runtime blocker.

## Boundary

`reset-plan` is read-only with respect to reset candidates. It may create a structured reset plan record and generated review view, but it must not delete runtime rows, structured payloads, generated views, or files.

Use structured records and Workspace Runtime state only. Do not use Git operations, project-root tracking, branch state, or stash material to decide what reset would preserve or delete.
