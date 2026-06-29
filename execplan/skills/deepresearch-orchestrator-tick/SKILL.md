---
name: deepresearch-orchestrator-tick
description: "Use when the deepresearch orchestrator is invoked from a notifier/operator prompt with no new result mail, after folding a result, on a periodic heartbeat reminder, or as a self-wakeup next_action — to run one bounded reconciliation/dispatch/terminate pass and re-arm the next durable self-wakeup. Keywords: orchestrator tick, on-tick, heartbeat, self-wakeup next_action, reconcile handoffs, stalled handoff, wait gate, terminal checks, finalize, dispatch next stage, gate status route_target, bo_idea_decision, bo_next_move, wakeup arm, plan render."
---

# deepresearch-orchestrator-tick

## Overview
The orchestrator on-tick pass: re-read persisted quest+round state and perform exactly ONE bounded reconciliation/dispatch/terminate step through the harness, then arm the next durable self-wakeup and stop. It is heartbeat-safe and idempotent — it never sleeps, polls, or waits in chat.

## When to Use
Trigger this skill when the orchestrator is woken to advance the deepresearch stage machine, specifically:
- A notifier/operator prompt fires with NO new result mail.
- Immediately after folding a `task-result` (continuation tick).
- A periodic **heartbeat** (a repeating gateway reminder on the orchestrator) fires — so a stalled round is caught even when no result mail ever arrives.
- A `deepresearch.email.self-wakeup`'s `next_action` resolves to a tick.

When NOT to use:
- Not for handling inbound event mail itself — a received `task-result` routes to **deepresearch-on-task-result**, a `receipt` to **deepresearch-on-receipt**, a `self-wakeup` envelope resolves via **deepresearch-on-self-wakeup** (which then runs this tick). Only the tick *body* lives here.
- Not for operator lifecycle control (status/start/pause/resume/stop/recover, mode switch, GPU confirm, amend-acceptance) — that is **deepresearch-operator-control**.
- Do nothing if `run_state` ∈ {paused, stopped, completed, waiting_user}. In `manual` mode, do one operator-prompted pass only.
- Strictly quest-local: never reuse, refer to, or inspect another quest's artifacts/findings/refs. Operate only on the quest `<q>` you were given.

## Workflow
Do **one** bounded pass, then stop. No sleeping/polling/in-chat waiting. Consult **deepresearch-shared-guide** for harness/comms conventions before any state read/write.

**Heartbeat-safe / idempotent:** re-read the cursor first and act only on persisted state. Deterministic handoff ids + idempotent `record apply` mean a duplicate fire never double-dispatches or double-opens.

1. **Read posture:** run `$HARNESS control status` + `$HARNESS state query cursor`. If `run_state` ∈ {paused, stopped, completed, waiting_user}: stop. In `manual` mode (`$HARNESS control get-mode`), do one operator-prompted pass only.
2. **Reconcile handoffs (heartbeat-driven liveness):** run `$HARNESS handoff query --quest-id <q> --stalled --now <ts>` and act on the per-row `action` — `resend` (reuse same `handoff_id` + `bump_attempt`, re-deliver task-request) or `fail+decision`. See **Handoff reconciliation** below for the exact verbs and guards.
3. **Wait gate:** if the round's fan-out is incomplete (`received_handoffs` < expected, cross-checked via `$HARNESS handoff query --quest-id <q>`), **stop** — a result will wake you.
4. **Terminal checks → finalize when any holds** (`round_index >= max_rounds`, convergence, acceptance met): run `$HARNESS completeness audit --quest-id <q>`, branch on `autonomy_mode` × `rigor_level`, enforce the publication-quality + scholarship gates before `complete`, then record a `--type finalize.record` outcome (`complete`/`stop`/`park`/`publish_and_continue`) + the paired `quest.update` run_state, with an honest closure report. Waivers are auditable, not silent — see **Finalize gate & waivers** below and full branches in **`references/finalize-and-dispatch.md`**.
5. **Else dispatch the next stage — driven by `$HARNESS gate status --quest-id <q>`:** route to the first blocking gate's `route_target`; re-validate stale gates first; honor the DECISIVE idea-level and next-move BO gates (`bo_idea_decision`, `bo_next_move`); consult advisory quest-local discovery. `decision`/`finalize`/`optimize` you do yourself; all other stages dispatch to the owning role. See **Dispatch routing** and **BO decision gates** below; the decision/optimize/experiment/GPU/round-open mechanics are in **`references/finalize-and-dispatch.md`**.
6. **Methodology self-audit for the orchestrator-internal stages you perform (`decision`/`optimize`/`finalize`):** record the `artifact.record` audit overlay yourself — see **Internal-stage methodology self-audit** below.
7. **Arm continuation:** `$HARNESS wakeup arm` on lane `main` → send the `deepresearch.email.self-wakeup` self-mail → `$HARNESS wakeup attach --message-ref <ref>`. After closing a round (`round.close`), **re-render the plan map** with `$HARNESS plan render --quest-id <q> --at <ts>` (record the 5b/step-6 methodology artifact BEFORE re-rendering). See **Continuation & plan render** below.
8. **Validate opportunistically:** run `$HARNESS state validate`; on any violation, surface to the operator via **deepresearch-operator-control** instead of proceeding.
9. End the turn after one bounded pass.

