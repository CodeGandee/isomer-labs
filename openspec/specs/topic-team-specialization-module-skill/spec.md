# topic-team-specialization-module-skill Specification

## Purpose
Define the module-level operator skill for Topic Team Specialization, including local subcommands, copied-template workflow, guide and plan artifacts, and validation boundaries.
## Requirements
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

### Requirement: Imsight Workflow Entrypoint
The module skill SHALL follow the Imsight skill-entrypoint structure.

#### Scenario: Workflow section is near the top
- **WHEN** `SKILL.md` is inspected
- **THEN** it contains a near-top `## Workflow` section before detailed guide, plan, helper, output, or guardrail sections

#### Scenario: Workflow steps are numbered
- **WHEN** the `## Workflow` section is inspected
- **THEN** it uses numbered steps that select default help mode for empty invocation, manual single-subcommand mode, guided `step-by-step` mode, automatic `fast-forward` mode, ambiguity handling, and shared validation boundaries

#### Scenario: Detailed rules are separated
- **WHEN** generated-guide rules, plan structure, subcommand routing, output fields, or guardrails require detail
- **THEN** `SKILL.md` keeps that detail in named sections outside the concise workflow steps

#### Scenario: Freeform fallback exists
- **WHEN** the user's task does not map cleanly to the default workflow steps
- **THEN** the skill tells the agent to use its native planning tool to build and execute a step-by-step plan from the project context, copied-template constraints, subcommands, output contract, and guardrails

#### Scenario: Subcommands have Imsight workflows
- **WHEN** each local subcommand page is inspected
- **THEN** it contains a near-top `## Workflow` section, numbered workflow steps, and a fallback for tasks that do not map cleanly to the default steps

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

### Requirement: Specialization Guide and Plan Artifacts
The module skill SHALL use `team-specialization-guide.md` and `team-specialization-plan.md` inside the copied template root to make Topic Team Specialization auditable.

#### Scenario: Existing guide is read first
- **WHEN** copied template material contains `team-specialization-guide.md`
- **THEN** the module skill reads that guide before inspecting other copied template material for adaptation decisions

#### Scenario: Missing guide is generated with fenced block
- **WHEN** copied template material does not contain `team-specialization-guide.md`
- **THEN** the module skill creates `team-specialization-guide.md` in the copied template root, synthesizes it from copied material, and includes a clear `generated-guide` fenced block stating that no source guide existed

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

### Requirement: Topic Initialization Subcommand
The module skill SHALL provide an `init-topic` subcommand that starts the user-facing Topic Team Specialization flow by creating provisional topic definition material before team specialization when the Research Topic is new or unclear, while routing authoritative Project registration through topic CRUD commands.

#### Scenario: Missing topic prompts clarification
- **WHEN** the user invokes `init-topic` without a Research Topic or with an unclear Research Topic
- **THEN** the subcommand asks the user for enough topic information before creating any directory or topic overview file

#### Scenario: Empty project topic registry is not topic substance
- **WHEN** the user invokes `init-topic` without supplying topic substance and the Project Manifest has no registered Research Topics
- **THEN** the subcommand asks the user for the concrete research topic and does not create or overwrite `topic-overview.md`

#### Scenario: Generic default topic is not sufficient
- **WHEN** the user invokes `init-topic` without supplying topic substance and the Project Manifest has a registered default Research Topic or generic `default Research Topic` statement
- **THEN** the subcommand asks the user for the concrete research topic and does not create or overwrite `topic-overview.md`

#### Scenario: Missing topic directory uses default base for clear topic
- **WHEN** the user-supplied Research Topic is clear but no topic workspace directory is supplied
- **THEN** the subcommand derives a provisional topic seed directory under the effective Topic Workspace base, normally `isomer-content/topic-ws/<topic-slug>/`, before creating topic material

#### Scenario: Default base comes from manifest or built-in layout
- **WHEN** `init-topic` derives a provisional topic seed directory
- **THEN** it uses the Project Manifest `topic_workspace_base_dir` when present and otherwise uses the built-in `isomer-content/topic-ws/` base

#### Scenario: Ambiguous derived directory prompts user
- **WHEN** the derived provisional topic seed directory already exists or would collide with registered or unrelated Project material
- **THEN** the subcommand asks the user to confirm or provide a different topic workspace directory before creating or modifying topic material

