---
name: deepresearch-on-task-result
description: Orchestrator on-event skill for the deepresearch loop. Trigger on received mail with schema_id "deepresearch.email.task-result". Fold the specialist's result into state, gate/validate it, advance the handoff, and route when the round's fan-out is complete.
---

# On Task Result (orchestrator)

**Trigger:** received mail, `schema_id = "deepresearch.email.task-result"`.

You are the orchestrator collecting a specialist's result. One bounded turn. See `deepresearch-shared-guide`.

## Inputs

- The task-result payload: metadata `loop_id` + `handoff_id`, `status`, `stage`, `produced[]`,
  `methodology_used[]`, `error`.

## Procedure

1. Parse metadata; confirm `schema_id`. **Dedup (covers retried handoffs):** `$HARNESS handoff query
   --seen <handoff_id>`. If status is `processed` (or `failed`), this is a **duplicate / late result for an
   already-settled handoff** — archive the mail and **stop**, recording nothing. A resend bumps
   `attempt_count` but keeps the same `handoff_id`, so a result that arrives after you already settled the
   round must never re-fold. (Belt-and-suspenders: even if a fold slipped through, `record apply` is
   idempotent on `record_id`, so produced rows would not duplicate; and the `handoff` transition guard
   rejects advancing a terminal handoff.)
2. **Fold in** (the specialist already wrote its rows; you confirm/gate):
   - `experiment` result → `$HARNESS result validate` (sets `result.validity`); if a new valid best,
     `$HARNESS record apply --type quest.update --best_result_ref ...`.
   - `scope` → `$HARNESS scope validate --quest-id <q>` (computes the validator-owned `valid` on the typed
     `scope.contract`: concrete objective + primary metric/direction + eval plan or explicit waivers). A vague
     or under-specified scope is rejected; idea selection (bound) cannot proceed until it passes.
   - `baseline` → **first** `$HARNESS baseline validate --quest-id <q>` (computes the validator-owned `valid`
     flag from the contract's `baseline_route` + eval contract + route-specific verification), **then** set the
     gate: `$HARNESS record apply --type quest.update --baseline_gate passed|waived|blocked`. `passed`/`waived`
     now require `valid=1` — an author-asserted `verification_verdict` alone is rejected; if `baseline validate`
     fails, route back to `baseline` with its reasons rather than opening the gate.
   - `analysis`/`write` → confirm the produced rows exist via `$HARNESS state query`.
   - `review` → the Reviewer must have recorded a typed `review.verdict` (verdict + verdict_ref to the typed
     verdict.json). Run `$HARNESS review validate --quest-id <q>` (schema + actionability; sets `valid` +
     `route_target`) and `$HARNESS evidence validate`. **If `review validate` fails** (non-actionable verdict),
     treat it like the Tier-3 gap below (auto: re-dispatch the review handoff with a corrective note; assistant:
     `decision.record(requires_user_confirm=1)`) — a non-actionable verdict is NOT accepted.
   - `status=failed` → record a `decision.record` (continue/branch/reset/stop) per the failure.
2a. **Review-verdict routing.** After a VALID review verdict, read `$HARNESS review route --quest-id <q>`
   and route deterministically by `route_target`: `reject`/`borderline` → open the next handoff to
   **experiment** (missing_experiments), **analysis** (missing_analysis), or **write** (overclaims /
   unsupported_claims / rewrite_requirements), carrying the verdict's `*_todo[]` as the task brief; do NOT
   route to finalize. `accept` → the review side permits finalize, but a `complete` finalize.record still requires
   `manuscript coverage` (`submission_ready=true`) — both gates are enforced at the write path. A `borderline`
   at standard rigor needs an operator `review confirm` before finalize (publication never permits borderline).
2b. **Methodology-resolution check (Tier-3 gate).** For each `methodology_used[]` item, run
   `$HARNESS methodology check --quest-id <q> --stage <stage> --applied-as <item.applied_as>`. It must
   **resolve** (the ref points at the stage's validated typed record: scope.contract / idea.select / baseline.contract /
   analysis.bridge / paper_spine / review.verdict). `methodology_used` is NO LONGER free text — an item whose
   `applied_as` does not resolve is treated as missing (background-only reading belongs in
   `methodology_consulted`, which does not count). If any required pack lacks a RESOLVING `methodology_used`
   item:
   - **`autonomy_mode='auto'`:** do **not** advance to `processed`. Re-dispatch the same `handoff_id`
     (`$HARNESS handoff open ... bump_attempt`) with a corrective note ("produce + validate the stage's typed
     record so each `methodology_used[].applied_as` resolves"), re-deliver the task-request, arm continuation, stop.
   - **`autonomy_mode='assistant'`:** record the gap as a `decision.record(requires_user_confirm=1)` + surface a
     clear BLOCKING warning to the operator (deepresearch-operator-control); do not silently accept.
   (`$HARNESS plan validate` independently warns at round close; this fold-time check is the active gate.)
3. **Advance the handoff:** `$HARNESS handoff advance --quest-id <quest_id> --handoff-id <handoff_id> --status
   result_received --at <ts>` then `--status processed`. Update fan-out: `$HARNESS record apply --type
   round.update --received_handoffs <n>`.
4. **If the round's fan-out is complete** (the round's `received_handoffs` ≥ expected, cross-checked via
   `$HARNESS handoff query --quest-id <q>`): close the round (`--type round.close`) and **route via
   `$HARNESS gate status --quest-id <q>`** — do NOT route on prose/LLM discretion when a hard gate says
   fail. Read `data.gates`: dispatch the next stage to the **first blocking gate's `route_target`**
   (scope_contract→scope, idea_gate→idea, baseline_contract→baseline, campaign_coverage→experiment|analysis,
   analysis_bridge→analysis, paper_spine/outline_valid→outline, manuscript_coverage→write,
   review_verdict→its `route_target`); if
   `finalize_readiness=pass` (no blocking gates), route to finalize. Then arm the continuation (as in
   `deepresearch-orchestrator-tick`). **If not complete:** stop and wait for the next worker's result.
5. `$HARNESS email apply` (in); archive the mail on success.

## Output

- State folded + gated; handoff `processed`; next stage dispatched when the round is complete.

## Stop

- End the turn after one result (and at most one routing pass when the round completes).
