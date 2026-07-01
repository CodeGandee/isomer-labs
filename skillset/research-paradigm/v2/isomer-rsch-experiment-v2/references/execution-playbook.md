# Execution Playbook

Use this reference to execute one bounded run while preserving evidence. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Preflight the route**. Confirm dataset path or source, version, split contract, comparator metrics, selected hypothesis, code-level plan, output names, and whether prior incidents or repeated failure patterns affect this run.
2. **Confirm the workspace**. Use the active workspace for the selected route, keep the comparator reference read-only, and do not create a fresh branch or run surface unless recovery or debugging truly requires it.
3. **Implement the minimum change**. Apply the smallest hypothesis-bound code or config change, record touched files in <IMPLEMENTATION_CHANGE_MAP>, preserve theory fidelity, and avoid unrelated cleanup.
4. **Use smoke or pilot work only for uncertainty**. Run <SMOKE_CHECK_RECORD> when command paths, outputs, evaluator wiring, or risky logic need verification; keep smoke work bounded and do not treat it as main evidence.
5. **Launch the real run**. Use the intended dataset and split, run the full agreed evaluation, keep logs durable, and preserve commands, configs, outputs, seeds, metric files, and environment facts in <MAIN_RUN_RECORD>.
6. **Monitor long runs from durable signals**. For long-running work, use managed Execution Adapter sessions, structured comments or progress markers when available, durable log reads, and checkpoint updates only when the frontier, blocker, or expected next reply changes materially.
7. **Track last-known-good state**. Preserve the most recent executable, comparable, and explainable state; when a new attempt breaks that state, debug forward from that point before stacking speculative edits.
8. **Switch to diagnosis when brute force stops helping**. Enter diagnosis mode after repeated no-evidence retries, unexpected baseline gaps, suspiciously strong or identical metrics, unstable results, or conflicts between logs, checkpoints, and claims.
9. **Validate outputs before interpretation**. Check that outputs match the intended code and config, required metrics are present and finite, comparator relation is fair, failure mode or confounder is visible, and each claim maps to a metric and observed result.
10. **Record and route**. Produce <EXPERIMENT_RESULT_SUMMARY>, <CLAIM_VALIDATION_RECORD>, and <EXPERIMENT_ROUTE_DECISION> or <EXPERIMENT_BLOCKER_RECORD>; do not launch the next large run before interpreting this result.

## Preferences

- Prefer non-interactive, auditable commands with durable logs (if a command must be interactive, otherwise wrap it through a reproducible adapter path).
- Prefer one clean experiment at a time (if parallel execution is justified, otherwise isolate each run and record why).
- Prefer a small discriminative diagnostic over another full retry when the cause is unclear (if the path is already understood, otherwise continue the planned run).
- Prefer changing only one major variable per retry (if recovery requires a broader change, otherwise record which layer changed).
- Prefer updating <EXPERIMENT_PLAN> and <EXPERIMENT_CHECKLIST> as evidence arrives (if the run is lightweight, otherwise keep a compact rolling log).

## Constraints

- Shell, CLI, Python, package, Git, scheduler, and environment work should go through an Execution Adapter Command Request or the approved source-compatible extension path until native bindings are finalized.
- The comparator reference must remain read-only.
- A real run must use the intended dataset, split, evaluator, metric keys, and comparison recipe unless a deviation is recorded.
- Smoke or pilot budget should stay at `0-2` for the current experiment pass unless a real code, command, environment, or evaluator change justifies another check.
- A retry must not repeat the same hypothesis, code path, command path, and evidence surface without a new reason.
- A run must not be reported complete until logs and output files both confirm completion.
- Invalid, wedged, or superseded long-running work should be stopped, recorded, fixed, and relaunched cleanly instead of being hidden.

## Quality Gates

### Metrics

- Required metric completeness: fraction of exact metric keys that decide success or failure and are present, finite, and comparable with the baseline contract; higher is better.
- Evidence-ladder progress: achieved position on the minimum -> solid -> maximum paper-facing evidence ladder; higher is better after comparability is preserved.

### Checks

- Preflight gate: dataset, split, comparator metrics, selected hypothesis, code plan, outputs, and prior incident risks are known.
- Implementation gate: <IMPLEMENTATION_CHANGE_MAP> names the changed files, intended mechanism, expected risk, and any guard or sanity check.
- Smoke gate: <SMOKE_CHECK_RECORD> states the uncertainty tested, result, and whether main execution is now justified.
- Execution gate: <MAIN_RUN_RECORD> preserves command, config, logs, outputs, seeds, metric files, environment facts, and last-known-good state.
- Diagnosis gate: repeated failures produce a named failure layer and a smallest discriminative next check.
- Validation gate: metrics are complete, finite, traceable, comparable, and mapped to claim verdicts.
- Routing gate: the next action follows from the measured result, not from optimism or inertia.
