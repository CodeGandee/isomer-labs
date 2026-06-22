## ADDED Requirements

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
