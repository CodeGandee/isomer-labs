## ADDED Requirements

### Requirement: Project Manager Content Root Relocation Guidance
The project manager skill SHALL guide generated content-root relocation through the supported Project CLI command and preserve the runtime repair boundary.

#### Scenario: Relocation request routes to content-root move guidance
- **WHEN** the user asks how to move, rename, or change the Project generated content root after initialization
- **THEN** the project-manager skill routes the request to content-root relocation guidance and uses `isomer-cli project content-root move --to <content-dir>` instead of instructing the operator to hand-edit the Project Manifest

#### Scenario: Guidance starts with dry-run
- **WHEN** the project-manager skill prepares a content-root relocation command
- **THEN** it first runs or recommends `isomer-cli project content-root move --to <content-dir> --dry-run` before any confirmed move

#### Scenario: Guidance explains confirmation
- **WHEN** the project-manager skill describes applying content-root relocation
- **THEN** it explains that actual filesystem and manifest mutation requires `--yes`, and that omitting `--yes` is non-mutating

#### Scenario: Guidance warns about runtime breakage
- **WHEN** content-root relocation may move Topic Workspaces with runtime material or Pixi environments
- **THEN** the skill warns that existing Workspace Runtime records, Pixi environments, installed packages, adapter runtime material, logs, and stored path plans may contain old paths and may require reinstall or reinitialization

#### Scenario: Guidance preserves unknown content
- **WHEN** the old content root contains unknown entries
- **THEN** the skill explains that relocation preserves unmanaged leftovers and does not rename the whole content root as an opaque directory

### Requirement: Project Manager Content Root Relocation Subcommand
The project manager skill SHALL expose a short local subcommand for generated content-root relocation workflows.

#### Scenario: Move content subcommand exists
- **WHEN** the `isomer-admin-project-mgr` skill folder is inspected
- **THEN** it contains a local subcommand page named `move-content` under `references/`

#### Scenario: Help lists move content
- **WHEN** project-manager help lists available subcommands
- **THEN** it includes `move-content` with a concise purpose and expected relocation outputs

#### Scenario: CLI boundary reference includes content-root move
- **WHEN** project-manager CLI boundary guidance is inspected
- **THEN** it includes `isomer-cli project content-root move --to <content-dir> --dry-run` and the confirmed `isomer-cli project content-root move --to <content-dir> --yes` command shape
