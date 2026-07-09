# Review of Skill Generality

## Summary

The GPU analytical modeling Toolbox is organized as stage-specific priors for generic GPU kernel analytical modeling. It avoids binding the reusable guidance to a specific topic workspace, kernel, GPU SKU, host, paper venue, or artifact path.

The strongest coverage remains hardware-grounded model shape, interpretable physical parameters, source/evidence boundaries, predicted-versus-measured latency gates, profiler-counter evidence, bottleneck observation checks, proxy-evidence downgrades, and final evidence visibility.

## Generality Assessment

The current stage-prior layout improves generality at the invocation boundary. Callback prompts now say which installed `gpu-analytic-{stage}-prior` skill and subcommand to invoke for a specific purpose, so broad source/model/evidence guidance no longer appears to apply uniformly at every insertion point.

The main operational specificity is still the Pixi/NCU posture inside `gpu-analytic-experiment-prior`. Pixi is acceptable Isomer project context, and NCU is a concrete profiler backend for NVIDIA GPU work, but the surrounding guidance frames it as profiler-counter evidence rather than as the only valid evidence route.

## Coverage Notes

- `gpu-analytic-scout-prior` frames source families, simulator-structure boundaries, model-shape needs, and evidence gaps before scout output hardens.
- `gpu-analytic-idea-prior` requires hardware components, physical parameters, equations, assumptions, and evidence targets before a model idea matures.
- `gpu-analytic-baseline-prior` separates analytical, roofline, simulator, emulator, microbenchmark, profiler-counter, and real-hardware timing evidence classes.
- `gpu-analytic-analysis-prior` keeps interpretations tied to hardware mechanisms, component/path observations, and mismatch routes.
- `gpu-analytic-experiment-prior` covers evaluation contracts, profiler-counter collection, NCU command posture, component stressors, result classification, and proxy-evidence boundaries.
- `gpu-analytic-review-prior`, `gpu-analytic-write-prior`, and `gpu-analytic-finalize-prior` gate claim strength, proof visibility, mathematical notation, closure posture, and final evidence class.

## Remaining Risks

- Measurement stability and uncertainty are still concise rather than exhaustive. Future guidance could add warmup policy, repeated-run distributions, variance/error bars, clock or thermal state, and outlier policy.
- Calibration quality is present through bounded physical parameters, but future guidance could add explicit sensitivity and identifiability checks.
- Publication wording should remain secondary to the more general language of report, closure record, or user-facing evidence artifact.
