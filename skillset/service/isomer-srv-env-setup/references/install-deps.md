# Install Dependencies

Use this subcommand to install dependencies for the derived gate through the Topic Workspace Pixi environment.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Workspace context | Require `project_root`, `research_topic_id`, `topic_workspace_dir`, `manifest_path`, and `pixi_environment` from `resolve-workspace`. Refuse to run if any value is missing, and tell the user to run `resolve-workspace` first. |
| Derived gate | Require `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md` from `derive-gate`. Refuse to run if it is missing, and tell the user to run `derive-gate` first. |
| Dependency plan, enclosure strategy, and Pixi install commands | Read from the derived gate's `## Dependency Plan` and `## Pixi Install Commands` sections, including the selected Python version, version evidence, starter Python dependencies, enclosure classification, and command style. Stop with blockers when the plan is missing, contradictory, still blocked, or missing enclosure strategy for a required dependency or runtime need. |
| Package-source override | Optional. Use only when the prompt or derived gate explicitly names a package source override; otherwise follow the PyPI-first Python and NVIDIA-channel policies in this page. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**: workspace context from `resolve-workspace` and `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md` from `derive-gate`.
2. **Read `isomer-env-gate.md`** and stop with blockers when its `## Blockers` section contains unresolved install blockers.
3. **Check enclosure classification** from the derived gate's `## Dependency Plan`. Every required dependency or runtime need must be classified as Pixi-managed, Pixi-mediated external runtime wiring, topic-local user-space fallback, or blocked. If any required item is unclassified, stop and report a blocker asking to update `isomer-env-gate.md` before mutation.
4. **Resolve the selected Python version** from the derived gate. If the derived gate does not already contain a usable selection, apply **Python Version Policy** before mutating the Pixi manifest and update the derived gate with the selected version and evidence.
5. **Ensure the Topic Workspace Pixi manifest exists** at `manifest_path`. If the active binding expects `<topic-workspace-dir>/pixi.toml` and it is missing, create a minimal Pixi manifest for the Topic Workspace with the selected Python version and appropriate channels before adding target dependencies.
6. **Ensure Topic Workspace VCS ignores** by creating or updating `<topic-workspace-dir>/.gitignore` with `.pixi/`, `tmp/`, and `.git/`. Add `.isomer-user-env/` only when topic-local fallback is used. Do not add `extern/orphan` ignore entries from this skill.
7. **Keep Python available** as the Topic Workspace root glue and orchestration language, even when the runnable target uses another language.
8. **Install Pixi-managed starter Python dependencies** through PyPI when missing or not already satisfied: `pixi add --manifest-path <manifest_path> --pypi scipy mdutils ruff mkdocs-material mypy attrs omegaconf imageio matplotlib jsonschema jinja2`.
9. **Install Pixi-managed Python packages from PyPI by default** with `pixi add --manifest-path <manifest_path> --pypi <requirement>` when PyPI can satisfy the gate.
10. **Install Pixi-managed native or Conda-required dependencies through Pixi/Conda** with `pixi add --manifest-path <manifest_path> <matchspec>` when the dependency is a non-Python tool, command-line program, binary or system-level runtime dependency, unavailable or unsuitable on PyPI, or required by setup instructions that PyPI cannot satisfy.
11. **Prefer the NVIDIA channel** for NVIDIA tools and runtime packages by adding it with `pixi workspace channel add --manifest-path <manifest_path> --prepend nvidia` before adding those packages. Record any fallback to `conda-forge` or another channel.
12. **Install editable repo packages when needed** using a PyPI editable requirement such as `pixi add --manifest-path <manifest_path> --pypi --editable '<package-name> @ file://<absolute-repo-path>'` when the repo is Python-installable and the gate needs it importable.
13. **Record Pixi-mediated external runtime wiring** when the derived gate requires an external runtime path, sourced script, compiler path, package-config path, CUDA variable, or library path. Do not mutate the host; record the exact variables or source commands and use them only inside `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <command>`.
14. **Use topic-local fallback only when justified** by the derived gate. Place fallback material under `<topic-workspace-dir>/.isomer-user-env/`, update `.gitignore`, run fallback setup through Pixi-scoped commands when commands are needed, and record the lower-portability warning.
15. **Run setup commands through the Topic Workspace Pixi environment** when the derived gate requires commands beyond dependency mutation: `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <command>`. Include any recorded runtime wiring in the command instead of relying on ambient shell state.
16. **Install the selected environment** with `pixi install --manifest-path <manifest_path> --environment <pixi_environment>`.
17. **Update `isomer-env-gate.md`** with commands run, selected Python version, version evidence, starter dependencies, VCS ignore changes, adaptation decisions, selected package sources, enclosure classification, external runtime wiring, topic-local fallbacks, changed files, channel decisions, blockers, and execution log entries.
18. **Report the install result** using the parent skill's output fields.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from `isomer-env-gate.md`, dependency policy, Pixi help, parent guardrails, and user request, then execute the plan.

## Minimal Pixi Manifest

Use this shape only when the active binding expects a missing `pixi.toml` in the selected Topic Workspace:

```toml
[workspace]
name = "<research_topic_id>"
channels = ["conda-forge"]
platforms = ["linux-64"]

[dependencies]
python = "<selected-python-minor>.*"
```

Adjust platforms when the current host or Project Manifest requires a different platform. Add `nvidia` with `--prepend` when NVIDIA packages are needed.

## Python Version Policy

Recover Python version evidence from the prompt, `env-gate.md`, the derived gate, and inspected repos before editing `pixi.toml`. Useful evidence includes `requires-python`, `python_requires`, requirement markers, `.python-version`, `runtime.txt`, `tox.ini`, `noxfile.py`, CI files, Dockerfiles, lockfiles, README setup notes, and package-manager config.

