---
name: deepresearch-on-self-wakeup
description: Use when orchestrator mail arrives with schema_id "deepresearch.email.self-wakeup" in the deepresearch loop. Keywords — self-wakeup, durable continuation, continuation_lane, loop_id, handoff_id, next_stage, next_action, wakeup list/resolve, orchestrator-tick, delivered/consumed/superseded. Resumes the durable continuation spine for one bounded tick.
---

# On Self-Wakeup (orchestrator)

## Overview

You are the deepresearch orchestrator resuming the durable continuation spine. A self-wakeup mail is the
**only** continuation mechanism in this loop (there are no live reminders): on receipt you resolve the matching
durable continuation and run exactly one reconciliation/dispatch tick to advance the stage machine, then stop.

## When to Use

- **Trigger:** received mail with `schema_id = "deepresearch.email.self-wakeup"`. The payload carries metadata
  `loop_id` + `handoff_id` + `continuation_lane`, plus `next_stage`, `reason`, and `next_action`.
- You are acting as the **orchestrator** resuming the continuation spine for one bounded turn.

**When NOT to use:**
- The mail is not a self-wakeup (`schema_id` differs) — route by its actual schema (e.g. a result mail goes to
  the result handler, a task request to the request handler), not here.
- You are not the orchestrator role / not on the continuation spine.
- The wakeup for this `handoff_id` is already `consumed` or `superseded` — this is a late/duplicate delivery;
  archive the mail and stop (see Workflow step 2). Do not run a tick.
- Quest-isolation bounds: act only on the continuation/lane named in THIS payload; never reach across quests.

## Workflow

1. **Parse + confirm.** Parse the payload metadata and confirm `schema_id = "deepresearch.email.self-wakeup"`.
   Look up the matching durable row: `$HARNESS wakeup list`. Identify the `wakeup_id` for this `handoff_id`.
2. **Dedup / late-delivery gate.** If the wakeup for this `handoff_id` is already `consumed` or `superseded`,
   a re-arm has replaced it — **archive the mail and stop**. Do not resolve or tick.
3. **Mark delivered.** `$HARNESS wakeup resolve --wakeup-id <wakeup_id> --status delivered --at <ts>`.
4. **Perform `next_action`.** Normally this runs **deepresearch-orchestrator-tick** for one
   reconciliation/dispatch pass on lane `<continuation_lane>` (default `main`). That tick reads posture,
   reconciles stalled handoffs, applies the wait/terminal/dispatch gates, and (if more work remains) arms the
   next self-wakeup.
5. **Consume + archive.** `$HARNESS wakeup resolve --wakeup-id <wakeup_id> --status consumed --at <ts>`; archive
   the self-mail.
6. **Stop.** End the turn. The tick (step 4) arms the next `deepresearch.email.self-wakeup` if more work remains;
   if nothing was armed, the spine is intentionally idle until the next continuation root fires.

If the task does not map cleanly to these steps, use your native planning tool to build a plan from the commands
and constraints in this skill, then execute it.

## Common Mistakes

- **Running a tick on a stale wakeup.** A `consumed`/`superseded` row means a re-arm already superseded this
  continuation — running the tick would double-advance the stage machine. Always run the dedup gate (step 2)
  before resolving or ticking.
- **Skipping the `delivered` → `consumed` transition.** Both resolves are required: `delivered` before the
  action, `consumed` after. Leaving the wakeup at `delivered` (or never resolving) corrupts the continuation
  ledger and breaks the next arm.
- **Not archiving the self-mail.** Archive on both paths — the late-delivery stop (step 2) and the normal
  completion (step 5) — so the inbox does not re-trigger on the same wakeup.
- **Treating self-wakeup as a poll/sleep loop.** This is one bounded turn, not a heartbeat you sit in. Do not
  sleep, poll, or wait in chat; if more work remains, the tick arms the next wakeup and a future mail resumes you.
- **Ignoring `continuation_lane`.** Run the tick on the lane named in the payload (default `main`); do not assume
  `main` when another lane is specified.
- **Cross-quest reach.** Operate only within the quest/lane this payload names.

## Inputs

- The self-wakeup payload: metadata `loop_id` + `handoff_id` + `continuation_lane`, plus `next_stage`, `reason`,
  and `next_action`.

## Commands (verbatim)

- Look up the durable continuation rows: `$HARNESS wakeup list`
- Mark delivered: `$HARNESS wakeup resolve --wakeup-id <wakeup_id> --status delivered --at <ts>`
- Mark consumed: `$HARNESS wakeup resolve --wakeup-id <wakeup_id> --status consumed --at <ts>`

(`$HARNESS <group> <verb>` commands are runtime tools. `<wakeup_id>`, `<ts>`, and `<continuation_lane>` are
resolved from the matching `wakeup list` row / the payload.)

## Output

- The continuation resolved (`delivered` → `consumed`) and one tick pass executed (or, on a late delivery, the
  mail archived with no tick).
