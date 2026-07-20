# Derive Env Gate

Use this subcommand to generate or validate the operational topic environment target spec from source intent, repo evidence, or an explicit manual target spec.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Workspace context | Require `project_root`, `research_topic_id`, `topic_workspace_dir`, `manifest_path_or_dir`, `manifest_path`, and `pixi_environment` from `resolve-topic-workspace`. Refuse to run if any value is missing, and tell the user to run `resolve-topic-workspace` first. |
| Source intent summary | Require the extracted `topic.intent.topic_env_requirements` summary from `read-env-gate` when deriving from source intent. Refuse to run if source-intent derivation was requested and the summary is missing. |
| Explicit target spec | Optional. A manual file, prompt, or context may supply the operational target spec directly. When supplied, validate it against this page's fixed sections and enclosure policy instead of requiring source intent. |
| Topic env target spec | Resolve `topic.env.topic_setup_target_spec` through Workspace Path Resolution. Under `isomer-default.v1`, this defaults to `<topic-workspace-dir>/intent/derived/isomer-env-gate.md`; create the parent directory when writing the target spec. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**:
   - Require workspace context from `resolve-topic-workspace`.
   - Require source intent summary from `read-env-gate` when deriving from source intent.
   - Require explicit target spec input when manual mode is used.
2. **Resolve the target spec label** `topic.env.topic_setup_target_spec`:
   - Record semantic label, resolved path, storage profile, source, source detail, diagnostics, and blockers.
   - Create the parent directory when writing the target spec.
3. **Translate or validate operations**:
   - Preserve every source-intent runnable target as either a verification target or a named blocker; do not narrow a requested build, inference, dataset, or benchmark target into an unrelated smoke test.
   - Convert source intent into concrete topic-main requirements, Canonical External Repository requirements, requested revision and repository-feature needs, user-supplied command requirements, agent-selection constraints, projection access intent, dependency plan, enclosure strategy, operation classification evidence, bounded real-path resource check plan when needed, Pixi install commands, verification commands, expected results, and blockers.
   - Ask `isomer-misc-bounded-run-tips` to classify each setup or verification item whose resource cost affects readiness planning.
   - Record `classification_source`, `classification_result`, `classification_reason`, `resource_dimensions`, and whether bounded guidance is required.
   - For `heavy` or `unknown-risk`, apply bounded-run tips guidance. If no recipe matches, write explicit generic best-effort bounded guidance that still exercises the source-intent path.
   - Or validate that the explicit target spec already contains those details.
4. **Apply dependency and enclosure policy**:
   - Include Python as the Topic Workspace glue language.
   - Select a Python version with **Python Version Policy**.
   - Include the starter Python dependencies from **Starter Python Dependencies**.
   - Apply **Package Installation Routing** before choosing package sources, writing install commands, writing runtime-wiring commands, or writing package-specific verification commands.
   - For every named package, consult `isomer-misc-pkg-specifics` first and record either the selected package-specific evidence or `no package-specific rule` before generic package-source, Pixi, PyPI, Conda, runtime-wiring, enclosure, or verification rules.
   - Use Pixi/Conda for native tools and binary/runtime dependencies.
   - Record package source evidence.
   - Consult `isomer-srv-resolve-pkg-repo` when repository, mirror, registry, or channel reachability is a material decision.
   - Use `isomer-misc-bounded-run-tips` for operation classification and bounded guidance. Use subcommand `cuda-compile` when its recipe matches CUDA architecture, `nvcc`, or CUDA build parallelism choices.
   - Consult `isomer-misc-nvidia-tools` only when CUDA/C++ Pixi environment setup or NVIDIA package/runtime wiring is needed.
   - Classify every dependency or runtime need with **Environment Enclosure Strategy**.
5. **Write or update the fixed Markdown template** from **Template**:
   - Write at the resolved `topic.env.topic_setup_target_spec` path when deriving from source intent.
   - When using an explicit manual target spec, record the explicit source and normalized target-spec copy or reference, then preserve every required section.
   - Use Markdown checkboxes in the generated gate file for every required setup item, resource check, verification command, expected-result comparison, and blocker-resolution item that must be done or checked before readiness can be declared.
   - Keep optional diagnostics and supporting smoke checks outside `## Gate Checklist` unless they are required readiness work.
6. **Warning-label inferred repo requirements** in `## Inferred Source Warnings` and carry the same warnings to the final skill output. `ensure-topic-repos` may later add stronger source evidence when it materializes missing repos.
7. **Report target spec metadata** and any blockers that prevent topic-main setup, repo acquisition, projection materialization, installation, or verification.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the source gate, repo evidence, dependency policy, parent guardrails, and user request, then execute the plan.

