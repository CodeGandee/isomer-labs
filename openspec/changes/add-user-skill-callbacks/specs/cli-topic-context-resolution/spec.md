## ADDED Requirements

### Requirement: User Skill Callback Registry Refs in Topic Context
The system SHALL let Project and Research Topic configuration expose User Skill Callback registry refs as declarative instruction-customization refs without treating callback material as runtime truth, executable provider payloads, or credentials.

#### Scenario: Research Topic Config carries callback registry refs
- **WHEN** a Research Topic Config is loaded
- **THEN** it may name User Skill Callback registry refs for topic-scoped callback resolution
- **AND** validation treats those refs as declarative instruction-customization refs rather than Run state, Artifact contents, provider implementation bodies, or command outputs

#### Scenario: Project Manifest carries callback registry refs
- **WHEN** a Project Manifest is loaded
- **THEN** it may name User Skill Callback registry refs for project-scoped callback resolution
- **AND** validation treats those refs as declarative instruction-customization refs rather than topic runtime state, credential material, provider implementation bodies, or command outputs

#### Scenario: Effective Topic Context exposes callback refs
- **WHEN** Effective Topic Context is resolved for a topic-scoped command
- **THEN** it includes the validated project-scoped and topic-scoped User Skill Callback registry refs that may influence callback resolution for that command

#### Scenario: Callback refs do not execute during context load
- **WHEN** Project discovery or Effective Topic Context resolution sees User Skill Callback registry refs
- **THEN** the system validates registry locations and metadata needed for the current command but does not execute callback content, external skill scripts, provider payloads, or agent workflows during context loading

#### Scenario: Inline callback bodies are rejected from config
- **WHEN** Project Manifest or Research Topic Config stores inline callback prompt bodies, external skill body text, runtime outputs, credentials, tokens, API keys, passwords, or other secret material directly in configuration fields
- **THEN** validation rejects those fields and directs the user to managed callback registry content or a credential backend as appropriate

#### Scenario: Durable records store callback refs only when consumed
- **WHEN** a future Run, command request, or provider-backed operation consumes Effective Topic Context that includes User Skill Callback registry refs
- **THEN** any durable record stores the validated callback registry refs and consumed callback ids rather than storing the full callback instruction bodies as runtime context truth
