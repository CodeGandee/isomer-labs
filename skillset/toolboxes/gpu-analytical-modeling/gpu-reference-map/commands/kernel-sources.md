# Kernel Sources

## Workflow

When kernel implementation details matter, execute the following steps in order.

1. **Find the owning implementation**. Prefer the real kernel repository, generated code, build configuration, launch harness, and input-shape contract over secondary summaries.
2. **Trace compile and launch facts**. Inspect compiler flags, generated variants, specialization choices, launch dimensions, precision modes, and runtime parameters that affect model inputs.
3. **Use instruction-level sources when needed**. Use PTX, SASS, disassembly, instruction mix, and dependency-path evidence when the model claim depends on execution path or component use.
4. **Separate implementation facts from hardware facts**. A kernel source can show what code asks the GPU to do, but hardware docs, counters, or measurements are needed for capacity, latency, or achieved behavior.
5. **Record version and scope**. Preserve repository revision, generated artifact version, compiler version, flags, kernel selector, input shape, precision, and launch configuration.

If the user's task does not map cleanly to these steps, use your native planning tool to build a kernel-source plan from the implementation source, launch path, compiler output, and model claim, then execute the plan.

## Can Justify

- Kernel algorithm, generated implementation path, launch configuration, input contract, precision path, instruction mix, and static dependency evidence.

## Cannot Justify

- Achieved runtime, saturated component, cache behavior, or memory-system bottleneck without matching measurement, profiler, or hardware evidence.
- General hardware limits beyond what the implementation explicitly queries or cites.

## Preserve

- Repository or generated-code revision, compiler toolchain, flags, launch parameters, kernel selector, input shape, precision, disassembly source, and any generation or specialization conditions.
