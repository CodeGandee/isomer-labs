## Why

Agents sometimes invert Pixi and subprocess-launching tools, producing commands such as `ncu pixi run ...`. That shape lets the wrapper tool launch Pixi instead of the intended target command, which can interfere with environment setup, library paths, argument parsing, signals, and profiler or debugger behavior.

## What Changes

- Add a generic Pixi command-shape rule for profiling, debugging, tracing, memory-checking, and similar wrapper tools that execute a target command as a subprocess.
- Require Topic Workspace setup and verification guidance to author and accept `pixi run <wrapper-tool> ... <target-command>` rather than `<wrapper-tool> pixi run ...`.
- Add bounded-run guidance so resource planning preserves the same wrapper-command ordering for profilers, debuggers, and tracing tools.
- Add NVIDIA-specific reinforcement for `ncu`, `nsys`, and `cuda-gdb` in the NVIDIA tools skill.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `isomer-service-env-setup-skill`: Topic environment setup and verification must document and enforce the Pixi wrapper-tool command-shape rule when deriving or running setup and verification commands.
- `isomer-bounded-run-tips-skill`: Bounded execution planning must preserve the Pixi wrapper-tool command-shape rule for profiler, debugger, tracer, and memory-checker commands.

## Impact

- Packaged system skills under `src/isomer_labs/assets/system_skills/`.
- Skill validation tests that assert key guidance exists in packaged skills.
- No CLI API, manifest schema, runtime schema, or package dependency changes.
