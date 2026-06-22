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

### Requirement: Houmao Reconciliation Lifecycle Summary
The system SHALL represent Houmao reconciliation state through adapter-linked lifecycle summaries for Agent Team Instances and Agent Instances.

#### Scenario: External detection is not adopted lifecycle
- **WHEN** reconciliation detects live Houmao-managed agents that match an Isomer link manifest but have not been adopted
- **THEN** the Agent Team Instance summary reports externally detected adapter state without marking the generic launch lifecycle as launched by Isomer

#### Scenario: Adoption updates lifecycle summary
- **WHEN** adoption succeeds for externally launched Houmao runtime state
- **THEN** the Agent Team Instance and mapped Agent Instance summaries include adopted adapter state, mapping confidence, and Provenance refs

#### Scenario: Drift keeps previous lifecycle visible
- **WHEN** reconciliation reports material drift, missing native runtime paths, stale sessions, or conflicting mappings
- **THEN** the lifecycle summary keeps the previous launch or adoption state visible and adds drift, stale, or conflict diagnostics

### Requirement: Manual Operation Does Not Bypass Normalization
The system SHALL prevent direct Houmao operation from bypassing Isomer handoff and Run normalization requirements.

#### Scenario: Direct Houmao reply remains observation
- **WHEN** direct Houmao mail, gateway output, files, or inspection output indicates progress or candidate completion
- **THEN** the system records or reports Signal Observations and does not mark handoff, Run, or Workflow Stage Cursor completion accepted without Operator Agent normalization

#### Scenario: Adopted runtime keeps normalization boundary
- **WHEN** an externally launched Houmao-backed Agent Team Instance is adopted
- **THEN** existing and future handoff completion still requires the same Operator Agent normalization path as Isomer-launched runtime
