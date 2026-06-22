## 1. Runtime Store Foundation

- [x] 1.1 Add Workspace Runtime schema constants, status sets, and runtime dataclasses for schema metadata, path plans, lifecycle refs, Agent Team Instances, Agent Instances, Agent Workspaces, handoff state, validation issues, and lightweight Provenance refs.
- [x] 1.2 Add a SQLite-backed runtime store module that opens `<topic-workspace>/state.sqlite`, creates the initial schema in one transaction, and exposes typed read/write helpers without adding a broad ORM dependency.
- [x] 1.3 Implement runtime schema metadata reads and writes with current-version checks, unsupported older-version diagnostics, unsupported newer-version diagnostics, and idempotent reopen behavior.
- [x] 1.4 Implement explicit Workspace Runtime directory creation for `artifacts/`, `agents/`, `tasks/`, `runs/`, `views/`, and `logs/` under the selected Topic Workspace.
- [x] 1.5 Ensure existing read-only commands never create `state.sqlite` or runtime directories by adding side-effect regression coverage before wiring mutating runtime commands.

## 2. Topic Environment Readiness

- [x] 2.1 Add readiness record dataclasses and store helpers for selected topic Pixi environment use, standalone Pixi isolation refs, readiness status (`ready`, `failed`, `blocked`, `stale`, or `superseded`), readiness diagnostics, checked or prepared timestamp, actor ref when known, and Provenance refs.
- [x] 2.2 Implement `runtime prepare` logic that requires an initialized current-schema Workspace Runtime before writing readiness records.
- [x] 2.3 Validate Project Manifest `topic_pixi_environment_bindings` and `topic_standalone_pixi_bindings` during preparation without inferring topic relationships from Pixi environment names.
- [x] 2.4 Record `ready`, `failed`, and `blocked` readiness outcomes durably without marking launch-facing readiness prepared when checks fail or repair is required.
- [x] 2.5 Keep environment repair explicit by reporting repair needs and directing user-visible setup or compatibility work through Service Requests rather than hiding it inside `runtime prepare`.
- [x] 2.6 Add validation that missing or failed readiness blocks launch-facing operations without blocking unrelated inspection.

## 3. Path Plan Durability

- [x] 3.1 Add a path-plan record API that stores canonical path, semantic surface, resolution source, optional source detail, owning Topic Workspace id, and created timestamp.
- [x] 3.2 Persist Topic Workspace runtime path plans during runtime initialization for `state.sqlite`, `artifacts/`, `agents/`, `tasks/`, `runs/`, `views/`, and `logs/`.
- [x] 3.3 Persist Agent Workspace path plans before creating Agent Workspace directories or Agent Workspace lifecycle records.
- [x] 3.4 Persist Run path plans before creating Run support directories, logs, prompts, tool-call records, outputs, or Artifact records.
- [x] 3.5 Preserve environment override source detail for supported `ISOMER_*` path variables without storing unrelated environment values.
- [x] 3.6 Add validation that reports historical path-plan mismatches and path-plan ownership mismatches without silently rewriting records.

## 4. Runtime Lifecycle Records

- [x] 4.1 Persist initial Research Topic and Topic Workspace refs from the Project Manifest when a Workspace Runtime is initialized.
- [x] 4.2 Add runtime record helpers for Research Inquiries, Research Tasks, Runs, Workflow Stage Cursors, and Topic Agent Team Profile refs with explicit statuses and transition metadata.
- [x] 4.3 Implement Agent Team Instance record creation from a validated Topic Agent Team Profile without creating Houmao launch material.
- [x] 4.4 Create Agent Instance records for active Topic Agent Team Profile role bindings, including Agent Role refs, optional Agent Profile refs, Topic Workspace refs, statuses, and Provenance refs when known.
- [x] 4.5 Create Agent Workspace records from stored path plans and materialize the corresponding Agent Workspace directories only during explicit Agent Team Instance creation.
- [x] 4.6 Add duplicate Agent Team Instance id detection that leaves existing runtime records unchanged.
- [x] 4.7 Add handoff state records with source actor refs, target actor refs, Research Task or Run refs, Agent Team Instance refs, status, Completion Watcher Contract refs, timestamps, and Provenance refs.
- [x] 4.8 Add restart recovery helpers that reopen Workspace Runtime and reconstruct Agent Team Instance summaries with Agent Instance, Agent Workspace, Run, Workflow Stage Cursor, blocker, and handoff refs.

## 5. CLI and API Surface

