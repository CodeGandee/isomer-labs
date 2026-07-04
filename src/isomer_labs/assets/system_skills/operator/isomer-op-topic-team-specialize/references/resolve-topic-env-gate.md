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
   - State whether any Git repository needs full history instead of a shallow source snapshot, and why.
   - Keep this source intent user-editable.
   - Avoid concrete install commands, package-source choices, cwd matrices, execution logs, or verification command detail unless the user explicitly supplied them as intent.
5. If the topic environment needs are too vague to derive a service target spec later:
   - Write open questions or report `topic_env_source_status: blocked`.
   - Stop before `setup-topic-env`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from `topic.intent.overview`, user-provided environment needs, Workspace Path Resolution output, and this reference page, then execute the plan.

## Prerequisite Artifacts

If any required predecessor artifact is missing, refuse to run directly and use **Targeted Fast-Forward Recovery** from the entrypoint when the missing predecessor can be created by the canonical flow. Required predecessor artifacts are resolved Project and Topic Workspace context, `topic.intent.overview` from `resolve-topic-intent` or equivalent evidence, and enough topic material or prompt context to identify topic-level runnable needs.

When `topic.intent.overview` is missing but the request contains enough topic substance, offer targeted fast-forward recovery to `resolve-topic-env-gate`. Use `python scripts/query_step_dependencies.py path --target resolve-topic-env-gate --include-target` for the inclusive default path and `python scripts/query_step_dependencies.py path --target resolve-topic-env-gate --exclude-target` for the exclusive path.

When the runnable need is too vague, ask the user what the Topic Workspace should be able to run after setup and stop. Do not invent runnable requirements from generic topic text.

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

Default to **Essential Output** in chat. Print **Complete Output** only when the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output.

### Essential Output

- `topic_env_source_status`: ready, revised, blocked, or not changed.
- `topic_env_source_path`: resolved path for `topic.intent.topic_env_requirements`.
- `blockers`: source-intent blockers or open questions.
- `next_operator_action`: usually `setup-topic-env` when source intent is usable, or ask the user to answer open questions.

### Complete Output

- `topic_env_source_status`
- `topic_env_source_label`
- `topic_env_source_path`
- `topic_env_source_storage_profile`
- `topic_env_source`
- `topic_env_source_detail`
- `topic_env_source_diagnostics`
- `next_operator_action`

## Guardrails

Do not derive `topic.env.topic_setup_target_spec` here. The topic env service owns operational target-spec generation, dependency plans, Pixi commands, repo acquisition decisions, expected outputs, and execution logs.

Do not request full Git history by default. Mention full history only when the prompt, Research Topic, benchmark protocol, provenance need, bisect or debugging task, changelog analysis, branch comparison, tag traversal, or version-history requirement implies it; otherwise the topic env service should default to a shallow clone with `--depth=1`.

Do not write canonical source intent to `<topic-workspace>/user-intent/src/env-gate.md`. If only that legacy path exists, report a breaking-layout diagnostic and name `topic.intent.topic_env_requirements` plus its resolved default-layout path.

Do not require Topic Agent Team Profile material, Agent Names, Agent Workspaces, or per-agent cwd readiness before resolving topic-level environment source intent.
