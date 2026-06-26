## Context

`skillset/service/isomer-srv-env-setup` is the service skill that guides Pixi environment setup for Isomer Labs topic work. The canonical domain language defines a Topic Workspace as a Project Manifest-declared project-local directory for one Research Topic, and says it owns the topic's Workspace Runtime, Pixi manifest, and Pixi environment.

The core correction is that the `setup-for-topic-workspace` workflow should treat the Topic Workspace directory itself as the standalone Pixi workspace. After successful environment setup, the expected filesystem result is:

```text
<topic-workspace-dir>/
  .pixi/
  .gitignore
  pixi.toml
  pixi.lock
  repos/
    <repo-name>/
  user-intent/
    src/
      env-gate.md
    derived/
      isomer-env-gate.md
```

The skill should be modular like a single command with many subcommands. The top-level `SKILL.md` should remain a lean router with a grouped `Subcommands` section and should route to exactly one subcommand reference page. Each executable reference page should have its own `## Required Inputs` section, numbered `## Workflow` near the top, and freeform fallback, following the structural pattern used by the `imsight-agent-skill-handling format` subcommand. The parent router should not keep a central required-inputs table for executable setup behavior; the selected page should be self-contained enough for direct invocation.

Complex skills should divide subcommands into three parts: procedural subcommands, helper subcommands, and misc subcommands.

Procedural subcommands are the public single-step workflow API:

| Subcommand | Purpose |
| --- | --- |
| `resolve-workspace` | Resolve Project root, Research Topic, Topic Workspace, Pixi binding, and preconditions. |
| `read-gate` | Read `user-intent/src/env-gate.md` and identify the runnable target. |
| `ensure-repos` | Find existing repos or acquire missing required repos under `repos/<repo-name>`. |
| `derive-gate` | Generate or update `user-intent/derived/isomer-env-gate.md`. |
| `install-deps` | Infer package sources and install dependencies through the Topic Workspace Pixi environment. |
| `verify-gate` | Run the desired command through Pixi and report readiness. |

Helper subcommands are lower-level commands called by procedural subcommands. This skill does not currently expose helper subcommands; future helpers should be listed separately and kept out of public help unless promoted.

Misc subcommands are public support commands and shortcuts:

| Subcommand | Purpose |
| --- | --- |
| `help` | Explain the skill and list public subcommands. |
| `setup-for-topic-workspace` | Run the full gate-driven Topic Workspace setup workflow for a given Topic Workspace; default for concrete setup tasks that do not name a subcommand. |

`setup-for-topic-workspace` should be the orchestrating full path. It should execute `resolve-workspace`, `read-gate`, `ensure-repos`, `derive-gate`, `install-deps`, and `verify-gate` in order. The procedural step subcommands should also be directly callable for manual or partial setup.

`setup-for-topic-workspace` should choose one execution mode from the prompt:

| Mode | Prompt aliases | Behavior |
| --- | --- | --- |
| `fast-forward` | `auto`, `automatic`, `fast-foward`, `just do it`, `fully setup` | Run the required steps in order without pausing except for blockers, missing required inputs, or unsafe ambiguity. |
| `step-by-step` | `manual`, `interactive`, `ask me`, `confirm before each step` | Stop before each required step, explain what will happen, present user choices, state the recommendation outside the table, wait for consent, then run only the chosen action before moving to the next step. |

If the invocation has no prompt, the skill should default to `help`. If the prompt asks for concrete Topic Workspace setup but does not choose a mode, `setup-for-topic-workspace` should default to `fast-forward` unless the prompt asks to inspect, decide, or proceed carefully.

Manual mode should use a compact option table before each step:

| Option | Explain | Pros and Cons |
| --- | --- | --- |
| A | Proceed with the next step. | Pros: keeps setup moving and preserves the documented order. Cons: may reveal blockers that require user repair. |
| B | Stop before this step. | Pros: safest when the next action is uncertain. Cons: leaves setup incomplete. |

