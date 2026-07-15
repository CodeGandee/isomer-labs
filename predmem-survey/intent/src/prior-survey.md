# Prior Survey Summaries

This file collects the seed survey material supplied before the formal Isomer/Kaoju survey begins. It is organized into three threads that together cover predictive memory, LLM-inference offloading, and LLM-in-a-Flash-style activation sparsity.

---

## Thread 1: Predictive Memory — MEXT, OS Tiering, and Academic Systems

### What "predictive memory" means

Predictive memory is a transparent memory-tiering system that tries to make cheap, slower storage behave like extra DRAM. The system watches memory pages, keeps hot pages in DRAM, moves cold pages to flash, and uses a predictive engine to bring likely-needed pages back into DRAM before the application touches them. It is a software control layer, not a new physical memory technology.

### Why it is getting attention

- DRAM is becoming a cost and capacity bottleneck.
- Large production workloads have big cold-memory fractions.
- Intel Optane is gone and CXL is still in transition.
- AMD acquired MEXT in June 2026, turning a startup story into a data-center platform story.

### Critical read

The aggressive claim is "DRAM-class performance at flash-level cost." That is only true under favorable workload conditions: large cold fraction, learnable access patterns, good prediction recall, low migration overhead, tolerable tail latency, and sufficient flash bandwidth/endurance. Predictive memory can reduce DRAM spend for workloads with large structured cold memory, but it is not a universal DRAM replacement.

### Major systems

| System | Layer | What it does | Status |
| --- | --- | --- | --- |
| MEXT Predictive Memory | Kernel/user-space product | Offloads cold pages to flash and predicts page demand for pre-promotion | Commercial, closed-source, acquired by AMD June 2026 |
| Meta TMO / Senpai / PSI | Linux kernel + user-space agent | Offloads cold pages under memory pressure using PSI/cgroup signals | Production at Meta since 2021; Senpai is open source |
| Google Software-Defined Far Memory | Kernel + node agent | Compresses cold pages and uses learning-based autotuning | Production at Google since 2016 |
| Linux zswap / zram / MGLRU / DAMON | Mainline Linux | Compression, cold-page tracking, reclaim, demotion/promotion foundations | Open-source, production Linux |

### Academic systems

- **TPP** — transparent page placement for CXL-enabled tiered memory.
- **HeMem** — user/kernel tiered-memory manager for DRAM + NVM using CPU event sampling.
- **Nimble** — OS-integrated page migration optimizing huge-page migration throughput.
- **MEMTIS** — dynamic page classification and page-size determination for DRAM + Optane.
- **Nomad** — non-exclusive tiering with shadow copies on the slow tier to reduce thrashing.
- **Colloid** — latency-aware tier balancing for CXL/HBM-like systems.

### ML / predictive prefetching

- **Learning Memory Access Patterns** — neural-network-based prefetching.
- **FarSight** — Linux far-memory system with deep-learning-based prefetching (up to 3.6× improvement reported).
- **Transformer-based UVM prefetching** — for CPU-GPU unified virtual memory.
- **Intelligent prefetching survey** — taxonomy of ML-based prefetching trade-offs.

### Best-fit and risky workloads

Best fit: offline rendering, semiconductor EDA, game-engine asset pipelines, batch analytics with phases, large graph/scientific workloads with recurring access phases.

Risky: low-latency trading/serving, unpredictable random-read databases, in-memory caches, real-time inference with strict p99/p999 budgets, high dirty-page churn, genuinely hot working sets.

### Key links

- NAND Research on MEXT: https://nand-research.com/mext-predictive-memory-software-to-control-dram-costs/
- MEXT technology: https://www.mext.ai/technology
- AMD acquires MEXT: https://www.amd.com/en/blogs/2026/amd-acquires-mext-for-memory-optimization.html
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

### Open questions from Thread 1

