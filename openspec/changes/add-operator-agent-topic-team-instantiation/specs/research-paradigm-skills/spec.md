## ADDED Requirements

### Requirement: Isomer Operator Agent Instantiation Skills
The repository SHALL include provider-neutral skill instructions for an Isomer Operator Agent to instantiate topic teams from Domain Agent Team Templates.

#### Scenario: Template inspection skill exists
- **WHEN** the Operator Agent needs to specialize a Domain Agent Team Template
- **THEN** a skill instructs it to inspect template manifest, placeholder catalog, role bindings, workflow stages, workspace contract, instantiation schema, and validation diagnostics

#### Scenario: Topic context resolution skill exists
- **WHEN** the Operator Agent needs topic-specific values
- **THEN** a skill instructs it to resolve Project Manifest, Research Topic Config, Effective Topic Context, Topic Workspace, Workspace Runtime readiness, policy refs, Capability Binding refs, Skill Binding Projection refs, provider refs, and Gate policy refs

#### Scenario: Placeholder reconciliation skill exists
- **WHEN** the Operator Agent maps template placeholders to topic-specific values
- **THEN** a skill instructs it to record resolved substitutions, explicit deferrals, unresolved blockers, and user decisions in an instantiation packet

#### Scenario: Profile drafting and review skills exist
- **WHEN** the Operator Agent drafts a Topic Agent Team Profile
- **THEN** skills instruct it to produce reviewable profile material, summarize role and policy choices, identify launch blockers, and request approval before materialization

#### Scenario: Materialization and launch orchestration skills exist
- **WHEN** the Operator Agent has approval to proceed
- **THEN** skills instruct it to call generic Isomer validators/materializers, record provenance, and route launch requests through the Houmao adapter without hand-editing runtime state

### Requirement: Operator Agent Skills Stay Bounded
Operator Agent skills SHALL describe orchestration decisions without granting authority to bypass Isomer validation, Gates, or runtime recording.

#### Scenario: Skills require validation
- **WHEN** a skill produces a packet, profile, runtime request, handoff, or launch request
- **THEN** the skill requires validation through generic Isomer APIs or CLI before treating the artifact as authoritative

#### Scenario: Skills preserve domain boundaries
- **WHEN** a skill handles Domain Agent Team Templates, Topic Agent Team Profiles, Agent Team Instances, Service Requests, or adapter material
- **THEN** it uses the canonical Isomer domain terms and does not collapse template, profile, runtime team, service team, and Houmao managed-agent concepts
