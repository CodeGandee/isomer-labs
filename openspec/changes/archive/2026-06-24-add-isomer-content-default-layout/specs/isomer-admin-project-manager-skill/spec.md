## ADDED Requirements

### Requirement: Project Manager Generated Content Layout Guidance
The project manager skill SHALL describe and report the default `isomer-content/` layout created by Project initialization.

#### Scenario: Init project reports content root
- **WHEN** the user asks to initialize an Isomer Project
- **THEN** the `init-project` subcommand reports `.isomer-labs/manifest.toml`, `.isomer-labs/research-topics/<topic-id>.toml`, `isomer-content/`, `isomer-content/topic-ws/<topic-id>/`, `.houmao/`, diagnostics, and next operator action

#### Scenario: Project concepts use new default workspace path
- **WHEN** project-manager references explain the default Topic Workspace path created by `isomer-cli project init <topic-id>`
- **THEN** they name `isomer-content/topic-ws/<topic-id>/` instead of `topic-workspaces/<topic-id>/`

#### Scenario: Content root policy is explained
- **WHEN** project-manager help or initialization guidance describes `isomer-content/`
- **THEN** it explains that `README.md` and `.gitignore` are generated policy files and that generated content under the root is ignored by default unless the user intentionally tracks selected files

#### Scenario: Project config remains separate from content
- **WHEN** project-manager guidance describes Project Config and generated content
- **THEN** it keeps `.isomer-labs/` as the Project Config Directory and `isomer-content/` as the default generated-content root
