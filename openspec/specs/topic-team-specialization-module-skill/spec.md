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
- **THEN** it contains local subcommand pages named `help`, `init-topic`, `clarify-topic`, `ensure-topic-registration`, `specialize-team`, `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, `resolve-project`, `inspect-template`, `resolve-context`, `map-placeholders`, `draft-profile`, `approve-profile`, `materialize-profile`, `fast-forward`, and `step-by-step` under `references/`

#### Scenario: Subcommands are grouped by contract
- **WHEN** the skill entrypoint, workflow text, or operator documentation lists local subcommands
- **THEN** it groups `init-topic`, `clarify-topic`, `ensure-topic-registration`, `specialize-team`, `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, `approve-profile`, and `materialize-profile` as procedural subcommands, `resolve-project`, `inspect-template`, `resolve-context`, `map-placeholders`, and `draft-profile` as helper subcommands, and `help`, `fast-forward`, and `step-by-step` as misc subcommands

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
The module skill SHALL provide an `init-topic` subcommand that starts the user-facing Topic Team Specialization flow by creating provisional topic definition material before team specialization when the Research Topic is new or unclear, while routing authoritative Project registration through `ensure-topic-registration`.

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
- **AND** it names `ensure-topic-registration` as the next registration action when downstream steps require authoritative refs

#### Scenario: Project config mutation routes through registration assurance
- **WHEN** `init-topic` needs the new topic to become an authoritative Project Manifest-registered Research Topic
- **THEN** it routes to `ensure-topic-registration`, which uses `isomer-cli project topics create <topic-id> --statement "<research topic>" --workspace-dir <topic-workspace-dir>` or another supported Isomer CLI/API path
- **AND** it does not hand-edit `.isomer-labs/manifest.toml` or Research Topic Config files
- **AND** it does not use `isomer-cli project init`

#### Scenario: Specialization waits for explicit topic readiness
- **WHEN** `fast-forward` or `step-by-step` cannot resolve a registered Research Topic but can create a provisional seed through `init-topic`
- **THEN** the workflow reports the provisional seed, runs or offers `ensure-topic-registration`, and stops on registration blockers before proceeding to template adaptation that requires authoritative topic refs

### Requirement: Topic Registration Assurance Subcommand
The module skill SHALL provide an `ensure-topic-registration` procedural subcommand that verifies or creates authoritative Project Manifest-backed Research Topic and Topic Workspace registration before registration-dependent topic-team work proceeds.

#### Scenario: Existing registration is verified
- **WHEN** `ensure-topic-registration` runs for an already registered Research Topic and Topic Workspace
- **THEN** it reads Project Manifest-backed registrations and reports `topic_registration_status: registered`
- **AND** it carries forward the registered `research_topic_ref` and `topic_workspace_ref`
- **AND** it does not create a second registration or mutate Project Config unnecessarily

#### Scenario: Provisional topic seed is registered through supported surface
- **WHEN** `ensure-topic-registration` receives a clear provisional topic seed from `init-topic`
- **AND** the Project Manifest does not yet register that Research Topic and Topic Workspace
- **THEN** it routes through `isomer-cli project topics create <topic-id> --statement "<research topic>" --workspace-dir <topic-workspace-dir>` or an equivalent supported Isomer CLI/API surface
- **AND** it does not hand-edit `.isomer-labs/manifest.toml` or Research Topic Config files

#### Scenario: Missing concrete topic statement blocks registration
- **WHEN** `ensure-topic-registration` cannot recover a concrete Research Topic statement from user input, `topic-overview.md`, or registered topic config
- **THEN** it reports a blocker asking for the concrete research topic
- **AND** it does not create or update Project Config files

#### Scenario: Colliding workspace blocks registration
- **WHEN** the provisional Topic Workspace directory collides with another registered Topic Workspace, Project Config directory, Houmao overlay, or unrelated project-owned path
- **THEN** `ensure-topic-registration` reports a blocker with the conflicting path
- **AND** it asks the user to choose or confirm a safe workspace path before registration

