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
5. If the topic is too vague to summarize without guessing:
   - Write the known facts and open questions only when safe.
   - Report `topic_intent_status: blocked`, and name the missing topic substance.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from Project context, topic source material, Workspace Path Resolution output, and this reference page, then execute the plan.

## Prerequisite Artifacts

If any required predecessor artifact is missing, refuse to run and tell the user why. Required predecessor artifacts are resolved Project context from `resolve-project` or equivalent evidence, a Research Topic candidate or user-provided topic prompt, and a candidate or registered Topic Workspace that can resolve `topic.intent.overview`.

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

- `topic_intent_status`: ready, revised, blocked, or not changed.
- `topic_overview_label`: `topic.intent.overview`.
- `topic_overview_path`: resolved path for `topic.intent.overview`.
- `topic_overview_storage_profile`: usually `topic_intent_source_file`.
- `topic_overview_source`: resolver source such as `default_profile`, `topic_workspace_manifest`, `env`, or `path_plan`.
- `topic_overview_source_detail`: resolver source detail such as `isomer-default.v1` or manifest binding detail.
- `topic_overview_diagnostics`: Workspace Path Resolution diagnostics and topic-understanding blockers.
- `open_questions`: topic questions that materially affect scope, goals, metrics, datasets, repositories, tools, or team selection.

## Guardrails

Do not write canonical topic understanding to `<topic-workspace>/topic-def/topic-overview.md`. If only that legacy path exists, report a legacy-path migration note and name `topic.intent.overview` plus its resolved default-layout path.

Do not infer exact dependency versions, repository URLs, datasets, metrics, or tools unless the source topic context explicitly names them. Record uncertainty as assumptions or open questions.

Do not specialize the team, derive env target specs, install dependencies, create Agent Workspaces, mutate Workspace Runtime, or launch live agents from this subcommand.
