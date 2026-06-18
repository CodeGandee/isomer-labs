## MODIFIED Requirements

### Requirement: Unsettled Concrete Surfaces Are Explicit
The extracted skills SHALL mark unsettled commands, runtime APIs, providers, schemas, policies, storage roots, and generated layouts as `yet-to-be-determined` only when they are not settled by accepted Isomer designs such as the Workspace Path Resolution contract or the Research Recording Contracts.

#### Scenario: Path surface is covered by workspace path resolution
- **WHEN** a skill needs an ordinary Topic Workspace, Workspace Runtime, Agent Workspace, Run log, experiment output, analysis output, paper output, figure output, or Artifact class location covered by the Workspace Path Resolution contract
- **THEN** the skill names the semantic workspace scope or Artifact kind and relies on the resolver instead of emitting a path TBD placeholder

#### Scenario: Recording surface is covered by research recording contracts
- **WHEN** a skill needs to record or query Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, or Gates covered by the Research Recording Contracts
- **THEN** the skill names the accepted record type or recording API instead of emitting `api-artifact-record`, `api-finding-query`, `api-gate`, `schema-decision-record`, `schema-evidence-item`, `schema-research-claim`, or `schema-gate` TBD placeholders

#### Scenario: Path surface remains unsettled outside the resolver
- **WHEN** a source skill uses a concrete path or filename that is not covered by the Workspace Path Resolution contract and no Isomer equivalent is settled by existing domain concepts or ADRs
- **THEN** the extracted skill marks that path or filename as `yet-to-be-determined` and states the missing design decision

#### Scenario: Runtime API is not settled
- **WHEN** a DeepScientist source skill depends on a command, tool wrapper, runner home, prompt injection mechanism, paper-search provider, scheduler behavior, Skill Binding, Agent Team State, baseline-waiver policy, branching policy, or cost/privacy policy with no settled Isomer equivalent
- **THEN** the extracted skill marks that surface as `yet-to-be-determined` and avoids inventing an implementation-specific default

### Requirement: Research Recording Contract Consumption
The research-paradigm skillset SHALL consume the Research Recording Contracts for durable record and validation surfaces.

#### Scenario: Shared registry reflects resolved recording surfaces
- **WHEN** `isomer-rsch-shared/references/tbd-surface-registry.md` is inspected after this change
- **THEN** `api-artifact-record`, `api-finding-query`, `api-gate`, `schema-decision-record`, `schema-evidence-item`, `schema-research-claim`, and `schema-gate` are removed as open TBDs or explicitly mapped to Research Recording Contracts

#### Scenario: Skill references use accepted record names
- **WHEN** a research-stage skill needs durable Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, or Gates
- **THEN** the skill names those accepted record types and the accepted recording APIs instead of a TBD placeholder

#### Scenario: Local contract copies stay consistent
- **WHEN** a local `isomer-research-contract.md` copy is inspected in an `isomer-rsch-*` skill directory
- **THEN** its recording guidance matches the shared Research Recording Contracts and does not reintroduce resolved recording TBD placeholders

#### Scenario: Non-recording TBD surfaces remain explicit
- **WHEN** a research-stage skill needs unsettled command execution, literature provider, scheduler policy, Skill Binding, Agent Team State, Stage Cursor, branching policy, baseline-waiver policy, or cost/privacy Gate policy
- **THEN** the skill continues to use the appropriate TBD placeholder until that surface has its own accepted Isomer contract

#### Scenario: Validation checks resolved and unresolved recording surfaces
- **WHEN** implementation validation runs
- **THEN** it confirms resolved recording TBDs were removed or mapped to the Research Recording Contracts, remaining TBDs are registered, and skill references do not invent concrete host APIs outside accepted contracts
