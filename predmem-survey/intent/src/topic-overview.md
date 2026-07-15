# Research Topic: Survey and Benchmark Predictive Memory Techniques in LLM Inference

Survey how memory-tiering, offloading, and activation-sparsity techniques let LLM inference run with less fast memory than the model nominally requires. The work is split into two stages:

1. **Stage 1 — Literature survey (no execution)**: Read and synthesize papers, blogs, websites, and source code across three threads:
   - OS/product-level predictive memory (MEXT/AMD, Meta TMO, Google software-defined far memory, Linux DAMON/MGLRU/zswap).
   - LLM inference framework offloading (vLLM, SGLang, TensorRT-LLM, Hugging Face Accelerate, DeepSpeed ZeRO-Inference, llama.cpp, LMCache, Dynamo KVBM, KV-cache offload research).
   - LLM-in-a-Flash and activation-sparsity follow-ups (ReLUfication/ProSparse/TurboSparse/Q-Sparse, training-free pruning CATS/TEAL/SCAP/WAS/WiSparse/R-Sparse/LaRoSA, cache-aware DIP, prompt-level GRIFFIN/TDA, system co-design PowerInfer/PowerInfer-2, architecture MoC/LTE).

2. **Stage 2 — Empirical validation (real inference runs)**: Pick a small set of usable open-source implementations and run them on this host with real models. Collect first-hand throughput, latency, and memory statistics, and compare measured behavior with the claims found in Stage 1.

The final output is a source-grounded survey report plus an empirical benchmark dossier.

## Motivation

- GPU VRAM is the dominant bottleneck for large-model and long-context inference.
- Three different communities attack the same problem: OS memory-tiering, LLM runtime offloading, and sparse-activation model/runtime co-design. They rarely cite each other cleanly.
- MEXT/AMD-style "AI predictive memory" promises transparent DRAM/flash tiering, but mainstream LLM inference uses model-aware tensor placement and, increasingly, activation-sparsity-based weight loading.
- First-hand benchmarks are needed because vendor and paper claims rarely match a specific host, model, and workload.

## Topic Breakdown

### Stage 1: Literature survey (with optional quick tests)

For each thread, read primary sources and compare systems along:

- What is placed or offloaded (weights, KV cache, activations, FFN neurons/experts).
- How the placement/prefetch/sparsity decision is made (transparent page prediction, explicit layer/tensor schedule, learned predictor, magnitude threshold, cache-aware score, architectural sparsity).
- Bandwidth and latency bottlenecks (PCIe, NVMe, CPU-GPU unified memory, flash I/O).
- Workload fit and failure modes (dense decode vs long-context KV vs offline batching).
- Production maturity and reproducibility of claims.

Stage 1 may also include quick installation/import checks or tiny smoke tests to verify that a shortlisted framework is runnable on this host, but no systematic model downloads or benchmarks.

### Stage 2: Empirical validation

- Select open-source frameworks and systems expected to run on this host.
- Establish a no-offload baseline on GPU.
- Run offloading or sparsity modes: CPU/NVMe weight offload, KV-cache offload, layer streaming, mmap/quantized inference, PowerInfer hot/cold neuron placement, sparse-activation kernels where available.
- Collect first-hand statistics: end-to-end latency, throughput (tokens/s), GPU/CPU/host memory footprint, PCIe/NVMe pressure when observable, and qualitative stability.
- Compare measurements with documentation and papers from Stage 1, recording gaps and caveats.

### Do's

- Keep the three threads (OS predictive memory, LLM runtime offloading, LLM-in-a-Flash sparsity) clearly separated while noting where they overlap.
- Cover the must-have LLM-in-a-Flash paper and its direct follow-ups (DIP, PowerInfer, PowerInfer-2, TurboSparse, CATS, TEAL, ProSparse, Q-Sparse, GRIFFIN, MoC, LTE).
- Cover production frameworks and KV-cache offload research (vLLM, SGLang, TensorRT-LLM, Accelerate, DeepSpeed, llama.cpp, LMCache, Dynamo KVBM, HeadInfer, SpecOffload, CLO).
- Ground survey claims in primary sources with exact locators.
- Keep benchmark scripts reproducible and version-pinned.
- Record exact host hardware, driver, CUDA, and library versions.
- Analyze weights vs KV-cache vs FFN-neuron sparsity separately.
- Record assumptions, failure modes, and open questions explicitly.

### Don'ts

- Do not conflate OS-level page prediction with model-aware tensor placement or activation sparsity.
- Do not treat every CPU/disk offload as "predictive memory."
- Do not generalize benchmark results beyond the measured models and host.
- Do not skip the bandwidth-bottleneck and tail-latency analysis.
- Do not produce a generic literature list without empirical comparison.

