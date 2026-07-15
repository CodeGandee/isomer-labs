# Analysis Evidence Gate

Use this reference to check whether slice evidence is strong enough to update a claim or route. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Verify intended execution**. Confirm the slice used the intended data, code, metric, observable, comparison target, fixed conditions, and execution envelope.
2. **Classify the slice outcome**. Mark each slice as completed, partial, failed, blocked, infeasible, superseded, or read-only audit; keep non-success outcomes visible.
3. **Check comparability**. State exactly what changed, what stayed fixed, whether direct comparison still holds, and whether a non-comparable slice is generalization, stress test, boundary evidence, or failure analysis.
4. **Classify the claim update**. Label stable support, partial support, contradiction, unresolved ambiguity, strengthened, weakened, narrowed, abandoned, or still ambiguous as appropriate.
5. **Apply paper or review write-back gates**. For paper-ready or reviewer-facing slices, verify DEEPSCI:ANALYSIS-WRITEBACK-MAP points to the relevant outline, matrix, evidence ledger, section, claim, table, reviewer item, or rebuttal item.
6. **Choose the route**. Route to continue analysis, experiment, idea, write, decision, stop, reset, or blocker from the evidence boundary, not from the planned slice count.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer treating failed execution separately from negative evidence (if the slice did not produce valid evidence, otherwise do not interpret it as claim refutation).
- Prefer direct-comparison claims only when the comparison contract is preserved (if it differs, otherwise label the slice as non-comparable or boundary evidence).
- Prefer stopping after one decisive slice (if the parent boundary and next route are already clear, otherwise continue only with claim-critical slices).
- Prefer the top `3-5` decision-relevant findings in campaign summaries (if there are many slices, otherwise keep the summary concise).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- Campaign-level claims must not precede per-slice evidence.
- Null, negative, partial, failed, blocked, infeasible, superseded, and contradictory slices must not be hidden.
- Subjective or manual inspection must not support a claim without rubric, sample, prompt or inspection basis, trace, and caveat.
- A new dataset, split, metric, or protocol must not be presented as apples-to-apples comparison unless the contract says so.
- A writing-facing slice must not be called paper-ready while its write-back target remains stale or missing.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Intended-execution coverage: fraction of intended data, code, metric, observable, comparison target, fixed conditions, and execution envelope confirmed for the slice; higher is better.
- Write-back blocker count: number of paper-ready or reviewer-facing slices without a current write-back map or recorded blocker; lower is better.

### Checks

- Execution gate: the slice evidence corresponds to the intended data, code, metric, comparison target, and fixed conditions.
- Outcome gate: the slice status is explicit and non-success states are preserved.
- Comparability gate: direct, non-comparable, generalization, stress-test, boundary, or failure-analysis status is labeled.
- Claim gate: claim update and caveat are traceable to slice evidence.
- Write-back gate: paper or review slices have a current DEEPSCI:ANALYSIS-WRITEBACK-MAP or a recorded blocker.
- Route gate: next action follows from the updated evidence boundary.
