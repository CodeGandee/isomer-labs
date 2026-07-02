## ADDED Requirements

### Requirement: Structured Initialization Checkpoint Creation
The system SHALL create topic-scoped structured reset checkpoints that record a selected Topic Workspace's post-initialization/pre-research baseline without using Git operations.

#### Scenario: Checkpoint records initialization boundary
- **WHEN** Topic Creator `finalize` creates a reset checkpoint for a selected initialized Research Topic and Topic Workspace
- **THEN** the system records the Research Topic ref, Topic Workspace ref, actor or operator ref, creation timestamp, Workspace Runtime schema version, source readiness evidence, `topic.workspace.summary` ref when available, `isomer-topic-summary.md` ref when available, semantic path inventory, preserved record ids, runtime high-watermarks, generated view digests when available, and blockers
- **AND** the checkpoint status is `ready`, `blocked`, or `stale`

#### Scenario: Checkpoint requires initialized topic context
- **WHEN** checkpoint creation cannot resolve a Project Manifest-backed Research Topic, Topic Workspace, current Workspace Runtime, and required semantic labels
- **THEN** the system reports deterministic diagnostics and does not create a checkpoint

#### Scenario: Checkpoint excludes Git metadata
- **WHEN** a checkpoint payload is created
- **THEN** it contains no Git stash id, Git branch reset instruction, Git commit creation instruction, Git tag, Git ref, project-root Git tracking instruction, or command that invokes Git

#### Scenario: Checkpoint excludes research-paradigm skill coupling
- **WHEN** Topic Creator `finalize` creates the first reset checkpoint
- **THEN** checkpoint creation depends only on operator-level Topic Workspace readiness evidence
- **AND** it does not inspect, require, name, or route to `skillset/research-paradigm` skills

### Requirement: Reset Checkpoint Structured Profiles
The system SHALL provide artifact format profiles for checkpoint, reset plan, and reset outcome payloads.

#### Scenario: Built-in profiles are resolvable
- **WHEN** artifact-format resolution inspects built-in DeepScientist record profiles
- **THEN** it can resolve `isomer:deepsci/record-format/profile/control/topic-reset-checkpoint/v1`, `isomer:deepsci/record-format/profile/control/topic-reset-plan/v1`, and `isomer:deepsci/record-format/profile/report/topic-reset-outcome/v1`

#### Scenario: Checkpoint payload validation rejects Git fields
- **WHEN** checkpoint, reset plan, or reset outcome payload validation sees Git operation fields or command strings that invoke Git
- **THEN** validation fails with deterministic diagnostics that name the forbidden field or command

#### Scenario: Markdown views are generated review material
- **WHEN** a checkpoint, reset plan, or reset outcome is rendered as Markdown
- **THEN** the generated view summarizes identity, readiness evidence, preserve/delete/regenerate/skip decisions, blockers, and no-Git boundary
- **AND** the structured JSON payload remains the source of truth

### Requirement: Explicit Checkpoint Extension
The system SHALL allow later preparation workflows to explicitly update a reset checkpoint with additional preserved setup evidence without requiring operator skills to know those workflows.

#### Scenario: Later preparation extends checkpoint
- **WHEN** a research-preparation workflow creates setup records, generated views, or support material that should survive Topic Workspace reset
- **THEN** it updates the selected reset checkpoint with its own preserved record ids, structured payload ids, generated view refs, semantic labels, digests when available, actor refs, and provenance refs
- **AND** the checkpoint records the update source without requiring `skillset/operator` guidance to name or understand that workflow

#### Scenario: Unrecorded preparation is resettable
- **WHEN** reset planning sees records, generated views, or support material created after the checkpoint that no checkpoint update preserved
- **THEN** it treats that material as post-checkpoint reset candidate state
- **AND** any workflow-specific preparation represented only by that material must be redone after reset

#### Scenario: Checkpoint update is topic scoped and no-Git
- **WHEN** a workflow updates a checkpoint
- **THEN** the update must belong to the selected Research Topic and Topic Workspace
- **AND** it contains no Git operation metadata or Git command strings

### Requirement: Reset Plan Generation
The system SHALL generate a read-only reset plan from a selected reset checkpoint and current Workspace Runtime state before applying any reset.

#### Scenario: Plan classifies current state
- **WHEN** an operator requests a reset plan for checkpoint `<checkpoint-id>`
- **THEN** the system compares the checkpoint to current lifecycle records, structured payload records, artifact format registrations, generated Markdown views, readiness records, runtime support records, and semantic-label-derived filesystem paths
- **AND** it classifies each planned action as `preserve`, `delete_record`, `delete_file`, `delete_generated_view`, `regenerate`, `skip`, or `blocked`

#### Scenario: Plan preserves setup records
- **WHEN** reset planning sees checkpoint records, Topic Creator readiness summaries, Topic Team specialization summaries, artifact format registrations, and the selected checkpoint's own generated view
- **THEN** the plan marks them as preserve candidates unless they are missing or invalid

#### Scenario: Plan treats unpreserved post-checkpoint research records as reset candidates
- **WHEN** reset planning sees accepted research records, structured payloads, generated views, View Manifests, Run records, Evidence Items, Decision Records, Findings, or Artifacts created after the checkpoint and not listed as preserved setup evidence by the checkpoint or a later checkpoint update
- **THEN** the plan marks them for destructive deletion or regeneration according to their record kind and source kind