## Template

```markdown
# Isomer Environment Gate

## Source Intent

## Gate Checklist

## Runnable Target

## Repo Requirements

## Inferred Source Warnings

## Projection Requirements

## Dependency Plan

## Resource Check Plan

## Pixi Install Commands

## Verification Commands

## Expected Results

## Blockers

## Execution Log
```

## Section Guidance

### Source Intent

- Cite `topic.intent.topic_env_requirements` and its resolved path when deriving from source intent.
- Name the explicit target spec source when the service was invoked manually.
- Preserve later Agent Workspace cwd assumptions as source context only.

### Gate Checklist

- Treat `## Gate Checklist` as the required readiness work contract, not a progress decoration. Every item in this section is required for `readiness_status: ready`.
- Use Markdown checkboxes for required actionable gate work: `- [ ]` before work runs and `- [x]` only after evidence exists.
- Include setup items, repo checks, projection checks, dependency installation, resource probes, bounded real-path verification commands, expected-result checks, and blocker-resolution items.
- For each required checklist item, state the pass condition, evidence source, operation classification evidence when relevant, bounded-run guidance source when required, and blocker condition either in the item text or in the matching `## Verification Commands`, `## Expected Results`, `## Resource Check Plan`, `## Blockers`, or `## Execution Log` entry.
- Keep optional diagnostics and supporting smoke checks outside `## Gate Checklist`; if a smoke check is included in the checklist, its item text must make clear that only the smoke check is required.
- Keep unchecked items visible when they are blocked, unsafe, or not yet run; explain the reason in `## Blockers` or `## Execution Log`.
- Do not mark a checkbox complete because a weaker smoke test passed unless the checkbox itself was only for that smoke test, or the user explicitly records a downgrade from the original critical-path item.

### Runnable Target

- Name the command or behavior that must work after setup.
- Keep every source-intent runnable target in scope as a verification target, bounded real-path target, or blocker.
- For operations classified as `heavy` or `unknown-risk`, state the bounded real-path variant.

### Repo Requirements

- List repo names, semantic `topic.repos.*` labels, expected resolved paths, source hints, and inspection notes.
- Use `repos/extern/<repo-label-path>` for helper-created non-main topic repos unless a safe explicit binding exists.
- Treat existing canonical external repos as read-only evidence unless this target spec explicitly authorizes mutation.
- Preserve exact user-supplied repository commands and their ordering as intent subject to authorization and safety limits.
- When the user supplies no commands, record the requested source, revision, authentication posture, sparse or partial needs, submodules, LFS, provider requirements, local-source posture, history needs, resource limits, and other constraints that `ensure-topic-repos` must use to select an external procedure.
- Do not prescribe one provider, remote name, clone depth, history posture, staging layout, retry sequence, or cleanup policy as the platform default.
- Require external verification of requested and resolved locators, target path, source relationship, and immutable commit or digest before `project repos register` and typed provenance recording.
- Include partial-result posture, registration conflict, and Artifact-recording failure as distinct blocker and resume stages.

### Inferred Source Warnings

- List each inferred repo source and the reason it was chosen.
- Use `None.` only when no repo source was inferred.

### Projection Requirements

- List canonical external repos that must be visible from topic-main.
- State intended access: `read-only` or `writable`.
- State expected projection root: `topic.repos.main.projections.readonly` or `topic.repos.main.projections.writable`.
- Include acceptable projection modes, mutation policy, and blockers.
- Use `None.` when no external repo must be projected into topic-main.

### Dependency Plan

- Include Python glue baseline, selected Python version, Python version evidence, version conflicts, and adaptation plan.
- Include starter Python dependencies, PyPI dependencies, Pixi/Conda dependencies, native toolchains, editable installs, local package stores, and system Python fallbacks when used.
- Classify every dependency or runtime need as Pixi-managed, Pixi-mediated external runtime wiring, topic-local user-space fallback, or blocked.
- For every non-Pixi-managed choice, record why Pixi-managed installation was not used.
- Record package source evidence, NVIDIA channel decisions, and `isomer-srv-resolve-pkg-repo` evidence when repository, mirror, registry, channel, local package store, or source reachability is uncertain or policy-relevant.
- Record CUDA architecture, CUDA/C++ build environment, and build parallelism preference evidence when those choices affect the gate.
- For every named package, consult `isomer-misc-pkg-specifics` before the generic source ladder. Record selected package-specific evidence when a page exists, or record `no package-specific rule` before continuing with generic routing.
- Keep package-specific caveats out of this core service workflow; record only the selected package-specific source, variant, verification expectation, warning, or blocker evidence needed by this gate.

