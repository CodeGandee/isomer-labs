# topic-workspace-git-publication Specification

## Purpose
TBD - created by archiving change add-topic-workspace-git-management. Update Purpose after archive.
## Requirements
### Requirement: Publication Is Available After Topic Workspace Registration
The publication layer SHALL allow publish init, plan, and sync after Research Topic and Topic Workspace registration without requiring Workspace Runtime or any later Topic Creator stage.

#### Scenario: Publication begins before runtime
- **WHEN** the selected Research Topic and Source Topic Workspace are registered and Workspace Runtime is missing
- **THEN** the workflow may prepare, approve, and push a sanitized publication through the Topic Publication Copy
- **AND** it does not initialize Workspace Runtime or write `state.sqlite`

#### Scenario: Later-stage component is unavailable
- **WHEN** Topic Main, a Topic Actor Workspace, or an Agent Workspace has not been created at the current lifecycle stage
- **THEN** the publication plan reports that component as unavailable
- **AND** it does not infer or fabricate the component from directory names

#### Scenario: Pre-runtime state stays local to the copy
- **WHEN** publication runs before Workspace Runtime exists
- **THEN** its binding, plan, conflict, and outcome state remains in an ignored Topic Publication Copy support root that is excluded from publication commits
- **AND** successfully pushed sanitized manifests may support later reconstruction when the remote is supplied again

### Requirement: Publication Selects All Available Components by Default
Each publication plan SHALL select every currently available Topic Main, registered Topic Actor Workspace, selected-team Agent Workspace, and registered GitHub reference repository resolved through read-only Isomer queries unless the user explicitly excludes that component or reference in the current plan.

#### Scenario: All current topic-owned components are available
- **WHEN** Topic Main, two registered Topic Actor Workspaces, and three selected-team Agent Workspaces resolve and exist
- **THEN** the publication plan selects all six topic-owned components by default
- **AND** each component remains subject to semantic classification, sanitization, privacy review, and current-plan approval

#### Scenario: Registered reference repositories are available
- **WHEN** canonical external repositories have registered credential-free GitHub locators and exact commits
- **THEN** the plan selects them as reference-repository submodules by default
- **AND** it records access, reachability, and license posture without copying their local checkout metadata

#### Scenario: Publication runs before components exist
- **WHEN** no topic-owned component workspace is available after Topic Workspace registration
- **THEN** the plan may produce a root-only publication with any independently registered reference repositories
- **AND** it reports unavailable expected topology without scanning directories or blocking solely because later lifecycle stages have not run

#### Scenario: Component or reference becomes available later
- **WHEN** a Topic Main, registered Topic Actor Workspace, selected-team Agent Workspace, or registered GitHub reference becomes available after an earlier plan or synchronization
- **THEN** the next plan selects it by default and treats the topology change as stale relative to the earlier plan
- **AND** publish sync requires renewed privacy and remote-mutation approval

#### Scenario: User excludes an available component or reference
- **WHEN** the user explicitly excludes an available component or reference in the current Publication Plan
- **THEN** the plan records that exclusion and omits it from the current projection
- **AND** the exclusion does not delete or mutate the Source Topic Workspace or canonical external repository

### Requirement: Remote Publication Is Independently Opt-In
The publication layer SHALL operate without requiring or enabling in-workspace local Git tracking.

#### Scenario: Publication begins without local tracking
- **WHEN** a user supplies a remote and approves `publish init` for a Source Topic Workspace whose root is not a Git repository
- **THEN** the workflow prepares the publication binding and Topic Publication Copy
- **AND** it does not initialize a Git repository in the Source Topic Workspace

#### Scenario: Local uncommitted content is eligible for review
- **WHEN** a Source Topic Workspace has local tracking with uncommitted or untracked root files
- **THEN** publication inventories the current filesystem and includes relevant paths in the publication plan
- **AND** it does not restrict publication to local commits

