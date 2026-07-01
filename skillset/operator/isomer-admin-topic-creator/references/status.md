# Status

## Workflow

When this command is selected, execute the following steps in order.

1. Resolve Project, Research Topic, Topic Workspace, runtime, topic environment, `topic.repos.main`, Topic Actors, bootstrap, and start-pack evidence through read-only context.
2. Classify each ladder stage as `ready`, `blocked`, `skipped`, or `not-started`.
3. Preserve explicit opt-outs, especially the default `operator` Topic Actor opt-out.
4. Report the next command that can advance the topic toward manual-research readiness.

If the user's task does not map cleanly to these steps, report all evidence that can be resolved and name the missing selector or Project context.

## Output

Report Project root, Research Topic ref, Topic Workspace ref, ladder table, blockers, skipped stages, and next command.
