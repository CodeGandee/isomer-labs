## MODIFIED Requirements

### Requirement: Packaged Kaoju Extension Group
The packaged system-skill manifest SHALL expose Kaoju as an optional extension group with stable id `kaoju` and the complete fourteen-skill survey-process inventory.

#### Scenario: Kaoju manifest group is classified and complete
- **WHEN** `src/isomer_labs/assets/system_skills/manifest.toml` is inspected
- **THEN** group `kaoju` declares `kind = "extension"`, `extension_id = "kaoju"`, and `always_available = false`
- **AND** it lists the fourteen production paths for `isomer-kaoju-pipeline`, `isomer-kaoju-shared`, `isomer-kaoju-workspace-mgr`, `isomer-kaoju-frame`, `isomer-kaoju-discover`, `isomer-kaoju-acquire`, `isomer-kaoju-examine`, `isomer-kaoju-reproduce`, `isomer-kaoju-trial`, `isomer-kaoju-compare`, `isomer-kaoju-audit`, `isomer-kaoju-synthesize`, `isomer-kaoju-write`, and `isomer-kaoju-export`

#### Scenario: Kaoju paths resolve inside package assets
- **WHEN** packaged system-skill discovery loads the `kaoju` group
- **THEN** every listed path resolves below the packaged system-skill root
- **AND** every listed directory contains `SKILL.md`, `agents/openai.yaml`, and its directly linked active commands, references, assets, or scripts

#### Scenario: Kaoju extension materializes safely
- **WHEN** a caller materializes or installs extension `kaoju`
- **THEN** the selected output includes the core group plus all fourteen Kaoju skills according to existing selector rules
- **AND** it does not include DeepSci skills unless DeepSci or all extensions were also selected

#### Scenario: Kaoju callback insertion points are cataloged
- **WHEN** callback insertion-point metadata is queried for extension `kaoju`
- **THEN** every manifest-listed Kaoju skill exposes its approved callback stages in deterministic manifest order
- **AND** the target skill name and manifest-relative path match the packaged skill identity

#### Scenario: Kaoju entry surface declares survey intents
- **WHEN** extension discovery metadata is queried for `kaoju`
- **THEN** `isomer-kaoju-pipeline` remains the entry skill and its ordered command ids include all ten survey-process intents plus retained compatibility procedures and grouped managers
- **AND** the metadata is derived from the packaged manifest rather than a duplicate hard-coded command list

#### Scenario: Kaoju package is self-contained
- **WHEN** an installed package materializes the Kaoju extension
- **THEN** every skill can resolve its active direct resources, semantic and binding references, command pages, templates, and helper scripts without a repository checkout
- **AND** no active skill requires feature-design files, archived OpenSpec changes, external source checkouts, provider credentials, or the external `imsight-llm-wiki` skill merely to load or validate
