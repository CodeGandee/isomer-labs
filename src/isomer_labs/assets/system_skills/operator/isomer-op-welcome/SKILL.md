---
name: isomer-op-welcome
description: Use when manually invoked by an Isomer Labs Project Operator Session to show supported operator workflow options, choose a safe owner skill, map visible usage paths such as start-research-manually or start-research-by-agent-team, or recommend a read-only next step. Manual invocation only.
---

# Isomer Admin Welcome

## Overview

Manual invocation only. Use this command-style operator skill as the action-oriented welcome menu for Isomer Labs. It names the active owner skill for each supported workflow and keeps all mutation inside those owner skills.

## When to Use

Use this skill when the user asks what Isomer Labs can do, which operator path to choose, how to start research manually, how to start research by Agent Team, which owner skill manages the Project Web GUI, which owner skill manages project-local Toolboxes, or what the next safe owner workflow is.

Do not use this skill to execute Project initialization, Research Topic creation, Topic Workspace mutation, package installation, Topic Team Specialization, Houmao launch, or research-paradigm v2 bootstrap. Route those requests to the active owner skill named by this menu.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Default option mode**:
   - Match an empty invocation or a broad onboarding request such as "what can Isomer Labs do?".
   - Select `show-options`, load [references/show-options.md](references/show-options.md), and print the visible usage paths and direct owner-skill routes.
2. **Visible usage path mode**:
   - Match when the user names `start-research-manually` or `start-research-by-agent-team`.
   - Load the matching usage-path reference and recommend its owner skill, safe first command, mutation boundary, and next action.
3. **Routing and support mode**:
   - Match when the user asks for help, an owner-skill map, ambiguous path choice, or a context-aware next step.
   - Select `help`, `choose-path`, `show-skill-map`, or `next-step` from the **Routing and Support Subcommands** table.
4. **Read-only context mode**:
   - Use `next-step` only when the user asks for context-aware guidance.
   - Announce any read-only Project inspection command before running it.
   - Do not run mutating commands from this skill.
5. **Report the welcome result** using **Essential Output** by default and **Complete Output** when requested.

If the user's task does not map cleanly to these steps, use your native planning tool to build a bounded routing plan from the user goal, visible usage paths, active owner skills, read-only context evidence, output contract, and guardrails in this skill, then recommend one safe owner workflow or ask for the missing decision.

## Usage Path Subcommands

These typical use cases are first-class public subcommands. Do not hide them inside `choose-path`.

| Subcommand | Intent | Owner Skill | Safe First Command | Detail |
| --- | --- | --- | --- | --- |
| `start-research-manually` | Create or prepare a Research Topic for human-orchestrated work with Topic Actors | `isomer-op-topic-creator` | `Use $isomer-op-topic-creator fast-forward` when the user has approved setup, or `Use $isomer-op-topic-creator step-by-step` for guided setup | [references/start-research-manually.md](references/start-research-manually.md) |
| `start-research-by-agent-team` | Specialize a Domain Agent Team Template over a Research Topic before later approval, materialization, or launch | `isomer-op-topic-team-specialize` | `Use $isomer-op-topic-team-specialize fast-forward` with the Research Topic and Domain Agent Team Template | [references/start-research-by-agent-team.md](references/start-research-by-agent-team.md) |

## Routing and Support Subcommands

Load only the selected reference page before answering.

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `help` | Print what this skill does, visible usage paths, owner routes, outputs, and guardrails | [references/help.md](references/help.md) |
| `show-options` | Print the default action-oriented menu with usage paths and active owner skills | [references/show-options.md](references/show-options.md) |
| `choose-path` | Interpret an ambiguous user goal and recommend one visible usage path or owner workflow without mutating state | [references/choose-path.md](references/choose-path.md) |
| `show-skill-map` | Show a compact direct-invocation table from user intent to active owner skill | [references/show-skill-map.md](references/show-skill-map.md) |
| `next-step` | Run only read-only Project inspection when explicitly useful, then recommend the next owner workflow | [references/next-step.md](references/next-step.md) |

