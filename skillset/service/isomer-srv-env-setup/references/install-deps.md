# Install Dependencies

Use this subcommand to install dependencies for the derived gate through the Topic Workspace Pixi environment.

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**: workspace context from `resolve-workspace` and `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md` from `derive-gate`.
2. **Read `isomer-env-gate.md`** and stop with blockers when its `## Blockers` section contains unresolved install blockers.
3. **Ensure the Topic Workspace Pixi manifest exists** at `manifest_path`. If the active binding expects `<topic-workspace-dir>/pixi.toml` and it is missing, create a minimal Pixi manifest for the Topic Workspace with Python and appropriate channels before adding target dependencies.
4. **Keep Python available** as the Topic Workspace root glue and orchestration language, even when the runnable target uses another language.
5. **Install Python packages from PyPI by default** with `pixi add --manifest-path <manifest_path> --pypi <requirement>` when PyPI can satisfy the gate.
6. **Install native or Conda-required dependencies through Pixi/Conda** with `pixi add --manifest-path <manifest_path> <matchspec>` when the dependency is a non-Python tool, command-line program, binary or system-level runtime dependency, unavailable or unsuitable on PyPI, or required by setup instructions that PyPI cannot satisfy.
7. **Prefer the NVIDIA channel** for NVIDIA tools and runtime packages by adding it with `pixi workspace channel add --manifest-path <manifest_path> --prepend nvidia` before adding those packages. Record any fallback to `conda-forge` or another channel.
8. **Install editable repo packages when needed** using a PyPI editable requirement such as `pixi add --manifest-path <manifest_path> --pypi --editable '<package-name> @ file://<absolute-repo-path>'` when the repo is Python-installable and the gate needs it importable.
9. **Install the selected environment** with `pixi install --manifest-path <manifest_path> --environment <pixi_environment>`.
10. **Update `isomer-env-gate.md`** with commands run, selected package sources, changed files, channel decisions, blockers, and execution log entries.
11. **Report the install result** using the parent skill's output fields.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from `isomer-env-gate.md`, dependency policy, Pixi help, parent guardrails, and user request, then execute the plan.

## Minimal Pixi Manifest

Use this shape only when the active binding expects a missing `pixi.toml` in the selected Topic Workspace:

```toml
[workspace]
name = "<research_topic_id>"
channels = ["conda-forge"]
platforms = ["linux-64"]

[dependencies]
python = "3.11.*"
```

Adjust platforms when the current host or Project Manifest requires a different platform. Add `nvidia` with `--prepend` when NVIDIA packages are needed.

## Package Source Policy

| Dependency Kind | Preferred Source |
| --- | --- |
| Normal Python package | PyPI through `pixi add --pypi` |
| Python package unsuitable or unavailable on PyPI | Pixi/Conda with reason recorded |
| Non-Python command-line tool | Pixi/Conda |
| Binary/runtime/system dependency | Pixi/Conda |
| NVIDIA tool or runtime package | Pixi with `nvidia` channel before `conda-forge` |
| Installable local Python repo | PyPI editable file requirement |

## Blockers

Report `blocked` when:

- the derived gate is missing;
- `manifest_path` is not resolved from the active binding;
- a dependency cannot be inferred, resolved, or installed;
- a Python package must use Pixi/Conda but the reason is unknown;
- a channel or package source cannot be reached;
- the desired dependency would mutate the Project-root Pixi environment or an Agent Workspace-specific environment.
