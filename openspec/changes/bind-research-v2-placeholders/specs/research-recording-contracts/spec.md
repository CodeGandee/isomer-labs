## ADDED Requirements

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
