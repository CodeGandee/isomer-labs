---
name: deepresearch-operator-control
description: Use when an operator-origin or freeform control mail, or an operator-invoked lifecycle command, targets the deepresearch loop. Covers ops status, start, pause, resume, stop, recover, set-mode (execution_mode --mode auto|manual AND autonomy_mode --autonomy auto|assistant), amend-acceptance (op 4b), manual-step, confirm-gpus (gpu confirm), clarify-quest. Covers $HARNESS control/gpu/plan/record/state/handoff/wakeup usage, operator_intent_event, run_state, GPU operator-gating, ambiguity start-gate, frozen-objective/amendable-acceptance, liveness watchdog, 401-vs-403 auth recovery.
---

# Operator Control (orchestrator / operator, deepresearch loop)

## Overview

Single-turn operator-control skill for the deepresearch loop: execute one operator-requested lifecycle, mode, recovery, or setup action (status/start/pause/resume/stop/recover/set-mode/amend-acceptance/manual-step/confirm-gpus/clarify-quest), record it as an `operator_intent_event` + run-state change, and stop. Platform mechanics (notifier, prompts, mailbox) route to maintained Houmao skills rather than being reimplemented.

## When to Use

Use when, in the generated deepresearch loop, you receive:
- an **operator-origin or freeform control mail**, or
- an **operator-invoked lifecycle/setup command** (status, start, pause, resume, stop, recover, set-mode, amend-acceptance, manual-step, confirm-gpus, clarify-quest).

One bounded turn: pick the single requested op, do one bounded action, record it, stop.

**When NOT to use:**
- Not a stage-work or research skill — it drives no specialist stage and does no literature/experiment/analysis work.
- Do not use it to launch agents (start only *triggers* a turn; agent launch is a pre-loop houmao-agent-definition/houmao-agent-instance concern).
- Do not self-confirm GPUs or fabricate clarification answers to unblock stalled work — those are operator-only authority (see Common Mistakes).
- Do not edit `objective.md` (frozen) or `acceptance.md` in place — acceptance changes only via op 4b.
- Quest isolation is absolute: act on a single named `--quest-id`; never cross into another quest.

## Identity

- loop slug: `deepresearch`; loop dir: this `execplan/`'s parent.
- manifest: `execplan/manifest.toml`; harness: `$HARNESS`.
- agent bindings: `execplan/agents/bindings.toml`.
- supported ops: status, start, pause, resume, stop, recover, set-mode (execution `--mode auto|manual` AND/OR run-mode `--autonomy auto|assistant`), amend-acceptance (operator-confirmed, append-only), manual-step, confirm-gpus, clarify-quest.

## Inputs

- `$HARNESS control status` / `get-mode` / `manual-context`; the operator instruction text.
- `$HARNESS` = the absolute harness path exported on each launch profile. Invoke as `$HARNESS <group> <verb>`. `$HARNESS <group> <verb>` commands are runtime tools, not external skill files.

## Workflow

Pick the requested op and perform exactly ONE bounded action, then record + stop. Each op is concise here; gate-heavy ops point to their detail section below.

