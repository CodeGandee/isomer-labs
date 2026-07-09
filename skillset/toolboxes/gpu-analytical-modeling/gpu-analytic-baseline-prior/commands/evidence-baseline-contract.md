# Evidence Baseline Contract

Before accepting a baseline, name whether each item is the proposed analytical model, a roofline baseline, simulator, emulator, microbenchmark, measurement harness, profiler-counter route, or writing aid.

Keep calibration, validation, and query inputs disjoint unless the deviation is explicit. Use shared input shapes, shared hardware assumptions, stable metric definitions, and a declared measurement method.

Do not merge analytical derivation, emulator ground truth, simulator traces, microbenchmarks, NCU counters, and real hardware timings into one validation claim. Treat roofline, compute-vs-memory labels, simulator output, and emulator output as insufficient for exact saturated-component or blocking-path claims unless component/path equations and matching evidence are also present.

Record caveats for stale, coarse, weak, or incomparable baselines before downstream use.
