# Package Source Preference

## Decision

For Python packages, `isomer-srv-env-setup` should prefer PyPI over Pixi/Conda packages by default. The workflow should use Pixi/Conda packages when Conda is clearly required for the gate to pass, such as for non-Python tools, binary or system-level runtime dependencies, packages unavailable or unsuitable on PyPI, or repo setup instructions that cannot be satisfied through PyPI.

The workflow should include starter Python dependencies through PyPI unless existing compatible constraints already provide them: `scipy`, `mdutils`, `ruff`, `mkdocs-material`, `mypy`, `attrs`, `omegaconf`, `imageio`, `matplotlib`, `jsonschema`, and `jinja2`.

For NVIDIA tools and runtime packages that need a Pixi channel, the workflow should prefer the `nvidia` channel over `conda-forge`.

## Rationale

Most Python projects publish primary installable packages through PyPI. A PyPI-first default keeps Python dependency inference close to common Python packaging expectations, while preserving Conda/Pixi for packages that need compiled runtime support, command-line tools, or non-Python system packages. NVIDIA packages are a special channel preference because the `nvidia` channel is the intended source for many NVIDIA-maintained CUDA and GPU runtime packages.

## Dependency Plan Impact

The generated `isomer-env-gate.md` should record the starter dependency command and the selected package source for each inferred dependency. If the workflow chooses Pixi/Conda instead of PyPI for a Python dependency, it should briefly explain why PyPI was not used. If the workflow uses an NVIDIA package through Pixi, it should record that the `nvidia` channel was preferred and note any fallback to `conda-forge` or another channel.

## Boundaries

This preference affects Topic Workspace environment setup only. It does not change Isomer Labs' own project dependencies or the repository-level Pixi environment used to run `isomer-cli`.
