# packaged-system-skills Specification

## Purpose
TBD - created by archiving change package-system-skills-as-assets. Update Purpose after archive.
## Requirements

### Requirement: System Skills Are Package Assets
The system SHALL distribute official non-development Isomer system skills as package-owned resources under the `isomer_labs` package.

#### Scenario: Packaged root contains distributable skillset material
- **WHEN** package resources are inspected for system skills
- **THEN** the packaged root contains `manifest.toml`, `README.md`, `misc/`, `operator/`, `research-paradigm/`, and `service/`
- **AND** it does not contain `dev/`

#### Scenario: Manifest-listed skills resolve inside package assets
- **WHEN** the system loads `assets/system_skills/manifest.toml`
- **THEN** every skill path listed in every manifest group resolves below the packaged system-skill root
- **AND** each listed skill directory contains `SKILL.md`

### Requirement: System Skill Discovery Uses Package Resources
The system SHALL expose package-resource helpers for discovering and reading official system skills without a repository checkout.

#### Scenario: Installed package can list system skill groups
- **WHEN** code asks for packaged system-skill groups
- **THEN** the result is derived from the packaged `manifest.toml`
- **AND** group skill paths are returned as manifest-relative paths rather than repository checkout paths

#### Scenario: Package resource lookup avoids checkout assumptions
- **WHEN** code locates packaged system skills
- **THEN** it uses package resources rather than `Path(__file__)` repository-root traversal
- **AND** it does not require repository-root `skillset/` to exist

### Requirement: System Skills Can Be Materialized Safely
The system SHALL support copying manifest-selected packaged system skills to a filesystem target while preserving relative skill paths.

#### Scenario: Materialize selected group
- **WHEN** a caller materializes the `core` group to an empty target directory
- **THEN** the target receives `manifest.toml` and only the skill directories listed for that group
- **AND** each copied skill keeps its manifest-relative path such as `operator/isomer-op-project-mgr`

#### Scenario: Development skills are never materialized from package assets
- **WHEN** a caller materializes any packaged system-skill group
- **THEN** no `dev/` directory or `isomer-dev-*` skill is copied from package assets

### Requirement: Core Packaged Skills Include Entrypoint
The packaged core system-skill group SHALL include `operator/isomer-op-entrypoint` and materialize it with the rest of the core operator, service, and misc skills.

#### Scenario: Core manifest includes entrypoint
- **WHEN** `src/isomer_labs/assets/system_skills/manifest.toml` is inspected
- **THEN** `groups.core.skills` includes `operator/isomer-op-entrypoint`
- **AND** the listed path resolves below the packaged system-skill root
- **AND** the listed directory contains `SKILL.md`

#### Scenario: Core materialization copies entrypoint
- **WHEN** a caller materializes the `core` group to an empty target directory
- **THEN** the target receives `operator/isomer-op-entrypoint/SKILL.md`
- **AND** it receives the entrypoint's `agents/openai.yaml` and directly linked references

#### Scenario: Packaged skill discovery returns entrypoint
- **WHEN** code asks for manifest-relative skill paths for the `core` group
- **THEN** the result includes `operator/isomer-op-entrypoint`
- **AND** it keeps the path manifest-relative rather than deriving a repository checkout path

### Requirement: System Skill Manifest Classifies Groups
The packaged system-skill manifest SHALL classify each manifest group as core or extension so callers can distinguish always-available system skills from optional system extensions.

#### Scenario: Core group is always available
- **WHEN** the system loads the packaged system-skill manifest
- **THEN** each core group declares that its skills are always available for Project operator discovery
- **AND** the core group does not require a Project Manifest operator extension declaration before its catalog metadata is listed

#### Scenario: Extension group has stable extension id
- **WHEN** the system loads a packaged system-skill manifest group whose kind is extension
- **THEN** the group declares a stable extension id
- **AND** callers can filter catalog metadata by that extension id

#### Scenario: Invalid group classification is rejected
- **WHEN** a packaged system-skill manifest group omits group classification or declares an invalid extension id
- **THEN** system-skill manifest loading fails with a deterministic package asset diagnostic

