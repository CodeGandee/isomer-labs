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
- supported ops: status, start, pause, resume, stop, recover, set-mode (auto|manual), manual-step, confirm-gpus, clarify-quest.

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
   query --quest-id <q> --stalled --now <ts>` (and `--due`) and resume the last consistent stage via
   deepresearch-orchestrator-tick (re-issue unanswered requests with the **same `handoff_id`** +
   `bump_attempt`; re-validate un-checked results). For a specialist that **acked but never returned a
   result** (turn died mid-work), the re-delivered task-request is new unread mail that re-wakes it; if it
   stays idle, send a direct operator prompt (`houmao-agent-messaging`) telling it to resume that
   `handoff_id`. Run `$HARNESS state validate`.
6. **manual-step** → `$HARNESS control manual-context`, do one bounded action, record via the harness, stop.
6b. **auth posture (credential)** → agents use the `default` bundle's **long-lived OAuth token** (Pro/Max,
   `claude setup-token`) — it does **not** expire on the ~5h interactive clock, so normal recovery never needs
   a re-login. Distinguish failures: a **`401 Invalid authentication credentials`** = the token is genuinely
   bad/lapsed → the **operator** re-runs `claude setup-token` + `credentials claude set --name default
   --oauth-token …`, then **relaunch agents fresh** (a bare relaunch reuses the home-cached token). A **`403
   … quota …`** = a *third-party proxy* (`ANTHROPIC_BASE_URL`+`AUTH_TOKEN`) is shadowing the OAuth token in
   the launch env — **not** a subscription problem; relaunch with those scrubbed (`unset` / `env -u …`). Never
   paste a token into a prompt. See `docs/credentials.md`.
7. **confirm-gpus** → record the operator-approved GPU device set for the quest so GPU-using work may run.
   **This is normally a PRE-LOOP / setup action** (Step 3 of the runbook) — GPU confirmation is required
   *before* the quest can move to `running`, so the live loop does not ask again. Use this op mid-loop only
   as a **fallback** (to recover a legacy/misconfigured quest that somehow started unconfirmed, or to change
   the device set). Command:
   `$HARNESS gpu confirm --quest-id <q> --devices "<list>" --by <operator> --at <ts>` (e.g. `--devices "0"`
   or `"0,1"`; comma list of integer indices only — `all`/`-1`/empty are rejected). This satisfies the hard
   apply-time gate over **both** the `experiment` and `analysis` stages (`experiment_requires_gpu_confirmation`);
   the Experimenter/Analyst then restrict `CUDA_VISIBLE_DEVICES` to exactly this set (and `experiment run`
   injects it + fails closed). One confirmation covers the whole quest; re-run only to change the device set.
   **Only the operator may confirm GPUs** — never self-confirm to unblock stalled work. Report current state
   anytime with `$HARNESS gpu status --quest-id <q>`.
8. **clarify-quest** → run/record the MANDATORY pre-launch ambiguity check. **Normally a PRE-LOOP / setup
   action** (runbook Step 3a) — before a quest can move to `running` it MUST have a `kind='clarification'`
   artifact (hard apply-time gate in `records.py`, fail-closed). Procedure: inspect the objective for
   unclear/underspecified parts across the **7 dimensions** (objective, acceptance, GPU/devices, domain,
   workspace/repo, budget/max_rounds, domain-specific constraints); for each unclear one, ask the operator
   with **multiple-choice options + a free-form "Other/custom"** choice; then either fold the resolutions
   into `runs/<q>/objective/objective.md` + `acceptance.md`, or attest "no blocking ambiguity". Record the
   outcome to `runs/<q>/objective/clarification.md` and `$HARNESS record apply` a
   `{"record_type":"artifact.record","kind":"clarification","ref":"runs/<q>/objective/clarification.md", ...}`.
   **Only the operator confirms/clarifies** — never fabricate answers to unblock launch. Use mid-loop only as
   a fallback (recover a legacy quest that started before the gate, or amend the brief from new operator input).

## Liveness watchdog (heartbeat + parked-agent recovery)

- **Heartbeat:** keep the loop live without inbound mail by setting a *repeating* gateway reminder on the
  Orchestrator that prompts it to run **deepresearch-orchestrator-tick** (the tick's step 2 then reconciles
  stalled handoffs). Via `houmao-agent-gateway`:
  `houmao-mgr agents single --agent-name orchestrator gateway reminders add --interval-seconds <N> \
  --prompt "Run deepresearch-orchestrator-tick: heartbeat reconcile (handoff query --stalled), then stop."`
  Pick `N` ≥ the shortest `result_due_at` window so a dead worker turn is retried within one or two beats.
- **Claude Code interstitials:** a parked TUI prompt (e.g. *"How is Claude doing this session? 1:Bad 2:Fine
  3:Good 0:Dismiss"*, trust/permission, or `/clear`-suggestion) blocks the agent's input so neither mail nor
  reminders advance it. Detect + safely dismiss with the operator helper `execplan/ops/loop-watchdog.sh`
  (read-only by default; `--apply` sends only the documented **dismiss/0** key to *known* interstitials —
  never a content answer). After dismissing, the agent's notifier/heartbeat resumes normally.

## Platform routing (do not reimplement)

- notifier enable/disable + reminders → `houmao-agent-gateway`.
- operator prompts to agents → `houmao-agent-messaging`.
- ordinary mailbox work → `houmao-agent-email-comms`.

## Output

- The requested lifecycle/mode/recovery effect, recorded as `operator_intent_event` + run-state change.

## Stop

- End the turn after one operator action.
