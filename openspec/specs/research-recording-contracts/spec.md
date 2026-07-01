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

### Requirement: Runtime-backed Recording Validation
The system SHALL use Workspace Runtime record lookup to validate Artifact, Gate, Research Claim, Evidence Item, Decision Record, and Provenance Record refs that affect runtime lifecycle state.

#### Scenario: Runtime validation checks unresolved Gates
- **WHEN** a Run, Workflow Stage Cursor, handoff, Agent Team Instance, or governed action references an open Gate
- **THEN** runtime validation reports the unresolved Gate as a blocker for only the governed action

#### Scenario: Runtime validation checks supported claims
- **WHEN** a Research Claim is marked supported in Workspace Runtime-visible records
- **THEN** runtime validation confirms that the claim links to at least one valid supporting Evidence Item

#### Scenario: Runtime validation checks stale provenance
- **WHEN** a runtime-visible record changed after its latest Provenance Record without a corrective Provenance Record
- **THEN** runtime validation reports stale provenance for that record

#### Scenario: Runtime validation preserves missing records
- **WHEN** an Artifact, Evidence Item, Research Claim, Decision Record, Gate, or Provenance Record ref is broken
- **THEN** runtime validation reports the missing record and keeps the referring record visible for repair, supersession, or withdrawal

### Requirement: Runtime Mutation Provenance
The system SHALL append or reference Provenance Records for Workspace Runtime mutations that create or change lifecycle, team instance, path, handoff, or validation state.

#### Scenario: Runtime init records provenance
- **WHEN** a Workspace Runtime is initialized
- **THEN** the system records or references a Provenance Record that names the actor, Project, Research Topic, Topic Workspace, path plans, runtime schema version, and source Project Manifest refs

#### Scenario: Team instance creation records provenance
- **WHEN** an Agent Team Instance record is created from a Topic Agent Team Profile
- **THEN** the system records or references Provenance Records for the Agent Team Instance, Agent Instance records, Agent Workspace records, path plans, and initial Workflow Stage Cursor records

#### Scenario: Corrective validation does not rewrite history
- **WHEN** runtime validation discovers broken refs, missing paths, stale handoffs, unsupported claims, unresolved Gates, or stale provenance
- **THEN** remediation records corrective Provenance Records or status transitions rather than silently rewriting prior Provenance Records

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

### Requirement: Manifest Provenance Records
The system SHALL record Provenance Records for Houmao adapter JSON manifest creation, update, reconciliation, and adoption.

#### Scenario: Link manifest provenance is recorded
- **WHEN** Isomer writes or exports `adapter-link.json`
- **THEN** the system records or links Provenance Records naming the actor, Project, Research Topic, Topic Workspace, Agent Team Instance, Topic Agent Team Profile, Execution Adapter ref, manifest path, and creation timestamp

#### Scenario: Runtime manifest provenance is recorded
- **WHEN** Isomer writes or updates `adapter-runtime-manifest.json`
- **THEN** the system records or links Provenance Records naming the observation source, Houmao read-only command refs, affected Agent Team Instance or Agent Instance refs, adapter refs, manifest digest, and timestamp

### Requirement: Reconciliation Diagnostic Artifacts
The system SHALL record reconciliation diagnostics as durable Artifacts or adapter payload refs when they are needed to explain adoption, drift, conflict, stale state, or rejection.

#### Scenario: Drift diagnostic is recorded
- **WHEN** reconciliation detects drift between JSON manifests, referenced launch-material digests, Workspace Runtime records, and live Houmao state
- **THEN** the system records a diagnostic Artifact or adapter payload ref linked to the affected Agent Team Instance, Agent Instance refs when known, manifest refs, and Provenance Records

#### Scenario: Conflict diagnostic is redacted
- **WHEN** reconciliation detects a mapping conflict involving Houmao native payloads
- **THEN** the recorded diagnostic excludes credentials, tokens, passwords, API keys, raw private messages, and other secret material

#### Scenario: Adoption decision is auditable
- **WHEN** an externally launched Houmao-backed Agent Team Instance is adopted or rejected
- **THEN** the system records the adoption decision, mapping confidence, manifest refs, diagnostics, actor ref, timestamp, and Provenance Records

