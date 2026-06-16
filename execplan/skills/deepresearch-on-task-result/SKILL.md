---
name: deepresearch-on-task-result
description: Orchestrator on-event skill for the deepresearch loop. Trigger on received mail with schema_id "deepresearch.email.task-result". Fold the specialist's result into state, gate/validate it, advance the handoff, and route when the round's fan-out is complete.
---

# On Task Result (Orchestrator)

**Trigger:** received mail, `schema_id = "deepresearch.email.task-result"`.

You are the Orchestrator collecting a specialist's result. One bounded turn.

## Inputs

- The task-result payload: metadata `loop_id` + `handoff_id`, `status`, `stage`, `produced[]`,
  `methodology_used[]`, `error`.

## Procedure

1. Parse metadata; confirm `schema_id`. **Dedup (covers retried handoffs):** `$HARNESS handoff query
   --seen <handoff_id>`. If status is `processed` (or `failed`), this is a **duplicate / late result for an
   already-settled handoff** — archive the mail and **stop**, recording nothing. A resend bumps
   `attempt_count` but keeps the same `handoff_id`, so a result that arrives after you already settled the
   round must never re-fold. (Belt-and-suspenders: even if a fold slipped through, `record apply` is
   idempotent on `record_id`, so the produced rows would not duplicate; and the `handoff` transition guard
   rejects advancing a terminal handoff.)
2. **Fold in** (the specialist already wrote its rows; you confirm/gate):
   - `experiment` result → `$HARNESS result validate` (sets `result.validity`); if a new valid best,
     `$HARNESS record apply --type quest.update --best_result_ref ...`.
   - `baseline` → set the gate: `$HARNESS record apply --type quest.update --baseline_gate passed|waived|blocked`.
   - `analysis`/`write`/`review` → confirm the produced rows exist via `$HARNESS state query`; for review,
     run `$HARNESS evidence validate` before any synthesis advance.
   - `status=failed` → record a `decision.record` (continue/branch/reset/stop) per the failure.
2b. **Methodology-usage check (Tier-3 gate).** For a stage with a required pack (see
   `deepresearch-on-task-request` 3b / `REQUIRED_PACKS`), confirm the result carries `methodology_used[]`
   covering EACH required pack AND that the worker's `artifact(kind='methodology-usage')` exists for this
   round (`$HARNESS state query` / artifact rows). Also confirm the **bound output** where cheap: `outline` →
   `outline validate` passes; `write` → `manuscript validate` passes; `review` → review-report + experiment-todo
   artifacts present; `idea` → a selection-gate artifact is referenced. If a required citation or the audit
   artifact is missing:
   - **`autonomy_mode='auto'`:** do **not** advance to `processed`. Re-dispatch the same `handoff_id`
     (`$HARNESS handoff open ... bump_attempt`) with a corrective note ("record the methodology-usage artifact +
     methodology_used for pack X before completing"), re-deliver the task-request, arm the continuation, stop.
   - **`autonomy_mode='assistant'`:** record the gap as a `decision.record(requires_user_confirm=1)` + surface a
     clear BLOCKING warning to the operator (deepresearch-operator-control); do not silently accept.
   (`$HARNESS plan validate` independently warns at round close; this fold-time check is the active gate.)
3. **Advance the handoff:** `$HARNESS handoff advance --quest-id <quest_id> --handoff-id <handoff_id> --status
   result_received --at <ts>` then `--status processed`. Update fan-out: `$HARNESS record apply --type
   round.update --received_handoffs <n>`.
4. **If the round's fan-out is complete** (the round's `received_handoffs` ≥ expected, cross-checked via `$HARNESS handoff query --quest-id <q>`):
   close the round (`--type round.close`) and route the next stage exactly as in
   `deepresearch-orchestrator-tick` (dispatch + arm continuation). **If not complete:** stop and wait for
   the next worker's result to wake you.
5. `$HARNESS email apply` (in); archive the mail on success.

## Output

- State folded + gated; handoff `processed`; next stage dispatched when the round is complete.

## Stop

- End the turn after one result (and at most one routing pass when the round completes).
