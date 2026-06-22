## Context

Milestones 1 through 3 established Project discovery, Effective Topic Context resolution, Workspace Path Resolution previews, `doctor`, Domain Agent Team Template validation, and design-time Topic Agent Team Profile specialization. Those commands intentionally avoid Workspace Runtime creation and launch state. Milestone 4 needs the first durable topic-scoped runtime layer so a Project can persist multiple `deepsci-org` Agent Team Instance records, reopen them after process restart, and validate that one Topic Workspace's runtime records do not leak into another Topic Workspace.

The current implementation is a compact Python package with dataclass models in `models.py`, path preview behavior in `paths.py`, validation in `validation.py` and profile modules, and Click command handlers in `cli.py`. The design should extend that style without adding a service process, a broad ORM dependency, or Houmao launch behavior.

## Goals / Non-Goals

**Goals:**

- Create and reopen a Workspace Runtime in each selected Topic Workspace, including `state.sqlite`, runtime schema metadata, and the default runtime directories named in the roadmap.
- Persist enough Research Lifecycle State to represent Research Topics, Research Inquiries, Research Tasks, Runs, Workflow Stage Cursors, Topic Agent Team Profile refs, Agent Team Instances, Agent Instances, Agent Workspaces, and handoff state.
- Prepare and record selected topic Pixi environment readiness through explicit `runtime prepare` commands before Milestone 5 Houmao launch work depends on it.
- Persist resolved path plans before runtime records depend on Agent Workspace paths, Run paths, Artifact paths, View Manifest paths, log paths, or later Houmao launch material.
- Add CLI and Python APIs for explicit runtime initialization, validation, inspection, and Agent Team Instance record creation.
- Validate broken refs, missing Agent Workspaces, invalid lifecycle transitions, stale handoffs, unresolved Gates, unsupported Research Claims, stale Provenance Records, schema-version mismatches, and cross-topic leakage.
- Prove restart recovery and topic isolation with integration tests that instantiate two `deepsci-org` Topic Agent Team Profiles under separate Topic Workspaces.

**Non-Goals:**

- Do not launch Houmao agents, create Houmao mailboxes or gateways, or materialize adapter launch dossiers.
- Do not turn Houmao-specific terms into Isomer core schema fields.
- Do not implement the Milestone 8 full recording APIs for all Artifact, Evidence Item, Finding, Research Claim, Decision Record, Gate, and Provenance write paths beyond the validation and lookup hooks needed by Milestone 4.
- Do not change `doctor`, `paths preview`, or profile specialization into runtime-creating commands.
- Do not introduce a GUI Backend, GUI Runtime State, or View Manifest renderer.

## Decisions

1. Store Workspace Runtime in SQLite at `<topic-workspace>/state.sqlite`.

Rationale: Milestone 4 needs restart-safe lookup, ref validation, and multi-record joins. SQLite gives deterministic local persistence without running a service or adding a large dependency. Rich content stays file-backed through Artifacts; SQLite stores ids, refs, statuses, timestamps, path plans, and validation metadata.

Alternatives considered: TOML or JSON files per record would be easier to inspect manually but would make ref validation, restart recovery, and migration checks more fragile. A server database is too heavy for a Project-local Topic Workspace.

2. Add a small runtime layer rather than expanding existing modules indiscriminately.

Rationale: New runtime concepts are large enough to deserve their own implementation boundary. Add `runtime_models.py` for dataclasses and status constants, `runtime_store.py` for SQLite schema and transactions, and `runtime_validation.py` for graph checks. Keep Click wiring in `cli.py` unless the file becomes unwieldy, then extract runtime command helpers into `runtime_cli.py`.

Alternatives considered: Adding every model to `models.py` keeps imports simple but would make the current design-time model file too broad. Using an ORM would add migration and dependency overhead before the data model settles.

3. Make runtime creation and readiness preparation explicit.

Rationale: Earlier commands rely on read-only or side-effect-light behavior. `isomer-cli runtime init`, `isomer-cli runtime prepare`, `isomer-cli runtime validate`, `isomer-cli runtime inspect`, and `isomer-cli team-instances create/list/show` should be the only new commands that create or mutate Workspace Runtime state. Existing `doctor`, `paths preview`, `context show`, `team-templates`, and profile validation commands stay non-mutating. `runtime prepare` is the narrow mutating readiness command for selected topic Pixi environment use, readiness diagnostics, and preparation provenance.

Alternatives considered: Auto-creating runtime state when a topic command sees a missing `state.sqlite` would reduce setup steps, but it would violate existing read-only guarantees and make tests less deterministic. Naming the command `workspaces prepare` would make the user-facing scope visible, but it would blur Project Manifest workspace discovery with Workspace Runtime mutation. Naming it `team-instances prepare` would place environment readiness too close to launch and too late for Topic Workspace-level preflight.

4. Persist path plans before dependent runtime records.

Rationale: Workspace Path Resolution already computes path surfaces and sources. Milestone 4 should turn selected paths into runtime path-plan records before creating Agent Workspace, Run, Artifact, View Manifest, or log records. Dependent records reference path-plan ids or stable path surfaces instead of re-resolving paths later.

