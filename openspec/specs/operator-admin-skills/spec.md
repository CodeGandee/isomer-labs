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
The repository SHALL validate operator/admin skill structure, command surfaces, and naming separately from research-paradigm skill validation.

#### Scenario: Operator validation checks structure
- **WHEN** the operator skill validation runs
- **THEN** it confirms each `skillset/operator/isomer-admin-*` folder has a valid `SKILL.md`, valid frontmatter, expected manifest metadata, and directly linked local references when present

#### Scenario: Operator validation checks old active names
- **WHEN** the operator skill validation scans active docs, team profiles, fixtures, and skill manifests
- **THEN** it fails if a migrated operator skill is still referenced by its old active `isomer-rsch-*` name outside historical provenance or archived change text

#### Scenario: Repository skill validation covers operator skills
- **WHEN** a developer or agent runs the repository skill validation command
- **THEN** validation covers the research, operator, and service skillsets or clearly prints the separate commands required to validate each skillset

#### Scenario: Operator validation checks Topic Creator finalization surface
- **WHEN** operator skill validation scans `skillset/operator/isomer-admin-topic-creator`
- **THEN** it requires local `references/finalize.md`, `references/step-by-step.md`, and `references/run-to.md` subcommand pages, user-facing command guidance for `finalize`, `step-by-step`, and `run-to`, and references to `topic.workspace.summary`
- **AND** it rejects active Topic Creator command guidance that lists `start-manual-research` as a subcommand
- **AND** it rejects terminal Topic Creator guidance that includes next-step routing, manual research start-pack handoff, or v2 research skill recommendations

#### Scenario: Operator validation checks Topic Creator guided execution
- **WHEN** operator skill validation scans Topic Creator `step-by-step` guidance
- **THEN** it requires wording that the subcommand follows the same main workflow order as `fast-forward`
- **AND** it requires per-step preview, option table, recommended choice, open question, and user acknowledgement guidance
- **AND** it fails if `step-by-step` can mutate a workflow step before user acknowledgement

#### Scenario: Operator validation checks Topic Creator run-to execution
- **WHEN** operator skill validation scans Topic Creator `run-to` guidance
- **THEN** it requires wording that the subcommand accepts a procedural subcommand target and follows the same readiness ladder as `fast-forward`
- **AND** it requires target exclusion by default, explicit inclusive execution behavior, invalid-target diagnostics, and missing-input blocker behavior
- **AND** it fails if `run-to` accepts helper, misc, unknown, or non-main-workflow targets as executable targets

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

### Requirement: Topic Creator Operator Skill Inventory
The operator/admin skillset SHALL include `isomer-admin-topic-creator` as the canonical user-facing skill for topic initialization to manual-research readiness.

#### Scenario: Topic creator skill is active
- **WHEN** the operator skillset is inspected
- **THEN** it contains `skillset/operator/isomer-admin-topic-creator/` as an active operator skill folder

#### Scenario: Operator docs list topic creator first for topic initialization
- **WHEN** a developer reads `skillset/operator/README.md`
- **THEN** it lists `isomer-admin-topic-creator`
- **AND** it describes the skill as the front door for creating or preparing a Research Topic from empty or partial Project state to manual-research-ready Topic Workspace

#### Scenario: Operator validation covers topic creator
- **WHEN** operator skill validation runs
- **THEN** it validates the topic creator skill with the same frontmatter, UI metadata, local-reference, workflow, and naming checks used for other active operator skills

### Requirement: Deprecated Compatibility Operator Skills
The operator/admin skillset SHALL keep selected compatibility skills available while marking them deprecated for direct user invocation.

#### Scenario: Topic prepare is compatibility-only
- **WHEN** `isomer-admin-topic-prepare` is inspected
- **THEN** its frontmatter marks it deprecated for direct user invocation and names `isomer-admin-topic-creator` as its replacement
- **AND** operator documentation describes it as retained for compatibility and delegated common preparation

