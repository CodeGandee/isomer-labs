## MODIFIED Requirements

### Requirement: User Skill Callback Contract
The system SHALL attach User Skill Callbacks to stable packaged capability logical ids and supported stages independently of public pack layout.

#### Scenario: Callback record has stable identity
- **WHEN** a callback is registered
- **THEN** the stored record includes stable callback id, target logical capability id, callback stage, source, scope, status, priority, and source metadata
- **AND** it does not store a nested filesystem path as the target identity

#### Scenario: Protected target is registered
- **WHEN** a callback targets a protected logical id such as `isomer-deepsci-scout`
- **THEN** catalog validation accepts it when that logical id and stage are declared
- **AND** discovery or explained output can report its owning pack and invocation designator

#### Scenario: Old pipeline target is registered
- **WHEN** compatibility input uses `isomer-deepsci-pipeline` or `isomer-kaoju-pipeline`
- **THEN** the system resolves the declared alias to the new public entrypoint id
- **AND** new storage uses the canonical id with a deprecation diagnostic

#### Scenario: Supported stages are bounded
- **WHEN** a callback is registered or resolved
- **THEN** only manifest-declared stages are accepted

### Requirement: Callback Resolution and Merge Order
The system SHALL resolve callbacks by canonical logical capability id and stage before the routed public entrypoint or protected member applies them.

#### Scenario: Exact logical id and stage match
- **WHEN** callbacks are resolved for a protected member
- **THEN** only active records whose normalized target logical id and stage match are included

#### Scenario: Parent routes protected member
- **WHEN** a public pack invokes a protected member
- **THEN** the protected member applies its own begin callbacks before its first capability-specific action and its own end callbacks before completion
- **AND** the parent does not retarget those callbacks to itself

#### Scenario: Scope precedence remains deterministic
- **WHEN** Project and topic callbacks match the same logical id and stage
- **THEN** existing scope and priority ordering remains effective

#### Scenario: Callback resolution is invalid
- **WHEN** target alias normalization is ambiguous or the catalog mapping is invalid
- **THEN** resolution fails with a deterministic diagnostic instead of guessing a nested route

### Requirement: Callback Target Validation Uses Insertion Point Catalog
The system SHALL validate target logical-id and stage pairs against the manifest catalog and SHALL resolve their current pack routing separately.

#### Scenario: Declared protected insertion point is accepted
- **WHEN** a callback targets a declared protected logical id and stage
- **THEN** validation accepts the pair subject to existing source, registry, scope, status, priority, and redaction rules
- **AND** it can report the owning public pack and invocation designator

#### Scenario: Undeclared insertion point is rejected
- **WHEN** a target logical id or stage pair is absent from the catalog
- **THEN** validation rejects it with a diagnostic that names the missing insertion point

#### Scenario: Optional extension target remains catalog based
- **WHEN** a callback targets a protected DeepSci or Kaoju member
- **THEN** validation uses package catalog metadata without inspecting a Project operator skill root
- **AND** output may separately report Project declaration and host verification posture

## ADDED Requirements

### Requirement: Callback Invocation Mapping Is Catalog-Owned
Callback tooling SHALL expose current routing metadata without changing the compact instruction payload consumed during normal execution.

#### Scenario: Insertion points are discovered
- **WHEN** a user or agent lists callback insertion points
- **THEN** each result includes target logical id, stage, public pack id, protected member name when applicable, and invocation designator

#### Scenario: Ordinary resolution succeeds
- **WHEN** a workflow resolves callbacks for one logical id and stage
- **THEN** the compact callback entries retain only the existing actionable instruction fields
- **AND** pack and invocation metadata remain in discovery or explained output rather than every compact entry
