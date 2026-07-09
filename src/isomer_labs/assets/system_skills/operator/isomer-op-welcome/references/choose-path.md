# Choose Path

## Workflow

1. Interpret the user's goal into one of the visible usage paths or active owner workflows.
2. Prefer `start-research-manually` when the user wants manual research, human-orchestrated work, multiple manually controlled coding agents, Topic Actors, or a prepared Topic Workspace without a formal Domain Agent Team Template.
3. Prefer `start-research-by-agent-team` when the user explicitly asks for a Domain Agent Team Template, formal Topic Team Specialization, or a team derived from a template.
4. Prefer `isomer-op-project-mgr` for Project setup, Project checks, topic listing, context inspection, runtime initialization, or Project-level routing.
5. Prefer `isomer-op-gui-mgr` for GUI Backend lifecycle, Project Web cache/debug, backend API reference, recent-errors inspection, GUI refresh, and GUI troubleshooting questions.
6. Prefer `isomer-op-toolbox-mgr` for project-local Toolbox creation, conversion, install, inspection, update, disable, uninstall, callback insertion, callback insertion-point discovery, Runtime Params, and effective Toolbox state.
7. Prefer `isomer-op-topic-mgr` for initialized-topic storage, Topic Actors after handoff, package mutation, environment verification, reset checkpoints, and diagnostics.
8. For Houmao loop, runtime, launch profile, mailbox, gateway, and template-mapping explanation, choose the owning operator workflow first: `isomer-op-project-mgr` for Project bootstrap or checks, and `isomer-op-topic-team-specialize` for Topic Team Specialization or launch-facing support. Mention that the owner workflow may delegate bounded Houmao adapter support to `isomer-srv-houmao-interop`.
9. Return `status`, `interpreted_goal`, `recommended_workflow`, `owner_skill`, `safe_first_command`, `blockers`, and `next_action` without mutating state.

If the user's task does not map cleanly to these steps, use your native planning tool to compare the active owner routes, then ask for the missing distinction instead of guessing between manual research and Topic Team Specialization.

## Routing Notes

`choose-path` recommends visible paths; it does not hide or replace them. When a visible path fits, set `recommended_workflow` to `start-research-manually` or `start-research-by-agent-team`.

Manual, human-orchestrated, or multiple manually controlled coding-agent research requests route to `isomer-op-topic-creator`, not to `isomer-op-topic-team-specialize`, unless the prompt explicitly asks for a Domain Agent Team Template.

When the prompt has missing Project context and asks for a context-aware recommendation, route to `next-step` rather than scanning directories or mutating state.

Project Web GUI lifecycle, cache-mode debugging, backend API reference, recent-errors, GUI refresh, and GUI troubleshooting requests route to `isomer-op-gui-mgr`. Project setup still routes to `isomer-op-project-mgr`, and initialized-topic storage or environment repair still routes to `isomer-op-topic-mgr`.

Do not present `isomer-srv-houmao-interop` as a direct first-click owner skill from this welcome surface. It is bounded service support routed by the owning operator workflow.

Do not route project-local Toolbox callback, insertion-point, or Runtime Param work to `isomer-misc-tool-packs`. Tool packs are an explicit misc helper for installable toolset contracts; Toolbox management belongs to `isomer-op-toolbox-mgr`.

Do not ask users or agents to invoke `isomer-op-topic-workspace-mgr`, `isomer-op-topic-prepare`, or `isomer-op-manual-research-session`.
