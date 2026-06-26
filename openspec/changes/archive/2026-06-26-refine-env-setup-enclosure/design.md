## Context

`skillset/service/isomer-srv-env-setup` prepares the shared Topic Workspace Pixi environment from `user-intent/src/env-gate.md` and records concrete setup and verification details in `user-intent/derived/isomer-env-gate.md`. The current skill already requires Pixi command style for dependency mutation and verification, but it does not say what to do when a gate needs native libraries, system-looking shared objects, CUDA or compiler environment variables, activation scripts, or tools that are not cleanly available through PyPI or Conda packages.

The desired behavior is not strict hermetic isolation. Scientific and engineering work often needs native runtimes, vendor SDKs, shared libraries, compilers, or externally installed toolchains. The desired behavior is enclosed, auditable setup: the agent should first prefer Pixi-managed dependencies, then explicitly route any external runtime pieces through Pixi-launched commands, then use topic-local user-space fallback only when Pixi cannot satisfy the gate, and finally block instead of requiring privileged or global host changes.

## Goals / Non-Goals

**Goals:**

- Define an environment enclosure policy for `isomer-srv-env-setup`.
- Keep dependency installation constrained to the selected Topic Workspace Pixi environment whenever Pixi can satisfy the gate.
- Allow explicit runtime wiring for DLL/SO paths, compiler paths, CUDA variables, package-config paths, and sourced setup scripts when that wiring is recorded and replayable through Pixi-run commands.
- Allow topic-local user-space fallback installs only as a secondary option, under a predictable ignored prefix, when Pixi cannot satisfy the gate.
- Forbid sudo, system package manager mutation, global shell profile changes, global Python or Node package installs, `/etc` edits, `ldconfig`, and other machine-global mutation.
- Make `isomer-env-gate.md`, command logs, and final output show which enclosure strategy was used for each dependency or runtime need.

**Non-Goals:**

- Do not make Topic Workspace environments fully hermetic against all host state.
- Do not solve relocation of arbitrary installed runtimes after the Topic Workspace moves.
- Do not add a new package manager abstraction or a new environment manager beyond Pixi.
- Do not mutate existing repos merely to adapt them to the enclosed environment.
- Do not support privileged system setup from this service skill.

## Decisions

Use an enclosure ladder rather than a new subcommand. `derive-gate` should record the planned strategy, `install-deps` should enforce the strategy while mutating environment files, and `verify-gate` should reject unrecorded ambient state. This keeps `setup-for-topic-workspace` in its existing order: resolve workspace, read gate, ensure repos, derive gate, install deps, verify gate.

The enclosure ladder is:

1. Pixi-managed dependencies. Use `pixi add --manifest-path <manifest_path> --pypi ...`, `pixi add --manifest-path <manifest_path> ...`, and `pixi install --manifest-path <manifest_path> --environment <pixi_environment>` for Python packages, native tools, command-line tools, compilers, and runtime libraries whenever Pixi can satisfy the gate.
2. Pixi-mediated external runtime wiring. If a needed DLL/SO, SDK, compiler, CUDA runtime, or setup script already exists outside Pixi and cannot reasonably be installed through Pixi, route it through explicit Pixi-run command environment. Examples include PATH, LD_LIBRARY_PATH, DYLD_LIBRARY_PATH where applicable, CPATH, LIBRARY_PATH, PKG_CONFIG_PATH, CUDA_HOME, and explicitly sourced environment scripts.
3. Topic-local user-space fallback. If Pixi cannot satisfy the gate and external runtime wiring is insufficient, install or materialize the fallback under `<topic-workspace-dir>/.isomer-user-env/`, add that path to the Topic Workspace `.gitignore`, and record every command and path. This is secondary because it is less portable than Pixi, but it is still enclosed inside the Topic Workspace boundary.
4. Blocker. If the setup requires sudo, apt/yum/brew mutation, `/usr` or `/etc` edits, global shell profile edits, global Python or Node package installs, `ldconfig`, service daemons, kernel drivers, or another privileged or machine-global action, stop and report a blocker.

`isomer-env-gate.md` should gain explicit section guidance rather than necessarily changing the fixed top-level template. The `## Dependency Plan`, `## Pixi Install Commands`, `## Verification Commands`, `## Blockers`, and `## Execution Log` sections should describe the enclosure strategy. This avoids expanding the template with another top-level section unless implementation finds that a dedicated section is clearer.

Runtime commands should continue to use the explicit Pixi form. A command may include explicit setup inside the command string, such as `pixi run --manifest-path <manifest_path> --environment <pixi_environment> bash -lc 'source <script> && export LD_LIBRARY_PATH=<path>:$LD_LIBRARY_PATH && <command>'`, only when the sourced script and exported paths are recorded in the derived gate.

Verification must prove replayability from the derived gate, not merely local success. If a command passes only because the ambient shell already has variables, a globally installed tool, or an unrecorded activated environment, `verify-gate` should report `blocked` or `failed` rather than `ready`.

## Risks / Trade-offs

- [Risk] Allowing external runtime wiring can still depend on host-specific paths. Mitigation: require explicit path records, warnings in the dependency plan, and blocker language when the path is required but not present.
- [Risk] Topic-local fallback installs can become another unmanaged environment. Mitigation: allow them only after Pixi and Pixi-mediated wiring are insufficient, keep them under `.isomer-user-env/`, ignore that prefix, and record all commands.
- [Risk] Agents may overuse fallback installs because they are convenient. Mitigation: require a reason in `isomer-env-gate.md` whenever a dependency does not use Pixi-managed installation.
- [Risk] Existing gate commands may appear to pass on the operator machine because of ambient state. Mitigation: verification readiness requires the explicit Pixi command and any required environment wiring to be present in the derived gate and command log.