The recommendation should be written outside the table in this shape: `Recommended: A - Proceed with the next step. This is recommended because the workflow needs this artifact or action before later setup can be correct.` When there are meaningful alternatives for a step, such as choosing a repo source, package source, or repair route, the table should list those alternatives instead of only `A` and `B`. The agent should describe the recommended option plainly, then ask the user to pick one option before continuing.

Independent repositories needed by the task should live under `<topic-workspace-dir>/repos/<repo-name>`. If the gate or task requires runnable code, the setup workflow should find the repo there, download or materialize it when the required repo is missing and the source is known, infer or search for a likely source when the missing repo source is unknown, or report a blocker when acquisition remains too ambiguous. When the expected repo path already exists, `ensure-repos` should inspect it as read-only evidence and should not pull, checkout, copy into, delete from, install into, regenerate inside, or otherwise mutate it. The workflow should not scatter task repos into the Project root, Agent Workspace, `.pixi/`, or another ad hoc location.

The skill should read `<topic-workspace-dir>/user-intent/src/env-gate.md` before declaring setup complete. That file is user-authored intent material: it names what must be able to run after the environment is prepared. The setup workflow should then generate `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md` as an agent-normalized gate. The derived gate translates the source gate and the available repository contents into concrete required-to-succeed dependencies, Pixi install commands, Pixi run commands, scripts, imports, tools, repository requirements, expected repository paths, and success criteria that the setup workflow can verify.

The intended execution order is:

1. Read `<topic-workspace-dir>/user-intent/src/env-gate.md` and identify the user-specified runnable target.
2. Determine whether the target requires independent repos, then find existing repos or download, infer, search for, or materialize missing repos under `<topic-workspace-dir>/repos/<repo-name>`.
3. Inspect the source gate and the required repos to infer dependencies needed for the gate to pass, including language runtimes, package managers, libraries, tools, editable repo installs, and command-line programs.
4. Generate `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md` with the inferred dependencies, Pixi install commands, and the desired command or commands that prove the target runs.
5. Use Pixi from the Topic Workspace root to install the starter Python dependencies, inferred packages, and tools.
6. Run the desired command through Pixi, then declare readiness only when the user-specified target is runnable or blockers are explicit.

The user-facing setup invocation itself authorizes direct, service-safe mutation of the selected Topic Workspace Pixi environment. The workflow should not require a separate Service Request before adding dependencies, updating `pixi.toml`, refreshing `pixi.lock`, installing packages, or running the desired gate command. This direct mutation authority is still limited to the selected Project Manifest-declared Topic Workspace and does not extend to agent launch, unrelated Workspace Runtime mutation, GUI operation, research decisions, Project-root dependency mutation, or Agent Workspace-specific environments.

When `src/env-gate.md` is vague, the generated `derived/isomer-env-gate.md` should make the gate operational rather than merely repeat the vague wording. It should preserve the user's intent while adding enough detail for a later agent to know exactly what dependencies must be installed and what checks must pass before reporting environment readiness. If independent repos are likely required, the derived gate should name each repo, its expected `<topic-workspace-dir>/repos/<repo-name>` path, the acquisition source, the inferred dependencies, and the commands or scripts that prove the repo is usable in the Topic Workspace Pixi environment. When the acquisition source was inferred or discovered by the agent rather than explicitly provided by the user, the derived gate should include a visible warning that names the inferred source, the reason it was selected, and any uncertainty or review needed.

Dependency inference should choose package sources according to these defaults:

1. Include starter Python dependencies through PyPI unless an existing compatible constraint already provides them: `scipy`, `mdutils`, `ruff`, `mkdocs-material`, `mypy`, `attrs`, `omegaconf`, `imageio`, `matplotlib`, `jsonschema`, and `jinja2`.
2. Prefer PyPI for Python packages unless Conda is clearly required for the gate to pass.
3. Use Pixi/Conda packages for non-Python tools, command-line programs, binary or system-level runtime dependencies, Python dependencies unavailable or unsuitable on PyPI, or setup instructions that cannot be satisfied through PyPI.
4. Prefer the `nvidia` Pixi channel over `conda-forge` for NVIDIA tools and runtime packages.
5. Record the selected package source for each inferred dependency in `isomer-env-gate.md`; when a Python dependency uses Pixi/Conda instead of PyPI, record the reason.

