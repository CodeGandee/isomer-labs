## MODIFIED Requirements

### Requirement: Research Paradigm Skillset Layout
The project SHALL provide a reusable production DeepSci research-paradigm skillset under `skillset/research-paradigm/deepsci/` using Codex skill folder layout and the `isomer-deepsci-<purpose>` naming convention for DeepScientist-derived domain extension skills.

#### Scenario: Production DeepSci root exists
- **WHEN** the research-paradigm skillset is inspected
- **THEN** it contains production skill folders under `skillset/research-paradigm/deepsci/`
- **AND** it does not contain active retired-generation or temporary-generation skill roots

#### Scenario: Retired v1 skill folders are absent
- **WHEN** the active research-paradigm skillset is inspected
- **THEN** retired first-generation research skill folders are absent
- **AND** active docs do not route users to `isomer-rsch-*-v1` or other retired-generation skills

#### Scenario: Production DeepSci skill folders exist
- **WHEN** the production DeepSci research-paradigm skillset is inspected
- **THEN** it contains `isomer-deepsci-shared` and folders for scout, baseline, idea, optimize, experiment, analysis, decision, finalize, science, write, review, rebuttal, paper-outline, paper-plot, figure-polish, nature-data, nature-figure, nature-paper2ppt, nature-polishing, and workspace-mgr

#### Scenario: Migrated production DeepSci companion skills keep bounded traceability material
- **WHEN** a refactor-migrated production DeepSci companion skill is inspected
- **THEN** it MAY contain `migrate/`, `org/analysis/`, `org/src/`, and passive `templates/` material for migration review and provenance
- **AND** active execution guidance remains in `SKILL.md`, `agents/openai.yaml`, directly linked `references/`, active `assets/`, and active `scripts/`

#### Scenario: Skill frontmatter is valid
- **WHEN** each production DeepSci research-stage skill's `SKILL.md` is inspected
- **THEN** the YAML frontmatter contains `name` and `description` fields
- **AND** the `name` field matches the `isomer-deepsci-<purpose>` folder name

#### Scenario: Skill manifest exists when a skill is packaged independently
- **WHEN** an extracted research-stage skill is packaged as a standalone skill bundle
- **THEN** it includes an `agents/openai.yaml` manifest with UI-facing metadata

#### Scenario: Standalone skill bundle is self-contained
- **WHEN** an extracted research-stage skill is packaged as a standalone skill bundle
- **THEN** its active `SKILL.md` and directly linked active resources do not require files outside that skill's directory

#### Scenario: Old active skill names are removed
- **WHEN** active research-paradigm skill folders and docs are inspected
- **THEN** they do not use `isomer-labs-research-*` or `isomer-rsch-*` as active skill folder names, frontmatter names, manifests, or role mappings

#### Scenario: Operator skills are excluded
- **WHEN** active research-paradigm skill folders and docs are inspected
- **THEN** Project Operator Session and Operator Agent orchestration skills are not stored or named as `isomer-deepsci-*` skills and instead use the operator skillset

### Requirement: Production DeepSci Research Workspace Manager
The research-paradigm skillset SHALL include an `isomer-deepsci-workspace-mgr` skill that performs research-specific Topic Workspace bootstrap after Topic Team Specialization and full Topic Workspace initialization.

#### Scenario: Workspace manager skill exists
- **WHEN** the production DeepSci research-paradigm skillset is inspected
- **THEN** it contains `skillset/research-paradigm/deepsci/isomer-deepsci-workspace-mgr/SKILL.md` with valid frontmatter, workflow, reference routing, fallback guidance, and an `agents/openai.yaml` manifest that invokes `$isomer-deepsci-workspace-mgr`

#### Scenario: Workspace manager runs after specialization
- **WHEN** the skill explains its entry conditions
- **THEN** it requires a selected Research Topic, a fully initialized Topic Workspace, completed Topic Team Specialization material, Workspace Runtime readiness, and Agent Workspace context before ordinary production DeepSci research skills rely on its bootstrap outputs

#### Scenario: Workspace manager is distinct from operator topic management
- **WHEN** the skill describes its boundary
- **THEN** it states that `isomer-op-topic-mgr` remains the operator initialized-topic manager while `isomer-deepsci-workspace-mgr` owns research placeholder binding and production DeepSci storage bootstrap guidance

#### Scenario: Topic Service Master is optional
- **WHEN** the skill describes the actor that performs bootstrap
- **THEN** it names the Topic Service Master as the preferred topic-workspace manager when started and states that the Project Operator Session or Operator Agent performs the same bounded work when no Topic Service Master is running

### Requirement: Production DeepSci Package Routing
Active research-paradigm production DeepSci skills SHALL route package installation, package update, package removal, and package verification needs to `isomer-op-topic-mgr` environment commands instead of installing packages directly.

#### Scenario: Missing Python package routes to topic manager
- **WHEN** a production DeepSci research skill detects that a required Python package is missing from the selected Topic Workspace environment
- **THEN** it stops before the dependent research action and routes a natural-language package request to `$isomer-op-topic-mgr env-install-packages`
- **AND** it does not create a local virtual environment, run ambient `pip`, or mutate machine-global Python state

#### Scenario: Missing R package routes to topic manager
- **WHEN** a production DeepSci research skill detects that a required R package is missing from the selected Topic Workspace environment
- **THEN** it stops before the dependent render, analysis, or verification action and routes a natural-language package request to `$isomer-op-topic-mgr env-install-packages`

#### Scenario: Package update or removal request routes to topic manager
- **WHEN** a production DeepSci research skill needs a package update, package downgrade, or package removal to proceed safely
- **THEN** it routes the request to `$isomer-op-topic-mgr env-update-packages` or `$isomer-op-topic-mgr env-remove-packages`
- **AND** it includes the research purpose and desired verification evidence in the request

#### Scenario: Package readiness evidence is consumed after verification
- **WHEN** `isomer-op-topic-mgr` reports package mutation or verification evidence with passing checks
- **THEN** the production DeepSci research skill may continue the blocked workflow from the same selected Topic Workspace context