1. **status** → `$HARNESS control status` + `$HARNESS state export`; report cursor, branches, open wakeups, due handoffs, blockers, next action.
2. **start** → confirm a quest exists (`quest.create` applied) and required agents are live; then trigger the first turn (notifier/operator prompt → deepresearch-orchestrator-tick). **Do not launch agents here.**
3. **pause / resume / stop** → `$HARNESS control pause|resume|stop` (records `run_state` + `operator_intent_event`). A low-quality `stop` requires a `decision.record(requires_user_confirm=1)` then `decision.confirm` first.
4. **set-mode** → `$HARNESS control set-mode` (records `operator_intent_event(set-mode)`); TWO independent axes — see [set-mode (two axes)](#set-mode-two-axes). Supply at least one of `--mode`/`--autonomy`.
4b. **amend-acceptance** → the ONLY post-launch way to change the done-bar; objective stays frozen, acceptance is append-only and operator-confirmed — see [amend-acceptance (op 4b)](#amend-acceptance-op-4b).
5. **recover** → `$HARNESS control resume --recovering`; reconcile stalled handoffs and resume the last consistent stage — see [recover](#recover).
6. **manual-step** → `$HARNESS control manual-context`, do one bounded action, record via the harness, stop.
7. **confirm-gpus** → record the operator-approved GPU device set so GPU-using work may run; normally a PRE-LOOP setup action — see [confirm-gpus](#confirm-gpus).
8. **clarify-quest** → run/record the MANDATORY pre-launch ambiguity check across 7 dimensions; normally a PRE-LOOP setup action — see [clarify-quest](#clarify-quest).

If the task does not map cleanly to these steps, use your native planning tool to build a plan from the commands and constraints in this skill, then execute it.

## set-mode (two axes)

`$HARNESS control set-mode` records `operator_intent_event(set-mode)`. TWO independent axes:

- `--mode auto|manual` (**execution_mode**, drive cadence): `manual` suspends notifier-driven wakeups (operator prompts each bounded pass); it is NOT `paused`.
- `--autonomy auto|assistant` (**autonomy_mode**, authority/strictness): `auto` lets the loop self-dispose (completeness HARD-gates `complete` at publication rigor); `assistant` is advisory (the loop recommends, the operator disposes). Chosen pre-launch (a launch gate); change mid-loop only by operator.

Supply at least one of `--mode`/`--autonomy`.

## amend-acceptance (op 4b)

**Acceptance-only, operator-confirmed, append-only** — the ONLY post-launch way to change the done-bar. The objective is **frozen**; only `acceptance.md` may be amended, and only via:
(i) `decision.record(route='amend-acceptance', requires_user_confirm=1)` with a diff+rationale `rationale_ref`;
(ii) operator `decision.confirm`;
(iii) write a NEW `runs/<q>/objective/acceptance.md@rev-K` (never overwrite rev 1);
(iv) `quest.update acceptance_ref=...@rev-K`.

The harness `_acceptance_amend_gate` rejects any `acceptance_ref` change lacking the confirmed decision; `_objective_frozen_gate` rejects objective changes; `acceptance_amend_not_self_clearing` flags a same-round amend→complete. `$HARNESS plan diff --quest-id <q>` shows the revisions.

## recover

`$HARNESS control resume --recovering`; read `$HARNESS wakeup list` + `$HARNESS handoff query --quest-id <q> --stalled --now <ts>` (and `--due`) and resume the last consistent stage via deepresearch-orchestrator-tick (re-issue unanswered requests with the **same `handoff_id`** + `bump_attempt`; re-validate un-checked results). For a specialist that **acked but never returned a result** (turn died mid-work), the re-delivered task-request is new unread mail that re-wakes it; if it stays idle, send a direct operator prompt (`houmao-agent-messaging`) telling it to resume that `handoff_id`. Run `$HARNESS state validate`. **Auth-failure recovery (401 vs 403)** — see [Auth posture (401 vs 403)](#auth-posture-401-vs-403).

## confirm-gpus

Record the operator-approved GPU device set for the quest so GPU-using work may run. **This is normally a PRE-LOOP / setup action** (Step 3 of the runbook) — GPU confirmation is required *before* the quest can move to `running`, so the live loop does not ask again. Use this op mid-loop only as a **fallback** (to recover a legacy/misconfigured quest that somehow started unconfirmed, or to change the device set). Command:

`$HARNESS gpu confirm --quest-id <q> --devices "<list>" --by <operator> --at <ts>`

(e.g. `--devices "0"` or `"0,1"`; comma list of integer indices only — `all`/`-1`/empty are rejected). This satisfies the hard apply-time gate over **both** the `experiment` and `analysis` stages (`experiment_requires_gpu_confirmation`); the experimenter/analyst then restrict `CUDA_VISIBLE_DEVICES` to exactly this set (and `experiment run` injects it + fails closed). One confirmation covers the whole quest; re-run only to change the device set. **Only the operator may confirm GPUs** — never self-confirm to unblock stalled work. Report current state anytime with `$HARNESS gpu status --quest-id <q>`.

## clarify-quest

Run/record the MANDATORY pre-launch ambiguity check. **Normally a PRE-LOOP / setup action** (runbook Step 3a) — before a quest can move to `running` it MUST have a `kind='clarification'` artifact (hard apply-time gate in `records.py`, fail-closed).

Procedure: inspect the objective for unclear/underspecified parts across the **7 dimensions** (objective, acceptance, GPU/devices, domain, workspace/repo, budget/max_rounds, domain-specific constraints); for each unclear one, ask the operator with **multiple-choice options + a free-form "Other/custom"** choice; then either fold the resolutions into `runs/<q>/objective/objective.md` + `acceptance.md`, or attest "no blocking ambiguity". Record the outcome to `runs/<q>/objective/clarification.md` and `$HARNESS record apply` a:

```
{"record_type":"artifact.record","kind":"clarification","ref":"runs/<q>/objective/clarification.md", ...}
```

**Only the operator confirms/clarifies** — never fabricate answers to unblock launch. Use mid-loop only as a fallback (recover a legacy quest that started before the gate, or amend the brief from new operator input). **Post-launch the brief is NOT freely editable:** the objective is frozen, and acceptance edits MUST go through the operator-confirmed, append-only **amend-acceptance** path (op 4b) — never an in-place edit of `objective.md`/`acceptance.md`. Mid-loop clarify-quest may *propose* a narrowed acceptance; it lands only after `decision.confirm`.

## Auth posture (401 vs 403)

Agents use the `default` bundle's **long-lived OAuth token** (Pro/Max, `claude setup-token`) — it does **not** expire on the ~5h interactive clock, so normal recovery never needs a re-login. Distinguish failures:
- A **`401 Invalid authentication credentials`** = the token is genuinely bad/lapsed → the **operator** re-runs `claude setup-token` + `credentials claude set --name default --oauth-token …`, then **relaunch agents fresh** (a bare relaunch reuses the home-cached token).
- A **`403 … quota …`** = a *third-party proxy* (`ANTHROPIC_BASE_URL`+`AUTH_TOKEN`) is shadowing the OAuth token in the launch env — **not** a subscription problem; relaunch with those scrubbed (`unset` / `env -u …`).

Never paste a token into a prompt. See `docs/credentials.md`.

## Liveness watchdog (heartbeat + parked-agent recovery)

Keep the loop live without inbound mail via a repeating gateway heartbeat reminder on the orchestrator, and detect/dismiss Claude Code TUI interstitials that block an agent's input.

- **Heartbeat:** set a *repeating* gateway reminder on the orchestrator that prompts it to run **deepresearch-orchestrator-tick** (the tick's step 2 then reconciles stalled handoffs). Via `houmao-agent-gateway`:

  ```
  houmao-mgr agents single --agent-name orchestrator gateway reminders create --interval-seconds <N> \
  --prompt "Run deepresearch-orchestrator-tick: heartbeat reconcile (handoff query --stalled), then stop."
  ```

  Pick `N` ≥ the shortest `result_due_at` window so a dead worker turn is retried within one or two beats.
- **Claude Code interstitials:** a parked TUI prompt (e.g. *"How is Claude doing this session? 1:Bad 2:Fine 3:Good 0:Dismiss"*, trust/permission, or `/clear`-suggestion) blocks the agent's input so neither mail nor reminders advance it. Detect + safely dismiss with the operator helper `execplan/ops/loop-watchdog.sh` (read-only by default; `--apply` sends only the documented **dismiss/0** key to *known* interstitials — never a content answer). After dismissing, the agent's notifier/heartbeat resumes normally.

## Platform routing (do not reimplement)

- notifier enable/disable + reminders → `houmao-agent-gateway`.
- operator prompts to agents → `houmao-agent-messaging`.
- ordinary mailbox work → `houmao-agent-email-comms`.

## Common Mistakes

- **Launching agents under `start`.** `start` only *triggers* the first turn; it confirms a quest + live agents and prompts deepresearch-orchestrator-tick. Agent launch is a separate pre-loop concern.
- **Self-confirming GPUs to unblock work.** Only the operator confirms via `$HARNESS gpu confirm`; never self-confirm. GPU confirmation is normally pre-loop (runbook Step 3); mid-loop use is a fallback only.
- **Fabricating clarification answers.** Only the operator confirms/clarifies; never invent answers to pass the ambiguity start-gate.
- **Editing `objective.md` (frozen) or `acceptance.md` in place.** Post-launch the objective is frozen and acceptance changes only via the append-only operator-confirmed **amend-acceptance** path (op 4b); in-place edits are rejected by `_objective_frozen_gate` / `_acceptance_amend_gate`.
- **Same-round amend→complete.** `acceptance_amend_not_self_clearing` flags amending acceptance and then closing `complete` in the same round.
- **Stopping a low-quality quest without confirmation.** A low-quality `stop` requires a `decision.record(requires_user_confirm=1)` then `decision.confirm` first.
- **Confusing `manual` execution-mode with `paused`.** `--mode manual` only suspends notifier-driven wakeups (operator prompts each pass); it is NOT `paused`.
- **Recovering with a fresh `handoff_id`.** Re-issue unanswered requests with the **same `handoff_id`** + `bump_attempt`; a new id orphans the prior handoff.
- **Doing more than one bounded action per turn.** One operator op per turn, recorded as `operator_intent_event` + run-state change, then stop.
- **Reimplementing platform mechanics.** Route notifier/reminders, operator prompts, and ordinary mailbox work to the maintained Houmao skills instead.

## Rationalizations vs. reality

| Rationalization | Reality |
|---|---|
| "GPUs are obviously free — I'll just confirm them myself to unblock." | Only the operator confirms GPUs via `$HARNESS gpu confirm`. Never self-confirm; mid-loop confirm is a fallback only. |
| "The objective is slightly off — I'll just edit `objective.md`." | The objective is frozen post-launch (`_objective_frozen_gate`). It is never edited. |
| "Acceptance is a hair too strict — I'll tweak `acceptance.md` to pass." | Acceptance changes only via op 4b: operator-confirmed `decision.record`+`decision.confirm`, a new `@rev-K`, and `quest.update`. Never an in-place edit, never to self-clear `complete`. |
| "Clarification is obvious — I'll fill the answers in for the operator." | Only the operator confirms/clarifies; fabricating answers to pass the start-gate is forbidden. |
| "This quest looks stalled — I'll just stop it." | A low-quality `stop` needs `decision.record(requires_user_confirm=1)` then `decision.confirm` first. |
| "I'll re-issue the stalled request with a fresh handoff id." | Reuse the SAME `handoff_id` + `bump_attempt`; recovery re-wakes the existing handoff, it does not orphan it. |
| "I'll switch to manual mode to pause the loop." | `--mode manual` is execution cadence (notifier off), not `paused`; use `control pause` to pause. |
## Output / Stop

- **Output:** the requested lifecycle/mode/recovery effect, recorded as `operator_intent_event` + run-state change.
- **Stop:** end the turn after one operator action.
