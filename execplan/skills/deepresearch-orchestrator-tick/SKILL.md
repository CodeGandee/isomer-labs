---
name: deepresearch-orchestrator-tick
description: Orchestrator on-tick skill for the deepresearch loop. Invoked from a notifier/operator/self-wakeup prompt. Inspect quest+round state and perform one bounded reconciliation/dispatch/terminate pass, then arm the next durable self-wakeup.
---

# Orchestrator Tick (Orchestrator on-tick)

Invoked from a notifier/operator prompt with no new result mail, after folding a result, or as a
self-wakeup's `next_action`. Do **one** bounded pass, then stop. No sleeping/polling/in-chat waiting.

**Heartbeat-safe / idempotent:** re-read the cursor first and act only on persisted state. Deterministic
handoff ids + idempotent `record apply` mean a duplicate fire never double-dispatches or double-opens.

## Inputs

- `$HARNESS control status`, `$HARNESS state query` views (`--cursor`, `--due-handoffs`, `--fanout <round>`,
  `--convergence`, `--best-result`), `$HARNESS get-mode`.

## Procedure

1. Read posture: `$HARNESS control status` + `$HARNESS state query --cursor`. If `run_state` ∈
   {paused, stopped, completed, waiting_user}: stop. In `manual` mode, do one operator-prompted pass only.
2. **Reconcile handoffs:** `$HARNESS state query --due-handoffs`. For each overdue + unobserved handoff:
   if `attempt_count >= max_attempts` → `$HARNESS handoff advance --status failed` + `$HARNESS record apply
   --type decision.record` (route the failure); else resend (reuse `handoff_id`, `$HARNESS handoff open`
   with `bump_attempt=true`, re-render + re-deliver the task-request).
3. **Wait gate:** if `$HARNESS state query --fanout <round>` shows received < expected, stop (a result will
   wake you).
4. **Terminal checks** → finalize when any holds: `round_index >= max_rounds`; `--convergence` reports no
   new admissible finding for `convergence_patience` rounds; acceptance criteria met. **Finalize records a
   `--type finalize.record` outcome + the paired `quest.update` run_state:**
   - `complete` → `run_state completed`; `stop` → `run_state stopped` (a low-quality stop needs a
     `decision.record(requires_user_confirm=1)` then `decision.confirm` first).
   - `park` (park_and_continue_later) → `run_state parked`; `reopen_conditions` REQUIRED.
   - `publish_and_continue` (from a new incumbent) → record `published_ref` + `next_incumbent_ref`
     (a frontier incumbent / new branch); `run_state` stays `running` and the next round continues from
     that incumbent. Emit the operator completion/closure report.
5. **Else dispatch the next stage:** pick it from `--cursor` (stage_catalog ordinal, or the last
   `decision`). `decision`/`finalize`/`optimize` you do yourself (orchestrator-internal); all other
   stages dispatch to the owning role:
   - `optimize` (algorithm-first frontier mgmt): read `--frontier` + `--bo-observations`; rank candidates
     by primary `measurement`, set the `incumbent` and promote/park/fuse routes via `--type
     frontier.record` (+ `branch.record` for branch status). Then dispatch a new `experiment` for the next
     candidate (via the experiment route) or route to `decision`/`write` when the frontier plateaus.
   - For `experiment` with a defined search space, `$HARNESS bo suggest`, then record `--type idea.upsert` +
     `--type experiment.upsert` (designed) + `--type experiment_param.record`.
   - Open the round if needed (`--type round.open`); for each fan-out target (1..`fanout_default`, ≤
     `fanout_max=4` for experiment): mint a `handoff_id`, `$HARNESS handoff open` (schema_id
     `deepresearch.email.task-request`, set `receipt_due_at`/`result_due_at`), build → `$HARNESS email
     validate`/`render` → deliver the task-request to the role, `$HARNESS email apply` (out). Set
     `--type round.update --expected_handoffs <k>`.
6. **Arm continuation:** `$HARNESS wakeup arm` on lane `main` (next_stage, reason, next_action) → send the
   `deepresearch.email.self-wakeup` self-mail → `$HARNESS wakeup attach --message-ref <ref>`.
7. `$HARNESS state validate` opportunistically; on any violation, surface to the operator via
   **deepresearch-operator-control** instead of proceeding.

## Output

- One reconciliation/dispatch/terminate step recorded through the harness, plus an armed self-wakeup.

## Stop

- End the turn after one bounded pass.