- [x] 5.1 Add `isomer-cli runtime init` with common Project selectors, topic selectors, text output, deterministic JSON output, idempotent reopen behavior, and schema-version diagnostics.
- [x] 5.2 Add `isomer-cli runtime prepare` with common Project selectors, topic selectors, text output, deterministic JSON output, readiness records, preparation status, and no Houmao launch side effects.
- [x] 5.3 Add `isomer-cli runtime inspect` that reads runtime metadata, selected record counts, runtime path, schema version, and readiness summaries without mutating runtime state.
- [x] 5.4 Add `isomer-cli runtime validate` that runs Workspace Runtime validation and emits deterministic diagnostics without creating directories, changing statuses, or repairing records.
- [x] 5.5 Add `isomer-cli team-instances create` with explicit or generated Agent Team Instance id, selected Topic Agent Team Profile, text output, deterministic JSON output, and no Houmao launch side effects.
- [x] 5.6 Add `isomer-cli team-instances list` scoped to the selected Topic Workspace.
- [x] 5.7 Add `isomer-cli team-instances show <agent-team-instance-id>` with Agent Instance refs, Agent Workspace refs, Run refs when known, Workflow Stage Cursor refs, status, blocker refs, and diagnostics.
- [x] 5.8 Update root help, command-surface documentation, and CLI tests so runtime, runtime prepare, and team-instance commands appear alongside existing commands.

## 6. Runtime Validation

- [x] 6.1 Validate runtime schema-version mismatches before any mutating runtime operation.
- [x] 6.2 Validate broken refs for Research Topics, Research Inquiries, Research Tasks, Runs, Topic Agent Team Profiles, Agent Team Instances, Agent Instances, Agent Workspaces, Artifacts, Gates, Research Claims, Evidence Items, Decision Records, Provenance Records, and readiness records.
- [x] 6.3 Validate missing Agent Workspace directories, missing Artifact files, missing readiness records, and missing path-plan targets while keeping the durable refs visible.
- [x] 6.4 Validate lifecycle transitions for required actor, timestamp, previous status, next status, and rationale fields.
- [x] 6.5 Validate stale handoffs without treating Signal Observations as authoritative completion.
- [x] 6.6 Validate unresolved Gates, supported Research Claims without valid Evidence Items, and stale Provenance Records through Workspace Runtime record lookup.
- [x] 6.7 Validate cross-topic leakage for Topic Workspace refs, Agent Team Instance refs, Agent Workspace refs, Run refs, Artifact refs, readiness records, and path plans.

## 7. Tests and Fixtures

- [x] 7.1 Add unit tests for runtime store initialization, schema metadata, idempotent reopen, unsupported schema diagnostics, and transaction rollback on failed writes.
- [x] 7.2 Add unit tests for readiness record persistence, readiness failures, Service Request repair boundaries, and cross-topic readiness isolation.
- [x] 7.3 Add unit tests for path-plan persistence, environment override source detail, path-plan ownership validation, and historical mismatch reporting.
- [x] 7.4 Add unit tests for Agent Team Instance creation from Topic Agent Team Profiles, Agent Instance records, Agent Workspace records, duplicate id rejection, and absence of Houmao launch fields.
- [x] 7.5 Add CLI tests for `runtime init`, `runtime prepare`, `runtime inspect`, `runtime validate`, `team-instances create`, `team-instances list`, and `team-instances show` in text and JSON modes.
- [x] 7.6 Add side-effect tests proving read-only commands do not create `state.sqlite`, runtime directories, Agent Workspaces, Runs, Artifacts, View Manifests, or Houmao launch material.
- [x] 7.7 Add negative validation tests for broken refs, missing Agent Workspaces, invalid transitions, stale handoffs, unresolved Gates, unsupported Research Claims, stale Provenance Records, missing or failed readiness, schema mismatches, and cross-topic leakage.
- [x] 7.8 Add an integration fixture that creates two Research Topics, specializes `deepsci-org` for both, initializes separate Workspace Runtimes, prepares readiness separately, creates separate Agent Team Instance records, and reopens them after process restart.
- [x] 7.9 Add an isolation integration test proving one topic's readiness records, Agent Team Instance, Agent Workspaces, Runs, Artifacts, and path plans do not appear in another Topic Workspace.

## 8. Documentation and Verification

- [x] 8.1 Document the Workspace Runtime command surface, `runtime prepare`, side-effect boundaries, runtime directory layout, schema-version behavior, readiness behavior, Service Request repair boundary, and no-Houmao-launch boundary in the CLI documentation or README location used for existing commands.
- [x] 8.2 Update developer notes or roadmap-adjacent documentation to explain how Milestone 4 prepares Milestone 5 Houmao Execution Adapter work while keeping Houmao details outside core schema.
- [x] 8.3 Update `ROADMAP.md` Milestone 4 checklist only after implementation and validation are complete.
- [x] 8.4 Run `openspec validate --all`, `pixi run lint`, `pixi run typecheck`, `pixi run test`, and `pixi run validate-research-skills` after implementation.
