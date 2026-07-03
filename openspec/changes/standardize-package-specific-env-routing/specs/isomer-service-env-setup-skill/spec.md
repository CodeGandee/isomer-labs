## ADDED Requirements

### Requirement: Topic Env Derivation Uses Package Specifics First
The topic environment setup service SHALL consult `isomer-misc-pkg-specifics` for every named package before applying generic package-source, Pixi, PyPI, Conda, runtime-wiring, or verification rules during operational topic env target-spec derivation.

#### Scenario: Named package has package-specific rule
- **WHEN** `derive-env-gate` converts source intent or an explicit target spec into `topic.env.topic_setup_target_spec`
- **AND** the dependency plan names a package listed by `isomer-misc-pkg-specifics`
- **THEN** `derive-env-gate` applies the selected package-specific source, variant, verification, warning, and blocker guidance before generic package routing
- **AND** the generated target spec records the selected package-specific evidence

#### Scenario: Named package has no package-specific rule
- **WHEN** `derive-env-gate` considers a named package that is not listed by `isomer-misc-pkg-specifics`
- **THEN** it records `no package-specific rule`
- **AND** it continues with the generic package-source ladder, enclosure strategy, bounded-run policy, and verification rules

#### Scenario: Generic PyPI preference is subordinate to package specifics
- **WHEN** a named Python package can satisfy a gate through PyPI in the generic ladder
- **AND** `isomer-misc-pkg-specifics` provides a package-specific rule that selects another source, variant, verification, warning, or blocker
- **THEN** the package-specific rule takes precedence over the generic PyPI preference

### Requirement: Topic Env Install and Verification Use Recorded Package Evidence
The topic environment setup service SHALL use package-specific evidence recorded in `topic.env.topic_setup_target_spec` when installing dependencies or verifying package-specific runtime readiness.

#### Scenario: Install uses package-specific source decision
- **WHEN** `install-topic-deps` installs a named package whose target spec entry includes package-specific source or variant evidence
- **THEN** it uses that recorded package-specific evidence for the Pixi, PyPI, Conda, runtime-wiring, fallback, or blocker decision
- **AND** it does not replace that evidence with a generic package-source choice

#### Scenario: Verification uses package-specific runtime expectation
- **WHEN** `verify-env-gate` verifies readiness for a named package whose target spec entry includes package-specific runtime checks
- **THEN** it runs or reports the recorded package-specific verification expectation
- **AND** it does not claim readiness from generic import success or solver success alone when the package-specific evidence requires a stronger check

### Requirement: Topic Env Service Owns Operational Topic Gate Derivation
The topic environment setup service SHALL remain the owner of operational `topic.env.topic_setup_target_spec` derivation from high-level topic env source intent.

#### Scenario: Operator source intent remains high level
- **WHEN** an operator skill writes or updates `topic.intent.topic_env_requirements`
- **THEN** it may name desired libraries, tools, repositories, runtimes, datasets, commands, or capabilities
- **AND** operational package-source choices, Pixi install commands, runtime-wiring commands, package-specific verification commands, and dependency blockers are derived by `isomer-srv-topic-env-setup`

#### Scenario: Full setup routes through service derivation
- **WHEN** a caller needs operational topic env target-spec derivation from source intent
- **THEN** it routes to `isomer-srv-topic-env-setup derive-env-gate` or the full `setup-topic-env` flow
- **AND** it does not hand-roll `topic.env.topic_setup_target_spec` in operator guidance unless the user supplied an explicit manual target spec for service validation
