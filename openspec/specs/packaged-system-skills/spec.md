# packaged-system-skills Specification

## Purpose
TBD - created by archiving change package-system-skills-as-assets. Update Purpose after archive.
## Requirements
### Requirement: System Skills Are Package Assets
The system SHALL distribute official non-development Isomer system skills as package-owned public packs containing independent welcome and entrypoint skills with `SKILL.md` plus protected nested capabilities with `SKILL-MAIN.md` under the `isomer_labs` package.

#### Scenario: Packaged root contains distributable pack material
- **WHEN** package resources are inspected for system skills
- **THEN** the packaged root contains `manifest.toml`, `README.md`, the core public welcome and entrypoint, and the optional DeepSci and Kaoju public welcome and entrypoint pairs
- **AND** every protected capability is below its owning execution entrypoint's `subskills/` directory
- **AND** the packaged root does not contain `dev/`

#### Scenario: Manifest paths resolve inside package assets
- **WHEN** the system loads `assets/system_skills/manifest.toml`
- **THEN** every public-skill path and protected capability path resolves below the packaged system-skill root
- **AND** each resolved public skill directory contains `SKILL.md`
- **AND** each resolved protected capability directory contains `SKILL-MAIN.md` and does not contain `SKILL.md`

#### Scenario: Protected capability is not duplicated
- **WHEN** package assets are inspected
- **THEN** no manifest-declared protected logical id also exists as an independently installable top-level skill directory
- **AND** the independent welcome directories are classified as public skills rather than protected capabilities
### Requirement: System Skill Discovery Uses Package Resources
The system SHALL expose package-resource helpers for discovering and reading official system skills without a repository checkout and SHALL resolve the entrypoint filename from the manifest-owned public or protected role.

#### Scenario: Installed package can list system skill groups
- **WHEN** code asks for packaged system-skill groups
- **THEN** the result is derived from the packaged `manifest.toml`
- **AND** group skill paths are returned as manifest-relative paths rather than repository checkout paths

#### Scenario: Package resource lookup avoids checkout assumptions
- **WHEN** code locates packaged system skills
- **THEN** it uses package resources rather than `Path(__file__)` repository-root traversal
- **AND** it does not require repository-root `skillset/` to exist

#### Scenario: Caller resolves a public entrypoint
- **WHEN** a caller requests the entrypoint resource for a manifest-declared public skill
- **THEN** the role-aware helper returns that directory's `SKILL.md`

#### Scenario: Caller resolves a protected entrypoint
- **WHEN** a caller requests the entrypoint resource for a manifest-declared protected capability
- **THEN** the role-aware helper returns that directory's `SKILL-MAIN.md`
- **AND** callers do not need to concatenate a hard-coded filename

### Requirement: System Skills Can Be Materialized Safely
The system SHALL materialize manifest-selected packs as complete sets of top-level public skill directories while preserving protected nested paths and `SKILL-MAIN.md` entrypoints under the designated execution entrypoint.

#### Scenario: Materialize core group
- **WHEN** a caller materializes the `core` group to an empty target directory
- **THEN** the target receives `manifest.toml`, `isomer-op-welcome`, and `isomer-op-entrypoint`
- **AND** protected core capabilities remain below `isomer-op-entrypoint/subskills/` with `SKILL-MAIN.md`
- **AND** no protected capability is copied beside the two public skills or retains nested `SKILL.md`

#### Scenario: Materialize selected extension
- **WHEN** a caller materializes extension `deepsci` or `kaoju`
- **THEN** the target receives the complete core public pair and the selected extension's welcome and entrypoint pair
- **AND** it does not receive the unselected extension pack

#### Scenario: Materialized host recursively scans discovery files
- **WHEN** a supported host recursively searches the materialized target for `SKILL.md`
- **THEN** it finds exactly the selected packs' public welcome and execution entrypoint roots
- **AND** it does not find protected members or provenance snapshots

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

#### Scenario: Core manifest declares public pack
- **WHEN** `src/isomer_labs/assets/system_skills/manifest.toml` is inspected
- **THEN** the core group declares `operator/isomer-op-entrypoint` as its public pack path and `isomer-op-entrypoint` as its entry skill
- **AND** the listed path resolves below the packaged system-skill root

#### Scenario: Packaged discovery returns core pack and members
- **WHEN** code asks for catalog metadata for the `core` group
- **THEN** the result identifies one public pack and the ordered protected logical capabilities it owns
- **AND** it does not classify those protected members as independent public install units
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

