## MODIFIED Requirements

### Requirement: Pipeline skill exists
The project SHALL provide `isomer-ext-deepsci-entrypoint` as the DeepSci execution entrypoint and `isomer-ext-deepsci-welcome` as its independent public newcomer skill.

#### Scenario: DeepSci public pair is packaged
- **WHEN** the production DeepSci pack is inspected
- **THEN** it contains sibling public bundles `isomer-ext-deepsci-welcome` and `isomer-ext-deepsci-entrypoint`
- **AND** all existing DeepSci stage capabilities remain protected below the entrypoint

#### Scenario: DeepSci public roles are distinct
- **WHEN** DeepSci metadata is inspected
- **THEN** welcome describes typical production-research patterns and performs no research task mutation
- **AND** entrypoint executes named pass commands or routes concrete tasks through protected DeepSci stages

#### Scenario: Historical pipeline identity is used
- **WHEN** compatibility lookup encounters `isomer-deepsci-pipeline`
- **THEN** it resolves to the execution entrypoint rather than the welcome skill
- **AND** guidance recommends the welcome skill only for onboarding or command-learning intent

### Requirement: Pipeline passes are self-contained subcommand pages
The DeepSci execution entrypoint SHALL retain self-contained pass command pages, while the independent DeepSci welcome skill SHALL own only newcomer use-case and command-learning resources.

#### Scenario: Pass page is inspected
- **WHEN** an active DeepSci pass command is inspected
- **THEN** its execution stages, handoffs, Gates, callbacks, and terminal contract remain owned by `isomer-ext-deepsci-entrypoint`
- **AND** the welcome skill links to the public command without copying the pass procedure

#### Scenario: Welcome example references a pass
- **WHEN** DeepSci welcome teaches a hypothesis, empirical, paper, revision, rebuttal, or polish pattern
- **THEN** it provides an exact `$isomer-ext-deepsci-entrypoint use <pass> to <task>` example
- **AND** it explains prerequisites and mutation posture without executing the pass

### Requirement: Initial pipeline catalog
The DeepSci pack SHALL preserve its accepted execution-pass catalog and expose complete newcomer mapping for that catalog through the independent welcome skill.

#### Scenario: Execution pass catalog is inspected
- **WHEN** `isomer-ext-deepsci-entrypoint` public commands are read from the manifest
- **THEN** they include the accepted empirical, hypothesis, paper, polish, rebuttal, revision, submission, list, and help commands in deterministic order
- **AND** protected stage ownership remains unchanged

#### Scenario: Welcome command map is inspected
- **WHEN** `isomer-ext-deepsci-welcome` command-map guidance is validated
- **THEN** every manifest-declared DeepSci entrypoint command appears exactly once with a one-sentence use condition and exact invocation
- **AND** no protected DeepSci logical id is advertised as a direct public skill
