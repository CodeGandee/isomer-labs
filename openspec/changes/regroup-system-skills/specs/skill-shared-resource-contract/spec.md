## MODIFIED Requirements

### Requirement: Private Skill Resources Determine the Bundle Boundary
Official public packs and protected subskills SHALL own every active private resource inside one bundle boundary, and command families SHALL use the boundary of their containing skill or subskill. Private means scoped ownership and lifecycle, not secrecy or access control.

#### Scenario: Protected member consumes a private resource
- **WHEN** a protected capability needs a command page, reference, asset, template, or script that no other capability or package service consumes
- **THEN** the resource is stored below `subskills/<logical-id>/` for that capability and reached through a descendant-relative reference
- **AND** it does not traverse into the parent, sibling subskills, or a family-root support path

#### Scenario: Public entrypoint consumes a private resource
- **WHEN** a command or reference belongs only to public entrypoint routing
- **THEN** it remains inside the public pack outside protected member directories

#### Scenario: Nested command uses support resources
- **WHEN** a parent or child command uses a detail page, script, reference, asset, or template
- **THEN** that resource is owned by the command's containing public pack or protected subskill
- **AND** the command does not establish an independent resource root

#### Scenario: Command family needs its own resource root
- **WHEN** a command family needs private scripts, references, commands, assets, templates, runtime metadata, or other files that should be loaded, validated, maintained, or projected as one scoped unit
- **THEN** the family is authored as a subskill instead of a subcommand
- **AND** the subskill owns those resources inside its bundle boundary

#### Scenario: Private projection loads resources
- **WHEN** a protected member is copied as a bounded private projection without its source siblings
- **THEN** every private active resource still resolves within the copied member directory

### Requirement: Shared Procedures Use a Prefix Shared Skill
Procedural guidance used by multiple protected members in one family SHALL be owned by that family's protected shared member and consumed through the parent-owned invocation designator.

#### Scenario: Several DeepSci members need one procedure
- **WHEN** two or more DeepSci capabilities need the same evidence, Gate, recording, or terminal process
- **THEN** logical capability `isomer-deepsci-shared` owns it
- **AND** consumers route through `isomer-ext-deepsci-entrypoint->shared` or a declared subcommand designator

#### Scenario: Several Kaoju members need one procedure
- **WHEN** two or more Kaoju capabilities need the same source identity, lineage, clarification, Gate, owner-routing, or terminal process
- **THEN** logical capability `isomer-kaoju-shared` owns it
- **AND** consumers route through `isomer-ext-kaoju-entrypoint->shared` or a declared subcommand designator

#### Scenario: Core members need shared support
- **WHEN** multiple core capabilities need bounded-run, package-specific, tool-pack, research-idea, or operation-set procedures
- **THEN** they route through the applicable protected member of `isomer-op-entrypoint`
- **AND** no separate top-level shared skill is required

#### Scenario: One capability owns a bounded procedure
- **WHEN** a command process is used by only one protected capability
- **THEN** that capability keeps the process in its own bundle

### Requirement: Validation Uses Real Installation Boundaries
System-skill validation SHALL test complete public packs and bounded protected projections against their actual resource and dependency boundaries.

#### Scenario: Active reference crosses a protected boundary
- **WHEN** a protected member traverses into its parent or sibling bundle without a declared invocation or package query
- **THEN** validation fails with the logical id, source file, and offending reference

#### Scenario: Selective projection omits a dependency
- **WHEN** a private-projection fixture selects a protected member without its manifest dependency closure
- **THEN** validation reports the missing logical ids and does not classify the projection as ready

#### Scenario: Shared procedure bypasses protected shared member
- **WHEN** family validation finds a cross-member process copied or loaded through a sibling path
- **THEN** it reports the required shared logical id and parent-owned invocation designator
