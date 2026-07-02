## REMOVED Requirements

### Requirement: Deprecated Topic Workspace Manager Compatibility Wrapper
**Reason**: The compatibility window is closed. Active routing has moved to `isomer-admin-topic-mgr`, and keeping an invokable wrapper keeps obsolete command names alive.
**Migration**: Use `isomer-admin-topic-mgr` and its scoped commands directly. Old invocations of `isomer-admin-topic-workspace-mgr` are unsupported and should be updated before use.

## ADDED Requirements

### Requirement: Topic Workspace Manager Skill Is Fully Retired
The repository SHALL NOT provide `isomer-admin-topic-workspace-mgr` as an invokable operator skill, compatibility wrapper, manifest entry, or user-facing route.

#### Scenario: Old skill folder is absent
- **WHEN** the operator skillset is inspected
- **THEN** `skillset/operator/isomer-admin-topic-workspace-mgr/` does not exist
- **AND** no `SKILL.md` or `agents/openai.yaml` for `isomer-admin-topic-workspace-mgr` is present

#### Scenario: Old invocations are not routed
- **WHEN** active skill documentation, active specs, or operator routing guidance describe initialized-topic management
- **THEN** they route users to `isomer-admin-topic-mgr`
- **AND** they do not ask users or agents to invoke `$isomer-admin-topic-workspace-mgr`

#### Scenario: Old command names are not public compatibility routes
- **WHEN** active guidance mentions retired command names such as `topic-workspace`, `summarize`, `resolve-workspace`, `ensure-main-repo`, `manage-actors`, `plan-agents`, `create-worktrees`, `write-boundaries`, `create-agent-branch`, `validate-worktrees`, or `install-packages`
- **THEN** the mention is either historical rationale or an explicit migration note to the corresponding `isomer-admin-topic-mgr` scoped command
- **AND** the mention does not present the old command as an invokable route