#### Scenario: Publication never commits local root state
- **WHEN** publish init, plan, or sync runs
- **THEN** it does not stage, commit, reset, clean, or configure the Source Topic Workspace root repository

### Requirement: Topic Publication Copy Is a Disposable Projection
The system SHALL treat the Topic Publication Copy as an ignored, Project-local, rebuildable projection rather than a canonical Topic Workspace or durable record authority.

#### Scenario: Publication copy has no canonical authority
- **WHEN** downstream code or guidance inspects a Topic Publication Copy
- **THEN** it does not treat the copy as a registered Topic Workspace, Workspace Runtime, Artifact Library, canonical external repository, or research record source

#### Scenario: Missing copy is recoverable
- **WHEN** a previously synchronized Topic Publication Copy is missing and a runtime binding exists or the user supplies the remote again
- **THEN** publication status reports `copy-missing`
- **AND** publish sync may reconstruct it from the publication binding, fetched remote branches, and sanitized manifests before comparing current source content

### Requirement: Publication Copy Uses Ignored Project Temporary Storage
The publication layer SHALL resolve a safe effectively ignored path under the Project root before creating a Topic Publication Copy.

#### Scenario: Existing ignored tmp is selected
- **WHEN** Project-root `tmp/` exists and effective Git ignore evidence marks it ignored
- **THEN** the default copy path is `<project-root>/tmp/topic-workspace-publish/<topic-id>/`

#### Scenario: Existing ignored temp is selected
- **WHEN** Project-root `tmp/` is unavailable and Project-root `temp/` exists and is effectively ignored
- **THEN** the default copy path is `<project-root>/temp/topic-workspace-publish/<topic-id>/`

#### Scenario: Declared ignored directory need not preexist
- **WHEN** `tmp/` or `temp/` is declared effectively ignored but the directory does not exist
- **THEN** publish init may create the selected directory after approval

#### Scenario: No temporary ignore policy exists
- **WHEN** neither Project-root `tmp/` nor `temp/` is effectively ignored
- **THEN** publish init plans an Isomer-managed `tmp/` entry in the Project-root `.gitignore` and creation of Project-root `tmp/`
- **AND** it preserves user-authored ignore rules outside the managed block

#### Scenario: Unsafe destination is rejected
- **WHEN** a default or custom copy path escapes the Project root or falls inside the Source Topic Workspace, Project Config Directory, generated content root, Houmao state, or a canonical repository
- **THEN** publication reports a blocker and creates no directory

### Requirement: Default Publication Preserves the Reproduction Graph
The publication layer SHALL select current intent, reproducible environment declarations, and every sanitizable typed durable research record needed to inspect evidence and reconstruct material decisions by default.

#### Scenario: Survey decision lineage exists
- **WHEN** the Source Topic Workspace contains current, superseded, rejected, failed, blocked, or accepted typed durable records linked by revision, evidence, decision, or provenance relationships
- **THEN** the publication plan selects their sanitizable structured content and relationships by default
- **AND** it does not reduce the publication to only the latest accepted outputs

#### Scenario: Reproducible environment declarations exist
- **WHEN** the Topic Workspace contains a manifest, Pixi declarations and lock, setup specifications, environment Gate records, or exact software and hardware observations
- **THEN** the plan selects the sanitizable declarations and reproducibility-relevant versions by default
- **AND** it excludes installed environments, caches, hardware serials, Workspace Runtime, and credentials

#### Scenario: Runtime database carries record state
- **WHEN** readers need a portable view of the published research lineage
- **THEN** the projection generates a sanitized research-record index with stable refs, semantic ids, revisions, states, fingerprints, and relationships
- **AND** it does not publish `state.sqlite`, runtime-only fields, absolute paths, or treat the index as canonical state

### Requirement: Raw Payload Bytes Require Explicit Selection
The publication layer SHALL distinguish default material and execution provenance from non-default raw payload bytes and SHALL include raw payload bytes only through explicit settings in the current approved Publication Plan.

