## MODIFIED Requirements

### Requirement: System Skills Are Package Assets
The system SHALL distribute official non-development Isomer system skills as package-owned public packs with protected nested capabilities under the `isomer_labs` package.

#### Scenario: Packaged root contains distributable pack material
- **WHEN** package resources are inspected for system skills
- **THEN** the packaged root contains `manifest.toml`, `README.md`, the core public pack, and the optional DeepSci and Kaoju public packs
- **AND** every non-entrypoint capability is below its owning pack's `subskills/` directory
- **AND** the packaged root does not contain `dev/`

#### Scenario: Manifest paths resolve inside package assets
- **WHEN** the system loads `assets/system_skills/manifest.toml`
- **THEN** every public pack path and protected capability path resolves below the packaged system-skill root
- **AND** each resolved pack and capability directory contains `SKILL.md`

#### Scenario: Protected capability is not duplicated
- **WHEN** package assets are inspected
- **THEN** no manifest-declared protected logical id also exists as an independently installable top-level skill directory

### Requirement: System Skills Can Be Materialized Safely
The system SHALL materialize manifest-selected public packs as whole top-level skill directories while preserving their protected nested paths.

#### Scenario: Materialize core group
- **WHEN** a caller materializes the `core` group to an empty target directory
- **THEN** the target receives `manifest.toml` and the complete `isomer-op-entrypoint` pack
- **AND** protected core capabilities remain below `isomer-op-entrypoint/subskills/`
- **AND** no protected capability is copied beside the public pack

#### Scenario: Materialize selected extension
- **WHEN** a caller materializes extension `deepsci` or `kaoju`
- **THEN** the target receives the core pack and the selected extension public pack
- **AND** it does not receive the unselected extension pack

#### Scenario: Development skills are never materialized from package assets
- **WHEN** a caller materializes any packaged system-skill selection
- **THEN** no `dev/` directory or `isomer-dev-*` skill is copied from package assets

### Requirement: Core Packaged Skills Include Entrypoint
The packaged core system-skill group SHALL use `operator/isomer-op-entrypoint` as its sole public pack and SHALL own all core operator, service, research-recording, and misc capabilities as protected members.

#### Scenario: Core manifest declares public pack
- **WHEN** `src/isomer_labs/assets/system_skills/manifest.toml` is inspected
- **THEN** the core group declares `operator/isomer-op-entrypoint` as its public pack path and `isomer-op-entrypoint` as its entry skill
- **AND** the listed path resolves below the packaged system-skill root

#### Scenario: Core materialization copies one public root
- **WHEN** a caller materializes the `core` group to an empty target directory
- **THEN** the target receives `isomer-op-entrypoint/SKILL.md`, its `agents/openai.yaml`, its directly linked resources, and every declared protected subskill
- **AND** it receives no other top-level Isomer skill directory

#### Scenario: Packaged discovery returns core pack and members
- **WHEN** code asks for catalog metadata for the `core` group
- **THEN** the result identifies one public pack and the ordered protected logical capabilities it owns
- **AND** it does not classify those protected members as independent public install units

### Requirement: System Skill Manifest Classifies Groups
The packaged system-skill manifest SHALL classify public packs and protected logical capabilities so callers can distinguish install units from routable capability members.

#### Scenario: Core group is always available
- **WHEN** the manifest loads the core pack
- **THEN** it declares `kind = "core"`, `always_available = true`, and no extension id
- **AND** it declares one public entry skill and its protected member inventory

#### Scenario: Extension pack has stable extension id
- **WHEN** the manifest loads a pack whose kind is extension
- **THEN** it declares a stable extension id, one `isomer-ext-<extension-id>-entrypoint` public skill, ordered public commands, and protected members
- **AND** callers can filter catalog metadata by extension id

#### Scenario: Protected capability metadata is complete
- **WHEN** the manifest loads a protected capability
- **THEN** it declares a logical id, pack id, nested path, scoped member name, invocation designator, area, dependencies, aliases, callback stages, and applicable compatibility floor

#### Scenario: Invalid classification is rejected
- **WHEN** a pack or protected capability omits required classification, conflicts with another identity, escapes its owning pack path, or declares an invalid extension id
- **THEN** manifest loading fails with a deterministic package asset diagnostic

### Requirement: System Skill Manifest Declares Callback Insertion Points
The packaged system-skill manifest SHALL declare callback stages against stable logical capability ids and SHALL provide their owning pack and invocation designators as catalog metadata.

#### Scenario: Stage definitions are loaded from manifest
- **WHEN** the system loads `assets/system_skills/manifest.toml`
- **THEN** callback insertion point stage ids, labels, and descriptions are derived from the manifest rather than hardcoded only in Python

