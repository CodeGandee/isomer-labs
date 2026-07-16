# skill-shared-resource-contract Specification

## Purpose
TBD - created by syncing completed OpenSpec changes.

## Requirements

### Requirement: Private Skill Resources Are Bundle-Local
Official system skills SHALL store every active resource consumed by only one skill inside that skill's directory and SHALL reference it without leaving the skill boundary.

#### Scenario: One skill consumes an active resource
- **WHEN** an active skill needs a command page, reference, asset, template, or script that no other skill or package service consumes
- **THEN** the resource is stored below that skill's directory and is reached through a descendant-relative reference
- **AND** the skill does not use parent traversal, an absolute source path, a sibling-skill path, or a family-root support path to load it

#### Scenario: Standalone projection loads private resources
- **WHEN** the skill directory is copied to an ordinary standalone installation without repository siblings or symlinks
- **THEN** every private active resource still resolves within the copied directory

### Requirement: Shared Machine Resources Use Extension Queries
Machine-readable resources consumed by more than one skill or by both skills and package services SHALL be package-owned by the matching extension implementation and SHALL be exposed to agents through read-only `isomer-cli ext <prefix>` queries.

#### Scenario: Agent needs a shared machine resource
- **WHEN** active skill guidance needs a shared contract, registry, schema-derived view, inventory, or other machine-readable extension resource
- **THEN** the guidance invokes a documented `isomer-cli --print-json ext <prefix> ...` query and consumes its versioned result
- **AND** it does not instruct the agent to open a package data file, family-root file, sibling-skill file, repository checkout path, or implementation schema directly

#### Scenario: Shared resource is queried from an installed package
- **WHEN** the extension CLI is installed without the source repository or projected skill-family root
- **THEN** the query returns deterministic version and resource data from package-owned resources
- **AND** the response does not expose an implementation filesystem path as the resource contract

#### Scenario: Shared resource cannot be loaded
- **WHEN** the package-owned resource is absent, invalid, or incompatible
- **THEN** the extension query returns a structured diagnostic and a non-success status
- **AND** active skill guidance does not fall back to repository traversal or a hand-authored duplicate

### Requirement: Shared Procedures Use a Prefix Shared Skill
Procedural guidance used by multiple skills in one named skill family SHALL be owned by the family's `<prefix>-shared` skill, while a procedure used by only one skill SHALL remain local to that skill.

#### Scenario: Several skills need the same procedure
- **WHEN** two or more `isomer-<family>-*` skills need the same command process, evidence discipline, Gate behavior, owner-routing sequence, or terminal protocol
- **THEN** `isomer-<family>-shared` owns the active procedure and the consumer skills invoke or route to that skill by name
- **AND** consumers do not load the shared procedure through a filesystem path or copy the full procedure into each skill

#### Scenario: One skill owns a bounded procedure
- **WHEN** a command process is used only by one skill
- **THEN** that skill stores the process in its own `SKILL.md` or a bundle-local active resource

### Requirement: Validation Uses Real Installation Boundaries
System-skill packaging and family validators SHALL enforce the skill/shared-resource contract against ordinary copied skill directories and installed package resources.

#### Scenario: Active reference crosses a skill boundary
- **WHEN** an active skill or active linked resource contains a filesystem reference that traverses above the owning skill directory or depends on an undeclared family-root file
- **THEN** validation fails with the owning skill, source file, line when available, and offending reference
- **AND** the diagnostic identifies whether the resource must become bundle-local or extension-queryable

#### Scenario: Symlink projection masks a missing resource
- **WHEN** repository symlinks would make an otherwise invalid parent-relative reference resolve
- **THEN** validation still fails by evaluating the logical skill boundary and a flat copied projection

#### Scenario: Shared procedure bypasses its shared skill
- **WHEN** family-specific validation finds a known cross-skill process loaded through a sibling path or duplicated where the family contract requires `<prefix>-shared` routing
- **THEN** validation reports the required shared skill and the consumer that bypassed it
