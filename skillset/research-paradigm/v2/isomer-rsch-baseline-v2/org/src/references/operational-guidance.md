# Operational Guidance

Use this reference when the baseline route needs the longer operational notes rather than the main control surface.

## Durable route records

Durable records are required in substance, not in fixed filenames.
The agent may choose the shortest durable form that lets a later turn resume without guessing.

For non-trivial, code-touching, expensive, unstable, or long-running baseline work, leave a route record that states:

- chosen route and acceptance target
- comparator identity and source identity
- command or evaluation path if one exists
- expected outputs or trusted-output pointers
- acceptance condition
- current blocker or fallback
- verification verdict

`PLAN.md`, `CHECKLIST.md`, `setup.md`, `execution.md`, `verification.md`, `analysis_plan.md`, and `REPRO_CHECKLIST.md` are allowed compatibility surfaces, not mandatory success paths.
Use `references/baseline-plan-template.md` and `references/baseline-checklist-template.md` when they help, but do not expand them as paperwork.

`attachment.yaml` or equivalent provenance is required for attached or imported baselines.
`<baseline_root>/json/metric_contract.json` as the canonical accepted comparison contract is required for accepted baselines.

## Execution tactics

Use whatever route is most faithful, observable, and efficient while preserving the hard gates.

- If source reproduction or repair is actually the active route, read the source paper and source repo before substantial setup.
- For attach, import, or verify-local-existing, inspect only the minimum evidence needed to trust the provided or local comparator.
- A bounded smoke test is usually helpful only when command path, environment viability, evaluator wiring, or output schema is still unclear.
- If the path is already concrete, go straight to real verification or the real run.
- Treat smoke or pilot work as a `0-2` default budget, but the real rule is not to repeat an unchanged check without new evidence, a code/environment change, or a route change.
- If runtime is uncertain or likely long, prefer `bash_exec(mode='detach', ...)` plus managed monitoring instead of pretending a short foreground timeout is enough.
- If a run is clearly invalid, wedged, or superseded, stop it cleanly and relaunch with the new route rather than stacking more retries.

## Environment tactics

For Python baselines, prefer a reproducible isolated environment, but choose the route that is most faithful to the source package and most likely to produce comparable evidence.

`uv` is a useful default tactic when the repo does not require a stronger native route.
Examples include `uv sync`, `uv venv`, `uv pip install ...`, and `uv run ...`.
Switch to repo-native conda, docker, poetry, shell scripts, service startup, or another local environment route when that is clearly more trustworthy, required by the source, or necessary to match the paper or package behavior.

Record only environment facts that affect trust or comparability.
Do not force a global `uv` route when it would make the reproduced baseline less faithful.

## Reuse and memory

Reuse or publish a baseline only after verification is complete and the current quest no longer depends on guesswork about provenance or comparability.
Do not publish a baseline for reuse if verification is incomplete, metrics are untrusted, or provenance is still weak.

Use memory only to avoid repeating known failures or to preserve reusable baseline lessons, not as a required step before every validation pass.
Write quest memory for route rationale, setup failures, paper-to-code mismatch notes, and accepted caveats that later stages must carry forward.
Promote to global memory only when another quest is likely to benefit from the lesson.