### Requirement: System Skill Manifest Declares Callback Insertion Points
The packaged system-skill manifest SHALL declare callback stage definitions and per-skill callback insertion points as catalog metadata.

#### Scenario: Stage definitions are loaded from manifest
- **WHEN** the system loads `assets/system_skills/manifest.toml`
- **THEN** callback insertion point stage ids, labels, and descriptions are derived from the manifest rather than hardcoded only in Python

#### Scenario: Per-skill insertion points are manifest-relative
- **WHEN** the manifest declares callback insertion points for a packaged system skill
- **THEN** the declaration is keyed by the skill's manifest-relative path
- **AND** every declared stage id resolves to a manifest callback stage definition
- **AND** every referenced skill path resolves below the packaged system-skill root and contains `SKILL.md`

#### Scenario: Skills without declarations expose no insertion points
- **WHEN** a packaged system skill has no callback insertion point declaration in the manifest
- **THEN** the system treats that skill as exposing no callback insertion points

#### Scenario: Callback insertion point discovery is deterministic
- **WHEN** code asks for packaged callback insertion points
- **THEN** the result is derived from the packaged manifest, grouped by manifest group, and returned in deterministic manifest order with target skill name, skill path, group name, optional extension id, stage id, and stage metadata

### Requirement: Public System Skill Installation Documentation
The system SHALL document how users install packaged Isomer system skills into supported agent hosts from the published repository.

#### Scenario: Install docs prefer skills CLI
- **WHEN** a user follows public system-skill installation documentation
- **THEN** the docs SHALL recommend `npx skills add CodeGandee/isomer-labs` or an equivalent repository URL as the primary installation mechanism
- **AND** the docs SHALL show how to select skills with `--skill`

#### Scenario: Agent target is explicit
- **WHEN** docs show a skill installation command
- **THEN** the command SHALL include or explain `--agent <agent>` so users know which agent host receives the skills

#### Scenario: Entrypoint skill is discoverable
- **WHEN** docs explain operator skill installation
- **THEN** they SHALL identify `isomer-op-entrypoint` as the recommended first operator skill for users who already know the system
- **AND** they SHALL identify `isomer-op-welcome` as the orientation menu skill

#### Scenario: Extension skills are optional
- **WHEN** docs explain DeepSci skill installation
- **THEN** they SHALL state that DeepSci skills are optional extension skills and do not need to be installed for basic Project lifecycle CLI usage

### Requirement: Core Packaged Skills Include Toolbox Manager
The packaged core system-skill group SHALL include `operator/isomer-op-toolbox-mgr` and materialize it with the rest of the core operator skills.

#### Scenario: Core manifest includes toolbox manager
- **WHEN** `src/isomer_labs/assets/system_skills/manifest.toml` is inspected
- **THEN** `groups.core.skills` includes `operator/isomer-op-toolbox-mgr`
- **AND** `groups.core.skills` does not include `operator/isomer-op-toolbox-creator`
- **AND** the listed manager path resolves below the packaged system-skill root
- **AND** the listed manager directory contains `SKILL.md`

#### Scenario: Core materialization copies toolbox manager
- **WHEN** a caller materializes the `core` group to an empty target directory
- **THEN** the target receives `operator/isomer-op-toolbox-mgr/SKILL.md`
- **AND** it receives the manager skill's directly linked command pages
- **AND** it does not receive `operator/isomer-op-toolbox-creator/`

#### Scenario: Packaged skill discovery returns toolbox manager
- **WHEN** code asks for manifest-relative skill paths for the `core` group
- **THEN** the result includes `operator/isomer-op-toolbox-mgr`
- **AND** the result does not include `operator/isomer-op-toolbox-creator`
- **AND** it keeps the manager path manifest-relative rather than deriving a repository checkout path

### Requirement: Core Isomer Skills Include Internal Houmao Bridge Support
The packaged Isomer system-skill catalog SHALL keep Isomer-facing Houmao bridge and Topic Service Agent support available in the core skill set while keeping Houmao-owned projected skill material Project-local and opt-in.

