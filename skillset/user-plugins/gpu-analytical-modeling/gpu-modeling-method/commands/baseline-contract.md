# Baseline Contract

## Workflow

When comparing GPU models or accepting baselines, execute the following steps in order.

1. **Name the comparison role**. Decide whether each item is the proposed analytical model, a baseline, a simulator, an emulator, a microbenchmark, a measurement harness, or a writing aid.
2. **Separate evidence classes**. Do not merge analytical derivation, emulator ground truth, simulator traces, microbenchmarks, NCU counters, and real hardware timings into one undifferentiated validation claim.
3. **Define fair comparison**. Use disjoint calibration and validation sets, shared input shapes, shared hardware assumptions, and stable metric definitions.
4. **Protect measured accuracy claims**. Reserve real-hardware accuracy language for measured kernel runs on the target hardware or an explicitly accepted hardware measurement proxy.
5. **Record caveats**. If a comparator is weak, stale, coarse, or incomparable, record the caveat before downstream use.

If the user's task does not map cleanly to these steps, use your native planning tool to build a baseline-classification plan from the available comparators, evidence classes, and claim scope, then execute the plan. If fair comparison cannot be established, route to baseline repair, decision, or a blocker according to the owning DeepSci workflow.

## Evidence Classes

- Analytical derivation: equations and source-backed terms.
- Roofline baseline: coarse upper-bound or bottleneck comparator.
- Emulator: proxy system that may share model structure with the predictor.
- Simulator: architecture model or trace-driven execution model.
- Microbenchmark: isolated hardware behavior measurement.
- NCU counter evidence: profiler counters and derived component labels.
- Real hardware timing: measured kernel runtime on the target or declared hardware.

## Common Mistakes

- Calling emulator agreement "real hardware error."
- Treating NCU's coarse compute or memory label as enough for component-level claims.
- Comparing models calibrated on different data without saying so.
