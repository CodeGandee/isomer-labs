# Framing Prior

Before scout framing, classify what the topic may need: local topic records, kernel implementation details, hardware documentation, profiler counters, measurements, simulator structure, literature, or several of these.

Use local topic intent first when it defines scope, metric, accepted assumptions, previous decisions, scripts, or measured outputs. Use kernel sources for implementation behavior, generated code, launch configuration, compiler output, and disassembly; use hardware docs or hardware queries for nominal limits and architecture facts.

For model structure, require early candidates to name model inputs, outputs, hardware components, ordered execution stages, aggregation logic, assumptions, and validity limits. Treat AccelSim, GPGPU-Sim, and similar projects as structure references for architecture concepts and execution paths, not as target-hardware truth.

Do not let scout outputs harden claims without source boundaries. Mark missing facts as assumptions, calibration candidates, follow-up searches, or blockers.
