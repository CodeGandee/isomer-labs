## ADDED Requirements

### Requirement: Agent Team Instance Instantiation Provenance
The system SHALL record the approved Operator Agent instantiation source when creating Agent Team Instance runtime records.

#### Scenario: Team instance links packet and profile
- **WHEN** an Agent Team Instance is created from a Topic Agent Team Profile materialized by an Operator Agent packet
- **THEN** Workspace Runtime records or links the Agent Team Instance to the Topic Agent Team Profile ref, packet ref, approval ref, Operator Agent actor ref, and validation result provenance

#### Scenario: Runtime creation rejects unapproved packet
- **WHEN** a launch-facing Agent Team Instance creation request references an Operator Agent packet that is missing, invalid, rejected, or unapproved
- **THEN** Workspace Runtime rejects the create request and leaves existing runtime records unchanged

#### Scenario: Preview profile remains non-launching
- **WHEN** a Topic Agent Team Profile only has preview provenance and no approved Operator Agent packet or equivalent explicit approval
- **THEN** launch-facing Agent Team Instance creation reports a diagnostic rather than silently treating synthetic preview defaults as authoritative

### Requirement: Operator Agent Runtime Actor Records
The system SHALL represent the Isomer Operator Agent as an actor that can author packets, approvals, runtime records, and orchestration requests.

#### Scenario: Operator Agent actor is recorded
- **WHEN** the Operator Agent materializes a profile, creates or launches an Agent Team Instance, dispatches handoffs, or records task routing decisions
- **THEN** runtime records include an Operator Agent actor ref or provenance ref distinct from team member Agent Instances and Service Agent Instances

#### Scenario: Operator Agent is not a team member by default
- **WHEN** an Agent Team Instance is created from a Topic Agent Team Profile
- **THEN** Workspace Runtime does not add the Operator Agent as a member Agent Instance unless the profile explicitly defines an operator role inside that team
