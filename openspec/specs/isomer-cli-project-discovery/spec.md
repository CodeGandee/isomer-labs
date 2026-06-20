# isomer-cli-project-discovery Specification

## Purpose
TBD - created by archiving changes implement-isomer-cli-project-discovery and refactor-isomer-cli-to-click. Update Purpose after archive.
## Requirements
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

### Requirement: Project Initialization
The system SHALL initialize the smallest valid Isomer-managed Project configuration without creating Workspace Runtime state.

#### Scenario: Initialize default project
- **WHEN** a user runs `isomer-cli init` in a directory without `.isomer-labs/manifest.toml`
- **THEN** the system creates `.isomer-labs/manifest.toml`, one registered Research Topic Config for Research Topic id `default`, and one project-local Topic Workspace directory at `topic-workspaces/default/`

#### Scenario: Initialize explicit topic
- **WHEN** a user runs `isomer-cli init` with an explicit Research Topic id
- **THEN** the system uses that id for the Research Topic registration, Research Topic Config path, and default Topic Workspace directory name

#### Scenario: Initialize does not create runtime database
- **WHEN** `isomer-cli init` completes
- **THEN** the system does not create `state.sqlite` or any Workspace Runtime database

#### Scenario: Existing project is not overwritten
- **WHEN** a user runs `isomer-cli init` in a Project that already has `.isomer-labs/manifest.toml`
- **THEN** the system refuses to overwrite the existing Project Manifest and does not offer a force-overwrite behavior in Milestone 1

### Requirement: Project Discovery
The system SHALL discover the active Project before resolving topic-scoped command behavior.

#### Scenario: Explicit project selector wins
- **WHEN** a user provides an explicit Project root or Project Manifest selector
- **THEN** the system loads that Project before checking the current directory or environment-derived Project fallbacks

#### Scenario: Current directory discovers project
- **WHEN** a user runs `isomer-cli` from inside a directory tree containing an ancestor `.isomer-labs/manifest.toml`
- **THEN** the system resolves that ancestor as the Project root and loads its Project Manifest

#### Scenario: Project environment fallback is used
- **WHEN** no explicit Project selector or current-directory Project applies and a supported Project environment override is set
- **THEN** the system treats that override as the candidate Project source and reports the source in diagnostic or JSON output

#### Scenario: Missing project is rejected
- **WHEN** no explicit selector, current-directory discovery, or supported Project environment override resolves a Project Manifest
- **THEN** the system rejects project-scoped and topic-scoped commands with a validation diagnostic instead of creating implicit Project state

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

### Requirement: Topic Listing and Workspace Listing
The system SHALL list registered Research Topics and Topic Workspaces from the Project Manifest without scanning unregistered directories.

#### Scenario: Topics list uses manifest registrations
- **WHEN** a user runs `isomer-cli topics list`
- **THEN** the output includes only Research Topics registered by the Project Manifest

#### Scenario: Workspace list uses manifest registrations and defaults
- **WHEN** a user runs `isomer-cli workspaces list`
- **THEN** the output includes Project Manifest-registered Topic Workspaces and valid built-in default Topic Workspace paths derivable for registered Research Topics

#### Scenario: Unregistered topic config files are ignored
- **WHEN** `.isomer-labs/research-topics/` contains TOML files that are not registered by the Project Manifest
- **THEN** `isomer-cli topics list` does not treat those files as managed Research Topics

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

### Requirement: Workspace Path Preview
The system SHALL preview Workspace Path Resolution outputs without creating Workspace Runtime state.

#### Scenario: Path preview shows topic workspace defaults
- **WHEN** a user runs `isomer-cli paths preview` for a registered Research Topic without a configured Topic Workspace path
- **THEN** the output derives the Topic Workspace path as `<project>/topic-workspaces/<topic-id>/` and labels the source as `default`

#### Scenario: Path preview applies precedence
- **WHEN** a path surface has candidates from a supported `ISOMER_*` path override, Project Manifest default, and built-in default
- **THEN** the preview applies the Milestone 1 precedence of environment, manifest, then default and reports the chosen source

#### Scenario: Recorded plan source is unavailable in Milestone 1
- **WHEN** `isomer-cli paths preview` runs before Workspace Runtime and recorded workspace plans are implemented
- **THEN** the command does not report any resolved path as coming from a recorded plan source

#### Scenario: Path preview validates bounds
- **WHEN** a resolved path points outside the Project root
- **THEN** the preview rejects the path without applying an external-root allowlist in Milestone 1

