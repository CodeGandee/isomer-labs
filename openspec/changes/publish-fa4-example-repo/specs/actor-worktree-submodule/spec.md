## ADDED Requirements

### Requirement: Actor worktrees become branches of the public repository
The system SHALL create a dedicated branch in the public repository for each actor worktree in the original workspace.

#### Scenario: Operator actor branch
- **WHEN** the original workspace has an operator actor worktree on branch `per-topic-actor/operator/main`
- **THEN** the public repository has a branch named `actor-operator` containing the sanitized operator worktree content

### Requirement: Actor branches are attached as submodules in the main branch
The main branch of the public repository SHALL include a Git submodule for each actor branch, configured to track the corresponding actor branch.

#### Scenario: Submodule configuration
- **WHEN** a user opens `.gitmodules` in the main branch
- **THEN** an entry exists for `actors/operator` pointing to the public repository URL with `branch = actor-operator`

#### Scenario: Recursive clone
- **WHEN** a user runs `git clone --recurse-submodules` on the public repository
- **THEN** the `actors/operator/` directory is populated with the content of the `actor-operator` branch

### Requirement: Actor branch history is sanitized
The system SHALL ensure that commits pushed to actor branches do not contain host identifiers or private workspace state.

#### Scenario: Sanitized actor history
- **WHEN** a user inspects the `actor-operator` branch history
- **THEN** no commit contains the original username, hostname, or host-specific absolute path
