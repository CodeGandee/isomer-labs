# Tool Packs

Use this reference after `SKILL.md` resolves a request to a named installable toolset. Return these entries as setup contracts; do not execute installs from this misc skill.

## Dependency Kinds

| Kind | Meaning | Install Preference |
| --- | --- | --- |
| `cli-pypi` | Command-line tool distributed as a Python package | Prefer `uv tool install <package>` when `uv` is available and PyPI has the package; fall back to `pixi global install <package>` when the uv tool route is unavailable, unsuitable, or does not expose the command. |
| `cli-conda` | Command-line or native tool best installed through Pixi/Conda global tooling | Prefer `pixi global install <package>` unless a pack-specific note says otherwise. |
| `python-library` | Importable Python package needed by the topic runnable target | Install into the selected Topic Workspace Pixi environment, normally with `pixi add --manifest-path <manifest_path> --pypi <package>`. |
| `r-library` | R package used by an R plotting workflow | Install through the selected R environment chosen by topic setup; preserve the Python/R backend gate. |
| `native-runtime` | Native runtime, compiler, binary, TeX engine, CUDA component, or system-style dependency | Route through topic env setup, package-source evidence, Pixi/Conda when possible, explicit runtime wiring when needed, or blocker when privileged setup is required. |
| `service-capability` | External API, local helper, or service integration rather than a package install | Record the capability and verification expectation; do not invent an install command. |

## Pack Index

| Canonical Pack | Aliases | Purpose |
| --- | --- | --- |
| `paper-writing` | `paper`, `manuscript`, `latex`, `paper-authoring`, `paper-build` | Manuscript build, citation/bibliography support, and default Python figure-generation tools. |
| `paper-figures-python` | `figures-python`, `python-figures`, `paper-plots`, `paper-plot`, `matplotlib` | Python publication figure generation. |
| `paper-figures-r` | `figures-r`, `r-figures`, `ggplot`, `nature-figure-r` | Opt-in R publication figure generation. |
| `paper2ppt` | `paper-to-ppt`, `paper-ppt`, `pptx`, `slides-from-paper`, `nature-paper2ppt` | Scientific paper PDF/text to editable PPTX deck. |
| `paper-citation` | `citation`, `bibliography`, `bibtex`, `references` | Citation discovery, BibTeX retrieval, and bibliography hygiene. |
| `cuda-build` | `cuda`, `cuda-cpp`, `cuda-compile`, `nvidia-build` | CUDA/C++ build toolchain and bounded build setup. |
| `torch-gpu` | `pytorch-gpu`, `torch-cuda`, `pytorch-cuda` | PyTorch CUDA/GPU package and runtime readiness. |
| `topic-python-starter` | `python-starter`, `topic-python`, `isomer-python-starter` | Baseline Python packages expected in Topic Workspace setup. |

## `paper-writing`

Purpose: prepare a normal paper authoring surface with LaTeX build support, citation/bibliography support, and Python figure-generation packages.

Includes:

- `paper-figures-python`
- `paper-citation`

Required tools:

| Tool | Kind | Install Preference | Verification |
| --- | --- | --- | --- |
| `tectonic` | `native-runtime` or `cli-conda` | Prefer available Pixi/Conda package or recorded external runtime wiring; use as the first LaTeX build engine. | `tectonic -X compile main.tex` on a minimal or project manuscript when available. |
| `matplotlib` | `python-library` | Topic Workspace Pixi environment through PyPI unless source evidence says otherwise. | `python -c "import matplotlib; print(matplotlib.__version__)"` inside Topic Workspace Pixi env. |
| `numpy` | `python-library` | Topic Workspace Pixi environment through PyPI unless source evidence says otherwise. | `python -c "import numpy; print(numpy.__version__)"` inside Topic Workspace Pixi env. |
| `scipy` | `python-library` | Topic Workspace Pixi environment through PyPI unless source evidence says otherwise. | `python -c "import scipy; print(scipy.__version__)"` inside Topic Workspace Pixi env. |

Fallback or venue-required tools:

| Tool | Kind | Install Preference | Verification |
| --- | --- | --- | --- |
| `latexmk` | `native-runtime` or `cli-conda` | Use only when Tectonic is unavailable, blocked by template behavior, or venue workflow requires it. | `latexmk -version`. |
| `pdflatex` | `native-runtime` or `cli-conda` | TeX Live fallback or venue-required workflow. | `pdflatex --version`. |
| `xelatex` | `native-runtime` or `cli-conda` | TeX Live fallback for templates or fonts that require XeTeX. | `xelatex --version`. |
| `lualatex` | `native-runtime` or `cli-conda` | TeX Live fallback for templates or fonts that require LuaTeX. | `lualatex --version`. |
| `bibtex` | `native-runtime` or `cli-conda` | Bibliography fallback when template uses BibTeX. | `bibtex --version`. |
| `biber` | `native-runtime` or `cli-conda` | Bibliography fallback when template uses Biber. | `biber --version`. |
| `pdfcrop` | `native-runtime` or `cli-conda` | Optional unless the active template or Makefile requires cropped figure PDFs. | `pdfcrop --version`. |

Routes:

- Use `isomer-srv-topic-env-setup` for install planning, Topic Workspace Pixi mutation, external runtime wiring, and readiness verification.
- Use `isomer-srv-resolve-pkg-repo` when PyPI, Conda, or mirror reachability affects package selection.
- Use `isomer-misc-bounded-run-tips` if build or rendering checks are resource-heavy or unknown-risk.

Blockers:

- No usable TeX engine and no permitted Pixi/Conda or external-runtime route.
- Manuscript template requires a specific TeX Live workflow that cannot be installed or wired safely.
- Python figure libraries cannot be installed into the selected Topic Workspace Pixi environment.

## `paper-figures-python`

Purpose: prepare Python publication plotting and first-pass paper figure generation.

Required tools:

| Tool | Kind | Install Preference | Verification |
| --- | --- | --- | --- |
| `matplotlib` | `python-library` | Topic Workspace Pixi environment through PyPI unless source evidence says otherwise. | Import inside Topic Workspace Pixi env and render a tiny noninteractive plot when needed. |
| `numpy` | `python-library` | Topic Workspace Pixi environment through PyPI unless source evidence says otherwise. | Import inside Topic Workspace Pixi env. |
| `scipy` | `python-library` | Topic Workspace Pixi environment through PyPI unless source evidence says otherwise. | Import inside Topic Workspace Pixi env. |

Optional tools:

| Tool | Kind | Install Preference | Use |
| --- | --- | --- | --- |
| `pandas` | `python-library` | Topic Workspace Pixi environment. | Tabular data shaping. |
| `seaborn` | `python-library` | Topic Workspace Pixi environment. | Statistical plots. |
| `statsmodels` | `python-library` | Topic Workspace Pixi environment. | Model/statistical result plots. |
| `scikit-image` | `python-library` | Topic Workspace Pixi environment. | Image panels and processing. |
| `tifffile` | `python-library` | Topic Workspace Pixi environment. | TIFF export or scientific image IO. |

Routes:

- Use `isomer-srv-topic-env-setup` for package installation and verification.
- Use `isomer-misc-bounded-run-tips` when rendering or figure-generation scripts are broad, GPU-backed, or unknown-risk.

Blockers:

- Required figure package cannot be installed into the Topic Workspace Pixi environment.
- Requested rendering path requires unavailable GUI or privileged system setup.

## `paper-figures-r`

Purpose: prepare opt-in R publication plotting when the user or source workflow has selected R.

Required tools:

| Tool | Kind | Install Preference | Verification |
| --- | --- | --- | --- |
| `R` / `Rscript` | `native-runtime` or `cli-conda` | Use the R environment selected by topic setup. | `Rscript --version`. |
| `ggplot2` | `r-library` | Selected R environment. | `Rscript -e "library(ggplot2)"`. |
| `patchwork` | `r-library` | Selected R environment. | `Rscript -e "library(patchwork)"`. |
| `ComplexHeatmap` | `r-library` | Selected R environment when heatmaps are needed. | `Rscript -e "library(ComplexHeatmap)"`. |

Optional tools:

| Tool | Kind | Install Preference | Use |
| --- | --- | --- | --- |
| `ggrepel` | `r-library` | Selected R environment. | Label placement. |
| `svglite` | `r-library` | Selected R environment. | Editable SVG export. |
| `cairo_pdf` / Cairo support | `native-runtime` or `r-library` | Selected R environment or explicit runtime wiring. | PDF export. |
| `ragg` | `r-library` | Selected R environment. | High-DPI raster export. |

