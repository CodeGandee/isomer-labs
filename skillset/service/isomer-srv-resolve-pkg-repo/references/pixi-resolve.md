# Pixi Resolve

Use this subcommand to choose reachable Conda channels for Pixi installations.

## Required Inputs

Recover these before running the workflow:

| Input | Resolution |
| --- | --- |
| Package context | The package name(s) or matchspec(s) the user wants to install, or the derived gate entry that names them. |
| NVIDIA signal | Whether any requested package is an NVIDIA/CUDA package. Treat packages whose names start with `cuda`, `cudnn`, `nccl`, `nvidia`, `libnv`, `libnpp`, `libcu`, or `nvtx`, or whose summary mentions NVIDIA CUDA, as NVIDIA packages. |
| Pixi manifest | Optional. `manifest_path` when the install must target a specific Topic Workspace Pixi manifest. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Test official conda-forge reachability**:
   - Send a lightweight HTTP request such as `curl -I --max-time 10 https://conda.anaconda.org/conda-forge/` or run `pixi search --channel conda-forge --limit 1 _libgcc_mutex`.
   - If the command succeeds and returns a usable channel index, mark `conda-forge` as reachable.
2. **If conda-forge is reachable and no NVIDIA packages are involved**, recommend `conda-forge` as the primary channel. Stop and report the result.
3. **If NVIDIA packages are involved**, also test the `nvidia` channel:
   - Use `curl -I --max-time 10 https://conda.anaconda.org/nvidia/` or `pixi search --channel nvidia --limit 1 cuda-version`.
   - If the `nvidia` channel is reachable, recommend `nvidia` first and `conda-forge` second.
   - Record that the NVIDIA channel is preferred for NVIDIA packages.
   - Stop and report the result.
4. **If official conda-forge is not reachable**, inspect local Conda configuration for declared mirrors or channels. See **Local Conda Config Discovery**.
5. **Test each candidate channel** discovered in local config:
   - Use declaration order and the same reachability tests.
   - Mark the first reachable candidate as the recommended mirror and stop.
6. **If no candidate is reachable**, report that `conda-forge` is not usable and stop with a blocker. Do not fall back to an unverified source.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the package context, NVIDIA signal, local config, and reachability tests, then execute the plan.

## Local Conda Config Discovery

Read Conda configuration from the user's home directory in this priority:

1. `~/.condarc`
2. `~/.conda/condarc`
3. `~/.conda/condarc.d/*.condarc` in sorted filename order

Parse YAML content and extract:

- `channels`: list of channel names or URLs to try in order.
- `default_channels`: list of default channel URLs when `defaults` is referenced.
- `custom_channels`: mapping from short channel names to full URLs.
- `show_channel_urls`: when true, prefer explicit URLs over short names.

Resolve short channel names to URLs using Conda's conventional mapping when `custom_channels` does not override them:

- `conda-forge` → `https://conda.anaconda.org/conda-forge/`
- `nvidia` → `https://conda.anaconda.org/nvidia/`
- `defaults` → the URLs in `default_channels`, or `https://repo.anaconda.com/pkgs/main`, `https://repo.anaconda.com/pkgs/r`, and `https://repo.anaconda.com/pkgs/msys2` when `default_channels` is absent.

Only use channels the user has explicitly declared. Do not invent mirrors.

## Reachability Test

A channel is reachable when at least one of these succeeds:

- `curl -I --max-time 10 --location <channel-url>/` returns HTTP 200 or 302 to a reachable endpoint.
- `pixi search --channel <channel-name-or-url> --limit 1 _libgcc_mutex` exits 0 and prints package metadata.

When a manifest is known, you may also test with `pixi project channel add --manifest-path <manifest_path> <channel-name-or-url>` followed by `pixi install --manifest-path <manifest_path> --dry-run` if the previous tests are inconclusive, but prefer the lightweight tests first.

## Output Contract

Report:

- `subcommand`: `pixi-resolve`.
- `official_conda_forge_reachable`: `true`, `false`, or `not tested`.
- `nvidia_channel_reachable`: `true`, `false`, or `not tested`.
- `nvidia_packages_requested`: list of detected NVIDIA package names or `none`.
- `local_config_paths`: files read and whether each was found.
- `local_config_channels`: channels declared in local config, in order, with resolved URLs.
- `recommended_channels`: ordered list of channels to use, with rationale for each.
- `tested_channels`: each candidate, reachability result, and reason for rejection when applicable.
- `manifest_path`: targeted Pixi manifest when provided.
- `blockers`: missing package context, no reachable channel, ambiguous NVIDIA signal, or network failure.
- `next_action`: add channels to the Pixi manifest, proceed with install, inspect local network config, or stop.

## Blockers

Report `blocked` when:

- no package context is available and the user has not asked for a general channel recommendation;
- official conda-forge is unreachable and no local config declares reachable channels;
- every declared local channel is unreachable;
- the `nvidia` channel is required for NVIDIA packages but unreachable, and no suitable fallback channel is reachable;
- the network test itself cannot run because required tools are missing.
