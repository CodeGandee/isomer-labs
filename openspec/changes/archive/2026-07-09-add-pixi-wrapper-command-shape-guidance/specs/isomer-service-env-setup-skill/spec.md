## ADDED Requirements

### Requirement: Pixi Wrapper Tool Command Shape
The service environment setup skill SHALL author and verify profiler, debugger, tracer, memory-checker, and similar wrapper-tool commands with Pixi wrapping the tool command rather than the tool wrapping Pixi.

#### Scenario: Derived gate uses Pixi to launch wrapper tool
- **WHEN** `derive-env-gate` writes a setup, profiling, debugging, tracing, memory-checking, or verification command for a tool that executes a target command as a subprocess
- **THEN** the command uses `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <wrapper-tool> <tool-options> <target-command> <target-args>`
- **AND** the command does not use `<wrapper-tool> pixi run ...` unless the derived gate records explicit local evidence that the target process must be Pixi itself

#### Scenario: Verification rejects inverted wrapper command
- **WHEN** `verify-env-gate` encounters a command shaped as `<wrapper-tool> pixi run ...` for a known or identified wrapper tool
- **THEN** the skill reports the command as blocked or repairs the target spec before execution
- **AND** it names the corrected command shape with Pixi launching the wrapper tool

#### Scenario: Common wrapper tools are named
- **WHEN** the skill documents command style for wrapper tools
- **THEN** it includes examples for tools such as `ncu`, `nsys`, `valgrind`, `gdb`, `cuda-gdb`, profilers, tracers, debuggers, and memory checkers
