# isomer-cli-project-discovery Specification

## Purpose
TBD - created by archiving changes implement-isomer-cli-project-discovery and refactor-isomer-cli-to-click. Update Purpose after archive.
## Requirements
### Requirement: CLI Entrypoint and Command Surface
The system SHALL provide an installed `isomer-cli` command with Project discovery, doctor diagnostics, Workspace Runtime management, topic environment readiness preparation, Agent Team Instance record management, template inspection, and Topic Agent Team Profile validation commands.

#### Scenario: CLI exposes project-discovery commands
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help lists `init`, `validate`, `doctor`, `topics list`, `workspaces list`, `context show`, `paths preview`, `schemas list`, `runtime init`, `runtime prepare`, `runtime inspect`, `runtime validate`, `team-instances create`, `team-instances list`, and `team-instances show`

#### Scenario: CLI exposes template and profile commands
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help lists `team-templates` and `team-profiles` command groups

#### Scenario: Project script is installed through package metadata
- **WHEN** the package is installed through the repository's editable Pixi PyPI dependency
- **THEN** the environment can invoke `isomer-cli` as a project script

### Requirement: Project Initialization
The system SHALL initialize the smallest valid Isomer-managed Project configuration and the Project-level Houmao overlay without creating Workspace Runtime state or live Houmao agent state.

#### Scenario: Initialize default project
- **WHEN** a user runs `isomer-cli init` in a directory without `.isomer-labs/manifest.toml`
- **THEN** the system creates `.isomer-labs/manifest.toml`, one registered Research Topic Config for Research Topic id `default`, one project-local Topic Workspace directory at `topic-workspaces/default/`, and a Project-level Houmao overlay at `.houmao/`

#### Scenario: Initialize explicit topic
- **WHEN** a user runs `isomer-cli init` with an explicit Research Topic id
- **THEN** the system uses that id for the Research Topic registration, Research Topic Config path, and default Topic Workspace directory name

#### Scenario: Initialize creates Houmao project overlay
- **WHEN** `isomer-cli init` completes successfully
- **THEN** the system has invoked the supported Houmao CLI project initialization boundary for the Project root and reports the resolved Houmao Project overlay path in deterministic text or JSON output

#### Scenario: Initialize does not create runtime database
- **WHEN** `isomer-cli init` completes
- **THEN** the system does not create `state.sqlite` or any Workspace Runtime database

#### Scenario: Initialize does not create runtime or live Houmao launch state
- **WHEN** `isomer-cli init` completes
- **THEN** the system does not create Workspace Runtime subdirectories, Agent Workspaces, adapter launch material, Houmao managed agents, mailboxes, gateways, sessions, or launch dossiers

#### Scenario: Houmao bootstrap failure blocks project init
- **WHEN** a user runs `isomer-cli init` and the required Houmao command boundary is unavailable or returns a failing result
- **THEN** the system returns deterministic diagnostics, does not write `.isomer-labs/manifest.toml`, and does not claim that the Isomer Project was initialized

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
The system SHALL produce deterministic diagnostics, structured human-readable text, and machine-readable output for Project discovery, doctor diagnostics, Workspace Runtime management, topic environment readiness preparation, Agent Team Instance record management, template inspection, and Topic Agent Team Profile commands.

#### Scenario: Diagnostics include stable codes
- **WHEN** validation reports an error
- **THEN** each diagnostic includes a stable code, severity, file path when known, Isomer concept name, and concise message

#### Scenario: Diagnostics avoid leaking secrets
- **WHEN** validation reports a secret-like field
- **THEN** diagnostic output identifies the offending field or path without printing the secret value

#### Scenario: JSON output is deterministic
- **WHEN** a user requests JSON output with root-level `--print-json` for `validate`, `doctor`, `topics list`, `workspaces list`, `context show`, `paths preview`, `schemas list`, `runtime init`, `runtime prepare`, `runtime inspect`, `runtime validate`, `team-instances create`, `team-instances list`, `team-instances show`, `team-templates list`, `team-templates inspect`, `team-templates validate`, `team-profiles specialize`, or `team-profiles validate`
- **THEN** the command emits deterministic JSON suitable for unit tests and future Operator Agent consumption

#### Scenario: JSON output is versioned but provisional
- **WHEN** a user requests JSON output from a command added for doctor diagnostics, Workspace Runtime management, topic environment readiness preparation, Agent Team Instance record management, template registration, or Topic Agent Team Profile specialization
- **THEN** the response includes an output schema version and is treated as a developer contract rather than a durable public research-record API

