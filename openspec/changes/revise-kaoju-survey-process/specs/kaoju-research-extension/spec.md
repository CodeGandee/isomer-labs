## MODIFIED Requirements

### Requirement: Production Kaoju Skill Family
The package SHALL provide a self-contained production Kaoju research-paradigm skill family under `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/` using the `isomer-kaoju-<purpose>` namespace.

#### Scenario: Exact production inventory exists
- **WHEN** the packaged Kaoju root is inspected
- **THEN** it contains `isomer-kaoju-pipeline`, `isomer-kaoju-shared`, `isomer-kaoju-workspace-mgr`, `isomer-kaoju-frame`, `isomer-kaoju-discover`, `isomer-kaoju-acquire`, `isomer-kaoju-examine`, `isomer-kaoju-reproduce`, `isomer-kaoju-trial`, `isomer-kaoju-compare`, `isomer-kaoju-audit`, `isomer-kaoju-synthesize`, `isomer-kaoju-write`, and `isomer-kaoju-export`
- **AND** no retired, version-suffixed, generic `isomer-ext-*`, or duplicate survey-facade Kaoju skill is active

#### Scenario: Skill identity is consistent
- **WHEN** a production Kaoju skill is inspected
- **THEN** its folder name, `SKILL.md` frontmatter name, `agents/openai.yaml` display name, and default-prompt invocation use the same `isomer-kaoju-*` name
- **AND** its active instructions and directly linked resources are self-contained within the skill directory

#### Scenario: Trial and reproduction remain distinct
- **WHEN** the production inventory is inspected for executable evidence work
- **THEN** `isomer-kaoju-trial` owns bounded method trials and generated-data capability probes while `isomer-kaoju-reproduce` owns only work that satisfies the stronger reproduction contract
- **AND** neither skill treats a repaired or capability-probe result as faithful paper reproduction

### Requirement: Kaoju Pipeline Command Surface
`isomer-kaoju-pipeline` SHALL use the complex-procedure shape as the single extension entry skill, with separate helper, survey-intent, legacy-procedure, and miscellaneous command groups.

#### Scenario: Survey-process commands match the ten use cases
- **WHEN** the pipeline command inventory is inspected
- **THEN** it exposes `choose-directions`, `build-reading-list`, `ingest-reading-item`, `draft-paper`, `manage-paper-template`, `build-paper-pdf`, `export-survey-wiki`, `ingest-source-code`, `prepare-code-run`, and `run-code-trial`
- **AND** each command links to one local command page containing its bounded stage recipe, owners, decisions, durable outputs, terminal states, and resume inputs

#### Scenario: Existing procedures remain callable
- **WHEN** the pipeline compatibility inventory is inspected
- **THEN** it retains `landscape-pass`, `curated-intake-pass`, `direction-expansion-pass`, `theory-comparison-pass`, `method-trial-pass`, `comparative-pass`, `audit-survey-pass`, `paper-pass`, and `create-paper-template`
- **AND** compatibility pages state how each procedure maps to current capability owners and canonical artifacts

#### Scenario: CRUD actions are grouped by object
- **WHEN** helper commands are inspected
- **THEN** `manage-survey` groups `list`, `show`, `status`, and `export`
- **AND** `manage-dataset` groups `register`, `list`, `show`, `refresh`, and `remove`
- **AND** `manage-paper-template` groups template `export`, `apply`, `inspect`, and `status` actions rather than exposing unrelated generic CRUD verbs

#### Scenario: Interaction and resume stay out of the procedure list
- **WHEN** a user requests clarification before work or resumes accepted prior state
- **THEN** clarification-first is represented as an interaction mode shared by procedures
- **AND** resume is represented by a Research Task, Run checkpoint, accepted input refs, and starting stage rather than a separate procedure

#### Scenario: Generic maintenance procedures are absent
- **WHEN** the pipeline public procedure list is inspected
- **THEN** it does not include standalone source-audit, repository-refresh, generic environment-repair, full-Kaoju, resume, or list-passes procedures
- **AND** `prepare-code-run` remains a specific UC-09 survey intent rather than a generic environment administration command

### Requirement: Paper Method Trial
The `method-trial-pass` compatibility procedure and `run-code-trial` survey intent SHALL support an intended-data trial route and an explicitly generated-data capability-probe route while keeping environment preparation separate.