#### Scenario: Environment binding is verified before setup
- **WHEN** later workflow steps require `setup-topic-env`
- **THEN** `ensure-topic-registration` verifies that the selected Research Topic has an active `topic_standalone_pixi_bindings` entry, a Pixi-resolvable implicit default Topic Workspace binding, or another supported environment binding accepted by `isomer-srv-topic-env-setup`
- **AND** the binding names or resolves to the selected Topic Workspace Pixi manifest and Pixi environment

#### Scenario: Missing environment binding blocks service delegation
- **WHEN** the Research Topic and Topic Workspace are registered but no explicit supported Topic Workspace Pixi binding exists and Pixi cannot resolve the Topic Workspace directory as an implicit default binding
- **THEN** `ensure-topic-registration` reports `topic_registration_status: blocked`
- **AND** it names the missing binding or unresolvable default target and the expected Topic Workspace Pixi manifest path
- **AND** `setup-topic-env` does not call `isomer-srv-topic-env-setup` until the binding exists or a supported Isomer CLI/API surface creates it

#### Scenario: Unsupported binding mutation remains a blocker
- **WHEN** the only way to add the required Pixi binding would be hand-editing `.isomer-labs/manifest.toml`
- **THEN** the subcommand reports a blocker instead of editing the manifest directly
- **AND** it tells the user which supported Isomer CLI/API surface is needed when that surface exists

#### Scenario: Registration assurance is reusable
- **WHEN** a user invokes `ensure-topic-registration` directly after prior registration
- **THEN** the subcommand revalidates the Project Manifest, Research Topic Config, Topic Workspace path, and environment binding
- **AND** it reports no mutation when all required registrations are already valid

### Requirement: User-Facing Topic Team Flow
The module skill SHALL present the primary user-facing flow as procedural subcommands for topic initialization, optional topic clarification, topic registration assurance, independent topic environment setup, team specialization, optional team clarification, per-agent workspace setup, static readiness validation, final summary, and explicit approval or materialization boundaries.

#### Scenario: Flow order is documented
- **WHEN** help text, workflow text, or operator documentation describes the normal user-facing path
- **THEN** it presents the order as `init-topic`, optional `clarify-topic`, `ensure-topic-registration`, optional or independent `setup-topic-env` when `env-gate.md` is available or needed, `specialize-team`, optional `clarify-topic-team`, optional repeated `setup-topic-env` when specialization changes runnable requirements, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, then explicit `approve-profile` or `materialize-profile` when requested
- **AND** it does not present Topic Workspace environment setup as requiring an existing Topic Agent Team Profile Bundle

#### Scenario: Procedural subcommands refuse missing predecessor artifacts
- **WHEN** a procedural subcommand after `init-topic` is selected and the artifacts expected from its predecessor steps are missing
- **THEN** the subcommand refuses to run, explains which predecessor artifacts are missing, and tells the user which previous subcommand should create them
- **AND** `setup-topic-env` treats manifest-backed topic registration, Topic Workspace Pixi binding evidence, and a usable `env-gate.md` as its predecessor requirements instead of requiring specialization outputs or team-profile material

#### Scenario: Init topic has no predecessor artifact requirement
- **WHEN** `init-topic` is selected
- **THEN** it states that no predecessor artifacts are required because it is the first procedural step

#### Scenario: Clarify topic revises topic overview
- **WHEN** the user asks to refine, answer open questions, or clarify the Research Topic after `init-topic`
- **THEN** the skill routes to `clarify-topic` and updates or reports revisions to `<topic-dir>/topic-def/topic-overview.md` without specializing the team yet

#### Scenario: Ensure registration prepares authoritative refs
- **WHEN** the user asks to continue from a provisional topic seed or before any registration-dependent workflow step
- **THEN** the skill routes to `ensure-topic-registration`, verifies or creates Project Manifest-backed Research Topic and Topic Workspace registration through supported Isomer surfaces, verifies required environment binding state, and reports registration blockers