## Required Inputs

- A user goal, selected visible usage path, or request for options.
- Optional Project root or current working directory when `next-step` needs context-aware guidance.
- Optional Research Topic, Topic Workspace, Domain Agent Team Template, or Houmao concept named in the prompt.

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

### Essential Output

Explain naturally how you understood the user's goal, then recommend the visible workflow and active owner skill. Provide the safe first invocation or read-only command, name any missing decision or context that blocks progress, and state the next action.

### Complete Output

Group the complete explanation by Project and prompt evidence, read-only commands, alternate owner workflows, routing rationale, and any retired compatibility routes excluded from consideration.

## Guardrails

- MUST keep the default posture read-only. This skill may recommend an owner skill and safe first command, but it must not initialize Projects, create Research Topics, mutate Topic Workspaces, install packages, specialize teams, launch agents, or bootstrap research-paradigm v2 artifacts.

- MUST limit `next-step` to read-only Project inspection commands such as `isomer-cli project validate`, `isomer-cli doctor`, `isomer-cli project topics list`, and `isomer-cli project context show`. Report commands run in Complete Output.

- MUST route Project setup, Project checks, topic listing, context inspection, runtime initialization, and Project-level routing to `isomer-op-project-mgr`.

- MUST route Project Web GUI lifecycle, GUI Backend launch or status, cache-mode debugging, GUI refresh, recent-errors inspection, backend API reference, or GUI troubleshooting to `isomer-op-gui-mgr`. This welcome skill may recommend the owner route, but it must not start the GUI Backend, inspect HTTP routes, rebuild query-index rows, or troubleshoot code defects itself.

- MUST route blank or partial Research Topic creation and manual-research-ready topic preparation to `isomer-op-topic-creator`.

- MUST route initialized-topic storage, Topic Actors, package mutation, environment verification, reset checkpoints, and diagnostics to `isomer-op-topic-mgr`.

- MUST route Topic Team Specialization to `isomer-op-topic-team-specialize` only when the user explicitly invokes that skill or a named specialization route, or when the prompt or authoritative context establishes a formal Agent Team target such as a Domain Agent Team Template, Topic Agent Team Profile or Bundle, Topic Team Instantiation Packet, Agent Team Instance, or selected formal-team material.

- MUST route Houmao loop, runtime, launch profile, mailbox, gateway, and template-mapping questions to the owning operator workflow first. Project bootstrap or check questions belong to `isomer-op-project-mgr`; launch-facing work belongs to `isomer-op-topic-team-specialize` only when the launch target is a formal Agent Team established by the prompt or authoritative context. Runtime, Topic Service Master, GUI, topic preparation, and other launch-facing requests retain their actual owners. Those workflows may delegate bounded Houmao adapter support to `isomer-srv-houmao-interop`.

- DO NOT infer a formal Agent Team target from generic topic preparation, launch-facing language, readiness gaps, missing summaries, missing Agent Workspaces, or Topic Workspace context alone. When a contextual formal-team route is valid, name the evidence in the recommendation.

- MUST route project-local Toolbox creation, conversion, install, inspection, callback insertion, callback insertion-point, Runtime Param, disable, uninstall, or source-update questions to `isomer-op-toolbox-mgr`. This welcome skill may recommend the owner route, but it must not author Toolbox files, install Toolboxes, mutate callback registries, or mutate Runtime Params itself.

- DO NOT ask users or agents to invoke `isomer-op-topic-workspace-mgr`, `isomer-op-topic-prepare`, or `isomer-op-manual-research-session`; those are retired operator compatibility skills, not active routes.

- DO NOT route manual, human-orchestrated, or multiple manually controlled coding-agent research requests to Topic Team Specialization unless the user explicitly invokes specialization or the prompt or authoritative context establishes a formal Agent Team target and applies the requested action to that team.

- DO NOT automatically route to `isomer-misc-tool-packs`. Mention `isomer-misc-tool-packs` only as a manual skill when the user explicitly asks for installable toolsets, and keep package mutation routing with the active owner skill.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