#### Scenario: Manual research session is compatibility-only
- **WHEN** `isomer-admin-manual-research-session` is inspected
- **THEN** its frontmatter marks it deprecated for direct user invocation and names `isomer-admin-topic-creator` as its replacement
- **AND** operator documentation describes it as retained for compatibility and delegated start-pack finalization

#### Scenario: Deprecated compatibility skills remain installable during transition
- **WHEN** the core operator skill group is installed
- **THEN** deprecated compatibility skills may remain installed with visible replacement guidance
- **AND** their presence does not make them the recommended front door for new topic initialization

### Requirement: Operator Skills Use Global Isomer CLI
Operator skills SHALL assume they are installed into agents outside the `isomer-labs` repository and SHALL invoke Isomer CLI commands through the globally installed `isomer-cli` executable.

#### Scenario: Operator skill examples avoid repo-local Pixi invocation
- **WHEN** validation scans files under `skillset/operator/`
- **THEN** it reports `pixi run isomer-cli` as invalid command guidance
- **AND** direct command examples use `isomer-cli ...` instead

#### Scenario: Developer skills are exempt
- **WHEN** validation scans files under `skillset/dev/`
- **THEN** repo-local examples may use `pixi run isomer-cli` because dev skills operate inside this repository

#### Scenario: Operator guidance can still mention Topic Workspace Pixi environments
- **WHEN** operator or service skills describe a Topic Workspace Pixi environment owned by the user's research workspace
- **THEN** they may mention Pixi environment setup or Pixi commands for that workspace
- **AND** they still must not invoke Isomer's own CLI as `pixi run isomer-cli`

### Requirement: Operator Skills Exclude Research-Paradigm Bootstrap
Operator admin skills SHALL prepare Project, Topic Workspace, Topic Actor, topology, readiness-summary, approval, materialization, and launch orchestration surfaces without owning research-paradigm-specific bootstrap.

#### Scenario: Operator topic creation does not invoke v2 bootstrap
- **WHEN** active operator skill guidance for topic creation or manual research preparation is inspected
- **THEN** it does not instruct the operator to invoke `isomer-rsch-workspace-mgr-v2`
- **AND** it does not require selected v2 skill sets, v2 `placeholder-bindings.md` files, v2 placeholder binding registries, or accepted research artifact command shapes before reporting Topic Workspace or Topic Actor readiness

#### Scenario: Operator docs route v2 bootstrap to research skills
- **WHEN** operator docs mention research-paradigm-specific bootstrap, placeholder bindings, selected v2 research skills, or accepted research artifact recording
- **THEN** they identify that work as belonging to `skillset/research-paradigm/v2/isomer-rsch-workspace-mgr-v2` or later research-stage skills rather than operator skills

### Requirement: Retired Operator Compatibility Skills Are Removed
The operator admin skillset SHALL retire the deprecated `isomer-admin-topic-prepare` and `isomer-admin-manual-research-session` compatibility skills from active operator inventory.

#### Scenario: Retired compatibility folders are absent
- **WHEN** the active operator skillset is inspected
- **THEN** `skillset/operator/isomer-admin-topic-prepare/` is absent
- **AND** `skillset/operator/isomer-admin-manual-research-session/` is absent

#### Scenario: Active operator references avoid retired skills
- **WHEN** active operator skill docs, manifests, README files, and routing references are inspected
- **THEN** they do not route normal or delegated work to `isomer-admin-topic-prepare` or `isomer-admin-manual-research-session`
- **AND** any historical mention is clearly marked as archived provenance rather than active guidance

#### Scenario: Topic preparation uses current Topic Creator subcommands
- **WHEN** operator docs route topic creation, topic preparation, manual-research-ready setup, or human-orchestrated Topic Actor preparation
- **THEN** they use actual `isomer-admin-topic-creator` subcommands such as `fast-forward`, `step-by-step`, `run-to`, `status`, or `repair`
- **AND** they do not reference nonexistent `create`, `plan`, or `start-manual-research` Topic Creator subcommands

