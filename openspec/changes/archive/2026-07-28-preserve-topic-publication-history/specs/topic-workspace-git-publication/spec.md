## ADDED Requirements

### Requirement: Publication Plans Select History-Aware Ref Strategies
The publication plan SHALL classify every expected topic-owned branch as `no-op`, `create`, `fast-forward`, or `force-replacement`, SHALL classify obsolete covered refs separately as exact deletions, and SHALL bind each mutation strategy to the freshly observed remote state.

#### Scenario: Planned ref already matches
- **WHEN** an expected topic-owned branch already resolves to the exact approved sanitized commit
- **THEN** the plan classifies that branch as `no-op`
- **AND** synchronization creates no redundant commit and performs no update push for that branch

#### Scenario: Planned ref is absent
- **WHEN** an expected topic-owned branch is absent from the freshly observed remote
- **THEN** the plan classifies that branch as `create`
- **AND** synchronization may publish one fresh parentless sanitized commit through an exact non-force refspec

#### Scenario: Prior publication is history compatible
- **WHEN** an expected topic-owned branch resolves to a prior publication commit whose binding, tracked metadata, canonical topology, pinned component relationship, and privacy posture remain compatible
- **THEN** the plan classifies the branch as `fast-forward`
- **AND** it records the observed commit as the required direct parent of the planned sanitized delta commit

#### Scenario: Prior publication is history incompatible
- **WHEN** the prior publication has an unsupported or mismatched layout, binding, tracked manifest, component relationship, ancestry, or history-retention posture
- **THEN** the plan classifies every affected branch as `force-replacement` or blocks when fallback authority is unavailable
- **AND** it records the exact incompatibility reason and the observed commit protected by the replacement lease

#### Scenario: Prior published content requires withdrawal from history
- **WHEN** a credential, identity, privacy, license, or explicit withdrawal decision requires prior published content to become unreachable
- **THEN** the plan treats the affected publication lineage as history incompatible
- **AND** the fallback scope includes canonical `main` whenever retained superproject ancestry would continue to reference the withdrawn component or content

#### Scenario: Destination conflict is not structural incompatibility
- **WHEN** the current Topic Publication Copy contains a destination-only or simultaneous edit that the projection comparison cannot safely resolve
- **THEN** the plan reports a conflict and blocks mutation
- **AND** it does not select force replacement merely to bypass the unresolved edit

#### Scenario: Ref strategy is persisted
- **WHEN** a publication plan or outcome is written
- **THEN** it records the strategy, observed commit, required base, planned or resulting commit, compatibility evidence, and fallback reason for each applicable ref
- **AND** plan fingerprints include those values so a changed remote or strategy stales approval

## MODIFIED Requirements

### Requirement: Publication Never Copies Source Git Metadata or History
The publication projection SHALL initialize topic-owned publication histories from approved sanitized content without Source Topic Workspace ancestry, SHALL permit later commits to extend only compatible sanitized publication history, SHALL exclude Source Topic Workspace and topic-owned component Git control data, and SHALL represent registered GitHub references only through credential-free upstream submodules pinned to exact commits.

#### Scenario: Topic-owned Git control paths are encountered
- **WHEN** projection inventory encounters a `.git` directory, `.git` worktree file, Git config, objects, refs, reflogs, index, worktree administration data, credential helper data, or incidental source remote
- **THEN** it excludes that material from every topic-owned publication file copy and commit

#### Scenario: Topic-owned source commit contains a deleted secret
- **WHEN** topic-owned source history may contain content that is absent from the current working tree
- **THEN** publication does not reuse, import, fetch, bundle, or push that source history

#### Scenario: Sanitized topic-owned component history is initialized
- **WHEN** a topic-owned publication component branch has no compatible prior publication commit
- **THEN** its initial commit contains only approved sanitized projection content and publication metadata
- **AND** it has no Source Topic Workspace commit as an ancestor

