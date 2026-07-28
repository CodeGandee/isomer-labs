## 1. Versioned Publication Contracts

- [x] 1.1 Add typed ref-update strategy, compatibility evidence, planned base/result, fallback reason, and per-ref outcome models for `no_op`, `create`, `fast_forward`, and `force_replacement`.
- [x] 1.2 Add a new closed publication-plan schema version that persists complete history-aware ref actions and includes them in plan fingerprint validation.
- [x] 1.3 Add a new publication-outcomes schema version for attempted strategy, observed lease, actual result, verification, fallback use, and safe resume state.
- [x] 1.4 Add only the stable tracked lineage fields needed for compatibility to a versioned projection manifest, if existing manifest evidence is insufficient, while keeping volatile plan and execution data out of the projected tree.
- [x] 1.5 Preserve Publication Binding v1 and legacy manifest/outcome read compatibility, and reject publication-plan v1 approvals as stale under the new synchronization semantics.

## 2. History Compatibility and Planning

- [x] 2.1 Replace differing-ref snapshot classification with conservative history compatibility evaluation that uses exact fetch and ancestry evidence, binding identity, supported metadata, canonical topology, component pins, and history-retention posture.
- [x] 2.2 Plan one persisted strategy for every expected topic-owned ref, separate exact obsolete-ref and tag deletions, and retain the complete observed and expected remote inventory.
- [x] 2.3 Detect exact projected-tree equality as `no_op`, absent refs as `create`, compatible prior publications as `fast_forward`, and unsupported or mismatched lineages as blocked or `force_replacement`.
- [x] 2.4 Treat destination-only and simultaneous edits as conflicts, and ensure dirty or divergent local preparation never becomes a force-replacement reason.
- [x] 2.5 Compute force-fallback topology closure for privacy, credential, identity, license, and withdrawal decisions, including canonical `main` when retained ancestry would reference affected content or components.
- [x] 2.6 Revalidate matching `exclusive_snapshot` authority, exact observed leases, strategy evidence, complete remote state, and current approvals before permitting any planned replacement or deletion.

## 3. Incremental Projection and Synchronization

- [x] 3.1 Materialize each approved sanitized tree from its exact planned base, remove unapproved paths, stage explicitly, and verify that no Source Topic Workspace Git metadata or ancestry enters a publication commit.
- [x] 3.2 Create parentless sanitized commits for `create`, direct-child sanitized delta commits for `fast_forward`, and no commit or branch update push for `no_op`.
- [x] 3.3 Reuse an existing Topic Publication Copy only when it is clean and based on the exact observed commit; otherwise block or construct a separate validated disposable recovery repository without modifying the unusable copy.
- [x] 3.4 Recover a missing Topic Publication Copy from exact compatible remote `main` and pinned component refs so local-copy loss remains eligible for fast-forward publication.
- [x] 3.5 Execute `create` and `fast_forward` through exact normal refspecs, and execute approved fallback through exact branch-scoped `--force-with-lease=<ref>:<observed-commit>` refspecs without bare force.
- [x] 3.6 Preserve deterministic component-first and canonical-`main`-last synchronization, record per-ref outcomes, and resume partial publication only after a fresh complete inventory recognizes exact completed results.
- [x] 3.7 Verify the final ref and tag set, expected parent relationships, clean publication copies, and a fresh recursive clone of canonical `main`.

## 4. Operator Skill and Documentation

- [x] 4.1 Update publication initialization, planning, status, and persistence guidance to distinguish `exclusive_snapshot` fallback authority from the default history-preserving update strategy.
- [x] 4.2 Update sync, publication-safety, and direct-Git guidance with exact normal pushes, missing-copy recovery, no-op behavior, conflict blockers, exact force-with-lease fallback, stale-plan handling, and component-first ordering.
- [x] 4.3 Update skill validation and Topic Git skill contract tests to accept exact normal publication pushes and exact leased fallback while rejecting bare force, wildcard refspecs, incomplete inventory, and `main`-before-components ordering.
- [x] 4.4 Update the canonical domain language and user/developer documentation to distinguish forbidden source ancestry from permitted compatible sanitized publication ancestry and to explain history-retention and history-purge outcomes.
- [x] 4.5 Verify that all modified packaged system-skill metadata versions still exactly match `project.version`.

## 5. Automated and Manual Verification

- [x] 5.1 Add model, schema, fingerprint, and migration tests for all ref strategies, compatibility evidence, legacy reads, and stale v1 publication plans.
- [x] 5.2 Add planning tests for initial publication, exact no-op, compatible fast-forward, incompatible fallback, history withdrawal, destination conflict, stale remote state, and fallback topology closure.
- [x] 5.3 Add synchronization tests for direct-parent commits, missing-copy recovery, preserved dirty copies, exact normal pushes, exact force-with-lease, component-first partial resume, and final ancestry verification.
- [x] 5.4 Extend integration coverage with consecutive publications that preserve sanitized history and a structurally incompatible remote that uses the approved force-replacement fallback.
- [x] 5.5 Run `pixi run lint`, `pixi run typecheck`, `pixi run test`, relevant integration or manual Topic Git checks, packaged skill validation, and strict OpenSpec validation.
