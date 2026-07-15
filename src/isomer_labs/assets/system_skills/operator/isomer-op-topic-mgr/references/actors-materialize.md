# Actors Materialize

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the selected Project, Research Topic, Topic Workspace, `topic.repos.main`, Topic Actor bindings, and actor-scoped semantic labels through `storage-resolve` and `actors-manage`.
2. Select the requested Topic Actors, defaulting only when the prompt or upstream creator evidence names them.
3. For each selected Topic Actor, resolve `topic.actors.workspace`, `topic.actors.tmp`, `topic.actors.isomer_managed`, `topic.actors.private_artifacts`, `topic.actors.logs`, and `topic.actors.links`.
4. Inspect `git worktree list --porcelain` from the resolved `topic.repos.main` before claiming actor cwd readiness.
5. Create, reuse, or repair the Topic Actor Workspace worktree only after explicit mutation intent, using `topic.repos.main` as the Git anchor and `per-topic-actor/<topic-actor-name>/main` as the default branch.
6. Treat an existing matching `topic.actors.workspace` worktree on the expected branch as ready, and treat an existing nonmatching path as a blocker; do not overwrite, delete, move, clean, reset, or reinitialize that path.
7. Reject alternate source repositories, unsafe paths, duplicate branch checkouts, cross-actor prefixes, and missing Topic Main Development Repository predecessor evidence.
8. Report materialized, reused, skipped, and blocked actor workspaces with command evidence, worktree source, branch evidence, blockers, and repair routes.

If the user's task does not map cleanly to these steps, materialize only the named actors with complete evidence and report blockers for the rest.

## Output

Report the materialization outcome and selected Research Topic, then summarize Topic Actor bindings, workspace paths, branch plan, worktree evidence by actor, support labels, runtime audit refs when available, blockers, and the next action.

## Guardrails

- MUST keep Topic Actor names separate from Agent Names and Agent Instance ids. Topic Actor Workspace materialization is actor topology, not Agent Team Instance membership or research-paradigm bootstrap.
