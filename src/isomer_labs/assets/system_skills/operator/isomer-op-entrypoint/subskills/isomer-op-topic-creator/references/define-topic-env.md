# Define Topic Env

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require `topic.intent.overview` from `create-research-intent` or equivalent validated topic overview evidence.
2. Resolve `topic.intent.topic_env_requirements` through Workspace Path Resolution; in the default layout it is `<topic-workspace>/intent/src/topic-env-gate.md`.
3. Create or refine the topic env source gate with topic-level runnable requirements, expected repositories, exact user-supplied repository commands when present, requested branches or commits, sparse or partial needs, submodules, LFS, provider or authentication constraints, history needs, datasets, libraries or tools, runtime assumptions, unavailable resources, success criteria, open setup questions, and source material.
4. Outside `fast-forward`, present the generated or refined topic env gate for user verification and stop before `setup-topic-env` until the user accepts, revises, or supplies equivalent verified intent.
5. Under `fast-forward`, report generated assumptions, open questions, and resolved path metadata, then allow the flow to continue to `setup-topic-env`.

If the user's task does not map cleanly to these steps, ask what the topic environment must be able to run and stop before setup or installation.

## Operational Notes

- Those belong to `setup-topic-env` and `isomer-srv-topic-env-setup` after the topic env source gate is verified or fast-forward accepted.
- Preserve exact user-supplied repository procedures. When none is supplied, describe source, revision, authentication, repository-feature, history, and resource needs so the service can select suitable external commands without treating one clone depth or provider as canonical.

## Guardrails

- DO NOT derive `topic.env.topic_setup_target_spec`, install dependencies, configure Pixi, create repositories, or claim topic environment readiness here.
- DO NOT ask for full Git history by default.
