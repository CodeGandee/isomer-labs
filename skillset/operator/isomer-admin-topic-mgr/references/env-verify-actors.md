# Env Verify Actors

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the selected Project, Research Topic, Topic Workspace, selected Topic Actors, actor-scoped semantic labels, and derived `topic.env.actor_env_gates`.
2. Require `topic.intent.actor_definitions`, topic environment readiness, `topic.repos.main` readiness, selected Topic Actor bindings, and selected `topic.actors.workspace` cwd evidence.
3. For each selected Topic Actor, run or delegate the derived actor env gate from the resolved `topic.actors.workspace` cwd.
4. Verify `topic.actors.isomer_managed`, `topic.actors.private_artifacts`, `topic.actors.logs`, `topic.actors.links`, and `topic.actors.tmp` posture enough for actor onboarding.
5. Report per-actor ready, failed, skipped, and blocked checks, including command evidence, support-label evidence, and repair routes.

If the user's task does not map cleanly to these steps, verify only the named actor or actor gate and report missing actor readiness signals as blockers.

## Output

Report `status`, `topic`, selected actors, actor cwd paths, derived `topic.env.actor_env_gates` path, commands run, verification evidence, support labels, blockers, and `next_action`.

## Guardrails

Do not claim actor readiness from workspace materialization alone. Actor readiness requires actor definitions, derived actor env gates, actor cwd verification evidence, and actor onboarding context.
