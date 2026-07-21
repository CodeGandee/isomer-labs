# isomer-op-welcome-skill Specification

## Purpose
TBD - created by archiving change add-isomer-op-welcome-skill. Update Purpose after archive.
## Requirements
### Requirement: Welcome Skill Presents Operator Workflow Options
`isomer-op-welcome` SHALL be an independent public, newcomer-oriented, read-only skill that explains common Isomer workflows and how to request them through `isomer-op-entrypoint`.

#### Scenario: Welcome assets are inspected
- **WHEN** the packaged core public skills are inspected
- **THEN** `operator/isomer-op-welcome` contains its own `SKILL.md`, `agents/openai.yaml`, and directly linked onboarding references
- **AND** no copy exists below `isomer-op-entrypoint/subskills/`

#### Scenario: Default welcome is invoked
- **WHEN** the public welcome receives empty invocation or a broad onboarding request
- **THEN** it introduces Isomer's main Project and research workflows in newcomer language
- **AND** it presents representative entrypoint request forms before exhaustive command details

#### Scenario: Public option menu is requested
- **WHEN** the user invokes `show-options`
- **THEN** welcome lists common Project, Topic, manual research, Agent Team, DeepSci, Kaoju, GUI, identity, extension-management, Toolbox, and environment-support patterns
- **AND** each pattern ends in a current public entrypoint or extension welcome route

#### Scenario: Menu avoids tutorial-first behavior
- **WHEN** orientation output is printed
- **THEN** it prioritizes available workflows and the next public invocation
- **AND** it does not primarily present a conceptual introduction
### Requirement: Welcome Skill Routes Only to Active Owner Skills
The public welcome skill SHALL describe active execution owners through public entrypoint forms and SHALL not expose protected logical ids as direct user invocations.

#### Scenario: Supported core path is shown
- **WHEN** welcome maps a core workflow
- **THEN** it provides `$isomer-op-entrypoint use <command> to <task>` or a concrete task-only invocation
- **AND** it may explain the owner area without instructing direct `isomer-op-*`, `isomer-srv-*`, or `isomer-misc-*` protected invocation

#### Scenario: Supported extension path is shown
- **WHEN** welcome introduces DeepSci or Kaoju typical use cases
- **THEN** it routes learning to `isomer-ext-deepsci-welcome` or `isomer-ext-kaoju-welcome`
- **AND** it routes concrete work to `isomer-ext-deepsci-entrypoint` or `isomer-ext-kaoju-entrypoint`

#### Scenario: Retired route is encountered
- **WHEN** active welcome guidance is inspected
- **THEN** it excludes retired workspace-manager, topic-preparation, manual-session, admin, old pipeline, and `isomer-op-entrypoint->welcome` routes

#### Scenario: Supported core paths use scoped routes
- **WHEN** welcome guidance maps a core workflow
- **THEN** it names the applicable `isomer-op-entrypoint-><member>` route and a public `$isomer-op-entrypoint use <subcommand> to <task>` example
- **AND** it does not tell users to invoke `isomer-op-*`, `isomer-srv-*`, or `isomer-misc-*` protected ids directly

#### Scenario: Supported research paths use public extension entrypoints
- **WHEN** welcome guidance maps a DeepSci or Kaoju workflow
- **THEN** it names `isomer-ext-deepsci-entrypoint` or `isomer-ext-kaoju-entrypoint`

#### Scenario: Retired skills are not active routes
- **WHEN** welcome guidance is inspected
- **THEN** it excludes retired workspace-manager, topic-preparation, manual-session, admin, and old pipeline public routes
### Requirement: Welcome Skill Stays Read-Only by Default
The independent welcome skill SHALL remain read-only for default, explicit, and implicit orientation requests.

#### Scenario: User chooses an option
- **WHEN** a user selects a typical use case or asks welcome to choose a path
- **THEN** welcome explains the recommended entrypoint invocation, prerequisites, expected mutation, and next step
- **AND** it does not execute that entrypoint or treat selection as mutation authorization

#### Scenario: Read-only context improves recommendation
- **WHEN** `next-step` needs current Project or extension context
- **THEN** welcome announces and runs only documented read-only inspection commands
- **AND** it reports the evidence used before recommending an execution route

#### Scenario: Concrete task reaches welcome
- **WHEN** implicit host selection routes a concrete task to welcome
- **THEN** welcome hands the complete task context to `isomer-op-entrypoint`
- **AND** it performs no owner mutation itself

#### Scenario: Welcome option selection does not mutate state
- **WHEN** a user asks the welcome skill what path to choose
- **THEN** the skill may recommend an owner skill and safe first command
- **AND** it does not initialize Projects, create Research Topics, mutate Topic Workspaces, install packages or system-skill extensions, register Project extension declarations, specialize teams, launch agents, or bootstrap research-paradigm artifacts

