# Optimize Checklist Template

Use this reference to keep the pass-level frontier and next action explicit. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Refresh the frontier**. Confirm <OPTIMIZATION_FRONTIER>, recent lessons, current line, candidates, failures, and active route.
2. **Select route and submode**. Mark explore, exploit, fusion, debug, or stop, and primary submode: brief, rank, seed, loop, fusion, debug, or stop.
3. **Track candidate slate quality**. Check mechanism-family diversity, change-layer diversity, candidate ranking, promotion cap, and candidate board status.
4. **Track implementation pool**. Record smoke queue, full-eval queue, failure classification, stagnation, family-shift trigger, and fusion eligibility.
5. **Write next action**. Keep exactly one concrete next action, blocker, or stop condition.

## Preferences

- Prefer a checklist that changes as the frontier changes (if it stops changing, otherwise revise the node contract or route).
- Prefer one active bottom-layer move (if several are active, otherwise state isolation and reason).
- Prefer explicit next action over broad "continue optimization" language.

## Constraints

- <OPTIMIZE_CHECKLIST> must not list candidate creation as completion by itself.
- Checklist state must distinguish candidate briefs from implementation attempts.
- Stagnation and family-shift checks must not be skipped after repeated non-improvement.
- Completion must leave a durable next action or stop condition.

## Quality Gates

### Metrics

- Checklist completion: fraction of optimize pass checklist items satisfied or explicitly waived with a route reason; higher is better.
- Mechanism-family count: number of mechanism families represented in the current brief slate; higher is better until the slate is not one-family narrow.

### Checks

- Frontier gate: current frontier and lessons are checked.
- Submode gate: route and primary submode are explicit.
- Slate gate: candidate diversity, ranking, and promotion status are visible.
- Execution gate: smoke, full-eval, failure, plateau, and fusion state are tracked when relevant.
- Closeout gate: one next action or stop condition is written.

## Template

- [ ] Frontier summary refreshed
- [ ] Primary optimize submode selected
- [ ] Frontier route selected: explore / exploit / fusion / debug / stop
- [ ] Recent lessons checked when relevant
- [ ] Brief slate covers more than one mechanism family or explains why not
- [ ] Candidate briefs updated or confirmed
- [ ] Candidate ranking updated
- [ ] Promotion cap applied
- [ ] Candidate board updated
- [ ] Smoke queue defined when needed
- [ ] Full-eval queue defined when needed
- [ ] Failures classified and debugged or archived
- [ ] Stagnation check performed
- [ ] Family-shift trigger checked
- [ ] Fusion eligibility checked
- [ ] Next concrete action written
