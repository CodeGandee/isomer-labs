---
name: isomer-misc-nvidia-tools
description: Use when Codex is compiling CUDA kernels with nvcc, setting CUDA architecture targets, choosing TORCH_CUDA_ARCH_LIST, CMAKE_CUDA_ARCHITECTURES, gencode flags, MAX_JOBS, ninja -j, cmake -j, CUDA build parallelism, or setting up a Pixi CUDA/C++ build environment in Isomer Labs.
---

# Isomer Misc NVIDIA Tools

## Overview

Use this skill as a compact preference ledger for NVIDIA and CUDA work in Isomer Labs. Do not expand it into a general NVIDIA guide.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Identify the NVIDIA/CUDA decision point** in the user's task.
2. **Select the applicable subcommand** from the **Subcommands** table.
3. **Load and execute the selected subcommand page**. Use `nvcc-tips` for CUDA compiler preferences and `pixi-cuda-cpp-env` for Pixi CUDA/C++ build environment setup.
4. **Keep the response or edit scoped** to the local Isomer preference; do not add generic NVIDIA guidance.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the subcommands and preferences in this skill, then execute the plan.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `nvcc-tips` | Apply Isomer preferences for CUDA kernel architecture targets and CUDA build parallelism | [references/nvcc-tips.md](references/nvcc-tips.md) |
| `pixi-cuda-cpp-env` | Set up or repair a Pixi environment for compiling CUDA and C++ code | [references/pixi-cuda-cpp-env.md](references/pixi-cuda-cpp-env.md) |
