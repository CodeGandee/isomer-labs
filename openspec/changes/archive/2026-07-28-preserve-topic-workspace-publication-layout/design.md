## Context

The reproduction-first publication change expanded the default content set but did not make path preservation normative. The projection model can record independent source and output paths, the operator guidance permits generated mappings, and the first full publication moved Topic Workspace root files into a synthetic `environment/` directory. The same publication also treated `topic-workspace/main` as the superproject branch and later created remote `main` directly from `topic-owner/main`, which exposes Topic Main content at the repository root instead of at the resolved `repos/topic-main` path.

The canonical domain model defines a Topic Workspace as the owner of root environment declarations, intent, records, Topic Main, Topic Actor Workspaces, Agent Workspaces, runtime support, and disposable local surfaces. A Topic Publication Copy is a disposable sanitized projection of that Topic Workspace. Readers therefore need the publication tree to preserve the Topic Workspace's relative path contract even when policy excludes private or raw paths.

The existing projection inventory already emits identical source and output paths for ordinary discovered files. The missing controls are a normative invariant, generated-entry separation, branch topology, collision handling, migration rules, and end-to-end tests that prevent a planner or operator from inventing a new taxonomy.

## Goals / Non-Goals

**Goals:**

- Make remote `main` the current sanitized, path-preserving representation of the complete publishable Topic Workspace.
- Preserve the exact relative path of every retained source-backed file, directory component, and registered reference.
- Keep Topic Main and selected Topic Actor Workspace and Agent Workspace worktree snapshots as fresh sanitized same-remote `components/...` branches mounted through gitlinks at their resolved Topic Workspace-relative paths.
- Record each selected actor or agent snapshot's declarative relationship to the Topic Main Git anchor without copying local Git worktree control state.
- Keep publication-only control data separate from Source Topic Workspace content.
- Preserve reproduction-first defaults, durable record lineage, raw-byte opt-ins, contextual identity sanitization, and neutral publication authorship.
- Persist one-time exclusive-snapshot authority while keeping content selection, privacy, complete remote inventory, and stale-plan validation current for every sync.
- Define safe whole-snapshot replacement and Topic Publication Copy recovery behavior for old synthetic projections, component-root `main` branches, and legacy publication refs.

**Non-Goals:**

- Reproducing excluded Workspace Runtime, `state.sqlite`, installed environments, caches, local temporary surfaces, credentials, raw downloads, or raw experiment outputs.
- Preserving empty directories that contain no published file or gitlink, because Git does not represent empty directories.
- Reusing Source Topic Workspace or component Git ancestry.
- Preserving publication commit ancestry or using the publication remote as a rollback archive.
- Treating the Topic Publication Copy as canonical Topic Workspace state.
- Using publication as a Topic Workspace backup or automatically reconstructing an operational Topic Workspace, Workspace Runtime, directory ownership, Artifact placement, branch bindings, or local worktrees.

## Decisions

### Enforce a source-path identity invariant

Every source-backed `track`, `template`, or `component` entry will use the normalized Topic Workspace-relative source path as its output path. A `template` transformation may replace sensitive bytes but may not rename or relocate the file. An `exclude` entry has no output path, and exclusion of one path never changes a retained sibling's location. A `block` entry prevents synchronization.

Projection validation will reject a source-backed entry when `output_relative_path != source_relative_path`. The Publication Plan and Publication Projection Manifest will distinguish `source` entries from `generated` entries so publication-only files cannot bypass the invariant by pretending to be Source Topic Workspace paths.

Alternative: permit reviewed arbitrary mappings. Rejected because reviewed remapping still produces a repository whose path contract differs from the Topic Workspace and makes reproduction commands, links, and decisions harder to trace.

### Define structural fidelity as a path-preserving subset

The publication tree will preserve paths for included content but will omit policy-excluded content. It will not create placeholders for `.pixi/`, Workspace Runtime, `state.sqlite`, local tmp, credentials, or non-selected raw bytes. The manifest records sanitized exclusion classes and limitations without relocating neighboring content.

Alternative: reproduce every source directory with placeholders. Rejected because Git does not track empty directories, private path names can themselves disclose information, and placeholders can falsely imply that excluded content is available.

### Reserve one publication metadata overlay

Tracked publication-only metadata will live under `.isomer-publication/`, including the portable research-record index, projection manifest, and version manifest. Root `README.md` and `.gitmodules` are the only generated root exceptions. Copy-local binding, plan, outcome, and authentication-adjacent support state remains under the ignored `.isomer/` support root and never enters a commit.

