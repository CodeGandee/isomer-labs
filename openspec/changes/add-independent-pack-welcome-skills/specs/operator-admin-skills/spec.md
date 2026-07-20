## MODIFIED Requirements

### Requirement: Operator Skillset Layout
The packaged operator surface SHALL contain public sibling skills `isomer-op-welcome` and `isomer-op-entrypoint` while preserving all other active operator owners as protected entrypoint capabilities.

#### Scenario: Public operator inventory is inspected
- **WHEN** packaged operator assets are inspected
- **THEN** `operator/isomer-op-welcome` and `operator/isomer-op-entrypoint` are the only top-level public operator skills
- **AND** `isomer-op-entrypoint/subskills/` contains the manifest-declared protected operator bundles except welcome

#### Scenario: Public roles are inspected
- **WHEN** operator catalog metadata loads
- **THEN** `isomer-op-welcome` has role `welcome` and `isomer-op-entrypoint` has role `entrypoint`
- **AND** both belong to the atomic core pack

#### Scenario: Protected operator bundle is inspected
- **WHEN** an operator owner subskill is inspected
- **THEN** its folder and frontmatter retain its logical id
- **AND** the entrypoint route table maps a scoped member name to that logical id

#### Scenario: Retired skills remain absent
- **WHEN** the operator pack is inspected
- **THEN** retired compatibility skills are not restored as public skills or protected members

### Requirement: Welcome Operator Skill Inventory
The operator pack SHALL expose `isomer-op-welcome` as an independent public newcomer skill and SHALL not retain it as an entrypoint-protected member.

#### Scenario: Welcome is independently discoverable
- **WHEN** a host lists top-level core Isomer skills
- **THEN** it lists both `isomer-op-welcome` and `isomer-op-entrypoint`
- **AND** users can invoke `$isomer-op-welcome` without first naming an entrypoint command

#### Scenario: Welcome is absent from protected inventory
- **WHEN** the core protected inventory is inspected
- **THEN** no member `welcome` or logical capability row `isomer-op-welcome` appears there
- **AND** no active route uses `isomer-op-entrypoint->welcome`

#### Scenario: Welcome and entrypoint remain bounded
- **WHEN** operator guidance is inspected
- **THEN** welcome owns read-only onboarding and usage teaching while entrypoint owns concrete route-and-proceed behavior
- **AND** neither duplicates the other's full procedure content

### Requirement: Entrypoint Operator Skill Inventory
The operator inventory SHALL classify `isomer-op-entrypoint` as the public execution entrypoint beside the public welcome skill rather than as the sole public core skill.

#### Scenario: Entrypoint is active
- **WHEN** the manifest and operator assets are inspected
- **THEN** `isomer-op-entrypoint` owns the protected core inventory except welcome
- **AND** its public commands and task routing remain executable

#### Scenario: Entrypoint links welcome
- **WHEN** entrypoint help or an orientation-only request is handled
- **THEN** it names or delegates to `$isomer-op-welcome`
- **AND** it does not require a protected welcome bundle

#### Scenario: Entrypoint does not absorb owner semantics
- **WHEN** a task selects a protected operator capability
- **THEN** the parent loads and follows that member's workflow, gates, and outputs
- **AND** it does not duplicate the full owner procedure in the parent or welcome skill
