# Topic Workspace Pixi Environment

Use this workflow to set up the shared Pixi environment for one Topic Workspace. The Topic Workspace Pixi environment is the default Python environment for all Agent Workspaces under one Research Topic unless an explicit Service Request authorizes a narrower environment.

## Contents

- [Workflow](#workflow)
- [Required Inputs](#required-inputs)
- [Preconditions](#preconditions)
- [Setup Commands](#setup-commands)
- [Topic Workspace Pixi Manifest](#topic-workspace-pixi-manifest)
- [Project Manifest Binding](#project-manifest-binding)
- [Readiness States](#readiness-states)
- [Repair and Divergence](#repair-and-divergence)
- [Guardrails](#guardrails)

## Workflow

When this reference workflow is selected, execute the following steps in order.

1. **Resolve inputs** from the prompt, current repository, and Project Manifest. See **Required Inputs**.
2. **Check preconditions** before running setup commands. See **Preconditions**.
3. **Run setup commands** from the Project root in the order defined by **Setup Commands**.
4. **Inspect readiness** using **Readiness States** and **Repair and Divergence**.
5. **Report the result** using the parent skill's output contract.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the required inputs, preconditions, setup commands, and guardrails in this reference, then execute the plan.

## Required Inputs

Recover these before asking the user:

| Input | Required When | Resolution |
| --- | --- | --- |
| `topic-id` | Always | Read from the prompt or Project Manifest context. |
| Project root | Always | Use the provided path or resolve from the current working directory. |
| `manifest_path` | Always for setup | Read from the active `topic_standalone_pixi_bindings` entry for the topic. |
| `pixi_environment` | Always for setup | Read from the active binding; use `default` only when the binding omits it. |

When asking for missing input, separate `Required` values from `Optional` modifiers. If no optional inputs apply, say `Optional: none for this step.`

## Preconditions

Before running setup commands:

1. Confirm the current working directory is inside the Isomer Project root.
2. Confirm `.isomer-labs/manifest.toml` exists.
3. Confirm the Research Topic is declared in the Project Manifest.
4. Confirm the Topic Workspace is declared under `topic_workspaces` in the Project Manifest.
5. Confirm the active `topic_standalone_pixi_bindings` entry for the topic exists.
6. Confirm the active binding's `manifest_path` points inside the Project root.

If any precondition fails, stop and report the failure. Do not guess paths or bindings.

## Setup Commands

Run these commands from the Project root in order.

### 1. Install Project-Level Pixi Dependencies

The Project-level Pixi environment supplies Isomer platform tools such as `isomer-cli`.

```bash
pixi install
```

### 2. Validate the Project Manifest

Run read-only validation before mutating topic environment state.

```bash
pixi run isomer-cli --print-json project validate
```

### 3. Run Read-Only Topic Diagnostics

`project doctor` does not install environments or mutate Workspace Runtime.

```bash
pixi run isomer-cli --print-json project doctor --topic <topic-id>
```

Inspect the output for:

- missing `topic_standalone_pixi_bindings`;
- a `manifest_path` that does not exist or lies outside the Project root;
- an unknown `pixi_environment`;
- a missing `pixi.lock`;
- `requires-pixi` version mismatches.

### 4. Install the Topic Workspace Pixi Environment

Use the manifest path from the active binding.

```bash
pixi install --manifest-path <manifest-path>
```

Example:

```bash
pixi install --manifest-path isomer-content/topic-ws/<topic-id>/pixi.toml
```

### 5. Initialize Workspace Runtime

This creates runtime directories such as `artifacts/`, `agents/`, `tasks/`, `runs/`, `views/`, and `logs/` under the Topic Workspace.

```bash
pixi run isomer-cli --print-json project runtime init --topic <topic-id>
```

### 6. Record Topic Environment Readiness

`project runtime prepare` checks the active binding and writes a `TopicEnvironmentReadinessRecord`. It does not install dependencies or repair the environment.

```bash
pixi run isomer-cli --print-json project runtime prepare --topic <topic-id>
```

### 7. Validate Readiness Before Launch-Facing Work

```bash
pixi run isomer-cli --print-json project runtime validate --topic <topic-id> --require-ready-readiness
```

If this command reports that readiness is not `ready`, stop and route the repair through a Service Request.

## Topic Workspace Pixi Manifest

The Topic Workspace Pixi manifest is usually one of:

- `isomer-content/topic-ws/<topic-id>/pixi.toml`;
- `isomer-content/topic-ws/<topic-id>/pyproject.toml` for fresh Projects;
- `<content-dir>/topic-ws/<topic-id>/pixi.toml` when Project init selected a custom content root.

It declares the topic-scoped Python version, research dependencies, and optional named environments for task-specific dependency sets.

Minimal `pyproject.toml` form:

```toml
[project]
name = "<topic-id>"
requires-python = ">= 3.11"

[tool.pixi.workspace]
channels = ["conda-forge"]
platforms = ["linux-aarch64"]

[tool.pixi.dependencies]
python = "3.11.*"

[tool.pixi.environments]
default = { solve-group = "default" }
```

The `default` environment is the shared Agent Workspace environment unless the active binding selects another named environment.

## Project Manifest Binding

The active binding lives in `.isomer-labs/manifest.toml` under `[[topic_standalone_pixi_bindings]]`:

```toml
[[topic_standalone_pixi_bindings]]
research_topic_id = "<topic-id>"
manifest_path = "isomer-content/topic-ws/<topic-id>/pixi.toml"
pixi_environment = "default"
purpose = "agent-execution"
status = "active"
```

Read the Project Manifest to resolve `manifest_path` and `pixi_environment`. Do not infer these values from the Topic Workspace directory name.

## Readiness States

`project runtime prepare` records one of these statuses in Workspace Runtime:

- `ready`: manifest, lockfile, and selected environment are present and valid.
- `failed`: the manifest is missing, the environment is unknown, or the lockfile is absent.
- `blocked`: a precondition prevents readiness checking, such as a missing Project Manifest.
- `stale`: a previous readiness record was superseded by a manifest or binding change.
- `superseded`: a newer readiness record exists.

## Repair and Divergence

Any mutating environment work beyond `pixi install` is a Service Request:

- installing or repairing Topic Workspace dependencies when `pixi install` fails;
- regenerating `pixi.lock`;
- adding a new named environment to the Topic Workspace manifest;
- creating a divergent environment for a specific Agent Workspace.

The Service Request must name the target scope, task, expected output, and completion observation rules. The Service Agent Instance records support Artifacts and Provenance Records.

## Guardrails

- Do not run `isomer-cli project runtime prepare` before `isomer-cli project doctor --topic <topic-id>`.
- Do not run `pixi install --manifest-path` without confirming the manifest path comes from an active `topic_standalone_pixi_bindings` entry.
- Do not treat the Project-root Pixi environment as the Topic Workspace execution environment.
- Do not create per-agent Pixi manifests or `.pixi/` directories unless a Service Request authorizes it.
- Do not regenerate `pixi.lock` silently; route lockfile changes through a Service Request.
- Do not proceed to launch-facing work if `isomer-cli project runtime validate --require-ready-readiness` fails.
