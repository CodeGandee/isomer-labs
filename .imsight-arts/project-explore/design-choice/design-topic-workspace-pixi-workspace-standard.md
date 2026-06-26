# Topic Workspace Pixi Workspace Standard

This design-choice record defines the default Python environment setup preference for Isomer Labs: every Topic Workspace is a Pixi workspace. The Topic Workspace Pixi environment is the shared default Python environment for all Agent Workspaces under that Research Topic, giving agents topic-scoped dependency sharing while keeping topics isolated from one another.

## Status

accepted

## Default Preference

- The default Python environment for research agents is created and managed inside the Topic Workspace.
- Each Topic Workspace has its own Pixi manifest, lockfile, and environment directory.
- All Agent Workspaces under one Topic Workspace share that Topic Workspace's Pixi environment by default.
- Different Research Topics do not share Python environments.

## Scope

This standard applies to:

- New Topic Workspaces created after this decision.
- The default environment setup for Agent Workspaces.
- `isomer-cli doctor`, `runtime prepare`, and `runtime validate` behavior for topic environment readiness.
- Project Manifest bindings that point to Topic Workspace Pixi manifests.

It does not forbid Project-root Pixi environments, but those are reserved for Isomer platform tooling rather than research agent execution.

## Topic Workspace Layout

A Topic Workspace with id `<topic-id>` and default path `topic-workspaces/<topic-id>/` contains:

```
topic-workspaces/<topic-id>/
  pixi.toml                    # Topic Workspace Pixi manifest
  pixi.lock                    # Resolved dependency lockfile
  .pixi/                       # Pixi environment directory
  state.sqlite                 # Workspace Runtime database
  artifacts/                   # Workspace-level research Artifacts
  agents/                      # Agent Workspace directories
  tasks/                       # Research Task support files
  runs/                        # Run support files
  views/                       # View Manifest support files
  logs/                        # Workspace-level logs
```

The manifest may be `pyproject.toml` instead of `pixi.toml` when the Topic Workspace also needs Python package metadata. The lockfile must accompany the manifest.

## Manifest Content

The Topic Workspace Pixi manifest declares the Python version, research dependencies, and optional task-specific environments. A minimal example:

```toml
[project]
name = "flash-attention-gb10"
requires-python = ">= 3.11"

[tool.pixi.workspace]
channels = ["conda-forge"]
platforms = ["linux-aarch64"]

[tool.pixi.dependencies]
python = "3.11.*"
torch = ">= 2.3.0"
numpy = ">= 1.26.0"

[tool.pixi.environments]
measure = { features = ["measure"], solve-group = "default" }

[tool.pixi.feature.measure]
dependencies = { matplotlib = ">= 3.9.0" }
```

The `default` environment is the shared Agent Workspace environment unless a binding selects another named environment.

## Project Manifest Binding

The Project Manifest may record an explicit Topic Workspace Pixi workspace target through `[[topic_standalone_pixi_bindings]]`. If no active explicit entry exists for the Research Topic, the effective target is the registered Topic Workspace directory and the binding source is `implicit-default`.

```toml
[[topic_standalone_pixi_bindings]]
research_topic_id = "flash-attention-gb10"
manifest_path_or_dir = "topic-workspaces/flash-attention-gb10/pixi.toml"
pixi_environment = "default"
purpose = "agent-execution"
status = "active"

[[topic_standalone_pixi_bindings]]
research_topic_id = "flash-attention-gb10"
manifest_path_or_dir = "topic-workspaces/flash-attention-gb10"
pixi_environment = "measure"
purpose = "measurement-tasks"
status = "active"
```

The `manifest_path_or_dir` value is relative to the Project root. It may name a manifest file or a directory. Isomer passes the target to Pixi with `pixi info --json --manifest-path <target>`, then accepts the result only when Pixi's resolved manifest and selected environment prefix are confined to the registered Topic Workspace.

## Project-root Pixi Environment

The Project root may keep its own Pixi manifest for Isomer platform tooling. It supplies the environment used to run `isomer-cli` and related platform commands. It is not the default execution environment for research agents unless a specific Research Topic explicitly binds to it through `[[topic_pixi_environment_bindings]]`.

## Agent Workspace Inheritance

Agent Workspaces live under `<topic-workspace>/agents/<agent-instance-id>/`. Each Agent Workspace inherits the selected Topic Workspace Pixi environment by default. The Agent Workspace directory does not contain its own Pixi manifest, lockfile, or `.pixi/` directory.