#### Scenario: Topic environment setup can run before team specialization
- **WHEN** the user asks to prepare the Topic Workspace development environment after `ensure-topic-registration`
- **AND** a source gate exists or the user provides a clear runnable target that can be written to the source gate
- **THEN** the skill routes to `setup-topic-env` without requiring `specialize-team`, `team-profile/`, Topic Agent Team Profile material, Agent Team Instance records, agent roles, or agent count
- **AND** it records the service output as durable setup evidence

#### Scenario: Specialize team selects domain team
- **WHEN** the user asks to specialize a team after the topic is clear and registration blockers are resolved
- **THEN** the skill routes to `specialize-team`, asks the user to select or confirm one Domain Agent Team Template, and runs the internal specialization path against the topic material

#### Scenario: Specialize team creates topic team material
- **WHEN** `specialize-team` completes its specialization work
- **THEN** it reports the created or updated Topic Agent Team Profile Bundle inputs, copied template material, placeholder resolutions, deferrals, validation refs, and next operator action

#### Scenario: Clarify topic team revises specialization
- **WHEN** the user asks to revise the specialized team, adjust roles, change assumptions, or answer open questions about the proposed topic team
- **THEN** the skill routes to `clarify-topic-team` and updates or reports revisions to the specialization outputs without claiming approval, materialization, or live operation

#### Scenario: Topic environment setup remains explicit
- **WHEN** the Topic Workspace needs a development environment before research work can start or when specialization changes runnable requirements
- **THEN** the skill requires `ensure-topic-registration` evidence first, then routes to `setup-topic-env`, runs or reports explicit environment setup steps, and records environment setup status, commands, blockers, and validation refs
- **AND** it does not require topic-team specialization material unless the requested runnable target explicitly depends on files produced by specialization

#### Scenario: Agent workspace setup is explicit
- **WHEN** the specialized topic team has expected agent roles or Agent Instances that need workspaces
- **THEN** the skill routes to `setup-agent-workspace`, creates or reports per-agent workspace directories and boundary notes, and records workspace paths, ownership, blockers, and validation refs

#### Scenario: Topic team readiness is validated
- **WHEN** topic definition, registration assurance, team specialization when required, environment setup, and agent workspace setup are complete or intentionally deferred
- **THEN** the skill routes to `validate-topic-team` and checks whether the topic team has the topic overview, registered topic refs, specialized team material, environment posture, per-agent workspaces, deferrals, and blockers needed for static material readiness
- **AND** it treats missing environment setup evidence as an environment-preparation blocker, not as proof that team-profile material is missing

#### Scenario: Final topic summary is written
- **WHEN** the topic team has been validated or blockers have been explicitly recorded
- **THEN** the skill routes to `finalize-topic-team` and creates `isomer-topic-summary.md` with the topic team, goal, working logic, registration status, environment setup, agent workspace layout, validation status, blockers, and next actions

#### Scenario: Fast-forward remains execution mode
- **WHEN** the user asks for `fast-forward`
- **THEN** the skill treats it as an execution mode that runs the same required path as `init-topic` when needed, optional clarification only when required to unblock, `ensure-topic-registration`, independent environment setup when a gate exists or is needed, team specialization when requested or needed, setup, validation, and final topic-team summary output

#### Scenario: Step-by-step remains guided execution mode
- **WHEN** the user asks for `step-by-step`
- **THEN** the skill treats it as the guided form of the same user-facing path and waits for confirmation between topic initialization, clarification, registration assurance, independent environment setup when applicable, team specialization, team clarification, setup, validation, and finalization steps

### Requirement: Topic Environment Setup is Explicit
The module skill SHALL route topic environment setup through `isomer-srv-topic-env-setup` and SHALL treat the setup as durable Topic Workspace preparation. The skill SHALL NOT block environment setup solely because the Project Manifest lacks an explicit `topic_standalone_pixi_bindings` entry when Pixi can resolve the registered Topic Workspace directory as the default Topic Workspace Pixi binding target. The skill SHALL NOT block environment setup solely because topic-team specialization material is absent.

