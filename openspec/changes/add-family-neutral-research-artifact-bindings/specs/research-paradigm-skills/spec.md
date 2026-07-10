## ADDED Requirements

### Requirement: Production Kaoju Skills Use Artifact Binding Authority
Production Kaoju skills SHALL route accepted durable outputs through registered semantic ids and their local artifact binding authority.

#### Scenario: Stage writes a bound artifact
- **WHEN** a Kaoju stage accepts a durable output
- **THEN** it reads the semantic definition from `isomer-kaoju-shared` and the actual record contract from its `artifact-bindings.md`
- **AND** it validates and records the canonical JSON payload with the exact semantic id, record kind, label, profile, producer, consumer, lineage, and actor metadata required by the binding

#### Scenario: Binding is unavailable
- **WHEN** the stage's semantic id, profile, semantic label, or recording command cannot be resolved
- **THEN** the stage returns an explicit storage blocker and does not fall back to an invented path, direct Markdown state, a DeepSci profile, or an untracked JSON file

### Requirement: Kaoju Shared Defines Durable Record Discipline
`isomer-kaoju-shared` SHALL teach the common latest-context, worker-output, canonical payload, lineage, revision, view, and material-boundary rules used by every bound stage.

#### Scenario: Durable work starts from current context
- **WHEN** a Kaoju skill will write, refresh, revise, audit, compare, synthesize, or manage accepted durable records
- **THEN** it resolves current Effective Topic Context, fresh Workspace Runtime state, applicable semantic ids, latest candidate records, duplicates, and supersession or conflict posture before trusting prompt memory or prior prose

#### Scenario: Worker file and durable record remain distinct
- **WHEN** a Kaoju skill produces operation-local notes, payload staging, tables, logs, or exports
- **THEN** it applies the worker output policy and treats those files as pre-promotion or derived material
- **AND** accepted machine-readable state remains the managed payload-file record named by the binding

### Requirement: Kaoju Workspace Manager Owns Binding Bootstrap
`isomer-kaoju-workspace-mgr` SHALL prepare and validate the Kaoju semantic-to-binding contract before ordinary production survey work.

#### Scenario: Selected skills become ready
- **WHEN** a Research Topic and selected Kaoju skill set have base Topic Workspace readiness
- **THEN** the workspace manager validates record labels, provider profiles, semantic registry, binding pages, binding index, dataset-manifest state, query filters, actor posture, worker output policy, and reset treatment
- **AND** it records readiness through bound Kaoju records before handing control to the selected stage

#### Scenario: Bootstrap preserves selected setup state
- **WHEN** the binding index, readiness record, registered custom support, or user-selected survey state should survive reset
- **THEN** the workspace manager updates the selected Topic Workspace reset checkpoint with exact durable refs
- **AND** it reports unpreserved state as subject to the accepted reset plan

### Requirement: Kaoju Managers Use Exact Bound Operations
The Kaoju pipeline's grouped management helpers SHALL use exact binding and query operations rather than unspecified recording interfaces.

#### Scenario: Manage survey dispatches bound reads
- **WHEN** a user selects `manage-survey list`, `show`, `status`, or `export`
- **THEN** the helper follows its documented family, semantic-id, record-id, latest, lineage, render, and export operations
- **AND** it does not mutate canonical content during read or export actions

#### Scenario: Manage dataset revises manifest through owner route
- **WHEN** a user selects dataset `register`, `refresh`, or `remove`
- **THEN** the Topic Workspace owner performs material or link mutation and the Kaoju helper revises the bound Topic Dataset Manifest with returned refs and provenance
- **AND** read-only `list` and `show` actions query the canonical manifest record

### Requirement: DeepSci Research Skill Behavior Remains Compatible
Adding Kaoju bindings and family-neutral format support SHALL preserve current production DeepSci skill, placeholder, provider, and validation behavior.

#### Scenario: DeepSci binding suite is unchanged in meaning
- **WHEN** research-paradigm validation runs after Kaoju binding support is added
- **THEN** every existing DeepSci inventory, placeholder coverage, payload-first command, display field, latest-context, lineage, query metadata, and profile-ref test retains its accepted behavior and diagnostics

