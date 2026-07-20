# Status

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve Project, Research Topic, Topic Workspace, `topic.intent.overview`, `topic.intent.topic_env_requirements`, runtime, topic environment, `topic.repos.main`, `topic.intent.actor_definitions`, Topic Actors, `topic.env.actor_env_gates`, actor onboarding context, and `topic.workspace.summary` evidence through read-only context.
2. Resolve read-only Houmao integration policy with `isomer-cli --print-json project integrations houmao status` when Topic Service Master preparation is in scope. Resolve Topic Service Master names and binding state with `isomer-cli --print-json project integrations houmao topic-service-master binding show --topic <research-topic-id>` when a Topic Workspace is selected.
3. Classify each ladder stage as `ready`, `blocked`, `skipped`, `not_configured`, or `not-started`.
4. Preserve explicit opt-outs, especially the default `operator` Topic Actor opt-out, and preserve disabled Houmao integration as a skip state rather than a failure.
5. Treat `topic.workspace.summary` as stale when predecessor evidence changed after it was written.
6. Report readiness, summary freshness, blockers, skipped stages, and Topic Service Master preparation state without naming a next research command.

If the user's task does not map cleanly to these steps, report all evidence that can be resolved and name the missing selector or Project context.

## Output

Report Project root, Research Topic ref, Topic Workspace ref, `topic.workspace.summary` path and freshness, ladder table, ready surfaces, verified checks, blockers, skipped stages, and Houmao-backed Topic Service Master suggested names, binding state, skip reason, or blocker.
