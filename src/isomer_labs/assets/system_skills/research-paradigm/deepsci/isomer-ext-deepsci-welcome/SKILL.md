---
name: isomer-ext-deepsci-welcome
description: Use when a newcomer asks what DeepSci production research is for, which hypothesis, empirical, experiment, analysis, paper, revision, rebuttal, polish, or submission pattern fits a goal, what readiness is required, or which public DeepSci command to use.
---

# Isomer DeepSci Welcome

## Overview

DeepSci supports hypothesis-driven production research from framing and measured evidence through decisions, writing, review, revision, rebuttal, polish, and submission. This independent public welcome teaches those patterns and recommends a DeepSci entrypoint request without executing research.

## When to Use

Use this skill for DeepSci orientation, pass comparison, readiness explanation, command learning, or a read-only next-step recommendation. Phrases such as "test a hypothesis," "run experiments," or "revise the paper" are representative routing cues, not mandatory parser keywords.

Do not use welcome to bootstrap a workspace, run an experiment, analyze data, change a Research Idea, write a paper, resolve callbacks, close an operation set, or approve a Gate. Send concrete work and all supplied context to `$isomer-ext-deepsci-entrypoint`.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Classify the request**. Distinguish DeepSci orientation from an actionable research task that already belongs at the execution entrypoint.
2. **Handle the default**. For empty invocation or broad onboarding, introduce the production-research flow and show several high-value patterns from [references/show-options.md](references/show-options.md).
3. **Select one subcommand** from **Subcommands** according to the user's goal.
4. **Load one detail page** and follow its numbered workflow; load the exhaustive map only when requested.
5. **Explain readiness**. Name missing Project, Topic Workspace, actor or agent workspace, environment, extension, or DeepSci bootstrap context and recommend its public recovery route without running recovery.
6. **Return one public invocation** with the expected action, mutation posture, blocker or Gate, and next step.

If the task does not map cleanly to these steps, use the native planning tool to compare the curated DeepSci patterns, public pass map, readiness evidence, and user goal, then recommend one entrypoint request or ask for the smallest missing decision.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `show-options` | Present curated hypothesis, empirical, experiment, analysis, paper, revision, rebuttal, polish, submission, and readiness patterns. | [references/show-options.md](references/show-options.md) |
| `choose-path` | Select one pass or task-only entrypoint form from an ambiguous production-research goal. | [references/show-options.md](references/show-options.md) |
| `show-command-map` | Show every current DeepSci entrypoint command exactly once. | [references/show-command-map.md](references/show-command-map.md) |
| `next-step` | Recommend the next DeepSci or core public route from useful read-only context. | [references/next-step.md](references/next-step.md) |
| `help` | Explain DeepSci welcome, its public commands, readiness, and execution handoff. | [references/help.md](references/help.md) |

## Typical Use Cases

[references/show-options.md](references/show-options.md) supplies each pattern's use condition, routing cues, required context, canonical route, exact invocation, expected action, mutation posture, and next step. It teaches task-only focused requests where a named pass would add no value, but it never exposes protected capability identities.

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable orientation information in that format.

### Essential Output

State the interpreted research goal, one-sentence pattern fit, required context, recommended public invocation, expected action, mutation posture, missing readiness or Gate, and next step.

### Complete Output

Include alternate patterns, the complete command map, readiness evidence, routing rationale, and excluded protected direct routes.

## Guardrails

- DO NOT execute a DeepSci pass, focused stage, experiment, analysis, writing, review, or submission task.
- DO NOT mutate Project, Topic, workspace, environment, research, paper, callback, operation-set, or durable record state.
- DO NOT advertise protected DeepSci logical ids or private subskill paths as direct invocations.
- DO NOT copy pass recipes, callback procedures, registries, storage bindings, templates, or other entrypoint-private resources.
- DO NOT claim that representative phrases are required parser keywords.
- DO NOT treat an example command as readiness proof, mutation approval, or approval for a later Gate.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the recommended DeepSci pattern and exact public entrypoint request, use descriptive headings when they improve readability, and use lists only for genuinely distinct choices. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat. Explain missing readiness in newcomer language and keep internal stage ownership out of ordinary output.
