# Manage Actors

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve Project, Research Topic, and Topic Workspace through Project Manifest-backed context. Do not infer the Topic Workspace from sibling directories.
2. List or inspect current Topic Actor bindings with `isomer-cli --print-json project topic-actors list --topic <topic>` or `isomer-cli --print-json project topic-actors show <topic-actor-name> --topic <topic>`.
3. For registration or update, validate path-safe `topic_actor_name`, actor kind, runtime kind, role kind, controller kind, default cwd label, workspace label, workspace path, branch, adapter ref, and status. Accept core enum values and `custom.*`; reject unknown non-extension values with a deterministic blocker.
4. Register or update bindings through `project topic-actors register` or `project topic-actors update`. The Topic Workspace Manifest is the actor topology authority; do not hand-edit `topic-workspace.toml`.
5. Materialize or repair Topic Actor Workspaces through `project topic-actors materialize` or `project topic-actors repair`. Use resolved `topic.repos.main` as the only worktree source accepted by this change, resolve `topic.actors.workspace` for the selected actor, and use `per-topic-actor/<topic-actor-name>/main` unless a safe actor-scoped branch is supplied.
6. Diagnose actor topology with `project topic-actors diagnose --topic <topic> --topic-actor <topic-actor-name>` and actor-scoped path queries such as `project paths get topic.actors.workspace --topic <topic> --topic-actor <topic-actor-name>`, `project paths get topic.actors.tmp --topic <topic> --topic-actor <topic-actor-name>`, and `project paths explain topic.actors.workspace --topic <topic> --topic-actor <topic-actor-name>`.
7. When Workspace Runtime is available, confirm registration or materialization wrote mutation or provenance audit records. Report those refs as audit evidence only; path resolution still uses the Topic Workspace Manifest binding.
8. Archive a Topic Actor binding with `project topic-actors archive <topic-actor-name> --topic <topic> --reason <reason>` only when the user explicitly requests it. Archiving does not delete the Topic Actor Workspace.
9. Summarize actor roster, actor workspaces, branch plan, runtime audit refs, blockers, and canonical repair routes.

If the user's task does not map cleanly to these steps, use your native planning tool to classify it as list/show, register/update, materialize/repair, diagnose, archive, or unsupported alternate-source worktree request.

## Command Shapes

```bash
isomer-cli --print-json project topic-actors list --topic <topic>
isomer-cli --print-json project topic-actors show <topic-actor-name> --topic <topic>
isomer-cli --print-json project topic-actors register <topic-actor-name> --topic <topic> --actor-kind manual_worker --runtime-kind codex --role-kind scout --controller-kind human_user --materialize
isomer-cli --print-json project topic-actors update <topic-actor-name> --topic <topic> --status active
isomer-cli --print-json project topic-actors materialize <topic-actor-name> --topic <topic>
isomer-cli --print-json project topic-actors repair <topic-actor-name> --topic <topic>
isomer-cli --print-json project topic-actors diagnose --topic <topic> --topic-actor <topic-actor-name>
isomer-cli --print-json project topic-actors archive <topic-actor-name> --topic <topic> --reason <reason>
```

## Guardrails

Do not accept `--source-repo` values other than the resolved `topic.repos.main` source in this change. Report alternate source repositories as unsupported instead of creating an ad hoc worktree.

Do not create Agent Team Instance records, Agent Instance records, formal Agent Workspaces, Houmao launch material, handoffs, or research records from actor management.

Do not treat Topic Actor Workspaces as formal Agent Workspaces. A Topic Actor binding is human-orchestrated topology, not team membership.
