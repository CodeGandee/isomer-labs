# isomer-internal-system-skill-inspection Specification

## Purpose
TBD - created by archiving change agent-guided-system-extension-reconciliation. Update Purpose after archive.
## Requirements
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

#### Scenario: Agent supplies one skill root
- **WHEN** an agent runs `isomer-cli internals inspect-system-skill-root --skill-root <path>`
- **THEN** the command inspects exactly the supplied root
- **AND** it does not search parent directories, user-home directories, provider configuration, plugins, or conventional agent-tool paths
- **AND** it reports `mutated: false`

#### Scenario: Root is absent
- **WHEN** the supplied skill root does not exist
- **THEN** the command reports a deterministic absent-root result
- **AND** it does not create the root or any receipt

#### Scenario: Category and catalog filters are accepted
- **WHEN** an agent supplies `--category core`, `--category extensions`, `--category all`, `--extension <extension-id>`, or `--group <group-name>`
- **THEN** the command resolves filters from the packaged system-skill catalog
- **AND** unknown filters fail without filesystem mutation
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
Internal inspection SHALL return public skills in manifest order, protected members in manifest order, and stable aggregate status independent of filesystem enumeration order.

#### Scenario: Structured output is repeated
- **WHEN** the same root or inventory is inspected more than once
- **THEN** pack, public-skill, protected-member, alias, and unmatched rows appear in deterministic order
- **AND** welcome precedes or follows entrypoint exactly as declared by manifest v4

#### Scenario: JSON describes evidence basis
- **WHEN** an inspection command runs in JSON mode
- **THEN** each recognized pack reports evidence basis, entrypoint status, coverage status, installed and missing logical members, receipt status, projection status, and version status
- **AND** output uses the standard CLI wrapper with `mutated: false`

#### Scenario: Inspection never registers extensions
- **WHEN** inspection verifies or observes an extension pack
- **THEN** it does not modify the Project Manifest
- **AND** registration remains an operator workflow decision
