# operator-admin-skills Specification

## Purpose
Define the operator skillset used by Project Operator Sessions and Operator Agents for project control surfaces, approval, materialization, Service Request routing, and team launch orchestration.
## Requirements
### Requirement: Operator Skillset Layout
The repository SHALL provide Project Operator Session and Operator Agent skills under `skillset/operator/` using the `isomer-op-<purpose>` naming convention.

#### Scenario: Operator skill folders exist
- **WHEN** the operator skillset is inspected
- **THEN** it contains active skill folders for project awareness, service request routing, template inspection, topic context resolution, placeholder reconciliation, topic profile drafting, profile review and approval, profile materialization, and team launch orchestration
- **AND** it does not contain an active `isomer-op-houmao-interop` folder

#### Scenario: Operator skill names are consistent
- **WHEN** an operator skill folder is inspected
- **THEN** the folder name, `SKILL.md` frontmatter `name`, `agents/openai.yaml` display name, and default prompt use the same `isomer-op-<purpose>` skill name

#### Scenario: Operator skillset is documented
- **WHEN** a developer reads skillset documentation
- **THEN** it identifies `skillset/operator/` as the installation source for Project Operator Session and Operator Agent skills and lists the supported `isomer-op-*` skills
- **AND** it does not list `isomer-op-houmao-interop` as a user-facing operator owner skill

#### Scenario: Houmao interop is routed to service
- **WHEN** operator guidance describes Houmao loop, runtime, launch profile, mailbox, gateway, or template-mapping support
- **THEN** it routes bounded support to `isomer-srv-houmao-interop`
- **AND** it keeps the visible first command on the appropriate user-facing operator workflow such as `isomer-op-project-mgr` or `isomer-op-topic-team-specialize`

### Requirement: Operator Skill Migration Mapping
The system SHALL migrate existing project-operator orchestration skills from previous research-prefixed operator names to `isomer-op-*` names without keeping duplicate active skill shims.

#### Scenario: Project awareness skill is renamed
- **WHEN** active skill refs are inspected
- **THEN** Project Operator Session project discovery uses `isomer-op-project-aware` rather than a research-prefixed operator skill name

#### Scenario: Service request routing skill is renamed
- **WHEN** active skill refs are inspected
- **THEN** Project Operator Session Service Request routing uses `isomer-op-service-request-route` rather than a research-prefixed operator skill name

#### Scenario: Template inspection skill is renamed
- **WHEN** active skill refs are inspected
- **THEN** operator template inspection uses `isomer-op-template-inspect` rather than a research-prefixed operator skill name

#### Scenario: Topic context resolution skill is renamed
- **WHEN** active skill refs are inspected
- **THEN** operator topic context resolution uses `isomer-op-topic-context-resolve` rather than a research-prefixed operator skill name

#### Scenario: Placeholder reconciliation skill is renamed
- **WHEN** active skill refs are inspected
- **THEN** operator placeholder reconciliation uses `isomer-op-placeholder-reconcile` rather than a research-prefixed operator skill name

#### Scenario: Topic profile drafting skill is renamed
- **WHEN** active skill refs are inspected
- **THEN** operator topic profile drafting uses `isomer-op-topic-profile-draft` rather than a research-prefixed operator skill name

#### Scenario: Profile review approval skill is renamed
- **WHEN** active skill refs are inspected
- **THEN** operator profile review and approval uses `isomer-op-profile-review-approval` rather than a research-prefixed operator skill name

#### Scenario: Profile materialization skill is renamed
- **WHEN** active skill refs are inspected
- **THEN** operator profile materialization uses `isomer-op-profile-materialize` rather than a research-prefixed operator skill name

#### Scenario: Team launch orchestration skill is renamed
- **WHEN** active skill refs are inspected
- **THEN** operator team launch orchestration uses `isomer-op-team-launch-orchestrate` rather than a research-prefixed operator skill name

### Requirement: Operator Skills Stay Bounded
Operator skills SHALL describe project operation, approval, materialization, Service Request routing, and launch orchestration without granting authority to bypass Isomer validation, Gates, or runtime recording.

#### Scenario: Operator skills require validation
- **WHEN** an operator skill produces a Topic Team Instantiation Packet, Topic Agent Team Profile Bundle, runtime request, handoff, Service Request, approval provenance, or launch request
- **THEN** the skill requires validation through generic Isomer APIs or CLI before treating the artifact as authoritative

#### Scenario: Operator skills preserve domain boundaries
- **WHEN** an operator skill handles Domain Agent Team Templates, Topic Agent Team Profiles, Agent Team Instances, Service Requests, Topic Service Agents, or adapter material
- **THEN** it uses canonical Isomer domain terms and keeps template, profile, runtime team, service team, Project Operator Session, Operator Agent, and Houmao managed-agent concepts distinct

#### Scenario: Operator skills are not research team member skills
- **WHEN** a Topic Agent Team Profile or Agent Team Instance member role maps research-stage skills
- **THEN** it does not install `isomer-op-*` skills unless the role is explicitly an Operator Agent role

### Requirement: Operator Skill Validation
The repository SHALL validate operator skill structure, command surfaces, and naming separately from research-paradigm and service skill validation.

