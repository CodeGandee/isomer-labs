## ADDED Requirements

### Requirement: Bounded Guidance Preserves Pixi Wrapper Tool Shape
The bounded-run tips misc skill SHALL preserve Pixi-first command ordering when producing bounded commands for wrapper tools that execute target commands as subprocesses.

#### Scenario: Bounded profiler command keeps wrapper inside Pixi
- **WHEN** bounded-run tips produces a bounded command for a profiler, tracer, debugger, memory checker, or similar wrapper tool
- **THEN** the bounded command uses `pixi run <wrapper-tool> ... <target-command>` or the explicit manifest equivalent
- **AND** it does not use `<wrapper-tool> pixi run ...` unless local evidence proves that Pixi itself is the intended target process

#### Scenario: Bounded guidance lists representative wrapper tools
- **WHEN** bounded-run tips documents common mistakes or generic bounded guidance
- **THEN** it names representative wrapper tools such as `ncu`, `nsys`, `valgrind`, `gdb`, and `cuda-gdb`