#### Scenario: Context-aware next step uses read-only inspection
- **WHEN** the user asks for a context-aware next step and a Project context is available
- **THEN** the skill may use read-only commands such as `isomer-cli project validate`, `isomer-cli doctor`, `isomer-cli project topics list`, or `isomer-cli project context show`
- **AND** it reports blockers and the recommended owner workflow without running mutating commands
### Requirement: Welcome Skill Exposes Focused Subcommands
`isomer-op-welcome` SHALL expose focused public commands for typical-use-case discovery, complete command mapping, path choice, extension discovery, context-aware recommendation, historical start paths, and help.

#### Scenario: Core welcome commands are inspected
- **WHEN** `isomer-op-welcome/SKILL.md` is inspected
- **THEN** it exposes `show-options`, `show-extensions`, `choose-path`, `show-command-map`, `next-step`, `start-research-manually`, `start-research-by-agent-team`, `start-deepsci-research`, `start-kaoju-survey`, and `help`
- **AND** each command links to one self-contained local page or bounded workflow

#### Scenario: Command map is complete
- **WHEN** `show-command-map` is inspected or invoked
- **THEN** it covers every current `isomer-op-entrypoint` public command exactly once
- **AND** each mapping contains a one-sentence use condition and exact public invocation

#### Scenario: Default output stays concise
- **WHEN** welcome is invoked without a specific command
- **THEN** it presents a curated set of high-value paths
- **AND** it loads the exhaustive command map only on explicit request or complete output

#### Scenario: Typical usage paths are first-class
- **WHEN** `isomer-op-entrypoint` help is inspected
- **THEN** it lists `start-research-manually`, `start-research-by-agent-team`, `start-deepsci-research`, and `start-kaoju-survey`
- **AND** each route states its public invocation, intent, safe first action, mutation boundary, and next action

#### Scenario: Orientation commands are documented
- **WHEN** public core help is inspected
- **THEN** it documents `help`, `show-options`, `show-extensions`, `choose-path`, `show-skill-map`, and `next-step`
- **AND** their detailed pages remain owned by the protected welcome bundle or parent routing resources
### Requirement: Welcome Skill Exposes Optional Research Paradigms
Core welcome SHALL introduce DeepSci and Kaoju through their independent welcome skills while distinguishing research paradigm from execution topology.

#### Scenario: DeepSci path is introduced
- **WHEN** core welcome describes hypothesis-driven production research
- **THEN** it recommends `$isomer-ext-deepsci-welcome` for typical use cases and command learning
- **AND** it shows `$isomer-ext-deepsci-entrypoint` only as the concrete execution surface

#### Scenario: Kaoju path is introduced
- **WHEN** core welcome describes evidence-led survey research
- **THEN** it recommends `$isomer-ext-kaoju-welcome` for typical use cases and command learning
- **AND** it shows `$isomer-ext-kaoju-entrypoint` only as the concrete execution surface

#### Scenario: Paradigm and topology remain independent
- **WHEN** manual, Agent Team, DeepSci, or Kaoju paths are compared
- **THEN** welcome explains that manual versus Agent Team selects execution topology and DeepSci versus Kaoju selects research paradigm
- **AND** it does not infer a formal Agent Team from extension choice

#### Scenario: DeepSci path is discoverable
- **WHEN** options or the skill map are printed
- **THEN** DeepSci is described as the hypothesis-driven production-research paradigm
- **AND** `isomer-ext-deepsci-entrypoint` is its public skill

#### Scenario: Kaoju path is discoverable
- **WHEN** options or the skill map are printed
- **THEN** Kaoju is described as the evidence-led survey paradigm
- **AND** `isomer-ext-kaoju-entrypoint` is its public skill

#### Scenario: Paradigm choice stays independent of topology
- **WHEN** manual, Agent Team, DeepSci, or Kaoju paths are explained
- **THEN** manual versus Agent Team selects execution topology and DeepSci versus Kaoju selects research paradigm
- **AND** selecting an extension does not imply a formal Agent Team
### Requirement: Welcome Skill Provides Read-Only Extension Discovery
Core welcome SHALL discover extension public pairs from package-owned catalog metadata and distinguish catalog, Project declaration, public-name observation, and verified pack evidence.

#### Scenario: Extension catalog is shown
- **WHEN** `show-extensions` runs
- **THEN** it reports each extension's welcome, execution entrypoint, description, and command summary from package metadata
- **AND** it does not maintain a duplicate extension inventory

#### Scenario: Evidence levels are reported
- **WHEN** extension state is available
- **THEN** welcome distinguishes catalog-known, Project-declared, welcome-seen, entrypoint-seen, and receipt or explicit-root verified states
- **AND** public-name observation alone does not prove complete pack integrity

