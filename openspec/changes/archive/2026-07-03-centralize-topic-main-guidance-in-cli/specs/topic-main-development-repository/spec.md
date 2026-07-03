## ADDED Requirements

### Requirement: Topic Main Guidance Source of Truth
The system SHALL treat the `isomer-cli project topic-main-guidance` renderer, backed by a packaged `.j2` template asset, as the source of truth for root `AGENTS.md` and `CLAUDE.md` Isomer guidance in Topic Main Development Repository.

#### Scenario: Rule files use CLI-rendered content
- **WHEN** Topic Workspace environment setup or Topic Manager repair writes topic-main agent guidance
- **THEN** the written block is produced by `isomer-cli project topic-main-guidance` behavior
- **AND** skill documentation does not own a separate full copy of the guidance prose

#### Scenario: Template remains topic independent
- **WHEN** the packaged guidance template is rendered
- **THEN** rendered content contains placeholders or command forms for `manifest_path`, `pixi_environment`, and semantic labels
- **AND** rendered content does not contain concrete selected-topic values

#### Scenario: Topic main stores rendered files only
- **WHEN** root `AGENTS.md` or `CLAUDE.md` contains the Isomer-managed guidance block
- **THEN** the repository stores rendered Markdown files
- **AND** the canonical editable template remains in the installed Isomer package assets, not inside the Topic Main Development Repository