The Topic Workspace root environment should always include Python as the glue and orchestration language. This is true even when the user-specified runnable target is C++, TypeScript, CUDA, Rust, shell, or another language. The dependency plan should add the native language toolchain, package manager, and runtime needed by the gate, but Python remains available for setup scripts, repo inspection, command orchestration, and result normalization.

Python version selection should first recover evidence from the prompt, `env-gate.md`, the derived gate, and inspected repos, including `requires-python`, `python_requires`, requirement markers, `.python-version`, runtime files, CI files, Dockerfiles, lockfiles, and README setup notes. If no version can be recovered, the workflow should choose the previous stable Python minor release relative to the latest stable Python release at execution time; it should not hard-code a specific fallback version in the skill. When several sources conflict, the workflow should choose the highest Python minor version mentioned or required by those sources, then adapt requirements to that version through environment-level dependency choices, compatibility shims, or setup-command changes. It should not mutate existing repo source files merely to force compatibility. If adaptation cannot be done within the service-safe environment setup boundary, it should report a blocker that names the conflicting sources and attempted target version.

The setup workflow should ensure `<topic-workspace-dir>/.gitignore` contains `.pixi/`, `tmp/`, and `.git/` while preserving unrelated entries. It should not add an `extern/orphan` ignore rule from this service skill.

Runtime commands that execute inside the prepared Topic Workspace environment should use the explicit Pixi command style: `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <command>`. Dependency mutation commands may use `pixi add --manifest-path <manifest_path> ...` and `pixi install --manifest-path <manifest_path> --environment <pixi_environment>`. The skill should not rely on activated shells or ambient Python environments.

`isomer-env-gate.md` should use a fixed Markdown section template so humans and later agents can find the same fields consistently without a separate parser:

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

Every section should be present. If a section does not apply, the agent should write `None.` or a short reason. Inferred repo-source warnings belong in `## Inferred Source Warnings` and should also be repeated in the final skill output.

Further command-level details may still be refined in later artifacts.

## Goals / Non-Goals

**Goals:**

- Leave a design placeholder so later artifacts can refine the concrete correction plan.
- Capture the command-style modular skill structure with short kebab-case subcommands, procedural/helper/misc grouping, and one-level reference pages.
- Capture that required inputs live inside executable subcommand pages rather than a central parent table.
- Capture the intended Topic Workspace Pixi layout.
- Capture the `user-intent/src/env-gate.md` verification gate.
- Capture generated `user-intent/derived/isomer-env-gate.md` as the operational readiness gate.
- Capture the fixed Markdown section template for `isomer-env-gate.md`.
- Capture `<topic-workspace-dir>/repos/<repo-name>` as the required location for independent repos needed by the task.
- Capture that repo sources may be agent-inferred or discovered, but such repos must be warning-labeled in `isomer-env-gate.md` and the final skill output.
- Capture package-source preferences: PyPI-first for Python packages, Pixi/Conda only when needed, and `nvidia` channel preferred for NVIDIA packages.
- Capture Python as the always-present Topic Workspace glue and orchestration language, independent of the target programming language.
- Capture Python version selection: recover from available context, default to the previous stable minor release when unspecified, and adapt conflicting requirements to the highest required version when possible.
- Capture starter Python dependencies: `scipy`, `mdutils`, `ruff`, `mkdocs-material`, `mypy`, `attrs`, `omegaconf`, `imageio`, `matplotlib`, `jsonschema`, and `jinja2`.
- Capture Topic Workspace VCS ignores: `.pixi/`, `tmp/`, and `.git/`, without adding an `extern/orphan` rule from this skill.
- Capture explicit Pixi command style for Topic Workspace runtime commands.
- Capture the workflow order from workspace resolution, to source gate, to repo materialization, to dependency inference, to derived gate, to Pixi installation, to Pixi verification commands.
- Capture `setup-for-topic-workspace` as the public full setup command with `fast-forward`/`auto` and `step-by-step`/`manual` modes.
- Capture compact step-by-step option tables with a recommendation line outside the table before each workflow step.
- Preserve the service-safe scope of `isomer-srv-env-setup`.
- Capture that direct Topic Workspace Pixi mutation is allowed during this skill invocation and does not require a separate Service Request.
- Keep future implementation focused on skill instructions and validation coverage.

