## ADDED Requirements

### Requirement: Content Root Relocation Planning
The system SHALL build a deterministic relocation plan before changing a Project generated content root.

#### Scenario: Dry-run reports relocation plan
- **WHEN** a user plans to move the Project generated content root from `isomer-content/` to `custom-content/`
- **THEN** the system reports the old content root, new content root, manifest updates, managed filesystem moves, skipped entries, unmanaged leftovers, warnings, and `mutated = false`

#### Scenario: Missing confirmation defaults to non-mutating plan
- **WHEN** a user runs content-root relocation without `--yes`
- **THEN** the system reports the relocation plan, does not create, move, modify, or delete Project files, and explains that `--yes` is required for mutation

#### Scenario: Plan requires valid manifest authority
- **WHEN** `.isomer-labs/manifest.toml` is missing or malformed
- **THEN** the system refuses relocation with a deterministic diagnostic and does not infer Topic Workspaces from directories

#### Scenario: Plan lists runtime breakage warning
- **WHEN** relocation planning succeeds
- **THEN** the plan warns that existing Workspace Runtime records, Pixi environments, installed packages, adapter runtime material, logs, and stored path plans may contain old paths and may require reinstall or reinitialization

### Requirement: Content Root Relocation Path Safety
The system SHALL validate old and new content-root paths before planning or applying relocation.

#### Scenario: Destination must stay project scoped
- **WHEN** the requested destination resolves outside the Project root
- **THEN** relocation refuses the destination and performs no filesystem or manifest mutation

#### Scenario: Destination must not be project root
- **WHEN** the requested destination resolves to the Project root
- **THEN** relocation refuses the destination and performs no filesystem or manifest mutation

#### Scenario: Destination must avoid project config and Houmao overlay
- **WHEN** the requested destination resolves inside `.isomer-labs/` or `.houmao/`
- **THEN** relocation refuses the destination and performs no filesystem or manifest mutation

#### Scenario: Symlink roots are refused
- **WHEN** the old content root or requested destination is a symlink entry
- **THEN** relocation refuses that root and does not follow the symlink destination

#### Scenario: Destination conflicts are refused
- **WHEN** a planned managed move would overwrite an existing destination entry
- **THEN** relocation refuses the conflicting move, reports the conflict, and performs no mutation

### Requirement: Managed Content Moves
The system SHALL move only Isomer-managed content entries when applying content-root relocation.

#### Scenario: Policy files move
- **WHEN** generated content-root policy files `README.md` and `.gitignore` exist under the old content root and relocation is confirmed
- **THEN** the system moves those policy files to the new content root and preserves them as content-root policy files

#### Scenario: Registered workspace inside old root moves
- **WHEN** a registered Topic Workspace path resolves inside the old content root and relocation is confirmed
- **THEN** the system moves that Topic Workspace directory to the same relative path under the new content root

#### Scenario: Registered workspace outside old root is skipped
- **WHEN** a registered Topic Workspace path resolves outside the old content root
- **THEN** the system leaves that directory and its manifest path unchanged and reports it as skipped by relocation

#### Scenario: Unknown old-root entries are preserved
- **WHEN** the old content root contains entries that are not generated policy files or registered Topic Workspace directories
- **THEN** relocation leaves those entries in place and reports them as unmanaged leftovers

#### Scenario: Empty old directories may be removed
- **WHEN** confirmed relocation moves all managed entries and the old content root or old `topic-ws` directory becomes empty
- **THEN** the system may remove those empty directories and reports the removal as part of the relocation result

### Requirement: Manifest Rewrite
The system SHALL rewrite Project Manifest paths for managed entries moved by content-root relocation.

#### Scenario: Content root default updates
- **WHEN** relocation is confirmed
- **THEN** the system updates `[paths].isomer_content_root` to the requested destination path using a Project-relative value when possible

#### Scenario: Topic workspace base updates when rooted in old content root
- **WHEN** `[paths].topic_workspace_base_dir` resolves inside the old content root and relocation is confirmed
- **THEN** the system rewrites it to the same relative path under the new content root

#### Scenario: Topic workspace base defaults to topic-ws under new root
- **WHEN** `[paths].topic_workspace_base_dir` is absent or derived from the old content root and relocation is confirmed
- **THEN** the system records `topic_workspace_base_dir` as `<new-content-root>/topic-ws`

#### Scenario: Registered workspace path updates when moved
- **WHEN** a registered Topic Workspace path resolves inside the old content root and relocation is confirmed
- **THEN** the system rewrites that `[[topic_workspaces]].path` to the new relative path under the new content root

#### Scenario: External registered workspace path is preserved
- **WHEN** a registered Topic Workspace path resolves outside the old content root
- **THEN** the system preserves that manifest path unchanged

### Requirement: Runtime Repair Boundary
The system SHALL warn about runtime breakage but SHALL NOT repair internal runtime or environment records during content-root relocation.

#### Scenario: Runtime DB is not rewritten
- **WHEN** a moved Topic Workspace contains `state.sqlite`
- **THEN** relocation does not open or rewrite the database and warns that stored path plans may still reference old paths

#### Scenario: Pixi environment is not rewritten
- **WHEN** a moved Topic Workspace contains `.pixi/` or other Pixi environment markers
- **THEN** relocation does not rewrite installed packages, virtual environments, lockfiles, shebangs, or package metadata and warns that the user may need to reinstall the environment

#### Scenario: Adapter runtime material is not rewritten
- **WHEN** a moved Topic Workspace contains adapter runtime manifests, launch material, logs, or handoff records
- **THEN** relocation moves the containing managed Topic Workspace directory if selected but does not rewrite the internal runtime records

### Requirement: Relocation Execution Result
The system SHALL report confirmed relocation results with deterministic text and machine-readable payloads.

#### Scenario: Confirmed payload reports mutation
- **WHEN** relocation runs with `--yes` and applies at least one managed move or manifest update
- **THEN** the output includes `mutated = true`, `dry_run = false`, the resolved Project root, old content root, new content root, applied moves, manifest updates, skipped entries, unmanaged leftovers, diagnostics, and warnings

#### Scenario: Failed execution reports partial state
- **WHEN** relocation cannot complete a planned move or manifest rewrite because of an operating-system error
- **THEN** the system returns deterministic diagnostics, reports any moves already applied or rolled back, and does not report successful completion

#### Scenario: Manifest write is atomic
- **WHEN** relocation applies manifest updates
- **THEN** the system writes the updated Project Manifest atomically so callers do not observe a partially written manifest file
