# Milestone 4 Workspace Organization and Pixi Readiness

> Update note: ADR 0027 supersedes ADR 0020 and changes the default from Project-root Pixi environments to Topic Workspace Pixi workspaces. The binding authority, read-only `doctor`, separate `runtime prepare`, and Service Request repair rules below remain valid; the default manifest location and environment scope now follow the Topic Workspace Pixi workspace standard.

## Context

Milestone 4 needs enough Workspace Runtime to create, reopen, inspect, and validate multiple Agent Team Instance records across Topic Workspaces before Milestone 5 launches live Houmao-backed agents. The key design pressure is that Isomer must use Pixi as a required environment manager while preserving Isomer's existing workspace language: Project, Topic Workspace, Workspace Runtime, Agent Workspace, Agent Runtime, and Service Request.

## Decisions

- Pixi is a required Project dependency. `isomer-cli doctor` must check for it and inspect Project-level Pixi configuration before launch preflight proceeds.
- Each Topic Workspace is a Pixi workspace by default. It contains its own Pixi manifest and lockfile, installs its own environment under `<topic-workspace>/.pixi/`, and exposes that environment as the shared default Python environment for Agent Workspaces under the topic. The Project Manifest can record explicit Topic Workspace Pixi targets through `[[topic_standalone_pixi_bindings]]`, while the registered Topic Workspace directory is the implicit default target when no explicit entry exists.
- The Project-level Pixi manifest, when present, supplies the Isomer platform environment for tools such as `isomer-cli`. It is not the default execution environment for research agents.
- A Research Topic may still bind to a Project-root Pixi environment through `[[topic_pixi_environment_bindings]]` for platform or shared tooling topics. Topic-to-environment relationships are not inferred from names.
- Project Manifest stores Research Topic to Project-root Pixi environment bindings with `research_topic_id`, `pixi_environment`, optional `purpose`, and optional `status`, and stores explicit Topic Workspace Pixi bindings separately with `research_topic_id`, `manifest_path_or_dir`, optional `pixi_environment`, optional `purpose`, and optional `status`. Research Topic Config does not own Pixi environment bindings. Workspace Runtime stores the resolved environment use, readiness status, and provenance after preparation.
- Milestone 4 prepares and records topic environment readiness before real Houmao launch, but live Houmao launch refs, mailbox refs, gateway refs, managed-agent ids, and handoff traffic remain Milestone 5 concerns.
- Agent Instance ids are globally unique runtime identity. The default `agent.workspace` binding is `<topic-workspace>/agents/<agent-name>/` under `isomer-default.v1`, where `agent_name` is topic-local planning language and the worktree is bound to a per-agent branch namespace.
- `isomer-cli doctor` is read-only. A later preparation command performs Pixi install/readiness work, creates Workspace Runtime readiness records, and records provenance.

## Implications for Milestone 4

- Add a `doctor` command that reports dependency status, Pixi version, Project-level Pixi manifest readiness, `requires-pixi` compatibility when declared, explicit Project Manifest `topic_pixi_environment_bindings` and `topic_standalone_pixi_bindings`, lock/readiness signals, and actionable diagnostics without mutating files.
- Add runtime preparation behavior separately from `doctor`, likely as a Workspace Runtime or Topic Workspace preparation command, so setup writes are explicit and provenance-bearing.
- Add Topic Workspace Runtime schema records for selected Pixi environment use, standalone Pixi isolation refs when used, readiness status, readiness diagnostics, resolved path sources, and preparation provenance.
- Add Agent Team Instance records that can exist before launch in a prepared or pending-launch lifecycle state.
- Validate that Agent Workspace paths, Run paths, Artifacts, View Manifests, and Houmao launch material do not depend on unresolved paths or unprepared environment readiness.
- Validate that topic-specific Pixi environment readiness does not leak across Research Topics.

## Implications for Milestone 5

- The Houmao Execution Adapter can assume the Topic Workspace has a recorded environment strategy and readiness result before launch starts.
- Houmao launch material should reference prepared Isomer records and preserve Houmao-specific launch, mailbox, gateway, and managed-agent details inside adapter records or adapter-backed Artifacts.
- Environment repair that mutates Project, Topic Workspace, dependency, runtime, or environment state should appear as a Service Request with support Artifacts and Provenance Records.

## Related ADRs

- ADR 0020: Topic-specific Pixi Environments (superseded by ADR 0027)
- ADR 0021: Topic Config Owns Environment Intent (superseded by ADR 0025)
- ADR 0022: Milestone 4 Prepares Topic Environment Readiness
- ADR 0023: Topic-local Agent Names and Flat Agent Worktrees
- ADR 0024: Doctor is Read-only
- ADR 0025: Project Manifest Owns Topic Pixi Environment Bindings
- ADR 0026: Standalone Pixi Isolation Uses Separate Manifest Bindings
- ADR 0027: Topic Workspaces Are Default Pixi Workspaces

## Deferred Choices

- Exact command name for the mutating preparation command.
- The minimal readiness record schema and lifecycle values for prepared or pending-launch Agent Team Instance records.

## Known Implementation Drift

- Earlier design-time Topic Agent Team Profile material emitted placeholder-style `agent-workspaces/<profile>/<role>` refs. Current profile and packet material should plan `agent_name`, `agent_branch`, and derived compatibility `agent_workspace_ref` values through semantic label `agent.workspace`; under `isomer-default.v1`, that label binds to `<topic-workspace>/agents/<agent-name>/`.
