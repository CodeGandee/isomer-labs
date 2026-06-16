---
name: deepresearch-on-receipt
description: Orchestrator on-event skill for the deepresearch loop. Trigger on received mail with schema_id "deepresearch.email.receipt". Advance the handoff to acked (or re-route if not accepted).
---

# On Receipt (Orchestrator)

**Trigger:** received mail, `schema_id = "deepresearch.email.receipt"`.

You are the Orchestrator confirming a specialist accepted a dispatched task. One bounded turn.

## Inputs

- The receipt payload: metadata `loop_id` + `handoff_id`, `accepted`, optional `reason` / `eta`.

## Procedure

1. Parse the metadata; confirm `schema_id` and `handoff_id`.
2. **If `accepted=true`:** `$HARNESS handoff advance --quest-id <quest_id> --handoff-id <handoff_id> --status acked
   --at <ts>` (idempotent: advancing an already-`acked`/later handoff is a no-op). This stops the
   receipt-due resend timer; the loop now waits on `result_due_at`.
3. **If `accepted=false`:** record a route with `$HARNESS record apply --type decision.record` (e.g. reassign
   or `branch`) so `deepresearch-orchestrator-tick` redispatches; optionally `$HARNESS handoff advance
   --status failed` for the declined handoff.
4. `$HARNESS email apply` (in) to log the receipt; archive the mail on success.

## Output

- Handoff advanced to `acked` (or a recorded decision when declined).

## Stop

- End the turn. The task-result reply (or a tick reconciliation) drives the next step.
