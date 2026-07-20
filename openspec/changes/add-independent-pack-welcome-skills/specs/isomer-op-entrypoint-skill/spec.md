## MODIFIED Requirements

### Requirement: Entrypoint Operator Skill Inventory
The system SHALL provide `isomer-op-entrypoint` as the public core execution skill for informed-user task routing while providing `isomer-op-welcome` as a separate public newcomer skill.

#### Scenario: Entrypoint assets exist
- **WHEN** the packaged core skillset is inspected
- **THEN** it contains `operator/isomer-op-entrypoint/SKILL.md`, `agents/openai.yaml`, directly linked routing resources, and the declared protected subskill inventory
- **AND** it contains no protected `isomer-op-welcome` bundle

#### Scenario: Public core pair is distinct
- **WHEN** the core catalog is inspected
- **THEN** `isomer-op-entrypoint` has role `entrypoint` and `isomer-op-welcome` has role `welcome`
- **AND** both public skills belong to the same complete core pack without sharing private resources

#### Scenario: Entrypoint identity is consistent
- **WHEN** `operator/isomer-op-entrypoint` is inspected
- **THEN** its folder, frontmatter, UI metadata, and default prompt use `isomer-op-entrypoint`
- **AND** its description identifies route-and-proceed execution rather than newcomer tutorial ownership

### Requirement: Entrypoint Routes Then Proceeds
The entrypoint SHALL resolve a public command or concrete task to one protected member, optional public extension entrypoint, or CLI surface and proceed by default, while orientation-only requests route to the independent welcome skill.

#### Scenario: User invokes a public execution command
- **WHEN** the user supplies `$isomer-op-entrypoint use <command> to <task>`
- **THEN** the entrypoint resolves the command and proceeds through the matching route or reports a concrete blocker

#### Scenario: Invocation is empty
- **WHEN** the user invokes `$isomer-op-entrypoint` without a task or command
- **THEN** the entrypoint delegates read-only output to `$isomer-op-welcome` while preserving supplied context
- **AND** it does not load a private welcome subskill

#### Scenario: User asks how to use Isomer
- **WHEN** the request is orientation, command-learning, route comparison, or typical-use-case discovery rather than execution
- **THEN** the entrypoint delegates to `$isomer-op-welcome` without losing supplied context
- **AND** welcome remains non-mutating

#### Scenario: Concrete task has no command
- **WHEN** the user gives a concrete task, prompt, or file without asking only for help
- **THEN** the entrypoint selects one protected member, public extension entrypoint, or CLI command family
- **AND** it proceeds or reports a blocker instead of stopping after route enumeration

### Requirement: Entrypoint Indexes All System Skill Families
The entrypoint SHALL index core protected operator, service, and shared capabilities while linking public welcome skills as orientation surfaces rather than protected owner routes.

#### Scenario: Operator routes are indexed
- **WHEN** the entrypoint protected route table is inspected
- **THEN** it contains Project lifecycle, GUI, identity, system-skill management, Toolbox management, Topic creation, Topic management, and Topic Team Specialization members
- **AND** it does not contain member `welcome`

#### Scenario: Welcome route is public
- **WHEN** entrypoint guidance explains orientation
- **THEN** it names `$isomer-op-welcome` as the public core learning surface
- **AND** it does not use `isomer-op-entrypoint->welcome` as an active designator

#### Scenario: Service and shared routes stay bounded
- **WHEN** service or shared support is needed
- **THEN** entrypoint routing uses the applicable protected member under its existing owner boundary
- **AND** public guidance does not present protected logical ids as peer welcome or entrypoint skills

### Requirement: Entrypoint Includes Extension Skill Routing
The core entrypoint SHALL route optional research paradigms through their public extension entrypoints and SHALL point orientation-only extension questions to their public welcome skills.

#### Scenario: Extension public pairs are indexed
- **WHEN** entrypoint extension references are inspected
- **THEN** they identify `isomer-ext-deepsci-welcome` with `isomer-ext-deepsci-entrypoint` and `isomer-ext-kaoju-welcome` with `isomer-ext-kaoju-entrypoint`
- **AND** they distinguish learning from execution

#### Scenario: Prepared extension task is selected
- **WHEN** a concrete task maps to DeepSci or Kaoju and required readiness exists
- **THEN** the core entrypoint routes to the matching extension execution entrypoint
- **AND** the extension entrypoint selects its protected member while preserving existing callbacks, evidence, Gate, and output contracts

#### Scenario: Extension comparison is requested
- **WHEN** the user asks how to use one extension or compare its typical workflows without requesting execution
- **THEN** the core entrypoint routes to the applicable extension welcome or core welcome comparison guidance
- **AND** it performs no extension task mutation

### Requirement: Entrypoint Validation
The repository SHALL validate `isomer-op-entrypoint` as the public core execution surface and enforce its boundary with the independent welcome skill.

#### Scenario: Valid entrypoint passes
- **WHEN** operator validation runs against a valid core pack
- **THEN** it checks public execution invocation, route-and-proceed language, protected inventory, CLI routes, extension public pairs, service and shared boundaries, compatibility delegation, and retired-route exclusions
- **AND** it confirms that welcome is absent from the protected inventory

#### Scenario: Entrypoint retains private welcome
- **WHEN** the entrypoint contains a protected `welcome` member, private welcome resources, or active `isomer-op-entrypoint->welcome` guidance
- **THEN** validation reports that welcome must be the independent public `isomer-op-welcome` skill

#### Scenario: Compatibility command duplicates welcome content
- **WHEN** a retained entrypoint help or onboarding alias copies the welcome procedure instead of delegating to the public welcome skill
- **THEN** validation reports duplicate ownership and the canonical welcome route
