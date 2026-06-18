# research-recording-contracts Specification

## Purpose
Define the durable research recording contract for Isomer Labs, including Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, Gates, record linkage, recording/query APIs, and validation behavior.

## Requirements
### Requirement: Durable Research Record Identity
The system SHALL define durable research records for Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, and Gates inside a Topic Workspace.

#### Scenario: Record ids are stable within a Topic Workspace
- **WHEN** the system creates an Artifact, Provenance Record, Evidence Item, Finding, Research Claim, Decision Record, or Gate
- **THEN** the record has a stable id, `topic_workspace_id`, created timestamp, updated timestamp, status, and record type

#### Scenario: Records carry lifecycle refs
- **WHEN** a record is created for bounded research work
- **THEN** the record carries applicable refs to accepted Research Lifecycle State objects such as Research Topic, Research Inquiry, Research Task, Run, Workflow Stage Cursor, Research Inquiry Relationship, Agent Team Instance, Agent Instance, or Agent Workspace

#### Scenario: Records do not define lifecycle state machines
- **WHEN** a durable research record references a Research Lifecycle State object
- **THEN** the record stores the lifecycle ref and does not redefine that lifecycle object's status set, transition rules, parallel execution scope, or relationship policy

#### Scenario: Rich content stays file-backed
- **WHEN** a record needs rich text, large JSON, tables, figures, logs, prompts, tool outputs, or reports
- **THEN** the record references an Artifact or other file-backed content instead of requiring the rich content to be stored inline

### Requirement: Minimal Artifact Core Record
The system SHALL keep the core Artifact record generic and minimal so topic-specific formats cannot fragment durable Artifact identity, lookup, or validation.

#### Scenario: Core artifact fields are minimal
- **WHEN** the system records the core fields for an Artifact
- **THEN** the core record contains only stable Artifact id, Topic Workspace id, Artifact kind, status, locator kind, locator, created timestamp, updated timestamp, and media type when known

#### Scenario: Core artifact locates content
- **WHEN** an Artifact points to project-local content or external content
- **THEN** the core record uses a locator kind and locator value to identify the file-backed or external content without embedding the rich content inline

#### Scenario: Core artifact does not require topic-specific format fields
- **WHEN** an Artifact is created without a matching Artifact Format Profile or Artifact Extension
- **THEN** the system can still list, locate, validate existence, display generically, and reference the Artifact through durable records

#### Scenario: Optional refs are attached outside core
- **WHEN** an Artifact needs lifecycle refs, producer refs, Run refs, Provenance Record refs, Evidence Item refs, supersession refs, format profile refs, extension refs, validation outcomes, or renderer hints
- **THEN** the system records those values through Artifact Link Records, metadata records, Provenance Records, or other accepted recording APIs rather than requiring them as core Artifact fields

### Requirement: Artifact Format Profiles
The system SHALL support optional Artifact Format Profiles for content-level expectations while preserving the generic Artifact Core Record.

#### Scenario: Format profile is optional
- **WHEN** a Research Topic, Research Task, Run, or command context selects an Artifact Format Profile for an expected output
- **THEN** the system records the selected profile as an optional format attachment or metadata ref for the Artifact and does not make the profile a mandatory core Artifact field

#### Scenario: Format profile describes content expectations
- **WHEN** an Artifact Format Profile is inspected
- **THEN** it may describe artifact kind applicability, media type expectations, schema refs, template refs, validation hints, renderer hints, export hints, opaque future capability refs, compatibility version, and status

#### Scenario: Format profile is declarative-only
- **WHEN** an Artifact Format Profile describes validation, rendering, export, or capability behavior
- **THEN** it does so with declarative metadata and opaque future capability refs, and does not define executable validators, renderers, exporters, command requests, provider contracts, or adapter-specific runtime behavior

#### Scenario: Format profile does not redefine core identity
- **WHEN** an Artifact Format Profile defines schema or template fields
- **THEN** validation rejects any profile field that shadows or redefines the Artifact id, Topic Workspace id, Artifact kind, status, locator kind, locator, or timestamps from the Artifact Core Record

