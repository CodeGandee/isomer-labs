## ADDED Requirements

### Requirement: Operator Agent Topic-Team Instantiation Workflow
The system SHALL instantiate topic-level teams through an Operator Agent workflow that specializes a Domain Agent Team Template before any Agent Team Instance is launched or resolved.

#### Scenario: Operator Agent inspects template and topic context
- **WHEN** a user requests a topic team from a selected Domain Agent Team Template
- **THEN** the Operator Agent inspects the template placeholder catalog, role binding slots, workflow stages, workspace contract, Effective Topic Context, Research Topic Config, Topic Workspace, and available policy or binding refs before drafting a Topic Agent Team Profile

#### Scenario: Template is not treated as directly launchable
- **WHEN** the selected Domain Agent Team Template contains unresolved placeholders
- **THEN** the system requires a topic-level instantiation packet or approved Topic Agent Team Profile before Agent Team Instance creation or Houmao launch materialization

### Requirement: Topic Team Instantiation Packet
The system SHALL represent Operator Agent specialization output as a structured instantiation packet before materializing a Topic Agent Team Profile.

#### Scenario: Packet records resolved substitutions
- **WHEN** the Operator Agent resolves template placeholders for a Research Topic
- **THEN** the packet records source template ref, Research Topic ref, Topic Workspace ref, Workspace Runtime ref, target Topic Agent Team Profile id, role bindings, policy refs, expected Artifact refs or kinds, control mode, approval state, and provenance refs

#### Scenario: Packet records explicit deferrals
- **WHEN** a required placeholder cannot be resolved at profile time
- **THEN** the packet records the placeholder, reason, launch impact, required user or service action, and whether the profile can be saved but not launched

#### Scenario: Packet rejects runtime truth at profile layer
- **WHEN** packet material intended for a Topic Agent Team Profile contains live process ids, mailbox state, gateway state, command outputs, credentials, tokens, API keys, passwords, Evidence Items, Findings, Gates, Decision Records, or rich Artifact contents
- **THEN** packet validation rejects the material and reports the offending field without exposing secret values

### Requirement: Operator Agent Review Gate
The system SHALL require reviewable Operator Agent output before writing an authoritative Topic Agent Team Profile.

#### Scenario: Draft profile is reviewable
- **WHEN** the Operator Agent drafts a Topic Agent Team Profile from an instantiation packet
- **THEN** the user-facing review includes selected roles, inactive roles, role binding refs, capability refs, skill projections, Agent Workspace refs, policy refs, expected Artifacts, unresolved placeholders, launch blockers, and provenance

#### Scenario: Approval precedes materialization
- **WHEN** a Topic Agent Team Profile is written as authoritative material
- **THEN** the write records approval context or deterministic test approval and links the written profile to the instantiation packet

### Requirement: Isomer Operator Agent Skills
The system SHALL provide bounded Isomer skills for the Houmao-backed Operator Agent to perform topic-team instantiation and orchestration.

#### Scenario: Required skills are discoverable
- **WHEN** the Operator Agent prepares to instantiate a topic team
- **THEN** it can use skills for template inspection, topic context resolution, placeholder reconciliation, profile drafting, profile review Gate preparation, profile materialization, team launch orchestration, runtime recording, and handoff orchestration

#### Scenario: Skills do not bypass validators
- **WHEN** an Operator Agent skill drafts or materializes topic-team artifacts
- **THEN** generic Isomer validators still parse and validate the packet, Topic Agent Team Profile, runtime records, and adapter material before mutation or launch

### Requirement: No Hardcoded Template Substitution
The system SHALL keep template-specific placeholder substitution out of authoritative product code paths.

#### Scenario: Generic code does not special-case deepsci-mini instantiation
- **WHEN** source code creates or validates an authoritative Topic Agent Team Profile
- **THEN** it uses generic packet/profile/template validation and does not hardcode `deepsci-mini` role ids, UC-01 ids, or template-specific placeholder substitutions except in tests, fixtures, or template data

#### Scenario: Preview defaults are labeled
- **WHEN** a CLI or API path emits synthetic Topic Agent Team Profile preview values without an Operator Agent packet
- **THEN** the output identifies the values as preview or candidate material and does not treat them as an approved profile materialization
