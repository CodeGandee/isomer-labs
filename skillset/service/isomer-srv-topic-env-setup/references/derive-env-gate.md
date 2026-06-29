# Derive Env Gate

Use this subcommand to generate or validate the operational topic environment target spec from source intent, repo evidence, or an explicit manual target spec.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Workspace context | Require `project_root`, `research_topic_id`, `topic_workspace_dir`, `manifest_path_or_dir`, `manifest_path`, and `pixi_environment` from `resolve-topic-workspace`. Refuse to run if any value is missing, and tell the user to run `resolve-topic-workspace` first. |
| Source intent summary | Require the extracted `topic.intent.topic_env_requirements` summary from `read-env-gate` when deriving from source intent. Refuse to run if source-intent derivation was requested and the summary is missing. |
| Explicit target spec | Optional. A manual file, prompt, or context may supply the operational target spec directly. When supplied, validate it against this page's fixed sections and enclosure policy instead of requiring source intent. |
| Repo context | Require repo context from `ensure-topic-repos` when the source intent or explicit target spec needs independent repos. If repos are required and context is missing, refuse to run and tell the user to run `ensure-topic-repos` first. |
| Topic env target spec | Resolve `topic.env.topic_setup_target_spec` through Workspace Path Resolution. Under `isomer-default.v1`, this defaults to `<topic-workspace-dir>/intent/derived/isomer-env-gate.md`; create the parent directory when writing the target spec. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**:
   - Require workspace context from `resolve-topic-workspace`.
   - Require source intent summary from `read-env-gate` when deriving from source intent.
   - Require explicit target spec input when manual mode is used.
   - Require repo context from `ensure-topic-repos` when repos are needed.
2. **Resolve the target spec label** `topic.env.topic_setup_target_spec`:
   - Record semantic label, resolved path, storage profile, source, source detail, diagnostics, and blockers.
   - Create the parent directory when writing the target spec.
3. **Translate or validate operations**:
   - Convert source intent and repo evidence into concrete repo requirements, dependency plan, enclosure strategy, Pixi install commands, verification commands, expected results, and blockers.
   - Or validate that the explicit target spec already contains those details.
4. **Apply dependency and enclosure policy**:
   - Include Python as the Topic Workspace glue language.
   - Select a Python version with **Python Version Policy**.
   - Include the starter Python dependencies from **Starter Python Dependencies**.
   - Prefer PyPI for Python packages unless Pixi/Conda is required for the gate.
   - Use Pixi/Conda for native tools and binary/runtime dependencies.
   - Record package source evidence.
   - Consult `isomer-srv-resolve-pkg-repo` when repository, mirror, registry, or channel reachability is a material decision.
   - Consult `isomer-misc-nvidia-tools` when CUDA architecture or CUDA/C++ build preferences are needed.
   - Classify every dependency or runtime need with **Environment Enclosure Strategy**.
5. **Write or update the fixed Markdown template** from **Template**:
   - Write at the resolved `topic.env.topic_setup_target_spec` path when deriving from source intent.
   - When using an explicit manual target spec, record the explicit source and normalized target-spec copy or reference, then preserve every required section.
6. **Warning-label inferred repos** in `## Inferred Source Warnings` and carry the same warnings to the final skill output.
7. **Report target spec metadata** and any blockers that prevent installation or verification.

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

`## Source Intent` should summarize the user-authored `topic.intent.topic_env_requirements` source intent and cite its resolved path, or name the explicit target spec source when the service was invoked manually.

`## Runnable Target` should name the desired command or behavior that must work after setup.

`## Repo Requirements` should list repo names, semantic `topic.repos.*` labels, resolved paths, sources, and inspection notes. For helper-created non-main topic repos, use the default `repos/extern/<repo-label-path>` location unless an explicit safe binding already exists.

`## Inferred Source Warnings` should list inferred repo sources and the reason each was chosen. Use `None.` only when no repo source was inferred.

`## Dependency Plan` should list Python glue baseline, selected Python version, Python version evidence, any version conflicts and adaptation plan, starter Python dependencies, PyPI dependencies, Pixi/Conda dependencies, native toolchains, package source evidence, NVIDIA channel decisions when relevant, editable installs, and an enclosure strategy for every dependency or runtime need. Mark each item as Pixi-managed, Pixi-mediated external runtime wiring, topic-local user-space fallback, or blocked. For every non-Pixi-managed choice, record why Pixi-managed installation was not used. When package repository, mirror, registry, or channel reachability is uncertain or policy-relevant, record the `isomer-srv-resolve-pkg-repo` resolution evidence. When CUDA architecture targets, CUDA/C++ build environments, or build parallelism choices affect the gate, record the `isomer-misc-nvidia-tools` preference evidence.

`## Pixi Install Commands` should list the concrete commands the agent will run from the Topic Workspace root or with `--manifest-path <manifest_path>`, including the starter dependency command when those packages are missing. Dependency mutation commands must use `pixi add --manifest-path <manifest_path>` or `pixi install --manifest-path <manifest_path> --environment <pixi_environment>`. Setup commands that need runtime wiring must use `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <command>` and record any sourced script or exported path.

`## Verification Commands` should list the exact Pixi commands that prove the runnable target works. If a command needs external runtime wiring, include the recorded environment variables, sourced scripts, or runtime paths inside the Pixi-run command rather than relying on ambient shell state.

When the source intent mentions later Agent Workspace use, preserve cwd assumptions explicitly as source context only. Commands that prove Topic Workspace readiness remain topic-scoped. Do not derive per-Agent Workspace verification here and do not write `topic.env.agent_setup_target_spec`.

`## Expected Results` should state pass/fail criteria and expected outputs.

`## Blockers` should list missing repos, missing dependencies, ambiguous commands, unavailable packages, unsupported live-agent actions, privileged or machine-global setup requirements, unclassified dependencies, or other reasons readiness cannot be claimed. When repo docs or the source gate ask for `sudo`, system package manager mutation, global shell profile edits, global Python or Node installs, `/etc` changes, `ldconfig`, daemons, kernel driver changes, or similar host mutation, record that request as a blocker or external prerequisite rather than an executable setup command.

`## Execution Log` should be initialized as `Not run yet.` before `install-topic-deps` or `verify-env-gate`, then updated by those subcommands when they run commands. The log should preserve enclosure evidence: Pixi-managed commands, external runtime wiring, topic-local fallback commands, changed files, and blockers.

## Python Version Policy

Recover Python version evidence from the prompt, resolved `topic.intent.topic_env_requirements`, explicit target spec input, repo metadata, and inspected repo files before choosing a version. Useful evidence includes `requires-python`, `python_requires`, requirement markers, `.python-version`, `runtime.txt`, `tox.ini`, `noxfile.py`, CI files, Dockerfiles, lockfiles, README setup notes, and package-manager config.

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