#### Scenario: Per-capability insertion points use logical ids
- **WHEN** the manifest declares callback insertion points for a public entrypoint or protected capability
- **THEN** the declaration is keyed by its canonical logical id
- **AND** every stage resolves to a manifest stage definition
- **AND** every protected target resolves to one nested path and invocation designator

#### Scenario: Capability without declaration exposes no insertion point
- **WHEN** a packaged capability has no callback insertion point declaration
- **THEN** the system treats it as exposing no callback insertion points

#### Scenario: Callback discovery is deterministic
- **WHEN** code asks for packaged callback insertion points
- **THEN** the result is returned in manifest order with target logical id, pack id, nested skill path, invocation designator, group, optional extension id, stage id, and stage metadata

### Requirement: Public System Skill Installation Documentation
The system SHALL document public pack installation and protected routing for supported agent hosts.

#### Scenario: Install docs list public packs
- **WHEN** a user follows public system-skill installation documentation
- **THEN** the docs identify `isomer-op-entrypoint`, `isomer-ext-deepsci-entrypoint`, and `isomer-ext-kaoju-entrypoint` as the complete public Isomer surface
- **AND** they show repository or `isomer-cli system-skills` selection commands with an explicit target or agent scope

#### Scenario: Entrypoint is the invocation surface
- **WHEN** docs explain ordinary use
- **THEN** they demonstrate `$<public-entrypoint> use <subcommand> to <task>` and task-only routing
- **AND** they state that empty invocation means `help`

#### Scenario: Protected members are not user install choices
- **WHEN** docs describe operator, service, shared, DeepSci, or Kaoju members
- **THEN** they describe those members as parent-routed protected capabilities
- **AND** they do not instruct users to install or invoke them as separate top-level skills

#### Scenario: Host refresh is required after migration
- **WHEN** docs explain migration from a flat installation
- **THEN** they tell the user to run a managed upgrade and refresh the agent host or begin a new agent session

### Requirement: Core Packaged Skills Include Toolbox Manager
The packaged core public pack SHALL include `isomer-op-toolbox-mgr` as the protected `toolbox` member.

#### Scenario: Core manifest includes toolbox member
- **WHEN** the core protected inventory is inspected
- **THEN** it maps member `toolbox` to logical id `isomer-op-toolbox-mgr` below `operator/isomer-op-entrypoint/subskills/isomer-op-toolbox-mgr`
- **AND** it does not include `isomer-op-toolbox-creator`

#### Scenario: Core materialization nests toolbox manager
- **WHEN** the core pack is materialized
- **THEN** the Toolbox Manager bundle and its directly linked resources are copied below the parent pack
- **AND** no top-level `isomer-op-toolbox-mgr` directory is created

### Requirement: Core Isomer Skills Include Internal Houmao Bridge Support
The packaged core public pack SHALL retain Isomer-facing Houmao bridge and Topic Service Agent support as protected service members while keeping Houmao-owned projected material Project-local and opt-in.

#### Scenario: Core installation does not expose Houmao administration
- **WHEN** a user installs the core pack
- **THEN** no independent Houmao or `isomer-srv-*` skill is advertised as a public Isomer entrypoint
- **AND** Houmao procedures remain reachable through protected Isomer routing or an explicit advanced support path

#### Scenario: Core includes bridge members
- **WHEN** the core protected inventory is inspected
- **THEN** it includes logical ids `isomer-srv-houmao-interop` and `isomer-srv-topic-service-agent-support`
- **AND** those members can report disabled or not-configured integration without requiring live Houmao state

#### Scenario: Project-local Houmao projection remains opt-in
- **WHEN** a Project has not enabled Houmao integration
- **THEN** core pack installation does not create `.isomer-labs/houmao-skills/`

### Requirement: Core Packaged Skills Include GUI Manager
The packaged core public pack SHALL include `isomer-op-gui-mgr` as the protected `gui` member.

#### Scenario: Core manifest includes GUI member
- **WHEN** the core protected inventory is inspected
- **THEN** it maps member `gui` to logical id `isomer-op-gui-mgr` below `operator/isomer-op-entrypoint/subskills/isomer-op-gui-mgr`

#### Scenario: Core materialization nests GUI manager
- **WHEN** the core pack is materialized
- **THEN** the GUI Manager bundle and directly linked resources are copied below the parent pack
- **AND** no top-level `isomer-op-gui-mgr` directory is created

### Requirement: Packaged Kaoju Extension Group
The packaged catalog SHALL expose Kaoju as optional extension `kaoju` through public pack `isomer-ext-kaoju-entrypoint` with thirteen protected capability members.

