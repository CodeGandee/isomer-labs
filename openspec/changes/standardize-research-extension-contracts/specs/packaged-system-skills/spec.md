## ADDED Requirements

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
