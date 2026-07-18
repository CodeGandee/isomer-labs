## MODIFIED Requirements

### Requirement: Toolbox Manager Skill Is Packaged Operator Guidance
The core public pack SHALL preserve `isomer-op-toolbox-mgr` as protected member `toolbox` for creating and managing Project-local Toolboxes through existing Isomer surfaces.

#### Scenario: Manager member exists
- **WHEN** core pack assets are inspected
- **THEN** `operator/isomer-op-entrypoint/subskills/isomer-op-toolbox-mgr/SKILL.md` exists
- **AND** its folder and frontmatter retain logical id `isomer-op-toolbox-mgr`

#### Scenario: Creator skill remains absent
- **WHEN** core protected inventory is inspected
- **THEN** `isomer-op-toolbox-creator` is not declared as a public or protected capability
- **AND** no compatibility folder is required

#### Scenario: Naming matches responsibility
- **WHEN** protected instructions and metadata are inspected
- **THEN** they identify logical capability `isomer-op-toolbox-mgr` and describe creation as one part of Toolbox management
- **AND** ordinary user prompts use `$isomer-op-entrypoint use toolbox to <task>`

#### Scenario: Domain language is preserved
- **WHEN** instructions are inspected
- **THEN** they use canonical Toolbox, Toolbox ID, Callback Insertion Point, Toolbox-Local Key, Runtime Param, and Toolbox Scope terms

#### Scenario: Public parent routes Toolbox work
- **WHEN** a concrete Toolbox request is received
- **THEN** the public entrypoint invokes `isomer-op-entrypoint->toolbox`
- **AND** the protected member does not bypass CLI validation or packaged ownership
