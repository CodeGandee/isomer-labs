## ADDED Requirements

### Requirement: UC-01 Runtime Research Records
The system SHALL persist the minimal research records needed by the UC-01 headless path in Workspace Runtime or file-backed payloads linked from Workspace Runtime.

#### Scenario: Runtime stores UC-01 records
- **WHEN** the UC-01 runner records Artifacts, Evidence Items, Findings or claim candidates, Gates, Decision Records, View Manifests, or Provenance Records
- **THEN** Workspace Runtime stores stable ids, record kinds, statuses, Topic Workspace refs, Research Topic refs, lifecycle refs, content refs when applicable, timestamps, and Provenance refs

#### Scenario: Runtime records remain topic scoped
- **WHEN** a UC-01 runtime record is written
- **THEN** validation confirms that its Research Topic, Topic Workspace, Agent Team Instance, Run, Artifact, Gate, Decision Record, and path refs belong to the selected Topic Workspace

### Requirement: UC-01 Manual Harness Recording
The system SHALL let the manual harness write and read UC-01 research records through generic runtime store helpers without exposing SQL details to product CLI or adapter code.

#### Scenario: Harness writes record bundle
- **WHEN** the UC-01 manual harness accepts a handoff result
- **THEN** runtime helpers can write the associated Artifact, Evidence Item, Finding or claim candidate, Provenance Record, and lifecycle links in one transaction

#### Scenario: Harness reads summary
- **WHEN** the UC-01 manual harness requests a UC-01 summary
- **THEN** harness code returns Research Inquiry, Research Task, Run, handoff, Artifact, Evidence Item, Gate, Decision Record, View Manifest, and Provenance refs needed for deterministic JSON output

### Requirement: UC-01 Harness Validation
The manual harness SHALL validate the UC-01 recording graph and report incomplete vertical-slice state without silently repairing it.

#### Scenario: Missing UC-01 record is reported by the harness
- **WHEN** a UC-01 run is missing a required Artifact, Evidence Item, Gate, Decision Record, View Manifest, or Provenance ref
- **THEN** the harness reports a diagnostic naming the missing record type and referring lifecycle object

#### Scenario: Open follow-up Gate is reported
- **WHEN** a UC-01 follow-up Gate remains open after runner closeout is requested
- **THEN** the harness reports the open Gate as a blocker for UC-01 completion while preserving all recorded options

### Requirement: UC-01 Harness Inspection Summary
The manual harness SHALL include UC-01 research records in deterministic inspection output.

#### Scenario: Runtime inspect reports counts
- **WHEN** a user inspects or validates the Workspace Runtime after a UC-01 run
- **THEN** harness JSON includes counts or summaries for UC-01 Artifacts, Evidence Items, Findings or claim candidates, Gates, Decision Records, View Manifests, and Provenance Records

#### Scenario: Team instance show includes UC-01 refs
- **WHEN** a user shows the UC-01 Agent Team Instance after runner completion
- **THEN** the summary includes linked Research Inquiry, Research Task, Run, handoff, accepted output Artifact, Gate, Decision Record, and View Manifest refs without exposing Houmao native fields
