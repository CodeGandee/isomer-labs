## ADDED Requirements

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
The topic workspace manager skill SHALL use `<topic-workspace-dir>/repos/topic-main` as the shared topic repository and `<topic-workspace-dir>/agents/<agent-key>` as each prepared Agent Workspace worktree.

#### Scenario: Workspace resolution uses Project Manifest
- **WHEN** `resolve-workspace` runs
- **THEN** it resolves Project root, Research Topic, and Topic Workspace through Project Manifest-backed Isomer context instead of inferring a Topic Workspace by scanning directories

#### Scenario: Shared topic repo is placed under repos
- **WHEN** `ensure-main-repo` creates or validates the shared topic repository
- **THEN** the expected repository path is `<topic-workspace-dir>/repos/topic-main`

#### Scenario: Agent worktrees are placed under agents
- **WHEN** `create-worktrees` creates an Agent Workspace for agent key `alice`
- **THEN** the expected worktree path is `<topic-workspace-dir>/agents/alice`

#### Scenario: Existing unsafe repo blocks preparation
- **WHEN** `<topic-workspace-dir>/repos/topic-main` exists but is not a usable Git repository for worktree creation
- **THEN** the skill reports a blocker and does not delete, replace, pull, or reinitialize the existing path without explicit user instruction

### Requirement: Agent Planning and Branch Names
The topic workspace manager skill SHALL normalize per-agent keys, map them to role bindings, and use deterministic per-agent branch namespaces.

#### Scenario: Agent keys are path safe
- **WHEN** `plan-agents` resolves requested agent keys
- **THEN** it rejects empty keys, unsafe path segments, and normalized key collisions before creating worktrees or updating workspace refs

#### Scenario: Default per-agent branch is deterministic
- **WHEN** `plan-agents` plans an Agent Workspace for agent key `alice`
- **THEN** the default branch is `per-agent/alice/main`

#### Scenario: Future per-agent branches stay under prefix
- **WHEN** `create-agent-branch` creates branch `experiment-1` for agent key `alice`
- **THEN** the branch name is `per-agent/alice/experiment-1`

#### Scenario: Cross-agent branch prefix is rejected
- **WHEN** an agent branch request for agent key `alice` names a branch outside `per-agent/alice/`
- **THEN** the skill rejects the branch request before mutating Git state

### Requirement: Worktree Creation Safety
The topic workspace manager skill SHALL create Git worktrees idempotently and refuse ambiguous or unsafe workspace topology.

#### Scenario: Worktree creation uses topic-main
- **WHEN** `create-worktrees` prepares an Agent Workspace for agent key `alice`
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

### Requirement: Profile and Packet Workspace Ref Updates
The topic workspace manager skill SHALL write or validate planned Agent Workspace refs in Topic Team Instantiation Packet or Topic Agent Team Profile material when requested by the operator workflow.

#### Scenario: Role binding receives workspace ref
- **WHEN** `plan-agents` maps an active role binding to agent key `alice`
- **THEN** the planned role binding `agent_workspace_ref` is `<topic-workspace-dir>/agents/alice` or an equivalent project-relative ref under the selected Topic Workspace

#### Scenario: Workspace refs are reported
- **WHEN** the skill completes planning or creation
- **THEN** its output reports role ids, agent keys, Agent Workspace paths, branch names, and any profile or packet files changed

#### Scenario: Cross-topic workspace ref is rejected
- **WHEN** a planned role binding points outside the selected Topic Workspace or into another Research Topic's Topic Workspace
- **THEN** the skill reports a blocker and does not treat the workspace plan as ready

### Requirement: Workspace Boundary and Summary Material
The topic workspace manager skill SHALL record advisory Workspace Boundary and summary material for prepared Git-backed Agent Workspaces.

#### Scenario: Boundary docs are written
- **WHEN** `write-boundaries` runs after worktree planning
- **THEN** it writes or updates topic-level and per-agent boundary material that names write ownership, Peer Read Access, branch rules, and safe integration expectations

#### Scenario: Boundaries are advisory
- **WHEN** the boundary material describes Agent Workspace access
- **THEN** it states that Workspace Boundaries and Peer Read Access are advisory and are not filesystem-grade security isolation

#### Scenario: Summary is consumer neutral
- **WHEN** `summarize` runs
- **THEN** it reports the shared topic repository, every agent key, worktree path, current branch, expected branch namespace, boundary material path, validation status, blockers, and next operator action

### Requirement: Topic Workspace Manager Validation
The topic workspace manager skill SHALL validate prepared Git-backed workspace topology without repairing it silently.

#### Scenario: Validation checks Git topology
- **WHEN** `validate-worktrees` runs
- **THEN** it checks `topic-main`, expected worktree paths, expected current branches, duplicate branch checkouts, and branch namespace compliance

#### Scenario: Validation checks Isomer refs
- **WHEN** `validate-worktrees` has access to packet or profile material
- **THEN** it checks that active role binding `agent_workspace_ref` values match prepared worktree paths for the selected Topic Workspace

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
