## ADDED Requirements

### Requirement: On-demand Jinja2 Record Rendering
The artifact-format processing system SHALL render Markdown from structured payload files on demand through resolved Jinja2 templates.

#### Scenario: Record render reads payload file
- **WHEN** a caller requests Markdown for a structured research record
- **THEN** the renderer reads the managed JSON payload file, validates or checks its recorded digest, resolves the selected template, and returns rendered Markdown content

#### Scenario: Render does not create durable file by default
- **WHEN** a caller renders a structured research record as Markdown for display
- **THEN** the renderer returns content to the CLI, API, or GUI without writing a generated Markdown file unless the caller explicitly requests export

#### Scenario: Explicit export writes generated artifact
- **WHEN** a caller explicitly exports rendered Markdown to a file
- **THEN** the system records the export as a generated artifact with source record id, payload digest, template ref, template digest when known, output locator, output digest, and provenance refs

#### Scenario: Template remains a view transform
- **WHEN** a Jinja2 template renders structured research payload JSON
- **THEN** the template produces display content and does not define lifecycle identity, revision policy, query-index ownership, or durable payload storage
