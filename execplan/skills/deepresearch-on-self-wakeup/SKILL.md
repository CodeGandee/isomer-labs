---
name: deepresearch-on-self-wakeup
description: Orchestrator on-event skill for the deepresearch loop. Trigger on received mail with schema_id "deepresearch.email.self-wakeup". Resolve the durable continuation and run one tick to advance the stage machine.
---

# On Self-Wakeup (orchestrator)

**Trigger:** received mail, `schema_id = "deepresearch.email.self-wakeup"`.

You are the orchestrator resuming the durable continuation spine. One bounded turn. This is the only
continuation mechanism — there are no live reminders. See `deepresearch-shared-guide`.

## Inputs

- The self-wakeup payload: metadata `loop_id` + `handoff_id` + `continuation_lane`, `next_stage`,
  `reason`, `next_action`.

## Procedure

1. Parse metadata; confirm `schema_id`. Look up the matching row: `$HARNESS wakeup list`.
2. **Dedup / late delivery:** if the wakeup for this `handoff_id` is already `consumed` or `superseded`,
   archive the mail and stop (a re-arm replaced it).
3. `$HARNESS wakeup resolve --wakeup-id <wakeup_id> --status delivered --at <ts>`.
4. Perform `next_action` — normally run **deepresearch-orchestrator-tick** for one reconciliation/dispatch
   pass on lane `<continuation_lane>` (default `main`).
5. `$HARNESS wakeup resolve --wakeup-id <wakeup_id> --status consumed --at <ts>`; archive the self-mail.

## Output

- The continuation resolved (`delivered`→`consumed`) and one tick pass executed.

## Stop

- End the turn. The tick arms the next self-wakeup if more work remains.
