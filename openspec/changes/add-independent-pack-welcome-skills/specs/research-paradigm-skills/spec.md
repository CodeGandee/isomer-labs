## MODIFIED Requirements

### Requirement: Research Paradigm Skillset Layout
The packaged research-paradigm surface SHALL organize each production extension as an independent public welcome and entrypoint pair with protected stage subskills below the entrypoint.

#### Scenario: DeepSci layout is inspected
- **WHEN** production DeepSci package assets are listed
- **THEN** `isomer-ext-deepsci-welcome` and `isomer-ext-deepsci-entrypoint` are public siblings
- **AND** current `isomer-deepsci-*` stage, shared, companion, Nature-facing, and workspace capabilities remain entrypoint-protected

#### Scenario: Kaoju layout is inspected
- **WHEN** production Kaoju package assets are listed
- **THEN** `isomer-ext-kaoju-welcome` and `isomer-ext-kaoju-entrypoint` are public siblings
- **AND** current `isomer-kaoju-*` survey, shared, and workspace capabilities remain entrypoint-protected

#### Scenario: Welcome does not duplicate private resources
- **WHEN** either extension welcome bundle is inspected
- **THEN** it owns only onboarding and command-learning resources
- **AND** it does not copy protected scripts, procedure pages, registries, templates, or execution metadata from the entrypoint tree

### Requirement: Progressive Disclosure
Research-paradigm packs SHALL use welcome for newcomer-oriented use-case selection, entrypoint commands for public execution, and protected subskills for private capability procedure detail.

#### Scenario: Newcomer asks for typical patterns
- **WHEN** the user asks what DeepSci or Kaoju is for or how to use it
- **THEN** the extension welcome presents concise representative patterns and exact entrypoint examples
- **AND** it loads a complete command map only when explicitly requested

#### Scenario: User gives a concrete research task
- **WHEN** the user supplies an actionable DeepSci or Kaoju task
- **THEN** the extension entrypoint selects a public command or protected member and proceeds under its workflow
- **AND** it does not force the user through welcome first

#### Scenario: Protected detail is needed
- **WHEN** an entrypoint selects a capability with its own resources
- **THEN** it loads only that protected subskill and its route-specific resources
- **AND** welcome remains outside the execution chain

### Requirement: Validation
The implementation SHALL include repository-runnable validation that covers extension public pairs, welcome teaching contracts, entrypoint execution contracts, protected members, and self-contained resource boundaries.

#### Scenario: Extension public pair validation runs
- **WHEN** research-paradigm validation inspects DeepSci or Kaoju
- **THEN** it confirms exactly one welcome and one entrypoint with canonical names, roles, metadata, versions, and sibling paths
- **AND** it validates that every protected capability remains nested below the entrypoint

#### Scenario: Welcome coverage validation runs
- **WHEN** an extension welcome skill is validated
- **THEN** the validator checks common welcome commands, pack-specific typical-use-case categories, exact public invocation examples, complete entrypoint command-map coverage, read-only posture, and no direct protected invocation

#### Scenario: Family rules remain active
- **WHEN** public welcome skills are added
- **THEN** existing DeepSci and Kaoju checks for domain language, placeholders, evidence, callbacks, output policy, resource ownership, provenance, Gate discipline, and executable boundaries continue to apply to their relevant entrypoint or protected files
- **AND** welcome-only teaching prose is not mistaken for execution authorization

### Requirement: Production Kaoju Research-Paradigm Layout
The production Kaoju family SHALL include an independent public welcome and execution entrypoint while preserving the accepted protected survey-process inventory and shared-resource ownership.

#### Scenario: Kaoju public layout is inspected
- **WHEN** production Kaoju directories are enumerated
- **THEN** the public directories are `isomer-ext-kaoju-welcome` and `isomer-ext-kaoju-entrypoint`
- **AND** protected capabilities remain below the entrypoint using stable `isomer-kaoju-*` logical ids

#### Scenario: Kaoju active resources are separated
- **WHEN** Kaoju welcome and entrypoint resources are classified
- **THEN** newcomer examples and command maps belong to welcome while command implementations and protected capability resources belong to entrypoint or the selected subskill
- **AND** the package-owned process and binding registries remain the sole machine authorities

### Requirement: Research-Paradigm Validation Supports Kaoju
Research-paradigm validation SHALL enforce Kaoju welcome, entrypoint, and protected-member roles without weakening existing Kaoju-specific rules.

#### Scenario: Valid Kaoju pair passes
- **WHEN** the Kaoju pack has canonical public metadata, complete welcome command coverage, a valid execution entrypoint, and thirteen valid protected members
- **THEN** research-paradigm validation accepts the public/protected layout

#### Scenario: Kaoju welcome copies execution procedure
- **WHEN** active welcome guidance embeds manager implementation, command execution steps, or protected private resource paths
- **THEN** validation reports a role-boundary violation
- **AND** it directs the content to an entrypoint command or protected owner
