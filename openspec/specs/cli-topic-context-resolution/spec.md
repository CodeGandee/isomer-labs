# cli-topic-context-resolution Specification

## Purpose
Define how `isomer-cli` discovers a Project, resolves topic-specific command context, loads Research Topic Config TOML, exposes Effective Topic Context to path resolution and future execution surfaces, and keeps topic-specific artifact customization declarative and optional.
## Requirements
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
The system SHALL define Research Topic Config TOML as topic-specific configuration for defaults and refs, not as Project-level environment binding policy or Workspace Runtime state.

#### Scenario: Topic config identifies its topic
- **WHEN** a Research Topic Config is loaded
- **THEN** the system requires its `research_topic_id` to match the Project Manifest Research Topic registration that referenced it

#### Scenario: Topic config can carry topic defaults
- **WHEN** a Research Topic Config is inspected
- **THEN** it may define topic statement text or refs, Measurable Objective text or refs, default Research Inquiry refs, default Topic Agent Team Profile refs, default Execution Adapter refs, default Control Mode, Capability Binding refs, Skill Binding projection refs, Research Operation Extension Point refs, Gate policy refs, scheduler policy refs, baseline-waiver policy refs, literature provider refs, Artifact Format Profile defaults, and Artifact Extension refs

#### Scenario: Topic config does not own Pixi environment bindings
- **WHEN** a Research Topic Config is loaded
- **THEN** validation treats Project-level Pixi environment bindings as Project Manifest-owned refs and does not infer them from Research Topic Config fields or Pixi environment names

#### Scenario: Topic statement can be inline and artifact-backed
- **WHEN** a Research Topic Config describes the Research Topic
- **THEN** it may include one short inline `topic_statement` for discovery, CLI previews, and human review, plus `topic_statement_artifact_refs` or other explicit Artifact refs for richer or evolving topic material

#### Scenario: Topic statement refs do not make config runtime state
- **WHEN** Research Topic Config references richer topic briefs, user notes, rationale, source notes, or objective material as Artifacts
- **THEN** the config stores only refs to those Artifacts and does not embed their rich content as authoritative Workspace Runtime state

#### Scenario: Topic config does not own runtime truth
- **WHEN** a Research Topic Config contains Run status, command outputs, live process ids, resolved command results, Artifact contents, Evidence Items, Findings, Gates, Decision Records, Provenance Records, environment readiness status, Pixi install output, prepared environment paths, or Project-level Pixi environment bindings as authoritative state
- **THEN** validation reports the config as invalid and directs those facts to Workspace Runtime or file-backed Artifacts

#### Scenario: Topic config does not store secrets
- **WHEN** a Research Topic Config contains inline credentials, tokens, API keys, passwords, or secret material
- **THEN** validation reports the config as invalid and directs the value to a credential backend or a Capability Binding ref

#### Scenario: Topic config extension refs are declarative
- **WHEN** a Research Topic Config names Research Operation Extension Point refs, Capability Binding refs, Skill Binding projection refs, literature provider refs, baseline-waiver policy refs, scheduler policy refs, cost/privacy Gate policy refs, or Execution Adapter refs
- **THEN** validation treats those values as declarative refs for later command, provider, policy, and skill availability resolution and does not execute or dereference provider-specific implementation bodies while loading the config

#### Scenario: Topic config does not replace team profile binding
- **WHEN** a Research Topic Config names topic-level defaults for extension refs, provider refs, policy refs, or Execution Adapter refs
- **THEN** validation keeps role-scoped, Workflow Stage-scoped, skill-availability, operation-authority, Project-level topic environment bindings, and per-agent environment-divergence details in Project Manifest, Topic Agent Team Profile, Capability Binding, Skill Binding projection, Workspace Runtime readiness records, or Service Request material rather than treating Research Topic Config as the complete execution binding

### Requirement: Project Manifest Topic Environment Bindings
The system SHALL let the Project Manifest explicitly record which Project-root Pixi environment or environments each Research Topic uses without inferring topic relationships from Pixi environment names.

#### Scenario: Topic environment bindings use repeated manifest tables
- **WHEN** the Project Manifest declares `[[topic_pixi_environment_bindings]]`
- **THEN** each binding identifies `research_topic_id`, `pixi_environment`, optional `purpose`, and optional `status`

