## ADDED Requirements

### Requirement: Concrete File Locator Extraction
The query index SHALL only create `research_record_files` rows for concrete file attachments, generated exports, structured payload files, rendered Markdown files, explicit query-index file hints, or payload objects with enough locator evidence to resolve them as files.

#### Scenario: Bare payload path stays unresolved
- **WHEN** a structured payload contains a bare relative path value such as an artifact name without semantic label, file role, operation-set id, locator kind, digest, media type, or accepted base path evidence
- **THEN** query-index rebuild does not create a `research_record_files` row for that value
- **AND** validation does not emit `query_index_file_missing` for that value

#### Scenario: Explicit file hint remains indexed
- **WHEN** lifecycle metadata or payload metadata explicitly declares a file attachment with file role and a resolvable project-local or external locator
- **THEN** query-index rebuild creates a file-index row with role, locator, existence status, and source metadata

#### Scenario: Semantic inventory does not become attachment
- **WHEN** a record payload contains semantic path inventory, readiness evidence, checkpoint paths, or expected workspace surfaces
- **THEN** those entries are not indexed as concrete file attachments unless a separate explicit file hint marks them as attachments

### Requirement: Query-index File Openability
The query index read APIs SHALL expose conservative file openability metadata for indexed file rows so GUI consumers can render actions without guessing filesystem state.

#### Scenario: Existing local file is openable
- **WHEN** a file-index row resolves to an existing project-local file inside an accepted Project or Topic Workspace surface
- **THEN** the read API marks the row as existing and openable and returns enough derived metadata for the GUI to display an open or preview affordance

#### Scenario: Missing or unresolved file is not openable
- **WHEN** a file-index row cannot be resolved locally or resolves to a missing path
- **THEN** the read API marks the row as not openable and includes a deterministic reason
- **AND** the GUI does not try to open the missing or unresolved file

### Requirement: GUI-safe Query Diagnostics
The query-index export API SHALL support generic GUI rendering by summarizing diagnostics while preserving detailed diagnostics.

#### Scenario: Export includes diagnostic summary
- **WHEN** a GUI or operator exports a query-index view for any Research Topic
- **THEN** the response includes full diagnostics and a grouped diagnostic summary by severity and diagnostic code

#### Scenario: GUI renders diagnostics dynamically
- **WHEN** the frontend receives query-index diagnostics for any selected Project root or Research Topic
- **THEN** it renders counts and expandable details from the returned diagnostic data
- **AND** it does not special-case topic ids, known file names, or repository-local paths
