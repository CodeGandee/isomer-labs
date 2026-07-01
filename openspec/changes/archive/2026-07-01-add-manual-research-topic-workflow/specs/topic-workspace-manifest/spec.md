## ADDED Requirements

### Requirement: Topic Actor Binding Schema
The Topic Workspace Manifest SHALL support Topic Actor bindings for human-orchestrated topic-local workers.

#### Scenario: Topic Actor binding is parsed
- **WHEN** `topic-workspace.toml` contains a Topic Actor binding
- **THEN** manifest loading exposes the actor's topic-local name, actor kind, runtime kind, role kind, controller, default cwd label, optional workspace label, optional workspace path, optional branch, optional adapter ref, status, and source detail

#### Scenario: Topic Actor name is path safe
- **WHEN** validation checks a Topic Actor binding
- **THEN** it requires `topic_actor_name` to be path-safe and unique among active Topic Actor bindings in the selected Topic Workspace

#### Scenario: Topic Actor enum fields are bounded and extensible
- **WHEN** validation checks `actor_kind`, `runtime_kind`, `role_kind`, `controller_kind`, or `status`
- **THEN** it accepts defined core values and values under `custom.*`
- **AND** it rejects unknown non-extension values with a deterministic diagnostic

#### Scenario: Topic Actor binding does not imply Agent Instance
- **WHEN** a Topic Actor binding omits Agent Instance or Agent Team Instance refs
- **THEN** manifest validation accepts the binding when its actor fields and workspace fields are otherwise valid

#### Scenario: Manifest remains actor topology authority
- **WHEN** Workspace Runtime contains mutation or provenance audit records for Topic Actor registration or materialization
- **THEN** path resolution still uses the Topic Workspace Manifest Topic Actor binding as the authoritative actor topology source

### Requirement: Actor-Scoped Semantic Labels
The Topic Workspace Manifest and default layout profile SHALL support actor-scoped semantic labels for Topic Actor Workspaces.

#### Scenario: Default Topic Actor Workspace label resolves under actors root
- **WHEN** a Topic Actor named `claude-scout` uses the default layout profile
- **THEN** `topic.actors.workspace` resolves to `<topic-workspace>/actors/claude-scout`
- **AND** the Topic Actor Workspace is separate from `topic.repos.main` and from formal `agent.workspace` paths

#### Scenario: Actor support labels resolve under Topic Actor Workspace
- **WHEN** actor-scoped support labels are resolved for a Topic Actor
- **THEN** labels such as `topic.actors.tmp`, `topic.actors.isomer_managed`, `topic.actors.private_artifacts`, `topic.actors.logs`, and `topic.actors.links` resolve under that Topic Actor Workspace according to the selected layout profile

#### Scenario: Actor label requires actor context
- **WHEN** a command resolves `topic.actors.workspace` or another actor-scoped label without a Topic Actor selector, environment actor context, cwd-derived actor context, or lifecycle actor ref
- **THEN** path resolution reports that a Topic Actor context is required

### Requirement: Topic Actor Workspace Metadata
The Topic Workspace Manifest SHALL record enough Topic Actor Workspace metadata for reproducible worktree setup.

#### Scenario: Actor branch namespace is recorded
- **WHEN** a Topic Actor binding requests a worktree-backed Topic Actor Workspace
- **THEN** the binding or derived plan records a branch under `per-topic-actor/<topic-actor-name>/`

#### Scenario: Actor workspace source is topic-main
- **WHEN** a Topic Actor Workspace worktree is prepared
- **THEN** the source repository is the resolved `topic.repos.main` repository and the actor binding does not redefine `topic.repos.main`
