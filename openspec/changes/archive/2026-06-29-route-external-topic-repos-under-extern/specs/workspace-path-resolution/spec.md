## ADDED Requirements

### Requirement: Non-main Topic Repository Default Placement
Workspace Path Resolution and repository helper commands SHALL keep `topic.repos.main` as the primary Topic Main Repository label while placing helper-created non-main topic repositories under the default external repository namespace.

#### Scenario: Main repository default remains stable
- **WHEN** a caller resolves or materializes the built-in `topic.repos.main` label under `isomer-default.v1`
- **THEN** the resolved default path remains `<topic-workspace>/repos/topic-main`

#### Scenario: Non-main topic repo helper default uses extern namespace
- **WHEN** a user creates a grouped non-main topic repository through `project repos create` without an explicit `--path`
- **THEN** the helper registers the requested `topic.repos.<group...>.<repo-name>` label with `storage_profile = "topic_repo"`
- **AND** it uses `<topic-workspace>/repos/extern/<group...>/<repo-name>` as the default target path

#### Scenario: Explicit bindings remain authoritative
- **WHEN** a manifest binding or path registration explicitly binds a non-main `topic.repos.*` label to a safe project-local path outside `repos/extern/...`
- **THEN** Workspace Path Resolution resolves that label through the explicit binding instead of rewriting it to the default external repository namespace

#### Scenario: Extern namespace is physical layout only
- **WHEN** a caller queries a non-main topic repository
- **THEN** the semantic label remains `topic.repos.<group...>.<repo-name>` rather than including `extern` as a semantic label segment unless the user explicitly chose `extern` as part of the repository label
