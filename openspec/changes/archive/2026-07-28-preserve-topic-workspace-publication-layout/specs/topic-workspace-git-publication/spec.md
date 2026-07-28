## ADDED Requirements

### Requirement: Publication Preserves Topic Workspace Relative Paths
The publication projection SHALL be a path-preserving subset of the Source Topic Workspace in which every retained source-backed entry uses its normalized Topic Workspace-relative source path as its publication path.

#### Scenario: Ordinary source file is retained
- **WHEN** a Source Topic Workspace file at relative path `p` receives disposition `track`
- **THEN** the projection records `output_relative_path` equal to `p`
- **AND** the Topic Publication Copy stores the approved bytes at `p`

#### Scenario: Source file requires sanitization
- **WHEN** a Source Topic Workspace file at relative path `p` receives disposition `template`
- **THEN** the projection may change its bytes through an approved transformation
- **AND** it stores the sanitized result at `p` without renaming or relocating it

#### Scenario: Nested repository is retained
- **WHEN** a selected topic-owned component or registered reference repository resolves at Topic Workspace-relative path `p`
- **THEN** the superproject records its exact gitlink at `p`
- **AND** publication does not flatten, copy, or merge that repository's files into another superproject path

#### Scenario: Source path is excluded
- **WHEN** policy assigns `exclude` to a Source Topic Workspace path
- **THEN** the projection omits that path
- **AND** the exclusion does not relocate any retained sibling or create a placeholder that claims the excluded content is available

#### Scenario: Planner proposes a relocated source output
- **WHEN** a source-backed `track`, `template`, or `component` entry has an output path different from its normalized source-relative path
- **THEN** plan validation reports a path-preservation blocker
- **AND** publish sync performs no commit or push

#### Scenario: Excluded directory becomes empty
- **WHEN** a source directory has no retained file or gitlink after policy exclusions
- **THEN** publication may omit the empty directory because Git does not represent empty directories
- **AND** structural fidelity is evaluated over retained paths rather than literal directory-entry equality

### Requirement: Publication-Only Metadata Uses Reserved Paths
The Topic Publication Copy SHALL distinguish source-backed entries from generated publication entries and SHALL confine tracked publication-only metadata to reserved paths that cannot silently shadow Source Topic Workspace content.

#### Scenario: Publication metadata is generated
- **WHEN** the projection renders its portable research-record index, Publication Projection Manifest, and Topic Workspace version manifest
- **THEN** it writes them below `.isomer-publication/`
- **AND** it does not place those files in a synthetic source-content directory

#### Scenario: Root navigation files are generated
- **WHEN** publication materializes the superproject
- **THEN** root `README.md` and Git-required `.gitmodules` are the only generated root-level exceptions
- **AND** every other generated tracked file uses an approved reserved overlay path

#### Scenario: Source README already exists
- **WHEN** the Source Topic Workspace contains a sanitizable root `README.md`
- **THEN** publication retains it at `README.md` and deterministically adds or replaces the versioned Isomer publication navigation block
- **AND** it does not move the source README or discard source-authored content outside that managed block

#### Scenario: Reserved path collides with source content
- **WHEN** Source Topic Workspace content already occupies `.isomer-publication/` or conflicts with generated `.gitmodules`
- **THEN** planning reports a collision blocker
- **AND** it does not overwrite, relocate, or reinterpret the source content

#### Scenario: Copy-local publication support exists
- **WHEN** binding, plan, outcome, credential-helper, or other copy-local publication support exists under `.isomer/`
- **THEN** the publication repository excludes it through repository-local Git exclusion state
- **AND** it does not replace or relocate the Source Topic Workspace `.gitignore` to hide that support

### Requirement: Canonical Publication Branch Represents the Topic Workspace
The publication remote SHALL use `main` as its only sanitized Topic Workspace superproject branch, SHALL expose the current approved snapshot rather than publication history, and SHALL keep any required component refs separate from the superproject root.

#### Scenario: New publication creates the canonical branch
- **WHEN** the remote has no `main` branch and an approved sanitized superproject commit is ready
- **THEN** publish sync pushes that exact commit to `refs/heads/main`
- **AND** the commit tree contains the path-preserving Topic Workspace projection

