# nvcc-tips

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Check whether the task is local or portable**. Treat local experimentation, local benchmarking, workspace setup, and host-specific optimization as local tasks unless the user specifies or implies a broader release target.
2. **Choose the CUDA architecture target** according to **Architecture Target Preference**.
3. **Choose CUDA build parallelism** according to **Build Parallelism Preference**.
4. **Apply the preference through the relevant build control**, such as `TORCH_CUDA_ARCH_LIST`, `CMAKE_CUDA_ARCHITECTURES`, `-gencode`, `MAX_JOBS`, `ninja -j`, `cmake --build ... -j`, or project-specific `nvcc` options.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this page and the user's request, then execute the plan.

## Architecture Target Preference

Unless the user specifies or implies a broader release target, compile CUDA kernels only for the specific architecture of the existing GPU on the host.

Before setting CUDA architecture flags, identify the host GPU architecture from local evidence such as `nvidia-smi`, framework device capability queries, or existing project configuration. Then set the narrowest appropriate target.

Do not compile broad architecture lists for convenience when the task is local. Broader targets are appropriate only when the user asks for portable wheels, release artifacts, multi-host deployment, CI coverage, or support for GPUs not present on the host.

## Build Parallelism Preference

CUDA compilation can consume substantial host memory. Do not parallelize too many CUDA build jobs or compiler threads when memory pressure is possible.

When running CUDA builds, choose conservative job counts first, especially for large extension builds or hosts without swap. Limit build-system jobs and CUDA compiler threads. Increase parallelism only after checking available memory and observing that the build is not memory-bound.
