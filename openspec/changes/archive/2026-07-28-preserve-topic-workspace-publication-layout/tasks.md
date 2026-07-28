## 1. Projection Model and Validation

- [x] 1.1 Add an explicit source-backed versus generated entry origin to publication models, schemas, JSON serialization, and stale-plan fingerprints with read compatibility for existing manifests.
- [x] 1.2 Enforce `output_relative_path == source_relative_path` for every source-backed `track`, `template`, and `component` entry, while keeping excluded entries pathless.
- [x] 1.3 Define the `.isomer-publication/` tracked overlay and validate root exceptions, reserved-path collisions, generated-entry origins, and complete staged-index topology.
- [x] 1.4 Extend Publication Bindings, Plans, and outcomes with `exclusive_snapshot` mode, canonical `main`, deterministic `components/...` refs, Topic Main anchor relationships for actor and agent worktree snapshots, observed remote HEAD, complete snapshot ref and tag sets, exact generated paths, and whole-remote replacement state.
- [x] 1.5 Invalidate exclusive-snapshot authority when the remote identity, Research Topic, Topic Workspace, or snapshot mode changes while keeping credentials and provider state outside the binding.

## 2. Path-Preserving Materialization

- [x] 2.1 Update semantic inventory and materialization so root manifests, Pixi declarations, attributes, ignore policy, readiness summaries, intent, and records retain their Topic Workspace-relative paths.
- [x] 2.2 Preserve the Source Topic Workspace `.gitignore` at the root and keep copy-local `.isomer/` support state untracked through repository-local Git exclusion configuration.
- [x] 2.3 Render the portable research-record index, Publication Projection Manifest, and Topic Workspace version manifest below `.isomer-publication/`.
- [x] 2.4 Compose the root README from any sanitizable source README plus a versioned generated navigation block, and link the latest eligible PDF at its path-preserved Artifact location.
- [x] 2.5 Reject relocated PDF aliases, source-shadowing generated files, synthetic content-class directories, and component files flattened into the superproject.

## 3. Branch Topology and Synchronization

- [x] 3.1 Change publication initialization, synchronization, status, and Topic Publication Copy recovery so `main` is the canonical superproject branch and selected component branches push before it.
- [x] 3.2 Publish Topic Main plus selected Topic Actor Workspace and Agent Workspace worktree snapshots through deterministic same-remote `components/...` branches, record their Topic Main anchor relationships without copying source Git control state, keep all component and registered reference gitlinks at their resolved Topic Workspace-relative paths, and verify every exact mode `160000` index entry.
- [x] 3.3 Add current-state snapshot replacement for legacy `main`, `topic-workspace/main`, source-style component branches, obsolete publication refs, and prior publication commits without preserving ancestry.
- [x] 3.4 Apply one-time exclusive-snapshot authority to force-replace and delete planned Git refs and tags without repeated destructive prompts while preserving current-plan and stale-state checks.
- [x] 3.5 Report remote HEAD separately from Git branch synchronization and require a distinct provider-supported action before changing the hosted default branch.
- [x] 3.6 Make failed component, `main`, ref-removal, and remote-HEAD operations persist unambiguous safe resume points without treating a legacy branch or prior commit as authoritative.

## 4. Operator Guidance and Migration

- [x] 4.1 Revise Topic Git publication planning, privacy, initialization, safety, synchronization, status, and Topic Publication Copy recovery guidance to state the path-preserving subset invariant and canonical `main` topology.
- [x] 4.2 Document reserved generated paths, source README composition, path-preserved latest-paper linking, empty-directory behavior, current-state-only remote semantics, the Topic Main worktree family represented by same-remote `components/...` branches, upstream third-party submodules, remote HEAD handling, the prohibition on merging component content into the superproject root, and the non-goal of operational Topic Workspace restoration.
- [x] 4.3 Produce a read-only migration assessment for `pwinfer-analysis` that compares every retained source path with its planned output path and describes the complete remote snapshot replacement without pushing it.

## 5. Verification

- [x] 5.1 Add unit tests for source-path identity, generated-entry origins, reserved-overlay collisions, in-place templates, root ignore preservation, README composition, and path-preserved PDFs.
- [x] 5.2 Add unit tests for canonical `main`, deterministic same-remote component refs, exclusive-snapshot binding identity, persistent overwrite authority, complete ref and tag replacement, remote HEAD diagnostics, legacy-ref removal, stale snapshot plans, and provider-state exclusion.
- [x] 5.3 Add integration coverage that recursively clones a publication with root files, durable records, Topic Main, Topic Actor Workspace, Agent Workspace, and upstream reference submodules at custom resolved paths; compares the clone against the publishable Source Topic Workspace path set; verifies actor and agent Topic Main anchor metadata; and confirms the result contains ordinary submodule checkouts rather than restored local worktrees.
- [x] 5.4 Add a regression fixture proving that `pixi.toml`, `pixi.lock`, `topic-workspace.toml`, `.gitattributes`, `.gitignore`, readiness summary, `records/`, `actors/`, and `repos/` are never relocated into synthetic directories.
- [x] 5.5 Run OpenSpec validation, focused Topic Git tests, skill validation, Ruff, MyPy, and the default unit suite; resolve all regressions before requesting migration approval.
