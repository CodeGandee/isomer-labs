## ADDED Requirements

### Requirement: Research Idea Display Key
The system SHALL assign each Research Idea a short monotonic decimal topic-scoped display key for GUI and operator-facing references.

#### Scenario: New idea receives display key
- **WHEN** a Research Idea is created
- **THEN** the system assigns a short `display_key` such as `I1`, `I2`, or `I3`
- **AND** the key is unique within the Topic Workspace
- **AND** Workspace Runtime database constraints enforce topic-scoped `display_key` uniqueness

#### Scenario: New display key follows topic allocator
- **WHEN** a Topic Workspace already has Research Ideas with assigned display keys
- **THEN** the next automatically assigned display key follows the Topic Workspace's monotonic decimal display-key allocator
- **AND** the system does not derive the key from the current visible timeline row position

#### Scenario: Display key is stable
- **WHEN** an existing Research Idea is updated, realized by a new record, or shown in Project Web
- **THEN** its `display_key` remains unchanged unless an explicit repair operation changes it

#### Scenario: Display key is not row position
- **WHEN** ideas are sorted, filtered, hidden, deleted, or shown with supporting records disabled
- **THEN** the system does not change surviving ideas' display keys to make visible rows consecutive

#### Scenario: Deleted key is not automatically reused
- **WHEN** a Research Idea is archived or deleted
- **THEN** the system does not automatically reuse that idea's display key for another Research Idea in the same Topic Workspace

#### Scenario: Hard delete does not make key reusable
- **WHEN** a Research Idea is hard-deleted and its row no longer exists
- **THEN** the system keeps enough allocator state or tombstone history to avoid automatically reassigning the deleted idea's display key

### Requirement: Display Key Repair and Migration
The system SHALL provide deterministic handling for existing or imported Research Ideas that lack display keys.

#### Scenario: Existing idea lacks display key
- **WHEN** validation or a timeline read model finds an existing Research Idea without a display key
- **THEN** the system reports a diagnostic that identifies the affected idea
- **AND** ordinary read-only Project Web browsing does not silently mutate the record
- **AND** generic runtime open or unrelated runtime write operations do not automatically assign the missing key

#### Scenario: Operator-invoked repair assigns missing keys
- **WHEN** an explicit operator-invoked migration or repair operation assigns display keys to existing Research Ideas
- **THEN** it assigns short unique keys deterministically within the Topic Workspace
- **AND** the assigned keys follow the monotonic decimal display-key format
- **AND** it reports collisions or unrepairable records as diagnostics

#### Scenario: Imported key collides
- **WHEN** an imported Research Idea proposes a display key already used by another idea in the same Topic Workspace
- **THEN** validation rejects the collision with diagnostics
- **AND** the Workspace Runtime database schema prevents committing the duplicate display key
- **AND** the system does not silently assign a different display key for the proposed colliding key
