## MODIFIED Requirements

### Requirement: Internal Root Inspection Owns Managed Receipt Details
The explicit-root inspector SHALL parse supported pack-aware and legacy receipts, inspect public projections, and verify protected nested inventories so agents do not reproduce catalog rules.

#### Scenario: Supported v4 receipt is present
- **WHEN** a supplied root contains a supported v4 Isomer receipt
- **THEN** the command reports receipt path, schema status, bindings, tracked public packs, extension ids, protected member coverage, projection modes, and version compatibility
- **AND** complete status requires every receipt and catalog member check to pass

#### Scenario: Legacy receipt is supported
- **WHEN** the root contains a supported v1, v2, or v3 receipt
- **THEN** the command reports the tracked flat skills and their legacy evidence basis
- **AND** it identifies candidate owning packs without claiming nested pack integrity

#### Scenario: Future or malformed receipt is not guessed
- **WHEN** the root contains an unsupported or malformed receipt
- **THEN** the command reports `unsupported_schema` or `malformed_receipt`
- **AND** it does not classify arbitrary directory names as managed pack evidence

### Requirement: Root Inspection Handles Directory and Symlink Projections
The explicit-root inspector SHALL evaluate each receipt-recorded public pack and its protected nested members without recursively discovering ambient skills.

#### Scenario: Real public pack is valid
- **WHEN** a tracked public pack is a directory containing the declared entrypoint and complete member inventory
- **THEN** the command reports copy projection and verified nested coverage

#### Scenario: Symlinked public pack is valid
- **WHEN** a tracked public pack is a symlink to a complete pack directory
- **THEN** the command reports symlink projection and verified nested coverage
- **AND** it does not modify the link or target

#### Scenario: Broken or invalid projection is diagnosed
- **WHEN** a tracked path is a broken symlink, regular file, unsupported path kind, or missing projection
- **THEN** the command reports the affected catalog skill and deterministic projection diagnostic
- **AND** a family containing that skill is not reported as complete

#### Scenario: Nested member is invalid
- **WHEN** a declared protected member is missing, has the wrong identity or version, or contains invalid required resources
- **THEN** the command reports the affected pack and logical id
- **AND** it does not report the pack or extension as complete

#### Scenario: Ambient sibling is present
- **WHEN** the root contains an untracked top-level path
- **THEN** inspection reports it as ambient without recursive classification or mutation

### Requirement: Internal Live Inventory Classification
The live-inventory classifier SHALL recognize public pack names but SHALL NOT infer complete protected coverage from name-only host inventory.

#### Scenario: Public entrypoint name is supplied
- **WHEN** live inventory contains `isomer-ext-deepsci-entrypoint` or `isomer-ext-kaoju-entrypoint`
- **THEN** the command reports `entrypoint_seen` evidence for that extension
- **AND** it reports protected member integrity as unverified

#### Scenario: All three public names are supplied
- **WHEN** live inventory contains all current public entrypoints without receipt or root evidence
- **THEN** the command reports all three entrypoints as seen
- **AND** it does not report any pack as complete solely from those names

#### Scenario: Legacy flat names are supplied
- **WHEN** live inventory contains protected logical ids from a prior flat installation
- **THEN** the command reports them as legacy member observations and identifies candidate owning packs
- **AND** it does not confuse them with current public install units

#### Scenario: Structured inventory input is versioned
- **WHEN** structured inventory JSON is supplied
- **THEN** the command validates its schema and returns a versioned output contract that distinguishes entrypoint observation, legacy member observation, and verified evidence

#### Scenario: Unknown names remain ambient
- **WHEN** supplied names match no public entrypoint, protected logical id, or declared alias
- **THEN** they remain unmatched ambient entries

### Requirement: Internal Inspection Output Is Deterministic
Internal inspection SHALL return deterministic pack, capability, evidence, and diagnostic data suitable for version-aligned skills.

#### Scenario: JSON describes evidence basis
- **WHEN** an inspection command runs in JSON mode
- **THEN** each recognized pack reports evidence basis, entrypoint status, coverage status, installed and missing logical members, receipt status, projection status, and version status
- **AND** output uses the standard CLI wrapper with `mutated: false`

#### Scenario: Inspection never registers extensions
- **WHEN** inspection verifies or observes an extension pack
- **THEN** it does not modify the Project Manifest
- **AND** registration remains an operator workflow decision
