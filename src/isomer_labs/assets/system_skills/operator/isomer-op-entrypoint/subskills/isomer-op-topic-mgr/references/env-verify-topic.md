# Env Verify Topic

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the selected Project, Research Topic, Topic Workspace, topic env target spec, Topic Workspace Pixi binding, and semantic paths through `storage-resolve`.
2. Inspect existing `topic.intent.topic_env_requirements`, `topic.env.topic_setup_target_spec`, Topic Workspace predecessor evidence, and Topic Main Development Repository evidence.
3. If full gate-driven setup or verification is missing, route to `isomer-srv-topic-env-setup` with selected Research Topic, Topic Workspace, semantic path expectations, and verification intent.
4. If verification evidence already exists, validate freshness, command evidence, required checklist coverage, skipped heavy checks, and blockers.
5. Report topic environment readiness, failed checks, skipped checks, service handoff evidence, blockers, and next action.

If the user's task does not map cleanly to these steps, verify only the named topic gate or package check and report missing full-gate context as a blocker.

## Output

Report the Topic environment verification outcome and selected Research Topic, then summarize semantic paths, the target specification, commands and verification, service evidence, blockers, and the next action.

## Operational Contract

- Limit this subcommand's readiness claim to the Topic Workspace environment; it does not prove per-Topic Actor cwd readiness, formal Agent Workspace cwd readiness, Agent Instance creation, or runtime launch readiness.

## Guardrails

- DO NOT claim per-Topic Actor cwd readiness, formal Agent Workspace cwd readiness, Agent Instance creation, or runtime launch readiness from this Topic Workspace environment check.
