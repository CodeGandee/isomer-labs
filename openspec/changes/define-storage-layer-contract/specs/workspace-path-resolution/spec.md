## ADDED Requirements

### Requirement: Effective Semantic Surface Catalog
Workspace Path Resolution SHALL resolve paths from an effective semantic surface catalog composed of built-in reserved labels, accepted grouped reserved labels, and valid manifest-declared `custom.*` labels.

#### Scenario: Built-in labels remain available
- **WHEN** a caller lists semantic paths for a selected Topic Workspace
- **THEN** the output includes built-in labels such as `topic.repos.main`, `topic.records.artifacts`, `topic.runtime.db`, `agent.workspace`, `agent.private_artifacts`, and `agent.tmp` with `storage_profile` id and storage-profile-derived traits

#### Scenario: Grouped topic repository labels are available
- **WHEN** the effective catalog contains accepted repository labels such as `topic.repos.main` or `topic.repos.inner_group.some_repo_name`
- **THEN** Workspace Path Resolution can resolve each label with source, `storage_profile` id, storage-profile-derived traits, and diagnostics

#### Scenario: Manifest custom labels are available
- **WHEN** the Topic Workspace Manifest declares a valid custom label under `custom.*`
- **THEN** Workspace Path Resolution includes that label in the effective catalog and can resolve it with source, `storage_profile` id, storage-profile-derived traits, and diagnostics

#### Scenario: Undeclared custom label is rejected
- **WHEN** a caller requests a label that is neither built into Isomer nor declared as a valid custom label in the Topic Workspace Manifest
- **THEN** Workspace Path Resolution reports an unknown semantic label diagnostic

### Requirement: Semantic Path Read Operations
Workspace Path Resolution SHALL expose side-effect-free read operations for effective semantic labels and their candidate sources.

#### Scenario: List reports effective labels
- **WHEN** a caller lists semantic paths for a selected context
- **THEN** the response reports effective labels, label source, resolved path when available, `storage_profile` id, storage-profile-derived traits, and diagnostics without creating or modifying filesystem targets

#### Scenario: Get resolves one effective label
- **WHEN** a caller gets a semantic path by label
- **THEN** the response returns the winning resolved path, source, `storage_profile` id, storage-profile-derived traits, and diagnostics without creating or modifying filesystem targets

#### Scenario: Explain does not mutate state
- **WHEN** a caller explains a semantic label
- **THEN** the response reports candidate sources and selection reasons without writing Path Plans, manifests, environment variables, or filesystem targets

### Requirement: Required Context Resolution
Workspace Path Resolution SHALL resolve labels only after the required Project, Topic, and Agent context selectors are available.

#### Scenario: Topic context inferred from cwd
- **WHEN** `isomer-cli` is invoked from inside a Topic Workspace and a caller requests a `topic.*` label
- **THEN** Workspace Path Resolution uses the cwd-derived Effective Topic Context when the cwd identifies exactly one Topic Workspace

#### Scenario: Topic selector required outside topic workspace
- **WHEN** `isomer-cli` is invoked from the Project root, outside a Topic Workspace, or from an ambiguous cwd and a caller requests a `topic.*` label
- **THEN** Workspace Path Resolution requires an explicit topic selector and reports a selection diagnostic when it is missing

#### Scenario: Agent context remains explicit
- **WHEN** a caller requests an `agent.*` label
- **THEN** Workspace Path Resolution requires both an Effective Topic Context and an Effective Agent Context from an explicit selector, supported environment context, cwd-derived Agent Workspace, or recorded runtime context

#### Scenario: Custom context follows metadata
- **WHEN** a caller requests a `custom.*` label
- **THEN** Workspace Path Resolution enforces the required context from that label's `storage_profile` before returning a path

### Requirement: Parent-derived Default Bindings
Workspace Path Resolution SHALL derive child default bindings from resolved parent semantic labels when the child surface semantically belongs under the parent.

#### Scenario: Topic Main Repository children follow custom parent
- **WHEN** the Topic Workspace Manifest binds `topic.repos.main` to a safe project-local path that differs from `repos/topic-main`
- **THEN** default child labels such as `topic.repos.main.tmp`, `topic.repos.main.isomer_managed`, and `topic.repos.main.tracked` resolve under the resolved `topic.repos.main` path unless they have their own higher-precedence binding

#### Scenario: Agent children follow custom workspace
- **WHEN** `agent.workspace` resolves from a manifest binding, environment override, or Path Plan
- **THEN** default child labels such as `agent.private_artifacts`, `agent.runtime`, `agent.scratch`, `agent.public_share`, and `agent.tmp` resolve under the resolved `agent.workspace` path unless they have their own higher-precedence binding

