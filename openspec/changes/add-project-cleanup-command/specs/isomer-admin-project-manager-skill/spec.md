## ADDED Requirements

### Requirement: Project Manager Cleanup Guidance
The project manager skill SHALL guide explicit Project cleanup through the supported `isomer-cli project cleanup` command surface without bypassing dry-run review or Isomer path-safety rules.

#### Scenario: Cleanup request routes to cleanup guidance
- **WHEN** the user asks to remove Isomer-managed Project material, reset Project bootstrap material, or prepare a Project root for reinitialization
- **THEN** the project-manager skill routes the request to cleanup guidance and uses `isomer-cli project cleanup` instead of instructing the operator to delete directories by hand

#### Scenario: Cleanup guidance starts with dry-run
- **WHEN** the project-manager skill prepares a cleanup command
- **THEN** it first runs or recommends `isomer-cli project cleanup --dry-run` with the selected parts before any command that can delete files

#### Scenario: Cleanup guidance explains confirmation
- **WHEN** the project-manager skill describes applying cleanup
- **THEN** it explains that actual deletion requires `--yes`, and that omitting `--yes` is non-mutating

#### Scenario: Cleanup guidance supports partial removal
- **WHEN** the user asks to remove only Project config, only the Project-level Houmao overlay, only content-root policy files, a selected Topic Workspace, runtime material, or the full content root
- **THEN** the skill selects the corresponding cleanup part and preserves unrelated Isomer-managed material

#### Scenario: Cleanup guidance preserves unknown content by default
- **WHEN** cleanup involves the selected generated content root
- **THEN** the skill explains that unknown files under the content root are preserved unless the user explicitly chooses content-root purge behavior

#### Scenario: Reinitialization guidance stays explicit
- **WHEN** the user wants to rerun `isomer-cli project init` after an existing manifest blocks initialization
- **THEN** the skill tells the user to review and apply cleanup first, then rerun `isomer-cli project init` only after the blocking Project Manifest has been removed

### Requirement: Project Manager Cleanup Subcommand
The project manager skill SHALL expose a short local cleanup subcommand for Project cleanup workflows.

#### Scenario: Cleanup project subcommand exists
- **WHEN** the `isomer-admin-project-mgr` skill folder is inspected
- **THEN** it contains a local subcommand page named `cleanup-project` under `references/`

#### Scenario: Help lists cleanup project
- **WHEN** project-manager help lists available subcommands
- **THEN** it includes `cleanup-project` with a concise purpose and expected cleanup outputs

#### Scenario: CLI boundary reference includes cleanup
- **WHEN** project-manager CLI boundary guidance is inspected
- **THEN** it includes `isomer-cli project cleanup --part <part> --dry-run` and the confirmed `isomer-cli project cleanup --part <part> --yes` command shape
