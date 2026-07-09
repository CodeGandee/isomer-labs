## MODIFIED Requirements

### Requirement: Welcome Skill Stays Read-Only by Default
The `isomer-op-welcome` skill SHALL be read-only by default and SHALL NOT perform owner workflow mutation from the welcome surface.

#### Scenario: Welcome option selection does not mutate state
- **WHEN** a user asks the welcome skill what path to choose
- **THEN** the skill may recommend an owner skill and safe first command
- **AND** it does not initialize Projects, create Research Topics, mutate Topic Workspaces, install packages, specialize teams, launch agents, or bootstrap research-paradigm v2 artifacts

#### Scenario: Context-aware next step uses read-only inspection
- **WHEN** the user asks for a context-aware next step and a Project context is available
- **THEN** the skill may use read-only commands such as `isomer-cli project validate`, `isomer-cli doctor`, `isomer-cli project topics list`, or `isomer-cli project context show`
- **AND** it reports blockers and the recommended owner workflow without running mutating commands