- How much of a target workload's RSS is cold for long enough?
- What is the p99/page-fault latency with predictive tiering enabled?
- What is prediction recall for pages that become hot?
- How much CPU does tracking and inference consume?
- What happens under memory pressure plus write-heavy phases?
- Does it improve throughput at equal cost, or merely avoid OOM?

---

## Thread 2: Predictive Memory in Mainstream LLM Inference Frameworks

### Strict answer: no

Mainstream LLM inference frameworks do **not** use MEXT-style transparent OS-level AI predictive memory. They use model-aware explicit offloading instead.

### Broad answer: yes

LLM frameworks use related ideas: CPU/NVMe offload, mmap, layer streaming, KV-cache paging, hierarchical KV caches, and explicit prefetch.

### The important distinction

MEXT-style predictive memory is generic and hidden below the application. LLM inference offloading is explicit and model-aware: the runtime knows the transformer layer order and places weights/KV/activations across GPU, CPU, and disk, prefetching exact next tensors.

### What mainstream frameworks do

| System | What it uses | Resembles predictive memory? | Enables otherwise impossible runs? |
| --- | --- | --- | --- |
| vLLM | PagedAttention, optional CPU offload, LMCache integration | OS-like paging, but not transparent AI page prediction | Yes, via `cpu_offload_gb` and LMCache |
| SGLang HiCache | Hierarchical KV cache across GPU/CPU/disk/remote | Close to application-level hierarchical memory | Yes, for long-context/multi-turn serving |
| TensorRT-LLM | KV-cache reuse, LRU eviction, host-memory offload | Explicit cache policy | Yes, for KV reuse |
| Hugging Face Accelerate | `device_map`, CPU/disk offload | Explicit module placement | Yes, useful for experimentation |
| DeepSpeed ZeRO-Inference | Host weights in CPU/NVMe, layer prefetch | Deterministic layer prefetch, not generic page prediction | Yes, for models too large for GPU memory |
| FlexGen | GPU+CPU+disk tensor placement, LP schedule, 4-bit compression | Model-aware hierarchy optimization | Yes, OPT-175B on a single 16 GB GPU reported |
| llama.cpp | mmap, CPU/GPU split, quantized GGUF | Relies on OS page cache, not predictive memory | Yes for local inference |
| NVIDIA Grace Hopper unified memory | CPU-GPU coherent memory | Hardware-coherent expansion, not flash prediction | Yes on specific platforms |

### Research systems moving closer

- **HeadInfer** — offloads KV cache to CPU RAM and keeps selective attention-head KV on GPU; reports 1M-token KV footprint reduction on Llama-3-8B.
- **SpecOffload** — combines offload scheduling with speculative decoding.
- **CLO, ScoutAttention, KVDrive, Tutti** — newer algorithm-system co-design for CPU/PCIe/SSD bottlenecks.

### Bottom line

> Is MEXT-like predictive memory used in mainstream LLM inference frameworks? No, not in the strict sense. Is the broader idea of slower memory tiers making impossible models/contexts possible used? Yes, very much, but as explicit LLM-aware offload.

### Key links

- vLLM cache config: https://docs.vllm.ai/en/v0.11.2/api/vllm/config/cache/
- SGLang HiCache: https://www.lmsys.org/blog/2025-09-10-sglang-hicache/
- TensorRT-LLM KV cache: https://nvidia.github.io/TensorRT-LLM/latest/features/kvcache.html
- Hugging Face Accelerate big-modeling: https://huggingface.co/docs/accelerate/en/package_reference/big_modeling
- DeepSpeed ZeRO-Inference: https://www.deepspeed.ai/2022/09/09/zero-inference.html
- FlexGen: https://proceedings.mlr.press/v202/sheng23a.html
- llama.cpp: https://github.com/ggml-org/llama.cpp
- NVIDIA CPU-GPU memory sharing: https://developer.nvidia.com/blog/accelerate-large-scale-llm-inference-and-kv-cache-offload-with-cpu-gpu-memory-sharing/
- LMCache: https://arxiv.org/abs/2510.09665
- NVIDIA Dynamo KV cache offloading: https://docs.nvidia.com/dynamo/v-0-9-0/user-guides/kv-cache-offloading
- KV offloading bottlenecks: https://arxiv.org/abs/2601.19910
- HeadInfer: https://arxiv.org/abs/2502.12574
- SpecOffload: https://arxiv.org/html/2505.10259v2
- CLO: https://arxiv.org/abs/2511.14510