### Requirement: Handoff Adapter Provenance
The system SHALL record Provenance Records for Houmao-backed handoff dispatch, observation, and normalization operations.

#### Scenario: Dispatch provenance names source refs
- **WHEN** a Houmao-backed handoff dispatch is attempted
- **THEN** Provenance Records name the actor, Project, Research Topic, Topic Workspace, Agent Team Instance, source Agent Instance, target Agent Instance, Run or Research Task refs, expected output refs, Completion Watcher Contract refs, Execution Adapter ref, adapter payload refs, and readiness or Gate refs when relevant

#### Scenario: Observation provenance names adapter payload
- **WHEN** adapter observation records a Signal Observation, snapshot, or Artifact
- **THEN** Provenance Records link the observation to the handoff, Run, Agent Team Instance, Agent Instance refs when known, opaque adapter refs, adapter payload refs, and observation source

#### Scenario: Normalization provenance records decision
- **WHEN** a normalization request accepts, rejects, blocks, supersedes, or routes repair for a candidate handoff result
- **THEN** Provenance Records capture the Operator Agent actor, reviewed Signal Observation refs, decision rationale, output refs, corrective refs when present, and affected lifecycle refs

### Requirement: Adapter Signal Observation Recording
The system SHALL record Houmao mail, gateway, file, and inspection signals as Signal Observations linked to runtime lifecycle refs.

#### Scenario: Mail observation is recorded
- **WHEN** Houmao mail returns a delegated agent reply
- **THEN** the system records a Signal Observation with handoff ref, Run ref when known, source Agent Instance ref, adapter payload ref, timestamp, and Provenance refs

#### Scenario: Gateway observation is recorded
- **WHEN** Houmao gateway state reports progress, failure, or candidate completion
- **THEN** the system records a Signal Observation linked to relevant Agent Team Instance, Agent Instance, Run, handoff, and adapter refs

#### Scenario: Observation content remains file-backed
- **WHEN** an observation includes rich reply text, logs, transcripts, generated files, or tool output
- **THEN** the system records or links that content as Artifacts, logs, or adapter payload refs instead of embedding it in lifecycle records

### Requirement: Handoff Result Normalization Recording
The system SHALL convert accepted manual handoff results into durable Run, Artifact, Decision Record, Evidence Item, Finding, or Provenance refs according to research recording contracts.

#### Scenario: Accepted result records outputs
- **WHEN** the Operator Agent accepts a Houmao-observed handoff result
- **THEN** the system records output Artifact refs, Run status updates, handoff accepted state, and Provenance Records

#### Scenario: Result is not automatically evidence
- **WHEN** a Houmao-backed specialist returns a claim, measurement, literature summary, or analysis note
- **THEN** the result is not treated as Evidence Item support for a Research Claim until normalized into accepted Evidence Item or Finding records

#### Scenario: Rejected result records rationale
- **WHEN** the Operator Agent rejects a candidate handoff result
- **THEN** the system records rejection rationale, affected refs, any corrective Service Request or follow-up handoff refs, and Provenance Records

### Requirement: UC-01 Artifact Recording Bundle
The system SHALL record UC-01 research outputs as durable Artifacts or Artifact-linked records with Provenance Records.

#### Scenario: Accepted handoff output becomes Artifact-backed record
- **WHEN** Operator Agent normalization accepts a UC-01 handoff output
- **THEN** the system records the output as a seed-source summary, Flash Attention implementation note, GB10 or Blackwell feature note, attention-kernel bottleneck note, shape-family constraint, correctness constraint, Evidence Item, Finding or claim candidate, review note, inquiry option, or Provenance Record according to its evidence-use intent

#### Scenario: Rich content is file-backed
- **WHEN** UC-01 output contains seed-source summaries, Flash Attention implementation notes, GB10 feature notes, tables, claim graph inputs, review notes, or inquiry comparison text
- **THEN** the system stores rich content as project-local files or Artifact payloads and stores refs in Workspace Runtime rather than embedding the full content in generic lifecycle fields

