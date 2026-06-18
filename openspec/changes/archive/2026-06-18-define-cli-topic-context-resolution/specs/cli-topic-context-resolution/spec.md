## ADDED Requirements

### Requirement: Project Discovery for CLI Commands
The system SHALL make `isomer-cli` discover the active Project from an explicit project selector, the current working directory, or a supported Project environment override before it resolves topic-scoped command behavior.

#### Scenario: Explicit project selector wins
- **WHEN** `isomer-cli` receives an explicit Project root or Project Manifest selector
- **THEN** the system resolves the Project from that selector before checking the current working directory or environment-derived fallbacks

#### Scenario: Current directory discovers project
- **WHEN** `isomer-cli` is invoked from inside a Project tree with a `.isomer-labs/manifest.toml`
- **THEN** the system resolves that directory tree as the Project and loads the Project Manifest as the discovery authority

#### Scenario: Missing project is rejected
- **WHEN** `isomer-cli` cannot resolve a Project Manifest from explicit selectors, current directory discovery, or supported environment overrides
- **THEN** the system rejects topic-scoped commands with a validation error instead of creating implicit Project state

### Requirement: Project Manifest Registers Research Topic Config
The system SHALL use the Project Manifest to register Research Topics, their Research Topic Config TOML paths, and their Topic Workspace refs.

#### Scenario: Research topic registration is declared
- **WHEN** the Project Manifest declares a Research Topic for `isomer-cli`
- **THEN** the declaration includes a stable Research Topic id, Research Topic Config path, Topic Workspace ref, status, and schema version or compatible manifest version

#### Scenario: Topic config path is project scoped
- **WHEN** the Project Manifest points to a Research Topic Config file
- **THEN** the system resolves the config path relative to the Project root and rejects paths outside the Project unless a later accepted external-root policy permits them

#### Scenario: Topic workspace ref is required
- **WHEN** a registered Research Topic is used for topic-scoped commands
- **THEN** the system requires a matching Topic Workspace ref in the Project Manifest or a valid built-in default derivable through Workspace Path Resolution

#### Scenario: Topic discovery does not scan directories
- **WHEN** `.isomer-labs/research-topics/` or another directory contains TOML files not registered by the Project Manifest
- **THEN** the system does not treat those files as managed Research Topic Configs for topic-scoped commands

### Requirement: Research Topic Config Content
The system SHALL define Research Topic Config TOML as topic-specific configuration for defaults and refs, not as Workspace Runtime state.

#### Scenario: Topic config identifies its topic
- **WHEN** a Research Topic Config is loaded
- **THEN** the system requires its `research_topic_id` to match the Project Manifest Research Topic registration that referenced it

#### Scenario: Topic config can carry topic defaults
- **WHEN** a Research Topic Config is inspected
- **THEN** it may define topic statement text or refs, Measurable Objective text or refs, default Research Inquiry refs, default Topic Agent Team Profile refs, default Execution Adapter refs, default Control Mode, Capability Binding refs, Gate policy refs, Artifact Format Profile defaults, and Artifact Extension refs

#### Scenario: Topic statement can be inline and artifact-backed
- **WHEN** a Research Topic Config describes the Research Topic
- **THEN** it may include one short inline `topic_statement` for discovery, CLI previews, and human review, plus `topic_statement_artifact_refs` or other explicit Artifact refs for richer or evolving topic material

#### Scenario: Topic statement refs do not make config runtime state
- **WHEN** Research Topic Config references richer topic briefs, user notes, rationale, source notes, or objective material as Artifacts
- **THEN** the config stores only refs to those Artifacts and does not embed their rich content as authoritative Workspace Runtime state

#### Scenario: Topic config does not own runtime truth
- **WHEN** a Research Topic Config contains Run status, command outputs, live process ids, resolved command results, Artifact contents, Evidence Items, Findings, Gates, Decision Records, or Provenance Records as authoritative state
- **THEN** validation reports the config as invalid and directs those facts to Workspace Runtime or file-backed Artifacts

#### Scenario: Topic config does not store secrets
- **WHEN** a Research Topic Config contains inline credentials, tokens, API keys, passwords, or secret material
- **THEN** validation reports the config as invalid and directs the value to a credential backend or a Capability Binding ref

### Requirement: Effective Topic Context
The system SHALL resolve an Effective Topic Context before `isomer-cli` performs a topic-scoped command.

#### Scenario: Effective context contains core refs
- **WHEN** `isomer-cli` resolves Effective Topic Context
- **THEN** the context includes Project root, Project Config Directory, Project Manifest path, Research Topic id, Research Topic Config path, Topic Workspace id, Topic Workspace path input, schema versions, and resolution source metadata

