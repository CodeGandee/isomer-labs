## ADDED Requirements

### Requirement: Canonical Lineage Projection
The research record query index SHALL project canonical artifact lineage into graph and lineage read models.

#### Scenario: Rebuild projects lineage edges
- **WHEN** query-index rebuild runs for a Topic Workspace
- **THEN** it reads canonical artifact lineage edges and projects them into exported graph and lineage views with source classification that identifies canonical lineage

#### Scenario: Query export distinguishes lineage
- **WHEN** query export returns graph edges
- **THEN** each edge identifies whether it came from canonical artifact lineage, authored relationship metadata, payload-derived refs, file-derived refs, or body inference

#### Scenario: Missing canonical lineage is diagnostic
- **WHEN** an artifact profile normally expects canonical lineage but no canonical lineage exists
- **THEN** query export reports a diagnostic or missing-lineage hint instead of fabricating parents from prose

### Requirement: Query Lineage Uses Canonical DAG
The record lineage query SHALL prefer canonical artifact lineage for ancestor, descendant, and sibling traversal.

#### Scenario: Ancestor traversal uses lineage table
- **WHEN** a caller runs a lineage query for ancestors
- **THEN** the command traverses canonical parent-child lineage before adding non-canonical relationship context

#### Scenario: Descendant traversal uses lineage table
- **WHEN** a caller runs a lineage query for descendants
- **THEN** the command traverses canonical child relationships before adding non-canonical relationship context

#### Scenario: Sibling traversal uses generation groups
- **WHEN** a caller runs a sibling or idea-iteration query
- **THEN** the command derives siblings from generation groups and parent-set identity rather than pairwise inferred sibling edges

### Requirement: Lineage Relation Vocabulary
The query index SHALL expose canonical lineage kinds in a stable vocabulary.

#### Scenario: Canonical lineage kinds are exported
- **WHEN** query export or lineage query returns canonical artifact lineage
- **THEN** it can expose `derived_from`, `revision_of`, `selected_from`, `merged_from`, and `follow_up_to` as lineage kinds or relation kinds

#### Scenario: Custom relationship extensions remain supported
- **WHEN** a non-canonical relationship uses a `custom.*` relation kind
- **THEN** the query index accepts it as an extension without confusing it with canonical artifact lineage
