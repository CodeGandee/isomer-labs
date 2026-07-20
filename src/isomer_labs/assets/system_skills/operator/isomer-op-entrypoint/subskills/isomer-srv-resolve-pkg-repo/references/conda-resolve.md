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

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

### Essential Output

Recommend the ordered Conda channels and state whether they are reachable, blocked, or untested. Name missing package context or the absence of a reachable channel as a blocker.

### Complete Output

Group the complete explanation by conda-forge and NVIDIA reachability, locally configured and tested channels, the ordered recommendation, and blockers.