#### Scenario: Effective context carries optional lifecycle refs
- **WHEN** the user or environment selects a Research Inquiry, Research Task, Run, Agent Team Instance, Agent Instance, or Topic Agent Team Profile
- **THEN** the context carries those refs only after validating that they belong to the selected Research Topic and Topic Workspace

#### Scenario: Effective context carries defaults and bindings
- **WHEN** Research Topic Config or Project Manifest defaults name Topic Agent Team Profiles, Execution Adapters, Capability Binding refs, Control Mode defaults, or Gate policy refs
- **THEN** the context exposes those values as defaults for the current command without treating unresolved provider, Skill Binding, command execution, scheduler, baseline-waiver, cost, or privacy policy schemas as settled

#### Scenario: Effective context carries artifact format defaults
- **WHEN** Research Topic Config, Research Task expected outputs, or explicit command context names Artifact Format Profile defaults or Artifact Extension refs
- **THEN** the context exposes those refs for expected output planning and Artifact recording without making them mandatory core Artifact fields

#### Scenario: Effective context is process input
- **WHEN** Effective Topic Context is produced
- **THEN** the system treats it as a resolved process input for `isomer-cli`, Workspace Path Resolution, Run initialization, and future Execution Adapter command requests, not as a replacement for Research Lifecycle State or Workspace Runtime records

#### Scenario: Run records store refs and resolution sources
- **WHEN** a Run, Run plan, or future Execution Adapter command request consumes Effective Topic Context
- **THEN** the durable record stores validated refs, resolution source metadata, and consumed config or default versions instead of storing the full Effective Topic Context snapshot

#### Scenario: Stored context refs remain bounded
- **WHEN** the durable record stores context refs from Effective Topic Context
- **THEN** it may include selected Project, Research Topic, Research Topic Config, Topic Workspace, Research Inquiry, Research Task, Run, Topic Agent Team Profile, Agent Team Instance, Agent Instance, Execution Adapter, Capability Binding, Gate policy, Artifact Format Profile, and Artifact Extension refs that influenced the action

#### Scenario: Stored context sources are explainable
- **WHEN** a context ref or default is stored for audit
- **THEN** the record identifies whether it came from an explicit selector, current directory, supported environment variable, `.isomer-labs/local.toml`, Project Manifest default, Research Topic Config, Topic Agent Team Profile, Domain Agent Team Template, built-in default, or Workspace Runtime record

### Requirement: Topic Selection Precedence
The system SHALL select the Research Topic for topic-scoped commands through deterministic precedence.

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

#### Scenario: Ambiguous selection is rejected
- **WHEN** selectors, environment values, active context, or manifest refs imply conflicting Research Topics, Topic Workspaces, Research Tasks, Runs, Agent Team Instances, or Agent Instances
- **THEN** the system rejects the command with a validation error that names the conflicting sources

### Requirement: Topic Context Environment Variables
The system SHALL support a bounded set of `ISOMER_*` environment variables for launch-time topic-context identity refs.

#### Scenario: Supported identity variables are recognized
- **WHEN** an Execution Adapter or user process exports `ISOMER_RESEARCH_TOPIC_ID`, `ISOMER_TOPIC_WORKSPACE_ID`, `ISOMER_RESEARCH_INQUIRY_ID`, `ISOMER_RESEARCH_TASK_ID`, `ISOMER_RUN_ID`, `ISOMER_AGENT_TEAM_INSTANCE_ID`, or `ISOMER_AGENT_INSTANCE_ID`
- **THEN** `isomer-cli` treats those values as candidate identity refs according to topic selection precedence and validation rules

#### Scenario: Identity variables are not path variables
- **WHEN** a supported topic-context identity variable is set
- **THEN** the system does not use that value to resolve filesystem paths except through validated Research Topic, Topic Workspace, Research Task, Run, Agent Team Instance, or Agent Instance refs

#### Scenario: Unknown context variables are ignored
- **WHEN** an environment variable is not part of the supported topic-context identity set or the accepted Workspace Path Resolution override set
- **THEN** the system does not use that variable to resolve Effective Topic Context or workspace paths

#### Scenario: Environment source is reported
- **WHEN** a topic-context value comes from an environment variable
- **THEN** the Effective Topic Context records the environment source and downstream durable records store validated refs rather than treating the environment value as durable truth

### Requirement: Topic Context Validation
The system SHALL validate Effective Topic Context before Run creation, Execution Adapter dispatch, or Workspace Runtime mutation.

