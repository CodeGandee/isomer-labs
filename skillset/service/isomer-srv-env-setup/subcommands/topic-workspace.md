# Topic Workspace Pixi Environment Setup

Use this subcommand to set up the Pixi environment for a topic-level agent team workspace. The Topic Workspace Pixi environment is the shared default Python environment for all Agent Workspaces under one Research Topic.

## When to Use

Use `topic-workspace` when:

- a new Topic Workspace needs its Pixi environment installed for the first time;
- the Topic Workspace Pixi manifest or lockfile changed and the environment must be refreshed;
- `isomer-cli doctor --topic <topic-id>` reports a missing or stale environment;
- an upstream plan asks to prepare topic environment readiness before launching agents.

This subcommand covers Pixi installation, read-only validation, runtime preparation, and readiness checks. It does not cover Houmao agent launch, mailbox setup, or GUI rendering.

## Required Inputs

Recover these from the prompt, current repo, and Project Manifest before asking questions:

| Input | Required when |
| --- | --- |
| `topic-id` | Always. |
| Project root | Resolve from the current working directory or a provided path. |
| `manifest_path` | Optional; read from the active `topic_standalone_pixi_bindings` entry for the topic. |
| `pixi_environment` | Optional; read from the active binding; default to `default` if absent. |

When asking for missing input, separate `Required` values from `Optional` modifiers. If no optional inputs apply, say `Optional: none for this step.`

## Pre-conditions

Before running setup commands:

1. Confirm the current working directory is inside the Isomer Project root.
2. Confirm the Project Manifest exists at `.isomer-labs/manifest.toml`.
3. Confirm the Research Topic is declared in the Project Manifest.
4. Confirm the Topic Workspace is declared under `topic_workspaces` in the Project Manifest.
5. Confirm the active `topic_standalone_pixi_bindings` entry for the topic exists and points to a manifest inside the Project root.

If any pre-condition fails, stop and report the failure. Do not guess paths or bindings.

## Setup Steps

Run these steps from the Project root in order.

### 1. Install Project-level Pixi dependencies

The Project-level Pixi environment supplies Isomer platform tools such as `isomer-cli`.

```bash
pixi install
```

### 2. Validate the Project Manifest

Run read-only validation before any mutating work.

```bash
pixi run isomer-cli --print-json validate
```

### 3. Run read-only topic diagnostics

`doctor` does not install environments or mutate Workspace Runtime.

```bash
pixi run isomer-cli --print-json doctor --topic <topic-id>
```

Inspect the output for:

- missing `topic_standalone_pixi_bindings`;
- a `manifest_path` that does not exist or lies outside the Project root;
- an unknown `pixi_environment`;
- a missing `pixi.lock`;
- `requires-pixi` version mismatches.

### 4. Install the Topic Workspace Pixi environment

Use the manifest path from the active binding.

```bash
pixi install --manifest-path <manifest-path>
```

For example, if `manifest_path` is `topic-workspaces/<topic-id>/pixi.toml`:

```bash
pixi install --manifest-path topic-workspaces/<topic-id>/pixi.toml
```

### 5. Initialize Workspace Runtime

This creates runtime directories such as `artifacts/`, `agents/`, `tasks/`, `runs/`, `views/`, and `logs/` under the Topic Workspace.

```bash
pixi run isomer-cli --print-json runtime init --topic <topic-id>
```

### 6. Record topic environment readiness

`runtime prepare` checks the active binding and writes a `TopicEnvironmentReadinessRecord`. It does not install dependencies or repair the environment.

```bash
pixi run isomer-cli --print-json runtime prepare --topic <topic-id>
```

### 7. Validate readiness before launch-facing work

```bash
pixi run isomer-cli --print-json runtime validate --topic <topic-id> --require-ready-readiness
```

If this command reports that readiness is not `ready`, stop and route the repair to a Service Request.

## Topic Workspace Pixi Manifest

The Topic Workspace Pixi manifest, typically `topic-workspaces/<topic-id>/pixi.toml` or `topic-workspaces/<topic-id>/pyproject.toml`, declares:

- the topic-scoped Python version;
- research dependencies;
- optional named environments for task-specific dependency sets.

A minimal example in `pyproject.toml` form:

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
manifest_path = "topic-workspaces/<topic-id>/pixi.toml"
pixi_environment = "default"
purpose = "agent-execution"
status = "active"
```

Read the Project Manifest to resolve `manifest_path` and `pixi_environment`. Do not infer these values from the Topic Workspace directory name.

## Readiness States

`runtime prepare` records one of these statuses in Workspace Runtime:

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

The Service Request must name the target scope, the task, the expected output, and the completion observation rules. The Service Agent Instance records support Artifacts and Provenance Records.

## Guardrails

- Do not run `isomer-cli runtime prepare` before `isomer-cli doctor --topic <topic-id>`.
- Do not run `pixi install --manifest-path` without confirming the manifest path comes from an active `topic_standalone_pixi_bindings` entry.
- Do not treat the Project-root Pixi environment as the Topic Workspace execution environment.
- Do not create per-agent Pixi manifests or `.pixi/` directories unless a Service Request authorizes it.
- Do not regenerate `pixi.lock` silently; route lockfile changes through a Service Request.
- Do not proceed to launch-facing work if `runtime validate --require-ready-readiness` fails.

## Related Documents

- `docs/runtime-and-files.md`: durable runtime files, Topic Workspace files, and Workspace Runtime records.
- `.imsight-arts/project-explore/design-choice/design-topic-workspace-pixi-workspace-standard.md`: accepted Topic Workspace Pixi workspace standard.
- `.imsight-arts/project-explore/adrs/0025-project-manifest-owns-topic-pixi-env-bindings.md`: Project Manifest owns bindings.
- `.imsight-arts/project-explore/adrs/0026-standalone-pixi-isolation-uses-separate-bindings.md`: standalone binding table.
- `.imsight-arts/project-explore/adrs/0027-topic-workspaces-are-default-pixi-workspaces.md`: Topic Workspaces are default Pixi workspaces.
