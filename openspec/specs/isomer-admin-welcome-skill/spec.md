# isomer-op-welcome-skill Specification

## Purpose
TBD - created by archiving change add-isomer-op-welcome-skill. Update Purpose after archive.
## Requirements
### Requirement: Welcome Skill Presents Operator Workflow Options
The `isomer-op-welcome` skill SHALL present an action-oriented menu of supported Isomer Labs operator workflows, name the owner skill for each workflow, and invite the user to choose a path, describe their goal, or invoke an owner skill directly.

#### Scenario: Default invocation prints option menu
- **WHEN** the welcome skill is invoked without a specific subcommand or with a broad onboarding request
- **THEN** it lists visible usage paths such as `start-research-manually` and `start-research-by-agent-team`
- **AND** it lists supported actions such as Project setup or checks, Research Topic creation or preparation, initialized-topic management, Topic Team Specialization, and Houmao interop
- **AND** each listed action names the direct owner skill to invoke
- **AND** it asks the user to choose an option, describe their goal, or invoke the named skill directly

#### Scenario: Menu avoids tutorial-first behavior
- **WHEN** the welcome skill prints its default output
- **THEN** it prioritizes what the system can do and which path to choose
- **AND** it does not primarily present a conceptual introduction to the Isomer system model

### Requirement: Welcome Skill Routes Only to Active Owner Skills
The `isomer-op-welcome` skill SHALL route users only to active owner skills and SHALL NOT route users to retired operator compatibility skills.

#### Scenario: Supported paths name active skills
- **WHEN** the welcome skill presents direct invocation guidance
- **THEN** Project lifecycle work routes to `isomer-op-project-mgr`
- **AND** blank or partial Research Topic creation and manual-research-ready topic preparation route to `isomer-op-topic-creator`
- **AND** initialized-topic storage, Topic Actors, environment package mutation, environment verification, reset checkpoints, and diagnostics route to `isomer-op-topic-mgr`
- **AND** Topic Team Specialization routes to `isomer-op-topic-team-specialize`
- **AND** Houmao loop, runtime, launch profile, mailbox, gateway, or template-mapping explanation routes through the owning operator workflow to `isomer-srv-houmao-interop`

#### Scenario: Retired skills are not active routes
- **WHEN** welcome skill guidance is inspected
- **THEN** it does not ask users or agents to invoke old retired topic workspace manager skills
- **AND** it does not ask users or agents to invoke old retired topic preparation skills
- **AND** it does not ask users or agents to invoke old retired manual research session skills

### Requirement: Welcome Skill Stays Read-Only by Default
The `isomer-op-welcome` skill SHALL be read-only by default and SHALL NOT perform owner workflow mutation from the welcome surface.

#### Scenario: Welcome option selection does not mutate state
- **WHEN** a user asks the welcome skill what path to choose
- **THEN** the skill may recommend an owner skill and safe first command
- **AND** it does not initialize Projects, create Research Topics, mutate Topic Workspaces, install packages, specialize teams, launch agents, or bootstrap research-paradigm v2 artifacts

#### Scenario: Context-aware next step uses read-only inspection
- **WHEN** the user asks for a context-aware next step and a Project context is available
- **THEN** the skill may use read-only commands such as `isomer-cli project validate`, `isomer-cli doctor`, `isomer-cli project topics list`, or `isomer-cli project context show`
- **AND** it reports blockers and the recommended owner workflow without running mutating commands

### Requirement: Welcome Skill Exposes Focused Subcommands
The `isomer-op-welcome` skill SHALL expose focused public subcommands for visible usage paths, option display, path choice, direct skill mapping, context-aware next-step recommendation, and help.

#### Scenario: Typical usage paths are first-class
- **WHEN** the welcome skill `SKILL.md` is inspected
- **THEN** it documents typical usage-path subcommands including `start-research-manually` and `start-research-by-agent-team`
- **AND** those paths are visible in `SKILL.md` rather than existing only as hidden branches inside `choose-path`
- **AND** each usage path names the owner skill, intent, safe first command, mutation boundary, and next action

#### Scenario: Public subcommands are documented
- **WHEN** the welcome skill help is inspected
- **THEN** it documents `start-research-manually`, `start-research-by-agent-team`, `help`, `show-options`, `choose-path`, `show-skill-map`, and `next-step`
- **AND** each subcommand has a bounded purpose and a local reference page

### Requirement: Welcome Skill Output Contract
The `isomer-op-welcome` skill SHALL report concise default output and provide complete output only when requested.

#### Scenario: Essential output names route and next action
- **WHEN** the welcome skill recommends a path
- **THEN** it reports `status`, `interpreted_goal`, `recommended_workflow`, `owner_skill`, `safe_first_command`, `blockers`, and `next_action`

#### Scenario: Complete output adds evidence and alternatives
- **WHEN** the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output
- **THEN** the skill includes context evidence, read-only commands run, alternate owner workflows, routing rationale, and retired-route exclusions when relevant

### Requirement: Welcome Skill Exposes Toolbox Manager Owner Route
The `isomer-op-welcome` skill SHALL expose `isomer-op-toolbox-mgr` as an active owner workflow for project-local Toolbox business while preserving the welcome skill's read-only posture.

#### Scenario: Default options include Toolbox management
- **WHEN** the welcome skill prints its default options
- **THEN** it includes project-local Toolbox creation, conversion, installation, inspection, update, disable, uninstall, callback insertion, Runtime Param, and insertion-point work as supported actions
- **AND** it names `isomer-op-toolbox-mgr` as the owner skill
- **AND** it does not present Toolbox management as a first-class research-start usage path such as `start-research-manually` or `start-research-by-agent-team`

#### Scenario: Skill map includes Toolbox manager
- **WHEN** the welcome skill prints its direct skill map
- **THEN** it includes a Toolbox management intent row that routes to `isomer-op-toolbox-mgr`
- **AND** the direct invocation guidance uses `$isomer-op-toolbox-mgr`

#### Scenario: Path choice recognizes Toolbox tasks
- **WHEN** the user asks the welcome skill which path owns Toolbox authoring, Toolbox installation, callback insertion, callback insertion points, Runtime Params, or effective Toolbox state
- **THEN** it recommends `isomer-op-toolbox-mgr`
- **AND** it does not route the request to `isomer-misc-tool-packs`

#### Scenario: Welcome remains read-only for Toolbox work
- **WHEN** the welcome skill recommends `isomer-op-toolbox-mgr`
- **THEN** it does not author Toolbox source, install Toolboxes, mutate callback registries, or mutate Runtime Params itself

### Requirement: Welcome Recommendations Require a Formal Team Target
The welcome skill SHALL recommend Topic Team Specialization only for an explicit specialization route or a prompt or authoritative context that establishes an Agent Team target.

#### Scenario: Manual topic preparation remains manual
- **WHEN** the user asks to prepare a Research Topic, Topic Workspace, Topic Actor workflow, runtime, or other launch-facing surface without formal Agent Team intent
- **THEN** the welcome skill recommends Topic Creator, Topic Manager, Project Manager, Topic Service Agent support, GUI Manager, or another applicable owner
- **AND** it does not infer Topic Team Specialization

#### Scenario: Agent Team launch recommendation is qualified
- **WHEN** the user asks for launch-facing help and the prompt or authoritative context identifies a Domain Agent Team Template, Topic Agent Team Profile, Topic Team Instantiation Packet, Agent Team Instance, or selected formal team
- **THEN** the welcome skill may recommend `isomer-op-topic-team-specialize`
- **AND** it explains the formal-team evidence that made the route applicable
