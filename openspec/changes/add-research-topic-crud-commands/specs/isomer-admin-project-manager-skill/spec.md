## ADDED Requirements

### Requirement: Project Manager Topic CRUD Guidance
The project manager skill SHALL describe Research Topic creation, inspection, update, and deletion through the supported `isomer-cli project topics` command surface.

#### Scenario: Help lists topic CRUD boundary
- **WHEN** project-manager help describes topic lifecycle operations
- **THEN** it names `isomer-cli project topics create`, `show`, `update`, `delete --dry-run`, and `delete --yes` as the authoritative Project Manifest mutation surfaces for Research Topics

#### Scenario: Init project points to topic creation
- **WHEN** `init-project` completes successfully
- **THEN** the skill reports that the Project has no Research Topic until the user runs `isomer-cli project topics create` or the topic-team specialization flow routes through that command

#### Scenario: Delete guidance is plan-first
- **WHEN** the user asks the project-manager skill to remove a Research Topic
- **THEN** the skill starts with `isomer-cli project topics delete <topic-id> --dry-run` and uses `--yes` only after the user reviews the plan

## MODIFIED Requirements

### Requirement: Project Manager Generated Content Layout Guidance
The project manager skill SHALL describe and report the default `isomer-content/` layout created by Project initialization without claiming that Project initialization creates a Research Topic or Topic Workspace.

#### Scenario: Init project reports content root
- **WHEN** the user asks to initialize an Isomer Project
- **THEN** the `init-project` subcommand reports `.isomer-labs/manifest.toml`, `isomer-content/`, generated content-root policy files, `.isomer-labs/.houmao/`, diagnostics, and next operator action
- **AND** it does not report `.isomer-labs/research-topics/<topic-id>.toml` or `isomer-content/topic-ws/<topic-id>/` as Project init outputs

#### Scenario: Project concepts separate topic workspace creation
- **WHEN** project-manager references explain the default Topic Workspace path
- **THEN** they say Topic Workspaces are created by explicit topic creation such as `isomer-cli project topics create <topic-id> --statement "<research topic>"`, which normally derives `isomer-content/topic-ws/<topic-id>/`

#### Scenario: Content root policy is explained
- **WHEN** project-manager help or initialization guidance describes `isomer-content/`
- **THEN** it explains that `README.md` and `.gitignore` are generated policy files and that generated content under the root is ignored by default unless the user intentionally tracks selected files

#### Scenario: Project config remains separate from content
- **WHEN** project-manager guidance describes Project Config and generated content
- **THEN** it keeps `.isomer-labs/` as the Project Config Directory and `isomer-content/` as the default generated-content root

### Requirement: Project Manager Custom Content Directory Guidance
The project manager skill SHALL describe and use the optional Project initialization content directory selector when the user wants generated Isomer content outside the default `isomer-content/` root, without creating a Topic Workspace during Project initialization.

#### Scenario: Init project accepts content directory request
- **WHEN** the user asks to initialize an Isomer Project with a custom generated content directory
- **THEN** the `init-project` subcommand includes `--content-dir <content-dir>` in the supported `isomer-cli project init` command shape instead of instructing the operator to hand-edit `.isomer-labs/manifest.toml`

#### Scenario: Init project reports custom content root
- **WHEN** Project initialization succeeds with a custom content directory
- **THEN** the `init-project` subcommand reports the selected generated content root, its generated `README.md` and `.gitignore` policy files, `.isomer-labs/manifest.toml`, `.isomer-labs/.houmao/`, diagnostics, and next operator action
- **AND** it does not report a derived `<content-dir>/topic-ws/<topic-id>/` Topic Workspace path as a Project init output

#### Scenario: Help explains content directory option
- **WHEN** project-manager help or CLI boundary guidance describes fresh Project initialization
- **THEN** it explains that omitting `--content-dir` uses `isomer-content/`, while supplying `--content-dir <content-dir>` chooses a project-local generated content root and records the default Topic Workspace base as `<content-dir>/topic-ws` for later topic creation

#### Scenario: Guardrails preserve project-local content
- **WHEN** project-manager guidance describes content directory choices
- **THEN** it says generated content roots must stay inside the Project root, must not live inside `.isomer-labs/`, and must not be used to initialize runtime or live Houmao state
