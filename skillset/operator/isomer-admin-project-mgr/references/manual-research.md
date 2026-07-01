# Manual Research

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the Project root, Research Topic, Topic Workspace, requested Topic Actor names, and requested v2 research skill route.
2. Check whether common topic preparation evidence exists. If it is missing, hand off to `isomer-admin-topic-prepare` before starting the manual session.
3. Route Topic Actor CRUD, Topic Actor Workspace materialization, actor repair, and actor diagnostics to `isomer-admin-topic-workspace-mgr`.
4. Hand off the session start, research bootstrap, and per-actor start-pack writing to `isomer-admin-manual-research-session`.
5. Report selected actor cwd targets, optional formal team coexistence material, blockers, and next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to classify whether the user is asking for Project setup, common topic preparation, actor topology management, human-orchestrated research, or formal Topic Team Specialization.

## Guardrails

- Do not route human-orchestrated research to `isomer-admin-topic-team-specialize fast-forward` unless the user explicitly asks for Domain Agent Team Template specialization.
- Do not make all manually controlled workers share `topic.repos.main` as cwd. Each prepared worker should receive its own `topic.actors.workspace` cwd when it needs independent work.
- Do not fabricate Agent Team Instance, Agent Instance, or Agent Workspace refs for Topic Actors.