#### Scenario: Topic Main component exists
- **WHEN** Topic Main is selected for the current snapshot
- **THEN** its sanitized commit is reachable from `components/topic-main`
- **AND** remote `main` records that component only as a gitlink at its resolved Topic Workspace-relative path
- **AND** publication does not merge or copy `topic-owner/main` content into the root of `main`

#### Scenario: Remote main contains a component-root or legacy layout
- **WHEN** existing `main` differs from the planned sanitized superproject snapshot
- **THEN** synchronization replaces it according to the current approved remote ownership and overwrite policy
- **AND** it does not merge the legacy tree or preserve its ancestry as a publication requirement

#### Scenario: Legacy superproject branch exists
- **WHEN** the publication remote contains `topic-workspace/main`
- **THEN** synchronization removes that ref under the approved snapshot replacement
- **AND** it does not retain a compatibility alias

#### Scenario: Remote default branch does not select main
- **WHEN** remote HEAD resolves to a branch other than `main`
- **THEN** publication reports that ordinary-clone readiness requires a provider default-branch update
- **AND** it performs that provider-specific mutation only through a separate explicit action

### Requirement: Publication Binding Grants Exclusive Git Snapshot Authority
The Publication Binding SHALL support an explicitly acknowledged `exclusive_snapshot` mode that dedicates the complete Git ref and tag namespace of one credential-safe remote to the current sanitized snapshot of one Research Topic and Topic Workspace.

#### Scenario: Exclusive snapshot mode is initialized
- **WHEN** the user explicitly acknowledges `exclusive_snapshot` mode for an exact remote, Research Topic, and Topic Workspace
- **THEN** the Publication Binding records the mode and binding identity without credentials
- **AND** it states that future approved syncs may force-replace or delete every Git ref and tag on that remote

#### Scenario: Later synchronization uses the binding
- **WHEN** a current content and privacy plan matches an existing exclusive-snapshot binding
- **THEN** synchronization may apply the complete planned ref and tag replacement without another branch-specific or tag-specific destructive approval
- **AND** the binding does not substitute for current content selection, privacy review, remote inventory, or stale-plan validation

#### Scenario: Binding identity changes
- **WHEN** the remote locator, normalized repository identity, Research Topic, Topic Workspace, or snapshot mode differs from the acknowledged binding
- **THEN** the exclusive-snapshot authority is invalid
- **AND** publication requires a new explicit acknowledgement before remote mutation

#### Scenario: Remote changes after planning
- **WHEN** any observed Git ref or tag differs from the fingerprint recorded by the current plan
- **THEN** synchronization stops and regenerates the complete snapshot plan
- **AND** it does not use persistent overwrite authority to apply stale state

#### Scenario: Provider data exists outside Git
- **WHEN** the remote provider stores issues, pull requests, releases, packages, access controls, repository settings, or other non-Git state
- **THEN** exclusive-snapshot authority does not mutate that state
- **AND** any provider-specific mutation requires its own applicable contract

## MODIFIED Requirements

### Requirement: Publication Plans Classify Every Source Path
The publish `plan` operation SHALL inventory every relevant Isomer-resolved semantic source surface, assign every considered path exactly one disposition of `track`, `template`, `exclude`, `component`, or `block`, record the semantic publication class that caused the disposition, and distinguish source-backed paths from generated publication paths.

#### Scenario: Publication plan records exact scope
- **WHEN** a plan is created
- **THEN** it records selected topic and workspace refs, safe Project-relative copy path, credential-safe remote, visibility acknowledgement, snapshot mode, canonical superproject branch, semantic content classes, entry origins, raw-byte settings, source and output fingerprints, relative mappings, dispositions, selected components and references, transformations, reserved generated paths, reproduction limitations, conflicts, the complete observed and expected Git ref and tag sets, remote HEAD observation, generated navigation fingerprints, expected commits, push order, blockers, and approval state
- **AND** it does not record secret values, sensitive excerpts, raw private diffs, source Git configuration, credential-bearing URLs, or publication-irrelevant absolute paths

#### Scenario: Required default surfaces exist
- **WHEN** planning encounters root environment declarations, the Topic Workspace Manifest, readiness summaries, intent, typed durable research records, topic-owned components, or registered GitHub reference repositories
- **THEN** it selects their sanitizable publication forms at their original Topic Workspace-relative paths by default
- **AND** it does not move them into a synthetic content-class directory

