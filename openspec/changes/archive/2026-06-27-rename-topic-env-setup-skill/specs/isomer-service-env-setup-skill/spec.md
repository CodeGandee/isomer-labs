## ADDED Requirements

### Requirement: Topic Workspace Environment Setup Independence
The service environment setup skill SHALL treat Topic Workspace development environment readiness as independent from Topic Agent Team Profile material, Agent Team Instance records, agent roles, and agent count.

#### Scenario: Missing team profile does not block environment setup
- **WHEN** `isomer-srv-topic-env-setup` runs for a Project Manifest-backed Research Topic and Topic Workspace
- **AND** `<topic-workspace-dir>/team-profile/` is missing, incomplete, unapproved, or not materialized
- **THEN** the skill continues environment setup when the Topic Workspace, Pixi binding, source gate, repos, dependencies, and verification commands can be resolved
- **AND** it does not report missing team-profile material as an environment setup blocker

#### Scenario: Agent team structure is not requested as input
- **WHEN** `isomer-srv-topic-env-setup` resolves setup context
- **THEN** it does not ask for Domain Agent Team Template selection, Topic Agent Team Profile fields, Topic Team Instantiation Packet contents, Agent Team Instance ids, Agent Instance ids, Agent Workspace plans, agent roles, or number of agents
- **AND** readiness is based on the Topic Workspace environment gate rather than team structure

#### Scenario: Project diagnostics are classified by environment relevance
- **WHEN** a read-only Project validation or doctor command reports diagnostics that mention missing Topic Agent Team Profile material, missing Agent Team Instances, missing Agent Workspaces, roles, or launch readiness
- **THEN** `isomer-srv-topic-env-setup` MAY report those diagnostics as unrelated or downstream context
- **AND** it MUST NOT treat those diagnostics as blockers unless they also prevent Topic Workspace discovery, Pixi binding resolution, source gate reading, dependency setup, repo checks, or Pixi-scoped verification

#### Scenario: Single-agent runnable target is the setup model
- **WHEN** `isomer-srv-topic-env-setup` interprets `env-gate.md`
- **THEN** it frames readiness as whether one agent or operator can run the commands needed to conduct the research inside the selected Topic Workspace
- **AND** it does not require proof that a multi-agent team can be launched or coordinated

## MODIFIED Requirements

### Requirement: Command-Style Subcommand Structure
The service environment setup skill SHALL be structured as a single command-style skill with short kebab-case subcommands, a lean top-level router, and linked executable reference pages.

#### Scenario: Entrypoint routes by subcommand
- **WHEN** an agent invokes `isomer-srv-topic-env-setup`
- **THEN** the top-level `SKILL.md` instructs the agent to select one subcommand from a grouped `Subcommands` section
- **AND** the top-level workflow loads the selected subcommand's reference page and executes that page's `## Workflow`
- **AND** if no prompt is given, the skill defaults to `help`
- **AND** if a concrete setup task is given without a subcommand, the skill defaults to `setup-topic-env`

#### Scenario: Subcommands are grouped for complex skill use
- **WHEN** the skill lists subcommands
- **THEN** it divides them into Procedural Subcommands, Helper Subcommands, and Misc Subcommands
- **AND** Procedural Subcommands include `resolve-topic-workspace`, `read-env-gate`, `ensure-topic-repos`, `derive-env-gate`, `install-topic-deps`, and `verify-env-gate`
- **AND** Misc Subcommands include `help` and `setup-topic-env`
- **AND** Helper Subcommands may explicitly state that no helper subcommands are currently exposed
- **AND** each subcommand name is short kebab-case

#### Scenario: Topic environment setup orchestrates the full workflow
- **WHEN** the `setup-topic-env` subcommand runs
- **THEN** it orchestrates `resolve-topic-workspace`, `read-env-gate`, `ensure-topic-repos`, `derive-env-gate`, `install-topic-deps`, and `verify-env-gate` in order
- **AND** it reports the combined result through the parent skill output contract

#### Scenario: Setup mode is selected from prompt
- **WHEN** the `setup-topic-env` subcommand is invoked
- **THEN** the skill selects `fast-forward` mode when the prompt asks for `fast-forward`, `fast-foward`, `auto`, `automatic`, or equivalent direct execution
- **AND** the skill selects `step-by-step` mode when the prompt asks for `step-by-step`, `manual`, `interactive`, confirmation, or equivalent user-controlled execution
- **AND** if the prompt gives a concrete setup task but no mode, the skill defaults to `fast-forward` mode unless the prompt asks to inspect, decide, or proceed carefully

