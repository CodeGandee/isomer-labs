# topic-workspace-manager-skill Specification

## Purpose
Define the operator skill that prepares Git-backed Topic Workspace repositories and per-agent Agent Workspace worktrees.
## Requirements
### Requirement: Topic Workspace Manager Skill Bundle
The repository SHALL provide a command-style operator skill named `isomer-admin-topic-workspace-mgr` for Git-backed Topic Workspace repository and Agent Workspace worktree preparation.

#### Scenario: Skill bundle exists
- **WHEN** the operator skillset is inspected
- **THEN** it contains `skillset/operator/isomer-admin-topic-workspace-mgr/SKILL.md` and `skillset/operator/isomer-admin-topic-workspace-mgr/agents/openai.yaml`

#### Scenario: Skill metadata is consistent
- **WHEN** the topic workspace manager skill bundle is inspected
- **THEN** the folder name, `SKILL.md` frontmatter `name`, `agents/openai.yaml` display name, and default prompt use `isomer-admin-topic-workspace-mgr`

#### Scenario: Skill remains operator scoped
- **WHEN** the skill entrypoint describes its purpose
- **THEN** it states that the skill prepares Topic Workspace Git layout and Agent Workspace worktrees without creating Agent Instances, mutating Workspace Runtime records, launching Houmao agents, or running Execution Adapters

### Requirement: Command-Style Subcommand Structure
The topic workspace manager skill SHALL use a lean top-level router, grouped short kebab-case subcommands, and one-level executable reference pages.

#### Scenario: Entrypoint routes by subcommand
- **WHEN** an agent invokes `isomer-admin-topic-workspace-mgr`
- **THEN** the top-level `SKILL.md` selects one subcommand from grouped subcommand tables and loads only the selected reference page before executing that page's `## Workflow`

#### Scenario: Default subcommand runs full flow
- **WHEN** the user invokes the skill without a subcommand and does not ask for help
- **THEN** the skill selects `topic-workspace` as the default full preparation flow

#### Scenario: Public subcommands exist
- **WHEN** the skill lists public subcommands
- **THEN** it includes procedural subcommands `resolve-workspace`, `ensure-main-repo`, `plan-agents`, `create-worktrees`, `write-boundaries`, `create-agent-branch`, `validate-worktrees`, and `summarize`
- **AND** it includes misc subcommands `help` and `topic-workspace`

#### Scenario: Subcommand pages have workflows
- **WHEN** an executable reference page is inspected
- **THEN** it has a near-top `## Workflow` section with numbered steps and a freeform fallback for tasks that do not map cleanly to the default steps

### Requirement: Topic Workspace Git Layout
The topic workspace manager skill SHALL use `<topic-workspace-dir>/repos/topic-main` as the shared topic repository and `<topic-workspace-dir>/agents/<agent-name>` as each prepared Agent Workspace worktree.

#### Scenario: Workspace resolution uses Project Manifest
- **WHEN** `resolve-workspace` runs
- **THEN** it resolves Project root, Research Topic, and Topic Workspace through Project Manifest-backed Isomer context instead of inferring a Topic Workspace by scanning directories

#### Scenario: Shared topic repo is placed under repos
- **WHEN** `ensure-main-repo` creates or validates the shared topic repository
- **THEN** the expected repository path is `<topic-workspace-dir>/repos/topic-main`

#### Scenario: Isomer-managed namespace is placed inside topic-main
- **WHEN** `ensure-main-repo` creates or validates the shared topic repository
- **THEN** the expected Isomer worker-facing namespace is `<topic-workspace-dir>/repos/topic-main/isomer-managed`

#### Scenario: Agent worktrees are placed under agents
- **WHEN** `create-worktrees` creates an Agent Workspace for agent name `alice`
- **THEN** the expected worktree path is `<topic-workspace-dir>/agents/alice`

#### Scenario: Existing unsafe repo blocks preparation
- **WHEN** `<topic-workspace-dir>/repos/topic-main` exists but is not a usable Git repository for worktree creation
- **THEN** the skill reports a blocker and does not delete, replace, pull, or reinitialize the existing path without explicit user instruction

#### Scenario: Shared topic repo path is semantic
- **WHEN** the skill inspects or validates the shared topic repository
- **THEN** it uses the resolved `topic.repos.main` path and reports the path source
- **AND** the default path remains `<topic-workspace-dir>/repos/topic-main` under `isomer-default.v1`

#### Scenario: Isomer-managed namespace is inside topic-main
- **WHEN** the skill inspects or validates the shared topic repository
- **THEN** the expected Isomer worker-facing namespace is the resolved `topic.repos.main.isomer_managed` path

#### Scenario: Agent worktrees are placed under resolved agent labels
- **WHEN** the skill inspects, validates, or optionally creates an Agent Workspace for agent name `alice`
- **THEN** the expected worktree path is the resolved `agent.workspace` path for `alice`

#### Scenario: Canonical main repo creation is not required from this skill
- **WHEN** topic env setup has already prepared Topic Main Development Repository predecessor evidence
- **THEN** the workspace manager uses that evidence for validation or summaries
- **AND** it does not present itself as the canonical creator of `topic.repos.main`

#### Scenario: Existing unsafe repo blocks optional topology work
- **WHEN** the resolved `topic.repos.main` exists but is not a usable Git repository for worktree inspection or creation
- **THEN** the skill reports a blocker
- **AND** it does not delete, replace, pull, or reinitialize the existing path without explicit user instruction

### Requirement: Agent Planning and Branch Names
The topic workspace manager skill SHALL normalize per-agent names, map them to role bindings, and use deterministic per-agent branch namespaces.

#### Scenario: Agent names are path safe
- **WHEN** `plan-agents` resolves requested agent names
- **THEN** it rejects empty names, unsafe path segments, reserved names, and normalized name collisions before creating worktrees or updating workspace refs

#### Scenario: Default per-agent branch is deterministic
- **WHEN** `plan-agents` plans an Agent Workspace for agent name `alice`
- **THEN** the default branch is `per-agent/alice/main`

#### Scenario: Future per-agent branches stay under prefix
- **WHEN** `create-agent-branch` creates branch `experiment-1` for agent name `alice`
- **THEN** the branch name is `per-agent/alice/experiment-1`

#### Scenario: Cross-agent branch prefix is rejected
- **WHEN** an agent branch request for agent name `alice` names a branch outside `per-agent/alice/`
- **THEN** the skill rejects the branch request before mutating Git state

### Requirement: Worktree Creation Safety
The topic workspace manager skill SHALL create Git worktrees idempotently and refuse ambiguous or unsafe workspace topology.

#### Scenario: Worktree creation uses topic-main
- **WHEN** `create-worktrees` prepares an Agent Workspace for agent name `alice`
- **THEN** it creates a Git worktree of `<topic-workspace-dir>/repos/topic-main` at `<topic-workspace-dir>/agents/alice` on `per-agent/alice/main`

#### Scenario: Existing matching worktree is ready
- **WHEN** `<topic-workspace-dir>/agents/alice` already exists as a worktree of `topic-main` on `per-agent/alice/main`
- **THEN** the skill reports the worktree as ready instead of creating another worktree

#### Scenario: Existing nonmatching path blocks creation
- **WHEN** `<topic-workspace-dir>/agents/alice` exists but is not the expected worktree
- **THEN** the skill reports a blocker and does not overwrite the path

#### Scenario: Duplicate branch checkout is rejected
- **WHEN** `per-agent/alice/main` is already checked out in another worktree of `topic-main`
- **THEN** the skill reports a blocker and does not create a second worktree for the same branch

#### Scenario: Agent Isomer-managed support directory is prepared
- **WHEN** a worktree is created or validated for agent name `alice`
- **THEN** the skill ensures the ignored support area `<topic-workspace-dir>/agents/alice/isomer-managed/` exists with the expected tracked, agent-owned, topic-owned, and link subpaths or reports why it could not be prepared

### Requirement: Profile and Packet Workspace Ref Updates
The topic workspace manager skill SHALL write or validate planned Agent Workspace refs in Topic Team Instantiation Packet or Topic Agent Team Profile material when requested by the operator workflow.

#### Scenario: Role binding receives workspace ref
- **WHEN** `plan-agents` maps an active role binding to agent name `alice`
- **THEN** the planned role binding `agent_workspace_ref` is `<topic-workspace-dir>/agents/alice` or an equivalent project-relative ref under the selected Topic Workspace

#### Scenario: Role binding receives agent name and branch plan
- **WHEN** `plan-agents` maps an active role binding to agent name `alice`
- **THEN** the skill reports or writes the topic-local agent name, branch `per-agent/alice/main`, and `isomer-managed/` support path as static setup evidence when the target material has fields for them

#### Scenario: Workspace refs are reported
- **WHEN** the skill completes planning or creation
- **THEN** its output reports role ids, agent names, Agent Workspace paths, branch names, `isomer-managed/` paths, and any profile or packet files changed

#### Scenario: Cross-topic workspace ref is rejected
- **WHEN** a planned role binding points outside the selected Topic Workspace or into another Research Topic's Topic Workspace
- **THEN** the skill reports a blocker and does not treat the workspace plan as ready

### Requirement: Workspace Boundary and Summary Material
The topic workspace manager skill SHALL record advisory Workspace Boundary and summary material for prepared Git-backed Agent Workspaces.

#### Scenario: Boundary docs are written
- **WHEN** `write-boundaries` runs after worktree planning
- **THEN** it writes or updates topic-level and per-agent boundary material that names write ownership, Peer Read Access, branch rules, `isomer-managed/` tracked and untracked directories, generated links, and safe integration expectations

#### Scenario: Boundaries are advisory
- **WHEN** the boundary material describes Agent Workspace access
- **THEN** it states that Workspace Boundaries, Peer Read Access, owner/reader split, and generated links are advisory and are not filesystem-grade security isolation

#### Scenario: Summary is consumer neutral
- **WHEN** `summarize` runs
- **THEN** it reports the shared topic repository, every agent name, worktree path, current branch, expected branch namespace, `isomer-managed/` path status, boundary material path, validation status, blockers, and next operator action

### Requirement: Topic Workspace Manager Validation
The topic workspace manager skill SHALL validate prepared Git-backed workspace topology without repairing it silently.

#### Scenario: Validation checks Git topology
- **WHEN** `validate-worktrees` runs
- **THEN** it checks `topic-main`, expected worktree paths, expected current branches, duplicate branch checkouts, and branch namespace compliance

#### Scenario: Validation checks Isomer refs
- **WHEN** `validate-worktrees` has access to packet or profile material
- **THEN** it checks that active role binding `agent_workspace_ref`, agent name, branch name, and `isomer-managed/` support refs match prepared worktree paths for the selected Topic Workspace

#### Scenario: Validation checks Isomer-managed layout
- **WHEN** `validate-worktrees` runs against a prepared Topic Workspace
- **THEN** it reports missing `isomer-managed/.gitignore`, missing tracked subdirectories, missing agent-owned support directories, missing topic-owned projection directories, unsafe generated links, legacy `.isomer-agent/` paths, and legacy top-level worker collaboration directories without deleting or moving files

#### Scenario: Validation does not launch
- **WHEN** validation succeeds
- **THEN** the skill reports readiness of the Git-backed workspace layout without creating Agent Instances, registering Workspace Runtime records, launching agents, or invoking Execution Adapters

### Requirement: Topic Workspace Manager Skill Validation
The implementation SHALL validate the new operator skill through repository skillset validation and OpenSpec validation.

#### Scenario: Operator skill validation includes topic workspace manager
- **WHEN** `pixi run validate-operator-skills` runs
- **THEN** it validates `isomer-admin-topic-workspace-mgr` frontmatter, UI metadata, subcommand pages, command-style workflow, local reference integrity, required output terms, and guardrail terms

#### Scenario: OpenSpec validation passes
- **WHEN** `openspec validate add-topic-workspace-manager-skill --strict` runs
- **THEN** the change artifacts validate without schema or scenario-format errors

### Requirement: Semantic Workspace Manager Inputs
The topic workspace manager skill SHALL plan and report Topic Workspace Git layout through semantic labels and Topic Workspace Manifest bindings.

#### Scenario: Resolve workspace reports semantic labels
- **WHEN** `resolve-workspace` resolves the selected Topic Workspace
- **THEN** it reports semantic labels for Topic Main Repository, Agent Workspace root, Isomer-managed support namespace, records root, and runtime support root along with their resolved paths and sources

#### Scenario: Existing custom binding is honored
- **WHEN** the Topic Workspace Manifest binds `topic.repos.main` or `agent.workspace` to safe project-local paths that differ from the default layout
- **THEN** the skill uses those bindings for planning and validation instead of assuming the default paths

#### Scenario: Missing manifest uses default profile for planning
- **WHEN** the Topic Workspace Manifest is missing and the operator has not requested a custom layout
- **THEN** the skill plans against the built-in `isomer-default.v1` labels and reports that the paths come from the default profile

### Requirement: Default Layout Materialization
The topic workspace manager skill SHALL materialize default semantic workspace directories only when the operator asks for default creation.

#### Scenario: Default main repo is explicitly created
- **WHEN** the operator asks the skill to create default Topic Main Repository material
- **THEN** the skill creates or validates the `topic.repos.main` default binding and directory through the Topic Workspace Manifest contract

#### Scenario: Default agent worktrees are explicitly created
- **WHEN** the operator asks the skill to create Agent Workspace worktrees at default locations
- **THEN** the skill creates or validates `agent.workspace` default bindings for the planned Agent Names before creating the worktrees

#### Scenario: Read-only planning does not create manifest
- **WHEN** the skill runs `resolve-workspace`, `plan-agents`, `validate-worktrees`, or `summarize` without creation intent
- **THEN** it does not create or rewrite `topic-workspace.toml`, directories, branches, or worktrees

#### Scenario: Default main repo materialization is not canonical
- **WHEN** the operator asks this skill to create default Topic Main Development Repository material
- **THEN** the skill reports that the canonical setup path is `isomer-srv-topic-env-setup`
- **AND** it may perform only an explicitly requested manual repair or compatibility operation with mutation confirmation

### Requirement: Semantic Agent Planning
The topic workspace manager skill SHALL plan Agent Names, branches, worktrees, and compatibility refs from semantic `agent.workspace` resolution.

#### Scenario: Planned agent path comes from semantic label
- **WHEN** `plan-agents` plans Agent Name `alice`
- **THEN** the planned Agent Workspace path is the resolved `agent.workspace` path for `alice`

#### Scenario: Compatibility workspace ref is derived from semantic path
- **WHEN** older packet or profile material still needs `agent_workspace_ref`
- **THEN** the skill derives the compatibility ref from the resolved `agent.workspace` path rather than assembling a default path directly

#### Scenario: Branch namespace remains agent scoped
- **WHEN** a semantic Agent Workspace path differs from the default layout
- **THEN** the planned branch still stays under `per-agent/<agent-name>/` unless a later accepted contract changes branch namespace semantics

#### Scenario: Cwd-friendly query guidance is included
- **WHEN** the skill writes Workspace Boundary or summary material for an Agent Workspace
- **THEN** it tells agents to use semantic path queries for their own agent-scoped surfaces from inside their Agent Workspace without requiring an Agent Name selector

### Requirement: Semantic Workspace Validation
The topic workspace manager skill SHALL validate Git-backed workspace topology against manifest-backed semantic labels.

#### Scenario: Validation checks manifest binding
- **WHEN** `validate-worktrees` checks a prepared Topic Main Repository or Agent Workspace
- **THEN** it verifies that the actual Git repository or worktree matches the resolved semantic binding for the selected Topic Workspace and Agent Name

#### Scenario: Custom path collision is a blocker
- **WHEN** a manifest binding points to an existing path that is not the expected repository or worktree for the requested semantic label
- **THEN** the skill reports a blocker and does not overwrite, reinitialize, delete, reset, or move the path

#### Scenario: Validation reports labels and paths
- **WHEN** validation completes
- **THEN** the output reports each checked semantic label, resolved path, source, readiness, blockers, and next operator action

### Requirement: Summary Uses Semantic Labels
The topic workspace manager skill SHALL summarize the workspace contract by semantic label first and default path second.

#### Scenario: Summary names tmp labels as local-only
- **WHEN** `summarize` reports tmp posture
- **THEN** it names semantic labels such as `topic.repos.main.tmp` and `agent.tmp`
- **AND** it identifies their default paths only as `isomer-default.v1` bindings

### Requirement: Isomer-Managed Sharing Preparation
The topic workspace manager skill SHALL prepare and validate the standard `isomer-managed/` sharing layout for the topic owner checkout and each Agent Workspace worktree while keeping tmp surfaces outside sharing.

#### Scenario: Tmp is separate from isomer-managed sharing
- **WHEN** `ensure-main-repo` or `create-worktrees` prepares `isomer-managed/` layout
- **THEN** it keeps `topic.repos.main.tmp` and `agent.tmp` outside tracked Isomer material, agent-owned public shares, topic-owned projections, and generated links

### Requirement: Isomer-Managed Conflict Diagnostics
The topic workspace manager skill SHALL report risky tracked Isomer material and untracked share ownership problems without trying to resolve them automatically.

#### Scenario: Tracked conflict markers are reported
- **WHEN** validation finds unresolved Git conflict markers under `isomer-managed/tracked/`
- **THEN** it reports the affected paths and does not mark the workspace layout ready

#### Scenario: Agent-owned reader writes are reported
- **WHEN** validation can determine that a peer wrote into another agent's `isomer-managed/agent-owned/public/` without an allowed policy
- **THEN** it reports an owner/reader split diagnostic and names the owning agent, reader agent, and affected path when known

#### Scenario: Topic-owned writable policy is required
- **WHEN** `isomer-managed/topic-owned/writable/` exists or is linked but boundary material does not state a write policy
- **THEN** validation reports a missing topic-owned writable policy diagnostic

### Requirement: Topic Workspace Manager Delegates Agent Env Readiness
The topic workspace manager skill SHALL route service-safe per-agent environment verification to `isomer-srv-agent-env-setup` when Agent Workspace cwd readiness is requested.

#### Scenario: Env readiness request routes to service
- **WHEN** the operator asks `isomer-admin-topic-workspace-mgr` to prove that prepared Agent Workspaces pass the environment gate
- **THEN** the skill routes to `isomer-srv-agent-env-setup setup-agent-env` or a specific service subcommand
- **AND** it preserves the selected Research Topic, Topic Workspace, role binding source, and semantic path expectations in the service request

#### Scenario: Static Git-only flow remains available
- **WHEN** the operator asks only for Git-backed workspace topology preparation
- **THEN** the skill may continue to run `resolve-workspace`, `ensure-main-repo`, `plan-agents`, `create-worktrees`, `write-boundaries`, `validate-worktrees`, and `summarize` without requiring per-agent env-gate execution

#### Scenario: Service output is consumed as evidence
- **WHEN** the agent env setup service returns output
- **THEN** the topic workspace manager summary includes the returned `source_agent_env_gate_path`, `agent_env_gate_path`, readiness by agent, worktree status by agent, semantic paths, commands run, blockers, and next operator action

### Requirement: Topic Workspace Manager Preserves Service Boundaries
The topic workspace manager skill SHALL distinguish static workspace topology readiness from agent env readiness and runtime readiness.

#### Scenario: Git readiness does not imply env readiness
- **WHEN** `validate-worktrees` reports Git topology as ready
- **THEN** the skill does not claim that the Topic Workspace Pixi env passes from every Agent Workspace cwd unless `isomer-srv-agent-env-setup` evidence says so

#### Scenario: Agent env readiness does not imply runtime readiness
- **WHEN** service evidence reports Agent Workspace env readiness as ready
- **THEN** the topic workspace manager still does not claim Agent Instance creation, Workspace Runtime records, Houmao launch, or Execution Adapter readiness

#### Scenario: Service blockers remain visible
- **WHEN** the service reports an unsafe path, missing topic env readiness, failing cwd gate command, or nonmatching worktree
- **THEN** the topic workspace manager reports that blocker without silently repairing it

### Requirement: Topic Workspace Manager Prepares Local Tmp Surfaces
The topic workspace manager skill SHALL prepare and validate local tmp labels for the resolved Topic Main Repository owner checkout and each Agent Workspace worktree.

#### Scenario: Ensure main repo prepares tmp ignore
- **WHEN** `ensure-main-repo` creates or validates resolved `topic.repos.main`
- **THEN** it prepares or validates resolved `topic.repos.main.tmp`
- **AND** it prepares or validates a root `.gitignore` rule that ignores tmp material

#### Scenario: Create worktrees prepares agent tmp
- **WHEN** `create-worktrees` prepares resolved `agent.workspace` for Agent Name `alice`
- **THEN** it prepares or validates resolved `agent.tmp` as an ignored local disposable directory
- **AND** it does not add tracked placeholder files under `agent.tmp`

#### Scenario: Validate worktrees checks tmp contract
- **WHEN** `validate-worktrees` checks prepared Git-backed workspace topology
- **THEN** it reports missing or ineffective tmp-label ignore policy, tracked tmp contents, or guidance that treats tmp material as shared or durable material

#### Scenario: Summaries do not present tmp as shared
- **WHEN** the topic workspace manager summarizes prepared Agent Workspaces
- **THEN** it may list `topic.repos.main.tmp` and `agent.tmp` as local disposable surfaces
- **AND** it does not include them in Peer Read Access, generated links, handoff paths, readiness evidence, or durable boundary material

### Requirement: Manager Skill Uses Storage Contract
The topic workspace manager skill SHALL use Workspace Path Resolution as its storage contract before planning, creating, or validating repositories and worktrees.

#### Scenario: Main repository mutation uses resolved label
- **WHEN** the skill creates, validates, or summarizes the Topic Main Repository
- **THEN** it uses the resolved `topic.repos.main` result and reports semantic label, path, source, and diagnostics instead of assembling `repos/topic-main`

#### Scenario: Worktree mutation uses resolved agent label
- **WHEN** the skill creates or validates an Agent Workspace for an Agent Name
- **THEN** it uses the resolved `agent.workspace` result for that Agent Name and reports semantic label, path, source, and diagnostics before mutating Git worktrees

#### Scenario: Parent-derived support paths are honored
- **WHEN** `topic.repos.main` or `agent.workspace` has a custom safe binding
- **THEN** the skill resolves support labels such as `topic.repos.main.isomer_managed`, `topic.repos.main.tmp`, `agent.private_artifacts`, and `agent.tmp` through Workspace Path Resolution rather than appending default suffixes by hand

### Requirement: Manager Skill Reports Custom Surface Evidence
The topic workspace manager skill SHALL preserve semantic evidence for custom storage surfaces it uses or reports.

#### Scenario: Custom label appears in output
- **WHEN** operator-provided topic material names a valid custom semantic label that affects repository or worktree setup
- **THEN** the skill includes that label's resolved path, source, `storage_profile` id, storage-profile-derived traits, and blockers in its semantic path evidence

#### Scenario: Unknown custom label blocks dependent step
- **WHEN** operator-provided topic material names a label that is not built in and not declared as a valid custom manifest binding
- **THEN** the skill reports a Workspace Path Resolution blocker instead of falling back to a guessed directory

### Requirement: Topic Workspace Manager Uses Essential and Complete Output
The Topic Workspace Manager operator skill SHALL split its output contract into Essential Output and Complete Output.

#### Scenario: Essential topic workspace output reports topology status
- **WHEN** `isomer-admin-topic-workspace-mgr` reports a result without a complete-output request
- **THEN** it reports the selected Research Topic, Topic Workspace, topic-main status, Agent Workspace path summary, local tmp posture summary, blockers, and next action
- **AND** it highlights unsafe topology problems that need operator attention

#### Scenario: Complete topic workspace output preserves semantic path detail
- **WHEN** complete output is requested from `isomer-admin-topic-workspace-mgr`
- **THEN** it reports semantic paths, path sources, readiness diagnostics, topic-main path evidence, `isomer-managed/` status, tmp posture, Agent Workspace paths, branch plan, boundary material paths, generated links, validation status, blockers, and next action

### Requirement: Optional Topology Support Boundary
The topic workspace manager skill SHALL be optional support for topology inspection, branch helpers, boundary summaries, and legacy compatibility diagnostics after the breaking Topic Main Development Repository revision.

#### Scenario: Topology inspection remains supported
- **WHEN** an operator asks to inspect prepared topic-main and Agent Workspace topology
- **THEN** the skill reports semantic paths, Git state, branch namespace, worktree state, Isomer-managed layout, projection roots, generated links, blockers, and next actions without materializing missing topic env surfaces

#### Scenario: Branch helper remains supported
- **WHEN** an operator asks to create a future per-agent branch under an accepted agent branch namespace
- **THEN** the skill may perform that bounded Git helper operation after validating the prepared Topic Main Development Repository and Agent Name

#### Scenario: Legacy generated content can break
- **WHEN** the skill sees old generated `isomer-content/` internals or old topic-main support paths
- **THEN** it may report them as unsupported under the revised layout
- **AND** it does not need to provide migration instructions beyond recreating generated topic content

### Requirement: Workspace Manager Owns Topic Actor Management
The Topic Workspace Manager skill SHALL manage Topic Actor CRUD and Topic Actor Workspace materialization as Topic Workspace topology operations.

#### Scenario: Actor CRUD uses workspace manager
- **WHEN** a user or operator asks to list, show, register, update, archive, materialize, repair, or diagnose Topic Actors
- **THEN** the Topic Workspace Manager performs or guides the operation through the `project topic-actors ...` CLI surface
- **AND** it updates Topic Workspace Manifest actor bindings as the actor topology authority

#### Scenario: Topic Actor binding records worker identity
- **WHEN** the Topic Workspace Manager registers a manually controlled worker for a Research Topic
- **THEN** the binding records a path-safe `topic_actor_name`, actor kind, runtime kind, role kind, controller ref or controller kind, default cwd label, optional workspace label, optional workspace path, optional branch, optional adapter ref, status, and provenance metadata

#### Scenario: Topic Actor field values are bounded but extensible
- **WHEN** the Topic Workspace Manager validates actor kind, runtime kind, role kind, controller kind, or status
- **THEN** it accepts the core values defined by the Topic Actor binding contract and accepts extension values under `custom.*`
- **AND** it rejects unknown non-extension values with a deterministic diagnostic

#### Scenario: Topic Actor registration is audited when runtime is available
- **WHEN** Topic Actor registration or materialization mutates the Topic Workspace and Workspace Runtime is initialized
- **THEN** the Topic Workspace Manager records a Workspace Runtime mutation or provenance audit record for the operation
- **AND** the Topic Workspace Manifest remains the topology and path-resolution authority for the actor binding

#### Scenario: Mixed runtimes are accepted
- **WHEN** the Topic Workspace Manager registers Topic Actors backed by Claude Code, Codex, Houmao, shell sessions, or another supported runtime kind
- **THEN** the workflow allows them to coexist in the same Topic Workspace when each actor has a distinct topic-local name and workspace binding

### Requirement: Workspace Manager Materializes Topic Actor Workspaces
The Topic Workspace Manager skill SHALL prepare separate Topic Actor Workspaces for Topic Actors that need independent development surfaces.

#### Scenario: Actor workspace worktree is created from topic-main
- **WHEN** the operator asks to create or repair a Topic Actor Workspace
- **THEN** the Topic Workspace Manager uses the resolved `topic.repos.main` repository as the Git anchor, resolves `topic.actors.workspace` for the selected Topic Actor, and prepares a worktree at the Topic Actor Workspace path
- **AND** the default branch uses the `per-topic-actor/<topic-actor-name>/main` namespace

#### Scenario: Alternate worktree sources are out of scope
- **WHEN** the user requests a Topic Actor Workspace worktree anchored from a repository other than `topic.repos.main`
- **THEN** the Topic Workspace Manager reports that alternate source repositories are unsupported in this change
- **AND** it does not create an ad hoc worktree from the alternate source

### Requirement: Workspace Manager Supports Actor Diagnostics
The Topic Workspace Manager skill SHALL support diagnostics and topology inspection for Topic Actor Workspaces without becoming the canonical creator of topic-main, topic env readiness, or research records.

#### Scenario: Actor diagnostics report resolved surfaces
- **WHEN** the Topic Workspace Manager skill is invoked for a human-orchestrated research topic
- **THEN** it reports the selected Topic Workspace, `topic.repos.main`, Topic Actor roster, Topic Actor Workspace paths, formal Agent Workspace paths when present, Isomer-managed namespace posture, research record labels, optional projection roots, blockers, and next actions
- **AND** it identifies which surfaces are authoritative records, Git anchors, actor work surfaces, formal agent work surfaces, or local temporary surfaces

#### Scenario: Manager does not replace setup services
- **WHEN** actor diagnostics find missing topic-main readiness, topic env readiness, research record labels, or Topic Actor Workspace readiness
- **THEN** the manager reports the missing evidence and routes repair to the common topic preparation workflow, Topic Workspace environment setup, Topic Actor management workflow, or research workspace bootstrap
- **AND** it does not claim canonical readiness by creating substitute files outside those workflows

### Requirement: Topic Workspace Manager Excludes Research Bootstrap
The Topic Workspace Manager SHALL remain responsible for Topic Workspace topology, Topic Actor CRUD, materialization, repair, archive, and actor-scoped path diagnostics without owning research-paradigm bootstrap or handoff records.

#### Scenario: Actor management avoids research records
- **WHEN** `isomer-admin-topic-workspace-mgr manage-actors` registers, updates, materializes, repairs, diagnoses, or archives Topic Actors
- **THEN** it reports actor topology, actor workspaces, branches, support labels, audit refs when available, blockers, and repair routes
- **AND** it does not create research records, v2 placeholder registries, v2 bootstrap outputs, or accepted research artifact instructions

#### Scenario: Topic workspace summary stays topology scoped
- **WHEN** `isomer-admin-topic-workspace-mgr summarize` reports Topic Actor readiness
- **THEN** it reports actor-scoped semantic paths, branch posture, support labels, tmp posture, boundary material, validation status, blockers, and next operator action
- **AND** it does not claim research-paradigm readiness or v2 bootstrap readiness

