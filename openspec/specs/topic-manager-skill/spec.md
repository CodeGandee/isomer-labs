# topic-manager-skill Specification

## Purpose
Define the operator skill that manages initialized Research Topics after Topic Creator handoff.
## Requirements
### Requirement: Topic Manager Skill Bundle
The repository SHALL provide a command-style operator skill named `isomer-admin-topic-mgr` for managing an initialized Research Topic after Topic Creator handoff.

#### Scenario: Topic manager bundle exists
- **WHEN** the operator skillset is inspected
- **THEN** it contains `skillset/operator/isomer-admin-topic-mgr/SKILL.md` and `skillset/operator/isomer-admin-topic-mgr/agents/openai.yaml`

#### Scenario: Topic manager metadata is consistent
- **WHEN** the topic manager skill bundle is inspected
- **THEN** the folder name, `SKILL.md` frontmatter `name`, `agents/openai.yaml` display name, and default prompt use `isomer-admin-topic-mgr`

#### Scenario: Topic manager is initialized-topic scoped
- **WHEN** the skill entrypoint describes its purpose
- **THEN** it states that `isomer-admin-topic-creator` owns topic initialization
- **AND** it states that `isomer-admin-topic-mgr` manages initialized-topic storage, Topic Actors, topic agent team topology, environment mutation, environment verification, and diagnostics

### Requirement: Initialized Topic Guard
The Topic Manager skill SHALL require Project Manifest-backed selected Research Topic and Topic Workspace context before managing topic state.

#### Scenario: Initialized topic is available
- **WHEN** `isomer-admin-topic-mgr` resolves a selected initialized Research Topic and Topic Workspace
- **THEN** it may run the selected management subcommand against that topic
- **AND** it reports the Research Topic ref, Topic Workspace ref, semantic path evidence, blockers, and next action

#### Scenario: Initialized topic is missing
- **WHEN** `isomer-admin-topic-mgr` cannot resolve an initialized Research Topic or Topic Workspace
- **THEN** it reports a blocker and routes initialization to `isomer-admin-topic-creator`
- **AND** it does not derive a topic id, register a topic, create a Topic Workspace, or write topic intent material itself

### Requirement: Scope-Prefixed Command Structure
The Topic Manager skill SHALL use grouped, one-level, scope-prefixed kebab-case subcommands with one executable reference page per subcommand.

#### Scenario: Entrypoint routes by subcommand
- **WHEN** an agent invokes `isomer-admin-topic-mgr`
- **THEN** the top-level `SKILL.md` selects one subcommand from grouped subcommand tables and loads only the selected reference page before executing that page's `## Workflow`

#### Scenario: Default command reports status
- **WHEN** the user invokes `isomer-admin-topic-mgr` without a subcommand and does not ask for help
- **THEN** the skill selects `status` as the default initialized-topic inspection flow

#### Scenario: Public subcommands are grouped by scope
- **WHEN** the skill lists public subcommands
- **THEN** it includes status commands `status`, `doctor`, and `help`
- **AND** it includes storage commands `storage-resolve`, `storage-inspect-main`, `storage-validate`, and `storage-register-repo`
- **AND** it includes actor commands `actors-manage`, `actors-materialize`, and `actors-diagnose`
- **AND** it includes team commands `team-plan`, `team-materialize-workspaces`, `team-write-boundaries`, `team-create-branch`, and `team-validate-workspaces`
- **AND** it includes environment mutation commands `env-install-packages`, `env-update-packages`, and `env-remove-packages`
- **AND** it includes environment verification commands `env-verify-topic`, `env-verify-actors`, and `env-verify-agents`

### Requirement: Storage Management Commands
The Topic Manager skill SHALL manage initialized-topic storage surfaces through Workspace Path Resolution and Topic Workspace Manifest bindings.

#### Scenario: Storage resolution uses manifest-backed context
- **WHEN** `storage-resolve` runs
- **THEN** it resolves Project root, Research Topic, Topic Workspace, Topic Main Repository, Topic Actor Workspace labels, Agent Workspace labels, tmp labels, records labels, and custom labels through Project Manifest-backed context
- **AND** it does not infer the selected Topic Workspace by scanning sibling directories