#### Scenario: Unknown format profile is non-fatal
- **WHEN** a recorded Artifact references an Artifact Format Profile that is missing, unsupported, disabled, or unknown
- **THEN** validation reports the format issue while preserving generic Artifact lookup, path validation, provenance linking, and display behavior

### Requirement: Artifact Extensions
The system SHALL support optional Artifact Extensions for topic-specific metadata without changing the core Artifact record.

#### Scenario: Extension adds topic metadata
- **WHEN** a Research Topic enables an Artifact Extension
- **THEN** the extension may add topic-specific metadata fields, validation hints, or renderer hints for matching Artifacts

#### Scenario: Extension is additive only
- **WHEN** an Artifact Extension is validated
- **THEN** validation rejects extension fields that shadow, rename, or redefine core Artifact fields or accepted durable record refs

#### Scenario: Extension data is separable
- **WHEN** an Artifact has topic-specific extension data
- **THEN** the system records that data as an extension record, metadata record, sidecar Artifact, or other explicit attachment linked to the Artifact Core Record

#### Scenario: Missing extension is non-fatal
- **WHEN** an Artifact references an Artifact Extension that is missing, unsupported, disabled, or unknown
- **THEN** validation reports the extension issue while preserving generic Artifact lookup, path validation, provenance linking, and display behavior

### Requirement: Artifact Format Resolution
The system SHALL resolve Artifact Format Profiles and Artifact Extensions from the most specific expected-output context before falling back to topic or built-in defaults.

#### Scenario: Format resolution uses specificity order
- **WHEN** the system determines an Artifact Format Profile for an expected Artifact output
- **THEN** it checks explicit Run or command expected output, Research Task expected output, Research Topic Config defaults, Topic Agent Team Profile or Domain Agent Team Template defaults, and built-in Artifact kind defaults in that order

#### Scenario: Resolved format source is recorded
- **WHEN** an Artifact Format Profile or Artifact Extension is applied to an Artifact
- **THEN** the system records the selected ref and resolution source in an attachment, metadata record, or Provenance Record

#### Scenario: Format resolution does not execute commands
- **WHEN** a resolved Artifact Format Profile references validation, rendering, or export behavior that needs command execution
- **THEN** the system treats those references as opaque future capability refs and does not execute them through Research Recording Contracts

### Requirement: Artifact and Provenance Recording API
The system SHALL expose a host-facing API for recording Artifacts and Provenance Records through Workspace Runtime.

#### Scenario: Artifact is recorded
- **WHEN** an Operator Agent, Execution Adapter, Agent Instance, Service Agent Instance, or GUI-approved action records an Artifact
- **THEN** the API stores the Artifact kind, resolved path or external ref, content type when known, producing actor refs, producing Run or stage refs when known, promotion state, and Provenance Record refs

#### Scenario: Artifact path uses workspace path resolution
- **WHEN** an Artifact points to a project-local file
- **THEN** the file path is resolved and validated through Workspace Path Resolution before the Artifact becomes durable

#### Scenario: Provenance Record is appended
- **WHEN** an Artifact, Evidence Item, Finding, Research Claim, Decision Record, Gate, or state ref is produced, updated, superseded, repaired, imported, or invalidated
- **THEN** the API appends a Provenance Record that links the actor, action summary, source refs, output refs, timestamp, and available prompt, tool-call, or provider refs

#### Scenario: Provenance is not silently rewritten
- **WHEN** a prior Provenance Record is incomplete or wrong
- **THEN** the system records a corrective Provenance Record instead of silently rewriting or deleting the prior record

### Requirement: Evidence Items and Research Claims
The system SHALL use Evidence Items as the support, contradiction, or context boundary for Research Claims.

#### Scenario: Evidence Item references a source
- **WHEN** the system creates an Evidence Item
- **THEN** the Evidence Item records source kind, source ref, relation intent, summary ref or short summary, confidence or quality label when known, and Provenance Record refs

