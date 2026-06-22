## ADDED Requirements

### Requirement: Persisted Agent Instance and Agent Workspace State
The system SHALL persist Agent Instance and Agent Workspace lifecycle records in Workspace Runtime when an Agent Team Instance record is instantiated.

#### Scenario: Agent Instance record belongs to one team instance
- **WHEN** an Agent Instance record is created for a Topic Agent Team Profile role binding
- **THEN** it references exactly one Agent Team Instance, Agent Role, Topic Workspace, Research Topic, optional Agent Profile ref, status, and Provenance Record refs when known

#### Scenario: Agent Workspace record belongs to one agent instance
- **WHEN** an Agent Workspace record is created
- **THEN** it references exactly one Agent Instance, Topic Workspace, path plan, workspace boundary refs when known, status, and Provenance Record refs when known

#### Scenario: Agent Instance status is explicit
- **WHEN** an Agent Instance lifecycle record is inspected
- **THEN** its status is one of `planned`, `active`, `paused`, `blocked`, `completed`, `stopped`, `failed`, or `archived`, or a later accepted contract has explicitly extended the status set

#### Scenario: Agent Workspace status is explicit
- **WHEN** an Agent Workspace lifecycle record is inspected
- **THEN** its status is one of `planned`, `ready`, `active`, `missing`, `stale`, `archived`, or `invalid`, or a later accepted contract has explicitly extended the status set

### Requirement: Handoff State Records
The system SHALL persist handoff state as Workspace Runtime records that support Operator Agent normalization and stale-handoff validation.

#### Scenario: Handoff records route delegated work
- **WHEN** the Operator Agent delegates work to an Agent Instance or Service Agent Instance
- **THEN** the system records a handoff state with source actor ref, target actor ref, Research Task or Run ref, Agent Team Instance ref when applicable, status, expected output refs, Completion Watcher Contract refs, created timestamp, and Provenance Record refs when known

#### Scenario: Handoff status is explicit
- **WHEN** a handoff state record is inspected
- **THEN** its status is one of `planned`, `sent`, `observing`, `candidate_complete`, `accepted`, `rejected`, `stale`, `cancelled`, or `superseded`, or a later accepted contract has explicitly extended the status set

#### Scenario: Signal observations do not complete handoff alone
- **WHEN** file observation, channel reply, Agent Instance inspection, or adapter event signals possible completion
- **THEN** the system records the observation without marking the handoff accepted until the Operator Agent records the normalized handoff result

### Requirement: Restart-safe Agent Team Instance State
The system SHALL recover Agent Team Instance, Agent Instance, Agent Workspace, Run, Workflow Stage Cursor, and handoff state from Workspace Runtime after process restart.

#### Scenario: Team instance can be reopened
- **WHEN** a Workspace Runtime is reopened after process restart
- **THEN** the system can inspect each Agent Team Instance with its Agent Instance refs, Agent Workspace refs, status, active Run refs when known, Workflow Stage Cursor refs, blocker refs, and handoff refs

#### Scenario: Runtime recovery preserves terminal records
- **WHEN** an Agent Team Instance, Agent Instance, Agent Workspace, Run, or handoff is stopped, failed, stale, archived, cancelled, or superseded
- **THEN** recovery keeps the terminal record visible for audit, repair, reuse, or provenance instead of deleting it silently

#### Scenario: Team instance context stays topic scoped
- **WHEN** an Agent Team Instance is recovered
- **THEN** validation confirms that its Research Topic, Topic Workspace, Topic Agent Team Profile, Agent Instance, Agent Workspace, and Run refs belong to the same Topic Workspace unless an explicit future cross-topic relation contract permits otherwise
