---
name: deepresearch-mentor-standards
description: "Use when the orchestrator (or a mentor calibration step) needs the repo owner's quality bar to judge whether a loop step, claim, or branch decision meets house standards. Keywords: mentor-standards, owner standards, taste cards, durable-truth, verification-rigor, scope-altitude, contract-hygiene, preserve-failed-routes, quality bar, calibration, knowledge cards, read-only methodology lookup."
---

# deepresearch-mentor-standards

## Overview
Surface the `mentor-standards` standards reference so the orchestrator can calibrate the loop to the repo owner's quality bar (durable-truth, verification-rigor, scope-altitude, contract-hygiene, preserve-failed-routes). This is a read-only methodology lookup: it surfaces advisory cards and changes no state — the DB stays canonical.

## When to Use
Trigger this skill when:
- The orchestrator, or a mentor calibration step, needs the owner's standards to judge whether a step, claim, or branch decision meets house standards.
- You must decide if a result is durable truth vs. an artifact of insufficient verification, if scope is at the right altitude, if a contract is clean, or whether a failed route should be preserved rather than discarded.

When NOT to use:
- Do not use this skill to finalize, mutate results, confirm GPU, or change quest state — it is advisory and read-only.
- Do not treat the surfaced cards as an authoritative state surface; the DB is canonical.
- Stay within quest-isolation bounds: apply the standard to the judgment in front of you and continue; do not reach across quests.

## Workflow
1. Surface the owner's standards cards with the harness knowledge command (see Commands). The cards cover durable-truth, verification-rigor, scope-altitude, contract-hygiene, and preserve-failed-routes, each stating the standard and the reason it holds.
2. Apply the relevant standard to the judgment at hand (the step, claim, or branch decision being evaluated).
3. Map any external tool names in the surfaced material (`artifact.*`, `memory.*`, `bash_exec`) onto the `$HARNESS` surface — the surfaced cards may reference tool names that are realized as harness verbs.
4. Do the actual stage work and record outcomes through your role's normal skill/commands. This craft is advisory only; never let it stand in for the canonical DB state surface.
5. Return the method to the calling task and continue (see Stop).
6. If the task does not map cleanly to these steps, use your native planning tool to build a plan from the commands/constraints in this skill, then execute it.

## Commands
Surface the cards (read-only; preserve the audit stamp verbatim):
```
$HARNESS --via skill:deepresearch-mentor-standards:<your-role> knowledge cards --query standards
```
Alternative query form for the same content:
```
$HARNESS --via skill:deepresearch-mentor-standards:<your-role> knowledge query --kind reference
```

## The Standards Cards
The owner's standards cards each state the standard and the reason it holds:
- **durable-truth** — a result must be durable truth, not an artifact of the run.
- **verification-rigor** — claims hold only to the level they were verified.
- **scope-altitude** — work must sit at the right altitude of scope.
- **contract-hygiene** — contracts stay clean.
- **preserve-failed-routes** — failed routes are preserved, not silently discarded.

Surface the cards via the command above for each card's full standard text and rationale (the authoritative wording).

## Audit / Boundaries
- `--via skill:deepresearch-mentor-standards:<role>` is passed for traceability. Because the lookup is read-only, it records no row.
- Never finalize, mutate results, confirm GPU, or change quest state from here.
- The DB stays canonical; this craft is advisory, never an authoritative state surface.

## Stop
- Return the method to the calling task and continue.

## Common Mistakes
- Treating the surfaced cards as an authoritative state surface — they are advisory; the DB is canonical.
- Finalizing, mutating results, confirming GPU, or changing quest state from this lookup — it is strictly read-only.
- Dropping or rewriting the `--via skill:deepresearch-mentor-standards:<role>` audit stamp — keep it verbatim for traceability.
- Failing to map external tool names (`artifact.*`, `memory.*`, `bash_exec`) in the surfaced material onto the `$HARNESS` surface, then acting on a tool name that does not exist as written.
- Recording stage outcomes from this skill instead of through your role's normal skill/commands.

| Rationalization | Red flag — do NOT |
| --- | --- |
| "These cards look authoritative, I'll treat them as state." | The DB is canonical; the cards are advisory only. |
| "I'm already calibrated, I can finalize/confirm GPU from here." | Never finalize, mutate results, confirm GPU, or change quest state from this lookup. |
| "I'll simplify the audit stamp." | Preserve `--via skill:deepresearch-mentor-standards:<role>` exactly. |
| "The surfaced material says `bash_exec`, I'll run that." | Map `artifact.*` / `memory.*` / `bash_exec` onto the `$HARNESS` surface first. |
