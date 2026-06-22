# research-execution-extension-contract Specification

## Purpose
Define provider-neutral execution and extension contracts for Isomer Labs research workflows, including Research Operation Extension Points, Capability Binding and Skill Binding projection behavior, Execution Adapter Command Requests, Gate policy preflight, scheduler boundaries, literature provider extension refs, baseline-waiver policy refs, validation, and skill consumption rules.
## Requirements
### Requirement: Research Operation Extension Points
The system SHALL define Research Operation Extension Points as provider-neutral slots that research-paradigm skills can require and topic-specific configuration can fill.

#### Scenario: Skills declare operation needs
- **WHEN** a research-paradigm skill needs execution, repository inspection, package management, notebook execution, HPC jobs, document builds, figure rendering, literature search, baseline acceptance, baseline waiver, cost/privacy policy, credential use, data export, Skill Binding, service requests, or agent launch behavior
- **THEN** the skill declares the matching Research Operation Extension Point instead of naming a provider, command runner, scheduler, credential backend, baseline registry, or host API directly

#### Scenario: Topic config supplies refs
- **WHEN** a Research Topic Config, Topic Agent Team Profile, Domain Agent Team Template, Run plan, or explicit command context fills a Research Operation Extension Point
- **THEN** it supplies stable refs to Capability Bindings, Execution Adapters, Skill Binding projections, Gate policies, provider bindings, Artifact Format Profiles, Artifact Extensions, or other accepted extension records without embedding executable implementation bodies

#### Scenario: Topic config and team profile refs have distinct scopes
- **WHEN** examples or validation rules describe where extension refs are declared
- **THEN** Research Topic Config carries topic-level defaults and selected extension refs, while Topic Agent Team Profile, Capability Binding, and Skill Binding projection material carry role-scoped, stage-scoped, and skill-availability details for the topic-specialized team

#### Scenario: Missing extension blocks only dependent behavior
- **WHEN** a requested operation depends on an extension point that has no valid ref
- **THEN** validation reports the missing extension point and blocks only the behavior that depends on it while allowing unrelated inspection, planning, and durable record review

#### Scenario: User-specific details remain external
- **WHEN** a topic needs domain-specific details such as datasets, metric contracts, CUDA profiling tools, venue templates, literature providers, package managers, credentials, remote queues, or renderer behavior
- **THEN** those details are selected through extension refs and topic-specific configuration rather than becoming mandatory fields in the generic research-paradigm skillset

### Requirement: Capability and Skill Binding Projection
The system SHALL define Capability Binding and Skill Binding projection behavior for research operations without requiring one provider-specific skill installer or tool runtime.

#### Scenario: Capability binding exposes operation authority
- **WHEN** a Capability Binding is selected for a Research Operation Extension Point
- **THEN** it identifies the allowed operation kinds, scoped Agent Roles or Agent Profiles, required credentials or credential refs, allowed data scopes, workspace permissions, available Execution Adapters or providers, and recording obligations

#### Scenario: Skill binding projection declares available skills
- **WHEN** a Skill Binding projection is selected for an Agent Role, Agent Profile, Topic Agent Team Profile, or Run context
- **THEN** it identifies available skill ids, skill versions or compatibility refs when known, directly required references or assets, allowed operation extension points, and any topic-specific skill parameters

#### Scenario: Skill binding is not an installer
- **WHEN** a Skill Binding projection references a skill
- **THEN** it records the intended skill availability and compatibility for validation without defining provider-specific installation, packaging, marketplace, or filesystem layout behavior

#### Scenario: Binding mismatch is reported
- **WHEN** a skill requires an operation extension point that is not available through the selected Capability Binding or Skill Binding projection
- **THEN** validation reports the mismatch before command dispatch or delegated execution starts

### Requirement: Execution Adapter Command Request
The system SHALL define a provider-neutral Execution Adapter Command Request envelope for executable research operations.

#### Scenario: Command request carries identity and context
- **WHEN** the system creates an Execution Adapter Command Request
- **THEN** the request includes selected Project, Research Topic, Topic Workspace, Research Inquiry, Research Task, Run when known, Agent Team Instance when known, Agent Instance when known, Effective Topic Context source metadata, and selected Execution Adapter refs

