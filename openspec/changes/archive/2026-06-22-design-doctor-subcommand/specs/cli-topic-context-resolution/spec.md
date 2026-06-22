## MODIFIED Requirements

### Requirement: Research Topic Config Content
The system SHALL define Research Topic Config TOML as topic-specific configuration for defaults and refs, not as Project-level environment binding policy or Workspace Runtime state.

#### Scenario: Topic config identifies its topic
- **WHEN** a Research Topic Config is loaded
- **THEN** the system requires its `research_topic_id` to match the Project Manifest Research Topic registration that referenced it

#### Scenario: Topic config can carry topic defaults
- **WHEN** a Research Topic Config is inspected
- **THEN** it may define topic statement text or refs, Measurable Objective text or refs, default Research Inquiry refs, default Topic Agent Team Profile refs, default Execution Adapter refs, default Control Mode, Capability Binding refs, Skill Binding projection refs, Research Operation Extension Point refs, Gate policy refs, scheduler policy refs, baseline-waiver policy refs, literature provider refs, Artifact Format Profile defaults, and Artifact Extension refs

#### Scenario: Topic config does not own Pixi environment bindings
- **WHEN** a Research Topic Config is loaded
- **THEN** validation treats Project-level Pixi environment bindings as Project Manifest-owned refs and does not infer them from Research Topic Config fields or Pixi environment names

### Requirement: Project Manifest Topic Environment Bindings
The system SHALL let the Project Manifest explicitly record which Project-root Pixi environment or environments each Research Topic uses without inferring topic relationships from Pixi environment names.

#### Scenario: Topic environment bindings use repeated manifest tables
- **WHEN** the Project Manifest declares `[[topic_pixi_environment_bindings]]`
- **THEN** each binding identifies `research_topic_id`, `pixi_environment`, optional `purpose`, and optional `status`

#### Scenario: Topic environment names are not semantic bindings
- **WHEN** a Project-level Pixi environment name resembles a Research Topic id, topic slug, role, stage, or purpose label
- **THEN** validation does not treat that name as a Research Topic binding unless the Project Manifest explicitly records the binding

#### Scenario: One topic can use multiple Pixi environments
- **WHEN** the Project Manifest contains multiple active `topic_pixi_environment_bindings` entries for the same Research Topic and different Pixi environment names
- **THEN** Effective Topic Context and `doctor` preserve the explicit set of bound environment refs for later readiness checks and runtime preparation

#### Scenario: Standalone Pixi isolation bindings use a separate manifest table
- **WHEN** the Project Manifest declares `[[topic_standalone_pixi_bindings]]`
- **THEN** each binding identifies `research_topic_id`, Project-root-relative `manifest_path`, optional `pixi_environment`, optional `purpose`, and optional `status`

#### Scenario: Standalone Pixi isolation is explicit opt-in
- **WHEN** a Topic Workspace contains a `pixi.toml`, `pyproject.toml`, or other Pixi-looking file
- **THEN** validation does not treat the Topic Workspace as using standalone Pixi isolation unless the Project Manifest explicitly records a `topic_standalone_pixi_bindings` entry for that Research Topic

#### Scenario: Standalone Pixi manifest path stays inside the Project
- **WHEN** the Project Manifest declares `topic_standalone_pixi_bindings.manifest_path`
- **THEN** validation requires the path to resolve inside the Project root and reports a Project Manifest diagnostic for absolute or relative paths that escape the Project

#### Scenario: Topic environment binding references registered topic
- **WHEN** a Project Manifest topic Pixi environment binding names `research_topic_id`
- **THEN** validation requires the id to match a registered Research Topic in the same Project Manifest

#### Scenario: Duplicate active topic environment binding is rejected
- **WHEN** the Project Manifest contains duplicate active `topic_pixi_environment_bindings` entries for the same `research_topic_id`, `pixi_environment`, and `purpose`
- **THEN** validation reports a Project Manifest diagnostic rather than treating the duplicate rows as separate environment uses

#### Scenario: Duplicate active standalone binding is rejected
- **WHEN** the Project Manifest contains duplicate active `topic_standalone_pixi_bindings` entries for the same `research_topic_id`, `manifest_path`, `pixi_environment`, and `purpose`
- **THEN** validation reports a Project Manifest diagnostic rather than treating the duplicate rows as separate standalone uses

#### Scenario: Topic statement can be inline and artifact-backed
- **WHEN** a Research Topic Config describes the Research Topic
- **THEN** it may include one short inline `topic_statement` for discovery, CLI previews, and human review, plus `topic_statement_artifact_refs` or other explicit Artifact refs for richer or evolving topic material

#### Scenario: Topic statement refs do not make config runtime state
- **WHEN** Research Topic Config references richer topic briefs, user notes, rationale, source notes, or objective material as Artifacts
- **THEN** the config stores only refs to those Artifacts and does not embed their rich content as authoritative Workspace Runtime state

#### Scenario: Topic config does not own runtime truth
- **WHEN** a Research Topic Config contains Run status, command outputs, live process ids, resolved command results, Artifact contents, Evidence Items, Findings, Gates, Decision Records, Provenance Records, environment readiness status, Pixi install output, prepared environment paths, or Project-level Pixi environment bindings as authoritative state
- **THEN** validation reports the config as invalid and directs those facts to Workspace Runtime or file-backed Artifacts

#### Scenario: Topic config does not store secrets
- **WHEN** a Research Topic Config contains inline credentials, tokens, API keys, passwords, or secret material
- **THEN** validation reports the config as invalid and directs the value to a credential backend or a Capability Binding ref

#### Scenario: Topic config extension refs are declarative
- **WHEN** a Research Topic Config names Research Operation Extension Point refs, Capability Binding refs, Skill Binding projection refs, literature provider refs, baseline-waiver policy refs, scheduler policy refs, cost/privacy Gate policy refs, or Execution Adapter refs
- **THEN** validation treats those values as declarative refs for later command, provider, policy, and skill availability resolution and does not execute or dereference provider-specific implementation bodies while loading the config

#### Scenario: Topic config does not replace team profile binding
- **WHEN** a Research Topic Config names topic-level defaults for extension refs, provider refs, policy refs, or Execution Adapter refs
- **THEN** validation keeps role-scoped, Workflow Stage-scoped, skill-availability, operation-authority, Project-level topic environment bindings, and per-agent environment-divergence details in Project Manifest, Topic Agent Team Profile, Capability Binding, Skill Binding projection, Workspace Runtime readiness records, or Service Request material rather than treating Research Topic Config as the complete execution binding
