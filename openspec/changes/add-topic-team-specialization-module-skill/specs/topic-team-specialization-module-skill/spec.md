## ADDED Requirements

### Requirement: Skill Creator Bundle Layout
The repository SHALL provide a lean operator skill bundle named `isomer-admin-topic-team-specialize` for Topic Team Specialization.

#### Scenario: Skill bundle exists
- **WHEN** the operator skillset is inspected
- **THEN** it contains `skillset/operator/isomer-admin-topic-team-specialize/SKILL.md` and `skillset/operator/isomer-admin-topic-team-specialize/agents/openai.yaml`

#### Scenario: Frontmatter is minimal
- **WHEN** `skillset/operator/isomer-admin-topic-team-specialize/SKILL.md` is inspected
- **THEN** its YAML frontmatter contains `name: isomer-admin-topic-team-specialize` and a trigger-oriented `description`, with no extra frontmatter fields

#### Scenario: UI metadata is present
- **WHEN** `skillset/operator/isomer-admin-topic-team-specialize/agents/openai.yaml` is inspected
- **THEN** it contains `interface.display_name`, `interface.short_description`, and `interface.default_prompt`, and the default prompt names `$isomer-admin-topic-team-specialize`

#### Scenario: Eval scaffolding is absent
- **WHEN** the `isomer-admin-topic-team-specialize` skill folder is inspected
- **THEN** it does not contain an `evals/` directory or auxiliary docs that are not needed to execute the skill

#### Scenario: Local subskills exist
- **WHEN** the `isomer-admin-topic-team-specialize` skill folder is inspected
- **THEN** it contains local subskill pages for project awareness, template inspection, topic context resolution, Service Request routing, placeholder reconciliation, topic profile drafting, profile review approval, profile materialization, and team launch orchestration under `references/`

#### Scenario: Incorporated standalone skills are absent
- **WHEN** the operator skillset is inspected
- **THEN** it does not contain standalone `isomer-admin-project-aware`, `isomer-admin-template-inspect`, `isomer-admin-topic-context-resolve`, `isomer-admin-service-request-route`, `isomer-admin-placeholder-reconcile`, `isomer-admin-topic-profile-draft`, `isomer-admin-profile-review-approval`, `isomer-admin-profile-materialize`, or `isomer-admin-team-launch-orchestrate` skill folders

### Requirement: Imsight Workflow Entrypoint
The module skill SHALL follow the Imsight skill-entrypoint structure.

#### Scenario: Workflow section is near the top
- **WHEN** `SKILL.md` is inspected
- **THEN** it contains a near-top `## Workflow` section before detailed guide, plan, helper, output, or guardrail sections

#### Scenario: Workflow steps are numbered
- **WHEN** the `## Workflow` section is inspected
- **THEN** it uses numbered steps that state concise actions for resolving context, copying template material, reading or creating guide material, planning, adapting, reporting, and preserving validation boundaries

#### Scenario: Detailed rules are separated
- **WHEN** generated-guide rules, plan structure, subskill routing, output fields, or guardrails require detail
- **THEN** `SKILL.md` keeps that detail in named sections outside the concise workflow steps

#### Scenario: Freeform fallback exists
- **WHEN** the user's task does not map cleanly to the default workflow steps
- **THEN** the skill tells the agent to use its native planning tool to build and execute a step-by-step plan from the project context, copied-template constraints, subskills, output contract, and guardrails

#### Scenario: Subskills have Imsight workflows
- **WHEN** each local subskill page is inspected
- **THEN** it contains a near-top `## Workflow` section, numbered workflow steps, and a fallback for tasks that do not map cleanly to the default steps

### Requirement: Subskill Incorporation
The module skill SHALL incorporate former helper-skill behavior as local subskills instead of requiring normal workflow calls to separate skills.

#### Scenario: Entrypoint routes to local subskills
- **WHEN** `SKILL.md` describes project awareness, template inspection, topic context resolution, Service Request routing, placeholder reconciliation, topic profile drafting, profile review approval, profile materialization, or team launch orchestration
- **THEN** it routes the agent to local subskill pages through a `## Subskills` table

#### Scenario: Normal specialization avoids external skill calls
- **WHEN** the module skill performs its normal Topic Team Specialization workflow
- **THEN** it uses local subskills for project awareness, template inspection, topic context resolution, Service Request routing, placeholder reconciliation, and topic profile drafting instead of asking the user to invoke separate operator skills

#### Scenario: Boundary operations remain explicit
- **WHEN** approval, materialization, or launch work is requested after specialization
- **THEN** the module skill uses the local profile review approval, profile materialization, or team launch orchestration subskill and preserves all validation and provenance boundaries

