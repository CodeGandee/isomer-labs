## MODIFIED Requirements

### Requirement: Reading-List Discovery Preserves Search and Identity Evidence
Reading-list construction SHALL search across papers, technical reports, source-code repositories, datasets, and models while treating papers and technical reports as the primary works.

#### Scenario: Paper retrieval uses the centralized owner
- **WHEN** reading-list discovery needs paper identity resolution, paper query, citing-paper search, cited-paper exploration, citation-neighborhood traversal, or adjacent-paper search
- **THEN** the discover skill invokes `isomer-ext-kaoju-entrypoint->paper-search` with the direction, query or seed, bounds, expected normalized fields, and evidence-use intent
- **AND** repositories, datasets, models, selection, target counts, and cross-source-class coverage remain owned by discover and their existing owners

#### Scenario: Candidate records query provenance
- **WHEN** a provider query or reference traversal yields a candidate
- **THEN** the discovery ledger records query text or seed ref, provider or access method, query time, searched-through date, discovery route, source class, and selection disposition
- **AND** provider ranking, citation count, or recency alone does not establish inclusion or authority

#### Scenario: Versions are grouped without inflating coverage
- **WHEN** multiple versions, mirrors, preprints, reports, or repository releases represent one source family
- **THEN** the reading list records a canonical Source Identity and version-family relationship
- **AND** variants do not count as independent priority or secondary works unless the recorded rationale establishes materially distinct evidence

#### Scenario: User-supplied source receives priority review
- **WHEN** the actor supplies a source for the direction
- **THEN** the system gives it priority review and records its terminal disposition
- **AND** user nomination does not grant automatic inclusion, correctness, or evidentiary authority
