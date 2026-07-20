# PyTorch Package Specifics

Use this page when a task depends on PyTorch package source, CPU/GPU variants, CUDA runtime support, Flash Attention builds, Triton compatibility, or model execution readiness.

## Core Rule

Do not treat PyTorch as ready merely because `import torch` succeeds. Match the installed PyTorch variant to the task's required runtime.

## Decision Points

1. **Identify the required runtime**:
   - CPU-only inference or tests may accept a CPU build.
   - CUDA kernel work, Flash Attention, GPU inference, NVIDIA profiling, or GPU benchmarks require a CUDA-enabled build.
   - Other accelerator targets need their own package-source evidence.
2. **Check GPU posture with `nvidia-smi` first**:
   - Prefer `nvidia-smi` for host GPU model, driver version, CUDA driver capability, visible devices, memory use, and active processes.
   - Use `nvcc --version` only for compiler/toolkit evidence; it does not replace `nvidia-smi` for GPU availability.
   - If `nvidia-smi` is missing or fails, record that blocker or caveat before choosing CUDA package variants.
3. **Choose package source deliberately** using **Installation Source Ladder**.
4. **Reject wrong variants**:
   - CPU-only PyTorch is a blocker when the task requires CUDA/GPU behavior.
   - Builds whose names or metadata indicate `cpu`, `cpu_generic`, or no CUDA runtime do not satisfy a CUDA gate.
5. **Verify runtime metadata**:
   - For CUDA-required tasks, check `torch.version.cuda`.
   - On a GPU host, also check `torch.cuda.is_available()`.
   - For architecture-sensitive builds, check `torch.cuda.get_arch_list()` when available.
6. **Report caveats**:
   - Distinguish package installation readiness from GPU runtime readiness.
   - Distinguish host CUDA driver/toolkit availability from PyTorch CUDA runtime support.

## Installation Source Ladder

Use this order when installing or repairing PyTorch in a Pixi environment:

1. **Online official guidance**:
   - When internet access is available, check the official PyTorch installation page at execution time and choose the command that matches the platform, Python version, package manager, and accelerator runtime.
   - Convert the official command into the caller's Pixi-scoped environment style. Prefer Pixi/PyPI dependency declarations when they can express the same source, otherwise use `pixi run --manifest-path <manifest_path> --environment <env> python -m pip install ...`.
   - Record the official URL, selected runtime, package source, and command.
2. **Offline or restricted network with pip source resolution**:
   - When public internet is unavailable, route package-source resolution to `isomer-srv-resolve-pkg-repo` before running pip.
   - Use the resolved reachable PyPI mirror, private index, wheelhouse, or local file source with an explicit pip command.
   - Record the source, index URL or `--find-links` path, package spec, and whether the selected artifact matches the required runtime.
3. **System Python fallback**:
   - If package installation cannot reach a suitable source, inspect whether a system Python already has a compatible PyTorch.
   - Check Python version, ABI compatibility, `torch.__file__`, `torch.__version__`, `torch.version.cuda`, `torch.cuda.is_available()`, and native library path needs.
   - Introduce it into Pixi only as an explicit fallback: prefer a local wheel or reproducible local artifact when available; otherwise use Pixi-mediated external runtime wiring such as `PYTHONPATH` and required library path variables in the recorded `pixi run` command.
   - Mark this fallback as host-specific and lower portability. Do not treat it as a normal Pixi-managed installation.

## Verification Snippet

Use a Pixi-scoped command shape from the caller's environment setup skill. The Python payload should include:

```python
import torch

print("torch", torch.__version__)
print("torch.version.cuda", torch.version.cuda)
print("torch.cuda.is_available", torch.cuda.is_available())
print("torch.cuda.get_arch_list", torch.cuda.get_arch_list() if hasattr(torch.cuda, "get_arch_list") else [])
```

## Common False Positives

| False Positive | Why It Is Wrong | Correct Check |
| --- | --- | --- |
| `import torch` succeeds | CPU builds import successfully. | Check the required runtime metadata. |
| Host `nvcc --version` works | Host CUDA tooling does not prove PyTorch was built with CUDA. | Check `torch.version.cuda`. |
| `nvidia-smi` sees a GPU | A visible GPU does not prove the Python package can use it. | Use it for host GPU posture, then check `torch.cuda.is_available()` from the target environment. |
| Solver installed `pytorch` | Solvers may choose CPU variants when constraints allow them. | Inspect package build metadata and runtime metadata. |
| System Python has PyTorch | The Pixi environment may still be isolated from those packages and native libraries. | Bridge it only with explicit fallback wiring or a local artifact. |

## Blockers

Report a blocker when:

- the task requires CUDA/GPU PyTorch but only a CPU build is reachable;
- package source evidence for the selected platform and Python version is unclear;
- runtime checks show `torch.version.cuda is None` for a CUDA-required task;
- `torch.cuda.is_available()` is false on a GPU host and the task requires immediate GPU execution;
- a Flash Attention or CUDA extension build requires a PyTorch/CUDA/architecture combination that is not available in the selected environment.
