# Derive Gate

Use this subcommand to generate the operational environment gate from the source gate and repo evidence.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Workspace context | Require `project_root`, `research_topic_id`, `topic_workspace_dir`, `manifest_path_or_dir`, `manifest_path`, and `pixi_environment` from `resolve-workspace`. Refuse to run if any value is missing, and tell the user to run `resolve-workspace` first. |
| Source gate summary | Require the extracted source gate summary from `read-gate`. Refuse to run if it is missing, and tell the user to run `read-gate` first. |
| Repo context | Require repo context from `ensure-repos` when the source gate needs independent repos. If repos are required and context is missing, refuse to run and tell the user to run `ensure-repos` first. |
| `derived_gate_path` | Use `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md`; create the parent directory when writing the gate. |
| Optional modifiers | None for this step. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**: workspace context from `resolve-workspace`, source gate summary from `read-gate`, and repo context from `ensure-repos` when the source gate needs repos.
2. **Resolve the derived gate path** as `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md` and create its parent directory when needed.
3. **Translate user intent into operations**. Convert the source gate and repo evidence into concrete repo requirements, dependency plan, enclosure strategy, Pixi install commands, verification commands, expected results, and blockers.
4. **Apply dependency and enclosure policy**. Include Python as the Topic Workspace glue language, select a Python version with **Python Version Policy**, include the starter Python dependencies from **Starter Python Dependencies**, prefer PyPI for Python packages unless Pixi/Conda is required for the gate, use Pixi/Conda for native tools and binary/runtime dependencies, prefer the `nvidia` channel for NVIDIA tools, and classify every dependency or runtime need with **Environment Enclosure Strategy**.
5. **Write the fixed Markdown template** from **Template**. Include every section; write `None.` or a short reason when a section does not apply.
6. **Warning-label inferred repos** in `## Inferred Source Warnings` and carry the same warnings to the final skill output.
7. **Report `derived_gate_path`** and any blockers that prevent installation or verification.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the source gate, repo evidence, dependency policy, parent guardrails, and user request, then execute the plan.

## Template

```markdown
# Isomer Environment Gate

## Source Intent

## Runnable Target

## Repo Requirements

## Inferred Source Warnings

## Dependency Plan

## Pixi Install Commands

## Verification Commands

## Expected Results

## Blockers

## Execution Log
```

## Section Guidance

`## Source Intent` should summarize the user-authored source gate and cite `<topic-workspace-dir>/user-intent/src/env-gate.md`.

`## Runnable Target` should name the desired command or behavior that must work after setup.

`## Repo Requirements` should list repo names, paths under `repos/<repo-name>`, sources, and inspection notes.

`## Inferred Source Warnings` should list inferred repo sources and the reason each was chosen. Use `None.` only when no repo source was inferred.

`## Dependency Plan` should list Python glue baseline, selected Python version, Python version evidence, any version conflicts and adaptation plan, starter Python dependencies, PyPI dependencies, Pixi/Conda dependencies, native toolchains, NVIDIA channel decisions, editable installs, and an enclosure strategy for every dependency or runtime need. Mark each item as Pixi-managed, Pixi-mediated external runtime wiring, topic-local user-space fallback, or blocked. For every non-Pixi-managed choice, record why Pixi-managed installation was not used.

`## Pixi Install Commands` should list the concrete commands the agent will run from the Topic Workspace root or with `--manifest-path <manifest_path>`, including the starter dependency command when those packages are missing. Dependency mutation commands must use `pixi add --manifest-path <manifest_path>` or `pixi install --manifest-path <manifest_path> --environment <pixi_environment>`. Setup commands that need runtime wiring must use `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <command>` and record any sourced script or exported path.

`## Verification Commands` should list the exact Pixi commands that prove the runnable target works. If a command needs external runtime wiring, include the recorded environment variables, sourced scripts, or runtime paths inside the Pixi-run command rather than relying on ambient shell state.

