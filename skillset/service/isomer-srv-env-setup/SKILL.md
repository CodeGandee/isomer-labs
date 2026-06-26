---
name: isomer-srv-env-setup
description: Use when an Isomer Labs agent needs gate-driven enclosed Pixi environment setup for a Topic Workspace, including env-gate.md, isomer-env-gate.md, topic_standalone_pixi_bindings, topic repos, Python version selection, starter Python dependencies, Topic Workspace VCS ignores, PyPI/Pixi dependency inference, NVIDIA channel preference, Pixi command style, explicit external runtime wiring, topic-local user-space fallback, no-sudo blockers, or readiness checks.
---

# Isomer Service Environment Setup

## Overview

Set up and validate the shared Topic Workspace Pixi environment for a user-specified runnable target. Keep setup enclosed and auditable: use Pixi-managed dependencies first, use explicit Pixi-run runtime wiring only when Pixi cannot fully provide a runtime piece, use topic-local user-space fallback only as a secondary option, and block privileged or machine-global mutation.

This skill is a command-style router: keep the entrypoint lean, choose one subcommand, then load that subcommand's reference page.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Handle help intent**. If the invocation has no prompt, or if the user asks for help, usage, or available functionality, answer from **Help** and stop unless they also ask for a concrete setup task.
2. **Select one subcommand** from the **Subcommands** tables. Prefer procedural or misc subcommands; use a helper subcommand only if one is added later and the user explicitly asks for it. If the prompt describes a concrete Topic Workspace setup task but does not name a subcommand, use `setup-for-topic-workspace`.
3. **Load the selected reference file**.
4. **Resolve that page's required inputs** from its `## Required Inputs` section, then execute its `## Workflow`.
5. **Report results** using **Output Contract**.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the subcommands, selected reference page, output contract, and guardrails in this skill, then execute the plan.

## Subcommands

Load only the subcommand pages needed for the user's task. Complex skills divide subcommands into three parts: procedural, helper, and misc.

### Procedural Subcommands

Procedural subcommands are the public single-step workflow API. Call them directly for manual or partial setup.

| Subcommand | Use For | Reference |
| --- | --- | --- |
| `resolve-workspace` | Resolve Project root, Research Topic, Topic Workspace, active Pixi binding, and setup preconditions. | [references/resolve-workspace.md](references/resolve-workspace.md) |
| `read-gate` | Read `user-intent/src/env-gate.md` and identify the runnable target. | [references/read-gate.md](references/read-gate.md) |
| `ensure-repos` | Find existing repos or acquire missing required repos under `repos/<repo-name>`. | [references/ensure-repos.md](references/ensure-repos.md) |
| `derive-gate` | Generate or update `user-intent/derived/isomer-env-gate.md`. | [references/derive-gate.md](references/derive-gate.md) |
| `install-deps` | Infer package sources and install dependencies through the Topic Workspace Pixi environment. | [references/install-deps.md](references/install-deps.md) |
| `verify-gate` | Run the desired command through Pixi and report readiness. | [references/verify-gate.md](references/verify-gate.md) |

### Helper Subcommands

Helper subcommands are lower-level commands called by procedural subcommands. This skill currently exposes no helper subcommands. If future helpers are added, list them here and keep them out of **Help** unless they become public workflow steps.

### Misc Subcommands

Misc subcommands are public support commands and shortcuts.

| Subcommand | Use For | Reference |
| --- | --- | --- |
| `help` | Explain this skill and list public subcommands. | This entrypoint |
| `setup-for-topic-workspace` | Run the full gate-driven Topic Workspace setup workflow. This is the default for concrete setup tasks that do not name a subcommand. | [references/setup-for-topic-workspace.md](references/setup-for-topic-workspace.md) |

Load exactly one reference page for the selected subcommand. The `setup-for-topic-workspace` reference may then load the procedural subcommand references it orchestrates.

Each executable reference page owns its `## Required Inputs` contract. Use the selected page as the self-contained input guide for direct calls.

## Help

`isomer-srv-env-setup` prepares a Topic Workspace Pixi environment so the user-specified target in `user-intent/src/env-gate.md` can run. It preserves environment enclosure by preferring Pixi-managed dependencies, recording any external runtime wiring that must be routed through Pixi-run commands, limiting fallback installs to topic-local user space, and refusing sudo or machine-global mutation. Public subcommands are grouped below.

Procedural subcommands:

| Subcommand | Purpose | Produces |
| --- | --- | --- |
| `resolve-workspace` | Resolve the Project root, Research Topic, Topic Workspace, Pixi manifest, and selected Pixi environment. | Resolved setup refs and blockers; no environment mutation. |
| `read-gate` | Read the source gate and extract the runnable target, repo hints, commands, and success criteria. | Source gate summary and readiness blockers. |
| `ensure-repos` | Find existing required repos or materialize missing repos under `<topic-workspace-dir>/repos/<repo-name>`. | Repo inventory and inspection notes; acquired topic repos and inferred-source warnings only for missing repos. |
| `derive-gate` | Write the fixed-section `isomer-env-gate.md` operational gate, including the enclosure strategy for each dependency or runtime need. | `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md`. |
| `install-deps` | Install inferred dependencies with Pixi first, record explicit external runtime wiring when needed, and use topic-local fallback only when Pixi cannot satisfy the gate. | Updated Topic Workspace Pixi environment files, `.gitignore`, dependency plan, enclosure records, and blockers. |
| `verify-gate` | Run the desired command through recorded Pixi-scoped commands and report readiness. | Gate execution results, readiness status, enclosure warnings, and blockers. |

