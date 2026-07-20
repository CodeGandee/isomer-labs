# Install Packages

Use this subcommand to infer, install, and verify packages for the selected Topic Workspace Pixi environment from a user prompt, a description file, or copied blocker text.

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Resolve workspace and Pixi target**:
   - Run or reuse `storage-resolve` evidence for the selected Project, Research Topic, Topic Workspace, and semantic paths.
   - Resolve the active Topic Workspace Pixi manifest and environment from the Topic Workspace binding or explicit operator input.
   - Stop if mutation would target the Project-root Pixi environment, an Agent Workspace-specific environment, an ambient virtual environment, or an unresolved manifest.
2. **Load package request input**:
   - If the prompt names a file, read it as plain text first and parse recognizable YAML, JSON, TOML, or requirements-style sections when present.
   - If the prompt itself names packages or describes a missing runtime, use the prompt directly.
   - If copied blocker text names a requester skill, backend, runtime check, or failed import, preserve that context in the install report.
3. **Infer package intent**:
   - Extract package names, aliases, language/runtime, requester skill, task purpose, optional versions, requested source, and desired verification checks.
   - Classify each entry with **Package Kind Inference**.
   - If a name is ambiguous, a package could map to incompatible ecosystems, or the requested target is unclear, report a blocker or ask a targeted clarification before mutation.
4. **Build the install plan**:
   - For every named package, consult `isomer-misc-pkg-specifics` before generic source, variant, runtime-wiring, or verification choices; record selected package-specific evidence or `no package-specific rule`.
   - Choose a Pixi-scoped route for each package using **Install Route Policy**.
   - Generate verification commands with **Verification Policy** when the request does not provide them.
   - Consult NVIDIA, package-source, or bounded-run helper skills when the package route needs those policies.
   - Record any privileged, system-global, local-venv, ambient-pip, unrecorded user-library, or external-runtime requirement as a blocker.
5. **Check existing availability**:
   - Run lightweight Pixi-scoped checks for packages that may already be present.
   - Mark packages as already present only when their verification check passes through the selected Topic Workspace Pixi environment.
6. **Install packages**:
   - Use `pixi add --manifest-path <manifest_path> --pypi <requirement>` for Python libraries selected for PyPI.
   - Use `pixi add --manifest-path <manifest_path> <matchspec>` for Conda/Pixi packages, native tools, runtimes, and R packages available as Pixi/Conda packages.
   - Use a workspace-scoped R route only when the selected Topic Workspace Pixi environment can provide and record it; otherwise block rather than using an unrecorded user R library.
   - Use `pixi install --manifest-path <manifest_path> --environment <pixi_environment>` after dependency mutation when needed.
7. **Verify installation**:
   - Run verification through `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <command>`.
   - Treat install command success as insufficient without verification evidence.
   - For heavy or unknown-risk verification, apply **Resource and Bounded-Run Policy** before running the real path.
8. **Report result**:
   - Report installed, already-present, skipped, deferred, failed, and blocked packages.
   - Include package request source, inferred package kinds, selected install routes, commands run, verification commands, changed files, blockers, and next safe action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a package plan from the request, workspace context, Pixi target, parent guardrails, and user intent, then execute the safe parts and block the rest.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Workspace context | Require `project_root`, `research_topic_ref`, `topic_workspace_ref`, `topic_workspace_dir`, `manifest_path_or_dir`, `manifest_path`, and `pixi_environment`. Resolve through `storage-resolve` and the active Topic Workspace Pixi binding; refuse to mutate when the selected Topic Workspace or Pixi target is ambiguous. |
| Package request | Accept a direct prompt, Markdown file, YAML, JSON, TOML, requirements-style list, or copied blocker text. Treat structured files as an input convenience, not as a required schema. If no package request is present, ask for the packages or description to install. |
| Mutation intent | Require clear operator intent to install or repair packages in the selected Topic Workspace. Read-only package availability checks may report an install plan without mutation when the prompt asks to inspect only. |

## Package Request Intake

Accepted inputs include:

- Plain prompts such as `install matplotlib scipy seaborn for Python paper figure generation`.
- Markdown notes or copied blockers with package names, backend, purpose, and desired checks.
- YAML, JSON, or TOML snippets when a caller naturally provides them.
- `requirements.txt`-style package lists.
- Mixed prose plus structured sections.

Do not require a formal package request schema before proceeding. Normalize whatever was provided into an internal install plan and state any assumptions before mutation.

## Package Kind Inference

Classify each requested item before installation:

