## ADDED Requirements

### Requirement: Idea Graph Display Key Payloads
The topic graph read API SHALL include Research Idea display keys in graph node payloads using the `I-<index>` format.

#### Scenario: Idea node includes display key
- **WHEN** the graph API returns a node for a canonical Research Idea with a display key
- **THEN** the node includes `display_key` in the `I-<index>` format
- **AND** the value matches the corresponding Workspace Runtime Research Idea row

#### Scenario: Missing display key is diagnostic data
- **WHEN** a graph node represents an old Research Idea without a display key
- **THEN** the graph API keeps returning a safe graph payload
- **AND** diagnostics or recent-errors data can report that explicit display-key repair is needed

### Requirement: Idea Graph Visible Labels Use Display Keys
The Project Web Idea Graph SHALL use display keys as the leading short identity in visible node labels when display keys are available.

#### Scenario: React Flow node label includes key
- **WHEN** an Idea Graph node has `display_key: "I-3"` and title `Precision model`
- **THEN** the visible node label begins with `I-3`
- **AND** the title remains visible in the same label

#### Scenario: Graph label falls back safely
- **WHEN** an Idea Graph node has no display key
- **THEN** the visible label falls back to the existing title or idea id behavior
- **AND** the graph does not crash
