## ADDED Requirements

### Requirement: Workspace Runtime Payload File Catalog
Workspace Runtime SHALL catalog managed structured payload files in SQLite while keeping those files as the canonical payload content.

#### Scenario: Payload locator is persisted
- **WHEN** a structured research payload file is accepted
- **THEN** Workspace Runtime stores the record id, structured payload id, payload locator, payload digest, payload media type, payload schema/profile refs, validation status, timestamps, and provenance refs in `state.sqlite`

#### Scenario: Payload content is file authoritative
- **WHEN** the runtime needs to validate, render, export, or rebuild indexes for a structured research record
- **THEN** it reads the managed payload JSON file and checks the recorded digest before using the content

#### Scenario: SQLite payload blobs are non-authoritative
- **WHEN** SQLite stores derived JSON snippets, scalar facts, summaries, or compatibility payload fields
- **THEN** those values are treated as cache or migration material and not as the authoritative structured payload

#### Scenario: File drift is reported
- **WHEN** runtime validation finds a missing payload file, invalid JSON payload file, or payload digest mismatch
- **THEN** validation reports a durable diagnostic and preserves the lifecycle record for repair, migration, supersession, or withdrawal

#### Scenario: Revision links are persisted
- **WHEN** a structured record supersedes, refreshes, snapshots, or derives from another record
- **THEN** Workspace Runtime stores explicit revision or relationship refs so current/latest views can be derived without mutating generated Markdown

### Requirement: Existing Payload Migration
Workspace Runtime SHALL provide a migration path from SQLite-stored structured payloads and generated Markdown views to managed payload files.

#### Scenario: Existing SQLite payload is exported
- **WHEN** migration sees a structured payload row with canonical JSON content in SQLite and no managed payload file
- **THEN** migration writes that JSON to the managed payload-file layout, records its locator and digest, and preserves the existing lifecycle record id

#### Scenario: Legacy Markdown is reclassified
- **WHEN** migration sees a generated Markdown file that was produced from a structured payload
- **THEN** migration records it as a legacy generated view or cleanup candidate and does not treat it as canonical payload content

#### Scenario: Index rebuild follows migration
- **WHEN** migration exports payload files
- **THEN** the query index is rebuilt from the managed payload files and recorded runtime metadata