### Requirement: UC-01 Evidence Boundary
The system SHALL keep Evidence Items as the boundary for claim support in the UC-01 path.

#### Scenario: Evidence Item records source relation
- **WHEN** a seed source, literature note, or review note is used as evidence in UC-01
- **THEN** the system records an Evidence Item with source ref, relation intent, summary or summary ref, quality or confidence label when known, and Provenance Record refs

#### Scenario: Claim candidate remains candidate without evidence
- **WHEN** a claim candidate has no accepted Evidence Item links
- **THEN** validation does not treat it as a supported Research Claim and reports unsupported support attempts as recording issues

### Requirement: UC-01 Gate and Decision Records
The system SHALL record follow-up inquiry choice through Gate and Decision Record objects rather than a freeform log entry.

#### Scenario: Gate includes options
- **WHEN** UC-01 generates follow-up inquiry options
- **THEN** the Gate or linked Artifact records the candidate options, governed action, actor refs, affected lifecycle refs, route classification candidates, and status

#### Scenario: Decision Record captures selection
- **WHEN** the follow-up inquiry Gate is resolved
- **THEN** the Decision Record records the selected option, route classification, rationale, actor, timestamp, consequence summary, selected Research Inquiry ref, rejected alternatives when material, and supporting Artifact or Evidence Item refs

#### Scenario: Measured optimization is deferred
- **WHEN** the selected follow-up inquiry route is UC-07-style measured optimization
- **THEN** UC-01 records the route decision and selected Research Inquiry ref without recording baseline measurement, candidate optimization, speedup, utilization, or correctness-result Artifacts

### Requirement: UC-01 Provenance Coverage
The system SHALL attach Provenance Records to UC-01 runtime mutations and research records.

#### Scenario: Runner records provenance
- **WHEN** the UC-01 runner creates or updates Research Inquiries, Research Tasks, Runs, handoffs, Artifacts, Evidence Items, Gates, Decision Records, View Manifests, or Agent Team Instance refs
- **THEN** each created or updated record has a Provenance Record or provenance ref naming the actor, action summary, source refs, output refs, and timestamp

#### Scenario: Corrective closeout preserves prior provenance
- **WHEN** a UC-01 result is rejected, repaired, superseded, or replaced
- **THEN** the system records corrective Provenance Records instead of rewriting or deleting the prior records

### Requirement: UC-01 View Manifest Records
The system SHALL record View Manifest refs for UC-01 semantic views without requiring GUI runtime state.

#### Scenario: Literature matrix manifest is recorded
- **WHEN** UC-01 records seed-source summaries, Flash Attention implementation notes, and GB10 or Blackwell feature notes
- **THEN** it records a literature matrix View Manifest that references the source Artifacts and Evidence Items

#### Scenario: Claim graph and inquiry comparison manifests are recorded
- **WHEN** UC-01 records claim candidates and follow-up inquiry options
- **THEN** it records claim graph and inquiry comparison View Manifests that reference the relevant Findings or claim candidates, Evidence Items, Gate, Decision Record, and Research Inquiry refs

### Requirement: Semantic Project-local Artifact Locators
Research Recording Contracts SHALL preserve semantic surface evidence for project-local file-backed Artifacts and Provenance-linked files.

#### Scenario: Artifact locator stores semantic surface evidence
- **WHEN** an Artifact is recorded for a project-local file under a resolved semantic surface
- **THEN** the durable record stores or links the semantic label, scope ref, Path Plan id when available, and relative path beneath the resolved surface instead of relying only on an absolute path

#### Scenario: Provenance file ref stores semantic surface evidence
- **WHEN** a Provenance Record or linked support record references a project-local file produced by a command, service, adapter, or Agent Instance
- **THEN** the durable reference stores or links semantic path evidence before the file becomes part of durable research state

#### Scenario: External locator remains explicit
- **WHEN** an Artifact points outside accepted Project or Topic Workspace semantic surfaces
- **THEN** the recording API stores it as an external or adopted locator with explicit provenance rather than pretending it is covered by Workspace Path Resolution