## Expected Outcome

- A bounded Kaoju Survey Contract or Frame.
- A curated source list with Source Digests for key papers, repos, and docs.
- A survey report from Stage 1.
- A reproducible benchmark harness and raw run logs from Stage 2.
- First-hand benchmark results for selected open-source systems.
- A combined Field Summary / Dossier that maps the three threads, compares claims and measurements, and identifies the most practical techniques for this host.
- A clear bottom-line view on whether MEXT-style predictive memory appears in mainstream LLM inference, what is used instead, and how well it works.

## Related Links

### OS/product predictive memory

- NAND Research on MEXT: https://nand-research.com/mext-predictive-memory-software-to-control-dram-costs/
- AMD acquires MEXT: https://www.amd.com/en/blogs/2026/amd-acquires-mext-for-memory-optimization.html
- MEXT technology: https://www.mext.ai/technology
- Meta TMO: https://engineering.fb.com/2022/06/20/data-infrastructure/transparent-memory-offloading-more-memory-at-a-fraction-of-the-cost-and-power/
- Google far memory: https://research.google/pubs/software-defined-far-memory-in-warehouse-scale-computers/
- Senpai: https://github.com/facebookincubator/senpai
- DAMON: https://docs.kernel.org/admin-guide/mm/damon/reclaim.html
- MGLRU: https://docs.kernel.org/admin-guide/mm/multigen_lru.html
- TPP: https://arxiv.org/abs/2206.02878
- HeMem: https://github.com/cuhk-mass/hemem
- MEMTIS: https://github.com/cosmoss-jigu/memtis
- Colloid: https://github.com/host-architecture/colloid
- FarSight: https://arxiv.org/html/2506.00384v1
- Learning Memory Access Patterns: https://proceedings.mlr.press/v80/hashemi18a/hashemi18a.pdf

### LLM inference offloading

- vLLM docs: https://docs.vllm.ai/
- SGLang docs: https://docs.sglang.ai/
- TensorRT-LLM docs: https://nvidia.github.io/TensorRT-LLM/latest/
- Hugging Face Accelerate: https://huggingface.co/docs/accelerate/
- DeepSpeed ZeRO-Inference: https://www.deepspeed.ai/2022/09/09/zero-inference.html
- FlexGen paper: https://proceedings.mlr.press/v202/sheng23a.html
- llama.cpp: https://github.com/ggml-org/llama.cpp
- NVIDIA CPU-GPU memory sharing: https://developer.nvidia.com/blog/accelerate-large-scale-llm-inference-and-kv-cache-offload-with-cpu-gpu-memory-sharing/
- LMCache paper: https://arxiv.org/abs/2510.09665
- NVIDIA Dynamo KV cache offloading: https://docs.nvidia.com/dynamo/v-0-9-0/user-guides/kv-cache-offloading
- KV offloading bottlenecks: https://arxiv.org/abs/2601.19910
- HeadInfer: https://arxiv.org/abs/2502.12574
- SpecOffload: https://arxiv.org/html/2505.10259v2
- CLO CPU-light KV offloading: https://arxiv.org/abs/2511.14510

### LLM-in-a-Flash and activation-sparsity follow-ups

- LLM in a Flash (Apple): https://arxiv.org/abs/2312.11514
- CATS: https://arxiv.org/abs/2404.08763
- CATS blog (Stanford): https://scalingintelligence.stanford.edu/blogs/cats/
- TEAL: https://arxiv.org/abs/2408.14690
- SCAP: https://proceedings.mlr.press/v262/seng-chua24a.html
- WAS: https://aclanthology.org/2025.emnlp-main.57/
- WiSparse: https://arxiv.org/abs/2602.14452
- R-Sparse: https://arxiv.org/abs/2504.19449
- LaRoSA: https://arxiv.org/html/2507.01299v1
- ProSparse: https://aclanthology.org/2025.coling-main.180/
- TurboSparse: https://arxiv.org/abs/2406.05955
- Q-Sparse: https://arxiv.org/abs/2407.10969
- DIP (Qualcomm): https://github.com/Qualcomm-AI-research/dynamic-sparsity
- GRIFFIN: https://arxiv.org/abs/2404.01365
- First Activations Matter / TDA: https://arxiv.org/abs/2408.11393
- Sirius: https://arxiv.org/abs/2409.03856
- PowerInfer: https://arxiv.org/abs/2312.12456
- PowerInfer-2: https://arxiv.org/abs/2406.06282
- Mixture-of-Channels: https://arxiv.org/abs/2511.09323
- LTE: https://arxiv.org/abs/2402.06126
