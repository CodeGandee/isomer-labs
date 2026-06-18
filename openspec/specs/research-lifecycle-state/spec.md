# research-lifecycle-state Specification

## Purpose
Define Isomer Labs research lifecycle state for Research Topics, Research Inquiries, Research Tasks, Runs, Workflow Stage Cursors, Research Inquiry Relationships, Agent Team Instance lifecycle state, and validation boundaries.

## Requirements
### Requirement: Research Execution Levels
The system SHALL define Research Topic, Research Inquiry, Research Task, and Run as distinct research execution levels with explicit ownership relationships.

#### Scenario: Research Topic initiates work
- **WHEN** research work is started from a root question, problem, anomaly, objective, or user request
- **THEN** the system records a Research Topic with a stable id, topic statement, optional Measurable Objective, Topic Workspace ref, status, actor refs, and Provenance Record refs

#### Scenario: Research Topic can be exploratory and measurable
- **WHEN** a Research Topic contains a Measurable Objective
- **THEN** the system still allows the topic to remain exploratory and does not treat measurable and exploratory as mutually exclusive topic modes

#### Scenario: Research Inquiry represents a question
- **WHEN** the user or an agent decomposes or generates a question to work out a Research Topic
- **THEN** the system records a Research Inquiry with a stable id, Research Topic ref, question statement, scope notes, status, source refs, and Provenance Record refs

#### Scenario: Research Task represents concrete work
- **WHEN** the user or an agent identifies a development, experiment, analysis, writing, review, validation, or setup action needed to answer a Research Inquiry
- **THEN** the system records a Research Task with a stable id, Research Inquiry ref, task statement, expected output refs or Artifact kinds, status, assigned Agent Team Instance or Agent Instance refs when known, and Provenance Record refs

#### Scenario: Run represents one bounded work pass
- **WHEN** an Agent Instance, Execution Adapter, Operator Agent, or approved service performs a bounded attempt for a Research Task
- **THEN** the system records a Run with a stable id, Research Task ref, actor refs, status, started and ended timestamps when known, output refs, Evidence Item refs when produced, and Provenance Record refs

### Requirement: Lifecycle Status and Transitions
The system SHALL use explicit lifecycle statuses for Research Topics, Research Inquiries, Research Tasks, Runs, Workflow Stage Cursors, and Agent Team Instance lifecycle state.

#### Scenario: Research Topic status is explicit
- **WHEN** a Research Topic is inspected
- **THEN** its status is one of `open`, `active`, `paused`, `blocked`, `finalized`, or `archived`, or a later accepted contract has explicitly extended the status set

#### Scenario: Research Inquiry status is explicit
- **WHEN** a Research Inquiry is inspected
- **THEN** its status is one of `open`, `active`, `answered`, `blocked`, `superseded`, or `withdrawn`, or a later accepted contract has explicitly extended the status set

#### Scenario: Research Task status is explicit
- **WHEN** a Research Task is inspected
- **THEN** its status is one of `planned`, `ready`, `active`, `blocked`, `completed`, `failed`, `cancelled`, or `superseded`, or a later accepted contract has explicitly extended the status set

#### Scenario: Run status is explicit
- **WHEN** a Run is inspected
- **THEN** its status is one of `planned`, `running`, `succeeded`, `failed`, `cancelled`, or `stale`, or a later accepted contract has explicitly extended the status set

#### Scenario: Status transition is recorded
- **WHEN** a lifecycle object changes status
- **THEN** the system records actor, timestamp, previous status, next status, rationale, and Decision Record, Gate, Evidence Item, Finding, or Provenance Record refs when applicable

#### Scenario: Terminal work can remain visible
- **WHEN** a Research Inquiry, Research Task, Run, or Agent Team Instance is superseded, withdrawn, cancelled, failed, stopped, stale, finalized, or archived
- **THEN** the system keeps the lifecycle object visible for provenance, audit, repair, reuse, or contradiction analysis instead of deleting it silently

### Requirement: Research Inquiry Relationships
The system SHALL represent relationships between Research Inquiries as durable graph relations rather than tree branches.

#### Scenario: Inquiry relationship is recorded
- **WHEN** one Research Inquiry decomposes, follows up, contrasts with, narrows, broadens, supersedes, duplicates, depends on, or otherwise relates to another Research Inquiry
- **THEN** the system records a Research Inquiry Relationship with source inquiry ref, target inquiry ref, relation type, rationale, status, supporting Finding, Evidence Item, Artifact, or Decision Record refs when known, and Provenance Record refs

#### Scenario: Topic can generate inquiry
- **WHEN** a Research Inquiry is created directly from a Research Topic before a parent Research Inquiry exists
- **THEN** the system records the topic-to-inquiry origin without inventing a parent inquiry

#### Scenario: Inquiry relationships do not force a tree
- **WHEN** Research Inquiries are cross-linked, merged, reopened, superseded, or reused across multiple paths
- **THEN** the system preserves the relationship graph and does not require the inquiries to form a single tree, branch collection, or exclusive parent-child hierarchy

#### Scenario: Meaningful route choice creates Decision Record
- **WHEN** the user, Operator Agent, or Agent Team Instance chooses among materially different Research Inquiry Relationships or route directions
- **THEN** the system records a Decision Record with selected relation or route, rejected alternatives when material, rationale, evidence refs, and consequences

