# Conda Resolve

Use this subcommand to choose reachable channels for Conda installs.

## Required Inputs

| Input | Resolution |
| --- | --- |
| Package context | The package name(s) or spec the user wants to install. |
| NVIDIA signal | Whether any requested package is an NVIDIA/CUDA package. See `pixi-resolve` for detection rules. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Test official conda-forge reachability**:
   - Use `curl -I --max-time 10 https://conda.anaconda.org/conda-forge/` or `conda search --channel conda-forge --override-channels _libgcc_mutex`.
2. **If conda-forge is reachable and no NVIDIA packages are involved**, recommend `conda-forge`.
3. **If NVIDIA packages are involved**, test the `nvidia` channel. If reachable, recommend `nvidia` first and `conda-forge` second.
4. **If conda-forge is not reachable**, read local Conda configuration:
   - Check `~/.condarc`, `~/.conda/condarc`, and `~/.conda/condarc.d/*.condarc` for declared channels or mirrors.
   - Resolve short names to URLs.
5. **Test each candidate** in declaration order and recommend the first reachable one.
6. **If no candidate is reachable**, report that conda-forge is not usable and stop with a blocker.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the package context, NVIDIA signal, local config, and reachability tests, then execute the plan.

## Output Contract

Default to **Essential Output** in chat. Print **Complete Output** only when the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output.

### Essential Output

- `subcommand`: `conda-resolve`.
- `recommended_channels`: ordered list of channels to use.
- `status`: reachable, blocked, or not tested.
- `blockers`: missing package context or no reachable channel.

### Complete Output

- `official_conda_forge_reachable`
- `nvidia_channel_reachable`
- `local_config_channels`
- `recommended_channels`
- `tested_channels`
- `blockers`
