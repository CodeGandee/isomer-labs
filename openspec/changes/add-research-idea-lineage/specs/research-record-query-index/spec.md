## ADDED Requirements

### Requirement: Canonical Research Idea Query Export
The research record query index SHALL export canonical Research Idea data for GUI, CLI, and operator graph views.

#### Scenario: Topic export includes ideas
- **WHEN** a GUI or operator exports a Topic Workspace query view
- **THEN** the payload includes canonical Research Ideas, Idea Realizations, Idea Lineage Edges, Idea Generation Groups, diagnostics, and detail locators when canonical idea data exists

#### Scenario: Canonical idea rows are rebuildable
- **WHEN** an operator rebuilds the query index
- **THEN** canonical idea export rows are derived from Workspace Runtime Research Idea tables and not from generated Markdown prose

#### Scenario: Idea query is read-only
- **WHEN** a caller queries idea graph, idea detail, idea siblings, or idea realizations
- **THEN** the query reads Workspace Runtime or query-index rows without creating, repairing, or backfilling canonical idea data

#### Scenario: Stale status is diagnostic
- **WHEN** indexed experiment, analysis, claim, or decision records suggest that a Research Idea status may be stale
- **THEN** the query or graph response may include a diagnostic or suggested status change without mutating the canonical Research Idea

### Requirement: Extracted Idea Facets Are Fallback Metadata
The query index SHALL keep extracted `research_record_ideas` facets available for legacy inspection while preferring canonical Research Idea rows for idea-lineage graphs.

#### Scenario: Canonical ideas suppress duplicate facets in graph
- **WHEN** canonical Research Idea rows exist for a Topic Workspace
- **THEN** the idea-lineage graph uses canonical idea nodes and does not create duplicate primary nodes from extracted record idea facets with the same idea id or source phrase

#### Scenario: Legacy facets remain queryable
- **WHEN** a caller requests record facets for an individual record
- **THEN** extracted ideas, route decisions, metrics, claims, and facts remain available as record facets even if canonical Research Idea rows also exist

#### Scenario: Heuristic graph is diagnosed
- **WHEN** the graph backend falls back to extracted idea facets because canonical Research Idea rows are absent
- **THEN** the response includes diagnostics that the graph is heuristic and may lack authoritative idea lineage

### Requirement: Primary Idea Graph Projection
The topic graph read model SHALL project canonical primary Research Ideas and their canonical idea edges for the default `idea-lineage` view.

#### Scenario: Default graph shows primary ideas
- **WHEN** the GUI requests the default `idea-lineage` graph for a Topic Workspace with canonical idea data
- **THEN** the backend returns only primary Research Ideas, including raw time-parent ideas when marked primary, and canonical idea-level edges unless the request includes supporting or secondary material

#### Scenario: Expanded graph includes realizations
- **WHEN** the GUI requests supporting material or opens an idea detail tab
- **THEN** the backend can return supporting ideas, realization records, route decisions, claims, files, and record-lineage refs linked to the selected idea
