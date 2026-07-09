## MODIFIED Requirements

### Requirement: Initial Contract Coverage
The initial GUI contract set SHALL cover the read models currently needed by Project Web topic inspection flows.

#### Scenario: Topic overview contract is covered
- **WHEN** the topic overview panel consumes a topic overview response
- **THEN** a documented contract and Python schema SHALL cover `ok`, `mutated`, topic identity, overview source metadata, Markdown content availability, supporting JSON payloads, and diagnostics

#### Scenario: Graph view contract is covered
- **WHEN** the idea lineage or artifact graph panels consume a graph response
- **THEN** a documented contract and Python schema SHALL cover graph identity fields, nodes, edges, groups, facets, paging, diagnostics, and renderer hints needed by Project Web

#### Scenario: Idea detail contract is covered
- **WHEN** the idea detail panel consumes an idea detail response
- **THEN** a documented contract and Python schema SHALL cover idea identity, canonical idea metadata, realizations, source provenance, source JSON availability, lineage edges, generation groups, diagnostics, and optional exact source JSON

#### Scenario: Record inspection contracts are covered
- **WHEN** record tabs consume viewer descriptors, rendered record payloads, file lists, lineage, siblings, or facets
- **THEN** documented contracts and Python schemas SHALL cover the fields required to choose a viewer, open canonical detail, display rendered Markdown, display file openability, group raw JSON modal payloads, report diagnostics, and copy an absolute artifact filepath when available
- **AND** record detail contracts SHALL cover optional Topic Workspace-relative path, absolute artifact filepath, and direct parent idea metadata when those values can be derived from structured read-model data
