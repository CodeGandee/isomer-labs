# Baseline Gate Checklist Template

Use this reference as a compact acceptance-boundary checklist when it helps. It is optional; the hard requirement is a durable and unambiguous accepted, blocked, waived, or route-changed state. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Record identity and frontier**. State baseline id, route, acceptance target, primary comparator, next step, active uncertainty, and next route if the gate clears.
2. **Apply the core gate**. Check comparator provenance, dataset, split, evaluation path, required metrics, metric directions, output pointers, smoke or direct verification rationale, and <COMPARABILITY_CONTRACT>.
3. **Apply the blocked boundary**. If blocked, record failure class, tried steps, evidence sources, and next best move.
4. **Close out**. Summarize the baseline and name the next route after acceptance, waiver, blocker, or route change.

## Preferences

- Prefer a checklist only when it clarifies acceptance (if the route is already obvious and recorded, otherwise keep it compact).
- Prefer active uncertainty as a concrete question (if there is no uncertainty, otherwise proceed to closeout).
- Prefer blocker classes that guide next action (if blocked, otherwise do not leave vague failure language).

## Constraints

- <BASELINE_GATE_CHECKLIST> must not replace verification evidence.
- Acceptance cannot be checked complete without <COMPARABILITY_CONTRACT> and <BASELINE_VERIFICATION_EVIDENCE>.
- Blocked closeout must state tried steps, evidence sources, failure class, and next best move.
- Closeout must name the next route explicitly.

## Quality Gates

- Identity gate: baseline id, route, acceptance target, and comparator are explicit.
- Frontier gate: next step, active uncertainty, and next route are visible.
- Core gate: comparator provenance, data, evaluation, metrics, output pointers, and contract are checked.
- Blocker gate: failure class, evidence, and next best move are recorded.
- Closeout gate: concise summary and next route exist.

## Template

### Identity

- baseline id:
- route:
- acceptance target:
- primary comparator:

### Current Frontier

- [ ] next execution, verification, acceptance, blocker, or route-switch step is explicit
- [ ] active uncertainty is written as a concrete question
- [ ] next route is known if this gate clears

### Core Gate

- [ ] comparator identity and provenance are explicit
- [ ] dataset, split, evaluation path, required metrics, and metric directions are explicit enough to judge comparability
- [ ] trusted outputs or metrics are traceable to concrete files, logs, service responses, source records, or accepted package records
- [ ] smoke was used, skipped, or replaced by direct verification for an explicit reason when that choice matters
- [ ] expected result files or trusted-output pointers have been checked
- [ ] <COMPARABILITY_CONTRACT> exists or will be produced before acceptance
- [ ] baseline is accepted, blocked, waived, or route-changed with a durable note

### Blocked Boundary

- [ ] if blocked, the failure class is explicit
- [ ] if blocked, tried steps and evidence sources are recorded
- [ ] if blocked, next best move is attach, import, retry, repair, reset, waive, or ask the user

### Closeout

- [ ] concise baseline summary written
- [ ] next route named explicitly
