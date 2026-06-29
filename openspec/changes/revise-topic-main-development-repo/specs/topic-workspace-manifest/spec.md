## ADDED Requirements

### Requirement: Topic Main Projection Semantic Labels
The Topic Workspace Manifest and built-in default layout profile SHALL support fixed semantic labels for Topic Main Development Repository projection roots and projection metadata.

#### Scenario: Default projection labels exist
- **WHEN** a Topic Workspace uses the built-in `isomer-default.v1` layout profile
- **THEN** `topic.repos.main.projections.readonly` resolves to `<resolved topic.repos.main>/isomer-managed/topic-owned/readonly/extern/`
- **AND** `topic.repos.main.projections.writable` resolves to `<resolved topic.repos.main>/isomer-managed/topic-owned/writable/extern/`
- **AND** `topic.repos.main.projections.manifest` resolves to `<resolved topic.repos.main>/isomer-managed/tracked/manifests/extern-projections.toml`

#### Scenario: Projection label storage profiles are explicit
- **WHEN** the built-in catalog declares Topic Main projection labels
- **THEN** read-only and writable projection roots use accepted topic-repo-local projection directory storage profiles
- **AND** the projection manifest uses an accepted topic-repo-local tracked file storage profile

#### Scenario: Projection labels follow custom main repo binding
- **WHEN** a Topic Workspace Manifest safely overrides `topic.repos.main`
- **THEN** the default projection label paths are derived under the resolved custom `topic.repos.main` path
- **AND** the system does not fall back to `<topic-workspace>/repos/topic-main` for those projection labels

### Requirement: Projection Namespace Is Reserved
The Topic Workspace Manifest SHALL reserve Topic Main Development Repository projection labels as built-in labels instead of treating them as dynamic grouped topic repository labels.

#### Scenario: Projection labels are not external repo sources
- **WHEN** a command resolves `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, or `topic.repos.main.projections.manifest`
- **THEN** it treats the label as a built-in Topic Main support surface
- **AND** it does not treat the label as a canonical `topic.repos.*` external repository

#### Scenario: Unknown main sublabels are rejected
- **WHEN** a manifest declares an unknown label under `topic.repos.main.*`
- **THEN** validation reports an unknown or reserved semantic label diagnostic
- **AND** it does not accept the label through the grouped `topic.repos.*` dynamic repository rule

### Requirement: Breaking Manifest Compatibility
The Topic Workspace Manifest implementation SHALL not preserve old generated layout internals after this breaking layout revision.

#### Scenario: Old generated bindings are invalid
- **WHEN** old generated Topic Workspace bindings point to deprecated source gate paths, deprecated topic-main support paths, or deprecated projection paths
- **THEN** validation may reject those bindings without offering an automatic migration path

#### Scenario: Recreated content uses new defaults
- **WHEN** a Project recreates generated `isomer-content/` material after this change
- **THEN** the default profile uses the revised Topic Main Development Repository and projection labels
