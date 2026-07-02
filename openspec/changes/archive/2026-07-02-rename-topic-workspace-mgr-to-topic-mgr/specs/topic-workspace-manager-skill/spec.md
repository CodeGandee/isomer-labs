## REMOVED Requirements

### Requirement: Topic Workspace Manager Skill Bundle
**Reason**: The full initialized-topic management surface is renamed and broadened to `isomer-admin-topic-mgr`.
**Migration**: Use `topic-manager-skill` for canonical requirements. Keep the old skill folder only as a deprecated compatibility wrapper when implementation needs transition support.

### Requirement: Command-Style Subcommand Structure
**Reason**: The old workspace-manager subcommand structure is replaced by scope-prefixed topic-manager subcommands.
**Migration**: Route old subcommands through the compatibility mapping to `isomer-admin-topic-mgr` commands.

### Requirement: Topic Workspace Git Layout
**Reason**: Storage behavior moves under the broader topic manager storage command group.
**Migration**: Use `isomer-admin-topic-mgr storage-resolve`, `storage-inspect-main`, `storage-validate`, or `storage-register-repo`.

### Requirement: Agent Planning and Branch Names
**Reason**: Agent planning behavior moves under the topic manager team command group.
**Migration**: Use `isomer-admin-topic-mgr team-plan` and related `team-*` commands.

### Requirement: Worktree Creation Safety
**Reason**: Worktree materialization behavior moves under the topic manager team command group.
**Migration**: Use `isomer-admin-topic-mgr team-materialize-workspaces` and `team-validate-workspaces`.

### Requirement: Profile and Packet Workspace Ref Updates
**Reason**: Static topic team workspace ref handling moves under the topic manager team command group.
**Migration**: Use `isomer-admin-topic-mgr team-plan` and `team-validate-workspaces`.

### Requirement: Workspace Boundary and Summary Material
**Reason**: Boundary and summary behavior moves under initialized-topic status and team commands.
**Migration**: Use `isomer-admin-topic-mgr team-write-boundaries` and `status`.

### Requirement: Topic Workspace Manager Validation
**Reason**: Validation behavior moves under topic manager storage, actor, team, and environment verification commands.
**Migration**: Use `isomer-admin-topic-mgr storage-validate`, `actors-diagnose`, `team-validate-workspaces`, or `env-verify-*`.

### Requirement: Topic Workspace Manager Skill Validation
**Reason**: Repository validation should target the canonical topic manager skill and any compatibility wrapper separately.
**Migration**: Validate `isomer-admin-topic-mgr` as the active skill and validate `isomer-admin-topic-workspace-mgr` only as a deprecated wrapper if retained.

### Requirement: Semantic Workspace Manager Inputs
**Reason**: Semantic input handling moves under the topic manager storage command group.
**Migration**: Use `isomer-admin-topic-mgr storage-resolve`.

### Requirement: Default Layout Materialization
**Reason**: Default layout materialization is now an initialized-topic storage or team operation, not a standalone workspace-manager concern.
**Migration**: Use `isomer-admin-topic-mgr storage-inspect-main`, `storage-register-repo`, or `team-materialize-workspaces` as appropriate.

### Requirement: Semantic Agent Planning
**Reason**: Semantic Agent Workspace planning moves under topic manager team planning.
**Migration**: Use `isomer-admin-topic-mgr team-plan`.

### Requirement: Semantic Workspace Validation
**Reason**: Semantic validation moves under topic manager storage and team validation.
**Migration**: Use `isomer-admin-topic-mgr storage-validate` or `team-validate-workspaces`.

### Requirement: Summary Uses Semantic Labels
**Reason**: Summary behavior moves to the topic manager default `status` command.
**Migration**: Use `isomer-admin-topic-mgr status`.

### Requirement: Isomer-Managed Sharing Preparation
**Reason**: Sharing layout preparation moves under topic manager storage, actor, and team commands.
**Migration**: Use `isomer-admin-topic-mgr storage-inspect-main`, `actors-materialize`, or `team-materialize-workspaces`.

### Requirement: Isomer-Managed Conflict Diagnostics
**Reason**: Conflict diagnostics move under topic manager diagnostics and validation commands.
**Migration**: Use `isomer-admin-topic-mgr doctor`, `storage-validate`, `actors-diagnose`, or `team-validate-workspaces`.