#### Scenario: Plan deletes managed actor and agent workspace contents
- **WHEN** reset planning resolves managed `topic.actors.workspace` or `agent.workspace` roots for the selected Topic Workspace
- **THEN** the plan preserves root directories and checkpoint-preserved baseline paths
- **AND** it marks all other post-checkpoint files and directories under those managed roots for destructive deletion

#### Scenario: Plan blocks unsafe surfaces
- **WHEN** reset planning encounters unresolved semantic labels, cross-topic runtime records, unsupported runtime schema versions, unknown managed files, possible secret material, running Agent Team Instances, open handoffs, live adapter records, actor or agent material outside managed workspace roots, or managed-root traversal hazards
- **THEN** the plan records blockers and is not applyable

#### Scenario: Plan is read-only
- **WHEN** reset planning completes
- **THEN** the system has not deleted records, deleted files, regenerated views, changed runtime statuses, or mutated Topic Workspace files

### Requirement: Reset Plan Application
The system SHALL apply only an approved reset plan whose checkpoint, diagnostics, and current Workspace Runtime state still match the plan preconditions.

#### Scenario: Apply requires explicit plan and confirmation
- **WHEN** an operator applies a reset
- **THEN** the command requires a reset plan id, selected checkpoint id, selected Research Topic and Topic Workspace context, and explicit confirmation

#### Scenario: Apply rejects stale plan
- **WHEN** the current Workspace Runtime state, checkpoint digest, semantic path resolution, or blocker set differs from the reset plan preconditions
- **THEN** apply rejects the plan as stale and reports that a new plan must be generated

#### Scenario: Apply deletes unpreserved records and generated views
- **WHEN** an approved reset plan contains unpreserved post-checkpoint runtime rows, structured payloads, generated Markdown views, or managed support files
- **THEN** the system destructively deletes only records and files named by the plan and derived from semantic labels, including named files and directories under managed actor and agent workspace roots
- **AND** it does not retain or preserve those candidates unless the checkpoint lists them as preserved setup evidence

#### Scenario: Apply writes reset outcome
- **WHEN** reset apply finishes, partially applies, or fails
- **THEN** the system writes a topic-scoped reset outcome record that lists applied actions, skipped actions, failed actions, diagnostics, actor ref, checkpoint ref, plan ref, timestamps, and generated Markdown view ref when rendered

#### Scenario: Apply uses no Git operations
- **WHEN** reset apply executes
- **THEN** it does not run Git commands, create Git commits, use Git stash, update Git branches, write Git refs, or depend on project-root Git state

### Requirement: Reset CLI and API Surface
The system SHALL expose deterministic Python APIs and `isomer-cli project topic-reset` commands for checkpoint lifecycle, reset planning, and reset application.

#### Scenario: CLI exposes reset commands
- **WHEN** a user inspects the project CLI
- **THEN** the command surface includes `project topic-reset checkpoint`, `project topic-reset update-checkpoint`, `project topic-reset list`, `project topic-reset show`, `project topic-reset plan`, `project topic-reset show-plan`, and `project topic-reset apply`

#### Scenario: JSON output uses standard wrapper
- **WHEN** a reset command runs with `--print-json`
- **THEN** the response uses the existing `isomer-cli-output.v1` wrapper and includes `ok`, `mutated`, operation name, selected Research Topic ref, selected Topic Workspace ref, checkpoint id when relevant, plan id when relevant, outcome id when relevant, diagnostics, and rendered view paths when available

#### Scenario: Human output names review artifacts
- **WHEN** a reset command runs without `--print-json`
- **THEN** it reports the status, checkpoint or plan id, generated Markdown review path, blockers, and next operator action without printing large payloads by default

### Requirement: Reset Validation
The system SHALL validate reset checkpoint, plan, and outcome records as part of Workspace Runtime validation.

#### Scenario: Missing preserved record is reported
- **WHEN** validation sees a reset checkpoint that preserves a lifecycle record, structured payload, generated view, artifact format registration, readiness record, or summary path that no longer exists
- **THEN** validation reports the missing preserved target and marks the checkpoint stale

#### Scenario: Cross-topic checkpoint is reported
- **WHEN** a reset checkpoint, plan, or outcome references records or paths from another Research Topic or Topic Workspace
- **THEN** validation reports cross-topic leakage and does not allow apply to proceed

#### Scenario: Forbidden Git metadata is reported
- **WHEN** validation sees Git operation metadata in a checkpoint, plan, outcome, or reset structured payload
- **THEN** validation reports it as an error

### Requirement: Operator Reset Guidance
The operator skillset SHALL guide agents to create and consume structured reset checkpoints at the research restart boundary without depending on research-paradigm skill knowledge.

#### Scenario: Topic Creator creates first checkpoint
- **WHEN** `isomer-admin-topic-creator finalize` completes Topic Workspace readiness summary work
- **THEN** it creates or refreshes the first reset checkpoint from operator-level readiness evidence
- **AND** it does not require or mention research-paradigm skill bootstrap records

#### Scenario: Topic Manager owns reset inspection and apply
- **WHEN** `isomer-admin-topic-mgr` describes initialized-topic management commands
- **THEN** it includes reset plan, inspect, and apply guidance as operator-owned initialized-topic operations
- **AND** it states that reset operations use structured records and Workspace Runtime state, not Git

#### Scenario: Operator guidance avoids research-paradigm routing
- **WHEN** operator reset guidance describes checkpoint, plan, inspect, or apply behavior
- **THEN** it does not route to, depend on, or require knowledge of `skillset/research-paradigm` skills
