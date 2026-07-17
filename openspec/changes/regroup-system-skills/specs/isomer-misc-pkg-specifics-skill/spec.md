## MODIFIED Requirements

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
