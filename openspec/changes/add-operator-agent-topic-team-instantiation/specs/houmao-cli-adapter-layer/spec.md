## ADDED Requirements

### Requirement: Operator-Agent Launch Orchestration Boundary
The Houmao adapter SHALL launch or resolve Agent Team Instances only from approved Isomer profile/runtime material and SHALL NOT perform topic-profile reasoning itself.

#### Scenario: Adapter consumes approved launch inputs
- **WHEN** the Operator Agent requests Houmao launch materialization for an Agent Team Instance
- **THEN** the adapter consumes the approved Topic Agent Team Profile, Agent Team Instance runtime record, Agent Instance records, Agent Workspace path plans, and packet provenance refs rather than inspecting a Domain Agent Team Template directly

#### Scenario: Adapter rejects template-only launch
- **WHEN** a launch request provides only a Domain Agent Team Template such as `deepsci-mini` without an approved Topic Agent Team Profile and Agent Team Instance record
- **THEN** the adapter rejects the request with an Isomer diagnostic and does not create Houmao launch material or live agents

#### Scenario: Adapter records Operator Agent provenance
- **WHEN** Houmao launch material, quick launch, inspect-live, stop, or reconciliation is triggered by the Operator Agent
- **THEN** adapter command and payload records include bounded Operator Agent actor or provenance refs without storing Operator Agent reasoning as adapter internals

### Requirement: Operator Agent Houmao Definition
The system SHALL provide a Houmao-compatible Operator Agent definition for Isomer orchestration work.

#### Scenario: Operator Agent can be launched or resolved
- **WHEN** a project needs agent-mediated topic-team instantiation
- **THEN** the Houmao adapter can launch or resolve an Isomer Operator Agent with the required Isomer instantiation skills and project/topic context refs

#### Scenario: Operator Agent launch is separate from research team launch
- **WHEN** the Operator Agent launches or resolves a `deepsci-mini` Agent Team Instance
- **THEN** adapter records distinguish the Operator Agent's own managed-agent refs from the managed-agent refs for team member Agent Instances
