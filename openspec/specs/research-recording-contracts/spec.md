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
