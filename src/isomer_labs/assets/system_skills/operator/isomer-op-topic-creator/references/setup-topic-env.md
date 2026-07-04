# Setup Topic Env

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require registered topic refs, Workspace Runtime status, `topic.intent.overview`, verified or fast-forward accepted `topic.intent.topic_env_requirements`, and effective Topic Workspace path evidence.
2. Resolve and read `topic.intent.topic_env_requirements`; do not create it in this subcommand.
3. Validate or derive `topic.env.topic_setup_target_spec` from the topic env source gate when topic environment setup is needed.
4. Delegate topic environment setup to `isomer-srv-topic-env-setup`, including dependency, Pixi, Topic Main Development Repository, repository acquisition, projection, and topic-root verification work.
5. Validate `topic.repos.main` readiness, repository acquisition decisions, projection predecessor evidence, topic environment status, and semantic labels needed by manual research.
6. Report topic environment status, topic env source gate path, derived target spec path, `topic.repos.main` path, repository acquisition decisions, projection evidence, blockers, and readiness state.

If the user's task does not map cleanly to these steps, report whether the missing evidence is topic overview, verified topic env requirements, target spec, service setup output, or topic-main readiness.

## Guardrails

Do not create or repair `topic.repos.main` directly in this skill. The canonical Topic Main Development Repository setup belongs to `isomer-srv-topic-env-setup`.

Do not invent `topic.intent.topic_env_requirements` here. Route missing or stale source gates to `define-topic-env`.
