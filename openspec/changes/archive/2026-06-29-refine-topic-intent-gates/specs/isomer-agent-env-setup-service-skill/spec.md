## ADDED Requirements

### Requirement: Agent Env Source Intent is High Level
The agent environment setup service skill SHALL treat `topic.intent.agent_env_requirements` as high-level user-editable source intent and SHALL place per-agent operational verification detail in `topic.env.agent_setup_target_spec`. In the normal operator flow those surfaces are resolved through Workspace Path Resolution; manual service invocation can supply an explicit target spec file, prompt, or context.

#### Scenario: High-level per-agent requirement is valid source intent
- **WHEN** `topic.intent.agent_env_requirements` says that every planned Agent Workspace cwd must support a tool, repository, runtime, dataset access posture, or development capability
- **THEN** the service treats that statement as sufficient source intent for deriving operational checks when the requirement is understandable
- **AND** it does not require the source file to name the exact per-agent command matrix

#### Scenario: Per-agent commands belong in the derived gate
- **WHEN** the service derives per-Agent Workspace commands, cwd assumptions, Topic Main Repository configuration, expected outputs, readiness matrices, or execution logs
- **THEN** it resolves `topic.env.agent_setup_target_spec` and writes those details to the resolved path
- **AND** it does not rewrite `topic.intent.agent_env_requirements` with generated implementation detail

### Requirement: Agent Env Target Spec Precedes Materialization
The agent environment setup service skill SHALL require a derived agent env target spec before it materializes Topic Main Repository configuration, Agent Workspace worktrees, or per-agent cwd verification changes.

#### Scenario: Derived agent env target spec is the materialization input
- **WHEN** `setup-agent-env` runs from `topic.intent.agent_env_requirements`
- **THEN** it creates or updates `topic.env.agent_setup_target_spec` before configuring the Topic Main Repository, creating or validating Agent Workspace worktrees, or running per-agent cwd verification commands
- **AND** those materialization actions use the derived target spec as their execution contract

#### Scenario: Explicit agent env target spec is accepted
- **WHEN** `isomer-srv-agent-env-setup` is invoked manually with an explicit derived gate file, target-spec prompt, or target-spec context
- **THEN** it treats that input as the agent env target spec after checking that it is operational enough to drive service-safe materialization and per-agent cwd verification
- **AND** it records the target spec source in output
- **AND** it does not require `topic.intent.agent_env_requirements` solely because the invocation is manual

#### Scenario: Materialization blocks when target spec is missing
- **WHEN** the service cannot create, load, or validate a usable derived agent env target spec
- **THEN** it reports a blocker
- **AND** it does not materialize Agent Workspace environment readiness from the high-level source intent alone

## MODIFIED Requirements

### Requirement: Topic Env Readiness Is a Predecessor
The service skill SHALL require Topic Workspace Pixi readiness evidence before it claims Agent Workspace environment readiness.

#### Scenario: Topic env gate is required
- **WHEN** `require-topic-env-ready` runs
- **THEN** it checks for the resolved Topic Workspace Pixi manifest path, selected Pixi environment, `pixi.lock`, `.pixi/`, and `topic.env.topic_setup_target_spec`
- **AND** it reports blockers when any predecessor is missing or not ready

#### Scenario: Topic env setup is not duplicated
- **WHEN** Topic Workspace dependency installation or Pixi repair is needed
- **THEN** the service reports a next action to run `isomer-srv-topic-env-setup`
- **AND** it does not create per-agent Pixi manifests, per-agent lockfiles, per-agent `.pixi/` directories, or topic dependency mutations by default

#### Scenario: Topic env gate is consumed as predecessor evidence
- **WHEN** the service derives the agent env gate
- **THEN** it references `topic.env.topic_setup_target_spec` as the topic-level predecessor gate
- **AND** it does not duplicate or reinterpret dependency installation policy as a separate per-agent dependency plan

### Requirement: Source Agent Env Gate
The service skill SHALL use a derived agent env target spec before configuring or verifying Agent Workspace cwd readiness. The target spec can come from `topic.env.agent_setup_target_spec`, derivation from `topic.intent.agent_env_requirements`, or explicit manual input.

#### Scenario: Source agent gate can derive target spec
- **WHEN** `read-agent-env-gate` runs
- **THEN** it resolves `topic.intent.agent_env_requirements`
- **AND** it treats the resolved file as the source of user intent for deriving `topic.env.agent_setup_target_spec` when no explicit target spec is supplied

#### Scenario: Missing source agent gate blocks only when no target spec is supplied
- **WHEN** `topic.intent.agent_env_requirements` is missing, unreadable, or too vague to derive required Agent Workspace cwd checks
- **AND** no explicit derived agent env target spec is supplied
- **THEN** the service reports a blocker instead of claiming Agent Workspace environment readiness
- **AND** it asks for `resolve-agent-env-gate` to create or repair the source gate, or for the caller to provide an explicit target spec, before materialization

