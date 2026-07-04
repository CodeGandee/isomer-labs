## ADDED Requirements

### Requirement: Workspace Runtime Research Record Query Index Persistence
The system SHALL persist additive research record query-index tables inside the selected Topic Workspace's Workspace Runtime.

#### Scenario: Runtime init prepares query-index tables
- **WHEN** Workspace Runtime initialization or reopening prepares the current supported schema
- **THEN** it ensures the research record index, edge index, file index, facet tables, and generic JSON fact table exist without replacing existing lifecycle records or structured payload rows

#### Scenario: Read-only runtime open does not prepare query-index tables
- **WHEN** a read-only command opens a Topic Workspace runtime to inspect records, validation diagnostics, or query exports
- **THEN** it does not create missing query-index tables or perform query-index refresh, repair, or backfill writes

#### Scenario: Query-index rows remain topic scoped
- **WHEN** the Workspace Runtime writes or rebuilds query-index rows
- **THEN** each row carries the selected Research Topic and Topic Workspace refs and validation reports cross-topic leakage

#### Scenario: Runtime validation includes query-index diagnostics
- **WHEN** runtime validation inspects a Topic Workspace with query-index tables
- **THEN** it reports missing indexed records, stale derived rows, broken edges, missing files, extractor failures, unsupported claim support, and cross-topic refs in the deterministic diagnostic stream

### Requirement: Workspace Runtime Query Index Rebuild
The system SHALL provide idempotent rebuild behavior for the research record query index.

#### Scenario: Rebuild preserves authored metadata
- **WHEN** the system rebuilds the query index for a Topic Workspace
- **THEN** it can recreate derived rows from canonical records and payloads while preserving or separately reporting authored metadata that cannot be regenerated from payloads

#### Scenario: Rebuild does not require clean Markdown parsing
- **WHEN** existing rendered Markdown bodies are malformed, manually edited, or missing parser-friendly structure
- **THEN** rebuild still indexes lifecycle records and structured payloads and records non-fatal diagnostics for unavailable body-derived hints

### Requirement: Workspace Runtime Query Index Cleanup
The system SHALL provide safe cleanup behavior for stale or orphaned research record query-index rows.

#### Scenario: Cleanup targets only query-index data
- **WHEN** query-index cleanup applies a cleanup plan
- **THEN** Workspace Runtime mutates only query-index tables and preserves canonical lifecycle records, structured payloads, rendered Markdown, operation-set files, accepted artifacts, and record bodies

#### Scenario: Cleanup respects row source classification
- **WHEN** cleanup evaluates authored, payload-derived, file-derived, or body-inferred rows
- **THEN** it reports the row source classification and applies only the selected cleanup classes instead of deleting all rows for a record blindly

#### Scenario: Cleanup reports deterministic results
- **WHEN** cleanup completes in preview or apply mode
- **THEN** the command returns deterministic JSON with selected cleanup classes, affected row counts by table, affected record ids when available, skipped rows, and diagnostics