**Non-Goals:**

- Do not decide every command-level correction in this placeholder.
- Do not expand the skill into live agent launch, general project management, or unrelated runtime operations.
- Do not add new dependencies to Isomer Labs itself or change Isomer CLI behavior from this design alone.

## Decisions

- Treat this change as a skill-instruction refinement centered on Topic Workspace Pixi materialization.
- State that `SKILL.md` should become a lean command router with a grouped `Subcommands` section and linked reference workflows.
- State that procedural subcommands are directly callable single-step workflow actions, helper subcommands are lower-level implementation commands, and misc subcommands hold support commands and shortcuts.
- State that `setup-for-topic-workspace` is the default full setup shortcut for concrete setup tasks that do not name a subcommand, while `resolve-workspace`, `read-gate`, `ensure-repos`, `derive-gate`, `install-deps`, and `verify-gate` are directly callable procedural step subcommands.
- State that `setup-for-topic-workspace` has `fast-forward`/`auto` and `step-by-step`/`manual` execution modes selected from the prompt.
- State that `fast-forward` mode executes the ordered setup steps directly, while `step-by-step` mode pauses before each step, presents a compact option table, states the recommended option outside the table, and waits for the user to choose before continuing.
- State that every executable subcommand reference page should have a numbered `## Workflow` near the top and a freeform fallback.
- State that every executable subcommand reference page should have its own `## Required Inputs` section, and that the parent `SKILL.md` should route to the selected page instead of maintaining a central required-inputs table for executable setup behavior.
- State that the skill should validate or produce `<topic-workspace-dir>/pixi.toml`, `<topic-workspace-dir>/pixi.lock`, and `<topic-workspace-dir>/.pixi/` for the selected Topic Workspace.
- State that independent repos required by the task live under `<topic-workspace-dir>/repos/<repo-name>`, where existing repos are inspected read-only and missing repos are downloaded, inferred, discovered, or reported as blockers.
- State that the skill should read `<topic-workspace-dir>/user-intent/src/env-gate.md` and use it to determine what post-setup commands or checks must pass before reporting readiness.
- State that the skill should write `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md` with concrete required-to-succeed dependencies, Pixi install commands, repo requirements, desired run commands, and verification checks derived from the source gate and available repo contents, especially when the source gate is vague.
- State that dependency inference should prefer PyPI for Python packages by default, use Pixi/Conda packages only when needed for the gate, and prefer the `nvidia` channel for NVIDIA tools.
- State that Topic Workspace setup should always keep Python available as the root orchestration layer while still installing the native tools required by non-Python targets.
- State that Python version selection should recover evidence from prompt, gate, and repo metadata; default to the previous stable minor release when unspecified; and choose the highest required version when sources conflict, adapting requirements where service-safe.
- State that starter Python dependencies should be installed through PyPI when missing or not already satisfied.
- State that `<topic-workspace-dir>/.gitignore` should include `.pixi/`, `tmp/`, and `.git/`, and should not gain an `extern/orphan` ignore entry from this skill.
- State that setup and verification commands should run through `pixi run --manifest-path <manifest_path> --environment <pixi_environment>`.
- State that `isomer-env-gate.md` should use the fixed Markdown section template and include every section even when the content is `None.`.
- State that old guidance requiring a separate Service Request for dependency repair or lockfile mutation should be replaced for this skill path by direct service-safe mutation of the selected Topic Workspace.
- Keep the skill's standard structure: lean `SKILL.md`, local references for detailed workflows, and validation through the service skill and skill-creator validators.
- Defer remaining command, guardrail, and output-contract details to the spec and task artifacts.

## Risks / Trade-offs

- [Risk] A placeholder design can hide unresolved requirements. Mitigation: keep open details explicit in the proposal, specs, and tasks before implementation.
- [Risk] Later fixes may reveal CLI behavior gaps rather than skill prose errors. Mitigation: update the OpenSpec artifacts before implementation if the scope broadens.
