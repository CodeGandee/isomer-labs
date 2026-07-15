# Choose Path

## Workflow

1. Decide whether the user wants read-only route explanation or has supplied a concrete task that should proceed.
2. Separate execution topology from research paradigm: manual versus formal Agent Team selects who works, while DeepSci versus Kaoju selects how research proceeds.
3. Prefer `start-research-manually` for human-orchestrated Topic Actor work without a formal Agent Team target.
4. Prefer `start-research-by-agent-team` only for explicit specialization or a prompt or authoritative context that establishes a formal Agent Team target.
5. Prefer `start-deepsci-research` for hypothesis development, experiments, analysis, evidence-backed decisions, production writing, review, rebuttal, revision, or submission.
6. Prefer `start-kaoju-survey` for evidence-led literature, codebase, dataset, or model surveys; bounded source-code trials; comparisons; paper production; or wiki export.
7. Route extension availability, installation, registration, compatibility, refresh, or repair to `isomer-op-system-skill-mgr`.
8. Route Project, GUI, identity, Toolbox, Topic, and formal-team operations to the matching active owner skill.
9. When the user supplied a concrete task rather than asking only for orientation, recommend `isomer-op-entrypoint` so the selected route can proceed.
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

DeepSci fits production hypothesis-driven work that develops or evaluates a route through experiments, analysis, decisions, writing, review, rebuttal, or submission. Its entry skill is `isomer-deepsci-pipeline`.

Kaoju fits evidence-led surveys of literature, codebases, datasets, and models, including source ingestion, bounded trials, comparisons, MyST-first paper production, and self-contained wiki export. Its entry skill is `isomer-kaoju-pipeline`.

Treat extension state as an evidence ladder:

1. `catalog-known`: the installed Isomer package describes the capability.
2. Project-declared: the Project Manifest records user-controlled routing intent.
3. Host-usable: compatible managed-receipt or live-inventory evidence establishes that the current host can load the complete family.

Use `show-extensions` for read-only catalog and Project declaration information. Use `Use $isomer-op-system-skill-mgr detect-extensions` or `status` for host-aware read-only evidence. Use `install-extension`, `reconcile-extensions`, or `repair` only through that owner and only with the required mutation authority.

If a declared extension later fails to load, preserve the declaration and recommend `Use $isomer-op-system-skill-mgr repair`. Do not remove user-controlled state automatically.

## Active Operator Routing

- Prefer `isomer-op-project-mgr` for Project setup, checks, topic listing, context inspection, runtime initialization, or Project-level routing.
- Prefer `isomer-op-gui-mgr` for GUI Backend lifecycle, Project Web cache or debug work, backend API reference, recent-errors inspection, GUI refresh, or troubleshooting.
- Prefer `isomer-op-switch-identity` for persistent or one-time work from a selected Topic Actor or Agent workspace cwd.
- Prefer `isomer-op-toolbox-mgr` for project-local Toolbox creation, conversion, installation, inspection, update, disable, uninstall, callback insertion, insertion-point discovery, Runtime Params, or effective state.
- Prefer `isomer-op-topic-mgr` for initialized-topic storage, Topic Actors after handoff, package mutation, environment verification, reset checkpoints, or diagnostics.
- Prefer `isomer-op-topic-team-specialize` only when formal Agent Team intent is established.
- Prefer `isomer-op-entrypoint` when a concrete task should be routed and performed instead of merely explained.

Manual, human-orchestrated, or multiple manually controlled coding-agent research routes to `isomer-op-topic-creator`, not to Topic Team Specialization, unless the user explicitly invokes specialization or formal-team evidence applies to the requested action.

Generic topic preparation, readiness gaps, missing summaries, missing Agent Workspaces, and launch-facing language do not establish formal Agent Team intent. When a formal-team route is valid, name the Domain Agent Team Template, Topic Agent Team Profile or Bundle, Topic Team Instantiation Packet, Agent Team Instance, or selected formal-team evidence.

Do not present `isomer-srv-houmao-interop` as a direct first-click owner skill. Do not route Toolbox callback, insertion-point, or Runtime Param work to `isomer-misc-tool-packs`, which remains an explicitly requested helper. Do not ask users or agents to invoke retired compatibility skills.
