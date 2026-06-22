## Why

Milestone 4 is the point where Isomer moves from design-time Project and Topic Agent Team Profile validation into durable topic-scoped runtime state. Without a Workspace Runtime, the CLI cannot create, reopen, inspect, or validate multiple `deepsci-org` Agent Team Instance records across Topic Workspaces, and later Houmao launch work would have nowhere canonical to store lifecycle refs, paths, handoffs, or validation issues.

## What Changes

- Add Workspace Runtime creation and reopening for each Topic Workspace, including `state.sqlite`, schema version metadata, migration compatibility checks, and default runtime directories for `artifacts/`, `agents/`, `tasks/`, `runs/`, `views/`, and `logs/`.
- Add durable runtime record APIs and CLI surfaces for Research Topics, Research Inquiries, Research Tasks, Runs, Workflow Stage Cursors, Topic Agent Team Profiles, Agent Team Instances, Agent Instances, Agent Workspaces, resolved path plans, and handoff state.
- Add `isomer-cli runtime prepare` as the explicit mutating readiness command that records selected topic Pixi environment use, readiness status, readiness diagnostics, and preparation provenance in Workspace Runtime before Houmao launch exists.
- Add multi-topic Agent Team Instance instantiation from existing `deepsci-org` Topic Agent Team Profiles without launching Houmao agents or creating adapter-specific launch material.
- Record resolved Workspace Path Resolution outputs before Agent Workspaces, Run logs, Artifacts, View Manifests, or future Houmao launch material depend on those paths.
- Treat the `deepsci-org` loop-local state contract as Houmao Execution Adapter bookkeeping input, not as a replacement for Workspace Runtime state.
- Add runtime validation for broken refs, missing Agent Workspaces, invalid lifecycle transitions, stale handoffs, unresolved Gates, unsupported Research Claims, stale Provenance Records, schema-version mismatches, and cross-topic leakage.
- Add integration tests that create two Research Topics, specialize `deepsci-org` for both, instantiate separate Agent Team Instance records under separate Topic Workspaces, and recover them after process restart.

## Capabilities

### New Capabilities

- `workspace-runtime-persistence`: Defines Workspace Runtime creation, reopening, schema metadata, SQLite-backed record storage, runtime directory layout, CLI/API surfaces, topic environment readiness preparation, multi-topic Agent Team Instance instantiation records, handoff state, and runtime validation.

### Modified Capabilities

- `research-lifecycle-state`: Extends lifecycle requirements for persisted Agent Instance, Agent Workspace, handoff state, and restart-safe Agent Team Instance records.
- `workspace-path-resolution`: Requires resolved path plans to be persisted through Workspace Runtime before runtime records, Agent Workspaces, Runs, Artifacts, View Manifests, or adapter launch material depend on them.
- `research-recording-contracts`: Connects Artifact, Gate, Research Claim, Provenance Record, and validation checks to Workspace Runtime issue reporting and runtime-backed record lookup.
- `isomer-cli-project-discovery`: Adds the Milestone 4 CLI command surface for runtime creation, validation, inspection, and Agent Team Instance record instantiation while preserving side-effect-free design-time commands.

## Impact

- Affects `src/isomer_labs/` models, persistence helpers, Workspace Path Resolution, CLI command groups, validation logic, and JSON/text output contracts.
- Adds SQLite-backed runtime storage under Topic Workspace paths and filesystem directory creation only through explicit runtime creation, runtime preparation, or Agent Team Instance record instantiation commands.
- Adds integration tests under `tests/integration/` plus focused unit tests under `tests/unit/` for runtime records, path-plan durability, readiness preparation, validation diagnostics, restart recovery, and cross-topic isolation.
- May run bounded Pixi readiness preparation through `runtime prepare`; does not launch Houmao, create Houmao mailboxes or gateways, or promote Houmao terms into Isomer core schema.
