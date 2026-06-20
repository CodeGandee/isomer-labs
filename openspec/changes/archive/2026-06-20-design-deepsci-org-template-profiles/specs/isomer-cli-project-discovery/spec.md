## MODIFIED Requirements

### Requirement: CLI Entrypoint and Command Surface
The system SHALL provide an installed `isomer-cli` command with Project discovery, template inspection, and Topic Agent Team Profile validation commands.

#### Scenario: CLI exposes project-discovery commands
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help lists `init`, `validate`, `topics list`, `workspaces list`, `context show`, `paths preview`, and `schemas list`

#### Scenario: CLI exposes template and profile commands
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help lists `team-templates` and `team-profiles` command groups

#### Scenario: Project script is installed through package metadata
- **WHEN** the package is installed through the repository's editable Pixi PyPI dependency
- **THEN** the environment can invoke `isomer-cli` as a project script

### Requirement: Manifest and Topic Config Validation
The system SHALL validate the Project Manifest, registered Research Topic Config files, optional local active context, Domain Agent Team Template refs, and Topic Agent Team Profile refs before command behavior depends on them.

#### Scenario: Manifest registers topics and workspaces
- **WHEN** `isomer-cli validate` inspects a Project Manifest
- **THEN** validation confirms that every registered Research Topic has a stable id, schema version or compatible manifest version, Research Topic Config path, and matching Topic Workspace ref or valid built-in Topic Workspace default

#### Scenario: Manifest registers team templates and profiles
- **WHEN** `isomer-cli validate` inspects a Project Manifest with Domain Agent Team Template or Topic Agent Team Profile refs
- **THEN** validation confirms that each template ref has a stable id and project-scoped or built-in source path, and that each profile ref has a stable id, source path, template ref, and Research Topic association

#### Scenario: Duplicate ids are rejected
- **WHEN** the Project Manifest declares duplicate Research Topic ids, duplicate Topic Workspace ids, duplicate Domain Agent Team Template ids, or duplicate Topic Agent Team Profile ids
- **THEN** validation reports each duplicate id as a Project Manifest error

#### Scenario: Topic config path stays project scoped
- **WHEN** a Research Topic Config path resolves outside the Project root
- **THEN** validation rejects the path without applying an external-root allowlist in Milestone 1

#### Scenario: Team profile path stays project scoped
- **WHEN** a Topic Agent Team Profile path resolves outside the Project root or into a Topic Workspace `teams/` directory
- **THEN** validation rejects the path and reports the Project Manifest or Research Topic Config source that declared it

#### Scenario: Topic config id must match manifest registration
- **WHEN** a registered Research Topic Config is loaded
- **THEN** validation confirms that its `research_topic_id` matches the Research Topic registration that referenced it

#### Scenario: Topic config profile default must match selected topic
- **WHEN** a Research Topic Config declares a default Topic Agent Team Profile ref
- **THEN** validation confirms that the referenced profile belongs to the same Research Topic and specializes a registered Domain Agent Team Template

#### Scenario: Runtime truth is rejected from config
- **WHEN** a Research Topic Config, Topic Agent Team Profile, or `.isomer-labs/local.toml` contains Run status, command outputs, live process ids, resolved command results, rich Artifact contents, Evidence Items, Findings, Gates, Decision Records, Provenance Records, mailbox state, gateway state, or scheduler internals as authoritative state
- **THEN** validation rejects those fields and directs the user to future Workspace Runtime or adapter-backed Artifact surfaces

#### Scenario: Secret material is rejected from config
- **WHEN** a Project Manifest, Research Topic Config, Topic Agent Team Profile, or `.isomer-labs/local.toml` contains inline credentials, tokens, API keys, passwords, or secret material
- **THEN** validation reports the field as invalid and does not expose the secret value in normal diagnostic output

### Requirement: Effective Topic Context Inspection
The system SHALL resolve and display Effective Topic Context for topic-scoped commands, including selected team template and profile defaults when available.

#### Scenario: Context show includes core refs
- **WHEN** a user runs `isomer-cli context show` with a resolvable Research Topic
- **THEN** the output includes Project root, Project Config Directory, Project Manifest path, Research Topic id, Research Topic Config path, Topic Workspace id, Topic Workspace path input, schema versions, selected Domain Agent Team Template refs, selected Topic Agent Team Profile refs, and source metadata

#### Scenario: Topic selection precedence is deterministic
- **WHEN** explicit selectors, current-directory Topic Workspace selection, supported identity environment refs, `.isomer-labs/local.toml`, and Project Manifest defaults are all available
- **THEN** the system selects the Research Topic using that precedence order and reports the selected source

#### Scenario: Team profile selection precedence is deterministic
- **WHEN** explicit profile selectors, Research Topic Config defaults, Project Manifest defaults, and template defaults are all available
- **THEN** the system selects the Topic Agent Team Profile using that precedence order and reports the selected source

#### Scenario: Ambiguous topic selection is rejected
- **WHEN** selectors, environment refs, local active context, or Project Manifest defaults imply conflicting Research Topics, Topic Workspaces, Research Tasks, Runs, Agent Team Instances, or Agent Instances
- **THEN** the system rejects the command with a diagnostic that names the conflicting sources

#### Scenario: Ambiguous team profile selection is rejected
- **WHEN** selectors, Research Topic Config defaults, Project Manifest defaults, or local active context imply conflicting Topic Agent Team Profiles for one Research Topic
- **THEN** the system rejects the command with a diagnostic that names the conflicting profile sources

#### Scenario: Optional lifecycle refs are validated before display
- **WHEN** context inputs include Research Inquiry, Research Task, Run, Agent Team Instance, Agent Instance, or Topic Agent Team Profile refs
- **THEN** the system includes those refs only after validating that they belong to the selected Research Topic and Topic Workspace or reports that the ref cannot yet be validated without Workspace Runtime support

### Requirement: Diagnostics and Output Formats
The system SHALL produce deterministic diagnostics and machine-readable output for Project discovery, template inspection, and Topic Agent Team Profile commands.

#### Scenario: Diagnostics include stable codes
- **WHEN** validation reports an error
- **THEN** each diagnostic includes a stable code, severity, file path when known, Isomer concept name, and concise message

#### Scenario: Diagnostics avoid leaking secrets
- **WHEN** validation reports a secret-like field
- **THEN** diagnostic output identifies the offending field or path without printing the secret value

#### Scenario: JSON output is deterministic
- **WHEN** a user requests JSON output for `validate`, `topics list`, `workspaces list`, `context show`, `paths preview`, `schemas list`, `team-templates list`, `team-templates inspect`, `team-templates validate`, `team-profiles specialize`, or `team-profiles validate`
- **THEN** the command emits deterministic JSON suitable for unit tests and future Operator Agent consumption

#### Scenario: JSON output is versioned but provisional
- **WHEN** a user requests JSON output from a command added for template registration or Topic Agent Team Profile specialization
- **THEN** the response includes an output schema version and is treated as a developer contract rather than a durable public research-record API
