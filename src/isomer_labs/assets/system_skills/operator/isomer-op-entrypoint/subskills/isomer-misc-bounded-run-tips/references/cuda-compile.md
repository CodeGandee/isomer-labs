# CUDA Compile

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Confirm this is an `nvcc` compile path**:
   - Use this page for CUDA kernels, CUDA/C++ extensions, PyTorch CUDA extensions, CMake CUDA targets, Ninja builds that invoke `nvcc`, and project wrappers around those tools.
   - If the task is CUDA runtime setup rather than compilation, use this page only for the compile step.
2. **Inspect host GPU architecture**:
   - Prefer `nvidia-smi` when available.
   - Query compute capability with a command such as:
     ```bash
     nvidia-smi --query-gpu=name,compute_cap --format=csv,noheader
     ```
   - Compile only for architectures that match any GPU present on the host unless the user explicitly asks for portable release artifacts.
3. **Compute the safe worker count**:
   - Assume each CUDA compile worker thread can consume 30 GB RAM.
   - Read available memory, preferably from `/proc/meminfo` `MemAvailable` or `free -g`.
   - Reserve memory for the OS and active processes before assigning workers.
   - Use:
     ```text
     safe_workers = max(1, floor((available_ram_gb - reserve_ram_gb) / 30))
     ```
   - Use at least 16 GB reserve, or 20% of available RAM, whichever is larger.
   - Cap workers by CPU count and by project-specific limits.
4. **Set compile controls**:
   - For PyTorch extension builds, set `MAX_JOBS=<safe_workers>`.
   - For CMake builds, set `CMAKE_BUILD_PARALLEL_LEVEL=<safe_workers>` or use `cmake --build ... -j <safe_workers>`.
   - For Ninja, use `ninja -j <safe_workers>`.
   - For Make, use `make -j <safe_workers>`.
   - For direct `nvcc`, avoid launching more than `<safe_workers>` concurrent compiler processes.
5. **Set architecture controls**:
   - For PyTorch, set `TORCH_CUDA_ARCH_LIST` to the host GPU capabilities only, for example `8.9` or `9.0`.
   - For CMake, set `CMAKE_CUDA_ARCHITECTURES` to host architecture numbers only, for example `89` or `90`.
   - For direct `nvcc`, pass `-gencode` entries only for matching host architectures.
   - If multiple different GPU architectures exist on the host, include each distinct host architecture once.
6. **Run the bounded compile**:
   - Run the smallest compile target that proves the required path.
   - Prefer one extension, one selected target, or one baseline kernel before building all artifacts.
   - Watch memory during the first run when possible.
7. **Report result and blockers**:
   - If the bounded compile passes, report the resource probe, architecture list, worker count, command, and artifact or import check that proves the compile path.
   - If it fails from code or dependency errors, report `failed` with command output summary.
   - If resources are insufficient even for one worker, report `blocked` with the minimum retry command and required memory.

If the user's CUDA compile task does not map cleanly to these steps, use your native planning tool to identify the compile launcher, architecture flag surface, and parallelism control before running anything heavy.

## Architecture Rule

For local development, local environment setup, local benchmarking, and host-specific optimization, compile only for architectures matching GPUs present on the host.

Do not compile for broad architecture lists such as every common Ampere, Ada, Hopper, and Blackwell target unless the user asks for portable wheels, release artifacts, CI coverage, multi-host deployment, or support for GPUs not present on the host.

## Worker Count Rule

Use 30 GB RAM per CUDA compile worker thread as the default sizing rule.

Example:

```text
available_ram_gb = 180
reserve_ram_gb = max(16, floor(180 * 0.20)) = 36
usable_ram_gb = 144
safe_workers = floor(144 / 30) = 4
```

Recommended settings for that host:

```bash
export MAX_JOBS=4
export CMAKE_BUILD_PARALLEL_LEVEL=4
ninja -j 4
```

If the host has only 48 GB available:

```text
reserve_ram_gb = 16
usable_ram_gb = 32
safe_workers = 1
```

Use one worker. Do not round up.

## Command Examples

PyTorch CUDA extension:

```bash
export MAX_JOBS=1
export TORCH_CUDA_ARCH_LIST="8.9"
pip install -v --no-build-isolation -e .
```

CMake and Ninja:

```bash
cmake -S . -B build -DCMAKE_CUDA_ARCHITECTURES=89
cmake --build build -j 1
```

Direct `nvcc` for compute capability 8.9:

```bash
nvcc -gencode arch=compute_89,code=sm_89 -O3 -c kernel.cu -o kernel.o
```

Multiple host architectures, one entry each:

```bash
export TORCH_CUDA_ARCH_LIST="8.9;9.0"
cmake -S . -B build -DCMAKE_CUDA_ARCHITECTURES="89;90"
```

## Guardrails

- DO NOT use all CPU cores as CUDA build workers without considering RAM.
- DO NOT compile many architectures for a local benchmark or local env gate.
- DO NOT set `TORCH_CUDA_ARCH_LIST` wider than the host GPUs because it feels safer.
- DO NOT treat `import torch` or `torch.cuda.is_available()` as proof that `nvcc` can compile the required extension.
- DO NOT continue to increase parallelism after out-of-memory errors, compiler crashes, or system pressure.