### Requirement: Topic Workspace Manager Delegates Agent Env Readiness
**Reason**: Agent environment verification routing moves under explicit topic manager environment verification commands.
**Migration**: Use `isomer-admin-topic-mgr env-verify-agents`, which delegates formal cwd proof to `isomer-srv-agent-env-setup`.

### Requirement: Topic Workspace Manager Preserves Service Boundaries
**Reason**: Service-boundary requirements are carried by the new topic manager environment verification requirements.
**Migration**: Use the `topic-manager-skill` environment verification requirements.

### Requirement: Topic Workspace Manager Prepares Local Tmp Surfaces
**Reason**: Tmp surface preparation moves under the new storage, actor, and team commands.
**Migration**: Use the corresponding `isomer-admin-topic-mgr` scoped command.

### Requirement: Manager Skill Uses Storage Contract
**Reason**: Storage contract requirements move under `topic-manager-skill`.
**Migration**: Use the new topic manager storage management requirements.

### Requirement: Manager Skill Reports Custom Surface Evidence
**Reason**: Custom surface evidence moves under topic manager output and storage requirements.
**Migration**: Use `isomer-admin-topic-mgr storage-resolve`, `storage-validate`, and Complete Output.

### Requirement: Topic Workspace Manager Uses Essential and Complete Output
**Reason**: Output contract requirements move under the new topic manager output contract.
**Migration**: Use `isomer-admin-topic-mgr` Essential Output and Complete Output.

### Requirement: Optional Topology Support Boundary
**Reason**: Optional topology support becomes one scope within the broader initialized-topic manager.
**Migration**: Use `isomer-admin-topic-mgr storage-*`, `team-*`, and `doctor` commands.

### Requirement: Workspace Manager Owns Topic Actor Management
**Reason**: Topic Actor management moves under the topic manager actor command group.
**Migration**: Use `isomer-admin-topic-mgr actors-manage`, `actors-materialize`, or `actors-diagnose`.

### Requirement: Workspace Manager Materializes Topic Actor Workspaces
**Reason**: Topic Actor Workspace materialization moves under `isomer-admin-topic-mgr actors-materialize`.
**Migration**: Use `isomer-admin-topic-mgr actors-materialize`.

### Requirement: Workspace Manager Supports Actor Diagnostics
**Reason**: Actor diagnostics move under `isomer-admin-topic-mgr actors-diagnose`.
**Migration**: Use `isomer-admin-topic-mgr actors-diagnose`.

### Requirement: Topic Workspace Manager Excludes Research Bootstrap
**Reason**: The boundary remains true but belongs to the new topic manager and research v2 manager specs.
**Migration**: Use `topic-manager-skill` for initialized-topic operations and `isomer-rsch-workspace-mgr-v2` for research-specific bootstrap.

## ADDED Requirements

### Requirement: Deprecated Topic Workspace Manager Compatibility Wrapper
The repository SHALL keep `isomer-admin-topic-workspace-mgr` only as a deprecated compatibility wrapper when the folder is retained, and that wrapper SHALL route old invocations to `isomer-admin-topic-mgr`.

#### Scenario: Compatibility wrapper names replacement
- **WHEN** `skillset/operator/isomer-admin-topic-workspace-mgr/SKILL.md` is retained
- **THEN** its frontmatter or entrypoint marks the skill as deprecated for direct use
- **AND** it names `isomer-admin-topic-mgr` as the replacement

#### Scenario: Old subcommands route to new commands
- **WHEN** a compatibility invocation names `resolve-workspace`, `ensure-main-repo`, `manage-actors`, `plan-agents`, `create-worktrees`, `write-boundaries`, `create-agent-branch`, `validate-worktrees`, `install-packages`, `summarize`, or `topic-workspace`
- **THEN** the wrapper maps the request to the corresponding `isomer-admin-topic-mgr` scope-prefixed command
- **AND** it reports the new command name in the handoff

#### Scenario: Wrapper does not own full behavior
- **WHEN** the deprecated wrapper handles an invocation
- **THEN** it does not duplicate the full initialized-topic management instructions
- **AND** it defers canonical behavior, guardrails, and output contracts to `isomer-admin-topic-mgr`
