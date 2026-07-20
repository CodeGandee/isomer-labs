## MODIFIED Requirements

### Requirement: Internal Explicit-Root Inspection Surface
The system SHALL expose read-only explicit-root inspection that reports every public skill role and protected-member integrity for selected packs without assuming one public name is a complete pack.

#### Scenario: Complete v5 pack is inspected
- **WHEN** an explicit skill root contains receipt-owned welcome and entrypoint projections plus a valid protected entrypoint inventory
- **THEN** inspection reports both public skills, their roles and projection states, the designated entrypoint, protected-member evidence, and aggregate verified pack coverage

#### Scenario: Only welcome is present
- **WHEN** an explicit root contains the expected welcome but not its sibling entrypoint
- **THEN** inspection reports `welcome_seen` and incomplete pack coverage
- **AND** it does not claim protected integrity or host usability

#### Scenario: Only entrypoint is present
- **WHEN** an explicit root contains the expected entrypoint but not its sibling welcome
- **THEN** inspection reports `entrypoint_seen`, any inspectable protected state, and incomplete public coverage
- **AND** it does not classify the pack as verified

### Requirement: Internal Root Inspection Owns Managed Receipt Details
Explicit-root inspection SHALL treat v5 pack receipts as the authority for ownership of multiple public projections and SHALL report earlier receipt evidence conservatively.

#### Scenario: V5 receipt is current
- **WHEN** root inspection reads a valid v5 receipt
- **THEN** it correlates each welcome and entrypoint destination with its public projection record
- **AND** it verifies the protected inventory against the designated entrypoint record

#### Scenario: V4 compacted receipt is read
- **WHEN** root inspection reads a supported v4 receipt containing one entrypoint projection per pack
- **THEN** it reports legacy public-role evidence and the missing independent welcome
- **AND** it recommends managed upgrade without inventing v5 ownership

#### Scenario: Receipt and live files disagree
- **WHEN** one public projection is absent, untracked, identity-mismatched, version-drifted, or uses a different mode from its v5 record
- **THEN** inspection reports that exact public-role failure
- **AND** aggregate pack status is not verified

### Requirement: Internal Live Inventory Classification
The internal inventory classifier SHALL recognize welcome and entrypoint names as separate public observations while reserving complete-pack claims for stronger evidence.

#### Scenario: Both public names are observed
- **WHEN** live inventory contains an extension welcome and entrypoint name
- **THEN** classification associates both with the same pack and reports their roles
- **AND** it still marks protected integrity as unverified without receipt or explicit-root evidence

#### Scenario: Welcome name is observed alone
- **WHEN** live inventory contains `isomer-op-welcome`, `isomer-ext-deepsci-welcome`, or `isomer-ext-kaoju-welcome` without its entrypoint
- **THEN** classification reports a welcome-only partial observation
- **AND** it does not treat welcome as a legacy alias or protected member

#### Scenario: Protected name is observed
- **WHEN** live inventory contains a protected logical id
- **THEN** classification retains its owning entrypoint designator and pack id
- **AND** it does not associate the protected identity with the welcome skill

### Requirement: Internal Inspection Output Is Deterministic
Internal inspection SHALL return public skills in manifest order, protected members in manifest order, and stable aggregate status independent of filesystem enumeration order.

#### Scenario: Structured output is repeated
- **WHEN** the same root or inventory is inspected more than once
- **THEN** pack, public-skill, protected-member, alias, and unmatched rows appear in deterministic order
- **AND** welcome precedes or follows entrypoint exactly as declared by manifest v4
