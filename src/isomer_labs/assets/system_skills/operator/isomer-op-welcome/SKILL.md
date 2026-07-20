---
name: isomer-op-welcome
description: Use when a newcomer asks what Isomer Labs is for, how Projects, Research Topics, Topic Actors, Agent Teams, DeepSci, Kaoju, extensions, Toolboxes, or the Project Web GUI fit together, which public command matches a goal, or what read-only next step to take.
---

# Isomer Operator Welcome

## Overview

Use this independent public skill to learn the common Isomer platform and research paths before asking the execution entrypoint to act. Welcome is read-only: it interprets a goal, teaches representative request language, and recommends one public invocation; `isomer-op-entrypoint` owns concrete route-and-proceed work.

## When to Use

Use this skill for first contact, capability discovery, workflow comparison, command learning, extension orientation, or a read-only recommendation. Representative phrases such as "start a research topic," "use an agent team," or "manage an extension" are routing cues, not mandatory parser keywords.

Do not use this skill to initialize or mutate a Project, create or change a Research Topic, launch an Agent Team, install skills or packages, alter a Toolbox, execute research, or approve a later Gate. Send a concrete task and its existing context to `$isomer-op-entrypoint`, `$isomer-ext-deepsci-entrypoint`, or `$isomer-ext-kaoju-entrypoint` as applicable.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Classify the request**. Distinguish orientation or comparison from an actionable task that already belongs at an execution entrypoint.
2. **Handle the default**. For empty invocation or broad onboarding, introduce Projects, Research Topics, Topic Workspaces, Topic Actors, manual versus formal Agent Team topology, and optional DeepSci versus Kaoju paradigms, then present several high-value patterns from [references/show-options.md](references/show-options.md).
3. **Select one subcommand** from **Subcommands**. Let the user's goal determine the narrowest useful read-only routine.
4. **Load one detail page**. Follow its numbered workflow and load no unrelated welcome references unless the user requests complete output.
5. **Preserve supplied context**. If the request is already concrete, recommend the matching public execution entrypoint with that context carried forward; do not make the user restate it.
6. **Return the recommendation** using **Output Contract** without executing the recommended task.

If the user's task does not map cleanly to these steps, use the native planning tool to build a bounded orientation plan from the typical use cases, public command map, supplied context, read-only boundary, and user goal, then recommend one public next invocation or ask for the smallest missing decision.

## Subcommands

These commands are peer read-only routines. Manual versus Agent Team selects execution topology; DeepSci versus Kaoju selects a research paradigm, so one choice does not imply the other.

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `show-options` | Present the most common platform, research-start, extension, GUI, identity, Toolbox, and environment-support patterns before exhaustive command detail. | [references/show-options.md](references/show-options.md) |
| `show-extensions` | Explain the package-catalog extension pairs and distinguish catalog, Project declaration, public-name observation, and verified pack evidence. | [references/show-extensions.md](references/show-extensions.md) |
| `choose-path` | Translate an ambiguous newcomer goal into one recommended public welcome or execution invocation. | [references/choose-path.md](references/choose-path.md) |
| `show-command-map` | Show every current `isomer-op-entrypoint` public command exactly once with its use condition and exact invocation. | [references/show-command-map.md](references/show-command-map.md) |
| `next-step` | Use only useful read-only context to recommend the next public invocation. | [references/next-step.md](references/next-step.md) |
| `start-research-manually` | Explain human-orchestrated Research Topic setup through Topic Actors without assuming a formal Agent Team. | [references/start-research-manually.md](references/start-research-manually.md) |
| `start-research-by-agent-team` | Explain formal Topic Team Specialization from a Domain Agent Team Template. | [references/start-research-by-agent-team.md](references/start-research-by-agent-team.md) |
| `start-deepsci-research` | Introduce hypothesis-driven production research and route learning or concrete work to the correct DeepSci public skill. | [references/start-deepsci-research.md](references/start-deepsci-research.md) |
| `start-kaoju-survey` | Introduce evidence-led survey research and route learning or concrete work to the correct Kaoju public skill. | [references/start-kaoju-survey.md](references/start-kaoju-survey.md) |
| `help` | Explain welcome, list its public commands, and show how welcome hands off to execution. | [references/help.md](references/help.md) |

## Typical Use Cases

The curated core patterns live in [references/show-options.md](references/show-options.md). Each pattern states when it fits, representative routing cues, required context, the canonical public route, an exact invocation, expected action, mutation posture, and likely next step. Load the complete entrypoint inventory only for `show-command-map`, `help`, or an explicit complete-output request.

## Read-Only Boundary

`next-step` and `show-extensions` may announce and run documented read-only `isomer-cli` inspection commands when the evidence materially improves a recommendation. Choosing an option or showing an example never authorizes the example's mutation, network access, execution, approval, or later Gate.

If a concrete task reaches this skill through implicit host routing, hand the complete task context to the sibling execution entrypoint. Do not perform an owner workflow inside welcome.

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable orientation information in that format.

### Essential Output

State the interpreted goal, one-sentence use-case fit, required context, recommended public invocation, expected action, mutation posture, blocker or missing decision, and next step.

### Complete Output

Also include alternate patterns, the complete command map, read-only evidence used, routing rationale, and excluded retired or protected direct routes.

## Guardrails

- DO NOT execute the public invocation that welcome recommends.
- DO NOT mutate a Project, Research Topic, Topic Workspace, Topic Actor, Agent Team, extension declaration, installed skill root, Toolbox, package environment, or research record.
- DO NOT advertise a protected logical id or parent-owned subskill designator as a direct user invocation.
- DO NOT describe representative natural-language phrases as mandatory parser keywords.
- DO NOT copy entrypoint execution procedures or private protected resources into this welcome bundle.
- DO NOT treat an example invocation as approval for mutation, execution, network exposure, publication, or a later Gate.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the recommended path, use descriptive headings when they improve readability, and use lists only for genuinely distinct choices. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat. Keep internal protected routing details out of ordinary newcomer output.
