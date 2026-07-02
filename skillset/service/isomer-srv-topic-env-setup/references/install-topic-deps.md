# Install Topic Deps

Use this subcommand to install dependencies for the derived gate through the Topic Workspace Pixi environment. For an ad hoc package-add request from a user or research skill, route to `$isomer-admin-topic-workspace-mgr install-packages` instead of calling this page directly.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Workspace context | Require `project_root`, `research_topic_id`, `topic_workspace_dir`, `manifest_path_or_dir`, `manifest_path`, and `pixi_environment` from `resolve-topic-workspace`. Refuse to run if any value is missing, and tell the user to run `resolve-topic-workspace` first. |
| Topic env target spec | Require resolved `topic.env.topic_setup_target_spec` from `derive-env-gate`, whether derived from source intent or supplied as an explicit manual target spec. Refuse to run if it is missing, and tell the user to run `derive-env-gate` first. |
| Dependency plan, resource check plan, enclosure strategy, and Pixi install commands | Read from the target spec's `## Dependency Plan`, `## Resource Check Plan`, and `## Pixi Install Commands` sections, including Python version evidence, enclosure classification, operation classification evidence, bounded-run guidance source when required, generic best-effort fallback evidence when used, and command style. Stop with blockers when the plan is missing, contradictory, still blocked, missing classification evidence for a resource-relevant setup command, missing bounded guidance for `heavy` or `unknown-risk`, or missing enclosure strategy for a required dependency or runtime need. |
| Package-source override or resolution evidence | Optional. Use only when the prompt or derived gate explicitly names a package source override, when package-specific rules from `isomer-misc-pkg-specifics` apply, or when `isomer-srv-resolve-pkg-repo` evidence is needed because repository, mirror, registry, or channel reachability is uncertain. Otherwise follow **Package Installation Routing** in this page. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**:
   - Require workspace context from `resolve-topic-workspace` and resolved `topic.env.topic_setup_target_spec` from `derive-env-gate`.
   - If the caller supplied only a package-add request without a derived target spec or full environment setup intent, stop and route to `$isomer-admin-topic-workspace-mgr install-packages`.
2. **Read the target spec** and stop with blockers when its `## Blockers` section contains unresolved install blockers.
3. **Check enclosure classification** from the target spec's `## Dependency Plan`:
   - Every required dependency or runtime need must be classified as Pixi-managed, Pixi-mediated external runtime wiring, topic-local user-space fallback, or blocked.
   - If any required item is unclassified, stop and report a blocker asking to update `topic.env.topic_setup_target_spec` before mutation.
4. **Resolve the selected Python version** from the target spec:
   - If the target spec does not already contain a usable selection, apply **Python Version Policy** before mutating the Pixi manifest.
   - Update the target spec with the selected version and evidence.
5. **Confirm the resolved Topic Workspace Pixi manifest exists** at `manifest_path`:
   - Do not create a missing manifest in this subcommand.
   - `resolve-topic-workspace` must have already used Pixi to resolve an explicit file target, explicit directory target, or the implicit Topic Workspace directory default.
6. **Ensure Topic Workspace VCS ignores**:
   - Create or update `<topic-workspace-dir>/.gitignore` with `.pixi/`, `tmp/`, and `.git/`.
   - Add `.isomer-user-env/` only when topic-local fallback is used.
   - Do not add `extern/orphan` ignore entries from this skill.
7. **Keep Python available** as the Topic Workspace root glue and orchestration language, even when the runnable target uses another language.
8. **Install Pixi-managed starter Python dependencies** through PyPI when missing or not already satisfied:
   - Use `pixi add --manifest-path <manifest_path> --pypi scipy mdutils ruff mkdocs-material mypy attrs omegaconf imageio matplotlib jsonschema jinja2`.
9. **Route package installation decisions**:
   - For each named package or library, first check whether `isomer-misc-pkg-specifics` is available in the skillset. If it exists and lists specific rules for that package, follow those rules before applying this page's generic source ladder.
   - If package-specific rules do not apply and the package concerns NVIDIA official packages, prefer the `nvidia` Conda channel, then PyPI, then `conda-forge`. Record evidence for each skipped source.
   - If package-specific rules do not apply and the dependency is a Python library, try PyPI first. Only use `conda-forge` after PyPI cannot satisfy the requirement. If `conda-forge` cannot satisfy it, scan the Project and Topic Workspace for an installable Python package source. If no project-local source can satisfy it, inspect system Python and introduce it into the Pixi environment only through explicit, recorded fallback wiring or a local artifact.
   - Do not skip a source-ladder step without evidence in `topic.env.topic_setup_target_spec`.
