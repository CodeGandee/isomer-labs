## MODIFIED Requirements

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
