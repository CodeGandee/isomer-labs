## ADDED Requirements

### Requirement: Indexed Research Record Write Metadata
The system SHALL allow research record create and update operations to carry optional relationship, file, and index-hint metadata for the research record query index while preserving payload-first record authoring.

#### Scenario: Record create accepts optional index metadata
- **WHEN** an Operator Agent, Topic Actor, Agent Instance, or GUI-approved action creates a structured research record
- **THEN** the recording API can accept optional relationship refs, file attachments, source JSON path hints, and GUI facet hints in the same request as the canonical record payload

#### Scenario: Record producers do not write index tables
- **WHEN** a record producer supplies relationship refs, file attachments, source JSON path hints, or GUI facet hints
- **THEN** the producer passes them to the recording API and Workspace Runtime owns the resulting query-index table writes

#### Scenario: Payload-first authoring remains normal
- **WHEN** a structured research record has an Artifact Format Profile and schema-backed payload
- **THEN** the normal accepted write path remains authoring the structured payload and rendering durable Markdown from that payload, not hand-authoring Markdown for later parsers to interpret

#### Scenario: Record update can refresh index metadata
- **WHEN** a structured research record is updated with a changed payload, relationship refs, file refs, or index hints
- **THEN** the recording API updates the canonical record first and then refreshes affected query index rows or marks them stale for rebuild

#### Scenario: Record reads stay non-mutating
- **WHEN** a record list, show, validate, render, or export operation inspects research records
- **THEN** it does not write canonical records, query-index rows, or index repair rows to Workspace Runtime

### Requirement: Indexed Research Record Validation
The system SHALL validate relationship, file, and index-hint metadata without deleting durable research records.

#### Scenario: Broken index refs are reported
- **WHEN** relationship metadata, file metadata, or extracted facet rows point to missing records, cross-topic records, invalid paths, or unsupported relation kinds
- **THEN** validation reports deterministic diagnostics that identify the referring record and the failed index metadata

#### Scenario: Unsupported claim support is not strengthened
- **WHEN** a claim facet or claim-bearing record is marked supported only by a low-confidence inferred edge
- **THEN** validation reports the claim support as insufficient until an accepted payload field, authored edge, or Evidence Item link supports it