#### Scenario: Extension lifecycle work is needed
- **WHEN** installation, upgrade, compatibility diagnosis, refresh, or repair is needed
- **THEN** welcome recommends `$isomer-op-entrypoint use system-skills to <task>`
- **AND** it does not mutate extension declarations or skill roots itself

#### Scenario: Extension catalog is discovered dynamically
- **WHEN** `show-extensions` runs through the public core entrypoint
- **THEN** it queries package-owned extension metadata for public entrypoints, commands, and protected member summaries
- **AND** it does not maintain a duplicate extension inventory

#### Scenario: Evidence levels remain distinct
- **WHEN** extension state is reported
- **THEN** output distinguishes catalog-known pack, Project-declared routing intent, entrypoint-seen inventory, and receipt or explicit-root verified integrity
- **AND** entrypoint-seen evidence alone does not prove complete protected coverage

#### Scenario: Lifecycle routes to protected owner
- **WHEN** installation, compatibility, refresh, or repair is needed
- **THEN** welcome guidance routes through `isomer-op-entrypoint->system-skills`
### Requirement: Welcome Skill Bridges Discovery to Execution
Core welcome SHALL translate newcomer goals into concrete public entrypoint requests without absorbing execution ownership.

#### Scenario: Core use case is selected
- **WHEN** a user selects or describes a core typical use case
- **THEN** welcome supplies one recommended `$isomer-op-entrypoint` invocation with the user's context carried forward
- **AND** it explains the expected action and mutation boundary

#### Scenario: Extension use case is selected
- **WHEN** a user needs more extension-specific orientation
- **THEN** welcome recommends the matching extension welcome
- **AND** when the task is already concrete it recommends the matching extension entrypoint instead

#### Scenario: Entry point compatibility route is used
- **WHEN** an established prompt invokes an entrypoint command formerly backed by protected welcome
- **THEN** the entrypoint may delegate read-only behavior to `$isomer-op-welcome` during the compatibility window
- **AND** `isomer-op-welcome` remains the sole owner of welcome procedure content

#### Scenario: Concrete core task uses informed entrypoint
- **WHEN** a user supplies a concrete core Isomer task
- **THEN** welcome guidance recommends `$isomer-op-entrypoint use <subcommand> to <task>` or task-only invocation
- **AND** the public entrypoint proceeds while the welcome member stays read-only

#### Scenario: Concrete extension task uses public extension
- **WHEN** a user selects a DeepSci or Kaoju workflow
- **THEN** welcome guidance recommends the matching `$isomer-ext-*-entrypoint use <subcommand> to <task>` form

#### Scenario: Extension terms remain distinct
- **WHEN** customization is explained
- **THEN** guidance distinguishes optional system-skill extensions, Project-local Toolboxes, and the `isomer-cli ext` runtime namespace
### Requirement: Welcome Skill Output Contract
The welcome skill SHALL optimize default output for first-time comprehension and provide full command mapping only on request.

#### Scenario: Essential output is returned
- **WHEN** welcome recommends a path
- **THEN** it states the interpreted goal, one-sentence use-case fit, required context, recommended public invocation, expected action, mutation posture, blocker or missing decision, and next step in natural-language Markdown

#### Scenario: Complete output is requested
- **WHEN** the user asks for complete, verbose, audit, debug, or full output
- **THEN** welcome includes alternate patterns, the complete command map, read-only context evidence, routing rationale, and excluded retired or protected direct routes

#### Scenario: Machine-readable output is requested
- **WHEN** the user explicitly requests JSON or another machine-readable format
- **THEN** welcome serializes the applicable orientation information without changing its read-only posture

#### Scenario: Essential output names route and next action
- **WHEN** the welcome skill recommends a path
- **THEN** it reports `status`, `interpreted_goal`, `recommended_workflow`, `owner_skill`, `safe_first_command`, `blockers`, and `next_action`

#### Scenario: Complete output adds evidence and alternatives
- **WHEN** the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output
- **THEN** the skill includes context evidence, read-only commands run, alternate owner workflows, routing rationale, and retired-route exclusions when relevant
### Requirement: Welcome Skill Exposes Toolbox Manager Owner Route
Welcome guidance SHALL expose Toolbox management through the protected `toolbox` member without exposing its logical id as a public skill.

#### Scenario: Default options include Toolbox management
- **WHEN** default options are printed
- **THEN** Project-local Toolbox operations are included
- **AND** the public example uses `$isomer-op-entrypoint use toolbox to <task>`

#### Scenario: Tool packs remain separate
- **WHEN** a user asks about installable dependency bundles rather than Toolbox configuration
- **THEN** guidance distinguishes protected `tool-packs` support from protected `toolbox` management

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