#### Scenario: Fast-forward mode runs the ordered setup chain
- **WHEN** `setup-topic-env` runs in `fast-forward` mode
- **THEN** it executes `resolve-topic-workspace`, `read-env-gate`, `ensure-topic-repos`, `derive-env-gate`, `install-topic-deps`, and `verify-env-gate` in order without pausing for optional user consent
- **AND** it still stops for blockers, missing required inputs, unsafe ambiguity, or out-of-scope requests

#### Scenario: Step-by-step mode asks consent before each step
- **WHEN** `setup-topic-env` runs in `step-by-step` mode
- **THEN** before each required workflow step it explains what is about to happen and why
- **AND** it presents choices in a table with columns for `Option`, `Explain`, and `Pros and Cons`
- **AND** it states the recommended option outside the table with the option name, reason, and why that option is recommended
- **AND** it waits for the user to choose an option before executing that step
- **AND** after executing the chosen action, it reports the result before offering the next step

#### Scenario: Step subcommands are directly callable
- **WHEN** a user or agent invokes `resolve-topic-workspace`, `read-env-gate`, `ensure-topic-repos`, `derive-env-gate`, `install-topic-deps`, or `verify-env-gate` directly
- **THEN** the skill executes only that subcommand's workflow
- **AND** it refuses or blocks when predecessor artifacts required by that subcommand are missing

#### Scenario: Executable subcommand pages follow the style format
- **WHEN** a reference page acts as an executable subcommand page
- **THEN** it has a `## Required Inputs` section before its `## Workflow`
- **AND** the `## Required Inputs` section names the prompt inputs, predecessor artifacts, default paths, and refusal conditions needed by that subcommand
- **AND** direct callers can resolve that subcommand's inputs from that page without reading a central parent required-inputs table
- **AND** the top-level `SKILL.md` does not keep a central `## Required Inputs` table for executable setup behavior
- **AND** it has a `## Workflow` section near the top
- **AND** the workflow is written as numbered steps
- **AND** the workflow ends with a freeform fallback for tasks that do not map cleanly to the default steps

### Requirement: Topic Workspace Pixi Layout
The service environment setup skill SHALL define Topic Workspace environment setup as materializing a standalone Pixi workspace directly under the selected Topic Workspace directory.

#### Scenario: Topic Workspace is the environment root
- **WHEN** an agent uses `isomer-srv-topic-env-setup` for a Topic Workspace environment
- **THEN** the skill instructs the agent to resolve the Project Manifest-declared Topic Workspace directory as the environment root
- **AND** the skill does not treat the Project root, a Topic Agent Team Profile Bundle, or an Agent Workspace as the Topic Workspace Pixi environment root

#### Scenario: Successful setup leaves Pixi files in the Topic Workspace
- **WHEN** Topic Workspace environment setup completes successfully
- **THEN** `<topic-workspace-dir>/pixi.toml` exists
- **AND** `<topic-workspace-dir>/pixi.lock` exists
- **AND** `<topic-workspace-dir>/.pixi/` exists

#### Scenario: Topic Workspace VCS ignores are created
- **WHEN** Topic Workspace environment setup mutates the selected Topic Workspace
- **THEN** `<topic-workspace-dir>/.gitignore` contains `.pixi/`
- **AND** it contains `tmp/`
- **AND** it contains `.git/`
- **AND** the skill preserves unrelated existing ignore entries
- **AND** the skill does not add an `extern/orphan` ignore rule from this service skill

#### Scenario: Setup result is validated before readiness is reported
- **WHEN** the skill reports a Topic Workspace environment as ready
- **THEN** it has checked for `<topic-workspace-dir>/pixi.toml`, `<topic-workspace-dir>/pixi.lock`, and `<topic-workspace-dir>/.pixi/`
- **AND** it reports blockers instead of readiness when any of those paths is missing

#### Scenario: Manifest binding remains authoritative
- **WHEN** the skill resolves Topic Workspace Pixi paths
- **THEN** it uses the Project Manifest and active `topic_standalone_pixi_bindings` entry or supported implicit Topic Workspace default binding to identify the selected Topic Workspace and expected Pixi manifest
- **AND** it refuses to infer the binding solely from directory names

### Requirement: Environment Gate Verification
The service environment setup skill SHALL read `<topic-workspace-dir>/user-intent/src/env-gate.md`, generate `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md`, and use the derived gate as the operational verification gate for Topic Workspace environment readiness.

#### Scenario: Gate file is required for readiness verification
- **WHEN** an agent uses `isomer-srv-topic-env-setup` for a Topic Workspace environment
- **THEN** the skill instructs the agent to look for `<topic-workspace-dir>/user-intent/src/env-gate.md`
- **AND** the skill treats the file as the source of user intent for what must be able to run after setup

