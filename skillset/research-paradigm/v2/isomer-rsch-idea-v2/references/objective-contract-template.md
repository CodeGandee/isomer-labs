# Objective Contract Template

Use this reference at the start of an `isomer-rsch-idea-v2` pass whenever the real target might differ from the easiest available surrogate. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Name the real target**. Create <OBJECTIVE_CONTRACT> with the primary objective, scoreboard metric, trusted proxy metrics, false-progress signals, hard constraints, contribution frame, and exit rule.
2. **Separate proxies from progress**. State which intermediate metrics may guide thinking and which apparent improvements must not count as route health.
3. **Check constraint validity**. Mark leakage, unavailable features, deployment constraints, comparability rules, and scope limits that invalidate a route even if a proxy improves.
4. **Gate frontier widening**. Do not move into candidate generation until the contract can distinguish true progress, false progress, and invalid routes.

## Preferences

- Prefer the real target over the easiest measurable surrogate (if the scoreboard metric is ambiguous, otherwise use the accepted metric contract).
- Prefer explicit false-progress signals over broad warnings (if the current evidence names known misleading metrics, otherwise name the likely misleading proxies).
- Prefer keeping the accepted dataset, metric, and evaluation contract fixed (if scope changed, otherwise record the scope change before ideation).

## Constraints

- <OBJECTIVE_CONTRACT> must name the primary objective, scoreboard metric, trusted proxies, false-progress signals, hard constraints, contribution frame, and exit rule.
- The idea pass must not widen the frontier while the true target and invalid routes are unclear.
- Candidate routes must not depend on submit-time unavailable features, leakage-prone labels, or post-hoc ranking information.
- Implementation convenience must not outrank target alignment.

## Quality Gates

- Target clarity: <OBJECTIVE_CONTRACT> lets a later agent tell whether a candidate improves the real target or only a proxy.
- Constraint clarity: every hard constraint is testable enough to reject an invalid route.
- False-progress clarity: the contract names at least one concrete misleading signal when the source context exposes one.
- Exit readiness: the contract is explicit enough to support <CURRENT_BOARD_PACKET> and <CANDIDATE_IDEA_FRONTIER> without guessing.
