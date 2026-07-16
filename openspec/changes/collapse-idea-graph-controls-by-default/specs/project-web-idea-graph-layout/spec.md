## MODIFIED Requirements

### Requirement: Idea Graph Owns Layout Controls
The Idea Graph SHALL provide a collapsible Graph Controls surface inside the owning Idea Graph panel for changing and previewing layout behavior. The Graph Controls surface SHALL be collapsed when the Idea Graph panel initially mounts.

#### Scenario: Idea Graph initially displays Graph Controls
- **WHEN** a user opens an Idea Graph
- **THEN** the Graph Controls summary is visible
- **AND** the Layout and Focus controls are collapsed by default

#### Scenario: User opens Graph Controls
- **WHEN** a user activates Graph Controls from the Idea Graph
- **THEN** the Idea Graph exposes its Layout and Focus controls inside that panel
- **AND** the React Flow canvas remains visible beside or beneath the controls according to available panel width

#### Scenario: User opens Project Settings
- **WHEN** a user opens the global Project Settings panel
- **THEN** Project Settings does not present Idea Graph layout algorithms, layout parameters, focus controls, or Graph Layout Preset management
