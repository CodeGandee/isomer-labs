# Claim Gate

## Workflow

When reviewing GPU analytical-modeling claims, execute the following steps in order.

1. **List central claims**. Include runtime accuracy, counter trends, saturated component, blocking path, model generality, and implementation readiness.
2. **Assign evidence class**. Use supported, partially supported, unsupported, or deferred.
3. **Name evidence sources**. Cite the relevant derivation, source, real timing, profiler counter, microbenchmark, simulator, emulator, or limitation record.
4. **Show the evidence packet for supported central claims**. Include the relevant inputs, predictions, measured latency when latency is claimed, observed bottleneck evidence when component or path is claimed, mapping rationale, and match or mismatch interpretation.
5. **Downgrade overclaims**. Replace unsupported certainty with measured scope, proxy support, explicit limitation, or a route back to experiment.
6. **Preserve rejected strength**. If a claim was weakened, say why so later reviewers do not restore the stronger wording by accident.

If the user's task does not map cleanly to these steps, use your native planning tool to build a claim-gating plan from the available claims, evidence sources, and publication scope, then execute the plan. If evidence is too ambiguous to classify, route to analysis, review, decision, or finalization blocker.

## Claim Classes

- Supported: direct evidence supports the stated scope.
- Partially supported: evidence supports a narrower scope or proxy version.
- Unsupported: evidence contradicts or does not reach the claim.
- Deferred: plausible but intentionally left for future evidence.

## Common Mistakes

- Treating a model derivation as validation by itself.
- Dropping a failed result instead of classifying the claim.
- Mixing "measured", "simulated", and "estimated" in one sentence.
- Marking a central claim supported while only naming a conclusion and not showing the evidence that produced it.