#### Scenario: Research Claim cites Evidence Items
- **WHEN** a Research Claim is marked supported, refuted, or withdrawn because of research evidence
- **THEN** the claim links to one or more Evidence Items that explain the support, contradiction, refutation, context, or withdrawal rationale

#### Scenario: Research Claim statuses are explicit
- **WHEN** a Research Claim is inspected
- **THEN** its status is one of `open`, `supported`, `refuted`, or `withdrawn`, or a later accepted contract has explicitly extended the status set

#### Scenario: Contradiction and context are evidence relations
- **WHEN** an Evidence Item supports, contradicts, contextualizes, refutes, or motivates withdrawal of a Research Claim
- **THEN** the relation is recorded on the Evidence Item or claim-evidence link rather than as a separate Research Claim status

#### Scenario: Unsupported claim remains open
- **WHEN** a Research Claim has no supporting Evidence Item and no explicit withdrawal or refutation
- **THEN** validation reports the claim as open or unsupported rather than supported

#### Scenario: Contradictory evidence blocks strengthening
- **WHEN** a Research Claim has unresolved contradictory Evidence Items
- **THEN** the system does not allow the claim to be strengthened to supported until a Decision Record or updated Evidence Item resolves the contradiction

### Requirement: Findings Query and Write API
The system SHALL expose a host-facing API for querying and writing Findings as reusable evidence-grounded insights.

#### Scenario: Finding is written from evidence
- **WHEN** the system records a Finding
- **THEN** the Finding includes a Research Inquiry ref when an applicable inquiry exists, a summary ref or short summary, scope refs, status, primary Evidence Item refs, optional related Research Claim refs, and Provenance Record refs

#### Scenario: Finding is topic scoped only when no inquiry exists
- **WHEN** the system records a Finding before a specific Research Inquiry exists
- **THEN** the Finding may be scoped to the Research Topic or Topic Workspace and remains eligible to be linked to a Research Inquiry later

#### Scenario: Finding query is scoped
- **WHEN** an Operator Agent or Agent Instance queries Findings
- **THEN** the query can be scoped by Project, Topic Workspace, Research Topic, Research Inquiry, Research Task, Run, tag, status, source record, or relevance text

#### Scenario: Finding does not replace evidence
- **WHEN** a Finding is used to steer later work, writing, review, or reuse
- **THEN** the Finding keeps refs to its supporting Evidence Items and does not become standalone support for a Research Claim without those refs

### Requirement: Decision Records and Gates
The system SHALL distinguish ordinary Decision Records from human-return Gates while allowing a Decision Record to resolve a Gate.

#### Scenario: Decision Record captures a meaningful choice
- **WHEN** the user, Operator Agent, or Agent Team Instance records a meaningful research choice
- **THEN** the Decision Record includes selected option, rationale, actor, timestamp, consequence summary, relevant Evidence Item or Artifact references, and rejected alternatives when material

#### Scenario: Gate blocks governed action
- **WHEN** a Gate is open
- **THEN** the system blocks only the action governed by that Gate and still permits unrelated inspection, safe edits, and non-governed work

#### Scenario: Gate resolution records outcome
- **WHEN** a human user resolves a Gate through the Operator Agent
- **THEN** the system records the resolution status, actor, timestamp, selected option, consequence summary, and associated Decision Record when a meaningful choice was made

#### Scenario: Gate cancellation records provenance
- **WHEN** a Gate is cancelled or superseded without a meaningful user choice
- **THEN** the system records the Gate status change and a Provenance Record without requiring a Decision Record

#### Scenario: Gate statuses are explicit
- **WHEN** a Gate is inspected
- **THEN** its status is one of `open`, `resolved`, `cancelled`, or `superseded`, or a later accepted contract has explicitly extended the status set

### Requirement: Recording Graph Validation
The system SHALL validate research recording refs and report durable workspace issues without silently deleting records.

#### Scenario: Missing Artifact file is reported
- **WHEN** an Artifact points to a project-local file that no longer exists
- **THEN** validation reports the missing file and keeps the durable Artifact visible for repair, supersession, or withdrawal