#### Scenario: Path preview is side-effect free
- **WHEN** `isomer-cli paths preview` resolves Topic Workspace, Workspace Runtime, Artifact, Run, log, View Manifest, or Agent Workspace paths
- **THEN** the command does not create `state.sqlite`, Run directories, Artifact directories, Agent Workspace directories, or View Manifest directories by default

### Requirement: Built-In Schema Listing
The system SHALL expose the built-in schema and contract names known to the Milestone 1 implementation.

#### Scenario: Schema list is project scoped or project independent
- **WHEN** a user runs `isomer-cli schemas list`
- **THEN** the system lists the Isomer built-in schema or contract names available for validation without requiring a selected Research Topic

#### Scenario: Schema list excludes OpenSpec planning names
- **WHEN** a user runs `isomer-cli schemas list`
- **THEN** the system does not list OpenSpec capability names, active change names, or planning artifact names by default

#### Scenario: Schema list does not copy built-ins into project config
- **WHEN** `isomer-cli schemas list` runs
- **THEN** the command does not create schema files under `.isomer-labs/`

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

### Requirement: Click Command Registration
The system SHALL implement the Milestone 1 `isomer-cli` command surface with Click command groups while preserving the established Project discovery command behavior.

#### Scenario: Root command is Click backed
- **WHEN** the package exposes `isomer-cli` through `isomer_labs.cli:main`
- **THEN** the command dispatch uses a Click command group rather than an `argparse` parser tree

#### Scenario: Existing commands remain available
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help still lists `init`, `validate`, `topics list`, `workspaces list`, `context show`, `paths preview`, and `schemas list`

#### Scenario: Existing command outputs remain compatible
- **WHEN** a user runs `validate`, `topics list`, `workspaces list`, `context show`, `paths preview`, or `schemas list` with JSON output requested
- **THEN** the command emits the same versioned JSON contract shape used by the Milestone 1 project-discovery implementation

#### Scenario: Domain diagnostics remain Isomer diagnostics
- **WHEN** Project discovery, Project Manifest validation, Research Topic Config validation, Effective Topic Context resolution, or Workspace Path Resolution fails
- **THEN** the command reports stable Isomer diagnostics rather than replacing domain validation failures with Click parser errors

### Requirement: Profile Write Output Contract
The system SHALL produce deterministic text and JSON output for Topic Agent Team Profile specialization previews and writes.

#### Scenario: Profile preview reports no written path
- **WHEN** a user runs `isomer-cli team-profiles specialize` without `--write` and requests JSON
- **THEN** the output includes the candidate profile, validation report, and `written_path` as null

#### Scenario: Profile write reports written path
- **WHEN** a user runs `isomer-cli team-profiles specialize --write` and requests JSON
- **THEN** the output includes the candidate profile, validation report, non-null `written_path`, and a deterministic `registration_suggestion` object

#### Scenario: Profile write does not mutate manifest
- **WHEN** `team-profiles specialize --write` writes a profile file
- **THEN** the Project Manifest and Research Topic Config files are unchanged unless a future explicit registration command or flag is added

### Requirement: Fixture Project Validation Commands
The system SHALL validate milestone fixture Projects through the public CLI surfaces used by normal Projects.

#### Scenario: Fixture Project validate command is deterministic
- **WHEN** the validation suite runs `isomer-cli validate --json` against the Milestone 2 and 3 fixture Project
- **THEN** the output has deterministic JSON and reports no diagnostics for the positive fixture

#### Scenario: Fixture template commands are deterministic
- **WHEN** the validation suite runs `team-templates list`, `team-templates inspect`, and `team-templates validate` against fixture Projects
- **THEN** the output has deterministic text and JSON for built-in and project-local template refs

#### Scenario: Fixture profile commands are deterministic
- **WHEN** the validation suite runs `team-profiles specialize` and `team-profiles validate` against fixture Projects
- **THEN** the output has deterministic text and JSON for preview, write, and validation flows

### Requirement: Milestone Documentation Completion
The system SHALL document the completed Milestone 2 and 3 command surface and fixture expectations.

#### Scenario: Developer docs describe template and profile completion
- **WHEN** Milestone 2 and 3 are completed
- **THEN** README or developer notes describe `team-templates`, `team-profiles`, fixture Project expectations, no-launch boundaries, and profile write semantics

#### Scenario: Roadmap reflects verified completion
- **WHEN** all Milestone 2 and 3 verification commands pass
- **THEN** ROADMAP Milestone 2 and 3 checklist items are marked complete without marking Milestone 4 or Houmao launch work complete