If an Agent Workspace needs a divergent environment, the Operator Agent or Project Operator Session opens a Service Request. The Service Agent Instance may create an isolated environment only after the Service Request is recorded, and it must record support Artifacts and Provenance Records.

## CLI Setup Workflow

From the Project root:

```bash
# 1. Install Isomer platform tooling dependencies.
pixi install

# 2. Validate Project Manifest and topic bindings.
pixi run isomer-cli --print-json validate
pixi run isomer-cli --print-json doctor --topic <topic-id>
```

For the Topic Workspace:

```bash
# 3. Install the Topic Workspace Pixi environment.
pixi install --manifest-path topic-workspaces/<topic-id>/pixi.toml

# 4. Initialize Workspace Runtime.
pixi run isomer-cli --print-json runtime init --topic <topic-id>

# 5. Record topic environment readiness.
pixi run isomer-cli --print-json runtime prepare --topic <topic-id>

# 6. Validate readiness before launch-facing work.
pixi run isomer-cli --print-json runtime validate --topic <topic-id> --require-ready-readiness

# 7. Create Agent Team Instance records and Agent Workspace directories.
pixi run isomer-cli --print-json team-instances create \
  --topic <topic-id> \
  --id <ati-id>
```

Agents launched under the Topic Workspace use the Topic Workspace Pixi environment by default. No per-agent Pixi install step is required.

## Readiness Checks

`isomer-cli doctor --topic <topic-id>` performs read-only checks:

- The Topic Workspace exists and is registered in the Project Manifest.
- The explicit `manifest_path_or_dir` target or implicit registered Topic Workspace directory target resolves through Pixi.
- Pixi's resolved manifest path is inside the registered Topic Workspace.
- The selected `pixi_environment`, fixed to `default` for implicit defaults, is reported by Pixi with an environment prefix under `<topic-workspace>/.pixi/`.
- A matching `pixi.lock` is present.
- `requires-pixi` constraints, if declared, are satisfied by the host Pixi executable.

`doctor` does not install environments, create lockfiles, or write Workspace Runtime records.

## Runtime Prepare

`isomer-cli runtime prepare --topic <topic-id>` records a `TopicEnvironmentReadinessRecord`:

- It resolves the effective Topic Workspace Pixi binding target for the Research Topic.
- It records `ready` when Pixi resolves the manifest, lockfile, and selected environment as present, valid, and confined.
- It records `failed` or `blocked` when Pixi is missing, the target is unresolvable, the environment is unknown, confinement fails, or the lockfile is absent.
- It sets `repair_service_request_hint` when repair is needed.
- It records provenance linking the check to the acting Project Operator Session or Operator Agent.

`runtime prepare` does not perform hidden repair, install dependencies, or regenerate lockfiles.

## Repair and Divergence

Any mutating environment work is a Service Request:

- Installing or repairing Topic Workspace dependencies.
- Regenerating `pixi.lock`.
- Adding a new named environment to the Topic Workspace manifest.
- Creating a divergent environment for a specific Agent Workspace.

The Service Request names the target Topic Workspace or Agent Workspace, the task, the expected output, and the completion observation rules. The Service Agent Instance records support Artifacts and Provenance Records.

## Migration from Project-root Environments

Existing Research Topics that used `[[topic_pixi_environment_bindings]]` to Project-root environments may keep those bindings for platform topics. Research topics that use the Topic Workspace root as their Pixi workspace can rely on the implicit default. Topics that need a non-root Pixi target should migrate to `[[topic_standalone_pixi_bindings]]` with `manifest_path_or_dir`. The migration itself is recorded as a Service Request or Project-level change with Provenance Records.

## What This Standard Does Not Cover

- Houmao managed-agent launch material or mailbox configuration.
- GUI rendering of environment status.
- Automatic lockfile updates on dependency changes; those remain Service Request or scheduler-policy concerns.
- Per-agent environment divergence without an explicit Service Request.

## Related Decisions

- ADR 0020: Topic-specific Pixi Environments (superseded by ADR 0027)
- ADR 0022: Milestone 4 Prepares Topic Environment Readiness
- ADR 0023: Global Agent Instance ids and Flat Agent Workspaces
- ADR 0024: Doctor is Read-only
- ADR 0025: Project Manifest Owns Topic Pixi Environment Bindings
- ADR 0026: Standalone Pixi Isolation Uses Separate Manifest Bindings
- ADR 0027: Topic Workspaces Are Default Pixi Workspaces
