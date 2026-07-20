---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Choose Path

## Workflow

1. Decide whether the user wants read-only route explanation or has supplied a concrete task that should proceed.
2. Separate execution topology from research paradigm: manual versus formal Agent Team selects who works, while DeepSci versus Kaoju selects how research proceeds.
3. Prefer `start-research-manually` for human-orchestrated Topic Actor work without a formal Agent Team target.
4. Prefer `start-research-by-agent-team` only for explicit specialization or a prompt or authoritative context that establishes a formal Agent Team target.
5. Prefer `start-deepsci-research` for hypothesis development, experiments, analysis, evidence-backed decisions, production writing, review, rebuttal, revision, or submission.
6. Prefer `start-kaoju-survey` for evidence-led literature, codebase, dataset, or model surveys; bounded source-code trials; comparisons; paper production; or wiki export.
7. Route extension availability, installation, upgrade, registration, compatibility, refresh, or repair through `isomer-op-entrypoint->system-skills`.
8. Route Project, GUI, identity, Toolbox, Topic, and formal-team operations through the matching parent-scoped member of `isomer-op-entrypoint`.
9. When the user supplied a concrete task rather than asking only for orientation, recommend `$isomer-op-entrypoint` so the selected route can proceed.
10. Explain how the goal was understood, recommend one visible workflow or owner route, provide the safe first invocation, name blockers, and state the next action without mutating state.

If the user's task does not map cleanly to these steps, use your native planning tool to compare the active owner, extension, and entrypoint routes, then ask for the smallest missing distinction instead of guessing.

This routine recommends visible paths for orientation. Use it to recommend the visible workflow or owner route, explain how it understood the goal, distinguish manual research from formal-team and optional-paradigm work, name the owner skill and safe first invocation, report blockers, and state the next action.

## Research Choice Dimensions

| Question | Choices | Meaning |
| --- | --- | --- |
| Who or what topology will conduct the work? | Manual Topic Actors or a formal Agent Team | Execution topology and workspace preparation. |
| Which optional research paradigm fits the goal? | DeepSci or Kaoju | Research process, evidence contract, and extension entry skill. |

The choices are independent. A DeepSci or Kaoju workflow may run through manual Topic Actors or an established formal Agent Team. A manual or Agent Team setup does not imply either research paradigm.

## Extension Routing

DeepSci fits production hypothesis-driven work that develops or evaluates a route through experiments, analysis, decisions, writing, review, rebuttal, or submission. Its entry skill is `isomer-ext-deepsci-entrypoint`.

Kaoju fits evidence-led surveys of literature, codebases, datasets, and models, including source ingestion, bounded trials, comparisons, MyST-first paper production, and self-contained wiki export. Its entry skill is `isomer-ext-kaoju-entrypoint`.

Treat extension state as an evidence ladder:

1. `catalog-known`: the installed Isomer package describes the capability.
2. Project-declared: the Project Manifest records user-controlled routing intent.
3. `entrypoint_seen`: limited live inventory shows the public entrypoint name, but protected integrity and current-session usability remain unverified.
4. Pack-integrity-verified: current v4 receipt or explicit-root evidence establishes complete protected coverage. A new installation or upgrade may still need a host refresh before the current session can load it.

Use `show-extensions` for read-only catalog and Project declaration information. Use `$isomer-op-entrypoint use system-skills to detect extensions` or inspect status for host-aware read-only evidence. Use installation, upgrade, reconciliation, or repair only through that public route and with the required mutation authority.

If a declared extension later fails to load, preserve the declaration and recommend `$isomer-op-entrypoint use system-skills to repair the extension`. Do not remove user-controlled state automatically.

## Active Operator Routing

- Prefer `isomer-op-entrypoint->project` for Project setup, checks, topic listing, context inspection, runtime initialization, or Project-level routing.
- Prefer `isomer-op-entrypoint->gui` for GUI Backend lifecycle, Project Web cache or debug work, backend API reference, recent-errors inspection, GUI refresh, or troubleshooting.
- Prefer `isomer-op-entrypoint->identity` for persistent or one-time work from a selected Topic Actor or Agent workspace cwd.
- Prefer `isomer-op-entrypoint->toolbox` for project-local Toolbox creation, conversion, installation, inspection, update, disable, uninstall, callback insertion, insertion-point discovery, Runtime Params, or effective state.
- Prefer `isomer-op-entrypoint->topic-manage` for initialized-topic storage, Topic Actors after handoff, package mutation, environment verification, reset checkpoints, or diagnostics.
- Prefer `isomer-op-entrypoint->topic-team` only when formal Agent Team intent is established.
- Prefer `$isomer-op-entrypoint` when a concrete task should be routed and performed instead of merely explained.

Manual, human-orchestrated, or multiple manually controlled coding-agent research routes to `isomer-op-entrypoint->topic-create`, not to Topic Team Specialization, unless the user explicitly invokes specialization or formal-team evidence applies to the requested action.

Generic topic preparation, readiness gaps, missing summaries, missing Agent Workspaces, and launch-facing language do not establish formal Agent Team intent. When a formal-team route is valid, name the Domain Agent Team Template, Topic Agent Team Profile or Bundle, Topic Team Instantiation Packet, Agent Team Instance, or selected formal-team evidence.

Do not present protected service members as direct first-click skills. Do not route Toolbox callback, insertion-point, or Runtime Param work to `isomer-op-entrypoint->tool-packs`, which remains an explicitly requested helper route. Do not ask users or agents to invoke retired compatibility skills.
