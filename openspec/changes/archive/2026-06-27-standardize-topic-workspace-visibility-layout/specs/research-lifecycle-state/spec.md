## MODIFIED Requirements

### Requirement: Persisted Agent Instance and Agent Workspace State
The system SHALL persist Agent Instance and Agent Workspace lifecycle records in Workspace Runtime when an Agent Team Instance record is instantiated, including the mapping between runtime Agent Instance ids and topic-local agent names.

#### Scenario: Agent Instance record belongs to one team instance
- **WHEN** an Agent Instance record is created for a Topic Agent Team Profile role binding
- **THEN** it references exactly one Agent Team Instance, Agent Role, Topic Workspace, Research Topic, optional Agent Profile ref, status, and Provenance Record refs when known

#### Scenario: Agent Workspace record belongs to one agent instance
- **WHEN** an Agent Workspace record is created
- **THEN** it references exactly one Agent Instance, Topic Workspace, topic-local agent name, path plan, workspace boundary refs when known, status, and Provenance Record refs when known

#### Scenario: Agent Workspace record carries worktree refs
- **WHEN** an Agent Workspace record represents a standard worker workspace
- **THEN** it records or links the expected Git repository ref, branch namespace, current branch when known, and `.isomer-agent/` support boundary without treating those refs as Agent Instance identity

#### Scenario: Agent Instance status is explicit
- **WHEN** an Agent Instance lifecycle record is inspected
- **THEN** its status is one of `planned`, `active`, `paused`, `blocked`, `completed`, `stopped`, `failed`, or `archived`, or a later accepted contract has explicitly extended the status set

#### Scenario: Agent Workspace status is explicit
- **WHEN** an Agent Workspace lifecycle record is inspected
- **THEN** its status is one of `planned`, `ready`, `active`, `missing`, `stale`, `archived`, or `invalid`, or a later accepted contract has explicitly extended the status set

#### Scenario: Agent name is not global identity
- **WHEN** two different Topic Workspaces use the same topic-local agent name such as `alice`
- **THEN** lifecycle validation allows the names because Agent Instance ids remain globally unique and Agent Workspace records remain Topic Workspace scoped
