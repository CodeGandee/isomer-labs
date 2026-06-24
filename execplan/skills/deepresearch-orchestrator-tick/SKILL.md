---
name: deepresearch-orchestrator-tick
description: Orchestrator on-tick skill for the deepresearch loop. Invoked from a notifier/operator/self-wakeup prompt. Inspect quest+round state and perform one bounded reconciliation/dispatch/terminate pass, then arm the next durable self-wakeup.
---

# Orchestrator Tick (orchestrator on-tick)

Invoked from a notifier/operator prompt with no new result mail, after folding a result, or as a
self-wakeup's `next_action`. Do **one** bounded pass, then stop. No sleeping/polling/in-chat waiting. See
`deepresearch-shared-guide`.

**Heartbeat-safe / idempotent:** re-read the cursor first and act only on persisted state. Deterministic
handoff ids + idempotent `record apply` mean a duplicate fire never double-dispatches or double-opens.

## Inputs

- `$HARNESS control status`, `$HARNESS state query <view>` (VIEW is **positional**, not a flag; available:
  `cursor`, `due-handoffs`, `best-result`, `frontier`, `bo-observations`, `open-claims`, `open-wakeups`,
  `branches`, `intake`), `$HARNESS control get-mode`. There is **no** `state query` fanout/convergence view:
  read fan-out completeness from the round (`received_handoffs` vs expected) / `$HARNESS handoff query`, and
  convergence posture from `$HARNESS bo status` (no-improvement streak) + `$HARNESS findings query`.

## Procedure

1. **Read posture:** `$HARNESS control status` + `$HARNESS state query cursor`. If `run_state` ∈
   {paused, stopped, completed, waiting_user}: stop. In `manual` mode, do one operator-prompted pass only.
2. **Reconcile handoffs (heartbeat-driven liveness):** this tick also fires on a periodic **heartbeat**
   (a repeating gateway reminder on the orchestrator — see `deepresearch-operator-control`), so a stalled
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
   The `$HARNESS state query due-handoffs` view is handled identically for anything not surfaced by
   `--stalled`. **Never** re-dispatch a `processed`/`failed` handoff (the `handoff` transition guard rejects it).
3. **Wait gate:** if the round's fan-out is incomplete (the round's `received_handoffs` < expected,
   cross-checked via `$HARNESS handoff query --quest-id <q>`), stop (a result will wake you).
4. **Terminal checks → finalize when any holds** (`round_index >= max_rounds`, convergence, acceptance met):
   run `$HARNESS completeness audit --quest-id <q>` and branch on `autonomy_mode` × `rigor_level`, enforce the
   publication-quality + scholarship gates before `complete`, then record a `--type finalize.record` outcome
   (`complete`/`stop`/`park`/`publish_and_continue`) + the paired `quest.update` run_state, with an honest
   closure report. **Waivers are auditable exceptions, not silent bypasses:** if any finalize-sensitive gate is
   env-waived (`gate status` → `active_waivers` / `finalize_ack_missing`), a bound `complete` is BLOCKED until a
   durable acknowledgement exists — have the operator record `--type quality_gate.waiver` (gate, `source=env`,
   `reason`, `finalize_ack=true`) per gate (`gate waiver list` is the audit view). Full gate branches, the
   publication-bundle checklist, and finalize-honesty rules are in **`reference/finalize-and-dispatch.md`**.
5. **Else dispatch the next stage — driven by `$HARNESS gate status --quest-id <q>`:** read `data.gates`
   and, when any gate is `blocking`, dispatch to the **first blocking gate's `route_target`** (idea_gate→idea,
   baseline_contract→baseline, campaign_coverage→experiment|analysis, analysis_bridge→analysis,
   paper_spine/outline_valid→outline, manuscript_coverage→write, review_verdict→its route_target). Do NOT route
   on LLM discretion when a hard gate says fail; the same hard guards block the write/finalize/handoff anyway
   (gate status only makes routing deterministic, it does not replace them). **Re-validate after changes:** a
   gate may report `status=fail` with a *stale* reason (or appear in `data.stale_gates`) when evidence/results/
   claims/spine/review target changed after the validator last ran — route back to re-run the relevant
   validator (`result`/`baseline`/`campaign`/`manuscript coverage`/`review` validate) before proceeding. When
   no gate blocks (`finalize_readiness=pass`), proceed to the cursor's next stage. **Quest-local discovery
   (advisory):** when choosing among ablation / robustness / boundary / baseline-repair / new-idea / write,
   consult `gate status` `data.discovery` (open opportunities + recommended_next_actions, unsupported/refuted
   claims, parked routes, negative-findings count) and `$HARNESS opportunity list`; record the next direction
   (and why, citing this quest's finding/result/claim ids) via `record apply --type opportunity.record`. This
   layer is ADVISORY — it never blocks — and is strictly quest-local (no cross-quest memory). `decision`/
   `finalize`/`optimize` you do yourself (orchestrator-internal); all other stages dispatch to the owning role. The decision discipline (name ≥2 candidates + mark losers + bottleneck
   classification + exploration-depth gate), the `optimize` frontier/search discipline, the `experiment` BO
   path, the **GPU gate** (normally already confirmed; route to operator-control only as a safety fallback),
   and the round-open + fan-out + dispatch mechanics are in **`reference/finalize-and-dispatch.md`**.
5b. **Methodology self-audit for the orchestrator-internal stages you perform (`decision`/`optimize`/
   `finalize`).** Workers self-report `methodology_used` for their stages; YOU are the worker for these three,
   so when you close a `decision`/`optimize`/`finalize` round you MUST record the audit artifact yourself:
   `$HARNESS record apply --type artifact.record` with `kind='methodology-usage'`, `round_index=<r>`, and
   `ref=runs/<q>/methodology/r<r>-<stage>.md` citing **`research-method`** (the decision-route-criteria /
   optimize search / finalization-checklist cards you applied) + the bound output (the `decision`/`frontier`/
   `finalize_outcome` row). `finalize` additionally consults `paper-craft`/`review-craft` for the closure
   report. This is an audit overlay only — NOT authoritative over the DB rows. `$HARNESS plan validate` warns
   when a closed internal-stage round lacks this artifact.
6. **Arm continuation:** `$HARNESS wakeup arm` on lane `main` (next_stage, reason, next_action) → send the
   `deepresearch.email.self-wakeup` self-mail → `$HARNESS wakeup attach --message-ref <ref>`.
   **Re-render the plan map:** after closing a round (`round.close`), run `$HARNESS plan render
   --quest-id <q> --at <ts>` so `runs/<q>/plan.md` (a pure DB projection; never read back as truth) reflects
   the new node/route/revision state. The `plan_map_fresh` invariant flags a stale map if this is skipped.
   Record the internal-stage methodology-usage artifact (5b) BEFORE re-rendering so the plan map reflects it.
7. `$HARNESS state validate` opportunistically; on any violation, surface to the operator via
   **deepresearch-operator-control** instead of proceeding.

## Output

- One reconciliation/dispatch/terminate step recorded through the harness, plus an armed self-wakeup.

## Stop

- End the turn after one bounded pass.