#### Scenario: Topic environment names are not semantic bindings
- **WHEN** a Project-level Pixi environment name resembles a Research Topic id, topic slug, role, stage, or purpose label
- **THEN** validation does not treat that name as a Research Topic binding unless the Project Manifest explicitly records the binding

#### Scenario: One topic can use multiple Pixi environments
- **WHEN** the Project Manifest contains multiple active `topic_pixi_environment_bindings` entries for the same Research Topic and different Pixi environment names
- **THEN** Effective Topic Context and `doctor` preserve the explicit set of bound environment refs for later readiness checks and runtime preparation

#### Scenario: Standalone Pixi isolation bindings use a separate manifest table
- **WHEN** the Project Manifest declares `[[topic_standalone_pixi_bindings]]`
- **THEN** each binding identifies `research_topic_id`, Project-root-relative `manifest_path`, optional `pixi_environment`, optional `purpose`, and optional `status`

#### Scenario: Standalone Pixi isolation is explicit opt-in
- **WHEN** a Topic Workspace contains a `pixi.toml`, `pyproject.toml`, or other Pixi-looking file
- **THEN** validation does not treat the Topic Workspace as using standalone Pixi isolation unless the Project Manifest explicitly records a `topic_standalone_pixi_bindings` entry for that Research Topic

#### Scenario: Standalone Pixi manifest path stays inside the Project
- **WHEN** the Project Manifest declares `topic_standalone_pixi_bindings.manifest_path`
- **THEN** validation requires the path to resolve inside the Project root and reports a Project Manifest diagnostic for absolute or relative paths that escape the Project

#### Scenario: Topic environment binding references registered topic
- **WHEN** a Project Manifest topic Pixi environment binding names `research_topic_id`
- **THEN** validation requires the id to match a registered Research Topic in the same Project Manifest

#### Scenario: Duplicate active topic environment binding is rejected
- **WHEN** the Project Manifest contains duplicate active `topic_pixi_environment_bindings` entries for the same `research_topic_id`, `pixi_environment`, and `purpose`
- **THEN** validation reports a Project Manifest diagnostic rather than treating the duplicate rows as separate environment uses

#### Scenario: Duplicate active standalone binding is rejected
- **WHEN** the Project Manifest contains duplicate active `topic_standalone_pixi_bindings` entries for the same `research_topic_id`, `manifest_path`, `pixi_environment`, and `purpose`
- **THEN** validation reports a Project Manifest diagnostic rather than treating the duplicate rows as separate standalone uses

### Requirement: Effective Topic Context
The system SHALL resolve an Effective Topic Context before `isomer-cli` performs a topic-scoped command.

#### Scenario: Effective context contains core refs
- **WHEN** `isomer-cli` resolves Effective Topic Context
- **THEN** the context includes Project root, Project Config Directory, Project Manifest path, Research Topic id, Research Topic Config path, Topic Workspace id, Topic Workspace path input, schema versions, and resolution source metadata

#### Scenario: Effective context carries optional lifecycle refs
- **WHEN** the user or environment selects a Research Inquiry, Research Task, Run, Agent Team Instance, Agent Instance, or Topic Agent Team Profile
- **THEN** the context carries those refs only after validating that they belong to the selected Research Topic and Topic Workspace

#### Scenario: Effective context carries defaults and extension refs
- **WHEN** Research Topic Config or Project Manifest defaults name Topic Agent Team Profiles, Execution Adapters, Capability Binding refs, Skill Binding projection refs, Research Operation Extension Point refs, Control Mode defaults, scheduler policy refs, baseline-waiver policy refs, literature provider refs, or Gate policy refs
- **THEN** the context exposes those values as refs for the current command without treating them as command outputs, runtime truth, credentials, provider payloads, or implementation bodies

#### Scenario: Effective context carries artifact format defaults
- **WHEN** Research Topic Config, Research Task expected outputs, or explicit command context names Artifact Format Profile defaults or Artifact Extension refs
- **THEN** the context exposes those refs for expected output planning and Artifact recording without making them mandatory core Artifact fields

#### Scenario: Effective context is process input
- **WHEN** Effective Topic Context is produced
- **THEN** the system treats it as a resolved process input for `isomer-cli`, Workspace Path Resolution, Run initialization, Execution Adapter Command Requests, and provider-backed extension operations, not as a replacement for Research Lifecycle State or Workspace Runtime records

