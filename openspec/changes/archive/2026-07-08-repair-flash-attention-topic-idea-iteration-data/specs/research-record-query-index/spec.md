## ADDED Requirements

### Requirement: Idea Iteration Fixture Export Integrity
The research record query index SHALL expose repaired fixture data for idea iteration views without requiring read-time repair or topic-specific GUI filtering.

#### Scenario: Repaired topic idea export is diagnostic-clean
- **WHEN** a caller exports the repaired Flash Attention topic with the `ideas` view
- **THEN** the export returns topic-scoped nodes, canonical-lineage edges, idea facets, route rows, metrics, claims, facts, and files with no missing-record, stale-index, unsupported-relation, or missing-file integrity diagnostics

#### Scenario: Repaired idea facets are stable enough for GUI grouping
- **WHEN** the export contains raw idea facets, serious candidate records, selected hypothesis records, and follow-up hypothesis records
- **THEN** each idea-like item has enough stable fields for the GUI read model to group by source record, idea id or hypothesis id, family, one-liner or title, status, and lineage role

#### Scenario: Historical extractor duplicates are not authoritative siblings
- **WHEN** an array-valued historical payload causes duplicate raw idea facet rows
- **THEN** the query data still includes stable ids and source JSON paths that allow the backend read model to deduplicate presentation nodes without treating duplicate rows as sibling alternatives

### Requirement: Fixture Relationship Projection
The query index SHALL project repaired canonical lineage and authored relationship metadata so the idea iteration map can distinguish relationship meaning.

#### Scenario: Canonical lineage is projected
- **WHEN** repaired records have canonical lineage edges or generation groups
- **THEN** query export and lineage queries expose relation kind, relation role, source and target record ids, rationale when known, source classification, and canonical edge ids

#### Scenario: Route and evidence context remain queryable
- **WHEN** a repaired idea node is connected to route decisions, experiment results, analysis summaries, claims, or metrics
- **THEN** facets and export output include the relevant route rows, evidence links, claims, metrics, and scalar facts needed for the GUI detail panel

#### Scenario: Test and archived records do not pollute fixture diagnostics
- **WHEN** historical test or archived records remain in the topic runtime
- **THEN** they are either indexed consistently as archived records or excluded by explicit status/facet filtering without producing query-index integrity diagnostics