#### Scenario: Kaoju manifest group is classified and complete
- **WHEN** `manifest.toml` is inspected
- **THEN** pack `kaoju` declares `kind = "extension"`, `extension_id = "kaoju"`, `always_available = false`, and public entry skill `isomer-ext-kaoju-entrypoint`
- **AND** it owns protected logical ids for shared, workspace, frame, discover, acquire, examine, reproduce, trial, compare, audit, synthesize, write, and export

#### Scenario: Kaoju paths resolve inside the pack
- **WHEN** Kaoju catalog metadata loads
- **THEN** every protected path resolves below `research-paradigm/kaoju/isomer-ext-kaoju-entrypoint/subskills/`
- **AND** every member contains its required skill metadata and active resources

#### Scenario: Kaoju materializes safely
- **WHEN** extension `kaoju` is selected
- **THEN** output includes core and the complete Kaoju public pack
- **AND** it does not include DeepSci unless selected

#### Scenario: Kaoju entry surface declares survey intents
- **WHEN** extension discovery metadata is queried for `kaoju`
- **THEN** it reports `isomer-ext-kaoju-entrypoint`, the accepted ordered public command inventory, and protected logical members from manifest metadata

#### Scenario: Kaoju role-aware baseline is packaged
- **WHEN** the Kaoju public pack and protected `write` member are materialized
- **THEN** public template-manager commands retain explicit content-versus-LaTeX role handling and the protected writer retains its private role-aware paper-production resources
- **AND** package-owned `isomer_labs.kaoju` services remain the machine authority for template state, composition, migration, validation, bindings, semantics, and process data

### Requirement: System Skill Manifest Describes Extension Entry Surfaces
The manifest SHALL describe each optional extension as one public entrypoint pack with ordered commands and protected members.

#### Scenario: Extension declares entrypoint and commands
- **WHEN** the system loads an extension pack
- **THEN** its entry skill belongs to the public pack path and matches `isomer-ext-<extension-id>-entrypoint`
- **AND** it declares an ordered public command list and protected capability inventory

#### Scenario: Extension discovery is package-derived
- **WHEN** code asks for packaged extensions
- **THEN** each result includes extension id, pack id, description, entry skill, public commands, public source path, and protected logical members
- **AND** the result does not depend on a repository checkout

#### Scenario: Invalid extension entry metadata is rejected
- **WHEN** an extension entry skill is missing, violates the naming rule, or has an invalid public command or member mapping
- **THEN** manifest loading fails with a deterministic diagnostic

### Requirement: Core Packaged Skills Include System Skill Manager
The core public pack SHALL include `isomer-op-system-skill-mgr` as the protected `system-skills` member.

#### Scenario: Core manifest includes manager member
- **WHEN** the core protected inventory is inspected
- **THEN** it maps `system-skills` to logical id `isomer-op-system-skill-mgr`
- **AND** the nested path resolves to a valid skill bundle

#### Scenario: Core catalog exposes route without public duplication
- **WHEN** system-skill catalog listing runs
- **THEN** it reports the manager as a protected core member routed by `isomer-op-entrypoint`
- **AND** it does not classify the manager as a public pack or optional extension

### Requirement: Extension Catalog Supports Inventory Classification
The catalog SHALL provide stable public pack membership and protected capability membership for receipt and inventory classification.

#### Scenario: Catalog maps extension pack and members
- **WHEN** internal inspection classifies receipt records or live inventory names
- **THEN** it derives the extension entrypoint, protected logical members, and expected nested paths from package-owned metadata
- **AND** agents do not maintain duplicate member lists

#### Scenario: Name-only inventory sees an entrypoint
- **WHEN** live inventory contains an extension public entrypoint but no receipt or root evidence
- **THEN** classification reports the entrypoint as seen
- **AND** it does not report protected member coverage as complete

### Requirement: Materialized Skills Preserve Standalone Resource Boundaries
Public pack materialization and protected private projection SHALL preserve every declared skill bundle's active resource boundary.

#### Scenario: Public pack is materialized
- **WHEN** a caller materializes a packaged public pack
- **THEN** every nested protected skill can resolve its bundle-local resources without leaving its directory
- **AND** shared machine resources remain available through the installed extension CLI

#### Scenario: Protected member is privately projected
- **WHEN** an internal adapter projects a protected logical capability and its dependencies
- **THEN** each copied member remains a self-contained ordinary directory
- **AND** no source-package sibling, symlink, or undeclared family-root support file is required

#### Scenario: Undeclared support path is required
- **WHEN** active guidance depends on a path not owned by its bundle or declared package service
- **THEN** validation fails with a deterministic resource-boundary diagnostic
