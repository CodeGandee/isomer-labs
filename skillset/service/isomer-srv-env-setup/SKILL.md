---
name: isomer-srv-env-setup
description: Use when an Isomer Labs agent needs gate-driven Pixi environment setup for a Topic Workspace, including env-gate.md, isomer-env-gate.md, topic_standalone_pixi_bindings, topic repos, PyPI/Pixi dependency inference, NVIDIA channel preference, or readiness checks.
---

# Isomer Service Environment Setup

## Overview

Set up and validate the shared Topic Workspace Pixi environment for a user-specified runnable target. This skill is a command-style router: keep the entrypoint lean, choose one subcommand, then load that subcommand's reference page.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Handle help intent**. If the user asks for help, usage, or available functionality, answer from **Help** and stop unless they also ask for a concrete setup task.
2. **Select one subcommand** from **Subcommands**. If the prompt does not name a subcommand, use `topic-workspace`.
3. **Resolve required inputs** from the prompt, current repository, and Project Manifest when the selected subcommand needs them. See **Required Inputs**.
4. **Load the selected reference file** and execute its `## Workflow`.
5. **Report results** using **Output Contract**.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the subcommands, required inputs, output contract, and guardrails in this skill, then execute the plan.

## Subcommands

| Subcommand | Use For | Reference |
| --- | --- | --- |
| `help` | Explain this skill and list public subcommands. | This entrypoint |
| `topic-workspace` | Run the full gate-driven Topic Workspace setup workflow. This is the default subcommand. | [references/topic-workspace.md](references/topic-workspace.md) |
| `resolve-workspace` | Resolve Project root, Research Topic, Topic Workspace, active Pixi binding, and setup preconditions. | [references/resolve-workspace.md](references/resolve-workspace.md) |
| `read-gate` | Read `user-intent/src/env-gate.md` and identify the runnable target. | [references/read-gate.md](references/read-gate.md) |
| `get-repos` | Find, infer, download, or verify required repos under `repos/<repo-name>`. | [references/get-repos.md](references/get-repos.md) |
| `derive-gate` | Generate or update `user-intent/derived/isomer-env-gate.md`. | [references/derive-gate.md](references/derive-gate.md) |
| `install-deps` | Infer package sources and install dependencies through the Topic Workspace Pixi environment. | [references/install-deps.md](references/install-deps.md) |
| `verify-gate` | Run the desired command through Pixi and report readiness. | [references/verify-gate.md](references/verify-gate.md) |

Load exactly one reference page for the selected subcommand. The `topic-workspace` reference may then load the step subcommand references it orchestrates.

## Required Inputs

Recover these before asking the user:

| Input | Required When | Resolution |
| --- | --- | --- |
| `subcommand` | Always | Use the prompt value, or default to `topic-workspace`. |
| Project root | Any setup subcommand | Use the provided path or resolve from the current working directory. |
| `research_topic_id` | Any setup subcommand | Read from the prompt or Project Manifest context. Ask only when several topics remain plausible. |
| `topic_workspace_dir` | Any setup subcommand after `resolve-workspace` | Read from the Project Manifest-declared Topic Workspace for the selected Research Topic. |
| `manifest_path` | Any Pixi mutation or verification | Read from the active `topic_standalone_pixi_bindings` entry. |
| `pixi_environment` | Any Pixi mutation or verification | Read from the active binding; use `default` only when the binding omits it. |
| `env_gate_path` | `read-gate` and later | Use `<topic-workspace-dir>/user-intent/src/env-gate.md`. |
| `derived_gate_path` | `derive-gate` and later | Use `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md`. |

When asking for missing input, separate `Required` values from `Optional` modifiers. If no optional inputs apply, say `Optional: none for this step.`

## Help

`isomer-srv-env-setup` prepares a Topic Workspace Pixi environment so the user-specified target in `user-intent/src/env-gate.md` can run. The public subcommands are:

| Subcommand | Purpose |
| --- | --- |
| `topic-workspace` | Run the full setup flow: resolve workspace, read the gate, get repos, derive the operational gate, install dependencies, and verify readiness. |
| `resolve-workspace` | Resolve the Project root, Research Topic, Topic Workspace, Pixi manifest, and selected Pixi environment. |
| `read-gate` | Read the source gate and extract the runnable target, repo hints, commands, and success criteria. |
| `get-repos` | Materialize required repos under `<topic-workspace-dir>/repos/<repo-name>`. |
| `derive-gate` | Write the fixed-section `isomer-env-gate.md` operational gate. |
| `install-deps` | Install inferred dependencies with Pixi, using PyPI-first Python package rules and NVIDIA channel preference. |
| `verify-gate` | Run the desired command through Pixi and report readiness. |

Example prompts:

- `$isomer-srv-env-setup help`
- `$isomer-srv-env-setup topic-workspace <topic-id>`
- `$isomer-srv-env-setup read-gate for <topic-id>`
- `$isomer-srv-env-setup verify-gate for <topic-id>`

## Output Contract

Report:

- `subcommand`: selected subcommand.
- `project_root`: resolved Isomer Project root.
- `research_topic_id`: selected Research Topic.
- `topic_workspace_dir`: Project Manifest-declared Topic Workspace directory.
- `manifest_path`: active Topic Workspace Pixi manifest path.
- `pixi_environment`: selected Pixi environment.
- `env_gate_path`: source gate path when relevant.
- `derived_gate_path`: generated gate path when relevant.
- `repos`: required repo names, paths, sources, and whether any source was inferred.
- `inferred_source_warnings`: warnings for repos acquired from inferred or discovered sources.
- `dependency_plan`: package sources, Pixi/PyPI choices, channels, editable installs, native tools, and Python glue baseline.
- `commands_run`: commands executed, in order.
- `changed_files`: environment files changed, especially `pixi.toml`, `pixi.lock`, `.pixi/`, and `isomer-env-gate.md`.
- `readiness_status`: ready, failed, blocked, or not checked.
- `blockers`: missing inputs, failed preconditions, command failures, out-of-scope requests, or repair requirements.
- `next_action`: safe follow-up, repair route, or stop condition.

## Guardrails

- Do not install or mutate a Topic Workspace environment until the selected Topic Workspace and active `topic_standalone_pixi_bindings` entry are confirmed from the Project Manifest.
- Direct setup mutation is allowed for the selected Topic Workspace Pixi environment after confirmation; do not require a separate Service Request for dependency, lockfile, install, or gate-command mutation in this workflow.
- Do not treat the Project-root Pixi environment as the Topic Workspace execution environment.
- Do not create or mutate per-agent Pixi environments unless a user task explicitly names an Agent Workspace-specific environment.
- Do not place required independent repos in the Project root, Agent Workspace, `.pixi/`, or another ad hoc location; use `<topic-workspace-dir>/repos/<repo-name>`.
- Do not infer `topic_standalone_pixi_bindings` from directory names; always read the Project Manifest.
- Do not choose repos, dependencies, Pixi install commands, setup commands, or verification commands before reading `user-intent/src/env-gate.md`.
- Do not hide inferred repo sources; warning-label them in `isomer-env-gate.md` and final output.
- Do not launch Houmao agents, create Agent Instances, mutate unrelated Workspace Runtime records, perform GUI work, or make research decisions from this skill.
