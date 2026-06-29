# Resolve Topic Env Gate

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require resolved topic context:
   - Require resolved Project and Topic Workspace context plus `topic.intent.overview` from `resolve-topic-intent` or equivalent evidence.
   - If topic intent is missing, route back to `resolve-topic-intent` before creating environment source intent.
2. Resolve the semantic label `topic.intent.topic_env_requirements` through Workspace Path Resolution:
   - Record the semantic label, resolved path, storage profile, source, source detail, and diagnostics.
   - In `isomer-default.v1`, the resolved path is `<topic-workspace>/intent/src/topic-env-gate.md`.
3. Read the topic overview, user prompt, explicitly mentioned repositories, required datasets, tools, libraries, runtimes, and runnable goals.
4. Write or update the resolved `topic.intent.topic_env_requirements` path with concise high-level Topic Workspace requirements:
   - State what must be available or runnable for the topic.
   - Keep this source intent user-editable.
   - Avoid concrete install commands, package-source choices, cwd matrices, execution logs, or verification command detail unless the user explicitly supplied them as intent.
5. If the topic environment needs are too vague to derive a service target spec later:
   - Write open questions or report `topic_env_source_status: blocked`.
   - Stop before `setup-topic-env`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from `topic.intent.overview`, user-provided environment needs, Workspace Path Resolution output, and this reference page, then execute the plan.

## Prerequisite Artifacts

If any required predecessor artifact is missing, refuse to run and tell the user why. Required predecessor artifacts are resolved Project and Topic Workspace context, `topic.intent.overview` from `resolve-topic-intent` or equivalent evidence, and enough topic material or prompt context to identify topic-level runnable needs.

## Topic Env Requirements Template

```markdown
# Topic Environment Requirements

## Required Capabilities

## Required Tools

## Required Libraries

## Required Repositories

## Required Datasets

## Runnable Targets

## Assumptions

## Open Questions

## Source Material
```

## Output Contract

- `topic_env_source_status`: ready, revised, blocked, or not changed.
- `topic_env_source_label`: `topic.intent.topic_env_requirements`.
- `topic_env_source_path`: resolved path for `topic.intent.topic_env_requirements`.
- `topic_env_source_storage_profile`: usually `topic_intent_source_file`.
- `topic_env_source`: resolver source such as `default_profile`, `topic_workspace_manifest`, `env`, or `path_plan`.
- `topic_env_source_detail`: resolver source detail such as `isomer-default.v1` or manifest binding detail.
- `topic_env_source_diagnostics`: Workspace Path Resolution diagnostics and source-intent blockers.
- `next_operator_action`: usually `setup-topic-env` when source intent is usable, or ask the user to answer open questions.

## Guardrails

Do not derive `topic.env.topic_setup_target_spec` here. The topic env service owns operational target-spec generation, dependency plans, Pixi commands, repo acquisition decisions, expected outputs, and execution logs.

Do not write canonical source intent to `<topic-workspace>/user-intent/src/env-gate.md`. If only that legacy path exists, report a breaking-layout diagnostic and name `topic.intent.topic_env_requirements` plus its resolved default-layout path.

Do not require Topic Agent Team Profile material, Agent Names, Agent Workspaces, or per-agent cwd readiness before resolving topic-level environment source intent.