#### Scenario: Explicit topic directory still wins
- **WHEN** the user supplies a topic workspace directory explicitly
- **THEN** the subcommand uses that directory after confirming it is clear and project-scoped according to this skill's guardrails

#### Scenario: Topic overview is created
- **WHEN** the user confirms a Research Topic and topic workspace directory or the subcommand derives a clear default directory
- **THEN** the subcommand creates the directory and writes `<topic-dir>/topic-def/topic-overview.md` from the agent's understanding of the Research Topic

#### Scenario: Topic overview has required sections
- **WHEN** `topic-overview.md` is written
- **THEN** it includes sections for the Research Topic, agent understanding, scope, initial objectives, assumptions, open questions, and source prompt or source material

#### Scenario: Provisional status is reported
- **WHEN** `init-topic` creates topic material that is not registered in the Project Manifest
- **THEN** the subcommand reports that the topic directory is a provisional topic workspace seed and is not yet an authoritative Isomer Research Topic or Topic Workspace registration

#### Scenario: Project config mutation routes through topic CRUD
- **WHEN** `init-topic` needs the new topic to become an authoritative Project Manifest-registered Research Topic
- **THEN** it routes through `isomer-cli project topics create <topic-id> --statement "<research topic>"` or reports that the user must run that command, instead of hand-editing `.isomer-labs/manifest.toml` or using `isomer-cli project init`

#### Scenario: Specialization waits for explicit topic readiness
- **WHEN** `fast-forward` or `step-by-step` cannot resolve a registered Research Topic but can create a provisional seed through `init-topic`
- **THEN** the workflow reports the provisional seed and any `isomer-cli project topics create` registration blockers before proceeding to template adaptation that requires authoritative topic refs

### Requirement: User-Facing Topic Team Flow
The module skill SHALL present the primary user-facing flow as procedural subcommands for topic initialization, optional topic clarification, team specialization, optional team clarification, topic environment setup, per-agent workspace setup, static readiness validation, final summary, and explicit approval or materialization boundaries.