#### Scenario: Core group is always available
- **WHEN** the manifest loads the core pack
- **THEN** it declares `kind = "core"`, `always_available = true`, and no extension id
- **AND** it declares one public entry skill and its protected member inventory

#### Scenario: Extension pack has stable extension id
- **WHEN** the manifest loads a pack whose kind is extension
- **THEN** it declares a stable extension id, one `isomer-ext-<extension-id>-entrypoint` public skill, ordered public commands, and protected members
- **AND** callers can filter catalog metadata by extension id
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

#### Scenario: Install docs list public packs
- **WHEN** a user follows public system-skill installation documentation
- **THEN** the docs identify `isomer-op-entrypoint`, `isomer-ext-deepsci-entrypoint`, and `isomer-ext-kaoju-entrypoint` as the complete public Isomer surface
- **AND** they show repository or `isomer-cli system-skills` selection commands with an explicit target or agent scope

#### Scenario: Entrypoint skill is discoverable
- **WHEN** docs explain operator skill installation
- **THEN** they SHALL identify `isomer-op-entrypoint` as the recommended first operator skill for users who already know the system
- **AND** they SHALL identify `isomer-op-welcome` as the orientation menu skill

#### Scenario: Extension skills are optional
- **WHEN** docs explain DeepSci skill installation
- **THEN** they SHALL state that DeepSci skills are optional extension skills and do not need to be installed for basic Project lifecycle CLI usage

#### Scenario: Entrypoint is the invocation surface
- **WHEN** docs explain ordinary use
- **THEN** they demonstrate `$<public-entrypoint> use <subcommand> to <task>` and task-only routing
- **AND** they state that empty invocation means `help`

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

#### Scenario: Project-local projection remains opt-in
- **WHEN** a Project has not enabled Houmao integration
- **THEN** core Isomer skill installation does not create `.isomer-labs/houmao-skills/`
- **AND** projected Houmao-owned skill material is prepared only through explicit Project integration setup

#### Scenario: Public installation guidance keeps Isomer first
- **WHEN** public system-skill installation documentation describes Houmao-backed behavior
- **THEN** it describes Houmao as an internal Isomer integration provider
- **AND** it directs users to Isomer setup and Project integration commands instead of direct Houmao skill installation as the primary route

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

#### Scenario: Kaoju paths resolve inside the pack
- **WHEN** Kaoju catalog metadata loads
- **THEN** every protected path resolves below `research-paradigm/kaoju/isomer-ext-kaoju-entrypoint/subskills/`
- **AND** every member contains its required skill metadata and active resources

#### Scenario: Kaoju callback insertion points are cataloged
- **WHEN** callback insertion-point metadata is queried for extension `kaoju`
- **THEN** every manifest-listed Kaoju skill exposes its approved callback stages in deterministic manifest order
- **AND** the target skill name and manifest-relative path match the packaged skill identity

#### Scenario: Kaoju entry surface declares survey intents
- **WHEN** extension discovery metadata is queried for `kaoju`
- **THEN** it reports `isomer-ext-kaoju-entrypoint`, the accepted ordered public command inventory, and protected logical members from manifest metadata

#### Scenario: Kaoju role-aware baseline is packaged
- **WHEN** the Kaoju public pack and protected `write` member are materialized
- **THEN** public template-manager commands retain explicit content-versus-LaTeX role handling and the protected writer retains its private role-aware paper-production resources
- **AND** package-owned `isomer_labs.kaoju` services remain the machine authority for template state, composition, migration, validation, bindings, semantics, and process data

#### Scenario: Kaoju package is self-contained
- **WHEN** an installed package materializes the Kaoju extension
- **THEN** every skill can resolve its active direct resources, semantic and binding references, command pages, templates, and helper scripts without a repository checkout
- **AND** no active skill requires feature-design files, archived OpenSpec changes, external source checkouts, provider credentials, or the external `imsight-llm-wiki` skill merely to load or validate
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

#### Scenario: Core groups reject extension entry metadata
- **WHEN** a core group declares an extension entry skill or public extension commands
- **THEN** system-skill manifest loading fails with a deterministic package asset diagnostic\n
### Requirement: Core Packaged Skills Include System Skill Manager
The core public pack SHALL include `isomer-op-system-skill-mgr` as the protected `system-skills` member.

