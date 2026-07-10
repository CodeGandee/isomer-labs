## ADDED Requirements

### Requirement: Packaged Kaoju Extension Group
The packaged system-skill manifest SHALL expose Kaoju as an optional extension group with stable id `kaoju`.

#### Scenario: Kaoju manifest group is classified and complete
- **WHEN** `src/isomer_labs/assets/system_skills/manifest.toml` is inspected
- **THEN** group `kaoju` declares `kind = "extension"`, `extension_id = "kaoju"`, and `always_available = false`
- **AND** it lists all eleven production `research-paradigm/kaoju/isomer-kaoju-*` skill paths

#### Scenario: Kaoju paths resolve inside package assets
- **WHEN** packaged system-skill discovery loads the `kaoju` group
- **THEN** every listed path resolves below the packaged system-skill root
- **AND** every listed directory contains `SKILL.md` and its directly linked active resources

#### Scenario: Kaoju extension materializes safely
- **WHEN** a caller materializes or installs extension `kaoju`
- **THEN** the selected output includes the core group plus the eleven Kaoju skills according to existing selector rules
- **AND** it does not include DeepSci skills unless DeepSci or all extensions were also selected

#### Scenario: Kaoju callback insertion points are cataloged
- **WHEN** callback insertion-point metadata is queried for extension `kaoju`
- **THEN** every manifest-listed Kaoju skill exposes the existing `begin` and `end` stages in deterministic manifest order
- **AND** the target skill name and manifest-relative path match the packaged skill identity
