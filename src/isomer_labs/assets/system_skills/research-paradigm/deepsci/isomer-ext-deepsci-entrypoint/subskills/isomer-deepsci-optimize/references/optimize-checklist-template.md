# Optimize Checklist Template

Use this reference to keep the pass-level frontier and next action explicit. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Refresh the frontier**. Confirm DEEPSCI:OPTIMIZATION-FRONTIER, recent lessons, current line, candidates, failures, and active route.
2. **Select route and submode**. Mark explore, exploit, fusion, debug, or stop, and primary submode: brief, rank, seed, loop, fusion, debug, or stop.
3. **Track candidate slate quality**. Check mechanism-family diversity, change-layer diversity, candidate ranking, promotion cap, and candidate board status.
4. **Track implementation pool**. Record smoke queue, full-eval queue, failure classification, stagnation, family-shift trigger, and fusion eligibility.
5. **Write next action**. Keep exactly one concrete next action, blocker, or stop condition.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer a checklist that changes as the frontier changes (if it stops changing, otherwise revise the node contract or route).
- Prefer one active bottom-layer move (if several are active, otherwise state isolation and reason).
- Prefer explicit next action over broad "continue optimization" language.

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- DEEPSCI:OPTIMIZE-CHECKLIST must not list candidate creation as completion by itself.
- Checklist state must distinguish candidate briefs from implementation attempts.
- Stagnation and family-shift checks must not be skipped after repeated non-improvement.
- Completion must leave a durable next action or stop condition.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

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
