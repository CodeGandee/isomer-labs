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