#### Scenario: Sanitized publication history is extended
- **WHEN** a prior topic-owned publication commit is history compatible and the newly approved sanitized projection differs
- **THEN** the new publication commit uses the observed prior publication commit as its direct parent
- **AND** the resulting ancestry contains only prior approved sanitized publication commits rather than Source Topic Workspace history

#### Scenario: Registered GitHub reference is selected
- **WHEN** a canonical external repository has an approved credential-free GitHub locator and exact commit
- **THEN** the superproject records an upstream submodule pinned to that commit
- **AND** it does not copy the local checkout or reinterpret upstream history as topic-owned publication history

### Requirement: Publish Sync Fetches Before Normal or Forced Push
Publish sync SHALL inspect the complete remote state before mutation, SHALL preserve compatible sanitized publication ancestry through exact fast-forward updates, and SHALL use exact force replacement only when the current approved plan identifies history incompatibility covered by matching `exclusive_snapshot` fallback authority.

#### Scenario: Synchronization plans a complete snapshot
- **WHEN** publish sync prepares remote mutation
- **THEN** it fetches or otherwise observes `main`, every planned topic-owned component ref, legacy publication refs, tags, remote HEAD, and every additional ref covered by the remote ownership policy
- **AND** the plan records the exact expected post-synchronization ref set and one history-aware strategy for every expected branch

#### Scenario: Existing compatible snapshot differs
- **WHEN** a covered remote ref is a valid prior sanitized publication commit and the newly approved projection differs
- **THEN** sync materializes one direct-child sanitized delta commit and pushes it through an exact non-force refspec
- **AND** it verifies that the observed remote commit is the planned commit's direct parent immediately before push

#### Scenario: Existing snapshot already matches
- **WHEN** every expected topic-owned ref and tracked superproject output already matches the approved projection
- **THEN** sync records a no-op outcome without creating a new plan-only metadata commit
- **AND** it performs no branch update push

#### Scenario: Missing publication copy is recoverable
- **WHEN** the Topic Publication Copy is missing but the binding and observed remote publication are history compatible
- **THEN** sync recovers disposable projection state from canonical `main` and the exact pinned component refs
- **AND** it remains eligible for fast-forward publication rather than selecting force replacement because the local copy was absent

#### Scenario: Existing local copy cannot prove the observed base
- **WHEN** a retained Topic Publication Copy or sanitized component repository is dirty, divergent, or not based on the freshly observed remote commit
- **THEN** sync preserves the local state and reports a blocker or uses a separately validated disposable recovery location
- **AND** it does not merge, rebase, reset, clean, or select force replacement solely because the local preparation state is unusable

#### Scenario: Existing snapshot is history incompatible
- **WHEN** a covered remote ref cannot safely serve as a publication-history base and the approved plan records exact fallback scope
- **THEN** sync creates the approved fresh sanitized replacement and pushes it with branch-scoped force-with-lease against the exact observed commit
- **AND** matching `exclusive_snapshot` authority permits that fallback without making force replacement the default strategy

#### Scenario: Remote changes after planning
- **WHEN** an observed covered remote ref differs from the ref recorded in the approved publication plan
- **THEN** sync treats the plan as stale and performs no mutation
- **AND** it observes the current remote again and regenerates the complete history-aware plan

#### Scenario: Components push before superproject
- **WHEN** an approved synchronization contains component and superproject changes
- **THEN** sync commits and pushes selected component branches first using each planned strategy
- **AND** it updates exact gitlinks and reserved publication metadata before pushing `main` last

#### Scenario: Partial push remains resumable
- **WHEN** a component push succeeds and a later component or `main` push fails
- **THEN** sync records per-ref strategy and outcome plus a safe resume point
- **AND** the previously published `main` remains the authoritative complete version until the planned `main` update succeeds

#### Scenario: Synchronization completes
- **WHEN** every planned component ref and `main` matches the approved commits and every obsolete covered ref is absent
- **THEN** sync verifies the complete ref set, expected parent relationships, and a clean recursive clone of `main`
- **AND** it reports the current snapshot together with the preserved sanitized publication-history relationship or exact fallback outcome
