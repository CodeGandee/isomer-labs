## ADDED Requirements

### Requirement: Project-Operator Launch Orchestration Boundary
The Houmao adapter SHALL launch or resolve Agent Team Instances only from approved Isomer profile bundle and runtime material and SHALL NOT perform topic-profile reasoning itself.

#### Scenario: Adapter consumes approved launch inputs
- **WHEN** a Project Operator Session or Operator Agent requests Houmao launch materialization for an Agent Team Instance
- **THEN** the adapter consumes the approved Topic Agent Team Profile Bundle, Agent Team Instance runtime record, Agent Instance records, Agent Workspace path plans, packet provenance refs, and Topic Service Agent support refs when present rather than inspecting a Domain Agent Team Template directly

#### Scenario: Adapter rejects template-only launch
- **WHEN** a launch request provides only a Domain Agent Team Template such as `deepsci-mini` without an approved Topic Agent Team Profile Bundle and Agent Team Instance record
- **THEN** the adapter rejects the request with an Isomer diagnostic and does not create Houmao launch material or live agents

#### Scenario: Adapter records project operator provenance
- **WHEN** Houmao launch material, quick launch, inspect-live, stop, or reconciliation is triggered by a Project Operator Session or Operator Agent
- **THEN** adapter command and payload records include bounded project operator actor or provenance refs without storing project-operator reasoning as adapter internals

### Requirement: Topic Service Agent Houmao Definition
The system SHALL provide a Houmao-compatible Topic Service Agent definition for topic-scoped Service Team work.

#### Scenario: Topic Service Agent can be launched or resolved
- **WHEN** a topic needs service support for environment readiness, topic-team instantiation, monitoring, or diagnostics
- **THEN** the Houmao adapter can launch or resolve a Topic Service Agent with the required Isomer Service Team skills and bounded Project/Topic context refs

#### Scenario: Topic Service Master posture is distinguishable
- **WHEN** one topic-scoped service actor coordinates multiple Service Requests or subordinate Service Agent Instances
- **THEN** Houmao definition material can represent a Topic Service Master posture or Agent Profile while preserving Service Team boundaries

#### Scenario: Topic Service Agent launch is separate from research team launch
- **WHEN** a Topic Service Agent supports launch or resolution of a `deepsci-mini` Agent Team Instance
- **THEN** adapter records distinguish the Topic Service Agent's managed-agent refs from the managed-agent refs for research team member Agent Instances
