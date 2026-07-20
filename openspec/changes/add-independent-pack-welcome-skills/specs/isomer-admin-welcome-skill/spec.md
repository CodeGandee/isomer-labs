## MODIFIED Requirements

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
