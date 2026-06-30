# Comparability Contract

Use this reference when deciding whether a baseline is truly usable downstream.

## Minimum Contract

Make these fields explicit before acceptance:

- comparator identity and baseline id
- route and acceptance target
- task identity
- dataset identity
- split contract
- evaluation path, evaluation procedure, or evaluation Capability Binding
- required metric ids for the current downstream comparison
- metric directions
- source paper, source repository, source package, local implementation, or reusable package identity as applicable
- trusted metric values or trusted-output pointers
- material environment or hardware facts that change interpretation
- known deviations from the source reference, paper protocol, local comparator, or selected target

A core contract is enough for `comparison-ready`. Expand it only when paper-facing claims, variant-heavy comparison, or reusable package work requires more coverage.

## Verdict Logic

Use one of these verdicts:

- `verified-match`: evidence matches the intended contract closely enough for the target.
- `verified-close`: evidence is near the intended contract and deviations are small, explicit, and acceptable for the target.
- `verified-diverged`: evidence is real but materially differs from the intended metric, data, split, evaluator, source, or environment.
- `trusted-with-caveats`: evidence can support downstream comparison only if caveats remain visible.
- `broken`: evidence cannot support honest comparison.

## Non-Comparable Changes

Do not mix a non-comparable run into the accepted comparison line. Treat changed datasets, split definitions, metric formulas, evaluation scripts, model variants, source commits, major environment constraints, or service behavior as deviations unless the change is explicitly the comparison target.

## Acceptance Boundary

The baseline is ready only when later experiment or writing work can cite the comparator without guessing task, data, split, metric ids, metric directions, source identity, evaluation path, provenance, or caveats.

If an accepted metric contract needs a concrete schema or file layout, treat it as a metric-contract Artifact and use semantic Artifact kind through Workspace Path Resolution or the accepted Evidence Item fields when metric evidence fields matter.