#### Scenario: Legacy source agent gate path is not canonical
- **WHEN** `<topic-workspace-dir>/user-intent/src/agent-env-gate.md` exists but `<topic-workspace-dir>/intent/src/agent-env-gate.md` is missing
- **THEN** the service reports a legacy-path blocker naming `topic.intent.agent_env_requirements` and its default-layout path
- **AND** it does not silently treat the legacy file as the canonical source gate

#### Scenario: Source agent gate is interpreted
- **WHEN** `read-agent-env-gate` reads the source gate
- **AND** no explicit derived agent env target spec is supplied
- **THEN** it extracts the source intent, high-level required capabilities, expected results or success criteria when present, Topic Main Repository configuration requirements, agent plan constraints, cwd assumptions, and blockers
- **AND** it treats passing as every derived required command being runnable from each planned `agent.workspace` cwd through the resolved Topic Workspace Pixi environment

#### Scenario: Source agent gate stays inside static setup scope
- **WHEN** the source gate asks for Agent Instance creation, Workspace Runtime mutation, Houmao launch, Execution Adapter launch, live research execution, privileged host mutation, or research decisions
- **THEN** the service reports an out-of-scope blocker instead of deriving executable setup steps for that request

### Requirement: Topic Main Repository and Agent Worktrees
The service skill SHALL create or reuse one shared Topic Main Repository, configure it for the derived agent env gate, and prepare per-agent Agent Workspace worktrees using semantic labels and deterministic branch namespaces.

#### Scenario: Topic Main Repository is normal and non-bare
- **WHEN** `ensure-topic-main-repository` prepares the resolved `topic.repos.main`
- **THEN** the target is a normal non-bare Git repository
- **AND** the owner-managed branch is `topic-owner/main`
- **AND** unsafe existing non-Git, bare, corrupt, or ambiguous paths are reported as blockers without destructive repair

#### Scenario: Missing or empty Topic Main Repository is initialized
- **WHEN** the resolved `topic.repos.main` path is missing, empty, or an empty normal Git repository
- **THEN** the service creates or initializes a normal non-bare Git repository at that path
- **AND** it creates `topic-owner/main`
- **AND** it creates a minimal baseline commit before creating per-agent worktrees

#### Scenario: Existing safe Topic Main Repository is reused
- **WHEN** the resolved `topic.repos.main` path is an existing normal non-bare Git repository with safe reusable history
- **THEN** the service reuses that repository without rewriting, cleaning, resetting, deleting, moving, or recloning it
- **AND** it creates or validates `topic-owner/main` from the accepted current base when the owner branch is missing
- **AND** it reports a blocker when the accepted base is ambiguous

#### Scenario: Topic Main Repository is configured for the agent gate
- **WHEN** `ensure-topic-main-repository` runs after the derived agent env target spec is resolved
- **THEN** it applies non-destructive Topic Main Repository configuration required by `topic.env.agent_setup_target_spec`
- **AND** it records changed files, commands run, semantic path evidence, and blockers in service output and the derived gate execution log
- **AND** it reports a blocker instead of deleting, resetting, cleaning, rewriting history, mutating topic dependencies, or applying ambiguous gate requirements

#### Scenario: Agent worktree uses Topic Main Repository
- **WHEN** `create-agent-worktrees` prepares Agent Name `alice`
- **THEN** it creates or validates the resolved `agent.workspace` path as a Git worktree of the resolved `topic.repos.main`
- **AND** the default branch is `per-agent/alice/main`

#### Scenario: Existing matching worktree is ready
- **WHEN** the resolved `agent.workspace` path already exists as the expected worktree on the expected branch
- **THEN** the service reports it as ready instead of creating another worktree

#### Scenario: Existing nonmatching path blocks creation
- **WHEN** the resolved `agent.workspace` path exists but is not the expected worktree
- **THEN** the service reports a blocker and does not overwrite, delete, move, clean, reset, or reinitialize the path

#### Scenario: Duplicate branch checkout is rejected
- **WHEN** `per-agent/<agent-name>/main` is already checked out in another worktree of the Topic Main Repository
- **THEN** the service reports a blocker instead of force-moving or deleting the existing checkout

### Requirement: Agent Env Gate File
The service skill SHALL resolve a derived per-agent readiness target spec before Agent Workspace materialization. In the normal operator flow, that target spec is `topic.env.agent_setup_target_spec`; in manual service invocation, it can be an explicit derived gate file, prompt, or context supplied by the caller.

#### Scenario: Source and derived agent gate paths are paired in operator flow
- **WHEN** `derive-agent-env-gate` resolves gate paths
- **THEN** it reads the source gate at `topic.intent.agent_env_requirements`
- **AND** it writes the derived gate at `topic.env.agent_setup_target_spec`

#### Scenario: Explicit agent target spec source is recorded
- **WHEN** the service receives an explicit derived gate file, target-spec prompt, or target-spec context from a manual invocation
- **THEN** it records that source in service output and in the execution log when a canonical derived gate is written

