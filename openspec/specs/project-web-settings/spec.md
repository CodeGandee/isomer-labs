# project-web-settings Specification

## Purpose
TBD - created by archiving change add-project-settings-theme-page. Update Purpose after archive.
## Requirements
### Requirement: Project settings openable item
The system SHALL expose a project-level settings item from the web GUI project explorer.

#### Scenario: User opens settings from project explorer
- **WHEN** the project explorer is loaded
- **THEN** it includes an openable `Settings` item for the project
- **AND** opening that item resolves to a `Project Settings` workbench tab descriptor

### Requirement: Project settings workbench tab
The system SHALL render project settings as a workbench tab that does not require a selected topic.

#### Scenario: User opens settings without selecting a topic
- **WHEN** no research topic is selected
- **AND** the user opens the project settings item
- **THEN** the workbench displays the `Project Settings` tab instead of the empty topic-only state

### Requirement: Global theme preference
The settings tab SHALL provide a global theme selector for `system`, `light`, and `dark`.

#### Scenario: User changes theme mode
- **WHEN** the user selects a theme mode in project settings
- **THEN** the GUI applies the selected mode immediately
- **AND** stores the preference as browser-local frontend state

#### Scenario: User reloads the GUI
- **WHEN** the user reloads the GUI after selecting a theme mode
- **THEN** the GUI initializes with the previously stored browser-local theme mode

### Requirement: Settings navigation history
The system SHALL use the same openable item history behavior for project settings as other semantic workbench tabs.

#### Scenario: User navigates back after opening settings
- **WHEN** the user opens `Project Settings` from the workbench
- **AND** the user presses browser Back
- **THEN** the URL and active tab return to the prior workbench state

