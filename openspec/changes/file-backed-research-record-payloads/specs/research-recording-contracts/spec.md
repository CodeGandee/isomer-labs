## ADDED Requirements

### Requirement: File-backed Structured Research Payloads
The system SHALL treat accepted structured research payload JSON files as the durable content for structured research records.

#### Scenario: Accepted payload is file-backed
- **WHEN** an agent, operator, GUI, or service creates an accepted structured research record
- **THEN** the system validates the JSON payload and writes it to a managed Topic Workspace payload file before treating the record as durable

#### Scenario: SQLite is not the only payload copy
- **WHEN** a structured research record is durable
- **THEN** the canonical payload can be recovered from its managed JSON file without reading a SQLite payload blob

#### Scenario: Payload file identity is recorded
- **WHEN** a structured payload file is accepted
- **THEN** the record stores payload locator, payload digest, format profile ref when known, schema ref when known, validation status, producer metadata, and provenance refs through the research recording API

#### Scenario: Historical rounds create distinct records
- **WHEN** a research round creates a new experiment result, evidence item, route decision, attempt record, or other historical event
- **THEN** the system records a distinct payload-backed record instead of appending the event to a generated Markdown file

#### Scenario: Current state uses snapshots or derived views
- **WHEN** a concept such as frontier, candidate board, latest context, or resume packet needs current-state inspection across rounds
- **THEN** the system represents it through payload-backed snapshots, revision links, latest pointers, or query-derived views instead of a living generated Markdown file

### Requirement: Markdown Is Not Structured Record State
The system SHALL render Markdown for structured research records only as a view or explicit export, not as the default durable state of the record.

#### Scenario: Default create does not write Markdown
- **WHEN** a structured research record is created with a JSON payload
- **THEN** the default durable output is the managed JSON payload record and not a generated Markdown file

#### Scenario: Markdown render is on demand
- **WHEN** a caller asks to inspect a structured research record as Markdown
- **THEN** the system resolves the payload file and template and renders Markdown for the caller without requiring a Markdown file to already exist

#### Scenario: Markdown export is generated artifact
- **WHEN** a caller explicitly exports a structured research record to Markdown
- **THEN** the exported Markdown is recorded as a generated artifact snapshot with provenance and is not parsed as the source of structured fields
