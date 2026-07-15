## ADDED Requirements

### Requirement: Kaoju Shared Contract Commands Are Read-Only and Context-Free
The CLI SHALL expose package-owned Kaoju survey-process and binding resources through deterministic read-only commands under `isomer-cli ext kaoju` without requiring Effective Topic Context.

#### Scenario: Survey-process contract is shown
- **WHEN** a caller runs `isomer-cli --print-json ext kaoju process show`
- **THEN** the command returns a success envelope with `mutated: false`, the survey-process schema version, entry skill, ordered skill and command inventories, manager actions, aliases, and public policy decisions
- **AND** logical links to other shared resources use extension query commands rather than package or repository filesystem paths

#### Scenario: Binding inventory is listed
- **WHEN** a caller runs `isomer-cli --print-json ext kaoju bindings list`
- **THEN** the command returns a deterministic semantic-id-sorted summary with registry version, family, status, artifact type, producer, and consumers for every binding
- **AND** it does not require a Project, Research Topic, or Topic Workspace selection

#### Scenario: One binding is described
- **WHEN** a caller runs a command such as `isomer-cli --print-json ext kaoju bindings describe KAOJU:SURVEY-CONTRACT` for a registered id
- **THEN** the command returns the complete declarative binding and storage-neutral semantic meaning needed by active guidance
- **AND** the request and response preserve the exact canonical `KAOJU:WHAT` identifier without case conversion or placeholder translation
- **AND** it does not return an internal resource path or executable provider payload

#### Scenario: Unknown binding is requested
- **WHEN** `bindings describe` receives an unregistered, non-uppercase, or incompatible semantic id
- **THEN** the command returns a structured non-mutating diagnostic with the requested id and required uppercase grammar
- **AND** it does not select an alias, normalize case, derive another identifier, or choose a fallback binding

#### Scenario: Installed package serves shared contracts
- **WHEN** the commands run from an installed wheel without the source repository or system-skill family root
- **THEN** they load and validate resources from the package-owned Kaoju implementation
- **AND** malformed or missing resources produce deterministic diagnostics rather than a traceback or repository fallback

### Requirement: Kaoju Contract Queries and Artifact Operations Share One Loader
The `ext kaoju` contract queries and `project artifacts` operations SHALL resolve the same validated Kaoju contract and binding objects.

#### Scenario: Agent describes then writes an artifact
- **WHEN** an agent describes a semantic id through `ext kaoju bindings describe` and later invokes `project artifacts put` or `project artifacts revise` for that id
- **THEN** both surfaces report or enforce the same exact uppercase identifier, schema version, binding fields, producer policy, scope policy, and validation expectations
- **AND** no second registry copy or skill-local projection can override the package-owned registry

#### Scenario: Existing project artifact description remains available
- **WHEN** a caller uses `project artifacts describe` during topic-scoped artifact work
- **THEN** the command continues to describe the binding through the shared loader
- **AND** active skill guidance uses `ext kaoju` for context-free shared-resource discovery and `project artifacts` for topic-scoped artifact operations