### Requirement: Runtime Command Side-effect Boundaries
The system SHALL make Workspace Runtime mutations explicit in CLI behavior while preserving the read-only guarantees of inspection and design-time commands.

#### Scenario: Runtime init is the runtime creation command
- **WHEN** a user runs `isomer-cli runtime init`
- **THEN** the command may create or reopen `state.sqlite` and the default Workspace Runtime directories for the selected Topic Workspace

#### Scenario: Runtime prepare is the readiness preparation command
- **WHEN** a user runs `isomer-cli runtime prepare`
- **THEN** the command may record selected topic Pixi environment use, readiness status, readiness diagnostics, and preparation provenance in the selected Workspace Runtime

#### Scenario: Runtime inspect is read-only
- **WHEN** a user runs `isomer-cli runtime inspect`
- **THEN** the command reads Workspace Runtime metadata and selected record counts without creating or mutating runtime state

#### Scenario: Runtime validate is read-only
- **WHEN** a user runs `isomer-cli runtime validate`
- **THEN** the command reports Workspace Runtime diagnostics without creating directories, changing statuses, or repairing records

#### Scenario: Team instance create is explicit mutation
- **WHEN** a user runs `isomer-cli team-instances create`
- **THEN** the command may create Agent Team Instance, Agent Instance, Agent Workspace, path plan, Workflow Stage Cursor, and Provenance records for the selected Topic Workspace

#### Scenario: Team instance inspection is read-only
- **WHEN** a user runs `isomer-cli team-instances list` or `isomer-cli team-instances show`
- **THEN** the command reads Workspace Runtime records without creating Agent Team Instances, Agent Instances, Agent Workspaces, Runs, Houmao launch material, or adapter refs

### Requirement: Click Command Registration
The system SHALL implement the `isomer-cli` command surface with modular Click command groups while preserving established Project discovery command behavior.

#### Scenario: Root command is Click backed
- **WHEN** the package exposes `isomer-cli` through `isomer_labs.cli:main`
- **THEN** the command dispatch uses a Click command group rather than an `argparse` parser tree

#### Scenario: Existing commands remain available
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help still lists `init`, `validate`, `topics list`, `workspaces list`, `context show`, `paths preview`, and `schemas list`

#### Scenario: Existing command outputs remain compatible
- **WHEN** a user runs `validate`, `topics list`, `workspaces list`, `context show`, `paths preview`, or `schemas list` with JSON output requested through root-level `--print-json`
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
- **WHEN** the validation suite runs `isomer-cli --print-json validate` against the Milestone 2 and 3 fixture Project
- **THEN** the output has deterministic JSON and reports no diagnostics for the positive fixture

#### Scenario: Fixture template commands are deterministic
- **WHEN** the validation suite runs `team-templates list`, `team-templates inspect`, and `team-templates validate` against fixture Projects with and without `--print-json`
- **THEN** the output has deterministic text and JSON for built-in and project-local template refs

#### Scenario: Fixture profile commands are deterministic
- **WHEN** the validation suite runs `team-profiles specialize` and `team-profiles validate` against fixture Projects with and without `--print-json`
- **THEN** the output has deterministic text and JSON for preview, write, and validation flows

### Requirement: Milestone Documentation Completion
The system SHALL document the completed Milestone 2 and 3 command surface and fixture expectations.

#### Scenario: Developer docs describe template and profile completion
- **WHEN** Milestone 2 and 3 are completed
- **THEN** README or developer notes describe `team-templates`, `team-profiles`, fixture Project expectations, no-launch boundaries, and profile write semantics

#### Scenario: Roadmap reflects verified completion
- **WHEN** all Milestone 2 and 3 verification commands pass
- **THEN** ROADMAP Milestone 2 and 3 checklist items are marked complete without marking Milestone 4 or Houmao launch work complete

### Requirement: Houmao adapter launch CLI surface
The system SHALL expose Houmao adapter launch, prepare-only, inspect-live, and stop behavior through explicit `isomer-cli team-instances` commands with deterministic text and JSON output.

#### Scenario: Help lists adapter launch commands
- **WHEN** a user runs `isomer-cli team-instances --help`
- **THEN** the command help lists `launch`, `launch-material prepare`, `inspect-live`, and `stop` without presenting Houmao-specific command names as core Isomer concepts

