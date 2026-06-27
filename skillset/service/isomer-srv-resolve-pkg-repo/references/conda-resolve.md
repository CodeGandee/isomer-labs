# Conda Resolve

Use this subcommand to choose reachable channels for Conda installs.

## Required Inputs

| Input | Resolution |
| --- | --- |
| Package context | The package name(s) or spec the user wants to install. |
| NVIDIA signal | Whether any requested package is an NVIDIA/CUDA package. See `pixi-resolve` for detection rules. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Test official conda-forge reachability** with `curl -I --max-time 10 https://conda.anaconda.org/conda-forge/` or `conda search --channel conda-forge --override-channels _libgcc_mutex`.
2. **If conda-forge is reachable and no NVIDIA packages are involved**, recommend `conda-forge`.
3. **If NVIDIA packages are involved**, test the `nvidia` channel. If reachable, recommend `nvidia` first and `conda-forge` second.
4. **If conda-forge is not reachable**, read `~/.condarc`, `~/.conda/condarc`, and `~/.conda/condarc.d/*.condarc` for declared channels or mirrors. Resolve short names to URLs.
5. **Test each candidate** in declaration order and recommend the first reachable one.
6. **If no candidate is reachable**, report that conda-forge is not usable and stop with a blocker.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the package context, NVIDIA signal, local config, and reachability tests, then execute the plan.

## Output Contract

Report:

- `subcommand`: `conda-resolve`.
- `official_conda_forge_reachable`: `true`, `false`, or `not tested`.
- `nvidia_channel_reachable`: `true`, `false`, or `not tested`.
- `local_config_channels`: channels declared in local config, in order.
- `recommended_channels`: ordered list of channels to use.
- `tested_channels`: each candidate and its reachability result.
- `blockers`: missing package context or no reachable channel.
