# Setup Actors

## Workflow

When this command is selected, execute the following steps in order.

1. Resolve the selected Topic Workspace, requested Topic Actors, runtime kinds, role kinds, controller kinds, and default `operator` actor opt-out status.
2. Unless explicitly opted out, include the reserved `operator` Topic Actor with default cwd label `topic.actors.workspace`.
3. Delegate Topic Actor registration, update, materialization, repair, archive, and diagnostics to `isomer-admin-topic-workspace-mgr manage-actors` or the backed `project topic-actors ...` CLI surface.
4. Validate each selected `topic.actors.workspace`, `topic.actors.isomer_managed`, `topic.actors.private_artifacts`, `topic.actors.logs`, and `topic.actors.links` surface enough for manual research handoff.
5. Report actor roster, each actor cwd, branch, support labels, blockers, and next command.

If the user's task does not map cleanly to these steps, ask for actor names, runtime kinds, role kinds, controller kinds, or explicit default-operator opt-out.

## Guardrails

Do not make every manually controlled worker share `topic.repos.main` as cwd. Each worker that needs independent work receives its own `topic.actors.workspace` cwd.
