# Create Research Intent

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require concrete Research Topic source material from `resolve-topic-input` or equivalent user-provided context.
2. Require a registered or candidate Topic Workspace that can resolve `topic.intent.overview` through Workspace Path Resolution.
3. Resolve `topic.intent.overview`; in the default layout it is `<topic-workspace>/intent/src/topic-overview.md`.
4. Create or update only the resolved topic overview file with the Research Topic, goals or objectives, scope, known success metrics, required datasets when known, explicitly mentioned repositories, explicitly mentioned libraries or tools, assumptions, open questions, and source material.
5. Report `topic_overview_label`, resolved path metadata, created or reused status, assumptions, open questions, blockers, and readiness state.

If the user's task does not map cleanly to these steps, explain whether the blocker is missing concrete topic material, missing Topic Workspace resolution, or conflicting existing overview material.

## Guardrails

Do not write `topic.intent.topic_env_requirements`, `topic.intent.actor_definitions`, `topic.env.topic_setup_target_spec`, or `topic.env.actor_env_gates` here. Route topic env source gates to `define-topic-env`, actor definitions to `define-actors`, topic environment setup to `setup-topic-env`, and actor materialization plus actor env verification to `setup-actors`.