If the task does not map cleanly to these steps, use your native planning tool to build a plan from the commands/constraints in this skill, then execute it.

## Inputs
- `$HARNESS control status`, `$HARNESS control get-mode`.
- `$HARNESS state query <view>` — VIEW is **positional**, not a flag. Available: `cursor`, `due-handoffs`, `best-result`, `frontier`, `bo-observations`, `open-claims`, `open-wakeups`, `branches`, `intake`.
- There is **no** `state query` fanout/convergence view: read fan-out completeness from the round (`received_handoffs` vs expected) / `$HARNESS handoff query`, and convergence posture from `$HARNESS bo status` (no-improvement streak) + `$HARNESS findings query`.

## Handoff reconciliation (step 2)
This tick also fires on a periodic **heartbeat** (a repeating gateway reminder on the orchestrator — see **deepresearch-operator-control**), so a stalled round is caught even when no result mail ever arrives. `$HARNESS handoff query --quest-id <q> --stalled --now <ts>` returns in-flight (`sent`/`acked`) handoffs past their `receipt_due_at`/`result_due_at`, each with an `action`:
- `action="resend (reuse handoff_id, bump_attempt)"` (attempts remain) → `$HARNESS handoff open` with the **same `handoff_id`** + `bump_attempt=true`, then re-render + **re-deliver** the task-request mail. The re-delivery is new *unread* mail, which re-wakes an idle specialist whose `unread_only` notifier would otherwise never re-fire. Idempotent: the same `handoff_id` never double-opens and the worker dedups via `handoff query --seen`.
- `action="fail+decision"` (`attempt_count >= max_attempts`) → `$HARNESS handoff advance --status failed` + `$HARNESS record apply --type decision.record` (route the failure: reassign / branch / stop).

The `$HARNESS state query due-handoffs` view is handled identically for anything not surfaced by `--stalled`. **Never** re-dispatch a `processed`/`failed` handoff (the `handoff` transition guard rejects it).

## Finalize gate & waivers (step 4)
Finalize when any holds: `round_index >= max_rounds`, convergence, or acceptance met. Run `$HARNESS completeness audit --quest-id <q>` and branch on `autonomy_mode` × `rigor_level`, enforce the publication-quality + scholarship gates before `complete`, then record a `--type finalize.record` outcome (`complete`/`stop`/`park`/`publish_and_continue`) + the paired `quest.update` run_state, with an honest closure report.

**Waivers are auditable exceptions, not silent bypasses:** if any finalize-sensitive gate is env-waived (`gate status` → `active_waivers` / `finalize_ack_missing`), a bound `complete` is BLOCKED until a durable acknowledgement exists — have the operator record `--type quality_gate.waiver` (gate, `source=env`, `reason`, `finalize_ack=true`) per gate (`gate waiver list` is the audit view).

Full gate branches (`auto`+`publication` HARD gate vs `assistant`/lower-rigor ADVISORY), the publication-bundle checklist (compiled PDF, ≥1 figure, bibliography, clean submission bundle, Chinese edition, `lit audit` scholarship bar), and finalize-honesty rules (classify every outcome, preserve belief-change history, keep Limitations) are in **`references/finalize-and-dispatch.md`**.

## Dispatch routing (step 5)
Read `$HARNESS gate status --quest-id <q>` → `data.gates`; when any gate is `blocking`, dispatch to the **first blocking gate's `route_target`**:

| Blocking gate | route_target |
| --- | --- |
| idea_gate | idea |
| bo_idea_decision | bo-review |
| baseline_contract | baseline |
| campaign_coverage | experiment / analysis |
| analysis_bridge | analysis |
| paper_spine / outline_valid | outline |
| manuscript_coverage | write |
| review_verdict | its route_target |
| bo_next_move | bo-review |