### Resource Check Plan

- Record bounded-run tips classification evidence for each setup or verification command whose resource cost affects readiness planning.
- Treat `heavy` and `unknown-risk` classifications as requiring resource-check planning, bounded real-path guidance, or a blocker.
- Keep operation examples non-normative; `isomer-misc-bounded-run-tips` owns classification for the active project and host.
- When a bounded-run tips subcommand applies, record the matched skill/subcommand, the selected lightweight probes, capacity signals, limits, bounded real-path command, expected result, and blocker condition.
- When no bounded-run tips subcommand applies, record the source as generic best-effort judgment, then name the probes, capacity signals, limits, bounded real-path command, expected result, and blocker condition.
- For `light` classifications, record why no resource check plan is required.
- Do not accept a simple smoke test that misses the source-intent heavy path as readiness evidence.

### Pixi Install Commands

- List concrete commands to run from the Topic Workspace root or with `--manifest-path <manifest_path>`.
- Use `pixi add --manifest-path <manifest_path>` or `pixi install --manifest-path <manifest_path> --environment <pixi_environment>` for dependency mutation.
- Use `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <command>` for setup commands that need the prepared environment.
- Include recorded sourced scripts, exported variables, or runtime paths inside the Pixi-run command when runtime wiring is required.

### Verification Commands

- List exact Pixi commands that prove the runnable target works.
- Ensure each source-intent runnable target has a corresponding verification command, bounded real-path command, or blocker.
- For operations classified as `heavy` or `unknown-risk`, align the command with the `## Resource Check Plan` guidance source and bounded limits instead of inventing an unrecorded full-scale command.
- For profiler, tracer, debugger, memory-checker, and similar wrapper tools that execute a target command as a subprocess, put the wrapper tool inside Pixi: `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <wrapper-tool> <tool-options> <target-command> <target-args>`. Do not write `<wrapper-tool> pixi run ...` unless local evidence proves that Pixi itself is the intended target process.
- Include recorded environment variables, sourced scripts, or runtime paths inside the Pixi-run command when needed.
- Keep Topic Workspace readiness topic-scoped; do not derive per-Agent Workspace verification here and do not write `topic.env.agent_setup_target_spec`.

Example for a CUDA kernel topic:

- Intent says: build the baseline kernel and run a baseline benchmark.
- Good action: identify the host GPU with `nvidia-smi`; compile only the host architecture rather than a broad portable architecture list; cap CUDA build parallelism with `MAX_JOBS=1` or another conservative build-job count; build a selected extension or kernel target instead of all release artifacts; run a tiny benchmark case with one short input shape and few iterations.
- Bad action: replace the required build and benchmark with only `import torch` and `torch.cuda.is_available()`.
- If the bounded build or benchmark still cannot run safely: mark readiness `blocked` with resource evidence and the exact command to retry later.

### Expected Results

- State pass/fail criteria.
- State expected outputs, files, command output snippets, metrics, or runtime signals.
- For operations classified as `heavy` or `unknown-risk`, include expected evidence that the bounded real-path command exercised the source-intent path, not merely a supporting smoke check.

### Blockers

- List missing repos, missing dependencies, ambiguous commands, unavailable packages, unsupported live-agent actions, privileged or machine-global setup requirements, unclassified dependencies, or other reasons readiness cannot be claimed.
- Record `sudo`, system package manager mutation, global shell profile edits, global Python or Node installs, `/etc` changes, `ldconfig`, daemons, kernel driver changes, or similar host mutation as blockers or external prerequisites.
- Do not turn privileged or machine-global setup requests into executable setup commands.

### Execution Log

- Initialize as `Not run yet.` before `install-topic-deps` or `verify-env-gate`.
- Preserve resource check evidence, bounded real-path execution decisions, enclosure evidence, Pixi-managed commands, external runtime wiring, topic-local fallback commands, changed files, and blockers.
- Update this section after `install-topic-deps` or `verify-env-gate` runs commands.

## Python Version Policy

Recover Python version evidence from the prompt, resolved `topic.intent.topic_env_requirements`, explicit target spec input, repo metadata, and inspected repo files before choosing a version. Useful evidence includes `requires-python`, `python_requires`, requirement markers, `.python-version`, `runtime.txt`, `tox.ini`, `noxfile.py`, CI files, Dockerfiles, lockfiles, README setup notes, and package-manager config.

If the version is unspecified or cannot be recovered from existing context, choose the previous stable Python minor release relative to the latest stable Python release at execution time. For example, if the latest stable line is `3.N`, select `3.(N-1)`; do not choose a prerelease and do not hard-code this fallback in the skill.

