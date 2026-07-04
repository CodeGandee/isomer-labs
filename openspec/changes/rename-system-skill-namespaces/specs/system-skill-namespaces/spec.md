## ADDED Requirements

### Requirement: Packaged System Skill Namespace Convention
The system SHALL define active packaged system-skill namespaces that keep the `isomer-` product prefix and encode responsibility in the next namespace segment.

#### Scenario: Namespace convention is documented
- **WHEN** the packaged system-skill documentation is inspected
- **THEN** it defines `isomer-misc-<purpose>` for public cross-domain helper interfaces
- **AND** it defines `isomer-op-<purpose>` for user-facing Project Operator Session and Operator Agent skills
- **AND** it defines `isomer-srv-<purpose>` for protected service-routed operational support skills
- **AND** it defines `isomer-<extension-name>-<purpose>` for domain extension skill families

#### Scenario: Generic extension bucket is avoided
- **WHEN** documentation explains future extension naming
- **THEN** it states that extension families are named by their domain or methodology, such as `deepsci`
- **AND** it does not introduce `isomer-ext-*` as a generic active extension namespace
- **AND** it keeps `isomer-misc-*` distinct from domain extension families

### Requirement: Active Namespace Inventory
The packaged system-skill manifest SHALL list active skill paths that match the current namespace convention.

#### Scenario: Manifest uses active namespace names
- **WHEN** `src/isomer_labs/assets/system_skills/manifest.toml` is inspected
- **THEN** every operator skill path uses `operator/isomer-op-<purpose>`
- **AND** every production DeepSci skill path uses `research-paradigm/deepsci/isomer-deepsci-<purpose>`
- **AND** misc helper skill paths continue to use `misc/isomer-misc-<purpose>`
- **AND** service skill paths continue to use `service/isomer-srv-<purpose>`

#### Scenario: Active skill identity matches folder name
- **WHEN** a manifest-listed active skill is inspected
- **THEN** its folder name, `SKILL.md` frontmatter `name`, `agents/openai.yaml` display name, and default prompt use the same active skill name

### Requirement: No Active Legacy Namespace Shims
The system SHALL NOT keep active compatibility skill folders, aliases, or duplicate shims for superseded `isomer-admin-*` or `isomer-rsch-*` names.

#### Scenario: Old operator and research names are absent from active catalog
- **WHEN** the packaged system-skill manifest and active skill directories are inspected
- **THEN** no active skill path starts with `operator/isomer-admin-`
- **AND** no active production DeepSci skill path starts with `research-paradigm/deepsci/isomer-rsch-`

#### Scenario: Historical material may preserve old names
- **WHEN** archived OpenSpec changes, passive provenance files, upstream source copies, or migration notes are inspected
- **THEN** they may retain old `isomer-admin-*` or `isomer-rsch-*` names as historical context
- **AND** active validators do not treat those passive references as current invokable skill names