#### Scenario: Trial requires prepared source and environment
- **WHEN** a user asks to run one paper method
- **THEN** Kaoju resolves the acquired source commit and accepted UC-09 environment and smoke result before planning execution
- **AND** missing prerequisites route to source acquisition or `prepare-code-run` without executing in an ambient environment

#### Scenario: Intended-data route preserves faithful and repaired evidence
- **WHEN** the user selects intended data and approves the trial plan
- **THEN** Kaoju pins the paper, code, data, model, evaluator, environment, wrapper, and execution contract before the claim-bearing Run
- **AND** an authorized repaired Run and patch remain separate from the upstream-faithful attempt and verdict

#### Scenario: Generated-data route is a capability probe
- **WHEN** the user requests generated data because the intended dataset is too large, restricted, costly, unavailable, or unnecessary for initial understanding
- **THEN** Kaoju records a Generated Dataset Artifact with generator, schema, size, seeds, assumptions, checks, and limitations
- **AND** resulting numbers are labeled `capability-probe` at no stronger than `executed` depth
- **AND** they are not presented as paper reproduction or benchmark evidence

#### Scenario: Trial waits for approval
- **WHEN** `kaoju:method-trial-plan` is ready
- **THEN** execution waits for the applicable human Gate decision
- **AND** plan revisions and rejected decisions remain durable

### Requirement: Kaoju Uses Existing Platform Owners
Kaoju skills SHALL use existing Isomer owner skills, Service Requests, and extension points for topology, environment, provider, execution, Gate, path, and recording behavior.

#### Scenario: Governed mutation routes to owner
- **WHEN** a Kaoju procedure needs repository acquisition or registration, Topic Workspace mutation, environment preparation, managed dataset links, credentials, private data, large downloads, document builds, viewer launch, or accelerator execution
- **THEN** it routes the operation to the applicable project, workspace, service, provider-binding, execution-adapter, or Gate owner
- **AND** it records and consumes returned durable refs rather than bypassing the owner

#### Scenario: Environment preparation uses a Service Request
- **WHEN** UC-09 needs to inspect or mutate Pixi environment state
- **THEN** the Project Operator Session or Operator Agent opens a Service Request for the Service Team and relates it to the active Research Task and Run
- **AND** the Kaoju skill does not represent itself as the environment owner

#### Scenario: Generic maintenance is not promoted to a survey procedure
- **WHEN** repository refresh, generic environment repair, claim tracing, or resume is needed only as an implementation step
- **THEN** Kaoju performs or routes that step inside the active survey procedure
- **AND** it does not create a new top-level survey procedure for the generic task

#### Scenario: Direct user intent remains public
- **WHEN** the actor explicitly requests source-code ingestion, code-run preparation, or a source-code trial as defined by UC-08, UC-09, or UC-10
- **THEN** the pipeline exposes the corresponding bounded intent while routing owned mutations to platform owners
- **AND** the public intent does not make the capability skill the owner of repository, environment, or execution infrastructure

## ADDED Requirements

### Requirement: Survey-Process Procedures Use Durable Stage Checkpoints
Each new survey-process procedure SHALL create or resume a bounded Run and checkpoint every accepted durable stage.

#### Scenario: Procedure begins
- **WHEN** a new survey-process intent starts
- **THEN** the pipeline records its Research Task and Run refs, procedure id, actor and control mode, normalized inputs, expected output semantics, initial stage, and applicable Gate policies

#### Scenario: Procedure pauses or completes
- **WHEN** a stage reaches a human decision, blocker, Service Request, or terminal result
- **THEN** the pipeline records completed output refs, pending refs, status, and resume hint through Workspace Runtime
- **AND** it reports `complete`, `paused`, or `blocked` without autonomously selecting another macro procedure

### Requirement: Pipeline Skills Query Durable Inputs Through the State DB
All production Kaoju procedures SHALL discover accepted durable inputs through deterministic state-DB queries.

#### Scenario: Procedure resolves prior work
- **WHEN** a stage needs a direction set, reading list, source digest, artifact library, audit, synthesis, paper, wiki, repository, environment, or trial record
- **THEN** it queries by semantic id, scope key, status, stable ref, and lineage as applicable
- **AND** it does not scan the Topic Workspace directory tree or trust conversation memory as canonical state
