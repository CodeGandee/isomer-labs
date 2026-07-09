# Hardware-Grounded Interpretation

Interpret GPU model outputs through named hardware terms: component graph, execution stages, data movement path, aggregation rule, bottleneck selection rule, assumptions, and validity limits.

For each conclusion, distinguish runtime accuracy, counter trend, saturated component, and blocking path. A runtime fit can support latency scope only when predicted and measured latency, workload scope, hardware scope, metric definition, and evidence class are reported together.

If analysis uses simulator or emulator evidence, label it as proxy evidence. If it uses profiler labels, preserve raw counter names, normalization, collection context, mapping rationale, and unresolved gaps before deriving component claims.
