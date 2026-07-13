# Resolve Topic Intent

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require resolved Project context from `resolve-project` or equivalent evidence:
   - Do not create or mutate topic intent until the target Project, Research Topic candidate, and Topic Workspace candidate are known or explicitly blocked.
2. Resolve the semantic label `topic.intent.overview` through Workspace Path Resolution:
   - Record the semantic label, resolved path, storage profile, source, source detail, and diagnostics.
   - In `isomer-default.v1`, the resolved path is `<topic-workspace>/intent/src/topic-overview.md`.
3. Read the user's Research Topic prompt, registered topic statement when present, existing topic material when present, and any explicit source files named by the caller.
4. Write or update the resolved `topic.intent.overview` path with a concise user-editable topic overview:
   - Include the Research Topic, goal, success metrics, required datasets, explicitly mentioned repositories, explicitly mentioned libraries or tools, assumptions, open questions, and source material.
   - Avoid dependency versions unless the topic context explicitly says them.
5. If the topic is too vague to status without guessing:
   - Write the known facts and open questions only when safe.
   - Explain that Topic intent is blocked and name the missing topic substance.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from Project context, topic source material, Workspace Path Resolution output, and this reference page, then execute the plan.

## Prerequisite Artifacts

If any required predecessor artifact is missing, refuse to run directly and use **Targeted Fast-Forward Recovery** from the entrypoint when the missing predecessor can be created by the canonical flow. Required predecessor artifacts are resolved Project context from `resolve-project` or equivalent evidence, a Research Topic candidate or user-provided topic prompt, and a candidate or registered Topic Workspace that can resolve `topic.intent.overview`.

When the Research Topic or candidate Topic Workspace is missing but the user gave enough topic substance to seed a workspace, offer targeted fast-forward recovery through `init-topic` to `resolve-topic-intent`. Use `python scripts/query_step_dependencies.py path --target resolve-topic-intent --include-target` for the inclusive default path and `python scripts/query_step_dependencies.py path --target resolve-topic-intent --exclude-target` for the exclusive path. When topic substance is missing or generic, ask for the actual Research Topic and stop before creating files.

## Topic Overview Template

```markdown
# Topic Overview

## Research Topic

## Goal

## Success Metrics

## Required Datasets

## Explicit Repositories

## Explicit Libraries and Tools

## Assumptions

## Open Questions

## Source Material
```

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

### Essential Output

State whether the Topic intent is ready, revised, blocked, or unchanged. Give the resolved overview path, material open questions, Topic-understanding blockers, and the next operator action.

### Complete Output

Group the complete explanation by Topic intent status, overview label and path, storage profile, source and diagnostics, and open questions.

## Guardrails

Do not write canonical topic understanding to `<topic-workspace>/topic-def/topic-overview.md`. If only that legacy path exists, report a breaking-layout diagnostic and name `topic.intent.overview` plus its resolved default-layout path.

Do not infer exact dependency versions, repository URLs, datasets, metrics, or tools unless the source topic context explicitly names them. Record uncertainty as assumptions or open questions.

Do not specialize the team, derive env target specs, install dependencies, create Agent Workspaces, mutate Workspace Runtime, or launch live agents from this subcommand.