#### Scenario: Core operator installation does not expose Houmao administration
- **WHEN** a user installs only the basic Isomer operator skill set
- **THEN** the installed user-facing skills do not require the user to install or invoke Houmao-owned system skills directly
- **AND** Houmao-specific procedures remain reachable only through Isomer-managed routing or an explicit advanced support path

#### Scenario: Core includes Isomer-facing bridge skills
- **WHEN** the packaged system-skill manifest is inspected
- **THEN** the core group may include Isomer-facing bridge/support skills such as `isomer-srv-houmao-interop` and `isomer-srv-topic-service-agent-support`
- **AND** those skills do not require Project-local Houmao skill projection, Houmao credentials, or live Houmao state merely to report disabled or not-configured integration

#### Scenario: Project-local projection remains opt-in
- **WHEN** a Project has not enabled Houmao integration
- **THEN** core Isomer skill installation does not create `.isomer-labs/houmao-skills/`
- **AND** projected Houmao-owned skill material is prepared only through explicit Project integration setup

#### Scenario: Public installation guidance keeps Isomer first
- **WHEN** public system-skill installation documentation describes Houmao-backed behavior
- **THEN** it describes Houmao as an internal Isomer integration provider
- **AND** it directs users to Isomer setup and Project integration commands instead of direct Houmao skill installation as the primary route

### Requirement: Core Packaged Skills Include GUI Manager
The packaged core system-skill group SHALL include `operator/isomer-op-gui-mgr` and materialize it with the rest of the core operator skills.

#### Scenario: Core manifest includes GUI manager
- **WHEN** `src/isomer_labs/assets/system_skills/manifest.toml` is inspected
- **THEN** `groups.core.skills` includes `operator/isomer-op-gui-mgr`
- **AND** the listed path resolves below the packaged system-skill root
- **AND** the listed directory contains `SKILL.md`

#### Scenario: Core materialization copies GUI manager
- **WHEN** a caller materializes the `core` group to an empty target directory
- **THEN** the target receives `operator/isomer-op-gui-mgr/SKILL.md`
- **AND** it receives the GUI manager skill's directly linked reference pages

#### Scenario: Packaged skill discovery returns GUI manager
- **WHEN** code asks for manifest-relative skill paths for the `core` group
- **THEN** the result includes `operator/isomer-op-gui-mgr`
- **AND** it keeps the path manifest-relative rather than deriving a repository checkout path

### Requirement: Packaged Kaoju Extension Group
The packaged system-skill manifest SHALL expose Kaoju as an optional extension group with stable id `kaoju` and the complete fourteen-skill survey-process inventory.

#### Scenario: Kaoju manifest group is classified and complete
- **WHEN** `src/isomer_labs/assets/system_skills/manifest.toml` is inspected
- **THEN** group `kaoju` declares `kind = "extension"`, `extension_id = "kaoju"`, and `always_available = false`
- **AND** it lists the fourteen production paths for `isomer-kaoju-pipeline`, `isomer-kaoju-shared`, `isomer-kaoju-workspace-mgr`, `isomer-kaoju-frame`, `isomer-kaoju-discover`, `isomer-kaoju-acquire`, `isomer-kaoju-examine`, `isomer-kaoju-reproduce`, `isomer-kaoju-trial`, `isomer-kaoju-compare`, `isomer-kaoju-audit`, `isomer-kaoju-synthesize`, `isomer-kaoju-write`, and `isomer-kaoju-export`

#### Scenario: Kaoju paths resolve inside package assets
- **WHEN** packaged system-skill discovery loads the `kaoju` group
- **THEN** every listed path resolves below the packaged system-skill root
- **AND** every listed directory contains `SKILL.md`, `agents/openai.yaml`, and its directly linked active commands, references, assets, or scripts

#### Scenario: Kaoju extension materializes safely
- **WHEN** a caller materializes or installs extension `kaoju`
- **THEN** the selected output includes the core group plus all fourteen Kaoju skills according to existing selector rules
- **AND** it does not include DeepSci skills unless DeepSci or all extensions were also selected

#### Scenario: Kaoju callback insertion points are cataloged
- **WHEN** callback insertion-point metadata is queried for extension `kaoju`
- **THEN** every manifest-listed Kaoju skill exposes its approved callback stages in deterministic manifest order
- **AND** the target skill name and manifest-relative path match the packaged skill identity

