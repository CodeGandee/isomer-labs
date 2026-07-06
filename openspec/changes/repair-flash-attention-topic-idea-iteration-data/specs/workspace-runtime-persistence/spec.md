## ADDED Requirements

### Requirement: Topic Fixture Runtime Repair Integrity
Workspace Runtime persistence SHALL support explicit fixture-quality repair of a topic-owned runtime database without corrupting canonical runtime state.

#### Scenario: Repair uses canonical runtime tables
- **WHEN** a topic fixture repair adds or updates lineage, generation groups, lifecycle records, structured payload refs, or statuses
- **THEN** the repaired data is stored in the current canonical Workspace Runtime tables for the selected Topic Workspace and preserves matching Research Topic and Topic Workspace refs

#### Scenario: Repair preserves history
- **WHEN** historical topic records are superseded, revised, or made obsolete by the repair
- **THEN** the prior records remain inspectable as archived or historical records unless an explicit cleanup task removes only derived query-index rows

#### Scenario: Repair can be rolled back
- **WHEN** the operator needs to undo a fixture repair
- **THEN** restoring the pre-repair `state.sqlite` snapshot and removing newly created topic-owned payload folders returns the Topic Workspace to its prior runtime state

### Requirement: Generation Group Runtime Consistency
Workspace Runtime persistence SHALL keep repaired generation groups consistent with their lineage edges.

#### Scenario: Generation group parent set is stable
- **WHEN** repaired lineage edges share a generation id
- **THEN** the corresponding generation group records the same Topic Workspace, a purpose, a deterministic parent-set digest for the shared parent records, and optional decision or producer metadata

#### Scenario: Generation group refs are valid
- **WHEN** runtime or lineage validation inspects repaired generation groups
- **THEN** every generation id referenced by a lineage edge resolves to an existing generation group in the same Topic Workspace

#### Scenario: Missing generation groups are not hidden
- **WHEN** a lineage edge references a missing generation group after repair
- **THEN** validation reports the issue rather than silently creating, deleting, or ignoring the group during read-only inspection
