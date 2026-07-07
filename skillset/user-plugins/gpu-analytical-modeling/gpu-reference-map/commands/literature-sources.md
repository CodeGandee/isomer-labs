# Literature Sources

## Workflow

When prior papers or public modeling references matter, execute the following steps in order.

1. **Start with claim relevance**. Choose papers or reports because they inform the current model shape, parameterization, validation method, source boundary, or comparison baseline.
2. **Prefer strong provenance**. Use peer-reviewed papers, vendor-supported papers, technical reports with artifacts, and surveys before blogs, informal notes, or issue threads.
3. **Extract transferable structure**. Capture equations, decomposition choices, variables, assumptions, validation methods, benchmark scope, and failure modes that can inform the current analytical model.
4. **Check applicability**. State differences in hardware generation, kernel family, workload shape, precision, compiler/runtime stack, and measurement method before transferring a result.
5. **Avoid citation overreach**. A paper can justify prior art, model shape inspiration, or comparison method, but target parameters and target accuracy still need source, measurement, or explicit assumption boundaries.

If the user's task does not map cleanly to these steps, use your native planning tool to build a literature-source plan from the current model claim, source candidates, applicability gaps, and citation boundary, then execute the plan.

## Can Justify

- Prior analytical forms, decomposition strategies, parameter classes, validation methods, baseline choices, terminology, and known limitations.

## Cannot Justify

- Current target hardware parameters, measured latency, saturated component, or blocking path unless the paper's evidence directly matches the declared target scope.

## Preserve

- Citation, artifact availability, hardware scope, workload scope, equations or method reused, assumptions, validation method, metrics, applicability gaps, and what claim the source supports.
