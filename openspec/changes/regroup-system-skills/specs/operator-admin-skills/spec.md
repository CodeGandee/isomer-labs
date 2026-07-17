## MODIFIED Requirements

### Requirement: Operator Skillset Layout
The packaged operator surface SHALL contain one public `isomer-op-entrypoint` pack and SHALL preserve active operator owners as protected nested logical capabilities.

#### Scenario: Public operator inventory is inspected
- **WHEN** packaged operator assets are inspected
- **THEN** `operator/isomer-op-entrypoint` is the only top-level public operator pack
- **AND** its `subskills/` tree contains the manifest-declared `isomer-op-*` protected bundles

#### Scenario: Protected operator bundle is inspected
- **WHEN** an operator owner subskill is inspected
- **THEN** its folder and frontmatter retain its logical id
- **AND** its parent route table maps a scoped member name to that logical id

#### Scenario: Retired skills remain absent
- **WHEN** the operator pack is inspected
- **THEN** retired compatibility skills are not restored as public packs or protected members

### Requirement: Welcome Operator Skill Inventory
The operator pack SHALL preserve `isomer-op-welcome` as protected member `welcome` and SHALL expose its visible routines through the public core entrypoint.

#### Scenario: Welcome member is active
- **WHEN** the core protected inventory is inspected
- **THEN** it maps `welcome` to `isomer-op-welcome`
- **AND** the public pack exposes help and accepted orientation routines

#### Scenario: Welcome is not independently discoverable
- **WHEN** a host lists top-level core Isomer skills
- **THEN** it lists `isomer-op-entrypoint`
- **AND** it does not list `isomer-op-welcome`

### Requirement: Operator Namespace Rename Inventory
Active operator logical ids SHALL retain the `isomer-op-*` namespace while their ordinary runtime entry is the public core pack.

#### Scenario: Active operator logical inventory uses op names
- **WHEN** protected operator capabilities are inspected
- **THEN** their logical ids use `isomer-op-<purpose>`
- **AND** no `isomer-admin-*` logical id is active

#### Scenario: Active routing uses parent designators
- **WHEN** one operator capability invokes another
- **THEN** it uses the applicable `isomer-op-entrypoint-><member>` designator
- **AND** user guidance uses the public core invocation convention

### Requirement: Switch Identity Operator Skill Inventory
The operator pack SHALL preserve `isomer-op-switch-identity` as protected member `identity`.

#### Scenario: Switch identity member is active
- **WHEN** the protected inventory is inspected
- **THEN** member `identity` maps to logical id `isomer-op-switch-identity`
- **AND** the complete bundle exists below the public parent

#### Scenario: Public route is documented
- **WHEN** operator help lists identity posture work
- **THEN** it uses `$isomer-op-entrypoint use identity to <task>`
- **AND** it does not advertise a top-level `$isomer-op-switch-identity` invocation

### Requirement: Entrypoint Operator Skill Inventory
The operator inventory SHALL classify `isomer-op-entrypoint` as the sole public core pack rather than one peer skill among many.

#### Scenario: Entrypoint pack is active
- **WHEN** the manifest and operator assets are inspected
- **THEN** `isomer-op-entrypoint` owns the complete protected core inventory
- **AND** its help and route-and-proceed behavior are public

#### Scenario: Entrypoint does not absorb owner semantics
- **WHEN** a task selects a protected operator capability
- **THEN** the parent loads and follows that member's workflow, gates, and outputs
- **AND** it does not duplicate the full owner procedure in the parent

### Requirement: Operator Inventory Routes Toolbox Manager
The operator pack SHALL preserve `isomer-op-toolbox-mgr` as protected member `toolbox` and SHALL route Toolbox work through the public parent.

#### Scenario: Toolbox member is active
- **WHEN** protected operator inventory is inspected
- **THEN** `toolbox` maps to `isomer-op-toolbox-mgr`
- **AND** no retired Toolbox Creator skill is added

#### Scenario: Welcome and entrypoint use public invocation
- **WHEN** operator guidance describes Toolbox management
- **THEN** it uses `$isomer-op-entrypoint use toolbox to <task>`
- **AND** internal routing uses `isomer-op-entrypoint->toolbox`