#### Scenario: Tmp path cannot become durable locator directly
- **WHEN** a caller tries to record a file under `topic.tmp`, `topic.repos.main.tmp`, `agent.tmp`, or another disposable semantic surface as a durable Artifact or Provenance file
- **THEN** validation rejects the dependency until the file is promoted or copied to an accepted durable semantic surface

### Requirement: Extension-backed Research Record CRUD
The system SHALL expose a transitional `isomer-cli ext research records` CRUD surface for topic-scoped research records before the native `project records ...` API exists.

#### Scenario: Record create stores runtime lifecycle row
- **WHEN** an actor creates a research record through `isomer-cli ext research records create`
- **THEN** the system writes a Workspace Runtime lifecycle record with record kind, status, topic refs, lifecycle refs, transition metadata, provenance refs, optional content path, and the exact placeholder token when provided

#### Scenario: Record create writes optional body
- **WHEN** the create request includes inline body content or a body file
- **THEN** the system writes or copies the body under the resolved semantic label for that record class and stores the resulting content path on the lifecycle record

#### Scenario: Record show reads one record
- **WHEN** an actor calls `isomer-cli ext research records show <record-id>`
- **THEN** the system returns the selected runtime-backed record and includes body content only when explicitly requested

#### Scenario: Record list filters records
- **WHEN** an actor calls `isomer-cli ext research records list` with filters such as record kind, placeholder, profile, status, producer, or consumer
- **THEN** the system returns only matching records from the selected Topic Workspace

#### Scenario: Record update preserves identity
- **WHEN** an actor updates metadata, status, body, or lifecycle refs through `isomer-cli ext research records update`
- **THEN** the system preserves the record id, updates the timestamp, records the mutation metadata, and does not silently rewrite prior provenance refs

#### Scenario: Record delete archives by default
- **WHEN** an actor deletes a research record through `isomer-cli ext research records delete`
- **THEN** the system archives the record by default and does not remove durable body files unless a later accepted contract defines destructive deletion

### Requirement: Placeholder Metadata on Research Records
The system SHALL preserve v2 placeholder binding metadata on records created through the research records extension.

#### Scenario: Placeholder metadata is queryable
- **WHEN** a record is created with `--placeholder <PLACEHOLDER>`
- **THEN** the record stores the placeholder token in transition metadata so later agents can list or show records by that placeholder

#### Scenario: Skill ownership metadata is queryable
- **WHEN** a record is created with producer, consumer, skill, or profile metadata
- **THEN** the record stores those values in transition metadata so later agents can query by semantic role as well as record kind

### Requirement: Topic Actor Research Recording
Research recording APIs SHALL accept records produced by Topic Actors, Project Operator Sessions, Operator Agents, or formal Agent Instances without requiring Agent Team Instance identity for human-orchestrated work.

#### Scenario: Topic Actor creates accepted artifact
- **WHEN** a Topic Actor creates or updates an accepted research artifact through `isomer-cli ext research records`
- **THEN** the recorded lifecycle row and body location include the Research Topic or Topic Workspace context, record kind, placeholder token when applicable, semantic label, profile metadata, producer metadata, `topic_actor_name`, actor kind or runtime kind when known, controller metadata when known, and optional adapter refs
- **AND** Agent Team Instance, Agent Instance, and formal Agent Workspace refs remain absent unless the record was actually produced inside a launched team context

#### Scenario: Topic Actor records remain queryable with team records
- **WHEN** a later skill queries research records for the selected Topic Workspace
- **THEN** records created by Topic Actors are returned alongside records created by Operator Agents, Execution Adapters, Agent Instances, or Service Agent Instances when they match the same topic, placeholder, record kind, profile, semantic label, producer, or topic actor filters

#### Scenario: Formal adoption is out of scope
- **WHEN** a caller asks to adopt Topic Actor-produced work into a formal Agent Instance or Agent Team Instance identity
- **THEN** the system reports that formal adoption is unsupported by this change
- **AND** it preserves the original Topic Actor production metadata instead of rewriting, copying, or linking it as formal team output