#### Scenario: Run records store refs and resolution sources
- **WHEN** a Run, Run plan, Execution Adapter Command Request, or provider-backed extension operation consumes Effective Topic Context
- **THEN** the durable record stores validated refs, resolution source metadata, and consumed config or default versions instead of storing the full Effective Topic Context snapshot

#### Scenario: Stored context refs remain bounded
- **WHEN** the durable record stores context refs from Effective Topic Context
- **THEN** it may include selected Project, Research Topic, Research Topic Config, Topic Workspace, Research Inquiry, Research Task, Run, Topic Agent Team Profile, Agent Team Instance, Agent Instance, Execution Adapter, Capability Binding, Skill Binding projection, Research Operation Extension Point, scheduler policy, baseline-waiver policy, literature provider, Gate policy, Artifact Format Profile, and Artifact Extension refs that influenced the action

#### Scenario: Stored context sources are explainable
- **WHEN** a context ref or default is stored for audit
- **THEN** the record identifies whether it came from an explicit selector, current directory, supported environment variable, `.isomer-labs/local.toml`, Project Manifest default, Research Topic Config, Topic Agent Team Profile, Domain Agent Team Template, built-in default, Workspace Runtime record, or explicit command context

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
The system SHALL validate Effective Topic Context before Run creation, Execution Adapter dispatch, provider-backed extension dispatch, or Workspace Runtime mutation.

#### Scenario: Topic refs are consistent
- **WHEN** Effective Topic Context includes Research Topic, Topic Workspace, Research Inquiry, Research Task, Run, Agent Team Instance, or Agent Instance refs
- **THEN** validation confirms those refs belong to the same Project and Research Topic or reports a context mismatch

#### Scenario: Topic config schema is checked
- **WHEN** a Research Topic Config is loaded
- **THEN** validation checks its schema version, required fields, allowed field classes, path bounds, ref consistency, and extension-ref field classes before the config can influence topic-scoped command behavior

#### Scenario: Missing references are reported
- **WHEN** Effective Topic Context references a missing Research Topic Config, Topic Workspace, Topic Agent Team Profile, Capability Binding ref, Skill Binding projection ref, Research Operation Extension Point ref, Gate policy ref, scheduler policy ref, baseline-waiver policy ref, literature provider ref, Research Task, Run, Agent Team Instance, or Agent Instance
- **THEN** validation reports the missing ref and blocks only the command behavior that depends on that ref

#### Scenario: Validation preserves provider-neutral boundaries
- **WHEN** Effective Topic Context names execution, scheduler, Skill Binding, baseline-waiver, cost/privacy, credential, literature provider, or data-export extension refs
- **THEN** validation confirms those refs are syntactically valid and leaves provider-specific implementation behavior to the accepted Research Execution and Extension Contract and selected provider or adapter

#### Scenario: Validation rejects inline implementation bodies
- **WHEN** Effective Topic Context or its source config includes inline provider-specific command bodies, credentials, tokens, API keys, live process state, command outputs, provider payloads, or scheduler internals
- **THEN** validation rejects those fields and directs them to the appropriate adapter payload ref, credential backend, Workspace Runtime record, Artifact, or Provenance Record

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

### Requirement: Effective Agent Context
The system SHALL resolve an Effective Agent Context for agent-scoped commands and semantic path queries when enough validated agent identity information is available.

#### Scenario: Explicit agent selector wins
- **WHEN** a user provides an explicit Agent Name, Agent Workspace, or Agent Instance selector for an agent-scoped command
- **THEN** the system uses that selector before checking environment context or cwd inference

#### Scenario: Environment agent context is used
- **WHEN** no explicit agent selector is provided and supported agent identity environment variables select an Agent Name, Agent Workspace, or Agent Instance
- **THEN** the system uses the environment context after validating it against the selected Topic Workspace

#### Scenario: Cwd inside Agent Workspace infers agent
- **WHEN** no explicit or environment agent context is provided
- **AND** `isomer-cli` runs from a cwd inside a known Agent Workspace for the selected Topic Workspace
- **THEN** the system infers Effective Agent Context from that Agent Workspace

#### Scenario: Missing agent context is explicit
- **WHEN** an agent-scoped command cannot resolve explicit, environment-derived, cwd-derived, or recorded agent context
- **THEN** the system reports that the command requires an Agent Name or Agent Instance selector

### Requirement: Cwd-derived Agent Workspace Matching
The system SHALL infer agent context from cwd only when cwd matches a known or uniquely derivable Agent Workspace.

