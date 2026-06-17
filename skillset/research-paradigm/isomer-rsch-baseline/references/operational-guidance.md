# Operational Guidance

Use this reference when the baseline route needs longer operational notes than the main control surface.

## Durable Route Records

Durable records are required in substance, not in fixed filenames. The shortest useful record is acceptable when it lets a later turn resume without guessing.

For non-trivial, code-touching, expensive, unstable, or long-running baseline work, leave a route record with chosen route, acceptance target, comparator identity, source identity, execution or evaluation surface, expected outputs, acceptance condition, current blocker or fallback, and verification verdict.

Use `references/route-record-template.md` and `references/gate-checklist.md` when they help, but do not expand them as paperwork.

## Execution Tactics

Use the route that is most faithful, observable, and efficient while preserving the hard Gates.

- If source reproduction or repair is active, read the source document and source package before substantial setup.
- For attach, import, or verify-local-existing, inspect only the minimum evidence needed to trust the provided or local comparator.
- A bounded smoke test is helpful only when command path, environment viability, evaluator wiring, or output schema is unclear.
- If the path is already concrete, go straight to real verification or the real run.
- Do not repeat an unchanged check without new evidence, code changes, environment changes, or a route change.
- If runtime is uncertain or likely long, prefer an Execution Adapter that records a Run and supports monitoring.
- If a run is invalid, wedged, or superseded, stop it cleanly and relaunch only after the route change is recorded.

## Environment Tactics

For code baselines, prefer a reproducible isolated environment, but choose the route that is most faithful to the source package and most likely to produce comparable evidence.

Source-specific package managers, scripts, containers, service startup commands, and local execution tools are Execution Adapter choices. Record only environment facts that affect trust or comparability, and do not force a generic setup route when it would make the baseline less faithful.

Cost, credential, privacy, data export, and long-running compute choices may require an Operator Agent Gate under `[[tbd-surface:policy-cost-privacy-gate]]`.

## Reuse and Durable Context

Reuse or package a baseline only after verification is complete and the current Research Task no longer depends on guesswork about provenance or comparability.

Write durable Findings only to avoid repeating known failures or to preserve reusable baseline lessons. Record route rationale, setup failures, source-to-code mismatch notes, and accepted caveats that later stages must carry forward.

## Blocked Classes

Use explicit classes when blocked:

- `missing-source`
- `missing-metric-contract`
- `environment-infeasible`
- `execution-surface-unknown`
- `run-failed`
- `verification-failed`
- `weak-provenance`
- `non-comparable-protocol`

A blocked result must state what failed, what was tried, which evidence shows the issue, and whether the next best move is attach, import, retry, repair, reset, waive, ask the Operator Agent, or route through decision.