`## Expected Results` should state pass/fail criteria and expected outputs.

`## Blockers` should list missing repos, missing dependencies, ambiguous commands, unavailable packages, unsupported live-agent actions, privileged or machine-global setup requirements, unclassified dependencies, or other reasons readiness cannot be claimed. When repo docs or the source gate ask for `sudo`, system package manager mutation, global shell profile edits, global Python or Node installs, `/etc` changes, `ldconfig`, daemons, kernel driver changes, or similar host mutation, record that request as a blocker or external prerequisite rather than an executable setup command.

`## Execution Log` should be initialized as `Not run yet.` before `install-deps` or `verify-gate`, then updated by those subcommands when they run commands. The log should preserve enclosure evidence: Pixi-managed commands, external runtime wiring, topic-local fallback commands, changed files, and blockers.

## Python Version Policy

Recover Python version evidence from the prompt, `env-gate.md`, repo metadata, and inspected repo files before choosing a version. Useful evidence includes `requires-python`, `python_requires`, requirement markers, `.python-version`, `runtime.txt`, `tox.ini`, `noxfile.py`, CI files, Dockerfiles, lockfiles, README setup notes, and package-manager config.

If the version is unspecified or cannot be recovered from existing context, choose the previous stable Python minor release relative to the latest stable Python release at execution time. For example, if the latest stable line is `3.N`, select `3.(N-1)`; do not choose a prerelease and do not hard-code this fallback in the skill.

If multiple sources conflict, choose the highest Python minor version mentioned or required by those sources as the target. Then adapt the dependency plan toward that target by selecting compatible package releases, loosening environment-only pins when safe, adding compatibility shims, or changing setup commands. Do not mutate existing repo source files merely to force compatibility. If adaptation cannot be done within the service-safe environment setup boundary, record a blocker that names the conflicting sources and the attempted target version.

## Starter Python Dependencies

Include these starter packages in the dependency plan as PyPI packages unless an existing compatible constraint already provides them: `scipy`, `mdutils`, `ruff`, `mkdocs-material`, `mypy`, `attrs`, `omegaconf`, `imageio`, `matplotlib`, `jsonschema`, and `jinja2`. Record any package that cannot be installed as a blocker with the reason and the attempted command.

## Environment Enclosure Strategy

Classify every dependency and runtime need before writing install or verification commands:

1. **Pixi-managed**: use `pixi add --manifest-path <manifest_path> --pypi ...`, `pixi add --manifest-path <manifest_path> ...`, or `pixi install --manifest-path <manifest_path> --environment <pixi_environment>` whenever PyPI or Pixi/Conda can satisfy the gate.
2. **Pixi-mediated external runtime wiring**: when a required DLL, SO, SDK, compiler, CUDA runtime, package-config path, activation script, or similar piece already exists outside Pixi and cannot reasonably be installed through Pixi, route it through an explicit `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...` command. Record paths, variables such as `PATH`, `LD_LIBRARY_PATH`, `DYLD_LIBRARY_PATH` when applicable, `CPATH`, `LIBRARY_PATH`, `PKG_CONFIG_PATH`, `CUDA_HOME`, and any sourced scripts.
3. **Topic-local user-space fallback**: when Pixi-managed installation and explicit runtime wiring cannot satisfy the gate, plan fallback materialization under `<topic-workspace-dir>/.isomer-user-env/`, record the commands and paths, and mark it as lower portability.
4. **Blocked**: if setup requires `sudo`, system package manager mutation, global shell profile edits, global Python or Node package installs, `/etc` changes, `ldconfig`, daemons, kernel driver changes, or another privileged or machine-global action, record a blocker and do not create an executable setup command for that action.

## Command Style

Write setup and verification commands that execute inside the prepared Topic Workspace environment as `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <command>`. Dependency mutation commands may use `pixi add --manifest-path <manifest_path> ...` and `pixi install --manifest-path <manifest_path> --environment <pixi_environment>`.