#### Scenario: Main repository inspection is bounded
- **WHEN** `storage-inspect-main` inspects or validates `topic.repos.main`
- **THEN** it reports path source, Git state, `isomer-managed/` posture, projection roots, tmp posture, blockers, and next action
- **AND** it does not delete, replace, pull, reset, reinitialize, or overwrite an existing repository without explicit user instruction

#### Scenario: Additional topic repo registration uses semantic labels
- **WHEN** `storage-register-repo` registers an additional non-main topic repository
- **THEN** it uses grouped `topic.repos.*` semantic labels with an explicit storage profile
- **AND** it does not describe non-main topic repositories as Topic Actor Workspace or Agent Workspace worktree sources

### Requirement: Topic Actor Management Commands
The Topic Manager skill SHALL manage Topic Actor CRUD, materialization, repair, archive, and diagnostics as initialized-topic topology operations.

#### Scenario: Actor management uses topic manager
- **WHEN** a user or operator asks to list, show, register, update, archive, materialize, repair, or diagnose Topic Actors
- **THEN** `isomer-admin-topic-mgr actors-manage`, `actors-materialize`, or `actors-diagnose` performs or guides the operation through the supported `project topic-actors ...` CLI surface
- **AND** Topic Workspace Manifest actor bindings remain the topology and path-resolution authority

#### Scenario: Actor workspace materialization stays actor scoped
- **WHEN** `actors-materialize` creates or repairs a Topic Actor Workspace
- **THEN** it uses `topic.repos.main` as the Git anchor, resolves `topic.actors.workspace` for the selected Topic Actor, and uses the `per-topic-actor/<topic-actor-name>/main` default branch namespace
- **AND** it keeps Topic Actor names separate from Agent Names and Agent Instance ids

### Requirement: Topic Agent Team Topology Commands
The Topic Manager skill SHALL manage static topic agent team topology support without creating live Agent Instances.

#### Scenario: Team planning normalizes agent names
- **WHEN** `team-plan` resolves requested Agent Names from role bindings or operator input
- **THEN** it rejects empty names, unsafe path segments, reserved names, normalized collisions, and cross-topic workspace refs before planning workspaces or branches

#### Scenario: Team workspace materialization is bounded
- **WHEN** `team-materialize-workspaces` creates or validates an Agent Workspace for Agent Name `alice`
- **THEN** it uses resolved `agent.workspace` and `agent.*` support labels, plans branch `per-agent/alice/main`, and reports path source, readiness, blockers, and next action

#### Scenario: Team topology validation avoids runtime claims
- **WHEN** `team-validate-workspaces` reports Git-backed topology as ready
- **THEN** it does not claim Topic Workspace Pixi env readiness, Agent Instance creation, Workspace Runtime records, Houmao launch, or Execution Adapter readiness

### Requirement: Environment Mutation Commands
The Topic Manager skill SHALL provide operator-facing environment mutation commands for selected Topic Workspace package changes.

#### Scenario: Package install accepts flexible input
- **WHEN** `env-install-packages` receives a package request from a user prompt, Markdown file, YAML, JSON, TOML, requirements-style list, or copied blocker text
- **THEN** it infers the requested packages, purpose, target environment, install route, and verification checks without requiring a schema-constrained request file

#### Scenario: Package mutation uses Topic Workspace Pixi environment
- **WHEN** `env-install-packages`, `env-update-packages`, or `env-remove-packages` mutates packages
- **THEN** it uses the selected Topic Workspace Pixi environment and records the Pixi route, changed environment files, verification evidence, blockers, and next action
- **AND** it does not create local `venv`, `.venv`, or `virtualenv` environments, run ambient `pip`, mutate system package managers, run `sudo`, edit global shell profiles, or perform machine-global package setup

