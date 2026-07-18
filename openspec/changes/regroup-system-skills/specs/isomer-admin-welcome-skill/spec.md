## MODIFIED Requirements

### Requirement: Welcome Skill Presents Operator Workflow Options
The `isomer-op-welcome` logical capability SHALL remain a read-only protected member of `isomer-op-entrypoint`, and its visible orientation commands SHALL also be available through the public parent.

#### Scenario: Public help prints option menu
- **WHEN** the public core entrypoint receives empty invocation, `use help`, `use show-options`, or a broad onboarding request
- **THEN** it uses the protected welcome procedure to list `start-research-manually`, `start-research-by-agent-team`, `start-deepsci-research`, and `start-kaoju-survey`
- **AND** it lists supported Project, Topic, extension, GUI, identity, Toolbox, team, and Houmao actions
- **AND** each action names the public entrypoint and public subcommand or task form rather than a direct protected invocation

#### Scenario: Menu avoids tutorial-first behavior
- **WHEN** orientation output is printed
- **THEN** it prioritizes available workflows and the next public invocation
- **AND** it does not primarily present a conceptual introduction

#### Scenario: Welcome is not a top-level skill
- **WHEN** core installation is inspected
- **THEN** `isomer-op-welcome` exists only below `isomer-op-entrypoint/subskills/`
- **AND** no top-level `isomer-op-welcome` projection is installed

### Requirement: Welcome Skill Routes Only to Active Owner Skills
The protected welcome member SHALL describe active owners through parent-scoped routes and public extension entrypoints.

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

### Requirement: Welcome Skill Exposes Focused Subcommands
The public core entrypoint SHALL expose the accepted welcome routines while the protected welcome member owns their read-only procedure detail.

#### Scenario: Typical usage paths are first-class
- **WHEN** `isomer-op-entrypoint` help is inspected
- **THEN** it lists `start-research-manually`, `start-research-by-agent-team`, `start-deepsci-research`, and `start-kaoju-survey`
- **AND** each route states its public invocation, intent, safe first action, mutation boundary, and next action

#### Scenario: Orientation commands are documented
- **WHEN** public core help is inspected
- **THEN** it documents `help`, `show-options`, `show-extensions`, `choose-path`, `show-skill-map`, and `next-step`
- **AND** their detailed pages remain owned by the protected welcome bundle or parent routing resources

### Requirement: Welcome Skill Exposes Optional Research Paradigms
Welcome guidance SHALL expose DeepSci and Kaoju through their public extension entrypoints without conflating research paradigm and execution topology.

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
The protected welcome member SHALL use package-catalog discovery while distinguishing public pack evidence from Project declaration and host integrity evidence.

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
Welcome guidance SHALL use the public core or extension entrypoint to move from read-only orientation to concrete execution.

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

### Requirement: Welcome Skill Exposes Toolbox Manager Owner Route
Welcome guidance SHALL expose Toolbox management through the protected `toolbox` member without exposing its logical id as a public skill.

#### Scenario: Default options include Toolbox management
- **WHEN** default options are printed
- **THEN** Project-local Toolbox operations are included
- **AND** the public example uses `$isomer-op-entrypoint use toolbox to <task>`

#### Scenario: Tool packs remain separate
- **WHEN** a user asks about installable dependency bundles rather than Toolbox configuration
- **THEN** guidance distinguishes protected `tool-packs` support from protected `toolbox` management
