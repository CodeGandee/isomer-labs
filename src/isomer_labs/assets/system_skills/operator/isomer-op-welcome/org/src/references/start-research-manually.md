---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Start Research Manually

## Workflow

1. Interpret this usage path as human-orchestrated research setup, not formal Topic Team Specialization.
2. Recommend parent-scoped route `isomer-op-entrypoint->topic-create`.
3. Use `$isomer-op-entrypoint use topic-create to fast-forward the requested setup` when the user has approved automatic setup, or ask the public entrypoint to guide setup step by step when they want acknowledgement.
4. Explain that manual research selects execution topology but does not select the DeepSci or Kaoju research paradigm; offer `start-deepsci-research`, `start-kaoju-survey`, or no optional paradigm as a separate choice when relevant.
5. Mention that the owner skill handles or delegates Project readiness, concrete Research Topic input, Research Topic and Topic Workspace registration, Workspace Runtime readiness, topic environment setup, default or requested Topic Actors, Topic Actor Workspaces, actor onboarding, and `topic.workspace.summary`.
6. Route lower-level initialized-topic storage, Topic Actor repair, package mutation, environment verification, reset checkpoints, and diagnostics through `isomer-op-entrypoint->topic-manage` after Topic Creator handoff.
7. Report the mutation boundary: this welcome skill does not initialize the Project, create the Research Topic, mutate the Topic Workspace, create Topic Actor Workspaces, or install or run an optional research extension.

If the user's task does not map cleanly to these steps, use your native planning tool to decide whether the user is asking for manual Topic Actor research or work on a formal Agent Team established by an explicit specialization invocation, a named formal-team artifact, or authoritative context, then recommend the matching visible usage path or ask for that distinction.

## Output Guidance

Recommend the manual research path in natural language and route it through `isomer-op-entrypoint->topic-create`. Give `$isomer-op-entrypoint use topic-create to fast-forward the requested setup` or the equivalent guided task as the safe first invocation. Name any missing Research Topic, Project decision, research-paradigm choice, or mutation authority, then state whether to invoke the public entrypoint or provide the missing topic substance.

Do not route this usage path to `isomer-op-entrypoint->topic-team` unless the user explicitly invokes specialization or the prompt or authoritative context establishes a formal Agent Team target and asks to deploy, specialize, instantiate, materialize, validate, repair, launch, or use that team. Generic preparation, launch-facing language, readiness gaps, missing summaries, and missing Agent Workspaces do not establish that target.