#### Scenario: Setup delegates to environment service
- **WHEN** the Topic Workspace needs a development environment before research work can start
- **THEN** the skill routes to `setup-topic-env`, prepares or reuses the source gate at `<topic-workspace>/user-intent/src/env-gate.md`, and delegates heavy environment setup to `isomer-srv-topic-env-setup`
- **AND** it does not perform dependency inference, repo acquisition, Pixi installation, or verification directly inside the operator subcommand

#### Scenario: Default binding removes explicit binding blocker
- **WHEN** `setup-topic-env` runs for a registered Topic Workspace
- **AND** the Project Manifest has no active `topic_standalone_pixi_bindings` entry for the Research Topic
- **AND** Pixi can resolve the registered Topic Workspace directory as a confined Topic Workspace Pixi binding target
- **THEN** the skill delegates environment setup to `isomer-srv-topic-env-setup` instead of reporting a missing binding blocker

#### Scenario: Missing default Pixi workspace still blocks
- **WHEN** `setup-topic-env` runs for a registered Topic Workspace
- **AND** the Project Manifest has no active `topic_standalone_pixi_bindings` entry for the Research Topic
- **AND** Pixi cannot resolve the registered Topic Workspace directory as a Topic Workspace Pixi binding target
- **THEN** the skill records a blocker that names the Topic Workspace directory as the default binding target and the option to add an explicit binding

#### Scenario: Missing team profile does not block service delegation
- **WHEN** `setup-topic-env` runs for a registered Topic Workspace with a usable source gate and effective Topic Workspace Pixi binding
- **AND** `<topic-workspace>/team-profile/` or Topic Agent Team Profile material is absent
- **THEN** the operator subcommand still delegates heavy environment setup to `isomer-srv-topic-env-setup`
- **AND** it records absent team-profile material only as unrelated or downstream topic-team context

#### Scenario: Setup records environment status
- **WHEN** `setup-topic-env` completes or stops on a blocker
- **THEN** it records environment setup status, commands run, changed files, validation refs, and blockers as durable static preparation evidence

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

### Requirement: Git-Backed Agent Workspace Delegation
The Topic Team Specialization module skill SHALL delegate Git-backed Agent Workspace repository, worktree, and `isomer-managed/` preparation to `isomer-admin-topic-workspace-mgr` when a specialized topic team needs the `repos/topic-main` layout.

#### Scenario: Setup agent workspace delegates Git worktree setup
- **WHEN** `setup-agent-workspace` determines that the selected topic team needs Git-backed Agent Workspaces under `<topic-workspace-dir>/agents/<agent-name>`
- **THEN** it routes or instructs the operator to use `isomer-admin-topic-workspace-mgr` rather than creating the worktrees itself

#### Scenario: Setup agent workspace delegates Isomer-managed setup
- **WHEN** `setup-agent-workspace` determines that per-agent worker-facing support paths, peer-readable large artifact paths, generated links, or boundary material are needed
- **THEN** it routes or instructs the operator to use `isomer-admin-topic-workspace-mgr` for `isomer-managed/` preparation rather than creating `.isomer-agent/` or top-level `topic-main` collaboration directories itself

#### Scenario: Static setup records delegated workspace refs
- **WHEN** delegated Git-backed workspace setup has completed
- **THEN** `setup-agent-workspace`, `validate-topic-team`, or `finalize-topic-team` may report the returned Agent Workspace paths, branch names, `isomer-managed/` paths, boundary docs, validation refs, blockers, and next actions as static setup evidence

#### Scenario: Delegation preserves static boundary
- **WHEN** Topic Team Specialization delegates Git-backed workspace setup
- **THEN** it still does not create Agent Instances, mutate Workspace Runtime records, launch agents, or invoke Execution Adapters

#### Scenario: Missing delegated setup blocks static readiness
- **WHEN** the specialized topic team requires Git-backed Agent Workspaces and no successful topic workspace manager output exists
- **THEN** `validate-topic-team` reports an Agent Workspace setup blocker rather than claiming static material readiness

