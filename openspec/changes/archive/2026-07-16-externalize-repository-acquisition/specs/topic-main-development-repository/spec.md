## MODIFIED Requirements

### Requirement: Canonical External Repositories
The system SHALL keep third-party or supporting repositories as canonical topic repositories under semantic `topic.repos.<group...>.<repo-name>` labels, defaulting to `repos/extern/<repo-label-path>`, and SHALL register their existing paths without owning repository acquisition commands.

#### Scenario: External repository target is semantic
- **WHEN** topic environment setup needs a third-party repository that is not already registered
- **THEN** it queries or selects a candidate path for a non-main `topic.repos.*` label without mutating the Topic Workspace Manifest
- **AND** the `isomer-default.v1` candidate path is under `<topic-workspace>/repos/extern/...`

#### Scenario: External repository becomes canonical after verification
- **WHEN** the acting user or agent completes external repository acquisition and verifies the intended source and immutable identity
- **THEN** it registers the existing path under the selected non-main `topic.repos.*` label with `storage_profile = "topic_repo"`
- **AND** Isomer does not create, clone, fetch, checkout, rewrite, move, or delete repository content as part of registration

#### Scenario: External repository is not the main repository
- **WHEN** a non-main topic repository is registered at `repos/extern/...` or another accepted path
- **THEN** the system treats it as canonical supporting source material
- **AND** it does not use that repository as the Git anchor for Agent Workspace worktrees

#### Scenario: External repository provenance is not path topology
- **WHEN** a research workflow records source locator, immutable revision, acquisition method, command evidence, access, license, limitation, or relationship data for a Canonical External Repository
- **THEN** it stores that information in applicable Artifacts and Provenance Records related to the semantic repository label
- **AND** the Topic Workspace Manifest remains authority only for the canonical semantic path binding
