# Isomer Admin Houmao Interop — Explain Loop

## Overview

Houmao's agent loop is not a single `while True` inside the agent process. It is a **gateway-driven request queue** plus a **TUI-tracking lifecycle kernel** that lives next to each managed agent. The gateway serializes work, handles reminders, and reacts to mailbox traffic; the lifecycle kernel decides when the agent is ready to accept input and when a turn has truly completed.

## Core Components

| Component | File | Responsibility |
| --- | --- | --- |
| `GatewayServiceRuntime` | `src/houmao/agents/realm_controller/gateway_service.py` | The loop engine: worker loop, reminder loop, notifier loop. |
| `RuntimeSessionController` | `src/houmao/agents/realm_controller/runtime.py` | Builds and controls one managed session: backend, manifest, mailbox, memory, gateway, tmux state. |
| Reactive lifecycle kernel | `src/houmao/agents/lifecycle/rx_lifecycle_kernel.py` | Computes readiness (`ready/waiting/blocked/unknown/stalled`) and anchored completion (`waiting/in_progress/candidate_complete/completed`). |
| Gateway adapters | `src/houmao/agents/realm_controller/gateway_service.py` | Bridge the queue to local interactive, headless, or REST backends. |
| Headless backends | `src/houmao/agents/realm_controller/backends/` | `ClaudeHeadlessSession`, `CodexHeadlessSession`, `KimiHeadlessSession`, `GeminiHeadlessSession`, `CaoRestSession`, `LocalInteractiveSession`. |
| TUI tracking state | Observed under `shared_tui_tracking/` inside the agent runtime root | Feeds the lifecycle kernel with phase and stability observations. |

## The Three Daemon Loops

`GatewayServiceRuntime.start()` runs three loops:

1. **`_worker_loop`** — serially dequeues accepted requests (`submit_prompt`, `mail_notifier_prompt`, `interrupt`) and executes them through the active backend adapter.
2. **`_reminder_loop`** — schedules due reminders and dispatches them as `prompt` or `send_keys` when the gateway is idle.
3. **`_notifier_loop`** — polls the agent mailbox; when open inbox mail is found, it builds a notifier prompt and enqueues it.

## Turn Lifecycle Phases

Each prompt request flows through TUI tracking states exposed by `HoumaoTerminalStateResponse.turn.phase`:

| Phase | Meaning |
| --- | --- |
| `ready` | Gateway can accept a prompt. |
| `working` | Model is executing. |
| `candidate_complete` | Surface looks stable; waiting for stability timer. |
| `completed` | Stability timer fired; turn is done. |
| `blocked` / `awaiting_operator` / `unknown` / `stalled` | Lifecycle recovery paths triggered. |

The readiness and completion timing is computed by `rx_lifecycle_kernel.py` from observations in the agent runtime's `shared_tui_tracking/` directory.

## What This Means for Isomer Operators

- The loop is **external** to the model. Isomer customization usually does not change `gateway_service.py`; it changes what the gateway feeds into the loop (presets, skills, prompts, mailbox, reminders).
- A "team" in Isomer terms usually becomes a set of Houmao-managed agents, each with its own gateway/runtime session, rather than one shared loop.
- Stage handoffs from a Domain Agent Team Template are normally implemented by updating durable state (quest state, plan, active anchor) and submitting the next prompt, not by reconfiguring the gateway.
