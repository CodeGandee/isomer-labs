---
name: isomer-srv-env-setup
description: Use when an Isomer Labs agent needs to install, validate, prepare, or repair Pixi environments for Topic Workspaces, Service Requests, Agent Workspaces, or topic-scoped execution; relevant signals include topic_standalone_pixi_bindings, isomer-cli project doctor, runtime prepare, missing pixi.lock, stale readiness, or missing TopicEnvironmentReadinessRecord.
---

# Isomer Service Environment Setup

Set up and validate Isomer Labs Pixi environments without launching agents or inventing runtime behavior. This skill is a router: keep the entrypoint lean, then load the one reference workflow that matches the requested environment scope.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Handle help intent**. If the user asks for help, usage, or available functionality, answer from **Help** and stop unless they also ask for a concrete setup task.
2. **Select one workflow** from **Reference Workflows**. If the prompt does not name a workflow, use `topic-workspace`.
3. **Resolve required inputs** from the prompt, current repository, and Project Manifest. See **Required Inputs**.
4. **Load the selected reference file** and execute its `## Workflow`.
5. **Report results** using **Output Contract**.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the reference workflows, required inputs, and guardrails in this skill, then execute the plan.

## Reference Workflows

| Workflow | Load When | Reference |
| --- | --- | --- |
| `topic-workspace` | Install, validate, or prepare the shared Pixi environment for one Topic Workspace. | [references/topic-workspace.md](references/topic-workspace.md) |

Load exactly one reference workflow per turn. Do not read or execute unrelated environment workflows.

## Required Inputs

Recover these before asking the user:

| Input | Required When | Resolution |
| --- | --- | --- |
| workflow | Always | Use the prompt value, or default to `topic-workspace`. |
| Project root | Always | Use the provided path or resolve from the current working directory. |
| `topic-id` | `topic-workspace` | Read from the prompt or Project Manifest context. |
| `manifest_path` | When a topic Pixi binding exists | Read from the active `topic_standalone_pixi_bindings` entry. |
| `pixi_environment` | When a topic Pixi binding exists | Read from the active binding; default to `default` only when the binding omits it. |

When asking for missing input, separate `Required` values from `Optional` modifiers. If no optional inputs apply, say `Optional: none for this step.`

## Help

`isomer-srv-env-setup` prepares Isomer Labs Pixi environments for service-safe topic work. The available workflow is:

| Workflow | Purpose |
| --- | --- |
| `topic-workspace` | Prepare the shared Topic Workspace Pixi environment, record readiness, and validate it before launch-facing work. |

Example prompts:

- `$isomer-srv-env-setup help`
- `$isomer-srv-env-setup topic-workspace <topic-id>`
- `$isomer-srv-env-setup topic-workspace for <topic-id>`

## Output Contract

Report:

- `workflow`: selected workflow name.
- `project_root`: resolved Isomer Project root.
- `research_topic_id`: selected topic when relevant.
- `manifest_path`: Pixi manifest path when relevant.
- `pixi_environment`: selected Pixi environment when relevant.
- `commands_run`: commands executed, in order.
- `readiness_status`: ready, failed, blocked, stale, superseded, or not checked.
- `blockers`: missing inputs, failed preconditions, command failures, or repair requirements.
- `next_action`: safe follow-up, repair route, or stop condition.

## Guardrails

- Do not install or mutate a Topic Workspace environment until the target Topic Workspace and active Pixi binding are confirmed from the Project Manifest.
- Do not treat the Project-root Pixi environment as the default agent execution environment.
- Do not create per-agent Pixi environments unless a Service Request explicitly authorizes it.
- Do not skip `isomer-cli project doctor` read-only validation before mutating preparation steps.
- Do not infer `topic_standalone_pixi_bindings` from directory names; always read the Project Manifest.
- Do not launch Houmao agents, create Agent Instances, mutate unrelated Workspace Runtime records, or perform GUI work from this skill.
