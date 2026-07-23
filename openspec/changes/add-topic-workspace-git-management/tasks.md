## 1. Domain and Independent State Models

- [x] 1.1 Update the canonical Isomer platform language to define Source Topic Workspace as a contextual role of the canonical Topic Workspace, Topic Publication Copy as a derived projection rather than a workspace type, in-workspace local tracking, publication binding, and publication projection manifest without changing the three-workspace taxonomy, canonical Topic Main, or worker topology.
- [x] 1.2 Add typed local-tracking states, publication states, privacy dispositions, remote visibility values, schema-validated layer-specific support files, component bindings, conflicts, and per-branch outcomes.
- [x] 1.3 Require valid Workspace Runtime and `<topic.runtime>/topic-git/` support files for local mutations; permit pre-runtime publication state only in an ignored Topic Publication Copy support root; promote a validated credential-safe publication binding into runtime support during a later approved publication mutation; never edit `state.sqlite` or store secrets, sensitive excerpts, raw private diffs, source Git configuration, or credential-bearing URLs.
- [x] 1.4 Author selected Topic Workspace context resolution using explicit `isomer-cli --print-json` read-only queries and ensure every Topic Git operation rejects sibling scanning, guessed paths, unresolved context, and Isomer CLI mutation commands.
- [x] 1.5 Implement overall read-only status for all four layer combinations and prove that an ancestor Project repository does not enable local tracking.

## 2. Local In-Workspace Tracking

- [x] 2.1 Author direct `git -C <source-topic-workspace> ...` read-only local status for repository identity, HEAD, index, working tree, ignore posture, nested workspace exclusions, warnings, and blockers.
- [x] 2.2 Author a local-init plan that discovers every ancestor Git top level, proves the Source Topic Workspace is absent from each ancestor index and effectively ignored, and shows exact direct Git initialization and local managed `.gitignore` mutations without changing ancestors, nested repositories, or remotes.
- [x] 2.3 Author direct local root repository initialization with explicit approval, safe existing-repository reuse, tracked or unignored ancestor blockers, invalid `.git` blockers, and immediate post-mutation verification; never edit an ancestor `.gitignore` or remove ancestor index entries.
- [x] 2.4 Implement non-Git local candidate classification and exact whole-file commit planning for root-owned material, including secret-like warnings and local-only defaults.
- [x] 2.5 Implement idempotent local managed `.gitignore` updates that preserve user rules and block already-tracked sensitive paths without implicit index removal, then inspect effective ignore behavior with direct Git.
- [x] 2.6 Implement optional `topic-workspace-local-version.toml` rendering with relative nested workspace labels, branch names, commit SHAs, dirty-state booleans, and an explicit pointer-only limitation.
- [x] 2.7 Author direct Git exact-pathspec staging, index verification, and commit procedures that reject stale plans, unexpected index content, `git add .`, and `git add -A`.
- [x] 2.8 Prove that every local operation avoids remote discovery, configuration, fetch, pull, and push and does not read or mutate publication state as a prerequisite.
- [x] 2.9 Add low-freedom local operation pages for status, init, plan, ignore, and commit; verify that they use direct Git and contain no `isomer-cli project topic-git ...` invocation or hidden Git wrapper.

## 3. Publication Destination and Binding

- [x] 3.1 Implement effective Project-root `tmp/` and `temp/` discovery using read-only Isomer Project-location queries, directory evidence, direct `git check-ignore` when applicable, and bounded `.gitignore` inspection otherwise.
- [x] 3.2 Implement deterministic destination selection with existing binding reuse, ignored `tmp/` preference, ignored `temp/` fallback, and managed ignored `tmp/` creation when needed.
- [x] 3.3 Validate that default and custom destinations remain inside the Project root and outside the Source Topic Workspace, Project Config Directory, generated content root, Houmao state, and canonical repositories.
- [x] 3.4 Implement an idempotent Project-root managed `.gitignore` block for publication temporary storage while preserving user-authored rules.
- [x] 3.5 Implement credential-safe remote validation, redacted reporting, typed visibility acknowledgement, pre-runtime copy-local binding persistence, and later runtime binding promotion without making Workspace Runtime a publication prerequisite.
- [x] 3.6 Implement publication status for disabled, prepared, synchronized, stale, copy-missing, and blocked states without requiring local tracking.
- [x] 3.7 Add low-freedom publication operation pages for status, init, and plan; allow them immediately after Topic Workspace registration, keep publish init free of remote push side effects, and verify that the pages use Isomer CLI only for read-only information queries.