#### Scenario: Legacy support setup is not accepted as new readiness
- **WHEN** the only available workspace setup evidence names `.isomer-agent/` or top-level `repos/topic-main/{shared,artifacts,tasks,runs,views,logs,tools}` as the current standard layout
- **THEN** `validate-topic-team` reports stale workspace setup evidence and asks for `isomer-admin-topic-workspace-mgr` validation of the `isomer-managed/` layout

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

### Requirement: Topic Team Workspace Evidence Language
The Topic Team Specialization module skill SHALL use topic-local agent names and worker visibility terms when reporting Agent Workspace setup evidence.

#### Scenario: Setup output uses agent names
- **WHEN** `setup-agent-workspace` reports prepared workspaces
- **THEN** it reports `agent_names`, `agent_workspace_paths`, `branch_plan`, `topic_main_repo`, `records_root`, and blockers instead of using `agent-key` as the user-facing term

#### Scenario: Setup output names worker visibility boundary
- **WHEN** `finalize-topic-team` summarizes static setup evidence
- **THEN** it distinguishes worker-visible material under `repos/topic-main` from owner-preserved records under `records/*` and runtime internals under `runtime/`

### Requirement: Topic Team Specialization Uses Semantic Workspace Surfaces
The Topic Team Specialization module skill SHALL consume and report workspace setup through semantic labels instead of treating default directory paths as the contract.

#### Scenario: Setup agent workspace requests semantic setup
- **WHEN** `setup-agent-workspace` determines that a specialized topic team needs Git-backed Agent Workspaces
- **THEN** it delegates to `isomer-admin-topic-workspace-mgr` with semantic surface expectations for Topic Main Repository and Agent Workspace preparation

#### Scenario: Delegated output records labels
- **WHEN** delegated Agent Workspace setup completes
- **THEN** `setup-agent-workspace` records the returned semantic labels, resolved paths, sources, Agent Names, branch namespaces, boundary material, validation refs, blockers, and next actions as static setup evidence

#### Scenario: Custom layout evidence is accepted
- **WHEN** delegated setup evidence shows safe manifest-backed paths that differ from `repos/topic-main` or `agents/<agent-name>`
- **THEN** the skill accepts the evidence when the semantic labels, ownership, and validation status are correct

#### Scenario: Hard-coded default-only evidence is insufficient
- **WHEN** setup evidence only says that default-looking directories exist without semantic label or manifest-backed validation
- **THEN** the skill reports the evidence as incomplete for static readiness

### Requirement: Topic Team Summaries Are Semantic Label First
The Topic Team Specialization module skill SHALL write summaries that name semantic workspace surfaces before concrete default paths.

#### Scenario: Final summary reports semantic layout
- **WHEN** `finalize-topic-team` writes or updates `isomer-topic-summary.md`
- **THEN** the Agent Workspace layout section reports semantic labels, Agent Names, resolved paths, path sources, Git branch plans, and validation status

#### Scenario: Default layout is described as default profile
- **WHEN** a summarized path comes from the built-in default layout
- **THEN** the summary identifies it as `isomer-default.v1` rather than implying that fixed paths are the workspace contract

#### Scenario: Custom layout remains understandable
- **WHEN** a summarized path differs from the default layout
- **THEN** the summary explains which semantic label the path satisfies and does not treat the path difference as a blocker by itself

### Requirement: Cwd-friendly Agent Guidance
The Topic Team Specialization module skill SHALL teach prepared agents to query their own Agent Workspace surfaces by semantic label from cwd.

#### Scenario: Boundary notes include self queries
- **WHEN** the skill records or summarizes Agent Workspace boundary material
- **THEN** it includes guidance that an agent running inside its own Agent Workspace can query agent-scoped labels without passing Agent Name

#### Scenario: Cross-agent queries remain explicit
- **WHEN** the skill describes peer inspection or integration behavior
- **THEN** it states that querying another agent's surface still requires an explicit Agent Name, Agent Instance, handoff, Artifact, or boundary-approved share

#### Scenario: Cwd inference is not security
- **WHEN** the skill describes cwd-derived agent context
- **THEN** it states that cwd inference is a convenience for path resolution and not filesystem-grade identity or access control

