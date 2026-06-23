# Workspace Pixi Environment Standard

This design-choice record defined how Isomer Labs Topic Workspaces and Agent Workspaces use Pixi to set up execution environments. It operationalized the accepted ADRs that place binding authority in the Project Manifest, keep `doctor` read-only, separate readiness preparation from launch, and route environment repair through Service Requests.

## Status

superseded by [Topic Workspace Pixi Workspace Standard](design-topic-workspace-pixi-workspace-standard.md)

> ADR 0027 changed the default from Project-root Pixi environments to Topic Workspace Pixi workspaces. Use the superseding document for current guidance.

## Scope

This standard applies to:

- Project-level Pixi manifest authority for Research Topic environments.
- Topic Workspace environment selection and readiness recording.
- Agent Workspace environment inheritance from the parent Topic Workspace.
- CLI commands and Workspace Runtime records that touch Pixi readiness.

It does not change Houmao launch mechanics, adapter payload formats, or GUI Backend environment rendering. Those surfaces consume the readiness records this standard produces.

## Principles

1. **Project-level Pixi manifest is the environment authority.** The Project root holds the canonical Pixi configuration in `pyproject.toml` or `pixi.toml`. Research Topics do not bring their own Pixi manifests unless the Project Manifest explicitly opts them into standalone isolation.
2. **Bindings are explicit and never inferred.** The Project Manifest declares `[[topic_pixi_environment_bindings]]` and `[[topic_standalone_pixi_bindings]]` tables. Isomer never derive a Research Topic's environment from topic names, environment names, or directory conventions.
3. **Topic Workspaces select environments; Agent Workspaces inherit them.** An Agent Workspace uses the Topic Workspace's selected Project-root or standalone Pixi environment by default. Per-agent environment divergence is an explicit operational decision recorded as a Service Request, not a hidden adapter default.
4. **`doctor` is read-only.** Host, Project, and topic Pixi diagnostics report status without installing environments, creating lockfiles, or mutating Workspace Runtime.
5. **Readiness preparation is a distinct mutating step.** `isomer-cli runtime prepare` records a `TopicEnvironmentReadinessRecord` after checking explicit bindings. It does not perform hidden repair or compatibility work.
6. **Repair is a Service Request.** Dependency installation, platform fixes, lockfile regeneration, or environment rebuilds that mutate Project or workspace state are recorded as Service Requests with support Artifacts and Provenance Records.

## Topic Workspace Standard

### Environment selection

A Topic Workspace uses the Pixi environment that the Project Manifest binds to its Research Topic.

- Default form: one active `[[topic_pixi_environment_bindings]]` entry with `research_topic_id` and `pixi_environment`.
- Optional stronger isolation: one active `[[topic_standalone_pixi_bindings]]` entry with `research_topic_id` and Project-root-relative `manifest_path`.
- A Research Topic may have multiple bindings for different purposes, distinguished by `purpose` and `status`. The runtime preparation step records which binding is selected for execution.

### Readiness recording

After Project-level Pixi dependencies are installed, `isomer-cli runtime prepare --topic <topic>` checks only explicit bindings and writes or updates a `TopicEnvironmentReadinessRecord` in Workspace Runtime.

The record stores:

- `status`: `ready`, `failed`, `blocked`, `stale`, or `superseded`.
- `project_pixi_environment_refs`: selected Project-root environment names.
- `standalone_pixi_manifest_refs`: selected standalone manifest paths when used.
- `diagnostics`: structured readiness diagnostics, not full command output.
- `actor_ref`: the actor that performed the preparation check.
- `repair_service_request_hint`: pointer to a Service Request when repair is needed.
- `provenance_refs`: links to the preparation run and any preceding Service Requests.

### Directory and path rules

- The Topic Workspace path is declared in the Project Manifest under `topic_workspaces`.
- Workspace Runtime lives at `<topic-workspace>/state.sqlite`.
- Runtime directories are created by `runtime init`: `artifacts/`, `agents/`, `tasks/`, `runs/`, `views/`, `logs/`.
- The Topic Workspace itself is not a Pixi workspace unless standalone isolation is active.

## Agent Workspace Standard

