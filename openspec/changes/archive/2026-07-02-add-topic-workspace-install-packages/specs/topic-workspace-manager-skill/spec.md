## MODIFIED Requirements

### Requirement: Command-Style Subcommand Structure
The topic workspace manager skill SHALL use a lean top-level router, grouped short kebab-case subcommands, and one-level executable reference pages.

#### Scenario: Entrypoint routes by subcommand
- **WHEN** an agent invokes `isomer-admin-topic-workspace-mgr`
- **THEN** the top-level `SKILL.md` selects one subcommand from grouped subcommand tables and loads only the selected reference page before executing that page's `## Workflow`

#### Scenario: Default subcommand runs full flow
- **WHEN** the user invokes the skill without a subcommand and does not ask for help
- **THEN** the skill selects `topic-workspace` as the default full preparation flow

#### Scenario: Public subcommands exist
- **WHEN** the skill lists public subcommands
- **THEN** it includes procedural subcommands `resolve-workspace`, `ensure-main-repo`, `manage-actors`, `plan-agents`, `create-worktrees`, `write-boundaries`, `create-agent-branch`, `validate-worktrees`, `install-packages`, and `summarize`
- **AND** it includes misc subcommands `help` and `topic-workspace`

#### Scenario: Subcommand pages have workflows
- **WHEN** an executable reference page is inspected
- **THEN** it has a near-top `## Workflow` section with numbered steps and a freeform fallback for tasks that do not map cleanly to the default steps

## ADDED Requirements

### Requirement: Topic Workspace Package Installation Subcommand
The topic workspace manager skill SHALL provide `install-packages` as the operator-owned package installation route for the selected Topic Workspace.

#### Scenario: Install packages subcommand is listed
- **WHEN** `isomer-admin-topic-workspace-mgr` lists procedural subcommands
- **THEN** it includes `install-packages`
- **AND** the subcommand points to `references/install-packages.md`

#### Scenario: Package installation remains topic scoped
- **WHEN** `install-packages` receives a package request
- **THEN** it resolves the selected Project, Research Topic, Topic Workspace, Topic Workspace Pixi manifest, and Pixi environment before mutation
- **AND** it refuses to mutate a Project-root Pixi environment, Agent Workspace-specific environment, ambient virtual environment, system package manager, or machine-global runtime as the package target

#### Scenario: Install packages owns mutation evidence
- **WHEN** `install-packages` installs, skips, defers, or blocks a requested package
- **THEN** it reports the selected install route, commands run, verification commands, changed files, already-present packages, blockers, and next safe action

### Requirement: Flexible Package Request Intake
The `install-packages` subcommand SHALL accept package requests from user prompts or description files without requiring a formal schema-constrained config file.

#### Scenario: Plain prompt package request is accepted
- **WHEN** a user invokes `install-packages` with plain text such as `install matplotlib scipy for Python paper figures`
- **THEN** the subcommand infers package names, package kind, purpose, install route, and verification checks from the prompt
- **AND** it does not require the user to provide YAML, JSON, or another fixed request schema before proceeding

#### Scenario: Markdown description file is accepted
- **WHEN** a user invokes `install-packages` with a Markdown file that describes missing packages, purpose, and desired checks
- **THEN** the subcommand extracts package requirements and verification intent from the Markdown
- **AND** it proceeds with an inferred install plan or reports a blocker when the description is ambiguous

#### Scenario: Structured files are accepted but optional
- **WHEN** a user invokes `install-packages` with YAML, JSON, TOML, or requirements-style package content
- **THEN** the subcommand reads the structured content when possible
- **AND** it treats the structured file as an input convenience rather than a mandatory schema contract

#### Scenario: Copied blocker text is accepted
- **WHEN** a research skill hands off copied blocker text that names missing packages or runtime checks
- **THEN** `install-packages` infers the package request from that text
- **AND** it preserves the requester skill and task purpose in the install report when available

#### Scenario: Ambiguous request blocks before mutation
- **WHEN** the package request could map to multiple incompatible packages, languages, or install routes
- **THEN** the subcommand reports a blocker or asks a targeted clarification before mutating the Topic Workspace environment

### Requirement: Pixi-Based Install Planning and Verification
The `install-packages` subcommand SHALL infer a concrete Pixi-based install and verification plan from the package request.

#### Scenario: Python libraries install into topic Pixi env
- **WHEN** a package request names importable Python libraries needed by the Topic Workspace runnable target
- **THEN** `install-packages` plans installation into the selected Topic Workspace Pixi environment
- **AND** verification uses Pixi-scoped Python import, version, or behavior checks

#### Scenario: Native or Conda packages use Pixi route
- **WHEN** a package request names a native tool, binary runtime, Conda-preferred package, or non-Python command-line dependency
- **THEN** `install-packages` plans a Pixi/Conda route for the selected Topic Workspace environment when available
- **AND** verification checks the executable, version, import, or task-specific behavior through Pixi-scoped commands

#### Scenario: R package requests stay workspace scoped
- **WHEN** a package request names R packages for an R backend
- **THEN** `install-packages` plans a workspace-scoped R package route
- **AND** it blocks rather than using an unrecorded user R library, system R mutation, or cross-backend fallback

#### Scenario: Verification is generated when absent
- **WHEN** the request does not provide explicit verification commands
- **THEN** `install-packages` generates appropriate verification checks such as Python imports, R library loads, CLI version checks, minimal file generation, or task-specific smoke checks

#### Scenario: Install success alone is insufficient
- **WHEN** package installation commands complete
- **THEN** the subcommand still runs or records verification checks
- **AND** it reports readiness only when verification passes or records an explicit blocker or deferral

### Requirement: Package Installation Guardrails
The `install-packages` subcommand SHALL enforce Topic Workspace package mutation boundaries.

#### Scenario: Local virtual environment creation is rejected
- **WHEN** a package request suggests creating a local `venv`, `.venv`, `virtualenv`, or ambient Python environment
- **THEN** `install-packages` rejects that route for Topic Workspace package mutation
- **AND** it converts the request to a Topic Workspace Pixi environment route or reports a blocker

#### Scenario: Ambient pip is rejected
- **WHEN** a package request suggests `pip install` outside the selected Topic Workspace Pixi environment
- **THEN** `install-packages` rejects the ambient install route
- **AND** it uses Pixi-managed package mutation or reports why the package cannot be installed safely

#### Scenario: Privileged host mutation is rejected
- **WHEN** a package request requires `sudo`, a system package manager, global shell profile edits, daemon installs, kernel driver changes, `/etc` mutation, or other privileged host changes
- **THEN** `install-packages` reports a blocker
- **AND** it does not create an executable command for the privileged mutation

#### Scenario: Heavy setup is bounded
- **WHEN** installation or verification may involve heavy compilation, large downloads, GPU jobs, broad tests, or unknown resource risk
- **THEN** `install-packages` records bounded-run or resource-risk guidance before running the heavy path
- **AND** it reports a blocker when the host cannot safely run the bounded verification