If multiple sources conflict, choose the highest Python minor version mentioned or required by those sources as the target. Then adapt the dependency plan toward that target by selecting compatible package releases, loosening environment-only pins when safe, adding compatibility shims, or changing setup commands. Do not mutate existing repo source files merely to force compatibility. If adaptation cannot be done within the service-safe environment setup boundary, record a blocker that names the conflicting sources and the attempted target version.

## Starter Python Dependencies

Include these starter packages in the dependency plan as PyPI packages unless an existing compatible constraint already provides them: `scipy`, `mdutils`, `ruff`, `mkdocs-material`, `mypy`, `attrs`, `omegaconf`, `imageio`, `matplotlib`, `jsonschema`, and `jinja2`. Record any package that cannot be installed as a blocker with the reason and the attempted command.

## Package Installation Routing

Apply this route before writing package sources or install commands:

1. **Package-specific rules**: for every named package, check whether `isomer-misc-pkg-specifics` exists and lists the package. If it does, load the selected package page and follow it before generic source, variant, runtime-wiring, or verification choices. These rules override the generic source ladder.
2. **No package-specific rule evidence**: when no package page exists for the named package, record `no package-specific rule` in `## Dependency Plan`, then continue with the generic source ladder.
3. **NVIDIA official packages**: when no package-specific rule overrides the choice, prefer the `nvidia` Conda channel, then PyPI, then `conda-forge`.
4. **Other Python libraries**: when no package-specific rule overrides the choice, try PyPI first. Use `conda-forge` only after PyPI cannot satisfy the requirement. If `conda-forge` cannot satisfy it, scan the Project and Topic Workspace for an installable Python package store. If that fails, inspect system Python and introduce it into Pixi only through explicit fallback wiring or a local artifact.
5. **Native tools and runtime dependencies**: use Pixi/Conda, package-specific guidance, or explicit runtime wiring according to **Environment Enclosure Strategy**.

Record evidence for every skipped ladder step in `## Dependency Plan` before writing a lower-preference source into `## Pixi Install Commands`.

## Environment Enclosure Strategy

Classify every dependency and runtime need before writing install or verification commands:

1. **Pixi-managed**: use `pixi add --manifest-path <manifest_path> --pypi ...`, `pixi add --manifest-path <manifest_path> ...`, or `pixi install --manifest-path <manifest_path> --environment <pixi_environment>` whenever PyPI or Pixi/Conda can satisfy the gate.
2. **Pixi-mediated external runtime wiring**: when a required DLL, SO, SDK, compiler, CUDA runtime, package-config path, activation script, or similar piece already exists outside Pixi and cannot reasonably be installed through Pixi, route it through an explicit `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...` command. Record paths, variables such as `PATH`, `LD_LIBRARY_PATH`, `DYLD_LIBRARY_PATH` when applicable, `CPATH`, `LIBRARY_PATH`, `PKG_CONFIG_PATH`, `CUDA_HOME`, and any sourced scripts.
3. **Topic-local user-space fallback**: when Pixi-managed installation and explicit runtime wiring cannot satisfy the gate, plan fallback materialization under `<topic-workspace-dir>/.isomer-user-env/`, record the commands and paths, and mark it as lower portability.
4. **Blocked**: if setup requires `sudo`, system package manager mutation, global shell profile edits, global Python or Node package installs, `/etc` changes, `ldconfig`, daemons, kernel driver changes, or another privileged or machine-global action, record a blocker and do not create an executable setup command for that action.

## Command Style

Write setup and verification commands that execute inside the prepared Topic Workspace environment as `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <command>`. Dependency mutation commands may use `pixi add --manifest-path <manifest_path> ...` and `pixi install --manifest-path <manifest_path> --environment <pixi_environment>`.

For command-wrapper tools that launch the measured or debugged program as a subprocess, Pixi must launch the wrapper tool, and the wrapper tool must launch the target command. Use:

```bash
pixi run --manifest-path <manifest_path> --environment <pixi_environment> ncu <ncu-options> python bench.py
pixi run --manifest-path <manifest_path> --environment <pixi_environment> nsys profile python bench.py
pixi run --manifest-path <manifest_path> --environment <pixi_environment> valgrind --tool=memcheck python script.py
pixi run --manifest-path <manifest_path> --environment <pixi_environment> gdb --args python script.py
pixi run --manifest-path <manifest_path> --environment <pixi_environment> cuda-gdb --args ./kernel_bench
```

Do not write inverted commands such as `ncu pixi run ...`, `nsys profile pixi run ...`, `valgrind pixi run ...`, or `gdb --args pixi run ...` unless the gate records explicit local evidence that Pixi itself, rather than the target program, is the process under inspection.