Routes:

- Preserve backend exclusivity: do not install or use this pack just because `paper-writing` was requested.
- Use `isomer-srv-topic-env-setup` for setup and verification.
- Use `isomer-misc-bounded-run-tips` for heavy rendering jobs.

Blockers:

- User has not selected R and the task requires backend choice.
- Required R runtime or packages cannot be installed or safely wired.

## `paper2ppt`

Purpose: prepare cross-platform tooling for converting paper PDFs, extracted text, figures, and notes into editable PPTX decks.

Required tools:

| Tool | Kind | Install Preference | Verification |
| --- | --- | --- | --- |
| `PyMuPDF` | `python-library` | Topic Workspace Pixi environment through PyPI unless source evidence says otherwise. | `python -c "import fitz; print(fitz.__doc__[:20])"`. |
| `Pillow` | `python-library` | Topic Workspace Pixi environment through PyPI unless source evidence says otherwise. | `python -c "from PIL import Image; print(Image.__module__)"`. |
| `python-pptx` | `python-library` | Topic Workspace Pixi environment through PyPI unless source evidence says otherwise. | `python -c "import pptx; print(pptx.__version__)"`. |
| `zipfile` | `python-library` | Standard library with Python. | `python -c "import zipfile"`. |

Optional tools:

| Tool | Kind | Install Preference | Use |
| --- | --- | --- | --- |
| `LibreOffice` / `soffice` | `native-runtime` or `cli-conda` | Optional only when already available or safely installable; do not require for normal deck creation. | Rendered slide preview. |

Routes:

- Use `isomer-srv-topic-env-setup` for package installation and verification.
- Use `isomer-srv-resolve-pkg-repo` when PyPI reachability is uncertain.

Blockers:

- PPTX must be created but `python-pptx` is unavailable.
- Source PDF is scanned and OCR is required but no OCR path is provided or permitted.

## `paper-citation`

Purpose: prepare citation discovery, BibTeX retrieval, and bibliography hygiene support.

Required capabilities:

| Capability | Kind | Install Preference | Verification |
| --- | --- | --- | --- |
| DOI BibTeX retrieval | `service-capability` | Use available service/API or caller-provided retrieval path; do not invent a package. | Retrieve one known DOI citation when network and policy permit. |
| arXiv BibTeX retrieval | `service-capability` | Use available service/API or caller-provided retrieval path; do not invent a package. | Retrieve one known arXiv citation when network and policy permit. |
| OpenAlex discovery | `service-capability` | Use when available for discovery; not a mandatory package install. | Query or record unavailable. |
| DeepXiv discovery | `service-capability` | Use only when declared available by the runtime. | Query or record unavailable. |

Optional tools:

| Tool | Kind | Install Preference | Use |
| --- | --- | --- | --- |
| `curl` | `cli-conda` or external tool | Use existing or Pixi/global route when needed for direct retrieval. | `curl --version`. |

Routes:

- Use `isomer-srv-topic-env-setup` to record available capabilities and blockers.
- Use `isomer-srv-resolve-pkg-repo` only if a concrete package or CLI is selected later.

Blockers:

- Network access, API availability, or source policy prevents citation retrieval.
- Requested bibliography source is not specified and no discovery capability is available.

## `cuda-build`

Purpose: prepare CUDA/C++ build tooling, NVIDIA package/channel choices, and bounded CUDA compile posture.

Required tools:

| Tool | Kind | Install Preference | Verification |
| --- | --- | --- | --- |
| CUDA toolkit components | `native-runtime` | Prefer Pixi/Conda with NVIDIA channel evidence when possible. | Toolkit command or compile check named by the target spec. |
| `cmake` | `cli-conda` | Prefer Pixi/Conda or `pixi global install` according to setup context. | `cmake --version`. |
| `ninja` | `cli-conda` | Prefer Pixi/Conda or `pixi global install` according to setup context. | `ninja --version`. |
| C++ compiler | `native-runtime` | Pixi/Conda compiler or explicit external runtime wiring. | Compiler version and bounded build check. |

Routes:

- Use `isomer-misc-nvidia-tools` for CUDA/C++ Pixi environment preferences and NVIDIA package/runtime wiring.
- Use `isomer-misc-bounded-run-tips` subcommand `cuda-compile` for host GPU architecture and build parallelism.
- Use `isomer-srv-resolve-pkg-repo` when NVIDIA or Conda channel reachability matters.

