## ADDED Requirements

### Requirement: Topic Workspace Documentation Explains Topic Main Development Repository
The documentation SHALL explain that the Topic Main Development Repository is the topic-owned development repository resolved by `topic.repos.main` and prepared by Topic Workspace environment setup.

#### Scenario: Topic workspace definition names ownership
- **WHEN** a reader opens Topic Workspace documentation
- **THEN** it states that `repos/topic-main` is the default Topic Main Development Repository
- **AND** it states that topic env setup creates, configures, and verifies it before Agent Workspace worktrees are created

#### Scenario: Existing user repo impact is explained
- **WHEN** documentation describes a custom or existing `topic.repos.main`
- **THEN** it explains that Isomer-created material belongs under `isomer-managed/`
- **AND** it does not instruct users to add top-level `extern/`, `shared/`, `tasks/`, `runs/`, or similar Isomer directories to the repository root

### Requirement: Documentation Explains External Repo Projections
The documentation SHALL distinguish canonical external repos under `repos/extern/...` from their Isomer-managed projections inside topic-main.

#### Scenario: Canonical external repo storage is documented
- **WHEN** documentation describes non-main `topic.repos.*` repositories
- **THEN** it states that their default canonical location is `repos/extern/<repo-label-path>`
- **AND** it states that these repositories are not Agent Workspace worktree anchors

#### Scenario: Projection roots are documented
- **WHEN** documentation describes how humans or agents access external repos from topic-main
- **THEN** it shows `isomer-managed/topic-owned/readonly/extern/...` for read-only projections
- **AND** it shows `isomer-managed/topic-owned/writable/extern/...` for writable projections
- **AND** it names `isomer-managed/tracked/manifests/extern-projections.toml` as the projection metadata file

### Requirement: Documentation States Breaking Recreate Policy
The documentation SHALL state that this Topic Workspace layout revision is breaking and that generated `isomer-content/` internals can be recreated instead of migrated.

#### Scenario: Old internals are not promised
- **WHEN** docs mention old generated paths, old topic-main setup responsibility, or old projection locations
- **THEN** they describe those conventions as replaced by the revised layout
- **AND** they do not promise compatibility for old generated Topic Workspace internals

#### Scenario: Validation docs prefer recreate
- **WHEN** docs describe validation failures caused by old generated `isomer-content/` internals
- **THEN** they name recreation under the revised layout as the accepted resolution
