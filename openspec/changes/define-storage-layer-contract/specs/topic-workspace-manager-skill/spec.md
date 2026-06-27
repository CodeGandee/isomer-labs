## ADDED Requirements

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