#### Scenario: Default layout output is unchanged without custom parent
- **WHEN** a Topic Workspace uses `isomer-default.v1` without custom parent bindings
- **THEN** parent-derived labels resolve to the same concrete default paths that existing default layout documentation shows

### Requirement: Default Path Query and Materialization
Workspace Path Resolution SHALL expose default-layout path queries and default path materialization for system-defined reserved semantic labels.

#### Scenario: Default path query ignores configured overrides
- **WHEN** a caller asks for the default path of a reserved semantic label such as `topic.repos.main`
- **THEN** Workspace Path Resolution returns the default-layout path for the selected context without using Path Plans, environment overrides, or Topic Workspace Manifest bindings

#### Scenario: Default path materialization creates the default target
- **WHEN** a caller asks to materialize the default path for a reserved semantic label with a default path definition
- **THEN** the command creates the path or path parent required by that label's storage profile and reports the default path, created paths, source, and diagnostics

#### Scenario: Custom label has no implicit default
- **WHEN** a caller asks for the default path of a `custom.*` label
- **THEN** Workspace Path Resolution reports that custom labels require an explicit registered path binding

### Requirement: Effective Path Materialization
Workspace Path Resolution SHALL support explicit materialization of the currently configured target for an existing effective semantic label.

#### Scenario: Configured materialization creates effective target
- **WHEN** a caller asks to materialize an existing effective semantic label
- **THEN** the command resolves the current configured target without stored Path Plan precedence, creates the path or path parent required by the label's storage profile, and reports created paths, source, and diagnostics

#### Scenario: Materialization does not define missing custom label
- **WHEN** a caller asks to materialize a `custom.*` label that is not declared in the effective catalog
- **THEN** Workspace Path Resolution reports an unknown semantic label diagnostic and does not create a guessed path

#### Scenario: Materialization leaves previous targets untouched
- **WHEN** a semantic label's configured binding changed since a previous materialization
- **THEN** materializing the current target does not delete, move, or rewrite files under the previous target and does not rewrite historical Path Plans

### Requirement: Universal Semantic Environment Overrides
Workspace Path Resolution SHALL support a generated 12-factor path environment variable for every effective semantic label while preserving existing compatibility variables.

#### Scenario: Canonical semantic env var resolves built-in label
- **WHEN** `ISOMER_PATH__TOPIC__REPOS__MAIN` is set and no Path Plan applies for `topic.repos.main`
- **THEN** Workspace Path Resolution uses that value for `topic.repos.main` before checking the Topic Workspace Manifest or default layout profile

#### Scenario: Canonical semantic env var resolves custom label
- **WHEN** `ISOMER_PATH__CUSTOM__DATASETS__RAW` is set for a manifest-declared label `custom.datasets.raw`
- **THEN** Workspace Path Resolution uses that value for the custom label before checking the Topic Workspace Manifest binding

#### Scenario: Environment variable does not create custom label
- **WHEN** `ISOMER_PATH__CUSTOM__DATASETS__RAW` is set but `custom.datasets.raw` is not declared in the effective catalog
- **THEN** Workspace Path Resolution reports an unknown semantic label diagnostic instead of treating the environment variable as a label registration

#### Scenario: Compatibility env conflict is diagnostic
- **WHEN** both the generated semantic env var and an existing compatibility env var apply to the same label and resolve to different paths
- **THEN** Workspace Path Resolution reports an environment override conflict instead of selecting one silently

### Requirement: Recorded and Configured Resolution Modes
Workspace Path Resolution SHALL expose both recorded-aware resolution and current configured resolution for semantic labels.

#### Scenario: Recorded-aware path get preserves Path Plan precedence
- **WHEN** a matching Path Plan exists for the requested semantic label and scope
- **THEN** the default single-label path query returns the Path Plan path before checking environment overrides, manifest bindings, or default layout profile bindings

#### Scenario: Configured resolution ignores Path Plans
- **WHEN** a caller requests configured resolution for a semantic label
- **THEN** Workspace Path Resolution ignores stored Path Plans and returns the current environment, Topic Workspace Manifest, Project Manifest, or default-layout-profile result with source metadata

#### Scenario: Explain reports candidate chain
- **WHEN** a caller requests explanation for a semantic label
- **THEN** the response reports applicable Path Plan, environment, Topic Workspace Manifest, Project Manifest, and default-layout-profile candidates and identifies why the selected candidate won
