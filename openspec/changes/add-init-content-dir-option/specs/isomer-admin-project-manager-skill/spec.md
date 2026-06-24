## ADDED Requirements

### Requirement: Project Manager Custom Content Directory Guidance
The project manager skill SHALL describe and use the optional Project initialization content directory selector when the user wants generated Isomer content outside the default `isomer-content/` root.

#### Scenario: Init project accepts content directory request
- **WHEN** the user asks to initialize an Isomer Project with a custom generated content directory
- **THEN** the `init-project` subcommand includes `--content-dir <content-dir>` in the supported `isomer-cli project init` command shape instead of instructing the operator to hand-edit `.isomer-labs/manifest.toml`

#### Scenario: Init project reports custom content root
- **WHEN** Project initialization succeeds with a custom content directory
- **THEN** the `init-project` subcommand reports the selected generated content root, its generated `README.md` and `.gitignore` policy files, the derived `<content-dir>/topic-ws/<topic-id>/` Topic Workspace path, `.isomer-labs/manifest.toml`, `.isomer-labs/research-topics/<topic-id>.toml`, `.houmao/`, diagnostics, and next operator action

#### Scenario: Help explains content directory option
- **WHEN** project-manager help or CLI boundary guidance describes fresh Project initialization
- **THEN** it explains that omitting `--content-dir` uses `isomer-content/`, while supplying `--content-dir <content-dir>` chooses a project-local generated content root and derives the default Topic Workspace base as `<content-dir>/topic-ws`

#### Scenario: Guardrails preserve project-local content
- **WHEN** project-manager guidance describes content directory choices
- **THEN** it says generated content roots must stay inside the Project root, must not live inside `.isomer-labs/`, and must not be used to initialize runtime or live Houmao state
