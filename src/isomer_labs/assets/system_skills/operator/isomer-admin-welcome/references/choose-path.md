# Choose Path

## Workflow

1. Interpret the user's goal into one of the visible usage paths or active owner workflows.
2. Prefer `start-research-manually` when the user wants manual research, human-orchestrated work, multiple manually controlled coding agents, Topic Actors, or a prepared Topic Workspace without a formal Domain Agent Team Template.
3. Prefer `start-research-by-agent-team` when the user explicitly asks for a Domain Agent Team Template, formal Topic Team Specialization, or a team derived from a template.
4. Prefer `isomer-admin-project-mgr` for Project setup, Project checks, topic listing, context inspection, runtime initialization, or Project-level routing.
5. Prefer `isomer-admin-topic-mgr` for initialized-topic storage, Topic Actors after handoff, package mutation, environment verification, reset checkpoints, and diagnostics.
6. Prefer `isomer-admin-houmao-interop` for Houmao loop, runtime, launch profile, mailbox, gateway, and template-mapping explanation.
7. Return `status`, `interpreted_goal`, `recommended_workflow`, `owner_skill`, `safe_first_command`, `blockers`, and `next_action` without mutating state.

If the user's task does not map cleanly to these steps, use your native planning tool to compare the active owner routes, then ask for the missing distinction instead of guessing between manual research and Topic Team Specialization.

## Routing Notes

`choose-path` recommends visible paths; it does not hide or replace them. When a visible path fits, set `recommended_workflow` to `start-research-manually` or `start-research-by-agent-team`.

Manual, human-orchestrated, or multiple manually controlled coding-agent research requests route to `isomer-admin-topic-creator`, not to `isomer-admin-topic-team-specialize`, unless the prompt explicitly asks for a Domain Agent Team Template.

When the prompt has missing Project context and asks for a context-aware recommendation, route to `next-step` rather than scanning directories or mutating state.

Do not ask users or agents to invoke `isomer-admin-topic-workspace-mgr`, `isomer-admin-topic-prepare`, or `isomer-admin-manual-research-session`.