### Environment inheritance

An Agent Workspace inherits the Topic Workspace's selected Pixi environment by default. The Agent Workspace directory does not contain its own Pixi manifest, `.pixi/` directory, or lockfile.

### Default path

Agent Workspaces live under `<topic-workspace>/agents/<agent-instance-id>/`. This flat layout uses globally unique Agent Instance ids and avoids nesting under Agent Team Instance ids or role names.

### Per-agent divergence

If an Agent Workspace needs a different environment than its Topic Workspace, the Operator Agent or Project Operator Session opens a Service Request. The Service Request records:

- target Agent Workspace or Agent Instance scope;
- reason for divergence, such as incompatible dependency versions or platform constraints;
- expected output, such as a validated local environment or updated binding proposal;
- completion observation rules.

The Service Agent Instance may inspect or modify the authorized Agent Workspace, but it must record support Artifacts and Provenance Records. The divergence is not silently encoded in adapter launch material.

## CLI Workflow

The standard command sequence for preparing a Topic Workspace and its Agent Workspaces is:

```bash
# 1. Install Project-level Pixi dependencies once at the Project root.
pixi install

# 2. Read-only validation and diagnostics.
pixi run isomer-cli --print-json validate
pixi run isomer-cli --print-json doctor --topic <topic>

# 3. Initialize Workspace Runtime and runtime directories.
pixi run isomer-cli --print-json runtime init --topic <topic>

# 4. Record topic environment readiness.
pixi run isomer-cli --print-json runtime prepare --topic <topic>

# 5. Validate readiness before launch-facing work.
pixi run isomer-cli --print-json runtime validate --topic <topic> --require-ready-readiness

# 6. Create Agent Team Instance records and Agent Workspace directories.
pixi run isomer-cli --print-json team-instances create \
  --topic <topic> \
  --id <ati-id>
```

Agent Workspaces created by `team-instances create` are expected to run inside the Topic Workspace's prepared environment. No additional per-agent Pixi setup command is required by default.

## Project Manifest Examples

### Project-root environment binding

```toml
[[topic_pixi_environment_bindings]]
research_topic_id = "flash-attention-gb10"
pixi_environment = "default"
purpose = "default-run"
status = "active"

[[topic_pixi_environment_bindings]]
research_topic_id = "flash-attention-gb10"
pixi_environment = "flash-attention-gb10-cuda"
purpose = "cuda-measurement"
status = "active"
```

### Standalone isolation binding

```toml
[[topic_standalone_pixi_bindings]]
research_topic_id = "legacy-torch"
manifest_path = "topic-workspaces/legacy-torch/pixi.toml"
pixi_environment = "default"
purpose = "isolated-legacy-deps"
status = "active"
```

## Readiness Diagnostics and Repair

- `doctor` reports missing bindings, unknown environments, missing standalone manifests, or `requires-pixi` mismatches as `fail` diagnostics. It does not install or repair.
- `runtime prepare` checks the same explicit bindings and records readiness. If a binding is invalid or the environment cannot be resolved, it records `failed` or `blocked` and may set a `repair_service_request_hint`.
- `runtime validate --require-ready-readiness` treats missing or non-`ready` readiness as a launch-facing error.
- Environment repair, lockfile regeneration, or dependency installation is dispatched as a Service Request. The Service Agent Instance records support Artifacts and Provenance Records; `runtime prepare` is rerun only after the Service Request resolves the underlying issue.

## What This Standard Does Not Cover

- Houmao managed-agent launch payloads or mailbox configuration.
- GUI rendering of environment status.
- Automatic environment rebuilds on dependency changes; those remain Service Request or scheduler-policy concerns.
- Research Topic Config environment intent fields, which are not used for binding authority.

## Related Decisions

- ADR 0020: Topic-specific Pixi Environments
- ADR 0022: Milestone 4 Prepares Topic Environment Readiness
- ADR 0023: Global Agent Instance ids and Flat Agent Workspaces
- ADR 0024: Doctor is Read-only
- ADR 0025: Project Manifest Owns Topic Pixi Environment Bindings
- ADR 0026: Standalone Pixi Isolation Uses Separate Manifest Bindings
