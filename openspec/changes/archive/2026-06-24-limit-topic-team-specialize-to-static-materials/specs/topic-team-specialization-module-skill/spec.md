## ADDED Requirements

### Requirement: Static Topic Team Material Boundary
The module skill SHALL focus on static Topic Team material and durable setup preparation, and SHALL exclude live runtime operation.

#### Scenario: Static scope is documented
- **WHEN** the skill entrypoint, help text, workflow text, or operator documentation describes the module purpose
- **THEN** it explains that the skill produces or revises static Topic Team material and durable setup state for one Research Topic from one Domain Agent Team Template

#### Scenario: Environment setup remains static preparation
- **WHEN** `setup-topic-env` is described or executed
- **THEN** the skill treats installed packages, environment files, setup commands, validation records, skipped actions, and blockers as durable static preparation, and does not start live team execution, launch adapters, store credentials, or record live provider state as profile material

#### Scenario: Agent Workspace setup remains static preparation
- **WHEN** `setup-agent-workspace` is described or executed
- **THEN** the skill creates or reports only static Agent Workspace directories, ownership notes, boundary notes, skipped actions, blockers, and validation refs, and does not create Agent Instances, register Workspace Runtime state, or launch agents

#### Scenario: Runtime launch subcommand is absent
- **WHEN** the `isomer-admin-topic-team-specialize` skill folder is inspected
- **THEN** it does not contain `references/launch-team.md`, does not list `launch-team` as a local subcommand, and does not include live launch as a `fast-forward` or `step-by-step` stage

#### Scenario: Static validation stops before live operation
- **WHEN** `validate-topic-team` or `finalize-topic-team` runs
- **THEN** the skill validates or summarizes topic overview material, copied specialization material, setup evidence, Agent Workspace layout, profile material, blockers, deferrals, and next actions without claiming Workspace Runtime readiness, Agent Team Instance creation, adapter preflight, or live launch readiness

## MODIFIED Requirements

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

#### Scenario: Local subcommands exist
- **WHEN** the `isomer-admin-topic-team-specialize` skill folder is inspected
- **THEN** it contains local subcommand pages named `help`, `init-topic`, `clarify-topic`, `specialize-team`, `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, `resolve-project`, `inspect-template`, `resolve-context`, `map-placeholders`, `draft-profile`, `approve-profile`, `materialize-profile`, `fast-forward`, and `step-by-step` under `references/`

#### Scenario: Subcommands are grouped by contract
- **WHEN** the skill entrypoint, workflow text, or operator documentation lists local subcommands
- **THEN** it groups `init-topic`, `clarify-topic`, `specialize-team`, `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, `approve-profile`, and `materialize-profile` as procedural subcommands, `resolve-project`, `inspect-template`, `resolve-context`, `map-placeholders`, and `draft-profile` as helper subcommands, and `help`, `fast-forward`, and `step-by-step` as misc subcommands

#### Scenario: Help lists public subcommands only
- **WHEN** the user invokes the local `help` subcommand
- **THEN** the help output lists procedural and misc subcommands in a table with `Subcommand`, `Purpose`, and `Produces` columns, and does not list helper subcommands such as `resolve-project`, `inspect-template`, `resolve-context`, `map-placeholders`, or `draft-profile`

#### Scenario: Helper subcommands remain lower-level
- **WHEN** helper subcommands are described in the skill entrypoint, workflow text, or operator documentation
- **THEN** the documentation frames the five helper subcommands as finer-grained commands called by procedural subcommands while still allowing direct manual invocation

#### Scenario: Subcommand names are short
- **WHEN** local subcommand pages are inspected
- **THEN** each subcommand filename uses a short verb-object form such as `do-something.md`, except the intentional `help.md` and `step-by-step.md` commands

#### Scenario: Help subcommand prints usage
- **WHEN** the user invokes the local `help` subcommand
- **THEN** the skill prints what `isomer-admin-topic-team-specialize` does, how to invoke it, available modes, public subcommands, outputs, and guardrails

