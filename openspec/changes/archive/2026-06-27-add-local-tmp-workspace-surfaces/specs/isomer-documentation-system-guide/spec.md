## MODIFIED Requirements

### Requirement: Documentation Verification for Semantic Paths
The documentation verification path SHALL detect stale wording that treats default paths as the only workspace contract or treats tmp material as shared, durable, or evidence-ready.

#### Scenario: Docs validation rejects durable tmp wording
- **WHEN** docs validation scans documentation that mentions `tmp/`
- **THEN** it allows the wording only when the same document names semantic labels such as `topic.tmp`, `topic.main_repo.tmp`, or `agent.tmp`
- **AND** the document states that tmp material is local, ignored, disposable, not shared, and not durable evidence

#### Scenario: Docs validation rejects fixed tmp path authority
- **WHEN** docs validation scans documentation that describes `tmp/` as the only supported path contract
- **THEN** it reports that tmp path wording must be semantic-label-first and must identify default directories as `isomer-default.v1` bindings

### Requirement: tmp Surfaces Are Documented as Downstream Labels
The documentation SHALL frame local `tmp/` surfaces as semantic labels that inherit the manifest-backed path model.

#### Scenario: Topic Workspace definition lists implemented tmp labels
- **WHEN** a reader opens the Topic Workspace definition after this change is implemented
- **THEN** it lists `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp` as Local Tmp Surface labels with local disposable meanings
- **AND** default directories are described only as `isomer-default.v1` bindings

#### Scenario: Documentation no longer calls implemented labels planned
- **WHEN** documentation describes `topic.tmp`, `topic.main_repo.tmp`, or `agent.tmp` after the semantic surface catalog supports them
- **THEN** it describes them as implemented standard labels rather than planned or future labels

#### Scenario: Documentation distinguishes tmp from sharing
- **WHEN** documentation explains worker visibility and collaboration paths
- **THEN** it states that tmp is not Peer Read Access, not a generated-link target, not owner-preserved records, and not Git-tracked collaboration material

#### Scenario: Documentation distinguishes tmp from scratch
- **WHEN** documentation explains `agent.scratch` or `isomer-managed/agent-owned/scratch/`
- **THEN** it distinguishes agent-owned draft support from root tmp disposable material
