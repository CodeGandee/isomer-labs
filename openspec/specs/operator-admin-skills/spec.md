# operator-admin-skills Specification

## Purpose
Define the operator/admin skillset used by Project Operator Sessions and Operator Agents for project control surfaces, approval, materialization, Service Request routing, and team launch orchestration.
## Requirements
### Requirement: Operator Admin Skillset Layout
The repository SHALL provide Project Operator Session and Operator Agent skills under `skillset/operator/` using the `isomer-admin-<purpose>` naming convention.

#### Scenario: Operator skill folders exist
- **WHEN** the operator skillset is inspected
- **THEN** it contains active skill folders for project awareness, service request routing, template inspection, topic context resolution, placeholder reconciliation, topic profile drafting, profile review and approval, profile materialization, and team launch orchestration

#### Scenario: Operator skill names are consistent
- **WHEN** an operator skill folder is inspected
- **THEN** the folder name, `SKILL.md` frontmatter `name`, `agents/openai.yaml` display name, and default prompt use the same `isomer-admin-<purpose>` skill name

#### Scenario: Operator skillset is documented
- **WHEN** a developer reads skillset documentation
- **THEN** it identifies `skillset/operator/` as the installation source for Project Operator Session and Operator Agent skills and lists the supported `isomer-admin-*` skills

### Requirement: Operator Skill Migration Mapping
The system SHALL migrate existing project-operator orchestration skills from `isomer-rsch-*` names to `isomer-admin-*` names without keeping duplicate active skill shims.

#### Scenario: Project awareness skill is renamed
- **WHEN** active skill refs are inspected
- **THEN** Project Operator Session project discovery uses `isomer-admin-project-aware` rather than a research-prefixed operator skill name

#### Scenario: Service request routing skill is renamed
- **WHEN** active skill refs are inspected
- **THEN** Project Operator Session Service Request routing uses `isomer-admin-service-request-route` rather than a research-prefixed operator skill name

#### Scenario: Template inspection skill is renamed
- **WHEN** active skill refs are inspected
- **THEN** operator template inspection uses `isomer-admin-template-inspect` rather than a research-prefixed operator skill name

#### Scenario: Topic context resolution skill is renamed
- **WHEN** active skill refs are inspected
- **THEN** operator topic context resolution uses `isomer-admin-topic-context-resolve` rather than a research-prefixed operator skill name

#### Scenario: Placeholder reconciliation skill is renamed
- **WHEN** active skill refs are inspected
- **THEN** operator placeholder reconciliation uses `isomer-admin-placeholder-reconcile` rather than a research-prefixed operator skill name

#### Scenario: Topic profile drafting skill is renamed
- **WHEN** active skill refs are inspected
- **THEN** operator topic profile drafting uses `isomer-admin-topic-profile-draft` rather than a research-prefixed operator skill name

#### Scenario: Profile review approval skill is renamed
- **WHEN** active skill refs are inspected
- **THEN** operator profile review and approval uses `isomer-admin-profile-review-approval` rather than a research-prefixed operator skill name

#### Scenario: Profile materialization skill is renamed
- **WHEN** active skill refs are inspected
- **THEN** operator profile materialization uses `isomer-admin-profile-materialize` rather than a research-prefixed operator skill name

#### Scenario: Team launch orchestration skill is renamed
- **WHEN** active skill refs are inspected
- **THEN** operator team launch orchestration uses `isomer-admin-team-launch-orchestrate` rather than a research-prefixed operator skill name

### Requirement: Operator Admin Skills Stay Bounded
Operator admin skills SHALL describe project operation, approval, materialization, Service Request routing, and launch orchestration without granting authority to bypass Isomer validation, Gates, or runtime recording.

#### Scenario: Operator skills require validation
- **WHEN** an operator admin skill produces a Topic Team Instantiation Packet, Topic Agent Team Profile Bundle, runtime request, handoff, Service Request, approval provenance, or launch request
- **THEN** the skill requires validation through generic Isomer APIs or CLI before treating the artifact as authoritative

#### Scenario: Operator skills preserve domain boundaries
- **WHEN** an operator admin skill handles Domain Agent Team Templates, Topic Agent Team Profiles, Agent Team Instances, Service Requests, Topic Service Agents, or adapter material
- **THEN** it uses canonical Isomer domain terms and keeps template, profile, runtime team, service team, Project Operator Session, Operator Agent, and Houmao managed-agent concepts distinct

#### Scenario: Operator skills are not research team member skills
- **WHEN** a Topic Agent Team Profile or Agent Team Instance member role maps research-stage skills
- **THEN** it does not install `isomer-admin-*` skills unless the role is explicitly an Operator Agent role

### Requirement: Operator Skill Validation
The repository SHALL validate operator/admin skill structure and naming separately from research-paradigm skill validation.

#### Scenario: Operator validation checks structure
- **WHEN** the operator skill validation runs
- **THEN** it confirms each `skillset/operator/isomer-admin-*` folder has a valid `SKILL.md`, valid frontmatter, expected manifest metadata, and directly linked local references when present

#### Scenario: Operator validation checks old active names
- **WHEN** the operator skill validation scans active docs, team profiles, fixtures, and skill manifests
- **THEN** it fails if a migrated operator skill is still referenced by its old active `isomer-rsch-*` name outside historical provenance or archived change text

#### Scenario: Repository skill validation covers operator skills
- **WHEN** a developer or agent runs the repository skill validation command
- **THEN** validation covers the research, operator, and service skillsets or clearly prints the separate commands required to validate each skillset

### Requirement: Topic Workspace Manager Operator Skill
The operator/admin skillset SHALL include `isomer-admin-topic-workspace-mgr` as the operator surface for Git-backed Topic Workspace repository and Agent Workspace worktree preparation, and it SHALL describe non-main topic repositories as supporting repositories resolved through the semantic storage contract.

#### Scenario: Topic workspace manager skill is active
- **WHEN** the operator skillset is inspected
- **THEN** it contains `skillset/operator/isomer-admin-topic-workspace-mgr/` as an active operator skill folder

#### Scenario: Operator docs list topic workspace manager
- **WHEN** a developer reads `skillset/operator/README.md`
- **THEN** it lists `isomer-admin-topic-workspace-mgr` and describes it as the skill for preparing and validating `repos/topic-main` plus per-agent Agent Workspace worktrees

#### Scenario: Operator validation covers topic workspace manager
- **WHEN** operator skill validation runs
- **THEN** it validates the topic workspace manager skill with the same frontmatter, UI metadata, local-reference, workflow, and naming checks used for other active operator skills

#### Scenario: Topic workspace manager stays bounded
- **WHEN** the topic workspace manager skill reports prepared workspaces
- **THEN** it does not claim Agent Team Instance creation, Workspace Runtime mutation, Houmao launch, adapter launch material readiness, or runtime team readiness

#### Scenario: Additional topic repositories are external support surfaces
- **WHEN** the topic workspace manager skill documents or registers an additional non-main topic repository
- **THEN** it uses `topic.repos.<group...>.<repo-name>` semantic labels with `storage_profile = "topic_repo"`
- **AND** it describes `repos/extern/...` as the default physical location for helper-created non-main topic repositories
- **AND** it does not describe non-main repositories as Agent Workspace worktree sources