### Requirement: Static Readiness Checks Semantic Bindings
The Topic Team Specialization skill SHALL validate static setup using semantic path evidence before reporting the topic team as ready.

#### Scenario: Tmp posture is required only as local setup evidence
- **WHEN** Git-backed Agent Workspaces were requested
- **THEN** `validate-topic-team` requires delegated tmp posture evidence from the workspace setup flow
- **AND** it does not treat tmp contents as static material readiness

### Requirement: Topic Team Specialization Uses Agent Env Service Evidence
The Topic Team Specialization module skill SHALL consume `isomer-srv-agent-env-setup` output as durable static setup evidence when Agent Workspace environment readiness is in scope.

#### Scenario: Setup agent workspace delegates env readiness
- **WHEN** `setup-agent-workspace` determines that a specialized topic team needs Git-backed Agent Workspaces and per-agent cwd env verification
- **THEN** it delegates that concrete setup to `isomer-srv-agent-env-setup setup-agent-env` or records an explicit blocker explaining why service delegation cannot run

#### Scenario: Setup records service evidence
- **WHEN** agent env setup service output is available
- **THEN** `setup-agent-workspace` records semantic paths, Agent Names, branch plans, worktree status by agent, source agent env gate path, derived agent env gate path, readiness by agent, commands run, blockers, and next actions as static setup evidence

#### Scenario: Service evidence can satisfy static readiness
- **WHEN** service output reports overall Agent Workspace env readiness as `ready`
- **THEN** `validate-topic-team` may treat Agent Workspace setup and agent-cwd environment posture as ready for static material validation
- **AND** it still does not claim runtime launch readiness

#### Scenario: Missing service evidence blocks readiness when required
- **WHEN** the specialized team requires Agent Workspace env readiness and no service output or explicit deferral exists
- **THEN** `validate-topic-team` reports an Agent Workspace environment setup blocker

### Requirement: Final Topic Summary Reports Agent Env Matrix
The Topic Team Specialization module skill SHALL include service-produced agent environment evidence in final topic summaries.

#### Scenario: Final summary includes gate path
- **WHEN** `finalize-topic-team` writes or updates `isomer-topic-summary.md`
- **THEN** the Agent Workspace layout or environment section includes `user-intent/src/agent-env-gate.md` and `user-intent/derived/isomer-agent-env-gate.md` when those files exist

#### Scenario: Final summary reports per-agent readiness
- **WHEN** service output contains readiness by agent
- **THEN** the final summary lists each Agent Name, resolved `agent.workspace`, branch, env readiness status, and blocker when present

#### Scenario: Runtime boundary remains explicit
- **WHEN** the final summary includes ready Agent Workspace env setup
- **THEN** it states that Agent Team Instance creation, Workspace Runtime records, Houmao launch, and Execution Adapter readiness remain separate downstream steps

### Requirement: Topic Team Specialization Preserves Tmp Boundary
The Topic Team Specialization skill SHALL require delegated Git-backed workspace setup evidence to preserve the local tmp-label non-sharing contract.

#### Scenario: Setup evidence includes tmp contract
- **WHEN** `setup-agent-workspace` records delegated topic workspace manager evidence for Git-backed worktrees
- **THEN** the evidence includes whether `topic.repos.main.tmp` and `agent.tmp` surfaces are ignored and local-only
- **AND** it reports blockers when delegated setup found tracked tmp contents or missing ignore policy

#### Scenario: Validation rejects tmp as readiness evidence
- **WHEN** `validate-topic-team` inspects Agent Workspace setup evidence
- **THEN** it does not accept files under resolved tmp labels as durable readiness evidence, profile material, handoff material, generated-link material, or Peer Read Access

#### Scenario: Final summary separates tmp from sharing
- **WHEN** `finalize-topic-team` summarizes Agent Workspace layout
- **THEN** it distinguishes ignored local tmp labels from Git-tracked material, agent-owned public shares, topic-owned projections, generated links, and owner-preserved records