#### Scenario: Command request carries operation refs
- **WHEN** the request describes executable work
- **THEN** it includes operation kind, Research Operation Extension Point refs, Capability Binding refs, Skill Binding projection refs when applicable, Gate policy refs, expected Artifact refs or specs, input refs, output refs or specs, and Provenance Record recording expectations

#### Scenario: Command request uses semantic working target
- **WHEN** the request needs a working directory, logs, scratch area, or output location
- **THEN** it names semantic Workspace Path Resolution targets or Artifact kinds instead of embedding unresolved absolute paths as the generic contract

#### Scenario: Command request carries bounded environment policy
- **WHEN** the request needs environment variables
- **THEN** it names allowed environment input refs, supported `ISOMER_*` identity or path overrides, and non-secret configuration refs without storing credentials, tokens, passwords, API keys, or secret material inline

#### Scenario: Adapter-specific payload is opaque
- **WHEN** a concrete Execution Adapter needs provider-specific command syntax, notebook payloads, queue parameters, service dispatch payloads, or agent launch material
- **THEN** the request may reference opaque adapter-specific payload refs while keeping the provider-neutral request fields valid and auditable

#### Scenario: Service and launch operations share the envelope
- **WHEN** the Operator Agent or Execution Adapter prepares a Service Request dispatch, Service Agent Instance launch, Agent Team Instance launch, or other agent-launch operation
- **THEN** it uses the Execution Adapter Command Request envelope with a narrow operation kind such as `service_request` or `agent_launch` and selected dispatch, preflight, monitoring, Gate policy, scheduler policy, expected Artifact, Run linkage, and Provenance refs, while preserving Service Request, Service Agent Instance, Agent Team Instance, and Agent Profile domain records as distinct objects

### Requirement: Execution Preflight and Gate Policy
The system SHALL run execution preflight before governed command dispatch or provider operations.

#### Scenario: Preflight checks required policies
- **WHEN** an Execution Adapter Command Request may incur cost, use credentials, access private data, export data, upload externally, run long compute, mutate project state, or produce publication-facing output
- **THEN** preflight requires matching Gate policy refs or an already resolved Gate decision before dispatch

#### Scenario: Gate is opened when human approval is needed
- **WHEN** preflight finds that a governed action needs Operator Agent approval
- **THEN** the system opens or references a Gate with concrete options, tradeoffs, affected operation refs, expected consequences, and the recommended option when one is defensible

#### Scenario: Preflight records decision inputs
- **WHEN** preflight allows, blocks, or defers a governed action
- **THEN** it records the relevant policy refs, source refs, actor refs, and rationale through a Provenance Record, Gate, or Decision Record according to Research Recording Contracts

#### Scenario: Missing policy blocks governed action
- **WHEN** an operation requires a cost, credential, privacy, safety, data-export, or publication-facing policy and no valid policy ref exists
- **THEN** validation blocks only the governed action and reports the missing policy ref

### Requirement: Scheduler and Monitoring Boundary
The system SHALL distinguish scheduler and monitoring policy from Research Lifecycle State and Workflow Stage Cursor.

#### Scenario: Scheduler policy authorizes dispatch behavior
- **WHEN** a Run, Agent Team Instance, command request, or service request uses automatic dispatch, retry, queueing, monitoring cadence, long-running checkpoints, or resume behavior
- **THEN** it references scheduler or continuation policy refs without redefining Workflow Stage Cursor or Agent Team Instance lifecycle statuses

#### Scenario: Manual mode does not require scheduler
- **WHEN** a Research Topic, Run, or Topic Agent Team Profile uses manual control mode
- **THEN** the system can proceed through Operator Agent handoffs, Gates, and explicit commands without requiring an automatic scheduler policy

#### Scenario: Monitoring produces durable observations
- **WHEN** a long-running operation is monitored
- **THEN** state changes, progress summaries, failures, completion signals, and stale-watch conditions are recorded through Run records, Signal Observations, Artifacts, or Provenance Records rather than hidden scheduler state

#### Scenario: Scheduler cannot change research route silently
- **WHEN** a scheduler or continuation policy recommends a new route, retry, Research Inquiry Relationship, pause, resume, or stop
- **THEN** meaningful research route changes still require accepted Research Lifecycle State objects, Decision Records, Gates, or Operator Agent instruction as applicable