Alternatives considered: Recomputing paths on each read would keep the database smaller, but it would lose the source metadata needed for audit and could change historical records after Project Manifest or environment changes.

5. Instantiate Agent Team Instance records from Topic Agent Team Profiles without launch.

Rationale: Milestone 4 prepares the canonical Isomer runtime state that Milestone 5 will map onto Houmao. `team-instances create` should load a validated Topic Agent Team Profile, create one Agent Team Instance record, create Agent Instance and Agent Workspace records for active role bindings, create initial Workflow Stage Cursor and handoff-state containers when needed, and record Provenance Records for the instantiation action. It must not create Houmao launch material.

Alternatives considered: Waiting until the Houmao Execution Adapter exists would blur Milestones 4 and 5 and leave no canonical state for adapter launch preparation. Creating only the Agent Team Instance without Agent Instance or Agent Workspace records would not test multi-agent topic isolation.

6. Record environment readiness before Houmao launch.

Rationale: Accepted project decisions require Milestone 4 to prepare topic environment readiness before Milestone 5 starts real Houmao launch. `runtime prepare` should read explicit Project Manifest topic Pixi bindings, verify or prepare the selected readiness surface, and store selected environment use, readiness status, readiness diagnostics, and preparation provenance in Workspace Runtime. User-visible environment repair that goes beyond bounded preparation remains Service Request work.

Alternatives considered: Deferring all readiness preparation to Milestone 5 would contradict the accepted readiness decision and make the Houmao Execution Adapter responsible for setup concerns. Recording readiness intent without preparation would reduce side effects, but it would leave launch preconditions ambiguous.

Readiness records use final-state statuses only in Milestone 4: `ready`, `failed`, `blocked`, `stale`, and `superseded`. Missing readiness is represented by no readiness record. If later preparation needs async tracking, a future change can add an explicit preparation operation record instead of overloading readiness status.

7. Treat the `deepsci-org` loop-local state contract as adapter input only.

Rationale: The roadmap explicitly keeps Houmao and generated loop-local state inside the Execution Adapter boundary. Runtime validation may read the loop-local contract to ensure later adapter bookkeeping can map to Isomer records, but canonical state remains Workspace Runtime records.

Alternatives considered: Importing loop-local state into core tables now would couple Isomer to one generated team package and make later adapter changes harder.

8. Return deterministic versioned JSON for all new commands.

Rationale: Existing CLI output uses `isomer-cli-output.v1` and deterministic JSON for tests and future Operator Agent consumption. New commands should reuse the wrapper and include `ok`, selected Project and Topic Workspace refs, runtime schema version, command result objects, and diagnostics.

Alternatives considered: Text-only runtime commands would be faster to implement but would not support robust integration tests or future Operator Agent workflows.

## Risks / Trade-offs

- Schema churn can make early runtime files stale. Mitigation: store `runtime_schema_version`, fail read/write on unsupported versions, and implement explicit migration checks before allowing mutation.
- Runtime validation may grow large quickly. Mitigation: split validation by graph area and keep diagnostics stable, with codes and Isomer concept names.
- Cross-topic leakage can hide in path strings or profile refs. Mitigation: validate every runtime record against the selected Research Topic, Topic Workspace, Project Manifest registration, and stored path-plan ownership.
- SQLite improves querying but is less transparent than plain files. Mitigation: keep rich content file-backed and provide `runtime inspect` JSON/text output for the indexed records.
- Runtime preparation can become an implicit environment repair tool. Mitigation: keep `runtime prepare` bounded to readiness recording and explicit preparation checks; route repair or compatibility work that changes project, dependency, runtime, or environment state through Service Requests with Artifacts and Provenance Records.
- Creating Agent Workspace directories during instantiation is a side effect. Mitigation: limit it to explicit `team-instances create`, record the created paths, and keep preview/validation commands read-only.
- Deepsci-specific fixture work could overfit the runtime. Mitigation: keep core tables generic and use `deepsci-org` only as the first Domain Agent Team Template fixture.

## Migration Plan

Existing Projects and Topic Workspaces remain valid without `state.sqlite` until a runtime command needs Workspace Runtime. `runtime init` creates the database and default directories for a selected Topic Workspace, stores schema metadata, and records initial Project, Research Topic, and Topic Workspace refs from the Project Manifest. If an existing `state.sqlite` has the current schema version, `runtime init` reopens it and reports it as already initialized. If the version is older or newer than supported, mutating commands fail with a schema-version diagnostic and `runtime validate` reports the mismatch.

`runtime prepare` requires a current Workspace Runtime. It records topic Pixi environment readiness only after Project Manifest bindings and Project-level Pixi configuration have passed validation. If preparation cannot complete, the command records diagnostics and leaves launch-facing readiness as `failed` or `blocked` rather than fabricating a prepared state.

Rollback is local: because Milestone 4 does not edit Project Manifest registrations by default, removing a bad Topic Workspace runtime directory or `state.sqlite` restores the pre-runtime Project state. Tests should exercise this by creating runtime state only under temporary fixture Projects.

## Open Questions

- The exact table names can be chosen during implementation, but the public JSON keys should follow the canonical domain identifiers from the project language file.
- The first implementation can keep migration support as version checking plus clear diagnostics; real data migrations can be added when a second runtime schema version exists.
