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
   bo_idea_decision→bo-review, baseline_contract→baseline, campaign_coverage→experiment|analysis,
   analysis_bridge→analysis, paper_spine/outline_valid→outline, manuscript_coverage→write,
   review_verdict→its route_target, bo_next_move→bo-review). Do NOT route
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
   layer is ADVISORY — it never blocks — and is strictly quest-local (no cross-quest memory).
   **Idea-level BO is DECISIVE (the `bo_idea_decision` gate).** After `idea validate` materializes the slate as
   enumerable, gate-eligibility-tagged `idea` rows, a multi-candidate selection is chosen by BO, not by the
   scout's prose: when `bo_idea_decision` is `blocking` (≥2 gate-eligible idea rows, no idea-selection
   `bo_decision`), dispatch the **BO-reviewer** for `bo-review` (task: value each viable candidate against the
   quest-local Findings-Memory digest — pass `$HARNESS findings summarize` + the candidate slate from
   `$HARNESS bo candidates`). Ingest its valuations with `$HARNESS bo review --from-json`, then
   `$HARNESS bo select --decision-kind idea-selection --bind --at <ts>` — this records the `bo_decision` and
   BINDS `idea_select.retained_candidate` to the winner. If exactly one candidate is gate-eligible, BO may be
   skipped but record it explicitly: `$HARNESS bo select --skip-reason "<why>" --at <ts>`. Only then does
   idea→baseline unblock. BO chooses ONLY among candidates the hard idea gate already deemed eligible — it never
   overrides scope/novelty/feasibility/validity floors. **Next-move BO is DECISIVE for the LATER route too (the
   `bo_next_move` gate).** Post-experiment/analysis, after you update quest-local Findings Memory
   (`findings update`), the next move is BO-chosen when NO hard gate forces it and ≥2 hard-gate-ELIGIBLE moves
   exist: when `bo_next_move` is `blocking`, dispatch the **BO-reviewer** for `bo-review` — pass the
   `findings summarize` digest + the eligible slate from `$HARNESS bo next-moves` (open opportunities + the
   synthetic write/finalize/stop moves, each tagged with hard-gate eligibility + a route_target). Ingest with
   `$HARNESS bo review --next-move --from-json`, then `$HARNESS bo select --next-move --at <ts>` — this records
   a `bo_decision` (decision_kind auto-derived: experiment-/opportunity-/stop-write-finalize-selection) and the
   winner's `selected_route` is the BOUND next stage you dispatch (open opportunity → experiment/analysis, write
   → outline/write, finalize → finalize, stop → decision). Create the handoff for that stage. If exactly one
   move is eligible, record an explicit skip (`bo select --next-move --skip-reason "<why>"`). BO ranks ONLY
   moves the hard gates already permit (`bo next-moves` excludes ineligible write/finalize/experiment moves), so
   it never bypasses the campaign/bridge/claim-evidence/review/finalize gates; a fresh decision is required after
   each new result/analysis. `decision`/
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