#### Scenario: Downloaded material was used
- **WHEN** research records identify a downloaded paper, copied source tree, dataset, model, or related raw material
- **THEN** the default publication includes its sanitizable exact locator, version or digest, retrieval observation, access posture, license posture, and evidence relationships
- **AND** it excludes the downloaded bytes unless the plan explicitly selects raw material bytes

#### Scenario: Experiment produced raw outputs
- **WHEN** a trial or comparison produced profiler reports, raw logs, generated dataset bytes, dumps, checkpoints, or other raw execution outputs
- **THEN** the default publication includes sanitizable plans, commands, environment identity, normalized results, checksums, verdicts, and limitations
- **AND** it excludes the raw output bytes unless the plan explicitly selects raw experiment-output bytes

#### Scenario: Explicit raw-byte setting changes
- **WHEN** a raw material or raw experiment-output selection differs from the approved Publication Plan
- **THEN** the plan is stale
- **AND** synchronization requires renewed privacy, access, license, size, and remote-mutation review

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

### Requirement: Publication Protects Individual Identity Without Erasing Organization Provenance
The publication layer SHALL sanitize individual researcher, machine-local, network-local, and credential information while preserving credential-free organization, citation, and source provenance.

#### Scenario: Local individual identity appears
- **WHEN** content contains a local username, home path, local Git author or email, personal contact field, workstation hostname or IP address, identity-bearing actor or agent name, or hardware serial
- **THEN** the projection replaces it with an approved stable placeholder or blocks publication when safe transformation is unavailable
- **AND** source content remains unchanged

#### Scenario: GitHub repository identity appears
- **WHEN** content contains a normalized credential-free public or private GitHub repository locator, organization or owner segment, repository name, and immutable commit
- **THEN** publication preserves that repository identity as organization or source provenance
- **AND** it does not classify the owner segment as an individual-identity leak merely because it resembles a username

#### Scenario: Repository locator carries authentication
- **WHEN** a repository locator contains an embedded username, password, token, signed query, credential parameter, or fragment
- **THEN** publication blocks the locator until it is normalized to a credential-free form
- **AND** no credential-bearing value enters a plan, manifest, Git argument, generated file, or diagnostic

#### Scenario: Private repository limits access
- **WHEN** a preserved private GitHub reference is unavailable to part of the intended audience
- **THEN** the publication records an explicit access and reproduction limitation
- **AND** it does not copy private repository bytes by default or claim complete reproduction

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

### Requirement: Publication Never Copies Source Git Metadata or History
The publication projection SHALL materialize fresh sanitized histories for topic-owned content, SHALL exclude Source Topic Workspace and topic-owned component Git control data, and SHALL represent registered GitHub references only through credential-free upstream submodules pinned to exact commits.

#### Scenario: Topic-owned Git control paths are encountered
- **WHEN** projection inventory encounters a `.git` directory, `.git` worktree file, Git config, objects, refs, reflogs, index, worktree administration data, credential helper data, or incidental source remote
- **THEN** it excludes that material from every topic-owned publication file copy and commit

#### Scenario: Topic-owned source commit contains a deleted secret
- **WHEN** topic-owned source history may contain content that is absent from the current working tree
- **THEN** publication does not reuse, import, fetch, bundle, or push that source history

#### Scenario: Sanitized topic-owned component history is fresh
- **WHEN** a topic-owned publication component is initialized
- **THEN** its commits contain only approved sanitized projection content and publication metadata

#### Scenario: Registered GitHub reference is selected
- **WHEN** a canonical external repository has an approved credential-free GitHub locator and exact commit
- **THEN** the superproject records an upstream submodule pinned to that commit
- **AND** it does not copy the local checkout or reinterpret upstream history as topic-owned publication history

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

