## MODIFIED Requirements

### Requirement: Documentation Explains Topic Publication Copies
The documentation SHALL describe Topic Publication Copy placement, sanitization, submodule layout, same-remote branch mapping, reconstruction, comparison, history-aware synchronization, fallback replacement, and push ordering.

#### Scenario: Default temporary path is explained
- **WHEN** a reader asks where publication work is stored
- **THEN** documentation explains effective Project-root `tmp/` and `temp/` ignore inspection, the default `topic-workspace-publish/<topic-id>/` subdirectory, and managed `tmp/` creation when no ignored candidate exists

#### Scenario: Privacy projection is explained
- **WHEN** documentation explains what enters publication history
- **THEN** it defines `track`, `template`, `exclude`, `component`, and `block`
- **AND** it states that placeholder generation and masking happen only in the Topic Publication Copy

#### Scenario: Source and publication history are distinguished
- **WHEN** documentation explains sanitized publication commits
- **THEN** it states that publication never imports Source Topic Workspace or component Git ancestry
- **AND** it explains that a compatible prior sanitized publication commit may be the parent of the next sanitized publication delta

#### Scenario: Same-remote submodules are explained
- **WHEN** documentation explains published nested workspaces
- **THEN** it maps Topic Main, Topic Actor, and Agent components to their deterministic branches in the same user-provided remote
- **AND** it states that canonical `main` pins exact component commits as submodules

#### Scenario: Synchronization comparison is explained
- **WHEN** documentation explains publish sync
- **THEN** it describes comparison among source content, expected sanitized output, last projection manifest, current publication copy, and fetched remote state
- **AND** it explains no-op, initial creation, fast-forward delta commits, conflict blocking, missing-copy reconstruction, component-first push, partial failure, and superproject-last behavior

#### Scenario: Force replacement is explained as fallback
- **WHEN** documentation explains an incompatible publication history or required history withdrawal
- **THEN** it explains exact force-with-lease replacement under current `exclusive_snapshot` authority
- **AND** it does not present local-copy loss, ordinary source changes, or unresolved destination conflicts as reasons to force-push
