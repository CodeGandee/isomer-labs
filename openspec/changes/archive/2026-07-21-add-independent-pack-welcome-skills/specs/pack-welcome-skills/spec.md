## ADDED Requirements

### Requirement: Every Public Pack Provides an Independent Welcome Skill
The packaged system-skill catalog SHALL provide one independently discoverable welcome skill beside the execution entrypoint for the core, DeepSci, and Kaoju packs.

#### Scenario: Public welcome inventory is inspected
- **WHEN** all packaged Isomer packs are listed
- **THEN** core exposes `isomer-op-welcome` beside `isomer-op-entrypoint`
- **AND** DeepSci exposes `isomer-ext-deepsci-welcome` beside `isomer-ext-deepsci-entrypoint`
- **AND** Kaoju exposes `isomer-ext-kaoju-welcome` beside `isomer-ext-kaoju-entrypoint`

#### Scenario: Welcome is physically independent
- **WHEN** a welcome skill bundle is inspected
- **THEN** it is a top-level public package resource and host projection rather than an entrypoint subskill
- **AND** it owns its `SKILL.md`, `agents/openai.yaml`, and active newcomer references without loading private resources from the sibling entrypoint

#### Scenario: Protected members remain entrypoint-owned
- **WHEN** the pack's protected capability inventory is inspected
- **THEN** protected subskills remain below the execution entrypoint's `subskills/` directory
- **AND** the welcome skill owns no protected capability and is not an alternate parent for protected invocation designators

### Requirement: Welcome Skills Teach Newcomer Usage Patterns
Each welcome skill SHALL explain what its pack is mainly designed for and teach representative ways to request those tasks before asking the user to invoke the execution entrypoint.

#### Scenario: Default welcome is invoked
- **WHEN** a user invokes a welcome skill without a subcommand or asks a broad how-to or onboarding question
- **THEN** the skill gives a concise one-sentence pack introduction and presents several high-value typical use cases
- **AND** it explains the distinction between read-only welcome guidance and route-and-proceed entrypoint execution

#### Scenario: Typical use case is presented
- **WHEN** welcome guidance describes a typical use case
- **THEN** it states when the pattern is useful, representative user phrases or routing cues, required context, the canonical entrypoint command or task form, one exact invocation example, expected action, mutation posture, and likely next step
- **AND** it does not describe representative phrases as a required hidden parser grammar

#### Scenario: Source metadata informs authored guidance
- **WHEN** maintainers create or refresh welcome guidance from entrypoint commands or protected-subskill metadata
- **THEN** they adapt and synthesize the information for a newcomer in the context already established by the welcome skill
- **AND** they do not simply copy command descriptions, subskill frontmatter, or entrypoint route-table sentences verbatim

### Requirement: Welcome Skills Expose a Common Read-Only Command Shape
Every welcome skill SHALL expose common commands for options, path choice, command mapping, next-step recommendation, and help while remaining non-mutating.

#### Scenario: Common welcome commands are inspected
- **WHEN** a core or extension welcome `SKILL.md` is inspected
- **THEN** it exposes `show-options`, `choose-path`, `show-command-map`, `next-step`, and `help`
- **AND** default invocation selects concise newcomer help or options

#### Scenario: Complete command map is requested
- **WHEN** the user invokes `show-command-map`
- **THEN** welcome reports every current public command of the sibling execution entrypoint exactly once with a one-sentence use condition and an exact invocation form
- **AND** manifest-aware validation detects missing, extra, duplicated, or stale command ids

#### Scenario: Context-aware next step is requested
- **WHEN** `next-step` needs Project or extension context to make a useful recommendation
- **THEN** welcome announces and performs only applicable read-only inspection
- **AND** it recommends a concrete entrypoint invocation without executing that invocation

### Requirement: Welcome Skills Hand Off Concrete Work
Welcome skills SHALL route concrete tasks to the matching execution entrypoint and SHALL not perform owner workflow mutation themselves.

#### Scenario: User selects a core task
- **WHEN** core welcome resolves a concrete Project, Topic, GUI, identity, extension-management, Toolbox, environment, or team task
- **THEN** it recommends `$isomer-op-entrypoint use <command> to <task>` or a concrete task-only `$isomer-op-entrypoint` invocation
- **AND** it does not invoke a protected logical id directly