#### Scenario: Operator validation checks structure
- **WHEN** the operator skill validation runs
- **THEN** it confirms each `skillset/operator/isomer-op-*` folder has a valid `SKILL.md`, valid frontmatter, expected manifest metadata, and directly linked local references when present
- **AND** it does not require or accept `skillset/operator/isomer-op-houmao-interop` as part of the active operator inventory

#### Scenario: Operator validation checks old active names
- **WHEN** the operator skill validation scans active docs, team profiles, fixtures, and skill manifests
- **THEN** it fails if a migrated operator skill is still referenced by its old active `isomer-deepsci-*` name outside historical provenance or archived change text
- **AND** it fails if current operator guidance presents `isomer-op-houmao-interop` as an active invokable skill outside historical provenance or migration-only text

#### Scenario: Repository skill validation covers operator skills
- **WHEN** a developer or agent runs the repository skill validation command
- **THEN** validation covers the research, operator, service, and misc skillsets or clearly prints the separate commands required to validate each skillset

#### Scenario: Operator validation checks Topic Creator finalization surface
- **WHEN** operator skill validation scans `skillset/operator/isomer-op-topic-creator`
- **THEN** it requires local `references/finalize.md`, `references/step-by-step.md`, and `references/run-to.md` subcommand pages, user-facing command guidance for `finalize`, `step-by-step`, and `run-to`, and references to `topic.workspace.summary`
- **AND** it rejects active Topic Creator command guidance that lists `start-manual-research` as a subcommand
- **AND** it rejects terminal Topic Creator guidance that includes next-step routing, manual research start-pack handoff, or production DeepSci research skill recommendations

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

### Requirement: Topic Manager Operator Skill
The operator skillset SHALL include `isomer-op-topic-mgr` as the only operator skill surface for managing initialized Research Topics after Topic Creator handoff.

#### Scenario: Topic manager skill is active
- **WHEN** the operator skillset is inspected
- **THEN** it contains `skillset/operator/isomer-op-topic-mgr/` as an active operator skill folder
- **AND** it does not contain `skillset/operator/isomer-op-topic-workspace-mgr/`

#### Scenario: Operator docs list only topic manager
- **WHEN** a developer reads `skillset/operator/README.md`
- **THEN** it lists `isomer-op-topic-mgr`
- **AND** it describes the skill as the initialized-topic manager for storage, Topic Actors, topic agent team topology, environment mutation, environment verification, and diagnostics
- **AND** it does not describe `isomer-op-topic-workspace-mgr` as a compatibility wrapper or active fallback

#### Scenario: Operator validation covers topic manager and rejects old folder
- **WHEN** operator skill validation runs
- **THEN** it validates the topic manager skill with frontmatter, UI metadata, local reference, workflow, scoped subcommand, output-contract, and guardrail checks
- **AND** it fails if `skillset/operator/isomer-op-topic-workspace-mgr/` exists
- **AND** it fails if active operator docs, manifests, or routing guidance present `isomer-op-topic-workspace-mgr` as invokable

#### Scenario: Topic manager stays bounded
- **WHEN** the topic manager reports initialized-topic management results
- **THEN** it does not claim Research Topic initialization, research-paradigm production DeepSci bootstrap, Agent Team Instance creation, Workspace Runtime mutation, Houmao launch, adapter launch material readiness, or runtime team readiness

### Requirement: Retired Workspace Manager Is Excluded From Operator Inventory
The operator skillset SHALL exclude the retired `isomer-op-topic-workspace-mgr` skill from active manifests, generated skill lists, and validation fixtures.

#### Scenario: Manifest excludes retired skill
- **WHEN** `skillset/manifest.toml` is inspected
- **THEN** it includes `operator/isomer-op-topic-mgr`
- **AND** it does not include `operator/isomer-op-topic-workspace-mgr`

#### Scenario: Validation fixtures do not recreate retired wrapper
- **WHEN** unit tests build valid operator skill fixtures
- **THEN** the fixtures include `isomer-op-topic-mgr`
- **AND** they do not create a valid `isomer-op-topic-workspace-mgr` wrapper fixture

#### Scenario: Revived old folder is rejected
- **WHEN** a test or real repository contains `skillset/operator/isomer-op-topic-workspace-mgr/`
- **THEN** operator skill validation reports that the skill is retired and must not be a standalone skill

### Requirement: Topic Creator Operator Skill Inventory
The operator skillset SHALL include `isomer-op-topic-creator` as the canonical user-facing skill for topic initialization to manual-research readiness.

#### Scenario: Topic creator skill is active
- **WHEN** the operator skillset is inspected
- **THEN** it contains `skillset/operator/isomer-op-topic-creator/` as an active operator skill folder

#### Scenario: Operator docs list topic creator first for topic initialization
- **WHEN** a developer reads `skillset/operator/README.md`
- **THEN** it lists `isomer-op-topic-creator`
- **AND** it describes the skill as the front door for creating or preparing a Research Topic from empty or partial Project state to manual-research-ready Topic Workspace

