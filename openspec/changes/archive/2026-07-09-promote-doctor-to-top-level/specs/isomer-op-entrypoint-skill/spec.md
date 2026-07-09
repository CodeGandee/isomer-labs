## MODIFIED Requirements

### Requirement: Entrypoint Includes CLI Surface Routing
The entrypoint SHALL include concise routing guidance for Isomer CLI command families without duplicating full CLI help.

#### Scenario: Read-only context discovery commands are named
- **WHEN** entrypoint CLI guidance is inspected
- **THEN** it names safe context discovery surfaces such as `isomer-cli project self queries`, `isomer-cli project self show`, `isomer-cli project validate`, `isomer-cli doctor`, `isomer-cli project topics list`, `isomer-cli project context show`, and Workspace Path Resolution commands

#### Scenario: Topic-owned record commands are named
- **WHEN** entrypoint CLI guidance is inspected
- **THEN** it routes structured research record create, list, show, update, delete, validate, render, query, index, and cleanup needs to `isomer-cli ext research records ...`
- **AND** it does not instruct agents to hand-edit record indexes

#### Scenario: Specialized CLI families are discoverable
- **WHEN** entrypoint CLI guidance is inspected
- **THEN** it mentions artifact-format processing, topic reset checkpoints, runtime, handoffs, team templates, team profiles, team instances, topic actors, topic-main guidance, paths, repositories, and outputs policy command families as CLI surfaces to inspect when the user task matches them
