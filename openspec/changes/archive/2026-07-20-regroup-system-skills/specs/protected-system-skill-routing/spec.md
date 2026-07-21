## ADDED Requirements

### Requirement: Public System Skills Are Pack Entrypoints
The system SHALL expose packaged Isomer capabilities to ordinary user and host discovery through exactly one core public pack and one public pack for each installed optional extension.

#### Scenario: All packaged extensions are installed
- **WHEN** a supported agent host lists top-level Isomer skills after core, DeepSci, and Kaoju installation
- **THEN** the Isomer list contains `isomer-op-entrypoint`, `isomer-ext-deepsci-entrypoint`, and `isomer-ext-kaoju-entrypoint`
- **AND** it does not contain an independently projected top-level protected capability

#### Scenario: Core is installed alone
- **WHEN** a user installs the default core selection
- **THEN** the host receives `isomer-op-entrypoint` as the only top-level Isomer pack
- **AND** optional DeepSci and Kaoju packs remain absent

#### Scenario: Protected is interpreted as visibility
- **WHEN** documentation defines a protected system-skill capability
- **THEN** it defines protected as parent-routed and omitted from ordinary top-level discovery
- **AND** it does not claim filesystem secrecy, encryption, or an authorization boundary

### Requirement: Protected Capabilities Are Parent-Owned Subskills
Every manifest-declared non-entrypoint logical system-skill capability SHALL be a self-contained subskill below exactly one public pack at `subskills/<logical-id>/`.

#### Scenario: Protected capability is inspected
- **WHEN** a manifest-declared protected capability is inspected
- **THEN** its path is below its owning public pack's `subskills/` directory
- **AND** it contains `SKILL.md` and every active bundle-local resource needed for its workflow
- **AND** it is not independently listed as a public install unit

#### Scenario: Parent route table is inspected
- **WHEN** a public pack owns protected capabilities
- **THEN** its `SKILL.md` lists each scoped member name and route in a Subskills or Subcommands section
- **AND** every route resolves to one manifest-declared protected capability inside that pack

#### Scenario: Existing workflow boundaries are preserved
- **WHEN** a flat skill becomes a protected subskill
- **THEN** its triggers, gates, callbacks, inputs, outputs, blockers, subcommands, and owner boundaries remain effective unless another accepted requirement changes them

### Requirement: Resource Ownership Determines Command or Subskill Form
The system SHALL model a procedure as a direct or nested subcommand when it uses resources owned by its containing skill or subskill, and SHALL model a capability as a subskill when it needs a private bundled-resource boundary. Private SHALL mean scoped ownership and lifecycle, not secrecy or access control.

#### Scenario: Procedure uses containing resources
- **WHEN** a procedure needs only the scripts, references, assets, templates, runtime metadata, and support files owned by its containing skill or subskill
- **THEN** it is authored as a direct or nested subcommand
- **AND** any command detail page or child command page remains owned by that containing bundle

#### Scenario: Capability needs privately owned resources
- **WHEN** a capability needs its own scripts, references, commands, assets, templates, runtime metadata, or other support files that should be maintained, loaded, validated, or projected as one scoped bundle
- **THEN** it is authored as a subskill with its own `SKILL.md` and bundle boundary
- **AND** workflow size or complexity alone does not determine the form

#### Scenario: Existing protected capability is classified
- **WHEN** migration inspects an existing non-entrypoint system skill with its own `SKILL.md`, `agents/openai.yaml`, and active support resources
- **THEN** it retains those private resources inside one protected subskill bundle
- **AND** parent-owned command families without an independent resource bundle remain commands

### Requirement: Public Invocation Uses Entrypoint Subcommands
Each public pack SHALL implement the Imsight public invocation convention while keeping protected member designators internal to parent routing.

#### Scenario: User names a public subcommand
- **WHEN** a user invokes `$<public-entrypoint> use <subcommand> to <task>`
- **THEN** the entrypoint resolves the public subcommand, selects the applicable protected route or parent-owned command page, and proceeds with the task

#### Scenario: Invocation is empty
- **WHEN** a public entrypoint is invoked without a task or subcommand
- **THEN** it behaves as `use help`
- **AND** it reports its public commands without advertising protected capabilities as independent top-level skills

#### Scenario: Task-only invocation is concrete
- **WHEN** a user invokes a public entrypoint with a concrete task but no subcommand
- **THEN** the entrypoint selects the applicable public command or protected member
- **AND** it proceeds or reports a blocker instead of stopping after route enumeration

#### Scenario: Internal page invokes a protected member
- **WHEN** an active page routes to a protected member or its subcommand
- **THEN** it uses a catalog-declared object designator such as `isomer-ext-deepsci-entrypoint->scout` or `isomer-op-entrypoint->project->init-project()`
- **AND** the page declares the standard `skill_invocation_notation` frontmatter value

### Requirement: Object Invocation Syntax Distinguishes Capability Kinds
The system SHALL use bare object components for skill and protected subskill entrypoints and SHALL require `()` on every subcommand component.

