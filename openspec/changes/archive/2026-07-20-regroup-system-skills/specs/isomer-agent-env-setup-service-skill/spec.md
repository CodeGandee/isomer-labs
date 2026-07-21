## MODIFIED Requirements

### Requirement: Agent Env Setup Service Skill Bundle
The core public pack SHALL preserve protected service logical capability `isomer-srv-agent-env-setup` as member `agent-env` for service-safe Agent Workspace setup and per-agent cwd verification.

#### Scenario: Protected service bundle exists
- **WHEN** the core pack is inspected
- **THEN** it contains `operator/isomer-op-entrypoint/subskills/isomer-srv-agent-env-setup/SKILL.md` and `agents/openai.yaml`

#### Scenario: Skill metadata is consistent
- **WHEN** the skill bundle is inspected
- **THEN** the folder name, `SKILL.md` frontmatter `name`, `agents/openai.yaml` display name, and default prompt use `isomer-srv-agent-env-setup`

#### Scenario: Service identity is consistent
- **WHEN** the protected bundle is inspected
- **THEN** its folder and frontmatter retain logical id `isomer-srv-agent-env-setup`
- **AND** its metadata version is release-aligned

#### Scenario: Service boundary is explicit
- **WHEN** the protected entrypoint describes purpose
- **THEN** it prepares Git-backed Agent Workspace cwd readiness without creating Agent Instances, mutating Workspace Runtime, launching Houmao agents, running Execution Adapters, or making research decisions

#### Scenario: Owning route invokes service member
- **WHEN** an authorized operator or extension workflow needs Agent Workspace environment setup
- **THEN** it invokes `isomer-op-entrypoint->agent-env` or resolves the logical id for bounded private projection
- **AND** ordinary user help does not advertise an independent service skill

### Requirement: Invocation and Provenance Posture
Agent environment setup SHALL use the parent-owned route at runtime while preserving `isomer-srv-agent-env-setup` as its logical owner in provenance.

#### Scenario: Service request is routed
- **WHEN** an owning workflow delegates Agent Workspace setup
- **THEN** the request identifies logical capability `isomer-srv-agent-env-setup` and current invocation designator `isomer-op-entrypoint->agent-env`

#### Scenario: Provenance is recorded
- **WHEN** setup produces governed mutation evidence
- **THEN** durable records retain the logical capability id
- **AND** they do not treat the installed public pack name as the service owner

#### Scenario: Direct Project Operator Session invocation is accepted
- **WHEN** a Project Operator Session invokes `setup-agent-env` or a mutating direct subcommand
- **THEN** the service may proceed after selected Project, Research Topic, Topic Workspace, topic env predecessor evidence, authoritative Agent Name plan, and mutation scope are confirmed
- **AND** it records the requester and confirmation source in the output

#### Scenario: Service refs are recorded when available
- **WHEN** the invocation includes Service Request refs, support Artifact refs, or Provenance refs
- **THEN** the service records those refs in its output and in the derived agent env gate execution log as available

#### Scenario: Missing service refs do not block direct setup
- **WHEN** no Service Request, support Artifact, or Provenance refs are available
- **THEN** the service still may perform confirmed static setup mutation
- **AND** it records changed files, commands run, blockers, and next action as static setup evidence

#### Scenario: Static setup evidence is not runtime truth
- **WHEN** the service records direct invocation or Service Request refs
- **THEN** it still does not create Workspace Runtime records, Agent Team Instance records, Agent Instance records, Houmao launch material, or Execution Adapter material
