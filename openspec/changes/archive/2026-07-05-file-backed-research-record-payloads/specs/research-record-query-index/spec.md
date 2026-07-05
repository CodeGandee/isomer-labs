## ADDED Requirements

### Requirement: Payload-file Query Index Rebuild
The research record query index SHALL derive record summaries, relationships, facets, and file refs from managed payload files and runtime metadata.

#### Scenario: Rebuild reads payload files
- **WHEN** an operator rebuilds the research record query index
- **THEN** the system reads each managed payload JSON file, verifies its digest, and derives indexed rows from the file content and lifecycle metadata

#### Scenario: Missing payload blocks derived rows
- **WHEN** a payload file is missing, invalid, or digest-mismatched during index rebuild
- **THEN** the system reports diagnostics and does not create fresh derived rows from stale SQLite cache content

#### Scenario: Query results locate payload files
- **WHEN** query list, export, lineage, files, facets, or detail commands return a structured research record
- **THEN** the result includes record id, structured payload id, payload locator, payload digest, format profile ref, schema ref, current/latest relationship hints when known, and generated artifact locators when any explicit exports exist

#### Scenario: Markdown is not queried as source
- **WHEN** the query index extracts title, summary, claims, metrics, ideas, routes, relationships, or file refs
- **THEN** extraction uses payload files and authored metadata rather than generated Markdown bodies

### Requirement: Latest and Historical Record Views
The query index SHALL distinguish historical records from current/latest views without relying on fixed generated Markdown files.

#### Scenario: Historical events remain append-only
- **WHEN** multiple rounds produce experiment results, evidence items, decisions, or attempts
- **THEN** the query index exposes them as distinct records with chronological and relationship metadata

#### Scenario: Latest view is derived
- **WHEN** a caller asks for the current candidate board, frontier, latest context, resume packet, or similar current-state concept
- **THEN** the query layer resolves the latest payload-backed snapshot or derives a view from related records without requiring a mutable Markdown file

#### Scenario: Cleanup preserves payload files
- **WHEN** index cleanup removes stale derived query rows or generated-export references
- **THEN** it does not delete managed payload JSON files unless an explicit record deletion or archival policy names those files
