# Plan

## Workflow

When this command is selected, execute the following steps in order.

1. Resolve the Project root, Project Manifest status, selected Research Topic, selected Topic Workspace, requested actor roster, and requested v2 research route through read-only Project Manifest-backed context.
2. Evaluate each ladder stage without mutation: Project readiness, topic definition, topic registration, Workspace Runtime, topic environment readiness, `topic.repos.main`, Topic Actor workspaces, v2 research bootstrap, and start packs.
3. For every incomplete stage, report the delegated owner, proposed command shape, required input, mutation approval needed, expected output, and blocker.
4. Report the safe next command, usually `ensure-project`, `define-topic`, `register-topic`, `init-runtime`, `setup-topic-env`, `setup-actors`, `bootstrap-research`, or `start-manual-research`.

If the user's task does not map cleanly to these steps, build a read-only planning summary from available Project context and name the missing topic statement, Project root, actor roster, or mutation approval.

## Mutation Boundary

`plan` is dry-run. It must not create or modify Project, Topic Workspace, runtime, repository, actor, bootstrap, or start-pack state.