#### Scenario: Empty invocation defaults to help
- **WHEN** the skill is invoked without a prompt
- **THEN** the entrypoint selects `help` and prints the same usage output

#### Scenario: Step-by-step performs guided specialization
- **WHEN** the user asks to specialize step by step, proceed interactively, or confirm each stage
- **THEN** the module skill executes `step-by-step`, follows the same required static-material path as `fast-forward`, explains the current step, and waits for user confirmation before continuing to the next step

#### Scenario: Service routing subcommand is absent
- **WHEN** the `isomer-admin-topic-team-specialize` skill folder is inspected
- **THEN** it does not contain `references/route-service.md`

#### Scenario: Required support references are local
- **WHEN** the `isomer-admin-topic-team-specialize` skill folder is inspected
- **THEN** it contains local support references for Isomer domain language and static/runtime file boundaries under `references/`

#### Scenario: External support refs are absent
- **WHEN** the `isomer-admin-topic-team-specialize` skill entrypoint and local references are inspected
- **THEN** they do not reference `.imsight-arts/`, `docs/`, `extern/`, or absolute local support paths for information needed to execute the skill

#### Scenario: Runtime launch subcommand is absent
- **WHEN** the `isomer-admin-topic-team-specialize` skill folder is inspected
- **THEN** it does not contain `references/launch-team.md`

#### Scenario: Incorporated standalone skills are absent
- **WHEN** the operator skillset is inspected
- **THEN** it does not contain standalone `isomer-admin-project-aware`, `isomer-admin-template-inspect`, `isomer-admin-topic-context-resolve`, `isomer-admin-service-request-route`, `isomer-admin-placeholder-reconcile`, `isomer-admin-topic-profile-draft`, `isomer-admin-profile-review-approval`, `isomer-admin-profile-materialize`, or `isomer-admin-team-launch-orchestrate` skill folders

### Requirement: Subcommand Incorporation
The module skill SHALL incorporate former helper-skill behavior as local subcommands instead of requiring normal workflow calls to separate skills.

#### Scenario: Entrypoint routes to local subcommands
- **WHEN** `SKILL.md` describes project awareness, template inspection, topic context resolution, placeholder reconciliation, topic profile drafting, profile review approval, or profile materialization
- **THEN** it routes the agent to local subcommand pages through a `## Subcommands` table

#### Scenario: Manual mode selects one subcommand
- **WHEN** the user names one local subcommand or asks for one bounded operation
- **THEN** the entrypoint loads only that subcommand page, executes that workflow, and reports that subcommand's output

#### Scenario: Normal specialization avoids external skill calls
- **WHEN** the module skill performs its normal Topic Team Specialization workflow
- **THEN** it uses local subcommands for project awareness, template inspection, topic context resolution, placeholder reconciliation, and topic profile drafting instead of asking the user to invoke separate operator skills

#### Scenario: Fast-forward performs automatic static specialization
- **WHEN** the user asks to fully specialize, prepare, adapt end-to-end, or says `fast-forward`
- **THEN** the module skill executes `fast-forward` to run the static Topic Team material path through final topic-team summary output

#### Scenario: Step-by-step confirms before continuing
- **WHEN** `step-by-step` completes one required static-material step
- **THEN** it summarizes what happened and waits for user confirmation before executing the next step

#### Scenario: Static boundary operations remain explicit
- **WHEN** approval or materialization work is requested after specialization
- **THEN** the module skill uses the local `approve-profile` or `materialize-profile` subcommand and preserves all static validation and provenance boundaries

#### Scenario: Live launch is not incorporated
- **WHEN** live team launch, Agent Team Instance creation, Workspace Runtime mutation, or Houmao Execution Adapter operation is requested
- **THEN** the module skill reports that live operation is outside this skill's scope rather than routing to a local launch subcommand