#### Scenario: User selects an extension task
- **WHEN** DeepSci or Kaoju welcome resolves a concrete research task
- **THEN** it recommends the matching `$isomer-ext-<extension-id>-entrypoint use <command> to <task>` or task-only entrypoint invocation
- **AND** it preserves any prerequisite, Gate, interaction, and mutation boundary described by the selected entrypoint command

#### Scenario: Concrete task triggers welcome implicitly
- **WHEN** host routing selects a welcome skill for a request that is already concrete and actionable
- **THEN** welcome performs no mutation and hands the task to the sibling entrypoint
- **AND** it does not require the user to repeat supplied task context

### Requirement: Core Welcome Covers Typical Platform Work
`isomer-op-welcome` SHALL teach the common platform and research-start paths a newcomer needs before using `isomer-op-entrypoint`.

#### Scenario: Core options are shown
- **WHEN** core welcome shows typical use cases
- **THEN** it covers Project initialization and inspection, manual Research Topic setup, formal Agent Team setup, Topic management, Project Web GUI work, identity posture, optional system-skill extensions, project-local Toolboxes, and environment or package support
- **AND** it distinguishes manual versus Agent Team topology from DeepSci versus Kaoju research paradigm selection

#### Scenario: Core extension paths are shown
- **WHEN** core welcome introduces DeepSci or Kaoju
- **THEN** it names the matching extension welcome skill for learning that paradigm
- **AND** it names the matching extension entrypoint only when showing how concrete work starts

#### Scenario: Historical start paths remain available
- **WHEN** core welcome commands are inspected
- **THEN** it retains read-only guidance for `start-research-manually`, `start-research-by-agent-team`, `start-deepsci-research`, `start-kaoju-survey`, and `show-extensions`
- **AND** each path ends in a current public welcome or entrypoint invocation

### Requirement: DeepSci Welcome Covers Typical Production-Research Work
`isomer-ext-deepsci-welcome` SHALL teach representative hypothesis-driven production-research patterns supported by the DeepSci pack.

#### Scenario: DeepSci options are shown
- **WHEN** DeepSci welcome shows typical use cases
- **THEN** it covers hypothesis development, empirical evaluation, experiment and analysis iteration, paper development, revision, rebuttal, and polish or finalization patterns
- **AND** it explains which public pass command or task-only entrypoint request fits each pattern

#### Scenario: DeepSci readiness is absent
- **WHEN** a selected DeepSci pattern lacks Topic Workspace, actor or agent workspace, environment, or DeepSci bootstrap readiness
- **THEN** welcome explains the prerequisite at a newcomer level and recommends the core or DeepSci entrypoint route that owns recovery
- **AND** it does not fabricate readiness or start recovery itself

### Requirement: Kaoju Welcome Covers Typical Evidence-Led Survey Work
`isomer-ext-kaoju-welcome` SHALL teach representative evidence-led literature, code, dataset, model, trial, comparison, paper, and wiki-survey patterns supported by the Kaoju pack.

#### Scenario: Kaoju options are shown
- **WHEN** Kaoju welcome shows typical use cases
- **THEN** it covers landscape discovery, reading-list construction and ingestion, direction framing, evidence comparison, source-code intake, environment preparation, code trials, survey synthesis, paper production, and wiki export
- **AND** it explains which public Kaoju command or task-only entrypoint request fits each pattern

#### Scenario: Kaoju interaction boundary is explained
- **WHEN** a typical Kaoju use case requires scope clarification, source selection, template choice, execution approval, or another Gate
- **THEN** welcome identifies that interaction boundary before showing the entrypoint example
- **AND** it does not imply that the example invocation pre-approves later governed actions

### Requirement: Welcome Skill Validation Is Pack-Aware
The repository SHALL validate independent welcome skills as newcomer teaching contracts and as members of complete public packs.

#### Scenario: Valid welcome pack passes
- **WHEN** skill validation runs against a valid core, DeepSci, or Kaoju pack
- **THEN** it checks welcome identity, public role, self-contained resources, common commands, read-only posture, entrypoint handoffs, typical-use-case fields, complete command-map coverage, and pack-specific use-case categories

#### Scenario: Welcome guidance exposes a protected id
- **WHEN** active welcome guidance tells users to invoke a protected logical id or parent-owned object designator directly
- **THEN** validation reports the offending route and the required public entrypoint form

#### Scenario: Welcome teaching drifts from entrypoint commands
- **WHEN** a welcome command map omits a current entrypoint command or names a command absent from the manifest
- **THEN** validation fails with the welcome skill, entrypoint, and mismatched command id
