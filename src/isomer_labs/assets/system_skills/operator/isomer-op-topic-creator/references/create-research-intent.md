# Create Research Intent

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require concrete Research Topic source material from `resolve-topic-input` or equivalent user-provided context.
2. Require a registered or candidate Topic Workspace that can resolve `topic.intent.overview` through Workspace Path Resolution.
3. Resolve `topic.intent.overview`; in the default layout it is `<topic-workspace>/intent/src/topic-overview.md`.
4. Load the canonical template from `templates/topic-overview.md` in this skill bundle.
5. When internet access is available, actively search online for current context before writing the topic overview. Research topics often depend on recent repositories, papers, datasets, standards, product behavior, or tooling state, so use online evidence to sharpen the intent, links, assumptions, and caveats.
6. Create or update only the resolved topic overview file from the template:
   - Fill sections that can be inferred from the source material: `Research Topic`, `Motivation`, `Topic Breakdown` with `Do's` and `Don'ts`, `Expected Outcome`, and `Related Links`.
   - Keep sections without available substance as empty headings rather than omitting them.
   - Leave `## Topic Breakdown` subsections (`Do's`, `Don'ts`) and `## Related Links` in a placeholder state when no substance is available.
   - Strip any template `>` example blocks from the written file.
   - Record uncertainty as assumptions or open questions instead of inventing missing details.
7. Report the Topic overview label and resolved path, whether it was created or reused, any online sources consulted, assumptions, open questions, blockers, and readiness in natural language.

If the user's task does not map cleanly to these steps, explain whether the blocker is missing concrete topic material, missing Topic Workspace resolution, or conflicting existing overview material.

## Guardrails

- DO NOT write `topic.intent.topic_env_requirements`, `topic.intent.actor_definitions`, `topic.env.topic_setup_target_spec`, or `topic.env.actor_env_gates` here. Route topic env source gates to `define-topic-env`, actor definitions to `define-actors`, topic environment setup to `setup-topic-env`, and actor materialization plus actor env verification to `setup-actors`.

- DO NOT infer exact dependency versions, repository URLs, datasets, metrics, or tools unless the source topic context or searched online evidence explicitly supports them. Record uncertainty as assumptions or open questions.
