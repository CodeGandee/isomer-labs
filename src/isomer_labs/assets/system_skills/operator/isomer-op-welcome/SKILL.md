---
name: isomer-op-welcome
description: Manual invocation only; use when an Isomer Labs Project Operator Session needs to show supported operator workflow options, choose a safe owner skill, map visible usage paths such as start-research-manually or start-research-by-agent-team, or recommend a read-only next step.
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

Default to **Essential Output** in chat. Print **Complete Output** only when the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output.

### Essential Output

Report:

- `status`: welcome, routing, recommendation, or blocker result.
- `interpreted_goal`: the normalized user goal or selected usage path.
- `recommended_workflow`: visible usage path or owner workflow.
- `owner_skill`: direct active owner skill to invoke.
- `safe_first_command`: the first owner-skill invocation or read-only inspection command.
- `blockers`: missing user decision, missing topic substance, missing template, unavailable Project context, or unsafe mutation request.
- `next_action`: choose a path, provide missing input, invoke the owner skill directly, or stop on blocker.

### Complete Output

When requested, include:

- `context_evidence`: read-only Project context facts, prompt evidence, and selected Project root.
- `read_only_commands_run`: any `isomer-cli project validate`, `isomer-cli doctor`, `isomer-cli project topics list`, or `isomer-cli project context show` command used for `next-step`.
- `alternate_owner_workflows`: plausible lower-priority visible usage paths or owner skills.
- `routing_rationale`: why the recommended owner skill is safer than nearby alternatives.
- `retired_route_exclusions`: explicit note that retired operator compatibility skills are not active routes when relevant.

## Guardrails

The default posture is read-only. This skill may recommend an owner skill and safe first command, but it must not initialize Projects, create Research Topics, mutate Topic Workspaces, install packages, specialize teams, launch agents, or bootstrap research-paradigm v2 artifacts.

`next-step` may use only read-only Project inspection commands such as `isomer-cli project validate`, `isomer-cli doctor`, `isomer-cli project topics list`, and `isomer-cli project context show`. Report commands run in Complete Output.

Route Project setup, Project checks, topic listing, context inspection, runtime initialization, and Project-level routing to `isomer-op-project-mgr`.

Route Project Web GUI lifecycle, GUI Backend launch or status, cache-mode debugging, GUI refresh, recent-errors inspection, backend API reference, or GUI troubleshooting to `isomer-op-gui-mgr`. This welcome skill may recommend the owner route, but it must not start the GUI Backend, inspect HTTP routes, rebuild query-index rows, or troubleshoot code defects itself.

Route blank or partial Research Topic creation and manual-research-ready topic preparation to `isomer-op-topic-creator`.

Route initialized-topic storage, Topic Actors, package mutation, environment verification, reset checkpoints, and diagnostics to `isomer-op-topic-mgr`.

Route Topic Team Specialization to `isomer-op-topic-team-specialize` only when the user asks for a Domain Agent Team Template or formal Agent Team path.

Route Houmao loop, runtime, launch profile, mailbox, gateway, and template-mapping questions to the owning operator workflow first. Project bootstrap or check questions belong to `isomer-op-project-mgr`; Topic Team Specialization and launch-facing questions belong to `isomer-op-topic-team-specialize`. Those workflows may delegate bounded Houmao adapter support to `isomer-srv-houmao-interop`.

Route project-local Toolbox creation, conversion, install, inspection, callback insertion, callback insertion-point, Runtime Param, disable, uninstall, or source-update questions to `isomer-op-toolbox-mgr`. This welcome skill may recommend the owner route, but it must not author Toolbox files, install Toolboxes, mutate callback registries, or mutate Runtime Params itself.

Do not ask users or agents to invoke `isomer-op-topic-workspace-mgr`, `isomer-op-topic-prepare`, or `isomer-op-manual-research-session`; those are retired operator compatibility skills, not active routes.

Do not route manual, human-orchestrated, or multiple manually controlled coding-agent research requests to Topic Team Specialization unless the user explicitly asks for a Domain Agent Team Template.

Do not automatically route to `isomer-misc-tool-packs`. Mention `isomer-misc-tool-packs` only as a manual skill when the user explicitly asks for installable toolsets, and keep package mutation routing with the active owner skill.
