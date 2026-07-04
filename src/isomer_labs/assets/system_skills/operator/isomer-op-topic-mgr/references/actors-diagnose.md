# Actors Diagnose

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the selected Project, Research Topic, Topic Workspace, Topic Actor bindings, and actor-scoped semantic labels.
2. Inspect each selected Topic Actor binding for path-safe `topic_actor_name`, actor kind, runtime kind, role kind, controller ref or controller kind, default cwd label, workspace label, branch, status, and provenance metadata.
3. Inspect the resolved `topic.actors.workspace`, `topic.actors.tmp`, `topic.actors.isomer_managed`, `topic.actors.private_artifacts`, `topic.actors.logs`, and `topic.actors.links` surfaces.
4. Inspect branch posture, worktree source, duplicate checkout state, runtime audit refs when available, and stale actor onboarding material.
5. Report ready actors, warnings, blockers, and the safest repair route through `actors-manage`, `actors-materialize`, `env-verify-actors`, or `isomer-op-topic-creator`.

If the user's task does not map cleanly to these steps, diagnose the named actor or actor surface first and report which actor checks were skipped.

## Output

Report `status`, `topic`, `topic_actor_bindings`, actor cwd evidence, support labels, branch posture, audit refs, blockers, and `next_action`.

## Guardrails

Do not archive, delete, or repurpose Topic Actor bindings during diagnostics. Do not claim actor readiness from a materialized workspace alone; report missing env gate or actor onboarding evidence as a blocker.