#### Scenario: Topic refs are consistent
- **WHEN** Effective Topic Context includes Research Topic, Topic Workspace, Research Inquiry, Research Task, Run, Agent Team Instance, or Agent Instance refs
- **THEN** validation confirms those refs belong to the same Project and Research Topic or reports a context mismatch

#### Scenario: Topic config schema is checked
- **WHEN** a Research Topic Config is loaded
- **THEN** validation checks its schema version, required fields, allowed field classes, path bounds, and ref consistency before the config can influence topic-scoped command behavior

#### Scenario: Missing references are reported
- **WHEN** Effective Topic Context references a missing Research Topic Config, Topic Workspace, Topic Agent Team Profile, Capability Binding ref, Gate policy ref, Research Task, Run, Agent Team Instance, or Agent Instance
- **THEN** validation reports the missing ref and blocks only the command behavior that depends on that ref

#### Scenario: Validation preserves unresolved surfaces
- **WHEN** Effective Topic Context names unresolved command execution, scheduler, Skill Binding, baseline-waiver, cost/privacy, credential, or provider surfaces
- **THEN** validation permits registered placeholder refs or opaque refs without inventing those contracts in CLI topic context resolution

### Requirement: Topic Artifact Format Defaults
The system SHALL allow Research Topic Config and more-specific output specs to select optional Artifact Format Profiles and Artifact Extensions for topic-specific Artifact content.

#### Scenario: Project manifest registers artifact format profiles
- **WHEN** the Project Manifest registers an Artifact Format Profile or Artifact Extension for topic use
- **THEN** the registration includes a stable id, project-scoped path or built-in ref, scope, and compatibility version or schema version

#### Scenario: Topic config selects artifact format defaults
- **WHEN** Research Topic Config defines Artifact Format Profile defaults by Artifact kind
- **THEN** `isomer-cli` treats those defaults as topic-specific expected-output guidance for matching Artifact kinds

#### Scenario: Output spec overrides topic default
- **WHEN** a Research Task expected output or explicit Run or command context selects an Artifact Format Profile for one output
- **THEN** the system uses that output-specific selection before checking Research Topic Config, Topic Agent Team Profile, Domain Agent Team Template, or built-in Artifact kind defaults

#### Scenario: Extensions are additive
- **WHEN** Research Topic Config enables Artifact Extensions
- **THEN** validation treats the extensions as additive topic metadata and rejects extensions that shadow or redefine core Artifact fields

#### Scenario: Unknown format degrades to generic artifact handling
- **WHEN** an Artifact Format Profile or Artifact Extension is missing, unsupported, disabled, or unknown
- **THEN** the system can still list, locate, display generically, and validate the core Artifact record while reporting the unresolved format or extension as a workspace issue

#### Scenario: Format profile does not define command execution
- **WHEN** an Artifact Format Profile names validation, rendering, or export behavior that needs concrete command execution
- **THEN** the profile only carries declarative hints and opaque future capability refs, while concrete command execution remains governed by the future Execution Adapter command surface

### Requirement: CLI Command Scope Boundaries
The system SHALL distinguish project-scoped, topic-scoped, and run-scoped `isomer-cli` command behavior in the first implementation.

#### Scenario: Project-scoped command families do not require topic
- **WHEN** a command validates or inspects the Project Manifest, lists registered Research Topics, lists Topic Workspaces, inspects built-in schemas, or checks project-level config without selecting one Research Topic
- **THEN** the command may run with Project context only and does not require Effective Topic Context

#### Scenario: Topic-scoped command families require topic context
- **WHEN** a command shows or validates Effective Topic Context, creates or inspects Research Inquiries, Research Tasks, Artifacts, Gates, Topic Agent Team Profiles, Agent Team Instance topic-participation records, topic-scoped views, or topic-specific path previews
- **THEN** the command resolves and validates Effective Topic Context before performing the action

#### Scenario: Run-scoped command families require run consistency
- **WHEN** a command inspects, resumes, cancels, records, or exports a Run
- **THEN** the command validates that the selected Run belongs to the selected Research Task, Research Inquiry, Research Topic, and Topic Workspace

#### Scenario: Workspace path commands use project or topic scope
- **WHEN** a command lists registered Topic Workspaces
- **THEN** the command remains project-scoped
- **AND WHEN** a command previews or resolves paths for one selected Topic Workspace
- **THEN** the command is topic-scoped and resolves Effective Topic Context

#### Scenario: Command request remains out of scope
- **WHEN** `isomer-cli` prepares to execute a shell command, package manager command, HPC job, notebook action, agent launch, or service request
- **THEN** this contract supplies Effective Topic Context but does not define the concrete Execution Adapter command request, scheduler behavior, or cost/privacy Gate thresholds
