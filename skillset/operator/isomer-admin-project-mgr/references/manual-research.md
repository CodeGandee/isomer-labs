# Manual Research

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the Project root, Research Topic, Topic Workspace, requested Topic Actor names, and requested v2 research skill route.
2. Hand off to `isomer-admin-topic-creator plan` or `isomer-admin-topic-creator create` when common topic preparation, actor topology, research bootstrap, or start packs may be missing.
3. If an advanced operator explicitly requests a lower-level actor operation, route Topic Actor CRUD, Topic Actor Workspace materialization, actor repair, and actor diagnostics to `isomer-admin-topic-workspace-mgr`.
4. If an advanced operator explicitly requests compatibility start-pack finalization after all predecessor evidence exists, hand off to `isomer-admin-manual-research-session` with a deprecation warning.
5. Report selected actor cwd targets, optional formal team coexistence material, blockers, and next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to classify whether the user is asking for Project setup, common topic preparation, actor topology management, human-orchestrated research, or formal Topic Team Specialization.

## Guardrails

- Do not route human-orchestrated research to `isomer-admin-topic-team-specialize fast-forward` unless the user explicitly asks for Domain Agent Team Template specialization.
- Do not ask users to chain `isomer-admin-topic-prepare` and `isomer-admin-manual-research-session` for normal manual research setup; route them to `isomer-admin-topic-creator`.
- Do not make all manually controlled workers share `topic.repos.main` as cwd. Each prepared worker should receive its own `topic.actors.workspace` cwd when it needs independent work.
- Do not fabricate Agent Team Instance, Agent Instance, or Agent Workspace refs for Topic Actors.
