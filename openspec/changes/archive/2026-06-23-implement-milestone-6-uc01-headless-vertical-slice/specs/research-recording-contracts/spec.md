## ADDED Requirements

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