#### Scenario: Missing gate file blocks readiness
- **WHEN** `<topic-workspace-dir>/user-intent/src/env-gate.md` is missing or unreadable
- **THEN** the skill reports a blocker instead of claiming the Topic Workspace environment is ready
- **AND** it asks for the gate file to be created or repaired before final readiness verification

#### Scenario: Derived gate is generated from source intent
- **WHEN** `<topic-workspace-dir>/user-intent/src/env-gate.md` is present and readable
- **THEN** the skill instructs the agent to generate `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md`
- **AND** the generated gate preserves the source gate's user intent while converting it into operational environment-readiness checks based on the user requirement and any required repo contents

#### Scenario: Derived gate uses fixed Markdown sections
- **WHEN** the skill generates `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md`
- **THEN** the generated file includes top-level sections named `Source Intent`, `Runnable Target`, `Repo Requirements`, `Inferred Source Warnings`, `Dependency Plan`, `Pixi Install Commands`, `Verification Commands`, `Expected Results`, `Blockers`, and `Execution Log`
- **AND** every section is present even when the section content is `None.` or a short reason that it does not apply

#### Scenario: Vague source gate is made operational
- **WHEN** the source gate is vague about what must run after environment setup
- **THEN** the generated `isomer-env-gate.md` includes concrete required-to-succeed dependencies, Pixi install commands, Pixi run commands, scripts, imports, tools, expected outputs, or equivalent pass/fail checks
- **AND** it establishes success criteria that another agent can execute or inspect without reinterpreting the vague source wording

#### Scenario: Derived gate contents drive post-setup checks
- **WHEN** the gate file describes commands, scripts, imports, tools, or other runnable checks expected after setup
- **THEN** the skill uses the derived `isomer-env-gate.md` expectations to select or report dependency installation commands and verification commands after Pixi setup
- **AND** readiness is reported only when the gate expectations are satisfied or explicitly deferred with blockers

#### Scenario: Gate verification remains service-safe
- **WHEN** either gate file names checks that imply live agent launch, Agent Instance creation, unrelated runtime mutation, GUI operation, research decision authority, or Topic Agent Team Profile materialization
- **THEN** the skill reports those parts as out-of-scope blockers or deferrals
- **AND** it verifies only the service-safe Topic Workspace environment setup portion

### Requirement: Direct Topic Workspace Environment Mutation
The service environment setup skill SHALL allow direct service-safe mutation of the selected Topic Workspace Pixi environment during an explicit setup invocation, without requiring a separate Service Request boundary.

#### Scenario: Setup invocation authorizes Topic Workspace Pixi mutation
- **WHEN** the user invokes `isomer-srv-topic-env-setup` for Topic Workspace environment setup
- **AND** the Project Manifest-declared Topic Workspace and effective Topic Workspace Pixi binding have been confirmed
- **THEN** the skill may instruct the agent to add dependencies, update `pixi.toml`, refresh `pixi.lock`, install packages, and run gate commands for that Topic Workspace
- **AND** it does not require a separate Service Request before performing those service-safe mutations

#### Scenario: Direct mutation remains scoped
- **WHEN** the skill performs direct setup mutation
- **THEN** the mutation scope is limited to the selected Topic Workspace Pixi environment and missing required repos under `<topic-workspace-dir>/repos/<repo-name>`

#### Scenario: Existing topic repos are not mutated by ensure-topic-repos
- **GIVEN** a required repo path already exists under `<topic-workspace-dir>/repos/<repo-name>`
- **WHEN** `ensure-topic-repos` runs
- **THEN** it inspects the existing repo as read-only evidence
- **AND** it does not run `git pull`, switch branches, copy files into the repo, delete files from the repo, install packages into the repo, regenerate files in the repo, or otherwise mutate the repo
- **AND** if the existing repo is unsuitable for the gate, it reports a blocker instead of repairing the repo without explicit user authorization
- **AND** the skill does not mutate the Project-root Pixi environment, an Agent Workspace-specific environment, unrelated Workspace Runtime records, team-profile material, agent launch material, GUI state, or research decision artifacts

#### Scenario: Mutation output remains auditable in the response
- **WHEN** direct setup mutation changes files or runs commands
- **THEN** the skill reports changed environment files, commands run, readiness status, and blockers through the parent skill output contract
- **AND** changed environment files include `.gitignore` when the VCS ignore rules are added or refreshed
- **AND** it does not hide dependency or lockfile changes behind generic readiness language
