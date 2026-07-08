# topic-overview-read-api Specification

## Purpose
TBD - created by archiving change show-topic-overview-markdown. Update Purpose after archive.
## Requirements
### Requirement: Topic Overview Markdown Read API
The Project Web API SHALL expose a topic-scoped read-only endpoint that resolves `topic.intent.overview` and returns the Markdown content of the resolved topic overview file when it exists.

#### Scenario: Overview file exists
- **WHEN** the frontend requests the topic overview for a Research Topic whose resolved `topic.intent.overview` file exists
- **THEN** the API SHALL return HTTP 200, `ok: true`, `mutated: false`, topic id, Topic Workspace id when available, overview label metadata, resolved overview path metadata, `exists: true`, and the Markdown content

#### Scenario: Overview file is missing
- **WHEN** the frontend requests the topic overview for a Research Topic whose resolved `topic.intent.overview` file is missing
- **THEN** the API SHALL return HTTP 200, `ok: true`, `mutated: false`, overview label metadata, resolved overview path metadata, `exists: false`, no Markdown content, and a warning diagnostic with a stable missing-overview code
- **AND** the API SHALL NOT raise an unhandled exception or return a frontend-crashing shape

#### Scenario: Overview file cannot be read
- **WHEN** the frontend requests the topic overview for a Research Topic whose resolved `topic.intent.overview` file exists but cannot be decoded, read, or accepted by the read-model size guard
- **THEN** the API SHALL return HTTP 200, keep the topic response usable, omit Markdown content, and include a warning diagnostic with a stable unreadable-overview code
- **AND** the API SHALL still include available supporting Topic and Workspace Runtime JSON

#### Scenario: Topic context cannot be resolved
- **WHEN** the requested Research Topic cannot be resolved through the Project Manifest and Topic Workspace context
- **THEN** the API SHALL return `ok: false`, `mutated: false`, diagnostics, and no Markdown content

### Requirement: Supporting Topic Overview JSON
The topic overview read API SHALL include or expose the supporting Topic and Workspace Runtime JSON data needed by the topic overview page's `View JSON` modal.

#### Scenario: Topic and runtime payloads are available
- **WHEN** the topic overview endpoint succeeds for a resolved Research Topic
- **THEN** the response SHALL provide the same semantic Topic context payload and Workspace Runtime summary currently shown by the overview page
- **AND** those payloads SHALL be suitable for tabbed JSON inspection without requiring the page body to render raw JSON
- **AND** the response SHALL include merged diagnostics and overview source metadata suitable for a `Diagnostics` or `Source` JSON tab

#### Scenario: Runtime inspection has diagnostics
- **WHEN** Workspace Runtime inspection produces warnings or errors
- **THEN** the topic overview response SHALL preserve those diagnostics in the supporting JSON and merged diagnostics list

### Requirement: Topic Overview Descriptor Uses Overview API
Openable item descriptors for `topic:<topic_id>:overview` SHALL advertise the topic overview read API as the primary detail URL for the overview tab.

#### Scenario: Descriptor returned for topic overview
- **WHEN** the frontend resolves `topic:<topic_id>:overview`
- **THEN** the descriptor SHALL keep `preferred_tab_component: topicOverview`
- **AND** the descriptor SHALL include a detail URL for the topic overview read API, plus supporting topic and runtime URLs when useful

