## MODIFIED Requirements

### Requirement: Topic Actor Workspace Metadata
The Topic Workspace Manifest SHALL record enough Topic Actor Workspace metadata for reproducible worktree setup and for distinguishing ready actor worktrees from path collisions.

#### Scenario: Actor branch namespace is recorded
- **WHEN** a Topic Actor binding requests a worktree-backed Topic Actor Workspace
- **THEN** the binding or derived plan records a branch under `per-topic-actor/<topic-actor-name>/`

#### Scenario: Actor workspace source is topic-main
- **WHEN** a Topic Actor Workspace worktree is prepared
- **THEN** the source repository is the resolved `topic.repos.main` repository and the actor binding does not redefine `topic.repos.main`

#### Scenario: Actor worktree identity is reproducible
- **WHEN** a Topic Actor binding or derived plan describes a worktree-backed Topic Actor Workspace
- **THEN** it carries enough metadata for materialization and diagnostics to derive the resolved actor workspace path, expected `topic.repos.main` source repository, and expected actor branch

#### Scenario: Actor workspace path alone is not readiness
- **WHEN** a Topic Actor binding names a workspace path or label
- **THEN** manifest consumers do not treat path existence alone as Topic Actor Workspace readiness
- **AND** they require materialization or diagnostic evidence that the path is the expected worktree before reporting readiness
