# Setup Actors

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require `topic.intent.actor_definitions` from `define-actors`, topic environment readiness, and `topic.repos.main` readiness evidence.
2. Resolve the selected Topic Workspace, actor definitions, runtime kinds, role kinds, controller kinds, and default `operator` actor opt-out status.
3. Unless explicitly opted out, include the reserved `operator` Topic Actor with default cwd label `topic.actors.workspace`.
4. Delegate Topic Actor registration, update, materialization, repair, archive, and diagnostics to `isomer-admin-topic-workspace-mgr manage-actors` or the backed `project topic-actors ...` CLI surface.
5. Resolve or create derived actor env gates at `topic.env.actor_env_gates`; in the default layout this is `<topic-workspace>/intent/derived/actor-env-gates.md`.
6. Validate each selected `topic.actors.workspace`, `topic.actors.isomer_managed`, `topic.actors.private_artifacts`, `topic.actors.logs`, and `topic.actors.links` surface enough for manual research handoff.
7. Verify each actor's derived env gate from that actor's resolved `topic.actors.workspace` cwd and report command evidence or blockers.
8. Report actor roster, each actor cwd, branch, support labels, derived actor env gate path, verification evidence, blockers, and next subcommand.

If the user's task does not map cleanly to these steps, ask for actor names, runtime kinds, role kinds, controller kinds, source env gate requirements, or explicit default-operator opt-out.

## Guardrails

Do not make every manually controlled worker share `topic.repos.main` as cwd. Each worker that needs independent work receives its own `topic.actors.workspace` cwd.

Do not claim actor readiness from a materialized workspace alone. Require `topic.intent.actor_definitions`, derived `topic.env.actor_env_gates`, and gate verification evidence from actor cwd.