### Requirement: Literature Provider Extension
The system SHALL define literature search and paper-reading as a typed provider extension point with durable recording obligations.

#### Scenario: Literature request declares purpose
- **WHEN** a skill requests literature search, paper metadata, citation data, paper reading, benchmark lookup, repository lookup, or adjacent-work scouting
- **THEN** the request declares the research purpose, query or source refs, scope boundaries, expected result fields, provider binding ref, and evidence-use intent

#### Scenario: Literature results carry source metadata
- **WHEN** a literature provider returns results
- **THEN** each result includes source title or identifier when known, authors or organization when known, venue or repository source when known, publication or access date when known, DOI, arXiv id, URL, repository ref, benchmark ref, confidence or quality label when known, and provider Provenance refs

#### Scenario: Literature context is not automatically evidence
- **WHEN** a literature result is recorded
- **THEN** it becomes an Artifact, Finding, or Evidence Item according to its evidence-use intent and does not support a Research Claim until linked through accepted Evidence Item rules

#### Scenario: Context-only literature starts as provider-output Artifact
- **WHEN** a literature result is collected for orientation, source review, adjacent-work scouting, or future comparison and is not yet used to support, contradict, contextualize, refute, or motivate withdrawal of a Research Claim
- **THEN** the system records it first as a provider-output Artifact with source metadata and Provenance refs, and may later derive a Finding or Evidence Item only when the evidence-use intent changes

#### Scenario: Missing provider degrades to local sources
- **WHEN** no valid literature provider binding is available
- **THEN** literature-facing skills may proceed only with user-provided sources, existing Artifacts, existing Findings, repository files, or explicit Operator Agent scope limitation, and validation reports the missing provider binding for external search

### Requirement: Baseline Waiver Policy Extension
The system SHALL define baseline waiver behavior as a separate policy extension point that distinguishes comparator relevance, active baseline acceptance, explicit waiver, and whether a human-return Gate is required.

#### Scenario: Baseline acceptance questions are separate
- **WHEN** a skill evaluates baseline status
- **THEN** it separately records whether a comparator is relevant, whether it is accepted as the active baseline, and whether a baseline-waiver policy allows bypassing active baseline acceptance

#### Scenario: Waiver requires policy or Gate
- **WHEN** a route would proceed without an accepted active baseline
- **THEN** the system requires a valid baseline-waiver policy ref or a Gate/Decision Record that explicitly records the waiver rationale and consequences

#### Scenario: Waiver policy may open a Gate
- **WHEN** a baseline-waiver policy determines that human judgment is required before bypassing active baseline acceptance
- **THEN** the system opens or references a Gate for the specific choice while keeping the reusable waiver policy ref separate from the Gate record

#### Scenario: Waiver does not erase comparator evidence
- **WHEN** a baseline waiver is granted
- **THEN** existing comparator Artifacts, Evidence Items, Findings, metric contracts, and known limitations remain visible and linked to later claims or decisions

#### Scenario: Missing waiver policy blocks baseline-dependent promotion
- **WHEN** a skill tries to promote an experiment, idea, optimization route, or paper claim that depends on waived baseline acceptance and no valid waiver policy or Gate exists
- **THEN** validation blocks only that promotion and reports the missing baseline-waiver policy

### Requirement: Extension Contract Validation
The system SHALL validate research execution and extension contracts before dispatch and during skillset review.

#### Scenario: Required extension refs validate before dispatch
- **WHEN** an executable or provider-backed operation is requested
- **THEN** validation checks required Research Operation Extension Points, Capability Bindings, Skill Binding projections, Execution Adapter refs, Gate policy refs, provider refs, expected outputs, and recording obligations before dispatch

#### Scenario: No provider-specific implementation body in generic config
- **WHEN** Research Topic Config, Effective Topic Context, or a generic skill reference is inspected
- **THEN** validation rejects inline provider-specific command bodies, credentials, tokens, API keys, live process state, command outputs, provider payloads, or scheduler internals as generic contract fields

#### Scenario: Unused extension refs are allowed
- **WHEN** a Research Topic Config or Topic Agent Team Profile provides extension refs that are not needed by the current command
- **THEN** validation does not block the command solely because those unrelated refs are missing optional runtime details

