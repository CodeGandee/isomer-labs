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
2. **Reconcile handoffs (heartbeat-driven liveness):** this tick also fires on a periodic **heartbeat**
   (a repeating gateway reminder on the Orchestrator — see `deepresearch-operator-control`), so a stalled
   round is caught even when no result mail ever arrives. Run
   `$HARNESS handoff query --quest-id <q> --stalled --now <ts>` — it returns in-flight (`sent`/`acked`)
   handoffs past their `receipt_due_at`/`result_due_at` with an `action` per row:
   - `action="resend (reuse handoff_id, bump_attempt)"` (attempts remain) → `$HARNESS handoff open` with the
     **same `handoff_id`** + `bump_attempt=true`, then re-render + **re-deliver** the task-request mail. The
     re-delivery is new *unread* mail, which re-wakes an idle specialist whose `unread_only` notifier would
     otherwise never re-fire. Idempotent: the same `handoff_id` never double-opens and the worker dedups via
     `handoff query --seen`.
   - `action="fail+decision"` (`attempt_count >= max_attempts`) → `$HARNESS handoff advance --status failed`
     + `$HARNESS record apply --type decision.record` (route the failure: reassign / branch / stop).
   The legacy `$HARNESS state query --due-handoffs` view is handled identically for anything not surfaced by
   `--stalled`. **Never** re-dispatch a `processed`/`failed` handoff (the `handoff` transition guard rejects it).
3. **Wait gate:** if `$HARNESS state query --fanout <round>` shows received < expected, stop (a result will
   wake you).
4. **Terminal checks** → finalize when any holds: `round_index >= max_rounds`; `--convergence` reports no
   new admissible finding for `convergence_patience` rounds; acceptance criteria met. **Publication-quality
   gate (before `complete`):** a `complete` finalize REQUIRES the publication bundle to exist — verify via
   `$HARNESS state query` / the artifact rows + `runs/<q>/report/submission_checklist.md`: (i) a **compiled
   PDF** report artifact (`runs/<q>/report/paper.pdf`, not just Markdown); (ii) ≥1 **figure** artifact;
   (iii) a **bibliography** (`runs/<q>/refs/references.bib`); (iv) a clean **submission bundle** (evidence_ledger +
   claim_evidence_map + checklist) with **no orphan supported claims** and `evidence validate` clean; and
   (v) the **Chinese edition** `runs/<q>/report/paper-zh.pdf` (bilingual output is expected). If any
   are missing, do **not** complete — record a `decision.record` routing back to `write` (or `outline`) and
   dispatch it. Only when the gate passes record the outcome. **Finalize records a `--type finalize.record`
   outcome + the paired `quest.update` run_state:**
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
   - **GPU gate (GPU-using stages — `experiment` AND `analysis`):** GPU use is confirmed **before the loop
     starts** (operator runs `gpu confirm` during quest setup; the quest cannot reach `run_state=running`
     without it — pre-loop start-gate). So in normal operation `$HARNESS gpu status --quest-id <q>` is
     **always** `confirmed=true` here, and you dispatch experiment/analysis handoffs directly. **Do NOT
     routinely route to operator-control for GPU confirmation** — that is reserved as a *safety fallback*
     only: if `gpu status` ever reports `confirmed=false` (a legacy or misconfigured quest that started
     before the gate), do not open the handoff (the harness blocks it apply-time anyway via `_gpu_gate`),
     record a `--type decision.record` (route to the blocked stage, `requires_user_confirm`), hand off to
     **deepresearch-operator-control**, arm the continuation, and stop. A single per-quest confirmation
     covers both stages. The Experimenter/Analyst restrict to the confirmed `devices` (and `experiment run`
     injects `CUDA_VISIBLE_DEVICES` + fails closed).
   - Open the round if needed (`--type round.open`); for each fan-out target (1..`fanout_default`, ≤
     `fanout_max=8` for experiment): mint a `handoff_id`, `$HARNESS handoff open` (schema_id
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
