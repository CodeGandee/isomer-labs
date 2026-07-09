# project-web-topic-overview Specification

## Purpose
TBD - created by archiving change show-topic-overview-markdown. Update Purpose after archive.
## Requirements
### Requirement: Topic Overview Renders Markdown First
The Project Web topic overview panel SHALL render the Markdown content from `topic.intent.overview` as the main page content.

#### Scenario: User opens topic overview with Markdown available
- **WHEN** a user opens the topic overview tab for a Research Topic whose topic overview Markdown is available
- **THEN** the page body SHALL render that Markdown through the standard Markdown preview component
- **AND** the page body SHALL NOT show raw Topic or Runtime JSON blocks as its primary content

#### Scenario: Topic overview is loading
- **WHEN** the topic overview request is pending
- **THEN** the panel SHALL show a loading state that does not flash raw JSON as placeholder content

### Requirement: Missing Topic Overview Shows Warning
The Project Web topic overview panel SHALL show an inline warning when the backend reports that `topic.intent.overview` is missing.

#### Scenario: Overview Markdown is missing
- **WHEN** the topic overview response reports `exists: false` for the resolved topic overview file
- **THEN** the panel SHALL show a warning or empty Markdown state that names `topic.intent.overview`
- **AND** the panel SHALL keep the tab usable and SHALL NOT crash

#### Scenario: Overview response contains diagnostics
- **WHEN** the topic overview response contains diagnostics
- **THEN** the panel SHALL surface relevant warning or error diagnostics near the overview content or status row

### Requirement: Topic Overview JSON Is On Demand
The Project Web topic overview panel SHALL move supporting Topic and Runtime JSON into a `View JSON` modal instead of rendering it inline as the overview body, and the backend SHALL defer those supporting JSON payloads until the user requests them.

#### Scenario: Initial overview omits supporting JSON payloads
- **WHEN** a user opens the topic overview panel
- **THEN** the initial overview API response SHALL include overview Markdown, source metadata, and diagnostics needed by the visible panel
- **AND** it SHALL NOT embed full supporting Topic or Runtime JSON payloads by default

#### Scenario: User opens View JSON
- **WHEN** a user clicks `View JSON` on the topic overview panel
- **THEN** the GUI SHALL fetch supporting JSON when it is not already available
- **AND** the GUI SHALL open a modal dialog with tabs for `Topic`, `Runtime`, and `Diagnostics` or `Source` depending on available response data

#### Scenario: Supporting JSON fetch fails
- **WHEN** the user opens `View JSON` and the supporting JSON request fails or returns partial data
- **THEN** the GUI SHALL keep the overview panel usable and show an error or warning in the JSON modal instead of replacing the overview body with raw failure data

#### Scenario: User copies JSON
- **WHEN** a user clicks `Copy JSON` in the topic overview JSON modal
- **THEN** the GUI SHALL copy the JSON content for the active tab and report copy success or failure

### Requirement: Topic Overview Markdown Copy
The Project Web topic overview panel SHALL provide a `Copy Markdown` action when Markdown content is available.

#### Scenario: User copies Markdown
- **WHEN** the topic overview Markdown content is available and the user clicks `Copy Markdown`
- **THEN** the GUI SHALL copy the exact Markdown content returned by the backend and report copy success or failure

#### Scenario: Markdown is unavailable
- **WHEN** the topic overview Markdown content is unavailable
- **THEN** the `Copy Markdown` action SHALL be disabled or report that nothing is available to copy
- **AND** the GUI SHALL NOT copy warning text as if it were Markdown content

### Requirement: JSON Modal Is Reusable
The shared JSON modal used by Project Web SHALL avoid idea-specific accessible descriptions when it is used by non-idea pages.

#### Scenario: Topic overview opens JSON modal
- **WHEN** the topic overview page opens the shared JSON modal
- **THEN** the modal's accessible description SHALL describe topic overview data rather than selected idea data