#### Scenario: Extension contract replaces resolved TBD placeholders
- **WHEN** active research-paradigm skills are validated after this contract is applied
- **THEN** the six placeholders `api-execution-command`, `policy-scheduler`, `policy-cost-privacy-gate`, `schema-skill-binding`, `policy-baseline-waiver`, and `provider-literature-search` are removed from active guidance or mapped to accepted extension-point terms rather than remaining open TBDs

### Requirement: Houmao adapter public backend boundary
The system SHALL route Houmao-backed live agent lifecycle operations through Execution Adapter Command Requests and Houmao’s public CLI JSON boundary rather than private Python internals.

#### Scenario: Agent launch request selects CLI-backed adapter
- **WHEN** the system prepares a Houmao-backed Agent Team Instance launch
- **THEN** it creates or validates an Execution Adapter Command Request with operation kind `agent_launch`, selected Execution Adapter ref, Agent Team Instance ref, Agent Instance refs, Agent Workspace refs, launch material refs, Gate policy refs, Provenance obligations, and an opaque adapter payload ref for Houmao CLI details

#### Scenario: Adapter uses public CLI JSON
- **WHEN** the Houmao adapter performs live launch, inspect, stop, or preflight behavior
- **THEN** it invokes `houmao-mgr --print-json` through the adapter runner and does not depend on private Houmao Python functions, Click callback internals, or in-process Houmao global state

#### Scenario: Future SDK requires accepted contract
- **WHEN** a future Houmao release exposes a stable Python SDK
- **THEN** Isomer may use it only after an accepted spec updates the Execution Adapter boundary and preserves equivalent recording, preflight, redaction, and manifest obligations

### Requirement: Houmao direct operation remains reconcilable
The system SHALL allow direct Houmao operation to coexist with Isomer quick launch by treating backend-native changes as observed adapter state until reconciliation or adoption records them.

#### Scenario: Direct launch does not bypass Isomer records
- **WHEN** a user invokes `houmao-mgr` directly from prepared material
- **THEN** Isomer does not treat the backend-native state as accepted Workspace Runtime launch state until reconciliation or adoption validates manifests, live observations, and Agent Instance mappings

#### Scenario: Backend observations are not generic completion
- **WHEN** the Houmao adapter observes live backend state during inspect-live, reconciliation, or stop
- **THEN** the observation remains an adapter inspection snapshot, Signal Observation, diagnostic Artifact, or adapter payload ref until accepted recording rules normalize it into generic lifecycle, handoff, Run, or research evidence records

### Requirement: Adapter Reconciliation Command Requests
The system SHALL route Houmao manifest reconciliation and adoption through provider-neutral Execution Adapter Command Requests.

#### Scenario: Reconcile request is created
- **WHEN** the system prepares to reconcile Houmao adapter manifests with Workspace Runtime and live Houmao state
- **THEN** it creates or validates an Execution Adapter Command Request with operation kind `adapter_reconcile`, selected Execution Adapter ref, Agent Team Instance ref, manifest refs, observation expectations, path validation expectations, and Provenance obligations

#### Scenario: Adopt request is created
- **WHEN** the system prepares to adopt externally launched Houmao runtime state
- **THEN** it creates or validates an Execution Adapter Command Request with operation kind `adapter_adopt`, target Agent Team Instance ref, proposed Agent Instance mappings, manifest refs, mapping confidence, Gate or approval refs when required, and Provenance obligations

#### Scenario: Reconciliation does not mutate Houmao
- **WHEN** an adapter reconciliation or adoption command request is executed
- **THEN** the adapter reads Houmao state and records Isomer-side outcomes without launching, stopping, or messaging Houmao-managed agents

### Requirement: Manifest Reconciliation Preflight
The system SHALL complete preflight before recording Houmao reconciliation or adoption outcomes.

#### Scenario: Reconciliation preflight validates inputs
- **WHEN** a Houmao reconciliation command is requested
- **THEN** preflight verifies current Workspace Runtime schema, selected Topic Workspace, selected Agent Team Instance, JSON manifest parseability, path-plan validity, redaction checks, and Houmao read-only inspection availability

#### Scenario: Failed preflight blocks recording
- **WHEN** reconciliation or adoption preflight fails
- **THEN** the system does not write reconciliation records, adoption records, or adapter-runtime manifests and returns deterministic diagnostics
