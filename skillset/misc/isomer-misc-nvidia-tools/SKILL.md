---
name: isomer-misc-nvidia-tools
description: Use when Codex is setting up or repairing a Pixi CUDA/C++ build environment, choosing CUDA Toolkit components, wiring host NVIDIA tools into Pixi commands, selecting NVIDIA Conda packages, or preparing CMake/Ninja CUDA build tasks in Isomer Labs.
---

# Isomer Misc NVIDIA Tools

## Overview

Use this skill as a compact preference ledger for NVIDIA and CUDA Pixi environment setup in Isomer Labs. Do not use it for `nvcc` architecture or compile-parallelism policy; route bounded CUDA compile decisions to `isomer-misc-bounded-run-tips`.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Identify the NVIDIA/CUDA decision point** in the user's task.
2. **Select the applicable subcommand** from the **Subcommands** table.
3. **Load and execute the selected subcommand page**. Use `pixi-cuda-cpp-env` for Pixi CUDA/C++ build environment setup.
4. **Keep the response or edit scoped** to the local Isomer preference; do not add generic NVIDIA guidance.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the subcommands and preferences in this skill, then execute the plan.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `pixi-cuda-cpp-env` | Set up or repair a Pixi environment for compiling CUDA and C++ code | [references/pixi-cuda-cpp-env.md](references/pixi-cuda-cpp-env.md) |

## Boundary

For CUDA compile bounding, host GPU architecture selection, `TORCH_CUDA_ARCH_LIST`, `CMAKE_CUDA_ARCHITECTURES`, `-gencode`, `MAX_JOBS`, `ninja -j`, `cmake --build ... -j`, or RAM-aware worker counts, use `isomer-misc-bounded-run-tips` subcommand `cuda-compile`.