10. **Install Pixi-managed Python packages from the selected source**:
   - Use `pixi add --manifest-path <manifest_path> --pypi <requirement>` when PyPI is the selected source.
   - Use package-specific commands when `isomer-misc-pkg-specifics` selects an official source, special index, wheelhouse, or fallback.
   - If PyPI, mirror, private-index, local package store, or source reachability is uncertain, use `isomer-srv-resolve-pkg-repo` evidence before mutating the manifest.
11. **Install Pixi-managed native or Conda-required dependencies through Pixi/Conda**:
   - Use `pixi add --manifest-path <manifest_path> <matchspec>` when the dependency is a non-Python tool, command-line program, binary or system-level runtime dependency, unavailable or unsuitable on PyPI, or required by setup instructions that PyPI cannot satisfy.
12. **Prefer resolved NVIDIA package sources** for NVIDIA tools and runtime packages:
   - When the derived gate or package-resolution evidence selects the `nvidia` channel, add it with `pixi workspace channel add --manifest-path <manifest_path> --prepend nvidia` before adding those packages.
   - For NVIDIA official packages, use `nvidia` channel first, PyPI second, and `conda-forge` third unless package-specific rules say otherwise.
   - Record any fallback to PyPI, `conda-forge`, or another channel.
   - If CUDA architecture targets, `nvcc` flags, or build parallelism need interpretation, use `isomer-misc-bounded-run-tips` subcommand `cuda-compile` evidence before converting them into setup commands.
   - If CUDA/C++ Pixi environment choices or NVIDIA package/runtime wiring need interpretation, use `isomer-misc-nvidia-tools` evidence.
13. **Record package-specific installation evidence when needed**:
   - Use the selected `isomer-misc-pkg-specifics` page when a named library has known package-source choices, CPU/GPU variants, platform constraints, accelerator runtimes, or runtime checks.
   - Record the selected package-specific reference and evidence in the target spec.
   - If the package-specific reference reports that the installed variant cannot satisfy the gate, report a blocker instead of accepting generic install success.
14. **Install editable repo packages when needed**:
   - Use a PyPI editable requirement such as `pixi add --manifest-path <manifest_path> --pypi --editable '<package-name> @ file://<absolute-repo-path>'` when the repo is Python-installable and the gate needs it importable.
15. **Record Pixi-mediated external runtime wiring**:
   - Apply this when the target spec requires an external runtime path, sourced script, compiler path, package-config path, CUDA variable, or library path.
   - Do not mutate the host.
   - Record the exact variables or source commands and use them only inside `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <command>`.
16. **Use topic-local fallback only when justified** by the target spec:
   - Place fallback material under `<topic-workspace-dir>/.isomer-user-env/`.
   - Update `.gitignore`.
   - Run fallback setup through Pixi-scoped commands when commands are needed.
   - Record the lower-portability warning.
17. **Check resources before classified risky setup commands**:
   - Apply this when the target spec classifies a setup command as `heavy` or `unknown-risk`.
   - Treat `## Resource Check Plan` as the execution contract.
   - Require classification source, result, reason, resource dimensions, bounded-run guidance source, bounded command, expected result, and blocker condition.
   - If classification evidence or required bounded guidance is missing, stop with a blocker and ask for `derive-env-gate` to repair `topic.env.topic_setup_target_spec`.
   - Use lightweight read-only probes such as CPU load, available memory, available disk space, and GPU availability or active GPU processes when relevant.
   - Run the bounded real setup path named by the target spec, such as reduced build parallelism, a selected native-extension target, sample data, reduced model/input size, or metadata-limited acquisition when that path is needed to make later verification meaningful.
   - If capacity is insufficient, unclear, or already busy, do not substitute an unrelated smoke test for the required setup path; record `resource_check_status: blocked` with the reason and the smallest real-path command that would be run when capacity is available.
18. **Run setup commands through the Topic Workspace Pixi environment** when the target spec requires commands beyond dependency mutation:
   - Use `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <command>`.
   - Include any recorded runtime wiring in the command instead of relying on ambient shell state.
