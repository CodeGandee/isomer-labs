## MODIFIED Requirements

### Requirement: Topic Workspace Manager Operator Skill
The operator/admin skillset SHALL include `isomer-admin-topic-workspace-mgr` as the operator surface for Git-backed Topic Workspace repository and Agent Workspace worktree preparation, and it SHALL describe non-main topic repositories as supporting repositories resolved through the semantic storage contract.

#### Scenario: Topic workspace manager skill is active
- **WHEN** the operator skillset is inspected
- **THEN** it contains `skillset/operator/isomer-admin-topic-workspace-mgr/` as an active operator skill folder

#### Scenario: Operator docs list topic workspace manager
- **WHEN** a developer reads `skillset/operator/README.md`
- **THEN** it lists `isomer-admin-topic-workspace-mgr` and describes it as the skill for preparing and validating `repos/topic-main` plus per-agent Agent Workspace worktrees

#### Scenario: Operator validation covers topic workspace manager
- **WHEN** operator skill validation runs
- **THEN** it validates the topic workspace manager skill with the same frontmatter, UI metadata, local-reference, workflow, and naming checks used for other active operator skills

#### Scenario: Topic workspace manager stays bounded
- **WHEN** the topic workspace manager skill reports prepared workspaces
- **THEN** it does not claim Agent Team Instance creation, Workspace Runtime mutation, Houmao launch, adapter launch material readiness, or runtime team readiness

#### Scenario: Additional topic repositories are external support surfaces
- **WHEN** the topic workspace manager skill documents or registers an additional non-main topic repository
- **THEN** it uses `topic.repos.<group...>.<repo-name>` semantic labels with `storage_profile = "topic_repo"`
- **AND** it describes `repos/extern/...` as the default physical location for helper-created non-main topic repositories
- **AND** it does not describe non-main repositories as Agent Workspace worktree sources