#### Scenario: Private and non-default surfaces exist
- **WHEN** planning encounters Workspace Runtime, `state.sqlite`, installed environments, caches, temporary material, credentials, downloaded raw-material bytes, or raw experiment-output bytes
- **THEN** it excludes or blocks those paths unless an applicable raw-byte class has an explicit current-plan selection
- **AND** it does not relocate retained siblings when applying those exclusions

#### Scenario: Risky material blocks publication
- **WHEN** planning encounters private keys, credential-like values, credential-bearing URLs, unsupported binaries, unsupported archives, excessive files, unresolved identity metadata, unresolved license or access posture, generated-path collisions, or content whose safe transformation cannot be established
- **THEN** it assigns `block`
- **AND** publish sync refuses the blocked scope

#### Scenario: Validated paper PDF is considered
- **WHEN** a checksummed paper PDF has accepted build and validation lineage and approved identity metadata
- **THEN** the planner treats it as a typed research output at its original Topic Workspace-relative Artifact path rather than an arbitrary unsupported binary
- **AND** size, signature, license, and privacy checks still apply

#### Scenario: Source-backed mapping is validated
- **WHEN** the plan contains a source-backed `track`, `template`, or `component` entry
- **THEN** its normalized output path equals its normalized source-relative path
- **AND** a mismatch blocks approval

#### Scenario: Generated mapping is validated
- **WHEN** the plan contains a generated entry
- **THEN** it has no false Source Topic Workspace path and uses only an approved reserved publication path
- **AND** its origin and fingerprint participate in stale-plan detection

### Requirement: Publication README Exposes the Latest Paper
The Topic Publication Copy SHALL always contain a root `README.md` with a stable latest-paper line, SHALL link an eligible paper at its path-preserved published Artifact location, and SHALL leave the Source Topic Workspace unchanged.

#### Scenario: Validated paper PDF exists
- **WHEN** one latest unambiguous checksummed paper PDF has accepted build and validation lineage and passes typed PDF privacy review
- **THEN** the projection publishes it at its original Topic Workspace-relative Artifact path
- **AND** `README.md` contains `Latest paper: [PDF](<path-preserved-artifact-path>)`

#### Scenario: Paper PDF is unavailable or ambiguous
- **WHEN** no eligible paper PDF exists or latest selection is ambiguous
- **THEN** `README.md` contains `Latest paper: not yet available.`
- **AND** the planner reports the absence or ambiguity without selecting by filename or modification time

#### Scenario: Prior paper revisions are safe
- **WHEN** prior checksummed paper PDF revisions are typed durable research outputs and pass size, license, and identity-metadata review
- **THEN** the plan may retain them at their original Topic Workspace-relative Artifact paths with their lineage by default
- **AND** the README still points only to the latest eligible revision

#### Scenario: Relocated latest-paper alias is proposed
- **WHEN** planning proposes a duplicate or relocated paper output such as `paper/latest.pdf`
- **THEN** validation rejects that mapping
- **AND** README generation links the selected path-preserved Artifact instead

### Requirement: Topic Main and Worktree Snapshots Become Sanitized Submodules
The Topic Publication Copy SHALL represent selected Topic Main, Topic Actor Workspace, and Agent Workspace projections as sanitized same-remote submodules backed by replaceable `components/...` snapshot branches at their resolved Topic Workspace-relative paths, SHALL record that actor and agent snapshots derive from the Topic Main Git anchor, and SHALL represent selected registered GitHub reference repositories as credential-free upstream submodules at their registered Topic Workspace-relative paths.

#### Scenario: Topic Main component is materialized
- **WHEN** Topic Main is selected for publication
- **THEN** its sanitized component repository uses publication branch `components/topic-main`
- **AND** superproject `main` records its exact commit at the resolved Topic Main relative path

#### Scenario: Topic Actor component is materialized
- **WHEN** Topic Actor `<name>` is selected for publication
- **THEN** the sanitized current tree of its Topic Main worktree uses publication branch `components/topic-actors/<sanitized-name>`
- **AND** superproject `main` records its exact commit at the actor's resolved relative workspace path

