## ADDED Requirements

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
Each publication plan SHALL select every currently available Topic Main, registered Topic Actor Workspace, and selected-team Agent Workspace resolved through read-only Isomer queries unless the user explicitly excludes a component in that plan.

#### Scenario: All current components are available
- **WHEN** Topic Main, two registered Topic Actor Workspaces, and three selected-team Agent Workspaces resolve and exist
- **THEN** the publication plan selects all six components by default
- **AND** each component remains subject to path classification, sanitization, privacy review, and current-plan approval

#### Scenario: Publication runs before components exist
- **WHEN** no component workspace is available after Topic Workspace registration
- **THEN** the plan may produce a root-only publication
- **AND** it reports unavailable expected topology without scanning directories or blocking solely because later lifecycle stages have not run

#### Scenario: Component becomes available later
- **WHEN** a Topic Main, registered Topic Actor Workspace, or selected-team Agent Workspace becomes available after an earlier plan or synchronization
- **THEN** the next plan selects it by default and treats the topology change as stale relative to the earlier plan
- **AND** publish sync requires renewed privacy review and approval before committing or pushing that component

#### Scenario: User excludes an available component
- **WHEN** the user explicitly excludes an available component in the current publication plan
- **THEN** the plan records that exclusion and omits the component from the current projection
- **AND** the exclusion does not delete or mutate the source workspace

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

### Requirement: Publication Never Copies Source Git Metadata or History
The publication projection SHALL materialize fresh sanitized histories and SHALL exclude all Source Topic Workspace and nested workspace Git metadata and history.

#### Scenario: Source Git control paths are encountered
- **WHEN** projection inventory encounters a `.git` directory, `.git` worktree file, Git config, objects, refs, reflogs, index, worktree administration data, credential helper data, or source remote
- **THEN** it excludes that material from every publication file copy and commit

#### Scenario: Source commit contains deleted secret
- **WHEN** source history may contain content that is absent from the current working tree
- **THEN** publication does not reuse, import, fetch, bundle, or push that source history

#### Scenario: Sanitized component history is fresh
- **WHEN** a publication component is initialized
- **THEN** its commits contain only approved sanitized projection content and publication metadata

### Requirement: Publication Plans Classify Every Source Path
The publish `plan` operation SHALL create a sanitized state-bound plan in which every considered source path has exactly one disposition: `track`, `template`, `exclude`, `component`, or `block`.

#### Scenario: Publication plan records exact scope
- **WHEN** a plan is created
- **THEN** it records selected topic and workspace refs, safe Project-relative copy path, credential-safe remote, visibility acknowledgement, source and output fingerprints, relative mappings, dispositions, selected components, transformations, conflicts, expected commits, push order, blockers, and approval state
- **AND** it does not record secret values, sensitive excerpts, raw private diffs, source Git configuration, credential-bearing URLs, or publication-irrelevant absolute paths

#### Scenario: Known private surfaces default to exclusion
- **WHEN** planning encounters Workspace Runtime, `state.sqlite`, local environments, caches, logs, tmp, credentials, canonical external repositories, or unapproved records
- **THEN** it assigns `exclude` or `block`

#### Scenario: Risky material blocks publication
- **WHEN** planning encounters private keys, credential-like values, credential-bearing URLs, unsupported binaries, unsupported archives, excessive files, or content whose safe transformation cannot be established
- **THEN** it assigns `block`
- **AND** publish sync refuses the blocked scope

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

### Requirement: Nested Workspaces Become Sanitized Submodules
The Topic Publication Copy SHALL represent default-selected and explicitly retained Topic Main, Topic Actor Workspace, and Agent Workspace projections as submodules of the sanitized superproject.

#### Scenario: Topic Main component is materialized
- **WHEN** Topic Main is selected for publication
- **THEN** its sanitized component repository uses publication branch `topic-owner/main`
- **AND** the superproject records its exact commit at the resolved Topic Main relative path

#### Scenario: Topic Actor component is materialized
- **WHEN** Topic Actor `<name>` is selected for publication
- **THEN** its sanitized component repository uses publication branch `per-topic-actor/<name>/main`
- **AND** the superproject records its exact commit at the actor's relative workspace path

#### Scenario: Agent component is materialized
- **WHEN** Agent `<name>` is selected for publication
- **THEN** its sanitized component repository uses publication branch `per-agent/<name>/main`
- **AND** the superproject records its exact commit at the agent's relative workspace path

#### Scenario: One remote backs every submodule
- **WHEN** `.gitmodules` is generated
- **THEN** every selected component uses the same credential-safe user-provided remote URL, names its deterministic component branch, and is pinned by a gitlink commit

#### Scenario: Recursive clone reproduces the publication
- **WHEN** a consumer clones `topic-workspace/main` with submodules
- **THEN** every published component commit is reachable from its named branch in the same remote and checks out at the recorded path

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
Publish sync SHALL fetch before mutation, use normal pushes for absent or compatible publication branches, and use plain `--force` only for exact incompatible branch replacements named in a fresh destructive-change plan with separate explicit user permission.

#### Scenario: Remote divergence without permission blocks synchronization
- **WHEN** a superproject or component publication branch has unexpected remote commits, divergence, or requires force and no current force-push permission covers it
- **THEN** sync reports the branch blocker
- **AND** it does not pull, merge, rebase, reset, rewrite history, or force-push

#### Scenario: User approves an incompatible branch replacement
- **WHEN** a fresh destructive-change plan identifies an incompatible deterministic publication branch, its observed remote commit, exact replacement commit, displaced commits, and push order and the user explicitly approves that replacement
- **THEN** sync may use plain `--force` for that named branch and exact replacement commit
- **AND** it does not force any unlisted branch or use `--all`, `--mirror`, or remote branch deletion

#### Scenario: Remote changes after force approval
- **WHEN** an observed remote ref differs from the ref recorded in the approved destructive-change plan
- **THEN** sync treats the force permission as stale and performs no push
- **AND** it fetches and requires a new plan, warning, and explicit permission

#### Scenario: Components push before superproject
- **WHEN** an approved synchronization contains component and superproject changes
- **THEN** sync commits and pushes selected component branches first
- **AND** it updates submodule gitlinks, projection manifest, and `topic-workspace-version.toml` before pushing `topic-workspace/main` last

#### Scenario: Partial push remains resumable
- **WHEN** a component push succeeds and a later component or superproject push fails
- **THEN** sync records per-branch outcomes and a safe resume point
- **AND** the previously published `topic-workspace/main` remains the authoritative complete version

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
