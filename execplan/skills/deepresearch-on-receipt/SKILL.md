---
name: deepresearch-on-receipt
description: "Use when the orchestrator receives mail with schema_id \"deepresearch.email.receipt\" in the deepresearch loop — a specialist's accept/decline ack for a dispatched handoff (metadata loop_id, handoff_id, accepted, optional reason/eta). Keywords: receipt, handoff advance, acked, re-route decision, receipt-due resend timer, result_due_at."
---

# Deepresearch On Receipt (orchestrator)

## Overview

Orchestrator on-event handler for the deepresearch loop: when a specialist returns a `deepresearch.email.receipt`, confirm acceptance by advancing the handoff to `acked` (stopping the receipt-due resend timer), or record a re-route decision when the specialist declined. One bounded turn.

## When to Use

- You are the **orchestrator** and have received mail whose `schema_id = "deepresearch.email.receipt"`.
- The mail is a specialist's acknowledgement of a dispatched task: payload metadata carries `loop_id` + `handoff_id`, `accepted` (true/false), and optional `reason` / `eta`.

**When NOT to use:**
- You are not the orchestrator role, or the event/`schema_id` is anything other than `deepresearch.email.receipt` (e.g. a task result, a tick, an operator control message) — route to the matching on-event skill instead.
- Do not cross quest boundaries: operate only on the handoff/quest named in this receipt; never reuse or inspect another quest's handoffs or artifacts.

## Inputs

- The receipt payload: metadata `loop_id` + `handoff_id`, `accepted`, optional `reason` / `eta`.

## Workflow

1. **Parse the metadata.** Confirm `schema_id` is `deepresearch.email.receipt` and read the `handoff_id` (and `loop_id`).
2. **If `accepted=true` — advance the handoff to `acked`:**
   ```
   $HARNESS handoff advance --quest-id <quest_id> --handoff-id <handoff_id> --status acked --at <ts>
   ```
   This is idempotent: advancing an already-`acked`/later handoff is a no-op. It stops the receipt-due resend timer; the loop now waits on `result_due_at`.
3. **If `accepted=false` — record a re-route decision:** apply a decision record so the tick redispatches:
   ```
   $HARNESS record apply --type decision.record
   ```
   (e.g. reassign or `branch`). Optionally also advance the declined handoff to `failed`:
   ```
   $HARNESS handoff advance --status failed
   ```
4. **Log and archive the mail:** `$HARNESS email apply` (in) to log the receipt; archive the mail on success.
5. **Stop.** End the turn. The task-result reply (or a tick reconciliation) drives the next step.

If the task does not map cleanly to these steps, use your native planning tool to build a plan from the commands/constraints in this skill, then execute it.

## Output

- Handoff advanced to `acked` (or a recorded decision when declined).

## Stop

- End the turn. The task-result reply (or a tick reconciliation) drives the next step.

## Common Mistakes

- **Acting outside one bounded turn.** This handler does exactly one thing (advance, or record a decision) and stops. Do not chain into redispatch, scheduling, or result handling here — those belong to `deepresearch-orchestrator-tick` and `deepresearch-on-task-result`.
- **Missing the `--at <ts>` / quest scoping.** Always pass `--quest-id <quest_id>` and `--at <ts>` so the advance is correctly attributed and ordered; never operate without the quest id.
- **Treating idempotency as an error.** Re-advancing an already-`acked`/later handoff is a deliberate no-op, not a failure — do not "fix" it or branch on it.
- **Dropping the decline path.** On `accepted=false` you MUST record a `decision.record` so the tick redispatches; silently archiving a decline strands the loop.
- **Archiving on failure.** Only archive the mail on success (after the advance/decision is applied).
- **Cross-quest leakage.** Never reference, reuse, or inspect another quest's handoffs/decisions while processing this receipt.
