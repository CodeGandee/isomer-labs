# Baseline Route Record Template

Use this reference when a durable route record would reduce ambiguity. It is a template, not a required filename. Keep it one-screen for fast attach, import, or local verification; expand only when the route is ambiguous, code-touching, expensive, broken, long-running, or reuse-facing. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **State the objective**. Record node objective, acceptance target, success condition, and user constraints that change comparability.
2. **State the baseline contract**. Record chosen route, baseline id, comparator identity, source identity, version, task, dataset, split, required metric ids, metric directions, and deviations.
3. **State execution choice**. Record working location, environment route, command, endpoint, trusted-output path, expected outputs, expected cost, smoke or direct-run decision, and why this path is sufficient.
4. **State acceptance boundary**. Record evidence required to accept, fastest failure signal, blocker condition, fallback, or route switch.
5. **State current frontier**. Record next action, active blocker, latest evidence, and next route when accepted, waived, blocked, or route-changed.

## Preferences

- Prefer one-screen route records for fast paths (if the route is complex, otherwise expand the sections that reduce ambiguity).
- Prefer explicit acceptance target and metric contract over process narration (if the route changes, otherwise revise before more work).
- Prefer frontier fields that make the next action obvious to a later turn (if blocked, otherwise name the blocker and fallback).

## Constraints

- <BASELINE_ROUTE_PLAN> must not turn route selection into unnecessary paperwork.
- <BASELINE_ROUTE_PLAN> must preserve comparator identity, metric contract, evidence required, and stop condition when the route is non-trivial.
- User constraints that change comparability must not be omitted.
- Material route changes should be reflected before more execution or verification work continues.

## Quality Gates

- Objective gate: acceptance target, success condition, and user constraints are explicit.
- Contract gate: route, comparator, source, task, dataset, split, metrics, and deviations are recorded.
- Execution gate: environment, command, endpoint, trusted-output path, expected outputs, and cost are visible.
- Acceptance gate: required evidence, fastest failure signal, blocker, fallback, and route switch are concrete.
- Frontier gate: next action and next route are recoverable.

## Template

### 1. Objective

- node objective:
- acceptance target:
- success condition:
- user constraints that change comparability:

### 2. Baseline Contract

- chosen route:
- baseline id:
- baseline variant:
- comparator identity:
- source paper, repository, package, service, or registry:
- source commit, version, or tag:
- task:
- dataset and split:
- required metric ids and directions:
- known deviations:

### 3. Execution Choice

- working location:
- environment route:
- command, endpoint, or trusted-output path:
- expected outputs:
- expected runtime or cost:
- smoke or direct-run decision:
- why this path is sufficient:

### 4. Acceptance Boundary

- evidence required to accept:
- fastest failure signal:
- blocker condition:
- fallback or route switch:

### 5. Current Frontier

- next action:
- active blocker:
- latest evidence:
- next route when accepted, waived, blocked, or route-changed:
