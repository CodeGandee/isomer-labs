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
- **WHEN** the Topic Workspace Manifest binds `topic.main_repo` or `agent.workspace` to safe project-local paths that differ from the default layout
- **THEN** the skill uses those bindings for planning and validation instead of assuming the default paths

#### Scenario: Missing manifest uses default profile for planning
- **WHEN** the Topic Workspace Manifest is missing and the operator has not requested a custom layout
- **THEN** the skill plans against the built-in `isomer-default.v1` labels and reports that the paths come from the default profile

### Requirement: Default Layout Materialization
The topic workspace manager skill SHALL materialize default semantic workspace directories only when the operator asks for default creation.

#### Scenario: Default main repo is explicitly created
- **WHEN** the operator asks the skill to create default Topic Main Repository material
- **THEN** the skill creates or validates the `topic.main_repo` default binding and directory through the Topic Workspace Manifest contract

#### Scenario: Default agent worktrees are explicitly created
- **WHEN** the operator asks the skill to create Agent Workspace worktrees at default locations
- **THEN** the skill creates or validates `agent.workspace` default bindings for the planned Agent Names before creating the worktrees

#### Scenario: Read-only planning does not create manifest
- **WHEN** the skill runs `resolve-workspace`, `plan-agents`, `validate-worktrees`, or `summarize` without creation intent
- **THEN** it does not create or rewrite `topic-workspace.toml`, directories, branches, or worktrees

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

#### Scenario: Summary is label-first
- **WHEN** `summarize` runs
- **THEN** it reports semantic labels such as `topic.main_repo`, `agent.workspace`, `agent.private_artifacts`, and `agent.public_share` before showing concrete paths

#### Scenario: Default path is identified as default
- **WHEN** a path comes from `isomer-default.v1`
- **THEN** the summary identifies it as the default layout rather than presenting it as the only valid path

### Requirement: Isomer-Managed Sharing Preparation
The topic workspace manager skill SHALL prepare and validate the standard `isomer-managed/` sharing layout for the topic owner checkout and each Agent Workspace worktree.

#### Scenario: Tracked Isomer layout is prepared
- **WHEN** `ensure-main-repo` or `create-worktrees` prepares the Topic Main Repository layout
- **THEN** it creates or validates `isomer-managed/.gitignore` and `isomer-managed/tracked/{shared,artifacts,tasks,runs,views,tools,boundaries,manifests}/` without creating top-level Isomer collaboration directories in `topic-main`

#### Scenario: Agent-owned untracked layout is prepared
- **WHEN** `create-worktrees` prepares an Agent Workspace for agent name `alice`
- **THEN** it creates or validates `isomer-managed/agent-owned/{runtime,scratch,logs,artifacts,public,inbox}/` as ignored agent-owned material

#### Scenario: Topic-owned projection layout is prepared
- **WHEN** topic-owned non-Git material is configured for worker visibility
- **THEN** the skill creates or validates `isomer-managed/topic-owned/readonly/`, `isomer-managed/topic-owned/writable/`, and corresponding boundary policy before reporting the projection as ready

#### Scenario: Peer links are generated only when requested or configured
- **WHEN** the operator requests peer-readable convenience links or the workspace plan declares them
- **THEN** the skill creates links under `isomer-managed/links/peers/` to peer `isomer-managed/agent-owned/public/` paths and reports each link target

#### Scenario: Link creation is safe
- **WHEN** a requested generated link would point outside the selected Topic Workspace or into a forbidden owner-preserved root without an explicit projection policy
- **THEN** the skill reports a blocker and does not create the link

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