19. **Install the selected environment** with `pixi install --manifest-path <manifest_path> --environment <pixi_environment>`.
20. **Update `topic.env.topic_setup_target_spec`**:
   - Include commands run, selected Python version, version evidence, starter dependencies, VCS ignore changes, adaptation decisions, selected package sources, resource check evidence, bounded real-path execution decisions, enclosure classification, external runtime wiring, topic-local fallbacks, changed files, channel decisions, blockers, and execution log entries.
21. **Report the install result** using the parent skill's output fields.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the resolved `topic.env.topic_setup_target_spec`, dependency policy, Pixi help, parent guardrails, and user request, then execute the plan.

## Python Version Policy

Recover Python version evidence from the prompt, resolved `topic.intent.topic_env_requirements`, explicit target spec input, resolved `topic.env.topic_setup_target_spec`, and inspected repos before editing `pixi.toml`. Useful evidence includes `requires-python`, `python_requires`, requirement markers, `.python-version`, `runtime.txt`, `tox.ini`, `noxfile.py`, CI files, Dockerfiles, lockfiles, README setup notes, and package-manager config.

If the version is unspecified or cannot be recovered from existing context, choose the previous stable Python minor release relative to the latest stable Python release at execution time. For example, if the latest stable line is `3.N`, select `3.(N-1)`; do not choose a prerelease and do not hard-code this fallback in the skill.

If multiple sources conflict, choose the highest Python minor version mentioned or required by those sources as the target. Then adapt requirements to that version by selecting compatible package releases, loosening environment-only pins when safe, adding compatibility shims, or changing setup commands. Do not mutate existing repo source files merely to force compatibility. If adaptation cannot be done within the service-safe environment setup boundary, report a blocker that names the conflicting sources and the attempted target version.

## Package Source Policy

| Dependency Kind | Preferred Source |
| --- | --- |
| Python runtime | Selected Python minor version from **Python Version Policy** |
| Starter Python dependencies | PyPI through `pixi add --manifest-path <manifest_path> --pypi scipy mdutils ruff mkdocs-material mypy attrs omegaconf imageio matplotlib jsonschema jinja2` |
| Named package with package-specific rules | Follow `isomer-misc-pkg-specifics` first; record the selected package page and evidence |
| NVIDIA official package | `nvidia` Conda channel, then PyPI, then `conda-forge`, with evidence for each skipped source |
| Normal Python package | PyPI through `pixi add --manifest-path <manifest_path> --pypi <requirement>` |
| Python package unsuitable or unavailable on PyPI | `conda-forge` with PyPI failure evidence recorded |
| Python package unavailable from PyPI and `conda-forge` | Project or Topic Workspace installable package store, such as local wheelhouse, `dist/`, local index, vendored package, or installable repo |
| Python package unavailable from remote and project-local sources | System Python fallback only through explicit Pixi-mediated wiring or a local artifact, marked host-specific and lower portability |
| Non-Python command-line tool | Pixi/Conda |
| Binary/runtime/system dependency | Pixi/Conda |
| NVIDIA tool or runtime package | Pixi with package source evidence; prefer `nvidia` channel, then PyPI when applicable, then `conda-forge` |
| Installable local Python repo | PyPI editable file requirement |

## Package Installation Routing

Apply this route before mutating the Pixi manifest for any package installation task:

1. **Package-specific rules**: if `isomer-misc-pkg-specifics` exists and lists the package, load the selected package page and follow it. These rules override the generic source ladder.
2. **NVIDIA official packages**: when no package-specific rule overrides the choice, prefer the `nvidia` Conda channel, then PyPI, then `conda-forge`.
3. **Other Python libraries**: when no package-specific rule overrides the choice, try PyPI first. Use `conda-forge` only after PyPI cannot satisfy the requirement. If `conda-forge` cannot satisfy it, scan the Project and Topic Workspace for an installable Python package store. If that fails, inspect system Python and introduce it into Pixi only through explicit fallback wiring or a local artifact.
4. **Native tools and runtime dependencies**: use Pixi/Conda, package-specific guidance, or explicit runtime wiring according to **Environment Enclosure Ladder**.

When source reachability is uncertain, a local mirror or private registry is likely configured, a local package store may exist, or NVIDIA channel choice is policy-relevant, use `isomer-srv-resolve-pkg-repo` to choose the reachable repository, registry, channel, or local source before dependency mutation. If the environment gate or manifest already fixes the source and no reachability concern exists, record that fixed source instead of adding a separate resolution step.

