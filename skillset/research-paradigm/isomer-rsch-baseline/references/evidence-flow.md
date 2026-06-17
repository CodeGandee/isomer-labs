# Evidence Flow

Use this reference when the baseline route is clear but the exact evidence sequence is not. These are examples, not required paths.

## Attach Existing Reusable Baseline

Use when a trustworthy reusable package can support the current comparison contract.

1. Attach or reference the reusable Artifact package through the available host Artifact API.
2. Inspect the package identity, provenance, trusted outputs, caveats, and metric contract.
3. Run only the minimum extra verification needed for current trust.
4. Record or reuse a metric-contract Artifact.
5. Close the Gate with an acceptance Decision Record or record the missing evidence.

Good evidence ties the attached package to the comparator that later stages will actually use. Bad evidence attaches one package and then compares against a different local path without recording the route change.

## Import Provided Package or Bundle

Use when the user or Isomer Workspace already provides a prepared package, bundle, snapshot, or result set.

1. Materialize or reference the imported Artifact package.
2. Keep provenance durable through a Provenance Record or equivalent package metadata.
3. Inspect outputs, metrics, source identity, and caveats.
4. Record or reuse a metric-contract Artifact.
5. Accept, block, waive, or route-change through a Decision Record.

Do not accept an imported number before checking what task, split, evaluator, metric, and source it used.

## Verify Local-Existing Comparator

Use when a local implementation, local result set, or evaluation Capability Binding already exists.

1. Identify the comparator and evaluation surface.
2. Identify trusted outputs or the real evaluation procedure.
3. Verify metrics under the intended contract.
4. Record metric-contract and verification Evidence Items.
5. Close the Gate or record the blocker.

A local comparator can be more faithful than clean reproduction when it is already the target of downstream comparison and its contract is explicit.

## Reproduce from Source

Use when attach, import, or local verification cannot establish trust.

1. Read the source document and source package enough to identify the intended task, data, split, evaluator, metrics, and expected outputs.
2. Record the execution route as a Capability Binding through an Execution Adapter.
3. Run the minimum trustworthy reproduction or trusted-output inspection.
4. Record Run logs, outputs, metric extraction, deviations, and comparability verdict.
5. Accept, block, repair, or route-change through a Decision Record.

Do not turn setup progress into baseline acceptance. Acceptance needs real evidence and a metric contract.

## Repair Existing Baseline

Use when a known baseline route failed and the failure may be bounded.

1. Identify the broken point and failure class.
2. Make only fixes that preserve scope, metric meaning, permissions, and scientific interpretation, or record a route change.
3. Re-run or re-read evidence that could change the trust state.
4. Record the new evidence, remaining caveats, and Gate outcome.

Stop after repeated failure of the same class unless new evidence, code changes, environment changes, or a route change justifies another attempt.

## Reusable Package After Verification

Use only after the current Research Task already trusts the baseline. Package publication is a downstream packaging action, not a substitute for verification.

Record package identity, provenance, metric contract, caveats, and reusable evidence. If a concrete publication API is required, use `[[tbd-surface:api-artifact-record]]`.

## Waive or Block

Use waiver only when the Research Task must continue without a baseline and the reason is durable. Use blocker when the Gate cannot honestly clear or waive within current constraints.

A waiver or blocker Decision Record should state what failed or was skipped, what was tried, which evidence supports the decision, what risk remains, and whether the next best move is attach, import, retry, repair, reset, ask the Operator Agent, decision, idea, experiment, or write.
