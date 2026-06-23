## ADDED Requirements

### Requirement: Topic Team Specialization Module Skill
The repository SHALL provide an operator/admin module skill named `isomer-admin-topic-team-specialize` that performs Domain Agent Team Template understanding and topic-specific adaptation as one coherent operator workflow.

#### Scenario: Module skill exists
- **WHEN** the operator skillset is inspected
- **THEN** it contains `skillset/operator/isomer-admin-topic-team-specialize/SKILL.md` with matching frontmatter name and operator-facing instructions

#### Scenario: Module skill is preferred entrypoint
- **WHEN** operator documentation describes specializing a Domain Agent Team Template for a Research Topic
- **THEN** it presents `isomer-admin-topic-team-specialize(project_root, topic_ref_or_prompt, domain_team_template_ref)` as the preferred module-level function before lower-level helper skills

#### Scenario: Module skill remains bounded
- **WHEN** the module skill prepares copied template material, specialization guide, specialization plan, topic edits, or packet inputs
- **THEN** it still requires generic Isomer packet, profile bundle, runtime, and adapter validators before any authoritative materialization or launch-facing operation

### Requirement: Copied Template Root Workflow
The module skill SHALL operate on copied Domain Agent Team Template material inside the selected Research Topic's Topic Agent Team Profile Bundle.

#### Scenario: Template material is copied before adaptation
- **WHEN** a Project Operator Session specializes a Domain Agent Team Template for a Research Topic
- **THEN** it first copies the selected template material into the Topic Agent Team Profile Bundle under the owning Topic Workspace before editing topic-specific template material

#### Scenario: Domain template source is not edited
- **WHEN** the module skill adapts template material for a specific Research Topic
- **THEN** it edits only the copied material inside the Topic Agent Team Profile Bundle and leaves the Domain Agent Team Template source generic

#### Scenario: Topic Workspace teams directory is not used
- **WHEN** the module skill stores copied or adapted topic-team material
- **THEN** it stores that material inside `<topic-workspace>/team-profile/` and does not create a Topic Workspace-local `teams/` directory for the topic team

### Requirement: Team Specialization Guide
The module skill SHALL use `team-specialization-guide.md` in the copied template root to understand the Domain Agent Team Template before planning topic-specific adaptation.

#### Scenario: Existing guide is read first
- **WHEN** copied template material contains `team-specialization-guide.md`
- **THEN** the module skill reads that guide before inspecting other copied template material for adaptation decisions

#### Scenario: Missing guide is generated with marker
- **WHEN** copied template material does not contain `team-specialization-guide.md`
- **THEN** the module skill creates `team-specialization-guide.md` in the copied template root, synthesizes it from the copied material, and includes a clear generated marker stating that no source guide existed

#### Scenario: Guide covers team internals
- **WHEN** a `team-specialization-guide.md` is created or maintained for a Domain Agent Team Template
- **THEN** it describes placeholders and definitions, assumptions, how the team works, contracts used by the team, and at least one example of how the team cooperates

### Requirement: Team Specialization Plan
The module skill SHALL create `team-specialization-plan.md` in the copied template root before adapting copied template material.

#### Scenario: Plan includes adaptation checklist
- **WHEN** the module skill prepares to adapt copied template material for a Research Topic
- **THEN** it writes `team-specialization-plan.md` with a checklist or task list describing the planned topic-specific adaptations before applying those adaptations

#### Scenario: Adaptation follows plan
- **WHEN** copied template material is adapted for the topic
- **THEN** the module skill follows the specialization plan or updates the plan to record why the adaptation changed

#### Scenario: Final report is appended
- **WHEN** adaptation work is complete
- **THEN** `team-specialization-plan.md` contains a `Final Report` section summarizing completed edits, deferred edits, generated-guide status, validation status, packet or profile outputs, and unresolved blockers

### Requirement: deepsci-mini Specialization Guide
The `deepsci-mini` Domain Agent Team Template SHALL include a source `team-specialization-guide.md` so operators do not need to synthesize the guide for the primary supported template.

#### Scenario: deepsci-mini guide exists
- **WHEN** `teams/deepsci-mini/execplan/` is inspected
- **THEN** it contains `team-specialization-guide.md`

#### Scenario: deepsci-mini guide covers required topics
- **WHEN** `teams/deepsci-mini/execplan/team-specialization-guide.md` is inspected
- **THEN** it describes `deepsci-mini` placeholders, assumptions, team workflow, relevant contracts, and an example cooperation flow among lead, scout, and synthesis-reviewer roles

### Requirement: Specialization Artifacts Feed Packet and Profile Drafting
The module skill SHALL produce human-readable specialization artifacts that can feed Topic Team Instantiation Packet and Topic Agent Team Profile Bundle drafting without replacing those structured artifacts.

#### Scenario: Packet inputs are explicit
- **WHEN** the module skill completes topic adaptation
- **THEN** it reports the copied material paths, guide path, plan path, adaptation summary, resolved placeholders, deferrals, and review points needed to build or update a Topic Team Instantiation Packet

#### Scenario: Profile materialization remains separate
- **WHEN** the module skill finishes adaptation
- **THEN** it does not claim that the Topic Agent Team Profile Bundle is approved or launchable unless existing approval provenance and generic profile bundle validation have completed