### Requirement: Sanitization Preserves the Source Workspace
Publication materialization SHALL create templates or sanitized derived outputs only in the Topic Publication Copy and SHALL leave canonical source files unchanged.

#### Scenario: Structured sensitive file becomes a template
- **WHEN** an approved plan assigns `template` to a supported structured source file
- **THEN** the projection creates the approved output with sensitive fields replaced by descriptive placeholders
- **AND** it does not edit, rename, or delete the source file

#### Scenario: Unsupported masking is blocked
- **WHEN** a binary or unsupported format would require content masking
- **THEN** projection leaves source and destination unchanged and reports a blocker

#### Scenario: Resulting content is rescanned
- **WHEN** projection files and component worktrees have been materialized
- **THEN** the workflow rescans every file eligible for a publication commit
- **AND** it blocks content that fails the privacy rules without deleting source material

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

### Requirement: Publish Init Prepares but Does Not Push
The `publish init` operation SHALL create or validate local publication preparation state without mutating the remote.

#### Scenario: Initial publication binding is prepared
- **WHEN** the user supplies a credential-safe remote, visibility acknowledgement, and approved destination plan
- **THEN** publish init records the binding in Workspace Runtime support state when available or the ignored Topic Publication Copy support root otherwise, prepares the ignored copy root, and may materialize sanitized superproject and available component repositories
- **AND** it performs no remote push

#### Scenario: Unknown visibility blocks preparation for push
- **WHEN** remote visibility is `unknown`
- **THEN** the binding may be inspected locally but publish sync reports a blocker until the user selects `private`, `restricted`, or `public`

### Requirement: Publish Sync Compares Source Copy Manifest and Remote
The `publish sync` operation SHALL compare the current Source Topic Workspace, expected sanitized projection, last projection manifest, current Topic Publication Copy, and fetched remote state before applying changes.

#### Scenario: Unchanged generated output is updated safely
- **WHEN** source content changes and the corresponding destination output still matches the last generated fingerprint
- **THEN** sync may replace the destination with the newly approved sanitized output

#### Scenario: Destination-only edit conflicts with source change
- **WHEN** a destination output changed after the last projection and its source also changed
- **THEN** sync reports a conflict and overwrites neither side without an explicit conflict decision

#### Scenario: Source deletion removes unchanged output
- **WHEN** a source path was removed and its destination output still matches the last generated fingerprint
- **THEN** sync may remove the output from the publication copy after approval

#### Scenario: Source deletion preserves edited output
- **WHEN** a source path was removed but its destination output changed after the last projection
- **THEN** sync reports a conflict and does not delete the destination output

#### Scenario: Local Git commit state is not publication authority
- **WHEN** the source root has local tracking
- **THEN** comparison uses current relevant filesystem content rather than only HEAD, the index, or tracked files

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

### Requirement: Publication Credentials Stay External
Publication operations SHALL use existing Git authentication mechanisms and SHALL keep credentials out of Git arguments, plans, manifests, generated content, and output.

#### Scenario: Credential-bearing remote is rejected
- **WHEN** a supplied remote URL contains embedded credentials, signed query parameters, or a fragment
- **THEN** publication reports a blocker and does not store, configure, or contact that URL

#### Scenario: Credential-safe remote is reported
- **WHEN** a remote is shown in status or plan output
- **THEN** the output contains only a credential-safe locator and remote name

### Requirement: Publication Mutations Reject Stale Plans
Each publication mutation SHALL recalculate the source, copy, binding, component, and remote state relevant to its approved plan.

#### Scenario: Publication state changed after approval
- **WHEN** relevant source content, expected output, current copy content, component HEAD, superproject HEAD, binding identity, or fetched remote state differs from the approved plan
- **THEN** publish sync reports the plan as stale or conflicted and performs no unapproved mutation

#### Scenario: Local root commit changes without filesystem change
- **WHEN** only local root Git history changes and publication-relevant filesystem content remains identical
- **THEN** the publication plan remains valid