#### Scenario: Kaoju entry surface declares survey intents
- **WHEN** extension discovery metadata is queried for `kaoju`
- **THEN** `isomer-kaoju-pipeline` remains the entry skill and its ordered command ids include all ten survey-process intents plus retained compatibility procedures and grouped managers
- **AND** the metadata is derived from the packaged manifest rather than a duplicate hard-coded command list

#### Scenario: Kaoju package is self-contained
- **WHEN** an installed package materializes the Kaoju extension
- **THEN** every skill can resolve its active direct resources, semantic and binding references, command pages, templates, and helper scripts without a repository checkout
- **AND** no active skill requires feature-design files, archived OpenSpec changes, external source checkouts, provider credentials, or the external `imsight-llm-wiki` skill merely to load or validate

### Requirement: System Skill Manifest Describes Extension Entry Surfaces
The packaged system-skill manifest SHALL describe how users enter each optional system-skill extension without requiring a repository checkout or extension-specific CLI code.

#### Scenario: Extension declares entry skill and commands
- **WHEN** the system loads a packaged group whose kind is `extension`
- **THEN** the group declares one entry skill that belongs to its packaged skill inventory
- **AND** it declares an ordered list of public command ids exposed through that entry skill

#### Scenario: Extension discovery metadata is package-derived
- **WHEN** code asks for packaged system-skill extensions
- **THEN** each result includes the manifest-owned extension id, group, description, entry skill, commands, and skill paths
- **AND** the result does not depend on a repository checkout

#### Scenario: Invalid extension entry metadata is rejected
- **WHEN** an extension entry skill is missing, is not part of that extension's skill inventory, or a public command id is invalid
- **THEN** system-skill manifest loading fails with a deterministic package asset diagnostic

#### Scenario: Core groups reject extension entry metadata
- **WHEN** a core group declares an extension entry skill or public extension commands
- **THEN** system-skill manifest loading fails with a deterministic package asset diagnostic\n

### Requirement: Core Packaged Skills Include System Skill Manager
The packaged core system-skill group SHALL include `operator/isomer-op-system-skill-mgr` so every complete Isomer operator installation can manage optional extensions.

#### Scenario: Core manifest includes manager
- **WHEN** the packaged system-skill manifest is inspected
- **THEN** the core group lists `operator/isomer-op-system-skill-mgr`
- **AND** the path resolves to a valid packaged skill directory

#### Scenario: Core installation projects manager
- **WHEN** the core group is installed or materialized
- **THEN** it includes the manager's `SKILL.md`, `agents/openai.yaml`, and directly linked references

#### Scenario: Core catalog exposes manager
- **WHEN** system-skill catalog listing runs
- **THEN** it reports `isomer-op-system-skill-mgr` as a core operator skill
- **AND** it does not classify the manager as an optional extension

### Requirement: Extension Catalog Supports Inventory Classification
The packaged system-skill catalog SHALL provide stable extension-family membership for explicit-root and live-inventory classification.

#### Scenario: Catalog maps extension members
- **WHEN** internal inspection classifies receipt records or inventory names
- **THEN** it derives each extension's entry skill and complete member set from package-owned catalog metadata
- **AND** agents do not maintain duplicate hard-coded member lists

### Requirement: Materialized Skills Preserve Standalone Resource Boundaries
System-skill materialization SHALL copy declared skill bundles as ordinary standalone directories and SHALL not treat undeclared family-root support files as implicit skill dependencies.

#### Scenario: Extension skills are materialized
- **WHEN** a caller materializes a packaged extension group
- **THEN** each manifest-listed skill directory contains every private active resource it needs and no active reference depends on the source package's sibling layout
- **AND** shared machine resources remain available through the installed extension CLI rather than being copied beside the skills

#### Scenario: Family-root support file is undeclared
- **WHEN** a system-skill family root contains a file or directory that is not a manifest-listed skill bundle
- **THEN** materialization does not copy it as an implicit dependency of selected skills
- **AND** validation fails if active skill guidance requires that undeclared path

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
