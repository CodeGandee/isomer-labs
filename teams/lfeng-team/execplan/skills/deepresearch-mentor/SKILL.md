---
name: deepresearch-mentor
description: Companion calibration skill for the deepresearch loop (ported DeepScientist mentor). Invoked when work drifts from the repo owner's standards/taste, or on explicit operator request. Tighten the route, then return to the active stage. Does not run the loop or mutate research state.
---

# Mentor (companion calibration)

**Trigger:** the Orchestrator (or operator) judges the current route is technically possible but drifting
from the repo owner's standards — architecture convergence, verification rigor, evidence discipline,
product/UI taste — or an operator explicitly asks for a mentor pass. One bounded turn; not a loop stage.

## Inputs

- The active quest cursor + recent decisions/findings (`$HARNESS state query`, `$HARNESS findings query`).
- The standards reference, when enabled: `$HARNESS knowledge query --kind reference --domain general`
  → the `mentor-standards` pack `ref` (read its cards). If no pack is enabled, calibrate from
  `state-overview.md` discipline + recent quest decisions only.

## Procedure

1. Read the standards pack (if enabled) + the recent route (last `decision`s, open claims, findings).
2. Judge alignment on: durable-truth discipline (no invented evidence), verification rigor (gates before
   `supported`), scope/altitude (smallest valid step), and contract hygiene (state only via `$HARNESS`).
3. Produce a concise corrective recommendation: name the drift, the corrected route, and which stage
   should run next. Record it as a `--type finding.add` (kind `lesson`) and, when it changes the route,
   recommend a `--type decision.record` for the Orchestrator to apply.
4. Return control to the active primary stage — do not turn this into meta-discussion.

## Output

- A calibration finding (+ optional recommended decision route). No research-state mutation beyond the
  finding; the Orchestrator owns any route change.

## Stop

- End the turn after one calibration pass.
