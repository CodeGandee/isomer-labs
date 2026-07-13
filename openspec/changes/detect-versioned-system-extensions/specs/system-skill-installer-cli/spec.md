## ADDED Requirements

### Requirement: Packaged Skills Carry Release-Aligned Versions
Every packaged Isomer system skill SHALL declare `metadata.version` in `agents/openai.yaml` using the exact PEP 440 Isomer CLI/package version that ships the skill, including release candidate versions.

#### Scenario: Packaged source version matches the CLI release
- **WHEN** packaged system-skill assets are validated for a release
- **THEN** every skill's `agents/openai.yaml` contains a valid PEP 440 `metadata.version`
- **AND** the version equals the Isomer CLI/package version
- **AND** `SKILL.md` frontmatter does not duplicate the skill version

#### Scenario: Release candidate version is accepted
- **WHEN** the Isomer CLI/package version is a valid release candidate such as `0.3.0rc1`
- **THEN** packaged skills declare that exact release candidate version
- **AND** validation uses PEP 440 ordering rather than ad hoc string comparison

### Requirement: Package Catalog Defines Skill Compatibility Floors
The package-owned system-skill catalog SHALL define a minimum compatible skill version for each system-skill group and SHALL allow a per-skill override for a skill that requires a newer floor.

#### Scenario: Group compatibility floor applies by default
- **WHEN** a packaged skill has no per-skill compatibility override
- **THEN** compatibility evaluation uses its group's minimum compatible skill version

#### Scenario: Per-skill compatibility floor overrides the group
- **WHEN** packaged skill metadata declares a minimum compatible version newer than its group default
- **THEN** compatibility evaluation uses the per-skill minimum

### Requirement: Installation Receipts Preserve Skill Versions
The system-skill installer SHALL snapshot each projected skill's release version in the target-root installation receipt and SHALL read legacy receipts without treating their unversioned records as verified.

#### Scenario: Install writes per-skill versions
- **WHEN** `isomer-cli system-skills install` projects selected skills
- **THEN** each tracked receipt record includes the skill name, source path, projection mode, and skill version read from packaged `agents/openai.yaml`

#### Scenario: Legacy receipt remains inspectable
- **WHEN** status or detection reads a supported legacy receipt without per-skill versions
- **THEN** it preserves the receipt as legacy evidence
- **AND** it reports affected skills as unversioned rather than inventing versions from the receipt package version

#### Scenario: Receipt and projected metadata disagree
- **WHEN** a tracked receipt version differs from the projected skill's `agents/openai.yaml` version
- **THEN** status reports receipt drift
- **AND** the installation is not reported as compatibility-verified

### Requirement: Status Classifies Skill Version Compatibility
System-skill status SHALL compare installed skill versions with the current CLI version and package-owned minimum compatibility floors using PEP 440 semantics.

#### Scenario: Compatible older skill is usable
- **WHEN** an installed skill version is at least its minimum compatible version and lower than the current CLI version
- **THEN** status reports `compatible_older`
- **AND** it may advise upgrade without classifying the skill as incompatible

#### Scenario: Obsolete skill is incompatible
- **WHEN** an installed skill version is lower than its minimum compatible version
- **THEN** status reports `obsolete_incompatible`
- **AND** it advises upgrading the target's system skills

#### Scenario: Newer skill has unknown compatibility
- **WHEN** an installed skill version is newer than the current CLI version
- **THEN** status reports `newer_than_cli`
- **AND** it advises upgrading the CLI instead of claiming compatibility

#### Scenario: Missing or malformed version is not verified
- **WHEN** projected `agents/openai.yaml` lacks `metadata.version` or contains an invalid PEP 440 version
- **THEN** status reports `unversioned` or `malformed_version`
- **AND** it does not claim compatibility
