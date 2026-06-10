---
name: deepresearch-operator-control
description: Operator control skill for the deepresearch loop. Handle status, start, pause, resume, stop, recover, mode switching, and manual steps; route platform mechanics to maintained Houmao skills.
---

# Operator Control (Orchestrator / operator)

**Trigger:** operator-origin / freeform control mail, or an operator-invoked lifecycle command. One
bounded turn.

## Identity

- loop slug: `deepresearch`; loop dir: this `execplan/`'s parent.
- manifest: `execplan/manifest.toml`; harness: `$HARNESS`.
- agent bindings: `execplan/agents/bindings.toml`.
- supported ops: status, start, pause, resume, stop, recover, set-mode (auto|manual), manual-step.

## Inputs

- `$HARNESS control status` / `get-mode` / `manual-context`; operator instruction text.

## Procedure (pick the requested op; one bounded action)

1. **status** → `$HARNESS control status` + `$HARNESS state export`; report cursor, branches, open wakeups,
   due handoffs, blockers, next action.
2. **start** → confirm a quest exists (`quest.create` applied) and required agents are live; then trigger
   the first turn (notifier/operator prompt → deepresearch-orchestrator-tick). Do not launch agents here.
3. **pause / resume / stop** → `$HARNESS control pause|resume|stop` (records `run_state` +
   `operator_intent_event`). A low-quality `stop` requires a `decision.record(requires_user_confirm=1)`
   then `decision.confirm` first.
4. **set-mode auto|manual** → `$HARNESS control set-mode` (records `operator_intent_event(set-mode)`).
   `manual` suspends notifier-driven wakeups (operator prompts each bounded pass); it is NOT `paused`.
5. **recover** → `$HARNESS control resume --recovering`; read `$HARNESS wakeup list` + `$HARNESS handoff
   query --due` and resume the last consistent stage via deepresearch-orchestrator-tick (re-issue
   unanswered requests with the same `handoff_id`; re-validate un-checked results). Run `$HARNESS state
   validate`.
6. **manual-step** → `$HARNESS control manual-context`, do one bounded action, record via the harness, stop.

## Platform routing (do not reimplement)

- notifier enable/disable + reminders → `houmao-agent-gateway`.
- operator prompts to agents → `houmao-agent-messaging`.
- ordinary mailbox work → `houmao-agent-email-comms`.

## Output

- The requested lifecycle/mode/recovery effect, recorded as `operator_intent_event` + run-state change.

## Stop

- End the turn after one operator action.
