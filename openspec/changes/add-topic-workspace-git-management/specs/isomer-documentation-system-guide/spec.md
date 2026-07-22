## ADDED Requirements

### Requirement: Documentation Explains Independent Topic Git Layers
The documentation SHALL explain in-workspace local tracking and remote publication as independent disabled-by-default capabilities.

#### Scenario: Publication terminology preserves workspace taxonomy
- **WHEN** documentation contrasts canonical source material with publication material
- **THEN** it defines Source Topic Workspace as a contextual role of the canonical Topic Workspace
- **AND** it defines Topic Publication Copy as a derived projection rather than a managed workspace type, canonical source, or Publication Workspace

#### Scenario: Topic Workspace documentation presents four combinations
- **WHEN** a reader opens Topic Workspace Git documentation
- **THEN** it explains that neither layer, local only, publication only, or both may be enabled
- **AND** it states that neither layer requires, triggers, disables, or mutates the other

#### Scenario: Local tracking documentation states its boundary
- **WHEN** documentation explains local tracking
- **THEN** it states that the Source Topic Workspace root repository is local-only, excludes existing nested Git workspaces, and never performs remote operations through Topic Git local operations

#### Scenario: Publication documentation states its boundary
- **WHEN** documentation explains remote publication
- **THEN** it states that publication reads the current source filesystem, uses an ignored Topic Publication Copy, never copies source Git metadata or history, and does not require local commits

#### Scenario: Query and execution boundary is explained
- **WHEN** documentation explains how Topic Git operations run
- **THEN** it states that Isomer CLI supplies only read-only selected-context and semantic-path information
- **AND** it states that the operator agent invokes Git directly with validated paths rather than through an Isomer CLI Topic Git command family or another Git wrapper

### Requirement: Documentation Explains Topic Publication Copies
The documentation SHALL describe Topic Publication Copy placement, sanitization, submodule layout, same-remote branch mapping, reconstruction, comparison, and push ordering.

#### Scenario: Default temporary path is explained
- **WHEN** a reader asks where publication work is stored
- **THEN** documentation explains effective Project-root `tmp/` and `temp/` ignore inspection, the default `topic-workspace-publish/<topic-id>/` subdirectory, and managed `tmp/` creation when no ignored candidate exists

#### Scenario: Privacy projection is explained
- **WHEN** documentation explains what enters publication history
- **THEN** it defines `track`, `template`, `exclude`, `component`, and `block`
- **AND** it states that placeholder generation and masking happen only in the Topic Publication Copy

#### Scenario: Same-remote submodules are explained
- **WHEN** documentation explains published nested workspaces
- **THEN** it maps Topic Main, Topic Actor, and Agent components to their deterministic branches in the same user-provided remote
- **AND** it states that `topic-workspace/main` pins exact component commits as submodules

#### Scenario: Synchronization comparison is explained
- **WHEN** documentation explains publish sync
- **THEN** it describes comparison among source content, expected sanitized output, last projection manifest, current publication copy, and fetched remote state
- **AND** it explains conflict, deletion, missing-copy reconstruction, component-first push, partial failure, and superproject-last behavior
