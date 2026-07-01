# Operator Topic Actor

## Workflow

When this reference is loaded, execute the following steps in order.

1. Check whether the user explicitly opted out of the reserved `operator` Topic Actor or its Topic Actor Workspace. Treat clear wording such as "do not create operator actor" or "no operator workspace" as an opt-out.
2. If there is no opt-out, list existing actors with `isomer-cli --print-json project topic-actors list --topic <topic>` and reuse an active `operator` binding when it already exists.
3. If the binding is missing, ask `isomer-admin-topic-workspace-mgr` to register and materialize it through `isomer-cli --print-json project topic-actors register operator --topic <topic> --actor-kind operator --runtime-kind human_cli --role-kind operator --controller-kind project_operator_session --materialize`, adjusting `--runtime-kind` to `codex`, `claude_code`, `shell`, `houmao`, or `custom.*` when the actual operator surface is known.
4. If the binding exists but its workspace is missing or stale, ask the Topic Workspace Manager to run `isomer-cli --print-json project topic-actors materialize operator --topic <topic>` or `isomer-cli --print-json project topic-actors repair operator --topic <topic>`.
5. Query `topic.actors.workspace` and `topic.actors.tmp` for the operator with `isomer-cli --print-json project paths get topic.actors.workspace --topic <topic> --topic-actor operator` and `isomer-cli --print-json project paths get topic.actors.tmp --topic <topic> --topic-actor operator`.
6. Record whether the operator actor is ready, opted out, blocked, or repaired, and include the result in the topic operation summary.

If the user's task does not map cleanly to these steps, route all Topic Actor CRUD, materialization, repair, archive, and actor-scoped path diagnostics to `isomer-admin-topic-workspace-mgr`.

## Guardrails

The `operator` Topic Actor is a Topic Actor, not an Operator Agent, Agent Instance, or Agent Team Instance member. Its workspace is a Topic Actor Workspace under `topic.actors.workspace`, not `agent.workspace`.

Use `topic.repos.main` as the worktree anchor and integration surface. Do not accept alternate source repositories for Topic Actor Workspace worktrees in this change.
