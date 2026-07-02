## MODIFIED Requirements

### Requirement: V2 Research Workspace Manager Skill
The research-paradigm skillset SHALL include an `isomer-rsch-workspace-mgr-v2` skill that performs research-specific Topic Workspace bootstrap after Topic Team Specialization and full Topic Workspace initialization.

#### Scenario: Workspace manager skill exists
- **WHEN** the v2 research-paradigm skillset is inspected
- **THEN** it contains `skillset/research-paradigm/v2/isomer-rsch-workspace-mgr-v2/SKILL.md` with valid frontmatter, workflow, reference routing, fallback guidance, and an `agents/openai.yaml` manifest that invokes `$isomer-rsch-workspace-mgr-v2`

#### Scenario: Workspace manager runs after specialization
- **WHEN** the skill explains its entry conditions
- **THEN** it requires a selected Research Topic, a fully initialized Topic Workspace, completed Topic Team Specialization material, Workspace Runtime readiness, and Agent Workspace context before ordinary v2 research skills rely on its bootstrap outputs

#### Scenario: Workspace manager is distinct from operator topic management
- **WHEN** the skill describes its boundary
- **THEN** it states that `isomer-admin-topic-mgr` remains the operator initialized-topic manager while `isomer-rsch-workspace-mgr-v2` owns research placeholder binding and v2 storage bootstrap guidance

#### Scenario: Topic Service Master is optional
- **WHEN** the skill describes the actor that performs bootstrap
- **THEN** it names the Topic Service Master as the preferred topic-workspace manager when started and states that the Project Operator Session or Operator Agent performs the same bounded work when no Topic Service Master is running

## ADDED Requirements

### Requirement: V2 Package Setup Routes to Topic Manager
Active research-paradigm v2 skills SHALL route package installation, package update, package removal, and package verification needs to `isomer-admin-topic-mgr` environment commands instead of installing packages directly.

#### Scenario: Missing Python package routes to topic manager
- **WHEN** a v2 research skill detects that a required Python package is missing from the selected Topic Workspace environment
- **THEN** it stops before the dependent research action and routes a natural-language package request to `$isomer-admin-topic-mgr env-install-packages`
- **AND** it does not create a local virtual environment, run ambient `pip`, or mutate machine-global Python state

#### Scenario: Missing R package routes to topic manager
- **WHEN** a v2 research skill detects that a required R package is missing from the selected Topic Workspace environment
- **THEN** it stops before the dependent render, analysis, or verification action and routes a natural-language package request to `$isomer-admin-topic-mgr env-install-packages`

#### Scenario: Package update or removal request routes to topic manager
- **WHEN** a v2 research skill needs a package update, package downgrade, or package removal to proceed safely
- **THEN** it routes the request to `$isomer-admin-topic-mgr env-update-packages` or `$isomer-admin-topic-mgr env-remove-packages`
- **AND** it includes the research purpose and desired verification evidence in the request

#### Scenario: Package readiness evidence is consumed after verification
- **WHEN** `isomer-admin-topic-mgr` reports package mutation or verification evidence with passing checks
- **THEN** the v2 research skill may continue the blocked workflow from the same selected Topic Workspace context
- **AND** it treats failed or skipped verification as a blocker rather than silently switching environments
