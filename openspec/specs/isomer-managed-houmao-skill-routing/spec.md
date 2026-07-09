# isomer-managed-houmao-skill-routing Specification

## Purpose
TBD - created by archiving change route-houmao-skills-through-isomer. Update Purpose after archive.
## Requirements
### Requirement: Project Houmao Integration State
The system SHALL store Project-scoped Houmao integration state in the Project Manifest so Isomer workflows can distinguish enabled, disabled, and not-configured integration without inspecting user-home skill installations.

#### Scenario: Enabled integration is explicit
- **WHEN** a Project Manifest declares Houmao integration as enabled
- **THEN** Isomer CLI context commands report `integration_status = "enabled"`
- **AND** they include the Project-relative Houmao skill projection root and Houmao Project directory

#### Scenario: Disabled integration is explicit
- **WHEN** a Project Manifest declares Houmao integration as disabled
- **THEN** Houmao-aware Isomer CLI and skill workflows report `integration_status = "disabled"`
- **AND** they return a skip reason instead of running `houmao-mgr` or requiring Houmao skill material

#### Scenario: Missing integration state is not configured
- **WHEN** a Project Manifest has no Houmao integration declaration
- **THEN** the system treats Houmao integration as not configured
- **AND** it reports a deterministic next action to enable, disable, or prepare the integration instead of assuming it is enabled

### Requirement: Isomer-Managed Houmao Skill Projection
The system SHALL project Houmao-owned system skill material into an Isomer-managed Project-local skill root under `.isomer-labs/houmao-skills/`.

#### Scenario: Projection root is inside Project Config Directory
- **WHEN** Houmao skill material is prepared for an enabled Project
- **THEN** the projected skills are placed under `<project-root>/.isomer-labs/houmao-skills/`
- **AND** the projection root is reported as Isomer-managed support material rather than user-authored Topic Workspace material

#### Scenario: Projection does not create nested Houmao project state
- **WHEN** Houmao skills are projected under `.isomer-labs/houmao-skills/`
- **THEN** the projection SHALL NOT create `.houmao/` inside that skill root
- **AND** the Houmao Project directory remains `<project-root>/.isomer-labs`

#### Scenario: Projection preserves ownership metadata
- **WHEN** the system writes a projected Houmao skill directory
- **THEN** it records ownership metadata that identifies the projection as Isomer-managed
- **AND** later projection updates refuse to overwrite unmanaged files with the same skill name

### Requirement: Houmao Skill Context CLI
The system SHALL expose an Isomer CLI context command that resolves a stable Isomer route name to an absolute Houmao skill path and explicit Houmao Project path.

#### Scenario: Skill context returns explicit paths
- **WHEN** a skill or operator runs `isomer-cli --print-json project integrations houmao skill-context <skill-name>` in an enabled Project
- **THEN** the JSON output includes `houmao_skill_path`, `houmao_project_path`, `houmao_overlay_path`, `integration_status`, and `instructions`
- **AND** the returned paths are absolute paths

#### Scenario: Topic context is included when selected
- **WHEN** the skill-context command is run with a selected Research Topic
- **THEN** the output includes the selected Research Topic id, Topic Workspace id, and Topic Workspace path
- **AND** the command resolves those values through Project Manifest-backed context rather than by scanning sibling directories

#### Scenario: Unknown skill route is rejected
- **WHEN** the requested Houmao skill route is not present in the Isomer-managed projection manifest
- **THEN** the command reports a deterministic diagnostic naming the unknown route
- **AND** it does not fabricate a skill path from the requested name

#### Scenario: Lifecycle route names are manifest backed
- **WHEN** the projection manifest declares Topic Service Master route entries
- **THEN** it declares separate entries for `prepare-topic-service-master`, `launch-topic-service-master`, `inspect-topic-service-master`, `stop-topic-service-master`, and `repair-topic-service-master`
- **AND** each route resolves to a concrete projected Houmao skill path through manifest data rather than string interpolation

### Requirement: Explicit Houmao Project Path Instruction
The system SHALL instruct agents routed to projected Houmao skills to pass the Isomer-managed Houmao Project path explicitly to Houmao commands.

#### Scenario: Instructions require explicit project dir
- **WHEN** Isomer returns a Houmao skill context
- **THEN** the instructions tell the agent to read the returned `houmao_skill_path`
- **AND** they tell the agent to run Houmao commands with `--project-dir <houmao_project_path>`

#### Scenario: Topic Workspace cwd does not imply discovery
- **WHEN** a projected Houmao skill is used from a Topic Workspace cwd
- **THEN** the agent guidance does not rely on Houmao discovering a root-level `.houmao/`
- **AND** it uses the explicit Houmao Project path returned by Isomer

### Requirement: Topic Service Master Lifecycle Skill Routes
The system SHALL expose explicit Isomer-facing Topic Service Master lifecycle routes from `isomer-srv-topic-service-agent-support`.

#### Scenario: Lifecycle subcommands are listed
- **WHEN** the Topic Service Agent support skill is inspected
- **THEN** it lists `prepare-topic-service-master`, `launch-topic-service-master`, `inspect-topic-service-master`, `stop-topic-service-master`, and `repair-topic-service-master`
- **AND** each lifecycle route points to a dedicated reference page

#### Scenario: Lifecycle subcommands resolve Houmao skill context
- **WHEN** any Topic Service Master lifecycle subcommand needs Houmao-backed behavior
- **THEN** it obtains Houmao skill context through the supported Isomer CLI integration command
- **AND** it routes the active agent to the returned `houmao_skill_path` with the returned `houmao_project_path`

#### Scenario: Lifecycle subcommands use matching routes
- **WHEN** `isomer-srv-topic-service-agent-support` executes a Topic Service Master lifecycle subcommand
- **THEN** it requests the Houmao skill context for the same lifecycle route name
- **AND** it does not request a generic Houmao administration route for lifecycle-specific work

#### Scenario: Creation flow uses preparation only
- **WHEN** Topic Creator setup asks for Houmao-backed Topic Service Master work during Topic Workspace creation
- **THEN** it routes to `prepare-topic-service-master`
- **AND** launch, inspect, stop, and repair remain explicit later lifecycle operations

