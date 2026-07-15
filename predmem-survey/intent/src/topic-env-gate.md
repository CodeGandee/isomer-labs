# Topic Environment Gate: Predictive Memory for LLM Inference — Survey + Benchmarks

## Shared environment

The Python/PyTorch stack below is needed for the whole topic, including quick tests during Stage 1 and full benchmarks during Stage 2.

### Host hardware

- 8× NVIDIA B200 GPUs (compute capability 10.0), driver 590.48.01.
- CUDA Toolkit 13.1 installed on the host (`nvcc` 13.1.115).
- ~2.2 TB CPU RAM.
- ~243 GB free NVMe storage on `/data/ssd1`.

### Target Python and PyTorch stack

Use the highest PyPI versions that are compatible with this host's driver:

- **Python 3.13** (latest stable at setup time).
- **PyTorch 2.13.0+cu130** (CUDA 13.0 wheel).
  - The host driver is **590.48.01**, which supports **CUDA 13.0/13.1**.
  - PyTorch `cu132` (CUDA 13.2) requires a newer driver (≈595.45+) and is therefore incompatible.
  - No PyTorch `cu131` wheels are available on PyPI.
  - `cu130` is the highest CUDA wheel available for this driver that also supports Blackwell/B200.
- If `cu130` wheels fail to load, fall back to the highest working CUDA wheel (e.g., `cu128` or `cu126`) that still supports Blackwell.
- Pixi will resolve the environment from PyPI inside the Topic Workspace.

## Stage 1: Literature Survey (with optional quick tests)

Stage 1 is primarily reading-based: papers, blogs, documentation, and source code. It may also include quick installation checks, import smoke tests, or tiny model runs to verify that a framework is usable on this host. No large model downloads or systematic benchmarking yet.

- Web access for fetching primary sources (framework docs, arXiv papers, GitHub repos, vendor blogs).
- Tools for content extraction and note-taking: a web browser or fetch tool, PDF/text extraction if needed, and the Isomer Kaoju survey skills.
- Markdown and PDF readers for examining acquired materials.
- The shared Python/PyTorch environment for quick tests.

## Stage 2: Empirical Validation (real inference runs)

Stage 2 runs real models on this host and collects first-hand statistics. It requires the same CUDA-capable GPU, CPU RAM, disk, and Python/PyTorch environment as Stage 1.

### Candidate workloads

No candidate models have been selected yet. Once Stage 1 narrows the scope, choose models that fit the selected frameworks and this host's memory. Candidate workload types include:

- Short-context single-request decode throughput and latency.
- Long-context prefill and decode (KV-cache pressure).
- Offline batched inference.
- Weight-offload / flash-backed scenarios where the model exceeds single-GPU VRAM.
- Sparse-activation / hot-cold neuron runs (PowerInfer, TurboSparse) where checkpoints are available.

### Frameworks and systems to benchmark

Primary targets (major, open-source, and expected to run on this host):

- vLLM (baseline GPU, CPU KV offload via LMCache, `cpu_offload_gb`)
- llama.cpp (CPU/GPU split, mmap, quantization)
- Hugging Face Accelerate with `device_map` CPU/disk offload
- DeepSpeed ZeRO-Inference (CPU/NVMe weight streaming)
- PowerInfer (hot/cold neuron placement for sparse/standard models)

Secondary targets if time and compatibility allow:

- SGLang HiCache
- TensorRT-LLM KV cache offload
- FlexGen (throughput-oriented single-GPU batching)
- Sparse-activation kernels from CATS/TEAL if they provide runnable code

### Additional libraries and tools

- Isomer Kaoju extension (installed and declared).
- `transformers`, `datasets`, `accelerate`, `deepspeed`, `vllm` from PyPI.
- `huggingface-cli` for model downloads (token needed for gated models).
- `nvidia-smi`, `nvtop` or similar for GPU memory/PCIe monitoring.
- CMake/build tools for llama.cpp and PowerInfer.

### Runtime assumptions

- At least one B200 GPU is available and not reserved by another process.
- Models can be downloaded from Hugging Face or another configured model hub.
- Closed-source systems (MEXT, TensorRT-LLM binaries where not open) are compared from documentation, not measured directly.
- Some sparse-activation research code may be CPU/GPU-kernel specific; fallback to survey-only coverage when code cannot run on B200.

## Expected Repositories

- Topic Main Development Repository for the benchmark harness and analysis notebooks.
- Open-source frameworks and systems to inspect and benchmark (shallow clones where needed):
  - `vllm-project/vllm`
  - `ggml-org/llama.cpp`
  - `sgl-project/sglang` (if Blackwell-compatible builds are available)
  - `microsoft/DeepSpeed`
  - `SJTU-IPADS/PowerInfer` and/or `SJTU-IPADS/PowerInfer-2`
  - `facebookincubator/senpai` (for Meta TMO comparison, no benchmark)
- Optional research-code repos if they release kernels or checkpoints:
  - CATS/TEAL/SCAP/WAS/WiSparse/R-Sparse/LaRoSA (check for public code)
  - TurboSparse/Q-Sparse model checkpoints on Hugging Face
  - DIP code (`Qualcomm-AI-research/dynamic-sparsity`)
- Use `--depth=1` unless version-history analysis is required.

## Datasets

- No fixed datasets. The survey may collect reported benchmark numbers from papers and docs; those should be recorded as Source Digests.
- Stage 2 may use small prompt datasets for benchmarking (e.g., `truthful_qa`, `hellaswag`, or custom prompts) downloaded on demand.

## Unavailable Resources

- MEXT software is closed-source; no direct measurement.
- Independent third-party MEXT benchmarks are not known.
- Some frameworks may not yet have stable Blackwell/B200 wheels; fallback to Ampere-compatible containers or CPU-only modes may be needed.
- Some sparse-activation methods may not release runnable kernels.

## Success Criteria

- A bounded Kaoju Survey Contract or Frame is accepted.
- Stage 1: primary sources for each thread are acquired and recorded with Source Digests; a survey report draft exists.
- Stage 2: a reproducible benchmark harness runs at least three open-source systems on selected models; first-hand statistics are captured with raw logs.
- A combined Field Summary / Dossier compares survey evidence and measured behavior across all three threads.

## Open Setup Questions

- Which frameworks install cleanly on B200 with PyTorch 2.13.0+cu130? Start with vLLM + llama.cpp + Accelerate + DeepSpeed + PowerInfer as the core set?
- Should benchmarks use gated models (Llama) or fully open models (Qwen, Mistral, TurboSparse)? A Hugging Face token may be needed.
- Should we pin a single CUDA/PyTorch stack, or allow per-framework environments?
- Should the benchmark harness live in `topic.repos.main` as a Python package or standalone scripts?
- Which sparse-activation systems have runnable GPU kernels for B200?

## Source Material

- Seed briefs provided by the operator:
  1. The markdown article covering predictive memory definition, MEXT/AMD acquisition, Meta TMO, Google far memory, Linux building blocks, academic systems, ML prefetching, workload fit, and evaluation questions.
  2. The markdown article covering LLM-in-a-Flash and its follow-ups: ReLUfication, training-free activation pruning, cache-aware DIP, prompt-level pruning, PowerInfer/PowerInfer-2, TurboSparse, MoC, and LTE.
- Synthesized prior survey: `intent/src/prior-survey.md`.