#### Scenario: Core manifest includes manager member
- **WHEN** the core protected inventory is inspected
- **THEN** it maps `system-skills` to logical id `isomer-op-system-skill-mgr`
- **AND** the nested path resolves to a valid skill bundle

#### Scenario: Core installation projects manager
- **WHEN** the core group is installed or materialized
- **THEN** it includes the manager's `SKILL.md`, `agents/openai.yaml`, and directly linked references

#### Scenario: Core catalog exposes route without public duplication
- **WHEN** system-skill catalog listing runs
- **THEN** it reports the manager as a protected core member routed by `isomer-op-entrypoint`
- **AND** it does not classify the manager as a public pack or optional extension

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

#### Scenario: Catalog maps extension pack and members
- **WHEN** internal inspection classifies receipt records or live inventory names
- **THEN** it derives the extension entrypoint, protected logical members, and expected nested paths from package-owned metadata
- **AND** agents do not maintain duplicate member lists

#### Scenario: Name-only inventory sees an entrypoint
- **WHEN** live inventory contains an extension public entrypoint but no receipt or root evidence
- **THEN** classification reports the entrypoint as seen
- **AND** it does not report protected member coverage as complete
### Requirement: Materialized Skills Preserve Standalone Resource Boundaries
Public pack materialization and protected private projection SHALL preserve every declared skill bundle's active resource boundary while applying the destination role's canonical entrypoint filename.

#### Scenario: Public pack is materialized
- **WHEN** a caller materializes a packaged public pack
- **THEN** every nested protected skill can resolve its `SKILL-MAIN.md` and bundle-local resources without leaving its directory
- **AND** shared machine resources remain available through the installed extension CLI

#### Scenario: Protected member is privately projected
- **WHEN** an internal adapter projects a protected logical capability and its dependencies into a flat private skill root
- **THEN** each copied member remains a self-contained ordinary directory whose source `SKILL-MAIN.md` is promoted to destination `SKILL.md`
- **AND** no source-package sibling, symlink, undeclared family-root support file, or destination `SKILL-MAIN.md` is required

#### Scenario: Family-root support file is undeclared
- **WHEN** a system-skill family root contains a file or directory that is not a manifest-listed skill bundle
- **THEN** materialization does not copy it as an implicit dependency of selected skills
- **AND** validation fails if active skill guidance requires that undeclared path

#### Scenario: Undeclared support path is required
- **WHEN** active guidance depends on a path not owned by its bundle or declared package service
- **THEN** validation fails with a deterministic resource-boundary diagnostic

#### Scenario: Materialized projection does not preserve symlinks
- **WHEN** package tests materialize skills into a temporary target
- **THEN** the test target uses ordinary directories and files with no link back to the package source or repository checkout
- **AND** each active local link is validated relative to its owning copied skill

### Requirement: Packaged Kaoju Shared Data Is CLI-Owned
The packaged Kaoju skill family SHALL not own canonical survey-process, binding-registry, or binding-schema data outside its fourteen declared skill bundles.

#### Scenario: Packaged Kaoju resources are inspected
- **WHEN** package assets and the Kaoju Python package are inspected
- **THEN** canonical survey-process and binding data are stored with the package-owned Kaoju extension implementation and load through its shared contract loader
- **AND** the system-skill family root contains only declared skill bundles and family documentation needed for discovery

#### Scenario: Kaoju package is used without repository layout
- **WHEN** an installed package materializes Kaoju skills and an agent queries their shared contracts
- **THEN** skill-local resources resolve from each materialized bundle and shared data resolves through `isomer-cli ext kaoju`
- **AND** no operation requires `.kimi-code`, a repository symlink, or `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/contracts`

### Requirement: Packaged Extension Skills Use Manifest-Owned Artifact Identities
Packaged extension skills SHALL use exact uppercase `EXTENSION-NAME:WHAT` artifact identifiers whose namespace is the uppercase projection of the owning manifest group id.

#### Scenario: Packaged research extension is materialized
- **WHEN** DeepSci or Kaoju skills are materialized from package assets
- **THEN** every active artifact reference, registry row, binding projection, source declaration, and command example uses the uppercase projection of the owning manifest `extension_id` as its namespace
- **AND** the materialized guidance contains no active angle-wrapped, double-bracket, bare, lowercase, mixed-case, or aliased artifact identity

