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
   - Classify the operation as `light`, `heavy`, `unknown-risk`, or `not-applicable`.
   - Explain the reason and the relevant resource dimensions, such as CPU, RAM, disk, network, GPU, wall time, or external service pressure.
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

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

### Essential Output

State whether the operation is light, heavy, of unknown risk, or outside this skill, and explain why. Say whether bounded guidance is required. When it is, provide the exact bounded command. Close with whether the operation is ready, failed, blocked, or not checked; name the blocker and retry command when execution is unsafe.

### Complete Output

Group the full explanation by operation, risk classification, resource evidence, bounded limits, command, and result. Include the working directory when known, the expected proof of success, relevant CPU, memory, disk, network, GPU, wall-time, or service pressure, and whether guidance came from a matching subcommand or a generic best-effort judgment.

## Common Mistakes

- Treating a generic smoke test as proof of a critical compile, inference, dataset, or benchmark path.
- Running default build parallelism without checking memory.
- Compiling CUDA kernels for broad architecture lists when the task is local to the current host.
- Saturating all RAM, CPU, disk, or GPU capacity just to prove environment readiness.
- Hiding skipped heavy work behind `ready` instead of reporting a blocker and the bounded command to retry.
- Inverting Pixi and a wrapper tool by writing `<wrapper-tool> pixi run ...` for profiler, debugger, tracer, or memory-checker work; the usual bounded command shape is `pixi run <wrapper-tool> ... <target-command>`.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
