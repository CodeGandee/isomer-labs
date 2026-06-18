---
name: deepresearch-mentor
description: Calibrates a drifting route back to the repo owner's standards and taste (architecture convergence, verification rigor, evidence discipline, product/UI taste) by reading the mentor-standards pack. Use when the orchestrator or operator judges the current route technically possible but off-standard, or on explicit operator request. Houmao-original. One bounded turn; does not run the loop or mutate research state.
---

# mentor (companion calibration)

Trigger: the orchestrator (or operator) judges the current route is technically possible but drifting from the repo owner's standards — architecture convergence, verification rigor, evidence discipline, product/UI taste — or an operator explicitly asks for a mentor pass. One bounded turn; not a loop stage.

## inputs
- The active quest cursor plus recent decisions/findings (`$HARNESS state query`, `$HARNESS findings query`).
- The standards reference, when enabled: `$HARNESS knowledge query --kind reference --domain general` → the `mentor-standards` pack `ref` (read its cards). If no pack is enabled, calibrate from state-overview.md discipline plus recent quest decisions only.

## procedure
1. Read the standards pack (if enabled) plus the recent route (last `decision`s, open claims, findings).
2. Judge alignment on: durable-truth discipline (no invented evidence), verification rigor (gates before `supported`), scope/altitude (smallest valid step), and contract hygiene (state only via `$HARNESS`).
3. Produce a concise corrective recommendation: name the drift, the corrected route, and which stage should run next. Record it as a `--type finding.add` (kind `lesson`) and, when it changes the route, recommend a `--type decision.record` for the orchestrator to apply.
4. Return control to the active primary stage — do not turn this into meta-discussion.

## output
- A calibration finding (plus optional recommended decision route). No research-state mutation beyond the finding; the orchestrator owns any route change.

## stop
- End the turn after one calibration pass.