#### Scenario: Agent component is materialized
- **WHEN** Agent `<name>` is selected for publication
- **THEN** the sanitized current tree of its Topic Main worktree uses publication branch `components/agents/<sanitized-name>`
- **AND** superproject `main` records its exact commit at the agent's resolved relative workspace path

#### Scenario: Worktree relationship is represented without local Git control state
- **WHEN** a selected Topic Actor Workspace or Agent Workspace is a worktree of Topic Main
- **THEN** the Publication Projection Manifest records its component kind, sanitized name, resolved relative path, Topic Main anchor relationship, publication branch, and exact sanitized commit
- **AND** publication excludes its source `.git` file, worktree administration data, source object database, Git configuration, and local absolute paths

#### Scenario: Topic-owned components use the publication remote
- **WHEN** `.gitmodules` is generated for selected Topic Main, Topic Actor, or Agent components
- **THEN** each topic-owned component uses the credential-safe user-provided publication remote, names its deterministic `components/...` snapshot branch, and is pinned by a gitlink commit
- **AND** its gitlink path equals the component's resolved Topic Workspace-relative path

#### Scenario: Reference repository uses upstream
- **WHEN** `.gitmodules` is generated for a selected registered GitHub reference repository
- **THEN** the entry uses its normalized credential-free upstream locator and records its exact commit at its registered Topic Workspace-relative path
- **AND** it does not name a publication component branch, copy local source Git metadata, or relocate the reference by content class

#### Scenario: Recursive clone reports reproducibility
- **WHEN** a consumer clones `main` with submodules
- **THEN** every published topic-owned component commit is reachable from its named `components/...` branch in the publication remote
- **AND** every reference commit is either reachable from its recorded upstream for the intended audience or named in a recorded access limitation

#### Scenario: Published clone is not an operational Topic Workspace
- **WHEN** a consumer clones `main` with submodules
- **THEN** Topic Main, Topic Actor Workspace, and Agent Workspace paths contain inspectable ordinary submodule checkouts
- **AND** publication does not claim to restore Workspace Runtime, local worktree links, source branch ancestry, operational directory ownership, or a working Topic Workspace
- **AND** any later reconstruction of Topic Workspace directories, Artifacts, gitlinks, branches, or worktrees is manual and outside the publication contract

### Requirement: Publish Sync Fetches Before Normal or Forced Push
Publish sync SHALL inspect the complete remote state before mutation and SHALL replace the refs covered by the current approved snapshot policy with the exact sanitized current-state ref set without merging or preserving publication ancestry.

#### Scenario: Synchronization plans a complete snapshot
- **WHEN** publish sync prepares remote mutation
- **THEN** it fetches or otherwise observes `main`, every planned topic-owned component ref, legacy publication refs, tags, remote HEAD, and every additional ref covered by the remote ownership policy
- **AND** the plan records the exact expected post-synchronization ref set

#### Scenario: Existing snapshot differs
- **WHEN** a remote ref covered by the approved snapshot policy differs from the planned current-state ref or is obsolete
- **THEN** sync may force the planned exact ref or remove the obsolete covered ref
- **AND** an applicable exclusive-snapshot binding removes the need for another branch-specific or tag-specific destructive approval

#### Scenario: Remote changes after snapshot planning
- **WHEN** an observed covered remote ref differs from the ref recorded in the approved snapshot plan
- **THEN** sync treats the plan as stale and performs no mutation
- **AND** it observes the current remote again and regenerates the complete replacement plan

#### Scenario: Components push before superproject
- **WHEN** an approved synchronization contains component and superproject changes
- **THEN** sync commits and pushes selected component branches first
- **AND** it updates exact gitlinks and reserved publication metadata before pushing `main` last

#### Scenario: Partial push remains resumable
- **WHEN** a component push succeeds and a later component or `main` push fails
- **THEN** sync records per-branch outcomes and a safe resume point
- **AND** the previously published `main` remains the authoritative complete version

#### Scenario: Snapshot replacement completes
- **WHEN** every planned component ref and `main` matches the approved commits and every obsolete covered ref is absent
- **THEN** sync verifies the complete ref set and a clean recursive clone of `main`
- **AND** it reports only the current snapshot as the publication result
