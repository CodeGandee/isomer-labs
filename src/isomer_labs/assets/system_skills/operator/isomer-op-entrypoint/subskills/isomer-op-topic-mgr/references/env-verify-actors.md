# Env Verify Actors

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the selected Project, Research Topic, Topic Workspace, selected Topic Actors, actor-scoped semantic labels, and derived `topic.env.actor_env_gates`.
2. Require `topic.intent.actor_definitions`, topic environment readiness, `topic.repos.main` readiness, selected Topic Actor bindings, and selected `topic.actors.workspace` worktree evidence showing the cwd is a worktree of `topic.repos.main` on the expected actor branch.
3. If worktree evidence is missing, blocked, or nonmatching, report that blocker and stop before actor env gate execution for that actor.
4. For each selected Topic Actor, run or delegate the derived actor env gate from the resolved `topic.actors.workspace` cwd.
5. Verify `topic.actors.isomer_managed`, `topic.actors.private_artifacts`, `topic.actors.logs`, `topic.actors.links`, and `topic.actors.tmp` posture enough for actor onboarding.
6. Report per-actor ready, failed, skipped, and blocked checks, including command evidence, support-label evidence, worktree evidence, and repair routes.

If the user's task does not map cleanly to these steps, verify only the named actor or actor gate and report missing actor readiness signals as blockers.

## Output

Report the verification outcome and selected Research Topic, then summarize selected actors, their cwd paths, the derived actor environment gate, commands and evidence, support labels, blockers, and the next action.

## Operational Notes

- Actor readiness requires actor definitions, matching `topic.repos.main` worktree evidence for the actor cwd, derived actor env gates, actor cwd verification evidence, and actor onboarding context.

## Guardrails

- DO NOT claim actor readiness from workspace materialization alone.
