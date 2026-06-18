---
name: deepresearch-operator-control
description: Operator control skill for the deepresearch loop. Handle status, start, pause, resume, stop, recover, mode switching, and manual steps; route platform mechanics to maintained Houmao skills.
---

# Operator Control (orchestrator / operator)

**Trigger:** operator-origin / freeform control mail, or an operator-invoked lifecycle command. One
bounded turn. See `deepresearch-shared-guide`.

## Identity

- loop slug: `deepresearch`; loop dir: this `execplan/`'s parent.
- manifest: `execplan/manifest.toml`; harness: `$HARNESS`.
- agent bindings: `execplan/agents/bindings.toml`.
- supported ops: status, start, pause, resume, stop, recover, set-mode (execution --mode auto|manual AND/OR run-mode --autonomy auto|assistant), amend-acceptance (operator-confirmed, append-only), manual-step, confirm-gpus, clarify-quest.

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
4. **set-mode** → `$HARNESS control set-mode` (records `operator_intent_event(set-mode)`). TWO independent axes:
   - `--mode auto|manual` (**execution_mode**, drive cadence): `manual` suspends notifier-driven wakeups
     (operator prompts each bounded pass); it is NOT `paused`.
   - `--autonomy auto|assistant` (**autonomy_mode**, authority/strictness): `auto` lets the loop
     self-dispose (completeness HARD-gates `complete` at publication rigor); `assistant` is advisory (the loop
     recommends, the operator disposes). Chosen pre-launch (a launch gate); change mid-loop only by operator.
   Supply at least one of `--mode`/`--autonomy`.
4b. **amend-acceptance (acceptance-only, operator-confirmed, append-only)** → the ONLY post-launch
   way to change the done-bar. The objective is **frozen**; only `acceptance.md` may be amended, and only via:
   (i) `decision.record(route='amend-acceptance', requires_user_confirm=1)` with a diff+rationale
   `rationale_ref`; (ii) operator `decision.confirm`; (iii) write a NEW `runs/<q>/objective/acceptance.md@rev-K`
   (never overwrite rev 1); (iv) `quest.update acceptance_ref=...@rev-K`. The harness `_acceptance_amend_gate`
   rejects any acceptance_ref change lacking the confirmed decision; `_objective_frozen_gate` rejects objective
   changes; `acceptance_amend_not_self_clearing` flags a same-round amend→complete. `$HARNESS plan diff
   --quest-id <q>` shows the revisions.
5. **recover** → `$HARNESS control resume --recovering`; read `$HARNESS wakeup list` + `$HARNESS handoff
   query --quest-id <q> --stalled --now <ts>` (and `--due`) and resume the last consistent stage via
   deepresearch-orchestrator-tick (re-issue unanswered requests with the **same `handoff_id`** +
   `bump_attempt`; re-validate un-checked results). For a specialist that **acked but never returned a
   result** (turn died mid-work), the re-delivered task-request is new unread mail that re-wakes it; if it
   stays idle, send a direct operator prompt (`houmao-agent-messaging`) telling it to resume that
   `handoff_id`. Run `$HARNESS state validate`. **Auth-failure recovery (401 vs 403)** is in
   `reference/recovery-and-liveness.md`.
6. **manual-step** → `$HARNESS control manual-context`, do one bounded action, record via the harness, stop.
7. **confirm-gpus** → record the operator-approved GPU device set for the quest so GPU-using work may run.
   **This is normally a PRE-LOOP / setup action** (Step 3 of the runbook) — GPU confirmation is required
   *before* the quest can move to `running`, so the live loop does not ask again. Use this op mid-loop only
   as a **fallback** (to recover a legacy/misconfigured quest that somehow started unconfirmed, or to change
   the device set). Command:
   `$HARNESS gpu confirm --quest-id <q> --devices "<list>" --by <operator> --at <ts>` (e.g. `--devices "0"`
   or `"0,1"`; comma list of integer indices only — `all`/`-1`/empty are rejected). This satisfies the hard
   apply-time gate over **both** the `experiment` and `analysis` stages (`experiment_requires_gpu_confirmation`);
   the experimenter/analyst then restrict `CUDA_VISIBLE_DEVICES` to exactly this set (and `experiment run`
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
   **Post-launch the brief is NOT freely editable:** the objective is frozen, and acceptance edits
   MUST go through the operator-confirmed, append-only **amend-acceptance** path (op 4b) — never an in-place
   edit of `objective.md`/`acceptance.md`. Mid-loop clarify-quest may *propose* a narrowed acceptance; it
   lands only after `decision.confirm`.

## Liveness watchdog (heartbeat + parked-agent recovery)

Keep the loop live without inbound mail via a repeating gateway heartbeat reminder on the orchestrator, and
detect/dismiss Claude Code TUI interstitials that block an agent's input. The heartbeat-reminder command, the
`N`-interval rule, and the `execplan/ops/loop-watchdog.sh` dismiss procedure are in
**`reference/recovery-and-liveness.md`**.

## Platform routing (do not reimplement)

- notifier enable/disable + reminders → `houmao-agent-gateway`.
- operator prompts to agents → `houmao-agent-messaging`.
- ordinary mailbox work → `houmao-agent-email-comms`.

## Output

- The requested lifecycle/mode/recovery effect, recorded as `operator_intent_event` + run-state change.

## Stop

- End the turn after one operator action.
