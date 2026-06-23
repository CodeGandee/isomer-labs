## ADDED Requirements

### Requirement: Isomer Project Operator and Topic Service Skills
The repository SHALL include provider-neutral skill instructions for Project Operator Sessions, Operator Agents, and Topic Service Agents to instantiate topic teams from Domain Agent Team Templates.

#### Scenario: Project awareness skill exists
- **WHEN** an agent is pointed at an Isomer Project root
- **THEN** a skill instructs it to resolve the project root, inspect Project Manifest, list Research Topics, locate Topic Workspaces, discover Domain Agent Team Templates, and discover Topic Service Agents

#### Scenario: Service request routing skill exists
- **WHEN** a Project Operator Session or Operator Agent needs topic-scoped service help
- **THEN** a skill instructs it to open a bounded Service Request to a Topic Service Agent with scope, expected output, authorization, dispatch form, and provenance obligations

#### Scenario: Template inspection skill exists
- **WHEN** the project operator or Topic Service Agent needs to specialize a Domain Agent Team Template
- **THEN** a skill instructs it to inspect template manifest, placeholder catalog, role bindings, workflow stages, workspace contract, instantiation schema, and validation diagnostics

#### Scenario: Topic context resolution skill exists
- **WHEN** the project operator or Topic Service Agent needs topic-specific values
- **THEN** a skill instructs it to resolve Project Manifest, Research Topic Config, Effective Topic Context, Topic Workspace, Workspace Runtime readiness, policy refs, Capability Binding refs, Skill Binding Projection refs, provider refs, and Gate policy refs

#### Scenario: Placeholder reconciliation skill exists
- **WHEN** the project operator or Topic Service Agent maps template placeholders to topic-specific values
- **THEN** a skill instructs it to record resolved substitutions, explicit deferrals, unresolved blockers, Service Request outputs, and user decisions in an instantiation packet

#### Scenario: Profile drafting and review skills exist
- **WHEN** a Project Operator Session or Operator Agent reviews a Topic Agent Team Profile draft
- **THEN** skills instruct it to produce reviewable profile bundle material, summarize copied and rewritten template content, summarize role and policy choices, identify launch blockers, include Topic Service Agent support outputs when relevant, and request approval before materialization

#### Scenario: Materialization and launch orchestration skills exist
- **WHEN** the project operator has approval to proceed
- **THEN** skills instruct it to call generic Isomer validators/materializers, record provenance, and route launch requests through the Houmao adapter without hand-editing runtime state

#### Scenario: Topic Service Agent support skills exist
- **WHEN** a Topic Service Agent receives a Service Request
- **THEN** skills instruct it to perform only bounded Service Team work such as environment readiness, work-agent setup, instantiation support, monitoring, diagnostics, and support Artifact writing

### Requirement: Project Operator and Topic Service Skills Stay Bounded
Project operator and Topic Service Agent skills SHALL describe orchestration and support decisions without granting authority to bypass Isomer validation, Gates, or runtime recording.

#### Scenario: Skills require validation
- **WHEN** a skill produces a packet, profile, runtime request, handoff, Service Request, support Artifact, or launch request
- **THEN** the skill requires validation through generic Isomer APIs or CLI before treating the artifact as authoritative

#### Scenario: Skills preserve domain boundaries
- **WHEN** a skill handles Domain Agent Team Templates, Topic Agent Team Profiles, Agent Team Instances, Service Requests, Topic Service Agents, or adapter material
- **THEN** it uses the canonical Isomer domain terms and does not collapse template, profile, runtime team, service team, and Houmao managed-agent concepts
