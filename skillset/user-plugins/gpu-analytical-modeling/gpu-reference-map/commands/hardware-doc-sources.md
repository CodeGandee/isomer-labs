# Hardware Documentation Sources

## Workflow

When hardware facts or architectural limits matter, execute the following steps in order.

1. **Prefer authoritative hardware documentation**. Use vendor architecture guides, tuning guides, programming guides, ISA references, profiler documentation, and official hardware queries for concrete limits.
2. **Match the hardware scope**. Check architecture generation, GPU family, exposed feature set, driver/toolchain assumptions, clock or mode assumptions, and whether the source applies to the target scope.
3. **Separate specification from achieved behavior**. Specs and docs can justify nominal limits, semantics, and architectural concepts, but measurements are needed for achieved runtime or observed bottlenecks.
4. **Keep units and conditions**. Preserve units, dimensions, clock assumptions, precision mode, cache or memory hierarchy terms, and documented validity conditions.
5. **Mark uncertainty**. If the documentation is absent, ambiguous, or not specific enough, mark the parameter as an assumption, calibration candidate, or blocker.

If the user's task does not map cleanly to these steps, use your native planning tool to build a hardware-documentation source plan from the needed hardware fact, target scope, available docs, and uncertainty boundary, then execute the plan.

## Can Justify

- Architectural components, nominal capacities, instruction semantics, memory hierarchy concepts, programming constraints, profiler metric definitions, and hardware-query results.

## Cannot Justify

- Observed full-kernel runtime, achieved throughput, active bottleneck, or target workload behavior without matching measurements or counters.
- Parameters for a different architecture generation or device scope unless the portability assumption is explicit.

## Preserve

- Document title or query source, version, architecture scope, units, precision or mode assumptions, clock assumptions, metric definitions, and applicability caveats.
