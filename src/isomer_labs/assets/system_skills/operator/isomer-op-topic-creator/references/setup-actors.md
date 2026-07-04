# Setup Actors

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require `topic.intent.actor_definitions` from `define-actors`, topic environment readiness, and `topic.repos.main` readiness evidence.
2. Resolve the selected Topic Workspace, actor definitions, runtime kinds, role kinds, controller kinds, and default `operator` actor opt-out status.
3. Unless explicitly opted out, include the reserved `operator` Topic Actor with default cwd label `topic.actors.workspace`.
4. Delegate Topic Actor registration, update, materialization, repair, archive, and diagnostics to `isomer-op-topic-mgr actors-manage` or the backed `project topic-actors ...` CLI surface.
5. Resolve or create derived actor env gates at `topic.env.actor_env_gates`; in the default layout this is `<topic-workspace>/intent/derived/actor-env-gates.md`.
6. Validate each selected `topic.actors.workspace`, `topic.actors.isomer_managed`, `topic.actors.private_artifacts`, `topic.actors.logs`, and `topic.actors.links` surface enough for manual actor onboarding.
7. Verify each actor's derived env gate from that actor's resolved `topic.actors.workspace` cwd and report command evidence or blockers.
8. Build v2-independent actor onboarding context for each selected Topic Actor: actor name, actor kind, runtime kind, role kind, controller kind, cwd, branch, integration surface, support labels, boundary notes, verification evidence, and blockers.
9. Report actor roster, each actor cwd, branch, support labels, derived actor env gate path, actor onboarding context, verification evidence, blockers, and readiness state.

If the user's task does not map cleanly to these steps, ask for actor names, runtime kinds, role kinds, controller kinds, source env gate requirements, or explicit default-operator opt-out.

## Guardrails

Do not make every manually controlled worker share `topic.repos.main` as cwd. Each worker that needs independent work receives its own `topic.actors.workspace` cwd.

Do not claim actor readiness from a materialized workspace alone. Require `topic.intent.actor_definitions`, derived `topic.env.actor_env_gates`, gate verification evidence from actor cwd, and enough actor onboarding context for the selected actors.

## Actor Onboarding Shape

Actor onboarding context is startup convenience for the selected Topic Actors, not accepted research truth. It should include:

- `actor_identity`: Topic Actor name plus actor kind, runtime kind, role kind, controller kind, and adapter ref when known.
- `cwd`: resolved `topic.actors.workspace` path and source.
- `branch`: current or intended `per-topic-actor/<topic-actor-name>/main` branch.
- `integration_surface`: `topic.repos.main` as the Git anchor and integration surface, not a shared cwd requirement for every worker.
- `support_labels`: resolved `topic.actors.isomer_managed`, `topic.actors.private_artifacts`, `topic.actors.logs`, `topic.actors.links`, and `topic.actors.tmp`.
- `boundary_notes`: private, log, link, and tmp posture; generated links are convenience pointers only.
- `verification_evidence`: gate check, cwd check, materialization evidence, and delegated owner evidence when available.
- `blockers`: missing labels, unsafe paths, unresolved actor definitions, failed gate checks, or explicit opt-outs.

If actor-local cards or pointers are written, keep them under `topic.actors.isomer_managed` or `topic.actors.links` and describe them as startup convenience. Do not describe them as authoritative research records, durable findings, or accepted artifact refs.