#### Scenario: Flow order is documented
- **WHEN** help text, workflow text, or operator documentation describes the normal user-facing path
- **THEN** it presents the order as `init-topic`, optional `clarify-topic`, `specialize-team`, optional `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, then explicit `approve-profile` or `materialize-profile` when requested

#### Scenario: Procedural subcommands refuse missing predecessor artifacts
- **WHEN** a procedural subcommand after `init-topic` is selected and the artifacts expected from its predecessor steps are missing
- **THEN** the subcommand refuses to run, explains which predecessor artifacts are missing, and tells the user which previous subcommand should create them

#### Scenario: Init topic has no predecessor artifact requirement
- **WHEN** `init-topic` is selected
- **THEN** it states that no predecessor artifacts are required because it is the first procedural step

#### Scenario: Clarify topic revises topic overview
- **WHEN** the user asks to refine, answer open questions, or clarify the Research Topic after `init-topic`
- **THEN** the skill routes to `clarify-topic` and updates or reports revisions to `<topic-dir>/topic-def/topic-overview.md` without specializing the team yet

#### Scenario: Specialize team selects domain team
- **WHEN** the user asks to specialize a team after the topic is clear
- **THEN** the skill routes to `specialize-team`, asks the user to select or confirm one Domain Agent Team Template, and runs the internal specialization path against the topic material

#### Scenario: Specialize team creates topic team material
- **WHEN** `specialize-team` completes its specialization work
- **THEN** it reports the created or updated Topic Agent Team Profile Bundle inputs, copied template material, placeholder resolutions, deferrals, validation refs, and next operator action

#### Scenario: Clarify topic team revises specialization
- **WHEN** the user asks to revise the specialized team, adjust roles, change assumptions, or answer open questions about the proposed topic team
- **THEN** the skill routes to `clarify-topic-team` and updates or reports revisions to the specialization outputs without claiming approval, materialization, or live operation

#### Scenario: Topic environment setup is explicit
- **WHEN** the specialized topic team needs a development environment before work can start
- **THEN** the skill routes to `setup-topic-env`, runs or reports explicit environment setup steps, and records environment setup status, commands, blockers, and validation refs

#### Scenario: Agent workspace setup is explicit
- **WHEN** the specialized topic team has expected agent roles or Agent Instances that need workspaces
- **THEN** the skill routes to `setup-agent-workspace`, creates or reports per-agent workspace directories and boundary notes, and records workspace paths, ownership, blockers, and validation refs

#### Scenario: Topic team readiness is validated
- **WHEN** topic definition, specialization, environment setup, and agent workspace setup are complete or intentionally deferred
- **THEN** the skill routes to `validate-topic-team` and checks whether the topic team has the topic overview, specialized team material, environment posture, per-agent workspaces, deferrals, and blockers needed for static material readiness

#### Scenario: Final topic summary is written
- **WHEN** the topic team has been validated or blockers have been explicitly recorded
- **THEN** the skill routes to `finalize-topic-team` and creates `isomer-topic-summary.md` with the topic team, goal, working logic, environment setup, agent workspace layout, validation status, blockers, and next actions

#### Scenario: Fast-forward remains execution mode
- **WHEN** the user asks for `fast-forward`
- **THEN** the skill treats it as an execution mode that runs the same required path as `init-topic` when needed, optional clarification only when required to unblock, `specialize-team`, setup, validation, and final topic-team summary output

#### Scenario: Step-by-step remains guided execution mode
- **WHEN** the user asks for `step-by-step`
- **THEN** the skill treats it as the guided form of the same user-facing path and waits for confirmation between topic initialization, clarification, team specialization, team clarification, setup, validation, and finalization steps

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

### Requirement: Clarification Option Loop
The module skill SHALL make `clarify-topic` and `clarify-topic-team` use a bounded option-asking clarification loop that updates static topic-team artifacts directly instead of creating separate user-decision records.

#### Scenario: Topic clarification scans and asks focused questions
- **WHEN** the `clarify-topic` subcommand runs after its predecessor artifacts exist
- **THEN** it performs a coverage and clarity scan of `<topic-dir>/topic-def/topic-overview.md`, identifies unresolved questions that materially affect topic scope, objectives, assumptions, open questions, or template selection, and asks at most one focused clarification question at a time

#### Scenario: Team clarification scans and asks focused questions
- **WHEN** the `clarify-topic-team` subcommand runs after its predecessor artifacts exist
- **THEN** it performs a coverage and clarity scan of the topic overview, copied template material, `team-specialization-guide.md`, `team-specialization-plan.md`, `Final Report`, placeholder resolutions, deferrals, and draft packet/profile inputs, then asks at most one focused clarification question at a time about role, workflow, policy, binding, copied-material, setup, validation, or blocker ambiguity

#### Scenario: Clarification question format is structured
- **WHEN** either `clarify-topic` or `clarify-topic-team` asks a clarification question
- **THEN** the question includes a motivation, a concrete example when useful, a proposed answer or option with rationale, the downstream implication of accepting it, and either two to five mutually exclusive options with a custom short-answer path or a short-answer prompt with a proposed answer

#### Scenario: Clarification answers update topic material directly
- **WHEN** the user answers a `clarify-topic` question clearly or accepts the proposed answer
- **THEN** the subcommand validates the answer, updates `<topic-dir>/topic-def/topic-overview.md` directly, removes or revises resolved open questions and obsolete assumptions, and reports remaining open questions and readiness for `specialize-team`

#### Scenario: Clarification answers update team material directly
- **WHEN** the user answers a `clarify-topic-team` question clearly or accepts the proposed answer
- **THEN** the subcommand validates the answer, updates the relevant copied topic-team material, specialization plan, `Final Report`, placeholder resolutions, deferrals, or draft packet/profile inputs directly, and reports changed paths, remaining blockers, and readiness for setup or validation

#### Scenario: Clarification loop does not create decision logs
- **WHEN** either `clarify-topic` or `clarify-topic-team` integrates an accepted user answer
- **THEN** it does not create an ADR, decision log, user-decision record, or separate clarification transcript as the durable source of truth for that answer

#### Scenario: Clarification loop stops predictably
- **WHEN** all critical ambiguities are resolved, the user signals completion, or five clarification questions have been asked in the current clarification session
- **THEN** the subcommand stops asking questions and reports remaining open questions, deferrals, blockers, changed artifacts, and the next safe operator action
