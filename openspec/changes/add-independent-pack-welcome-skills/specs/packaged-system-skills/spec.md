## MODIFIED Requirements

### Requirement: System Skills Are Package Assets
The system SHALL distribute official non-development Isomer system skills as package-owned public packs containing independent welcome and entrypoint skills plus protected nested capabilities under the `isomer_labs` package.

#### Scenario: Packaged root contains distributable pack material
- **WHEN** package resources are inspected for system skills
- **THEN** the packaged root contains `manifest.toml`, `README.md`, the core public welcome and entrypoint, and the optional DeepSci and Kaoju public welcome and entrypoint pairs
- **AND** every protected capability is below its owning execution entrypoint's `subskills/` directory
- **AND** the packaged root does not contain `dev/`

#### Scenario: Manifest paths resolve inside package assets
- **WHEN** the system loads `assets/system_skills/manifest.toml`
- **THEN** every public-skill path and protected capability path resolves below the packaged system-skill root
- **AND** each resolved public skill and capability directory contains `SKILL.md`

#### Scenario: Protected capability is not duplicated
- **WHEN** package assets are inspected
- **THEN** no manifest-declared protected logical id also exists as an independently installable top-level skill directory
- **AND** the independent welcome directories are classified as public skills rather than protected capabilities

### Requirement: System Skills Can Be Materialized Safely
The system SHALL materialize manifest-selected packs as complete sets of top-level public skill directories while preserving protected nested paths under the designated execution entrypoint.

#### Scenario: Materialize core group
- **WHEN** a caller materializes the `core` group to an empty target directory
- **THEN** the target receives `manifest.toml`, `isomer-op-welcome`, and `isomer-op-entrypoint`
- **AND** protected core capabilities remain below `isomer-op-entrypoint/subskills/`
- **AND** no protected capability is copied beside the two public skills

#### Scenario: Materialize selected extension
- **WHEN** a caller materializes extension `deepsci` or `kaoju`
- **THEN** the target receives the complete core public pair and the selected extension's welcome and entrypoint pair
- **AND** it does not receive the unselected extension pack

#### Scenario: Development skills are never materialized from package assets
- **WHEN** a caller materializes any packaged system-skill selection
- **THEN** no `dev/` directory or `isomer-dev-*` skill is copied from package assets

### Requirement: Core Packaged Skills Include Entrypoint
The packaged core system-skill group SHALL include `operator/isomer-op-entrypoint` as its designated execution entrypoint and `operator/isomer-op-welcome` as its independent public onboarding skill, while all other core capabilities remain protected members of the entrypoint.

#### Scenario: Core manifest declares public pair
- **WHEN** `src/isomer_labs/assets/system_skills/manifest.toml` is inspected
- **THEN** core declares public skills `isomer-op-welcome` with role `welcome` and `isomer-op-entrypoint` with role `entrypoint`
- **AND** `entry_skill` is `isomer-op-entrypoint`

#### Scenario: Core materialization copies two public roots
- **WHEN** a caller materializes the `core` group
- **THEN** the target receives standalone `isomer-op-welcome` and complete `isomer-op-entrypoint` directories
- **AND** no other core logical capability is a top-level projection

#### Scenario: Packaged discovery distinguishes roles
- **WHEN** code asks for catalog metadata for the `core` group
- **THEN** it identifies the ordered public pair, their roles, paths, descriptions, versions, and commands
- **AND** it separately identifies the protected logical capabilities owned by `isomer-op-entrypoint`

### Requirement: System Skill Manifest Classifies Groups
The packaged system-skill manifest SHALL classify packs, public skills, and protected logical capabilities so callers can distinguish pack mutation units, newcomer and execution surfaces, and internally routed members.

#### Scenario: Pack public roles are complete
- **WHEN** manifest v4 loads a core or extension pack
- **THEN** the pack declares exactly one public skill with role `welcome` and exactly one public skill with role `entrypoint`
- **AND** the pack's `entry_skill` names the entrypoint-role record

#### Scenario: Public skill metadata is complete
- **WHEN** manifest v4 loads a public skill
- **THEN** the record declares canonical name, pack id, role, source path, ordered public commands, aliases, callback stages, and applicable compatibility floor
- **AND** public names and source paths are globally unique

#### Scenario: Protected capability metadata is complete
- **WHEN** manifest v4 loads a protected capability
- **THEN** it declares logical id, pack id, nested entrypoint path, scoped member name, invocation designator, area, dependencies, aliases, callback stages, and applicable compatibility floor
- **AND** its invocation designator begins with the owning pack's execution entrypoint rather than its welcome skill

#### Scenario: Invalid classification is rejected
- **WHEN** a pack lacks one required public role, a public identity collides, a protected capability escapes the entrypoint, or an extension public name does not match its extension id and role
- **THEN** manifest loading fails with a deterministic package asset diagnostic