#### Scenario: Runtime path plan match wins
- **WHEN** Workspace Runtime contains Agent Workspace path plans and cwd is inside exactly one recorded Agent Workspace path
- **THEN** cwd inference uses the matching Agent Workspace record and may expose both Agent Name and Agent Instance id

#### Scenario: Manifest template match is used without runtime
- **WHEN** Workspace Runtime has no matching Agent Workspace record and the Topic Workspace Manifest has a unique `agent.workspace` template that matches cwd
- **THEN** cwd inference may derive Agent Name from the template without claiming an Agent Instance id

#### Scenario: Manifest template captures one agent segment
- **WHEN** cwd inference uses a manifest `agent.workspace` template
- **THEN** the system canonicalizes cwd and the template, captures exactly one path segment for `{agent_name}`, and treats the instantiated template path as the Agent Workspace root

#### Scenario: Unsupported template does not infer cwd agent
- **WHEN** a manifest `agent.workspace` template has no `{agent_name}` placeholder, more than one `{agent_name}` placeholder, or a placeholder that would capture multiple path segments
- **THEN** cwd-derived agent inference reports that the template cannot be used for reverse matching instead of guessing

#### Scenario: Default layout match is used when applicable
- **WHEN** no runtime or manifest match exists and the default layout profile is active
- **THEN** cwd inside `<topic-workspace>/agents/<agent-name>` may derive Agent Name from the default Agent Workspace path shape

#### Scenario: Topic Main Repository is not an Agent Workspace
- **WHEN** cwd is inside the Topic Main Repository owner checkout such as `repos/topic-main`
- **THEN** the system does not infer Effective Agent Context from cwd

#### Scenario: Nested cwd keeps owning agent
- **WHEN** cwd is inside a subdirectory of one Agent Workspace
- **THEN** cwd inference resolves to that owning Agent Workspace rather than requiring cwd to equal the workspace root

### Requirement: Agent Context Conflict Handling
The system SHALL report conflicts between explicit selectors, environment context, cwd inference, and runtime records instead of silently guessing.

#### Scenario: Explicit selector overrides cwd
- **WHEN** cwd is inside Agent Workspace `alice` and the user explicitly selects Agent Name `bob`
- **THEN** the command uses `bob` and reports source metadata showing the explicit selector won

#### Scenario: Environment and cwd conflict blocks implicit selection
- **WHEN** environment context selects Agent Name `alice` and cwd inference selects Agent Name `bob`
- **AND** the user does not provide an explicit agent selector
- **THEN** the system reports an agent context conflict diagnostic

#### Scenario: Ambiguous cwd match is rejected
- **WHEN** cwd matches more than one active Agent Workspace binding with incompatible Agent Names or Agent Instance ids
- **THEN** the system rejects cwd-derived agent context as ambiguous

#### Scenario: Cross-topic cwd conflict is rejected
- **WHEN** cwd matches an Agent Workspace under a different registered Topic Workspace than the selected Topic Workspace
- **THEN** the system reports a context mismatch instead of using the other topic's agent context

### Requirement: Effective Agent Context Output
The CLI SHALL expose agent context source metadata when a command resolves or displays Effective Topic Context.

#### Scenario: Context show reports inferred agent
- **WHEN** `isomer-cli project context show` runs from inside a known Agent Workspace and no explicit agent selector is supplied
- **THEN** the output includes the inferred Agent Name, Agent Workspace path, source `cwd`, and Agent Instance id when runtime records provide it

#### Scenario: Path query reports agent source
- **WHEN** an agent-scoped semantic path query resolves by cwd inference
- **THEN** the result includes the resolved Agent Name and source `cwd`

#### Scenario: Topic-only context remains topic-only
- **WHEN** cwd is inside a Topic Workspace but not inside an Agent Workspace
- **THEN** Effective Topic Context may be resolved without adding Effective Agent Context

### Requirement: Progressive Agent Self Query Context
The system SHALL expose process-local self queries as selectable, read-only slices rather than one large default packet.

#### Scenario: Self show is a small index
- **WHEN** `isomer-cli --print-json project self show` runs with resolvable Project context
- **THEN** the response includes only a minimal summary with selected Research Topic and Topic Workspace refs when available, resolved Topic Actor or Agent headline when available, diagnostic counts, and available self query subcommands
- **AND** it does not include full environment listings, broad semantic path lists, full Pixi binding candidates, or recommended query catalogs

