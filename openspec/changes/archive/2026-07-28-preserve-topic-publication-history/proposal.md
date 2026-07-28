## Why

Topic publication currently creates fresh sanitized commits and force-replaces every differing component ref and canonical `main`, even when the prior publication is available as a valid base for one incremental sanitized commit. This discards useful publication history and applies destructive Git operations where an exact normal push would preserve the same privacy, topology, and current-snapshot guarantees.

## What Changes

- Prefer history-preserving publication updates when the prior remote publication is compatible: materialize the newly approved sanitized tree as a direct child of the freshly observed publication commit, commit only the delta, and use an exact non-force push.
- Treat absent refs as initial publication, exact matches as no-op, compatible differing refs as fast-forward updates, changed remote state as stale, unresolved destination edits as conflicts, and history-incompatible refs as force-replacement candidates.
- Recover a missing disposable Topic Publication Copy from a compatible remote and continue incrementally instead of treating local-copy loss as a reason to rewrite remote history.
- Define publication-history compatibility from the matching Publication Binding, supported tracked manifests, canonical branch and component topology, pinned component commits, current privacy policy, and freshly observed ref ancestry.
- Retain `exclusive_snapshot` as fallback authority for exact ref replacement and obsolete-ref deletion, but stop treating it as the default synchronization strategy.
- Use branch-scoped force-with-lease against the exact observed commit for approved fallback replacement, and expand fallback eligibility to privacy, credential, license, or withdrawal decisions that require prior published content to become unreachable.
- Preserve complete remote inventory, stale-plan detection, exact staging, component-first and `main`-last ordering, neutral publication identity, source-history exclusion, conflict handling, and recursive-clone verification.
- Extend publication plans and outcomes with the selected per-ref update strategy, observed base, planned result, compatibility evidence, and fallback reason, with read compatibility for existing bindings and publication metadata.
- Update operator skills, validation rules, canonical documentation, and tests for initial, no-op, incremental, recovery, conflict, stale, and force-fallback synchronization.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `topic-workspace-git-publication`: Change publish synchronization from unconditional snapshot replacement to incremental sanitized publication by default, with exact force replacement retained as a history-incompatibility fallback.
- `isomer-documentation-system-guide`: Explain the distinction between forbidden Source Topic Workspace Git ancestry and permitted sanitized publication ancestry, including recovery, no-op, fast-forward, conflict, and fallback behavior.

## Impact

The change affects the Topic Git publication models, schemas, branch classification, plan fingerprinting, projection metadata, publication outcomes, packaged `isomer-op-topic-workspace-git` guidance, skill validation rules, canonical domain language, manual and developer documentation, and Topic Git unit and integration tests. Existing `exclusive_snapshot` bindings remain valid as fallback authority, while existing approved plans become stale because the plan schema and ref-update strategy change.