Misc subcommands:

| Subcommand | Purpose | Produces |
| --- | --- | --- |
| `setup-for-topic-workspace` | Run the full setup flow in `fast-forward`/`auto` or `step-by-step`/`manual` mode. | Combined setup report, selected mode, repo state, derived gate, Pixi environment files, enclosure strategy, and readiness status. |
| `help` | Print what this skill does and how to use it. | Usage table and examples. |

Example prompts:

- `$isomer-srv-env-setup help`
- `$isomer-srv-env-setup`
- `$isomer-srv-env-setup setup-for-topic-workspace <topic-id> auto`
- `$isomer-srv-env-setup setup-for-topic-workspace <topic-id> manual`
- `$isomer-srv-env-setup read-gate for <topic-id>`
- `$isomer-srv-env-setup verify-gate for <topic-id>`

## Output Contract

Report:

- `subcommand`: selected subcommand.
- `mode`: selected `setup-for-topic-workspace` mode when relevant.
- `project_root`: resolved Isomer Project root.
- `research_topic_id`: selected Research Topic.
- `topic_workspace_dir`: Project Manifest-declared Topic Workspace directory.
- `manifest_path`: active Topic Workspace Pixi manifest path.
- `pixi_environment`: selected Pixi environment.
- `env_gate_path`: source gate path when relevant.
- `derived_gate_path`: generated gate path when relevant.
- `repos`: required repo names, paths, sources, and whether any source was inferred.
- `inferred_source_warnings`: warnings for repos acquired from inferred or discovered sources.
- `dependency_plan`: selected Python version, version evidence, starter Python dependencies, package sources, Pixi/PyPI choices, channels, editable installs, native tools, Python glue baseline, and enclosure strategy.
- `environment_enclosure`: dependency and runtime classification as Pixi-managed, Pixi-mediated external runtime wiring, topic-local user-space fallback, or blocked.
- `external_runtime_wiring`: any PATH, library path, compiler path, package-config path, CUDA variable, sourced script, or external runtime path used through Pixi-run commands.
- `topic_local_fallbacks`: any fallback installs under `<topic-workspace-dir>/.isomer-user-env/`, including commands, installed paths, changed files, and portability warnings.
- `enclosure_warnings`: warnings for external runtime wiring, topic-local fallbacks, host-specific paths, relocation risk, or missing enclosure records.
- `commands_run`: commands executed, in order.
- `changed_files`: environment files changed, especially `pixi.toml`, `pixi.lock`, `.pixi/`, `.gitignore`, `.isomer-user-env/` when used, and `isomer-env-gate.md`.
- `readiness_status`: ready, failed, blocked, or not checked.
- `blockers`: missing inputs, failed preconditions, command failures, out-of-scope requests, or repair requirements.
- `next_action`: safe follow-up, repair route, or stop condition.

## Guardrails

- Do not install or mutate a Topic Workspace environment until the selected Topic Workspace and active `topic_standalone_pixi_bindings` entry are confirmed from the Project Manifest.
- Direct setup mutation is allowed for the selected Topic Workspace Pixi environment after confirmation; do not require a separate Service Request for dependency, lockfile, install, or gate-command mutation in this workflow.
- Do not treat the Project-root Pixi environment as the Topic Workspace execution environment.
- Do not create or mutate per-agent Pixi environments unless a user task explicitly names an Agent Workspace-specific environment.
- Do not place required independent repos in the Project root, Agent Workspace, `.pixi/`, or another ad hoc location; use `<topic-workspace-dir>/repos/<repo-name>`.
- Do not modify an existing `<topic-workspace-dir>/repos/<repo-name>` during `ensure-repos`; inspect it as read-only evidence and report blockers if it is unsuitable.
- Do not infer `topic_standalone_pixi_bindings` from directory names; always read the Project Manifest.
- Do not choose repos, dependencies, Pixi install commands, setup commands, or verification commands before reading `user-intent/src/env-gate.md`.
- Apply the enclosure ladder before dependency mutation or verification: Pixi-managed install first, Pixi-mediated external runtime wiring second, topic-local user-space fallback under `<topic-workspace-dir>/.isomer-user-env/` third, and blockers for privileged or machine-global mutation.
- When running Topic Workspace setup, inspection, or verification commands inside the prepared environment, use `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <command>` instead of relying on the ambient shell environment. Explicitly sourced scripts and exported runtime paths are allowed only when recorded in `isomer-env-gate.md` and the execution log.
- Do not run `sudo`, mutate system package managers, edit global shell profiles, install global Python or Node packages, change `/etc`, run `ldconfig`, install daemons, change kernel drivers, or perform other privileged or machine-global setup from this skill. Report those needs as blockers or external prerequisites.
- Do not hide inferred repo sources; warning-label them in `isomer-env-gate.md` and final output.
- Do not launch Houmao agents, create Agent Instances, mutate unrelated Workspace Runtime records, perform GUI work, or make research decisions from this skill.
