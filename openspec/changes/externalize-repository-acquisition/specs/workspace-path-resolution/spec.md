## MODIFIED Requirements

### Requirement: Non-main Topic Repository Default Placement
Workspace Path Resolution and repository helper commands SHALL keep `topic.repos.main` as the primary Topic Main Repository label while planning, registering, or helper-creating non-main topic repositories under the default external repository namespace.

#### Scenario: Main repository default remains stable
- **WHEN** a caller resolves or materializes the built-in `topic.repos.main` label under `isomer-default.v1`
- **THEN** the resolved default path remains `<topic-workspace>/repos/topic-main`

#### Scenario: Unregistered non-main repository default can be queried
- **WHEN** a caller queries `project paths default` for a valid unregistered `topic.repos.<group...>.<repo-name>` label
- **THEN** Workspace Path Resolution returns `<topic-workspace>/repos/extern/<group...>/<repo-name>` with `storage_profile = "topic_repo"`
- **AND** the query does not create a binding, directory, repository, or Path Plan

#### Scenario: Existing non-main repository is registered
- **WHEN** a user runs `project repos register <repo-label> --path <existing-path>` after externally acquiring and verifying a repository
- **THEN** the helper registers the requested `topic.repos.<group...>.<repo-name>` label with `storage_profile = "topic_repo"` at the existing canonical path
- **AND** it does not create, initialize, clone, fetch, checkout, move, rewrite, or delete repository content

#### Scenario: Non-main topic repo creation helper uses extern namespace
- **WHEN** a user creates a grouped non-main topic repository directory through `project repos create` without an explicit `--path`
- **THEN** the helper registers the requested `topic.repos.<group...>.<repo-name>` label with `storage_profile = "topic_repo"`
- **AND** it uses `<topic-workspace>/repos/extern/<group...>/<repo-name>` as the default target path without initializing or acquiring a Git repository

#### Scenario: Explicit bindings remain authoritative
- **WHEN** a manifest binding or path registration explicitly binds a non-main `topic.repos.*` label to a safe project-local path outside `repos/extern/...`
- **THEN** Workspace Path Resolution resolves that label through the explicit binding instead of rewriting it to the default external repository namespace

#### Scenario: Extern namespace is physical layout only
- **WHEN** a caller queries a non-main topic repository
- **THEN** the semantic label remains `topic.repos.<group...>.<repo-name>` rather than including `extern` as a semantic label segment unless the user explicitly chose `extern` as part of the repository label
