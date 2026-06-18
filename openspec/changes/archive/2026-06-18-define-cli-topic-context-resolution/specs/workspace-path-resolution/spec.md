## ADDED Requirements

### Requirement: Effective Topic Context Input
The system SHALL allow Workspace Path Resolution to consume a validated Effective Topic Context from `isomer-cli`, an Operator Agent, or an Execution Adapter before resolving Topic Workspace and related path surfaces.

#### Scenario: Context supplies selected topic
- **WHEN** Workspace Path Resolution receives an Effective Topic Context with Project, Research Topic, and Topic Workspace refs
- **THEN** the resolver uses those refs to select the applicable recorded workspace plan, Project Manifest defaults, and built-in defaults without performing independent Research Topic selection

#### Scenario: Context supplies optional run and agent refs
- **WHEN** Effective Topic Context includes validated Research Task, Run, Agent Team Instance, or Agent Instance refs
- **THEN** the resolver uses those refs to choose applicable task support, run, log, Agent Workspace, Agent Runtime, and Artifact path surfaces according to the existing path precedence rules

#### Scenario: Path precedence is unchanged
- **WHEN** Effective Topic Context is present and a path surface has recorded plan, supported path environment variable, Project Manifest default, or built-in default candidates
- **THEN** the resolver still applies the accepted precedence of recorded plan, environment path override, Project Manifest default, then built-in default

#### Scenario: Topic context does not become durable path truth
- **WHEN** path values are resolved from Effective Topic Context and Workspace Path Resolution inputs
- **THEN** the system records the effective paths and sources in Workspace Runtime or Provenance Records before downstream research work depends on those paths

#### Scenario: Context mismatch blocks path resolution
- **WHEN** Effective Topic Context names a Research Topic, Topic Workspace, Research Task, Run, Agent Team Instance, or Agent Instance that is inconsistent with the Project Manifest or Workspace Runtime refs needed for a path surface
- **THEN** path resolution fails with a validation error instead of choosing a path from an ambiguous or mismatched context
