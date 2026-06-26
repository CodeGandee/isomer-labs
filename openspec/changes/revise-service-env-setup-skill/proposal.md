## Why

The `isomer-srv-env-setup` skill needs refinement because the current instructions contain errors or underspecified behavior that can mislead service agents during Pixi environment setup. The exact corrections and additional details will be worked out in later artifacts.

## What Changes

- Revise `skillset/service/isomer-srv-env-setup` to correct known errors.
- Restructure the skill as one command-style skill with many short kebab-case subcommands, following the `imsight-agent-skill-handling format` pattern: a lean `SKILL.md` router, a grouped `Subcommands` section, and linked reference pages with numbered `## Workflow` sections.
- Add clearer operational detail for the supported Topic Workspace environment setup workflow.
- Replace the full-flow shortcut with `setup-for-topic-workspace`, a public setup subcommand that runs all required setup steps for a given Topic Workspace.
- Split `setup-for-topic-workspace` into two execution modes: `fast-forward`/`auto` for direct execution and `step-by-step`/`manual` for interactive execution with user consent before each step.
- Require manual mode to pause before each workflow step, explain what is about to happen, present options in a compact table with columns for option, explanation, and pros/cons, then state the recommended option outside the table with its reason before waiting for the user to choose.
- Make the intended setup result explicit: given a Project Manifest-declared Topic Workspace, environment setup leaves the Topic Workspace directory with `.pixi/`, `pixi.toml`, and `pixi.lock` directly under `<topic-workspace-dir>/`.
- Require the skill to read `<topic-workspace-dir>/user-intent/src/env-gate.md`, which describes what must be able to run after setup and serves as the verification gate for readiness.
- Require independent repositories needed by the gate or task to reside under `<topic-workspace-dir>/repos/<repo-name>`, downloading or materializing them there when enough source information is available.
- Allow the agent to infer or search for missing repository sources when the gate implies runnable repo code is needed, while adding a visible warning to the generated `isomer-env-gate.md` and final output when a repo source was inferred rather than explicitly provided.
- Teach the skill to generate `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md` after repo requirements are resolved, translating the user's source gate and available repo contents into concrete required-to-succeed dependencies, Pixi install commands, verification commands, scripts, imports, tools, and success criteria for environment setup.
- Require `isomer-env-gate.md` to use a fixed Markdown section template so later agents can find source intent, runnable target, repo requirements, inferred-source warnings, dependency plan, Pixi commands, expected results, blockers, and execution log consistently.
- Add package-source preferences for dependency inference: prefer PyPI for Python packages by default, use Pixi/Conda packages when they are clearly required for the gate to pass, and prefer the `nvidia` channel over `conda-forge` for NVIDIA tools.
- Require the Topic Workspace root environment to always include Python as the glue and orchestration language, even when the runnable target uses another programming language.
- Make the workflow order explicit: read `env-gate.md`, ensure required repos exist without mutating existing repo directories, infer the dependencies needed for the gate to pass, generate `isomer-env-gate.md`, use Pixi to install the required packages and tools, then run the desired command that verifies the user-specified runnable target works.
- Preserve the skill's service-safe boundary and avoid expanding it into agent launch, runtime operation, or unrelated project management behavior.

## Capabilities

### New Capabilities

- `isomer-service-env-setup-skill`: define the service environment setup skill's Topic Workspace Pixi layout expectations and validation behavior.

### Modified Capabilities

None.

## Impact

- Affects `skillset/service/isomer-srv-env-setup/`.
- May add or revise OpenSpec coverage for the service environment setup skill if no existing capability cleanly covers it.
