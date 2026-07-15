---
name: isomer-op-welcome
description: Use when manually invoked by an Isomer Labs Project Operator Session to discover supported workflows, compare manual, Agent Team, DeepSci, or Kaoju research paths, inspect optional system-skill extensions, map a goal to an active owner skill, or request a read-only next step. Manual invocation only.
---

# Isomer Operator Welcome

## Overview

Manual invocation only. Use this command-style operator skill as the action-oriented welcome menu for Isomer Labs. It presents common research paths, optional research paradigms, operating and customization capabilities, and the active route from discovery to execution while keeping all mutation inside the owning workflow.

## When to Use

Use this skill when the user asks what Isomer Labs can do, which research or operator path to choose, how DeepSci differs from Kaoju, which optional system-skill extensions exist, how to start research manually or by Agent Team, which owner manages system-skill extensions, the Project Web GUI, or project-local Toolboxes, or what the next safe owner workflow is.

Do not use this skill to execute a concrete task, Project initialization, Research Topic creation, Topic Workspace mutation, package or system-skill extension installation, Topic Team Specialization, Houmao launch, or research-paradigm bootstrap. Route concrete work through `isomer-op-entrypoint` or the active owner skill named by this menu.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Handle the default**. Select `show-options` for an empty invocation or broad onboarding request such as "what can Isomer Labs do?".
2. **Select one subcommand** from the **Subcommands** table that matches the user's research path, extension question, routing need, or context request.
3. **Load the selected reference** and follow its `## Workflow`; load no unrelated reference pages.
4. **Preserve the read-only boundary**. Announce any inspection command before running it, and route mutation or concrete execution to the named owner or `isomer-op-entrypoint`.
5. **Report the welcome result** using **Essential Output** by default and **Complete Output** when requested.

If the user's task does not map cleanly to these steps, use your native planning tool to build a bounded routing plan from the user goal, visible usage paths, active owner skills, read-only context evidence, output contract, and guardrails in this skill, then recommend one safe owner workflow or ask for the missing decision.

## Subcommands

These routines are peers. Manual versus Agent Team selects execution topology; DeepSci versus Kaoju selects an optional research paradigm. Treat those as independent decisions.

| Subcommand | Kind | Use For | Owner or Safe Next Route | Detail |
| --- | --- | --- | --- | --- |
| `start-research-manually` | Research topology | Create or prepare a Research Topic for human-orchestrated work with Topic Actors | `Use $isomer-op-topic-creator fast-forward` or `Use $isomer-op-topic-creator step-by-step` | [references/start-research-manually.md](references/start-research-manually.md) |
| `start-research-by-agent-team` | Research topology | Specialize a Domain Agent Team Template over a Research Topic | `Use $isomer-op-topic-team-specialize fast-forward` | [references/start-research-by-agent-team.md](references/start-research-by-agent-team.md) |
| `start-deepsci-research` | Research paradigm | Develop or evaluate a hypothesis through the optional DeepSci production-research paradigm | `Use $isomer-op-entrypoint` with the concrete DeepSci goal when readiness is not established | [references/start-deepsci-research.md](references/start-deepsci-research.md) |
| `start-kaoju-survey` | Research paradigm | Survey literature, code, datasets, or models through the optional Kaoju evidence-led paradigm | `Use $isomer-op-entrypoint` with the concrete Kaoju goal when readiness is not established | [references/start-kaoju-survey.md](references/start-kaoju-survey.md) |
| `show-options` | Discovery | Print the default grouped capability menu | Remain in this read-only welcome skill | [references/show-options.md](references/show-options.md) |
| `show-extensions` | Discovery | List package-catalog research extensions, Project declarations when available, and the route to host usability checks | `Use $isomer-op-system-skill-mgr` for host-aware lifecycle work | [references/show-extensions.md](references/show-extensions.md) |
| `choose-path` | Routing | Interpret an ambiguous goal and recommend one visible path or owner | Remain read-only until the user invokes the next route | [references/choose-path.md](references/choose-path.md) |
| `show-skill-map` | Discovery | Map user intent to active operator and optional extension entry skills | Remain in this read-only welcome skill | [references/show-skill-map.md](references/show-skill-map.md) |
| `next-step` | Routing | Run only useful read-only inspection, then recommend the next route | Remain read-only until the user invokes the next route | [references/next-step.md](references/next-step.md) |
| `help` | Support | Print usage, paths, owner routes, outputs, and guardrails | Remain in this read-only welcome skill | [references/help.md](references/help.md) |

## Required Inputs

- A user goal, selected visible usage path, or request for options.
- Optional Project root or current working directory when `next-step` needs context-aware guidance.
- Optional Research Topic, Topic Workspace, Domain Agent Team Template, or Houmao concept named in the prompt.

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

### Essential Output

Explain naturally how you understood the user's goal, then recommend the visible workflow and active owner skill or extension entry skill. Provide the safe first invocation or read-only command, distinguish extension availability evidence when relevant, name any missing decision or context that blocks progress, and state the next action.

### Complete Output

Group the complete explanation by Project and prompt evidence, read-only commands, alternate owner workflows, routing rationale, and any retired compatibility routes excluded from consideration.

## Operational Contract

