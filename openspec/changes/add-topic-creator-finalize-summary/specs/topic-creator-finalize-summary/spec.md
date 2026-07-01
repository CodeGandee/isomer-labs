## ADDED Requirements

### Requirement: Topic Creator Finalize Subcommand
The Topic Creator skill SHALL expose `finalize` as the terminal workspace-preparation subcommand for validating Topic Workspace readiness, writing a durable readiness summary, and printing final readiness status.

#### Scenario: Help lists finalize and omits stale handoff command
- **WHEN** `isomer-admin-topic-creator help` runs or the skill is invoked without a prompt
- **THEN** the command list includes `finalize`
- **AND** the command list includes `step-by-step`
- **AND** the command list includes `run-to`
- **AND** the command list does not include `start-manual-research`
- **AND** the help text describes `finalize` as the terminal Topic Workspace preparation validation and reporting step

#### Scenario: Fast-forward ends at finalize
- **WHEN** Topic Creator `fast-forward` runs for a new or partial topic
- **THEN** it runs the required setup ladder through research bootstrap and then runs `finalize`
- **AND** it treats the summary written by `finalize` as the terminal output of Topic Creator
- **AND** it does not run a `start-manual-research` stage after `finalize`

#### Scenario: Finalize validates required preparation ladder
- **WHEN** `finalize` runs for a selected Topic Workspace
- **THEN** it validates Project readiness, Research Topic registration, Topic Workspace registration, Workspace Runtime initialization, `topic.intent.overview`, topic environment readiness evidence, ready `topic.repos.main`, v2 research bootstrap outputs, and materialized placeholder-binding entrypoints
- **AND** it reports missing or invalid required signals as blockers rather than treating the workspace as ready

#### Scenario: Finalize writes summary through semantic label
- **WHEN** `finalize` can resolve `topic.workspace.summary` for the selected Topic Workspace
- **THEN** it writes or updates the resolved summary file
- **AND** the built-in default path is `<topic-workspace>/isomer-topic-workspace-summary.md`
- **AND** the output reports the semantic label, resolved path, source, and storage profile used for the write

#### Scenario: Finalize prints compact readiness report
- **WHEN** `finalize` completes validation with a resolvable summary path
- **THEN** it prints a compact final report organized into `ready`, `verified`, and `blocked` status groups
- **AND** the printed report names the written summary path
- **AND** the printed report does not include next-step routing, research-stage recommendations, start-pack instructions, or v2 skill recommendations

#### Scenario: Finalize writes blocked status when setup is incomplete
- **WHEN** `finalize` can resolve the selected Topic Workspace and `topic.workspace.summary` but one or more required readiness signals are missing
- **THEN** it writes the summary with blocked status and the exact missing signals
- **AND** it does not claim that the Topic Workspace is fully available

### Requirement: Topic Workspace Readiness Summary Content
The Topic Creator readiness summary SHALL record enough durable context for a user or later operator agent to inspect what was prepared, what was verified, what was skipped, and what is blocked without relying on chat history.

#### Scenario: Summary records identity and readiness classes
- **WHEN** `finalize` writes `topic.workspace.summary`
- **THEN** the summary includes Topic Workspace identity, Project identity when available, Research Topic ref, resolved Topic Workspace path, generated-at timestamp, overall status, `ready`, `verified`, `blocked`, and `skipped` sections
- **AND** `ready` lists usable workspace surfaces, `verified` lists checks and evidence, `blocked` lists missing or failed required signals, and `skipped` lists optional work that was intentionally not required

#### Scenario: Summary records materialized surfaces and evidence
- **WHEN** `finalize` writes `topic.workspace.summary`
- **THEN** the summary includes installed or materialized workspace surfaces, semantic path labels and resolved paths, delegated owner evidence, command evidence when available, and environment-readiness evidence
- **AND** it distinguishes durable Topic Workspace records from editable files, repositories, and actor workspace content

#### Scenario: Actor readiness is required when actors are in scope
- **WHEN** actor setup was requested or the default `operator` Topic Actor was not explicitly opted out
- **THEN** `finalize` requires actor definitions, selected Topic Actor bindings, selected Topic Actor Workspace readiness, derived actor env gates, and actor cwd verification evidence
- **AND** missing actor signals appear as blockers with the affected actor name and semantic label or artifact

#### Scenario: Actor readiness is skipped when explicitly out of scope
- **WHEN** no actors were requested and the default `operator` Topic Actor was explicitly opted out
- **THEN** `finalize` records actor readiness under `skipped` with the opt-out reason
- **AND** the missing actor workspace evidence does not block Topic Workspace readiness

#### Scenario: Status and repair detect stale summaries
- **WHEN** Topic Creator `status` or `repair` finds that predecessor setup evidence changed after `topic.workspace.summary` was written
- **THEN** it reports the summary as stale
- **AND** it does not treat the stale summary as current readiness evidence until `finalize` refreshes it

### Requirement: Topic Creator No-Next-Routing Boundary
The Topic Creator finalization path SHALL report workspace preparation state without recommending or launching the next research action.

#### Scenario: Terminal output reports state only
- **WHEN** `finalize` succeeds, partially succeeds, or blocks
- **THEN** the terminal output reports ready surfaces, verified checks, blockers, skipped optional work, and the summary file path
- **AND** it does not route the user to scout, baseline, idea, write, `start-manual-research`, Houmao launch, or another research or team specialization command

#### Scenario: Summary omits next-action section
- **WHEN** `topic.workspace.summary` is written by Topic Creator `finalize`
- **THEN** the summary does not contain a required `next actions` section
- **AND** any blocker text names the blocked condition without prescribing the next command to run

#### Scenario: Validator rejects stale Topic Creator handoff guidance
- **WHEN** operator skill validation scans `isomer-admin-topic-creator`
- **THEN** it fails if the active Topic Creator command surface includes `start-manual-research`
- **AND** it fails if Topic Creator final output claims to create manual start packs, recommends a next v2 research skill, or routes to a manual research start command
