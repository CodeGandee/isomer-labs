---
name: isomer-misc-bounded-run-tips
description: Use when an Isomer Labs agent must run resource-heavy work safely, choose bounded execution settings, avoid host crashes, size CUDA compile jobs, limit nvcc architectures, or balance system resource utilization against environment verification needs.
---

# Isomer Misc Bounded Run Tips

## Overview

Use this skill to turn resource-heavy work into bounded real-path execution: run enough of the real code path to prove the environment or task, while keeping CPU, RAM, disk, network, and GPU load within safe host limits.

## When to Use

Use this skill when a task involves compilation, CUDA builds, native extensions, model inference, dataset processing, broad test suites, large downloads, archive extraction, benchmarks, or any operation that could overload the host.

Do not use this skill to justify replacing a required critical path with an unrelated smoke test. A bounded run must still exercise the relevant code path; otherwise report a blocker or ask the user for permission to downgrade the check.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Identify the heavy operation**:
   - Name the command, working directory, expected result, and why it is heavy.
   - Decide whether the goal is environment verification, local benchmarking, debugging, release artifact creation, or full production execution.
2. **Select the applicable subcommand** from **Subcommands**:
   - Use `cuda-compile` for `nvcc`, CUDA extension builds, CUDA architecture flags, and CUDA build parallelism.
3. **Probe resources before running**:
   - Check memory, CPU load, disk space, and GPU status when relevant.
   - Prefer lightweight read-only probes such as `free -h`, `/proc/meminfo`, `df -h`, `nproc`, `uptime`, and `nvidia-smi`.
4. **Choose a bounded real-path command**:
   - Reduce breadth, not meaning: fewer workers, selected targets, smaller inputs, shorter benchmarks, selected tests, or sample data.
   - Keep the command on the same critical path that the task or gate needs to prove.
5. **Run, observe, and adjust**:
   - Start with conservative limits.
   - Increase parallelism only when resource headroom remains clear during the first run.
   - Stop and report a blocker if even the bounded real path is unsafe.
6. **Report evidence**:
   - Include probes, chosen limits, command, expected result, actual result, and any remaining limitation.

If the user's task does not map cleanly to these steps, use your native planning tool to build a bounded execution plan from the requested command, available resources, and expected result, then execute only the safe portion.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `cuda-compile` | Bound `nvcc` and CUDA extension compilation by host GPU architecture and RAM-aware worker count | [references/cuda-compile.md](references/cuda-compile.md) |

## Bounded Run Principle

Bounded does not mean superficial. A bounded run is valid when it still exercises the important implementation path with smaller scope or lower parallelism. For example, compiling one CUDA extension for the host GPU architecture with one worker is bounded; replacing compilation with `python -c "import torch"` is only a smoke test.

## Reporting Contract

When applying this skill, report:

- `heavy_operation`: command or task being bounded.
- `resource_probe`: memory, CPU, disk, GPU, and active process evidence used.
- `bounded_limits`: worker count, architecture list, input size, test selection, or benchmark duration.
- `bounded_command`: exact command to run.
- `expected_result`: what proves the real path works.
- `result`: ready, failed, blocked, or not checked.
- `blocker`: exact reason and retry command when unsafe.

## Common Mistakes

- Treating a generic smoke test as proof of a critical compile, inference, dataset, or benchmark path.
- Running default build parallelism without checking memory.
- Compiling CUDA kernels for broad architecture lists when the task is local to the current host.
- Saturating all RAM, CPU, disk, or GPU capacity just to prove environment readiness.
- Hiding skipped heavy work behind `ready` instead of reporting a blocker and the bounded command to retry.