#### Scenario: Identity query reports identity only
- **WHEN** `isomer-cli --print-json project self identity` runs from inside the selected Topic Main Development Repository
- **AND** supported launch environment variables provide `ISOMER_RESEARCH_TOPIC_ID` and `ISOMER_AGENT_INSTANCE_ID` or `ISOMER_AGENT_NAME`
- **THEN** the response includes Effective Topic Context identity, Topic Actor context when resolved, Effective Agent Context when resolved, and source metadata
- **AND** the command does not infer Agent Workspace identity from the Topic Main Development Repository cwd
- **AND** it does not include Pixi binding details, semantic path payloads beyond identity-adjacent refs, or broad environment listings

#### Scenario: Self query reports topic actor context only in identity slice
- **WHEN** supported environment variables, cwd, recorded context, or a single manifest default identify a Topic Actor
- **THEN** `project self identity` includes the resolved Topic Actor name, workspace path, binding metadata when available, and source metadata
- **AND** `project self show` includes at most the Topic Actor name and source headline

#### Scenario: Self query degrades without agent identity
- **WHEN** Effective Topic Context resolves but no explicit, environment-derived, cwd-derived, or recorded Effective Agent Context is available
- **THEN** `project self show` reports that Agent identity is unresolved without expanding a full diagnostic packet
- **AND** `project self identity` reports how to provide `--agent`, `--agent-instance`, `ISOMER_AGENT_NAME`, or `ISOMER_AGENT_INSTANCE_ID`

#### Scenario: Self query reports conflicts instead of guessing
- **WHEN** environment identity, explicit selectors, cwd inference, recorded runtime refs, or manifest defaults conflict
- **THEN** the relevant self subcommand reports diagnostics that name the conflicting sources
- **AND** it does not silently choose an Agent Name, Agent Instance, Topic Actor, Research Topic, or Topic Workspace from the conflicting inputs

### Requirement: Agent Self Environment Query
The system SHALL expose recognized Isomer launch environment inputs only through an explicit environment self query.

#### Scenario: Env query reports recognized safe names by default
- **WHEN** `isomer-cli --print-json project self env` runs
- **THEN** the response reports recognized Isomer identity, path, or non-secret configuration variable names, classes, presence, and whether each value influenced resolution
- **AND** it omits values by default
- **AND** it does not include arbitrary environment variables, credentials, tokens, API keys, passwords, or secret-like values

#### Scenario: Env query values require explicit safe-value request
- **WHEN** `project self env` supports a value-emitting option
- **THEN** values are emitted only for allowlisted non-secret identity, path, or configuration refs
- **AND** secret-like variables remain omitted or redacted even when value output is requested

### Requirement: Agent Self Path and Pixi Queries
The system SHALL expose semantic path and Pixi details only through explicit self query subcommands.

#### Scenario: Paths query resolves requested labels only
- **WHEN** a caller runs `isomer-cli --print-json project self paths topic.repos.main agent.workspace`
- **THEN** the response includes only the requested semantic labels and diagnostics needed to resolve them
- **AND** each path entry includes the semantic label, resolved path when available, source, storage profile metadata when available, and diagnostics
- **AND** the command does not include unrelated common paths or a full semantic path catalog

#### Scenario: Paths query requires at least one label
- **WHEN** a caller runs `project self paths` without a semantic label
- **THEN** the command reports that at least one label is required
- **AND** it points callers to `project self queries` or `project paths list` for discovery instead of dumping all paths

#### Scenario: Pixi query returns run hint for selected topic environment
- **WHEN** `isomer-cli --print-json project self pixi` runs for a selected Research Topic with a resolvable Project-root Pixi environment binding or standalone Topic Workspace Pixi binding
- **THEN** the response includes the selected Pixi manifest path, Pixi environment name, binding source, and a Python command form using `pixi run --manifest-path <manifest_path> --environment <pixi_environment> python ...`
- **AND** it does not include identity, environment, or semantic path details beyond what is needed to explain the Pixi selection

#### Scenario: Pixi query does not guess across ambiguous bindings
- **WHEN** multiple active Pixi bindings are available and no single binding can be selected for the Pixi query
- **THEN** the response reports the candidate bindings and a diagnostic instead of emitting a misleading single `pixi run` command

#### Scenario: Pixi query reports missing binding clearly
- **WHEN** no usable Pixi manifest or environment can be resolved for the selected topic
- **THEN** the response includes a diagnostic and points the caller to `doctor` or topic environment setup rather than using system Python or a local virtual environment