#### Scenario: Source and packaged skill trees are compared
- **WHEN** validation compares an extension skill maintained in a source skill tree with its packaged system-skill copy
- **THEN** their canonical artifact identifier sets and relevant guidance agree exactly
- **AND** any superseded or noncanonical identifier in either copy fails validation

### Requirement: Packaged System Skills Externalize Repository Acquisition
Every packaged system skill that obtains or updates a source repository SHALL keep repository command selection and execution outside Isomer APIs and SHALL use Isomer only for semantic target planning, post-verification registration, topology, policy, and durable records.

#### Scenario: Skill receives a user-supplied repository procedure
- **WHEN** a user names custom `git`, provider-CLI, local-copy, wrapper, authentication, checkout, sparse, partial, submodule, LFS, or history commands
- **THEN** the applicable skill preserves those commands within the user request and applicable Gate instead of replacing them with an Isomer acquisition command
- **AND** it registers the verified existing repository only after those commands succeed

#### Scenario: Skill chooses repository commands
- **WHEN** a repository is required and the user has not specified exact commands
- **THEN** the skill instructs the acting agent to choose commands suited to the source and task through its ordinary external command surface
- **AND** it does not invoke `project repos acquire`, a `repository_acquisition` extension point, or another Isomer API that executes source-control commands

#### Scenario: Skill records successful acquisition
- **WHEN** external acquisition and identity verification succeed
- **THEN** the skill uses the applicable non-executing semantic registration command and durable-record operations
- **AND** it distinguishes the Topic Workspace Manifest path binding from source identity, command evidence, access, license, relationship, and limitation provenance

#### Scenario: Skill encounters failed acquisition
- **WHEN** repository acquisition, identity verification, or post-acquisition registration fails
- **THEN** the skill reports a blocker or resumable checkpoint with sanitized evidence and the safe next action
- **AND** it does not claim a successful binding or ask Isomer to delete, move, reset, or repair the partial checkout

### Requirement: Packaged Skill Validation Enforces the Repository Boundary
System-skill validation SHALL reject active guidance that assigns repository acquisition commands to Isomer APIs or registers a new repository before external verification.

#### Scenario: Obsolete acquisition API appears in active guidance
- **WHEN** a packaged or source-mirrored system skill names `project repos acquire`, `repository_acquisition`, the removed Kaoju repository service, or an equivalent Isomer-owned Git execution route as active procedure
- **THEN** validation reports the skill, file, line when available, and violated external-acquisition boundary

#### Scenario: Acquire-then-register guidance is valid
- **WHEN** a skill uses a read-only semantic target query, authorized external repository commands, external identity verification, `project repos register`, and typed durable-record operations in that order
- **THEN** repository-boundary validation accepts the guidance
- **AND** family-specific validators continue to enforce their other owner, Gate, evidence, and command rules

#### Scenario: Registration precedes verification
- **WHEN** active skill guidance creates a successful non-main repository binding before external acquisition and identity verification complete
- **THEN** validation reports the ordering violation
- **AND** it directs the skill author to use a read-only default-path query before acquisition and semantic registration afterward

### Requirement: Core Packaged Skills Include Operation Set Recording
The packaged core system-skill group SHALL include `research/isomer-research-operation-set-recording` as the provider-neutral owner of operation-set research acceptance guidance.

#### Scenario: Core manifest includes recording skill
- **WHEN** `src/isomer_labs/assets/system_skills/manifest.toml` is inspected
- **THEN** `groups.core.skills` includes `research/isomer-research-operation-set-recording`
- **AND** the path resolves to a skill directory containing `SKILL.md`, `agents/openai.yaml`, and its directly required references

#### Scenario: Recording skill has a bounded workflow
- **WHEN** the packaged skill is inspected
- **THEN** its numbered workflow covers worker context, inspection, binding resolution, manifest completion, preview, apply, verify, partial recovery, and legacy repair
- **AND** it forbids inferred record or Research Idea lineage

#### Scenario: Core materialization copies recording skill
- **WHEN** a caller materializes or installs the core system-skill group
- **THEN** the target includes the operation-set recording skill and its required resources at the manifest-relative path

#### Scenario: Skill metadata version matches package release
- **WHEN** a release or release candidate validates packaged system skills
- **THEN** the new skill's `agents/openai.yaml` metadata version matches `project.version` under the existing release rule