#### Scenario: Broken record ref is reported
- **WHEN** an Evidence Item, Finding, Research Claim, Decision Record, Gate, or Provenance Record points to a missing record
- **THEN** validation reports the broken ref and identifies the referring record

#### Scenario: Unsupported Research Claim is reported
- **WHEN** a Research Claim is marked supported without a valid supporting Evidence Item
- **THEN** validation reports the claim as unsupported

#### Scenario: Unresolved Gate is reported
- **WHEN** a Gate is open and its governed action is requested
- **THEN** validation reports the unresolved Gate as a blocker for that action

#### Scenario: Stale Provenance is reported
- **WHEN** a record has changed after its latest Provenance Record without a corrective Provenance Record
- **THEN** validation reports stale provenance for that record

### Requirement: Research Extension Recording
The system SHALL record execution, provider, scheduler, baseline-waiver, Skill Binding, and Gate policy extension choices through existing durable research records without creating runtime-state fields on Artifact Core Records, Research Topic Config, or Effective Topic Context.

#### Scenario: Command request is linked to Run and Provenance records
- **WHEN** an Execution Adapter Command Request is created, dispatched, completed, failed, cancelled, superseded, retried, or imported from an external executor
- **THEN** the system records selected extension point refs, Capability Binding refs, Skill Binding projection refs, Execution Adapter refs, policy refs, source refs, input refs, expected output refs, outcome summary refs, and actor refs through Run records, Artifact refs, and Provenance Records

#### Scenario: Provider results are recorded by evidence-use intent
- **WHEN** a literature provider, baseline provider, renderer, exporter, service adapter, or other provider-backed extension returns results
- **THEN** the system records those results as Artifacts, Findings, Evidence Items, or Provenance Records according to the result's evidence-use intent and does not treat provider output as claim support until accepted Evidence Item links exist

#### Scenario: Context-only literature is preserved before distillation
- **WHEN** a literature provider result is collected only for orientation, source review, adjacent-work scouting, or future comparison
- **THEN** the system records the raw or provider-shaped result as a provider-output Artifact with source metadata and Provenance refs before any optional Finding or Evidence Item is derived from it

#### Scenario: Gate policy preflight records governed decisions
- **WHEN** execution preflight allows, blocks, defers, or escalates a governed operation because of cost, credential use, private data access, external upload, long compute, destructive change, publication-facing output, or baseline waiver
- **THEN** the system records the selected policy refs, operation refs, affected resources, rationale, actor refs, and outcome through Gates, Decision Records, or Provenance Records according to the Research Recording Contracts

#### Scenario: Baseline waiver preserves comparator context
- **WHEN** a baseline-waiver policy or Gate permits work to continue without an accepted active baseline
- **THEN** the system records the waiver as a Decision Record or Gate outcome, links the affected Research Topic, Research Inquiry, Research Task, Run, comparator Artifacts, Evidence Items, Findings, and known limitations, and keeps later claims from treating the waiver itself as comparator evidence

#### Scenario: Scheduler observations stay durable but not authoritative over route state
- **WHEN** scheduler policy, continuation policy, a completion watcher, or an external queue reports progress, retry, pause, resume, stale-watch, failure, or completion signals
- **THEN** the system records durable observations through Run records, Signal Observations, Artifacts, or Provenance Records while leaving Workflow Stage Cursor and Agent Team Instance lifecycle state as the authority for research route and lifecycle state

#### Scenario: Extension refs do not expand Artifact Core Record
- **WHEN** an Artifact was produced, validated, rendered, exported, imported, or superseded through an execution or provider extension
- **THEN** selected extension refs, adapter refs, command request refs, validation outcomes, provider refs, and policy refs are stored through Provenance Records, metadata records, Artifact Link Records, or other accepted attachments rather than new mandatory Artifact Core Record fields

#### Scenario: Missing recording obligations block dispatch
- **WHEN** an executable or provider-backed operation lacks the Run, Artifact, Evidence Item, Finding, Decision Record, Gate, or Provenance recording obligations required by its selected Research Operation Extension Point
- **THEN** validation blocks only the dependent dispatch or promotion and reports the missing recording obligation
