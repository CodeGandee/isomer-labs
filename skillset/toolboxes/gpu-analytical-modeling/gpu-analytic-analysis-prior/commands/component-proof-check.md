# Component Proof Check

Before analysis output is accepted, check whether every saturated-component or blocking-path claim names the predicted component set, the selection rule, the intended stressor or regime, the observed evidence, and the match or miss interpretation.

Good evidence can include raw counters, conservative counter mappings, instruction mix, pipeline activity, dependency-path evidence, microbenchmarks, measured timings, or an explicit evidence gap. Coarse compute-bound or memory-bound labels are only coarse support.

When predictions and evidence disagree, check the harness first, then counter mapping, model structure, missing hardware nodes, hidden overlap, cache reuse, scheduler effects, unsupported regimes, invalid calibration bounds, proxy transfer, and missing measured latency. Choose a route: refine, add evidence, limit the claim, park, block, or accept partial support.
