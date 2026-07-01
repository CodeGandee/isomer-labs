# Setup Topic Env

## Workflow

When this command is selected, execute the following steps in order.

1. Require registered topic refs, Workspace Runtime status, topic intent evidence, and effective Topic Workspace path evidence.
2. Resolve or create `topic.intent.topic_env_requirements` and validate or derive `topic.env.topic_setup_target_spec` when topic environment setup is needed.
3. Delegate topic environment setup to `isomer-srv-topic-env-setup`, including dependency, Pixi, Topic Main Development Repository, projection, and topic-root verification work.
4. Validate `topic.repos.main` readiness, projection predecessor evidence, topic environment status, and semantic labels needed by manual research.
5. Report topic environment status, `topic.repos.main` path, projection evidence, blockers, and next command.

If the user's task does not map cleanly to these steps, report whether the missing evidence is topic intent, topic env requirements, target spec, service setup output, or topic-main readiness.

## Guardrails

Do not create or repair `topic.repos.main` directly in this skill. The canonical Topic Main Development Repository setup belongs to `isomer-srv-topic-env-setup`.
