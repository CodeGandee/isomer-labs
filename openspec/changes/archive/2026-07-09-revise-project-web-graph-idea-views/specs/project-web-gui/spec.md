## ADDED Requirements

### Requirement: Graphs Navigation Is Idea-led
Project Web SHALL make the visible Research Topic `Graphs` navigation focus on Research Idea progress views.

#### Scenario: Graphs exposes idea views
- **WHEN** a user expands a Research Topic in the Project Explorer
- **THEN** the `Graphs` section shows openable views for Idea Graph and Idea Timeline
- **AND** both views target the selected Research Topic

#### Scenario: Dense non-idea graph sections are hidden
- **WHEN** a user expands the `Graphs` section
- **THEN** Project Web does not show `Artifact Overview`, `Experiment Records`, or `Paper Revisions` as visible graph entries

#### Scenario: Removed dense graph URLs do not restore views
- **WHEN** a user opens an old Project Web URL for `artifact-overview`, `experiment-records`, or `paper-revisions`
- **THEN** Project Web does not render the removed dense graph view
- **AND** it reports or routes through unsupported graph-scope behavior

#### Scenario: Idea graph opens relationship view
- **WHEN** a user opens the Idea Graph view
- **THEN** Project Web opens the existing idea relationship graph backed by the `idea-lineage` read model

#### Scenario: Idea timeline opens table view
- **WHEN** a user opens the Idea Timeline view
- **THEN** Project Web opens a table-oriented view of Research Ideas for the same selected Research Topic

### Requirement: Graph View History Uses Idea View Identity
Project Web SHALL keep browser history and workbench openable identity stable for separate Idea Graph and Idea Timeline views.

#### Scenario: Idea graph URL is stable
- **WHEN** a user opens the Idea Graph view for a Research Topic
- **THEN** browser history records a stable graph/view state that can restore that idea relationship view

#### Scenario: Idea timeline URL is stable
- **WHEN** a user opens the Idea Timeline view for a Research Topic
- **THEN** browser history records a stable graph/view state that can restore that timeline table view