Do NOT route on LLM discretion when a hard gate says fail; the same hard guards block the write/finalize/handoff anyway (gate status only makes routing deterministic, it does not replace them). **Re-validate after changes:** a gate may report `status=fail` with a *stale* reason (or appear in `data.stale_gates`) when evidence/results/claims/spine/review target changed after the validator last ran — route back to re-run the relevant validator (`result`/`baseline`/`campaign`/`manuscript coverage`/`review` validate) before proceeding. When no gate blocks (`finalize_readiness=pass`), proceed to the cursor's next stage.

**Quest-local discovery (advisory):** when choosing among ablation / robustness / boundary / baseline-repair / new-idea / write, consult `gate status` `data.discovery` (open opportunities + recommended_next_actions, unsupported/refuted claims, parked routes, negative-findings count) and `$HARNESS opportunity list`; record the next direction (and why, citing this quest's finding/result/claim ids) via `record apply --type opportunity.record`. This layer is ADVISORY — it never blocks — and is strictly quest-local (no cross-quest memory).

`decision`/`finalize`/`optimize` you do yourself (orchestrator-internal); all other stages dispatch to the owning role. The decision discipline (name ≥2 candidates + mark losers + bottleneck classification + exploration-depth gate), the `optimize` frontier/search discipline, the `experiment` BO path, the **GPU gate** (normally already confirmed; route to operator-control only as a safety fallback), and the round-open + fan-out + dispatch mechanics are in **`references/finalize-and-dispatch.md`**.

## BO decision gates (step 5, DECISIVE)
**Idea-level BO is DECISIVE (the `bo_idea_decision` gate).** After `idea validate` materializes the slate as enumerable, gate-eligibility-tagged `idea` rows, a multi-candidate selection is chosen by BO, not by the scout's prose: when `bo_idea_decision` is `blocking` (≥2 gate-eligible idea rows, no idea-selection `bo_decision`), dispatch the **BO-reviewer** for `bo-review` (task: value each viable candidate against the quest-local Findings-Memory digest — pass `$HARNESS findings summarize` + the candidate slate from `$HARNESS bo candidates`). Ingest its valuations with `$HARNESS bo review --from-json`, then `$HARNESS bo select --decision-kind idea-selection --bind --at <ts>` — this records the `bo_decision` and BINDS `idea_select.retained_candidate` to the winner. If exactly one candidate is gate-eligible, BO may be skipped but record it explicitly: `$HARNESS bo select --skip-reason "<why>" --at <ts>`. Only then does idea→baseline unblock. BO chooses ONLY among candidates the hard idea gate already deemed eligible — it never overrides scope/novelty/feasibility/validity floors.

**Next-move BO is DECISIVE for the LATER route too (the `bo_next_move` gate).** Post-experiment/analysis, after you update quest-local Findings Memory (`findings update`), the next move is BO-chosen when NO hard gate forces it and ≥2 hard-gate-ELIGIBLE moves exist: when `bo_next_move` is `blocking`, dispatch the **BO-reviewer** for `bo-review` — pass the `findings summarize` digest + the eligible slate from `$HARNESS bo next-moves` (open opportunities + the synthetic write/finalize/stop moves, each tagged with hard-gate eligibility + a route_target). Ingest with `$HARNESS bo review --next-move --from-json`, then `$HARNESS bo select --next-move --at <ts>` — this records a `bo_decision` (decision_kind auto-derived: experiment-/opportunity-/stop-write-finalize-selection) and the winner's `selected_route` is the BOUND next stage you dispatch (open opportunity → experiment/analysis, write → outline/write, finalize → finalize, stop → decision). Create the handoff for that stage. If exactly one move is eligible, record an explicit skip (`bo select --next-move --skip-reason "<why>"`). BO ranks ONLY moves the hard gates already permit (`bo next-moves` excludes ineligible write/finalize/experiment moves), so it never bypasses the campaign/bridge/claim-evidence/review/finalize gates; a fresh decision is required after each new result/analysis.

## Internal-stage methodology self-audit (step 5b / 6)
Workers self-report `methodology_used` for their stages; YOU are the worker for `decision`/`optimize`/`finalize`, so when you close one of those rounds you MUST record the audit artifact yourself:
`$HARNESS record apply --type artifact.record` with `kind='methodology-usage'`, `round_index=<r>`, and `ref=runs/<q>/methodology/r<r>-<stage>.md` citing **research-method** (the decision-route-criteria / optimize search / finalization-checklist cards you applied) + the bound output (the `decision`/`frontier`/`finalize_outcome` row). `finalize` additionally consults **paper-craft**/**review-craft** for the closure report. This is an audit overlay only — NOT authoritative over the DB rows. `$HARNESS plan validate` warns when a closed internal-stage round lacks this artifact.

## Continuation & plan render (step 6 / 7)
`$HARNESS wakeup arm` on lane `main` (next_stage, reason, next_action) → send the `deepresearch.email.self-wakeup` self-mail → `$HARNESS wakeup attach --message-ref <ref>`.

**Re-render the plan map:** after closing a round (`round.close`), run `$HARNESS plan render --quest-id <q> --at <ts>` so `runs/<q>/plan.md` (a pure DB projection; never read back as truth) reflects the new node/route/revision state. The `plan_map_fresh` invariant flags a stale map if this is skipped. Record the internal-stage methodology-usage artifact (step 6) BEFORE re-rendering so the plan map reflects it.

## Output & Stop
- One reconciliation/dispatch/terminate step recorded through the harness, plus an armed self-wakeup.
- End the turn after one bounded pass.

## Common Mistakes
- Acting on chat-provided or remembered state instead of re-reading the cursor first — the tick must act only on persisted state to stay heartbeat-safe and idempotent.
- Sleeping, polling, or waiting in chat for a result — instead **stop** at the wait gate (step 3); the result mail will wake you.
- Doing more than one bounded pass per tick — record exactly one step, then arm the wakeup and end the turn.
- Re-dispatching a `processed`/`failed` handoff (the transition guard rejects it), or opening a *new* `handoff_id` on a resend instead of reusing the same id with `bump_attempt` (causes double-open / no specialist re-wake).
- Routing on LLM discretion when a hard gate is `blocking` — always dispatch to the first blocking gate's `route_target`; gate status makes routing deterministic but never replaces the hard guards.
- Proceeding on a `fail` gate that is actually *stale* (changed evidence/results/claims/spine/review target) — re-run the relevant validator before routing onward.
- Letting the scout's prose (or your own discretion) pick the winner when `bo_idea_decision`/`bo_next_move` is blocking — BO is DECISIVE among gate-eligible candidates; you must run `bo review` + `bo select` (or record an explicit skip), and BO never overrides the hard floors/gates.
- Completing without the full publication bundle / scholarship bar, or env-waiving a finalize-sensitive gate silently — the harness hard-blocks these apply-time; route back to `write`/`outline` or record a `quality_gate.waiver` with `finalize_ack=true`.
- Self-finalizing in `assistant` / lower-rigor mode when completeness is advisory — recommend via `decision.record(requires_user_confirm=1)` and wait for `decision.confirm`.
- Routinely routing to operator-control for GPU confirmation — GPU is confirmed pre-loop; route there only as a safety fallback if `gpu status` is `confirmed=false`.
- Closing a `decision`/`optimize`/`finalize` round without the `methodology-usage` artifact, or re-rendering the plan map before recording it (stale `plan_map_fresh`).
- Skipping the post-round `plan render`, or reading `runs/<q>/plan.md` back as truth — it is a pure DB projection.
- Reaching across quest boundaries (another quest's findings/refs/artifacts) — every read/write is quest-local to `<q>`.

| Rationalization | Red flag — do NOT |
| --- | --- |
| "I already know the state from the prompt; I'll skip the re-read." | Re-read `control status` + `state query cursor` first; act only on persisted state. |
| "The round isn't done but I'll dispatch the next stage anyway." | Honor the wait gate — stop; a result will wake you. |
| "I'll do a couple of steps while I'm here." | One bounded pass only, then arm the wakeup and stop. |
| "I'll open a fresh handoff_id on resend." | Reuse the same `handoff_id` + `bump_attempt`; never re-dispatch a `processed`/`failed` handoff. |
| "The gate says fail but I think the better route is X." | Dispatch to the first blocking gate's `route_target`; don't override hard gates with discretion. |
| "The gate failed last run, so it's still fail." | Re-validate stale gates (re-run the validator) before routing onward. |
| "The scout already named the winner, so I'll skip BO." | When `bo_idea_decision`/`bo_next_move` is blocking, run BO `review` + `select` (or record an explicit skip). |
| "Acceptance is technically met, I'll just complete." | Run the completeness audit + publication/scholarship gates; technically satisfied ≠ scientifically done. |
| "I'll env-waive the gate and move on." | A bound `complete` is blocked until a durable `quality_gate.waiver` (`finalize_ack=true`) exists. |
| "I performed the decision myself, no audit needed." | Record the `methodology-usage` `artifact.record` for `decision`/`optimize`/`finalize` BEFORE plan render. |
| "Another quest already explored this; I'll reuse it." | Strictly quest-local — never reuse/refer-to/inspect another quest's artifacts. |
