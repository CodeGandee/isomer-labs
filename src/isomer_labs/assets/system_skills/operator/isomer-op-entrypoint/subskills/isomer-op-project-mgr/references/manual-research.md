# Manual Research

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the Project root, Research Topic, Topic Workspace, and requested Topic Actor names.
2. Hand off to `isomer-op-topic-creator fast-forward`, `isomer-op-topic-creator step-by-step`, or `isomer-op-topic-creator run-to setup-actors` when topic setup, actor topology, or actor onboarding context may be missing.
3. If an advanced operator explicitly requests a lower-level actor operation, route Topic Actor CRUD, Topic Actor Workspace materialization, actor repair, and actor diagnostics to `isomer-op-topic-mgr`.
4. Report selected actor cwd targets, optional formal team coexistence material, blockers, and next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to classify whether the user is asking for Project setup, common topic preparation, actor topology management, human-orchestrated research, or formal Topic Team Specialization.

## Operational Notes

- Generic topic preparation, launch-facing language, readiness gaps, missing summaries, and missing Agent Workspaces do not establish that target.
- Each prepared worker should receive its own `topic.actors.workspace` cwd when it needs independent work.
- Route it to `isomer-op-topic-creator`.

## Guardrails

- DO NOT route human-orchestrated research to `isomer-op-topic-team-specialize fast-forward` unless the user explicitly invokes specialization or the prompt or authoritative context establishes a formal Agent Team target and applies the requested action to that team.
- DO NOT split normal manual research setup across retired compatibility skills.
- DO NOT make all manually controlled workers share `topic.repos.main` as cwd.
- DO NOT fabricate Agent Team Instance, Agent Instance, or Agent Workspace refs for Topic Actors.