### Requirement: Public System Skill Installation Documentation
The system SHALL document welcome-first onboarding and entrypoint execution for public packs on supported agent hosts.

#### Scenario: Install docs list public pairs
- **WHEN** a user follows public system-skill installation documentation
- **THEN** the docs list `isomer-op-welcome` with `isomer-op-entrypoint`, `isomer-ext-deepsci-welcome` with `isomer-ext-deepsci-entrypoint`, and `isomer-ext-kaoju-welcome` with `isomer-ext-kaoju-entrypoint`
- **AND** they explain that selecting either public name through Isomer pack installation installs the complete owning pack

#### Scenario: Newcomer and informed-user routes differ
- **WHEN** docs explain ordinary use
- **THEN** they recommend `$<welcome>` for orientation, typical use cases, and command learning
- **AND** they recommend `$<entrypoint> use <command> to <task>` or a concrete task-only entrypoint request for execution

#### Scenario: Protected members are not user install choices
- **WHEN** docs describe operator, service, shared, DeepSci, or Kaoju members
- **THEN** they describe those members as entrypoint-routed protected capabilities
- **AND** they do not instruct users to install or invoke them as top-level skills

### Requirement: Packaged Kaoju Extension Group
The packaged catalog SHALL expose Kaoju as optional extension `kaoju` through independent public skills `isomer-ext-kaoju-welcome` and `isomer-ext-kaoju-entrypoint`, with the existing thirteen protected capabilities owned by the entrypoint.

#### Scenario: Kaoju manifest group is classified and complete
- **WHEN** `manifest.toml` is inspected
- **THEN** pack `kaoju` declares `kind = "extension"`, `extension_id = "kaoju"`, `always_available = false`, public welcome `isomer-ext-kaoju-welcome`, and execution entrypoint `isomer-ext-kaoju-entrypoint`
- **AND** it owns protected logical ids for shared, workspace, frame, discover, acquire, examine, reproduce, trial, compare, audit, synthesize, write, and export

#### Scenario: Kaoju paths resolve inside their owners
- **WHEN** Kaoju catalog metadata loads
- **THEN** the welcome path resolves as an independent sibling bundle
- **AND** every protected path resolves below `research-paradigm/kaoju/isomer-ext-kaoju-entrypoint/subskills/`

#### Scenario: Kaoju materializes safely
- **WHEN** extension `kaoju` is selected
- **THEN** output includes core plus both Kaoju public skills and the complete protected entrypoint inventory
- **AND** it does not include DeepSci unless selected

#### Scenario: Kaoju discovery distinguishes learning and execution
- **WHEN** extension discovery metadata is queried for `kaoju`
- **THEN** it reports `isomer-ext-kaoju-welcome` as the onboarding surface and `isomer-ext-kaoju-entrypoint` as the execution surface
- **AND** it reports entrypoint commands and protected logical members from manifest metadata

### Requirement: System Skill Manifest Describes Extension Entry Surfaces
The packaged system-skill manifest SHALL describe both the welcome and execution surfaces of each optional extension without requiring a repository checkout or extension-specific CLI inventory.

#### Scenario: Extension declares public pair
- **WHEN** the system loads a pack whose kind is `extension`
- **THEN** it declares one `isomer-ext-<extension-id>-welcome` public skill and one `isomer-ext-<extension-id>-entrypoint` public skill
- **AND** it declares ordered public commands on the public skill that owns each command

#### Scenario: Extension discovery metadata is package-derived
- **WHEN** code asks for packaged system-skill extensions
- **THEN** each result includes extension id, pack description, ordered public skill records, designated execution entrypoint, command inventories, and protected member summaries
- **AND** the result does not depend on a repository checkout

#### Scenario: Invalid extension public metadata is rejected
- **WHEN** an extension welcome or entrypoint is missing, has the wrong role or name, lies outside the extension family, or declares an invalid command id
- **THEN** manifest loading fails with a deterministic package asset diagnostic

### Requirement: Extension Catalog Supports Inventory Classification
The packaged system-skill catalog SHALL provide stable extension-family membership and public roles for explicit-root and live-inventory classification.

#### Scenario: Catalog maps extension public skills
- **WHEN** internal inspection classifies receipt records or inventory names
- **THEN** it derives each extension's welcome, entrypoint, and complete protected member set from package-owned catalog metadata
- **AND** agents do not maintain duplicate hard-coded member or public-skill lists

#### Scenario: One public name does not prove complete coverage
- **WHEN** live inventory contains only an extension welcome or only its entrypoint
- **THEN** classification reports the observed public role
- **AND** it does not claim the extension pack is complete or host-usable from that name alone
