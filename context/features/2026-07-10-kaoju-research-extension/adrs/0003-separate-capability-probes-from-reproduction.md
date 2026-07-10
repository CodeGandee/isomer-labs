# Separate Capability Probes from Reproduction

Status: accepted

Kaoju shall support both intended-data runs and lightweight generated-data trials for a paper method. A generated-data trial is a `capability-probe` whose numbers describe only the declared synthetic setup; it cannot receive reproduction depth, support a paper benchmark verdict, or be compared directly with the paper's reported values.

## Considered Options

- Disallow generated-data runs and require the intended dataset for every method trial. This was rejected because large, restricted, or costly datasets would prevent useful low-cost inspection of an implementation's execution path and outputs.
- Treat generated-data runs as adapted reproductions. This was rejected because synthetic inputs may omit the semantics, distribution, scale, labels, and evaluator assumptions that give the reported result its meaning.

## Consequences

- Every first-hand method trial records `run_purpose` and input basis separately from execution fidelity and evidence verdict.
- A capability probe uses a versioned Generated Dataset Artifact that preserves generator source, schema, size, seeds, assumptions, validation checks, and known limitations.
- Capability-probe Runs stop at verification depth `executed`. Their outputs may support claims about execution behavior, output shape, invariants, failures, and measured resource use under the probe conditions, but not benchmark quality or real-data generalization.
- If the intended dataset is unavailable or exceeds the resource envelope, Kaoju preserves that blocked route and offers a capability probe explicitly rather than silently substituting data.
- Every reported number links to its Run and conditions; paper-reported values and capability-probe values remain visibly separate.