Use `isomer-misc-bounded-run-tips` for setup-operation classification and bounded guidance. Use subcommand `cuda-compile` when it matches CUDA architecture targets, `TORCH_CUDA_ARCH_LIST`, `CMAKE_CUDA_ARCHITECTURES`, `nvcc` flags, or CUDA build parallelism. If no bounded-run tips recipe applies to an operation classified as `heavy` or `unknown-risk`, require generic best-effort guidance with probes, capacity signals, limits, bounded command, expected result, and blocker condition. Use `isomer-misc-nvidia-tools` for CUDA/C++ Pixi build environment preferences and NVIDIA package/runtime wiring.

## Environment Enclosure Ladder

Apply this ladder before installing or verifying any dependency or runtime need:

1. **Pixi-managed install**: install through `pixi add --manifest-path <manifest_path> --pypi ...`, `pixi add --manifest-path <manifest_path> ...`, or `pixi install --manifest-path <manifest_path> --environment <pixi_environment>`.
2. **Pixi-mediated external runtime wiring**: when Pixi cannot reasonably provide a needed DLL, SO, SDK, compiler, CUDA runtime, activation script, package-config path, or library path, use that external piece only through recorded `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...` commands.
3. **Topic-local user-space fallback**: when Pixi-managed installation and external runtime wiring cannot satisfy the gate, materialize fallback files under `<topic-workspace-dir>/.isomer-user-env/`, record commands and paths, and warn that the result is less portable than Pixi-managed setup.
4. **Blocker**: when setup would require `sudo`, apt/yum/brew or another system package manager mutation, global shell profile edits, global Python or Node package installs, `/etc` changes, `ldconfig`, daemons, kernel driver changes, or another privileged or machine-global action.

## Runtime Wiring Policy

External runtime wiring must be explicit and replayable. Record the exact source script, runtime path, environment variable, and reason in `topic.env.topic_setup_target_spec`, then run commands through Pixi. Common variables include `PATH`, `LD_LIBRARY_PATH`, `DYLD_LIBRARY_PATH` when applicable, `CPATH`, `LIBRARY_PATH`, `PKG_CONFIG_PATH`, and `CUDA_HOME`.

Do not treat a tool found in the ambient shell as ready unless the derived gate records how it is made available through the Pixi-scoped command. A valid verification or setup command may use a form like:

```bash
pixi run --manifest-path <manifest_path> --environment <pixi_environment> bash -lc 'source <script> && export LD_LIBRARY_PATH=<path>:$LD_LIBRARY_PATH && <command>'
```

## Topic-Local Fallback Policy

Use `<topic-workspace-dir>/.isomer-user-env/` only after Pixi-managed installation and Pixi-mediated runtime wiring are insufficient. Preserve all fallback commands and installed paths in `topic.env.topic_setup_target_spec`, add `.isomer-user-env/` to the Topic Workspace `.gitignore`, and report a lower-portability warning in the final output.

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
- `manifest_path` is not resolved from the effective Topic Workspace Pixi binding;
- the selected Python version is missing from the derived gate and cannot be recovered or selected by policy;
- Python version conflicts cannot be adapted within the service-safe environment setup boundary;
- a starter Python dependency cannot be resolved or installed;
- a dependency cannot be inferred, resolved, or installed;
- a required dependency or runtime need lacks an enclosure strategy in `topic.env.topic_setup_target_spec`;
- a resource-relevant setup command lacks bounded-run tips classification evidence;
- a setup command classified as `heavy` or `unknown-risk` lacks a resource check plan, lacks a bounded-run guidance source, lacks generic best-effort fallback evidence when no recipe applies, lacks a bounded real-path setup command, or would overload the host even in bounded form;
- a Python package must use Pixi/Conda but the reason is unknown;
- a package-source ladder step is skipped without evidence;
- a channel or package source cannot be reached or cannot be resolved through fixed evidence or `isomer-srv-resolve-pkg-repo`;
- package-specific guidance reports that the installed package variant cannot satisfy the gate;
- the desired dependency would mutate the Project-root Pixi environment or an Agent Workspace-specific environment;
- the setup requires `sudo`, system package manager mutation, global shell profile edits, global Python or Node package installs, `/etc` changes, `ldconfig`, daemons, kernel driver changes, or another privileged or machine-global action.
