---
skill_invocation_notation: >
  Top-level skill entrypoints use SKILL.md. Parent-scoped subskill entrypoints use
  SKILL-MAIN.md and are loaded explicitly through their parent; nested SKILL.md is
  accepted only as legacy input when SKILL-MAIN.md is absent.
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Show Options

## Workflow

1. Print the visible usage paths first, beginning with research setup: `start-research-manually` and `start-research-by-agent-team`.
2. Print the optional research paradigm paths `start-deepsci-research` and `start-kaoju-survey`; explain that paradigm and execution topology are independent choices.
3. Show Project operation routes for Project lifecycle, Topic management, Project Web GUI, identity posture, and formal Agent Team work.
4. Show customization routes for system-skill extensions and project-local Toolboxes, keeping their ownership and meanings distinct.
5. Offer `Use $isomer-op-entrypoint` when the user already has a concrete task and wants Isomer to route and proceed.
6. Ask the user to choose a visible path, inspect extensions, or describe a goal for the public entrypoint.

If the user's task does not map cleanly to these steps, use your native planning tool to build the shortest helpful menu from the visible research paths, package-catalog extension metadata, active owner skills, and guardrails, then print that menu without mutating state.

## Start and Organize Research

| User Goal | Parent-Scoped Route | Public Invocation |
| --- | --- | --- |
| Start research manually with human-orchestrated Topic Actors. | `isomer-op-entrypoint->topic-create` | `$isomer-op-entrypoint use topic-create to fast-forward the requested setup` or guide it step by step. |
| Start research by formal Agent Team from a Domain Agent Team Template. | `isomer-op-entrypoint->topic-team` | `$isomer-op-entrypoint use topic-team to fast-forward specialization for the selected formal team`. |

## Choose an Optional Research Paradigm

| User Goal | Entry Skill | Safe Route |
| --- | --- | --- |
| Develop or evaluate a hypothesis with experiments, analysis, decisions, writing, review, rebuttal, or submission. | `isomer-ext-deepsci-entrypoint` | Select `start-deepsci-research`; use `$isomer-ext-deepsci-entrypoint use <subcommand> to <task>` when ready, or `$isomer-op-entrypoint` with the concrete goal when readiness is unknown. |
| Survey literature, codebases, datasets, or models; run bounded trials or comparisons; produce a paper or wiki. | `isomer-ext-kaoju-entrypoint` | Select `start-kaoju-survey`; use `$isomer-ext-kaoju-entrypoint use <subcommand> to <task>` when ready, or `$isomer-op-entrypoint` with the concrete goal when readiness is unknown. |

These rows describe package-catalog capabilities, not proof of current host installation. Use `show-extensions` for catalog and Project declaration state, and `$isomer-op-entrypoint use system-skills to <task>` for pack integrity, installation, upgrade, compatibility, refresh, or repair.

## Operate the Project

Use these routes for Project setup or checks, Topic management, identity posture, Project Web GUI work, and contextually established Topic Team work.

| User Goal | Parent-Scoped Route | Public Invocation |
| --- | --- | --- |
| Initialize or check an Isomer Project, list topics, inspect context, or prepare runtime. | `isomer-op-entrypoint->project` | `$isomer-op-entrypoint use project to <task>`. |
| Start, inspect, refresh, debug, or troubleshoot the Project Web GUI, or look up GUI Backend API routes. | `isomer-op-entrypoint->gui` | `$isomer-op-entrypoint use gui to <task>`. |
| Act from a selected Topic Actor or Agent workspace cwd for takeover or one-time prompt execution. | `isomer-op-entrypoint->identity` | `$isomer-op-entrypoint use identity to <task>`. |
| Manage an initialized Research Topic, Topic Actors, package mutation, environment verification, reset checkpoints, or diagnostics. | `isomer-op-entrypoint->topic-manage` | `$isomer-op-entrypoint use topic-manage to <task>`. |
| Need Houmao adapter support during Project or formal Agent Team work. | Owning parent-scoped route | Use `$isomer-op-entrypoint use project to <task>` for Project bootstrap or checks. Use `topic-team` only when the prompt or authoritative context establishes a formal Agent Team target. |

## Extend and Customize

| User Goal | Parent-Scoped Route | Public Invocation |
| --- | --- | --- |
| Detect, reconcile, install, upgrade, inspect, or repair optional system-skill extensions such as DeepSci or Kaoju. | `isomer-op-entrypoint->system-skills` | `$isomer-op-entrypoint use system-skills to <task>`. |
| Create, convert, install, inspect, update, disable, uninstall, or explain project-local Toolboxes, callback insertion points, callback declarations, or Toolbox Runtime Params. | `isomer-op-entrypoint->toolbox` | `$isomer-op-entrypoint use toolbox to <task>`. |

A system-skill extension installs an optional agent-skill family. A Toolbox provides project-local callback and Runtime Param customization. The `isomer-cli ext` namespace exposes runtime or compatibility commands and is not the system-skill installer.

## Route a Concrete Task

When the user already knows the desired outcome, recommend `Use $isomer-op-entrypoint` with the concrete task. The entrypoint selects one owner skill, extension skill, or CLI family and proceeds under that route's readiness and mutation rules. The welcome skill itself remains read-only.

Do not list retired operator compatibility skills or protected service logical ids as active invocations. Mention `isomer-op-entrypoint->tool-packs` only when the user explicitly asks for installable toolsets. Do not infer a formal Agent Team from generic topic preparation, launch-facing work, readiness gaps, missing summaries, or missing Agent Workspaces.
