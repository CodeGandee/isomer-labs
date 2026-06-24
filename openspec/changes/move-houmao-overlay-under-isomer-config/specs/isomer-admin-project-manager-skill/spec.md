## MODIFIED Requirements

### Requirement: Project Manager Help Behavior
The project manager skill SHALL explain its purpose and usage when invoked for help or without a prompt.

#### Scenario: Help subcommand prints usage
- **WHEN** the user invokes the local `help` subcommand
- **THEN** the skill prints what `isomer-admin-project-mgr` does, how to invoke it, available subcommands, expected outputs, and guardrails

#### Scenario: Empty invocation defaults to help
- **WHEN** the skill is invoked without a prompt
- **THEN** the entrypoint selects `help` and prints the same usage output

#### Scenario: Purpose is plain text
- **WHEN** operator documentation or skill text describes the workflow
- **THEN** it explains in plain text that the skill initializes and manages an Isomer Project by coordinating Project config, Research Topics, Topic Workspaces, Workspace Runtime preparation, and the Isomer-managed Project-level Houmao overlay under `.isomer-labs/`

### Requirement: Project Lifecycle Subcommands
The project manager skill SHALL guide Project lifecycle commands without bypassing Isomer CLI validation or Houmao CLI boundaries.

#### Scenario: Init project guides Isomer and Houmao bootstrap
- **WHEN** the user asks to initialize an Isomer Project
- **THEN** the skill routes to `init-project`, uses the supported `isomer-cli project init` command shape, and reports the resulting `.isomer-labs/` Project config and `.isomer-labs/.houmao/` Isomer-managed Houmao overlay status

#### Scenario: Check project remains read-only
- **WHEN** the user asks to check, diagnose, or validate an existing Project
- **THEN** the skill routes to `check-project`, uses read-only `isomer-cli project validate`, `isomer-cli project doctor`, and related diagnostics commands, and includes Isomer-managed Houmao project status checks without launching, stopping, or messaging managed agents

#### Scenario: Topic listing uses CLI surfaces
- **WHEN** the user asks what Research Topics or Topic Workspaces are available
- **THEN** the skill routes to `list-topics` and uses `isomer-cli project topics list` and `isomer-cli project workspaces list` rather than scanning unregistered directories as authority

#### Scenario: Context inspection uses Effective Topic Context
- **WHEN** the user asks which Project, Research Topic, Topic Workspace, template, profile, or runtime refs are selected
- **THEN** the skill routes to `show-context` and uses `isomer-cli project context show` or equivalent read-only context resolution surfaces

#### Scenario: Runtime init stays explicit
- **WHEN** the user asks to create or open Workspace Runtime state
- **THEN** the skill routes to `init-runtime` and preserves the explicit `isomer-cli project runtime init` boundary for creating `state.sqlite` and runtime directories

#### Scenario: Runtime preparation stays explicit
- **WHEN** the user asks to prepare launch-facing readiness
- **THEN** the skill routes to `prep-runtime` and preserves the explicit `isomer-cli project runtime prepare` and `project runtime validate --require-ready-readiness` boundaries

#### Scenario: Cleanup project stays explicit
- **WHEN** the user asks to remove Isomer-managed Project material or prepare a Project root for reinitialization
- **THEN** the skill routes to cleanup guidance that uses `isomer-cli project cleanup --dry-run` before any confirmed cleanup command

#### Scenario: Topic team specialization is handed off
- **WHEN** the user asks to adapt, instantiate, or specialize a Domain Agent Team Template for a Research Topic
- **THEN** the skill routes to `specialize-team`, resolves enough Project context with `isomer-cli project ...` command surfaces, and hands off to `isomer-admin-topic-team-specialize` instead of duplicating Topic Team Specialization logic

### Requirement: Project Manager Generated Content Layout Guidance
The project manager skill SHALL describe and report the default `isomer-content/` layout created by Project initialization.

#### Scenario: Init project reports content root
- **WHEN** the user asks to initialize an Isomer Project
- **THEN** the `init-project` subcommand reports `.isomer-labs/manifest.toml`, `.isomer-labs/research-topics/<topic-id>.toml`, `isomer-content/`, `isomer-content/topic-ws/<topic-id>/`, `.isomer-labs/.houmao/`, diagnostics, and next operator action

#### Scenario: Project concepts use new default workspace path
- **WHEN** project-manager references explain the default Topic Workspace path created by `isomer-cli project init <topic-id>`
- **THEN** they name `isomer-content/topic-ws/<topic-id>/` instead of `topic-workspaces/<topic-id>/`

#### Scenario: Content root policy is explained
- **WHEN** project-manager help or initialization guidance describes `isomer-content/`
- **THEN** it explains that `README.md` and `.gitignore` are generated policy files and that generated content under the root is ignored by default unless the user intentionally tracks selected files

#### Scenario: Project config remains separate from content
- **WHEN** project-manager guidance describes Project Config and generated content
- **THEN** it keeps `.isomer-labs/` as the Project Config Directory, `.isomer-labs/.houmao/` as the Isomer-managed Houmao overlay, and `isomer-content/` as the default generated-content root

### Requirement: Project Manager Custom Content Directory Guidance
The project manager skill SHALL describe and use the optional Project initialization content directory selector when the user wants generated Isomer content outside the default `isomer-content/` root.

#### Scenario: Init project accepts content directory request
- **WHEN** the user asks to initialize an Isomer Project with a custom generated content directory
- **THEN** the `init-project` subcommand includes `--content-dir <content-dir>` in the supported `isomer-cli project init` command shape instead of instructing the operator to hand-edit `.isomer-labs/manifest.toml`

#### Scenario: Init project reports custom content root
- **WHEN** Project initialization succeeds with a custom content directory
- **THEN** the `init-project` subcommand reports the selected generated content root, its generated `README.md` and `.gitignore` policy files, the derived `<content-dir>/topic-ws/<topic-id>/` Topic Workspace path, `.isomer-labs/manifest.toml`, `.isomer-labs/research-topics/<topic-id>.toml`, `.isomer-labs/.houmao/`, diagnostics, and next operator action

#### Scenario: Help explains content directory option
- **WHEN** project-manager help or CLI boundary guidance describes fresh Project initialization
- **THEN** it explains that omitting `--content-dir` uses `isomer-content/`, while supplying `--content-dir <content-dir>` chooses a project-local generated content root and derives the default Topic Workspace base as `<content-dir>/topic-ws`

#### Scenario: Guardrails preserve project-local content
- **WHEN** project-manager guidance describes content directory choices
- **THEN** it says generated content roots must stay inside the Project root, must not live inside `.isomer-labs/`, and must not be used to initialize runtime or live Houmao state
