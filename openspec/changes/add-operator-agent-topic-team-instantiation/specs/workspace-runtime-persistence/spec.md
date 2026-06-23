## ADDED Requirements

### Requirement: Agent Team Instance Instantiation Provenance
The system SHALL record the approved instantiation source when creating Agent Team Instance runtime records.

#### Scenario: Team instance links packet and profile
- **WHEN** an Agent Team Instance is created from a Topic Agent Team Profile materialized by an approved instantiation packet
- **THEN** Workspace Runtime records or links the Agent Team Instance to the Topic Agent Team Profile ref, packet ref, approval ref, project operator actor or session ref, Topic Service Agent refs when used, and validation result provenance

#### Scenario: Runtime creation rejects unapproved packet
- **WHEN** a launch-facing Agent Team Instance creation request references an instantiation packet that is missing, invalid, rejected, or unapproved
- **THEN** Workspace Runtime rejects the create request and leaves existing runtime records unchanged

#### Scenario: Preview profile remains non-launching
- **WHEN** a Topic Agent Team Profile only has preview provenance and no approved instantiation packet or equivalent explicit approval
- **THEN** launch-facing Agent Team Instance creation reports a diagnostic rather than silently treating synthetic preview defaults as authoritative

### Requirement: Project Operator and Topic Service Runtime Actor Records
The system SHALL represent project operator provenance and Topic Service Agent provenance distinctly from research team membership.

#### Scenario: Project operator actor or session is recorded
- **WHEN** a Project Operator Session or Operator Agent materializes a profile, creates or launches an Agent Team Instance, dispatches handoffs, dispatches Service Requests, or records task routing decisions
- **THEN** runtime records include project operator actor or session provenance distinct from team member Agent Instances and Service Agent Instances

#### Scenario: Topic Service Agent support is recorded
- **WHEN** a Topic Service Agent supports profile materialization, environment setup, diagnostics, monitoring, or launch preparation
- **THEN** Workspace Runtime or linked support metadata records the Service Request ref, Topic Service Agent ref, support Artifacts, and Provenance Records

#### Scenario: Operators and service agents are not team members by default
- **WHEN** an Agent Team Instance is created from a Topic Agent Team Profile
- **THEN** Workspace Runtime does not add the Project Operator Session, Operator Agent, or Topic Service Agent as a member Agent Instance unless the profile explicitly defines a corresponding operator role inside that research team
