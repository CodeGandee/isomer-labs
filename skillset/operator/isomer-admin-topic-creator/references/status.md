# Status

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve Project, Research Topic, Topic Workspace, `topic.intent.overview`, `topic.intent.topic_env_requirements`, runtime, topic environment, `topic.repos.main`, `topic.intent.actor_definitions`, Topic Actors, `topic.env.actor_env_gates`, bootstrap, and `topic.workspace.summary` evidence through read-only context.
2. Classify each ladder stage as `ready`, `blocked`, `skipped`, or `not-started`.
3. Preserve explicit opt-outs, especially the default `operator` Topic Actor opt-out.
4. Treat `topic.workspace.summary` as stale when predecessor evidence changed after it was written.
5. Report readiness, summary freshness, blockers, and skipped stages without naming a next research command.

If the user's task does not map cleanly to these steps, report all evidence that can be resolved and name the missing selector or Project context.

## Output

Report Project root, Research Topic ref, Topic Workspace ref, `topic.workspace.summary` path and freshness, ladder table, ready surfaces, verified checks, blockers, and skipped stages.
