# Actors Materialize

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the selected Project, Research Topic, Topic Workspace, `topic.repos.main`, Topic Actor bindings, and actor-scoped semantic labels through `storage-resolve` and `actors-manage`.
2. Select the requested Topic Actors, defaulting only when the prompt or upstream creator evidence names them.
3. For each selected Topic Actor, resolve `topic.actors.workspace`, `topic.actors.tmp`, `topic.actors.isomer_managed`, `topic.actors.private_artifacts`, `topic.actors.logs`, and `topic.actors.links`.
4. Create, reuse, or repair the Topic Actor Workspace worktree only after explicit mutation intent, using `topic.repos.main` as the Git anchor and `per-topic-actor/<topic-actor-name>/main` as the default branch.
5. Reject alternate source repositories, unsafe paths, duplicate branch checkouts, cross-actor prefixes, and missing Topic Main Development Repository predecessor evidence.
6. Report materialized, reused, skipped, and blocked actor workspaces with command evidence and repair routes.

If the user's task does not map cleanly to these steps, materialize only the named actors with complete evidence and report blockers for the rest.

## Output

Report `status`, `topic`, `topic_actor_bindings`, `topic_actor_workspace_paths`, `topic_actor_branch_plan`, support labels, runtime audit refs when available, blockers, and `next_action`.

## Guardrails

Keep Topic Actor names separate from Agent Names and Agent Instance ids. Topic Actor Workspace materialization is actor topology, not Agent Team Instance membership or research-paradigm bootstrap.