If the Source Topic Workspace already contains `.isomer-publication/` or a root `.gitmodules` whose semantics conflict with the generated topology, planning blocks until an explicit design changes the reserved path or resolves the collision. The publication copy will use repository-local Git exclusions for `.isomer/`; it will not replace or relocate the Source Topic Workspace `.gitignore`.

Alternative: keep publication manifests at the repository root. Rejected because several generated root files obscure whether the repository mirrors the Topic Workspace and can collide with future topic-owned files.

### Compose the root README without moving source content

When the Source Topic Workspace has a `README.md`, publication will sanitize it in place and deterministically add or replace an Isomer publication navigation block. When it has no `README.md`, publication generates one. The README links the preserved intent, environment, record, component, and publication metadata paths.

The latest eligible paper PDF remains at its original Topic Workspace-relative Artifact path. The README's stable latest-paper line links that path. Publication does not create a relocated `paper/latest.pdf` duplicate. If no eligible PDF exists, the line remains `Latest paper: not yet available.`

Alternative: create a stable duplicate at `paper/latest.pdf`. Rejected because it breaks the source-path identity rule, duplicates binary content, and obscures the exact Artifact revision that the reader is opening.

### Publish only the current superproject snapshot on `main`

Remote `main` will contain the sanitized Topic Workspace superproject. Topic Main and selected Topic Actor Workspace and Agent Workspace snapshots appear only as gitlinks at their resolved Topic Workspace-relative paths and use the same publication remote. Registered GitHub references use their normalized upstream locators and exact commits at their registered Topic Workspace-relative paths.

The publication remote represents current state rather than publication history. Synchronization may replace prior publication commits with fresh neutral snapshot commits, and it removes the legacy `topic-workspace/main` ref instead of retaining a compatibility alias. Correctness comes from the complete verified tree, manifest, and exact gitlinks rather than ancestry.

Remote HEAD should select `main` so a normal clone opens the Topic Workspace tree. Because hosted default-branch mutation is provider-specific, publication reports the observed remote HEAD and performs a provider-supported update only through a separate explicit action. A successful Git push does not silently claim that remote HEAD changed.

Alternative: retain a same-commit `topic-workspace/main` alias. Rejected because compatibility history is not a publication goal and an extra superproject ref creates synchronization and privacy surface without reproduction value.

### Use a dedicated same-remote component namespace

Topic Main is the source Git anchor for Topic Actor Workspace and Agent Workspace worktrees. Publication will not copy their `.git` files, source object database, worktree administration directories, source configuration, or local absolute paths. It instead makes the sanitized current tree of Topic Main and each selected worktree reachable from replaceable branches named `components/topic-main`, `components/topic-actors/<sanitized-name>`, and `components/agents/<sanitized-name>`.

Every topic-owned `.gitmodules` entry uses the same publication remote, and the Publication Projection Manifest records the component kind, sanitized name, resolved relative path, Topic Main anchor relationship, publication branch, and exact sanitized commit. These refs are publication transport for the current snapshot, not copies of source branch identity or ancestry. Synchronization publishes every selected component ref before `main`, and `main` pins the exact commits through mode `160000` gitlinks.

A recursive clone produces ordinary submodule checkouts at Topic Main, Topic Actor Workspace, and Agent Workspace paths. It does not recreate the local shared object database or linked-worktree administration relationship. This is intentional because the Topic Publication Copy is an inspectable snapshot rather than an operational Topic Workspace.

Registered GitHub reference repositories remain upstream submodules. Their `.gitmodules` entries use normalized credential-free upstream locators and their gitlinks pin exact registered commits; publication never creates `components/...` branches for third-party references.

Alternative: reuse `topic-owner/main` and `per-topic-actor/<name>/main`. Rejected because those names imply source ownership and continuing branch history. Separate repositories were rejected because one Topic Workspace snapshot would require many remote bindings. Flattening was rejected because it destroys the nested repository topology.

### Keep operational Topic Workspace reconstruction manual

Publication preserves selected paths, Artifacts, sanitized component commits, gitlinks, and declarative relationships so readers can inspect the state that informed the research. It does not promise that cloning the publication yields a valid operational Topic Workspace or provide a command that converts published submodules into Topic Main worktrees.

A reader may manually build a new Topic Workspace from published material, but that process must re-establish the applicable directory, Artifact, Git, Workspace Runtime, and worktree contracts independently. Publication verification therefore checks the published snapshot and recursive submodule checkout, not operational Topic Workspace readiness.