### Open questions from Thread 2

- How much of a dense model's working set is actually "cold" during decode?
- Does PCIe/NVMe bandwidth dominate latency when weights or KV cache are offloaded?
- Which is more practical for this host: weight offload, KV-cache offload, or unified CPU-GPU memory?
- How do quantization and sparsity change the offload vs native-GPU trade-off?

---

## Thread 3: LLM-in-a-Flash and Activation-Sparsity Follow-ups

### Core problem

The original LLM-in-a-Flash idea exploited ReLU-style FFN activation sparsity: if most neurons are zero, only active neurons' weights need to be loaded from flash. Modern Llama/Mistral/Qwen-style models use SwiGLU, which does **not** produce exact zeros. This breaks the original trick and created a large follow-up literature.

### Two philosophies

1. Make the model sparse again (ReLUfication / trained sparse models).
2. Keep SwiGLU checkpoints but approximate sparsity with Top-(k), thresholding, ranking, or cache-aware pruning.

### Method families

| Family | Representatives | Core answer to SwiGLU | Best fit |
| --- | --- | --- | --- |
| Activation replacement / ReLUfication | ReLU Strikes Back, ProSparse, TurboSparse, Q-Sparse | Change model so FFN activations become hard-sparse | Future sparse checkpoints and flash-style loading |
| Training-free activation pruning | CATS, TEAL, SCAP, R-Sparse, WAS, WiSparse, LaRoSA | Prune low-importance activation channels | Existing Llama/Mistral/Qwen models |
| Cache-aware dynamic offload | DIP | Pick active channels while considering what is already cached | Direct continuation of LLM-in-a-Flash |
| Prompt/sequence-level pruning | GRIFFIN, First Activations Matter / TDA | Reuse masks across a prompt/sequence | Lower overhead, longer generation |
| Model-system co-design | PowerInfer, PowerInfer-2, TurboSparse models, MoC, LTE | Train/convert models with hardware-friendly sparsity | Deployable large models on small devices |

### Key works in detail

- **ProSparse** — ReLU replacement with progressive sparsity regularization; ~89% activation sparsity and up to 4.52× speedup reported on LLaMA2-7B/13B.
- **TurboSparse** — dReLU activation + continued training; released sparse Mistral/Mixtral models; 2–5× decoding speedups reported.
- **Q-Sparse** — trains models with Top-(K) activation sparsification and straight-through estimator.
- **CATS** — contextually-aware thresholding for sparsity; ~50% activation sparsity with ~1–2% quality loss and ~15% latency improvement.
- **TEAL** — magnitude-based training-free sparsity; 40–50% model-wide activation sparsity, ~1.53× at 40%, ~1.8× at 50% speedup.
- **SCAP, WAS, WiSparse, R-Sparse, LaRoSA** — refine scoring rules (statistical calibration, weight-aware, rank-aware, rotated spaces).
- **DIP** — predictor-free cache-aware dynamic input pruning; ~46% memory reduction and 40% throughput increase on Phi-3-Medium with <0.1 perplexity loss.
- **GRIFFIN** — prompt-conditioned structured pruning; ~50% FFN parameter pruning, ~1.29× speedup on Gemma 7B.
- **PowerInfer** — hot/cold neuron placement on GPU/CPU with predictors; up to 11.69× speedup over llama.cpp reported.
- **PowerInfer-2** — extends to smartphones; clusters neurons, uses NPU/CPU/storage pipeline; up to 27.8× speedup and 47B model on a smartphone reported.
- **MoC (Mixture-of-Channels)** and **LTE (Learn-To-Be-Efficient)** — architectural alternatives that build structured sparsity into the model.

