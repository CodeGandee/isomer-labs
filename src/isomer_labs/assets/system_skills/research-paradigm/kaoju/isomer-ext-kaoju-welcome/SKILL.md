---
name: isomer-ext-kaoju-welcome
description: Use when a newcomer asks what Kaoju evidence-led survey research is for, how framing, discovery, acquisition, examination, comparison, reproduction, bounded trials, synthesis, paper production, or wiki export differ, or which public Kaoju command fits a goal.
---

# Isomer Kaoju Welcome

## Overview

Kaoju supports evidence-led surveys of literature, code, datasets, models, and first-hand trials from scope framing through audited synthesis, paper production, and self-contained wiki export. This independent public welcome teaches the supported patterns and recommends a Kaoju entrypoint request without running a manager or research procedure.

## When to Use

Use this skill for Kaoju orientation, procedure comparison, evidence-stage explanation, command learning, readiness guidance, or a read-only next-step recommendation. Phrases such as "survey the landscape," "ingest this repository," or "run a bounded trial" are representative routing cues, not mandatory parser keywords.

Do not use welcome to acquire sources, modify a survey, prepare an environment, run code, compare evidence, write a paper, export a wiki, or approve a Gate. Send concrete work and supplied context to `$isomer-ext-kaoju-entrypoint`.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Classify the request**. Distinguish Kaoju orientation from an actionable survey task that already belongs at the execution entrypoint.
2. **Handle the default**. For empty invocation or broad onboarding, introduce the evidence-led flow and show several high-value patterns from [references/show-options.md](references/show-options.md).
3. **Select one subcommand** from **Subcommands** according to the user's goal.
4. **Load one detail page** and follow its numbered workflow; load the exhaustive command map only when requested.
5. **Explain evidence and interaction boundaries**. Distinguish discover, acquire, and examine; genuine reproduction and bounded trial; and scope, source, template, execution, network, and publication Gates.
6. **Return one public invocation** with required context, expected action, mutation posture, blocker or Gate, and next step.

If the task does not map cleanly to these steps, use the native planning tool to compare the curated Kaoju patterns, public command map, evidence state, interaction boundaries, and user goal, then recommend one entrypoint request or ask for the smallest missing decision.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `show-options` | Present curated framing, landscape, reading-list, intake, comparison, code, trial, paper, and wiki patterns. | [references/show-options.md](references/show-options.md) |
| `choose-path` | Select one public procedure or task-only entrypoint form from an ambiguous survey goal. | [references/show-options.md](references/show-options.md) |
| `show-command-map` | Show every current Kaoju entrypoint command exactly once. | [references/show-command-map.md](references/show-command-map.md) |
| `next-step` | Recommend the next Kaoju or core public route from useful read-only context. | [references/next-step.md](references/next-step.md) |
| `help` | Explain Kaoju welcome, its public commands, evidence stages, Gates, and execution handoff. | [references/help.md](references/help.md) |

## Typical Use Cases

[references/show-options.md](references/show-options.md) supplies each pattern's use condition, routing cues, required context, canonical route, exact invocation, expected action, mutation posture, and next step. It teaches public managers and procedures without exposing protected capability identities or private object-generator syntax.

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable orientation information in that format.

### Essential Output

State the interpreted survey goal, one-sentence pattern fit, required context, recommended public invocation, expected action, mutation posture, missing readiness or Gate, and next step.

### Complete Output

Include alternate patterns, the complete command map, evidence and readiness distinctions, routing rationale, and excluded protected direct routes.

## Guardrails

- DO NOT execute a Kaoju manager, survey procedure, acquisition, comparison, reproduction, trial, writing, build, or export task.
- DO NOT mutate Project, Topic, workspace, environment, survey, dataset, repository, template, paper, wiki, Run, Gate, Service Request, or durable record state.
- DO NOT advertise protected Kaoju logical ids, private paths, or internal object-generator notation as direct user invocations.
- DO NOT copy execution procedures, process registries, artifact bindings, templates, scripts, or protected private resources.
- DO NOT claim that representative phrases are required parser keywords.
- DO NOT treat an example command as approval for later source selection, execution, network exposure, publication, mutation, or another Gate.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the recommended Kaoju pattern and exact public entrypoint request, use descriptive headings when they improve readability, and use lists only for genuinely distinct choices. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat. Name material evidence and interaction boundaries in newcomer language, and keep private stage ownership out of ordinary output.