### Requirement: Topic Team Specialization Workflow
The module skill SHALL guide a Project Operator Session or Operator Agent through adapting one Domain Agent Team Template for one Research Topic.

#### Scenario: Module function is explicit
- **WHEN** operator documentation or skill text describes the workflow
- **THEN** it presents `isomer-admin-topic-team-specialize(project_root, topic_ref_or_prompt, domain_team_template_ref)` as the preferred module-level entrypoint

#### Scenario: Template material is copied before adaptation
- **WHEN** a Project Operator Session specializes a Domain Agent Team Template for a Research Topic
- **THEN** it copies selected template material into the Topic Agent Team Profile Bundle under the owning Topic Workspace before editing topic-specific material

#### Scenario: Source template remains generic
- **WHEN** copied template material is adapted for a Research Topic
- **THEN** the module skill edits only copied material inside the Topic Agent Team Profile Bundle and leaves the Domain Agent Team Template source generic

#### Scenario: Topic Workspace teams directory is not used
- **WHEN** the module skill stores copied or adapted topic-team material
- **THEN** it stores that material inside `<topic-workspace>/team-profile/` and does not create a Topic Workspace-local `teams/` directory

### Requirement: Specialization Guide and Plan Artifacts
The module skill SHALL use `team-specialization-guide.md` and `team-specialization-plan.md` inside the copied template root to make Topic Team Specialization auditable.

#### Scenario: Existing guide is read first
- **WHEN** copied template material contains `team-specialization-guide.md`
- **THEN** the module skill reads that guide before inspecting other copied template material for adaptation decisions

#### Scenario: Missing guide is generated with marker
- **WHEN** copied template material does not contain `team-specialization-guide.md`
- **THEN** the module skill creates `team-specialization-guide.md` in the copied template root, synthesizes it from copied material, and includes a clear generated marker stating that no source guide existed

#### Scenario: Plan exists before adaptation
- **WHEN** the module skill prepares to adapt copied template material
- **THEN** it writes `team-specialization-plan.md` in the copied template root with a checklist or task list describing planned topic-specific adaptations before applying those adaptations

#### Scenario: Final report is recorded
- **WHEN** adaptation work is complete
- **THEN** `team-specialization-plan.md` contains a `Final Report` section summarizing completed edits, deferred edits, generated-guide status, validation status, packet or profile outputs, and unresolved blockers

### Requirement: deepsci-mini Source Guide
The `deepsci-mini` Domain Agent Team Template SHALL include a source `team-specialization-guide.md` for the primary supported template.

#### Scenario: deepsci-mini guide exists
- **WHEN** `teams/deepsci-mini/execplan/` is inspected
- **THEN** it contains `team-specialization-guide.md`

#### Scenario: deepsci-mini guide covers required topics
- **WHEN** `teams/deepsci-mini/execplan/team-specialization-guide.md` is inspected
- **THEN** it describes placeholders, assumptions, team workflow, relevant contracts, and an example cooperation flow among lead, scout, and synthesis-reviewer roles

### Requirement: Packet and Profile Boundaries
The module skill SHALL produce human-readable specialization artifacts that can feed Topic Team Instantiation Packet and Topic Agent Team Profile Bundle drafting without replacing those structured artifacts.

#### Scenario: Packet inputs are explicit
- **WHEN** the module skill completes topic adaptation
- **THEN** it reports copied material paths, guide path, plan path, adaptation summary, resolved placeholders, deferrals, review points, and validation refs needed to build or update a Topic Team Instantiation Packet

#### Scenario: Profile materialization remains separate
- **WHEN** the module skill finishes adaptation
- **THEN** it does not claim that the Topic Agent Team Profile Bundle is approved, materialized, launchable, or attached to an Agent Team Instance unless existing approval provenance and generic validation have completed through their own boundaries

### Requirement: Skill Validation
The implementation SHALL validate the module skill with skill-creator and repository validation surfaces.

#### Scenario: Skill creator validation runs
- **WHEN** the module skill bundle is ready for review
- **THEN** a developer or agent can run `pixi run python /home/huangzhe/.codex/skills/.system/skill-creator/scripts/quick_validate.py skillset/operator/isomer-admin-topic-team-specialize` or the repo-local equivalent and receive a passing result

#### Scenario: Operator skillset validation runs
- **WHEN** `pixi run validate-operator-skills` runs
- **THEN** it accepts the module skill, detects missing required guide, plan, or subskill terms, verifies local subskill workflow structure, and does not require `evals/`

#### Scenario: OpenSpec validation runs
- **WHEN** `openspec validate add-topic-team-specialization-module-skill --strict` runs
- **THEN** the change artifacts validate without schema or scenario-format errors
