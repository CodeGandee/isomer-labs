---
name: deepresearch-mentor
description: Use when the orchestrator or operator judges the current research route technically possible but drifting off the repo owner's standards and taste (architecture convergence, verification rigor, evidence discipline, product/UI taste), or on explicit operator request for a mentor pass. Keywords — companion calibration, mentor pass, drift correction, durable-truth, verification-rigor, scope-altitude, contract-hygiene, mentor-standards pack, finding.add lesson, decision.record, one bounded turn. Houmao-original. One bounded turn; does not run the loop or mutate research state.
---

# deepresearch-mentor

## Overview
Companion calibration craft (Houmao-original): in one bounded turn, judge whether the current research route is drifting from the repo owner's standards and taste, name the drift, and record a concise corrective recommendation as a calibration finding. It does not run the loop or mutate research state — the orchestrator owns any route change.

## When to Use
- The orchestrator (or operator) judges the current route is **technically possible but drifting** from the repo owner's standards — architecture convergence, verification rigor, evidence discipline, product/UI taste.
- An operator **explicitly asks for a mentor pass**.

When NOT to use:
- Not a loop stage: this is a single bounded calibration turn, not a research stage. Do not run the loop from here.
- Not a state-mutation surface: never finalize, mutate results, or change quest state beyond the one calibration finding (and an optional recommended decision the orchestrator applies).
- Not for routes that are infeasible: this calibrates an off-standard but *possible* route, not a re-plan of an impossible one.
- Stay within quest-isolation bounds: calibrate the active quest's route only.

## Workflow
1. Read the recent route: pull the active quest cursor plus recent decisions/findings.
   - `$HARNESS state query`
   - `$HARNESS findings query`
2. Read the standards reference, when enabled: `$HARNESS knowledge query --kind reference --domain general` → the `mentor-standards` pack `ref` (read its cards). If no pack is enabled, calibrate from `state-overview.md` discipline plus the recent quest decisions only. (The cards are surfaced by the **deepresearch-mentor-standards** skill.)
3. Judge alignment on the four axes (see **Alignment Axes** below): durable-truth discipline, verification rigor, scope/altitude, and contract hygiene.
4. Produce a concise corrective recommendation — name the drift, the corrected route, and which stage should run next. Record it as a `--type finding.add` (kind `lesson`). When it changes the route, recommend a `--type decision.record` for the orchestrator to apply.
5. Return control to the active primary stage. Do not turn this into meta-discussion.

If the task does not map cleanly to these steps, use your native planning tool to build a plan from the commands/constraints in this skill, then execute it.

## Inputs
- The active quest cursor plus recent decisions/findings (`$HARNESS state query`, `$HARNESS findings query`).
- The standards reference, when enabled (`$HARNESS knowledge query --kind reference --domain general` → the `mentor-standards` pack `ref`; read its cards). If no pack is enabled, calibrate from `state-overview.md` discipline plus recent quest decisions only.

## Alignment Axes
Judge the recent route (last `decision`s, open claims, findings) against:
- **Durable-truth discipline** — no invented evidence.
- **Verification rigor** — gates pass before any claim is marked `supported`.
- **Scope / altitude** — the smallest valid step, not an oversized leap.
- **Contract hygiene** — state changes go only via `$HARNESS`.

## Output
- A calibration finding recorded via `--type finding.add` (kind `lesson`), plus an optional recommended decision route (`--type decision.record`) for the orchestrator to apply. No research-state mutation beyond the finding; the orchestrator owns any route change.

## Stop
- End the turn after one calibration pass.

## Audit / Boundaries
- One bounded turn only — not a loop stage.
- The only state this skill writes is the calibration `finding.add` (kind `lesson`); any `decision.record` is a *recommendation* the orchestrator applies, not a change you make to research state.
- All state changes go via `$HARNESS`; the DB stays canonical and this craft is advisory.

## Common Mistakes
- **Turning the pass into meta-discussion.** Produce the corrective recommendation, record the finding, and return control to the active primary stage.
- **Mutating research state.** Beyond the one calibration finding (and an optional *recommended* decision), make no state change — the orchestrator owns any route change.
- **Running the loop.** This is one bounded turn, not a loop stage; do not advance stages from here.
- **Calibrating an infeasible route.** Only correct routes that are technically possible but off-standard; an impossible route needs a re-plan, not calibration.
- **Skipping the standards pack when it is enabled.** Read the `mentor-standards` cards; fall back to `state-overview.md` discipline plus recent decisions only when no pack is enabled.
- **Bypassing the contract.** Record outcomes only through `$HARNESS` (`finding.add`, `decision.record`); never assert evidence or mark a claim `supported` without gates passing.

## Rationalizations / Red Flags
| If you catch yourself thinking… | Stop — the rule is |
|---|---|
| "I'll just fix the route directly while I'm here." | Record a `decision.record` *recommendation*; the orchestrator applies route changes, not the mentor. |
| "One more turn to discuss the architecture." | One bounded calibration pass, then return control. End the turn. |
| "The claim is basically fine, mark it supported." | Verification rigor — gates pass before `supported`. Flag the missing gate as the drift. |
| "A bigger step will save a round." | Scope/altitude — recommend the smallest valid step. |
| "I'll note it in memory / a side file." | Contract hygiene — record via `$HARNESS finding.add` (kind `lesson`); the DB is canonical. |
| "I can infer this evidence." | Durable-truth — no invented evidence; name it as drift. |
