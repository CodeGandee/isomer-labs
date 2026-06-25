## MODIFIED Requirements

### Requirement: Topic Selection Precedence
The system SHALL select the Research Topic for topic-scoped commands through deterministic precedence and SHALL treat a Project with no registered Research Topics as a valid Project that cannot satisfy topic-scoped selection.

#### Scenario: Explicit selectors have highest precedence
- **WHEN** the user provides explicit selectors such as `--topic`, `--topic-workspace`, `--task`, or `--run`
- **THEN** the system selects the Research Topic implied by those selectors before checking current directory, environment variables, local active context, or Project Manifest defaults

#### Scenario: Current directory can select topic workspace
- **WHEN** `isomer-cli` is invoked from within a Project Manifest-registered Topic Workspace and no explicit selector is provided
- **THEN** the system selects the Research Topic associated with that Topic Workspace

#### Scenario: Environment can select context
- **WHEN** no explicit selector or current-directory Topic Workspace applies and supported topic-context environment variables are set
- **THEN** the system uses those environment values as candidate context refs after validating them against the Project Manifest and Research Topic Config

#### Scenario: Local active context can select topic
- **WHEN** no explicit selector, current-directory Topic Workspace, or supported topic-context environment variable applies and untracked `.isomer-labs/local.toml` is present
- **THEN** the system uses the local active context as a candidate Research Topic selection after validating it against the Project Manifest

#### Scenario: Local active context is local convenience state
- **WHEN** `.isomer-labs/local.toml` is present
- **THEN** the file may contain only candidate active Research Topic, Topic Workspace, Research Inquiry, Research Task, and Run identity refs plus schema version, and it is not treated as shared project truth or authoritative Workspace Runtime state

#### Scenario: Local active context cannot store runtime truth or secrets
- **WHEN** `.isomer-labs/local.toml` contains Run status, command outputs, live process ids, resolved command results, Artifact contents, Evidence Items, Findings, Gates, Decision Records, Provenance Records, credentials, tokens, API keys, passwords, or secret material
- **THEN** validation rejects those fields or refuses to load the local active context

#### Scenario: Manifest default is final fallback
- **WHEN** no higher-precedence source selects a Research Topic and the Project Manifest defines a default Research Topic
- **THEN** the system selects the Project Manifest default Research Topic

#### Scenario: Empty project has no topic fallback
- **WHEN** no higher-precedence source selects a Research Topic and the Project Manifest registers no Research Topics
- **THEN** topic-scoped selection fails with a deterministic diagnostic that tells the user to create a Research Topic with `isomer-cli project topics create`

#### Scenario: Ambiguous selection is rejected
- **WHEN** selectors, environment values, active context, or manifest refs imply conflicting Research Topics, Topic Workspaces, Research Tasks, Runs, Agent Team Instances, or Agent Instances
- **THEN** the system rejects the command with a validation error that names the conflicting sources

### Requirement: CLI Command Scope Boundaries
The system SHALL distinguish project-scoped, topic-scoped, run-scoped, and extension-backed `isomer-cli` command behavior in the first implementation.

#### Scenario: Project-scoped command families do not require topic
- **WHEN** a command validates or inspects the Project Manifest, lists registered Research Topics, lists Topic Workspaces, inspects built-in schemas, creates a Research Topic, shows a Research Topic registration, deletes a Research Topic with a dry-run plan, or checks project-level config without selecting one Research Topic
- **THEN** the command may run with Project context only and does not require Effective Topic Context

#### Scenario: Project-scoped commands work in empty project
- **WHEN** a Project Manifest has no registered Research Topics
- **THEN** Project-scoped commands that do not select one Research Topic can still validate, inspect, list, and mutate Project-level topic registration state according to their command contracts

#### Scenario: Topic-scoped command families require topic context
- **WHEN** a command shows or validates Effective Topic Context, creates or inspects Research Inquiries, Research Tasks, Artifacts, Gates, Topic Agent Team Profiles, Agent Team Instance topic-participation records, topic-scoped views, or topic-specific path previews
- **THEN** the command resolves and validates Effective Topic Context before performing the action

#### Scenario: Topic-scoped command reports empty project
- **WHEN** a topic-scoped command runs in a Project with no registered Research Topics and no explicit valid topic context
- **THEN** the command returns a deterministic diagnostic that no Research Topic is registered and does not create placeholder topic material

#### Scenario: Run-scoped command families require run consistency
- **WHEN** a command inspects, resumes, cancels, records, or exports a Run
- **THEN** the command validates that the selected Run belongs to the selected Research Task, Research Inquiry, Research Topic, and Topic Workspace

#### Scenario: Workspace path commands use project or topic scope
- **WHEN** a command lists registered Topic Workspaces
- **THEN** the command remains project-scoped
- **AND WHEN** a command previews or resolves paths for one selected Topic Workspace
- **THEN** the command is topic-scoped and resolves Effective Topic Context

#### Scenario: Extension-backed commands use execution extension contract
- **WHEN** `isomer-cli` prepares to execute a shell command, package manager command, HPC job, notebook action, literature provider request, document build, figure render, service request, agent launch, baseline-waiver check, or other provider-backed operation
- **THEN** this contract supplies and validates Effective Topic Context while the Research Execution and Extension Contract defines the command request, extension refs, preflight, scheduler boundary, provider binding, and recording obligations
