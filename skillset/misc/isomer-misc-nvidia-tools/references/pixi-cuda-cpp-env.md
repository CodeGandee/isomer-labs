# pixi-cuda-cpp-env

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Resolve the Pixi project**. Identify the project path, the manifest file (`pixi.toml` or `pyproject.toml`), and the target Pixi environment. Default to the current working directory and `default` only when the local evidence supports that choice.
2. **Resolve CUDA requirements**. Identify the requested CUDA version and whether optional libraries or tools such as `cudnn`, `nccl`, or `nsight-compute` are needed.
3. **Inspect host and manifest state**. Check host build tools (`cmake`, `ninja`, and a C++ compiler), existing CUDA packages, channel order, feature layout, pins, and `solve-group` usage before modifying the manifest.
4. **Choose the setup mode** from **Setup Modes**. Prefer an isolated environment unless the user explicitly asks to change the existing environment or the manifest is already dedicated to CUDA builds.
5. **Apply Pixi dependency changes** according to **Dependency Preferences**.
6. **Configure build tasks** according to **CMake Task Preferences**.
7. **Apply `nvcc-tips`** for architecture targets and build parallelism.
8. **Verify with a small build** according to **Verification Preference**.
9. **Report changes and caveats** using **Output Contract**.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this page, `nvcc-tips`, and the user's request, then execute the plan.

## Setup Modes

| Mode | Use When | Preference |
| --- | --- | --- |
| `isolated-env` | Existing environment has unrelated dependencies, channel order conflicts, CUDA pins, or unclear ownership | Recommended default |
| `adjust-existing-env` | User explicitly asks to fix or use the current environment, or the manifest is already a CUDA build environment | Warn about dependency impact before mutation |
| `plan-only` | User asks how to set it up, lacks required inputs, or manifest conflicts need approval | Report commands and manifest edits without applying |

For `isolated-env`, create a dedicated feature/environment name such as `cu<version>-build` or the user-provided name, and give it its own `solve-group`.

For `adjust-existing-env`, avoid rewriting broad manifest structure. Add the minimum channels, dependencies, and tasks needed for the requested build.

## Dependency Preferences

Add the `nvidia` channel before adding CUDA packages. Prefer channel-local CUDA packages from `nvidia` for `cuda-*` dependencies rather than mixing CUDA packages across channels.

Include core build dependencies when missing or unsuitable:

```bash
cmake ninja cxx-compiler make pkg-config cuda-toolkit=<version> cuda-nvcc=<version>
```

Add optional packages only when requested or clearly required:

```bash
cudnn=<version> nccl=<version> nsight-compute
```

Use Pixi commands when they can express the change clearly. If the CLI cannot express a needed environment or `solve-group` shape, edit the manifest directly and preserve existing formatting as much as practical.

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
- `channels_changed`
- `dependencies_added`
- `tasks_added_or_changed`
- `nvcc_tips_applied`
- `verification_command`
- `verification_result`
- `changed_files`
- `warnings_or_blockers`
