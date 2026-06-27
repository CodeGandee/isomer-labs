# pixi-cuda-cpp-env

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Resolve the Pixi project**. Identify the project path, the manifest file (`pixi.toml` or `pyproject.toml`), and the target Pixi environment. Default to the current working directory and `default` only when the local evidence supports that choice.
2. **Resolve CUDA requirements**. Identify the requested CUDA version and whether optional libraries or tools such as `cudnn`, `nccl`, or `nsight-compute` are needed.
3. **Inspect host and manifest state**. Check host build tools (`cmake`, `ninja`, and a C++ compiler), Pixi-provided build tools and NVIDIA components, host-provided NVIDIA components, channel order, feature layout, pins, and `solve-group` usage before modifying the manifest.
4. **Choose the setup mode** from **Setup Modes**. Prefer an isolated environment unless the user explicitly asks to change the existing environment or the manifest is already dedicated to CUDA builds.
5. **Resolve C++ build tools** according to **C++ Toolchain Resolution**.
6. **Resolve NVIDIA components** according to **NVIDIA Component Resolution**.
7. **Configure build tasks** according to **CMake Task Preferences**.
8. **Apply `nvcc-tips`** for architecture targets and build parallelism.
9. **Verify with a small build** according to **Verification Preference**.
10. **Report changes and caveats** using **Output Contract**.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this page, `nvcc-tips`, and the user's request, then execute the plan.

## Setup Modes

| Mode | Use When | Preference |
| --- | --- | --- |
| `isolated-env` | Existing environment has unrelated dependencies, channel order conflicts, CUDA pins, or unclear ownership | Recommended default |
| `adjust-existing-env` | User explicitly asks to fix or use the current environment, or the manifest is already a CUDA build environment | Warn about dependency impact before mutation |
| `plan-only` | User asks how to set it up, lacks required inputs, or manifest conflicts need approval | Report commands and manifest edits without applying |

For `isolated-env`, create a dedicated feature/environment name such as `cu<version>-build` or the user-provided name, and give it its own `solve-group`.

For `adjust-existing-env`, avoid rewriting broad manifest structure. Add the minimum channels, dependencies, and tasks needed for the requested build.

## C++ Toolchain Resolution

If `cmake`, `ninja`, `make`, `pkg-config`, or a C++ compiler is missing or unsuitable, resolve build tools in this order:

1. **Install through Pixi from `conda-forge`**. Prefer Pixi-managed packages such as `cmake`, `ninja`, `cxx-compiler`, `make`, and `pkg-config` from `conda-forge` so the build environment remains user-space and reproducible.
2. **Use a vendor-specific Conda channel when official docs recommend one**. If `conda-forge` does not provide the needed tool or version, check the tool's official documentation for a vendor-maintained Conda channel. Add that channel to the Pixi environment and install the tool from there when available.
3. **Use official binary downloads in a temporary local directory**. If Pixi cannot provide a suitable tool, get a binary release from the tool's official source and place it in a project-local temporary directory such as `tmp/`, `temp/`, or another existing project temp area. If no project-local temp directory exists, use the system temp directory. Wire the binary into Pixi-run commands explicitly and record the path.
4. **Produce user guidance for system package installation when sudo is required**. If the remaining path appears to require privileged package installation, system compiler packages, system repositories, `/usr/local`, or other machine-level changes, stop and write exact guidance for the user. Do not run `sudo` from this workflow.

## NVIDIA Component Resolution

Resolve NVIDIA components in this order:

1. **Use Pixi-provided components already present in the target environment**. If the target Pixi environment already provides a suitable component, keep it and avoid adding duplicate host wiring or packages.
2. **Introduce host-provided components into Pixi execution when suitable**. If the host system already has the needed component, such as a compatible CUDA Toolkit, `nvcc`, driver library, Nsight tool, `cudnn`, or `nccl`, try to wire it explicitly into Pixi-run commands or tasks. Record the exact paths and environment variables used, such as `CUDA_HOME`, `CUDACXX`, `PATH`, `LD_LIBRARY_PATH`, `CMAKE_CUDA_COMPILER`, `CUDAToolkit_ROOT`, or package-specific include/library paths.
3. **Install through Pixi from the `nvidia` channel if host wiring fails or is unsuitable**. Add the `nvidia` channel before adding CUDA packages. Prefer channel-local NVIDIA packages for `cuda-*` dependencies rather than mixing CUDA packages across channels.
4. **Produce user guidance for system package installation when Pixi and host wiring cannot satisfy the need**. If the remaining path appears to require `sudo`, kernel drivers, system repositories, `/usr/local` installation, daemon restarts, or other machine-level package work, stop and write exact guidance for the user to run outside the skill. Do not perform privileged system installation from this workflow.

Core build dependencies, when resolved through Pixi, usually include:

```bash
cmake ninja cxx-compiler make pkg-config cuda-toolkit=<version> cuda-nvcc=<version>
```

Optional NVIDIA packages should be resolved through the same ladder and added only when requested or clearly required:

```bash
cudnn=<version> nccl=<version> nsight-compute
```

Use Pixi commands when they can express the change clearly. If the CLI cannot express a needed environment or `solve-group` shape, edit the manifest directly and preserve existing formatting as much as practical.

Treat the NVIDIA driver as a host component. Do not try to install GPU drivers with Pixi.

## CMake Task Preferences

Prefer explicit Pixi-managed CUDA paths so CMake does not pick up a host `nvcc`.

Use the manifest's task style, but keep these settings:

```toml
configure = { cmd = "cmake -G Ninja -S . -B build -DCMAKE_CUDA_COMPILER=$CONDA_PREFIX/bin/nvcc -DCUDAToolkit_ROOT=$CONDA_PREFIX", env = { CUDACXX = "$CONDA_PREFIX/bin/nvcc" } }
build = "cmake --build build"
test = "ctest --test-dir build"
```

Adjust task names only to fit existing project conventions.

## Verification Preference

Use a small CUDA/C++ build check when the project lacks a targeted verification command. Place temporary verification material under `tmp/build-check` when `tmp/` exists, otherwise under `build-check`.

Treat compile success separately from runtime success. On a host without a compatible GPU driver, the build may succeed while execution fails. In that case, confirm the compiled binary or library exists and report the driver/runtime caveat.

## Output Contract

Report:

- `project_path`
- `manifest_file`
- `target_environment`
- `cuda_version`
- `setup_mode`
- `cpp_toolchain_source`
- `channels_changed`
- `pixi_components_reused`
- `host_components_wired`
- `dependencies_added`
- `system_install_guidance`
- `tasks_added_or_changed`
- `nvcc_tips_applied`
- `verification_command`
- `verification_result`
- `changed_files`
- `warnings_or_blockers`
