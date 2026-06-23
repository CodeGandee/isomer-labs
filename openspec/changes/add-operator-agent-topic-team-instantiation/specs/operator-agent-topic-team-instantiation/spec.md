## ADDED Requirements

### Requirement: Project Operator Session Topic-Team Instantiation Workflow
The system SHALL instantiate topic-level teams through a Project Operator Session or Operator Agent workflow that specializes a Domain Agent Team Template before any Agent Team Instance is launched or resolved.

#### Scenario: Project operator discovers project and topic surfaces
- **WHEN** a user points an agent with Isomer system skills at an Isomer Project root
- **THEN** the Project Operator Session can discover the Project Manifest, Research Topics, Topic Workspaces, Domain Agent Team Templates, Topic Agent Team Profiles, Workspace Runtime refs, and available Topic Service Agents

#### Scenario: Project operator inspects template and topic context
- **WHEN** a user requests a topic team from a selected Domain Agent Team Template
- **THEN** the Project Operator Session or Operator Agent inspects the template placeholder catalog, role binding slots, workflow stages, workspace contract, Effective Topic Context, Research Topic Config, Topic Workspace, and available policy or binding refs before drafting or approving a Topic Agent Team Profile

#### Scenario: Topic Service Agent supports topic instantiation
- **WHEN** template specialization requires topic-specific operational support
- **THEN** the Project Operator Session or Operator Agent can open a Service Request to a Topic Service Agent for template inspection support, placeholder reconciliation support, topic environment readiness, Agent Workspace setup, diagnostics, or support Artifact production

#### Scenario: Template is not treated as directly launchable
- **WHEN** the selected Domain Agent Team Template contains unresolved placeholders
- **THEN** the system requires a topic-level instantiation packet or approved Topic Agent Team Profile before Agent Team Instance creation or Houmao launch materialization

### Requirement: Topic Team Instantiation Packet
The system SHALL represent agent-mediated specialization output as a structured instantiation packet before materializing a Topic Agent Team Profile.

#### Scenario: Packet records resolved substitutions and bundle target
- **WHEN** the Project Operator Session, Operator Agent, or Topic Service Agent resolves template placeholders for a Research Topic
- **THEN** the packet records source template ref, Research Topic ref, Topic Workspace ref, Workspace Runtime ref, target Topic Agent Team Profile Bundle path inside the owning Topic Workspace, role bindings, policy refs, expected Artifact refs or kinds, control mode, copied template material plan, approval state, project operator provenance, Topic Service Agent provenance when used, and validation refs

#### Scenario: Packet target is fixed per topic
- **WHEN** a packet attempts to select a second profile id, alternate profile bundle path, or competing team for an already selected Research Topic
- **THEN** packet validation rejects the packet and reports that topic-level parallelism requires a separate Research Topic with its own dedicated team

#### Scenario: Packet records explicit deferrals
- **WHEN** a required placeholder cannot be resolved at profile time
- **THEN** the packet records the placeholder, reason, launch impact, required user or service action, and whether the profile can be saved but not launched

#### Scenario: Packet rejects runtime truth at profile layer
- **WHEN** packet material intended for a Topic Agent Team Profile contains live process ids, mailbox state, gateway state, command outputs, credentials, tokens, API keys, passwords, Evidence Items, Findings, Gates, Decision Records, or rich Artifact contents
- **THEN** packet validation rejects the material and reports the offending field without exposing secret values

### Requirement: Project Operator Review Gate
The system SHALL require reviewable project-operator output before writing an authoritative Topic Agent Team Profile.

#### Scenario: Draft profile bundle is reviewable
- **WHEN** a Project Operator Session or Operator Agent reviews a Topic Agent Team Profile draft from an instantiation packet
- **THEN** the user-facing review includes selected roles, inactive roles, role binding refs, capability refs, skill projections, Agent Workspace refs, policy refs, expected Artifacts, copied or rewritten template material, unresolved placeholders, launch blockers, Service Request outputs when relevant, and provenance

#### Scenario: Approval precedes materialization
- **WHEN** a Topic Agent Team Profile is written as authoritative material
- **THEN** the write records approval context or deterministic test approval and links the written Topic Agent Team Profile Bundle to the instantiation packet

### Requirement: Isomer Project Operator and Topic Service Skills
The system SHALL provide bounded Isomer skills for project-operator-capable agents and Houmao-backed Topic Service Agents to perform topic-team instantiation and orchestration.

#### Scenario: Project operator skills are discoverable
- **WHEN** an agent prepares to operate an Isomer Project
- **THEN** it can use skills for project awareness, topic discovery, template discovery, Topic Service Agent discovery, Service Request routing, review Gate preparation, materialization, launch orchestration, runtime recording, and handoff orchestration

#### Scenario: Topic Service Agent skills are discoverable
- **WHEN** a Topic Service Agent receives a Service Request for topic-team instantiation support
- **THEN** it can use topic-specific Service Team skills for template inspection, topic context resolution, placeholder reconciliation, topic environment readiness, Agent Workspace setup, diagnostics, monitoring, and support Artifact writing

#### Scenario: Skills do not bypass validators
- **WHEN** a project-operator or Topic Service Agent skill drafts or materializes topic-team artifacts
- **THEN** generic Isomer validators still parse and validate the packet, Topic Agent Team Profile, runtime records, and adapter material before mutation or launch

### Requirement: No Hardcoded Template Substitution
The system SHALL keep template-specific placeholder substitution out of authoritative product code paths.

#### Scenario: Generic code does not special-case deepsci-mini instantiation
- **WHEN** source code creates or validates an authoritative Topic Agent Team Profile
- **THEN** it uses generic packet/profile/template validation and does not hardcode `deepsci-mini` role ids, UC-01 ids, or template-specific placeholder substitutions except in tests, fixtures, or template data

#### Scenario: Preview defaults are labeled
- **WHEN** a CLI or API path emits synthetic Topic Agent Team Profile preview values without an approved instantiation packet
- **THEN** the output identifies the values as preview or candidate material and does not treat them as an approved profile bundle materialization
