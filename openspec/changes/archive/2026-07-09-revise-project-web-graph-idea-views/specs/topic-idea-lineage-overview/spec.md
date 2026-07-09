## ADDED Requirements

### Requirement: Idea Relationship Graph Remains Separate
Project Web SHALL keep the idea relationship graph as a distinct graph-section view when adding timeline/table navigation.

#### Scenario: Idea graph remains relationship-focused
- **WHEN** a user opens the Idea Graph view
- **THEN** Project Web renders the relationship graph for Research Ideas using the idea-lineage graph semantics
- **AND** it does not replace the graph with the timeline table

#### Scenario: Timeline does not change graph node opening
- **WHEN** a user opens an idea from the Idea Graph view
- **THEN** Project Web uses the existing idea detail opening behavior for graph nodes
- **AND** adding the Idea Timeline view does not change graph hover, selection, or double-click behavior

#### Scenario: Graph and timeline can be open together
- **WHEN** a user opens both Idea Graph and Idea Timeline for the same Research Topic
- **THEN** Project Web treats them as separate workbench panels or restorable views
- **AND** refreshing, selecting, or opening from one view does not require closing the other view
