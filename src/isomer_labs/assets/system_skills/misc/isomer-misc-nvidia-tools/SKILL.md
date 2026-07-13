---
name: isomer-misc-nvidia-tools
description: Use when Codex is setting up or repairing a Pixi CUDA/C++ build environment, choosing CUDA Toolkit components, wiring host NVIDIA tools into Pixi commands, selecting NVIDIA Conda packages, or preparing CMake/Ninja CUDA build tasks in Isomer Labs.
---

# Isomer Misc NVIDIA Tools

## Overview

- **Purpose**: keep NVIDIA and CUDA Pixi environment setup preferences for Isomer Labs.
- **Boundary**: do not use this skill for `nvcc` architecture or compile-parallelism policy.
- **Routing**: send bounded CUDA compile decisions to `isomer-misc-bounded-run-tips`.

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

## NVIDIA Profiler and Debugger Command Shape

For NVIDIA tools that launch a measured or debugged command, Pixi must launch the NVIDIA tool, and the NVIDIA tool must launch the target command. Use `pixi run ncu ... <target-command>`, `pixi run nsys profile ... <target-command>`, or `pixi run cuda-gdb --args <target-command>`.

Do not use inverted commands such as `ncu pixi run ...`, `nsys profile pixi run ...`, or `cuda-gdb --args pixi run ...` unless local evidence proves that Pixi itself is deliberately the profiled or debugged process. In Topic Workspace setup or verification, prefer the explicit form `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <nvidia-tool> ... <target-command>`.

## Boundary

For CUDA compile bounding, host GPU architecture selection, `TORCH_CUDA_ARCH_LIST`, `CMAKE_CUDA_ARCHITECTURES`, `-gencode`, `MAX_JOBS`, `ninja -j`, `cmake --build ... -j`, or RAM-aware worker counts, use `isomer-misc-bounded-run-tips` subcommand `cuda-compile`.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