### Requirement: Topic Team Specialization Workflow
The module skill SHALL guide a Project Operator Session or Operator Agent through adapting one Domain Agent Team Template for one Research Topic and producing static Topic Team material.

#### Scenario: Module purpose is plain text
- **WHEN** operator documentation or skill text describes the workflow
- **THEN** it explains in plain text that the skill adapts one Domain Agent Team Template for one Research Topic by copying template material into the topic workspace and producing reviewable static specialization outputs

#### Scenario: Template material is copied before adaptation
- **WHEN** a Project Operator Session specializes a Domain Agent Team Template for a Research Topic
- **THEN** it copies selected template material into the Topic Agent Team Profile Bundle under the owning Topic Workspace before editing topic-specific material

#### Scenario: Source template remains generic
- **WHEN** copied template material is adapted for a Research Topic
- **THEN** the module skill edits only copied material inside the Topic Agent Team Profile Bundle and leaves the Domain Agent Team Template source generic

#### Scenario: Topic Workspace teams directory is not used
- **WHEN** the module skill stores copied or adapted topic-team material
- **THEN** it stores that material inside `<topic-workspace>/team-profile/` and does not create a Topic Workspace-local `teams/` directory

#### Scenario: Static setup remains in workflow
- **WHEN** the workflow prepares the topic environment or Agent Workspace layout
- **THEN** it treats package installation, environment setup records, created workspace directories, and boundary notes as durable static preparation rather than live team operation

### Requirement: Packet and Profile Boundaries
The module skill SHALL produce human-readable specialization artifacts that can feed Topic Team Instantiation Packet and Topic Agent Team Profile Bundle drafting without replacing those structured artifacts or live runtime workflows.

#### Scenario: Packet inputs are explicit
- **WHEN** the module skill completes topic adaptation
- **THEN** it reports copied material paths, guide path, plan path, adaptation summary, resolved placeholders, deferrals, review points, setup evidence, Agent Workspace layout refs, and validation refs needed to build or update a Topic Team Instantiation Packet

#### Scenario: Profile materialization remains separate
- **WHEN** the module skill finishes adaptation
- **THEN** it does not claim that the Topic Agent Team Profile Bundle is approved or materialized unless existing approval provenance and generic validation have completed through their own static profile-material boundaries

#### Scenario: Runtime attachment remains out of scope
- **WHEN** the module skill finishes adaptation, approval, materialization, validation, or finalization
- **THEN** it does not claim that the topic team is launched, launchable, attached to an Agent Team Instance, registered in Workspace Runtime, or ready for adapter execution

### Requirement: Skill Validation
The implementation SHALL validate the module skill with skill-creator and repository validation surfaces.

#### Scenario: Skill creator validation runs
- **WHEN** the module skill bundle is ready for review
- **THEN** a developer or agent can run `pixi run python /home/huangzhe/.codex/skills/.system/skill-creator/scripts/quick_validate.py skillset/operator/isomer-admin-topic-team-specialize` or the repo-local equivalent and receive a passing result

#### Scenario: Operator skillset validation runs
- **WHEN** `pixi run validate-operator-skills` runs
- **THEN** it accepts the module skill without `references/launch-team.md`, detects missing required guide, plan, support-reference, subcommand-group, predecessor-artifact, or static-material terms including `init-topic`, `clarify-topic`, `specialize-team`, `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, and `finalize-topic-team`, verifies local subcommand workflow structure and naming, rejects external support refs, rejects unexpected runtime launch subcommand pages, and does not require `evals/`

#### Scenario: Unit validation covers removed launch subcommand
- **WHEN** `pixi run python -m unittest tests.unit.test_validate_skillsets` runs
- **THEN** the tests cover the accepted static-material subcommand set and fail if `launch-team` is required or listed as a public subcommand

#### Scenario: OpenSpec validation runs
- **WHEN** `openspec validate limit-topic-team-specialize-to-static-materials --strict` runs
- **THEN** the change artifacts validate without schema or scenario-format errors