#### Scenario: Protected member entrypoint is designated
- **WHEN** the catalog emits the invocation designator for protected member `scout`
- **THEN** the canonical designator is `isomer-ext-deepsci-entrypoint->scout`
- **AND** it does not end in `()`

#### Scenario: Protected member subcommand is designated
- **WHEN** an internal page invokes subcommand `init-project` of protected member `project`
- **THEN** the canonical designator is `isomer-op-entrypoint->project->init-project()`
- **AND** the bare `project` component identifies the protected subskill while `init-project()` identifies its command

#### Scenario: Parent command exposes a child command
- **WHEN** an internal page invokes child command `list` declared by parent command `manage-survey` of the Kaoju entrypoint
- **THEN** the canonical designator is `isomer-ext-kaoju-entrypoint->manage-survey()->list()`
- **AND** every command component has `()`
- **AND** `manage-survey()` generates its declared child-routing context without implicitly executing its standalone terminal workflow
- **AND** `list()` is the terminal invoked command

#### Scenario: Child command exposes a grandchild command
- **WHEN** the Kaoju paper-template manager invokes `put` declared by child command `file`
- **THEN** the canonical designator is `isomer-ext-kaoju-entrypoint->manage-paper-template()->file()->put()`
- **AND** both intermediate commands act as declared object generators while `put()` is the terminal invoked command
- **AND** the separate `--kind content|latex` role parameter does not become a bare or parenthesized capability component

#### Scenario: Parent command is invoked terminally
- **WHEN** an invocation ends at `X->parent()`
- **THEN** it executes the parent's declared standalone workflow
- **AND** a routing-only parent instead follows its explicitly declared help, selection, or blocker behavior

#### Scenario: Command chain returns to a bare component
- **WHEN** an invocation appends a bare component after any parenthesized command component
- **THEN** validation rejects the designator because command chains may contain only declared parenthesized command descendants

#### Scenario: Parent declares same-name routes
- **WHEN** one public pack declares protected member `gui` and public subcommand `gui`
- **THEN** `isomer-op-entrypoint->gui` invokes the protected member entrypoint
- **AND** `isomer-op-entrypoint->gui()` invokes the public subcommand
- **AND** catalog and help output report each route's declared capability kind

#### Scenario: Entrypoint uses callable syntax
- **WHEN** active guidance or catalog metadata uses `X()` or `X->Y()` to identify a skill or protected subskill entrypoint
- **THEN** skill validation rejects the designator instead of inferring its kind from prose context

### Requirement: Capability Identity Is Independent of Pack Layout
The system SHALL distinguish a public pack identity, a stable protected logical capability id, and a parent-owned invocation designator.

#### Scenario: Protected capability metadata is loaded
- **WHEN** the catalog loads a protected capability
- **THEN** it reports the capability's unique logical id, owning pack id, scoped member name, nested source path, and canonical invocation designator
- **AND** no one field is inferred by parsing another field's spelling

#### Scenario: Durable consumer names a protected capability
- **WHEN** a User Skill Callback, Skill Binding Projection, provenance record, or package-owned route refers to an existing protected capability
- **THEN** it continues to use the capability's preserved logical id
- **AND** runtime routing resolves the current invocation designator through catalog metadata

#### Scenario: Old pipeline id is encountered
- **WHEN** compatibility lookup receives `isomer-deepsci-pipeline` or `isomer-kaoju-pipeline`
- **THEN** it resolves to `isomer-ext-deepsci-entrypoint` or `isomer-ext-kaoju-entrypoint` respectively
- **AND** new output identifies the old id as deprecated without requiring a compatibility skill folder

### Requirement: Protected Projection Includes Dependency Closure
The system SHALL resolve protected logical capabilities and their declared dependencies for bounded internal or role-specific projection without turning those capabilities into public install units.

#### Scenario: One protected capability is selected internally
- **WHEN** an Isomer adapter requests a protected logical id for an Agent Role, Agent Profile, Topic Actor, or Service Agent
- **THEN** catalog resolution returns the selected nested source path and the deterministic transitive dependency closure
- **AND** each result retains its logical id, owning pack, and invocation designator

#### Scenario: Dependency crosses pack areas
- **WHEN** a protected research member depends on a core shared or service capability
- **THEN** the dependency graph records the cross-pack logical-id edge
- **AND** bounded projection includes the dependency without exposing either member as an ordinary user entrypoint

#### Scenario: Dependency graph is invalid
- **WHEN** a protected dependency names an unknown logical id or creates a cycle
- **THEN** manifest loading and skill validation fail with a deterministic diagnostic

### Requirement: Protected Members Remain Independently Verifiable
Every protected member SHALL retain enough identity and version metadata for package validation, callback lookup, and bounded private projection.

#### Scenario: Protected member metadata is inspected
- **WHEN** a nested protected bundle is inspected
- **THEN** its folder and `SKILL.md` frontmatter retain the protected logical id
- **AND** its `agents/openai.yaml` version exactly matches the package project version

#### Scenario: Public pack integrity is checked
- **WHEN** status or explicit-root inspection verifies a public pack
- **THEN** it checks every declared protected member path, identity, version, and required active resource
- **AND** one missing or mismatched member prevents complete pack status