## 4. Sanitized Publication Projection

- [x] 4.1 Implement source inventory through semantic Topic Workspace surfaces without using the local root Git index or HEAD as publication authority.
- [x] 4.2 Implement publication classification for `track`, `template`, `exclude`, `component`, and `block`, including size, format, credential, private-key, signed-URL, license, and ambiguity diagnostics.
- [x] 4.3 Implement a copier that never transfers `.git` directories, `.git` worktree files, Git configuration, refs, objects, reflogs, indexes, credentials, source remotes, or source repository history.
- [x] 4.4 Implement structured placeholder generation and explicitly targeted sanitized text copies inside the Topic Publication Copy while preserving every source file.
- [x] 4.5 Block unsupported binary and archive masking and rescan all files before they become eligible for a publication commit.
- [x] 4.6 Implement the tracked sanitized projection manifest and `topic-workspace-version.toml` without absolute source paths or sensitive content.
- [x] 4.7 Add stale-plan fingerprints for source content, expected output, copy content, binding identity, components, and remote refs.
- [x] 4.8 Select every currently available Topic Main, registered Topic Actor Workspace, and selected-team Agent Workspace through read-only Isomer topology queries by default; support explicit plan exclusions; invalidate older plans when a newly available component changes the projection.

## 5. Component Repositories and Submodules

- [x] 5.1 Author direct Git materialization of fresh sanitized Topic Main publication history on `topic-owner/main` without source Git ancestry.
- [x] 5.2 Author direct Git materialization of selected Topic Actor publication histories on `per-topic-actor/<name>/main` without source Git ancestry.
- [x] 5.3 Author direct Git materialization of selected Agent publication histories on `per-agent/<name>/main` without source Git ancestry.
- [x] 5.4 Author direct Git superproject submodule construction whose `.gitmodules` entries use the same credential-safe remote, name deterministic component branches, and pin exact component commits at source-relative workspace paths.
- [x] 5.5 Author direct Git materialization of the sanitized superproject on `topic-workspace/main` and ensure nested component directories are represented only as submodule gitlinks.
- [x] 5.6 Validate recursive clone and submodule checkout from one remote with unrelated sanitized component and superproject histories.
- [x] 5.7 Report unavailable, explicitly excluded, blocked, and selected components explicitly without inventing Topic Actor or Agent bindings from directory scans.

## 6. Publication Comparison and Synchronization

- [x] 6.1 Author direct Git reconstruction of a missing Topic Publication Copy from its binding, fetched remote branches, and sanitized manifests.
- [x] 6.2 Implement comparison among current source content, expected sanitized projection, last projection manifest, current copy content, and fetched remote branch state.
- [x] 6.3 Update outputs only when they match the prior generated fingerprint or have an explicit approved conflict resolution.
- [x] 6.4 Remove outputs only when their source disappeared and the destination still matches the prior generated fingerprint.
- [x] 6.5 Report source-and-destination conflicts without overwriting either side and persist the safe resume point.
- [x] 6.6 Author direct Git fetch and ancestry checks for every selected component and superproject branch before mutation; classify absent, compatible, and incompatible publication refs; reject unapproved divergence or force requirements without pulling or merging.
- [x] 6.7 Author direct Git exact-pathspec commits and explicit-ref pushes for selected component branches first, then update gitlinks and sanitized manifests and push `topic-workspace/main` last; use normal push for absent or compatible refs and plain `--force` only for exact approved incompatible branch replacements.
- [x] 6.8 Record per-branch partial outcomes and make publication sync idempotently resumable while the previous superproject version remains authoritative.
- [x] 6.9 Add the low-freedom publish sync operation page and ensure its direct Git procedure never pulls, merges, rebases, resets, cleans, deletes remote branches, creates provider repositories, mutates Source Topic Workspace Git state, or force-pushes without a fresh branch-specific destructive plan and separate explicit permission.
- [x] 6.10 Implement destructive-change plans that record observed remote commits, exact replacement commits, displaced commits, branch-scoped approval, push order, stale-ref invalidation, and warnings; prohibit `--all`, `--mirror`, deletion, and force against unlisted branches.