### Persist exclusive-snapshot authority in the Publication Binding

Publication initialization will offer an explicit `exclusive_snapshot` remote mode. Accepting it binds one credential-safe remote identity to one Research Topic and Topic Workspace and acknowledges that every Git ref and tag on that remote is disposable publication state. Later syncs may force-replace planned refs and delete obsolete refs or tags without separate destructive approval for each name.

The authority does not bypass current content and privacy approval. Every sync inventories and fingerprints the complete remote ref and tag set, renders a complete expected post-sync set, and stops if the remote changes after planning. A changed remote locator, repository identity, Research Topic, Topic Workspace, or snapshot mode invalidates the binding and requires a new acknowledgement.

Provider settings and non-Git repository data remain outside this authority. Remote HEAD selection continues through its provider-specific action unless a later decision includes it in the binding.

Alternative: request destructive approval for every sync or every ref. Rejected because a dedicated snapshot remote has no historical or manually maintained Git state to preserve, and repeated branch prompts contradict the selected whole-repository replacement model.

### Validate topology as well as content

Planning fingerprints the source-path identity mapping, generated-overlay paths, canonical branch, component gitlink paths and commits, remote HEAD observation, README links, exclusions, and complete expected remote ref set. Synchronization verifies the complete staged index:

- every source-backed tracked path is identical to its source-relative path;
- every selected component and reference has mode `160000` at its resolved path;
- every selected actor or agent component records its Topic Main anchor relationship without source Git control paths;
- generated metadata appears only at approved reserved paths;
- no retained source file is shadowed by generated output;
- `main` contains the superproject tree rather than a component tree;
- no legacy superproject ref remains.

Topic Publication Copy recovery clones or fetches `main`, initializes exact submodules, validates the tracked manifest, and refuses a legacy layout that cannot prove the same invariants. It does not reconstruct an operational Topic Workspace or linked worktrees.

## Risks / Trade-offs

- [The target remote contains manually added Git refs or tags] → Make the one-time exclusive-snapshot acknowledgement explicit, preview the complete current and expected ref sets, and document that later approved syncs delete unplanned Git state.
- [The remote identity changes after authorization] → Invalidate the Publication Binding and require a new exclusive-snapshot acknowledgement before mutation.
- [A Topic Workspace already uses the reserved overlay path] → Treat the collision as a blocker and revise the reserved namespace through a new approved plan rather than overwriting topic-owned content.
- [A source README contains publication block markers] → Use versioned unambiguous markers and compare the prior generated fingerprint before replacing the managed block.
- [Remote HEAD remains on a legacy branch after Git synchronization] → Report publication as requiring a provider default-branch action and do not claim ordinary-clone readiness.
- [Path-preserved records produce long paths] → Keep canonical paths and use README plus the portable index for navigation rather than flattening.
- [Two active OpenSpec changes modify the same publication requirements] → Archive or sync `publish-reproducible-topic-workspaces` before applying and archiving this corrective change, then validate the combined specification.

## Migration Plan

1. Land the reproduction-first specification and implementation as the baseline for this corrective change.
2. Add path-origin and reserved-overlay validation while retaining read compatibility for existing manifests.
3. Update renderers, planning, synchronization, Topic Publication Copy recovery, operator guidance, and tests to use path-preserved source entries and canonical `main`.
4. Mark every prior Publication Plan stale because branch topology, generated paths, README links, snapshot semantics, and projection fingerprints changed.
5. Obtain one explicit exclusive-snapshot acknowledgement for the exact remote and Topic Workspace identity, then inventory `main`, `topic-workspace/main`, component refs, tags, remote HEAD, and every other Git ref without merging.
6. Build fresh sanitized component commits as needed, then build one fresh neutral superproject commit whose tree satisfies the path invariant.
7. Replace the approved topic-owned component refs, push `main` last, and remove legacy publication refs according to the accepted snapshot authorization policy.
8. Verify the complete remote ref set and a clean recursive clone, then perform or request the separately approved provider default-branch update.

Rollback through publication history is not guaranteed. Republishing a prior Source Topic Workspace state requires rebuilding it as a new current snapshot; source repositories and Source Topic Workspace files remain unchanged throughout.

## Open Questions

None. The publication is a path-preserving current-state snapshot on `main`, uses one-time exclusive Git snapshot authority, represents Topic Main and selected worker-worktree snapshots through same-remote `components/...` branches, confines non-navigation generated metadata to `.isomer-publication/`, and does not promise operational Topic Workspace restoration.
