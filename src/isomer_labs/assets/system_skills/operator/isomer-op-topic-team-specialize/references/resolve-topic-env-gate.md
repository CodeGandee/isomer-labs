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
   - Preserve exact user-supplied repository commands when present. Otherwise, state requested source, revision, authentication, sparse or partial needs, submodules, LFS, provider constraints, history needs, and resource limits so the service can select suitable external commands.
   - Keep this source intent user-editable.
   - Avoid concrete install commands, package-source choices, cwd matrices, execution logs, or verification command detail unless the user explicitly supplied them as intent.
5. If the topic environment needs are too vague to derive a service target spec later:
   - Write open questions or explain that Topic environment source intent is blocked.
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

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

### Essential Output

State whether the Topic environment source intent is ready, revised, blocked, or unchanged. Give the resolved requirements path, source-intent blockers or open questions, and the next operator action.

### Complete Output

Group the complete explanation by source-intent status, semantic label and path, storage profile, source and diagnostics, and next operator action.

## Operational Notes

- The topic env service owns operational target-spec generation, dependency plans, Pixi commands, repo acquisition decisions, expected outputs, and execution logs.
- Do not impose a clone depth, provider, remote name, or command sequence. The acting user or service agent selects repository commands outside Isomer from the user request and repository requirements, verifies source and immutable identity, then registers the existing path.
- If only that legacy path exists, report a breaking-layout diagnostic and name `topic.intent.topic_env_requirements` plus its resolved default-layout path.

## Guardrails

- DO NOT derive `topic.env.topic_setup_target_spec` here.
- DO NOT request full Git history by default.
- DO NOT write canonical source intent to `<topic-workspace>/user-intent/src/env-gate.md`.
- DO NOT require Topic Agent Team Profile material, Agent Names, Agent Workspaces, or per-agent cwd readiness before resolving topic-level environment source intent.