#### Scenario: Quick launch command reports mutation
- **WHEN** a user runs `isomer-cli --print-json team-instances launch <agent-team-instance-id> --adapter houmao`
- **THEN** the command emits deterministic JSON with Project, Research Topic, Topic Workspace, Agent Team Instance, selected Execution Adapter, launch attempt refs, manifest refs, diagnostics, and an explicit mutation summary

#### Scenario: Prepare-only command reports manual guidance
- **WHEN** a user runs `isomer-cli --print-json team-instances launch-material prepare <agent-team-instance-id> --adapter houmao`
- **THEN** the command emits deterministic JSON with generated material refs, manifest refs, validation diagnostics, and bounded manual `houmao-mgr` guidance without launching Houmao-managed agents

### Requirement: Houmao adapter CLI side-effect boundaries
The system SHALL make side effects explicit for all Houmao adapter CLI commands.

#### Scenario: Inspect-live is read-only by default
- **WHEN** a user runs `isomer-cli team-instances inspect-live <agent-team-instance-id> --adapter houmao`
- **THEN** the command may read Workspace Runtime, manifests, and live Houmao state, but it does not create Agent Team Instances, launch agents, stop agents, or write adoption state unless a separate explicit recording or reconciliation command is used

#### Scenario: Stop is explicit mutation
- **WHEN** a user runs `isomer-cli team-instances stop <agent-team-instance-id> --adapter houmao`
- **THEN** the command reports that it may mutate live Houmao state and records the stop outcome in Workspace Runtime when the selected runtime schema supports adapter stop records

#### Scenario: Failed preflight has no live mutation
- **WHEN** quick launch or stop preflight fails
- **THEN** the command returns deterministic diagnostics and does not start, stop, message, or edit Houmao-managed agents

### Requirement: Houmao Adapter Manifest CLI Surface
The system SHALL expose deterministic CLI commands for Houmao adapter link export, integrity inspection, reconciliation, and adoption.

#### Scenario: Adapter link export is non-launching
- **WHEN** a user runs the adapter link export command for a Houmao-backed Agent Team Instance
- **THEN** the command writes or prints an `adapter-link.json` manifest and does not launch, stop, message, or inspect Houmao-managed agents

#### Scenario: Integrity inspection is read-only
- **WHEN** a user runs live inspection with integrity reporting for a Houmao-backed Agent Team Instance
- **THEN** the command reads Workspace Runtime refs, JSON manifests, and live Houmao state and emits deterministic output without recording adoption or changing launch state

#### Scenario: Reconcile records only when explicit
- **WHEN** a user runs the reconcile command for a Houmao-backed Agent Team Instance with recording enabled by the command contract
- **THEN** the command may write `adapter-runtime-manifest.json`, reconciliation records, diagnostics, and Provenance Records but does not start or stop Houmao-managed agents

#### Scenario: Adopt records external launch
- **WHEN** a user runs the adopt command for externally launched Houmao runtime state
- **THEN** the command validates mapping, paths, digests, and redaction before recording adopted adapter refs in Workspace Runtime

### Requirement: Houmao Manifest CLI Output
The system SHALL emit deterministic text and JSON output for Houmao adapter manifest and reconciliation commands.

#### Scenario: JSON output names generic refs
- **WHEN** a user requests JSON output with root-level `--print-json` from adapter link export, integrity inspection, reconcile, or adopt
- **THEN** the output names Project, Research Topic, Topic Workspace, Agent Team Instance, Agent Instance, Artifact, and Provenance refs plus opaque adapter refs and manifest paths

#### Scenario: Output reports reconciliation state
- **WHEN** a command observes linked, externally detected, adopted, drifted, conflicted, stale, or rejected state
- **THEN** the output includes the reconciliation state, mapping confidence, affected refs, and redacted diagnostics in stable field order

### Requirement: Global Print JSON Mode
The system SHALL use root-level `--print-json` as the canonical JSON output switch for `isomer-cli`.

#### Scenario: Root print-json applies to subcommands
- **WHEN** a user runs `isomer-cli --print-json validate`, `isomer-cli --print-json doctor`, or `isomer-cli --print-json runtime inspect`
- **THEN** the selected command emits the deterministic `isomer-cli-output.v1` JSON wrapper

#### Scenario: Default output is structured text
- **WHEN** a user runs `isomer-cli validate`, `isomer-cli doctor`, or another supported command without `--print-json`
- **THEN** the command emits structured human-readable text and does not emit the JSON wrapper

