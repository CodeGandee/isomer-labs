# isomer-misc-pkg-specifics-skill Specification

## Purpose
TBD - created by archiving change standardize-package-specific-env-routing. Update Purpose after archive.
## Requirements
### Requirement: Package Specifics Skill Provides Named Package Caveats
The system SHALL provide `isomer-misc-pkg-specifics` as the package-specific caveat registry for named package source choices, variant checks, runtime checks, verification expectations, warnings, and blockers.

#### Scenario: Listed package returns package-specific evidence
- **WHEN** a caller asks `isomer-misc-pkg-specifics` about a package listed in its package index
- **THEN** the skill loads only the selected package page
- **AND** it reports package name, selected source or unresolved source, required variant, verification expectation, warnings, and blockers

#### Scenario: Unlisted package returns no package-specific rule
- **WHEN** a caller asks `isomer-misc-pkg-specifics` about a package that is not listed in its package index
- **THEN** the skill reports `no package-specific rule`
- **AND** it returns control to the caller's generic package routing instead of inventing a full setup plan

### Requirement: Package Specifics Skill Stays Narrow
The package-specific caveat registry SHALL NOT replace generic environment setup, generic Pixi mechanics, package-source reachability checks, or bounded-run classification.

#### Scenario: Generic setup remains outside package specifics
- **WHEN** a package-specific page is used during environment setup
- **THEN** it provides only selected package source, variant, verification, caveat, warning, or blocker evidence
- **AND** the caller remains responsible for Pixi mutation, env gate writing, package-source reachability checks, bounded-run handling, and final readiness reporting

#### Scenario: Package-specific caveats stay out of core services
- **WHEN** a known package has special source, variant, accelerator, build, or runtime behavior
- **THEN** the package-specific details live in `isomer-misc-pkg-specifics` package pages
- **AND** service and operator skills reference the selected package-specific evidence instead of duplicating the full caveat text

### Requirement: Package Specifics Remain Misc Helper Interface
Package-specific guidance SHALL remain a narrow logical helper while becoming protected shared member `package-specifics` of the core public pack.

#### Scenario: Protected package-specific bundle exists
- **WHEN** core pack assets are inspected
- **THEN** `operator/isomer-op-entrypoint/subskills/isomer-misc-pkg-specifics/SKILL.md` exists
- **AND** its folder and frontmatter retain logical id `isomer-misc-pkg-specifics`

#### Scenario: Generic package mutation routes to owner
- **WHEN** a user asks to install, update, or remove a Topic Workspace package
- **THEN** the public entrypoint routes to the owning Topic Manager or environment workflow
- **AND** that owner invokes `isomer-op-entrypoint->package-specifics` for named caveats before mutation

#### Scenario: Package-specific question is direct
- **WHEN** a user asks only for package-specific caveats
- **THEN** `$isomer-op-entrypoint use package-specifics to <task>` may route to the protected helper
- **AND** no top-level `$isomer-misc-pkg-specifics` invocation is advertised

#### Scenario: Logical id remains stable
- **WHEN** a binding, dependency, or provenance field names the helper
- **THEN** it continues to use `isomer-misc-pkg-specifics`

#### Scenario: Package-specifics skill name remains stable
- **WHEN** the misc skillset is inspected after the namespace rename
- **THEN** the package-specifics skill remains `isomer-misc-pkg-specifics`
- **AND** it is not renamed to `isomer-ext-pkg-specifics`

#### Scenario: Package-specifics consumers use stable helper name
- **WHEN** service, operator, or domain extension guidance references package-specific caveats
- **THEN** it references `isomer-misc-pkg-specifics`
- **AND** it does not duplicate the full caveat text into the consuming skill

#### Scenario: Package-specifics is not a domain extension
- **WHEN** documentation explains extension family naming
- **THEN** it treats `isomer-misc-pkg-specifics` as shared helper infrastructure
- **AND** it reserves `isomer-<extension-name>-<purpose>` for concrete domain extension families such as `isomer-deepsci-*`