#### Scenario: Ordinary decomposition can avoid Decision Record
- **WHEN** an agent creates a straightforward Research Inquiry Relationship that does not choose among material alternatives or govern a risky action
- **THEN** the system may record the relationship and Provenance Record without requiring a Decision Record

### Requirement: Workflow Stage Cursor
The system SHALL define Workflow Stage Cursor as durable routing state for research workflow progress, not as a scheduler command.

#### Scenario: Stage cursor records current stage
- **WHEN** a Research Topic, Research Inquiry, Research Task, Run, or Agent Team Instance has an active or recommended workflow stage
- **THEN** the system records a Workflow Stage Cursor with owner ref, stage name, status, rationale, updated timestamp, actor refs, blocker refs when present, next recommended stage when known, and Decision Record or Provenance Record refs

#### Scenario: Stage cursor status is explicit
- **WHEN** a Workflow Stage Cursor is inspected
- **THEN** its status is one of `active`, `recommended`, `blocked`, `paused`, `completed`, or `superseded`, or a later accepted contract has explicitly extended the status set

#### Scenario: Stage cursor does not schedule work
- **WHEN** a Workflow Stage Cursor recommends a next stage, pause, blocker, or handoff
- **THEN** the system treats it as durable routing state and does not infer queueing, auto-continue, retry, resource allocation, or command execution behavior from it

#### Scenario: Stage cursor can point to settled recording objects
- **WHEN** a Workflow Stage Cursor is based on evidence, finding reuse, a route decision, a gate, or a blocker
- **THEN** it references accepted Evidence Items, Findings, Decision Records, Gates, Artifacts, or Provenance Records instead of embedding unsupported freeform state

### Requirement: Agent Team Instance Lifecycle State
The system SHALL define Agent Team Instance lifecycle state without defining Skill Binding, Capability Binding, credential binding, or command execution details.

#### Scenario: Agent Team Instance state is recorded
- **WHEN** an Agent Team Instance is created or inspected for research work
- **THEN** the system records a stable id, Research Topic ref, optional active or relevant Research Inquiry refs, optional Research Task ref, Topic Workspace ref, participating Agent Instance refs when known, Agent Workspace refs when known, Workflow Stage Cursor refs, status, blocker refs, and Provenance Record refs

#### Scenario: Agent Team Instance inquiry refs are context
- **WHEN** Agent Team Instance lifecycle state records active or relevant Research Inquiry refs
- **THEN** the system treats those refs as context and routing anchors and does not use them to assign parallel execution scope, scheduling authority, or execution ownership to the Research Inquiry

#### Scenario: Agent Team Instance status is explicit
- **WHEN** an Agent Team Instance lifecycle state is inspected
- **THEN** its status is one of `planned`, `active`, `paused`, `blocked`, `completed`, `stopped`, or `archived`, or a later accepted contract has explicitly extended the status set

#### Scenario: Topic-level parallel execution is allowed
- **WHEN** multiple Agent Team Instances work under the same Research Topic
- **THEN** the system records distinct Agent Team Instance lifecycle states and their active Research Inquiry, Research Task, Run, and Workflow Stage Cursor refs without requiring a single shared execution branch

#### Scenario: Task-level parallel execution is allowed
- **WHEN** multiple Agent Instances inside one Agent Team Instance distribute work for a Research Task
- **THEN** the system records the participating Agent Instance refs, task refs, run refs, output refs, and provenance needed to distinguish the distributed work

#### Scenario: Research Inquiry is not a parallel execution scope
- **WHEN** an agent needs to express parallel work related to a Research Inquiry
- **THEN** the system represents that parallelism through Topic-level Agent Team Instances or Task-level Agent Instances rather than by assigning parallel execution state to the Research Inquiry itself

#### Scenario: Agent Team Instance state does not define bindings
- **WHEN** Agent Team Instance lifecycle state references Agent Instances, roles, skills, tools, credentials, or providers
- **THEN** the system treats those refs as lifecycle context and does not define Skill Binding, Capability Binding, credential binding, or provider binding schemas in this contract

### Requirement: Lifecycle Validation
The system SHALL validate lifecycle refs, stale vocabulary, and resolved lifecycle TBD placeholders.

#### Scenario: Broken lifecycle ref is reported
- **WHEN** a Research Inquiry, Research Task, Run, Workflow Stage Cursor, Research Inquiry Relationship, or Agent Team Instance points to a missing lifecycle object
- **THEN** validation reports the broken ref and identifies the referring lifecycle object

#### Scenario: Invalid lifecycle transition is reported
- **WHEN** a lifecycle object changes status without actor, timestamp, previous status, next status, or rationale
- **THEN** validation reports the transition as incomplete

#### Scenario: Stale lifecycle term is reported
- **WHEN** active research-paradigm skill text uses Research Goal, Research Thread, Research Branch, or Isomer Workspace as current domain terms
- **THEN** validation reports the stale term unless the occurrence is confined to provenance, migration notes, or explicit source-term mapping

#### Scenario: Resolved lifecycle placeholders are reported
- **WHEN** active research-paradigm skill text emits `[[tbd-surface:schema-stage-cursor]]`, `[[tbd-surface:schema-agent-team-state]]`, or `[[tbd-surface:policy-branching]]`
- **THEN** validation reports the placeholder as stale and directs the skill to use Research Lifecycle State terms instead
