## ADDED Requirements

### Requirement: Query Index Stores Artifact Family and Semantic Identity
The research record query index SHALL index family-neutral artifact identity from canonical record metadata and managed payloads.

#### Scenario: Semantic record is indexed
- **WHEN** a record carries `artifact_family` and `semantic_id`
- **THEN** its indexed summary stores both fields with record id, kind, status, profile, title, summary, revision state, validation state, timestamps, and canonical detail locators
- **AND** a payload and metadata mismatch produces a diagnostic instead of conflicting indexed values

#### Scenario: Existing placeholder record remains indexable
- **WHEN** a DeepSci record carries a placeholder but no authored family-neutral semantic id
- **THEN** the index preserves the placeholder and current DeepSci facets
- **AND** any compatibility-derived semantic identity is marked as derived rather than authored

### Requirement: Query CLI Filters Research Artifact Families
The research-record query surface SHALL provide deterministic filters for artifact family, semantic id, and latest-state candidates.

#### Scenario: Family filter lists Kaoju records
- **WHEN** a caller queries with `--artifact-family kaoju`
- **THEN** only Kaoju records in the selected Topic Workspace are returned
- **AND** optional record kind, status, profile, semantic id, procedure, or limit filters compose with the family filter

#### Scenario: Semantic id filter is exact
- **WHEN** a caller queries with `--semantic-id kaoju:<id>`
- **THEN** results match that exact semantic id and do not match a prefix, title, placeholder, or similarly named profile

#### Scenario: Latest-only resolves explicit state
- **WHEN** a caller requests `--latest-only`
- **THEN** the query prefers explicit revision, supersession, and latest metadata over timestamps
- **AND** competing active records without a responsible latest choice are returned with ambiguity diagnostics rather than silently reduced to one record

### Requirement: Family-Neutral Profiles Drive Query Facets
The query index SHALL use declarative neutral-profile metadata to derive family-specific facets without hard-coded Kaoju extraction branches.

#### Scenario: Kaoju profile extracts declared facets
- **WHEN** a managed Kaoju payload uses a profile declaring relationship, file, claim, metric, catalog, source, evidence, procedure, or terminal-status paths
- **THEN** index rebuild extracts values only from those declared paths and explicit authored metadata
- **AND** it records profile and JSON-path provenance for derived facets

#### Scenario: Unknown profile preserves generic summary
- **WHEN** a neutral research payload uses an unknown, disabled, or invalid profile
- **THEN** the index preserves generic record identity, title, summary, family, semantic id, and content locators when valid
- **AND** it reports profile diagnostics and does not invent family-specific facets

### Requirement: Kaoju Survey Queries Support Management Views
The query index SHALL expose enough canonical information for Kaoju survey list, status, detail, lineage, and export actions.

#### Scenario: Survey list returns management fields
- **WHEN** `manage-survey list` queries indexed Kaoju records
- **THEN** each result includes stable record id, semantic id, title, summary, status, revision or latest posture, procedure, terminal status when applicable, validation state, and canonical detail locator

#### Scenario: Survey status follows lineage and state
- **WHEN** `manage-survey status` inspects a survey or procedure record
- **THEN** it can query current and historical state, canonical parents and descendants, blockers, Gates, Runs, and terminal reports without parsing generated Markdown

