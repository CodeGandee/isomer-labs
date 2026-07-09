---
name: isomer-misc-bounded-run-tips
description: Use when an Isomer Labs agent must run resource-heavy work safely, choose bounded execution settings, avoid host crashes, size CUDA compile jobs, limit nvcc architectures, or balance system resource utilization against environment verification needs.
---

# Isomer Misc Bounded Run Tips

## Overview

- **Purpose**: classify operation resource risk and, when needed, turn risky work into bounded real-path execution.
- **Ownership**: this skill owns the user-tunable definition of operation resource risk for Isomer skills.
- **Consumers**: core env setup and team specialization skills consume this classification evidence and should not override it with their own fixed heavy-operation list.

## When to Use

Use this skill before planning resource checks for setup, verification, benchmark, compile, inference, dataset, test, download, archive, or similar operations.

Examples such as CUDA builds, model inference, broad tests, downloads, and benchmarks are guidance, not an exhaustive list. Users may edit this skill to match their host, project, and risk tolerance.

Do not use this skill to justify replacing a required critical path with an unrelated smoke test. A bounded run must still exercise the relevant code path; otherwise report a blocker or ask the user for permission to downgrade the check.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Classify the operation**:
   - Input: task or command, cwd when known, expected result, purpose, and relevant context.
   - Output one `classification_result`: `light`, `heavy`, `unknown-risk`, or `not-applicable`.
   - Record `classification_reason` and `resource_dimensions`, such as CPU, RAM, disk, network, GPU, wall time, or external service pressure.
2. **Decide the follow-up**:
   - `light`: no resource check plan is required; record why.
   - `not-applicable`: route to the relevant non-runtime policy; record why.
   - `heavy` or `unknown-risk`: continue to bounded execution planning.
3. **Select a bounded-run recipe**:
   - Use `cuda-compile` for `nvcc`, CUDA extension builds, CUDA architecture flags, and CUDA build parallelism.
   - If no recipe matches, use generic best-effort bounded guidance and record that limitation.
4. **Probe resources before running**:
   - Prefer lightweight read-only probes: `free -h`, `/proc/meminfo`, `df -h`, `nproc`, `uptime`, and `nvidia-smi`.
5. **Choose a bounded real-path command**:
   - Reduce breadth, not meaning: fewer workers, selected targets, smaller inputs, shorter benchmarks, selected tests, or sample data.
   - Keep the command on the critical path that the task or gate needs to prove.
   - For profiler, tracer, debugger, memory-checker, and similar wrapper tools that execute a target command as a subprocess, keep Pixi outside the wrapper: use `pixi run <wrapper-tool> <tool-options> <target-command> <target-args>` or the explicit manifest equivalent, not `<wrapper-tool> pixi run ...`, unless local evidence proves that Pixi itself is the intended target process.
6. **Run, observe, and adjust**:
   - Start with conservative limits.
   - Increase parallelism only when resource headroom remains clear.
   - Stop and report a blocker if even the bounded real path is unsafe.
7. **Report evidence**:
   - Include classification, probes, limits, command, expected result, actual result, and limitation.

If the user's task does not map cleanly to these steps, use your native planning tool to build a bounded execution plan from the requested command, available resources, and expected result, then execute only the safe portion.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `cuda-compile` | Bound `nvcc` and CUDA extension compilation by host GPU architecture and RAM-aware worker count | [references/cuda-compile.md](references/cuda-compile.md) |

## Bounded Run Principle

Bounded does not mean superficial. A bounded run is valid when it still exercises the important implementation path with smaller scope or lower parallelism. For example, compiling one CUDA extension for the host GPU architecture with one worker is bounded; replacing compilation with `python -c "import torch"` is only a smoke test.

For tools that wrap and launch another command, such as `ncu`, `nsys`, `valgrind`, `gdb`, `cuda-gdb`, profilers, tracers, debuggers, and memory checkers, the bounded command must preserve the Pixi-first shape. Use `pixi run ncu ... python bench.py`, `pixi run valgrind ... python script.py`, or `pixi run gdb --args python script.py`. Do not use `ncu pixi run ...`, `valgrind pixi run ...`, or `gdb --args pixi run ...` unless Pixi itself is deliberately the command being profiled or debugged.

## Reporting Contract

Default to **Essential Output** in chat. Print **Complete Output** only when the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output.

### Essential Output

Report:

- `classification_result`: `light`, `heavy`, `unknown-risk`, or `not-applicable`.
- `classification_reason`: concise reason for the classification.
- `bounded_guidance_required`: yes or no.
- `bounded_command`: exact command to run when bounded guidance is required.
- `result`: ready, failed, blocked, or not checked.
- `blocker`: exact blocker and retry command when unsafe.

### Complete Output

When requested, include:

- `classification_source`: `isomer-misc-bounded-run-tips`.
- `classification_result`
- `classification_reason`
- `resource_dimensions`: CPU, RAM, disk, network, GPU, wall time, external service pressure, or `none`.
- `bounded_guidance_required`
- `operation`: command or task being classified or bounded.
- `cwd`: working directory when known.
- `expected_result`: what proves the real path works.
- `bounded_guidance_source`: matching subcommand, generic best-effort, or not needed.
- `resource_probe`: memory, CPU, disk, GPU, and active process evidence used when bounded guidance is required.
- `bounded_limits`: worker count, architecture list, input size, test selection, or benchmark duration.
- `bounded_command`
- `result`
- `blocker`

## Common Mistakes

- Treating a generic smoke test as proof of a critical compile, inference, dataset, or benchmark path.
- Running default build parallelism without checking memory.
- Compiling CUDA kernels for broad architecture lists when the task is local to the current host.
- Saturating all RAM, CPU, disk, or GPU capacity just to prove environment readiness.
- Hiding skipped heavy work behind `ready` instead of reporting a blocker and the bounded command to retry.
- Inverting Pixi and a wrapper tool by writing `<wrapper-tool> pixi run ...` for profiler, debugger, tracer, or memory-checker work; the usual bounded command shape is `pixi run <wrapper-tool> ... <target-command>`.