### How these compare for LLM-in-a-Flash

| Goal | Best-suited family | Why |
| --- | --- | --- |
| Run existing checkpoint faster | TEAL/CATS/SCAP/WAS/WiSparse/R-Sparse/LaRoSA | No model conversion |
| Run model larger than RAM/VRAM with flash/SSD | DIP, PowerInfer-2, TurboSparse-style models | They reason about cache/storage |
| Preserve exact model semantics | Pure offload only | Activation pruning changes computation |
| Large speedup on GPU kernels | TEAL/CATS-style sparsity with custom kernels | Needs hardware-friendly sparsity |
| Large speedup on tiny devices | PowerInfer-2 + sparse model variants | Exploits heterogeneous compute/storage |
| Make future models easy to page/load sparsely | Q-Sparse, ProSparse, TurboSparse, MoC, LTE | Model is trained to be sparse |

### Key links

- LLM in a Flash: https://arxiv.org/abs/2312.11514
- CATS: https://arxiv.org/abs/2404.08763
- CATS blog: https://scalingintelligence.stanford.edu/blogs/cats/
- TEAL: https://arxiv.org/abs/2408.14690
- SCAP: https://proceedings.mlr.press/v262/seng-chua24a.html
- WAS: https://aclanthology.org/2025.emnlp-main.57/
- WiSparse: https://arxiv.org/abs/2602.14452
- R-Sparse: https://arxiv.org/abs/2504.19449
- LaRoSA: https://arxiv.org/html/2507.01299v1
- ProSparse: https://aclanthology.org/2025.coling-main.180/
- TurboSparse: https://arxiv.org/abs/2406.05955
- Q-Sparse: https://arxiv.org/abs/2407.10969
- DIP: https://github.com/Qualcomm-AI-research/dynamic-sparsity
- GRIFFIN: https://arxiv.org/abs/2404.01365
- First Activations Matter / TDA: https://arxiv.org/abs/2408.11393
- Sirius: https://arxiv.org/abs/2409.03856
- PowerInfer: https://arxiv.org/abs/2312.12456
- PowerInfer-2: https://arxiv.org/abs/2406.06282
- Mixture-of-Channels: https://arxiv.org/abs/2511.09323
- LTE: https://arxiv.org/abs/2402.06126

### Open questions from Thread 3

- Which of these sparse-activation methods have runnable GPU kernels for B200?
- Do TurboSparse/Q-Sparse checkpoints run out-of-the-box on vLLM/llama.cpp/PowerInfer?
- How much quality loss is acceptable for a given speedup/memory-reduction target?
- Does cache-aware pruning (DIP) generalize across model families and batch sizes?
- How does activation sparsity interact with quantization and KV-cache offloading?

---

## Cross-thread synthesis

The three threads attack the same problem — running large memory-hungry workloads with less fast memory — but with different assumptions:

- **OS predictive memory** is generic and transparent, but pays tail-latency penalties and needs cold memory.
- **LLM runtime offloading** is model-aware and explicit, making it practical for dense transformers but not transparent.
- **LLM-in-a-Flash sparsity** changes or approximates the model so that only a fraction of weights need to be resident, making flash/SSD loading feasible but requiring special checkpoints or approximate pruning.

The most relevant combinations for this survey are:

1. Whether explicit LLM offloading (vLLM/DeepSpeed/Accelerate) can be compared quantitatively with OS-level memory tiering on this host.
2. Whether PowerInfer/TurboSparse-style sparse models give measurable gains over dense offloading on the same hardware.
3. Whether activation-pruning methods (CATS/TEAL/DIP) can be reproduced and whether their quality/speedup trade-offs hold on modern SwiGLU checkpoints.
