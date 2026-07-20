# Baseline Gate Checklist Template

Use this reference as a compact acceptance-boundary checklist when it helps. It is optional; the hard requirement is a durable and unambiguous accepted, blocked, waived, or route-changed state. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Record identity and frontier**. State baseline id, route, acceptance target, primary comparator, next step, active uncertainty, and next route if the gate clears.
2. **Apply the core gate**. Check comparator provenance, dataset, split, evaluation path, required metrics, metric directions, output pointers, smoke or direct verification rationale, and DEEPSCI:COMPARABILITY-CONTRACT.
3. **Apply the blocked boundary**. If blocked, record failure class, tried steps, evidence sources, and next best move.
4. **Close out**. Summarize the baseline and name the next route after acceptance, waiver, blocker, or route change.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer a checklist only when it clarifies acceptance (if the route is already obvious and recorded, otherwise keep it compact).
- Prefer active uncertainty as a concrete question (if there is no uncertainty, otherwise proceed to closeout).
- Prefer blocker classes that guide next action (if blocked, otherwise do not leave vague failure language).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- DEEPSCI:BASELINE-GATE-CHECKLIST must not replace verification evidence.
- Acceptance cannot be checked complete without DEEPSCI:COMPARABILITY-CONTRACT and DEEPSCI:BASELINE-VERIFICATION-EVIDENCE.
- Blocked closeout must state tried steps, evidence sources, failure class, and next best move.
- Closeout must name the next route explicitly.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Core checklist completion: fraction of identity, frontier, core gate, blocked-boundary, and closeout checklist items satisfied or explicitly marked not applicable; higher is better.
- Blocker-field coverage: fraction of blocked-state fields with failure class, tried steps, evidence sources, and next best move recorded when blocked; higher is better.

### Checks

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
- [ ] DEEPSCI:COMPARABILITY-CONTRACT exists or will be produced before acceptance
- [ ] baseline is accepted, blocked, waived, or route-changed with a durable note

### Blocked Boundary

- [ ] if blocked, the failure class is explicit
- [ ] if blocked, tried steps and evidence sources are recorded
- [ ] if blocked, next best move is attach, import, retry, repair, reset, waive, or ask the user

### Closeout

- [ ] concise baseline summary written
- [ ] next route named explicitly
