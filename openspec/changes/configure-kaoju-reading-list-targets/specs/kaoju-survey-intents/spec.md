## MODIFIED Requirements

### Requirement: Kaoju Maintains One Reading List per Direction
The system SHALL maintain one scoped current `kaoju:reading-list` for each selected direction, SHALL preserve prior revisions, and SHALL derive and persist the effective priority and secondary target counts that bound discovery.

#### Scenario: Default reading-list target is applied
- **WHEN** the actor asks to collect online information for one accepted direction without specifying a count
- **THEN** the discover skill targets three priority items and three secondary items
- **AND** the Reading List records the default target, achieved counts, unresolved deficits, search boundaries, and why each selected item has its priority

#### Scenario: Actor specifies category targets
- **WHEN** the actor specifies a priority count, a secondary count, or both for one direction
- **THEN** the discover skill uses each supplied non-negative integer as that category's target and defaults each omitted category to three
- **AND** the combined effective target must contain at least one work
- **AND** the Reading List records the effective counts with a user-category derivation

#### Scenario: Actor specifies a total target
- **WHEN** the actor requests a positive integer total of `N` works without category counts
- **THEN** the discover skill targets `ceil(N / 2)` priority works and `floor(N / 2)` secondary works
- **AND** the Reading List records `N`, the derived category counts, and a user-total derivation

#### Scenario: Count request is invalid or ambiguous
- **WHEN** the actor supplies a negative or fractional count, a zero total, category counts whose effective sum is zero, or both total and category count modes
- **THEN** the system requests clarification before discovery
- **AND** it does not invent, clamp, or silently prioritize a count

#### Scenario: Shorter result is a warning
- **WHEN** bounded discovery cannot identify enough suitable priority or secondary items to meet the effective target
- **THEN** the system records the reachable list, achieved counts, category deficits, and a non-blocking coverage warning against that target
- **AND** the actor may approve the shorter list or request further discovery

#### Scenario: Candidate is blocked during discovery
- **WHEN** a selected candidate cannot be accessed or its identity cannot be resolved
- **THEN** the system preserves the candidate and blocker in discovery provenance without counting it toward the applicable reachable target
- **AND** it performs bounded backfill before reporting any remaining coverage deficit

#### Scenario: Legacy list omits target metadata
- **WHEN** the system validates a Reading List created before configurable target metadata was recorded
- **THEN** it interprets the missing target as three priority items and three secondary items
- **AND** it does not require migration or mutation of the existing Artifact

#### Scenario: Different directions do not collide
- **WHEN** a topic contains reading lists for two accepted directions
- **THEN** each list uses the applicable direction scope key and independently records its effective target
- **AND** a target or item revision for one direction does not supersede the other direction's list
