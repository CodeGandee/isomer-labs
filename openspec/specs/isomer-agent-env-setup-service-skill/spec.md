# isomer-agent-env-setup-service-skill Specification

## Purpose
TBD - created by archiving change add-agent-env-setup-service-skill. Update Purpose after archive.
## Requirements
### Requirement: Agent Env Setup Service Skill Bundle
The repository SHALL provide a command-style service skill named `isomer-srv-agent-env-setup` for service-safe Agent Workspace environment setup and per-agent cwd env-gate verification.

#### Scenario: Skill bundle exists
- **WHEN** the service skillset is inspected
- **THEN** it contains `skillset/service/isomer-srv-agent-env-setup/SKILL.md`
- **AND** it contains `skillset/service/isomer-srv-agent-env-setup/agents/openai.yaml`

#### Scenario: Skill metadata is consistent
- **WHEN** the skill bundle is inspected
- **THEN** the folder name, `SKILL.md` frontmatter `name`, `agents/openai.yaml` display name, and default prompt use `isomer-srv-agent-env-setup`

#### Scenario: Service boundary is explicit
- **WHEN** the skill entrypoint describes its purpose
- **THEN** it states that the service prepares Git-backed Agent Workspace cwd readiness without creating Agent Instances, mutating Workspace Runtime records, launching Houmao agents, running Execution Adapters, or making research decisions

### Requirement: Command-Style Agent Env Subcommands
The service skill SHALL use a lean top-level router, grouped short kebab-case subcommands, and one executable reference page per subcommand.

#### Scenario: Entrypoint routes by subcommand
- **WHEN** an agent invokes `isomer-srv-agent-env-setup`
- **THEN** the top-level `SKILL.md` instructs the agent to select one subcommand from grouped `Subcommands` sections
- **AND** the top-level workflow loads only the selected reference page before executing that page's `## Workflow`

#### Scenario: Public subcommands exist
- **WHEN** the skill lists public subcommands
- **THEN** Procedural Subcommands include `resolve-agent-env-context`, `require-topic-env-ready`, `read-agent-env-gate`, `plan-agent-workspaces`, `derive-agent-env-gate`, `ensure-topic-main-repository`, `create-agent-worktrees`, and `verify-agent-env-gate`
- **AND** Misc Subcommands include `help` and `setup-agent-env`

#### Scenario: Full flow is directly callable
- **WHEN** the user invokes `setup-agent-env` or gives a concrete Agent Workspace env setup request without naming another subcommand
- **THEN** the skill orchestrates `resolve-agent-env-context`, `require-topic-env-ready`, `read-agent-env-gate`, `plan-agent-workspaces`, `derive-agent-env-gate`, `ensure-topic-main-repository`, `create-agent-worktrees`, and `verify-agent-env-gate` in order
- **AND** it verifies every authoritative planned Agent Name before reporting overall readiness

#### Scenario: Direct verification can target one authoritative agent
- **WHEN** the user invokes `verify-agent-env-gate` for one Agent Name present in authoritative topic-team material
- **THEN** the skill may verify only that Agent Name's worktree and derived gate commands
- **AND** it reports the result as selected-agent partial readiness evidence, not overall readiness

#### Scenario: Unknown selected agent blocks verification
- **WHEN** the user invokes a selected-agent direct subcommand for an Agent Name absent from authoritative topic-team material
- **THEN** the service reports an Agent Workspace planning blocker
- **AND** it does not infer the agent from directories, branches, or ad hoc maps

#### Scenario: Reference pages are executable
- **WHEN** a subcommand reference page is inspected
- **THEN** it contains a `## Required Inputs` section before `## Workflow`
- **AND** it contains a numbered `## Workflow`
- **AND** the workflow ends with a freeform fallback for tasks that do not map cleanly to the default steps

### Requirement: Topic Env Readiness Is a Predecessor
The service skill SHALL require Topic Workspace Pixi readiness evidence before it claims Agent Workspace environment readiness.

#### Scenario: Topic env gate is required
- **WHEN** `require-topic-env-ready` runs
- **THEN** it checks for the resolved Topic Workspace Pixi manifest path, selected Pixi environment, `pixi.lock`, `.pixi/`, and `user-intent/derived/isomer-env-gate.md`
- **AND** it reports blockers when any predecessor is missing or not ready

#### Scenario: Topic env setup is not duplicated
- **WHEN** Topic Workspace dependency installation or Pixi repair is needed
- **THEN** the service reports a next action to run `isomer-srv-topic-env-setup`
- **AND** it does not create per-agent Pixi manifests, per-agent lockfiles, per-agent `.pixi/` directories, or topic dependency mutations by default

#### Scenario: Topic env gate is consumed as predecessor evidence
- **WHEN** the service derives the agent env gate
- **THEN** it references `user-intent/derived/isomer-env-gate.md` as the topic-level predecessor gate
- **AND** it does not duplicate or reinterpret dependency installation policy as a separate per-agent dependency plan

### Requirement: Invocation and Provenance Posture
The service skill SHALL allow direct Project Operator Session invocation for static setup mutation while preserving Service Request and provenance hooks when those refs are available.

#### Scenario: Direct Project Operator Session invocation is accepted
- **WHEN** a Project Operator Session invokes `setup-agent-env` or a mutating direct subcommand
- **THEN** the service may proceed after selected Project, Research Topic, Topic Workspace, topic env predecessor evidence, authoritative Agent Name plan, and mutation scope are confirmed
- **AND** it records the requester and confirmation source in the output

#### Scenario: Service refs are recorded when available
- **WHEN** the invocation includes Service Request refs, support Artifact refs, or Provenance refs
- **THEN** the service records those refs in its output and in the derived agent env gate execution log as available

#### Scenario: Missing service refs do not block direct setup
- **WHEN** no Service Request, support Artifact, or Provenance refs are available
- **THEN** the service still may perform confirmed static setup mutation
- **AND** it records changed files, commands run, blockers, and next action as static setup evidence

#### Scenario: Static setup evidence is not runtime truth
- **WHEN** the service records direct invocation or Service Request refs
- **THEN** it still does not create Workspace Runtime records, Agent Team Instance records, Agent Instance records, Houmao launch material, or Execution Adapter material

### Requirement: Source Agent Env Gate
The service skill SHALL read a user-authored Agent Workspace source gate at `user-intent/src/agent-env-gate.md` before deriving, configuring, or verifying Agent Workspace cwd readiness.

#### Scenario: Source agent gate is required
- **WHEN** `read-agent-env-gate` runs
- **THEN** it resolves `<topic-workspace-dir>/user-intent/src/agent-env-gate.md`
- **AND** it reports a blocker when that file is missing, unreadable, or not specific enough to derive required Agent Workspace cwd commands

#### Scenario: Source agent gate is interpreted
- **WHEN** `read-agent-env-gate` reads the source gate
- **THEN** it extracts the source intent, required command set, expected results, success criteria, Topic Main Repository configuration requirements, agent plan constraints, cwd assumptions, and blockers
- **AND** it treats passing as every required command being runnable from each planned `agent.workspace` cwd through the resolved Topic Workspace Pixi environment

#### Scenario: Source agent gate stays inside static setup scope
- **WHEN** the source gate asks for Agent Instance creation, Workspace Runtime mutation, Houmao launch, Execution Adapter launch, live research execution, privileged host mutation, or research decisions
- **THEN** the service reports an out-of-scope blocker instead of deriving executable setup steps for that request

### Requirement: Semantic Agent Env Context Resolution
The service skill SHALL resolve every setup path through semantic workspace labels before mutating Git state or claiming readiness.

#### Scenario: Topic labels are resolved first
- **WHEN** `resolve-agent-env-context` runs
- **THEN** it resolves Project, Research Topic, and Topic Workspace through Project Manifest-backed context
- **AND** it resolves `topic.repos.main`, `topic.repos.main.isomer_managed`, `topic.agents_root`, `topic.records`, and `topic.runtime` with path sources and diagnostics

#### Scenario: Agent labels are resolved for each planned agent
- **WHEN** the service has an Agent Name plan
- **THEN** it resolves `agent.workspace`, `agent.isomer_managed`, `agent.runtime`, `agent.private_artifacts`, `agent.scratch`, `agent.logs`, `agent.public_share`, `agent.inbox`, `agent.topic_readonly`, `agent.topic_writable`, and `agent.links` for each Agent Name
- **AND** it reports each semantic label, resolved path, source, and blocker

#### Scenario: Default paths are identified as defaults
- **WHEN** a resolved path comes from `isomer-default.v1`
- **THEN** the service output identifies the default profile source instead of presenting the concrete path as the workspace contract

#### Scenario: Custom safe bindings are accepted
- **WHEN** a Topic Workspace Manifest binds `topic.repos.main` or `agent.workspace` to a safe project-local path that differs from the default layout
- **THEN** the service uses that binding for setup and validation
- **AND** the path difference is not itself a blocker

### Requirement: Agent Workspace Plan Inputs
The service skill SHALL plan Agent Workspaces from authoritative topic-team material, not from directory scans or ad hoc Agent Names.

#### Scenario: Role binding source is accepted
- **WHEN** `plan-agent-workspaces` reads a Topic Team Instantiation Packet or Topic Agent Team Profile material with active role bindings
- **THEN** it extracts active role ids, Agent Names, optional branch plans, and compatibility `agent_workspace_ref` evidence for planning

#### Scenario: Missing authoritative agent names block planning
- **WHEN** no Topic Team Instantiation Packet or Topic Agent Team Profile material provides authoritative Agent Names for the planned roles
- **THEN** the service reports an Agent Workspace planning blocker
- **AND** it routes the operator back to Topic Team Specialization to repair or complete the packet or profile material

#### Scenario: Explicit agent map cannot override topic-team material
- **WHEN** the user provides an explicit role-to-Agent-Name map or Agent Name list that disagrees with the Topic Team Instantiation Packet or Topic Agent Team Profile material
- **THEN** the service reports an `agent-plan-conflict` blocker
- **AND** it does not create branches, worktrees, support paths, or gate entries from the conflicting map

#### Scenario: Matching explicit agent map is corroborating evidence
- **WHEN** the user provides an explicit role-to-Agent-Name map or Agent Name list that matches the authoritative topic-team material
- **THEN** the service may record that map as corroborating operator-provided evidence
- **AND** it still treats the Topic Team Instantiation Packet or Topic Agent Team Profile material as the Agent Name authority

#### Scenario: Directory scan does not select agents
- **WHEN** directories already exist under the resolved agents root
- **THEN** the service does not treat those directories as the agent plan unless they are also present in the authoritative Topic Team Instantiation Packet or Topic Agent Team Profile material

#### Scenario: Unsafe Agent Names block planning
- **WHEN** a planned Agent Name is empty, `.` or `..`, contains path separators, contains unsafe shell metacharacters, or collides after normalization
- **THEN** the service reports a blocker before creating branches, worktrees, support paths, or gate entries

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
- **WHEN** `ensure-topic-main-repository` runs after `derive-agent-env-gate`
- **THEN** it applies non-destructive Topic Main Repository configuration required by `user-intent/derived/isomer-agent-env-gate.md`
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
- **THEN** the service reports a blocker and does not create a second worktree for that branch

### Requirement: Agent Support Paths and Boundaries
The service skill SHALL prepare or validate required agent support surfaces and advisory boundary material for each prepared Agent Workspace.

#### Scenario: Support paths are prepared
- **WHEN** an Agent Workspace worktree is ready or newly created
- **THEN** the service creates or validates required support paths for `agent.isomer_managed`, `agent.runtime`, `agent.private_artifacts`, `agent.scratch`, `agent.logs`, `agent.public_share`, `agent.inbox`, `agent.topic_readonly`, `agent.topic_writable`, and `agent.links`

#### Scenario: Tmp surfaces remain disposable
- **WHEN** `topic.repos.main.tmp` or `agent.tmp` labels are available
- **THEN** the service treats them as local ignored disposable surfaces
- **AND** it does not include tmp paths in durable readiness evidence except as ignored local path posture

#### Scenario: Boundary material names cwd query guidance
- **WHEN** the service writes or validates Agent Workspace boundary notes
- **THEN** the material states that an agent running inside its own Agent Workspace can query agent-scoped labels without passing Agent Name
- **AND** it states that cwd inference is a path-resolution convenience, not filesystem-grade identity or access control

#### Scenario: Peer read surfaces are explicit
- **WHEN** boundary material describes peer inspection
- **THEN** it names `agent.public_share`, approved topic-owned projections, generated links, or Git-tracked material as supported sharing routes
- **AND** it does not describe tmp or private runtime material as a sharing surface

### Requirement: Agent Env Gate File
The service skill SHALL generate and maintain a topic-owned derived per-agent readiness gate at `user-intent/derived/isomer-agent-env-gate.md` from the source gate `user-intent/src/agent-env-gate.md`.

#### Scenario: Source and derived agent gate paths are paired
- **WHEN** `derive-agent-env-gate` resolves gate paths
- **THEN** it reads the source gate at `<topic-workspace-dir>/user-intent/src/agent-env-gate.md`
- **AND** it writes the derived gate at `<topic-workspace-dir>/user-intent/derived/isomer-agent-env-gate.md`

#### Scenario: Gate file has fixed sections
- **WHEN** `derive-agent-env-gate` writes the gate
- **THEN** the file includes sections named `Source Agent Gate`, `Topic Env Gate`, `Topic Pixi Binding`, `Topic Main Repository Configuration`, `Agent Plan`, `Semantic Paths`, `Worktree Plan`, `Verification Matrix`, `Expected Results`, `Blockers`, and `Execution Log`
- **AND** every section is present even when the section content is `None.` or a short reason that it does not apply

#### Scenario: Gate records per-agent cwd commands
- **WHEN** verification commands are derived
- **THEN** each command records the source `agent-env-gate.md` requirement, Agent Name, cwd as the resolved `agent.workspace`, the `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...` command, and expected result

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
- **THEN** every required command from `user-intent/derived/isomer-agent-env-gate.md` for `alice` has passed with the resolved `agent.workspace` as process cwd
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

### Requirement: Agent Env Setup Output Contract
The service skill SHALL report structured output that downstream operator skills can treat as static setup evidence.

#### Scenario: Output includes setup fields
- **WHEN** any subcommand completes, blocks, or fails
- **THEN** the output includes the selected subcommand, Project root, Research Topic id, Topic Workspace path, Topic Workspace Pixi binding, requester, confirmation source, optional Service Request or Provenance refs, semantic paths, changed files, commands run, readiness status, blockers, and next action as relevant

#### Scenario: Full flow output includes agent matrix
- **WHEN** `setup-agent-env` completes, blocks, or fails
- **THEN** the output includes `topic_environment_status`, `source_agent_env_gate_path`, `agent_env_gate_path`, `topic_main_repository`, `agent_workspace_paths`, `branch_plan`, `worktree_status_by_agent`, `readiness_by_agent`, and `overall_readiness_status`

#### Scenario: Selected-agent output identifies partial scope
- **WHEN** a direct subcommand runs for one selected Agent Name
- **THEN** the output includes the selected Agent Name, the authoritative source for that name, updated readiness evidence for that agent, blockers, and a statement that the result is partial evidence unless the full matrix has passed

#### Scenario: Runtime readiness is not implied
- **WHEN** agent env setup reports `ready`
- **THEN** the output still states that Agent Instances, Workspace Runtime Agent Workspace records, Houmao launch material, and Execution Adapter readiness remain separate downstream workflows

### Requirement: Agent Env Setup Validation
The implementation SHALL validate the service skill through repository skillset validation and OpenSpec validation.

#### Scenario: Service skill validation runs
- **WHEN** the repository service skill validator runs
- **THEN** it validates the `isomer-srv-agent-env-setup` entrypoint, UI metadata, subcommands, reference pages, semantic label terms, predecessor topic env terms, output contract terms, and runtime-boundary guardrails

#### Scenario: Unit validation covers required terms
- **WHEN** unit validation for skillsets runs
- **THEN** it fails if the service skill omits `user-intent/src/agent-env-gate.md`, `isomer-agent-env-gate.md`, `topic.repos.main`, `agent.workspace`, `pixi run --manifest-path`, per-agent cwd verification, or the no-runtime-mutation boundary

#### Scenario: OpenSpec validation passes
- **WHEN** `openspec validate add-agent-env-setup-service-skill --strict` runs
- **THEN** the change artifacts validate without schema or scenario-format errors

### Requirement: Agent Env Setup Consumes Storage Contract
The Agent Workspace environment setup service SHALL resolve every target path through Workspace Path Resolution before mutating Git state, writing support files, or claiming readiness.

#### Scenario: Agent workspace setup uses resolved labels
- **WHEN** the service prepares an Agent Workspace for a planned Agent Name
- **THEN** it resolves `agent.workspace`, `agent.isomer_managed`, `agent.runtime`, `agent.private_artifacts`, `agent.scratch`, `agent.logs`, `agent.public_share`, `agent.inbox`, `agent.topic_readonly`, `agent.topic_writable`, `agent.links`, and `agent.tmp` through Workspace Path Resolution

#### Scenario: Default worktree path is not assembled directly
- **WHEN** the service creates or validates a Git worktree
- **THEN** it uses the resolved `agent.workspace` path and resolved `topic.repos.main` path rather than assembling `agents/<agent-name>` and `repos/topic-main`

#### Scenario: Custom agent support label is accepted
- **WHEN** the Topic Workspace Manifest declares a valid agent-required `custom.*` support label needed by agent setup
- **THEN** the service resolves that label for each relevant Agent Name and reports path, source, `storage_profile` id, storage-profile-derived traits, and blockers

#### Scenario: Missing custom agent label blocks dependent setup
- **WHEN** agent setup material names a custom semantic label that is not valid in the effective catalog
- **THEN** the service reports a Workspace Path Resolution blocker and avoids mutating a guessed fallback directory

### Requirement: Agent Env Setup Preserves Path Source Evidence
The Agent Workspace environment setup service SHALL include path source evidence in readiness output for every semantic surface it uses.

#### Scenario: Readiness output names path sources
- **WHEN** setup readiness succeeds or partially succeeds
- **THEN** the output includes each semantic label used, resolved path, source, source detail, scope ref, `storage_profile` id, and storage-profile-derived traits

#### Scenario: Default layout profile source remains explicit
- **WHEN** an agent setup path comes from `isomer-default.v1`
- **THEN** the readiness output identifies the default layout profile source instead of presenting the concrete path as an authored contract