Blockers:

- CUDA build requires privileged driver/toolkit mutation.
- Host GPU architecture or available resources cannot support even the bounded compile path.

## `torch-gpu`

Purpose: prepare PyTorch CUDA/GPU package and runtime checks.

Required tools:

| Tool | Kind | Install Preference | Verification |
| --- | --- | --- | --- |
| `torch` | `python-library` | Follow `isomer-misc-pkg-specifics` PyTorch guidance; install into Topic Workspace Pixi environment or record explicit fallback wiring. | Check `torch.__version__`, `torch.version.cuda`, `torch.cuda.is_available()`, and `torch.cuda.get_arch_list()` when available. |
| `nvidia-smi` | `native-runtime` | Host tool or explicit external runtime evidence; do not install by normal Python package route. | `nvidia-smi` for host GPU, driver, visible devices, memory, and active processes. |

Optional tools:

| Tool | Kind | Install Preference | Use |
| --- | --- | --- | --- |
| `triton` | `python-library` | Topic Workspace Pixi environment when compatible with selected PyTorch/CUDA. | Kernel/runtime workflows. |
| Flash Attention package | `python-library` or native build | Topic Workspace Pixi environment with package-specific evidence and bounded build guidance. | Attention kernel import or bounded runtime check. |

Routes:

- Use `isomer-misc-pkg-specifics` package `pytorch` first.
- Use `isomer-misc-nvidia-tools` for NVIDIA runtime wiring when needed.
- Use `isomer-misc-bounded-run-tips` for CUDA extension builds, GPU inference checks, or benchmarks.

Blockers:

- CUDA-required task can only reach CPU-only PyTorch.
- `torch.version.cuda` is `None` when CUDA behavior is required.
- GPU runtime checks fail on a host where immediate GPU execution is required.

## `topic-python-starter`

Purpose: provide the baseline Python packages used by Topic Workspace setup.

Required tools:

| Tool | Kind | Install Preference | Verification |
| --- | --- | --- | --- |
| `scipy` | `python-library` | Topic Workspace Pixi environment through PyPI unless already satisfied. | Import inside Topic Workspace Pixi env. |
| `mdutils` | `python-library` | Topic Workspace Pixi environment through PyPI unless already satisfied. | Import inside Topic Workspace Pixi env. |
| `ruff` | `python-library` or `cli-pypi` | If used as project library/config dependency, Topic Workspace Pixi env; if requested only as reusable CLI, prefer `uv tool install`, then `pixi global install`. | `ruff --version` or import/check command as appropriate. |
| `mkdocs-material` | `python-library` | Topic Workspace Pixi environment through PyPI unless already satisfied. | `python -c "import material"`, or docs build check when relevant. |
| `mypy` | `python-library` or `cli-pypi` | If used by project checks, Topic Workspace Pixi env; if requested only as reusable CLI, prefer `uv tool install`, then `pixi global install`. | `mypy --version`. |
| `attrs` | `python-library` | Topic Workspace Pixi environment through PyPI unless already satisfied. | Import inside Topic Workspace Pixi env. |
| `omegaconf` | `python-library` | Topic Workspace Pixi environment through PyPI unless already satisfied. | Import inside Topic Workspace Pixi env. |
| `imageio` | `python-library` | Topic Workspace Pixi environment through PyPI unless already satisfied. | Import inside Topic Workspace Pixi env. |
| `matplotlib` | `python-library` | Topic Workspace Pixi environment through PyPI unless already satisfied. | Import inside Topic Workspace Pixi env. |
| `jsonschema` | `python-library` | Topic Workspace Pixi environment through PyPI unless already satisfied. | Import inside Topic Workspace Pixi env. |
| `jinja2` | `python-library` | Topic Workspace Pixi environment through PyPI unless already satisfied. | Import inside Topic Workspace Pixi env. |

Routes:

- Use `isomer-srv-topic-env-setup` starter dependency policy for normal Topic Workspace setup.
- Use CLI route only when the user specifically asks for a reusable command-line tool rather than a topic runnable-target dependency.

Blockers:

- A starter dependency cannot be installed from PyPI or an accepted fallback source.