### Requirement: Agent Self Query Catalog
The system SHALL expose safe follow-up commands through an explicit query catalog rather than embedding the catalog in every self response.

#### Scenario: Queries command lists follow-up commands
- **WHEN** `isomer-cli --print-json project self queries` runs
- **THEN** the response includes safe follow-up command examples for `project self identity`, `project self pixi`, `project self env`, `project self paths <semantic-label>`, `project context show`, `project paths get <semantic-label>`, `project paths explain <semantic-label>`, `project topic-actors show`, and topic or runtime inspection commands as applicable
- **AND** the command examples use `--print-json`

#### Scenario: Other self commands do not embed the full query catalog
- **WHEN** `project self show`, `project self identity`, `project self pixi`, `project self env`, or `project self paths` runs
- **THEN** the response may mention the next relevant self command
- **AND** it does not embed the full follow-up query catalog unless the caller explicitly invokes `project self queries`

### Requirement: User Skill Callback Registry Refs in Topic Context
The system SHALL let Project and Research Topic configuration expose User Skill Callback registry refs as declarative instruction-customization refs without treating callback material as runtime truth, executable provider payloads, or credentials.

#### Scenario: Research Topic Config carries callback registry refs
- **WHEN** a Research Topic Config is loaded
- **THEN** it may name User Skill Callback registry refs for topic-scoped callback resolution
- **AND** validation treats those refs as declarative instruction-customization refs rather than Run state, Artifact contents, provider implementation bodies, or command outputs

#### Scenario: Project Manifest carries callback registry refs
- **WHEN** a Project Manifest is loaded
- **THEN** it may name User Skill Callback registry refs for project-scoped callback resolution
- **AND** validation treats those refs as declarative instruction-customization refs rather than topic runtime state, credential material, provider implementation bodies, or command outputs

#### Scenario: Effective Topic Context exposes callback refs
- **WHEN** Effective Topic Context is resolved for a topic-scoped command
- **THEN** it includes the validated project-scoped and topic-scoped User Skill Callback registry refs that may influence callback resolution for that command

#### Scenario: Callback refs do not execute during context load
- **WHEN** Project discovery or Effective Topic Context resolution sees User Skill Callback registry refs
- **THEN** the system validates registry locations and metadata needed for the current command but does not execute callback content, external skill scripts, provider payloads, or agent workflows during context loading

#### Scenario: Inline callback bodies are rejected from config
- **WHEN** Project Manifest or Research Topic Config stores inline callback prompt bodies, external skill body text, runtime outputs, credentials, tokens, API keys, passwords, or other secret material directly in configuration fields
- **THEN** validation rejects those fields and directs the user to managed callback registry content or a credential backend as appropriate

#### Scenario: Durable records store callback refs only when consumed
- **WHEN** a future Run, command request, or provider-backed operation consumes Effective Topic Context that includes User Skill Callback registry refs
- **THEN** any durable record stores the validated callback registry refs and consumed callback ids rather than storing the full callback instruction bodies as runtime context truth

### Requirement: Topic Workspace Identity for Agents and Actors
The CLI SHALL expose the selected Topic Workspace id to agents and Topic Actors running inside a Topic Workspace.

#### Scenario: Self identity includes Topic Workspace id
- **WHEN** an agent or Topic Actor runs `isomer-cli --print-json project self identity` from inside a registered Topic Workspace
- **THEN** the JSON output includes the selected `topic_workspace_id`
- **AND** it includes the selected `research_topic_id` and Topic Workspace path

#### Scenario: Self show includes compact Topic Workspace identity
- **WHEN** an agent or Topic Actor runs `isomer-cli --print-json project self show` from inside a registered Topic Workspace
- **THEN** the summary includes the selected Topic Workspace id
- **AND** it does not require the agent to parse Project Manifest TOML directly

#### Scenario: Topic Service Master identity is available to agents
- **WHEN** a selected Topic Workspace has suggested Topic Service Master names or a recorded binding
- **THEN** self/context output includes a Topic Service Master identity block with suggested names and current binding status
- **AND** the output omits credentials and live runtime state

#### Scenario: Environment-selected workspace is reported
- **WHEN** `ISOMER_TOPIC_WORKSPACE_ID` selects the Topic Workspace
- **THEN** self/context output reports the environment source
- **AND** downstream records store validated refs rather than treating the environment value as durable truth