#### Scenario: Operator validation covers topic creator
- **WHEN** operator skill validation runs
- **THEN** it validates the topic creator skill with the same frontmatter, UI metadata, local-reference, workflow, and naming checks used for other active operator skills

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
Operator skills SHALL prepare Project, Topic Workspace, Topic Actor, topology, readiness-summary, approval, materialization, and launch orchestration surfaces without owning research-paradigm-specific bootstrap.

#### Scenario: Operator topic creation does not invoke production DeepSci bootstrap
- **WHEN** active operator skill guidance for topic creation or manual research preparation is inspected
- **THEN** it does not instruct the operator to invoke `isomer-deepsci-workspace-mgr`
- **AND** it does not require selected production DeepSci skill sets, production DeepSci `placeholder-bindings.md` files, production DeepSci placeholder binding registries, or accepted research artifact command shapes before reporting Topic Workspace or Topic Actor readiness

#### Scenario: Operator docs route production DeepSci bootstrap to research skills
- **WHEN** operator docs mention research-paradigm-specific bootstrap, placeholder bindings, selected production DeepSci research skills, or accepted research artifact recording
- **THEN** they identify that work as belonging to `skillset/research-paradigm/deepsci/isomer-deepsci-workspace-mgr` or later research-stage skills rather than operator skills

### Requirement: Retired Operator Compatibility Skills Are Removed
The operator skillset SHALL retire the deprecated `isomer-op-topic-prepare` and `isomer-op-manual-research-session` compatibility skills from active operator inventory.

#### Scenario: Retired compatibility folders are absent
- **WHEN** the active operator skillset is inspected
- **THEN** `skillset/operator/isomer-op-topic-prepare/` is absent
- **AND** `skillset/operator/isomer-op-manual-research-session/` is absent

#### Scenario: Active operator references avoid retired skills
- **WHEN** active operator skill docs, manifests, README files, and routing references are inspected
- **THEN** they do not route normal or delegated work to `isomer-op-topic-prepare` or `isomer-op-manual-research-session`
- **AND** any historical mention is clearly marked as archived provenance rather than active guidance

#### Scenario: Topic preparation uses current Topic Creator subcommands
- **WHEN** operator docs route topic creation, topic preparation, manual-research-ready setup, or human-orchestrated Topic Actor preparation
- **THEN** they use actual `isomer-op-topic-creator` subcommands such as `fast-forward`, `step-by-step`, `run-to`, `status`, or `repair`
- **AND** they do not reference nonexistent `create`, `plan`, or `start-manual-research` Topic Creator subcommands

### Requirement: Welcome Operator Skill Inventory
The operator/admin skillset SHALL include `isomer-admin-welcome` as the user-facing action menu and path chooser for supported Isomer Labs operator workflows.

#### Scenario: Welcome skill is active
- **WHEN** the operator skillset is inspected
- **THEN** it contains `skillset/operator/isomer-admin-welcome/` as an active operator skill folder
- **AND** the folder name, `SKILL.md` frontmatter `name`, `agents/openai.yaml` display name, and default prompt use `isomer-admin-welcome`

#### Scenario: Operator docs list welcome entrypoint
- **WHEN** a developer reads `skillset/operator/README.md`
- **THEN** it lists `isomer-admin-welcome`
- **AND** it describes the skill as the action-oriented menu and path chooser that tells users what Isomer Labs can do, shows typical usage paths such as `start-research-manually` and `start-research-by-agent-team`, and names which owner skill to invoke directly

#### Scenario: Manifest includes welcome and excludes retired compatibility entries
- **WHEN** `skillset/manifest.toml` is inspected
- **THEN** it includes `operator/isomer-admin-welcome`
- **AND** it does not include `operator/isomer-admin-topic-prepare`
- **AND** it does not include `operator/isomer-admin-manual-research-session`

#### Scenario: Operator validation covers welcome
- **WHEN** operator skill validation runs
- **THEN** it validates the welcome skill with frontmatter, UI metadata, local-reference, workflow, subcommand, output-contract, read-only posture, active-owner routing, and retired-skill exclusion checks

### Requirement: Operator Namespace Rename Inventory
The operator skillset SHALL expose the renamed active operator inventory without duplicate active compatibility wrappers.

#### Scenario: Active operator inventory uses op names
- **WHEN** the operator skillset is inspected
- **THEN** it contains `isomer-op-project-mgr`, `isomer-op-topic-creator`, `isomer-op-topic-mgr`, `isomer-op-topic-team-specialize`, and `isomer-op-welcome`
- **AND** it does not contain active `isomer-admin-project-mgr`, `isomer-admin-topic-creator`, `isomer-admin-topic-mgr`, `isomer-admin-topic-team-specialize`, `isomer-admin-welcome`, or `isomer-admin-houmao-interop` folders
- **AND** it does not contain active `isomer-op-houmao-interop`

#### Scenario: Active routing uses op names
- **WHEN** active operator guidance routes between operator skills
- **THEN** it invokes the renamed `isomer-op-*` skill names
- **AND** it routes bounded Houmao interop support to `isomer-srv-houmao-interop`
- **AND** it treats old `isomer-admin-*` names as historical or migration-only references
