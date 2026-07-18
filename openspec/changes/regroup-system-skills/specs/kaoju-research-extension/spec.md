## MODIFIED Requirements

### Requirement: Production Kaoju Skill Family
The package SHALL provide Kaoju as public pack `isomer-ext-kaoju-entrypoint` with thirteen self-contained protected `isomer-kaoju-*` logical capabilities.

#### Scenario: Exact production inventory exists
- **WHEN** the packaged Kaoju root is inspected
- **THEN** it contains public directory `isomer-ext-kaoju-entrypoint`
- **AND** that pack contains protected bundles for `isomer-kaoju-shared`, `isomer-kaoju-workspace-mgr`, `isomer-kaoju-frame`, `isomer-kaoju-discover`, `isomer-kaoju-acquire`, `isomer-kaoju-examine`, `isomer-kaoju-reproduce`, `isomer-kaoju-trial`, `isomer-kaoju-compare`, `isomer-kaoju-audit`, `isomer-kaoju-synthesize`, `isomer-kaoju-write`, and `isomer-kaoju-export`
- **AND** no `isomer-kaoju-pipeline` skill folder or duplicate facade is active

#### Scenario: Public identity is consistent
- **WHEN** the Kaoju public pack is inspected
- **THEN** its folder, frontmatter, metadata, and public default prompt use `isomer-ext-kaoju-entrypoint`

#### Scenario: Protected identity is consistent
- **WHEN** a protected Kaoju bundle is inspected
- **THEN** its folder and frontmatter retain its `isomer-kaoju-*` logical id
- **AND** its active resources remain self-contained

#### Scenario: Trial and reproduction remain distinct
- **WHEN** executable evidence members are inspected
- **THEN** `trial` maps to `isomer-kaoju-trial` and `reproduce` maps to `isomer-kaoju-reproduce`
- **AND** neither capability weakens the accepted evidence distinction

#### Scenario: Artifact identity is consistent
- **WHEN** a protected Kaoju member names a durable extension artifact
- **THEN** it continues to use the exact registered `KAOJU:WHAT` identifier

### Requirement: Kaoju Pipeline Command Surface
`isomer-ext-kaoju-entrypoint` SHALL be the single public Kaoju entrypoint and SHALL retain the accepted complex-procedure public command surface.

#### Scenario: Survey-process commands match ten use cases
- **WHEN** public help is inspected
- **THEN** it exposes `choose-directions`, `build-reading-list`, `ingest-reading-item`, `draft-paper`, `manage-paper-template`, `build-paper-pdf`, `export-survey-wiki`, `ingest-source-code`, `prepare-code-run`, and `run-code-trial`
- **AND** each command page preserves its bounded recipe, owners, decisions, durable outputs, terminal states, and resume inputs

#### Scenario: Existing procedures remain callable
- **WHEN** compatibility procedures are inspected
- **THEN** the accepted landscape, intake, expansion, theory comparison, method trial, comparative, audit, paper, and template procedures remain public commands of the new entrypoint

#### Scenario: CRUD actions remain grouped by object
- **WHEN** manager actions are inspected
- **THEN** survey and dataset actions remain grouped under their accepted public manager commands

#### Scenario: Generic maintenance remains absent
- **WHEN** the public command list is inspected
- **THEN** it excludes standalone source-audit, repository-refresh, generic environment-repair, full-Kaoju, resume, and list-passes commands

#### Scenario: Empty invocation uses help
- **WHEN** the public entrypoint is invoked without a task or command
- **THEN** it executes help and reports the public command groups

### Requirement: Kaoju Survey Process Data Is Extension-Queried
Kaoju active guidance SHALL query the checked process contract through the package extension while resolving protected members through catalog metadata.

#### Scenario: Entrypoint loads checked contract
- **WHEN** `isomer-ext-kaoju-entrypoint` starts a routing task
- **THEN** it runs `isomer-cli --print-json ext kaoju process show`
- **AND** the response identifies the new public entry skill, public commands, protected logical ids, and binding policy

#### Scenario: Entrypoint loads local command process
- **WHEN** a selected public command has a parent-owned procedure
- **THEN** it loads the corresponding command page from the public pack's `commands/` directory
- **AND** it does not duplicate that procedure in a protected member

### Requirement: Kaoju Cross-Skill Procedures Are Shared-Skill Owned
Kaoju guidance used across multiple protected stages SHALL remain owned by logical capability `isomer-kaoju-shared` and routed through the public parent.

#### Scenario: Stage needs common discipline
- **WHEN** a protected Kaoju member needs common evidence, source identity, lineage, context, Gate, owner-routing, Artifact recording, or terminal rules
- **THEN** it invokes `isomer-ext-kaoju-entrypoint->shared` or a declared shared subcommand
- **AND** it does not traverse into the shared member or duplicate the complete process

#### Scenario: Shared member is privately projected
- **WHEN** a Kaoju member is selected for bounded private projection
- **THEN** manifest dependency closure includes `isomer-kaoju-shared` when required

### Requirement: Kaoju Pipeline Supports Authorized Run-To Recovery
The public Kaoju entrypoint SHALL keep each survey command bounded while allowing authorized target-scoped chaining across protected members and public procedures.

#### Scenario: Target lacks accepted artifacts
- **WHEN** synthesis, drafting, PDF construction, comparison, or export lacks known producible artifacts
- **THEN** the operation reports paused status, exact missing semantic ids, producer routes, and resume point
- **AND** it offers inclusive run-to recovery

#### Scenario: Authorized run-to chains procedures
- **WHEN** the user authorizes a named target
- **THEN** the public entrypoint may call bounded public commands and protected member designators in prerequisite order
- **AND** each invoked capability preserves its own Gates and terminal contract

#### Scenario: No run-to authorization exists
- **WHEN** a bounded procedure recommends another macro action without authorization
- **THEN** the public entrypoint reports the recommendation and stops

### Requirement: Kaoju Run-To Preserves Interaction and Gate Contracts
Kaoju run-to SHALL automate only routine in-scope prerequisite routing and preserve clarification, Proceed Decision, resource, publication, and human Gate contracts.

#### Scenario: Routine prerequisite is discovered
- **WHEN** a protected member or public procedure reports a routine producible prerequisite
- **THEN** the entrypoint may invoke its declared owner under active run-to authorization

#### Scenario: Protected boundary is reached
- **WHEN** continuation requires an unresolved choice, Gate, unauthorized resource, or no-progress repeat
- **THEN** the entrypoint pauses with the current durable state and precise resume guidance

## ADDED Requirements

### Requirement: Direct User Intent Remains Public
Accepted Kaoju survey intents SHALL remain public commands of `isomer-ext-kaoju-entrypoint` even when protected members perform their bounded stages.

#### Scenario: User requests source-code survey work
- **WHEN** the user explicitly requests source ingestion, code-run preparation, or a source-code trial
- **THEN** the public entrypoint exposes the corresponding accepted command
- **AND** it routes protected acquisition, examination, trial, service, or platform owners without changing their authority

#### Scenario: User requests a protected stage by task
- **WHEN** a concrete Kaoju task maps directly to audit, comparison, synthesis, writing, or export but omits a public subcommand
- **THEN** task-only entrypoint routing may select the applicable protected member
- **AND** the member remains absent from top-level host discovery
