---
name: deepsci-mini-operator-control
description: Generated operator-control skill for deepsci-mini lifecycle, manual stepping, and support-skill routing.
---

# deepsci-mini Operator Control

## Scope

Use this skill for loop-local `deepsci-mini` lifecycle semantics: status, manual stepping, pause, resume, recovery, stop intent, and explaining which maintained Houmao skill owns platform work.

## Loop Identity

- Loop slug: `deepsci-mini`.
- Loop directory: `teams/deepsci-mini`.
- Manifest path: `teams/deepsci-mini/execplan/manifest.toml`.
- Harness path: `teams/deepsci-mini/execplan/harness/bin/deepsci-mini`.
- Agent bindings path: `teams/deepsci-mini/execplan/agents/bindings.toml`.

## Maintained Houmao Routes

- Workspace planning, creation, validation, and summaries: `houmao-utils-workspace-mgr`.
- Specialist, project-profile, and pre-launch definition preparation: `houmao-agent-definition`.
- Managed-agent launch, join, relaunch, stop, and lifecycle: `houmao-agent-instance`.
- Mail status, list, read, send, reply, mark, move, and archive: `houmao-agent-email-comms`.
- Gateway lifecycle, notifier posture, reminders, and gateway posture: `houmao-agent-gateway`.
- Read-only liveness, TUI state, mailbox posture, logs, and runtime artifacts: `houmao-agent-inspect`.

## Action

1. For package-shape checks, run `teams/deepsci-mini/execplan/harness/bin/deepsci-mini validate`.
2. For role or topology lookup, query the harness instead of reading raw TOML when a command is available.
3. For manual stepping, prompt one participant for one bounded pass and stop.
4. For platform launch or messaging, route to the maintained Houmao skill that owns that surface.
5. Do not implement mailbox, gateway, managed-agent lifecycle, or workspace creation inside this generated skill.
