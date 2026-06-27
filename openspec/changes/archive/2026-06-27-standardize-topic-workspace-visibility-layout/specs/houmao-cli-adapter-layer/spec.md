## MODIFIED Requirements

### Requirement: Project-Operator Launch Orchestration Boundary
The Houmao adapter SHALL launch or resolve Agent Team Instances only from approved Isomer profile bundle and runtime material and SHALL NOT perform topic-profile reasoning itself.

#### Scenario: Adapter consumes approved launch inputs
- **WHEN** a Project Operator Session or Operator Agent requests Houmao launch materialization for an Agent Team Instance
- **THEN** the adapter consumes the approved Topic Agent Team Profile Bundle, Agent Team Instance runtime record, Agent Instance records, Agent Workspace path plans, topic-local agent names, packet provenance refs, and Topic Service Agent support refs when present rather than inspecting a Domain Agent Team Template directly

#### Scenario: Adapter launches from Agent Workspace cwd
- **WHEN** the adapter launches or prepares one mapped Houmao managed agent for an Isomer Agent Instance
- **THEN** it uses the recorded `<topic-workspace>/agents/<agent-name>` worktree as the command cwd for that mapped worker agent

#### Scenario: Adapter rejects template-only launch
- **WHEN** a launch request provides only a Domain Agent Team Template such as `deepsci-mini` without an approved Topic Agent Team Profile Bundle and Agent Team Instance record
- **THEN** the adapter rejects the request with an Isomer diagnostic and does not create Houmao launch material or live agents

#### Scenario: Adapter records project operator provenance
- **WHEN** Houmao launch material, quick launch, inspect-live, stop, or reconciliation is triggered by a Project Operator Session or Operator Agent
- **THEN** adapter command and payload records include bounded project operator actor or provenance refs without storing project-operator reasoning as adapter internals

## ADDED Requirements

### Requirement: Houmao Adapter Workspace Visibility
The Houmao adapter SHALL keep generated adapter material out of worker-visible Git surfaces unless an explicit publication workflow promotes selected output.

#### Scenario: Adapter payloads stay in runtime or records
- **WHEN** the adapter writes command payloads, launch logs, generated Houmao profile material, inspection snapshots, stop outcomes, or reconciliation material
- **THEN** those files resolve under recorded `runtime/`, `runtime/adapters/houmao/`, or `records/*` path plans rather than under `repos/topic-main` or worker branches by default

#### Scenario: Worker-published material is explicit
- **WHEN** adapter output needs to become visible to worker agents through Git
- **THEN** the adapter or Operator Agent publishes a bounded summary or artifact into `repos/topic-main` through an explicit workflow and records provenance for the publication

#### Scenario: Agent cwd does not imply root access
- **WHEN** a managed agent process is launched with cwd set to `agents/<agent-name>`
- **THEN** the adapter does not instruct the worker to browse root `records/`, `runtime/`, or `state.sqlite` as normal input