| Kind | Signals | Default route |
| --- | --- | --- |
| `python-library` | Python import, PyPI package, notebook/script dependency, `import <name>` check | Package-specific lookup first, then Topic Workspace Pixi environment through PyPI unless package-specific evidence says otherwise |
| `r-package` | R backend, `library(<name>)`, CRAN/Bioconductor-style package, R plotting package | Topic Workspace Pixi/R route; block if only unrecorded user-library or system R mutation is available |
| `native-conda` | binary, compiler, shared library, native CLI, Conda package, system runtime | Pixi/Conda package in Topic Workspace environment |
| `cli-tool` | command executable, `--version` check, document or build CLI | Pixi/Conda in Topic Workspace environment by default; block or ask before any user-global tool route |
| `latex-document-tool` | Tectonic, LaTeX, BibTeX/Biber, `latexmk`, `pdfcrop`, manuscript build | Pixi/Conda or documented Topic Workspace route, with verification by build/version command |
| `science-runtime` | solver, module, container, license-bound executable, HPC package | Package-specific availability check and Pixi/Conda route when possible; otherwise blocker or external-runtime wiring request |
| `external-runtime` | driver, daemon, system package, kernel, privileged SDK, external module only | Block or record external prerequisite; do not mutate host |

When a package could fit multiple kinds, choose the route that satisfies the task with the least host mutation. Ask a targeted clarification when the wrong choice could change behavior.

## Install Route Policy

Apply these routes before mutation:

1. **Already present**: if the Pixi-scoped verification check passes, say that the package is already present and skip mutation.
2. **Package-specific route**: for every named package, check `isomer-misc-pkg-specifics` before generic source choices. Follow the selected package page when it exists, or record `no package-specific rule` before continuing.
3. **Python PyPI route**: use `pixi add --manifest-path <manifest_path> --pypi <requirement>` for importable Python libraries that PyPI can satisfy and have no overriding package-specific rule.
4. **Pixi/Conda route**: use `pixi add --manifest-path <manifest_path> <matchspec>` for native tools, Conda-preferred packages, R packages available through channels, binary runtimes, and CLI tools that should live in the Topic Workspace environment.
5. **External runtime blocker**: if the requested package requires privileged host mutation, unavailable licenses, driver changes, daemons, system package managers, or unrecorded host state, report a blocker.

Do not use local `venv`, `.venv`, `virtualenv`, ambient `pip`, unrecorded user R library installs, `sudo`, system package managers, global shell profile edits, daemons, kernel driver changes, `/etc` mutation, or machine-global package setup from this subcommand.

## Verification Policy

Generate the smallest verification that proves the package is usable for the request:

- Python library: package-specific verification expectation when selected, otherwise `python -c "import <module>; print(getattr(<module>, '__version__', 'ok'))"` or a task-specific import/render/export check after recording `no package-specific rule`.
- R package: `Rscript -e "library(<package>); cat('ok\\n')"` through the selected Topic Workspace Pixi environment.
- CLI tool: `<command> --version`, `--help`, or a minimal no-output task command.
- Document tool: version check plus a minimal compile/export check when the request needs real build readiness.
- PPTX or figure package: create, reopen, render, or export a minimal file only when that is the task-critical proof.
- Science runtime: package-card or task-specific import, executable, module, license, backend, or smoke evidence.

Record verification status per package. Report `failed` when verification runs and misses its expected result, `blocked` when it cannot safely run, and `deferred` only when the user explicitly asks not to verify.

## Resource and Bounded-Run Policy

Before heavy or unknown-risk installation or verification, classify the operation with bounded-run guidance. Treat large downloads, compilation, GPU jobs, broad tests, large model inference, and scheduler/HPC work as risk signals. Use a bounded real-path check when possible, such as a selected build target, tiny input, minimal document, one representative import, or short CLI smoke command. Do not replace a task-critical verification path with an unrelated smoke test.

## Output

Lead with whether packages were installed, already present, partially installed, blocked, failed, deferred, or only inspected. Name the selected Research Topic, Topic Workspace, Pixi manifest and environment, and whether mutation ran. Summarize the request, plan, package-specific guidance, commands, changed files, per-package verification, blockers, and next action in natural language.

## Operational Notes

- Use structured content when available, but accept natural-language package requests and copied blockers.
- If the user manually provides a tool-pack contract, treat it as package request context and still own install planning here.

## Guardrails

- DO NOT mutate packages until the selected Topic Workspace and Pixi binding are confirmed.
- DO NOT require a formal schema-constrained package request file.
- DO NOT route to `isomer-misc-tool-packs` automatically.
- DO NOT mutate Project-root, Agent Workspace-specific, ambient, system, or machine-global environments.
- DO NOT claim package readiness from package metadata, install success, or package-card catalog entries without a Pixi-scoped verification check or explicit blocker.