#### Scenario: Target spec has fixed sections
- **WHEN** the service generates or accepts the target spec
- **THEN** the file includes sections named `Source Agent Gate`, `Topic Env Gate`, `Topic Pixi Binding`, `Topic Main Repository Configuration`, `Agent Plan`, `Semantic Paths`, `Worktree Plan`, `Verification Matrix`, `Expected Results`, `Blockers`, and `Execution Log`
- **AND** every section is present even when the section content is `None.` or a short reason that it does not apply

#### Scenario: Gate records per-agent cwd commands
- **WHEN** verification commands are defined by the target spec
- **THEN** each command records the source `topic.intent.agent_env_requirements` requirement, Agent Name, cwd as the resolved `agent.workspace`, the `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...` command, and expected result

#### Scenario: Gate records path evidence
- **WHEN** the gate records an Agent Workspace
- **THEN** it includes the relevant semantic labels, resolved paths, path sources, branch plan, and worktree status

#### Scenario: Gate does not record tmp as durable evidence
- **WHEN** the gate mentions tmp labels
- **THEN** it describes them as local ignored disposable surfaces
- **AND** it does not use tmp contents as readiness evidence

### Requirement: Agent Cwd Env Verification
The service skill SHALL verify the Topic Workspace environment from each planned Agent Workspace cwd.

#### Scenario: Commands run from Agent Workspace cwd
- **WHEN** `verify-agent-env-gate` runs a verification command for Agent Name `alice`
- **THEN** the process cwd is the resolved `agent.workspace` for `alice`
- **AND** the command uses the resolved Topic Workspace Pixi manifest and selected Pixi environment

#### Scenario: Passing means required commands run
- **WHEN** `verify-agent-env-gate` reports Agent Name `alice` as ready
- **THEN** every required command from `topic.env.agent_setup_target_spec` for `alice` has passed with the resolved `agent.workspace` as process cwd
- **AND** a command passing from the Topic Workspace root alone does not satisfy the agent gate

#### Scenario: Cwd-friendly agent path query is verified
- **WHEN** an Agent Workspace is prepared
- **THEN** verification includes or records a check that an agent-scoped semantic label can be resolved from inside that Agent Workspace without passing Agent Name

#### Scenario: Topic-root-only pass is insufficient
- **WHEN** the topic env gate passes from the Topic Workspace root but fails from an Agent Workspace cwd
- **THEN** the service does not report agent env readiness
- **AND** it reports a `gate-cwd-incompatible` or equivalent blocker naming the failing agent and command

#### Scenario: Overall readiness requires every agent
- **WHEN** the service reports overall readiness as `ready`
- **THEN** every planned agent has a ready worktree, required support paths, complete path evidence, and passing agent-env-gate verification from that agent's cwd

#### Scenario: Selected-agent verification does not imply overall readiness
- **WHEN** `verify-agent-env-gate` is run for one selected Agent Name
- **THEN** the service updates or reports that agent's verification evidence
- **AND** it does not report `overall_readiness_status` as `ready` unless the complete planned Agent Name matrix has already passed

#### Scenario: Partial results remain visible
- **WHEN** one or more agents fail or block
- **THEN** the service reports readiness by agent, commands run, command outcomes, blockers, and the next safe repair action

### Requirement: Agent Env Setup Consumes Storage Contract
The agent environment setup service skill SHALL resolve setup file surfaces through Workspace Path Resolution before reading, writing, or reporting them.

#### Scenario: Agent env intent and target labels are resolved
- **WHEN** agent environment setup needs source intent, a derived agent target spec, or predecessor topic env evidence in the normal operator flow
- **THEN** it resolves `topic.intent.agent_env_requirements`, `topic.env.agent_setup_target_spec`, and `topic.env.topic_setup_target_spec` through Workspace Path Resolution
- **AND** it reports the semantic labels, resolved paths, storage profiles, sources, source details, and diagnostics in service output

#### Scenario: Explicit manual target spec records source
- **WHEN** manual invocation supplies an explicit derived gate file, target-spec prompt, or target-spec context instead of a resolved semantic label
- **THEN** the service records that explicit source and still resolves related semantic labels needed for Topic Workspace, Topic Main Repository, and Agent Workspace path evidence

### Requirement: Agent Env Setup Validation
The implementation SHALL validate the service skill through repository skillset validation and OpenSpec validation.

#### Scenario: Service skill validation runs
- **WHEN** the repository service skill validator runs
- **THEN** it validates the `isomer-srv-agent-env-setup` entrypoint, UI metadata, subcommands, reference pages, semantic label terms, predecessor topic env terms, output contract terms, and runtime-boundary guardrails

#### Scenario: Unit validation covers required terms
- **WHEN** unit validation for skillsets runs
- **THEN** it fails if the service skill omits `topic.intent.agent_env_requirements`, `topic.env.agent_setup_target_spec`, `topic.repos.main`, `agent.workspace`, `pixi run --manifest-path`, per-agent cwd verification, or the no-runtime-mutation boundary

#### Scenario: OpenSpec validation passes
- **WHEN** `openspec validate refine-topic-intent-gates --strict` runs
- **THEN** the change artifacts validate without schema or scenario-format errors