#### Scenario: Help shows global output mode
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the root help lists `--print-json` as the global machine-readable output switch

### Requirement: Handoff CLI Surface
The system SHALL expose top-level deterministic CLI commands for manual handoff dispatch, observation, and normalization while preserving existing read-only command guarantees.

#### Scenario: Handoff group is discoverable
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help lists a top-level `handoffs` command group without presenting Houmao-specific command names as core Isomer concepts

#### Scenario: Handoff dispatch command is explicit mutation
- **WHEN** a user runs `isomer-cli handoffs dispatch` for a launched or adopted Agent Team Instance
- **THEN** the command may create or update Run, handoff, adapter dispatch, adapter payload, Signal Observation, Artifact, and Provenance records for the selected Topic Workspace

#### Scenario: Handoff observe command is explicit mutation
- **WHEN** a user runs `isomer-cli handoffs observe`
- **THEN** the command may ingest Houmao mail, gateway, file, or bounded inspection signals as Signal Observations while keeping adapter observations separate from accepted handoff completion

#### Scenario: Handoff normalize command is explicit mutation
- **WHEN** a user runs `isomer-cli handoffs normalize`
- **THEN** the command may record accepted, rejected, blocked, superseded, repair-routed, or follow-up handoff normalization results with Run, Artifact, and Provenance refs

#### Scenario: Runtime record inspection remains read-only
- **WHEN** a user runs `runtime inspect`, `runtime validate`, `team-instances list`, `team-instances show`, or future read-only handoff inspection commands
- **THEN** those commands do not launch Houmao agents, send handoffs, stop agents, normalize results, or mutate adapter records

### Requirement: Handoff CLI Output
The system SHALL emit structured human-readable text by default and deterministic root-level `--print-json` output for manual handoff commands.

#### Scenario: Handoff dispatch JSON names runtime and adapter refs
- **WHEN** a user runs `isomer-cli --print-json handoffs dispatch`
- **THEN** the output includes generic Project, Research Topic, Topic Workspace, Agent Team Instance, source Agent Instance, target Agent Instance, handoff, Run, expected output, adapter dispatch, adapter payload, and Provenance refs plus diagnostics

#### Scenario: Handoff observe JSON keeps signals non-authoritative
- **WHEN** a user runs `isomer-cli --print-json handoffs observe`
- **THEN** the output includes Signal Observation refs, adapter payload refs, candidate status, diagnostics, and a field or diagnostic that indicates the observation did not mark the handoff accepted

#### Scenario: Handoff normalize JSON reports accepted or rejected result
- **WHEN** a user runs `isomer-cli --print-json handoffs normalize`
- **THEN** the output includes the handoff ref, normalization status, Run updates, Artifact refs, rejected or repair refs when present, Provenance refs, and diagnostics

#### Scenario: Handoff text output is structured
- **WHEN** a user runs `isomer-cli handoffs dispatch`, `isomer-cli handoffs observe`, or `isomer-cli handoffs normalize` without `--print-json`
- **THEN** the command emits structured human-readable text that names the selected Project, Research Topic, Topic Workspace, handoff status, relevant runtime refs, and diagnostics without dumping raw Houmao payloads

#### Scenario: Handoff commands do not add local JSON flags
- **WHEN** a user inspects help for `handoffs dispatch`, `handoffs observe`, or `handoffs normalize`
- **THEN** the commands do not advertise command-local `--json`, `--format json`, or `--format=json` flags and rely on root-level `--print-json` for machine-readable output

### Requirement: UC-01 Headless Manual Harness
The system SHALL expose a manual harness for running or validating the UC-01 headless workflow from an Isomer Project while keeping named UC-01 orchestration out of the product CLI.

#### Scenario: UC-01 harness is discoverable
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command surface does not include `uc01`, `uc01 run`, or `uc01 inspect`
- **AND** workflow docs point to `tests/manual/uc01_headless_vertical_slice`

#### Scenario: UC-01 harness uses generic context APIs
- **WHEN** a user runs the UC-01 manual harness
- **THEN** the harness resolves the Project, Research Topic, Topic Workspace, Topic Agent Team Profile, adapter mode, actor ref, and follow-up inquiry selection through generic CLI commands or reusable Python APIs

### Requirement: UC-01 Deterministic JSON Output
The system SHALL emit deterministic JSON for the UC-01 headless workflow through the manual harness.