## 7. Operator Skill and Routing

- [x] 7.1 Create protected subskill `isomer-op-topic-workspace-git` with concise `SKILL-MAIN.md`, matching `agents/openai.yaml`, and separate read-only query, direct Git, local, publication, privacy, and persistence safety references.
- [x] 7.2 Add progressive-disclosure operation pages for overall status, local status/init/plan/ignore/commit, and publish status/init/plan/sync.
- [x] 7.3 Register protected member `topic-git` in the core system-skill manifest, entrypoint route table, routing indexes, help, and validation fixtures.
- [x] 7.4 Update Topic Manager guidance to delegate explicit local-tracking and publication requests without changing ordinary topic management.
- [x] 7.5 Ensure task-only “publish now” requests may run from publication initialization through synchronization only after privacy and remote mutation gates, with direct Git commands scoped to validated publication-copy paths.
- [x] 7.6 Ensure packaged system-skill metadata remains internally consistent and matches the project version when released.
- [x] 7.7 Add validation fixtures that reject an Isomer CLI Topic Git mutation family, Git subprocess calls from Isomer CLI or non-Git helpers, ambient-cwd Git execution, broad staging, unsafe Git commands, unplanned force push, `--all`, `--mirror`, remote branch deletion, and missing read-only Isomer context queries.

## 8. Documentation and Verification

- [x] 8.1 Update Topic Workspace, storage, CLI, system-skill, and troubleshooting documentation for independent opt-in layers, unchanged canonical worker topology, read-only Isomer CLI queries, and direct agent-run Git.
- [x] 8.2 Document Topic Publication Copy terminology, temporary-path selection, privacy dispositions, fresh histories, same-remote submodules, reconstruction, conflicts, and push ordering.
- [x] 8.3 Add unit tests for independent state combinations, namespaced support-file schemas, ancestor Git detection, tracked ancestor paths, unignored ancestor paths, effective ancestor ignore evidence, no-ancestor operation, local planning, managed ignore blocks, exact staging, stale plans, redaction, placeholder generation, and source immutability.
- [x] 8.4 Add Project fixture tests for ignored `tmp/`, ignored `temp/`, declared-but-missing directories, managed `tmp/` creation, nested ignore negation, non-Git Projects, and unsafe custom destinations.
- [x] 8.5 Add projection tests proving that source `.git` metadata, histories, credentials, runtime state, and excluded surfaces never enter the Topic Publication Copy.
- [x] 8.6 Add local bare-remote integration tests for same-remote component branches, superproject submodules, recursive clone, fetch-first sync, component-first push, and superproject-last publication.
- [x] 8.7 Add synchronization tests for untracked source content, destination-only edits, simultaneous edits, safe deletion, deletion conflicts, missing-copy reconstruction, divergence refusal, partial push, and resume.
- [x] 8.8 Add cross-layer tests proving that publication works without local tracking, local commits work without publication, local commits do not trigger publication, and publication never stages or commits the local root repository.
- [x] 8.9 Add lifecycle-boundary tests proving that local mutations require Workspace Runtime, pre-runtime publication works after Topic Workspace registration, pre-runtime state stays out of publication commits, later approved publication mutation promotes the binding into runtime support, and loss of an unpushed pre-runtime copy requires replanning.
- [x] 8.10 Add boundary tests proving that Isomer CLI calls in Topic Git are read-only, all Git commands run directly with validated `git -C` paths, non-Git helpers never execute Git, and missing required Isomer information blocks the applicable mutation without making Workspace Runtime a publication prerequisite.
- [x] 8.11 Add component-default tests proving that every currently available resolved component is selected, unavailable components do not block root-only publication, explicit exclusions are honored, newly available components stale older plans, and no component is inferred from directory scans.
- [x] 8.12 Add remote-compatibility tests for an empty first-use remote, compatible fast-forward publication, incompatible-branch blocking, explicit plain-force replacement, displaced-commit reporting, stale force approval, and refusal of unlisted branches, `--all`, `--mirror`, and deletion.
- [x] 8.13 Run `pixi run lint`, `pixi run typecheck`, `pixi run test`, strict OpenSpec validation, and packaged system-skill validators, then resolve every failure attributable to this change.
