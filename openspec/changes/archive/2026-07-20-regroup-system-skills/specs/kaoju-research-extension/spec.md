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

#### Scenario: Paper-template actions remain grouped by object
- **WHEN** the role-aware paper-template manager is migrated into the public pack
- **THEN** `manage-paper-template()` remains one parent command with declared children `list()`, `show()`, `create()`, `copy()`, `update()`, `replace()`, `merge()`, `file()`, `metadata()`, `export()`, `observe()`, `archive()`, `delete()`, and `migrate()`
- **AND** `file()` declares `put()` and `remove()` children while `metadata()` declares `patch()`
- **AND** internal routes may use complete chains such as `isomer-ext-kaoju-entrypoint->manage-paper-template()->file()->put()`

#### Scenario: Paper-template role remains command context
- **WHEN** a paper-template action selects content authoring or LaTeX presentation state
- **THEN** the manager resolves explicit `--kind content|latex` context before role-local discovery or mutation
- **AND** content and LaTeX do not become skills, subskills, or command-path components

#### Scenario: Compatibility template creation remains content-only
- **WHEN** the retained `create-paper-template` procedure is invoked
- **THEN** it creates or updates a named content template backed by `KAOJU:PAPER-TEMPLATE-MYST`
- **AND** LaTeX stock creation routes through `manage-paper-template()` with `--kind latex`

#### Scenario: Interaction and resume stay out of the procedure list
- **WHEN** a user requests clarification before work or resumes accepted prior state
- **THEN** clarification-first is represented as an interaction mode shared by procedures
- **AND** resume is represented by a Research Task, Run checkpoint, accepted input refs, and starting stage rather than a separate procedure

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
- **AND** the response identifies the new public entry skill, public commands, protected logical ids, binding policy, manager-action hierarchy, independent content and LaTeX template roles, and current paper-template implementation decisions

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

#### Scenario: Kaoju audit recommends repair
- **WHEN** an audit procedure remains non-repairing and returns defects with bounded producer or repair routes inside an authorized target closure
- **THEN** the controller invokes those repair owners as separate procedures
- **AND** it starts a fresh audit after repair before allowing synthesis or paper writing to consume the repaired evidence

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

### Requirement: Kaoju Template Separation Survives Skill Regrouping
The Kaoju public pack and protected `write` member SHALL preserve the implemented separation between canonical content-template state and named LaTeX presentation stock while changing only skill packaging and routing identities.

#### Scenario: Role-aware process contract is rewritten
- **WHEN** regrouping updates the checked Kaoju survey-process resource
- **THEN** its public entry skill becomes `isomer-ext-kaoju-entrypoint` and its focused skills resolve through protected logical ids and parent-owned designators
- **AND** its manager actions, `template_roles`, independent `main` defaults, `KAOJU:PAPER-TEMPLATE-MYST`, `KAOJU:PAPER-TEMPLATE-LATEX`, preamble, marker, and include composition modes, derived snapshot identities, and drift policy remain intact

#### Scenario: Protected write bundle is moved
- **WHEN** `isomer-kaoju-write` becomes protected member `write`
- **THEN** it retains its private artifact-binding guidance and paper-contract, manuscript-structure, LaTeX-build, validation, and survey-quality references
- **AND** its content-template selection, LaTeX stock selection, exact snapshot composition, entrypoint-aware build, paper-local repair, and publication-lineage behavior remain effective

#### Scenario: Package-owned template services remain external to skill bundles
- **WHEN** the Kaoju skill pack is materialized or `write` is privately projected
- **THEN** template state, payload, support, validation, migration, composition, build, binding, semantic, and process services remain package-owned under `isomer_labs.kaoju`
- **AND** active skills query those services through `isomer-cli ext kaoju` without copying or traversing to their source files

#### Scenario: Existing Topic Workspace template state is encountered
- **WHEN** regrouped skills operate on a Topic Workspace already migrated to the content-template and LaTeX-template contract
- **THEN** they preserve its stable refs, state tokens, managed trees, exports, TeX snapshots, drafts, builds, PDFs, and historical source records
- **AND** skill installation, upgrade, or first invocation does not rerun template-contract migration or adopt another LaTeX source implicitly

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
