## ADDED Requirements

### Requirement: Project Manager CLI Namespace Guidance
The project manager skill SHALL use `isomer-cli project ...` as the canonical command shape for Project-targeted CLI guidance.

#### Scenario: Help names project namespace
- **WHEN** project-manager help describes supported Isomer CLI command surfaces
- **THEN** it explains that Project-targeted commands live under `isomer-cli project`

#### Scenario: CLI boundary examples use project namespace
- **WHEN** the project-manager CLI boundary reference lists command examples
- **THEN** Project-scoped commands use shapes such as `isomer-cli project init`, `isomer-cli project validate`, `isomer-cli project doctor`, `isomer-cli project runtime init`, and `isomer-cli project cleanup --dry-run`

#### Scenario: Project selector examples use root option
- **WHEN** project-manager guidance selects a Project root explicitly
- **THEN** it uses `isomer-cli project --root <project-root> <subcmd>` as the canonical selector shape

#### Scenario: Ancestor discovery is explained
- **WHEN** project-manager guidance explains Project resolution
- **THEN** it says `isomer-cli project <subcmd>` starts at cwd and walks parent directories until it finds `.isomer-labs/manifest.toml` or fails

#### Scenario: Root-level project commands are not taught
- **WHEN** project-manager skill text or local references are inspected
- **THEN** they do not present root-level Project command shapes such as `isomer-cli init`, `isomer-cli validate`, or `isomer-cli runtime init` as canonical usage

## MODIFIED Requirements

### Requirement: Project Lifecycle Subcommands
The project manager skill SHALL guide Project lifecycle commands without bypassing Isomer CLI validation or Houmao CLI boundaries.

#### Scenario: Init project guides Isomer and Houmao bootstrap
- **WHEN** the user asks to initialize an Isomer Project
- **THEN** the skill routes to `init-project`, uses the supported `isomer-cli project init` command shape, and reports the resulting `.isomer-labs/` Project config and `.houmao/` Project-level Houmao overlay status

#### Scenario: Check project remains read-only
- **WHEN** the user asks to check, diagnose, or validate an existing Project
- **THEN** the skill routes to `check-project`, uses read-only `isomer-cli project validate`, `isomer-cli project doctor`, and related diagnostics commands, and includes Houmao project status checks without launching, stopping, or messaging managed agents

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
