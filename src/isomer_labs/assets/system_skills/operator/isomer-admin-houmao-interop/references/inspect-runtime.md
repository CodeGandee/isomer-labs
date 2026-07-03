# Isomer Admin Houmao Interop — Inspect Runtime

## Overview

Inspect a live Houmao-managed agent through the operator CLI, the passive API server, or the runtime filesystem. Read-only inspection is preferred; use prompt/interrupt/stop commands only when the user explicitly asks for control actions.

## CLI Inspection

### List agents

```bash
houmao-mgr agents global list
```

### Inspect a single agent

```bash
houmao-mgr agents single --agent-id <id> state
houmao-mgr agents single --agent-id <id> gateway status
houmao-mgr agents single --agent-id <id> mailbox list
houmao-mgr agents single --agent-id <id> memory show
```

### Inspect gateway queue and status

```bash
houmao-mgr agents single --agent-id <id> gateway status
```

This reports gateway state, pending requests, active turn phase, and notifier/reminder status.

### Inspect tmux session

If the agent runs under tmux, attach or list the session:

```bash
tmux ls
# or
tmux attach -t <session-name>
```

Session names are recorded in the runtime state under the agent runtime root.

## Filesystem Inspection

| Location | Content |
| --- | --- |
| `.houmao/runtime/` | Gateway config, queue, status, tmux state. |
| `.houmao/runtime/<agent-id>/gateway_storage/` | Gateway storage files. |
| `.houmao/runtime/<agent-id>/shared_tui_tracking/` | TUI tracking observations used by the lifecycle kernel. |
| `.houmao/mailbox/` | Filesystem mailbox store. |
| `.houmao/memory/` | `houmao-memo.md` and memory pages. |

## Passive API Server

Start the server:

```bash
houmao-passive-server serve --host 127.0.0.1 --port 8000
```

Useful endpoints:

| Endpoint | Purpose |
| --- | --- |
| `GET /health` | Server health. |
| `GET /houmao/agents` | List managed agents. |
| `GET /houmao/agents/{agent_ref}/requests` | Pending requests. |
| `GET /houmao/agents/{agent_ref}/turns/...` | Turn history. |
| Gateway routes | Gateway status and control. |
| Mailbox routes | Mailbox status and mail. |
| Memory routes | Memory pages. |

Implementation: `src/houmao/passive_server/app.py`.

## Python APIs

| API | Use |
| --- | --- |
| `houmao.agents.realm_controller.runtime.RuntimeSessionController` | Runtime control surface. |
| `houmao.agents.realm_controller.gateway_service.GatewayServiceRuntime` | Live gateway/queue/notifier/reminder loop. |
| `houmao.agents.realm_controller.gateway_client.GatewayClient` | HTTP client to a live gateway. |
| `houmao.project.overlay.discover_project_overlay(start_directory)` | Find the `.houmao/` overlay from a path. |

## Common Mistakes

- Killing tmux sessions directly instead of using `houmao-mgr agents single --agent-id <id> stop`. Direct tmux kills can leave gateway state inconsistent.
- Reading runtime files while a turn is active; the files may be partially written.
- Confusing gateway status with model status. `blocked` or `stalled` often means a lifecycle recovery action is needed, not that the model is broken.