#### Scenario: Package update and removal are verified
- **WHEN** `env-update-packages` or `env-remove-packages` changes the selected Topic Workspace environment
- **THEN** it verifies relevant imports, libraries, CLI tools, minimal outputs, or task-specific smoke checks after mutation
- **AND** it reports dependency conflicts, failed checks, skipped heavy checks, and rollback or repair guidance as blockers or next actions

### Requirement: Environment Verification Commands
The Topic Manager skill SHALL expose explicit verification commands for topic, actor, and agent environment readiness without replacing setup services.

#### Scenario: Topic verification uses topic setup evidence
- **WHEN** `env-verify-topic` verifies Topic Workspace readiness
- **THEN** it uses existing topic env target spec and gate evidence when available
- **AND** it routes missing full gate-driven setup to `isomer-srv-topic-env-setup`

#### Scenario: Actor verification uses actor cwd
- **WHEN** `env-verify-actors` verifies selected Topic Actors
- **THEN** it runs or delegates the derived actor env gate from each resolved `topic.actors.workspace` cwd and reports per-actor readiness, commands, support-label evidence, blockers, and next action

#### Scenario: Agent verification delegates formal agent cwd proof
- **WHEN** `env-verify-agents` is asked to prove formal Agent Workspace cwd readiness
- **THEN** it routes to `isomer-srv-agent-env-setup` with selected Research Topic, Topic Workspace, role binding source, Agent Names, and semantic path expectations
- **AND** it reports returned service evidence without claiming runtime launch readiness

### Requirement: Topic Manager Output Contract
The Topic Manager skill SHALL split initialized-topic results into Essential Output and Complete Output.

#### Scenario: Essential output reports initialized-topic state
- **WHEN** `isomer-admin-topic-mgr` reports a result without a complete-output request
- **THEN** it reports status, Research Topic ref, Topic Workspace ref, relevant semantic paths, actor or team workspace summaries when relevant, environment mutation or verification summary when relevant, changed paths, blockers, and next action

#### Scenario: Complete output preserves audit detail
- **WHEN** complete output is requested from `isomer-admin-topic-mgr`
- **THEN** it reports semantic path sources, Topic Workspace Manifest evidence, Topic Actor bindings, Agent Workspace plans, package request source, package mutation plan, verification commands, service evidence, boundary material, validation status, blockers, and next action when those fields apply

### Requirement: Topic Manager Package Mutation Uses Package Specifics First
The Topic Manager environment mutation commands SHALL consult `isomer-misc-pkg-specifics` for every named package before applying generic install, update, remove, source-selection, or verification rules.

#### Scenario: Package install checks package-specific guidance first
- **WHEN** `env-install-packages` receives a named package request
- **THEN** it checks `isomer-misc-pkg-specifics` before choosing a generic PyPI, Pixi, Conda, R, CLI, runtime-wiring, or verification route
- **AND** it records selected package-specific evidence or `no package-specific rule` in the install plan

#### Scenario: Package update checks package-specific guidance first
- **WHEN** `env-update-packages` receives a named package update, downgrade, or constraint request
- **THEN** it checks `isomer-misc-pkg-specifics` before choosing a generic update route
- **AND** it preserves package-specific variant, accelerator, runtime, compatibility, and verification expectations in the update plan

#### Scenario: Package removal checks package-specific risk first
- **WHEN** `env-remove-packages` receives a named package removal request
- **THEN** it checks `isomer-misc-pkg-specifics` for known runtime, accelerator, or companion-package caveats before planning removal
- **AND** it reports package-specific breakage risks, verification checks, or blockers before mutation

#### Scenario: Package-specific verification outranks generic import checks
- **WHEN** an environment mutation command verifies a package with package-specific runtime guidance
- **THEN** it uses the package-specific verification expectation
- **AND** it does not report ready from solver success, package metadata, or generic import success alone when the package-specific rule requires stronger evidence

### Requirement: Topic Manager Package Mutation Keeps Topic Workspace Pixi Ownership
The Topic Manager package mutation commands SHALL continue to mutate only the selected Topic Workspace Pixi environment and SHALL NOT route ad hoc package mutation to full topic env setup unless the user asks for full gate-driven setup.

#### Scenario: Ad hoc package request stays in topic manager
- **WHEN** a user asks only to install, update, remove, repair, or verify named packages for an initialized Topic Workspace
- **THEN** Topic Manager handles the request through the matching `env-*` command
- **AND** it uses package-specific guidance as a preflight before generic package planning

#### Scenario: Full gate setup still routes to topic env service
- **WHEN** a package request requires deriving or repairing `topic.env.topic_setup_target_spec` from `topic.intent.topic_env_requirements`
- **THEN** Topic Manager routes full gate-driven setup or repair to `isomer-srv-topic-env-setup`
- **AND** it does not derive the operational topic env target spec itself

### Requirement: Topic Main Guidance Inspection
The Topic Manager skill SHALL report Topic Main Development Repository agent guidance posture during storage inspection.

#### Scenario: Storage inspection reports rule-file posture
- **WHEN** `isomer-admin-topic-mgr storage-inspect-main` inspects a usable normal non-bare `topic.repos.main`
- **THEN** it reports whether root-level `AGENTS.md` and `CLAUDE.md` exist
- **AND** it reports whether each file contains the current Isomer-managed topic-main guidance block
- **AND** it reports missing, stale, duplicated, malformed, or unknown-version guidance blocks as blockers or next actions

#### Scenario: Storage inspection remains non-destructive
- **WHEN** `storage-inspect-main` detects missing or stale topic-main guidance without an explicit repair request
- **THEN** it reports the condition and the recommended repair route
- **AND** it does not create, append, update, delete, reset, or rewrite rule files

### Requirement: Topic Main Guidance Repair Route
The Topic Manager skill SHALL provide an explicit storage-scoped route for refreshing topic-main agent guidance after topic initialization.

#### Scenario: Explicit repair refreshes guidance
- **WHEN** the operator explicitly requests topic-main agent guidance repair or refresh for an initialized topic
- **THEN** the Topic Manager resolves `topic.repos.main` through `storage-resolve`
- **AND** it creates missing root-level `AGENTS.md` or `CLAUDE.md`
- **AND** it appends or updates the Isomer-managed topic-main guidance block without changing unrelated rule-file content
- **AND** it reports changed files, guidance block version, blockers, and next action

#### Scenario: Repair blocks on unsafe repository state
- **WHEN** the resolved `topic.repos.main` is missing, not a normal Git repository, bare, corrupt, ambiguous, or otherwise unsafe for bounded rule-file mutation
- **THEN** the Topic Manager reports a blocker
- **AND** it routes canonical repository repair to `isomer-srv-topic-env-setup` when repository preparation is needed

### Requirement: Topic Manager Uses CLI Topic Main Guidance Source
The Topic Manager skill SHALL use `isomer-cli project topic-main-guidance` as the source of truth for topic-main agent guidance inspection and repair.

#### Scenario: Storage inspection routes guidance checks to CLI
- **WHEN** `storage-inspect-main` reports root `AGENTS.md` and `CLAUDE.md` guidance posture
- **THEN** it routes the read-only check through `isomer-cli --print-json project topic-main-guidance inspect --topic <topic>` or an equivalent CLI-backed API
- **AND** it reports target statuses, guidance version, blockers, and next action from that command

#### Scenario: Storage repair routes guidance mutation to CLI
- **WHEN** the operator explicitly requests topic-main agent guidance repair or refresh
- **THEN** the Topic Manager routes mutation through `isomer-cli --print-json project topic-main-guidance ensure --topic <topic> --yes` or an equivalent CLI-backed API
- **AND** it does not carry the full guidance body in the skill instructions

#### Scenario: Topic Manager does not duplicate template text
- **WHEN** operator skillset validation inspects Topic Manager documentation
- **THEN** it accepts concise references to the CLI command, marker names, and `.j2` template source of truth
- **AND** it reports diagnostics if Topic Manager docs reintroduce the full guidance block body as copied prose

