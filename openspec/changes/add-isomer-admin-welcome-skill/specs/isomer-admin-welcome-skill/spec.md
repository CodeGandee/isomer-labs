## ADDED Requirements

### Requirement: Welcome Skill Presents Operator Workflow Options
The `isomer-admin-welcome` skill SHALL present an action-oriented menu of supported Isomer Labs operator workflows, name the owner skill for each workflow, and invite the user to choose a path, describe their goal, or invoke an owner skill directly.

#### Scenario: Default invocation prints option menu
- **WHEN** the welcome skill is invoked without a specific subcommand or with a broad onboarding request
- **THEN** it lists supported actions such as Project setup or checks, Research Topic creation or preparation, initialized-topic management, Topic Team Specialization, and Houmao interop
- **AND** each listed action names the direct owner skill to invoke
- **AND** it asks the user to choose an option, describe their goal, or invoke the named skill directly

#### Scenario: Menu avoids tutorial-first behavior
- **WHEN** the welcome skill prints its default output
- **THEN** it prioritizes what the system can do and which path to choose
- **AND** it does not primarily present a conceptual introduction to the Isomer system model

### Requirement: Welcome Skill Routes Only to Active Owner Skills
The `isomer-admin-welcome` skill SHALL route users only to active owner skills and SHALL NOT route users to retired operator compatibility skills.

#### Scenario: Supported paths name active skills
- **WHEN** the welcome skill presents direct invocation guidance
- **THEN** Project lifecycle work routes to `isomer-admin-project-mgr`
- **AND** blank or partial Research Topic creation and manual-research-ready topic preparation route to `isomer-admin-topic-creator`
- **AND** initialized-topic storage, Topic Actors, environment package mutation, environment verification, reset checkpoints, and diagnostics route to `isomer-admin-topic-mgr`
- **AND** Topic Team Specialization routes to `isomer-admin-topic-team-specialize`
- **AND** Houmao loop, runtime, launch profile, mailbox, gateway, or template-mapping explanation routes to `isomer-admin-houmao-interop`

#### Scenario: Retired skills are not active routes
- **WHEN** welcome skill guidance is inspected
- **THEN** it does not ask users or agents to invoke `isomer-admin-topic-workspace-mgr`
- **AND** it does not ask users or agents to invoke `isomer-admin-topic-prepare`
- **AND** it does not ask users or agents to invoke `isomer-admin-manual-research-session`

### Requirement: Welcome Skill Stays Read-Only by Default
The `isomer-admin-welcome` skill SHALL be read-only by default and SHALL NOT perform owner workflow mutation from the welcome surface.

#### Scenario: Welcome option selection does not mutate state
- **WHEN** a user asks the welcome skill what path to choose
- **THEN** the skill may recommend an owner skill and safe first command
- **AND** it does not initialize Projects, create Research Topics, mutate Topic Workspaces, install packages, specialize teams, launch agents, or bootstrap research-paradigm v2 artifacts

#### Scenario: Context-aware next step uses read-only inspection
- **WHEN** the user asks for a context-aware next step and a Project context is available
- **THEN** the skill may use read-only commands such as `isomer-cli project validate`, `isomer-cli project doctor`, `isomer-cli project topics list`, or `isomer-cli project context show`
- **AND** it reports blockers and the recommended owner workflow without running mutating commands

### Requirement: Welcome Skill Exposes Focused Subcommands
The `isomer-admin-welcome` skill SHALL expose focused public subcommands for option display, path choice, direct skill mapping, context-aware next-step recommendation, and help.

#### Scenario: Public subcommands are documented
- **WHEN** the welcome skill help is inspected
- **THEN** it documents `help`, `show-options`, `choose-path`, `show-skill-map`, and `next-step`
- **AND** each subcommand has a bounded purpose and a local reference page

### Requirement: Welcome Skill Output Contract
The `isomer-admin-welcome` skill SHALL report concise default output and provide complete output only when requested.

#### Scenario: Essential output names route and next action
- **WHEN** the welcome skill recommends a path
- **THEN** it reports `status`, `interpreted_goal`, `recommended_workflow`, `owner_skill`, `safe_first_command`, `blockers`, and `next_action`

#### Scenario: Complete output adds evidence and alternatives
- **WHEN** the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output
- **THEN** the skill includes context evidence, read-only commands run, alternate owner workflows, routing rationale, and retired-route exclusions when relevant