#### Scenario: JSON output reports created records
- **WHEN** a user runs `pixi run python tests/manual/uc01_headless_vertical_slice`
- **THEN** the output includes `ok`, selected Project and topic refs, Agent Team Instance ref, Research Inquiry refs, Research Task refs, Run refs, handoff refs, Artifact refs, Evidence Item refs, Gate ref, Decision Record ref, route classification, View Manifest refs, Provenance refs, diagnostics, and live or simulated mode

#### Scenario: Generic commands keep structured output behavior
- **WHEN** a user runs generic Isomer CLI commands with or without `--print-json`
- **THEN** those commands keep their generic JSON or human-readable output behavior without adding command-local `--json`, `--format json`, or `--format=json` options

### Requirement: UC-01 Harness Side-effect Boundary
The system SHALL make UC-01 workflow mutation explicit and keep fixture validation side-effect free.

#### Scenario: Harness mutates only temporary fixture copies
- **WHEN** the user invokes the UC-01 harness in simulated or live mode
- **THEN** the harness copies the fixture Project to a temporary directory before creating Workspace Runtime records, adapter payloads, Artifacts, Gates, Decision Records, View Manifests, and Provenance Records

#### Scenario: Harness does not start UC-07 work
- **WHEN** the UC-01 harness records a follow-up inquiry classified as UC-07-style measured optimization
- **THEN** the harness exits after recording the Gate, Decision Record, selected Research Inquiry, and route classification without running measurement, baseline, or candidate optimization commands

#### Scenario: Fixture validation is read-only
- **WHEN** the user invokes generic `validate` against the pinned UC-01 fixture Project
- **THEN** the command reports Project diagnostics without creating runtime records, launching agents, dispatching handoffs, or resolving Gates

### Requirement: UC-01 Live Gate Reporting
The system SHALL report live-gated Houmao validation status before UC-01 live mutation.

#### Scenario: Missing live gate skips live mode
- **WHEN** live Houmao mode is requested without the required live-validation environment gate
- **THEN** the harness exits the live check with a deterministic skipped status and does not mutate Project files, Workspace Runtime, adapter files, or live Houmao state for that live copy

#### Scenario: Capability report precedes live mutation
- **WHEN** live Houmao mode is allowed
- **THEN** the harness reports the Houmao command resolution, checkout path candidates, read-only capability checks, and cleanup plan before running launch, handoff, or stop mutations

### Requirement: Use-Case Command Boundary
The public `isomer-cli` command surface SHALL expose reusable platform operations rather than named use-case acceptance runners unless a later accepted product spec explicitly promotes the command.

#### Scenario: UC-01 command group is absent
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command surface does not list `uc01`, `uc01 run`, or `uc01 inspect`

#### Scenario: Generic commands remain available
- **WHEN** a manual acceptance harness needs to validate a Project, prepare Workspace Runtime state, create or inspect Agent Team Instance records, dispatch or normalize handoffs, or validate runtime records
- **THEN** it can use generic command groups such as `validate`, `runtime`, `team-instances`, `handoffs`, `team-templates`, and `team-profiles`

#### Scenario: Root print-json remains global
- **WHEN** a manual acceptance harness invokes generic CLI commands for deterministic output
- **THEN** it uses root-level `--print-json` and no command-local `--json`, `--format json`, or `--format=json` options are introduced for use-case harness behavior

### Requirement: Manual Harness Entry Points Are Outside Product CLI
Named use-case acceptance runners SHALL be invoked through test or manual script entry points outside the installed `isomer-cli` command surface.

#### Scenario: UC-01 harness has script entry point
- **WHEN** a developer wants to run the pinned UC-01 headless acceptance path
- **THEN** they use a documented command such as `pixi run python tests/manual/uc01_headless_vertical_slice` or an equivalent manual script entry point

#### Scenario: Harness output is not product CLI schema
- **WHEN** the UC-01 harness prints a deterministic summary
- **THEN** the summary may include harness-specific fields, but core CLI commands still emit the versioned `isomer-cli-output.v1` wrapper only for generic platform commands

### Requirement: Product Promotion Requires Spec Update
A named use-case command SHALL require an accepted spec update before it appears in `isomer-cli`.

#### Scenario: Future use-case command is proposed
- **WHEN** a future milestone wants `isomer-cli uc07` or another named use-case command
- **THEN** the proposal identifies why the command is reusable product behavior, adds or modifies CLI requirements, and updates command-surface tests before implementation
