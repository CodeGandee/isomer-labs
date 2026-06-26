## 1. Skill Structure and Routing

- [x] 1.1 Revise `skillset/service/isomer-srv-env-setup/SKILL.md` into a lean command router with a grouped `Subcommands` section.
- [x] 1.2 Add public subcommands `help`, `setup-for-topic-workspace`, `resolve-workspace`, `read-gate`, `ensure-repos`, `derive-gate`, `install-deps`, and `verify-gate`.
- [x] 1.3 Make `help` the default when no prompt is given and `setup-for-topic-workspace` the default for concrete setup tasks that do not name a subcommand.
- [x] 1.4 Create or revise one-level reference pages for executable subcommands, including `references/setup-for-topic-workspace.md`, `references/resolve-workspace.md`, `references/read-gate.md`, `references/ensure-repos.md`, `references/derive-gate.md`, `references/install-deps.md`, and `references/verify-gate.md`.
- [x] 1.5 Ensure every executable subcommand reference page has a numbered `## Workflow` near the top and a freeform fallback.
- [x] 1.6 Update the parent skill help, required inputs, output contract, and guardrails so they mention gate-driven Topic Workspace setup without expanding into agent launch or unrelated runtime management.
- [x] 1.7 Confirm the parent skill does not tell agents to treat the Project root or an Agent Workspace as the Topic Workspace Pixi root.
- [x] 1.8 Remove or revise wording that requires a separate Service Request before direct Topic Workspace Pixi dependency, lockfile, or install mutation during this skill workflow.
- [x] 1.9 Divide subcommands into procedural, helper, and misc groups for complex-skill readability.
- [x] 1.10 Teach `setup-for-topic-workspace` to select `fast-forward`/`auto` or `step-by-step`/`manual` mode from the prompt, accepting `fast-foward` as an alias for `fast-forward`.

## 2. Topic Workspace Workflow

- [x] 2.1 Revise `references/setup-for-topic-workspace.md` so it orchestrates `resolve-workspace`, `read-gate`, `ensure-repos`, `derive-gate`, `install-deps`, and `verify-gate` in order.
- [x] 2.2 Revise `references/resolve-workspace.md` so it resolves the Project Manifest-declared Topic Workspace and active `topic_standalone_pixi_bindings`.
- [x] 2.3 Add the required layout contract for `<topic-workspace-dir>/.pixi/`, `<topic-workspace-dir>/pixi.toml`, `<topic-workspace-dir>/pixi.lock`, `<topic-workspace-dir>/repos/<repo-name>`, `<topic-workspace-dir>/user-intent/src/env-gate.md`, and `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md`.
- [x] 2.4 Revise `references/read-gate.md` so it reads `<topic-workspace-dir>/user-intent/src/env-gate.md` before choosing repos, dependencies, Pixi install commands, setup commands, or verification commands.
- [x] 2.5 Make missing or unreadable `user-intent/src/env-gate.md` a readiness blocker with a clear repair instruction.
- [x] 2.6 In `setup-for-topic-workspace`, implement `fast-forward` mode as direct ordered execution that stops only for blockers, missing required inputs, unsafe ambiguity, or out-of-scope requests.
- [x] 2.7 In `setup-for-topic-workspace`, implement `step-by-step` mode so it pauses before each step, explains the step, presents options in a table with `Option`, `Explain`, and `Pros and Cons`, states the recommendation outside the table, waits for user consent, executes one chosen action, and reports the result before continuing.

## 3. Repo and Gate Handling

- [x] 3.1 Teach the workflow to identify whether the gate requires independent repos and to use `<topic-workspace-dir>/repos/<repo-name>` as the only location for those repos.
- [x] 3.2 Teach the workflow to find existing repos, download or materialize repos when the source is known, infer or search for repo sources when needed, and block readiness when a required repo source remains unverifiable.
- [x] 3.3 Teach `ensure-repos` to treat existing repo directories as read-only evidence and to report blockers instead of mutating unsuitable existing repos.
- [x] 3.3 Teach the workflow to inspect `env-gate.md` and required repo contents before finalizing `user-intent/derived/isomer-env-gate.md`.
- [x] 3.4 Specify that `isomer-env-gate.md` records repo names, expected repo paths, acquisition sources when known, inferred dependencies, Pixi install commands, Pixi run commands, expected outputs, and pass/fail criteria.
- [x] 3.5 Require `isomer-env-gate.md` and the final output to warn when a repo source was inferred or discovered by the agent rather than explicitly provided by the user.
- [x] 3.6 Add the fixed `isomer-env-gate.md` Markdown section template with `Source Intent`, `Runnable Target`, `Repo Requirements`, `Inferred Source Warnings`, `Dependency Plan`, `Pixi Install Commands`, `Verification Commands`, `Expected Results`, `Blockers`, and `Execution Log`.

## 4. Dependency Inference and Pixi Execution

- [x] 4.1 Teach the workflow to infer language runtimes, libraries, tools, package-manager requirements, editable repo installs, and command-line programs needed for `env-gate.md` to pass.
- [x] 4.2 Teach the workflow to prefer PyPI for Python packages by default, use Pixi/Conda packages when required for the gate, and record the selected source for each dependency.
- [x] 4.3 Teach the workflow to prefer the `nvidia` Pixi channel over `conda-forge` for NVIDIA tools and runtime packages, including recording fallbacks.
- [x] 4.4 Teach the workflow to always include Python as the Topic Workspace root glue and orchestration language, even when the runnable target uses another language.
- [x] 4.5 Teach the workflow to install native toolchains, package managers, runtimes, and command-line tools required by non-Python targets in addition to the Python glue baseline.
- [x] 4.6 Teach the workflow to use Pixi from the Topic Workspace root to add or install inferred dependencies into the Topic Workspace environment.
- [x] 4.7 Teach the workflow to run the desired command through Pixi and treat that command result as the final gate outcome.
- [x] 4.8 Require blockers to name any dependency that cannot be inferred or installed, why it is needed, and what information or manual action is required.
- [x] 4.9 Require the workflow to report changed environment files, commands run, readiness status, and blockers after direct setup mutation.

## 5. Validation

- [x] 5.1 Validate the revised skill with the repository's skill formatting or skill-creator checks when available.
- [x] 5.2 Run `openspec validate revise-service-env-setup-skill --strict`.
- [x] 5.3 Review the final diff to ensure the service-safe boundary remains intact and the workflow order is source gate, repos, dependency inference, derived gate, Pixi install, desired command, readiness.
