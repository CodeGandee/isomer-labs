## ADDED Requirements

### Requirement: Query Index Exposes Idea Source Fragment Status
The research record query index SHALL expose exact idea source-fragment status for canonical Research Ideas and Idea Realizations.

#### Scenario: Canonical idea export includes source status
- **WHEN** `isomer-cli ext research records query export` returns canonical ideas or idea graph data
- **THEN** each idea or realization summary includes source record id, source JSON path, source fragment status, source classification, payload digest when known, and diagnostics when the source fragment is missing, unresolved, broad, or non-object
- **AND** `source_fragment_status` uses `exact`, `missing_payload`, `missing_path`, `unresolved_path`, `broad_path`, `non_object`, or `legacy_fallback`
- **AND** `source_classification` uses `canonical_idea_source`, `record_context`, or `legacy_heuristic`

#### Scenario: Query index does not promote context notes
- **WHEN** a structured payload contains idea entries and context sections such as filter notes, rejection notes, route notes, or slate summaries
- **THEN** query-index facet extraction maps idea facets only from declared idea-bearing sections
- **AND** it does not expose context-only sections as canonical Primary Idea nodes

#### Scenario: Rebuild preserves canonical source truth
- **WHEN** the query index is rebuilt
- **THEN** it derives idea source status from canonical Workspace Runtime idea rows, Idea Realizations, managed payload files, and profile-aware mappings
- **AND** it does not infer authoritative idea source paths from generated Markdown bodies

### Requirement: Idea Graph Detail Refs Prefer Exact Idea Content
The topic graph read model SHALL route Primary Idea nodes to exact idea detail refs while keeping record refs as provenance.

#### Scenario: Primary idea node detail refs
- **WHEN** the backend returns an `idea-lineage` graph node for a canonical Primary Idea
- **THEN** the node includes an idea detail ref for the exact idea content read model
- **AND** source record refs remain available as latest record detail, rendered Markdown, or provenance refs

#### Scenario: Legacy fallback is diagnostic
- **WHEN** a topic has record idea facets but lacks canonical exact source-fragment metadata
- **THEN** the graph may return a legacy heuristic view
- **AND** it includes diagnostics that the idea source data requires import or repair before the GUI can show authoritative Primary Idea content
