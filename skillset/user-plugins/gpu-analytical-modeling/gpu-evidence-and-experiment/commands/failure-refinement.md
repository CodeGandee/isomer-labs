# Failure Refinement

## Workflow

When prediction and evidence disagree, execute the following steps in order.

1. **Classify the mismatch**. Choose the smallest class that explains the evidence.
2. **Check harness first** when results are impossible or surprising. Confirm command shape, kernel selection, measurement timing, warmup, device, and installed package.
3. **Check evidence mapping**. Confirm counter names, normalization, and component mapping before changing the model.
4. **Check model structure**. Look for missing hardware nodes, hidden overlap, cache reuse, scheduler effects, unsupported regimes, or invalid calibration bounds.
5. **Choose a route**. Refine, add evidence, limit the claim, park, block, or accept partial support.
6. **Record the decision**. Preserve the mismatch, likely cause, rejected causes, and next route for later stages.

If the user's task does not map cleanly to these steps, use your native planning tool to build a mismatch-refinement plan from the observed failure, evidence mapping, model structure, and decision routes, then execute the plan. If the mismatch cannot be explained with available evidence, say so and route to decision or blocker rather than smoothing it away.

## Mismatch Classes

- Harness issue.
- Counter mapping error.
- Missing hardware node.
- Hidden overlap or pipeline effect.
- Cache or locality effect.
- Scheduler or occupancy effect.
- Unsupported shape or precision regime.
- Invalid calibration parameter.
- Proxy evidence not transferring to real hardware.

## Common Mistakes

- Fitting a new coefficient before checking the harness.
- Treating a miss as embarrassing rather than as model-discovery evidence.
- Deleting a failed result from the narrative without recording the limitation.
