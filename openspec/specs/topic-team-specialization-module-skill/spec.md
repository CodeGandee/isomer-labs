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
- **THEN** it contains local subcommand pages named `help`, `init-topic`, `clarify-topic`, `ensure-topic-registration`, `adapt-team-template`, `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, `resolve-project`, `inspect-template`, `resolve-context`, `map-placeholders`, `draft-profile`, `approve-profile`, `materialize-profile`, `fast-forward`, and `step-by-step` under `references/`

#### Scenario: Subcommands are grouped by contract
- **WHEN** the skill entrypoint, workflow text, or operator documentation lists local subcommands
- **THEN** it groups `init-topic`, `clarify-topic`, `ensure-topic-registration`, `adapt-team-template`, `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, `approve-profile`, and `materialize-profile` as procedural subcommands, `resolve-project`, `inspect-template`, `resolve-context`, `map-placeholders`, and `draft-profile` as helper subcommands, and `help`, `fast-forward`, and `step-by-step` as misc subcommands

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
- **THEN** it accepts the module skill without `references/launch-team.md`, detects missing required guide, plan, support-reference, subcommand-group, predecessor-artifact, or static-material terms including `init-topic`, `clarify-topic`, `adapt-team-template`, `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, and `finalize-topic-team`, verifies local subcommand workflow structure and naming, rejects external support refs, rejects unexpected runtime launch subcommand pages, and does not require `evals/`

#### Scenario: Unit validation covers removed launch subcommand
- **WHEN** `pixi run python -m unittest tests.unit.test_validate_skillsets` runs
- **THEN** the tests cover the accepted static-material subcommand set and fail if `launch-team` is required or listed as a public subcommand

#### Scenario: OpenSpec validation runs
- **WHEN** `openspec validate limit-topic-team-specialize-to-static-materials --strict` runs
- **THEN** the change artifacts validate without schema or scenario-format errors

### Requirement: Topic Initialization Subcommand
The module skill SHALL provide an `init-topic` subcommand that starts the user-facing Topic Team Specialization flow by creating or selecting a provisional Topic Workspace before topic intent resolution when the Research Topic is new or unclear, while routing authoritative Project registration through `ensure-topic-registration`.

#### Scenario: Missing topic prompts clarification
- **WHEN** the user invokes `init-topic` without a Research Topic or with an unclear Research Topic
- **THEN** the subcommand asks the user for enough topic information before creating any directory or source intent file

#### Scenario: Empty project topic registry is not topic substance
- **WHEN** the user invokes `init-topic` without supplying topic substance and the Project Manifest has no registered Research Topics
- **THEN** the subcommand asks the user for the concrete research topic and does not create or overwrite `topic.intent.overview`

#### Scenario: Generic default topic is not sufficient
- **WHEN** the user invokes `init-topic` without supplying topic substance and the Project Manifest has a registered default Research Topic or generic `default Research Topic` statement
- **THEN** the subcommand asks the user for the concrete research topic and does not create or overwrite `topic.intent.overview`

#### Scenario: Missing topic directory uses default base for clear topic
- **WHEN** the user-supplied Research Topic is clear but no Topic Workspace directory is supplied
- **THEN** the subcommand derives a provisional topic seed directory under the effective Topic Workspace base, normally `isomer-content/topic-ws/<topic-slug>/`, before creating source intent material

#### Scenario: Default base comes from manifest or built-in layout
- **WHEN** `init-topic` derives a provisional topic seed directory
- **THEN** it uses the Project Manifest `topic_workspace_base_dir` when present and otherwise uses the built-in `isomer-content/topic-ws/` base

#### Scenario: Ambiguous derived directory prompts user
- **WHEN** the derived provisional topic seed directory already exists or would collide with registered or unrelated Project material
- **THEN** the subcommand asks the user to confirm or provide a different Topic Workspace directory before creating or modifying source intent material

#### Scenario: Explicit topic directory still wins
- **WHEN** the user supplies a Topic Workspace directory explicitly
- **THEN** the subcommand uses that directory after confirming it is clear and project-scoped according to this skill's guardrails

#### Scenario: Topic overview is created through topic intent resolution
- **WHEN** the user confirms a Research Topic and Topic Workspace directory or the subcommand derives a clear default directory
- **THEN** the subcommand creates the directory and routes topic understanding to `resolve-topic-intent`
- **AND** `resolve-topic-intent` writes `topic.intent.overview`

#### Scenario: Topic overview has required sections
- **WHEN** `topic.intent.overview` is written
- **THEN** it includes sections for the Research Topic, agent understanding, scope, goals or objectives, metrics, required datasets, explicitly mentioned repositories, explicitly mentioned libraries or tools, assumptions, open questions, and source prompt or source material

#### Scenario: Provisional status is reported
- **WHEN** `init-topic` creates source intent material that is not registered in the Project Manifest
- **THEN** the subcommand reports that the topic directory is a provisional Topic Workspace seed and is not yet an authoritative Isomer Research Topic or Topic Workspace registration
- **AND** it names `ensure-topic-registration` as the next registration action when downstream steps require authoritative refs

#### Scenario: Project config mutation routes through registration assurance
- **WHEN** `init-topic` needs the new topic to become an authoritative Project Manifest-registered Research Topic
- **THEN** it routes to `ensure-topic-registration`, which uses `isomer-cli project topics create <topic-id> --statement "<research topic>" --workspace-dir <topic-workspace-dir>` or another supported Isomer CLI/API path
- **AND** it does not hand-edit `.isomer-labs/manifest.toml` or Research Topic Config files
- **AND** it does not use `isomer-cli project init`

#### Scenario: Specialization waits for explicit topic readiness
- **WHEN** `fast-forward` or `step-by-step` cannot resolve a registered Research Topic but can create a provisional seed through `init-topic`
- **THEN** the workflow reports the provisional seed, runs or offers `resolve-topic-intent` and `ensure-topic-registration`, and stops on registration blockers before proceeding to template adaptation that requires authoritative topic refs

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
The module skill SHALL present the primary user-facing flow as procedural subcommands for project resolution, topic and intent resolution, topic env source gate resolution, topic env derived spec creation, topic env materialization, agent env source gate resolution, agent env derived spec creation, agent env materialization, static readiness validation, final summary, and explicit approval or materialization boundaries.

#### Scenario: Flow order is documented
- **WHEN** help text, workflow text, or operator documentation describes the normal user-facing path
- **THEN** it presents the order as `resolve-project`, `resolve-topic-intent`, `resolve-topic-env-gate`, derive `topic.env.topic_setup_target_spec`, materialize topic env, `resolve-agent-env-gate`, derive `topic.env.agent_setup_target_spec`, materialize agent env, `validate-topic-team`, `finalize-topic-team`, then explicit `approve-profile` or `materialize-profile` when requested
- **AND** it does not present Topic Workspace environment setup as requiring an existing Topic Agent Team Profile Bundle

#### Scenario: Procedural subcommands refuse missing predecessor artifacts
- **WHEN** a procedural subcommand after `init-topic` is selected and the artifacts expected from its predecessor steps are missing
- **THEN** the subcommand refuses to run, explains which predecessor artifacts are missing, and tells the user which previous subcommand should create them
- **AND** `setup-topic-env` treats manifest-backed topic registration, Topic Workspace Pixi binding evidence, and a usable `topic.intent.topic_env_requirements` surface as its predecessor requirements instead of requiring specialization outputs or team-profile material

#### Scenario: Init topic has no predecessor artifact requirement
- **WHEN** `init-topic` is selected
- **THEN** it states that no predecessor artifacts are required because it is the first procedural step

#### Scenario: Resolve topic intent creates canonical topic overview
- **WHEN** the user asks to understand, summarize, seed, or revise the Research Topic before team specialization
- **THEN** the skill routes to `resolve-topic-intent` and writes or updates `topic.intent.overview`

#### Scenario: Clarify topic revises topic overview
- **WHEN** the user asks to refine, answer open questions, or clarify the Research Topic after topic intent exists
- **THEN** the skill routes to `clarify-topic` and updates or reports revisions to `topic.intent.overview` without specializing the team yet

#### Scenario: Ensure registration prepares authoritative refs
- **WHEN** the user asks to continue from a provisional topic seed or before any registration-dependent workflow step
- **THEN** the skill routes to `ensure-topic-registration`, verifies or creates Project Manifest-backed Research Topic and Topic Workspace registration through supported Isomer surfaces, verifies required environment binding state, and reports registration blockers

#### Scenario: Resolve topic env gate prepares source setup contract
- **WHEN** the user asks to prepare topic-level environment intent or when setup-topic-env would otherwise need to infer source requirements
- **THEN** the skill routes to `resolve-topic-env-gate` and writes or updates `topic.intent.topic_env_requirements`
- **AND** it keeps the gate high level and source-editable

#### Scenario: Topic environment setup can run before team specialization
- **WHEN** the user asks to prepare the Topic Workspace development environment after `ensure-topic-registration`
- **AND** `topic.intent.topic_env_requirements` exists and is usable
- **THEN** the skill routes to `setup-topic-env` without requiring `adapt-team-template`, `team-profile/`, Topic Agent Team Profile material, Agent Team Instance records, agent roles, or agent count
- **AND** it records the service output as durable setup evidence

#### Scenario: Direct specialize request runs full flow
- **WHEN** the user asks to specialize a team over a topic, such as `specialize <team-path> over topic <topic>`
- **THEN** the skill routes to `fast-forward`, carries the supplied team path as the selected Domain Agent Team Template, carries the supplied topic as the Research Topic input, and runs the full topic-team setup path rather than calling the internal template-adaptation stage directly

#### Scenario: Adapt team template selects domain team
- **WHEN** the user explicitly asks for `adapt-team-template` after the topic is clear and registration blockers are resolved
- **THEN** the skill asks the user to select or confirm one Domain Agent Team Template, copies it into the Topic Workspace, maps placeholders, and adapts copied template material against the topic material

#### Scenario: Adapt team template creates topic team material
- **WHEN** `adapt-team-template` completes its template-adaptation work
- **THEN** it reports the created or updated Topic Agent Team Profile Bundle inputs, copied template material, placeholder resolutions, deferrals, validation refs, and next operator action

#### Scenario: Clarify topic team revises specialization
- **WHEN** the user asks to revise the specialized team, adjust roles, change assumptions, or answer open questions about the proposed topic team
- **THEN** the skill routes to `clarify-topic-team` and updates or reports revisions to the specialization outputs without claiming approval, materialization, or live operation

#### Scenario: Topic environment setup remains explicit
- **WHEN** the Topic Workspace needs a development environment before research work can start or when specialization changes topic-level runnable requirements
- **THEN** the skill requires `ensure-topic-registration` evidence and `resolve-topic-env-gate` source gate evidence first, then routes to `setup-topic-env`, runs or reports explicit environment setup steps, and records environment setup status, commands, blockers, and validation refs
- **AND** it does not require topic-team specialization material unless the requested topic-level runnable target explicitly depends on files produced by specialization

#### Scenario: Resolve agent env gate prepares source setup contract
- **WHEN** the specialized topic team has authoritative Agent Names or the caller provides an explicit selected-agent scope and asks for Agent Workspace cwd readiness
- **THEN** the skill routes to `resolve-agent-env-gate` and writes or updates `topic.intent.agent_env_requirements`
- **AND** it keeps the gate high level and source-editable

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
- **THEN** the skill treats it as an execution mode that runs the same required path as project resolution, topic intent creation, topic env source intent creation, topic env derived spec creation, topic env materialization, agent env source intent creation when per-agent readiness is in scope, agent env derived spec creation, agent env materialization, validation, and final topic-team summary output

#### Scenario: Step-by-step remains guided execution mode
- **WHEN** the user asks for `step-by-step`
- **THEN** the skill treats it as the guided form of the same user-facing path and waits for confirmation between project resolution, topic intent creation, topic env source intent creation, topic env derived spec creation, topic env materialization, agent env source intent creation when in scope, agent env derived spec creation, agent env materialization, validation, and finalization steps

#### Scenario: Procedural subcommands offer prerequisite recovery
- **WHEN** a procedural subcommand after `init-topic` is selected and the artifacts expected from its predecessor steps are missing
- **THEN** the subcommand refuses to run directly, explains which predecessor artifacts are missing, and offers targeted fast-forward recovery to the selected subcommand
- **AND** the recovery offer presents inclusive mode as the default, which runs missing predecessor stages and then runs the selected subcommand
- **AND** the recovery offer presents exclusive mode as an alternative, which runs missing predecessor stages and stops before the selected subcommand
- **AND** `setup-topic-env` treats manifest-backed topic registration, Topic Workspace Pixi binding evidence, and a usable `topic.intent.topic_env_requirements` surface as its predecessor requirements instead of requiring specialization outputs or team-profile material

#### Scenario: Targeted fast-forward is bounded by selected subcommand
- **WHEN** targeted fast-forward recovery starts for a selected subcommand
- **THEN** the skill runs the canonical predecessor path only as far as the selected subcommand requires
- **AND** it does not continue through later specialization stages, validation, finalization, approval, or materialization unless those later stages are part of the selected target or explicitly requested by the user

#### Scenario: Inclusive targeted fast-forward runs target
- **WHEN** the user accepts targeted fast-forward recovery without choosing a mode
- **THEN** the skill uses inclusive mode
- **AND** it runs the missing predecessor subcommands in canonical order and then runs the originally selected subcommand when prerequisites are satisfied

#### Scenario: Exclusive targeted fast-forward stops before target
- **WHEN** the user chooses exclusive targeted fast-forward recovery
- **THEN** the skill runs the missing predecessor subcommands in canonical order
- **AND** it stops before running the originally selected subcommand and reports that the target is now ready or names any remaining blocker

#### Scenario: Targeted fast-forward asks before mutation
- **WHEN** targeted fast-forward recovery would create or update topic intent, registration, derived target specs, environment material, topic-team material, Agent Workspace material, or validation summaries
- **AND** the user has not already given clear permission to proceed automatically
- **THEN** the skill asks the user to confirm inclusive mode, choose exclusive mode, or stop before performing the mutation

### Requirement: Topic Environment Setup is Explicit
The module skill SHALL route topic environment setup through `isomer-srv-topic-env-setup` and SHALL treat the setup as durable Topic Workspace preparation. The skill SHALL NOT block environment setup solely because the Project Manifest lacks an explicit `topic_standalone_pixi_bindings` entry when Pixi can resolve the registered Topic Workspace directory as the default Topic Workspace Pixi binding target. The skill SHALL NOT block environment setup solely because topic-team specialization material is absent.

#### Scenario: Setup delegates to environment service
- **WHEN** the Topic Workspace needs a development environment before research work can start
- **THEN** the skill routes to `setup-topic-env`, requires or reuses `topic.intent.topic_env_requirements`, and delegates environment setup to `isomer-srv-topic-env-setup`
- **AND** it does not perform dependency inference, repo acquisition, Pixi installation, source gate generation, or verification directly inside the operator subcommand

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
- **THEN** the operator subcommand still delegates environment setup to `isomer-srv-topic-env-setup`
- **AND** it records absent team-profile material only as unrelated or downstream topic-team context

#### Scenario: Setup records environment status
- **WHEN** `setup-topic-env` completes or stops on a blocker
- **THEN** it records environment setup status, commands run, changed files, validation refs, and blockers as durable static preparation evidence

### Requirement: Topic Team Specialization Consumes Operation Classification Evidence
The Topic Team Specialization operator skill SHALL rely on delegated service outputs for operation classification and bounded-run evidence instead of defining heavy-operation categories itself.

#### Scenario: Operator requires classification evidence from topic env service
- **WHEN** Topic Team Specialization delegates Topic Workspace environment setup to `isomer-srv-topic-env-setup`
- **THEN** the operator output contract expects classification source, classification result, resource dimensions, bounded guidance when required, and blockers from the delegated service output
- **AND** the operator does not classify operations from a fixed heavy-operation category list before delegation

#### Scenario: Operator requires classification evidence from agent env service
- **WHEN** Topic Team Specialization delegates Agent Workspace environment setup to `isomer-srv-agent-env-setup`
- **THEN** the operator output contract expects per-agent or matrix-scope classification source, classification result, resource dimensions, bounded guidance when required, selected-agent partial scope when used, and blockers from the delegated service output
- **AND** the operator does not classify per-agent operations from a fixed heavy-operation category list before delegation

#### Scenario: Operator examples remain non-normative
- **WHEN** Topic Team Specialization documentation gives examples of operations that often need bounded handling
- **THEN** it states that `isomer-misc-bounded-run-tips` owns the classification decision
- **AND** it treats the examples as reader guidance rather than the definition of heavy operation

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

#### Scenario: Topic-main setup is not workspace-manager work in the canonical path
- **WHEN** the normal topic-team setup path needs `topic.repos.main`
- **THEN** `isomer-admin-topic-team-specialize` gets that evidence through `setup-topic-env` and `isomer-srv-topic-env-setup`
- **AND** it does not route canonical Topic Main Development Repository creation to `isomer-admin-topic-workspace-mgr`

#### Scenario: Setup agent workspace delegates agent worktree setup
- **WHEN** `setup-agent-workspace` determines that the selected topic team needs Git-backed Agent Workspaces under resolved `agent.workspace` paths
- **THEN** it routes per-agent worktree creation and cwd verification through `isomer-srv-agent-env-setup` after Topic Main Development Repository predecessor evidence exists
- **AND** it does not create the worktrees itself

#### Scenario: Workspace manager remains optional
- **WHEN** the operator asks for read-only topology inspection, branch helper operations, boundary summaries, or legacy compatibility diagnostics
- **THEN** the skill may route that bounded work to `isomer-admin-topic-workspace-mgr`
- **AND** it records that evidence separately from topic env materialization and agent env readiness evidence

### Requirement: Clarification Option Loop
The module skill SHALL make `clarify-topic` and `clarify-topic-team` use a bounded option-asking clarification loop that updates static topic-team artifacts directly instead of creating separate user-decision records.

#### Scenario: Topic clarification scans and asks focused questions
- **WHEN** the `clarify-topic` subcommand runs after its predecessor artifacts exist
- **THEN** it performs a coverage and clarity scan of `topic.intent.overview`, identifies unresolved questions that materially affect topic scope, objectives, assumptions, open questions, or template selection, and asks at most one focused clarification question at a time

#### Scenario: Team clarification scans and asks focused questions
- **WHEN** the `clarify-topic-team` subcommand runs after its predecessor artifacts exist
- **THEN** it performs a coverage and clarity scan of the topic overview, copied template material, `team-specialization-guide.md`, `team-specialization-plan.md`, `Final Report`, placeholder resolutions, deferrals, and draft packet/profile inputs, then asks at most one focused clarification question at a time about role, workflow, policy, binding, copied-material, setup, validation, or blocker ambiguity

#### Scenario: Clarification question format is structured
- **WHEN** either `clarify-topic` or `clarify-topic-team` asks a clarification question
- **THEN** the question includes a motivation, a concrete example when useful, a proposed answer or option with rationale, the downstream implication of accepting it, and either two to five mutually exclusive options with a custom short-answer path or a short-answer prompt with a proposed answer

#### Scenario: Clarification answers update topic material directly
- **WHEN** the user answers a `clarify-topic` question clearly or accepts the proposed answer
- **THEN** the subcommand validates the answer, updates `topic.intent.overview` directly, removes or revises resolved open questions and obsolete assumptions, and reports remaining open questions and readiness for `adapt-team-template`

#### Scenario: Clarification answers update team material directly
- **WHEN** the user answers a `clarify-topic-team` question clearly or accepts the proposed answer
- **THEN** the subcommand validates the answer, updates the relevant copied topic-team material, specialization plan, `Final Report`, placeholder resolutions, deferrals, or draft packet/profile inputs directly, and reports changed paths, remaining blockers, and readiness for setup or validation

#### Scenario: Clarification loop does not create decision logs
- **WHEN** either clarification subcommand completes
- **THEN** it does not create standalone decision-log files for the clarification unless a separate workflow explicitly asks for that artifact

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
- **THEN** the Agent Workspace layout or environment section includes `topic.intent.agent_env_requirements`, `topic.env.agent_setup_target_spec`, and their resolved paths when those surfaces exist

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

### Requirement: Operator Owns Environment Setup Orchestration
The Topic Team Specialization module skill SHALL own the decision to invoke Topic Workspace environment setup, Git-backed Agent Workspace topology setup, and Agent Workspace environment readiness setup.

#### Scenario: Topic setup is delegated only from operator topic setup
- **WHEN** `isomer-admin-topic-team-specialize setup-topic-env` runs after registration and Topic Workspace Pixi binding evidence exists
- **THEN** it delegates Topic Workspace dependency, repo acquisition, Pixi mutation, and topic-root verification work to `isomer-srv-topic-env-setup`
- **AND** it records topic env setup evidence as Topic Workspace predecessor evidence
- **AND** it does not treat that evidence as per-Agent Workspace cwd readiness

#### Scenario: Agent setup is delegated only from operator agent workspace setup
- **WHEN** `isomer-admin-topic-team-specialize setup-agent-workspace` receives a request for `agent-env-gate.md`, per-Agent Workspace cwd verification, selected-agent repair, or launch-facing Agent Workspace readiness
- **THEN** it ensures a usable `user-intent/src/agent-env-gate.md` exists or asks for the missing per-agent readiness target
- **AND** after Topic Workspace environment readiness and Git topology evidence exist, it delegates gate-driven Agent Workspace environment setup to `isomer-srv-agent-env-setup`

#### Scenario: Git topology remains workspace manager work
- **WHEN** Git-backed `topic.repos.main`, per-agent `agent.workspace` worktrees, branch plans, worker-facing support paths, or Workspace Boundary material are needed
- **THEN** Topic Team Specialization delegates that topology to `isomer-admin-topic-workspace-mgr`
- **AND** it records the workspace manager evidence separately from topic env setup evidence and agent env setup evidence

#### Scenario: Topic setup is delegated only after derived topic target spec exists
- **WHEN** `isomer-admin-topic-team-specialize setup-topic-env` runs after registration and Topic Workspace Pixi binding evidence exists
- **THEN** it ensures `topic.intent.topic_env_requirements` and `topic.env.topic_setup_target_spec` exist or reports blockers
- **AND** it delegates Topic Main Development Repository setup, external repo acquisition, external projection materialization, Pixi mutation, and topic-root or repo-specific verification work to `isomer-srv-topic-env-setup`
- **AND** it records topic env setup evidence as Topic Workspace predecessor evidence
- **AND** it does not treat that evidence as per-Agent Workspace cwd readiness

#### Scenario: Agent setup is delegated after topic-main readiness exists
- **WHEN** `isomer-admin-topic-team-specialize setup-agent-workspace` receives a request for per-Agent Workspace cwd verification, selected-agent repair, or launch-facing Agent Workspace readiness
- **THEN** it ensures `topic.intent.agent_env_requirements`, `topic.env.agent_setup_target_spec`, Topic Workspace env readiness, authoritative Agent Names, and Topic Main Development Repository predecessor evidence exist or reports blockers
- **AND** it delegates gate-driven Agent Workspace environment setup to `isomer-srv-agent-env-setup`

#### Scenario: Derived gates are orchestrator-owned in normal flow
- **WHEN** the normal topic-team setup flow creates operational target specs
- **THEN** `isomer-admin-topic-team-specialize` owns the creation or update of `topic.env.topic_setup_target_spec` and `topic.env.agent_setup_target_spec`
- **AND** direct service invocation may still accept explicit target specs outside the normal operator flow

### Requirement: Validation Distinguishes Topic and Agent Readiness Evidence
The Topic Team Specialization module skill SHALL validate topic environment readiness and Agent Workspace readiness as separate static setup evidence streams.

#### Scenario: Topic env evidence cannot satisfy agent env evidence
- **WHEN** `validate-topic-team` or `finalize-topic-team` reads setup evidence
- **THEN** readiness from `isomer-srv-topic-env-setup` may satisfy only Topic Workspace environment setup evidence
- **AND** per-Agent Workspace cwd readiness requires `isomer-srv-agent-env-setup` evidence when that proof was requested

#### Scenario: Missing agent env proof is explicit
- **WHEN** per-Agent Workspace cwd verification was requested but `isomer-srv-agent-env-setup` evidence is missing
- **THEN** Topic Team Specialization reports an explicit blocker or deferral for Agent Workspace environment readiness
- **AND** it does not infer readiness from topic-root verification, Pixi install success, or Git topology readiness

#### Scenario: Topic env ready requires complete topic checklist evidence
- **WHEN** `validate-topic-team` or `finalize-topic-team` consumes `isomer-srv-topic-env-setup` output that reports Topic Workspace environment readiness as `ready`
- **THEN** the operator evidence includes `topic.env.topic_setup_target_spec`, its `Gate Checklist`, and confirmation that every required checklist item is checked with supporting execution, path, dependency, resource, or expected-result evidence
- **AND** the operator does not treat topic env setup as ready when required checklist items are unchecked, missing, or completed only by a weaker smoke test that does not prove the named critical path

#### Scenario: Agent env ready requires complete per-agent checklist evidence
- **WHEN** `validate-topic-team` or `finalize-topic-team` consumes `isomer-srv-agent-env-setup` output that reports Agent Workspace environment readiness as `ready`
- **THEN** the operator evidence includes `topic.env.agent_setup_target_spec`, its `Gate Checklist`, readiness by Agent Name, and confirmation that every planned Agent Name has every required checklist item checked with supporting cwd execution, path, dependency, resource, projection, or expected-result evidence
- **AND** selected-agent partial evidence does not satisfy overall Agent Workspace environment readiness unless the complete planned Agent Name matrix has already passed

#### Scenario: Incomplete checklist item blocks static readiness
- **WHEN** delegated topic env or agent env evidence contains a required unchecked checklist item
- **THEN** `validate-topic-team` reports static setup readiness as blocked, failed, or not checked according to the delegated evidence
- **AND** it names the incomplete checklist item, owning target spec, reason, and next safe repair action

#### Scenario: Smoke-test downgrade remains visible
- **WHEN** delegated env setup evidence records that the user accepted a weaker smoke test instead of the original critical-path checklist item
- **THEN** `validate-topic-team` and `finalize-topic-team` preserve that limitation in validation and summary output
- **AND** they do not describe the weaker evidence as proof that the original critical path passed

### Requirement: Topic Intent Semantic Surfaces
The Topic Team Specialization module skill SHALL treat semantic labels, not hard-coded paths, as the canonical user-editable source specification surfaces for one Research Topic.

#### Scenario: Topic overview source label is canonical
- **WHEN** topic-team specialization creates or revises the user's topic understanding
- **THEN** it resolves `topic.intent.overview` and writes or updates the resolved path
- **AND** the default `isomer-default.v1` path for that label is `<topic-workspace>/intent/src/topic-overview.md`
- **AND** it does not write new canonical topic understanding material to `<topic-workspace>/topic-def/topic-overview.md`

#### Scenario: Topic env source gate label is canonical
- **WHEN** topic-team specialization records high-level Topic Workspace environment needs
- **THEN** it resolves `topic.intent.topic_env_requirements` and writes or updates the resolved path
- **AND** the default `isomer-default.v1` path for that label is `<topic-workspace>/intent/src/topic-env-gate.md`
- **AND** that file remains user-editable source intent rather than an implementation command matrix

#### Scenario: Agent env source gate label is canonical
- **WHEN** topic-team specialization records high-level per-Agent Workspace cwd needs
- **THEN** it resolves `topic.intent.agent_env_requirements` and writes or updates the resolved path
- **AND** the default `isomer-default.v1` path for that label is `<topic-workspace>/intent/src/agent-env-gate.md`
- **AND** that file remains user-editable source intent rather than a generated verification matrix

#### Scenario: Derived implementation material is separate
- **WHEN** setup services derive commands, dependency plans, package-source choices, repo acquisition details, cwd matrices, expected outputs, or execution logs
- **THEN** those implementation-specific details are written to `topic.env.topic_setup_target_spec` or `topic.env.agent_setup_target_spec`
- **AND** the default `isomer-default.v1` paths for those labels are under `<topic-workspace>/intent/derived/`
- **AND** they are not written into source intent files unless the user explicitly supplied the exact detail as part of the source intent

#### Scenario: Intent resolution output includes path metadata
- **WHEN** a topic-team specialization subcommand reads, writes, validates, or reports an intent or target-spec surface
- **THEN** its output includes the semantic label, resolved path, storage profile, source, source detail, and any blocker diagnostics available from Workspace Path Resolution

### Requirement: Canonical Team Specialization Process Order
The Topic Team Specialization module skill SHALL present and execute the setup path as project resolution, source intent creation, derived operational spec creation, materialization, and validation stages.

#### Scenario: Process starts with project resolution
- **WHEN** Topic Team Specialization is invoked for a Research Topic
- **THEN** the skill first resolves the Project, Research Topic registration context, Topic Workspace candidate, and relevant Project Manifest evidence through `resolve-project` or equivalent project resolution logic
- **AND** it does not create or mutate topic intent files until the target Project and Topic Workspace context are known or an explicit blocker is reported

#### Scenario: Topic intent precedes topic env intent
- **WHEN** project resolution has identified a safe Topic Workspace candidate or registered Topic Workspace
- **THEN** the process resolves the topic and creates `topic.intent.overview`
- **AND** it resolves topic env requirements and creates `topic.intent.topic_env_requirements` only after topic intent exists or an explicit topic-intent blocker is recorded

#### Scenario: Topic env derivation precedes materialization
- **WHEN** `topic.intent.topic_env_requirements` exists and topic env setup is requested
- **THEN** the process creates `topic.env.topic_setup_target_spec` from that source intent before materializing the Topic Workspace environment
- **AND** materialization uses the derived operational spec instead of reinterpreting the source intent directly

#### Scenario: Agent env derivation precedes materialization
- **WHEN** topic env evidence exists and Agent Workspace environment readiness is requested
- **THEN** the process resolves agent env requirements and creates `topic.intent.agent_env_requirements`
- **AND** it creates `topic.env.agent_setup_target_spec` from that source intent before materializing Agent Workspace environment readiness
- **AND** materialization uses the derived operational spec instead of reinterpreting the source intent directly

#### Scenario: Validation follows materialization
- **WHEN** topic env and requested agent env materialization have completed, blocked, or been explicitly deferred
- **THEN** the process runs `validate-topic-team`
- **AND** validation reports separate source intent, derived spec, materialization evidence, blockers, and deferrals

### Requirement: Intent Resolution Subcommands
The Topic Team Specialization module skill SHALL provide `resolve-topic-intent`, `resolve-topic-env-gate`, and `resolve-agent-env-gate` as procedural subcommands that resolve high-level source intent before setup execution.

#### Scenario: Resolve topic intent writes topic overview
- **WHEN** `resolve-topic-intent` receives a concrete Research Topic, source prompt, existing topic material, or registered topic statement
- **THEN** it resolves `topic.intent.overview` and writes the resolved path with the goal, metrics, required datasets, explicitly mentioned repositories, explicitly mentioned libraries or tools, assumptions, open questions, and source material
- **AND** it avoids dependency versions unless the source topic context explicitly names versions

#### Scenario: Resolve topic env gate writes high-level topic gate
- **WHEN** `resolve-topic-env-gate` receives enough topic intent to describe shared Topic Workspace environment needs
- **THEN** it resolves `topic.intent.topic_env_requirements` and writes the resolved path
- **AND** it records concise high-level requirements such as required tools, libraries, datasets, repos, or runnable capabilities
- **AND** it leaves concrete setup commands and verification commands for the topic env service to derive into `topic.env.topic_setup_target_spec`

#### Scenario: Resolve agent env gate writes high-level agent gate
- **WHEN** `resolve-agent-env-gate` receives authoritative Agent Names or an explicit partial Agent Workspace scope plus enough topic-team material to describe per-agent cwd needs
- **THEN** it resolves `topic.intent.agent_env_requirements` and writes the resolved path
- **AND** it records concise high-level per-Agent Workspace requirements without deriving the command matrix itself

#### Scenario: Missing source intent remains a blocker
- **WHEN** a resolve subcommand cannot infer a high-level source requirement without guessing
- **THEN** it records open questions or blockers in the relevant source file or report
- **AND** setup subcommands do not proceed as if the missing source gate exists

### Requirement: Topic Team Specialization Uses Essential and Complete Output
The Topic Team Specialization operator skill SHALL split its output contract into Essential Output and Complete Output.

#### Scenario: Essential specialization output reports user-facing progress
- **WHEN** `isomer-admin-topic-team-specialize` reports a result without a complete-output request
- **THEN** it reports the selected Research Topic and Topic Workspace, registration status, selected Domain Agent Team Template, topic-team material status, topic environment status, agent environment status when checked, validation status, blockers, and next action
- **AND** it names important created or changed paths such as topic overview, copied team material, environment gates, and final summary when those paths exist

#### Scenario: Complete specialization output preserves handoff detail
- **WHEN** complete output is requested from `isomer-admin-topic-team-specialize`
- **THEN** it reports registration evidence, environment binding evidence, copied material paths, placeholder resolutions, source and target intent paths, delegated service outputs, semantic path evidence, Agent Workspace paths, tmp posture, validation details, deferrals, packet/profile inputs, blockers, and next action

#### Scenario: Delegated service output remains summarized by default
- **WHEN** topic or agent environment services return large output payloads during specialization
- **THEN** Essential Output summarizes their readiness, blockers, important paths, and next action
- **AND** Complete Output may include the full delegated service output or the complete field groups needed for handoff

### Requirement: Breaking Topic Team Setup Order
The Topic Team Specialization module skill SHALL present the revised setup order as a breaking replacement for old generated Topic Workspace internals.

#### Scenario: Revised order is canonical
- **WHEN** help text, workflow text, or operator documentation describes the normal setup path
- **THEN** it presents the order as `resolve-project`, `resolve-topic-intent`, `resolve-topic-env-gate`, create `topic.env.topic_setup_target_spec`, materialize topic env including Topic Main Development Repository and projections, `specialize-team` when team material is needed, `resolve-agent-env-gate`, create `topic.env.agent_setup_target_spec`, materialize agent env worktrees and cwd proof, `validate-topic-team`, and `finalize-topic-team`

#### Scenario: Old generated internals are not preserved
- **WHEN** existing generated `isomer-content/` internals conflict with the revised setup order
- **THEN** the skill reports that generated topic content should be recreated
- **AND** it does not require compatibility steps for the old internal layout

### Requirement: Centralized Step Dependency Contract
The Topic Team Specialization module skill SHALL centralize procedural step dependencies, recovery paths, produced artifacts, and blocker metadata in a machine-readable dependency manifest and SHALL provide a local script for querying that manifest.

#### Scenario: Dependency manifest and query script exist
- **WHEN** the `isomer-admin-topic-team-specialize` skill bundle is inspected
- **THEN** it contains `references/step-dependencies.json`
- **AND** it contains `scripts/query_step_dependencies.py`

#### Scenario: Manifest covers procedural subcommands
- **WHEN** `references/step-dependencies.json` is inspected
- **THEN** it records every public procedural subcommand in the Topic Team Specialization flow
- **AND** each recorded step includes a step id, display name, kind, required predecessor artifacts or inputs, produced artifacts or outputs, dependency edges or predecessor steps, recovery conditions, mutation notes, and unrecoverable blockers when applicable

#### Scenario: Query script validates graph
- **WHEN** `python skillset/operator/isomer-admin-topic-team-specialize/scripts/query_step_dependencies.py validate` runs from the repository root
- **THEN** it validates that all referenced step ids exist
- **AND** it validates that dependency paths are acyclic
- **AND** it reports an error for missing required fields, unknown targets, invalid edges, or malformed manifest data

#### Scenario: Query script returns targeted recovery paths
- **WHEN** an agent needs a targeted fast-forward recovery path for a selected subcommand
- **THEN** it can run `python skillset/operator/isomer-admin-topic-team-specialize/scripts/query_step_dependencies.py path --target <subcommand> --include-target`
- **AND** the output includes the canonical predecessor path plus the selected subcommand
- **AND** it can run the same command with `--exclude-target` to stop before the selected subcommand

#### Scenario: Query script answers local dependency questions
- **WHEN** an agent needs the prerequisites, produced artifacts, blockers, or explanation for one subcommand
- **THEN** it can query the script with `prereqs`, `produces`, `blockers`, or `explain`
- **AND** the script answers from `references/step-dependencies.json` without reading or mutating the Topic Workspace

#### Scenario: Skill prose delegates recovery paths to script
- **WHEN** the skill entrypoint, `fast-forward`, or procedural subcommand pages describe missing-prerequisite recovery
- **THEN** they instruct the agent to query `scripts/query_step_dependencies.py` for dependency paths
- **AND** they avoid duplicating long full recovery chains that are already represented in `references/step-dependencies.json`
- **AND** they preserve local prose for subcommand purpose, local evidence requirements, safety blockers, and information the agent must not invent

#### Scenario: Validation checks centralized contract
- **WHEN** `pixi run python scripts/validate_skillsets.py --scope operator` runs
- **THEN** it verifies that the dependency manifest and query script exist
- **AND** it verifies that the query script can validate the manifest
- **AND** it verifies that the manifest covers the topic-team procedural subcommands
- **AND** it does not require every procedural subcommand page to duplicate the full targeted fast-forward path in prose

### Requirement: Team Specialization Consumes Prepared Topic and Actor Context
The Topic Team Specialization skill SHALL treat reusable topic preparation and existing Topic Actor bindings as predecessor context that can coexist with team-specific material.

#### Scenario: Prepared topic satisfies reusable prerequisites
- **WHEN** Topic Team Specialization starts with valid prepared-topic evidence for the selected Research Topic
- **THEN** it consumes the Research Topic ref, Topic Workspace ref, topic overview, topic environment readiness, Topic Main Development Repository readiness, runtime readiness, storage bootstrap refs, current Topic Actor roster, and Topic Actor Workspace refs
- **AND** it proceeds to team template adaptation, Topic Agent Team Profile material, agent environment gate resolution, formal Agent Workspace setup, validation, and team summary work without recreating the common topic preparation artifacts

#### Scenario: Full team fast-forward delegates common preparation
- **WHEN** the user asks for full Topic Team Specialization and the selected topic is not prepared
- **THEN** the specialization flow runs or delegates common topic preparation before team-specific steps
- **AND** the final team summary records which common preparation refs and Topic Actor refs were used or preserved

### Requirement: Team Specialization Preserves Topic Actors
The Topic Team Specialization skill SHALL keep Topic Actor bindings and formal team material separate.

#### Scenario: Existing actors are not removed by team specialization
- **WHEN** Topic Team Specialization runs in a Topic Workspace with active Topic Actor bindings
- **THEN** the flow preserves those bindings and Topic Actor Workspace refs unless the user explicitly asks to remove or archive them through the Topic Workspace Manager actor-management workflow

#### Scenario: Actor preparation does not create team material
- **WHEN** common topic preparation or human-orchestrated actor preparation runs
- **THEN** Topic Team Specialization requirements for Domain Agent Team Template adaptation, Topic Agent Team Profile Bundle materialization, formal per-Agent Workspace setup, and launch approval remain unsatisfied until the team specialization workflow runs

