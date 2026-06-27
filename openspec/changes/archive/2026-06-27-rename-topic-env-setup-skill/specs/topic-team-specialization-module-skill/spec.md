## MODIFIED Requirements

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
