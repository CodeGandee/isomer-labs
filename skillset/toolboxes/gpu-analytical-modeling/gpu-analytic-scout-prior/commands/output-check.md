# Output Check

Before scout output is accepted, check that each promising direction names the claim it might support and the source family needed to support it.

Look for these slots: current topic scope, kernel or workload target, expected model output, likely hardware components, evidence class, source gaps, and validation risk. Runtime, throughput, counter trend, saturated-component, and blocking-path claims need different evidence; do not collapse them into one "validated" bucket.

If the scout result uses simulator, emulator, synthetic, or derivation-only evidence, label that evidence class explicitly. If it mentions exact GPU internals, ask whether the source is local implementation, hardware documentation, profiler counter evidence, measurement, simulator structure, or literature.
