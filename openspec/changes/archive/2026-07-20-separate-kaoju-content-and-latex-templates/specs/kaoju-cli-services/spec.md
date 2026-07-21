## ADDED Requirements

### Requirement: Template CLI Operations Are Role-Explicit
The CLI SHALL expose named-template operations for `content` and `latex` kinds through one checked service and SHALL default omitted names to `main` within the selected kind.

#### Scenario: Backward-compatible content command runs
- **WHEN** an existing caller invokes `ext kaoju paper template` without `--kind`
- **THEN** the command operates on the content-template namespace and emits compatibility metadata identifying that default
- **AND** new documentation and skill calls use explicit `--kind content`

#### Scenario: LaTeX template directory is stocked
- **WHEN** `template create` or `template update` receives `--kind latex`, a prepared directory, valid authored metadata, actor, and required state token
- **THEN** it invokes the same atomic named-state boundary with the LaTeX binding and kind-specific validation
- **AND** it returns the LaTeX stable ref, name, token, digest, working path, audit ref, and diagnostics

#### Scenario: Kind-specific export is requested
- **WHEN** `template export --kind latex` or `--kind content` omits a target
- **THEN** it writes beneath the resolved kind-specific exchange directory and records the kind in reserved export metadata
- **AND** export discovery never treats a working copy of the other kind as eligible

### Requirement: CLI Composes Stocked LaTeX Templates
The paper CLI SHALL compose canonical MyST content with an exact named LaTeX state rather than generating presentation state solely from document-class flags.

#### Scenario: Explicit LaTeX selection is composed
- **WHEN** `init-tex` receives an explicit LaTeX name or ref
- **THEN** it resolves and snapshots that exact state, validates its composition contract, and creates a self-contained TeX draft
- **AND** the result reports separate content-template and LaTeX-template identities

#### Scenario: Default LaTeX selection is composed
- **WHEN** `init-tex` omits the LaTeX selector
- **THEN** it resolves named LaTeX template `main`
- **AND** missing or ambiguous state returns a stable non-mutating diagnostic

### Requirement: CLI Migrates Template Contracts Deterministically
The CLI SHALL provide preview and apply operations for upgrading template-kind metadata and explicitly adopting a source tree into named LaTeX stock.

#### Scenario: Migration preview runs
- **WHEN** a caller previews template-contract migration for a Topic Workspace
- **THEN** the command reports content records, legacy export paths, LaTeX candidates, required metadata, conflicts, and proposed mutations
- **AND** it writes no records or files

#### Scenario: Explicit adoption runs
- **WHEN** a caller applies migration with an exact source ref, target name, authored metadata, and actor
- **THEN** it creates or concurrency-safely updates the named LaTeX state and records adoption provenance
- **AND** it never mutates the adopted source record

### Requirement: CLI Tests Exercise Real Template Consumption
Integration coverage SHALL prove that composition and build behavior depends on the selected LaTeX tree.

#### Scenario: Template-owned dependency is required
- **WHEN** a fixture draft depends on a class or style file that exists only in the selected LaTeX stock
- **THEN** composition and build tests pass only when that file is copied into the composed tree
- **AND** a mismatched or omitted template causes deterministic failure
