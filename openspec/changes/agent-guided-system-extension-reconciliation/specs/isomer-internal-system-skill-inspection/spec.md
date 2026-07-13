## ADDED Requirements

### Requirement: Internal Explicit-Root Inspection Surface
The system SHALL expose a read-only internal CLI command that inspects one agent-supplied system-skill root without discovering provider-specific roots.

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
The explicit-root inspector SHALL own Isomer receipt discovery, supported schema parsing, catalog membership, projection inspection, and version interpretation so agents do not reproduce those details.

#### Scenario: Supported receipt is present
- **WHEN** the supplied root contains a supported Isomer target-root receipt
- **THEN** the command reports the receipt path, schema status, managed evidence basis, tracked skills, catalog groups, extension ids, and aggregate family coverage
- **AND** the calling agent does not need to provide the receipt filename or schema version

#### Scenario: Legacy receipt is supported
- **WHEN** the root contains a supported legacy receipt
- **THEN** the command parses it through the package-owned migration rules
- **AND** it identifies unversioned or legacy evidence without inventing per-skill versions

#### Scenario: Future or malformed receipt is not guessed
- **WHEN** the root contains an unsupported-schema or malformed receipt
- **THEN** the command reports `unsupported_schema` or `malformed_receipt`
- **AND** it does not silently classify arbitrary directory names as managed receipt evidence

### Requirement: Root Inspection Handles Directory and Symlink Projections
The explicit-root inspector SHALL evaluate receipt-recorded skill projections as real directories or symlinked directories without recursive discovery.

#### Scenario: Real directory projection is valid
- **WHEN** a tracked skill path is a directory containing the required skill material
- **THEN** the command reports its projection mode as `copy` or directory projection

#### Scenario: Symlinked skill directory is valid
- **WHEN** a tracked skill path is a symlink that resolves to a skill directory
- **THEN** the command reports a symlink projection and its resolved inspection status
- **AND** it does not modify the link or target

#### Scenario: Broken or invalid projection is diagnosed
- **WHEN** a tracked path is a broken symlink, regular file, unsupported path kind, or missing projection
- **THEN** the command reports the affected catalog skill and deterministic projection diagnostic
- **AND** a family containing that skill is not reported as complete

### Requirement: Internal Live Inventory Classification
The system SHALL expose a read-only internal CLI command that maps agent-supplied live skill inventory entries to packaged core and extension families.

#### Scenario: Repeated skill names classify a complete extension
- **WHEN** an agent runs `isomer-cli internals classify-system-skill-inventory` with repeated `--skill-name` values covering every member of one packaged extension
- **THEN** the command reports that extension as complete with `live_inventory` evidence
- **AND** the agent does not need to know which names belong to the extension family

#### Scenario: Partial inventory names missing members
- **WHEN** supplied inventory names include only part of a packaged extension family
- **THEN** the command reports the family as partial and names the missing catalog members

#### Scenario: Structured inventory input is versioned
- **WHEN** the command accepts a structured inventory JSON input
- **THEN** it validates a versioned input schema and returns a versioned internal output contract
- **AND** unsupported input schemas fail deterministically without mutation

#### Scenario: Unknown inventory skills remain ambient
- **WHEN** supplied names do not match packaged Isomer system skills
- **THEN** the command reports them as unmatched ambient inventory entries
- **AND** it does not assign them to an Isomer extension

### Requirement: Internal Inspection Output Is Deterministic
Internal system-skill inspection SHALL return deterministic evidence and diagnostics suitable for version-aligned packaged system skills.

#### Scenario: JSON describes evidence basis
- **WHEN** an internal inspection command runs in JSON mode
- **THEN** each recognized family reports its evidence basis, coverage status, installed and missing members, receipt status when applicable, projection status when applicable, and version or compatibility status when known
- **AND** the response uses the standard CLI output wrapper with `mutated: false`

#### Scenario: Inspection never registers extensions
- **WHEN** internal root or inventory inspection finds a complete extension
- **THEN** it does not modify a Project Manifest
- **AND** registration remains an operator-skill orchestration decision
