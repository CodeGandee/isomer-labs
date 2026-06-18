---
name: deepresearch-mentor-standards
description: Repo-owner standards and taste cards that calibrate the loop to the owner's quality bar — durable-truth, verification-rigor, scope-altitude, contract-hygiene, and preserve-failed-routes, each stating the standard and why it holds. Use when the orchestrator (or the mentor calibration step) needs the owner's bar to judge whether a step, claim, or branch decision meets house standards. Read-only methodology lookup; surfaces a reference pack and changes no state.
---

# mentor-standards (read-only methodology lookup)

Surfaces the `mentor-standards` reference pack for the **orchestrator** to calibrate the loop to the repo
owner's quality bar. The pack is the source of truth; this skill only surfaces its cards and makes no state
change.

## Use
1. Surface the cards:
   `$HARNESS --via skill:deepresearch-mentor-standards:<your-role> knowledge cards --query standards`
   (or `knowledge query --kind reference`). The pack delivers the owner's standards cards
   (durable-truth, verification-rigor, scope-altitude, contract-hygiene, preserve-failed-routes), each with
   the standard and the reason it holds.
2. Apply the standard to the judgment at hand.
3. Do the stage work and record outcomes through your role's normal skill/commands. The DB stays canonical;
   this craft is advisory, never an authoritative state surface. Map any external tool names in the
   surfaced material (`artifact.*`, `memory.*`, `bash_exec`) to the `$HARNESS` surface.

## Audit / boundaries
- `--via skill:deepresearch-mentor-standards:<role>` is passed for traceability; read-only, so it records no row.
- Never finalize, mutate results, confirm GPU, or change quest state from here.

## Stop
- Return the method to the calling task and continue.
