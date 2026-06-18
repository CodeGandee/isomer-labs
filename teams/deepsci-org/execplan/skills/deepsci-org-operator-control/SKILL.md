---
name: deepsci-org-operator-control
description: Generated operator-control skill for deepsci-org lifecycle semantics, mode switches, manual stepping, pause, resume, recovery, and stop intent.
---

# deepsci-org Operator Control

## Identity

- Loop slug: `deepsci-org`.
- Loop dir: the parent of this generated `execplan/`.
- Manifest: `../../manifest.toml`.
- Harness: `../../harness/bin/deepsci-org`.
- Agent bindings: `../../agents/bindings.toml`.

## Supported Loop-Local Operations

- Inspect generated control status.
- Explain default mode and topic-policy requirements for automatic mode.
- Record or request pause, resume, stop, recovery, redirect, manual step, and mode-switch intent.
- Route operator actions to generated harness commands and maintained Houmao platform skills.

## Boundaries

This skill does not launch agents, create workspaces, send ordinary mail, archive mail, inspect gateway state, bind mailboxes, manage memory, or stop managed agents. Use maintained Houmao skills for those platform operations.

## Action Rules

1. Read `../../manifest.toml` and `../../harness/commands.toml`.
2. Use `../../harness/bin/deepsci-org control status --run-id <run-id>` for generated read-only control context when available.
3. For platform mechanics, route to the maintained Houmao skill that owns the operation.
4. For mode switches, keep Isomer `control_mode` and generated `execution_mode` distinct: Isomer uses `manual` or `automatic`; generated runtime uses `manual` or `auto`.
5. For stop, record operator intent and clarify that stop does not mean scientific completion.
6. For recovery, identify the last stable refs, open mail, open handoff, open Gate, and missing readiness facts before prompting participants.
