## ADDED Requirements

### Requirement: Idea Timeline Read Model
The Topic Graph read API SHALL provide or support a timeline-friendly read model for Research Ideas without introducing a separate canonical timeline store.

#### Scenario: Timeline read model includes idea rows
- **WHEN** Project Web requests data for the Idea Timeline view of a valid Research Topic
- **THEN** the response includes topic identity, index revision when available, generated timestamp, idea nodes or rows, idea lineage edges or parent refs, diagnostics, and `mutated: false`

#### Scenario: Timeline can derive parent indexes
- **WHEN** the timeline response includes parent-child idea relationships
- **THEN** the frontend has enough stable source and target idea identity to derive parent display indexes for the current sorted table

#### Scenario: Timeline read model uses existing idea semantics
- **WHEN** the backend builds the timeline read model
- **THEN** it uses canonical Research Ideas, Idea Realizations, and Idea Lineage Edges when available
- **AND** it preserves existing legacy fallback diagnostics when canonical Research Ideas are absent

#### Scenario: Timeline request is read-only
- **WHEN** Project Web requests the Idea Timeline read model
- **THEN** the backend does not rebuild, repair, cleanup, migrate, backfill, or write Workspace Runtime records or query-index rows

### Requirement: Visible Graph Scope Metadata Favors Idea Views
The Topic Graph read API SHALL expose enough graph/view metadata for Project Web to distinguish the visible Idea Graph and Idea Timeline views.

#### Scenario: Idea graph metadata is available
- **WHEN** Project Web opens the Idea Graph view
- **THEN** the read model identifies the relationship graph view and preserves the `idea-lineage` semantics used by existing graph rendering

#### Scenario: Idea timeline metadata is available
- **WHEN** Project Web opens the Idea Timeline view
- **THEN** the read model or openable descriptor identifies the timeline/table presentation separately from the relationship graph presentation
