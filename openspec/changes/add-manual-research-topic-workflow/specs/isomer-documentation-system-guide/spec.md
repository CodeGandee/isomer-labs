## ADDED Requirements

### Requirement: Canonical Domain Language Includes Topic Actor Workspace
The documentation system SHALL update canonical Isomer domain language so Topic Actor Workspace is a managed workspace type for human-orchestrated Topic Actors.

#### Scenario: Workspace taxonomy includes Topic Actor Workspaces
- **WHEN** canonical domain language describes Isomer-managed workspace types
- **THEN** it lists Topic Workspace, Agent Workspace, and Topic Actor Workspace as the managed workspace types
- **AND** it defines Topic Actor Workspace as the per-Topic Actor work area inside a Topic Workspace, separate from formal Agent Workspace identity

#### Scenario: Topic Actor Workspace remains separate from Agent Workspace
- **WHEN** documentation, schemas, CLI help, or skill prose describes manually controlled workers
- **THEN** it uses Topic Actor Workspace for their managed cwd surface
- **AND** it does not describe Topic Actor Workspaces as Agent Workspaces, Agent Instance ids, or Agent Team Instance membership
