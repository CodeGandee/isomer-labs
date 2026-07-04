# Frontier Review Template

Use this reference at meaningful route boundaries, after measured results, after debug or fusion outcomes, or when plateau/stall signals appear. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Summarize the current frontier**. Record mode, best branch or line, best run, stagnant branches, candidate backlog, fusion candidates, and blockers in <FRONTIER_REVIEW>.
2. **Summarize evidence**. State strongest support, strongest contradiction, biggest unresolved risk, and whether evidence favors explore, exploit, fusion, debug, or stop.
3. **Choose the route**. Select explore, exploit, fusion, debug, or stop with why-this-now reasoning.
4. **Choose the active submode**. Select brief, rank, seed, loop, fusion, debug, or stop and explain why it dominates now.
5. **Name the immediate next action**. State exact next step, what result triggers another frontier review, and what result forces a different mode.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer explore when no line is dominant, lines are too similar, or no strong incumbent exists (if one line clearly leads, otherwise exploit).
- Prefer exploit when one line leads on evidence and comparability (if repeated non-improvement appears, otherwise review plateau).
- Prefer fusion when two lines have complementary strengths (if strengths are redundant, otherwise avoid fusion).
- Prefer debug when a valuable candidate failed for a concrete fixable reason (if failure is strategic, otherwise archive).
- Prefer stop when remaining routes are redundant, saturated, or unjustified relative to cost.

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- <FRONTIER_REVIEW> must not skip stagnant branches, candidate backlog, fusion candidates, or blockers.
- Route choice must follow evidence rather than momentum.
- The active submode must be singular for the next pass.
- Frontier review must name the trigger for another review.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Frontier-field coverage: fraction of mode, best line, best run, stagnant branches, candidate backlog, fusion candidates, blockers, strongest support, contradiction, unresolved risk, route choice, submode, and review trigger fields completed; higher is better.
- Active-submode count: number of active optimize submodes selected for the next pass; closer to exactly 1 is better.

### Checks

- State gate: best line, best run, stagnation, backlog, fusion candidates, and blockers are visible.
- Evidence gate: support, contradiction, and unresolved risk are separate.
- Route gate: explore, exploit, fusion, debug, or stop is justified.
- Submode gate: one active submode is selected.
- Action gate: exact next step and review trigger are stated.

## Template

### Current Frontier

- mode:
- best branch or line:
- best run:
- stagnant branches:
- candidate backlog:
- fusion candidates:

### Evidence Summary

- strongest support:
- strongest contradiction:
- biggest unresolved risk:

### Route Choice

- explore / exploit / fusion / debug / stop:
- why this is the best next move:

### Active Optimize Submode

- brief / rank / seed / loop / fusion / debug / stop:
- why this submode is dominant now:

### Immediate Next Action

- exact next step:
- what result will trigger another frontier review:
- what result would force a different mode:
