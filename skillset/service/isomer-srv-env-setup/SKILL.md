---
name: isomer-srv-env-setup
description: Set up Pixi environments for a given Isomer Labs purpose. Routes to subcommand pages that teach the agent how to install, validate, and prepare topic-scoped or service-scoped Pixi environments.
license: MIT
---

# Isomer Service Environment Setup

Use this skill when you need to set up or repair a Pixi environment for an Isomer Labs purpose. The skill routes to subcommand pages; each page teaches one environment setup workflow. Do not run unrelated Pixi commands from this skill.

## Activation

- Use this skill when the user asks to set up a Pixi environment for a topic workspace, service request, agent workspace, or other Isomer Labs purpose.
- If the operation is unclear, default to `topic-workspace`.
- If the user invokes explicit help intent, answer from `## Help` before choosing a subcommand.

## Help

When the user asks `$isomer-srv-env-setup help`, `help for isomer-srv-env-setup`, `usage for isomer-srv-env-setup`, `available functionality for isomer-srv-env-setup`, or what this skill can do, answer from this section before choosing a subcommand, inspecting state, or asking missing-input questions. This is read-only help: do not run commands, mutate files, or alter environment state during help. If the user asks a concrete task such as "help me set up the topic workspace Pixi env for topic X", route to the matching subcommand instead of stopping at generic help.

Purpose: teach agents how to set up Pixi environments for Isomer Labs purposes.

Available subcommands:

- `topic-workspace`: set up the Pixi environment for a topic-level agent team workspace.

Common starting prompts:

- `$isomer-srv-env-setup help`
- `$isomer-srv-env-setup topic-workspace <topic-id>`
- `$isomer-srv-env-setup topic-workspace for <topic-id>`

Related skills and boundaries:

- Use `houmao-agent-instance` or `houmao-agent-definition` to launch agents after the environment is ready.
- Use `houmao-project-mgr` for Houmao project overlay lifecycle, not Pixi environment installation.
- Use `isomer-cli project doctor` and `isomer-cli project runtime` commands as described in the subcommand pages; do not invent equivalent behavior.

## Subcommands

| Subcommand | Page | Use when |
| --- | --- | --- |
| `topic-workspace` | [subcommands/topic-workspace.md](subcommands/topic-workspace.md) | You need to install, validate, or prepare the Pixi environment for a Topic Workspace. |

Load exactly one subcommand page per turn. Read only the page that matches the user's request.

## Required Inputs

Recover these from the prompt, current repo, and Project Manifest before asking questions:

| Input | Required when |
| --- | --- |
| subcommand | Not safely inferred; default to `topic-workspace` when unclear. |
| `topic-id` | `topic-workspace` subcommand. |
| Project root | Resolve from the current working directory or a provided path. |
| `manifest_path` | Optional; read from `topic_standalone_pixi_bindings` in the Project Manifest when present. |
| `pixi_environment` | Optional; read from the active binding when present; otherwise use `default`. |

When asking for missing input, separate `Required` values from `Optional` modifiers. If no optional inputs apply, say `Optional: none for this step.`

## Routing

1. Identify the subcommand from the prompt. If it is missing or ambiguous, default to `topic-workspace`.
2. Load the matching subcommand page from the table above.
3. Follow that page's steps in order.
4. Report the result of the last command and any readiness status.

## Guardrails

- Do not install or mutate Topic Workspace environments without confirming the target Topic Workspace and active Pixi binding.
- Do not treat Project-root Pixi environments as the default agent execution environment.
- Do not create per-agent Pixi environments unless a Service Request explicitly authorizes it.
- Do not skip `isomer-cli project doctor` read-only validation before mutating preparation steps.
- Do not silently infer `topic_standalone_pixi_bindings` from directory names; always read the Project Manifest.
