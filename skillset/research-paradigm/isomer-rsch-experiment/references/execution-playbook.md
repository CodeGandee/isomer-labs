# Execution Playbook

Use this reference when the experiment route needs the full execution checklist rather than the short control surface in `SKILL.md`.

## Define the Run Contract

Before implementation or execution, state run id, experiment tier, research question, null hypothesis, alternative hypothesis, comparator id, metric targets, expected changed files or components, expected outputs, stop condition, compute or runtime budget, minimal experiment, abandonment condition, strongest alternative hypothesis, and exact metric keys that decide success or failure.

For substantial Runs, keep these seven fields updated: research question, research type, research objective, experimental setup, experimental results, experimental analysis, and experimental conclusions.

Treat the Run contract as a research-question contract. Before coding, be able to explain why this Run is the best current route, what observation would answer the question, what result would force downgrade or route change, and what confounder would make the Run non-comparable.

## Preflight Check

Confirm dataset, version, split, comparator metrics, selected route claim, code-level plan, prior incidents, output placeholders, and current Decision Record. Confirm required metric keys and primary metric before comparison work. Extra metrics may be supplementary, but missing required metrics are not acceptable.

If the Run is claim-carrying and superiority is likely to be claimed, define the significance or uncertainty plan before looking at the numbers.

## Diagnosis Mode Trigger

Switch from ordinary execution to diagnosis mode when two retries add no evidence, baseline gap is much larger than expected, metrics are suspiciously strong or identical, outputs conflict with claimed behavior, or instability prevents interpretation.

In diagnosis mode, stop brute-force retrying, run the smallest discriminative test, resolve obvious environment or data-contract issues, and make the diagnosis goal explicit.

## Implement the Minimum Change

Keep the change hypothesis-bound, prefer small explainable edits, avoid unrelated cleanup, record which files matter, preserve theory fidelity, and add checks when the mechanism risks invalid numeric behavior.

Change only one major variable per retry unless the current state is non-executable. If broader recovery is unavoidable, record which layer changed: data, preprocessing, model, objective, optimization, evaluation, or environment.

## Smoke and Pilot Discipline

Use a bounded smoke or pilot only when it resolves real uncertainty about command path, output schema, evaluator wiring, or environment assumptions. Treat smoke work as a limited budget, not as a mandatory separate phase.

If the stage goal is a real experiment, continue to the evidence-bearing Run once the path is verified unless the Run is blocked and recorded.

## Execute and Monitor

Run through a Capability Binding and Execution Adapter. Use non-interactive execution when possible, keep logs durable, report progress for long Runs when state materially changes, avoid silent metric-definition changes, and run the full agreed evaluation rather than only a smoke test.

For long-running Runs, prefer an initial bounded smoke when paths are unverified, then monitor through durable logs and Signal Observations. Use `[[tbd-surface:api-execution-command]]` for the concrete command surface and `[[tbd-surface:path-run-logs]]` for the concrete log layout until those surfaces are accepted.

## Long-Running Monitoring Cadence

When a Run may take longer than a few minutes, record a Completion Watcher Contract or equivalent monitoring note with expected signal, next check, stall condition, and stop condition. A practical default cadence is to check after about one minute, then two minutes, five minutes, ten minutes, thirty minutes, and then about every thirty minutes while the Run is active. After each check, inspect durable logs before reporting progress, and report only when user-visible state, blocker status, evidence, or expected next check materially changes.

## Incremental Recording

Update durable notes after contract definition, important code changes, pilot validation, full execution checkpoints, post-run analysis, and closeout. Preserve failed attempts, anomalies, and partial outcomes rather than overwriting them.

Track the last state that was executable, comparable, and explainable. If a new attempt breaks it, debug forward from that last-known-good state.

## Validate Outputs

After the Run, verify outputs correspond to intended code and config, metrics are complete and interpretable, comparator comparison is fair, caveats are visible, required metric keys are present and finite, and the result maps back to the Research Claim.

Create a claim-validation record with claim, metric key, expected direction, observed result, and verdict: supported, refuted, or inconclusive.

## Record the Run

Every meaningful Run should produce a durable Run record with setup, execution, results, conclusion, comparator reference, metric rows, metric contract used, verdict, evidence paths, changed files or components, evaluation summary, and next route.

The evaluation summary should include takeaway, claim update, comparator relation, comparability, failure mode, and next action.

## Decide the Next Move

End with one of: continue current line, branch a new line, launch analysis, move to writing, reset, stop, or blocker. If analysis is selected, record why the expected information gain justifies added compute, time, or annotation budget.
