## ADDED Requirements

### Requirement: Canonical Idea Detail Read Model
The topic-scoped web read model SHALL expose canonical Research Idea detail data needed by GUI idea inspection without mutating Workspace Runtime.

#### Scenario: Idea detail resolves canonical idea
- **WHEN** the GUI requests detail for a topic-scoped canonical Research Idea id
- **THEN** the backend returns the Research Idea metadata, realization history, latest realization when known, generation group context when known, and incoming or outgoing idea lineage refs when available
- **AND** the response includes diagnostics instead of mutating runtime state when some related data is missing

#### Scenario: Idea detail resolves source JSON
- **WHEN** the selected Research Idea or latest realization points to a managed structured payload JSON source
- **THEN** the backend returns exact source JSON content or the exact source JSON fragment, source locator metadata, payload digest when known, and source record refs
- **AND** the response is read from canonical runtime records or managed payload files rather than generated Markdown prose

#### Scenario: Source JSON precedence is deterministic
- **WHEN** multiple possible JSON sources exist for one Research Idea
- **THEN** the backend chooses the latest Idea Realization `source_json_path` first, the latest realization record payload second, and Research Idea source metadata third
- **AND** the response identifies the selected source so the frontend can show realization history separately from the preview source

#### Scenario: Large source JSON is capped by default
- **WHEN** the selected source JSON serializes above the default 1 MiB response cap and the caller has not explicitly requested full source JSON
- **THEN** the backend returns source metadata, omits the full JSON body, and emits a non-fatal `source_json_truncated` diagnostic
- **AND** an explicit full-source request can fetch the exact JSON for the modal or copy action without mutating Workspace Runtime

#### Scenario: Missing source JSON is diagnostic
- **WHEN** the selected Research Idea has no resolvable source JSON payload
- **THEN** the backend returns the available idea metadata and realization records with a non-fatal diagnostic explaining why exact JSON is unavailable
- **AND** the read operation does not create, rebuild, repair, or backfill query-index rows

### Requirement: Idea Openable Descriptor
The semantic openable item resolver SHALL support canonical Research Idea items as workbench-openable resources.

#### Scenario: Idea openable descriptor resolves
- **WHEN** the frontend requests an openable descriptor for `idea:<topic_id>:<idea_id>`
- **THEN** the backend returns a descriptor for an `ideaDetail` workbench tab with topic id, idea id, title, stable tab id, and idea detail URL

#### Scenario: Unknown idea descriptor reports error
- **WHEN** the frontend requests an openable descriptor for an unknown or cross-topic idea id
- **THEN** the backend returns an error descriptor with diagnostics and does not fall back to a record tab for the wrong object
