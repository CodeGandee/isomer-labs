# Define Actors

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require `topic.intent.overview` and topic environment setup evidence, or a clear operator request to draft actor intent before setup is complete.
2. Resolve `topic.intent.actor_definitions` through Workspace Path Resolution; in the default layout it is `<topic-workspace>/intent/src/actor-definitions.md`.
3. Create or refine actor definitions with each actor's name, duty, intended usage, expected cwd label, actor kind, runtime kind, role kind, controller kind, source env gate requirements, selected v2 skills when known, and open actor setup questions.
4. If invoked without further actor information, create or refine a default `operator` actor definition.
5. Treat requests such as "create the operator actor" as the same default `operator` actor definition path.
6. Report actor definitions path, actor roster, default-operator opt-out status, assumptions, open questions, blockers, and next subcommand.

If the user's task does not map cleanly to these steps, ask for actor names or confirm that the default `operator` actor is enough.

## Guardrails

Do not register Topic Actors, materialize Topic Actor Workspaces, generate derived actor env gates, or claim actor cwd readiness here. Those belong to `setup-actors`.