If the version is unspecified or cannot be recovered from existing context, choose the previous stable Python minor release relative to the latest stable Python release at execution time. For example, if the latest stable line is `3.N`, select `3.(N-1)`; do not choose a prerelease and do not hard-code this fallback in the skill.

If multiple sources conflict, choose the highest Python minor version mentioned or required by those sources as the target. Then adapt requirements to that version by selecting compatible package releases, loosening environment-only pins when safe, adding compatibility shims, or changing setup commands. Do not mutate existing repo source files merely to force compatibility. If adaptation cannot be done within the service-safe environment setup boundary, report a blocker that names the conflicting sources and the attempted target version.

## Package Source Policy

| Dependency Kind | Preferred Source |
| --- | --- |
| Python runtime | Selected Python minor version from **Python Version Policy** |
| Starter Python dependencies | PyPI through `pixi add --manifest-path <manifest_path> --pypi scipy mdutils ruff mkdocs-material mypy attrs omegaconf imageio matplotlib jsonschema jinja2` |
| Normal Python package | PyPI through `pixi add --pypi` |
| Python package unsuitable or unavailable on PyPI | Pixi/Conda with reason recorded |
| Non-Python command-line tool | Pixi/Conda |
| Binary/runtime/system dependency | Pixi/Conda |
| NVIDIA tool or runtime package | Pixi with `nvidia` channel before `conda-forge` |
| Installable local Python repo | PyPI editable file requirement |

## Environment Enclosure Ladder

Apply this ladder before installing or verifying any dependency or runtime need:

1. **Pixi-managed install**: install through `pixi add --manifest-path <manifest_path> --pypi ...`, `pixi add --manifest-path <manifest_path> ...`, or `pixi install --manifest-path <manifest_path> --environment <pixi_environment>`.
2. **Pixi-mediated external runtime wiring**: when Pixi cannot reasonably provide a needed DLL, SO, SDK, compiler, CUDA runtime, activation script, package-config path, or library path, use that external piece only through recorded `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...` commands.
3. **Topic-local user-space fallback**: when Pixi-managed installation and external runtime wiring cannot satisfy the gate, materialize fallback files under `<topic-workspace-dir>/.isomer-user-env/`, record commands and paths, and warn that the result is less portable than Pixi-managed setup.
4. **Blocker**: when setup would require `sudo`, apt/yum/brew or another system package manager mutation, global shell profile edits, global Python or Node package installs, `/etc` changes, `ldconfig`, daemons, kernel driver changes, or another privileged or machine-global action.

## Runtime Wiring Policy

External runtime wiring must be explicit and replayable. Record the exact source script, runtime path, environment variable, and reason in `isomer-env-gate.md`, then run commands through Pixi. Common variables include `PATH`, `LD_LIBRARY_PATH`, `DYLD_LIBRARY_PATH` when applicable, `CPATH`, `LIBRARY_PATH`, `PKG_CONFIG_PATH`, and `CUDA_HOME`.

Do not treat a tool found in the ambient shell as ready unless the derived gate records how it is made available through the Pixi-scoped command. A valid verification or setup command may use a form like:

```bash
pixi run --manifest-path <manifest_path> --environment <pixi_environment> bash -lc 'source <script> && export LD_LIBRARY_PATH=<path>:$LD_LIBRARY_PATH && <command>'
```

## Topic-Local Fallback Policy

Use `<topic-workspace-dir>/.isomer-user-env/` only after Pixi-managed installation and Pixi-mediated runtime wiring are insufficient. Preserve all fallback commands and installed paths in `isomer-env-gate.md`, add `.isomer-user-env/` to the Topic Workspace `.gitignore`, and report a lower-portability warning in the final output.

## VCS Ignore Policy

Ensure `<topic-workspace-dir>/.gitignore` contains these baseline Isomer environment setup ignore entries when missing:

```gitignore
.pixi/
tmp/
.git/
```

When topic-local fallback is used, also add:

```gitignore
.isomer-user-env/
```

Preserve unrelated existing ignore entries. Do not add an `extern/orphan` ignore entry from this skill.

## Command Style

Run Topic Workspace setup, inspection, and verification commands inside the prepared environment with:

```bash
pixi run --manifest-path <manifest_path> --environment <pixi_environment> <command>
```

Use `pixi add --manifest-path <manifest_path> ...` and `pixi install --manifest-path <manifest_path> --environment <pixi_environment>` for dependency mutation and installation. Do not rely on activated shells or ambient Python environments.

Explicit external runtime wiring is allowed only inside recorded Pixi-run commands. Do not use an already activated shell, unrecorded PATH entry, unrecorded library path, or global package as proof of setup.

## Blockers

Report `blocked` when:

- the derived gate is missing;
- `manifest_path` is not resolved from the active binding;
- the selected Python version is missing from the derived gate and cannot be recovered or selected by policy;
- Python version conflicts cannot be adapted within the service-safe environment setup boundary;
- a starter Python dependency cannot be resolved or installed;
- a dependency cannot be inferred, resolved, or installed;
- a required dependency or runtime need lacks an enclosure strategy in `isomer-env-gate.md`;
- a Python package must use Pixi/Conda but the reason is unknown;
- a channel or package source cannot be reached;
- the desired dependency would mutate the Project-root Pixi environment or an Agent Workspace-specific environment;
- the setup requires `sudo`, system package manager mutation, global shell profile edits, global Python or Node package installs, `/etc` changes, `ldconfig`, daemons, kernel driver changes, or another privileged or machine-global action.