- Keep the default posture read-only. This skill may recommend an owner skill and safe first command, but it must not initialize Projects, create Research Topics, mutate Topic Workspaces, install packages or system-skill extensions, register extensions, specialize teams, launch agents, or bootstrap research-paradigm artifacts.
- Limit `next-step` to read-only inspection commands such as `isomer-cli project validate`, `isomer-cli doctor`, `isomer-cli project topics list`, `isomer-cli project context show`, `isomer-cli project self show`, `isomer-cli project outputs policy`, `isomer-cli system-skills extensions list`, and `isomer-cli project system-extensions list`. Report commands run in Complete Output.
- Route concrete tasks that should proceed beyond orientation to `isomer-op-entrypoint`, which selects one owner skill, extension skill, or CLI family and proceeds under that route's guardrails.
- Route system-skill extension detection, reconciliation, installation, status, compatibility diagnosis, host refresh guidance, and repair to `isomer-op-system-skill-mgr`. This welcome skill may report catalog and Project declaration state, but it must not install files, register declarations, inspect guessed host roots, or claim host usability without the manager's evidence.
- Distinguish `catalog-known`, Project-declared, and host-usable extension state. A catalog entry describes a packaged capability; a Project declaration is authoritative routing intent; only compatible managed-receipt or live-inventory evidence establishes host usability.
- Present DeepSci as the optional hypothesis-driven production-research paradigm through `isomer-deepsci-pipeline`, and Kaoju as the optional evidence-led literature, codebase, dataset, model, trial, comparison, paper, and wiki-survey paradigm through `isomer-kaoju-pipeline`. Unknown or missing extension availability routes to `isomer-op-system-skill-mgr`; missing Project, Topic Workspace, actor or agent workspace, or paradigm bootstrap readiness routes through `isomer-op-entrypoint` to the applicable owner.
- Treat research paradigm and execution topology as independent choices. Selecting DeepSci or Kaoju does not imply manual Topic Actor work or a formal Agent Team, and selecting manual or Agent Team setup does not select a research paradigm.
- Route Project setup, Project checks, topic listing, context inspection, runtime initialization, and Project-level routing to `isomer-op-project-mgr`.
- Route Project Web GUI lifecycle, GUI Backend launch or status, cache-mode debugging, GUI refresh, recent-errors inspection, backend API reference, or GUI troubleshooting to `isomer-op-gui-mgr`. This welcome skill may recommend the owner route, but it must not start the GUI Backend, inspect HTTP routes, rebuild query-index rows, or troubleshoot code defects itself.
- Route blank or partial Research Topic creation and manual-research-ready topic preparation to `isomer-op-topic-creator`.
- Route initialized-topic storage, Topic Actors, package mutation, environment verification, reset checkpoints, and diagnostics to `isomer-op-topic-mgr`.
- Route Topic Team Specialization to `isomer-op-topic-team-specialize` only when the user explicitly invokes that skill or a named specialization route, or when the prompt or authoritative context establishes a formal Agent Team target such as a Domain Agent Team Template, Topic Agent Team Profile or Bundle, Topic Team Instantiation Packet, Agent Team Instance, or selected formal-team material.
- Route Houmao loop, runtime, launch profile, mailbox, gateway, and template-mapping questions to the owning operator workflow first. Project bootstrap or check questions belong to `isomer-op-project-mgr`; launch-facing work belongs to `isomer-op-topic-team-specialize` only when the launch target is a formal Agent Team established by the prompt or authoritative context. Runtime, Topic Service Master, GUI, topic preparation, and other launch-facing requests retain their actual owners. Those workflows may delegate bounded Houmao adapter support to `isomer-srv-houmao-interop`.
- Route project-local Toolbox creation, conversion, install, inspection, callback insertion, callback insertion-point, Runtime Param, disable, uninstall, or source-update questions to `isomer-op-toolbox-mgr`. This welcome skill may recommend the owner route, but it must not author Toolbox files, install Toolboxes, mutate callback registries, or mutate Runtime Params itself.
- Distinguish system-skill extensions from Toolboxes and from the `isomer-cli ext` namespace. System-skill extensions install optional agent-skill families, Toolboxes provide project-local callback and Runtime Param customization, and `isomer-cli ext` exposes runtime or compatibility command families.

## Operational Notes

- When a contextual formal-team route is valid, name the evidence in the recommendation.
- Mention `isomer-misc-tool-packs` only as a manual skill when the user explicitly asks for installable toolsets, and keep package mutation routing with the active owner skill.

## Guardrails

- DO NOT infer a formal Agent Team target from generic topic preparation, launch-facing language, readiness gaps, missing summaries, missing Agent Workspaces, or Topic Workspace context alone.
- DO NOT ask users or agents to invoke `isomer-op-topic-workspace-mgr`, `isomer-op-topic-prepare`, or `isomer-op-manual-research-session`; those are retired operator compatibility skills, not active routes.
- DO NOT route manual, human-orchestrated, or multiple manually controlled coding-agent research requests to Topic Team Specialization unless the user explicitly invokes specialization or the prompt or authoritative context establishes a formal Agent Team target and applies the requested action to that team.
- DO NOT automatically route to `isomer-misc-tool-packs`.
## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
