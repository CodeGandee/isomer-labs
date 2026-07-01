# Operational Guidance

Use this reference when the optimize route needs the longer execution notes rather than the short control surface in `SKILL.md`. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Recover working surfaces**. Refresh <OPTIMIZATION_FRONTIER>, <OPTIMIZE_CHECKLIST>, <CANDIDATE_BOARD>, active line plan, and immediate next move before creating or promoting anything.
2. **Recover frontier state and prior lessons**. Inspect candidate briefs, durable lines, implementation attempts, measured results, failures, blockers, route recommendation, and relevant <OPTIMIZATION_MEMORY_CARD> entries.
3. **Select exactly one submode**. Choose fusion, debug, rank, brief, seed, loop, or stop based on frontier state; record a route shift if new evidence changes the selected submode.
4. **Run the candidate protocol**. For brief mode, shape `2-4` serious branchless briefs; for rank mode, compare on one surface and apply promotion caps; for promotion, create one or a few distinct durable lines only when justified.
5. **Run seed or loop protocol**. For seed mode, create a small differentiated within-line candidate pool; for loop mode, move one candidate through smoke, full evaluation, archive, debug, fusion, stop, or experiment handoff.
6. **Use validation-cost-aware breadth**. Use broader quick checks when first-pass validation is cheap and differentiated; keep active pools narrow when validation is slow or expensive.
7. **Record attempts and results**. Keep <OPTIMIZATION_ATTEMPT_RECORD> distinct from <PROMOTED_OPTIMIZATION_LINE> and measured experiment results; update <CANDIDATE_BOARD> and <FRONTIER_REVIEW> after meaningful movement.
8. **Handle debug, fusion, and plateau deliberately**. Use <DEBUG_RESPONSE>, <FUSION_PLAN>, and <PLATEAU_RESPONSE> when those routes dominate, and stop near-duplicate low-information moves.
9. **Preserve reusable lessons**. Write <OPTIMIZATION_MEMORY_CARD> only for reusable success patterns, repeated failure patterns, fusion lessons, or non-retry rules.
10. **Complete with one route**. End only when <OPTIMIZE_ROUTE_DECISION> or <OPTIMIZE_BLOCKER_RECORD> names one next action, stop condition, experiment handoff, route change, or blocker.

## Preferences

- Prefer one bottom-layer optimize move in progress at a time (if multiple live attempts exist, otherwise isolate and justify them).
- Prefer frontier refresh before candidate generation (if frontier is stale or missing, otherwise recover it first).
- Prefer fusion before debug only when the frontier explicitly says fusion (if a concrete fixable failure dominates, otherwise debug).
- Prefer rank before promotion when several serious briefs exist (if one candidate clearly dominates, otherwise rank).
- Prefer seed before broad loop when a durable line lacks an implementation-candidate pool.
- Prefer quick evidence over over-arguing when validation is cheap (if validation is slow, otherwise narrow the candidate pool).

## Constraints

- <OPTIMIZATION_FRONTIER> must be checked before new candidates, promotion, fusion, debug, or stop decisions.
- One pass must not bounce among submodes without recording a route shift.
- Candidate briefs should remain branchless until promotion is justified.
- Promotion should normally be capped at `1-3` durable lines and at most one per mechanism family unless a candidate clearly dominates.
- A live implementation pool should not be dominated by one mechanism family.
- Same unchanged candidates must not be rerun.
- Full evaluations should not start when smoke, pilot, or quick validation is required to remove avoidable uncertainty.
- A completed optimize pass must leave one durable next action or stop condition.

## Quality Gates

### Metrics

- Mechanism-family coverage: number of distinct mechanism families represented in the serious brief slate before ranking; higher is better until the slate is not one-family narrow.
- Primary-submode count: number of primary optimize submodes selected for one meaningful pass; closer to exactly 1 is better.

### Checks

- Frontier gate: candidates, active lines, recent results, failures, blockers, and recommended route are current.
- Submode gate: fusion, debug, rank, brief, seed, loop, or stop is singular and justified.
- Candidate gate: brief slate has differentiated mechanisms, shared comparison surface, ranking or promotion rationale, and cap.
- Execution gate: seed or loop action has candidate id, parent line, strategy, validation step, status, and archive condition.
- Cost gate: active pool breadth matches validation cost and expected information gain.
- Plateau gate: repeated non-improvement triggers widen, stronger alternative, fusion, debug, stop, or non-repeat rule.
- Memory gate: reusable lessons are recorded only when decision-relevant.
- Completion gate: one next route, experiment handoff, stop, or blocker is recorded.

## Submode Selection

Use this default priority unless local evidence gives a stronger reason:

1. `fusion` when the frontier explicitly says fusion and source-line strengths are complementary.
2. `debug` when a strategically valuable candidate failed for a concrete and likely fixable reason.
3. `rank` when several candidate briefs exist and promotion is unresolved.
4. `brief` when the candidate slate is too thin, weak, same-family, or unclear.
5. `seed` when a durable line exists but no live implementation-candidate pool exists.
6. `loop` when a live candidate pool or leading durable line needs bounded execution progress.
7. `stop` when remaining routes are low-value, redundant, or unjustified.

## Route Meanings

- `explore`: widen search with fresh candidate directions.
- `exploit`: focus on the strongest current line.
- `fusion`: combine insights from complementary successful or promising lines.
- `debug`: rescue a strategically valuable candidate or line blocked by concrete failure.
- `stop`: record that the frontier is saturated or not worth further cost.

## Seed and Loop Rules

- Seed mode should usually create `2-3` implementation-level candidates, or `1-2` when validation is slow.
- A newly promoted line should include one simple-first candidate unless evidence already rules it out.
- Loop mode should choose one primary action: smoke, promote to full evaluation, archive, record measured result, switch to fusion, switch to debug, or stop.
- Every loop pass should update candidate status, next action, and frontier-review trigger.
- Do not bundle unrelated exploit changes unless they form one coupled design package or the route is fusion.

## Execution Rules

- Use Execution Adapter Command Requests for smoke checks, quick validations, and full runs until native execution bindings are finalized.
- Prefer bounded smoke before full evaluation unless cheap direct validation is equally informative.
- Keep live implementation candidates small: usually `2-3` in smoke and `1-2` in full evaluation unless resources clearly support more.
- If validation is under about `20` minutes and likely to separate candidates, modestly broaden quick validation.
- If validation is slow, require objective signal before heavier resource investment.
- When a candidate fails with a clear root cause, debug it deliberately or archive it.

## Completion Rule

Optimize is complete only when a stronger line was promoted, the current line produced a measured result and route, the frontier says stop, or a blocker is recorded. One candidate creation or one smoke pass is not completion.
