## MODIFIED Requirements

### Requirement: User-Facing Topic Team Flow
The module skill SHALL present the primary user-facing flow as procedural subcommands for project resolution, topic and intent resolution, topic env source gate resolution, topic env derived spec creation, topic env materialization, agent env source gate resolution, agent env derived spec creation, agent env materialization, static readiness validation, final summary, and explicit approval or materialization boundaries.

#### Scenario: Flow order is documented
- **WHEN** help text, workflow text, or operator documentation describes the normal user-facing path
- **THEN** it presents the order as `resolve-project`, `resolve-topic-intent`, `resolve-topic-env-gate`, derive `topic.env.topic_setup_target_spec`, materialize topic env, `resolve-agent-env-gate`, derive `topic.env.agent_setup_target_spec`, materialize agent env, `validate-topic-team`, `finalize-topic-team`, then explicit `approve-profile` or `materialize-profile` when requested
- **AND** it does not present Topic Workspace environment setup as requiring an existing Topic Agent Team Profile Bundle

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
