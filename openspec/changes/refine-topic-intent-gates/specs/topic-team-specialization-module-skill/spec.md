## ADDED Requirements

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

## MODIFIED Requirements

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

### Requirement: Topic Environment Setup is Explicit
The module skill SHALL route topic environment setup through `isomer-srv-topic-env-setup` and SHALL treat the setup as durable Topic Workspace preparation. The skill SHALL NOT block environment setup solely because the Project Manifest lacks an explicit `topic_standalone_pixi_bindings` entry when Pixi can resolve the registered Topic Workspace directory as the default Topic Workspace Pixi binding target. The skill SHALL NOT block environment setup solely because topic-team specialization material is absent.

#### Scenario: Setup delegates to environment service
- **WHEN** the Topic Workspace needs a development environment before research work can start
- **THEN** the skill routes to `setup-topic-env`, requires or reuses `topic.intent.topic_env_requirements`, and delegates heavy environment setup to `isomer-srv-topic-env-setup`
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
- **THEN** the operator subcommand still delegates heavy environment setup to `isomer-srv-topic-env-setup`
- **AND** it records absent team-profile material only as unrelated or downstream topic-team context

#### Scenario: Setup records environment status
- **WHEN** `setup-topic-env` completes or stops on a blocker
- **THEN** it records environment setup status, commands run, changed files, validation refs, and blockers as durable static preparation evidence

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
- **THEN** the subcommand validates the answer, updates `topic.intent.overview` directly, removes or revises resolved open questions and obsolete assumptions, and reports remaining open questions and readiness for `specialize-team`

#### Scenario: Clarification answers update team material directly
- **WHEN** the user answers a `clarify-topic-team` question clearly or accepts the proposed answer
- **THEN** the subcommand validates the answer, updates the relevant copied topic-team material, specialization plan, `Final Report`, placeholder resolutions, deferrals, or draft packet/profile inputs directly, and reports changed paths, remaining blockers, and readiness for setup or validation

#### Scenario: Clarification loop does not create decision logs
- **WHEN** either clarification subcommand completes
- **THEN** it does not create standalone decision-log files for the clarification unless a separate workflow explicitly asks for that artifact

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
