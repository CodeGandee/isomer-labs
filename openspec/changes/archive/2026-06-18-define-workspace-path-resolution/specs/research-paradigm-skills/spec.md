## MODIFIED Requirements

### Requirement: Unsettled Concrete Surfaces Are Explicit
The extracted skills SHALL mark unsettled commands, runtime APIs, providers, schemas, policies, storage roots, and generated layouts as `yet-to-be-determined` only when they are not settled by accepted Isomer designs such as the Workspace Path Resolution contract.

#### Scenario: Path surface is covered by workspace path resolution
- **WHEN** a skill needs an ordinary Topic Workspace, Workspace Runtime, Agent Workspace, Run log, experiment output, analysis output, paper output, figure output, or Artifact class location covered by the Workspace Path Resolution contract
- **THEN** the skill names the semantic workspace scope or Artifact kind and relies on the resolver instead of emitting a path TBD placeholder

#### Scenario: Path surface remains unsettled outside the resolver
- **WHEN** a source skill uses a concrete path or filename that is not covered by the Workspace Path Resolution contract and no Isomer equivalent is settled by existing domain concepts or ADRs
- **THEN** the extracted skill marks that path or filename as `yet-to-be-determined` and states the missing design decision

#### Scenario: Runtime API is not settled
- **WHEN** a DeepScientist source skill depends on a command, tool wrapper, artifact API, memory API, runner home, prompt injection mechanism, or paper-search provider with no settled Isomer equivalent
- **THEN** the extracted skill marks that surface as `yet-to-be-determined` and avoids inventing an implementation-specific default

## ADDED Requirements

### Requirement: Workspace Path Resolution Consumption
The research-paradigm skillset SHALL consume the Workspace Path Resolution contract for ordinary files, workspaces, logs, and Artifact class locations.

#### Scenario: Shared registry reflects resolved path surfaces
- **WHEN** `isomer-rsch-shared/references/tbd-surface-registry.md` is inspected after this change
- **THEN** ordinary path surfaces for Topic Workspace, Workspace Runtime, Agent Workspace, Artifact layout, Run logs, experiment output, analysis output, paper layout, and figure output are removed as open TBDs or explicitly mapped to the Workspace Path Resolution contract

#### Scenario: Skill references request semantic outputs
- **WHEN** a research-stage skill needs to create intake notes, baseline records, experiment outputs, analysis results, figures, paper drafts, decisions, evidence, findings, handoffs, logs, or agent scratch files
- **THEN** the skill names the semantic Artifact kind or workspace scope rather than prescribing a concrete path

#### Scenario: Local contract copies stay consistent
- **WHEN** a local `isomer-research-contract.md` copy is inspected in an `isomer-rsch-*` skill directory
- **THEN** its path guidance matches the shared workspace path resolution contract and does not reintroduce ordinary path TBD placeholders

#### Scenario: Non-path TBD surfaces remain explicit
- **WHEN** a research-stage skill needs an unsettled runtime API, command surface, provider, schema, or policy
- **THEN** the skill continues to use the appropriate non-path TBD placeholder until that surface has its own accepted Isomer contract

#### Scenario: Validation checks resolved and unresolved surfaces
- **WHEN** implementation validation runs
- **THEN** it confirms ordinary workspace path TBDs were removed or mapped to the path resolver, non-path TBDs remain registered, and no skill reference depends on hard-coded DeepScientist paths or local absolute paths
